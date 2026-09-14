"""Original Chapter 3 ER diagrams, independent of textbook artwork."""
from html import escape
import math

FIGURES = {}
STUDENTS = ("S101", "S102", "S103")
STUDENT_PROFILES = (
    ("S101", "Alex", "Lin", ("02-0000-0101", "02-0000-0102")),
    ("S102", "Blair", "Wu", ("02-0000-0201",)),
    ("S103", "Casey", "Chen", ()),
)
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


def add(name, section, title, conclusion, height=None, nodes=(), edges=(), notes=(), panels=(), *, stacked=False):
    FIGURES["opening_ch03_" + name] = dict(
        heading="## " + section, title=title, conclusion=conclusion,
        kind="er" if height else "tables", arrows=False, panels=panels, stacked=stacked,
        text_outside_image=True,
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
    "STUDENT is the type; S101 identifies one entity. Adding a fourth student changes the set, not the type definition.",
    panels=[panel("Type description", ["Type", "Properties"], [["STUDENT", "StudentId, Name, Phone"]]),
            panel("Current illustrative set: three students", ["StudentId", "Name", "Phone"],
                  [[sid, f"{given} {family}", "; ".join(phones) or "None recorded"]
                   for sid, given, family, phones in STUDENT_PROFILES],
                  "Phone may have several recorded values. None recorded does not mean the student owns no phone. The numbers are invented.")],
    stacked=True)
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
                  [["Credits", "Whole numbers from 1 through 6"]], "Currently observed values: 2 and 3."),
            panel("Check proposed values", ["Value", "Decision"],
                  [["5", "Allowed"], ["2.5", "Reject: not whole"], ["7", "Reject: above 6"]])])
add("relationships", "6. Relationships Connect Entities", "An enrollment connects a student to a section",
    "The three rows describe three relationship instances, not three relationship types.",
    panels=[panel("ENROLLS_IN instances", ["Student", "Section (course / number)", "Grade"],
                  [[s, f"{c} / {n}", str(g)] for s, c, n, g in ENROLLMENTS]),
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
    "MENTORS is binary because it has two roles: mentor and mentee. These counts alone do not forbid self-mentoring.",
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
    "The same two sections remain. Name describes INSTRUCTOR; TEACHES records assignments. Matching names alone do not establish identity.",
    panels=[panel("Initial description", ["Section", "Teacher name"],
                  [["DB101 / 1", "Morgan"], ["DB101 / 2", "Morgan"]]),
            panel("INSTRUCTOR: identity checked separately", ["InstructorId", "Name"],
                  [["I1", "Morgan"]], "The example supplies I1's identity independently of the repeated name."),
            panel("TEACHES: assignments for the same two sections", ["InstructorId", "Section taught"],
                  [[i, f"{c} / {n}"] for i, c, n in TEACHES if c == "DB101"],
                  "The example confirms that I1 teaches both sections. Other sections are outside this comparison.")],
    stacked=True)
add("ternary", "14. A Fact That Needs Three Participants", "One approval names a student, instructor, and course",
    "APPROVES is ternary. Each line connects a participating type to the same diamond; it is not a sequence.",
    450,
    [node("s", "STUDENT", "entity", 190, 120), node("a", "APPROVES", "relationship", 600, 120),
     node("i", "INSTRUCTOR", "entity", 1010, 120), node("c", "COURSE", "entity", 600, 380)],
    [edge("s", "a"), edge("a", "i"), edge("a", "c")])
add("pairs", "14. A Fact That Needs Three Participants", "Three pairwise facts do not prove a three-way fact",
    "All three pairs for (S101, I1, CS102) appear, but that approval is absent from the supplied records.",
    panels=[panel("Recorded approvals", ["Record", "Student", "Instructor", "Course"],
                  [[str(index), *r] for index, r in enumerate(APPROVALS, 1)],
                  "Record numbers label these example rows; they are not an added identifying attribute."),
            panel("Pairs for the missing triple", ["Pair", "Seen in record"],
                  [["S101 + I1", "1"], ["S101 + CS102", "2"], ["I1 + CS102", "3"]])],
    stacked=True)

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


# Additional instructor-approved Ch3 examples, separate from the original core.
ORDER_ITEMS = (("O10", 1, "Notebook", 2), ("O10", 2, "Pen", 3), ("O20", 1, "Notebook", 2))
ITEM_NOTES = (("O10", 1, 1), ("O10", 2, 1), ("O20", 1, 1))
INTERVIEWS = (("S101", "C1", 1), ("S101", "C2", 1), ("S102", "C1", 1))
APPROVAL_ADDITIONS = (("S101", "I2", "DB101"), ("S103", "I1", "DB101"), ("S103", "I2", "DB101"))
UNIVERSITY_RELATIONSHIPS = (
    ("ADMINS", "COLLEGE", "(0,N)", "DEPT", "(1,1)"),
    ("DEAN", "COLLEGE", "(1,1)", "INSTRUCTOR", "(0,1)"),
    ("CHAIR", "DEPT", "(1,1)", "INSTRUCTOR", "(0,1)"),
    ("EMPLOYS", "DEPT", "(0,N)", "INSTRUCTOR", "(1,1)"),
    ("HAS", "DEPT", "(0,N)", "STUDENT", "(0,1)"),
    ("OFFERS", "DEPT", "(0,N)", "COURSE", "(1,1)"),
    ("SECS", "COURSE", "(0,N)", "SECTION", "(1,1)"),
    ("TEACHES", "INSTRUCTOR", "(0,N)", "SECTION", "(1,1)"),
    ("TAKES", "STUDENT", "(0,N)", "SECTION", "(5,N)"),
)
WEAK_HEADING = "12. Weak Entities and Partial Keys / ### "
TERNARY_HEADING = "14. A Fact That Needs Three Participants / ### "
UNIVERSITY_HEADING = "16. Section 3.10: A UNIVERSITY Database / ### "

add("order_items", WEAK_HEADING + "12.1. Order Items: the Same Number under Different Owners",
    "An item number identifies an item only within its order",
    "O10 / 1 and O20 / 1 are distinct items. Product and Quantity describe an item; neither is its partial key.",
    470,
    [node("o", "ORDER", "entity", 190, 225), node("r", "CONTAINS", "identifying", 600, 225),
     node("i", "ORDER_ITEM", "weak", 1010, 225),
     node("oid", "OrderId", "attribute", 190, 35, key="full"),
     node("line", "LineNo", "attribute", 1010, 35, key="partial"),
     node("product", "Product", "attribute", 750, 405), node("qty", "Quantity", "attribute", 1050, 405)],
    [edge("o", "r"), edge("r", "i", True), edge("o", "oid"), edge("i", "line"),
     edge("i", "product"), edge("i", "qty")],
    [(350, 200, "1"), (820, 200, "N")])
add("strong_card", WEAK_HEADING + "12.2. A Required Owner Does Not Automatically Make an Entity Weak",
    "CARD has its own key even when ownership is required",
    "CardId is globally unique. A required owner changes participation, not this independent identification.",
    330,
    [node("s", "STUDENT", "entity", 190, 230), node("h", "HOLDS", "relationship", 600, 230),
     node("c", "CARD", "entity", 1010, 230),
     node("sid", "StudentId", "attribute", 190, 35, key="full"),
     node("cid", "CardId", "attribute", 1010, 35, key="full")],
    [edge("s", "h"), edge("h", "c", True), edge("s", "sid"), edge("c", "cid")],
    [(350, 205, "1"), (820, 205, "N")])
add("nested_weak", WEAK_HEADING + "12.3. A Weak Entity Can Own Another Weak Entity",
    "Follow identification through every owner",
    "A note is identified by OrderId, LineNo, and NoteNo. ORDER_ITEM is both weak and an owner. Only identifying attributes are shown.",
    920,
    [node("o", "ORDER", "entity", 700, 65), node("id", "OrderId", "attribute", 250, 65, key="full"),
     node("r", "CONTAINS", "identifying", 700, 260),
     node("i", "ORDER_ITEM", "weak", 700, 450), node("line", "LineNo", "attribute", 250, 450, key="partial"),
     node("h", "HAS_NOTE", "identifying", 700, 640),
     node("n", "ITEM_NOTE", "weak", 700, 830), node("no", "NoteNo", "attribute", 250, 830, key="partial")],
    [edge("o", "id"), edge("o", "r"), edge("r", "i", True), edge("i", "line"),
     edge("i", "h"), edge("h", "n", True), edge("n", "no")],
    [(725, 155, "1"), (725, 390, "N"), (725, 540, "1"), (725, 770, "N")])
add("two_owners", WEAK_HEADING + "12.4. Two Owners Can Be Needed Together",
    "An interview number is local to a student-company pair",
    "Fix both owners, then use VisitNo. StudentId or CompanyId plus VisitNo alone is insufficient.",
    650,
    [node("s", "STUDENT", "entity", 190, 120), node("c", "COMPANY", "entity", 1010, 120),
     node("sid", "StudentId", "attribute", 190, 15, key="full"),
     node("cid", "CompanyId", "attribute", 1010, 15, key="full"),
     node("r", "ARRANGES", "identifying", 600, 120),
     node("i", "INTERVIEW", "weak", 600, 365),
     node("v", "VisitNo", "attribute", 600, 575, key="partial")],
    [edge("s", "sid"), edge("c", "cid"), edge("s", "r"), edge("c", "r"), edge("r", "i", True), edge("i", "v")])

add("ternary_one", TERNARY_HEADING + "14.1. Section 3.9.2: Fix Two Participants before Reading a 1",
    "Fix student and course: at most one instructor",
    "The 1 limits the instructor for a fixed student-course pair, not all approvals involving that instructor.",
    490,
    [node("s", "STUDENT", "entity", 190, 100), node("a", "APPROVES", "relationship", 600, 100),
     node("i", "INSTRUCTOR", "entity", 1010, 100), node("c", "COURSE", "entity", 600, 375)],
    [edge("s", "a"), edge("a", "i"), edge("a", "c")],
    [(350, 70, "M"), (820, 70, "1"), (625, 285, "N")])
add("ternary_count", TERNARY_HEADING + "14.2. Section 3.9.2: Count All Participations with Min-Max",
    "Count every approval involving one instructor",
    "(0,2) permits zero to two approval instances per instructor; it does not enforce one instructor per student-course pair.",
    490,
    [node("s", "STUDENT", "entity", 190, 100), node("a", "APPROVES", "relationship", 600, 100),
     node("i", "INSTRUCTOR", "entity", 1010, 100), node("c", "COURSE", "entity", 600, 375)],
    [edge("s", "a"), edge("a", "i"), edge("a", "c")],
    [(335, 65, "(0,N)"), (790, 65, "(0,2)"), (625, 295, "(0,N)")])
add("ternary_checks", TERNARY_HEADING + "14.3. Use Both Checks When Both Rules Are Required",
    "Test the same proposed addition against two different rules",
    "Each row starts from the original three approvals. Only (S103, I2, DB101) passes both rules.",
    panels=[panel("One row contains both checks for the same addition",
                  ["Proposed addition", "One instructor per student-course pair?", "At most two approvals per instructor?", "Passes both?"],
                  [["S101, I2, DB101", "No: I1 already approves this pair", "Yes: I2 goes from 1 to 2", "No"],
                   ["S103, I1, DB101", "Yes: a new pair", "No: I1 goes from 2 to 3", "No"],
                   ["S103, I2, DB101", "Yes: a new pair", "Yes: I2 goes from 1 to 2", "Yes"]],
                  "Start each check from records 1-3: (S101, I1, DB101); (S101, I2, CS102); (S102, I1, CS102).")])

add("university_section", UNIVERSITY_HEADING + "16.1. Identify the Entities and Attributes",
    "In Section 3.10, SECTION has a globally unique SecId",
    "SecId is a full key. CRoom has Building and RoomNo components; SecNo is not a global identifier.",
    710,
    [node("s", "SECTION", "entity", 600, 275),
     node("id", "SecId", "attribute", 220, 80, key="full"), node("no", "SecNo", "attribute", 600, 50),
     node("sem", "Sem", "attribute", 980, 80), node("year", "Year", "attribute", 1020, 360),
     node("time", "DaysTime", "attribute", 180, 360), node("room", "CRoom", "attribute", 600, 510),
     node("b", "Bldg", "attribute", 390, 660), node("r", "RoomNo", "attribute", 820, 660)],
    [edge("s", a) for a in ("id", "no", "sem", "year", "time", "room")] +
    [edge("room", "b"), edge("room", "r")])

for name, section, title, rules, conclusion in (
    ("university_organization", "16.2. Build the Organization and Staff Relationships",
     "Read the organization one relationship at a time", UNIVERSITY_RELATIONSHIPS[:5],
     "Counts follow Figure 3.20. HAS shows STUDENT (0,1); the prose instead requires (1,1). Keep that discrepancy explicit."),
    ("university_teaching", "16.3. Connect Courses, Sections, Teachers, and Students",
     "Link courses and sections without making SECTION weak", UNIVERSITY_RELATIONSHIPS[5:],
     "Each SECTION needs a course, an instructor, and at least five students. A COURSE may have no section."),
):
    nodes, edges, notes = [], [], []
    for index, (rel, left, lcount, right, rcount) in enumerate(rules):
        y = 80 + index * 220
        prefix = str(index)
        nodes += [node(prefix+"l", left, "entity", 190, y),
                  node(prefix+"r", rel, "relationship", 600, y),
                  node(prefix+"e", right, "entity", 1010, y)]
        edges += [edge(prefix+"l", prefix+"r"), edge(prefix+"r", prefix+"e")]
        notes += [(325, y-35, lcount), (785, y-35, rcount)]
    add(name, UNIVERSITY_HEADING + section, title, conclusion,
        len(rules)*220, nodes, edges, notes)
add("university_conflicts", UNIVERSITY_HEADING + "16.4. Some Uniqueness Rules Need More Than a SecId Oval",
    "Different section IDs do not prevent other conflicts",
    "Each pair has different SecId values but violates its named extra rule. The three cases are checked independently.",
    panels=[panel("Each row is one independent proposed pair",
                  ["Case / SecId pair", "Values shared by both sections", "Reason to reject"],
                  [["A: Q101 / Q102", "DB101; Fall 2026; SecNo 1", "Duplicate local section number"],
                   ["B: Q201 / Q202", "Fall 2026; room A/201; Thu-P5", "Room occupied at the same time"],
                   ["C: Q301 / Q302", "Fall 2026; instructor I1; Thu-P5", "Instructor teaching at the same time"]],
                  "Other fields can differ to isolate each rule. Case C assumes combined sections are not permitted. Time equality does not detect every possible overlap.")])
# Worked illustrations accompany the existing scope; they add no assignments.
add("contact", "3. Attributes Describe an Entity / ### Worked Example: Two Contacts for One Student",
    "Several values can each have meaningful components",
    "One Contact value is a Label-PhoneNumber pair. The double oval permits several such pairs for one student.",
    430,
    [node("s", "STUDENT", "entity", 600, 335),
     node("contact", "Contact", "multi", 600, 175),
     node("label", "Label", "attribute", 300, 25),
     node("number", "PhoneNumber", "attribute", 900, 25)],
    [edge("s", "contact"), edge("contact", "label"), edge("contact", "number")],
    [(65, 425, "Attribute close-up: StudentId and other profile attributes are omitted.")])

add("key_lookup", "4. Keys Identify Entities / ### Worked Example: Find One Room",
    "How many rooms match the information supplied?",
    "Building and RoomNo work together. The stated rule, not this small sample alone, guarantees that Location is a key.",
    panels=[panel("Use the three rooms A/101, A/102, B/101", ["Information supplied", "Matching rooms", "Count"],
                  [["RoomNo = 101", "A/101; B/101", "2"],
                   ["Building = A", "A/101; A/102", "2"],
                   ["Building = A and RoomNo = 101", "A/101", "1"]])])

add("missing_values", "5. Domains and Missing Values / ### Worked Example: Missing Is Not Zero",
    "Similar empty entries can have different meanings",
    "Do not replace missing information with zero or with a claim that no value exists. First establish what is known.",
    panels=[panel("Separate fictional cases", ["Recorded information", "Known situation", "What it means"],
                  [["Grade = 0", "A marked assessment earned zero.", "Known numeric value"],
                   ["Grade not recorded", "Marking is unfinished.", "Unknown grade, not a zero"],
                   ["ParkingPermitNo absent", "The person confirms having no permit.", "Not applicable"],
                   ["ParkingPermitNo absent", "Nobody has checked whether a permit exists.", "Unknown whether a value exists"]],
                  "This is a conceptual comparison of meanings, not SQL storage or SQL NULL evaluation.")])


def instance_figure(name, section, title, conclusion, left, right, links):
    """Use the existing network renderer for labeled objects, not ER types."""
    add(name, section, title, conclusion)
    left_positions = {label: 50 + 150 * i for i, label in enumerate(left)}
    right_positions = {label: 50 + 150 * i for i, label in enumerate(right)}
    graph = dict(
        directed=False, height=50 + 150 * max(len(left), len(right)),
        nodes=[(65, y, 310, 80, label) for label, y in left_positions.items()] +
              [(825, y, 310, 80, label) for label, y in right_positions.items()],
        edges=[(375, left_positions[a]+40, 825, right_positions[b]+40, "", 0, 0)
               for a, b in links])
    FIGURES["opening_ch03_" + name].update(kind="network", graph=graph)


instance_figure("enrollment_links",
    "6. Relationships Connect Entities / ### Worked Example: Trace the Three Enrollments",
    "M:N: follow each recorded enrollment line",
    "These boxes are individual objects, not ER type symbols. Each line is one enrollment; Grade is omitted in this connection-only view.",
    ["Student " + s for s in STUDENTS],
    ["Section CS102 / 1", "Section DB101 / 1", "Section DB101 / 2"],
    [("Student " + s, f"Section {c} / {n}") for s, c, n, _ in ENROLLMENTS])

instance_figure("one_to_one",
    "7. Maximum Cardinality / ### Worked Example: One Card or Several Sections",
    "1:1: no object has more than one HOLDS line",
    "Objects, not ER type symbols. This separate variant allows at most one card per student and at most one student per card; it does not require a line.",
    ["Student S101", "Student S102", "Student S103"], ["Card K10", "Card K11"],
    [("Student S101", "Card K10"), ("Student S102", "Card K11")])
instance_figure("one_to_many",
    "7. Maximum Cardinality / ### Worked Example: One Card or Several Sections",
    "1:N: I1 has two lines; each section has one",
    "Objects, not ER type symbols. I1 teaching two sections is allowed. A second instructor on either section would violate its maximum of one.",
    ["Instructor I1", "Instructor I2"],
    ["Section DB101 / 1", "Section DB101 / 2", "Section CS102 / 1"],
    [("Instructor " + i, f"Section {c} / {n}") for i, c, n in TEACHES])

add("participation_changes", "8. Total and Partial Participation / ### Worked Example: Change One Fact at a Time",
    "A minimum and a maximum reject different changes",
    "Each proposal starts from the original three assignments. A section's owner course remains present; the table checks TEACHES only.",
    panels=[panel("Original: I1 teaches DB101/1 and DB101/2; I2 teaches CS102/1",
                  ["Isolated proposal", "Count to inspect", "TEACHES decision"],
                  [["Add I3 without an assignment", "I3: 0 sections", "Allowed: instructor minimum is 0"],
                   ["Remove I1's DB101/2 assignment; keep the section", "DB101/2: 0 instructors", "Reject: section minimum is 1"],
                   ["Also assign I2 to DB101/1", "DB101/1: 2 instructors", "Reject: section maximum is 1"],
                   ["Replace I1 with I2 on DB101/2", "DB101/2: 1 instructor; I2: 2 sections", "Allowed: exactly one per section"]])])

add("notation_counts", "9. Read Min-Max Labels Carefully / ### Worked Example: Count First, Then Choose the Label",
    "The same TEACHES counts, written in two notations",
    "For a binary relationship, maximum-ratio labels refer across the connection. A min-max pair is placed beside the entity being counted.",
    panels=[panel("Original assignments", ["Object inspected", "Observed count", "Permitted range"],
                  [["Instructor I1", "2 sections", "0 or more"],
                   ["Section DB101 / 1", "1 instructor", "Exactly 1"]]),
            panel("Translate the same rules", ["Rule", "Maximum-ratio notation", "Min-max notation"],
                  [["An instructor may teach many sections", "N near SECTION; single line at INSTRUCTOR", "(0,N) near INSTRUCTOR"],
                   ["A section needs exactly one instructor", "1 near INSTRUCTOR; double line at SECTION", "(1,1) near SECTION"]])], stacked=True)

instance_figure("mentor_roles",
    "10. Recursive Relationships and Roles / ### Worked Example: Follow the Named Roles",
    "Read each line from mentor role to mentee role",
    "Both columns use the same STUDENT set. Repeating S101 does not create a second student. The named roles, not an arrow, determine each fact.",
    ["Mentor S101", "Mentor S102", "Mentor S103"],
    ["Mentee S101", "Mentee S102", "Mentee S103"],
    [("Mentor S101", "Mentee S102"), ("Mentor S101", "Mentee S103")])

add("grade_matrix", "11. Attributes of a Relationship / ### Worked Example: Read a Grade at the Intersection",
    "Choose a student AND a section before reading Grade",
    "S101's row contains 80 and 90. DB101/1's column contains 80 and 70. Neither participant alone determines Grade in this M:N example.",
    panels=[panel("The original three enrollment facts", ["Student", "DB101 / 1", "CS102 / 1", "DB101 / 2"],
                  [[s, *[str(next((g for sid, c, n, g in ENROLLMENTS if sid == s and (c, n) == section), "No enrollment"))
                         for section in (("DB101", 1), ("CS102", 1), ("DB101", 2))]] for s in STUDENTS],
                  "No enrollment means no relationship instance. It is different from an existing enrollment whose grade is unknown.")])

add("weak_lookup", WEAK_HEADING + "Worked Example: Find the Owner Before the Item",
    "Repeated properties do not make two order items identical",
    "Start with the owner, then use its partial key. Quantity and Product describe the chosen item; they do not repair a duplicated identity.",
    panels=[panel("Compare the same three order items", ["Information supplied", "Matching items", "Result"],
                  [["LineNo = 1", "O10/1; O20/1", "Two different owners"],
                   ["Product = Notebook; Quantity = 2", "O10/1; O20/1", "Same properties, different items"],
                   ["OrderId = O10", "O10/1; O10/2", "Owner alone is insufficient"],
                   ["OrderId = O10; LineNo = 1", "O10/1", "One identified item"]])])

add("ternary_states", TERNARY_HEADING + "Worked Example: Two Approval Sets with the Same Pairs",
    "Pairwise information cannot distinguish these two states",
    "State B adds (S101, I1, CS102), but introduces no new pair. Keeping only the pairs loses whether that three-way approval is present.",
    panels=[panel("Compare against the original three approvals", ["Information retained", "State A: original", "State B: add one approval"],
                  [["Approval instances", "3", "4"],
                   ["Student-instructor pairs", "S101/I1; S101/I2; S102/I1", "Same three pairs"],
                   ["Student-course pairs", "S101/DB101; S101/CS102; S102/CS102", "Same three pairs"],
                   ["Instructor-course pairs", "I1/DB101; I2/CS102; I1/CS102", "Same three pairs"],
                   ["Is (S101, I1, CS102) recorded?", "No", "Yes"]],
                  "Use the core APPROVES rules here. The later one-instructor-per-pair and two-approval limits are not imposed.")])

add("university_staff_facts", UNIVERSITY_HEADING + "Worked Example: A Chair Is Not Every Employee",
    "Read CHAIR and EMPLOYS as separate facts",
    "I3 works in D1 but chairs no department. That satisfies both rules: employment is required, chairing is optional for an instructor.",
    panels=[panel("Synthetic organization snapshot", ["Relationship", "Recorded facts", "What to count"],
                  [["ADMINS", "C-A / D1; C-A / D2", "One college per department"],
                   ["DEAN", "C-A / I1", "One dean for C-A"],
                   ["CHAIR", "D1 / I1; D2 / I2", "One chair per department; none for I3"],
                   ["EMPLOYS", "D1 / I1; D2 / I2; D1 / I3", "One employing department per instructor"]],
                  "Organization facts only. The date of each CHAIR appointment and other attributes are omitted in this relationship-only view.")])

add("university_enrollment_change", UNIVERSITY_HEADING + "Worked Example: Five Distinct Students Become Four",
    "Removing one TAKES fact can violate a minimum",
    "After U5 leaves, Q101 still has its SecId, course, and instructor, but its four TAKES instances violate this UNIVERSITY model's minimum of five.",
    panels=[panel("Q101 remains a section of DB101 taught by I1", ["State", "Distinct students taking Q101", "Count and check"],
                  [["Before U5 leaves", "U1; U2; U3; U4; U5", "5: meets minimum 5"],
                   ["After U5 leaves", "U1; U2; U3; U4", "4: below minimum 5"],
                   ["Keep U5 in STUDENT, but not in TAKES", "U1; U2; U3; U4", "Still 4: entity presence is not enrollment"]],
                  "Five copies of the U1/Q101 fact would still represent one distinct relationship instance, not five students.")])

for name, data in FIGURES.items():
    if name.startswith("opening_ch03_university_"):
        data["subtitle"] = "Original teaching layout | Textbook Section 3.10"


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
    outside = data.get("text_outside_image", False)
    if outside:
        parts, offset = [], 50
    else:
        title, used = paragraph(45, 48, data["title"], 1110, 32, weight=700)
        offset = used + 135
        parts = [title, paragraph(45, used + 85, data.get("subtitle", "Original synthetic campus example"), 1110, 20)[0]]
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
    height = int(bottom + 35)
    if not outside:
        conclusion, used = paragraph(45, bottom+60, data["conclusion"], 1110, 25, weight=600)
        parts.append(f'<line x1="45" y1="{bottom+25}" x2="1155" y2="{bottom+25}" stroke="#9eafb8"/>')
        parts.append(conclusion)
        height = int(bottom + used + 90)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img"><title>{escape(data["title"])}</title><desc>{escape(data["conclusion"])}</desc><rect width="1200" height="{height}" fill="#fafcfc"/>{"".join(parts)}</svg>'
