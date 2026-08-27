"""Verify Chapter 17 transaction materials in a clean temporary directory."""

from __future__ import annotations

import importlib.util
import json
import sqlite3
import tempfile
from pathlib import Path


CHAPTER = Path(__file__).resolve().parents[1]


def load_analyzer():
    module_path = CHAPTER / "schedule_analyzer.py"
    spec = importlib.util.spec_from_file_location("schedule_analyzer", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load schedule_analyzer.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def setup_accounts(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        PRAGMA foreign_keys = ON;
        CREATE TABLE account (
            account_id TEXT PRIMARY KEY,
            balance INTEGER NOT NULL CHECK (balance >= 0)
        );
        CREATE TABLE transfer_log (
            transfer_id INTEGER PRIMARY KEY,
            from_account TEXT NOT NULL REFERENCES account(account_id),
            to_account TEXT NOT NULL REFERENCES account(account_id),
            amount INTEGER NOT NULL CHECK (amount > 0),
            status TEXT NOT NULL CHECK (status IN ('COMMITTED'))
        );
        INSERT INTO account(account_id, balance)
        VALUES ('A', 1000), ('B', 2000);
        """
    )


def balances(connection: sqlite3.Connection) -> list[tuple[str, int]]:
    return connection.execute(
        "SELECT account_id, balance FROM account ORDER BY account_id"
    ).fetchall()


def verify_transactions(database_path: Path) -> None:
    connection = sqlite3.connect(database_path)
    setup_accounts(connection)
    connection.commit()

    connection.execute("BEGIN")
    connection.execute(
        "UPDATE account SET balance = balance - 50 WHERE account_id = 'A'"
    )
    assert balances(connection) == [("A", 950), ("B", 2000)]
    connection.rollback()
    assert balances(connection) == [("A", 1000), ("B", 2000)]
    print("PASS rollback removes the partial transfer")

    connection.execute("BEGIN IMMEDIATE")
    debit = connection.execute(
        """
        UPDATE account
        SET balance = balance - 50
        WHERE account_id = 'A' AND balance >= 50
        """
    )
    assert debit.rowcount == 1
    credit = connection.execute(
        "UPDATE account SET balance = balance + 50 WHERE account_id = 'B'"
    )
    assert credit.rowcount == 1
    connection.execute(
        """
        INSERT INTO transfer_log(from_account, to_account, amount, status)
        VALUES ('A', 'B', 50, 'COMMITTED')
        """
    )
    connection.commit()
    assert balances(connection) == [("A", 950), ("B", 2050)]
    assert connection.execute("SELECT SUM(balance) FROM account").fetchone()[0] == 3000
    assert connection.execute("SELECT COUNT(*) FROM transfer_log").fetchone()[0] == 1
    print("PASS committed transfer preserves balances, total, and log")

    connection.close()
    reopened = sqlite3.connect(database_path)
    assert balances(reopened) == [("A", 950), ("B", 2050)]
    assert reopened.execute("PRAGMA foreign_key_check").fetchall() == []
    reopened.close()
    print("PASS committed result remains after close and reopen")


def executable_sql(script: str) -> str:
    return "\n".join(
        line for line in script.splitlines() if not line.lstrip().startswith(".")
    )


def verify_complete_lab(temp_directory: Path) -> None:
    lab_path = CHAPTER / "student_lab.sql"
    database_path = temp_directory / "complete_lab.db"
    connection = sqlite3.connect(database_path)
    connection.executescript(executable_sql(lab_path.read_text(encoding="utf-8")))
    assert balances(connection) == [("A", 950), ("B", 2050)]
    assert connection.execute("SELECT SUM(balance) FROM account").fetchone()[0] == 3000
    assert connection.execute("SELECT COUNT(*) FROM transfer_log").fetchone()[0] == 1
    assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
    connection.close()
    print("PASS complete student_lab.sql and foreign-key check")


def verify_schedules() -> None:
    analyzer = load_analyzer()
    schedules = json.loads(
        (CHAPTER / "schedule_examples.json").read_text(encoding="utf-8")
    )
    expected = {
        "acyclic": (True, ["T1", "T2"], True, True),
        "cycle": (False, None, True, True),
        "recoverable_but_not_cascadeless": (True, ["T1", "T2"], True, False),
        "nonrecoverable": (True, ["T1", "T2"], False, False),
        "cascadeless": (True, ["T1", "T2"], True, True),
    }
    for name, values in expected.items():
        result = analyzer.analyze(schedules[name])
        observed = (
            result["conflict_serializable"],
            result["serial_order"],
            result["recoverable"],
            result["cascadeless"],
        )
        assert observed == values, (name, observed, values)
    assert analyzer.analyze(schedules["acyclic"])["edges"] == ["T1->T2"]
    assert analyzer.analyze(schedules["cycle"])["edges"] == [
        "T1->T2",
        "T2->T1",
    ]
    print("PASS five schedule classifications and precedence edges")


def main() -> None:
    print(f"SQLite {sqlite3.sqlite_version}")
    with tempfile.TemporaryDirectory(prefix="ch17_verify_") as temporary:
        temp_directory = Path(temporary)
        verify_transactions(temp_directory / "transactions.db")
        verify_complete_lab(temp_directory)
    verify_schedules()


if __name__ == "__main__":
    main()
