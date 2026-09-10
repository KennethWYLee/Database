"""Original Chapter 3 ER diagrams, independent of textbook artwork."""
from html import escape
import math

FIGURES = {}
STUDENTS = ("S101", "S102", "S103")
SECTIONS = (("DB101", 1), ("DB101", 2), ("CS102", 1))
ENROLLMENTS = (("S101", "DB101", 1, 80), ("S101", "CS102", 1, 90),
               ("S102", "DB101", 1, 70))
TEACHES = (("I1", "DB101", 1), ("I1", "DB101", 2), ("I2", "CS102", 1))
APPROVALS = (("S101", "I1", "DB101"), ("S101", "I2", "CS102"),
             ("S102", "I1", "CS102"))


def node(id, label, kind, x, y, w=None, h=None, key=None):
    sizes = {"entity": (220, 74), "weak": (220, 74), "attribute": (210, 72),
             "multi": (210, 72), "derived": (285, 72),
             "relationship": (300, 140), "identifying": (320, 155)}
    width, height = sizes[kind]
    return dict(id=id, label=label, kind=kind, x=x, y=y, w=w or width, h=h or height, key=key)


def edge(a, b, total=False, points=None):
    return dict(a=a, b=b, total=total, points=points)


def add(name, section, title, conclusion, height=None, nodes=(), edges=(), notes=(), panels=()):
    FIGURES["opening_ch03_" + name] = dict(
        heading="## " + section, title=title, conclusion=conclusion,
        kind="er" if height else "tables", arrows=False, panels=panels,
        diagram=dict(height=height, nodes=list(nodes), edges=list(edges), notes=list(notes)))


def panel(title, headers, rows, note=""):
    return dict(title=title, headers=headers, rows=rows, note=note, marks=())


add("requirements", "1. From Requirements to a Diagram", "Start with facts and rules",
    "An ER diagram describes the miniworld before relational mapping or storage choices.",
    panels=[panel("Requirement", ["Given statement", "Design question"],
                  [["Each section belongs to one course.", "Which objects are related?"],
                   ["Section numbers repeat across courses.", "What identifies a section?"]]),
            panel("Conceptual decision", ["Object or rule", "ER representation"],
                  [["COURSE and SECTION", "Entity types"],
                   ["One owner per section", "Relationship and constraints"]])])
add("entities", "2. Entity, Entity Type, and Entity Set", "One entity is not the whole entity type",
    "STUDENT is the type; S101 is one entity; these three students form the displayed current set.",
    panels=[panel("Type description", ["Type", "Properties"], [["STUDENT", "StudentId, Name, Phone"]]),
            panel("Current illustrative set", ["StudentId", "Name"],
                  [["S101", "Alex Lin"], ["S102", "Blair Wu"], ["S103", "Casey Chen"]],
                  "Adding S104 changes the set, not the type definition.")])
add("attributes", "3. Attributes Describe an Entity", "Different attribute properties use different symbols",
    "Name has components; Phone can have several values; EnrollmentCount is calculated from enrollments.",
    500,
    [node("s", "STUDENT", "entity", 600, 280),
     node("id", "StudentId", "attribute", 210, 130, key="full"),
     node("name", "Name", "attribute", 600, 130),
     node("first", "GivenName", "attribute", 425, 20),
     node("last", "FamilyName", "attribute", 785, 20),
     node("phone", "Phone", "multi", 990, 130),
     node("count", "EnrollmentCount", "derived", 600, 440)],
    [edge("s", a) for a in ("id", "name", "phone", "count")] +
    [edge("name", "first"), edge("name", "last")])
add("keys", "4. Keys Identify Entities", "One composite key is not two separate keys",
    "Underline Location, not Building and RoomNo separately. Neither component identifies a room alone.",
    425,
    [node("r", "ROOM", "entity", 600, 340),
     node("loc", "Location", "attribute", 600, 190, key="full"),
     node("b", "Building", "attribute", 340, 35),
     node("no", "RoomNo", "attribute", 860, 35)],
    [edge("r", "loc"), edge("loc", "b"), edge("loc", "no")])
add("domains", "5. Domains and Missing Values", "Allowed values are not just the observed values",
    "Under this example's rule, 5 is allowed even though only 2 and 3 occur in the current courses.",
    panels=[panel("Course rule", ["Attribute", "Allowed values"],
                  [["Credits", "Whole numbers from 1 through 6"]]),
            panel("Check proposed values", ["Value", "Decision"],
                  [["5", "Allowed"], ["2.5", "Reject: not whole"], ["7", "Reject: above 6"]])])
add("relationships", "6. Relationships Connect Entities", "An enrollment connects a student to a section",
    "The three rows describe three relationship instances, not three relationship types.",
    panels=[panel("ENROLLS_IN instances", ["Student", "Section (course / number)"],
                  [[s, f"{c} / {n}"] for s, c, n, _ in ENROLLMENTS]),
            panel("Count participation", ["Student", "Enrollment count"],
                  [[s, str(sum(r[0] == s for r in ENROLLMENTS))] for s in STUDENTS])])
nodes, edges, notes = [], [], []
for y, a, rel, b, left, right, label in (
    (95, "STUDENT", "HOLDS", "CARD", "1", "1", "At most one card per student; at most one student per card."),
    (355, "INSTRUCTOR", "TEACHES", "SECTION", "1", "N", "One instructor may teach many sections; one section has at most one instructor."),
    (615, "STUDENT", "ENROLLS_IN", "SECTION", "M", "N", "One student may enroll in many sections; one section may have many students."),
):
    suffix = str(y)
    nodes += [node("a"+suffix, a, "entity", 190, y), node("r"+suffix, rel, "relationship", 600, y),
              node("b"+suffix, b, "entity", 1010, y)]
    edges += [edge("a"+suffix, "r"+suffix), edge("r"+suffix, "b"+suffix)]
    notes += [(345, y-20, left), (820, y-20, right), (65, y+115, label)]
add("cardinality", "7. Maximum Cardinality", "Compare maximum counts in both directions",
    "These panels isolate maximum ratios. Participation requirements are added in the next figure.",
    800, nodes, edges, notes)
add("participation", "8. Total and Partial Participation", "A double line requires participation",
    "Every SECTION must have a teacher. An INSTRUCTOR may currently teach no section.",
    350,
    [node("i", "INSTRUCTOR", "entity", 195, 130), node("t", "TEACHES", "relationship", 600, 130),
     node("s", "SECTION", "entity", 1005, 130)],
    [edge("i", "t"), edge("t", "s", True)],
    [(345, 100, "1"), (825, 100, "N"), (65, 275, "Single line: zero is allowed."),
     (640, 275, "Double line: at least one is required.")])
add("minmax", "9. Read Min-Max Labels Carefully", "Place this notation beside the entity being counted",
    "Here (0,N) counts sections for one instructor; (1,1) counts teachers for one section.",
    320,
    [node("i", "INSTRUCTOR", "entity", 195, 120), node("t", "TEACHES", "relationship", 600, 120),
     node("s", "SECTION", "entity", 1005, 120)],
    [edge("i", "t"), edge("t", "s")],
    [(330, 85, "(0,N)"), (780, 85, "(1,1)"),
     (65, 260, "Min-max replaces the maximum-ratio and single/double-line convention here.")])
add("roles", "10. Recursive Relationships and Roles", "One entity type can participate twice",
    "MENTORS is binary: one student plays mentor and another plays mentee. The roles distinguish the two.",
    460,
    [node("s", "STUDENT", "entity", 310, 220), node("m", "MENTORS", "relationship", 855, 220)],
    [edge("s", "m", points=[(310, 45), (855, 45)]),
     edge("s", "m", points=[(310, 395), (855, 395)])],
    [(350, 25, "mentor (0,N)"), (350, 435, "mentee (0,1)")])
add("grade", "11. Attributes of a Relationship", "A grade belongs to a particular enrollment",
    "S101 has 80 in DB101 / 1 and 90 in CS102 / 1. One grade on STUDENT cannot describe both.",
    345,
    [node("s", "STUDENT", "entity", 190, 240), node("e", "ENROLLS_IN", "relationship", 600, 240),
     node("q", "SECTION", "entity", 1010, 240), node("g", "Grade", "attribute", 600, 35)],
    [edge("s", "e"), edge("e", "q"), edge("e", "g")],
    [(350, 210, "M"), (820, 210, "N")])
add("weak", "12. Weak Entities and Partial Keys", "A section needs its owner to be identified",
    "Within Fall 2026, COURSE plus SectionNo identifies SECTION. SectionNo alone can repeat across courses.",
    390,
    [node("c", "COURSE", "entity", 190, 245), node("h", "HAS_SECTION", "identifying", 600, 245),
     node("s", "SECTION", "weak", 1010, 245),
     node("id", "CourseCode", "attribute", 190, 40, 235, key="full"),
     node("no", "SectionNo", "attribute", 1010, 40, key="partial")],
    [edge("c", "h"), edge("h", "s", True), edge("c", "id"), edge("s", "no")],
    [(345, 210, "1"), (815, 210, "N")])
add("refinement", "13. Refine a Design from Its Requirements", "Replace an entity reference with a relationship",
    "Use INSTRUCTOR and TEACHES when instructor identity and name are needed. A teacher name alone need not identify a person.",
    panels=[panel("Initial description", ["Section", "Teacher name"],
                  [["DB101 / 1", "Morgan"], ["DB101 / 2", "Morgan"]]),
            panel("Refined facts", ["Instructor", "Section taught"],
                  [[i, f"{c} / {n}"] for i, c, n in TEACHES],
                  "Name remains an attribute of INSTRUCTOR.")])
add("ternary", "14. A Fact That Needs Three Participants", "One approval names a student, instructor, and course",
    "APPROVES is ternary. Each line connects a participating type to the same diamond; it is not a sequence.",
    450,
    [node("s", "STUDENT", "entity", 190, 120), node("a", "APPROVES", "relationship", 600, 120),
     node("i", "INSTRUCTOR", "entity", 1010, 120), node("c", "COURSE", "entity", 600, 380)],
    [edge("s", "a"), edge("a", "i"), edge("a", "c")])
add("pairs", "14. A Fact That Needs Three Participants", "Three pairwise facts do not prove a three-way fact",
    "All three pairs for (S101, I1, CS102) appear, but that approval is absent from the supplied records.",
    panels=[panel("Recorded approvals", ["Student", "Instructor", "Course"], [list(r) for r in APPROVALS]),
            panel("Pairs for the missing triple", ["Pair", "Seen in record"],
                  [["S101 + I1", "1"], ["S101 + CS102", "2"], ["I1 + CS102", "3"]])])

# A compact complete core schema uses a deliberately smaller attribute inventory.
add("complete", "15. Assemble the Campus Diagram", "The core campus ER schema for Fall 2026",
    "Maximum ratios and double participation lines describe the binary relationships. APPROVES records three-way facts.",
    1370,
    [node("s", "STUDENT", "entity", 190, 265),
     node("sid", "StudentId", "attribute", 150, 50, key="full"),
     node("phone", "Phone", "multi", 190, 470),
     node("e", "ENROLLS_IN", "relationship", 600, 265),
     node("g", "Grade", "attribute", 600, 50),
     node("q", "SECTION", "weak", 1010, 265),
     node("no", "SectionNo", "attribute", 1020, 50, key="partial"),
     node("a", "APPROVES", "relationship", 190, 720),
     node("h", "HAS_SECTION", "identifying", 1010, 720),
     node("t", "TEACHES", "relationship", 600, 560),
     node("i", "INSTRUCTOR", "entity", 190, 1110),
     node("iid", "InstructorId", "attribute", 150, 1310, 235, key="full"),
     node("c", "COURSE", "entity", 1010, 1110),
     node("cid", "CourseCode", "attribute", 1020, 1310, 235, key="full")],
    [edge("s", "e"), edge("e", "q"),
     edge("s", "a", points=[(60, 390), (60, 600)]),
     edge("a", "i"), edge("a", "c", points=[(580, 930)]),
     edge("c", "h"), edge("h", "q", True),
     edge("i", "t", points=[(600, 1100)]),
     edge("t", "q", True, points=[(820, 560), (840, 400)]),
     edge("s", "sid"), edge("s", "phone"), edge("e", "g"),
     edge("q", "no"), edge("i", "iid"), edge("c", "cid")],
    [(350, 235, "M"), (820, 235, "N"),
     (1030, 430, "N"), (1030, 1020, "1"),
     (620, 1020, "1"), (805, 500, "N"),
     (355, 1290, "Core attributes only; see the inventory below.")])


def boundary(n, target):
    dx, dy = target[0] - n["x"], target[1] - n["y"]
    a, b = n["w"] / 2, n["h"] / 2
    if n["kind"] in {"relationship", "identifying"}:
        scale = 1 / (abs(dx) / a + abs(dy) / b)
    elif n["kind"] in {"attribute", "multi", "derived"}:
        scale = 1 / math.sqrt((dx / a) ** 2 + (dy / b) ** 2)
    else:
        scale = 1 / max(abs(dx) / a, abs(dy) / b)
    return n["x"] + dx * scale, n["y"] + dy * scale


def render_er(data, paragraph, font):
    """Render Chen shapes with explicitly routed, undirected lines."""
    title, used = paragraph(45, 48, data["title"], 1110, 32, weight=700)
    offset = used + 135
    parts = [title, paragraph(45, used + 85, "Original synthetic campus example", 1110, 20)[0]]
    d = data["diagram"]
    nodes = {n["id"]: n for n in d["nodes"]}
    for link in d["edges"]:
        a, b = nodes[link["a"]], nodes[link["b"]]
        via = link["points"] or []
        start = boundary(a, via[0] if via else (b["x"], b["y"]))
        end = boundary(b, via[-1] if via else (a["x"], a["y"]))
        points = [start, *via, end]
        path = " ".join(f"{'M' if i == 0 else 'L'} {x:.2f} {y+offset:.2f}" for i, (x, y) in enumerate(points))
        # A small gap at crossings keeps unrelated connections visually separate.
        parts.append(f'<path d="{path}" fill="none" stroke="#fafcfc" stroke-width="{12 if link["total"] else 7}"/>')
        parts.append(f'<path class="er-edge" d="{path}" fill="none" stroke="#384f59" stroke-width="{8 if link["total"] else 2.5}"/>')
        if link["total"]:
            parts.append(f'<path d="{path}" fill="none" stroke="#fafcfc" stroke-width="3"/>')
    for n in d["nodes"]:
        x, y, w, h, kind = n["x"], n["y"]+offset, n["w"], n["h"], n["kind"]
        fill = "#e4f2ed" if kind in {"entity", "weak"} else "#fbe9ef" if kind in {"relationship", "identifying"} else "#ffffff"
        parts.append(f'<g class="er-node" data-kind="{kind}" data-id="{escape(n["id"])}">')
        for inset in ([0, 7] if kind in {"weak", "multi", "identifying"} else [0]):
            a, b = w/2-inset, h/2-inset
            style = f'fill="{fill}" stroke="#384f59" stroke-width="2.5"'
            if kind == "derived":
                style += ' stroke-dasharray="7 5"'
            if kind in {"relationship", "identifying"}:
                parts.append(f'<polygon points="{x-a},{y} {x},{y-b} {x+a},{y} {x},{y+b}" {style}/>')
            elif kind in {"entity", "weak"}:
                parts.append(f'<rect x="{x-a}" y="{y-b}" width="{2*a}" height="{2*b}" {style}/>')
            else:
                parts.append(f'<ellipse cx="{x}" cy="{y}" rx="{a}" ry="{b}" {style}/>')
        size = 22
        text_width = font(size, 600).getlength(n["label"])
        if text_width > w * (0.72 if kind in {"relationship", "identifying"} else 0.82):
            raise ValueError(f'ER label too wide: {n["label"]}')
        parts.append(f'<text x="{x}" y="{y+7}" text-anchor="middle" font-family="Arial, sans-serif" font-size="{size}" font-weight="600" fill="#18252b">{escape(n["label"])}</text>')
        if n["key"]:
            dash = ' stroke-dasharray="5 4"' if n["key"] == "partial" else ""
            parts.append(f'<line x1="{x-text_width/2}" y1="{y+12}" x2="{x+text_width/2}" y2="{y+12}" stroke="#18252b" stroke-width="2"{dash}/>')
        parts.append("</g>")
    for x, y, label in d["notes"]:
        parts.append(paragraph(x, y+offset, label, min(1110, 1170-x), 22)[0])
    bottom = offset + d["height"]
    conclusion, used = paragraph(45, bottom+60, data["conclusion"], 1110, 25, weight=600)
    parts.append(f'<line x1="45" y1="{bottom+25}" x2="1155" y2="{bottom+25}" stroke="#9eafb8"/>')
    parts.append(conclusion)
    height = int(bottom + used + 90)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img"><title>{escape(data["title"])}</title><desc>{escape(data["conclusion"])}</desc><rect width="1200" height="{height}" fill="#fafcfc"/>{"".join(parts)}</svg>'
