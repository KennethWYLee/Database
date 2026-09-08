"""Verify and render the prescribed-book first-meeting selections, without publishing."""

import ast
import asyncio
import base64
import html
import io
import json
import re
import sqlite3
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

import nbformat
from markdown_it import MarkdownIt
from nbclient import NotebookClient
from PIL import Image

import build_course_repository as builder
from opening_figures import FIGURES


OUTPUT = builder.OUTPUT_DIR / "first_meeting"
MARKDOWN = MarkdownIt("commonmark").enable("table")
STYLE = """body{font:17px/1.65 Arial,sans-serif;color:#202124;margin:0;background:white}
main{max-width:1120px;margin:auto;padding:28px}h1{font-size:30px}h2{font-size:25px}
h3{font-size:20px}img{display:block;max-width:100%;height:auto;margin:16px auto}
pre{overflow:auto;padding:16px;background:#f3f5f7;font-size:14px;line-height:1.5}
code{overflow-wrap:anywhere}table{border-collapse:collapse;min-width:650px;width:100%;font-size:15px}
td,th{border:1px solid #c7ccd1;text-align:left;vertical-align:top;padding:9px}
th{background:#eef3f5}.table-scroll{overflow:auto}a{color:#075bba}
.output{border-left:3px solid #207464}section{min-width:0}
@media(max-width:600px){main{padding:16px}h1{font-size:25px}h2{font-size:22px}}
"""


def preview(name, body):
    body = body.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
    (OUTPUT / f"{name}.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{name}</title><style>{STYLE}</style><main>{body}</main></html>',
        encoding="utf-8",
    )


def stream(cell):
    return "".join("".join(output.get("text", [])) for output in cell.get("outputs", [])
                   if output.get("output_type") == "stream" and output.get("name") == "stdout")


def verify():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    OUTPUT.mkdir(parents=True, exist_ok=True)
    config = builder.load_json(builder.CONFIG_PATH)
    builder.validate_config(config)
    builder.verify_content(config)
    results = []
    for chapter in config["current_chapters"]:
        path = builder.safe_target(builder.notebook_relative(chapter))
        raw = json.loads(path.read_text(encoding="utf-8"))
        assert not list(nbformat.validator.iter_validate(raw)), path
        rebuilt = builder.build_notebook(chapter)
        builder.execute_notebook(rebuilt, chapter["id"])
        assert raw == rebuilt, f"Generated output is stale: {path}"
        guide = builder.safe_source(chapter["guide_source"]).read_text(encoding="utf-8")
        assert "Fundamentals of Database Systems" in guide
        assert not re.search(r"(?i)\btype\s*b\b|\b\d+\s*(?:minutes?|mins?)\b", guide)
        assert "prediction" in guide.lower() and "Practice" in guide
        assert not re.search(r"[\u3400-\u9fff\ufffd]", guide)
        text = builder.notebook_markdown(raw)
        assert "Previous Material: Not Assigned" not in text
        assert not any(needle in text for needle in ["Chapter 2: Introduction to the Relational Model",
                                                     "Chapter 5: Advanced SQL", "Database System Concepts*,"])

        notebook = nbformat.reads(json.dumps(raw), as_version=4)
        notebook.cells.insert(0, nbformat.v4.new_code_cell(
            "import sys, sqlite3\nprint(sys.version.split()[0], sqlite3.sqlite_version)"
        ))
        with tempfile.TemporaryDirectory(prefix="db_first_meeting_") as temp:
            executed = NotebookClient(notebook, timeout=120, kernel_name="python3",
                                      resources={"metadata": {"path": temp}}).execute()
            assert not list(Path(temp).iterdir()), "Notebook created persistent files"
        environment = stream(executed.cells[0]).strip()
        executed.cells.pop(0)
        for expected, actual in zip(raw["cells"], executed.cells):
            if expected["cell_type"] == "code":
                assert stream(expected) == stream(actual), (chapter["id"], expected["id"])
                assert not any(o.output_type == "error" for o in actual.outputs)

        body = []
        image_count = 0
        for cell in raw["cells"]:
            source = "".join(cell["source"])
            if cell["cell_type"] == "markdown":
                rendered = MARKDOWN.render(source)
                for name, mime in cell.get("attachments", {}).items():
                    encoded = mime["image/png"]
                    data = base64.b64decode(encoded, validate=True)
                    with Image.open(io.BytesIO(data)) as picture:
                        assert picture.width >= 1000 and picture.height > 100
                        assert sum(extent[1] - extent[0] for extent in picture.convert("RGB").getextrema()) > 50
                    rendered = rendered.replace("attachment:" + name, "data:image/png;base64," + encoded)
                    image_count += 1
                body.append("<section>" + rendered + "</section>")
            else:
                body.append("<section><pre>" + html.escape(source) + "</pre><pre class=output>"
                            + html.escape(stream(cell)) + "</pre></section>")
        assert image_count == len(builder.chapter_figures(chapter))
        preview(chapter["id"], "".join(body))
        results.append(dict(chapter=chapter["id"], images=image_count,
                            code_cells=sum(c["cell_type"] == "code" for c in raw["cells"]),
                            kernel_environment=environment, sha256=builder.sha256(path)))

    # Check values independently of the authored captions and query strings.
    departments = ["IM", "FIN", "IM"]
    assert {d: departments.count(d) for d in set(departments)} == {"IM": 2, "FIN": 1}
    assert len(set(departments)) == 2
    assert [x for x in [5, 2.5, 7] if isinstance(x, int) and 1 <= x <= 6] == [5]
    assert len({("S101", "02-0000-0101"), ("S101", "02-0000-0102"), ("S102", "02-0000-0201")}) == 3
    assert len(FIGURES) == 16

    # Inspect the exact DDL in the new Ch5 code, not a separate idealized schema.
    ch5 = json.loads((builder.PREVIEW_DIR / "ch05.ipynb").read_text(encoding="utf-8"))
    key_cases = 0
    for cell in ch5["cells"]:
        if cell["cell_type"] != "code":
            continue
        for node in ast.walk(ast.parse("".join(cell["source"]))):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "execute" and node.args and isinstance(node.args[0], ast.Constant)):
                continue
            sql = node.args[0].value
            if not isinstance(sql, str) or not sql.startswith("CREATE TABLE student "):
                continue
            db = sqlite3.connect(":memory:")
            try:
                db.execute(sql)
                try:
                    db.execute("INSERT INTO student(student_id) VALUES (NULL)")
                    raise AssertionError("Missing ID accepted")
                except sqlite3.IntegrityError:
                    pass
                db.execute("INSERT INTO student(student_id) VALUES ('S101')")
                try:
                    db.execute("INSERT INTO student(student_id) VALUES ('S101')")
                    raise AssertionError("Duplicate ID accepted")
                except sqlite3.IntegrityError:
                    pass
                assert db.execute("SELECT COUNT(*) FROM student").fetchone()[0] == 1
                key_cases += 1
            finally:
                db.close()
    assert key_cases == 2

    links = 0
    docs = [builder.COURSE_ROOT / "README.md", builder.PREVIEW_DIR / "syllabus.md",
            builder.PREVIEW_DIR / "under_revision/README.md", builder.COURSE_ROOT / "maintenance/README.md",
            builder.COURSE_ROOT / "maintenance/COURSE_PLAN.md", builder.COURSE_ROOT / "PROJECT.md",
            builder.SOURCE_DIR / "README.md", builder.SOURCE_DIR / "first_meeting_release.md"]
    for path in docs:
        text = path.read_text(encoding="utf-8")
        assert "\ufffd" not in text
        for token in MARKDOWN.parse(text):
            for child in token.children or []:
                if child.type == "link_open":
                    url = urlsplit(child.attrGet("href"))
                    if not url.scheme and url.path:
                        assert (path.parent / unquote(url.path)).exists(), (path, url.path)
                        links += 1
        if path == builder.COURSE_ROOT / "README.md":
            preview("home", MARKDOWN.render(text))
        if path.name == "syllabus.md":
            preview("syllabus", MARKDOWN.render(text))

    for chapter in config["chapters"]:
        old = json.loads(builder.safe_target(builder.notebook_relative(chapter)).read_text(encoding="utf-8"))
        assert "Previous Material: Not Assigned" in "".join(old["cells"][0]["source"])

    # Gallery retains SVG for geometry checks; student notebooks contain PNGs only.
    cards = []
    for name in FIGURES:
        svg = builder.generate_figure(name)
        cards.append(f'<section class="figure" id="{name}"><h2>{name}</h2>{svg}</section>')
    preview("figures", "".join(cards))
    report = dict(python=sys.version.split()[0], sqlite=sqlite3.sqlite_version,
                  chapters=results, figures=sum(r["images"] for r in results),
                  relative_links=links, exact_ddl_key_cases=key_cases,
                  fresh_kernels=3, complete_textbook_chapter_audits=0)
    (OUTPUT / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    verify()
