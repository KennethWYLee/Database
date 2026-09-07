from pathlib import Path
import sqlite3


CHAPTER_DIR = Path(__file__).resolve().parents[1]
SETUP_SQL = CHAPTER_DIR / "course_registration_setup.sql"
STUDENT_LAB_SQL = CHAPTER_DIR / "student_lab.sql"


def fetchall(connection: sqlite3.Connection, query: str):
    return connection.execute(query).fetchall()


def expect_integrity_error(connection: sqlite3.Connection, statement: str) -> None:
    try:
        connection.execute(statement)
    except sqlite3.IntegrityError:
        connection.rollback()
        connection.execute("PRAGMA foreign_keys = ON")
        return
    raise AssertionError(f"Expected an integrity error: {statement}")


def main() -> None:
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SETUP_SQL.read_text(encoding="utf-8"))

    assert fetchall(connection, "SELECT COUNT(*) FROM department") == [(3,)]
    assert fetchall(connection, "SELECT COUNT(*) FROM student") == [(4,)]
    assert fetchall(connection, "SELECT COUNT(*) FROM course") == [(4,)]
    assert fetchall(connection, "SELECT COUNT(*) FROM enrollment") == [(6,)]

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


if __name__ == "__main__":
    main()
