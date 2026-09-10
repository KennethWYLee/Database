from __future__ import annotations

import argparse
import base64
import contextlib
import hashlib
import io
import json
import re
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

from notebook_figures import generate_figure
from teaching_figures import definitions as teaching_figure_definitions
from simple_examples import EXAMPLES, RUNTIME as SMALL_EXAMPLE_RUNTIME


SOURCE_DIR = Path(__file__).resolve().parent
COURSE_ROOT = SOURCE_DIR.parents[1]
CONFIG_PATH = SOURCE_DIR / "repository_config.json"
OUTPUT_DIR = SOURCE_DIR / "output"
PREVIEW_DIR = COURSE_ROOT / "Intro DB"
MANIFEST_PATH = OUTPUT_DIR / "course_repository_manifest.json"

CJK_PATTERN = re.compile(
    "["
    "\u3000-\u303f"
    "\u3040-\u30ff"
    "\u3400-\u4dbf"
    "\u4e00-\u9fff"
    "\uac00-\ud7af"
    "]"
)
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FORBIDDEN_TEXT_PATTERNS = {
    "internal working path": re.compile(r"\b(?:working_materials|maintenance)[/\\]", re.IGNORECASE),
    "instruction file": re.compile(r"\b(?:AGENTS|CLAUDE|PROJECT)\.md\b", re.IGNORECASE),
    "coverage record": re.compile(r"coverage_and_verification", re.IGNORECASE),
    "instructor audit": re.compile(r"pre_instructor_review", re.IGNORECASE),
    "internal teaching label": re.compile(r"\bType\s*B\b|\bTypeB\b", re.IGNORECASE),
    "Windows local path": re.compile(
        r"\b[A-Za-z]:\\(?:Users|Windows|Program Files|ProgramData|Temp)\\",
        re.IGNORECASE,
    ),
}
EXPECTED_CHAPTERS = (
    "ch02",
    "ch03",
    "ch04",
    "ch05",
    "ch06",
    "ch07",
    "ch14",
    "ch15",
    "ch16",
    "ch17",
    "ch18",
    "ch19",
)

SQL_HELPERS = '''import sqlite3

print(f"Python {__import__('sys').version.split()[0]}; SQLite {sqlite3.sqlite_version}")
DATABASE_NAME = ":memory:"  # Change to "chapter_database.db" to keep a database file.
connection = sqlite3.connect(DATABASE_NAME, isolation_level=None)
connection.execute("PRAGMA foreign_keys = ON")


def run_sql_script(connection, script, max_rows=20):
    """Execute a SQLite script and display result-producing statements."""
    buffer = ""
    for raw_line in script.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith(".print"):
            message = stripped[len(".print"):].strip().strip("\\\"'")
            print(f"\\n{message}")
            continue
        buffer += raw_line + "\\n"
        if not sqlite3.complete_statement(buffer):
            continue
        statement = buffer.strip()
        buffer = ""
        if not statement:
            continue
        cursor = connection.execute(statement)
        if cursor.description:
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchmany(max_rows + 1)
            print(" | ".join(columns))
            for row in rows[:max_rows]:
                print(" | ".join("NULL" if value is None else str(value) for value in row))
            if len(rows) > max_rows:
                print(f"... additional rows omitted after {max_rows}")
    remaining = "\\n".join(
        line for line in buffer.splitlines() if not line.strip().startswith("--")
    ).strip()
    if remaining:
        raise ValueError("The embedded SQL ends with an incomplete statement.")


def inspect_database(connection):
    """Display tables, columns, primary keys, foreign keys, and integrity status."""
    tables = [
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]
    print("Tables:", ", ".join(tables) if tables else "none")
    for table in tables:
        columns = connection.execute(f'PRAGMA table_info("{table}")').fetchall()
        primary_key = [row[1] for row in sorted(columns, key=lambda row: row[5]) if row[5]]
        print(f"\\n{table}")
        print("  columns:", ", ".join(f"{row[1]} {row[2]}" for row in columns))
        print("  primary key:", ", ".join(primary_key) if primary_key else "none")
        for index_row in connection.execute(f'PRAGMA index_list("{table}")').fetchall():
            if index_row[2] and index_row[3] == "u":
                unique_columns = [
                    row[2]
                    for row in connection.execute(
                        f'PRAGMA index_info("{index_row[1]}")'
                    ).fetchall()
                ]
                print("  unique constraint:", ", ".join(unique_columns))
        foreign_keys = connection.execute(f'PRAGMA foreign_key_list("{table}")').fetchall()
        for foreign_key in foreign_keys:
            print(f"  foreign key: {foreign_key[3]} -> {foreign_key[2]}.{foreign_key[4]}")
    violations = connection.execute("PRAGMA foreign_key_check").fetchall()
    print("\\nForeign-key check:", "PASS" if not violations else violations)
'''

SQL_BUILD_GUIDE = '''## Build and Inspect the Chapter Database

The executable cells use SQLite through Python's standard `sqlite3` module. Follow the
cells in order:

1. Open a database connection and enable foreign-key enforcement.
2. Execute the chapter's `CREATE TABLE` statements before inserting rows.
3. Load the synthetic example data.
4. Inspect the resulting tables, columns, primary keys, and foreign keys.
5. Check referential integrity before running the chapter queries.
6. Predict each query result, execute it, and explain any difference.

`DATABASE_NAME` is initially `:memory:`. The database disappears when its connection
closes; closing a browser tab alone may leave the kernel and connection running.
Change it to a filename such as `chapter_database.db` when you want SQLite to create a
persistent database in the notebook's working directory. Do not switch to a persistent
file until the in-memory version runs successfully from top to bottom.'''

SQL_CHECKS = {
    "ch02": '''assert connection.execute("SELECT COUNT(*) FROM department").fetchone()[0] == 3
assert connection.execute("SELECT COUNT(*) FROM student").fetchone()[0] == 4
assert connection.execute("SELECT COUNT(*) FROM course").fetchone()[0] == 4
assert connection.execute("SELECT COUNT(*) FROM enrollment").fetchone()[0] == 6
assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
print("Notebook checks passed.")''',
    "ch03": '''assert connection.execute("SELECT COUNT(*) FROM department").fetchone()[0] == 3
assert connection.execute("SELECT COUNT(*) FROM student").fetchone()[0] == 4
assert connection.execute("SELECT COUNT(*) FROM course").fetchone()[0] == 4
assert connection.execute("SELECT COUNT(*) FROM enrollment").fetchone()[0] == 6
assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
print("Notebook checks passed.")''',
    "ch04": '''assert connection.execute("SELECT COUNT(*) FROM department").fetchone()[0] == 3
assert connection.execute("SELECT COUNT(*) FROM student").fetchone()[0] == 4
assert connection.execute("SELECT COUNT(*) FROM course").fetchone()[0] == 4
assert connection.execute("SELECT COUNT(*) FROM enrollment").fetchone()[0] == 6
assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
print("Notebook checks passed.")''',
    "ch05": '''assert connection.execute("SELECT COUNT(*) FROM department").fetchone()[0] == 3
assert connection.execute("SELECT COUNT(*) FROM student").fetchone()[0] == 4
assert connection.execute("SELECT COUNT(*) FROM course").fetchone()[0] == 4
assert connection.execute("SELECT COUNT(*) FROM enrollment").fetchone()[0] == 6
assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
print("Notebook checks passed.")''',
    "ch06": '''expected = {"department": 2, "student": 3, "student_phone": 3, "course": 3, "section": 3, "enrollment": 5}
for table, count in expected.items():
    assert connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == count
assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
print("Notebook checks passed.")''',
    "ch07": '''assert connection.execute("SELECT COUNT(*) FROM ch07_course_enrollment_record").fetchone()[0] == 4
lossy_count = connection.execute("SELECT COUNT(*) FROM ch07_employee_identity JOIN ch07_employee_details USING (name)").fetchone()[0]
assert lossy_count == 4
assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
print("Notebook checks passed.")''',
    "ch14": '''assert connection.execute("SELECT COUNT(*) FROM ch14_order_line").fetchone()[0] == 20000
assert connection.execute("SELECT COUNT(*) FROM ch14_order_line WHERE status='COMPLETE'").fetchone()[0] == 16000
print("Notebook checks passed.")''',
    "ch15": '''assert connection.execute("SELECT COUNT(*) FROM ch15_department").fetchone()[0] == 100
assert connection.execute("SELECT COUNT(*) FROM ch15_course").fetchone()[0] == 5000
assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
print("Notebook checks passed.")''',
    "ch16": '''expected = {"ch16_department": 101, "ch16_student": 10000, "ch16_course": 500, "ch16_enrollment": 50000, "ch16_event": 10000}
for table, count in expected.items():
    assert connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == count
assert connection.execute("SELECT COUNT(*) FROM ch16_event WHERE event_type='RARE'").fetchone()[0] == 100
assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
print("Notebook checks passed.")''',
    "ch17": '''balances = connection.execute("SELECT account_id, balance FROM account ORDER BY account_id").fetchall()
assert balances == [("A", 950), ("B", 2050)]
assert connection.execute("SELECT SUM(balance) FROM account").fetchone()[0] == 3000
assert connection.execute("SELECT COUNT(*) FROM transfer_log").fetchone()[0] == 1
assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
print("Notebook checks passed.")''',
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_source(relative: str) -> Path:
    source = (COURSE_ROOT / relative).resolve()
    if not source.is_relative_to(COURSE_ROOT.resolve()) or not source.is_file():
        raise FileNotFoundError(f"Missing or unsafe source: {relative}")
    return source


def safe_target(relative: str) -> Path:
    parts = PurePosixPath(relative).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"Unsafe target: {relative}")
    target = PREVIEW_DIR.joinpath(*parts).resolve()
    if not target.is_relative_to(PREVIEW_DIR.resolve()):
        raise ValueError(f"Target escapes preview directory: {relative}")
    return target


def source_lines(text: str) -> list[str]:
    normalized = text.rstrip() + "\n"
    return normalized.splitlines(keepends=True)


def markdown_cell(text: str, attachments: dict | None = None) -> dict:
    cell = {"cell_type": "markdown", "metadata": {}, "source": source_lines(text)}
    if attachments:
        cell["attachments"] = attachments
    return cell


def code_cell(code: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_lines(code),
    }


def validate_config(config: dict) -> None:
    if safe_source(config["syllabus_source"]) != safe_target("syllabus.md"):
        raise ValueError("The maintained syllabus must be Intro DB/syllabus.md")
    chapters = config["chapters"]
    ids = tuple(chapter["id"] for chapter in chapters)
    if ids != EXPECTED_CHAPTERS:
        raise ValueError(f"Chapter order must be {EXPECTED_CHAPTERS}; received {ids}")
    if len(set(ids)) != len(ids):
        raise ValueError("Chapter identifiers must be unique")
    current = config.get("current_chapters", [])
    if tuple(chapter["id"] for chapter in current) != ("ch01", "ch02", "ch05", "ch08"):
        raise ValueError("Current revised chapters must be ch01, ch02, ch05, ch08")
    if any(not chapter.get("prescribed_textbook") for chapter in current):
        raise ValueError("Current chapters must identify the prescribed textbook")
    for chapter in [*chapters, *current]:
        safe_source(chapter["guide_source"])
        figure_names: set[str] = set()
        for figure in chapter_figures(chapter):
            for key in ("generator", "filename", "title", "alt", "after_heading"):
                if not figure.get(key):
                    raise ValueError(f"{chapter['id']} figure is missing {key}")
            if figure["filename"] in figure_names or not figure["filename"].endswith(".png"):
                raise ValueError(f"Invalid or duplicate generated figure in {chapter['id']}")
            figure_names.add(figure["filename"])
            ET.fromstring(generate_figure(figure["generator"]))
        for group in ("markdown_sources", "image_sources", "sql_sources"):
            for item in chapter.get(group, []):
                safe_source(item["source"])
        for program in chapter.get("programs", []):
            safe_source(program["script_source"])
            for source in program.get("data_sources", []):
                safe_source(source)

    weeks = config["weeks"]
    numbers = [week["week"] for week in weeks]
    if numbers != list(range(1, 19)):
        raise ValueError(f"Weeks must be ordered 1 through 18; received {numbers}")
    known = set(ids)
    for week in weeks:
        if not set(week["materials"]).issubset(known):
            raise ValueError(f"Week {week['week']} refers to an unknown chapter")


def normalize_guide(text: str) -> str:
    replacements = {
        "py -3 run_labs.py ch04": "Run the executable SQL cells below.",
        "py -3 schedule_analyzer.py schedule_examples.json": "Run the embedded schedule-analyzer cell below.",
        "py -3 lock_simulator.py lock_scenarios.json": "Run the embedded lock-simulator cell below.",
        "py -3 recovery_simulator.py recovery_case.json": "Run the embedded recovery-simulator cell below.",
        "py -3 wal_checker.py wal_scenarios.json": "Run the embedded write-ahead logging checker below.",
        "`course_registration_setup.sql`": "the shared setup SQL cell",
        "`student_lab.sql`": "the executable SQL lab cell",
        "`mapped_schema.sql`": "the mapped-schema SQL cell",
        "`standard_routine_examples.sql`": "the standard-routine reference cell",
        "`schedule_analyzer.py`": "the embedded schedule analyzer",
        "`schedule_examples.json`": "the embedded schedule examples",
        "`lock_simulator.py`": "the embedded lock simulator",
        "`lock_scenarios.json`": "the embedded lock scenarios",
        "`mvcc_demo.py`": "the embedded multiversion demonstration",
        "`recovery_simulator.py`": "the embedded recovery simulator",
        "`recovery_case.json`": "the embedded recovery case",
        "`wal_checker.py`": "the embedded write-ahead logging checker",
        "`wal_scenarios.json`": "the embedded write-ahead logging scenarios",
        "`run_labs.py`": "the executable notebook cells",
        "![Course registration E-R diagram](course_registration_er.png)": "![Course registration E-R diagram](attachment:course_registration_er.png)",
        "![B+ tree example](bplus_tree_example.png)": "![B+ tree example](attachment:bplus_tree_example.png)",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def split_guide(text: str, subsections: bool = False) -> list[str]:
    pattern = r"(?=^#{2,3}\s)" if subsections else r"(?=^##\s)"
    return [section.strip() for section in re.split(pattern, text, flags=re.MULTILINE) if section.strip()]


def chapter_figures(chapter: dict) -> list[dict]:
    figures = list(chapter.get("generated_figures", []))
    if chapter.get("visual_teaching"):
        prefix = "opening_" if chapter.get("prescribed_textbook") else ""
        figures.extend(teaching_figure_definitions(prefix + chapter["id"]))
    return figures


def guide_section_cells(section: str, attachments: dict, executable: bool) -> list[dict]:
    if not executable:
        return [markdown_cell(section, attachments)]
    cells: list[dict] = []
    position = 0
    # Only opted-in guides turn fenced examples into cells. Output fences verify
    # the adjacent example; the notebook displays its actual executed output.
    for match in re.finditer(r"^```(python|output)\n(.*?)^```[ \t]*$", section, re.MULTILINE | re.DOTALL):
        prose = section[position:match.start()].strip()
        if prose:
            cells.append(markdown_cell(prose))
        if match.group(1) == "python":
            cells.append(code_cell(match.group(2)))
        else:
            if not cells or cells[-1]["cell_type"] != "code":
                raise ValueError("An output fence must immediately follow its Python example")
            cells[-1]["_expected_stdout"] = match.group(2).rstrip()
        position = match.end()
    tail = section[position:].strip()
    if tail:
        cells.append(markdown_cell(tail))
    for cell in cells:
        if cell["cell_type"] == "markdown":
            used = {name: value for name, value in attachments.items()
                    if f"attachment:{name}" in "".join(cell["source"])}
            if used:
                cell["attachments"] = used
    return cells


def image_attachments(chapter: dict) -> dict[str, dict]:
    attachments: dict[str, dict] = {}
    for item in chapter.get("image_sources", []):
        data = base64.b64encode(safe_source(item["source"]).read_bytes()).decode("ascii")
        attachments[item["filename"]] = {item["mime_type"]: data}
    return attachments


def generated_figure_cells(chapter: dict, heading: str) -> list[dict]:
    cells: list[dict] = []
    for figure in chapter_figures(chapter):
        if figure["after_heading"] != heading:
            continue
        example = EXAMPLES.get(figure["generator"])
        if example:
            cells.extend(small_example_cells(example))
        svg = generate_figure(figure["generator"])
        ET.fromstring(svg)
        # GitHub's notebook preview does not display the SVG attachments used here.
        # Rasterize the maintained vector source without losing markers or dashes.
        try:
            import resvg_py
        except ImportError as error:
            raise RuntimeError("Building diagrams requires resvg-py==0.5.0; see the build README") from error
        png = resvg_py.svg_to_bytes(svg_string=svg)
        encoded = base64.b64encode(png).decode("ascii")
        markdown = (
            f"### {figure['title']}\n\n"
            f"![{figure['alt']}](attachment:{figure['filename']})\n\n"
            + figure.get("caption", "This original diagram applies the chapter concepts to the synthetic "
                         "course-registration example used throughout the notebooks.")
        )
        if example:
            markdown = f"![{figure['alt']}](attachment:{figure['filename']})"
        cells.append(
            markdown_cell(
                markdown,
                {figure["filename"]: {"image/png": encoded}},
            )
        )
        if example:
            cells.append(markdown_cell(
                "**Read the result.** " + example["interpretation"] + "\n\n"
                "**Try a change.** " + example["practice"] + "\n\n"
                "**Check your reasoning.** " + example["check"] + "\n\n"
                "When this variation is assigned, retain your prediction, result, "
                "and correction or explanation."
            ))
    return cells


def small_example_cells(example: dict) -> list[dict]:
    intro = f"### Small Example: {example['title']}\n\n{example['concept']}\n\n"
    intro += "The following data are artificial teaching inputs, not student records.\n\n"
    for item in example["inputs"]:
        intro += f"**Input: {item['name']}**\n\n"
        intro += "| " + " | ".join(item["headers"]) + " |\n"
        intro += "| " + " | ".join("---" for _ in item["headers"]) + " |\n"
        for row in item["rows"]:
            intro += "| " + " | ".join("NULL" if v is None else str(v) for v in row) + " |\n"
        if not item["rows"]:
            intro += "\nThe input table is empty.\n"
        intro += "\n"
    intro += "**Predict before checking.** " + example["prediction"]
    cells = [markdown_cell(intro)]
    if example["steps"]:
        tables = [(t["name"], t["schema"], t["rows"]) for t in example["inputs"]]
        import pprint
        code = "tables = " + pprint.pformat(tables, width=90, sort_dicts=False)
        code += "\nstatements = [\n"
        for label, sql in example["steps"]:
            code += f"    ({label!r}, \"\"\"\n{sql}\n\"\"\"),\n"
        code += "]\nrun_small_example(tables, statements)"
        cell = code_cell(code)
        expected = []
        for output in example["outputs"]:
            expected.append(output["title"])
            if output["headers"]:
                expected.append(" | ".join(output["headers"]))
            for row in output["rows"]:
                expected.append(" | ".join("NULL" if v is None else str(v) for v in row))
            if not output["rows"]:
                expected.append("(no rows)")
            expected.append("")
        cell["_expected_stdout"] = "\n".join(expected).rstrip()
        cells.append(cell)
    return cells


def embedded_text_assignment(variable: str, text: str) -> str:
    escaped = text.replace("\\", "\\\\")
    if '"""' not in text:
        return f'{variable} = """{escaped.rstrip()}\n"""'
    if "'''" not in text:
        return f"{variable} = '''{escaped.rstrip()}\n'''"
    return f"{variable} = {text!r}"


def sql_cells(chapter: dict) -> list[dict]:
    sources = chapter.get("sql_sources", [])
    if not sources:
        return []
    cells = [markdown_cell(SQL_BUILD_GUIDE)]
    executable = [item for item in sources if item["execute"]]
    if executable:
        cells.append(code_cell(SQL_HELPERS))
    inspection_added = False
    for index, item in enumerate(sources, start=1):
        sql = safe_source(item["source"]).read_text(encoding="utf-8")
        if item["execute"]:
            variable = f"SQL_{index}"
            cells.append(markdown_cell(f"### {item['title']}"))
            cells.append(code_cell(embedded_text_assignment(variable, sql)))
            cells.append(code_cell(f"run_sql_script(connection, {variable})"))
            if not inspection_added:
                cells.append(
                    markdown_cell(
                        "### Inspect the Database You Created\n\n"
                        "Read the output as a schema check: confirm the table names, column "
                        "types, primary-key order, foreign-key direction, and integrity result."
                    )
                )
                cells.append(code_cell("inspect_database(connection)"))
                inspection_added = True
        else:
            cells.append(
                markdown_cell(
                    f"### {item['title']}\n\nThis reference uses standard SQL/PSM syntax and is not executed by SQLite.\n\n```sql\n{sql.rstrip()}\n```"
                )
            )
    check = SQL_CHECKS.get(chapter["id"])
    if check:
        cells.append(markdown_cell("### Reproducibility Check"))
        cells.append(code_cell(check))
    if executable:
        cells.append(code_cell('connection.close()\nprint("Database connection closed.")'))
    return cells


def load_sql_examples(text: str) -> dict[str, str]:
    """Read the numbered example blocks from a maintained SQL lab."""
    text = text.split("-- Student practice:", 1)[0]
    markers = list(re.finditer(r"^-- Example (\d+[a-z]?):.*$", text, re.MULTILINE))
    examples: dict[str, str] = {}
    for index, marker in enumerate(markers):
        identifier = marker.group(1)
        if identifier in examples:
            raise ValueError(f"Duplicate SQL example: {identifier}")
        end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        examples[identifier] = text[marker.start():end].strip()
    if not examples:
        raise ValueError("No numbered SQL examples found")
    return examples


def expand_inline_sql(guide: str, chapter: dict) -> str:
    """Embed maintained SQL at explicit positions without duplicating its source."""
    sources = chapter["sql_sources"]
    if len(sources) != 2 or not all(item["execute"] for item in sources):
        raise ValueError("Inline SQL requires one setup and one executable numbered lab")
    setup = safe_source(sources[0]["source"]).read_text(encoding="utf-8")
    examples = load_sql_examples(safe_source(sources[1]["source"]).read_text(encoding="utf-8"))
    seen: set[str] = set()

    def replace(match: re.Match) -> str:
        token = match.group(1)
        if token in seen:
            raise ValueError(f"Repeated inline SQL marker: {token}")
        seen.add(token)
        if token == "setup":
            code = SQL_HELPERS + "\n" + embedded_text_assignment("SQL_1", setup)
            code += '\nrun_sql_script(connection, SQL_1)\ninspect_database(connection)'
            code += '\nprint("\\nTable | rows")\nfor table in ("department", "student", "course", "enrollment"):\n    count = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]\n    print(f"{table} | {count}")'
            return SQL_BUILD_GUIDE + "\n\n```python\n" + code + "\n```"
        if token == "checks":
            code = SQL_CHECKS[chapter["id"]] + '\nconnection.close()\nprint("Database connection closed.")'
        else:
            identifier = token.removeprefix("example ")
            if identifier not in examples:
                raise ValueError(f"Unknown SQL example: {identifier}")
            variable = f"SQL_EXAMPLE_{identifier}"
            code = embedded_text_assignment(variable, examples[identifier])
            code += f"\nrun_sql_script(connection, {variable})"
        return "```python\n" + code + "\n```"

    result = re.sub(r"^<!-- sql:(setup|checks|example \d+[a-z]?) -->$", replace, guide, flags=re.MULTILINE)
    expected = {"setup", "checks", *(f"example {identifier}" for identifier in examples)}
    if seen != expected or "<!-- sql:" in result:
        raise ValueError(f"Incomplete inline SQL mapping: missing={sorted(expected - seen)}")
    return result


def program_cell(program: dict) -> dict:
    script_path = safe_source(program["script_source"])
    assignments = [
        embedded_text_assignment(
            "SCRIPT_SOURCE", script_path.read_text(encoding="utf-8")
        )
    ]
    file_entries = [f"    {script_path.name!r}: SCRIPT_SOURCE,"]
    arguments: list[str] = []
    for index, relative in enumerate(program.get("data_sources", []), start=1):
        path = safe_source(relative)
        variable = f"DATA_{index}_SOURCE"
        assignments.append(
            embedded_text_assignment(variable, path.read_text(encoding="utf-8"))
        )
        file_entries.append(f"    {path.name!r}: {variable},")
        arguments.append(path.name)
    embedded_sources = "\n\n".join(assignments)
    embedded_mapping = "\n".join(file_entries)
    code = f'''import subprocess
import sys
import tempfile
from pathlib import Path

{embedded_sources}

embedded_files = {{
{embedded_mapping}
}}
with tempfile.TemporaryDirectory(prefix="database_notebook_") as temp_directory:
    temp_path = Path(temp_directory)
    for filename, content in embedded_files.items():
        (temp_path / filename).write_text(content, encoding="utf-8")
    command = [sys.executable, str(temp_path / {script_path.name!r})] + {arguments!r}
    completed = subprocess.run(command, cwd=temp_path, text=True, capture_output=True, check=False)
    print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    if completed.returncode != 0:
        raise RuntimeError(f"Embedded program failed with exit code {{completed.returncode}}")
'''
    return code_cell(code)


def build_notebook(chapter: dict) -> dict:
    guide = normalize_guide(safe_source(chapter["guide_source"]).read_text(encoding="utf-8"))
    if chapter.get("inline_sql"):
        if not chapter.get("executable_guide"):
            raise ValueError("Inline SQL requires executable_guide")
        guide = expand_inline_sql(guide, chapter)
    attachments = image_attachments(chapter)
    cells: list[dict] = []
    if not chapter.get("prescribed_textbook"):
        cells.append(markdown_cell(
            "# Previous Material: Not Assigned\n\n"
            "This notebook uses another textbook's chapter numbering. It is retained "
            "for review, not assigned reading for the current course. Its chapter, week, "
            "and examination labels are historical and do not define current requirements. "
            "Use the current course syllabus and its first-meeting notebook links."
        ))
    parent_heading = ""
    seen_anchors: dict[str, int] = {}
    small_setup_added = False
    for section in split_guide(guide, chapter.get("visual_teaching", False)):
        section_attachments = {
            filename: value
            for filename, value in attachments.items()
            if f"attachment:{filename}" in section
        }
        cells.extend(guide_section_cells(section, section_attachments, chapter.get("executable_guide", False)))
        heading = section.splitlines()[0].strip()
        if heading.startswith("## "):
            parent_heading = heading
        seen_anchors[heading] = seen_anchors.get(heading, 0) + 1
        anchors = {heading, parent_heading + " / " + heading}
        if not chapter.get("prescribed_textbook") and not small_setup_added and any(e["chapter"] == chapter["id"] and e["steps"]
                                         and e["heading"] in anchors for e in EXAMPLES.values()):
            cells.append(markdown_cell(
                "### Running the Small Examples\n\n"
                "Run this setup cell once. Each small SQL example starts from its displayed "
                "input tables in a fresh in-memory SQLite database and closes it afterward. "
                "The table definitions and SQL are supplied; Python helper syntax is not "
                "an additional learning requirement. Read and predict before running each example. "
                "The larger chapter lab remains available later in this notebook."
                " The instructor will select variations for class practice; the additional "
                "examples are not separate required assignments."
            ))
            cells.append(code_cell(SMALL_EXAMPLE_RUNTIME))
            small_setup_added = True
        cells.extend(generated_figure_cells(chapter, heading))
        if heading.startswith("### "):
            qualified = parent_heading + " / " + heading
            seen_anchors[qualified] = seen_anchors.get(qualified, 0) + 1
            cells.extend(generated_figure_cells(chapter, qualified))

    for figure in chapter_figures(chapter):
        if seen_anchors.get(figure["after_heading"]) != 1:
            raise ValueError(f"Missing or ambiguous figure anchor: {figure['after_heading']}")

    for item in chapter.get("markdown_sources", []):
        text = normalize_guide(safe_source(item["source"]).read_text(encoding="utf-8"))
        cells.append(markdown_cell(f"## {item['title']}\n\n{text}"))

    if not chapter.get("inline_sql"):
        cells.extend(sql_cells(chapter))
    if chapter.get("programs"):
        if not chapter.get("sql_sources"):
            cells.append(
                markdown_cell(
                    "## Why This Chapter Uses a Simulation\n\n"
                    "SQLite can create tables and execute transactions, but it does not expose "
                    "a server lock manager, wait-for graph, write-ahead log, or restart-recovery "
                    "procedure for direct classroom inspection. This notebook therefore uses a "
                    "small verified Python simulation for the chapter mechanism. Treat the "
                    "result as an instructional model, not as observed SQLite server behavior."
                )
            )
        cells.append(
            markdown_cell(
                "## Executable Notebook Demonstrations\n\nThe source code and data are embedded in this notebook. Each cell creates a temporary directory, runs the demonstration, and removes the temporary files automatically."
            )
        )
        for program in chapter["programs"]:
            cells.append(markdown_cell(f"### {program['title']}"))
            cells.append(program_cell(program))

    for index, cell in enumerate(cells, start=1):
        cell["id"] = f"{chapter['id']}-{index:04d}"

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": sys.version.split()[0]},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def execute_notebook(notebook: dict, notebook_name: str) -> None:
    namespace = {"__name__": "__notebook__"}
    execution_count = 0
    for cell_index, cell in enumerate(notebook["cells"], start=1):
        if cell["cell_type"] != "code":
            continue
        execution_count += 1
        stdout = io.StringIO()
        stderr = io.StringIO()
        source = "".join(cell["source"])
        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(compile(source, f"{notebook_name}:cell-{cell_index}", "exec"), namespace)
        except Exception as error:
            raise RuntimeError(
                f"Notebook execution failed in {notebook_name}, cell {cell_index}: {error}"
            ) from error
        expected = cell.pop("_expected_stdout", None)
        if expected is not None and stdout.getvalue().rstrip() != expected:
            raise RuntimeError(f"Worked-example output mismatch in {notebook_name}, cell {cell_index}")
        outputs = []
        if stdout.getvalue():
            outputs.append({"name": "stdout", "output_type": "stream", "text": stdout.getvalue().splitlines(keepends=True)})
        if stderr.getvalue():
            outputs.append({"name": "stderr", "output_type": "stream", "text": stderr.getvalue().splitlines(keepends=True)})
        cell["execution_count"] = execution_count
        cell["outputs"] = outputs


def all_chapters(config: dict) -> list[dict]:
    return [*config.get("current_chapters", []), *config["chapters"]]


def notebook_relative(chapter: dict) -> str:
    prefix = "" if chapter.get("prescribed_textbook") else "under_revision/"
    return f"{prefix}{chapter['id']}.ipynb"


def expected_files(config: dict) -> set[str]:
    return {"syllabus.md", "under_revision/README.md",
            *(notebook_relative(chapter) for chapter in all_chapters(config))}


def build_preview(config: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    expected = expected_files(config)
    unexpected = {path.relative_to(PREVIEW_DIR).as_posix()
                  for path in PREVIEW_DIR.rglob("*") if path.is_file()} - expected
    if unexpected:
        raise ValueError(f"Unexpected files in Intro DB; nothing removed: {sorted(unexpected)}")
    # Finish all executions before replacing the known generated notebooks. Never
    # remove the course folder, its maintained syllabus, or the root README.
    with tempfile.TemporaryDirectory(prefix="notebooks_", dir=OUTPUT_DIR) as temporary:
        staging = Path(temporary)
        for chapter in all_chapters(config):
            notebook = build_notebook(chapter)
            execute_notebook(notebook, f"{chapter['id']}.ipynb")
            target = staging / notebook_relative(chapter)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8", newline="\n",
            )
        for chapter in all_chapters(config):
            filename = notebook_relative(chapter)
            safe_target(filename).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(staging / filename, safe_target(filename))


def write_manifest(config: dict) -> list[dict]:
    files = []
    for path in sorted(PREVIEW_DIR.rglob("*")):
        if path.is_file():
            files.append(
                {
                    "path": path.relative_to(PREVIEW_DIR).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    manifest = {
        "repository_name": config["repository_name"],
        "repository_version": config["repository_version"],
        "content_status": "Intro DB files built locally; Git synchronization is a separate action",
        "files": files,
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return files


def verify_manifest(files: list[dict]) -> None:
    listed = {item["path"]: item for item in files}
    actual = {
        path.relative_to(PREVIEW_DIR).as_posix()
        for path in PREVIEW_DIR.rglob("*")
        if path.is_file()
    }
    if actual != set(listed):
        raise RuntimeError("Manifest does not match the generated repository")
    for relative, item in listed.items():
        path = safe_target(relative)
        if path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            raise RuntimeError(f"Manifest verification failed: {relative}")


def notebook_markdown(notebook: dict) -> str:
    return "\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "markdown"
    )


def verify_content(config: dict) -> None:
    errors: list[str] = []
    expected = expected_files(config)
    actual_files = {
        path.relative_to(PREVIEW_DIR).as_posix()
        for path in PREVIEW_DIR.rglob("*")
        if path.is_file()
    }
    if actual_files != expected:
        errors.append(
            f"Unexpected Intro DB layout; missing={sorted(expected - actual_files)}, unexpected={sorted(actual_files - expected)}"
        )

    for path in PREVIEW_DIR.rglob("*"):
        if not path.is_file() or path.name == ".gitignore":
            continue
        relative = path.relative_to(PREVIEW_DIR).as_posix()
        if path.suffix == ".ipynb":
            try:
                notebook = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as error:
                errors.append(f"Invalid notebook JSON in {relative}: {error}")
                continue
            if notebook.get("nbformat") != 4:
                errors.append(f"Unsupported notebook format in {relative}")
            cell_ids = [cell.get("id") for cell in notebook.get("cells", [])]
            if any(not isinstance(cell_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", cell_id)
                   for cell_id in cell_ids):
                errors.append(f"Missing or invalid cell ID in {relative}")
            elif len(cell_ids) != len(set(cell_ids)):
                errors.append(f"Duplicate cell ID in {relative}")
            code_cells = [cell for cell in notebook.get("cells", []) if cell.get("cell_type") == "code"]
            if any(cell.get("execution_count") is None for cell in code_cells):
                errors.append(f"Unexecuted code cell in {relative}")
            markdown = notebook_markdown(notebook)
            for match in MARKDOWN_LINK_PATTERN.finditer(markdown):
                target = match.group(1).strip()
                if target.startswith(("attachment:", "http://", "https://", "mailto:", "#")):
                    continue
                errors.append(f"External local-file dependency in {relative}: {target}")
            content_parts = [
                "".join(cell.get("source", []))
                for cell in notebook.get("cells", [])
            ]
            content_parts.extend(
                "".join(output.get("text", []))
                for cell in notebook.get("cells", [])
                for output in cell.get("outputs", [])
                if output.get("output_type") == "stream"
            )
            content = "\n".join(content_parts)
        else:
            content = path.read_text(encoding="utf-8")
            if path.suffix == ".md":
                for match in MARKDOWN_LINK_PATTERN.finditer(content):
                    target_text = unquote(match.group(1).strip().strip("<>").split("#", 1)[0])
                    if not target_text or target_text.startswith(
                        ("http://", "https://", "mailto:")
                    ):
                        continue
                    target = (path.parent / target_text).resolve()
                    if not target.is_relative_to(PREVIEW_DIR.resolve()) or not target.exists():
                        errors.append(f"Broken local link in {relative}: {target_text}")
        if CJK_PATTERN.search(content):
            errors.append(f"Non-English CJK text in {relative}")
        for label, pattern in FORBIDDEN_TEXT_PATTERNS.items():
            if pattern.search(content):
                errors.append(f"{label} in {relative}")

    for chapter in all_chapters(config):
        notebook = json.loads(safe_target(notebook_relative(chapter)).read_text(encoding="utf-8"))
        expected_attachments = {item["filename"] for item in chapter.get("image_sources", [])}
        expected_attachments.update(
            item["filename"] for item in chapter_figures(chapter)
        )
        actual_attachments = {
            filename
            for cell in notebook["cells"]
            for filename in cell.get("attachments", {})
        }
        if actual_attachments != expected_attachments:
            errors.append(f"Attachment mismatch in {chapter['id']}.ipynb")

    if errors:
        raise RuntimeError("Course-repository verification failed:\n- " + "\n- ".join(errors))
    print(f"COURSE_CONTENT_VERIFICATION=PASS NOTEBOOKS={len(all_chapters(config))} ASSET_FILES=0")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the unified Database Management course repository.")
    parser.add_argument("--verify", action="store_true", help="verify content, manifest, and notebook execution")
    args = parser.parse_args()

    config = load_json(CONFIG_PATH)
    validate_config(config)
    build_preview(config)
    files = write_manifest(config)
    print(f"BUILT_FILES={len(files)}")
    print(f"COURSE_MATERIALS_DIR={PREVIEW_DIR}")
    print(f"MANIFEST_PATH={MANIFEST_PATH}")
    if args.verify:
        verify_manifest(files)
        print("COURSE_REPOSITORY_MANIFEST=PASS")
        verify_content(config)
        print("ALL_NOTEBOOKS_EXECUTED=PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
