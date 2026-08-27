from pathlib import Path
import sqlite3


CHAPTER_DIR = Path(__file__).resolve().parents[1]
CH02_DIR = CHAPTER_DIR.parent / "ch02_relational_model"
SETUP_SQL = CH02_DIR / "course_registration_setup.sql"
STUDENT_LAB_SQL = CHAPTER_DIR / "student_lab.sql"


def rows(connection: sqlite3.Connection, query: str):
    return connection.execute(query).fetchall()


def expect_integrity_error(connection: sqlite3.Connection, statement: str) -> None:
    connection.execute("SAVEPOINT expected_failure")
    try:
        connection.execute(statement)
    except sqlite3.IntegrityError:
        connection.execute("ROLLBACK TO expected_failure")
        connection.execute("RELEASE expected_failure")
        return
    connection.execute("ROLLBACK TO expected_failure")
    connection.execute("RELEASE expected_failure")
    raise AssertionError(f"Expected an integrity error: {statement}")


def main() -> None:
    if sqlite3.sqlite_version_info < (3, 39, 0):
        raise RuntimeError("SQLite 3.39.0 or later is required for RIGHT/FULL JOIN")

    connection = sqlite3.connect(":memory:", isolation_level=None)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SETUP_SQL.read_text(encoding="utf-8"))

    explicit_join = rows(
        connection,
        """
        SELECT s.student_id, c.course_id
        FROM student AS s
        JOIN enrollment AS e ON e.student_id = s.student_id
        JOIN course AS c ON c.course_id = e.course_id
        ORDER BY s.student_id, c.course_id
        """,
    )
    assert len(explicit_join) == 6
    assert ("S101", "FT210") in explicit_join

    natural_join = rows(
        connection,
        """
        SELECT student_id, course_id
        FROM student
        NATURAL JOIN enrollment
        NATURAL JOIN course
        ORDER BY student_id, course_id
        """,
    )
    assert len(natural_join) == 5
    assert ("S101", "FT210") not in natural_join

    using_join = rows(
        connection,
        """
        SELECT c.course_id, d.dept_name
        FROM course AS c JOIN department AS d USING (dept_code)
        ORDER BY c.course_id
        """,
    )
    assert using_join == [
        ("DB201", "Information Management"),
        ("FT210", "Finance"),
        ("ML230", "Information Management"),
        ("WD120", "Digital Design"),
    ]

    connection.execute("SAVEPOINT outer_check")
    connection.execute(
        "INSERT INTO course VALUES ('IS250', 'Information Security', 'IM', 3)"
    )
    outer_counts = rows(
        connection,
        """
        SELECT c.course_id, COUNT(e.student_id)
        FROM course AS c
        LEFT JOIN enrollment AS e ON e.course_id = c.course_id
        GROUP BY c.course_id
        ORDER BY c.course_id
        """,
    )
    assert outer_counts == [
        ("DB201", 2),
        ("FT210", 2),
        ("IS250", 0),
        ("ML230", 1),
        ("WD120", 1),
    ]

    predicate_in_on = rows(
        connection,
        """
        SELECT c.course_id, e.student_id
        FROM course AS c
        LEFT JOIN enrollment AS e
          ON e.course_id = c.course_id AND e.grade IN ('A', 'A-')
        ORDER BY c.course_id, e.student_id
        """,
    )
    assert predicate_in_on == [
        ("DB201", "S101"),
        ("FT210", "S102"),
        ("IS250", None),
        ("ML230", "S103"),
        ("WD120", "S104"),
    ]
    predicate_in_where = rows(
        connection,
        """
        SELECT c.course_id, e.student_id
        FROM course AS c
        LEFT JOIN enrollment AS e ON e.course_id = c.course_id
        WHERE e.grade IN ('A', 'A-')
        ORDER BY c.course_id, e.student_id
        """,
    )
    assert predicate_in_where == [
        ("DB201", "S101"),
        ("FT210", "S102"),
        ("ML230", "S103"),
        ("WD120", "S104"),
    ]
    connection.execute("ROLLBACK TO outer_check")
    connection.execute("RELEASE outer_check")

    connection.executescript(
        """
        CREATE TEMP TABLE planned_student (student_id TEXT PRIMARY KEY);
        CREATE TEMP TABLE planned_enrollment (
            student_id TEXT NOT NULL,
            course_id TEXT NOT NULL
        );
        INSERT INTO planned_student VALUES ('S101'), ('S105');
        INSERT INTO planned_enrollment VALUES ('S101', 'DB201'), ('S999', 'AI999');
        """
    )
    right_join = rows(
        connection,
        """
        SELECT ps.student_id, pe.student_id, pe.course_id
        FROM planned_student AS ps
        RIGHT JOIN planned_enrollment AS pe ON pe.student_id = ps.student_id
        ORDER BY pe.student_id
        """,
    )
    assert right_join == [
        ("S101", "S101", "DB201"),
        (None, "S999", "AI999"),
    ]
    full_join = rows(
        connection,
        """
        SELECT ps.student_id, pe.student_id, pe.course_id
        FROM planned_student AS ps
        FULL JOIN planned_enrollment AS pe ON pe.student_id = ps.student_id
        ORDER BY COALESCE(ps.student_id, pe.student_id)
        """,
    )
    assert full_join == [
        ("S101", "S101", "DB201"),
        ("S105", None, None),
        (None, "S999", "AI999"),
    ]

    connection.executescript(
        """
        CREATE VIEW course_enrollment_summary AS
        SELECT c.course_id, c.title, COUNT(e.student_id) AS enrollment_count
        FROM course AS c
        LEFT JOIN enrollment AS e ON e.course_id = c.course_id
        GROUP BY c.course_id, c.title;
        """
    )
    assert rows(
        connection,
        "SELECT enrollment_count FROM course_enrollment_summary WHERE course_id='DB201'",
    ) == [(2,)]
    connection.execute(
        "INSERT INTO enrollment VALUES ('S102', 'DB201', '115-1', NULL)"
    )
    assert rows(
        connection,
        "SELECT enrollment_count FROM course_enrollment_summary WHERE course_id='DB201'",
    ) == [(3,)]
    connection.execute(
        "DELETE FROM enrollment WHERE student_id='S102' AND course_id='DB201'"
    )
    try:
        connection.execute(
            "UPDATE course_enrollment_summary SET enrollment_count=99 "
            "WHERE course_id='DB201'"
        )
    except sqlite3.OperationalError as error:
        assert "view" in str(error).lower()
    else:
        raise AssertionError("SQLite aggregate view update should fail")

    before_swap = rows(
        connection,
        "SELECT course_id FROM enrollment WHERE student_id='S101' ORDER BY course_id",
    )
    connection.execute("BEGIN")
    connection.execute(
        "DELETE FROM enrollment WHERE student_id='S101' AND course_id='FT210' "
        "AND term='115-1'"
    )
    connection.execute(
        "INSERT INTO enrollment VALUES ('S101', 'ML230', '115-1', NULL)"
    )
    assert rows(
        connection,
        "SELECT course_id FROM enrollment WHERE student_id='S101' ORDER BY course_id",
    ) == [("DB201",), ("ML230",)]
    connection.execute("ROLLBACK")
    assert rows(
        connection,
        "SELECT course_id FROM enrollment WHERE student_id='S101' ORDER BY course_id",
    ) == before_swap == [("DB201",), ("FT210",)]

    connection.executescript(
        """
        CREATE TABLE waitlist_entry (
            request_id INTEGER PRIMARY KEY,
            student_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            term TEXT NOT NULL DEFAULT '115-1',
            priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 5),
            UNIQUE (student_id, course_id, term),
            FOREIGN KEY (student_id) REFERENCES student (student_id)
                ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES course (course_id)
        );
        INSERT INTO waitlist_entry
            (request_id, student_id, course_id, priority)
        VALUES (1, 'S104', 'ML230', 2);
        """
    )
    expect_integrity_error(
        connection,
        "INSERT INTO waitlist_entry VALUES (2, 'S104', 'ML230', '115-1', 3)",
    )
    expect_integrity_error(
        connection,
        "INSERT INTO waitlist_entry VALUES (3, 'S103', 'FT210', '115-1', 8)",
    )
    expect_integrity_error(
        connection,
        "INSERT INTO waitlist_entry VALUES (4, 'S999', 'FT210', '115-1', 3)",
    )
    expect_integrity_error(
        connection,
        "INSERT INTO waitlist_entry VALUES (5, NULL, 'FT210', '115-1', 3)",
    )

    connection.execute("SAVEPOINT cascade_check")
    connection.execute(
        "INSERT INTO student VALUES "
        "('S105', 'noah.lee@example.edu', 'Noah Lee', 'IM')"
    )
    connection.execute(
        "INSERT INTO waitlist_entry VALUES (5, 'S105', 'FT210', '115-1', 3)"
    )
    connection.execute("DELETE FROM student WHERE student_id='S105'")
    assert rows(
        connection,
        "SELECT COUNT(*) FROM waitlist_entry WHERE student_id='S105'",
    ) == [(0,)]
    connection.execute("ROLLBACK TO cascade_check")
    connection.execute("RELEASE cascade_check")

    expect_integrity_error(connection, "DELETE FROM department WHERE dept_code='IM'")

    connection.execute(
        "CREATE TEMP TABLE check_without_not_null "
        "(value INTEGER CHECK (value > 0))"
    )
    connection.execute("INSERT INTO check_without_not_null VALUES (NULL)")
    assert rows(
        connection,
        "SELECT value IS NULL FROM check_without_not_null",
    ) == [(1,)]

    lab_connection = sqlite3.connect(":memory:", isolation_level=None)
    lab_connection.execute("PRAGMA foreign_keys = ON")
    lab_connection.executescript(SETUP_SQL.read_text(encoding="utf-8"))
    lab_connection.executescript(STUDENT_LAB_SQL.read_text(encoding="utf-8"))
    assert rows(lab_connection, "SELECT COUNT(*) FROM student") == [(4,)]
    assert rows(lab_connection, "SELECT COUNT(*) FROM enrollment") == [(6,)]
    assert rows(lab_connection, "SELECT COUNT(*) FROM waitlist_entry") == [(1,)]
    assert rows(lab_connection, "PRAGMA foreign_key_check") == []

    print(f"SQLite version: {sqlite3.sqlite_version}")
    print("PASS: explicit, USING, and NATURAL JOIN behavior")
    print("PASS: LEFT/RIGHT/FULL OUTER JOIN and ON-versus-WHERE behavior")
    print("PASS: view definition, live query result, and failed aggregate-view update")
    print("PASS: multi-statement transaction rollback")
    print("PASS: NOT NULL, UNIQUE, CHECK, foreign keys, and ON DELETE CASCADE")
    print("PASS: CHECK with NULL edge case")
    print("PASS: complete student_lab.sql and foreign-key check")


if __name__ == "__main__":
    main()
