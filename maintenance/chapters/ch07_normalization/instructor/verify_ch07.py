from __future__ import annotations

import itertools
import sqlite3
from pathlib import Path


CHAPTER_DIR = Path(__file__).resolve().parents[1]
LAB_PATH = CHAPTER_DIR / "student_lab.sql"


def closure(attributes: set[str], fds: list[tuple[set[str], set[str]]]) -> set[str]:
    result = set(attributes)
    changed = True
    while changed:
        changed = False
        for left, right in fds:
            if left <= result and not right <= result:
                result |= right
                changed = True
    return result


def candidate_keys(
    attributes: set[str], fds: list[tuple[set[str], set[str]]]
) -> list[frozenset[str]]:
    keys: list[frozenset[str]] = []
    ordered = sorted(attributes)
    for size in range(1, len(ordered) + 1):
        for values in itertools.combinations(ordered, size):
            candidate = frozenset(values)
            if any(key <= candidate for key in keys):
                continue
            if closure(set(candidate), fds) == attributes:
                keys.append(candidate)
    return keys


def assert_fk_clean(connection: sqlite3.Connection) -> None:
    violations = connection.execute("PRAGMA foreign_key_check").fetchall()
    assert violations == [], violations


def main() -> None:
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(LAB_PATH.read_text(encoding="utf-8"))

    flat_count = connection.execute(
        "SELECT COUNT(*) FROM ch07_course_enrollment_record"
    ).fetchone()[0]
    assert flat_count == 4

    dept_counts = connection.execute(
        """
        SELECT dept_code, COUNT(*)
        FROM ch07_course_enrollment_record
        GROUP BY dept_code ORDER BY dept_code
        """
    ).fetchall()
    assert dept_counts == [("FIN", 1), ("IM", 3)], dept_counts
    assert connection.execute(
        "SELECT COUNT(DISTINCT dept_name) FROM ch07_course_enrollment_record "
        "WHERE dept_code = 'IM'"
    ).fetchone()[0] == 1

    ai_count = connection.execute(
        """
        SELECT COUNT(e.student_id)
        FROM ch07_course AS c
        LEFT JOIN ch07_enrollment AS e ON e.course_id = c.course_id
        WHERE c.course_id = 'AI301'
        """
    ).fetchone()[0]
    assert ai_count == 0

    reconstructed = connection.execute(
        """
        SELECT s.student_id, s.student_name, d.dept_code, d.dept_name,
               c.course_id, c.course_title, c.credits, e.grade
        FROM ch07_enrollment AS e
        JOIN ch07_student AS s ON s.student_id = e.student_id
        JOIN ch07_department AS d ON d.dept_code = s.dept_code
        JOIN ch07_course AS c ON c.course_id = e.course_id
        ORDER BY s.student_id, c.course_id
        """
    ).fetchall()
    original = connection.execute(
        "SELECT * FROM ch07_course_enrollment_record ORDER BY student_id, course_id"
    ).fetchall()
    assert reconstructed == original

    lossy_rows = connection.execute(
        """
        SELECT i.employee_id, i.name, d.city, d.salary
        FROM ch07_employee_identity AS i
        JOIN ch07_employee_details AS d USING (name)
        ORDER BY i.employee_id, d.city
        """
    ).fetchall()
    assert len(lossy_rows) == 4
    assert ("E1", "Kim", "Tainan", 62000) in lossy_rows
    assert ("E2", "Kim", "Taipei", 60000) in lossy_rows

    flat_attributes = {
        "student_id", "student_name", "dept_code", "dept_name",
        "course_id", "course_title", "credits", "grade",
    }
    flat_fds = [
        ({"student_id"}, {"student_name", "dept_code"}),
        ({"dept_code"}, {"dept_name"}),
        ({"course_id"}, {"course_title", "credits"}),
        ({"student_id", "course_id"}, {"grade"}),
    ]
    flat_keys = candidate_keys(flat_attributes, flat_fds)
    assert flat_keys == [frozenset({"student_id", "course_id"})], flat_keys
    assert closure({"dept_code"}, flat_fds) != flat_attributes
    assert {"dept_code", "dept_name"} <= closure({"dept_code"}, flat_fds)

    teaching_attributes = {"student_id", "course_id", "instructor_id"}
    teaching_fds = [
        ({"student_id", "course_id"}, {"instructor_id"}),
        ({"instructor_id"}, {"course_id"}),
    ]
    teaching_keys = set(candidate_keys(teaching_attributes, teaching_fds))
    assert teaching_keys == {
        frozenset({"student_id", "course_id"}),
        frozenset({"student_id", "instructor_id"}),
    }
    assert closure({"instructor_id"}, teaching_fds) != teaching_attributes
    prime_attributes = set().union(*teaching_keys)
    assert "course_id" in prime_attributes

    assert_fk_clean(connection)
    connection.close()

    print(f"SQLite {sqlite3.sqlite_version}")
    print("PASS flattened facts and reversible anomaly demonstration")
    print("PASS normalized inserts and independent course fact")
    print("PASS lossless reconstruction in both directions")
    print("PASS deliberately lossy join and spurious tuples")
    print("PASS attribute closure and flattened candidate key")
    print("PASS 3NF-but-not-BCNF example classification inputs")
    print("PASS complete lab and foreign-key check")


if __name__ == "__main__":
    main()
