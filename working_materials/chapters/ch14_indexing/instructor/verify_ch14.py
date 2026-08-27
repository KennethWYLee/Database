from __future__ import annotations

import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path


CHAPTER_DIR = Path(__file__).resolve().parents[1]
LAB_PATH = CHAPTER_DIR / "student_lab.sql"
SVG_PATH = CHAPTER_DIR / "bplus_tree_example.svg"
PNG_PATH = CHAPTER_DIR / "bplus_tree_example.png"

PHASE_2 = "-- === PHASE 2: COMPOSITE INDEX ==="
PHASE_3 = "-- === PHASE 3: COVERING INDEX ==="

QUERY = """
SELECT ordered_at, amount
FROM ch14_order_line
WHERE customer_id = 'C0042'
  AND ordered_at BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY ordered_at
"""


def plan_details(connection: sqlite3.Connection, query: str) -> list[str]:
    return [row[3] for row in connection.execute("EXPLAIN QUERY PLAN " + query)]


def main() -> None:
    script = LAB_PATH.read_text(encoding="utf-8")
    assert script.count(PHASE_2) == 1
    assert script.count(PHASE_3) == 1
    phase_1, remainder = script.split(PHASE_2)
    phase_2, phase_3 = remainder.split(PHASE_3)

    connection = sqlite3.connect(":memory:")
    connection.executescript(phase_1)
    assert connection.execute("SELECT COUNT(*) FROM ch14_order_line").fetchone()[0] == 20000
    assert connection.execute(
        "SELECT COUNT(DISTINCT customer_id) FROM ch14_order_line"
    ).fetchone()[0] == 1000
    no_index_plan = plan_details(connection, QUERY)
    assert any("SCAN ch14_order_line" in item for item in no_index_plan), no_index_plan

    connection.executescript(phase_2)
    composite_plan = plan_details(connection, QUERY)
    assert any(
        "SEARCH ch14_order_line" in item
        and "ch14_idx_customer_date" in item
        and "customer_id=?" in item
        and "ordered_at>?" in item
        and "ordered_at<?" in item
        for item in composite_plan
    ), composite_plan
    result = connection.execute(QUERY).fetchall()
    assert len(result) == 20, len(result)
    assert result == sorted(result, key=lambda row: row[0])

    connection.executescript(phase_3)
    covering_plan = plan_details(connection, QUERY)
    assert any(
        "COVERING INDEX ch14_idx_customer_date_amount" in item
        for item in covering_plan
    ), covering_plan
    status_plan = plan_details(
        connection,
        "SELECT line_id, customer_id, ordered_at, status, amount "
        "FROM ch14_order_line WHERE status = 'COMPLETE'",
    )
    assert any("SCAN ch14_order_line" in item for item in status_plan), status_plan
    assert connection.execute(
        "SELECT COUNT(*) FROM ch14_order_line WHERE status='COMPLETE'"
    ).fetchone()[0] == 16000
    connection.close()

    root = ET.parse(SVG_PATH).getroot()
    assert root.tag.endswith("svg")
    assert "1200" == root.attrib.get("width")
    assert "620" == root.attrib.get("height")
    assert PNG_PATH.exists() and PNG_PATH.stat().st_size > 10_000

    print(f"SQLite {sqlite3.sqlite_version}")
    print("PASS deterministic 20,000-row workload")
    print("PASS table scan before secondary index")
    print("PASS composite customer/date index search and row order")
    print("PASS covering-index plan")
    print("PASS low-selectivity status scan")
    print("PASS parseable SVG and rendered PNG")


if __name__ == "__main__":
    main()
