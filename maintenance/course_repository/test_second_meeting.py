"""Independent boundary and set-result checks for the revised Ch5/Ch8 examples."""

import contextlib
import io
import itertools
import sqlite3
import unittest

import build_course_repository as builder


def executed_namespace(chapter_id):
    config = builder.load_json(builder.CONFIG_PATH)
    chapter = next(c for c in config["current_chapters"] if c["id"] == chapter_id)
    notebook = builder.build_notebook(chapter)
    builder.execute_notebook(notebook, chapter_id)
    namespace = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                exec("".join(cell["source"]), namespace)
    return namespace


class SecondMeetingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ch5 = executed_namespace("ch05")
        cls.ch8 = executed_namespace("ch08")

    def test_credits_boundaries_on_authored_ddl(self):
        for credits, accepted in [(1, True), (6, True), (2.0, True),
                                  (0, False), (7, False), (2.5, False),
                                  (None, False), ("many", False)]:
            with self.subTest(credits=credits), contextlib.closing(self.ch5["new_database"]()) as db:
                if accepted:
                    db.execute("INSERT INTO course VALUES ('X1', ?)", (credits,))
                    self.assertEqual(db.execute("SELECT typeof(credits) FROM course WHERE course_id='X1'").fetchone(), ("integer",))
                else:
                    with self.assertRaises(sqlite3.IntegrityError):
                        db.execute("INSERT INTO course VALUES ('X1', ?)", (credits,))

    def test_every_composite_key_component_is_required(self):
        for position in range(3):
            row = ["S103", "AI1", "F26"]
            row[position] = None
            with self.subTest(position=position), contextlib.closing(self.ch5["new_database"]()) as db:
                with self.assertRaises(sqlite3.IntegrityError):
                    db.execute("INSERT INTO enrollment VALUES (?, ?, ?)", row)

    def test_authored_twenty_changes_preserve_or_change_state(self):
        accepted = {"Optional department", "Repeated name", "Another term",
                    "Update to existing department", "Delete unreferenced student",
                    "Delete one registration"}
        self.assertEqual(len(self.ch5["cases"]), 20)
        for label, sql in self.ch5["cases"]:
            with self.subTest(label=label), contextlib.closing(self.ch5["new_database"]()) as db:
                before = list(db.iterdump())
                self.assertEqual(db.execute("PRAGMA foreign_keys").fetchone(), (1,))
                if label in accepted:
                    db.execute(sql)
                    self.assertNotEqual(list(db.iterdump()), before)
                else:
                    with self.assertRaises(sqlite3.IntegrityError):
                        db.execute(sql)
                    self.assertEqual(list(db.iterdump()), before)
                self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(), [])

    def test_referential_action_limits(self):
        for action, definition in [
            ("SET NULL", "TEXT NOT NULL"),
            ("SET DEFAULT", "TEXT DEFAULT 'ABSENT'"),
        ]:
            with self.subTest(action=action), contextlib.closing(sqlite3.connect(":memory:", isolation_level=None)) as db:
                db.execute("PRAGMA foreign_keys=ON")
                db.execute("CREATE TABLE parent(id TEXT NOT NULL PRIMARY KEY)")
                db.execute(f"CREATE TABLE child(id {definition} REFERENCES parent(id) ON DELETE {action})")
                db.execute("INSERT INTO parent VALUES ('IM')")
                db.execute("INSERT INTO child VALUES ('IM')")
                with self.assertRaises(sqlite3.IntegrityError):
                    db.execute("DELETE FROM parent WHERE id='IM'")
                self.assertEqual(db.execute("SELECT * FROM child").fetchall(), [("IM",)])

    def test_full_transaction_rollback(self):
        with contextlib.closing(self.ch5["new_database"]()) as db:
            before = list(db.iterdump())
            db.execute("BEGIN")
            db.execute("INSERT INTO student VALUES ('S104','new@example.test','New','IM')")
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("INSERT INTO enrollment VALUES ('S104','Z9','F26')")
            # A statement error alone has not undone the preceding insert.
            self.assertEqual(db.execute("SELECT count(*) FROM student WHERE student_id='S104'").fetchone(), (1,))
            db.execute("ROLLBACK")
            self.assertEqual(list(db.iterdump()), before)

    def test_algebra_against_python_sets(self):
        with contextlib.closing(self.ch8["algebra_database"]()) as db:
            students = set(db.execute("SELECT * FROM student"))
            enrollments = set(db.execute("SELECT * FROM enrollment"))
            courses = set(db.execute("SELECT * FROM course"))
            r = set(db.execute("SELECT * FROM db_club"))
            s = set(db.execute("SELECT * FROM ai_club"))
            cases = [
                ("SELECT * FROM student WHERE dept_code='IM'", {t for t in students if t[2] == "IM"}),
                ("SELECT DISTINCT dept_code FROM student", {(t[2],) for t in students}),
                ("SELECT student_id FROM db_club UNION SELECT student_id FROM ai_club", r | s),
                ("SELECT student_id FROM db_club INTERSECT SELECT student_id FROM ai_club", r & s),
                ("SELECT student_id FROM db_club EXCEPT SELECT student_id FROM ai_club", r - s),
                ("SELECT student_id FROM ai_club EXCEPT SELECT student_id FROM db_club", s - r),
                ("SELECT * FROM student CROSS JOIN course", {a + b for a, b in itertools.product(students, courses)}),
                ("SELECT * FROM student AS s JOIN enrollment AS e ON s.student_id=e.student_id",
                 {a + b for a, b in itertools.product(students, enrollments) if a[0] == b[0]}),
                ("SELECT c.course_id, d.course_id FROM course c JOIN course d ON c.credits < d.credits",
                 {(a[0], b[0]) for a, b in itertools.product(courses, courses) if a[1] < b[1]}),
                ("SELECT DISTINCT s.student_id, s.student_name FROM student s JOIN enrollment e ON s.student_id=e.student_id WHERE s.dept_code='IM' AND e.course_id='DB1' AND e.term='F26'",
                 {(a[0], a[1]) for a, b in itertools.product(students, enrollments)
                  if a[0] == b[0] and a[2] == "IM" and b[1:] == ("DB1", "F26")}),
            ]
            for sql, expected in cases:
                with self.subTest(sql=sql):
                    rows = db.execute(sql).fetchall()
                    self.assertEqual(set(rows), expected)
                    self.assertEqual(len(rows), len(expected))

    def test_bag_duplicates_and_empty_products(self):
        with contextlib.closing(self.ch8["algebra_database"]()) as db:
            values = db.execute("SELECT dept_code FROM student").fetchall()
            self.assertEqual(len(values), 3)
            self.assertEqual(len(set(values)), 2)
            self.assertEqual(db.execute("SELECT * FROM student CROSS JOIN course WHERE course_id='Z9'").fetchall(), [])
            self.assertEqual(db.execute("SELECT * FROM student WHERE dept_code='MED'").fetchall(), [])

    def test_natural_join_shared_names(self):
        with contextlib.closing(self.ch8["algebra_database"]()) as db:
            prefix = "WITH offering(student_id,dept_code) AS (VALUES ('S101','FIN')) "
            self.assertEqual(db.execute(prefix + "SELECT * FROM student NATURAL JOIN offering").fetchall(), [])
            self.assertEqual(db.execute(prefix + "SELECT s.student_id FROM student s JOIN offering o ON s.student_id=o.student_id").fetchall(), [("S101",)])
            renamed = "WITH offering(student_id,offering_dept) AS (VALUES ('S101','FIN')) "
            self.assertEqual(db.execute(renamed + "SELECT student_id FROM student NATURAL JOIN offering").fetchall(), [("S101",)])

    def test_coverage_and_opening_stop(self):
        ch5 = builder.safe_source("maintenance/chapters/ch05_relational_model/student_guide.md").read_text(encoding="utf-8")
        self.assertLess(ch5.index("## Table Concepts: Summary and Practice"), ch5.index("## Continue: Keys and Integrity Constraints"))
        self.assertNotIn("first-meeting", ch5)
        for chapter_id in ("ch05", "ch08"):
            config = builder.load_json(builder.CONFIG_PATH)
            chapter = next(c for c in config["current_chapters"] if c["id"] == chapter_id)
            guide = builder.safe_source(chapter["guide_source"]).read_text(encoding="utf-8")
            for section in guide.split("\n## ")[1:]:
                if section[0].isdigit():
                    self.assertIn("**Predict:", section)
                    self.assertIn("**Practice", section)


if __name__ == "__main__":
    unittest.main()
