from pathlib import Path
import sqlite3
import xml.etree.ElementTree as ET


CHAPTER_DIR = Path(__file__).resolve().parents[1]
SCHEMA_SQL = CHAPTER_DIR / "mapped_schema.sql"
DIAGRAM_SVG = CHAPTER_DIR / "course_registration_er.svg"
DIAGRAM_PNG = CHAPTER_DIR / "course_registration_er.png"


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
    raise AssertionError(f"Expected integrity error: {statement}")


def main() -> None:
    connection = sqlite3.connect(":memory:", isolation_level=None)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SCHEMA_SQL.read_text(encoding="utf-8"))

    assert rows(connection, "SELECT COUNT(*) FROM department") == [(2,)]
    assert rows(connection, "SELECT COUNT(*) FROM student") == [(3,)]
    assert rows(connection, "SELECT COUNT(*) FROM student_phone") == [(3,)]
    assert rows(connection, "SELECT COUNT(*) FROM course") == [(3,)]
    assert rows(connection, "SELECT COUNT(*) FROM section") == [(3,)]
    assert rows(connection, "SELECT COUNT(*) FROM enrollment") == [(5,)]

    # Candidate key and total many-to-one relationship mappings.
    expect_integrity_error(
        connection,
        "INSERT INTO student VALUES "
        "('S104', 'an.chen@example.edu', 'Mira', 'Ho', 'IM')",
    )
    expect_integrity_error(
        connection,
        "INSERT INTO student VALUES "
        "('S104', 'mira.ho@example.edu', 'Mira', 'Ho', 'NONE')",
    )
    expect_integrity_error(
        connection,
        "INSERT INTO course VALUES ('WD120', 'Web Design', 2, 'NONE')",
    )

    # Multivalued attribute mapping permits multiple values, not duplicate pairs.
    assert rows(
        connection,
        "SELECT phone_number FROM student_phone WHERE student_id='S101' "
        "ORDER BY phone_number",
    ) == [("02-2322-1010",), ("0911-000-101",)]
    expect_integrity_error(
        connection,
        "INSERT INTO student_phone VALUES ('S101', '0911-000-101')",
    )

    # Weak entity owner key plus discriminator and identifying foreign key.
    expect_integrity_error(
        connection,
        "INSERT INTO section VALUES ('NONE', '115-1', 1, 'H999', 20)",
    )
    connection.execute("SAVEPOINT weak_key_check")
    connection.execute(
        "INSERT INTO section VALUES ('DB201', '115-1', 2, 'H502', 45)"
    )
    assert rows(
        connection,
        "SELECT section_no FROM section WHERE course_id='DB201' ORDER BY section_no",
    ) == [(1,), (2,)]
    connection.execute("ROLLBACK TO weak_key_check")
    connection.execute("RELEASE weak_key_check")

    # M:N relationship and descriptive attribute constraints.
    expect_integrity_error(
        connection,
        "INSERT INTO enrollment VALUES ('S101', 'DB201', '115-1', 9, 'A')",
    )
    expect_integrity_error(
        connection,
        "INSERT INTO enrollment VALUES ('S101', 'DB201', '115-1', 1, 'Z')",
    )
    assert rows(
        connection,
        """
        SELECT s.student_id,
               COALESCE(SUM(CASE WHEN e.grade IS NOT NULL AND e.grade <> 'F'
                                 THEN c.credits ELSE 0 END), 0)
        FROM student AS s
        LEFT JOIN enrollment AS e ON e.student_id=s.student_id
        LEFT JOIN course AS c ON c.course_id=e.course_id
        GROUP BY s.student_id ORDER BY s.student_id
        """,
    ) == [("S101", 6), ("S102", 3), ("S103", 3)]

    # Recursive relationship roles and direct self-reference constraint.
    expect_integrity_error(
        connection,
        "INSERT INTO course_prerequisite VALUES ('DB201', 'DB201')",
    )
    assert rows(
        connection,
        "SELECT course_id, prereq_id FROM course_prerequisite",
    ) == [("ML230", "DB201")]

    assert rows(connection, "PRAGMA foreign_key_check") == []

    root = ET.parse(DIAGRAM_SVG).getroot()
    assert root.tag.endswith("svg")
    svg_text = "".join(root.itertext())
    for required in (
        "Department",
        "Student",
        "Course",
        "Section [weak]",
        "majors_in",
        "offers",
        "registers",
        "identifies",
        "0..*",
        "1..1",
    ):
        assert required in svg_text
    assert DIAGRAM_PNG.exists() and DIAGRAM_PNG.stat().st_size > 10_000

    print(f"SQLite version: {sqlite3.sqlite_version}")
    print("PASS: strong entities, candidate key, and total many-to-one mappings")
    print("PASS: composite and multivalued attribute mappings")
    print("PASS: weak entity owner key, discriminator, and identifying foreign key")
    print("PASS: M:N registration relationship and grade attribute")
    print("PASS: role-named recursive relationship and direct self-reference check")
    print("PASS: derived completed-credit query and all foreign keys")
    print("PASS: parseable SVG and rendered PNG diagram")


if __name__ == "__main__":
    main()
