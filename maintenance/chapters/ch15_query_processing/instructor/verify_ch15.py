from __future__ import annotations

import sqlite3
from pathlib import Path


CHAPTER_DIR = Path(__file__).resolve().parents[1]
LAB_PATH = CHAPTER_DIR / "student_lab.sql"
PHASE_2 = "-- === PHASE 2: ADD SELECTION AND JOIN ACCESS PATHS ==="

SELECTION = """
SELECT course_id, title
FROM ch15_course
WHERE title = 'Course 04999'
"""

JOIN = """
SELECT c.course_id, c.title
FROM ch15_department AS d
JOIN ch15_course AS c ON c.dept_id = d.dept_id
WHERE d.dept_name = 'Department 042'
"""


def plan(connection: sqlite3.Connection, query: str) -> list[str]:
    return [row[3] for row in connection.execute("EXPLAIN QUERY PLAN " + query)]


def main() -> None:
    script = LAB_PATH.read_text(encoding="utf-8")
    assert script.count(PHASE_2) == 1
    phase_1, phase_2 = script.split(PHASE_2)

    connection = sqlite3.connect(":memory:")
    connection.executescript(phase_1)
    assert connection.execute("PRAGMA automatic_index").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM ch15_department").fetchone()[0] == 100
    assert connection.execute("SELECT COUNT(*) FROM ch15_course").fetchone()[0] == 5000
    assert connection.execute(
        "SELECT COUNT(*) FROM ch15_course WHERE credits=3"
    ).fetchone()[0] == 1000

    selection_before = plan(connection, SELECTION)
    assert any("SCAN ch15_course" in item for item in selection_before), selection_before
    join_before = plan(connection, JOIN)
    assert not any("ch15_idx_" in item for item in join_before), join_before
    result_before = connection.execute(JOIN).fetchall()
    assert len(result_before) == 50

    connection.executescript(phase_2)
    selection_after = plan(connection, SELECTION)
    assert any(
        "SEARCH ch15_course" in item
        and "ch15_idx_course_title" in item
        and "title=?" in item
        for item in selection_after
    ), selection_after
    assert connection.execute(SELECTION).fetchall() == [("C04999", "Course 04999")]

    join_after = plan(connection, JOIN)
    assert any(
        "SEARCH d" in item and "ch15_idx_department_name" in item
        for item in join_after
    ), join_after
    assert any(
        "SEARCH c" in item and "ch15_idx_course_dept" in item
        for item in join_after
    ), join_after
    result_after = connection.execute(JOIN).fetchall()
    assert result_after == result_before

    ordered_plan = plan(connection, JOIN + " ORDER BY c.title")
    assert any("TEMP B-TREE FOR ORDER BY" in item for item in ordered_plan), ordered_plan
    assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
    connection.close()

    print(f"SQLite {sqlite3.sqlite_version}")
    print("PASS deterministic department/course workload")
    print("PASS selection scan before and index search after")
    print("PASS join result equality across physical designs")
    print("PASS indexed department-to-course join plan")
    print("PASS temporary ORDER BY work observed")
    print("PASS complete lab and foreign-key check")


if __name__ == "__main__":
    main()
