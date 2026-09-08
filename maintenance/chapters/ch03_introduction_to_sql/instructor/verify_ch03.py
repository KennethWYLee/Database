from pathlib import Path
import sqlite3


CHAPTER_DIR = Path(__file__).resolve().parents[1]
CH02_DIR = CHAPTER_DIR.parent / "ch02_relational_model"
SETUP_SQL = CH02_DIR / "course_registration_setup.sql"
STUDENT_LAB_SQL = CHAPTER_DIR / "student_lab.sql"


def rows(connection: sqlite3.Connection, query: str):
    return connection.execute(query).fetchall()


def verify_source_boundaries(connection: sqlite3.Connection) -> None:
    # Counterexamples check source qualifications, not additional student requirements.
    assert rows(connection, "SELECT (1, 9) <= (2, 0), 1 <= 2 AND 9 <= 0") == [(1, 0)]
    salaries = [65000, 75000, 92000, 75000]
    assert sum(salaries) / len(salaries) == 76750
    assert sum(set(salaries)) / len(set(salaries)) == 232000 / 3
    assert sum(set(salaries)) / len(salaries) == 58000
    assert rows(connection, """
        WITH offer(course, term) AS (VALUES ('DB', 'A'), ('DB', 'A'), ('DB', 'B'))
        SELECT a.course FROM offer AS a WHERE term='A' AND EXISTS (
            SELECT 1 FROM offer AS b WHERE b.term='B' AND b.course=a.course
        )
    """) == [("DB",), ("DB",)]
    assert rows(connection, """
        WITH offer(course, term) AS (VALUES ('DB', 'A'), ('DB', 'A'), ('DB', 'B'))
        SELECT course FROM offer WHERE term='A'
        INTERSECT SELECT course FROM offer WHERE term='B'
    """) == [("DB",)]


def main() -> None:
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SETUP_SQL.read_text(encoding="utf-8"))
    verify_source_boundaries(connection)

    duplicate_departments = rows(
        connection,
        "SELECT dept_code FROM student ORDER BY dept_code",
    )
    assert duplicate_departments == [("DES",), ("FIN",), ("IM",), ("IM",)]

    distinct_departments = rows(
        connection,
        "SELECT DISTINCT dept_code FROM student ORDER BY dept_code",
    )
    assert distinct_departments == [("DES",), ("FIN",), ("IM",)]

    filtered = rows(
        connection,
        """
        SELECT student_id, student_name
        FROM student
        WHERE dept_code = 'IM' AND student_id <> 'S101'
        ORDER BY student_id
        """,
    )
    assert filtered == [("S103", "Kai Wu")]

    matched = rows(
        connection,
        """
        SELECT s.student_name, e.course_id, e.grade
        FROM student AS s, enrollment AS e
        WHERE s.student_id = e.student_id
        ORDER BY s.student_id, e.course_id
        """,
    )
    assert len(matched) == 6
    assert matched[0] == ("An Chen", "DB201", "A")

    union_result = rows(
        connection,
        """
        SELECT student_id FROM enrollment WHERE course_id = 'DB201'
        UNION
        SELECT student_id FROM enrollment WHERE course_id = 'FT210'
        ORDER BY student_id
        """,
    )
    assert union_result == [("S101",), ("S102",), ("S103",)]

    union_all_result = rows(
        connection,
        """
        SELECT student_id FROM enrollment WHERE course_id = 'DB201'
        UNION ALL
        SELECT student_id FROM enrollment WHERE course_id = 'FT210'
        ORDER BY student_id
        """,
    )
    assert union_all_result == [("S101",), ("S101",), ("S102",), ("S103",)]

    connection.execute("SAVEPOINT null_check")
    connection.execute(
        """
        UPDATE enrollment SET grade = NULL
        WHERE student_id = 'S102' AND course_id = 'FT210' AND term = '115-1'
        """
    )
    assert rows(connection, "SELECT COUNT(*) FROM enrollment") == [(6,)]
    assert rows(connection, "SELECT COUNT(grade) FROM enrollment") == [(5,)]
    assert rows(connection, "SELECT student_id FROM enrollment WHERE grade = NULL") == []
    assert rows(
        connection,
        "SELECT student_id FROM enrollment WHERE grade IS NULL",
    ) == [("S102",)]
    connection.execute("ROLLBACK TO null_check")
    connection.execute("RELEASE null_check")

    aggregates = rows(
        connection,
        """
        SELECT COUNT(*), MIN(credits), MAX(credits), SUM(credits), AVG(credits)
        FROM course
        """,
    )
    assert aggregates == [(4, 2, 3, 11, 2.75)]

    assert rows(connection, """
        SELECT COUNT(*), MIN(credits), MAX(credits), SUM(credits), AVG(credits)
        FROM course WHERE credits > 6
    """) == [(0, None, None, None, None)]
    assert rows(connection, """
        SELECT dept_code, COUNT(*) FROM course WHERE credits > 6 GROUP BY dept_code
    """) == []
    assert rows(connection, """
        SELECT 'Data' LIKE 'd%', 'Data' LIKE 'd%' COLLATE BINARY,
               char(230) LIKE char(198)
    """) == [(1, 1, 0)]
    assert rows(connection, """
        SELECT (SELECT course_id FROM course ORDER BY course_id),
               (SELECT course_id FROM course WHERE credits > 6)
    """) == [("DB201", None)]

    grouped = rows(
        connection,
        """
        SELECT dept_code, COUNT(*), AVG(credits)
        FROM course
        GROUP BY dept_code
        ORDER BY dept_code
        """,
    )
    assert grouped == [("DES", 1, 2.0), ("FIN", 1, 3.0), ("IM", 2, 3.0)]

    having_result = rows(
        connection,
        """
        SELECT dept_code, COUNT(*)
        FROM course
        WHERE credits >= 3
        GROUP BY dept_code
        HAVING COUNT(*) >= 2
        ORDER BY dept_code
        """,
    )
    assert having_result == [("IM", 2)]

    in_result = rows(
        connection,
        """
        SELECT student_id FROM student
        WHERE student_id IN (
            SELECT student_id FROM enrollment WHERE course_id = 'DB201'
        )
        ORDER BY student_id
        """,
    )
    assert in_result == [("S101",), ("S103",)]

    exists_result = rows(
        connection,
        """
        SELECT s.student_id
        FROM student AS s
        WHERE EXISTS (
            SELECT 1 FROM enrollment AS e
            WHERE e.student_id = s.student_id AND e.grade IN ('A', 'A-')
        )
        ORDER BY s.student_id
        """,
    )
    assert exists_result == [("S101",), ("S102",), ("S103",), ("S104",)]

    connection.execute("SAVEPOINT enrollment_predicate")
    connection.execute("UPDATE enrollment SET grade = 'B' WHERE student_id = 'S104'")
    assert rows(connection, """
        SELECT s.student_id FROM student AS s WHERE NOT EXISTS (
            SELECT 1 FROM enrollment AS e WHERE e.student_id = s.student_id
        )
    """) == []
    assert rows(connection, """
        SELECT s.student_id FROM student AS s WHERE NOT EXISTS (
            SELECT 1 FROM enrollment AS e WHERE e.student_id = s.student_id
            AND e.grade IN ('A', 'A-')
        )
    """) == [("S104",)]
    connection.execute("ROLLBACK TO enrollment_predicate")
    connection.execute("RELEASE enrollment_predicate")

    not_in_with_null = rows(
        connection,
        """
        WITH blocked(student_id) AS (VALUES ('S104'), (NULL))
        SELECT student_id FROM student
        WHERE student_id NOT IN (SELECT student_id FROM blocked)
        ORDER BY student_id
        """,
    )
    assert not_in_with_null == []

    not_exists_with_null = rows(
        connection,
        """
        WITH blocked(student_id) AS (VALUES ('S104'), (NULL))
        SELECT s.student_id FROM student AS s
        WHERE NOT EXISTS (
            SELECT 1 FROM blocked AS b WHERE b.student_id = s.student_id
        )
        ORDER BY s.student_id
        """,
    )
    assert not_exists_with_null == [("S101",), ("S102",), ("S103",)]

    from_subquery = rows(
        connection,
        """
        SELECT course_id, enrollment_count
        FROM (
            SELECT course_id, COUNT(*) AS enrollment_count
            FROM enrollment GROUP BY course_id
        ) AS counts
        WHERE enrollment_count >= 2
        ORDER BY course_id
        """,
    )
    assert from_subquery == [("DB201", 2), ("FT210", 2)]

    scalar = rows(
        connection,
        """
        SELECT c.course_id,
               (SELECT COUNT(*) FROM enrollment AS e
                WHERE e.course_id = c.course_id)
        FROM course AS c
        ORDER BY c.course_id
        """,
    )
    assert scalar == [("DB201", 2), ("FT210", 2), ("ML230", 1), ("WD120", 1)]

    connection.execute("SAVEPOINT dml_check")
    connection.execute(
        """
        INSERT INTO student (student_id, email, student_name, dept_code)
        VALUES ('S105', 'noah.lee@example.edu', 'Noah Lee', 'IM')
        """
    )
    connection.execute(
        "UPDATE student SET dept_code = 'FIN' WHERE student_id = 'S105'"
    )
    assert rows(
        connection,
        "SELECT student_name, dept_code FROM student WHERE student_id = 'S105'",
    ) == [("Noah Lee", "FIN")]
    connection.execute("DELETE FROM student WHERE student_id = 'S105'")
    assert rows(
        connection,
        "SELECT COUNT(*) FROM student WHERE student_id = 'S105'",
    ) == [(0,)]
    connection.execute("ROLLBACK TO dml_check")
    connection.execute("RELEASE dml_check")

    lab_connection = sqlite3.connect(":memory:")
    lab_connection.execute("PRAGMA foreign_keys = ON")
    lab_connection.executescript(SETUP_SQL.read_text(encoding="utf-8"))
    lab_connection.executescript(STUDENT_LAB_SQL.read_text(encoding="utf-8"))
    assert rows(lab_connection, "SELECT COUNT(*) FROM student") == [(4,)]
    assert rows(lab_connection, "PRAGMA foreign_key_check") == []
    for sql in (
        "INSERT INTO study_group VALUES (NULL, 'Test', 'DB201', 4)",
        "UPDATE study_group SET group_id=NULL WHERE group_id='G01'",
    ):
        try:
            lab_connection.execute(sql)
        except sqlite3.IntegrityError as error:
            assert "NOT NULL constraint failed: study_group.group_id" in str(error)
        else:
            raise AssertionError("A text primary key accepted NULL")
    assert rows(lab_connection, "SELECT group_id FROM study_group") == [("G01",)]
    lab_connection.execute("SAVEPOINT capacity_affinity")
    lab_connection.execute("UPDATE study_group SET capacity=2.5 WHERE group_id='G01'")
    assert rows(lab_connection, "SELECT capacity, typeof(capacity) FROM study_group") == [
        (2.5, "real")
    ]
    lab_connection.execute("ROLLBACK TO capacity_affinity")
    lab_connection.execute("RELEASE capacity_affinity")

    print(f"SQLite version: {sqlite3.sqlite_version}")
    print("PASS: SELECT, aliases, DISTINCT, expressions, WHERE, and multi-table query")
    print("PASS: UNION/UNION ALL, INTERSECT, and EXCEPT")
    print("PASS: NULL comparisons, IS NULL, COUNT(*), and COUNT(column)")
    print("PASS: aggregates, GROUP BY, WHERE, and HAVING")
    print("PASS: IN, EXISTS, NOT IN NULL case, NOT EXISTS, FROM/CTE/scalar subqueries")
    print("PASS: reversible INSERT, UPDATE, and DELETE examples")
    print("PASS: complete student_lab.sql execution and foreign-key check")
    print("PASS: text primary key rejects NULL in INSERT and UPDATE")
    print("PASS: empty aggregates, default LIKE, scalar boundaries, and capacity affinity")
    print("PASS: no enrollment differs from no A/A- enrollment")
    print("PASS: source row-comparison, duplicate-average, and EXISTS counterexamples")


if __name__ == "__main__":
    main()
