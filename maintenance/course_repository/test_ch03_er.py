"""Independent checks of Ch3 examples, scope, and ER notation."""
import base64
from collections import Counter
import hashlib
import io
import json
import re
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
from itertools import product
from bs4 import BeautifulSoup
import fitz
from markdown_it import MarkdownIt
from PIL import Image

import build_course_repository as builder
from er_figures import APPROVALS, ENROLLMENTS, FIGURES, SECTIONS, STUDENTS, TEACHES
from er_figures import ORDER_ITEMS, ITEM_NOTES, INTERVIEWS, APPROVAL_ADDITIONS, UNIVERSITY_RELATIONSHIPS


class ERChapterTests(unittest.TestCase):
    def setUp(self):
        self.config = builder.load_json(builder.CONFIG_PATH)
        self.chapter = next(c for c in self.config["current_chapters"] if c["id"] == "ch03")
        self.guide = builder.safe_source(self.chapter["guide_source"]).read_text(encoding="utf-8")

    def test_current_order_and_no_sql(self):
        self.assertEqual([c["id"] for c in self.config["current_chapters"]],
                         ["ch01", "ch02", "ch03", "ch05", "ch08"])
        book = builder.build_notebook(self.chapter)
        self.assertTrue(all(c["cell_type"] == "markdown" for c in book["cells"]))
        self.assertNotIn("CREATE TABLE", builder.notebook_markdown(book))
        self.assertIn("Ch4 adds", self.guide)
        self.assertIn("Relational mapping and SQL implementation come later", self.guide)

    def test_teaching_sections_and_figure_placement(self):
        sections = re.split(r"(?m)^## (?=\d+\. )", self.guide)[1:]
        self.assertEqual(len(sections), 17)
        for index, section in enumerate(sections, 1):
            self.assertIn("Practice" if index == 17 else "**Practice:**", section)
            if index < 17:
                self.assertIn("**Prediction:**", section)
                self.assertRegex(section, r"(?m)^### (Read|Check) ")
        self.assertEqual(len(FIGURES), 45)
        for figure in FIGURES.values():
            for heading in figure["heading"].split(" / "):
                self.assertEqual(self.guide.count(heading + "\n"), 1)
        self.assertIn("either your correction or an explanation", self.guide)
        self.assertIn("Submit only the work the instructor assigns", self.guide)

    def test_snapshot_entities_and_enrollment_counts(self):
        self.assertEqual(len(set(SECTIONS)), 3)
        self.assertTrue(all(s in STUDENTS and (c, n) in SECTIONS for s, c, n, g in ENROLLMENTS))
        self.assertEqual({s: sum(r[0] == s for r in ENROLLMENTS) for s in STUDENTS},
                         {"S101": 2, "S102": 1, "S103": 0})
        self.assertEqual({g for s, c, n, g in ENROLLMENTS if s == "S101"}, {80, 90})
        self.assertEqual({g for s, c, n, g in ENROLLMENTS if (c, n) == ("DB101", 1)}, {80, 70})

    def test_entity_figure_preserves_declared_properties_and_profile_values(self):
        definition, state = FIGURES["opening_ch03_entities"]["panels"]
        self.assertEqual(definition["rows"][0][1].split(", "), state["headers"])
        self.assertEqual(state["rows"], [
            ["S101", "Alex Lin", "02-0000-0101; 02-0000-0102"],
            ["S102", "Blair Wu", "02-0000-0201"],
            ["S103", "Casey Chen", "None recorded"],
        ])
        soup = BeautifulSoup(MarkdownIt("commonmark").enable("table").render(self.guide), "html.parser")
        profile = next(t for t in soup.find_all("table") if "Recorded Phone values" in t.get_text())
        rows = [[cell.get_text() for cell in row.find_all("td")] for row in profile.select("tbody tr")]
        self.assertEqual([[r[0], r[1] + " " + r[2], r[3]] for r in rows], state["rows"])
        self.assertIn("does not mean the student owns no phone", state["note"])

    def test_refinement_preserves_names_and_compares_the_same_sections(self):
        before, instructors, assignments = FIGURES["opening_ch03_refinement"]["panels"]
        self.assertEqual(instructors["headers"], ["InstructorId", "Name"])
        self.assertEqual(assignments["headers"], ["InstructorId", "Section taught"])
        names = dict(instructors["rows"])
        reconstructed = [[section, names[instructor]] for instructor, section in assignments["rows"]]
        self.assertEqual(reconstructed, before["rows"])
        self.assertEqual({row[0] for row in before["rows"]}, {"DB101 / 1", "DB101 / 2"})
        self.assertIn("independently", instructors["note"])
        self.assertIn("Matching names alone do not establish identity", FIGURES["opening_ch03_refinement"]["conclusion"])

    def test_visible_tables_preserve_rows_and_reference_labels(self):
        for name, figure in FIGURES.items():
            for panel in figure["panels"]:
                self.assertTrue(all(len(row) == len(panel["headers"]) for row in panel["rows"]), name)
        enrollment, _ = FIGURES["opening_ch03_relationships"]["panels"]
        self.assertEqual(enrollment["headers"][-1], "Grade")
        self.assertEqual(enrollment["rows"], [[s, f"{c} / {n}", str(g)] for s, c, n, g in ENROLLMENTS])
        approvals, references = FIGURES["opening_ch03_pairs"]["panels"]
        self.assertEqual(approvals["headers"][0], "Record")
        records = {row[0]: row[1:] for row in approvals["rows"]}
        self.assertEqual(list(records.values()), [list(row) for row in APPROVALS])
        for pair, record in references["rows"]:
            self.assertTrue(set(pair.split(" + ")).issubset(records[record]))

    def test_weak_figures_account_for_input_properties(self):
        d = FIGURES["opening_ch03_order_items"]["diagram"]
        nodes = {n["id"]: n for n in d["nodes"]}
        attrs = {nodes[e["b"]]["label"] for e in d["edges"]
                 if e["a"] == "i" and nodes[e["b"]]["kind"] == "attribute"}
        self.assertEqual(attrs, {"LineNo", "Product", "Quantity"})
        self.assertIsNone(nodes["product"]["key"])
        self.assertIsNone(nodes["qty"]["key"])
        self.assertIn("Only identifying attributes are shown", FIGURES["opening_ch03_nested_weak"]["conclusion"])
        owners = FIGURES["opening_ch03_two_owners"]["diagram"]["nodes"]
        self.assertEqual({n["label"] for n in owners if n["key"] == "full"}, {"StudentId", "CompanyId"})

    def test_recursive_caption_does_not_add_a_distinct_person_rule(self):
        caption = FIGURES["opening_ch03_roles"]["conclusion"]
        self.assertNotIn("another", caption)
        self.assertIn("two roles", caption)
        self.assertIn("do not forbid self-mentoring", caption)
        rows = [("S101", "S102"), ("S101", "S103"), ("S101", "S101")]
        self.assertTrue(all(sum(mentee == s for _, mentee in rows) <= 1 for s in STUDENTS))
        self.assertIn("forbidding it needs a separate rule", self.guide)

    def test_two_checks_remain_on_the_same_visible_row(self):
        panels = FIGURES["opening_ch03_ternary_checks"]["panels"]
        self.assertEqual(len(panels), 1)
        self.assertEqual(len(panels[0]["headers"]), 4)
        for addition, displayed in zip(APPROVAL_ADDITIONS, panels[0]["rows"], strict=True):
            s, i, c = addition
            before = sum(ii == i for _, ii, _ in APPROVALS)
            pair_ok = not any(ss == s and cc == c and ii != i for ss, ii, cc in APPROVALS)
            count_ok = before + 1 <= 2
            self.assertEqual(displayed[0], ", ".join(addition))
            self.assertEqual(displayed[1].split(":")[0], "Yes" if pair_ok else "No")
            self.assertEqual(displayed[2], f"{'Yes' if count_ok else 'No'}: {i} goes from {before} to {before + 1}")
            self.assertEqual(displayed[3], "Yes" if pair_ok and count_ok else "No")

    def test_conflict_figure_keeps_case_data_with_its_result(self):
        panels = FIGURES["opening_ch03_university_conflicts"]["panels"]
        self.assertEqual(len(panels), 1)
        self.assertEqual(panels[0]["rows"], [
            ["A: Q101 / Q102", "DB101; Fall 2026; SecNo 1", "Duplicate local section number"],
            ["B: Q201 / Q202", "Fall 2026; room A/201; Thu-P5", "Room occupied at the same time"],
            ["C: Q301 / Q302", "Fall 2026; instructor I1; Thu-P5", "Instructor teaching at the same time"],
        ])
        self.assertIn("combined sections are not permitted", panels[0]["note"])

    def test_stacked_panels_do_not_overlap(self):
        ns = {"s": "http://www.w3.org/2000/svg"}
        for name in ("entities", "refinement", "pairs"):
            root = ET.fromstring(builder.generate_figure("opening_ch03_" + name))
            rows = [e for e in root.findall("s:rect", ns) if e.get("stroke") == "#9eafb8"]
            self.assertTrue(all(float(e.get("width")) == 1110 for e in rows))
            for first, second in zip(rows, rows[1:]):
                self.assertLessEqual(float(first.get("y")) + float(first.get("height")), float(second.get("y")))

    @unittest.skipUnless(builder.safe_target("ch03.ipynb").exists() and builder.safe_target("ch03.pdf").exists(),
                         "The Ch3 notebook/PDF export was retired; source checks remain active.")
    def test_pdf_retains_the_current_notebook_figure_pixels(self):
        notebook = json.loads(builder.safe_target("ch03.ipynb").read_text(encoding="utf-8"))
        self.assertEqual(notebook, builder.build_notebook(self.chapter))

        def pixels(data):
            with Image.open(io.BytesIO(data)) as image:
                rgb = image.convert("RGB")
                return rgb.size, hashlib.sha256(rgb.tobytes()).hexdigest()

        original = [pixels(base64.b64decode(value["image/png"]))
                    for cell in notebook["cells"] for value in cell.get("attachments", {}).values()]
        with fitz.open(builder.safe_target("ch03.pdf")) as pdf:
            exported = [pixels(pdf.extract_image(info[0])["image"])
                        for page in pdf for info in page.get_images(full=True)]
        self.assertEqual(len(original), 45)
        self.assertEqual(Counter(exported), Counter(original))

    def test_reading_labels_match_the_visual_content(self):
        cells = builder.build_notebook(self.chapter)["cells"]
        expected = {
            "Read the ER Steps": ("requirements_steps", "er"),
            "Read the Entity Tables": ("entities", "tables"),
            "Read the Domain Tables": ("domains", "tables"),
            "Read the Enrollment Tables": ("relationships", "tables"),
            "Read the Design Tables": ("refinement", "tables"),
            "Read the ER Comparison": ("refinement_er", "er"),
            "Read the Section Instances": ("section_owners", "network"),
            "Read the Weak-Entity Diagram": ("weak", "er"),
            "Read the Global-ID Diagram": ("section_global_id", "er"),
        }
        seen = set()
        for i, cell in enumerate(cells):
            heading = "".join(cell["source"]).splitlines()[0]
            names = list(cells[i-1].get("attachments", {})) if i else []
            if re.fullmatch(r"### Read the (?:.* )?Diagram", heading):
                self.assertEqual(len(names), 1)
                self.assertEqual(FIGURES[names[0][:-4]]["kind"], "er", heading)
            if heading.removeprefix("### ") in expected:
                title = heading.removeprefix("### ")
                name, kind = expected[title]
                self.assertEqual(names, ["opening_ch03_" + name + ".png"])
                self.assertEqual(FIGURES["opening_ch03_" + name]["kind"], kind)
                seen.add(title)
            if heading == "### Read the Approval Diagram and Tables":
                self.assertEqual(names, ["opening_ch03_pairs.png"])
                self.assertIn("opening_ch03_ternary.png", cells[i-2]["attachments"])
        self.assertEqual(seen, set(expected))

    def test_weak_example_starts_with_objects_before_terms_and_symbols(self):
        weak = self.guide.split("## 12. Weak Entities and Partial Keys", 1)[1].split("## 13.", 1)[0]
        self.assertLess(weak.index('Which class do you mean'), weak.index('Weak entity type: SECTION'))
        self.assertLess(weak.index('### Read the Section Instances'), weak.index('### From the Example to ER Symbols'))
        for value in ('DB101 / 1; CS102 / 1', 'DB101 / 1; DB101 / 2',
                      'Double rectangle around SECTION', 'Double diamond around HAS_SECTION',
                      'does not mean two courses', 'no other identifying attributes of its own'):
            self.assertIn(value, weak)
        self.assertIn('not a conclusion drawn only from three sample', weak)
        graph = FIGURES['opening_ch03_section_owners']['graph']
        starts = {(x+w, y+h/2): label for x,y,w,h,label in graph['nodes']}
        ends = {(x, y+h/2): label for x,y,w,h,label in graph['nodes']}
        self.assertEqual({(starts[x1,y1], ends[x2,y2]) for x1,y1,x2,y2,*_ in graph['edges']},
                         {('Course '+c, f'Section {c} / {n}') for c,n in SECTIONS})

    def test_global_identifier_changes_weakness_but_not_owner_requirement(self):
        original = FIGURES['opening_ch03_weak']['diagram']
        revised = FIGURES['opening_ch03_section_global_id']['diagram']
        before = {n['id']: n for n in original['nodes']}
        after = {n['id']: n for n in revised['nodes']}
        self.assertEqual(before['s']['kind'], 'weak')
        self.assertEqual(before['h']['kind'], 'identifying')
        self.assertEqual(before['no']['key'], 'partial')
        self.assertEqual(after['s']['kind'], 'entity')
        self.assertEqual(after['r']['kind'], 'relationship')
        self.assertEqual(after['sid']['key'], 'full')
        self.assertIsNone(after['no']['key'])
        self.assertTrue(next(e['total'] for e in original['edges'] if (e['a'],e['b']) == ('h','s')))
        self.assertTrue(next(e['total'] for e in revised['edges'] if (e['a'],e['b']) == ('r','s')))
        soup = BeautifulSoup(MarkdownIt('commonmark').enable('table').render(self.guide), 'html.parser')
        table = next(t for t in soup.find_all('table') if 'New SectionId' in t.get_text())
        rows = [[td.get_text() for td in tr.find_all('td')] for tr in table.select('tbody tr')]
        self.assertEqual(rows, [['Q01','DB101','1'], ['Q02','DB101','2'], ['Q03','CS102','1']])
        self.assertEqual(len({r[0] for r in rows}), 3)
        self.assertEqual([(r[1],int(r[2])) for r in rows], list(SECTIONS))

    def test_new_er_steps_and_refinement_have_the_explained_connections(self):
        steps = FIGURES["opening_ch03_requirements_steps"]["diagram"]
        self.assertEqual({(e["a"], e["b"], e["total"]) for e in steps["edges"]},
                         {("c2", "r2", False), ("r2", "s2", False),
                          ("c3", "r3", False), ("r3", "s3", True)})
        refinement = FIGURES["opening_ch03_refinement_er"]["diagram"]
        links = {(e["a"], e["b"]): e for e in refinement["edges"]}
        self.assertIn(("before", "teacher"), links)
        self.assertNotIn(("s", "teacher"), links)
        self.assertIn(("i", "name"), links)
        self.assertIn(("i", "iid"), links)
        self.assertIn(("i", "t"), links)
        self.assertTrue(links["t", "s"]["total"])
        nodes = {n["id"]: n for n in refinement["nodes"]}
        self.assertEqual(nodes["iid"]["key"], "full")
        for node_id in ("before", "s"):
            self.assertEqual(nodes[node_id]["kind"], "weak")
        for node_id in ("bn", "sn"):
            self.assertEqual(nodes[node_id]["key"], "partial")
        self.assertIn("omitted from both close-ups", FIGURES["opening_ch03_refinement_er"]["conclusion"])

    @unittest.skipUnless(builder.safe_target("ch03.pdf").exists(), "The Ch3 notebook PDF was retired.")
    def test_pdf_reading_starts_share_a_page_with_the_referenced_visual(self):
        import export_chapter_pdfs as exporter
        exporter.OUT.mkdir(parents=True, exist_ok=True)
        exporter.make_html("ch03")
        soup = BeautifulSoup((exporter.OUT / "ch03.html").read_text(encoding="utf-8"), "html.parser")
        with fitz.open(builder.safe_target("ch03.pdf")) as pdf:
            pages = [" ".join(p.get_text().split()) for p in pdf]
            for group in soup.select(".visual-reading"):
                title = group.select_one(".figure-cell h3").get_text()
                first_block = group.find(["p", "ul", "ol"], recursive=False)
                matching = [i for i, text in enumerate(pages) if title in text]
                self.assertEqual(len(matching), 1, title)
                points = first_block.find_all("li") if first_block.name in {"ul", "ol"} else [first_block]
                for point in points:
                    beginning = " ".join(point.get_text().split())[:75]
                    self.assertIn(beginning, pages[matching[0]], title)
                self.assertTrue(pdf[matching[0]].get_images(), title)
                if title == "A section needs its owner to be identified":
                    self.assertIn('Where to point in the diagram', pages[matching[0]])
                    self.assertIn('1 near COURSE and N near SECTION', pages[matching[0]])

    def test_weak_entity_explanations_use_short_points_without_losing_tables(self):
        section = self.guide.split("## 12. Weak Entities and Partial Keys", 1)[1].split("## 13.", 1)[0]
        soup = BeautifulSoup(MarkdownIt("commonmark").enable("table").render(section), "html.parser")
        readings = [h for h in soup.find_all("h3") if h.get_text().startswith(("Read ", "Check "))]
        self.assertEqual(len(readings), 9)
        for heading in readings:
            block = heading.find_next_sibling()
            self.assertIn(block.name, {"ul", "ol"}, heading.get_text())
            points = block.find_all("li", recursive=False)
            self.assertLessEqual(len(points), 6)
            for point in points:
                self.assertLessEqual(len(point.get_text(" ", strip=True).split()), 35, point.get_text())
        self.assertEqual(len(soup.find_all("table")), 11)

    def test_worked_examples_include_prediction_and_explanation(self):
        sections = builder.split_guide(self.guide, True)
        worked = [i for i, section in enumerate(sections)
                  if section.startswith("### Worked Example:")]
        self.assertEqual(len(worked), 13)
        lecture_figures = [f for f in FIGURES.values() if " / ### Worked Example:" in f["heading"]]
        self.assertEqual(len(lecture_figures), 14)
        for index in worked:
            self.assertIn("**Prediction:**", sections[index])
            self.assertTrue(sections[index+1].startswith("### Read "))
            explanation = sections[index+1].split("**Practice:**")[0]
            self.assertGreater(len(explanation.split()), 35)
        self.assertIn("without requiring you to complete", self.guide)
        self.assertIn("Practice provides additional variations", self.guide)

    def test_instance_lines_match_the_recorded_facts(self):
        expected = {
            "enrollment_links": {("Student " + s, f"Section {c} / {n}") for s, c, n, _ in ENROLLMENTS},
            "one_to_one": {("Student S101", "Card K10"), ("Student S102", "Card K11")},
            "one_to_many": {("Instructor " + i, f"Section {c} / {n}") for i, c, n in TEACHES},
            "mentor_roles": {("Mentor S101", "Mentee S102"), ("Mentor S101", "Mentee S103")},
        }
        for name, pairs in expected.items():
            figure = FIGURES["opening_ch03_" + name]
            graph = figure["graph"]
            starts = {(x+w, y+h/2): label for x, y, w, h, label in graph["nodes"]}
            ends = {(x, y+h/2): label for x, y, w, h, label in graph["nodes"]}
            actual = {(starts[x1, y1], ends[x2, y2]) for x1, y1, x2, y2, *_ in graph["edges"]}
            self.assertEqual(actual, pairs, name)
            self.assertFalse(graph["directed"])
        graph = FIGURES["opening_ch03_enrollment_links"]["graph"]
        self.assertIn("Student S103", {n[-1] for n in graph["nodes"]})
        self.assertIn("Section DB101 / 2", {n[-1] for n in graph["nodes"]})

    def test_contact_components_and_explicit_missing_meanings(self):
        diagram = FIGURES["opening_ch03_contact"]["diagram"]
        self.assertEqual(next(n["kind"] for n in diagram["nodes"] if n["id"] == "contact"), "multi")
        self.assertEqual({e["b"] for e in diagram["edges"] if e["a"] == "contact"}, {"label", "number"})
        rows = FIGURES["opening_ch03_missing_values"]["panels"][0]["rows"]
        self.assertEqual([row[2] for row in rows], ["Known numeric value", "Unknown grade, not a zero",
                                                 "Not applicable", "Unknown whether a value exists"])
        self.assertIn("replaces the bare Phone list", self.guide)

    def test_room_and_item_lookup_tables_are_computed_from_inputs(self):
        rooms = (("A", 101), ("A", 102), ("B", 101))
        checks = [lambda b, n: n == 101, lambda b, n: b == "A", lambda b, n: (b, n) == ("A", 101)]
        for row, check in zip(FIGURES["opening_ch03_key_lookup"]["panels"][0]["rows"], checks):
            matches = [f"{b}/{n}" for b, n in rooms if check(b, n)]
            self.assertEqual(row[1], "; ".join(matches))
            self.assertEqual(int(row[2]), len(matches))
        checks = [lambda o, n, p, q: n == 1, lambda o, n, p, q: (p, q) == ("Notebook", 2),
                  lambda o, n, p, q: o == "O10", lambda o, n, p, q: (o, n) == ("O10", 1)]
        for row, check in zip(FIGURES["opening_ch03_weak_lookup"]["panels"][0]["rows"], checks):
            self.assertEqual(row[1], "; ".join(f"{o}/{n}" for o, n, p, q in ORDER_ITEMS if check(o, n, p, q)))

    def test_grade_matrix_retains_exact_facts_and_absences(self):
        p = FIGURES["opening_ch03_grade_matrix"]["panels"][0]
        facts = {(s, f"{c} / {n}"): str(g) for s, c, n, g in ENROLLMENTS}
        for row in p["rows"]:
            for column, value in zip(p["headers"][1:], row[1:]):
                self.assertEqual(value, facts.get((row[0], column), "No enrollment"))
        self.assertEqual(sum(value != "No enrollment" for row in p["rows"] for value in row[1:]), 3)
        self.assertIn("existing enrollment whose grade is unknown", p["note"])

    def test_assignment_changes_and_notation_counts(self):
        states = [TEACHES, tuple(t for t in TEACHES if t != ("I1", "DB101", 2)),
                  (*TEACHES, ("I2", "DB101", 1)),
                  tuple(("I2", c, n) if (c, n) == ("DB101", 2) else (i, c, n) for i, c, n in TEACHES)]
        decisions = []
        for state in states:
            counts = [sum((c, n) == section for _, c, n in state) for section in SECTIONS]
            decisions.append(all(count == 1 for count in counts))
        self.assertEqual(decisions, [True, False, False, True])
        rows = FIGURES["opening_ch03_participation_changes"]["panels"][0]["rows"]
        self.assertEqual([row[2].startswith("Allowed:") for row in rows], decisions)
        self.assertEqual([row[1] for row in rows], ["I3: 0 sections", "DB101/2: 0 instructors",
                         "DB101/1: 2 instructors", "DB101/2: 1 instructor; I2: 2 sections"])
        count_rows = FIGURES["opening_ch03_notation_counts"]["panels"][0]["rows"]
        self.assertEqual(count_rows[0][1], f"{sum(i == 'I1' for i, _, _ in TEACHES)} sections")
        self.assertEqual(count_rows[1][1], f"{sum((c, n) == ('DB101', 1) for _, c, n in TEACHES)} instructor")

    def test_two_approval_states_retain_identical_pairs(self):
        first = set(APPROVALS)
        second = first | {("S101", "I1", "CS102")}
        rows = FIGURES["opening_ch03_ternary_states"]["panels"][0]["rows"]
        self.assertEqual(rows[0][1:], [str(len(first)), str(len(second))])
        for row, columns in zip(rows[1:4], [(0, 1), (0, 2), (1, 2)]):
            before = {tuple(r[c] for c in columns) for r in first}
            after = {tuple(r[c] for c in columns) for r in second}
            displayed = {tuple(pair.split("/")) for pair in row[1].split("; ")}
            self.assertEqual(displayed, before)
            self.assertEqual(before, after)
            self.assertEqual(row[2], "Same three pairs")
        self.assertIn("limits are not imposed", FIGURES["opening_ch03_ternary_states"]["panels"][0]["note"])

    def test_university_worked_facts_and_distinct_participants(self):
        table = FIGURES["opening_ch03_university_staff_facts"]["panels"][0]["rows"]
        facts = {r[0]: [tuple(p.split(" / ")) for p in r[1].split("; ")] for r in table}
        self.assertEqual({i for _, i in facts["EMPLOYS"]}, {"I1", "I2", "I3"})
        self.assertNotIn("I3", {i for _, i in facts["CHAIR"]})
        self.assertTrue(all(sum(ii == i for _, ii in facts["EMPLOYS"]) == 1 for i in ("I1", "I2", "I3")))
        self.assertEqual({d for d, _ in facts["CHAIR"]}, {"D1", "D2"})
        rows = FIGURES["opening_ch03_university_enrollment_change"]["panels"][0]["rows"]
        self.assertEqual([len(set(r[1].split("; "))) for r in rows], [5, 4, 4])
        self.assertEqual([r[2].split(":")[0] for r in rows], ["5", "4", "Still 4"])

    def test_titles_and_captions_are_outside_images_only(self):
        ns = {"s": "http://www.w3.org/2000/svg"}
        for definition in builder.chapter_figures(self.chapter):
            name = definition["generator"]
            data = FIGURES[name]
            self.assertTrue(data["text_outside_image"])
            cells = builder.generated_figure_cells(self.chapter, definition["after_heading"])
            cell = next(c for c in cells if definition["filename"] in c.get("attachments", {}))
            soup = BeautifulSoup(MarkdownIt().render("".join(cell["source"])), "html.parser")
            self.assertEqual([h.get_text() for h in soup.find_all("h3")], [data["title"]])
            paragraphs = [p.get_text() for p in soup.find_all("p") if not p.find("img")]
            self.assertEqual(paragraphs, [data["conclusion"]])
            root = ET.fromstring(builder.generate_figure(name))
            visible = " ".join("".join(t.itertext()) for t in root.findall(".//s:text", ns))
            self.assertNotIn(data["title"], visible)
            self.assertNotIn(data["conclusion"], visible)
            self.assertNotIn("Original teaching illustration", visible)
            self.assertEqual(root.find("s:title", ns).text, data["title"])
            self.assertEqual(root.find("s:desc", ns).text, data["conclusion"])

    def test_removing_duplicate_labels_preserves_all_figure_body_words(self):
        ns = {"s": "http://www.w3.org/2000/svg"}

        def words(text):
            return Counter(re.findall(r"[A-Za-z0-9_]+", text))

        def visible_words(svg):
            root = ET.fromstring(svg)
            return words(" ".join("".join(t.itertext()) for t in root.findall(".//s:text", ns)))

        for name, data in FIGURES.items():
            current = visible_words(builder.generate_figure(name))
            with patch.dict(data, text_outside_image=False):
                previous = visible_words(builder.generate_figure(name))
            subtitle = (data.get("subtitle", "Original synthetic campus example") if data["kind"] == "er"
                        else "Original teaching illustration | Read with the worked example")
            removed = words(" ".join((data["title"], subtitle, data["conclusion"])))
            self.assertEqual(current + removed, previous, name)

    @unittest.skipUnless(builder.safe_target("ch03.pdf").exists(), "The Ch3 notebook PDF was retired.")
    def test_pdf_retains_searchable_figure_titles_once(self):
        with fitz.open(builder.safe_target("ch03.pdf")) as pdf:
            text = " ".join(" ".join(page.get_text().split()) for page in pdf)
        for data in FIGURES.values():
            self.assertEqual(text.count(data["title"]), 1, data["title"])

    def test_teacher_constraint_and_counterexample(self):
        owners = {(c, n): [i for i, cc, nn in TEACHES if (cc, nn) == (c, n)] for c, n in SECTIONS}
        self.assertTrue(all(len(value) == 1 for value in owners.values()))
        self.assertEqual(sum(i == "I1" for i, _, _ in TEACHES), 2)
        changed = [*TEACHES, ("I2", "DB101", 1)]
        self.assertEqual(sum((c, n) == ("DB101", 1) for i, c, n in changed), 2)

    def test_partial_and_composite_keys(self):
        self.assertLess(len({n for c, n in SECTIONS}), len(SECTIONS))
        self.assertIn(("CS102", 1), SECTIONS)
        self.assertIn(("DB101", 1), SECTIONS)
        rooms = {("A", 101), ("A", 102), ("B", 101)}
        self.assertEqual(len(rooms), 3)
        self.assertEqual(len({x for x, _ in rooms}), 2)
        self.assertEqual(len({x for _, x in rooms}), 2)
        keyed = [n["id"] for n in FIGURES["opening_ch03_keys"]["diagram"]["nodes"] if n["key"]]
        self.assertEqual(keyed, ["loc"])

    def test_ternary_counterexample_from_exact_inputs(self):
        triples = set(APPROVALS)
        si = {(s, i) for s, i, c in triples}
        sc = {(s, c) for s, i, c in triples}
        ic = {(i, c) for s, i, c in triples}
        reconstructed = {(s, i, c) for s, i, c in product({s for s, _, _ in triples},
                         {i for _, i, _ in triples}, {c for _, _, c in triples})
                         if (s, i) in si and (s, c) in sc and (i, c) in ic}
        self.assertEqual(reconstructed - triples, {("S101", "I1", "CS102")})
        self.assertEqual({(s, i) for s, i, c in reconstructed}, si)
        self.assertEqual({(s, c) for s, i, c in reconstructed}, sc)
        self.assertEqual({(i, c) for s, i, c in reconstructed}, ic)

    def test_weak_shapes_and_undirected_lines(self):
        ns = {"s": "http://www.w3.org/2000/svg"}
        root = ET.fromstring(builder.generate_figure("opening_ch03_weak"))
        groups = {g.attrib["data-id"]: g for g in root.findall("s:g", ns)}
        self.assertEqual(len(groups["s"].findall("s:rect", ns)), 2)
        self.assertEqual(len(groups["h"].findall("s:polygon", ns)), 2)
        self.assertIn("stroke-dasharray", groups["no"].find("s:line", ns).attrib)
        self.assertNotIn("stroke-dasharray", groups["id"].find("s:line", ns).attrib)
        for name in FIGURES:
            svg = builder.generate_figure(name)
            self.assertNotIn("marker-end", svg)
            ET.fromstring(svg)

    def test_core_edges_and_attributes(self):
        d = FIGURES["opening_ch03_complete"]["diagram"]
        nodes = {n["id"]: n for n in d["nodes"]}
        endpoints = {(e["a"], e["b"]): e for e in d["edges"]}
        self.assertEqual({e["a"] for e in d["edges"] if e["b"] == "a"} |
                         {e["b"] for e in d["edges"] if e["a"] == "a"}, {"s", "i", "c"})
        self.assertEqual(nodes["q"]["kind"], "weak")
        self.assertEqual(nodes["no"]["key"], "partial")
        self.assertEqual(nodes["phone"]["kind"], "multi")
        self.assertTrue(endpoints[("h", "q")]["total"])
        self.assertTrue(endpoints[("t", "q")]["total"])
        self.assertFalse(endpoints[("s", "e")]["total"])

    def test_additional_owner_identification_examples(self):
        self.assertEqual(len({(o, n) for o, n, _, _ in ORDER_ITEMS}), 3)
        self.assertLess(len({n for _, n, _, _ in ORDER_ITEMS}), 3)
        self.assertLess(len({(line, note) for _, line, note in ITEM_NOTES}), len(ITEM_NOTES))
        self.assertEqual(len(set(ITEM_NOTES)), 3)
        self.assertEqual(len(set(INTERVIEWS)), 3)
        self.assertLess(len({(s, v) for s, _, v in INTERVIEWS}), 3)
        self.assertLess(len({(c, v) for _, c, v in INTERVIEWS}), 3)
        d = FIGURES["opening_ch03_strong_card"]["diagram"]
        self.assertEqual(next(n for n in d["nodes"] if n["id"] == "c")["kind"], "entity")
        self.assertTrue(next(e for e in d["edges"] if e["b"] == "c")["total"])

    def test_two_ternary_rules_are_independent(self):
        results = []
        for addition in APPROVAL_ADDITIONS:
            rows = set(APPROVALS) | {addition}
            pairs = {(s, c) for s, i, c in rows}
            pair_ok = all(len({i for ss, i, cc in rows if (ss, cc) == (s, c)}) <= 1
                          for s, c in pairs)
            count_ok = all(sum(ii == i for _, ii, _ in rows) <= 2
                           for i in {i for _, i, _ in rows})
            results.append((pair_ok, count_ok))
        self.assertEqual(results, [(False, True), (True, False), (True, True)])

    def test_university_constraints_preserve_source_difference(self):
        rules = {r[0]: r for r in UNIVERSITY_RELATIONSHIPS}
        self.assertEqual(len(rules), 9)
        self.assertEqual(rules["HAS"], ("HAS", "DEPT", "(0,N)", "STUDENT", "(0,1)"))
        self.assertEqual(rules["TAKES"], ("TAKES", "STUDENT", "(0,N)", "SECTION", "(5,N)"))
        self.assertEqual(rules["TEACHES"][-1], "(1,1)")
        self.assertIn("source inconsistency", self.guide)
        self.assertIn("the prose version would instead use (1,1)", self.guide)
        d = FIGURES["opening_ch03_university_section"]["diagram"]
        nodes = {n["id"]: n for n in d["nodes"]}
        self.assertEqual(nodes["s"]["kind"], "entity")
        self.assertEqual(nodes["id"]["key"], "full")
        self.assertIsNone(nodes["no"]["key"])
        self.assertEqual({(e["a"], e["b"]) for e in d["edges"] if e["a"] == "room"},
                         {("room", "b"), ("room", "r")})
        enrollment = {(f"U{i}", "Q101") for i in range(1, 6)}
        self.assertEqual(len(enrollment), 5)
        enrollment.remove(("U5", "Q101"))
        self.assertLess(len(enrollment), 5)

    def test_university_extra_uniqueness_checks(self):
        # A different global ID leaves each local collision unchanged.
        original = dict(SecId="Q101", Course="DB101", Sem="Fall", Year=2026,
                        SecNo=1, Room="A/201", Time="Thu-P5", Instructor="I1")
        for keys, changed, collision in [
            (("Course", "Sem", "Year", "SecNo"), dict(SecId="Q102", Room="B/201", Instructor="I2"), True),
            (("Sem", "Year", "Room", "Time"), dict(SecId="Q202", Course="CS102", Instructor="I2"), True),
            (("Sem", "Year", "Instructor", "Time"), dict(SecId="Q302", Course="CS102", Room="B/201"), True),
            (("Course", "Sem", "Year", "SecNo"), dict(SecId="Q102", Sem="Spring", Year=2027), False),
        ]:
            other = dict(original, **changed)
            self.assertNotEqual(original["SecId"], other["SecId"])
            self.assertEqual(tuple(original[k] for k in keys) == tuple(other[k] for k in keys), collision)

    def test_language_and_public_boundary(self):
        prohibited = r"(?i)\btype\s*b\b|\b\d+\s*(?:minutes?|mins?)\b|[\u3400-\u9fff\ufffd]"
        self.assertNotRegex(self.guide, prohibited)
        self.assertNotRegex("a strong entity type because it has its own key", prohibited)
        self.assertRegex("Type B", prohibited)
        self.assertNotRegex(self.guide, r"(?i)C:[/\\]|private_references|maintenance/|answer key|API[_ -]?KEY")
        self.assertIn("All campus records are synthetic", self.guide)
        self.assertIn("Fall 2026 only", self.guide)
        self.assertIn("No SQL", self.guide)
        self.assertIn("Peer ranking does not determine grades", self.guide)

    def test_photographed_source_correction(self):
        self.assertIn("underlines both CCode and CoName", self.guide)
        self.assertNotIn("underlines CCode but not CoName", self.guide)
        self.assertIn("3.5, p.109", self.guide)
        self.assertIn("3.9.2, pp.121-122", self.guide)
        self.assertIn("3.10, pp.122-124", self.guide)
        self.assertNotRegex(self.guide, r"pp\.92-94|(?<!p)p\.93\b")


if __name__ == "__main__":
    unittest.main()
