"""Check the single-branch layout and ensure builds preserve maintained files."""

import contextlib
import copy
import io
import json
import itertools
from datetime import datetime, timedelta
from graphlib import TopologicalSorter, CycleError
import re
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote

import nbformat

import build_course_repository as builder


class RepositoryLayoutTests(unittest.TestCase):
    def test_execution_preserves_actual_stream_whitespace(self):
        notebook = {"cells": [builder.code_cell('print("result\\n")')]}
        builder.execute_notebook(notebook, "stream-test")
        self.assertEqual("".join(notebook["cells"][0]["outputs"][0]["text"]), "result\n\n")

    def test_syllabus_weekly_chapter_labels_match_plan(self):
        syllabus = (builder.PREVIEW_DIR / "syllabus.md").read_text(encoding="utf-8")
        config = builder.load_json(builder.CONFIG_PATH)
        # Notebook IDs still identify the other textbook; compare current course documents.
        self.assertEqual(config["weeks_status"], "historical_not_current_syllabus")
        self.assertEqual(config["material_status"], "legacy_textbook_alignment_pending")
        plan = builder.safe_source(config["current_course_plan"]).read_text(encoding="utf-8")

        def schedule_rows(text):
            section = text.split("## Weekly Schedule\n", 1)[1].split("\n## ", 1)[0]
            return [[cell.strip() for cell in line.split("|")[1:-1]]
                    for line in section.splitlines() if re.match(r"\| \d+ \|", line)]

        rows, plan_rows = schedule_rows(syllabus), schedule_rows(plan)

        self.assertEqual(len(rows), 18)
        self.assertEqual(len(plan_rows), 18)
        start = datetime(2026, 9, 10)
        for number, (row, planned) in enumerate(zip(rows, plan_rows), 1):
            with self.subTest(week=number):
                self.assertEqual(len(row), 4)
                self.assertEqual(len(planned), 4)
                self.assertEqual(int(row[0]), number)
                self.assertEqual(row[0], planned[0])
                self.assertEqual(row[2], planned[2])
                self.assertLessEqual(len(row[3].split()), 16)
                actual = datetime.strptime(row[1], "%Y-%m-%d")
                self.assertEqual(actual, datetime.strptime(planned[1], "%Y-%m-%d"))
                self.assertEqual(actual, start + timedelta(weeks=number - 1))
                self.assertEqual(actual.weekday(), 3)
        self.assertEqual([int(row[0]) for row in rows if row[3].startswith("Written Exam")], [6, 12, 16])
        self.assertIn("review only", rows[8][3])
        self.assertIn("Written Exam 3", rows[15][3])
        self.assertIn("integrated review", rows[14][3])
        self.assertEqual(rows[16][2], "None")
        self.assertEqual(rows[17][2], "Previously taught sections")
        self.assertIn("Make-up examination", rows[17][3])
        self.assertNotIn("Written Exam 3", rows[17][3])

    def test_final_and_makeup_dates_agree(self):
        syllabus = (builder.PREVIEW_DIR / "syllabus.md").read_text(encoding="utf-8")
        plan = (builder.COURSE_ROOT / "maintenance/COURSE_PLAN.md").read_text(encoding="utf-8")
        self.assertIn("December 24 (Week 16)", syllabus)
        self.assertIn("January 7 (Week 18)", syllabus)
        self.assertIn("no additional assessment weight", syllabus)
        self.assertIn("not a fourth separately", plan)
        for document in (syllabus, plan):
            self.assertIn("January 4-8", document)
        self.assertRegex(plan, r"\| Written Exam 3 \(Final Examination\) \| 2026-12-24 \| 30% \|")
        project = (builder.COURSE_ROOT / "PROJECT.md").read_text(encoding="utf-8")
        self.assertRegex(project, r"\| Written Exam 3 / Final Examination \| Week 16, 2026-12-24 \| 30% \|")

    def test_current_assessment_weights(self):
        expected = {
            "Written Exam 1": "30%", "Written Exam 2": "30%",
            "Written Exam 3 (Final Examination)": "30%", "Class Performance": "10%",
            "Total": "100%",
        }
        for path, weight_column in [(builder.PREVIEW_DIR / "syllabus.md", 1),
                                    (builder.COURSE_ROOT / "maintenance/COURSE_PLAN.md", 2)]:
            with self.subTest(path=path.name):
                section = path.read_text(encoding="utf-8").split("## Assessment\n", 1)[1].split("\n## ", 1)[0]
                rows = [[cell.strip() for cell in line.split("|")[1:-1]]
                        for line in section.splitlines() if line.startswith("| ")]
                actual = {row[0]: row[weight_column] for row in rows if row[0] in expected}
                self.assertEqual(actual, expected)
                self.assertEqual(sum(int(value[:-1]) for key, value in actual.items()
                                     if key != "Total"), 100)

    def test_current_syllabus_scope_and_language(self):
        syllabus = (builder.PREVIEW_DIR / "syllabus.md").read_text(encoding="utf-8")
        self.assertIn("Sections 4.1-4.7", syllabus)
        self.assertIn("Sections 9.1-9.2", syllabus)
        self.assertIn("Ch14-19 use selected concepts", syllabus)
        self.assertIn("Ch20 is not scheduled", syllabus)
        # Full textbook chapter titles add words; weekly topic summaries remain short.
        self.assertLessEqual(len(syllabus.split()), 900)
        self.assertIn("Five group comparisons", syllabus)
        self.assertIn("rankings do not determine grades", syllabus)
        self.assertIn("Written exams are individual and AI-free", syllabus)
        self.assertNotIn("*Database System Concepts*", syllabus)
        self.assertNotRegex(syllabus, r"[\u3400-\u9fff\ufffd]")
        self.assertNotRegex(syllabus, r"(?i)\btype\s*b\b|\b\d+\s*(?:minutes?|mins?)\b")
        for chapter_id in ("ch01", "ch02", "ch05"):
            self.assertIn(f"({chapter_id}.ipynb)", syllabus)

    def test_textbook_details_and_updated_travel(self):
        syllabus = (builder.PREVIEW_DIR / "syllabus.md").read_text(encoding="utf-8")
        textbook = syllabus.split("## Textbook\n", 1)[1].split("\n## ", 1)[0]
        for detail in ("Fundamentals of Database Systems", "Ramez Elmasri",
                       "Shamkant B. Navathe", "7th Edition", "Pearson"):
            self.assertIn(detail, textbook)
        self.assertLess(syllabus.index("## Textbook\n"), syllabus.index("## Course Materials\n"))
        plan = (builder.COURSE_ROOT / "maintenance/COURSE_PLAN.md").read_text(encoding="utf-8")
        for document in (syllabus, plan):
            self.assertIn("November 1-8", document)
            self.assertNotRegex(document, r"November 1-7|November 1 through November 7")
        self.assertIn("in-person classes resume November 12", syllabus)
        project = (builder.COURSE_ROOT / "PROJECT.md").read_text(encoding="utf-8")
        current_dates = project.split("## 115-1 固定日期與進度範圍", 1)[1].split("\n## ", 1)[0]
        self.assertIn("2026-11-08", current_dates)
        self.assertNotIn("2026-11-07", current_dates)

    def test_detailed_coverage_includes_full_eer(self):
        plan = (builder.COURSE_ROOT / "maintenance/COURSE_PLAN.md").read_text(encoding="utf-8")
        coverage = plan.split("## Detailed Coverage\n", 1)[1].split("\n## ", 1)[0]
        rows = [line for line in coverage.splitlines() if re.match(r"\| \d", line)]
        self.assertEqual(len(rows), 14)
        for detail in ("1.1-1.3", "3.1-3.7", "5.1-5.3", "6.1-6.4", "7.1-7.4",
                       "8.1-8.3", "Sections 4.1-4.7", "Sections 9.1-9.2", "14.1-14.5",
                       "15.1-15.3", "Algorithm 15.4", "8A-8D", "16.1-16.8",
                       "17.1-17.4", "17.7", "18.1", "18.3-18.4", "19.1-19.3", "4NF and 5NF",
                       "division and relational calculus", "knowledge representation", "ontology concepts"):
            self.assertIn(detail, coverage)


    def test_syllabus_chapter_titles_and_eer_sequence(self):
        syllabus = (builder.PREVIEW_DIR / "syllabus.md").read_text(encoding="utf-8")
        # Titles checked against the prescribed PDF contents, PDF pages 18-30.
        titles = {
            1: "Databases and Database Users",
            2: "Database System Concepts and Architecture",
            3: "Data Modeling Using the Entity-Relationship (ER) Model",
            4: "The Enhanced Entity-Relationship (EER) Model",
            5: "The Relational Data Model and Relational Database Constraints",
            6: "Basic SQL",
            7: "More SQL: Complex Queries, Triggers, Views, and Schema Modification",
            8: "The Relational Algebra and Relational Calculus",
            9: "Relational Database Design by ER- and EER-to-Relational Mapping",
            14: "Basics of Functional Dependencies and Normalization for Relational Databases",
            15: "Relational Database Design Algorithms and Further Dependencies",
            16: "Disk Storage, Basic File Structures, Hashing, and Modern Storage Architectures",
            17: "Indexing Structures for Files and Physical Database Design",
            18: "Strategies for Query Processing",
            19: "Query Optimization",
        }
        schedule = syllabus.split("## Weekly Schedule\n", 1)[1].split("\n## ", 1)[0]
        rows = [[cell.strip() for cell in line.split("|")[1:-1]]
                for line in schedule.splitlines() if re.match(r"\| \d+ \|", line)]
        seen = set()
        for row in rows:
            for label in row[2].split("<br>"):
                match = re.match(r"Ch(\d+): (.+)", label)
                if match:
                    number = int(match[1])
                    self.assertIn(number, titles)
                    self.assertTrue(match[2].startswith(titles[number]), label)
                    seen.add(number)
                elif row[0] in {"6", "9", "12", "16"}:
                    self.assertRegex(label, r"\bCh\d+")
                else:
                    self.assertNotRegex(label, r"\bCh\d+|Chapter\s+\d")
        self.assertEqual(seen, set(titles))
        for index, fragment in [(2, "(4.1-4.4)"), (3, "(4.5-4.7)"),
                                (9, "(9.1-9.2)"), (10, "(14.1-14.5 selected)"),
                                (10, "(15.1-15.3 selected)")]:
            self.assertIn(fragment, rows[index][2])
        for index, expected in {
            5: "Ch1-6 (taught selections)",
            8: "Ch1-8 (review only)",
            11: "Ch7-9 and Ch14-15 (taught selections)",
            15: "Ch16-19 (selected); cumulative SQL and design",
        }.items():
            self.assertEqual(rows[index][2], expected)
        exam_rows = [line for line in syllabus.splitlines() if line.startswith("| Written Exam")]
        self.assertEqual(len(exam_rows), 3)
        self.assertTrue(all(re.search(r"\bCh\d+", line) for line in exam_rows))
        expected_teaching = {1: [1, 2], 2: [3], 3: [4], 4: [4, 5], 5: [6],
                             7: [7], 8: [8], 10: [9], 11: [14, 15],
                             13: [16], 14: [17], 15: [18, 19]}
        for week, chapters in expected_teaching.items():
            self.assertEqual([int(n) for n in re.findall(r"Ch(\d+):", rows[week-1][2])], chapters)
        self.assertIn("normalization", rows[11][3])
        plan = (builder.COURSE_ROOT / "maintenance/COURSE_PLAN.md").read_text(encoding="utf-8")
        self.assertIn("Weeks 2, 4, 10, 13, and 14", plan)
        project = (builder.COURSE_ROOT / "PROJECT.md").read_text(encoding="utf-8")
        assessment = project.split("## 評量與章節對應", 1)[1].split("\n## ", 1)[0]
        self.assertIn("Ch1-6", assessment)
        self.assertIn("Ch7-9及Ch14-15", assessment)
        self.assertIn("Ch16-19", assessment)
        self.assertIn("不另考Ch20", assessment)

    def test_today_and_notebook_transitions(self):
        home = (builder.COURSE_ROOT / "README.md").read_text(encoding="utf-8")
        today = home.split("## Today:", 1)[1].split("## Course Order", 1)[0]
        self.assertIn("ch01.ipynb", today)
        self.assertIn("ch02.ipynb", today)
        self.assertNotIn("ch05.ipynb", today)
        self.assertIn("Next class: Ch3", home)
        config = builder.load_json(builder.CONFIG_PATH)
        guides = {c["id"]: builder.safe_source(c["guide_source"]).read_text(encoding="utf-8")
                  for c in config["current_chapters"]}
        self.assertIn("Next, Chapter 3", guides["ch02"])
        self.assertIn("Continue with Chapter 6", guides["ch05"])
        self.assertIn("Chapter 9 for ER/EER-to-relational mapping", guides["ch08"])
        prompt = (builder.COURSE_ROOT / "maintenance/database_chapter_teaching_material_prompt.md").read_text(encoding="utf-8")
        self.assertIn("今天只教Ch1/Ch2", prompt)
        self.assertIn("Ch14-Ch19", prompt)
        self.assertNotIn("Ch15：延伸參考", prompt)

    def test_visual_figures_and_unique_anchors(self):
        config = builder.load_json(builder.CONFIG_PATH)
        total = 0
        for chapter in config["chapters"]:
            with self.subTest(chapter=chapter["id"]):
                notebook = builder.build_notebook(chapter)
                attachments = [name for cell in notebook["cells"]
                               for name in cell.get("attachments", {})]
                self.assertEqual(len(attachments), len(set(attachments)))
                baseline = (19 if chapter["id"] == "ch02" else
                            3 if chapter["id"] in {"ch05", "ch06", "ch14", "ch19"} else 2)
                added = sum(e["chapter"] == chapter["id"] for e in builder.EXAMPLES.values())
                self.assertEqual(len(attachments), baseline + added)
                total += len(attachments)
        self.assertEqual(total, 45 + len(builder.EXAMPLES))

    def test_small_examples_have_instruction_and_verified_outputs(self):
        for name, example in builder.EXAMPLES.items():
            with self.subTest(example=name):
                for field in ("heading", "source", "concept", "inputs", "prediction",
                              "interpretation", "practice", "check", "panels"):
                    self.assertTrue(example[field], field)
                self.assertFalse(any(value is None for panel in example["panels"]
                                     for row in panel["rows"] for value in row))
                cells = builder.small_example_cells(example)
                if example["steps"]:
                    self.assertEqual(len(example["steps"]), len(example["outputs"]))
                    notebook = {"cells": [builder.code_cell(builder.SMALL_EXAMPLE_RUNTIME), *cells]}
                    builder.execute_notebook(notebook, name)
                    self.assertTrue(notebook["cells"][-1]["outputs"])

    def test_conceptual_examples_with_separate_calculations(self):
        def closure(start, rules):
            known = set(start)
            while True:
                expanded = known | set().union(*(right for left, right in rules if left <= known))
                if expanded == known:
                    return known
                known = expanded

        rules = [({"employee"}, {"name"}), ({"project"}, {"title"}),
                 ({"employee", "project"}, {"hours"})]
        self.assertEqual(closure({"employee", "project"}, rules),
                         {"employee", "project", "name", "title", "hours"})
        self.assertEqual(closure({"employee"}, rules), {"employee", "name"})
        self.assertEqual(closure({"project"}, rules), {"project", "title"})
        self.assertEqual(len(closure({"project"}, rules + [({"project"}, {"employee"})])), 5)

        attributes = {"student", "course", "teacher"}
        rules = [({"student", "course"}, {"teacher"}), ({"teacher"}, {"course"})]
        keys = []
        for size in range(1, 4):
            for combination in itertools.combinations(sorted(attributes), size):
                key = set(combination)
                if closure(key, rules) == attributes and not any(k <= key for k in keys):
                    keys.append(key)
        self.assertEqual(keys, [{"course", "student"}, {"student", "teacher"}])
        prime = set().union(*keys)
        bcnf = third = True
        for size in range(4):
            for combination in itertools.combinations(sorted(attributes), size):
                left = set(combination)
                determined = closure(left, rules)
                for right in determined - left:
                    bcnf &= determined == attributes
                    third &= determined == attributes or right in prime
        self.assertFalse(bcnf)
        self.assertTrue(third)

        chain = {a: {b} for a, b in builder.EXAMPLES["ch18_small_wait_chain"]["inputs"][0]["rows"]}
        self.assertEqual(list(TopologicalSorter(chain).static_order()), ["T3", "T2", "T1"])
        chain["T3"] = {"T1"}
        with self.assertRaises(CycleError):
            list(TopologicalSorter(chain).static_order())
        chain["T4"] = {"T2"}
        self.assertNotIn("T4", chain["T1"] | chain["T2"] | chain["T3"])

        pairs = builder.EXAMPLES["ch17_small_conflicts"]["inputs"][0]["rows"]
        flags = [a[1] != b[1] and a[3] == b[3] and "w" in (a[0], b[0]) for a, b in pairs]
        self.assertEqual(flags, [False, True, False, True])
        schedule = [event for _, event in builder.EXAMPLES["ch17_small_commit_order"]["inputs"][0]["rows"]]
        self.assertLess(schedule.index("c1"), schedule.index("c2"))
        self.assertGreater(schedule.index("c1"), schedule.index("r2(A)"))

        held = {"A": ("T1", "S"), "B": ("T2", "X")}
        decisions = []
        for mode, item in [("S", "A"), ("X", "A"), ("S", "B"), ("X", "C")]:
            if item not in held or mode == held[item][1] == "S":
                decisions.append("grant")
            else:
                decisions.append("wait for " + held[item][0])
        displayed = builder.EXAMPLES["ch18_small_items"]["panels"][1]["rows"]
        self.assertEqual(decisions, [decision for _, decision in displayed])

        disk = {"A": 8, "B": 4}
        updates = [("T1", "A", 10, 8), ("T2", "B", 7, 4)]
        committed = {"T1"}
        for transaction, item, old, new in updates:
            if transaction in committed:
                disk[item] = new
        for transaction, item, old, new in reversed(updates):
            if transaction not in committed:
                disk[item] = old
        self.assertEqual(list(disk.values()),
                         builder.EXAMPLES["ch19_small_status"]["panels"][2]["rows"][0])

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
        config = builder.load_json(builder.CONFIG_PATH)
        self.assertEqual({p.relative_to(builder.PREVIEW_DIR).as_posix()
                          for p in builder.PREVIEW_DIR.rglob("*") if p.is_file()},
                         builder.expected_files(config))
        builder.validate_config(config)
        with contextlib.redirect_stdout(io.StringIO()):
            builder.verify_content(config)

    def test_raw_notebook_schema(self):
        for path in builder.PREVIEW_DIR.rglob("*.ipynb"):
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
            (course / "under_revision").mkdir()
            syllabus = course / "syllabus.md"
            notebook = course / "under_revision/ch02.ipynb"
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
