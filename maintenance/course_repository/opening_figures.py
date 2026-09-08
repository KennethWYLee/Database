"""Original diagrams for the prescribed textbook's first-meeting selections."""

FIGURES = {}


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
