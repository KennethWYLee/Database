"""Check figure data against executable examples and export local visual-review files."""

import base64
from html import escape
import json
from pathlib import Path
import sqlite3
import xml.etree.ElementTree as ET

import nbformat
from nbconvert import HTMLExporter
import resvg_py

import build_course_repository as builder
from teaching_figures import FIGURES


ROOT = builder.COURSE_ROOT
OUTPUT = builder.OUTPUT_DIR / "visual_review"


def rows(name, index):
    return FIGURES[name]["panels"][index]["rows"]


def strings(result):
    return [["NULL" if v is None else str(v) for v in row] for row in result]


def check_data():
    db = sqlite3.connect(":memory:")
    chapter = ROOT / "maintenance/chapters/ch02_relational_model"
    db.executescript((chapter / "course_registration_setup.sql").read_text(encoding="utf-8"))
    original = db.execute("SELECT student_id, student_name, dept_code FROM student ORDER BY student_id").fetchall()
    assert rows("ch02_selection", 0) == strings(original)
    selected = db.execute("SELECT student_id, student_name, dept_code FROM student WHERE dept_code='IM' ORDER BY student_id").fetchall()
    assert rows("ch02_selection", 1) == strings(selected)
    assert rows("ch02_composition", 0) == strings(original)
    assert rows("ch02_composition", 1) == strings(selected)
    examples = builder.load_sql_examples((chapter / "student_lab.sql").read_text(encoding="utf-8"))
    for name, panel_index, example in [("ch02_projection", 1, "3"), ("ch02_composition", 2, "4"), ("ch02_product", 2, "5")]:
        assert rows(name, panel_index) == strings(db.execute(examples[example]).fetchall())
    assert rows("ch02_order", 0) == [r[:2] for r in strings(original)]
    assert rows("ch02_order", 1) == rows("ch02_order", 0)[::-1]
    for row, example in zip(rows("ch02_sets", 2)[:3], ["7a", "7b", "7c"]):
        assert row[1].split(", ") == [r[0] for r in db.execute(examples[example])]
    assert rows("ch02_sets", 2)[3][1] == db.execute("SELECT student_id FROM enrollment WHERE course_id='FT210' EXCEPT SELECT student_id FROM enrollment WHERE course_id='DB201'").fetchone()[0]
    db.execute("INSERT INTO enrollment VALUES ('S101','DB201','115-2',NULL)")
    assert rows("ch02_composite", 0) == strings(db.execute("SELECT student_id,course_id,term FROM enrollment WHERE student_id='S101' AND course_id='DB201' ORDER BY term").fetchall())
    db.rollback()
    assert rows("ch03_groups", 0) == strings(db.execute("SELECT course_id,dept_code FROM course WHERE credits>=3 ORDER BY course_id").fetchall())
    assert rows("ch03_groups", 1) == strings(db.execute("SELECT dept_code,COUNT(*) FROM course WHERE credits>=3 GROUP BY dept_code ORDER BY dept_code").fetchall())
    assert rows("ch03_groups", 2) == strings(db.execute("SELECT dept_code,COUNT(*) FROM course WHERE credits>=3 GROUP BY dept_code HAVING COUNT(*)>=2").fetchall())
    db.execute("CREATE TABLE figure_grades(grade TEXT)")
    db.executemany("INSERT INTO figure_grades VALUES (?)", [("B",), ("F",), (None,)])
    truth = {1: "TRUE", 0: "FALSE", None: "UNKNOWN"}
    assert rows("ch03_null", 0) == [["NULL" if g is None else g, truth[t], "Yes" if t == 1 else "No"]
                                    for g, t in db.execute("SELECT grade, grade <> 'F' FROM figure_grades")]
    assert db.execute("SELECT COUNT(*),COUNT(grade) FROM figure_grades").fetchone() == (3, 2)
    db.execute("INSERT INTO course VALUES ('IS250','Information Systems','IM',3)")
    for idx, join in [(0, "JOIN"), (1, "LEFT JOIN")]:
        sql = f"SELECT c.course_id,COUNT(e.student_id) FROM course c {join} enrollment e ON c.course_id=e.course_id GROUP BY c.course_id ORDER BY c.course_id"
        assert rows("ch04_outer", idx) == strings(db.execute(sql).fetchall())
    on = db.execute("SELECT c.course_id FROM course c LEFT JOIN enrollment e ON c.course_id=e.course_id AND e.grade IN ('A','A-')").fetchall()
    where = db.execute("SELECT c.course_id FROM course c LEFT JOIN enrollment e ON c.course_id=e.course_id WHERE e.grade IN ('A','A-')").fetchall()
    assert ("IS250",) in on and ("IS250",) not in where
    db.executescript((chapter / "course_registration_setup.sql").read_text(encoding="utf-8"))
    db.executescript((ROOT / "maintenance/chapters/ch05_advanced_sql/student_lab.sql").read_text(encoding="utf-8"))
    ranked = db.execute("WITH best AS (SELECT student_id,MAX(score) AS score FROM sql_practice_score GROUP BY student_id) SELECT student_id,score,RANK() OVER(ORDER BY score DESC),DENSE_RANK() OVER(ORDER BY score DESC),ROW_NUMBER() OVER(ORDER BY score DESC,student_id) FROM best ORDER BY score DESC,student_id").fetchall()
    assert rows("ch05_ranks", 0) == strings(ranked)
    direct = set(db.execute("SELECT course_id,prereq_id FROM course_prerequisite"))
    added = {(a, d) for a, b in direct for c, d in direct if b == c} - direct
    assert set(map(tuple, rows("ch05_recursive", 0))) == direct
    assert set(map(tuple, rows("ch05_recursive", 1))) == added
    assert len(direct | added) == 5
    db.executescript((ROOT / "maintenance/chapters/ch07_normalization/student_lab.sql").read_text(encoding="utf-8"))
    actual = db.execute("SELECT employee_id,city FROM ch07_employee_identity JOIN ch07_employee_details USING(name) ORDER BY employee_id,city").fetchall()
    displayed = [(r[0], r[1]) for r in rows("ch07_lossy", 1)]
    assert sorted(displayed) == sorted(actual)
    originals = {("E1", "Taipei"), ("E2", "Tainan")}
    assert all(r[2] == ("Yes" if tuple(r[:2]) in originals else "No") for r in rows("ch07_lossy", 1))
    for definition in ["a", "b"]:
        db.execute(f"CREATE TABLE {definition}(value TEXT)")
    db.executemany("INSERT INTO a VALUES (?)", rows("ch16_equivalence", 0))
    db.executemany("INSERT INTO b VALUES (?)", rows("ch16_equivalence", 1))
    assert db.execute("SELECT * FROM a EXCEPT SELECT * FROM b").fetchall() == []
    assert db.execute("SELECT * FROM b EXCEPT SELECT * FROM a").fetchall() == []
    assert db.execute("SELECT value,COUNT(*) FROM a GROUP BY value").fetchall() != db.execute("SELECT value,COUNT(*) FROM b GROUP BY value").fetchall()
    assert 10000 / 2 == 5000
    assert 9900 / 10000 == 0.99 and 100 / 10000 == 0.01
    assert sum(map(int, [r[1] for r in rows("ch17_transfer", 0)])) == 3000
    assert sum(map(int, [r[1] for r in rows("ch17_transfer", 1)])) == 3000
    assert rows("ch17_transfer", 0) == rows("ch17_transfer", 2)
    assert rows("ch19_recovery", 0) == [["950", "2000", "600"]]
    assert rows("ch19_recovery", 1) == [["950", "2050", "600"]]
    assert rows("ch19_recovery", 2) == [["950", "2050", "700"]]
    db.close()
    print("FIGURE_DATA_CHECKS=PASS")


def main():
    check_data()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    config = builder.load_json(builder.CONFIG_PATH)
    manifest = []
    gallery = []
    for chapter in config["chapters"]:
        notebook = nbformat.read(builder.PREVIEW_DIR / f"{chapter['id']}.ipynb", as_version=4)
        nbformat.validate(notebook)
        attachment_count = sum(len(c.get("attachments", {})) for c in notebook.cells)
        generated = builder.chapter_figures(chapter)
        assert attachment_count == len(generated) + len(chapter.get("image_sources", []))
        for f in generated:
            name = f["generator"]
            svg = builder.generate_figure(name)
            root = ET.fromstring(svg)
            assert root.attrib["width"] == "1200"
            png = resvg_py.svg_to_bytes(svg_string=svg)
            assert png.startswith(b"\x89PNG")
            (OUTPUT / f"{name}.svg").write_text(svg, encoding="utf-8")
            (OUTPUT / f"{name}.png").write_bytes(png)
            matching = [c for c in notebook.cells if f["filename"] in c.get("attachments", {})]
            assert len(matching) == 1
            assert base64.b64decode(matching[0].attachments[f["filename"]]["image/png"]) == png
            manifest.append(dict(chapter=chapter["id"], name=name, width=1200, height=int(root.attrib["height"])))
            gallery.append(f'<figure><img src="{name}.png" alt="{escape(f["alt"])}"><figcaption>{chapter["id"]}: {escape(f["title"])}</figcaption></figure>')
        html, _ = HTMLExporter(template_name="lab").from_notebook_node(notebook)
        (OUTPUT / f"{chapter['id']}.html").write_text(html, encoding="utf-8")
        print(chapter["id"], "EMBEDDED_FIGURES", attachment_count)
    (OUTPUT / "figures.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (OUTPUT / "gallery.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Course figures</title><style>body{margin:24px;font:18px Arial;background:#fff}main{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}figure{margin:0;break-inside:avoid}img{width:100%;height:auto}figcaption{padding:8px 0}</style><main>' + ''.join(gallery) + '</main></html>', encoding="utf-8")
    print("GENERATED_FIGURES", len(manifest), "ORIGINAL_NEW_FIGURES", len(FIGURES))


if __name__ == "__main__":
    main()
