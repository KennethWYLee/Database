"""Original diagrams for the prescribed textbook's first-meeting selections."""

from er_figures import FIGURES as ER_FIGURES

FIGURES = dict(ER_FIGURES)



def panel(title, headers, rows, note=""):
    return dict(title=title, headers=headers, rows=rows, note=note, marks=())


def add(chapter, name, heading, title, panels, conclusion, graph=None):
    FIGURES[f"opening_{chapter}_{name}"] = dict(
        heading=heading, title=title, panels=panels, conclusion=conclusion,
        arrows=False, kind="network" if graph else "tables", graph=graph,
    )


add("ch01", "system", "## 1. Data, Software, and a Database System",
    "A request, the DBMS, and stored data", [],
    "The DBMS processes requests; the email is a stored value. Arrows show request and result flow.",
    dict(height=360, nodes=[
        (40, 80, 270, 110, "Office request: find S101's email"),
        (450, 80, 270, 110, "SQLite: DBMS software"),
        (860, 80, 290, 110, "Database: S101, an@example.test"),
    ], edges=[
        (310, 105, 450, 105, "request", 330, 80),
        (720, 105, 860, 105, "read", 765, 80),
        (860, 170, 720, 170, "value", 765, 220),
        (450, 170, 310, 170, "result", 330, 220),
    ]))

add("ch01", "conflict", "## 2. Two Files Can Disagree",
    "The same ID has conflicting contact values", [
        panel("Registration file", ["ID", "email"], [["S101", "an@example.test"]]),
        panel("Contact file", ["ID", "email"], [["S101", "an.old@example.test"]]),
    ], "Neither stored row proves which email is current. Confirm the fact before changing the shared record.")

add("ch01", "catalog", "## 3. The Catalog Describes the Data",
    "A description is not the student's stored value", [
        panel("Simplified catalog", ["table", "attribute", "declared type"],
              [["student", "student_id", "TEXT"], ["student", "email", "TEXT"]]),
        panel("Stored data", ["student_id", "email"], [["S101", "an@example.test"]]),
    ], "The catalog describes the attributes. The student row supplies values for those attributes.")

add("ch01", "views", "## 4. Different Users Need Different Views",
    "Two views of the same three student records", [
        panel("Contact list", ["ID", "email"], [["S101", "an@example.test"], ["S102", "bea@example.test"], ["S103", "kai@example.test"]]),
        panel("Department summary", ["department", "students"], [["IM", "2"], ["FIN", "1"]],
              "Counts are derived from the input; they are not additional student records."),
    ], "Different questions use different attributes or derived values. A displayed view alone is not access enforcement.")

add("ch01", "rules", "## 5. Sharing Still Needs Rules",
    "Permission and factual correctness are separate checks", [
        panel("Stated role policy", ["role", "email change"], [["Contact officer", "Permitted after verification"], ["Summary reader", "Not permitted"]]),
        panel("Value check", ["proposed value", "what remains unknown"], [["new@example.test", "Does it belong to S101?"]]),
    ], "A permitted operation can still contain a wrong fact. The example states policy; it does not implement user accounts.")

add("ch02", "models", "## 1. A Model Describes What We Represent",
    "One student-department fact, three descriptions", [
        panel("Conceptual", ["meaning"], [["S101 belongs to IM"]], "Informal concept, not an ER notation lesson."),
        panel("Relational", ["student_id", "dept_code"], [["S101", "IM"]]),
        panel("Physical", ["illustrative location"], [["A record in storage block 4"]], "The block number is invented, not observed."),
    ], "A model chooses which details to describe. A storage address is not evidence that the department fact is correct.")

add("ch02", "changes", "## 2. Schema and Database State",
    "Count rows and attributes separately", [
        panel("Insert S103", ["state", "rows", "attributes"], [["Before", "2", "3"], ["After", "3", "3"]]),
        panel("Correct S101's name", ["before", "after"], [["An Chen", "Ann Chen"]], "Still 3 rows and 3 attributes."),
        panel("Add status", ["state", "rows", "attributes"], [["Before", "3", "3"], ["After", "3", "4"]]),
    ], "Inserting and correcting data change the state. Adding an attribute changes the schema as well.")

add("ch02", "levels", "## 3. Three Schema Levels",
    "Three descriptions, not three copies of the facts", [],
    "Lines connect schema descriptions through mappings. User views omit storage details.",
    dict(height=535, directed=False, nodes=[
        (80, 0, 470, 110, "External: contact view with ID and email"),
        (650, 0, 470, 110, "External: department summary"),
        (310, 200, 580, 110, "Conceptual: students, contact details, departments"),
        (310, 400, 580, 110, "Internal: stored records and access structures"),
    ], edges=[(315, 110, 450, 200, "", 0, 0), (885, 110, 750, 200, "", 0, 0),
              (600, 310, 600, 400, "mapping", 635, 362)]))

add("ch02", "independence", "## 4. Data Independence Has Conditions",
    "What changes, and what must stay the same?", [
        panel("Logical independence example", ["changes", "preserved"],
              [["Conceptual tables split", "External contact view's attributes, rows, meaning"]],
              "The mapping is adjusted; direct users of the old table may need changes."),
        panel("Physical independence example", ["changes", "preserved"],
              [["Internal access structure", "Conceptual schema"]],
              "Query answers stay the same in this illustration; timing is not measured."),
    ], "Independence is a claim about specified unchanged descriptions or interfaces, not a promise that nothing changes.")

add("ch02", "languages", "## 5. Database Languages Express Different Requests",
    "Structure and data requests have different purposes", [
        panel("DDL: structure", ["statement", "purpose"], [["CREATE TABLE", "Define attributes and constraints"], ["ALTER TABLE", "Change structure"]]),
        panel("DML: data", ["statement", "purpose"], [["SELECT", "Retrieve values"], ["INSERT", "Add rows"], ["UPDATE", "Change values"]]),
    ], "SQL includes both kinds of requests. Selecting columns does not redefine the stored table.")

add("ch02", "architecture", "## 6. Client/Server and Embedded Databases",
    "SQLite does not need a separate DBMS server", [],
    "Top: requests cross a process boundary. Bottom: Python calls SQLite inside the same application process.",
    dict(height=485, nodes=[
        (60, 30, 390, 100, "Client process"), (740, 30, 410, 100, "DBMS server process"),
        (180, 290, 850, 125, "One application process: Python calls SQLite; the database can use memory or a file"),
    ], edges=[(450, 60, 740, 60, "request", 535, 35),
              (740, 115, 450, 115, "result", 535, 160)]))

add("ch05", "table", "## 1. Read One Student Table",
    "Read the complete tuple and one attribute value", [
        panel("S103's complete tuple", ["attribute", "value"], [["student_id", "S103"], ["email", "kai@example.test"], ["student_name", "Kai Wu"], ["dept_code", "IM"]]),
        panel("Three different things", ["kind", "example"], [["Tuple", "All four S103 values"], ["Attribute", "dept_code"], ["Value", "IM"]]),
    ], "One tuple describes one student in this relation. A single value does not describe the whole student.")

add("ch05", "domain", "## 2. A Domain Is More Than This Sample",
    "Allowed credits: whole numbers 1 through 6", [
        panel("Observed sample", ["course", "credits"], [["DB", "3"], ["WEB", "2"]]),
        panel("Check against the rule", ["value", "allowed?"], [["5", "Yes: whole number in range"], ["2.5", "No: not whole"], ["7", "No: above 6"]]),
    ], "The sample contains 2 and 3. The domain also permits values not yet observed, including 5.")

add("ch05", "phones", "## 3. One Phone Value at a Time",
    "A row can describe a student-phone association", [
        panel("List representation", ["student", "phones"], [["S101", "02-0000-0101, 02-0000-0102"], ["S102", "02-0000-0201"]]),
        panel("One pair per tuple", ["student_id", "phone_number"], [["S101", "02-0000-0101"], ["S101", "02-0000-0102"], ["S102", "02-0000-0201"]]),
    ], "Three synthetic phone tuples represent three associations. The two S101 pairs differ in their phone value.")

add("ch05", "order", "## 4. Display Order and Repeated Values",
    "Same student facts, different display orders", [
        panel("Ascending ID", ["ID", "department"], [["S101", "IM"], ["S102", "FIN"], ["S103", "IM"]]),
        panel("Descending ID", ["ID", "department"], [["S103", "IM"], ["S102", "FIN"], ["S101", "IM"]]),
    ], "No student is added or removed. Repeated department values are not duplicate complete student tuples.")

add("ch05", "identifiers", "## 5. Why Identifiers Matter",
    "One name can match two different students", [
        panel("Verified distinct students", ["student_id", "student_name", "dept_code"], [["S103", "Kai Wu", "IM"], ["S105", "Kai Wu", "DES"]]),
        panel("Interpret a request", ["condition", "matching rows"], [["Name is Kai Wu", "2"], ["ID is S105", "1 under the stated ID rule"]]),
    ], "Names do not identify a unique student here. The ID's meaning comes from the stated business rule.")

add("ch05", "notation", "## 6. Read a Schema and a Missing Value",
    "One missing value does not remove an attribute", [
        panel("Schema", ["position", "attribute"], [["1", "student_id"], ["2", "student_name"], ["3", "dept_code"]]),
        panel("Two tuples", ["student_id", "student_name", "dept_code"], [["S103", "Kai Wu", "IM"], ["S104", "New Name", "NULL"]]),
    ], "Degree = 3; tuple count = 2. NULL does not establish S104's department.")

add("ch05", "keys", "## 7. Superkeys, Candidate Keys, and the Primary Key",
    "Uniqueness and minimality are different checks", [
        panel("Given rules", ["attribute", "rule"], [["student_id", "Unique; not missing"], ["email", "Unique; not missing"], ["student_name", "May repeat"]]),
        panel("Classify the attribute set", ["set", "superkey?", "minimal?"], [["student_id", "Yes", "Yes"], ["email", "Yes", "Yes"], ["student_id + name", "Yes", "No"], ["name", "Not guaranteed", "Not a key"]]),
    ], "Choose student_id as primary; email remains a candidate key. Sample uniqueness is not a rule.")

add("ch05", "composite", "## 8. A Composite Key Identifies a Combination",
    "A permitted retake needs the term in the key", [
        panel("Existing registrations", ["student", "course", "term"], [["S101", "DB1", "F26"], ["S101", "DB1", "S27"], ["S102", "DB1", "F26"]]),
        panel("Proposed registrations", ["student", "course", "term", "decision"], [["S101", "DB1", "F26", "Duplicate"], ["S102", "DB1", "S27", "New key"]]),
    ], "The complete triple is unique. Neither individual columns nor the student/course pair must be unique.")

add("ch05", "references", "## 9. Connect Relations with Foreign Keys",
    "Foreign keys point to referenced keys", [],
    "Arrows show enrollment references and the optional student department reference, not execution or ER cardinality.",
    dict(height=500, nodes=[
        (40, 0, 470, 100, "department: primary key dept_code"),
        (40, 210, 470, 110, "student: primary key student_id; foreign key dept_code"),
        (700, 0, 470, 100, "course: primary key course_id"),
        (680, 340, 500, 130, "enrollment: primary key (student_id, course_id, term); student_id and course_id are foreign keys"),
    ], edges=[
        (275, 210, 275, 100, "", 0, 0),
        (680, 385, 510, 290, "", 0, 0),
        (930, 340, 930, 100, "", 0, 0),
    ]))

add("ch05", "database", "## 10. Build and Inspect a Small Database",
    "Create parents before inserting references", [
        panel("department", ["dept_code"], [["IM"], ["FIN"], ["DES"]]),
        panel("course", ["course_id", "credits"], [["DB1", "3"], ["AI1", "2"]]),
        panel("student", ["student_id", "dept_code"], [["S101", "IM"], ["S102", "FIN"], ["S103", "IM"]]),
    ], "Enrollment also needs student_id, course_id, and term. These are synthetic input rows, not the full schema.")

add("ch05", "violations", "## 11. Predict Accepted and Rejected Changes",
    "A new ID alone does not make a new row valid", [
        panel("Proposal", ["change", "decision"], [["Duplicate S101", "Blocked"], ["NULL primary key", "Blocked"], ["MED reference", "Blocked"], ["NULL optional department", "Accepted"]]),
        panel("Other independent checks", ["change", "decision"], [["2.5 credits", "Blocked"], ["7 credits", "Blocked"], ["Repeated name", "Accepted"], ["Another enrollment term", "Accepted"]]),
    ], "Check each rule against the same starting state. Accepted means the implemented constraints passed, not factual truth.")

add("ch05", "deletion", "## 12. Choose What Happens to References",
    "Deleting IM has four different consequences", [
        panel("Initial contacts", ["id", "department"], [["C1", "IM"], ["C2", "IM"]]),
        panel("After attempted parent deletion", ["action", "contacts", "department"], [["RESTRICT", "2", "IM; deletion blocked"], ["CASCADE", "0", "No contacts remain"], ["SET NULL", "2", "NULL"], ["SET DEFAULT", "2", "UNASSIGNED"]]),
    ], "The example creates UNASSIGNED first. Clearing a mandatory foreign key or referencing an absent default would fail.")

add("ch05", "business", "## 13. Business Rules and a Unit of Work",
    "Valid references do not enforce every intended rule", [
        panel("S101 registrations in F26", ["before", "after"], [["DB1", "DB1"], ["AI1", "AI1"], ["", "X1"]], "All three course IDs exist; the intended limit is two."),
        panel("Credits", ["old", "new", "domain", "no-decrease rule"], [["3", "2", "Both valid", "Change violates rule"]]),
    ], "The current DDL does not enforce these extra rules. Check the count or both old and new values separately.")

add("ch08", "inputs", "## 1. Start with Small Relations",
    "Three registrations do not mean three registered students", [
        panel("student", ["ID", "name", "department"], [["S101", "An Chen", "IM"], ["S102", "Bea Lin", "FIN"], ["S103", "Kai Wu", "IM"]]),
        panel("enrollment", ["ID", "course", "term"], [["S101", "DB1", "F26"], ["S101", "DB1", "S27"], ["S102", "DB1", "F26"]]),
    ], "Both inputs contain three tuples. Only S101 and S102 occur in enrollment.")

add("ch08", "select", "## 2. SELECT Keeps Rows That Satisfy a Condition",
    "Filter by department; retain all attributes", [
        panel("Input: student", ["ID", "name", "department"], [["S101", "An Chen", "IM"], ["S102", "Bea Lin", "FIN"], ["S103", "Kai Wu", "IM"]]),
        panel("Output: department = IM", ["ID", "name", "department"], [["S101", "An Chen", "IM"], ["S103", "Kai Wu", "IM"]]),
    ], "Three input tuples become two output tuples. The three attributes are unchanged.")

add("ch08", "project", "## 3. PROJECT Keeps Attributes and Removes Duplicate Tuples",
    "Remove duplicate complete projected tuples", [
        panel("Input values", ["ID", "department"], [["S101", "IM"], ["S102", "FIN"], ["S103", "IM"]]),
        panel("Project department", ["department"], [["FIN"], ["IM"]]),
        panel("Keep the ID too", ["ID", "department"], [["S101", "IM"], ["S102", "FIN"], ["S103", "IM"]]),
    ], "A one-attribute projection has two tuples. Including the unique ID preserves all three.")

add("ch08", "sequence", "## 4. Name Intermediate Results and Preserve Needed Attributes",
    "Check a condition before removing its attribute", [
        panel("Select department = IM", ["student_id", "student_name", "dept_code"], [["S101", "An Chen", "IM"], ["S103", "Kai Wu", "IM"]]),
        panel("Project; rename output attributes", ["id", "name"], [["S101", "An Chen"], ["S103", "Kai Wu"]]),
    ], "The right result no longer contains dept_code. Renaming changes names, not the values.")

add("ch08", "sets", "## 5. UNION, INTERSECTION, and DIFFERENCE Compare Sets",
    "Compare the same student-ID domain", [
        panel("Inputs", ["DB club (R)", "AI club (S)"], [["S101", "S102"], ["S102", "S103"]], "Read each column as its own one-attribute relation."),
        panel("Outputs", ["operation", "student IDs"], [["Union", "S101, S102, S103"], ["Intersection", "S102"], ["R minus S", "S101"], ["S minus R", "S103"]]),
    ], "S102 occurs once in the union. Reversing difference changes its result.")

add("ch08", "product", "## 6. CARTESIAN PRODUCT Makes Every Pair",
    "Three students times two courses gives six pairs", [
        panel("Student IDs", ["ID"], [["S101"], ["S102"], ["S103"]]),
        panel("Course IDs", ["course"], [["AI1"], ["DB1"]]),
        panel("Product, showing IDs only", ["ID", "course"], [["S101", "AI1"], ["S101", "DB1"], ["S102", "AI1"], ["S102", "DB1"], ["S103", "AI1"], ["S103", "DB1"]]),
    ], "These are possible pairs, not enrollment facts. The full product also carries the other input attributes.")

add("ch08", "join", "## 7. JOIN Keeps Matching Pairs",
    "One student may match several registrations", [
        panel("Matches by ID", ["student", "registrations"], [["S101", "DB1/F26; DB1/S27"], ["S102", "DB1/F26"], ["S103", "None"]]),
        panel("Equijoin, showing IDs and registration", ["student ID", "enrolled ID", "course", "term"], [["S101", "S101", "DB1", "F26"], ["S101", "S101", "DB1", "S27"], ["S102", "S102", "DB1", "F26"]]),
    ], "All three matching pairs remain. Both compared ID attributes are retained; S103 has no match.")

add("ch08", "natural", "## 8. NATURAL JOIN Uses Every Shared Attribute Name",
    "Same attribute name can hide different meanings", [
        panel("S101 input facts", ["relation", "student_id", "dept_code"], [["student", "S101", "IM"], ["offering", "S101", "FIN"]]),
        panel("Compare the join conditions", ["condition", "matching tuples"], [["ID and department equal", "0"], ["ID equal only", "1: S101, An Chen"]]),
    ], "Natural join uses both shared names. The offering's department is not the student's major.")

add("ch08", "combine", "## 9. Combine Operations to Answer a Question",
    "Find IM students registered in DB1 during F26", [
        panel("Selected students", ["ID", "name"], [["S101", "An Chen"], ["S103", "Kai Wu"]], "Department = IM; selected input shown without department."),
        panel("Selected registrations", ["ID", "course", "term"], [["S101", "DB1", "F26"], ["S102", "DB1", "F26"]]),
        panel("Join; project ID and name", ["ID", "name"], [["S101", "An Chen"]]),
    ], "The only shared student ID is S101. Omitting the term filter adds a join tuple but not a distinct projected student.")
