"""Check the single-branch layout and ensure builds preserve maintained files."""

import contextlib
import copy
import io
import json
import re
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote

import nbformat

import build_course_repository as builder


class RepositoryLayoutTests(unittest.TestCase):
    def test_syllabus_weekly_chapter_labels_match_plan(self):
        syllabus = (builder.PREVIEW_DIR / "syllabus.md").read_text(encoding="utf-8")
        schedule = syllabus.split("## Weekly Schedule\n", 1)[1].split("\n## Assessment", 1)[0]
        rows = [line.split("|")[1:-1] for line in schedule.splitlines()
                if re.match(r"\| \d+ \|", line)]
        weeks = builder.load_json(builder.CONFIG_PATH)["weeks"]
        self.assertEqual(len(rows), len(weeks))
        for row, week in zip(rows, weeks):
            self.assertEqual(len(row), 5)
            self.assertEqual(int(row[0]), week["week"])
            match = re.search(r"Chapters? (\d+)(?:-(\d+))?", row[2])
            expected = [int(chapter[2:]) for chapter in week["materials"]]
            actual = list(range(int(match[1]), int(match[2] or match[1]) + 1)) if match else []
            self.assertEqual(actual, expected, week["week"])

    def test_visual_figures_and_unique_anchors(self):
        config = builder.load_json(builder.CONFIG_PATH)
        total = 0
        for chapter in config["chapters"]:
            with self.subTest(chapter=chapter["id"]):
                notebook = builder.build_notebook(chapter)
                attachments = [name for cell in notebook["cells"]
                               for name in cell.get("attachments", {})]
                self.assertEqual(len(attachments), len(set(attachments)))
                self.assertEqual(len(attachments), 19 if chapter["id"] == "ch02"
                                 else 3 if chapter["id"] in {"ch05", "ch06", "ch14", "ch19"} else 2)
                total += len(attachments)
        self.assertEqual(total, 45)

    def test_invalid_figure_anchors_are_rejected(self):
        chapter = builder.load_json(builder.CONFIG_PATH)["chapters"][0]
        original = builder.chapter_figures(chapter)
        for anchor in ["## Missing topic", "### Read the Output"]:
            altered = copy.deepcopy(original)
            altered[0]["after_heading"] = anchor
            with self.subTest(anchor=anchor), patch.object(builder, "chapter_figures", return_value=altered):
                with self.assertRaisesRegex(ValueError, "Missing or ambiguous figure anchor"):
                    builder.build_notebook(chapter)

    def test_inline_sql_mapping_and_outputs(self):
        chapter = builder.load_json(builder.CONFIG_PATH)["chapters"][0]
        guide = builder.safe_source(chapter["guide_source"]).read_text(encoding="utf-8")
        expanded = builder.expand_inline_sql(guide, chapter)
        self.assertNotIn("<!-- sql:", expanded)
        self.assertEqual(expanded.count("## Build and Inspect the Chapter Database"), 1)
        self.assertLess(expanded.index("## Build and Inspect"), expanded.index("## 3. Keys"))
        notebook = builder.build_notebook(chapter)
        builder.execute_notebook(notebook, "inline-test")
        code = "\n".join("".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code")
        self.assertNotIn("SQL_2 =", code)
        self.assertEqual(code.count("-- Example 4:"), 1)
        self.assertEqual(code.count("connection.close()"), 1)
        for marker in ["<!-- sql:setup -->", "<!-- sql:example 4 -->", "<!-- sql:checks -->"]:
            with self.subTest(marker=marker):
                with self.assertRaisesRegex(ValueError, "Incomplete inline"):
                    builder.expand_inline_sql(guide.replace(marker, ""), chapter)
                with self.assertRaisesRegex(ValueError, "Repeated inline"):
                    builder.expand_inline_sql(guide + "\n" + marker, chapter)
        with self.assertRaisesRegex(ValueError, "Unknown SQL example"):
            builder.expand_inline_sql(guide.replace("example 4 -->", "example 99 -->"), chapter)
        with self.assertRaisesRegex(ValueError, "Duplicate SQL example"):
            builder.load_sql_examples("-- Example 1: first\nSELECT 1;\n-- Example 1: second\nSELECT 2;")

    def test_root_and_course_files(self):
        root = builder.COURSE_ROOT
        self.assertEqual({p.name for p in root.glob("*.md")},
                         {"README.md", "PROJECT.md", "AGENTS.md", "CLAUDE.md"})
        self.assertEqual((root / "AGENTS.md").read_bytes(), (root / "CLAUDE.md").read_bytes())
        self.assertEqual({p.name for p in builder.PREVIEW_DIR.iterdir()},
                         {"syllabus.md", *(f"{c}.ipynb" for c in builder.EXPECTED_CHAPTERS)})
        config = builder.load_json(builder.CONFIG_PATH)
        builder.validate_config(config)
        with contextlib.redirect_stdout(io.StringIO()):
            builder.verify_content(config)

    def test_raw_notebook_schema(self):
        for path in builder.PREVIEW_DIR.glob("*.ipynb"):
            with self.subTest(path=path.name):
                raw = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(list(nbformat.validator.iter_validate(raw)), [])

    def test_current_navigation_links(self):
        root = builder.COURSE_ROOT
        paths = [root / "README.md", root / "Intro DB/syllabus.md", root / "maintenance/README.md"]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("tree/course-materials", text)
            for match in builder.MARKDOWN_LINK_PATTERN.finditer(text):
                link = match.group(1).strip().strip("<>").split("#", 1)[0]
                if not link or link.startswith(("https://", "http://", "mailto:")):
                    continue
                target = (path.parent / unquote(link)).resolve()
                self.assertTrue(target.is_relative_to(root.resolve()), (path, link))
                self.assertTrue(target.exists(), (path, link))

    def test_maintenance_word_is_not_a_private_path(self):
        pattern = builder.FORBIDDEN_TEXT_PATTERNS["internal working path"]
        self.assertIsNone(pattern.search("Index maintenance can require additional writes."))
        self.assertIsNotNone(pattern.search("maintenance/chapters/example.md"))
        self.assertIsNotNone(pattern.search("working_materials/chapters/example.md"))

    def test_missing_invalid_and_duplicate_ids_are_rejected(self):
        path = builder.PREVIEW_DIR / "ch02.ipynb"
        original = Path.read_text
        raw = json.loads(path.read_text(encoding="utf-8"))
        for case in ("missing", "invalid", "duplicate"):
            altered = copy.deepcopy(raw)
            if case == "missing":
                altered["cells"][0].pop("id")
            elif case == "invalid":
                altered["cells"][0]["id"] = "invalid id"
            else:
                altered["cells"][1]["id"] = altered["cells"][0]["id"]

            def read(instance, *args, **kwargs):
                return json.dumps(altered) if instance == path else original(instance, *args, **kwargs)

            with self.subTest(case=case), patch.object(Path, "read_text", read):
                with self.assertRaisesRegex(RuntimeError, "cell ID"):
                    builder.verify_content(builder.load_json(builder.CONFIG_PATH))

    def test_unsafe_target_is_rejected(self):
        with self.assertRaises(ValueError):
            builder.safe_target("../PROJECT.md")

    def test_build_preserves_syllabus_and_existing_files_on_failure(self):
        with tempfile.TemporaryDirectory(prefix="db_layout_") as directory:
            root = Path(directory).resolve()
            course = root / "Intro DB"
            course.mkdir()
            syllabus = course / "syllabus.md"
            notebook = course / "ch02.ipynb"
            syllabus.write_text("maintained syllabus", encoding="utf-8")
            notebook.write_text("previous notebook", encoding="utf-8")
            config = {"chapters": [{"id": "ch02"}, {"id": "ch03"}]}
            with patch.object(builder, "PREVIEW_DIR", course), patch.object(builder, "OUTPUT_DIR", root / "output"):
                with patch.object(builder, "build_notebook", side_effect=[{}, RuntimeError("simulated failure")]), \
                     patch.object(builder, "execute_notebook"):
                    with self.assertRaisesRegex(RuntimeError, "simulated failure"):
                        builder.build_preview(config)
                self.assertEqual(notebook.read_text(), "previous notebook")
                self.assertEqual(syllabus.read_text(), "maintained syllabus")
                extra = course / "my_notes.md"
                extra.write_text("keep this", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "nothing removed"):
                    builder.build_preview(config)
                self.assertEqual(extra.read_text(), "keep this")


if __name__ == "__main__":
    unittest.main(verbosity=2)
