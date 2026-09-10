"""Independent checks of Ch3 examples, scope, and ER notation."""
import re
import unittest
import xml.etree.ElementTree as ET
from itertools import product

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
        self.assertEqual(len(FIGURES), 27)
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
        self.assertNotRegex(self.guide, r"(?i)type\s*b|\b\d+\s*(?:minutes?|mins?)\b|[\u3400-\u9fff\ufffd]")
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
