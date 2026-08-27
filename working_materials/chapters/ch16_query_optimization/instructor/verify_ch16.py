from __future__ import annotations

import sqlite3
from pathlib import Path


CHAPTER_DIR = Path(__file__).resolve().parents[1]
LAB_PATH = CHAPTER_DIR / "student_lab.sql"

BASE_QUERY = """
SELECT s.student_id, c.course_id
FROM ch16_student AS s
JOIN ch16_enrollment AS e ON e.student_id = s.student_id
JOIN ch16_course AS c ON c.course_id = e.course_id
WHERE s.dept_id = 42 AND c.credits = 5
"""

PUSHDOWN_QUERY = """
SELECT s.student_id, c.course_id
FROM (SELECT student_id FROM ch16_student WHERE dept_id = 42) AS s
JOIN ch16_enrollment AS e ON e.student_id = s.student_id
JOIN (SELECT course_id FROM ch16_course WHERE credits = 5) AS c
  ON c.course_id = e.course_id
"""


def plan(connection: sqlite3.Connection, query: str) -> list[str]:
    return [row[3] for row in connection.execute("EXPLAIN QUERY PLAN " + query)]


def index_sequence(details: list[str]) -> list[str]:
    expected = [
        "ch16_idx_student_dept",
        "sqlite_autoindex_ch16_enrollment_1",
        "ch16_idx_course_credits",
    ]
    return [name for item in details for name in expected if name in item]


def main() -> None:
    connection = sqlite3.connect(":memory:")
    connection.executescript(LAB_PATH.read_text(encoding="utf-8"))

    assert connection.execute("PRAGMA automatic_index").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM ch16_department").fetchone()[0] == 101
    assert connection.execute("SELECT COUNT(*) FROM ch16_student").fetchone()[0] == 10000
    assert connection.execute("SELECT COUNT(*) FROM ch16_course").fetchone()[0] == 500
    assert connection.execute("SELECT COUNT(*) FROM ch16_enrollment").fetchone()[0] == 50000

    base_rows = connection.execute(BASE_QUERY).fetchall()
    pushed_rows = connection.execute(PUSHDOWN_QUERY).fetchall()
    assert base_rows == pushed_rows
    assert len(base_rows) == 100, len(base_rows)
    base_plan = plan(connection, BASE_QUERY)
    pushed_plan = plan(connection, PUSHDOWN_QUERY)
    assert index_sequence(base_plan) == index_sequence(pushed_plan), (
        base_plan,
        pushed_plan,
    )
    assert any("ch16_idx_student_dept" in item for item in base_plan), base_plan
    assert any("sqlite_autoindex_ch16_enrollment_1" in item for item in base_plan), base_plan

    where_filter = connection.execute(
        """
        SELECT d.dept_id, s.student_id
        FROM ch16_department AS d
        LEFT JOIN ch16_student AS s ON s.dept_id = d.dept_id
        WHERE s.student_id < 3
        ORDER BY d.dept_id, s.student_id
        """
    ).fetchall()
    on_filter = connection.execute(
        """
        SELECT d.dept_id, s.student_id
        FROM ch16_department AS d
        LEFT JOIN ch16_student AS s
          ON s.dept_id = d.dept_id AND s.student_id < 3
        WHERE d.dept_id IN (1, 2, 101)
        ORDER BY d.dept_id, s.student_id
        """
    ).fetchall()
    assert where_filter == [(1, 1), (2, 2)], where_filter
    assert on_filter == [(1, 1), (2, 2), (101, None)], on_filter

    event_stats = connection.execute(
        "SELECT stat FROM sqlite_stat1 WHERE idx='ch16_idx_event_type'"
    ).fetchone()
    assert event_stats is not None
    assert event_stats[0].split()[:2] == ["10000", "5000"], event_stats
    counts = connection.execute(
        "SELECT event_type, COUNT(*) FROM ch16_event GROUP BY event_type ORDER BY event_type"
    ).fetchall()
    assert counts == [("COMMON", 9900), ("RARE", 100)], counts

    rare_plan = plan(
        connection,
        "SELECT event_id, event_type, amount FROM ch16_event WHERE event_type='RARE'",
    )
    common_plan = plan(
        connection,
        "SELECT event_id, event_type, amount FROM ch16_event WHERE event_type='COMMON'",
    )
    assert all(isinstance(item, str) and item for item in rare_plan + common_plan)
    assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
    connection.close()

    print(f"SQLite {sqlite3.sqlite_version}")
    print("PASS deterministic four-relation workload")
    print("PASS equivalent base/pushdown results and flattened plans")
    print("PASS selected join access paths")
    print("PASS outer-join WHERE/ON counterexample")
    print("PASS sqlite_stat1 average and skewed actual counts")
    print("PASS RARE/COMMON plans captured without overclaim")
    print("PASS complete lab and foreign-key check")


if __name__ == "__main__":
    main()
