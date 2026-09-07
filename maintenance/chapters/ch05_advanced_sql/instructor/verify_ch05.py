from pathlib import Path
import sqlite3


CHAPTER_DIR = Path(__file__).resolve().parents[1]
CH02_DIR = CHAPTER_DIR.parent / "ch02_relational_model"
SETUP_SQL = CH02_DIR / "course_registration_setup.sql"
STUDENT_LAB_SQL = CHAPTER_DIR / "student_lab.sql"


def rows(connection: sqlite3.Connection, query: str):
    return connection.execute(query).fetchall()


def main() -> None:
    connection = sqlite3.connect(":memory:", isolation_level=None)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SETUP_SQL.read_text(encoding="utf-8"))
    connection.executescript(STUDENT_LAB_SQL.read_text(encoding="utf-8"))

    routine_body_results = rows(
        connection,
        """
        SELECT c.course_id,
               (SELECT COUNT(*) FROM enrollment AS e
                WHERE e.course_id = c.course_id)
        FROM course AS c
        ORDER BY c.course_id
        """,
    )
    assert routine_body_results == [
        ("DB201", 2),
        ("FT210", 2),
        ("ML230", 1),
        ("WD120", 1),
    ]
    assert rows(
        connection,
        "SELECT credits FROM course WHERE course_id='DB201'",
    ) == [(3,)]

    connection.execute("SAVEPOINT trigger_check")
    connection.execute(
        """
        UPDATE enrollment SET grade='B+'
        WHERE student_id='S103' AND course_id='DB201' AND term='115-1'
        """
    )
    assert rows(
        connection,
        """
        SELECT action_name, student_id, course_id, term, old_grade, new_grade
        FROM enrollment_audit
        """,
    ) == [("GRADE_UPDATE", "S103", "DB201", "115-1", "B", "B+")]
    connection.execute(
        """
        UPDATE enrollment SET grade='B+'
        WHERE student_id='S103' AND course_id='DB201' AND term='115-1'
        """
    )
    assert rows(connection, "SELECT COUNT(*) FROM enrollment_audit") == [(1,)]
    connection.execute("ROLLBACK TO trigger_check")
    connection.execute("RELEASE trigger_check")
    assert rows(connection, "SELECT COUNT(*) FROM enrollment_audit") == [(0,)]
    assert rows(
        connection,
        """
        SELECT grade FROM enrollment
        WHERE student_id='S103' AND course_id='DB201' AND term='115-1'
        """,
    ) == [("B",)]

    closure = rows(
        connection,
        """
        WITH RECURSIVE all_prereq(course_id, prereq_id) AS (
            SELECT course_id, prereq_id FROM course_prerequisite
            UNION
            SELECT ap.course_id, cp.prereq_id
            FROM all_prereq AS ap
            JOIN course_prerequisite AS cp ON cp.course_id = ap.prereq_id
        )
        SELECT course_id, prereq_id FROM all_prereq
        ORDER BY course_id, prereq_id
        """,
    )
    assert closure == [
        ("DB201", "WD120"),
        ("FT210", "DB201"),
        ("FT210", "WD120"),
        ("ML230", "DB201"),
        ("ML230", "WD120"),
    ]
    ml_path = rows(
        connection,
        """
        WITH RECURSIVE prereq_path(prereq_id, depth) AS (
            SELECT prereq_id, 1 FROM course_prerequisite
            WHERE course_id='ML230'
            UNION ALL
            SELECT cp.prereq_id, pp.depth + 1
            FROM prereq_path AS pp
            JOIN course_prerequisite AS cp ON cp.course_id=pp.prereq_id
        )
        SELECT prereq_id, depth FROM prereq_path ORDER BY depth, prereq_id
        """,
    )
    assert ml_path == [("DB201", 1), ("WD120", 2)]

    ranking = rows(
        connection,
        """
        WITH best_score AS (
            SELECT student_id, MAX(score) AS best_score
            FROM sql_practice_score GROUP BY student_id
        )
        SELECT student_id, best_score,
               RANK() OVER (ORDER BY best_score DESC),
               DENSE_RANK() OVER (ORDER BY best_score DESC),
               ROW_NUMBER() OVER (ORDER BY best_score DESC, student_id)
        FROM best_score
        ORDER BY best_score DESC, student_id
        """,
    )
    assert ranking == [
        ("S101", 92, 1, 1, 1),
        ("S102", 92, 1, 1, 2),
        ("S103", 84, 3, 2, 3),
        ("S104", 84, 3, 2, 4),
    ]

    running = rows(
        connection,
        """
        SELECT student_id, attempt_no,
               ROUND(AVG(score) OVER (
                   PARTITION BY student_id ORDER BY attempt_no
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
               ), 1)
        FROM sql_practice_score
        ORDER BY student_id, attempt_no
        """,
    )
    assert running == [
        ("S101", 1, 78.0),
        ("S101", 2, 85.0),
        ("S102", 1, 92.0),
        ("S103", 1, 84.0),
        ("S104", 1, 70.0),
        ("S104", 2, 77.0),
    ]

    pivot = rows(
        connection,
        """
        SELECT student_id,
               MAX(CASE WHEN attempt_no=1 THEN score END),
               MAX(CASE WHEN attempt_no=2 THEN score END)
        FROM sql_practice_score
        GROUP BY student_id
        ORDER BY student_id
        """,
    )
    assert pivot == [
        ("S101", 78, 92),
        ("S102", 92, None),
        ("S103", 84, None),
        ("S104", 70, 84),
    ]

    assert rows(connection, "SELECT COUNT(*) FROM student") == [(4,)]
    assert rows(connection, "SELECT COUNT(*) FROM enrollment") == [(6,)]
    assert rows(connection, "PRAGMA foreign_key_check") == []

    print(f"SQLite version: {sqlite3.sqlite_version}")
    print("PASS: stored-routine body results and reversible procedure-body example")
    print("PASS: OLD/NEW audit trigger, no-op guard, and transaction rollback")
    print("PASS: recursive transitive closure and target depth")
    print("PASS: RANK, DENSE_RANK, deterministic ROW_NUMBER, and ties")
    print("PASS: partitioned running window and conditional aggregation")
    print("PASS: complete student_lab.sql and foreign-key check")


if __name__ == "__main__":
    main()
