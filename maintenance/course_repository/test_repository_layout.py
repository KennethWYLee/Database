"""Check the single-branch layout and ensure builds preserve maintained files."""

import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote

import nbformat

import build_course_repository as builder


class RepositoryLayoutTests(unittest.TestCase):
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
