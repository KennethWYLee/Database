"""Small, original worked examples embedded beside the existing chapter explanations."""

EXAMPLES = {}


def table(name, schema, headers, rows):
    return dict(name=name, schema=schema, headers=headers, rows=rows)


def result(title, headers, rows):
    displayed = [["NULL" if value is None else value for value in row] for row in rows]
    return dict(title=title, headers=headers, rows=displayed, note="", marks=())


def add(chapter, name, heading, title, source, concept, inputs, prediction,
        steps, outputs, interpretation, practice, check, *, panels=None):
    identifier = f"{chapter}_small_{name}"
    if identifier in EXAMPLES:
        raise ValueError(identifier)
    pictures = panels or [
        *(result(t["name"] + ": input", t["headers"], t["rows"]) for t in inputs),
        *(output for output in outputs if output["headers"]),
    ]
    EXAMPLES[identifier] = dict(
        chapter=chapter, heading=heading, title=title, source=source, concept=concept,
        inputs=inputs, prediction=prediction, steps=steps, outputs=outputs,
        interpretation=interpretation, practice=practice, check=check, panels=pictures,
    )


RUNTIME = '''import sqlite3


def run_small_example(tables, statements):
    """Start with the displayed input again each time; keep no database file."""
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("PRAGMA foreign_keys = ON")
    try:
        for name, definition, rows in tables:
            db.execute(f"CREATE TABLE {name} ({definition})")
            if rows:
                marks = ", ".join("?" for _ in rows[0])
                db.executemany(f"INSERT INTO {name} VALUES ({marks})", rows)
        for label, sql in statements:
            print(label)
            try:
                cursor = db.execute(sql)
                if cursor.description:
                    print(" | ".join(column[0] for column in cursor.description))
                    rows = cursor.fetchall()
                    for row in rows:
                        print(" | ".join("NULL" if value is None else str(value) for value in row))
                    if not rows:
                        print("(no rows)")
                else:
                    print("Statement completed.")
            except sqlite3.IntegrityError:
                print("IntegrityError: the statement was rejected.")
            print()
    finally:
        db.close()
'''


COURSES = table("course", "id TEXT NOT NULL PRIMARY KEY, dept TEXT, credits INTEGER",
                ["id", "dept", "credits"], [["DB", "IM", 3], ["WEB", "IM", 2], ["FIN", "FN", 3]])
STUDENTS = table("student", "id TEXT NOT NULL PRIMARY KEY, name TEXT, dept TEXT",
                 ["id", "name", "dept"], [["S1", "Amy", "IM"], ["S2", "Ben", "FN"], ["S3", "Cal", "IM"]])

add("ch03", "definition", "## 1. Defining Structure", "A table definition rejects an invalid row",
    "3.2 SQL Data Definition, pp.66-70", "The column definitions describe every row. A primary key identifies a row; NOT NULL requires a value; CHECK limits the allowed value. SQLite text primary keys need an explicit NOT NULL in this example.",
    [table("team", "id TEXT NOT NULL PRIMARY KEY, seats INTEGER NOT NULL CHECK(seats BETWEEN 2 AND 8)", ["id", "seats"], [["G1", 4]])],
    "Which insert is rejected: G2 with 1 seat or G3 with 6 seats? How many rows remain?",
    [("Insert G2", "INSERT INTO team VALUES ('G2',1)"), ("Insert G3", "INSERT INTO team VALUES ('G3',6)"), ("Stored teams", "SELECT * FROM team ORDER BY id")],
    [result("Insert G2", [], [["IntegrityError: the statement was rejected."]]), result("Insert G3", [], [["Statement completed."]]), result("Stored teams", ["id", "seats"], [["G1",4],["G3",6]])],
    "G2 is rejected because 1 is below the minimum 2. G3 is accepted; the final table has two rows. This range constraint is not a guarantee that every integer-like input has the intended business meaning.",
    "Try a new G4 with NULL seats, then a new G4 with 8 seats. Keep the statement and outcome for each.",
    "Check NOT NULL separately from the inclusive upper boundary. A rejected insert must leave the stored rows unchanged.",
    panels=[result("Input", ["id","seats"], [["G1",4]]),result("Check each request",["request","decision"],[["G2 / 1","reject: below 2"],["G3 / 6","accept: 2 to 8"]]),result("Stored teams",["id","seats"],[["G1",4],["G3",6]])])

add("ch03", "filter", "## 2. Basic Queries", "Filter rows, then calculate an output column",
    "3.3 Basic Structure of SQL Queries, pp.71-78", "FROM names the input. WHERE keeps rows meeting the condition. SELECT chooses output expressions, and AS gives an output a readable name. The calculation does not update stored credits.",
    [COURSES], "Predict the course IDs and doubled credits for courses with at least 3 credits.",
    [("Selected courses", "SELECT id, credits * 2 AS doubled FROM course WHERE credits >= 3 ORDER BY id")],
    [result("Selected courses",["id","doubled"],[["DB",6],["FIN",6]])],
    "DB and FIN pass the predicate and each displays 6. WEB has 2 credits and is excluded. The stored values for DB and FIN remain 3.",
    "Change the predicate to dept = 'IM' and the expression to credits + 1. Predict both output rows before running.",
    "Check each IM input row and calculate its output independently. Querying the original credits must still return 3, 2, and 3.")

add("ch03", "distinct", "### Duplicates and Expressions", "DISTINCT applies to the whole output row",
    "3.3.1 Queries on a Single Relation; 3.4.1 Rename Operation", "A repeated department is not a duplicate student row. DISTINCT removes repeated complete result rows, so changing the SELECT columns changes what counts as a duplicate.",
    [STUDENTS], "Predict the row counts for DISTINCT dept and DISTINCT dept, id.",
    [("Departments", "SELECT DISTINCT dept FROM student ORDER BY dept"), ("Department and ID", "SELECT DISTINCT dept,id FROM student ORDER BY dept,id")],
    [result("Departments",["dept"],[["FN"],["IM"]]),result("Department and ID",["dept","id"],[["FN","S2"],["IM","S1"],["IM","S3"]])],
    "There are two department rows but three department-ID rows. S1 and S3 have different identifiers, so the two IM rows are distinct when ID is included.",
    "Add S4, Dee, IM and rerun both queries. Record which result count changes.",
    "Compare complete output rows, not only the repeated department value.",
    panels=[result("Input pairs",["dept","id"],[["IM","S1"],["FN","S2"],["IM","S3"]]),result("DISTINCT dept",["dept"],[["FN"],["IM"]]),result("DISTINCT dept, id",["dept","id"],[["FN","S2"],["IM","S1"],["IM","S3"]])])

add("ch03", "patterns", "## 3. Patterns, Ranges, and Ordering", "A pattern, an inclusive range, and an explicit order",
    "3.4 Additional Basic Operations, pp.79-85", "In LIKE, percent matches a sequence of characters and underscore matches one character. BETWEEN includes both endpoints. ORDER BY makes the requested display order explicit.",
    [table("item", "id TEXT, title TEXT, credits INTEGER",["id","title","credits"],[["C1","Data",3],["C2","Design",2],["C3","Web",2]])],
    "Which IDs match titles beginning with D and credits from 2 through 3? Which appears first in descending credit order?",
    [("Pattern and range", "SELECT id,title,credits FROM item WHERE title LIKE 'D%' AND credits BETWEEN 2 AND 3 ORDER BY credits DESC,id")],
    [result("Pattern and range",["id","title","credits"],[["C1","Data",3],["C2","Design",2]])],
    "C1 and C2 satisfy both conditions. C1 precedes C2 because 3 exceeds 2. C3 is excluded by its title even though its credits are inside the range.",
    "Replace D% with _e% and use ORDER BY id. Predict IDs and explain the underscore.",
    "Inspect the second character of each title. Do not infer LIKE case rules for another DBMS from this example.")

add("ch03", "sets", "## 4. SQL Set Operations", "Combining two enrollment lists",
    "3.5 Set Operations, pp.85-89", "UNION removes repeated result rows. UNION ALL retains every copy. INTERSECT keeps shared rows; EXCEPT keeps rows found only on the left.",
    [table("a","id TEXT",["id"],[["S1"],["S2"]]), table("b","id TEXT",["id"],[["S2"],["S3"]])],
    "Predict how many copies of S2 UNION ALL retains and which ID A EXCEPT B returns.",
    [("All copies", "SELECT id FROM a UNION ALL SELECT id FROM b ORDER BY id"), ("Only in A", "SELECT id FROM a EXCEPT SELECT id FROM b ORDER BY id")],
    [result("All copies",["id"],[["S1"],["S2"],["S2"],["S3"]]),result("Only in A",["id"],[["S1"]])],
    "UNION ALL returns four rows, including two S2 copies. A EXCEPT B returns only S1. Both lists have one compatible result column.",
    "Run UNION and INTERSECT, then exchange A and B in EXCEPT. Retain all three outputs.",
    "Account for duplicates separately from membership; reversing EXCEPT changes its meaning.",
    panels=[result("Input lists",["A","B"],[["S1","S2"],["S2","S3"]]),result("UNION ALL",["id"],[["S1"],["S2"],["S2"],["S3"]]),result("A EXCEPT B",["id"],[["S1"]])])

add("ch03", "subquery", "### `EXISTS` and Correlation", "Ask whether a matching row exists for each student",
    "3.8.1 Set Membership; 3.8.2 Set Comparison; 3.8.3 Test for Empty Relations", "A correlated EXISTS query uses the current outer-row identifier inside the inner query. Multiple matches still produce only one copy of that outer student row.",
    [table("person","id TEXT",["id"],[["S1"],["S2"],["S3"]]),table("registration","sid TEXT, course TEXT",["sid","course"],[["S1","DB"],["S1","WEB"],["S2","DB"]])],
    "How many student rows survive EXISTS? Does S1 appear twice because it has two registrations?",
    [("Students with registrations", "SELECT p.id FROM person AS p WHERE EXISTS (SELECT 1 FROM registration AS r WHERE r.sid=p.id) ORDER BY p.id")],
    [result("Students with registrations",["id"],[["S1"],["S2"]])],
    "S1 and S2 each appear once. S3 has no matching inner row. EXISTS tests whether a match is present; it does not join every matching row into the output.",
    "Use NOT EXISTS to find people with no registration, then express the positive query using IN.",
    "Retain the correlated equality r.sid=p.id. Removing it changes the question to whether any registration exists anywhere.")

add("ch03", "cte", "### Common Table Expression", "Name the group result, then filter it",
    "3.8 Nested Subqueries: With Clause", "A CTE gives a query result a name inside one statement. The named result can make two logical steps easier to inspect; it is not a promise about physical materialization.",
    [COURSES], "Predict the department counts and which count passes n >= 2.",
    [("Named counts", "WITH counts AS (SELECT dept,COUNT(*) AS n FROM course GROUP BY dept) SELECT dept,n FROM counts WHERE n>=2 ORDER BY dept")],
    [result("Named counts",["dept","n"],[["IM",2]])],
    "The inner grouping gives FN=1 and IM=2. Only IM passes the outer condition. This output does not show whether the DBMS stored an intermediate table.",
    "Write the equivalent GROUP BY query using HAVING, and compare rows and column names.",
    "The two forms must apply the threshold to groups, not individual credit values.",
    panels=[result("Input",["id","dept"],[["DB","IM"],["WEB","IM"],["FIN","FN"]]),result("counts",["dept","n"],[["FN",1],["IM",2]]),result("n >= 2",["dept","n"],[["IM",2]])])

add("ch03", "modify", "## 8. Data Modification", "Check the target before changing it",
    "3.9 Modification of the Database, pp.108-113", "INSERT adds a row, UPDATE changes selected rows, and DELETE removes selected rows. In this demonstration a savepoint lets us inspect changes and then restore the input.",
    [COURSES], "How many rows will UPDATE target when WHERE id = 'WEB' is present? What does rollback restore?",
    [("Start", "SAVEPOINT demo"),("Change WEB", "UPDATE course SET credits=4 WHERE id='WEB'"),("During change", "SELECT id,credits FROM course ORDER BY id"),("Undo change", "ROLLBACK TO demo"),("Restored", "SELECT id,credits FROM course ORDER BY id"),("Finish", "RELEASE demo")],
    [result("Start",[],[["Statement completed."]]),result("Change WEB",[],[["Statement completed."]]),result("During change",["id","credits"],[["DB",3],["FIN",3],["WEB",4]]),result("Undo change",[],[["Statement completed."]]),result("Restored",["id","credits"],[["DB",3],["FIN",3],["WEB",2]]),result("Finish",[],[["Statement completed."]])],
    "Only WEB changes from 2 to 4. ROLLBACK TO restores its original 2; DB and FIN stay 3 throughout. Without WHERE, all three rows would be update targets.",
    "Inside a savepoint, insert C4 with 2 credits, update it to 3, then delete it. Query after each step and restore the input.",
    "Track the same identifier through absence, insertion, update, and deletion. Keep the target query with each modification.",
    panels=[result("Before",["id","credits"],[["WEB",2]]),result("UPDATE",["id","credits"],[["WEB",4]]),result("ROLLBACK TO",["id","credits"],[["WEB",2]])])

add("ch04", "inner", "## 1. Explicit Inner Joins", "Match identifiers, not unrelated department values",
    "4.1 Join Expressions", "ON states the relationship being followed. An extra equality is an additional rule, not a harmless way to make a query look precise.",
    [table("person","id TEXT, dept TEXT",["id","dept"],[["S1","IM"],["S2","FN"]]),table("takes","sid TEXT, course TEXT, dept TEXT",["sid","course","dept"],[["S1","DB","IM"],["S1","FIN","FN"]])],
    "Should S1's FIN registration survive when the requested relationship is student ID equality?",
    [("ID relationship", "SELECT p.id,t.course FROM person p JOIN takes t ON p.id=t.sid ORDER BY t.course")],
    [result("ID relationship",["id","course"],[["S1","DB"],["S1","FIN"]])],
    "Both registrations belong to S1. FIN remains even though its department differs from S1's major. Requiring p.dept=t.dept would remove a valid registration.",
    "Add the department condition and compare the missing row with the stated requirement.",
    "Explain why the removed row is valid using its student identifier, not the coincidental department names.")

add("ch04", "natural", "## 2. `USING` and `NATURAL JOIN`", "A shared column name can silently add a join condition",
    "4.1 Join Expressions", "USING(id) chooses one same-named column explicitly. NATURAL JOIN uses every common column name, so the schema participates in deciding the predicate.",
    [table("a","id TEXT, label TEXT",["id","label"],[["1","old"],["2","same"]]),table("b","id TEXT, label TEXT",["id","label"],[["1","new"],["2","same"]])],
    "Predict which IDs survive USING(id), and which survive NATURAL JOIN.",
    [("Chosen column", "SELECT a.id FROM a JOIN b USING(id) ORDER BY a.id"),("All common columns", "SELECT id FROM a NATURAL JOIN b ORDER BY id")],
    [result("Chosen column",["id"],[["1"],["2"]]),result("All common columns",["id"],[["2"]])],
    "USING(id) returns 1 and 2. NATURAL JOIN also requires matching labels and returns only 2. The spelling label has changed the query meaning.",
    "Rewrite both joins with ON so every equality is visible.",
    "Compare both outputs. The natural join requires two equalities in this schema.",
    panels=[result("Inputs by ID",["id","A label","B label"],[["1","old","new"],["2","same","same"]]),result("Output IDs",["USING(id)","NATURAL"],[["1, 2","2"]])])

add("ch04", "outer_count", "## 3. Inner and Outer Joins", "An unmatched row is not an enrollment",
    "4.1 Join Expressions; 3.7 Aggregate Functions", "A left join keeps a course even when no registration matches. It pads the right-hand columns with NULL. Counting a required registration ID avoids counting that placeholder as an enrollment.",
    [table("course","id TEXT",["id"],[["DB"],["WEB"]]),table("takes","course TEXT, sid TEXT NOT NULL",["course","sid"],[["DB","S1"],["DB","S2"]])],
    "For WEB, predict COUNT(*) and COUNT(t.sid).",
    [("Two counts", "SELECT c.id,COUNT(*) AS joined_rows,COUNT(t.sid) AS enrollments FROM course c LEFT JOIN takes t ON c.id=t.course GROUP BY c.id ORDER BY c.id")],
    [result("Two counts",["id","joined_rows","enrollments"],[["DB",2,2],["WEB",1,0]])],
    "WEB contributes one null-padded join row, so COUNT(*) is 1. No non-NULL student ID is present, so its enrollment count is 0.",
    "Add a real WEB registration. Predict which of WEB's two counts changes.",
    "Distinguish a retained course row from evidence of a matching registration.",
    panels=[result("Left-join rows",["course","sid"],[["DB","S1"],["DB","S2"],["WEB","NULL"]]),result("Counts",["course","rows","enrollments"],[["DB",2,2],["WEB",1,0]])])

add("ch04", "view", "## 5. Views", "The view reads current base rows",
    "4.2.1 View Definition; 4.2.2 Using Views", "A regular view names a query. It does not freeze the rows that existed when CREATE VIEW ran.",
    [COURSES], "After WEB changes from 2 to 3 credits, will it appear in a previously created three-credit view?",
    [("Define view", "CREATE VIEW three_credit AS SELECT id,credits FROM course WHERE credits=3"),("Before update", "SELECT * FROM three_credit ORDER BY id"),("Update base row", "UPDATE course SET credits=3 WHERE id='WEB'"),("After update", "SELECT * FROM three_credit ORDER BY id")],
    [result("Define view",[],[["Statement completed."]]),result("Before update",["id","credits"],[["DB",3],["FIN",3]]),result("Update base row",[],[["Statement completed."]]),result("After update",["id","credits"],[["DB",3],["FIN",3],["WEB",3]])],
    "The second view query includes WEB. The definition stayed the same, but the base row changed. This demonstrates current-query behavior, not a materialized view.",
    "Change DB to 2 credits in the base table and query the view again. Explain the removed row.",
    "Verify that the row still exists in course; absence from a view need not mean deletion.",
    panels=[result("Base change",["id","old credits","new credits"],[["WEB",2,3]]),result("View before",["id"],[["DB"],["FIN"]]),result("View after",["id"],[["DB"],["FIN"],["WEB"]])])

add("ch04", "constraints", "## 7. Integrity Constraints", "CHECK and NOT NULL reject different cases",
    "4.4.2 Not Null; 4.4.3 Unique; 4.4.4 Check", "CHECK rejects FALSE. A comparison involving NULL can be UNKNOWN and therefore need not be rejected by CHECK. Use NOT NULL when the value is required.",
    [table("optional","rating INTEGER CHECK(rating BETWEEN 1 AND 5)",["rating"],[[3]]),table("required","rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5)",["rating"],[[3]])],
    "Predict whether NULL is accepted by each table and whether 6 is accepted by required.",
    [("Optional NULL", "INSERT INTO optional VALUES (NULL)"),("Required NULL", "INSERT INTO required VALUES (NULL)"),("Required 6", "INSERT INTO required VALUES (6)"),("Optional rows", "SELECT rating FROM optional ORDER BY rating")],
    [result("Optional NULL",[],[["Statement completed."]]),result("Required NULL",[],[["IntegrityError: the statement was rejected."]]),result("Required 6",[],[["IntegrityError: the statement was rejected."]]),result("Optional rows",["rating"],[[None],[3]])],
    "The optional table accepts NULL. The required table rejects NULL and 6 for different reasons: absence violates NOT NULL, while 6 violates the range.",
    "Test 1 and 5 separately, then add UNIQUE(rating) and test a repeated 3.",
    "Retain one case for each rule. Do not use one row with several violations to infer constraint-check order.",
    panels=[result("Candidate values",["value"],[["NULL"],[6],[3]]),result("Decisions",["value","CHECK only","NOT NULL + CHECK"],[["NULL","accept","reject"],[6,"reject","reject"],[3,"accept","accept"]])])

add("ch04", "cascade", "## 8. Foreign-Key Actions", "Delete the parent and inspect the dependent rows",
    "4.4.5 Referential Integrity", "A foreign key connects a child value to an existing parent key. ON DELETE CASCADE removes dependent child rows when their parent is deleted; it does not delete unrelated parents or children.",
    [table("person","id TEXT NOT NULL PRIMARY KEY",["id"],[["S1"],["S2"]]),table("request","id TEXT, sid TEXT REFERENCES person(id) ON DELETE CASCADE",["id","sid"],[["R1","S1"],["R2","S1"],["R3","S2"]])],
    "Which request IDs survive deleting S1? Does S2 survive?",
    [("Delete S1", "DELETE FROM person WHERE id='S1'"),("Remaining requests", "SELECT * FROM request ORDER BY id"),("Remaining people", "SELECT * FROM person ORDER BY id")],
    [result("Delete S1",[],[["Statement completed."]]),result("Remaining requests",["id","sid"],[["R3","S2"]]),result("Remaining people",["id"],[["S2"]])],
    "R1 and R2 depend on S1 and are removed. R3 and S2 remain. This rule is suitable only when the dependent data should disappear with its parent.",
    "Replace CASCADE with SET NULL in the table definition and repeat. Then remove the action and repeat again.",
    "Inspect surviving child rows and NULL references; the default immediate foreign-key check should reject a parent deletion that leaves references.",
    panels=[result("Before requests",["id","sid"],[["R1","S1"],["R2","S1"],["R3","S2"]]),result("Delete parent S1",["effect"],[["remove R1"],["remove R2"],["keep R3"]]),result("After requests",["id","sid"],[["R3","S2"]])])

add("ch05", "contract", "## 1. Functions, Procedures, and Triggers", "One input value, one calculated result",
    "5.2 Functions and Procedures, pp.198-205", "A routine interface states the input and returned value or effect. The query below checks the body of a department-count function. SQLite does not install a stored SQL function here.",
    [COURSES], "Predict the function-body count for IM and for a department code that is absent.",
    [("Count for IM", "SELECT COUNT(*) AS n FROM course WHERE dept='IM'"),("Count for ZZ", "SELECT COUNT(*) AS n FROM course WHERE dept='ZZ'")],
    [result("Count for IM",["n"],[[2]]),result("Count for ZZ",["n"],[[0]])],
    "IM gives 2 and ZZ gives 0. The count has a defined result even when no row matches. This checks the calculation, not stored-routine installation or an application's full error policy.",
    "Describe a procedure that changes one course's credits. State its two inputs and what an absent course ID should mean; verify the proposed UPDATE target with SELECT.",
    "Distinguish a returned count from a data modification and from an automatically triggered action. Do not report a procedure as installed in SQLite.",
    panels=[result("Input",["department"],[["IM"],["ZZ"]]),result("Body query",["operation"],[["count matching courses"]]),result("Return value",["department","n"],[["IM",2],["ZZ",0]])])

add("ch05", "trigger_null", "## 2. Row-Level Audit Trigger", "Record a transition from ungraded to graded",
    "5.3 Triggers, pp.206-212", "An AFTER UPDATE trigger can inspect OLD and NEW values. SQLite IS NOT detects a changed value even when one side is NULL; an ordinary inequality does not reliably do that.",
    [table("grade","sid TEXT NOT NULL PRIMARY KEY, value TEXT",["sid","value"],[["S1",None]]),table("audit","old_value TEXT, new_value TEXT",["old_value","new_value"],[])],
    "Will changing NULL to B create one audit row? Will assigning B a second time create another?",
    [("Define trigger", "CREATE TRIGGER record_grade AFTER UPDATE OF value ON grade FOR EACH ROW WHEN OLD.value IS NOT NEW.value BEGIN INSERT INTO audit VALUES (OLD.value,NEW.value); END"),("First update", "UPDATE grade SET value='B' WHERE sid='S1'"),("Same value again", "UPDATE grade SET value='B' WHERE sid='S1'"),("Audit rows", "SELECT old_value,new_value FROM audit")],
    [result("Define trigger",[],[["Statement completed."]]),result("First update",[],[["Statement completed."]]),result("Same value again",[],[["Statement completed."]]),result("Audit rows",["old_value","new_value"],[[None,"B"]])],
    "Only the NULL-to-B transition appears. The second update leaves the value unchanged, so the WHEN condition prevents an extra audit record.",
    "Change B back to NULL and inspect the second audit row. Explain which value belongs to OLD and which to NEW.",
    "Count actual changes, not UPDATE statements. Keep the nullable case; it is the reason for the null-safe comparison.",
    panels=[result("First update",["OLD","NEW"],[["NULL","B"]]),result("Second update",["OLD","NEW"],[["B","B"]]),result("Audit",["old_value","new_value"],[["NULL","B"]])])

add("ch05", "recursion", "## 3. Recursive CTEs", "Follow a chain one edge at a time",
    "5.4 Recursive Queries, pp.213-218", "The base term returns the direct prerequisites of C. The recursive term follows an edge from the current node. UNION removes repeated complete result rows; here each result row contains just node, so a known node is not added again.",
    [table("edge","course TEXT, prerequisite TEXT",["course","prerequisite"],[["C","B"],["B","A"]])],
    "Starting at C, which prerequisites appear in the base term and after one recursive step?",
    [("Prerequisites of C", "WITH RECURSIVE reach(node) AS (SELECT prerequisite FROM edge WHERE course='C' UNION SELECT e.prerequisite FROM edge e JOIN reach r ON e.course=r.node) SELECT node FROM reach ORDER BY node")],
    [result("Prerequisites of C",["node"],[["A"],["B"]])],
    "The base term finds B. Following B's edge adds A. A has no outgoing prerequisite edge, so no further node is added. The final ORDER BY sorts labels; it does not show discovery order.",
    "Add edge A to Z and predict the additional recursive step. Then explain why adding a changing depth column would require a new termination argument on cyclic data.",
    "Trace edge direction and complete-row duplicate removal separately. A depth limit alone would not prove the data is acyclic.",
    panels=[result("Input edges",["course","prerequisite"],[["C","B"],["B","A"]]),result("Trace",["round","new node"],[["base","B"],["recursive 1","A"],["recursive 2","none"]]),result("Final set",["node"],[["A"],["B"]])])

add("ch05", "frames", "## 5. Partitions and Window Frames", "A running total keeps each detail row",
    "5.5 Advanced Aggregation Features: Windowing", "GROUP BY combines rows. A window calculation can retain every row and compute a value over related rows. Here PARTITION BY restarts the total for each student, and the explicit ROWS frame includes the current and preceding rows.",
    [table("attempt","sid TEXT, attempt_no INTEGER, points INTEGER",["sid","attempt_no","points"],[["S1",1,10],["S1",2,20],["S1",3,30],["S2",1,7]])],
    "Predict S1's three running totals and S2's first total. How many output rows remain?",
    [("Running totals", "SELECT sid,attempt_no,SUM(points) OVER (PARTITION BY sid ORDER BY attempt_no ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS total FROM attempt ORDER BY sid,attempt_no")],
    [result("Running totals",["sid","attempt_no","total"],[["S1",1,10],["S1",2,30],["S1",3,60],["S2",1,7]])],
    "S1 accumulates 10, then 30, then 60. S2 starts a new partition at 7. All four attempts remain visible; a grouped student total would return only two rows.",
    "Change the frame to 1 PRECEDING AND CURRENT ROW. Predict the total for S1's third attempt and explain which earlier row is excluded.",
    "Write the included attempt numbers for each frame before adding the points.")

add("ch05", "pivot", "## 6. Short Extension: Conditional Aggregation", "Turn known attempt numbers into fixed columns",
    "5.5 Advanced Aggregation Features", "CASE chooses the values for a particular output column. MAX then reduces each student's matching value to one cell. This short illustration is extension reading, not a new required pivot language.",
    [table("score","sid TEXT, attempt INTEGER, points INTEGER",["sid","attempt","points"],[["S1",1,6],["S1",2,9],["S2",1,8]])],
    "What will the second-attempt column contain for S2?",
    [("Fixed columns", "SELECT sid,MAX(CASE WHEN attempt=1 THEN points END) AS first,MAX(CASE WHEN attempt=2 THEN points END) AS second FROM score GROUP BY sid ORDER BY sid")],
    [result("Fixed columns",["sid","first","second"],[["S1",6,9],["S2",8,None]])],
    "S2 has no second attempt, so second is NULL, not zero. The CASE expressions define exactly two attempt columns.",
    "As optional practice, add attempt 3. Explain why the result does not automatically gain a third column.",
    "Separate missing observations from zero points and fixed output columns from changing categories.")

add("ch06", "stages", "## 1. Design Stages", "One requirement appears differently in a diagram and a table",
    "6.1 Overview of the Design Process, pp.241-243", "Requirements describe allowed facts. A conceptual relationship records the association. Relational mapping implements it with columns and constraints; an index belongs to a later physical decision.",
    [table("rules","",["object","rule"],[["Student","exactly one major"],["Department","zero or more students"]])],
    "Which side should receive a foreign-key column when a student has exactly one department?",
    [],[],
    "Student receives a required department reference because many students can share one department. The conceptual relationship and the foreign-key column are two representations of the same association, not two independent facts.",
    "Change the rule to allow an undeclared student. Identify the conceptual minimum and the column constraint that must change.",
    "Explain optional participation using the rule, then check whether a NULL department reference is allowed.",
    panels=[result("Requirement",["fact"],[["one major per student"]]),result("Conceptual",["association"],[["Student majors in Department"]]),result("Relational",["Student column"],[["dept NOT NULL"],["FK to Department"]])])

add("ch06", "separate", "## 2. Redundancy and Incompleteness", "A course exists before its first section",
    "6.1 Overview of the Design Process; 6.2 The Entity-Relationship Model", "A course title describes the course, not a particular teaching section. Separate course facts from section facts so an unoffered course still has a place to be stored.",
    [table("flat","",["course","title","section"],[["DB","Database",1],["DB","Database",2]])],
    "If WEB has no section, where can its title be stored without inventing a section?",
    [],[],
    "Course stores DB and WEB independently. Section stores only the two actual DB sections. DB's title is written once, and WEB does not require a fake section.",
    "Add a third DB section and rename Database to Database Systems. Count the title values that need changing in each design.",
    "Preserve the two kinds of facts and every existing section. A smaller number of tables alone is not the design criterion.",
    panels=[result("Mixed rows",["course","title","section"],[["DB","Database",1],["DB","Database",2]]),result("Course",["course","title"],[["DB","Database"],["WEB","Web Design"]]),result("Section",["course","section"],[["DB",1],["DB",2]])])

add("ch06", "attributes", "## 3. Entities and Attributes", "Split a name, keep multiple phones, calculate a total",
    "6.2 The Entity-Relationship Model; 6.3 Complex Attributes, pp.249-251", "An attribute's structure depends on the facts the application needs. A name can have components, phone can have multiple values, and completed credits can be derived from completed courses.",
    [table("facts","",["student","fact","value"],[["S1","name","Amy Lin"],["S1","phones","111; 222"],["S1","passed credits","3 and 2"]])],
    "How many phone rows are needed, and what is the derived credit total?",
    [],[],
    "The name has two components, the two phone values become two rows, and completed credits total 5 under the stated rule. Storing a total separately would require keeping it consistent after grade or credit changes.",
    "Suppose each phone needs a type such as home or office. Draw the extra attribute and explain whether Phone needs its own identity under your requirements.",
    "Distinguish several phone values from several components of one value. State the calculation rule for derived data.",
    panels=[result("Name components",["first","last"],[["Amy","Lin"]]),result("Phone rows",["student","phone"],[["S1","111"],["S1","222"]]),result("Derived credits",["calculation","result"],[["3 + 2",5]])])

add("ch06", "roles", "## 4. Relationships, Roles, and Degree", "The same entity set can play two roles",
    "6.2 The Entity-Relationship Model: Relationship Sets", "A recursive prerequisite relationship connects Course to Course. Role names identify which course requires the other. Reversing the roles reverses the question.",
    [table("prerequisite","course TEXT, required_course TEXT",["course","required_course"],[["B","A"],["C","B"]])],
    "Which course is required by B, and which course directly requires B?",
    [("Required by B", "SELECT required_course FROM prerequisite WHERE course='B'"),("Directly requires B", "SELECT course FROM prerequisite WHERE required_course='B'")],
    [result("Required by B",["required_course"],[["A"]]),result("Directly requires B",["course"],[["C"]])],
    "B requires A, while C requires B. Both columns refer to Course, but they have different roles. These are direct relationships, not the recursive closure computed in Chapter 5.",
    "Draw both associations with a legend saying what the arrow means. Explain why B-to-A does not mean A requires B.",
    "Every edge must be readable as a complete sentence with the two course roles named.",
    panels=[result("B in the course role",["course","requires"],[["B","A"]]),result("B in the prerequisite role",["course","requires"],[["C","B"]])])

add("ch06", "weak", "## 6. Keys and Weak Entities", "Section number is unique only within its owner and term",
    "6.5 Primary Key: Weak Entity Sets; 6.7 Reducing E-R Diagrams", "A weak entity's discriminator is not a global identifier. In this case, section number and term distinguish sections only within one Course. The owner's key must participate in the complete identifier.",
    [table("section","course TEXT, term TEXT, number INTEGER",["course","term","number"],[["DB","T1",1],["WEB","T1",1],["DB","T2",1]])],
    "Is number alone unique? Is course plus number unique across both terms?",
    [("Repeated partial keys", "SELECT course,number,COUNT(*) AS n FROM section GROUP BY course,number HAVING COUNT(*)>1 ORDER BY course")],
    [result("Repeated partial keys",["course","number","n"],[["DB",1,2]])],
    "DB/1 occurs in T1 and T2. Number alone also repeats across courses. The complete course-term-number key distinguishes all three rows and reflects the stated ownership rule.",
    "Add WEB/T2/1, then propose an Enrollment foreign key that names one exact section.",
    "Carry all three section-key components into the reference. A foreign key to section number alone does not identify the intended row.")

add("ch06", "many", "### Many-to-Many Relationship", "Store the grade on the student-section association",
    "6.7 Reducing E-R Diagrams to Relational Schemas", "A student may attend several sections and a section may have several students. A separate Enrollment relation stores each association and its grade. One grade column on Student cannot represent a different grade in each section.",
    [table("enrollment","student TEXT, section TEXT, grade TEXT",["student","section","grade"],[["S1","DB-T1-1","A"],["S1","WEB-T1-1","B"],["S2","DB-T1-1","B+"]])],
    "How many grades does S1 need, and how many enrollment rows belong to DB-T1-1?",
    [("S1's grades", "SELECT section,grade FROM enrollment WHERE student='S1' ORDER BY section"),("DB section count", "SELECT COUNT(*) AS n FROM enrollment WHERE section='DB-T1-1'")],
    [result("S1's grades",["section","grade"],[["DB-T1-1","A"],["WEB-T1-1","B"]]),result("DB section count",["n"],[[2]])],
    "S1 has two association-specific grades, and DB-T1-1 has two students. Here section strings are display labels for complete section identities; the full course schema uses the separate key components.",
    "Add S2 to WEB-T1-1 with grade A-. Explain why this adds an association, not a new student or section.",
    "Keep entity identity separate from relationship instances and keep grade with the relationship.",
    panels=[result("S1 associations",["section","grade"],[["DB-T1-1","A"],["WEB-T1-1","B"]]),result("DB-T1-1 associations",["student","grade"],[["S1","A"],["S2","B+"]])])

add("ch06", "identity", "## 9. Design Choices Require Evidence", "A new requirement can justify a new entity",
    "6.9 Entity-Relationship Design Issues, pp.279-284", "Choose an entity when the requirements need an independently identifiable object with its own facts or relationships. Do not add an entity solely because a noun appears in a sentence.",
    [table("rules","",["case","required facts"],[["A","student, section, grade"],["B","registration ID, payment, appeal"]])],
    "In which case does an appeal need to refer to one identifiable registration?",
    [],[],
    "Case A can keep grade on the Student-Section relationship. Case B needs a registration that an appeal can reference. A Registration entity is a defensible design for that requirement, but uniqueness of the underlying student-section association may still be needed.",
    "Suppose repeated registration attempts must be retained. State which attempt identity or rule distinguishes them before drawing the revised design.",
    "Name the new fact or relationship the design must preserve; do not claim that adding a surrogate ID automatically enforces every business rule.",
    panels=[result("Case A",["association"],[["Student -- Section"],["grade belongs here"]]),result("Case B",["identifiable object"],[["Registration ID R1"],["payment and appeal refer to R1"]])])

add("ch07", "anomaly", "## 1. Mixed Facts and Anomalies", "Deleting an enrollment can erase a course fact",
    "7.1 Features of Good Relational Designs, pp.303-307", "An enrollment row and a course description are different facts. When only one mixed row contains a course's description, deleting the enrollment also removes that description.",
    [table("flat","student TEXT, course TEXT, title TEXT",["student","course","title"],[["S1","DB","Database"],["S2","DB","Database"],["S1","WEB","Web Design"]])],
    "After deleting S1's WEB enrollment, can this table still tell us WEB's title?",
    [("Delete enrollment", "DELETE FROM flat WHERE student='S1' AND course='WEB'"),("Remaining course facts", "SELECT DISTINCT course,title FROM flat ORDER BY course")],
    [result("Delete enrollment",[],[["Statement completed."]]),result("Remaining course facts",["course","title"],[["DB","Database"]])],
    "Only DB's title remains. WEB may still be a valid course, but the mixed table lost its only description. A separate Course relation allows deletion of an enrollment without deleting the course fact.",
    "Identify the insertion problem for a new course with no student, and the update problem when only one DB title copy is renamed.",
    "For each anomaly, name the valid fact that is lost, impossible to insert naturally, or made inconsistent.")

add("ch07", "dependency", "## 2. Functional Dependencies", "Two rows can disprove a proposed dependency",
    "7.2 Decomposition Using Functional Dependencies, pp.308-312", "X determines Y when every legal pair agreeing on X also agrees on Y. A single counterexample can disprove a proposed rule; a convenient sample cannot establish that the rule holds in every future state.",
    [table("registration","student TEXT, course TEXT",["student","course"],[["S1","DB"],["S1","WEB"],["S2","DB"]])],
    "Does this instance satisfy student -> course? Which two rows decide the answer?",
    [("Conflicting course values", "SELECT student,COUNT(DISTINCT course) AS different_courses FROM registration GROUP BY student HAVING COUNT(DISTINCT course)>1 ORDER BY student")],
    [result("Conflicting course values",["student","different_courses"],[["S1",2]])],
    "S1 agrees on student but has two different courses. That pair violates student -> course. Removing one row would remove the counterexample, not prove a permanent one-course-per-student rule.",
    "Construct two legal courses with the same title to test the proposed dependency title -> course ID.",
    "Write both rows and the supporting business permission. Distinguish disproof by a legal instance from a rule stated by requirements.")

add("ch07", "closure", "## 3. Attribute Closure and Candidate Keys", "Follow dependencies until no new attribute appears",
    "7.4 Functional-Dependency Theory: Closure of Attribute Sets", "A closure is the set of attributes determined by the starting attributes under the stated dependencies. Test minimality by removing each proposed key component, not by counting unique rows in a sample.",
    [table("dependencies","",["left side","right side"],[["employee","name"],["project","title"],["employee, project","hours"]])],
    "Starting with employee and project, can you reach every attribute? What is missing from employee alone?",
    [],[],
    "The pair reaches name, title, and hours, so it determines all five attributes. Employee alone cannot reach project, title, or hours. Project alone cannot reach employee, name, or hours. Therefore the pair is a candidate key under exactly these dependencies.",
    "Add the rule project -> employee and recompute the candidate key. Record the closure steps, not just the final key.",
    "A newly added dependency can change the key. State the full rule set used for each conclusion.",
    panels=[result("Start",["known"],[["employee"],["project"]]),result("Apply rules",["from","add"],[["employee","name"],["project","title"],["both","hours"]]),result("Closure",["determined"],[["employee, project"],["name, title, hours"]])])

add("ch07", "lossless", "## 4. Lossless Decomposition", "A shared department key reconstructs the same facts",
    "7.1 Features of Good Relational Designs; 7.2 Decomposition Using Functional Dependencies", "For a binary decomposition under functional dependencies, a sufficient and necessary lossless-join condition is that the shared attributes determine one whole side. Sample reconstruction checks illustrate the result; the dependency supplies the general reason.",
    [table("flat","student TEXT, dept TEXT, name TEXT",["student","dept","name"],[["S1","IM","Information"],["S2","IM","Information"],["S3","FN","Finance"]])],
    "Will projecting Student(student,dept) and Department(dept,name) and joining them create a new combination under dept -> name?",
    [("Reconstructed", "WITH s AS (SELECT DISTINCT student,dept FROM flat), d AS (SELECT DISTINCT dept,name FROM flat) SELECT s.student,s.dept,d.name FROM s JOIN d USING(dept) ORDER BY s.student")],
    [result("Reconstructed",["student","dept","name"],[["S1","IM","Information"],["S2","IM","Information"],["S3","FN","Finance"]])],
    "The three original rows are reconstructed. The shared dept determines the Department side because each code has one name. This is the reason the decomposition is lossless for legal data under that dependency.",
    "Explain why replacing the shared key with a nonunique person name fails in the Kim example below. Retain the extra reconstructed pairs.",
    "Distinguish a dependency argument from a test of only three rows.",
    panels=[result("Student",["student","dept"],[["S1","IM"],["S2","IM"],["S3","FN"]]),result("Department",["dept","name"],[["IM","Information"],["FN","Finance"]]),result("Join",["student","dept","name"],[["S1","IM","Information"],["S2","IM","Information"],["S3","FN","Finance"]])])

add("ch07", "bcnf", "## 5. Boyce-Codd Normal Form", "Ask whether the determinant identifies the entire row",
    "7.3 Normal Forms: Boyce-Codd Normal Form", "BCNF requires a superkey on the left of every nontrivial dependency. A determinant may identify a department fact without identifying the whole mixed enrollment row.",
    [table("rules","",["relation","dependency"],[["Mixed(student,dept,name)","student -> dept; dept -> name"],["Department(dept,name)","dept -> name"]])],
    "In which relation does dept determine every attribute?",
    [],[],
    "In Mixed, dept cannot determine student, so dept -> name violates BCNF. In Department, dept determines both attributes and is a key. The same dependency has a different consequence when the relation schema changes.",
    "Give two students in one department to demonstrate why dept is not a key of Mixed. Then identify the key of Student(student,dept).",    "Use the relation's complete attribute set when deciding whether the determinant is a superkey.",
    panels=[result("Mixed",["dept determines","missing"],[["dept, name","student"]]),result("Decompose",["relation","key"],[["Student(student,dept)","student"],["Department(dept,name)","dept"]])])

add("ch07", "third", "## 6. Third Normal Form", "A prime attribute explains the 3NF exception",
    "7.3 Normal Forms: Third Normal Form", "A prime attribute belongs to at least one candidate key. For a nontrivial dependency, 3NF permits a non-superkey determinant when each remaining right-side attribute is prime. BCNF does not have that exception.",
    [table("rules","",["left side","right side"],[["student, course","teacher"],["teacher","course"]])],
    "Given the keys (student,course) and (student,teacher), is course prime? Is teacher alone a superkey?",
    [],[],
    "Course is prime because it belongs to the first key. Teacher alone cannot determine student, so it is not a superkey. Thus teacher -> course violates BCNF but meets the 3NF prime-attribute condition under these dependencies.",
    "Show how each stated pair reaches all three attributes, then remove one component from each pair to test minimality.",
    "Use both candidate keys. Checking only a chosen primary key can miss prime attributes.",
    panels=[result("Candidate keys",["key"],[["student + course"],["student + teacher"]]),result("teacher -> course",["test","result"],[["teacher superkey?","no"],["course prime?","yes"]]),result("Classification",["3NF","BCNF"],[["yes","no"]])])

add("ch14", "search_key", "## 1. Index and Search Key", "An index search value need not be unique",
    "14.1 Basic Concepts, pp.623-624", "An index search key is the value used to locate records. It is not necessarily a candidate key. A grade lookup may identify several enrollment rows, while the enrollment ID identifies one row.",
    [table("entry","id TEXT NOT NULL PRIMARY KEY, grade TEXT",["id","grade"],[["E1","A"],["E2","B"],["E3","A"]])],
    "How many records must a grade-A lookup return? Would making grade UNIQUE preserve the stated data?",
    [("Grade A", "SELECT id,grade FROM entry WHERE grade='A' ORDER BY id")],
    [result("Grade A",["id","grade"],[["E1","A"],["E3","A"]])],
    "A identifies E1 and E3. A nonunique index can support both matches. UNIQUE(grade) would reject valid repeated grades and change the logical rules.",
    "Add E4 with grade A and predict the result. Explain why CREATE INDEX and CREATE UNIQUE INDEX express different promises.",
    "Separate access-path choices from uniqueness constraints.",
    panels=[result("Table",["id","grade"],[["E1","A"],["E2","B"],["E3","A"]]),result("Schematic grade entries",["grade","record IDs"],[["A","E1, E3"],["B","E2"]]),result("A lookup",["id"],[["E1"],["E3"]])])

add("ch14", "range", "### Range Lookup", "Follow ordered leaves until the upper bound is exceeded",
    "14.3 B+-Tree Index Files: Queries on B+-Trees", "For an inclusive range, first find the earliest qualifying entry, then follow ordered leaf entries. Stop when the next key exceeds the upper bound. This is a schematic traversal, not a SQLite page-layout claim.",
    [table("leaf_keys","key INTEGER",["key"],[[10],[20],[30],[40],[50],[60],[70],[80],[90]])],
    "For 45 <= key <= 80, which key is first returned, which is last returned, and which establishes the stop?",
    [("Range result", "SELECT key FROM leaf_keys WHERE key BETWEEN 45 AND 80 ORDER BY key")],
    [result("Range result",["key"],[[50],[60],[70],[80]])],
    "The result begins at 50 because 45 is absent, includes 80 because the bound is inclusive, and stops before 90. The SQL checks the values; the accompanying traversal is a textbook model.",
    "Change the upper bound to key < 80. Identify the returned values and the first value that fails the condition.",
    "State inclusive versus exclusive bounds. Do not count missing key 45 as a returned entry.",
    panels=[result("Descend",["target","first entry"],[[45,50]]),result("Follow leaf order",["return"],[[50],[60],[70],[80]]),result("Stop",["next key","reason"],[[90,"above 80"]])])

add("ch14", "writes", "## 2. Workload Evidence", "An indexed value change also changes index entries",
    "14.1 Basic Concepts; 14.3 B+-Tree Index Files", "An index is additional maintained data. Updating an indexed value changes where the record belongs in that index, while a nonindexed attribute change need not change the search-key entry. Exact I/O cost depends on the implementation.",
    [table("workload","",["operation","frequency"],[["lookup one student","many times"],["change a grade","many times"],["search by grade","rarely"]])],
    "If E2 changes from B to A in a grade index, which old entry must stop referring to E2 and which entry gains it?",
    [],[],
    "The B entry loses E2 and the A entry gains E2. Frequent grade changes create maintenance work even when grade lookups are rare. The diagram does not measure pages, time, or the final optimizer choice.",
    "Compare a student-ID index and a grade index for the displayed workload. Name the query each supports and a write or storage cost still to investigate.",
    "An index recommendation needs a query benefit and a maintenance discussion, not simply an index on every searchable column.",
    panels=[result("Before grade index",["grade","IDs"],[["A","E1"],["B","E2"]]),result("Update E2",["old","new"],[["B","A"]]),result("After grade index",["grade","IDs"],[["A","E1, E2"],["B","none"]])])

add("ch15", "workflow", "## 1. From SQL to Execution", "Separate a valid request from the plan used to answer it",
    "15.1 Overview, pp.689-691", "Parsing and translation check the query and produce a logical representation. Optimization chooses physical operations. Evaluation runs those operations. A misspelled column fails before an index can make the query useful.",
    [table("request","",["SQL request"],[["Return the course with ID DB"]])],
    "Where is an unknown column detected, and where are actual result rows produced?",
    [],[],
    "Name checking belongs to parsing/translation. Choosing a scan or search belongs to optimization. Producing the returned rows belongs to evaluation. SQL text specifies the result, not a required physical route.",
    "Classify three observations: an unknown column error, a SEARCH line in a plan, and one returned DB row. Give a reason for each.",
    "Do not label a name-resolution error as an index-performance problem.",
    panels=[result("Parse and translate",["work"],[["check names and syntax"],["describe required rows"]]),result("Optimize",["work"],[["compare valid access paths"],["choose a plan"]]),result("Evaluate",["work"],[["run operators"],["return rows"]])])

add("ch15", "nested", "## 4. Reading a Join Plan", "A small outer result drives the inner lookups",
    "15.5 Join Operation: Nested-Loop Join and Indexed Nested-Loop Join", "In a nested-loop join, each outer row drives work on the inner input. An indexed inner lookup can find matching keys without repeating a complete inner scan. The number of matching rows is different from the number of candidate pairs.",
    [table("department","id TEXT",["id"],[["IM"],["FN"]]),table("course","id TEXT, dept TEXT",["id","dept"],[["DB","IM"],["WEB","IM"],["FIN","FN"]])],
    "How many candidate pairs exist for a plain two-by-three comparison, and how many pairs satisfy equal department IDs?",
    [("Matched pairs", "SELECT d.id AS dept,c.id AS course FROM department d JOIN course c ON d.id=c.dept ORDER BY d.id,c.id")],
    [result("Matched pairs",["dept","course"],[["FN","FIN"],["IM","DB"],["IM","WEB"]])],
    "Two outer rows and three inner rows give six possible comparisons in the simple nested-loop model. Only three pairs match. An inner index would support two keyed lookups, which may each return several rows; two lookups is not a claim of two page reads.",
    "Filter the outer input to IM and trace the remaining lookup. Then inspect the actual lab plan before claiming that this is its chosen join order.",
    "Keep logical matches, modeled comparisons, displayed plan operations, and measured I/O separate.",
    panels=[result("Outer row",["department"],[["FN"],["IM"]]),result("Inner-key lookup",["key","matching courses"],[["FN","FIN"],["IM","DB, WEB"]]),result("Join result",["dept","course"],[["FN","FIN"],["IM","DB"],["IM","WEB"]])])

add("ch15", "evidence", "## 5. Evidence and Limits", "A plan label is not an elapsed-time measurement",
    "15.2 Measures of Query Cost, pp.692-694", "A compact plan describes chosen access methods. It does not by itself provide actual execution time or every row, page, and memory count. Compare results first, then make only the claim supported by the displayed evidence.",
    [table("evidence","",["before","after"],[["SCAN course","SEARCH course using title index"],["C7, Databases","C7, Databases"]])],
    "Does the displayed evidence establish an access-path change, a result change, or a measured speedup?",
    [],[],
    "The access path changes, while the displayed result is unchanged. No elapsed time appears, so a speedup percentage cannot be calculated. These are schematic labels; the lab supplies the actual SQLite plans.",
    "Write one supported sentence and one claim that would require controlled timing measurements.",
    "Name the observed operator and retained result; do not turn an estimated or schematic plan into a runtime benchmark.",
    panels=[result("Observed in this display",["fact"],[["SCAN becomes SEARCH"],["same C7 row"]]),result("Not measured",["quantity"],[["elapsed time"],["page reads"],["memory used"]])])

add("ch16", "equivalence", "## 1. What an Optimizer Does", "Keep the requested rows while changing the expression",
    "16.1 Overview, pp.743-746; 16.2 Transformation of Relational Expressions", "An alternative expression must retain the intended result. The small example checks an inclusive range written in two ways. It is a logical comparison, not a claim that the planner must choose different physical plans.",
    [table("value_list","x INTEGER",["x"],[[1],[2],[2],[3],[4],[None]])],
    "Will x BETWEEN 2 AND 3 and x >= 2 AND x <= 3 retain the same duplicates and NULL behavior?",
    [("BETWEEN", "SELECT x FROM value_list WHERE x BETWEEN 2 AND 3 ORDER BY x"),("Two comparisons", "SELECT x FROM value_list WHERE x>=2 AND x<=3 ORDER BY x")],
    [result("BETWEEN",["x"],[[2],[2],[3]]),result("Two comparisons",["x"],[[2],[2],[3]])],
    "Both forms return two copies of 2 and one 3. NULL does not pass either predicate. The inclusive-range definition explains the equivalence for these numeric comparisons; the matching sample is an additional check, not a general license to rewrite arbitrary SQL.",
    "Change the second query to x > 2 AND x <= 3. Identify the exact rows lost and explain why performance comparison must wait.",
    "Check boundaries, duplicates, NULL, and result columns before comparing plans.",
    panels=[result("Input x",["x"],[[1],[2],[2],[3],[4],["NULL"]]),result("BETWEEN 2 AND 3",["x"],[[2],[2],[3]]),result(">= 2 AND <= 3",["x"],[[2],[2],[3]])])

add("ch16", "average", "## 3. Statistics and Selectivity", "An average is not the frequency of every value",
    "16.3 Estimating Statistics of Expression Results, pp.757-765", "Under a uniform-value assumption, estimated matches equal total rows divided by distinct values. Selectivity is the matching fraction. The assumption must be stated because actual frequencies may differ.",
    [table("event","kind TEXT",["kind"],[["A"],["A"],["A"],["A"],["A"],["B"]])],
    "With six rows and two distinct values, what does the uniform estimate predict for B? What is B's actual count?",
    [("Actual frequencies", "SELECT kind,COUNT(*) AS n FROM event GROUP BY kind ORDER BY kind")],
    [result("Actual frequencies",["kind","n"],[["A",5],["B",1]])],
    "The uniform estimate is 6/2 = 3 rows for either value. Actual B has 1 row, so its selectivity is 1/6, about 16.7%, not 50%. This difference alone does not determine whether an index is chosen.",
    "Replace two A rows with B rows and recompute the estimate and actual frequencies.",
    "Retain the total, distinct count, assumption, and actual grouped counts. Do not label estimated rows as observed rows.",
    panels=[result("Statistics",["total rows","distinct values"],[[6,2]]),result("Uniform estimate",["kind","rows"],[["A",3],["B",3]]),result("Actual counts",["kind","rows"],[["A",5],["B",1]])])

add("ch16", "analyze", "## 4. `ANALYZE` and Plan Evidence", "Refresh statistics after the stored data changes",
    "16.3 Estimating Statistics of Expression Results; SQLite ANALYZE documentation", "SQLite ANALYZE updates planner statistics. In this single-column example, sqlite_stat1 describes the index row count and an average count per distinct key. It is not a list of exact per-value frequencies.",
    [table("event","kind TEXT",["kind"],[["A"],["A"],["A"],["A"],["A"],["B"]])],
    "After adding two B rows, will actual row count change immediately? Will the saved sqlite_stat1 string change before ANALYZE runs again?",
    [("Create index", "CREATE INDEX event_kind ON event(kind)"),("Collect statistics", "ANALYZE"),("Initial statistics", "SELECT stat FROM sqlite_stat1 WHERE idx='event_kind'"),("Add data", "INSERT INTO event VALUES ('B'),('B')"),("Actual total", "SELECT COUNT(*) AS n FROM event"),("Still-saved statistics", "SELECT stat FROM sqlite_stat1 WHERE idx='event_kind'"),("Refresh", "ANALYZE"),("Refreshed statistics", "SELECT stat FROM sqlite_stat1 WHERE idx='event_kind'")],
    [result("Create index",[],[["Statement completed."]]),result("Collect statistics",[],[["Statement completed."]]),result("Initial statistics",["stat"],[["6 3"]]),result("Add data",[],[["Statement completed."]]),result("Actual total",["n"],[[8]]),result("Still-saved statistics",["stat"],[["6 3"]]),result("Refresh",[],[["Statement completed."]]),result("Refreshed statistics",["stat"],[["8 4"]])],
    "The actual total becomes 8 while the saved statistics remain 6 3. After ANALYZE, the string becomes 8 4. Neither average, 3 nor 4, gives the exact separate A and B counts. This example uses SQLite's product-specific format.",
    "Query the actual A and B counts after the insert. Explain the difference between these counts and the second number in 8 4.",
    "Record statistics state with the plan. Do not assume a data modification automatically refreshed planner statistics.",
    panels=[result("After first ANALYZE",["actual rows","stat"],[[6,"6 3"]]),result("After two inserts",["actual rows","stat"],[[8,"6 3"]]),result("After refresh",["actual rows","stat"],[[8,"8 4"]])])

add("ch17", "logic", "## 1. Transaction and ACID", "Committing the wrong calculation does not fix it",
    "17.1 Transaction Concept; 17.2 A Simple Transaction Model", "Atomicity groups changes, but consistency still depends on correct rules and application logic. A transaction can commit successfully while a missing business check allows a wrong total.",
    [table("account","id TEXT NOT NULL PRIMARY KEY, balance INTEGER CHECK(balance>=0)",["id","balance"],[["A",100],["B",50]])],
    "If 10 is deducted from A but only 5 is added to B, does the nonnegative-balance CHECK detect the missing money?",
    [("Start", "BEGIN"),("Debit", "UPDATE account SET balance=balance-10 WHERE id='A'"),("Incorrect credit", "UPDATE account SET balance=balance+5 WHERE id='B'"),("Commit", "COMMIT"),("Balances", "SELECT * FROM account ORDER BY id"),("Total", "SELECT SUM(balance) AS total FROM account")],
    [result("Start",[],[["Statement completed."]]),result("Debit",[],[["Statement completed."]]),result("Incorrect credit",[],[["Statement completed."]]),result("Commit",[],[["Statement completed."]]),result("Balances",["id","balance"],[["A",90],["B",55]]),result("Total",["total"],[[145]])],
    "The statements commit because both balances remain nonnegative. The total falls from 150 to 145, violating the stated transfer rule. A successful commit is not proof that the business calculation is correct.",
    "Correct the credit amount and check both individual balances and the unchanged total.",
    "A total check and a row-level range constraint test different properties.",
    panels=[result("Before",["A","B","total"],[[100,50,150]]),result("Wrong changes",["A change","B change"],[[-10,5]]),result("Committed",["A","B","total"],[[90,55,145]])])

add("ch17", "states", "## 2. Transaction States", "The last statement is not yet a durable commit",
    "17.4 Transaction Atomicity and Durability, pp.805-806", "A transaction may finish its last statement before its commit is durably established. That partially committed point still has a failure path. An aborted transaction has had its effects removed.",
    [table("events","",["step","event"],[[1,"last UPDATE finishes"],[2,"commit not yet durable"],[3,"system fails"]])],
    "Does finishing the last UPDATE justify calling this transaction committed? Which state follows failure and removal of its effects?",
    [],[],
    "The transaction is partially committed after its last statement, not yet committed. In the stated failure path it becomes failed, then aborted after its effects are removed. Safe retry requires a separate decision.",
    "Draw the successful alternative through durable commit, then the failed alternative without assuming that identical retry is always appropriate.",
    "Place the durable-commit event explicitly. Do not merge failed, aborted, and committed into one state.",
    panels=[result("Still executing",["state"],[["active"]]),result("Last statement done",["state"],[["partially committed"]]),result("Failure path",["state sequence"],[["failed"],["effects removed"],["aborted"]])])

add("ch17", "conflicts", "## 3. Schedules and Conflicts", "Check all three conflict conditions",
    "17.6 Serializability, pp.812-818", "Two operations conflict only when different transactions access the same item and at least one writes. Operation order then determines the precedence edge. Similar-looking letters on different items do not conflict.",
    [table("pairs","",["first","second"],[["r1(A)","r2(A)"],["r1(A)","w2(A)"],["w1(A)","w2(B)"],["w1(A)","w2(A)"]])],
    "Which pairs create T1 -> T2 when the first operation precedes the second?",
    [],[],
    "The read-write and write-write pairs on A create T1 -> T2. The read-read pair has no write, and the A/B pair uses different items. Neither of those two pairs creates a conflict edge.",
    "Reverse the operation order of the read-write pair, then place both directions in one schedule and check for a cycle.",
    "For every edge cite the two operations, shared item, and earlier-to-later direction.",
    panels=[result("Operation pair",["first","second"],[["r1(A)","r2(A)"],["r1(A)","w2(A)"],["w1(A)","w2(B)"],["w1(A)","w2(A)"]]),result("Decision",["reason","edge"],[["reads only","none"],["same A; write","T1 to T2"],["different items","none"],["same A; writes","T1 to T2"]])])

add("ch17", "commit_order", "## 4. Recoverability and Cascadelessness", "Move the writer's commit before the dependent read",
    "17.7 Transaction Isolation and Atomicity, pp.819-820", "When T2 reads a value written by T1, recoverability constrains their commits. Cascadelessness adds a stronger requirement: T1 must commit before T2 reads that value.",
    [table("events","",["position","event"],[[1,"w1(A)"],[2,"r2(A)"],[3,"c1"],[4,"c2"]])],
    "Is the shown schedule recoverable? Is its dependent read already protected from a rollback of T1?",
    [],[],
    "T1 commits before T2, so the displayed completed schedule is recoverable. However, T2 read before T1 committed, so it is not cascadeless. Moving c1 before r2(A) gives the stronger order.",
    "Place c2 before c1 and explain why T2 could commit a result based on work that later aborts.",
    "Identify the write-read dependency first, then compare the relevant event positions. Do not use the precedence graph as a substitute for commit-order analysis.",
    panels=[result("Recoverable only",["order"],[["w1(A)"],["r2(A)"],["c1"],["c2"]]),result("Cascadeless",["order"],[["w1(A)"],["c1"],["r2(A)"],["c2"]])])

add("ch17", "reads", "## 5. Isolation Phenomena", "An existing value changes versus a new matching row appears",
    "17.8 Transaction Isolation Levels, pp.821-822", "A nonrepeatable read changes a previously read row value. A phantom changes the set selected by a predicate. The following event trace is a conceptual concurrency scenario, not a live SQLite isolation test.",
    [table("initial","",["row","salary"],[["I1",100],["I2",80]])],
    "T1 counts salaries above 90 and gets 1. If T2 inserts I3 with 110 and commits, how does a later visible repeat differ from rereading I1 after its salary is updated?",
    [],[],
    "The insert changes the predicate count from 1 to 2 by adding I3, a phantom scenario. Updating I1 from 100 to 120 changes an existing row value, a nonrepeatable-read scenario. Whether either becomes visible depends on the actual isolation behavior.",
    "Describe a dirty-read variant in which T2 has not committed and later rolls back. State exactly which value T1 used.",
    "Separate uncommitted values, changes to existing rows, and changes to predicate membership. Do not claim a specific product permits them without a concurrent test.",
    panels=[result("First predicate read",["salary > 90"],[["I1: 100"]]),result("Other transaction",["event"],[["insert I3: 110"],["commit"]]),result("Later visible predicate read",["salary > 90"],[["I1: 100"],["I3: 110"]])])

add("ch18", "items", "## 1. Shared and Exclusive Locks", "Compatibility is checked for the requested item",
    "18.1 Lock-Based Protocols, pp.835-848", "Locks on different data items do not conflict in this simple item-lock model. On the same item, S is compatible with S; an X lock conflicts with a lock held by another transaction.",
    [table("held","",["holder","lock"],[["T1","S(A)"],["T2","X(B)"]])],
    "For independent requests by T3, which of S(A), X(A), S(B), and X(C) must wait?",
    [],[],
    "S(A) can coexist with T1's shared lock. X(A) waits for T1. S(B) waits for T2's exclusive lock. X(C) is free to proceed because nobody holds C in this model.",
    "Replace T1's S(A) with X(A) and repeat the S(A) request. Draw the resulting waiter-to-holder edge.",
    "Name the requested item and incompatible holder. These requests are independent, not a sequence that silently retains T3's earlier locks.",
    panels=[result("Held locks",["transaction","lock"],[["T1","S(A)"],["T2","X(B)"]]),result("Independent T3 requests",["request","decision"],[["S(A)","grant"],["X(A)","wait for T1"],["S(B)","wait for T2"],["X(C)","grant"]])])

add("ch18", "wait_chain", "## 2. Wait-For Graphs and Deadlock", "A waiting chain is not necessarily a deadlock",
    "18.2 Deadlock Handling, pp.849-852", "A wait-for edge points from the waiter to the incompatible holder. A chain with no cycle may resolve when the last holder finishes. Waiting alone is not evidence of deadlock.",
    [table("waits","",["waiter","holder"],[["T1","T2"],["T2","T3"]])],
    "Is there a cycle now? Which additional edge would close the three-transaction cycle?",
    [],[],
    "T1 waits for T2 and T2 waits for T3, but T3 does not wait in the displayed state. There is no cycle. Adding T3 -> T1 closes a cycle; only then do these three transactions wait on each other.",
    "Add a separate T4 -> T2 edge and explain why T4 is not part of the three-node cycle.",
    "Trace a directed path back to its starting node. Do not treat every vertex that reaches a cycle as a member of that cycle.",
    panels=[result("Current chain",["edge"],[["T1 -> T2"],["T2 -> T3"]]),result("No cycle yet",["reason"],[["T3 has no outgoing wait"]]),result("Add one edge",["edge","effect"],[["T3 -> T1","cycle closes"]])])

add("ch18", "victim", "## 3. Responding to Deadlock", "Remove a victim's effects before granting conflicting work",
    "18.2 Deadlock Handling: Deadlock Recovery", "Breaking a deadlock requires aborting or rolling back work and releasing the corresponding locks. Merely erasing an edge on paper does not change the protected data or lock state.",
    [table("state","",["transaction","holds","waits for"],[["T1","X(A)","X(B) from T2"],["T2","X(B)","X(A) from T1"]])],
    "If T2 is the victim, which work must be undone and which requested lock can become available to T1?",
    [],[],
    "T2's uncommitted work is rolled back and its locks are released as part of recovery. B can then become available to T1. A later T2 retry must start from an allowed state and must not duplicate an external action such as a payment.",
    "Explain why choosing an unrelated waiting T4 would not break this T1/T2 cycle. State one reason not to retry forever.",
    "Recompute waits from actual remaining holders and requests. Victim choice and safe retry are separate decisions.",
    panels=[result("Cycle",["waiter","holder"],[["T1","T2"],["T2","T1"]]),result("T2 recovery",["action"],[["undo uncommitted work"],["release locks"]]),result("Then",["possible progress"],[["T1 may obtain X(B)"],["T2 retry requires checks"]])])

add("ch19", "storage", "## 1. Failure and Storage Assumptions", "Separate lost memory from lost persistent data",
    "19.1 Failure Classification; 19.2 Storage, pp.907-911", "A restart-recovery example needs an explicit failure assumption. If volatile buffers are lost but the database and log remain readable, the stable log can support recovery. Loss of the persistent database needs additional retained evidence.",
    [table("places","",["location","example content"],[["memory buffer","recent unflushed changes"],["database storage","written data pages"],["stable log","forced log records"]])],
    "In a fail-stop system crash with readable storage, which of these three sources is lost? What changes when database storage is unreadable?",
    [],[],
    "The stated system crash loses memory buffers but leaves written database pages and stable log records readable. Storage loss removes that assumption; a usable base copy and retained logs may be needed. A readable log is not automatically a complete copy of the database.",
    "Classify a failed constraint and a deadlock victim separately from storage loss. State which transaction effects need removal.",
    "Name what survives before choosing a recovery explanation. Do not treat all failures as the same restart case.",
    panels=[result("System crash assumption",["source","after crash"],[["memory","lost"],["database pages","readable"],["stable log","readable"]]),result("Storage loss",["source","concern"],[["database pages","may be unreadable"],["base copy and logs","must be available"]])])

add("ch19", "status", "## 2. Log Records", "Determine commit status from the stable log",
    "19.3 Recovery and Atomicity, pp.912-921", "A data value already on disk does not prove its transaction committed. Inspect start, update, and commit records in the stable log before choosing what must survive recovery.",
    [table("log","",["position","record"],[[1,"T1 start"],[2,"T1: A, old 10, new 8"],[3,"T1 commit"],[4,"T2 start"],[5,"T2: B, old 7, new 4"]])],
    "If disk already contains A=8 and B=4, which transaction is still incomplete at the crash?",
    [],[],
    "T1 has a stable commit record. T2 has only start and update records, so it remains incomplete in this case. The final state must retain T1's A=8 and remove T2's B=4 effect, restoring B=7 under the simple old/new-value model.",
    "Add a stable T2 commit record before the crash. Explain how the required final value of B changes.",
    "Use log status and old/new fields together. Do not use the current disk value as a substitute for commit evidence.",
    panels=[result("Disk at crash",["A","B"],[[8,4]]),result("Stable log status",["transaction","status"],[["T1","committed"],["T2","incomplete"]]),result("Required final values",["A","B"],[[8,7]])])


# Coordinates describe original diagrams, not a DBMS's physical representation.
EXAMPLES["ch06_small_roles"]["graph"] = dict(
    height=220,
    nodes=[(70, 70, 220, 85, "Course A"), (490, 70, 220, 85, "Course B"),
           (910, 70, 220, 85, "Course C")],
    edges=[(490, 112, 290, 112, "requires", 340, 88),
           (910, 112, 710, 112, "requires", 760, 88)],
)
EXAMPLES["ch06_small_weak"]["graph"] = dict(
    height=400,
    nodes=[(205, 20, 230, 85, "Owner: Course DB"),
           (870, 20, 260, 85, "Owner: Course WEB"),
           (50, 230, 300, 110, "DB / T1 / section 1"),
           (440, 230, 300, 110, "DB / T2 / section 1"),
           (830, 230, 300, 110, "WEB / T1 / section 1")],
    edges=[(260, 105, 200, 230, "owns", 70, 175),
           (390, 105, 590, 230, "owns", 500, 150),
           (1000, 105, 980, 230, "owns", 1020, 175)],
)
EXAMPLES["ch06_small_many"]["graph"] = dict(
    height=400, directed=False,
    nodes=[(70, 30, 240, 85, "Student S2"), (70, 280, 240, 85, "Student S1"),
           (850, 30, 280, 85, "Section DB-T1-1"),
           (850, 280, 280, 85, "Section WEB-T1-1")],
    edges=[(310, 72, 850, 72, "grade B+", 510, 55),
           (310, 322, 850, 72, "grade A", 540, 145),
           (310, 322, 850, 322, "grade B", 520, 305)],
)
EXAMPLES["ch15_small_workflow"]["graph"] = dict(
    height=240,
    nodes=[(50, 40, 290, 140, "Parse and translate: check the request"),
           (455, 40, 290, 140, "Optimize: choose operations"),
           (860, 40, 290, 140, "Evaluate: produce rows")],
    edges=[(340, 110, 455, 110, "", 0, 0), (745, 110, 860, 110, "", 0, 0)],
)
EXAMPLES["ch17_small_states"]["graph"] = dict(
    height=415,
    nodes=[(50, 40, 230, 100, "Active"), (455, 40, 270, 100, "Partially committed"),
           (900, 40, 250, 100, "Committed"), (455, 275, 270, 85, "Failed"),
           (900, 275, 250, 85, "Aborted")],
    edges=[(280, 90, 455, 90, "last statement", 290, 12),
           (725, 90, 900, 90, "durable commit", 733, 12),
           (590, 140, 590, 275, "failure", 615, 215),
           (165, 140, 455, 310, "failure", 165, 240),
           (725, 317, 900, 317, "effects removed", 725, 260)],
)
EXAMPLES["ch18_small_wait_chain"]["graph"] = dict(
    height=250,
    nodes=[(70, 70, 220, 85, "T1"), (490, 70, 220, 85, "T2"),
           (910, 70, 220, 85, "T3")],
    edges=[(290, 112, 490, 112, "waits for", 335, 88),
           (710, 112, 910, 112, "waits for", 755, 88)],
)
