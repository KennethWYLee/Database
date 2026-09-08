from pathlib import Path
import sqlite3
import sys


CHAPTER_DIR = Path(__file__).resolve().parents[1]
SETUP_SQL = CHAPTER_DIR / "course_registration_setup.sql"
STUDENT_LAB_SQL = CHAPTER_DIR / "student_lab.sql"
sys.path.insert(0, str(CHAPTER_DIR.parents[1] / "course_repository"))
from build_course_repository import load_sql_examples


def fetchall(connection: sqlite3.Connection, query: str):
    return connection.execute(query).fetchall()


def expect_integrity_error(connection: sqlite3.Connection, statement: str,
                           error_code: int | None = None) -> None:
    connection.execute("SAVEPOINT constraint_test")
    try:
        connection.execute(statement)
    except sqlite3.IntegrityError as error:
        if error_code is not None:
            assert error.sqlite_errorcode == error_code, (statement, str(error))
    else:
        raise AssertionError(f"Expected an integrity error: {statement}")
    finally:
        connection.execute("ROLLBACK TO constraint_test")
        connection.execute("RELEASE constraint_test")


def verify_null_keys(connection):
    inserts = [
        "INSERT INTO department VALUES (NULL, 'New Department', 'Hong Hall')",
        "INSERT INTO student VALUES (NULL, 'missing@example.edu', 'New Student', 'IM')",
        "INSERT INTO course VALUES (NULL, 'New Course', 'IM', 3)",
        "INSERT INTO enrollment VALUES (NULL, 'DB201', '115-2', NULL)",
        "INSERT INTO enrollment VALUES ('S101', NULL, '115-2', NULL)",
        "INSERT INTO enrollment VALUES ('S101', 'DB201', NULL, NULL)",
    ]
    for statement in inserts:
        expect_integrity_error(connection, statement, sqlite3.SQLITE_CONSTRAINT_NOTNULL)
    for table, columns in {
        "department": ["dept_code"], "student": ["student_id"],
        "course": ["course_id"], "enrollment": ["student_id", "course_id", "term"],
    }.items():
        for column in columns:
            expect_integrity_error(connection, f"UPDATE {table} SET {column} = NULL",
                                   sqlite3.SQLITE_CONSTRAINT_NOTNULL)


def verify_maintained_examples(connection):
    examples = load_sql_examples(STUDENT_LAB_SQL.read_text(encoding="utf-8"))
    assert set(examples) == {"1", "2", "3", "4", "5", "6", "7a", "7b", "7c", "8", "9", "10a", "10b"}
    results = {key: fetchall(connection, sql) for key, sql in examples.items()}
    assert [row[0] for row in results["1"]] == ["S101", "S102", "S103", "S104"]
    assert [row[0] for row in results["2"]] == ["S101", "S103"]
    assert results["3"] == [("DES",), ("FIN",), ("IM",)]
    assert results["4"] == [("An Chen",), ("Kai Wu",)]
    assert len(results["5"]) == 4 and len(results["6"]) == 6
    assert results["7a"] == [("S101",), ("S102",), ("S103",)]
    assert results["7b"] == results["8"] == [("S101",)]
    assert results["7c"] == [("S103",)]
    assert results["9"] == [("An Chen", "Kai Wu", "IM")]
    assert results["10a"] == results["10b"]

    connection.execute("SAVEPOINT changed_data")
    try:
        connection.execute("INSERT INTO student VALUES ('S106', 'second.an@example.edu', 'An Chen', 'IM')")
        assert fetchall(connection, examples["4"]) == [("An Chen",), ("Kai Wu",)]
        assert fetchall(connection, "SELECT student_name FROM student WHERE dept_code='IM' ORDER BY student_name") == [
            ("An Chen",), ("An Chen",), ("Kai Wu",)]
        connection.execute("INSERT INTO enrollment VALUES ('S101', 'DB201', '115-2', NULL)")
        assert fetchall(connection, "SELECT term FROM enrollment WHERE student_id='S101' AND course_id='DB201' ORDER BY term") == [
            ("115-1",), ("115-2",)]
        expect_integrity_error(connection,
            "INSERT INTO enrollment VALUES ('S101', 'DB201', '115-2', NULL)",
            sqlite3.SQLITE_CONSTRAINT_PRIMARYKEY)
        for pair in ["student_id, course_id", "student_id, term", "course_id, term"]:
            assert fetchall(connection, f"SELECT {pair} FROM enrollment GROUP BY {pair} HAVING COUNT(*) > 1")
    finally:
        connection.execute("ROLLBACK TO changed_data")
        connection.execute("RELEASE changed_data")
    assert fetchall(connection, "SELECT COUNT(*) FROM student") == [(4,)]
    assert fetchall(connection, "SELECT COUNT(*) FROM enrollment") == [(6,)]


def verify_credit_domain(connection):
    for value in ("0", "7", "2.5", "'unknown'"):
        expect_integrity_error(connection,
            f"INSERT INTO course VALUES ('TEST', 'Domain Test', 'IM', {value})",
            sqlite3.SQLITE_CONSTRAINT_CHECK)
        expect_integrity_error(connection,
            f"UPDATE course SET credits = {value} WHERE course_id = 'DB201'",
            sqlite3.SQLITE_CONSTRAINT_CHECK)
    for value in ("1", "6", "'4'", "4.0"):
        connection.execute("SAVEPOINT valid_credit")
        try:
            connection.execute(f"UPDATE course SET credits = {value} WHERE course_id = 'DB201'")
            actual, storage = connection.execute(
                "SELECT credits, typeof(credits) FROM course WHERE course_id = 'DB201'"
            ).fetchone()
            assert storage == "integer" and 1 <= actual <= 6
        finally:
            connection.execute("ROLLBACK TO valid_credit")
            connection.execute("RELEASE valid_credit")


def main() -> None:
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SETUP_SQL.read_text(encoding="utf-8"))

    assert fetchall(connection, "SELECT COUNT(*) FROM department") == [(3,)]
    assert fetchall(connection, "SELECT COUNT(*) FROM student") == [(4,)]
    assert fetchall(connection, "SELECT COUNT(*) FROM course") == [(4,)]
    assert fetchall(connection, "SELECT COUNT(*) FROM enrollment") == [(6,)]

    verify_null_keys(connection)
    verify_credit_domain(connection)
    verify_maintained_examples(connection)

    expect_integrity_error(
        connection,
        "INSERT INTO student VALUES "
        "('S101', 'new@example.edu', 'Duplicate ID', 'IM')",
    )
    expect_integrity_error(
        connection,
        "INSERT INTO student VALUES "
        "('S105', 'an.chen@example.edu', 'Duplicate Email', 'IM')",
    )
    expect_integrity_error(
        connection,
        "INSERT INTO student VALUES "
        "('S105', 'new@example.edu', 'Invalid Department', 'LAW')",
    )
    expect_integrity_error(
        connection,
        "INSERT INTO enrollment VALUES ('S101', 'DB201', '115-1', 'A')",
    )

    selection = fetchall(
        connection,
        "SELECT student_id FROM student WHERE dept_code = 'IM' ORDER BY student_id",
    )
    assert selection == [("S101",), ("S103",)]

    projection = fetchall(
        connection,
        "SELECT DISTINCT dept_code FROM student ORDER BY dept_code",
    )
    assert projection == [("DES",), ("FIN",), ("IM",)]

    cartesian_product = fetchall(
        connection,
        """
        WITH selected_students AS (
            SELECT student_id FROM student WHERE student_id IN ('S101', 'S102')
        ), selected_courses AS (
            SELECT course_id FROM course WHERE course_id IN ('DB201', 'FT210')
        )
        SELECT selected_students.student_id, selected_courses.course_id
        FROM selected_students CROSS JOIN selected_courses
        ORDER BY selected_students.student_id, selected_courses.course_id
        """,
    )
    assert cartesian_product == [
        ("S101", "DB201"),
        ("S101", "FT210"),
        ("S102", "DB201"),
        ("S102", "FT210"),
    ]

    joined = fetchall(
        connection,
        """
        SELECT student.student_name, enrollment.course_id, enrollment.term
        FROM student
        JOIN enrollment ON student.student_id = enrollment.student_id
        ORDER BY student.student_id, enrollment.course_id
        """,
    )
    assert joined == [
        ("An Chen", "DB201", "115-1"),
        ("An Chen", "FT210", "115-1"),
        ("Bea Lin", "FT210", "115-1"),
        ("Kai Wu", "DB201", "115-1"),
        ("Kai Wu", "ML230", "115-1"),
        ("Mira Ho", "WD120", "115-1"),
    ]

    union_result = fetchall(
        connection,
        """
        SELECT student_id FROM enrollment WHERE course_id = 'DB201'
        UNION
        SELECT student_id FROM enrollment WHERE course_id = 'FT210'
        ORDER BY student_id
        """,
    )
    assert union_result == [("S101",), ("S102",), ("S103",)]

    intersection_result = fetchall(
        connection,
        """
        SELECT student_id FROM enrollment WHERE course_id = 'DB201'
        INTERSECT
        SELECT student_id FROM enrollment WHERE course_id = 'FT210'
        ORDER BY student_id
        """,
    )
    assert intersection_result == [("S101",)]

    difference_result = fetchall(
        connection,
        """
        SELECT student_id FROM enrollment WHERE course_id = 'DB201'
        EXCEPT
        SELECT student_id FROM enrollment WHERE course_id = 'FT210'
        ORDER BY student_id
        """,
    )
    assert difference_result == [("S103",)]

    renamed = fetchall(
        connection,
        """
        SELECT s1.student_name, s2.student_name, s1.dept_code
        FROM student AS s1 CROSS JOIN student AS s2
        WHERE s1.dept_code = s2.dept_code
          AND s1.student_id < s2.student_id
        ORDER BY s1.student_id, s2.student_id
        """,
    )
    assert renamed == [("An Chen", "Kai Wu", "IM")]

    filter_after_join = fetchall(
        connection,
        """
        SELECT student.student_name, enrollment.course_id
        FROM student
        JOIN enrollment ON student.student_id = enrollment.student_id
        WHERE student.dept_code = 'IM'
        ORDER BY student.student_id, enrollment.course_id
        """,
    )
    filter_before_join = fetchall(
        connection,
        """
        WITH im_students AS (
            SELECT student_id, student_name FROM student WHERE dept_code = 'IM'
        )
        SELECT im_students.student_name, enrollment.course_id
        FROM im_students
        JOIN enrollment ON im_students.student_id = enrollment.student_id
        ORDER BY im_students.student_id, enrollment.course_id
        """,
    )
    assert filter_after_join == filter_before_join
    assert filter_after_join == [
        ("An Chen", "DB201"),
        ("An Chen", "FT210"),
        ("Kai Wu", "DB201"),
        ("Kai Wu", "ML230"),
    ]

    foreign_key_violations = fetchall(connection, "PRAGMA foreign_key_check")
    assert foreign_key_violations == []

    lab_connection = sqlite3.connect(":memory:")
    lab_connection.execute("PRAGMA foreign_keys = ON")
    lab_connection.executescript(SETUP_SQL.read_text(encoding="utf-8"))
    lab_connection.executescript(STUDENT_LAB_SQL.read_text(encoding="utf-8"))

    print(f"SQLite version: {sqlite3.sqlite_version}")
    print("PASS: schema and row counts")
    print("PASS: primary, candidate, composite, and foreign-key constraints")
    print("PASS: selection, projection, composition, product, and join examples")
    print("PASS: union, intersection, difference, assignment, and rename examples")
    print("PASS: equivalent-query results")
    print("PASS: no foreign-key violations")
    print("PASS: complete student_lab.sql execution")
    print("PASS: all six primary-key columns reject NULL on insert and update")
    print("PASS: actual maintained projection handles same-name students")
    print("PASS: cross-term enrollment and all three composite-key minimality counterexamples")
    print("PASS: credits reject fractional/out-of-range/non-numeric values on insert and update")
    print("PASS: credits preserve integer-affinity conversion and valid boundary values")
    lab_connection.close()
    connection.close()


if __name__ == "__main__":
    main()
