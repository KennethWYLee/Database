from __future__ import annotations

import argparse
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Callable


PACKAGE_ROOT = Path(__file__).resolve().parent
MATERIALS = PACKAGE_ROOT / "materials"
DATABASES = PACKAGE_ROOT / "databases"
MIN_SQLITE = (3, 39, 0)
CHAPTERS = ("ch02", "ch03", "ch04", "ch05", "ch06", "ch07", "ch14", "ch15", "ch16", "ch17")


def fail(message: str) -> None:
    raise RuntimeError(message)


def scalar(connection: sqlite3.Connection, query: str):
    row = connection.execute(query).fetchone()
    if row is None:
        fail(f"Query returned no row: {query}")
    return row[0]


def expect(actual, expected, label: str) -> None:
    if actual != expected:
        fail(f"{label}: expected {expected!r}, received {actual!r}")


def load_sql(path: Path) -> str:
    output: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith(".print"):
            message = stripped[len(".print") :].strip()
            if len(message) >= 2 and message[0] == message[-1] and message[0] in "\"'":
                message = message[1:-1]
            print(f"  {message}")
            continue
        output.append(line)
    return "\n".join(output) + "\n"


def execute_file(connection: sqlite3.Connection, relative_path: str) -> None:
    path = PACKAGE_ROOT / relative_path
    if not path.is_file():
        fail(f"Missing package file: {relative_path}")
    print(f"  RUN {relative_path}")
    connection.executescript(load_sql(path))


def fresh_connection(database_name: str) -> sqlite3.Connection:
    DATABASES.mkdir(exist_ok=True)
    database_path = DATABASES / database_name
    if database_path.exists():
        database_path.unlink()
    connection = sqlite3.connect(database_path, isolation_level=None)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def check_foreign_keys(connection: sqlite3.Connection) -> None:
    violations = connection.execute("PRAGMA foreign_key_check").fetchall()
    expect(violations, [], "foreign-key check")


def check_shared(connection: sqlite3.Connection) -> None:
    expect(scalar(connection, "SELECT COUNT(*) FROM department"), 3, "department count")
    expect(scalar(connection, "SELECT COUNT(*) FROM student"), 4, "student count")
    expect(scalar(connection, "SELECT COUNT(*) FROM course"), 4, "course count")
    expect(scalar(connection, "SELECT COUNT(*) FROM enrollment"), 6, "enrollment count")
    check_foreign_keys(connection)


def run_shared(selected: list[str]) -> None:
    connection = fresh_connection("course_registration.db")
    try:
        execute_file(connection, "materials/ch02/course_registration_setup.sql")
        for chapter in ("ch02", "ch03", "ch04", "ch05"):
            if chapter in selected:
                execute_file(connection, f"materials/{chapter}/student_lab.sql")
                check_shared(connection)
                print(f"PASS {chapter}")
    finally:
        connection.close()


def check_ch06(connection: sqlite3.Connection) -> None:
    expected_counts = {
        "department": 2,
        "student": 3,
        "student_phone": 3,
        "course": 3,
        "section": 3,
        "enrollment": 5,
    }
    for table, count in expected_counts.items():
        expect(scalar(connection, f"SELECT COUNT(*) FROM {table}"), count, f"{table} count")
    check_foreign_keys(connection)


def check_ch07(connection: sqlite3.Connection) -> None:
    expect(scalar(connection, "SELECT COUNT(*) FROM ch07_course_enrollment_record"), 4, "flat row count")
    lossy_count = scalar(
        connection,
        """
        SELECT COUNT(*)
        FROM ch07_employee_identity AS i
        JOIN ch07_employee_details AS d USING (name)
        """,
    )
    expect(lossy_count, 4, "lossy join row count")
    check_foreign_keys(connection)


def check_ch14(connection: sqlite3.Connection) -> None:
    expect(scalar(connection, "SELECT COUNT(*) FROM ch14_order_line"), 20000, "order-line count")
    expect(
        scalar(connection, "SELECT COUNT(*) FROM ch14_order_line WHERE status='COMPLETE'"),
        16000,
        "COMPLETE row count",
    )


def check_ch15(connection: sqlite3.Connection) -> None:
    expect(scalar(connection, "SELECT COUNT(*) FROM ch15_department"), 100, "department count")
    expect(scalar(connection, "SELECT COUNT(*) FROM ch15_course"), 5000, "course count")
    check_foreign_keys(connection)


def check_ch16(connection: sqlite3.Connection) -> None:
    expected_counts = {
        "ch16_department": 101,
        "ch16_student": 10000,
        "ch16_course": 500,
        "ch16_enrollment": 50000,
        "ch16_event": 10000,
    }
    for table, count in expected_counts.items():
        expect(scalar(connection, f"SELECT COUNT(*) FROM {table}"), count, f"{table} count")
    expect(scalar(connection, "SELECT COUNT(*) FROM ch16_event WHERE event_type='RARE'"), 100, "RARE count")
    check_foreign_keys(connection)


def check_ch17(connection: sqlite3.Connection) -> None:
    balances = connection.execute(
        "SELECT account_id, balance FROM account ORDER BY account_id"
    ).fetchall()
    expect(balances, [("A", 950), ("B", 2050)], "committed balances")
    expect(scalar(connection, "SELECT SUM(balance) FROM account"), 3000, "total balance")
    expect(scalar(connection, "SELECT COUNT(*) FROM transfer_log"), 1, "transfer-log count")
    check_foreign_keys(connection)


def run_ch17_schedule_analyzer() -> None:
    analyzer = MATERIALS / "ch17" / "schedule_analyzer.py"
    schedules = MATERIALS / "ch17" / "schedule_examples.json"
    result = subprocess.run(
        [sys.executable, str(analyzer), str(schedules)],
        cwd=analyzer.parent,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        for line in result.stdout.rstrip().splitlines():
            print(f"  {line}")
    if result.returncode != 0:
        detail = result.stderr.strip() or f"exit code {result.returncode}"
        fail(f"Chapter 17 schedule analyzer failed: {detail}")


SEPARATE_LABS: dict[str, tuple[str, str, Callable[[sqlite3.Connection], None]]] = {
    "ch06": ("ch06_er_design.db", "materials/ch06/mapped_schema.sql", check_ch06),
    "ch07": ("ch07_normalization.db", "materials/ch07/student_lab.sql", check_ch07),
    "ch14": ("ch14_indexing.db", "materials/ch14/student_lab.sql", check_ch14),
    "ch15": ("ch15_query_processing.db", "materials/ch15/student_lab.sql", check_ch15),
    "ch16": ("ch16_query_optimization.db", "materials/ch16/student_lab.sql", check_ch16),
    "ch17": ("ch17_transactions.db", "materials/ch17/student_lab.sql", check_ch17),
}


def run_separate(chapter: str) -> None:
    database_name, script, checker = SEPARATE_LABS[chapter]
    connection = fresh_connection(database_name)
    try:
        execute_file(connection, script)
        checker(connection)
        if chapter == "ch17":
            run_ch17_schedule_analyzer()
        print(f"PASS {chapter}")
    finally:
        connection.close()


def parse_chapters(values: list[str]) -> list[str]:
    if not values or values == ["all"]:
        return list(CHAPTERS)
    if "all" in values:
        fail("Use 'all' by itself, or list individual chapters.")
    unknown = sorted(set(values) - set(CHAPTERS))
    if unknown:
        fail(f"Unknown chapter selection: {', '.join(unknown)}")
    return [chapter for chapter in CHAPTERS if chapter in values]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and verify the course SQLite lab databases.")
    parser.add_argument("chapters", nargs="*", help="all or any of ch02-ch07 and ch14-ch17")
    parser.add_argument("--list", action="store_true", help="list available chapter identifiers")
    args = parser.parse_args()

    if args.list:
        print(" ".join(CHAPTERS))
        return 0
    if sqlite3.sqlite_version_info < MIN_SQLITE:
        fail(
            "SQLite 3.39 or later is required; "
            f"this Python uses SQLite {sqlite3.sqlite_version}."
        )

    selected = parse_chapters(args.chapters)
    print(f"Python {sys.version.split()[0]}; SQLite {sqlite3.sqlite_version}")
    shared = [chapter for chapter in selected if chapter in {"ch02", "ch03", "ch04", "ch05"}]
    if shared:
        run_shared(shared)
    for chapter in selected:
        if chapter in SEPARATE_LABS:
            run_separate(chapter)
    print(f"ALL_SELECTED_LABS_PASSED={len(selected)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, sqlite3.Error) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
