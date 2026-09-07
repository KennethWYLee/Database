"""Check Week 1 results and independence from the Week 2 database."""

import base64
import contextlib
import io
import json
from pathlib import Path
import sqlite3
import sys


COURSE_ROOT = Path(__file__).resolve().parents[4]
NOTEBOOK = COURSE_ROOT / "Intro DB/ch02.ipynb"


def run_cells(cells):
    namespace = {"__name__": "__notebook__"}
    outputs = []
    for cell in cells:
        if cell["cell_type"] != "code":
            continue
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exec(compile("".join(cell["source"]), "ch02-review-cell", "exec"), namespace)
        actual = stdout.getvalue()
        preserved = "".join(
            "".join(output.get("text", []))
            for output in cell["outputs"] if output.get("name") == "stdout"
        )
        assert actual == preserved, "Preserved output differs from a fresh execution"
        outputs.append(actual)
    return namespace, outputs


def verify_worked_tables(markdown):
    before = [("S101", "555-0101;555-0102"), ("S102", "555-0103")]
    after = [("S101", "555-0101"), ("S101", "555-0102"), ("S102", "555-0103")]
    for heading, rows in [("phone_numbers", before), ("phone_number", after)]:
        table = "\n".join([
            f"| student_id | {heading} |", "|---|---|",
            *(f"| {student} | {phone} |" for student, phone in rows),
        ])
        assert table in markdown, f"Missing or changed worked table: {heading}"

    # Verify the displayed paper example independently without changing the notebook DB.
    db = sqlite3.connect(":memory:")
    try:
        db.execute("CREATE TABLE contact_list (student_id TEXT, phone_numbers TEXT)")
        db.execute("CREATE TABLE student_phone (student_id TEXT, phone_number TEXT)")
        db.executemany("INSERT INTO contact_list VALUES (?, ?)", before)
        db.executemany("INSERT INTO student_phone VALUES (?, ?)", after)
        assert db.execute(
            "SELECT student_id FROM contact_list WHERE phone_numbers = ?", ("555-0102",)
        ).fetchall() == []
        assert db.execute(
            "SELECT student_id FROM student_phone WHERE phone_number = ?", ("555-0102",)
        ).fetchall() == [("S101",)]
        assert db.execute(
            "SELECT COUNT(*), COUNT(DISTINCT student_id) FROM student_phone"
        ).fetchone() == (3, 2)
        assert [(student, phone) for student, numbers in before
                for phone in numbers.split(";")] == after

        db.execute("CREATE TABLE duplicate_example (value TEXT)")
        db.executemany("INSERT INTO duplicate_example VALUES (?)", [("IM",), ("IM",)])
        assert db.execute("SELECT DISTINCT value FROM duplicate_example").fetchall() == [("IM",)]
        assert db.execute("SELECT COUNT(*) FROM duplicate_example").fetchone() == (2,)
    finally:
        db.close()

    assert "Removing duplicates\nfrom a query result does not remove rows from the stored table." in markdown
    assert "constraints or queries prevent this" not in markdown
    practice = markdown.split("## Week 1 Practice", 1)[1]
    assert "add a description attribute" in practice
    assert "one catalog description per course" in practice
    assert "room attribute" not in practice


def verify_lesson_completion(markdown, namespace, outputs):
    for heading in [
        "### Worked Example: Two Copies Disagree",
        "### Worked Comparison: Repeated Value or Repeated Tuple?",
        "### Comparing the Three Changes",
    ]:
        assert heading in markdown
    assert "| Registration file | S101 | an.chen@example.edu |" in markdown
    assert "| Contact file | S101 | an.old@example.edu |" in markdown
    assert "assume\nthe office verifies S101's identity" in markdown

    original = namespace["ascending"]
    assert original[0][3] == original[2][3] == "IM"
    assert original[0] != original[2]
    assert len(set(original + [original[0]])) == 4
    assert len(original + [original[0]]) == 5
    for index, state, count in [
        (0, "Original student table", (4, 4)),
        (3, "After adding S105", (5, 4)),
        (4, "After changing S102 from FIN to IM", (5, 4)),
        (5, "After adding status", (5, 5)),
    ]:
        assert f"| {state} | {count[0]} | {count[1]} |" in markdown
        assert outputs[index].endswith(f"Tuples: {count[0]}; attributes: {count[1]}\n")

    practice = markdown.split("## Week 1 Practice", 1)[1]
    assert "either your correction or an explanation of why your prediction was\ncorrect" in practice
    assert "one correction you made" not in practice
    courses = [("DB201", "Database Management", 3), ("ML230", "Machine Learning", 3),
               ("WD120", "Web Design", 2)]
    for course_id, title, credits in courses:
        assert f"| {course_id} | {title} | {credits} |" in practice
    assert "(DB205, Database Management, 5)" in practice
    assert "change WD120's credits from 2 to 3" in practice
    for action in ("add", "update", "attribute"):
        db = sqlite3.connect(":memory:")
        try:
            db.execute("CREATE TABLE course (course_id TEXT PRIMARY KEY, title TEXT, credits INTEGER)")
            db.executemany("INSERT INTO course VALUES (?, ?, ?)", courses)
            if action == "add":
                db.execute("INSERT INTO course VALUES ('DB205', 'Database Management', 5)")
                assert db.execute(
                    "SELECT course_id FROM course WHERE title='Database Management' ORDER BY course_id"
                ).fetchall() == [("DB201",), ("DB205",)]
            elif action == "update":
                db.execute("UPDATE course SET credits=3 WHERE course_id='WD120'")
                assert db.execute("SELECT credits FROM course WHERE course_id='WD120'").fetchone() == (3,)
            else:
                db.execute("ALTER TABLE course ADD COLUMN description TEXT")
            assert db.execute("SELECT COUNT(*) FROM course").fetchone()[0] == (4 if action == "add" else 3)
            assert len(db.execute("PRAGMA table_info(course)").fetchall()) == (4 if action == "attribute" else 3)
        finally:
            db.close()


def main():
    cells = json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]
    headings = ["".join(cell["source"]).splitlines()[0] for cell in cells]
    stop = headings.index("## End of Week 1")
    start_week2 = headings.index("## Week 2: Keys and Relational Algebra")
    assert stop < start_week2
    assert headings.index("## 3. Keys") > start_week2
    assert headings.index("## Build and Inspect the Chapter Database") > start_week2
    assert headings.index("## Week 1 Practice") < stop

    week1 = cells[:stop]
    markdown = "\n".join("".join(cell["source"]) for cell in week1
                         if cell["cell_type"] == "markdown")
    verify_worked_tables(markdown)
    namespace, outputs = run_cells(week1)
    assert len(outputs) == 7
    assert outputs[0].endswith("Tuples: 4; attributes: 4\n")
    assert namespace["ascending"] == [
        ("S101", "an.chen@example.edu", "An Chen", "IM"),
        ("S102", "bea.lin@example.edu", "Bea Lin", "FIN"),
        ("S103", "kai.wu@example.edu", "Kai Wu", "IM"),
        ("S104", "mira.ho@example.edu", "Mira Ho", "DES"),
    ]
    assert namespace["descending"] == namespace["ascending"][::-1]
    assert outputs[1].splitlines() == [
        "1: allowed", "4: allowed", "6: allowed",
        "0: outside the stated domain", "7: outside the stated domain",
        "2.5: outside the stated domain",
    ]
    assert "S105 | an.second@example.edu | An Chen | FIN" in outputs[3]
    assert outputs[3].endswith("Tuples: 5; attributes: 4\n")
    assert "S102 | bea.lin@example.edu | Bea Lin | IM" in outputs[4]
    assert outputs[4].endswith("Tuples: 5; attributes: 4\n")
    assert outputs[5].count(" | active\n") == 5
    assert outputs[5].endswith("Tuples: 5; attributes: 5\n")
    assert namespace["matches"] == [("S101", "An Chen", "IM"), ("S105", "An Chen", "FIN")]
    verify_lesson_completion(markdown, namespace, outputs)
    try:
        namespace["week1_db"].execute("SELECT 1")
    except sqlite3.ProgrammingError:
        pass
    else:
        raise AssertionError("Week 1 database must be closed at the stopping point")

    # Week 2 must also work in a fresh namespace, without running Week 1.
    week2_namespace, week2_outputs = run_cells(cells[start_week2:])
    assert "week1_db" not in week2_namespace
    assert "S105" not in "\n".join(week2_outputs)
    assert "Foreign-key check: PASS" in "\n".join(week2_outputs)
    assert "status" not in week2_namespace["SQL_1"]

    figure_cells = [cell for cell in week1 if "ch02_table_anatomy.png" in cell.get("attachments", {})]
    assert len(figure_cells) == 1
    for cell in cells:
        for filename, formats in cell.get("attachments", {}).items():
            assert filename.endswith(".png") and set(formats) == {"image/png"}
            png = base64.b64decode(formats["image/png"], validate=True)
            assert png.startswith(b"\x89PNG\r\n\x1a\n")
            assert int.from_bytes(png[16:20], "big") == 1200
    assert not any("_expected_stdout" in cell for cell in cells)
    assert not any("```output" in "".join(cell["source"]) for cell in cells)
    print(f"Python {sys.version.split()[0]}; SQLite {sqlite3.sqlite_version}")
    print("PASS: seven interleaved Week 1 demonstrations and preserved outputs")
    print("PASS: domain decisions, row order, insert, update, added attribute, same-name students")
    print("PASS: Week 1 database closed; Week 2 executes independently with original data")
    print("PASS: meeting boundaries, original annotated table, and no output-fence leakage")
    print("PASS: phone tables preserve all three contacts for two students; exact match identifies S101")
    print("PASS: query deduplication leaves stored duplicates; course descriptions keep the same row meaning")
    print("PASS: concrete DBMS example, duplicate-tuple comparison, state summary, and all practice changes")


if __name__ == "__main__":
    main()
