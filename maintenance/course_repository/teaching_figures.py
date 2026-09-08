"""Original table transformations and diagrams for the maintained chapter examples."""

from html import escape
from functools import lru_cache

from PIL import ImageFont


COLORS = ("#17665d", "#245e9c", "#a13251")
FIGURES = {}


def panel(title, headers, rows, note="", marks=()):
    return dict(title=title, headers=headers, rows=rows, note=note, marks=marks)


def figure(name, heading, title, panels, conclusion, *, arrows=False, kind="tables"):
    FIGURES[name] = dict(heading=heading, title=title, panels=panels,
                         conclusion=conclusion, arrows=arrows, kind=kind)


figure("ch02_files", "### Worked Example: Two Copies Disagree", "Two files disagree about one student", [
    panel("Registration file", ["student_id", "email"], [["S101", "an.chen@example.edu"]]),
    panel("Contact file", ["student_id", "email"], [["S101", "an.old@example.edu"]], marks=(0,)),
], "Same student, different email values. Verify which address is current before choosing a value.")

figure("ch02_dbms", "### Why Keep a Database?", "The database is not the DBMS", [
    panel("1. A request", ["Question"], [["Find S101's email"]], "A person or program asks for data."),
    panel("2. DBMS: SQLite", ["Software action"], [["Read stored student data"]], "The DBMS processes the request."),
    panel("3. Database", ["student_id", "email"], [["S101", "an.chen@example.edu"]], "Stored related data; not the software."),
], "Request direction is shown left to right. The result returns to the requester.", arrows=True)

figure("ch02_domains", "## 1.1 Domains and Atomic Values / ### Read the Output", "A domain is more than the values observed", [
    panel("Current course sample", ["Observed credits"], [["3"], ["3"], ["2"]], "Repeated values are allowed."),
    panel("Declared domain", ["Allowed whole numbers"], [["1, 2, 3, 4, 5, 6"]], "4 is allowed even when absent from this sample."),
    panel("Outside this domain", ["Proposed value", "Reason"], [["0", "Below 1"], ["7", "Above 6"], ["2.5", "Not a whole number"]]),
], "This is the chapter's illustrative whole-number rule, not a claim about SQLite type affinity.")

figure("ch02_phones", "### Worked Example: One Phone Number per Row", "Find one phone number without splitting a list", [
    panel("Two list-valued cells", ["student_id", "phone_numbers"], [["S101", "555-0101;555-0102"], ["S102", "555-0103"]], "The whole first cell is not equal to 555-0102."),
    panel("One phone number per row", ["student_id", "phone_number"], [["S101", "555-0101"], ["S101", "555-0102"], ["S102", "555-0103"]], "An exact match now identifies S101.", marks=(1,)),
], "Three phone numbers for two students are preserved. S101 repeating does not make the complete rows duplicates.", arrows=True)

figure("ch02_order", "## 1.2 Row Order and Repeated Values / ### Read the Output", "Changing display order does not change the facts", [
    panel("Ascending display", ["student_id", "student_name"], [["S101", "An Chen"], ["S102", "Bea Lin"], ["S103", "Kai Wu"], ["S104", "Mira Ho"]]),
    panel("Descending display", ["student_id", "student_name"], [["S104", "Mira Ho"], ["S103", "Kai Wu"], ["S102", "Bea Lin"], ["S101", "An Chen"]]),
], "The same four ID/name pairs occur in both displays. A formal relation has no tuple order.", arrows=True)

figure("ch02_duplicates", "### Worked Comparison: Repeated Value or Repeated Tuple?", "Repeated value or repeated complete tuple?", [
    panel("Repeated department", ["student_id", "dept_code"], [["S101", "IM"], ["S103", "IM"]], "These two ID/department tuples differ."),
    panel("Exact repeated tuple", ["student_id", "dept_code"], [["S101", "IM"], ["S101", "IM"]], "A formal set contains this complete tuple once.", marks=(1,)),
], "Compare every displayed attribute before calling two tuples duplicates. This illustration shows two-column relations.")

figure("ch02_changes", "### Comparing the Three Changes", "Three changes: count rows and columns separately", [
    panel("Insert S105", ["State", "Rows", "Columns"], [["Before", "4", "4"], ["After", "5", "4"]], "New tuple; same schema.", marks=(1,)),
    panel("Update S102", ["State", "Rows", "Columns"], [["Before", "5", "4"], ["After", "5", "4"]], "FIN becomes IM. The instance changes even though counts do not.", marks=(1,)),
    panel("Add status", ["State", "Rows", "Columns"], [["Before", "5", "4"], ["After", "5", "5"]], "A new attribute changes the schema.", marks=(1,)),
], "These are the consecutive notebook steps. Row counts alone cannot tell whether the instance changed.", arrows=True)

figure("ch02_identifiers", "## 2.1 Why Do Students Need Identifiers?", "One name can refer to two different students", [
    panel("Search by name: An Chen", ["student_id", "Name", "Department"], [["S101", "An Chen", "IM"], ["S105", "An Chen", "FIN"]], "Two students match the name."),
    panel("Search by ID: S105", ["student_id", "Name", "Department"], [["S105", "An Chen", "FIN"]], "The identifier selects the intended student."),
], "These are the introductory example's two students. A name is not guaranteed to identify one student.", arrows=True)

figure("ch02_keys", "### Worked Example: `student`", "A candidate key has no unnecessary attribute", [
    panel("Minimal identifiers", ["Attribute set", "Under the stated rules"], [["{student_id}", "Unique and required"], ["{email}", "Unique and required"]], "Both are candidate keys."),
    panel("Unnecessary addition", ["Proposed set"], [["{student_id, student_name}"]], "Remove student_name: student_id still identifies the tuple."),
    panel("Chosen primary key", ["Chosen set"], [["{student_id}"]], "The designer chooses one candidate key as the primary key."),
], "A superkey may contain extra attributes. Observed uniqueness in four sample rows is not a lasting business rule.")

figure("ch02_composite", "### Worked Example: `enrollment`", "Why the enrollment key includes the term", [
    panel("The pair repeats", ["student_id", "course_id", "term"], [["S101", "DB201", "115-1"], ["S101", "DB201", "115-2"]], "The student/course pair cannot distinguish these enrollments.", marks=(1,)),
    panel("Remove one attribute", ["Removed", "Remaining pair can repeat"], [["term", "Same student and course in two terms"], ["course_id", "Two courses for S101 in 115-1"], ["student_id", "Two students in DB201 in 115-1"]]),
], "Under the declared rules, the complete student/course/term triple is unique and each attribute is needed.")

figure("ch02_references", "## 4. Foreign Keys and Schema Diagrams", "A foreign key points to an existing referenced row", [
    panel("Referencing student rows", ["student_id", "dept_code"], [["S101", "IM"], ["S103", "IM"]], "Repeated IM values are allowed."),
    panel("Referenced department", ["dept_code", "dept_name"], [["IM", "Information Management"]], "Both student values match this key."),
    panel("Rejected proposal", ["student_id", "dept_code"], [["S106", "LAW"]], "No LAW row exists in department.", marks=(0,)),
], "The arrow runs from the referencing value toward the referenced key. A foreign key need not be unique.", arrows=(0,))

figure("ch02_selection", "### Selection", "Selection keeps rows that satisfy the condition", [
    panel("Before: student", ["student_id", "student_name", "dept_code"], [["S101", "An Chen", "IM"], ["S102", "Bea Lin", "FIN"], ["S103", "Kai Wu", "IM"], ["S104", "Mira Ho", "DES"]], marks=(0, 2)),
    panel("After: dept_code = IM", ["student_id", "student_name", "dept_code"], [["S101", "An Chen", "IM"], ["S103", "Kai Wu", "IM"]], "2 rows remain; selection does not remove attributes."),
], "Only three attributes are displayed here. Each retained tuple also keeps its email value from student.", arrows=True)

figure("ch02_projection", "### Projection", "Projection keeps attributes and removes duplicates", [
    panel("Input department values", ["dept_code"], [["IM"], ["FIN"], ["IM"], ["DES"]], "Four input rows; IM repeats.", marks=(0, 2)),
    panel("Formal projection result", ["dept_code"], [["DES"], ["FIN"], ["IM"]], "Three distinct one-attribute tuples."),
], "SELECT DISTINCT dept_code matches this formal projection. The four stored student rows are not deleted.", arrows=True)

figure("ch02_composition", "### Composition", "Compose operations from the inside out", [
    panel("Input: student", ["student_id", "student_name", "dept_code"], [["S101", "An Chen", "IM"], ["S102", "Bea Lin", "FIN"], ["S103", "Kai Wu", "IM"], ["S104", "Mira Ho", "DES"]]),
    panel("Select IM rows", ["student_id", "student_name", "dept_code"], [["S101", "An Chen", "IM"], ["S103", "Kai Wu", "IM"]]),
    panel("Project student_name", ["student_name"], [["An Chen"], ["Kai Wu"]]),
], "Email is omitted only from the first two displays; selection retains it. Projection neither expands nor changes a name.", arrows=True)

figure("ch02_product", "### Cartesian Product", "A product forms every possible pair", [
    panel("First input", ["student_id"], [["S101"], ["S102"]]),
    panel("Second input", ["course_id"], [["DB201"], ["FT210"]]),
    panel("2 x 2 = 4 pairs", ["student_id", "course_id"], [["S101", "DB201"], ["S101", "FT210"], ["S102", "DB201"], ["S102", "FT210"]], "S102/DB201 is a combination, not an enrollment fact.", marks=(2,)),
], "The product does not test enrollment. Every row from one input is paired with every row from the other.")

figure("ch02_join", "### Theta Join", "The join condition separates matches from nonmatches", [
    panel("Candidate row pairs", ["student.student_id", "enrollment.student_id", "Decision"], [["S101", "S101", "Keep"], ["S101", "S102", "Remove"], ["S102", "S101", "Remove"], ["S102", "S102", "Keep"]], "Illustrative subset of the 24 combinations."),
    panel("Full example counts", ["Operation", "Rows"], [["4 students x 6 enrollments", "24"], ["Keep equal student IDs", "6"]], "Each enrollment references exactly one student."),
], "The ID equality is the join condition. Student and course department equality is not an enrollment rule.", arrows=True)

figure("ch02_sets", "## 6. Set Operations", "One overlap, four set-operation results", [
    panel("A: DB201", ["A only", "In both"], [["S103", "S101"]]),
    panel("B: FT210", ["In both", "B only"], [["S101", "S102"]]),
    panel("Compare the results", ["Operation", "student_id values"], [["A union B", "S101, S102, S103"], ["A intersect B", "S101"], ["A minus B", "S103"], ["B minus A", "S102"]]),
], "S101 appears once in the union. Difference has direction: exchanging the inputs changes the answer.")

figure("ch03_null", "## 5. `NULL` and Three-Valued Logic", "WHERE keeps TRUE, not UNKNOWN", [
    panel("Illustrative grades", ["grade", "grade <> 'F'", "Pass WHERE?"], [["B", "TRUE", "Yes"], ["F", "FALSE", "No"], ["NULL", "UNKNOWN", "No"]], marks=(2,)),
    panel("Count the same rows", ["Expression", "Result"], [["COUNT(*)", "3"], ["COUNT(grade)", "2"], ["grade IS NULL", "Finds the NULL row"]]),
], "NULL is neither F nor a guaranteed passing grade. The illustration applies the chapter's comparison rules.")

figure("ch03_groups", "## 6. Aggregation and Grouping", "Filter rows, form groups, then filter groups", [
    panel("WHERE credits >= 3", ["course_id", "dept_code"], [["DB201", "IM"], ["FT210", "FIN"], ["ML230", "IM"]], "WD120 has 2 credits and is removed."),
    panel("GROUP BY dept_code", ["Department", "COUNT(*)"], [["FIN", "1"], ["IM", "2"]]),
    panel("HAVING COUNT(*) >= 2", ["Department", "COUNT(*)"], [["IM", "2"]]),
], "This sequence explains query meaning, not a required physical execution order.", arrows=True)

figure("ch04_outer", "## 3. Inner and Outer Joins", "Keep a course even when nobody enrolled", [
    panel("INNER JOIN", ["course_id", "Enrollment count"], [["DB201", "2"], ["FT210", "2"], ["ML230", "1"], ["WD120", "1"]], "Temporary course IS250 has no match."),
    panel("LEFT JOIN from course", ["course_id", "COUNT(e.student_id)"], [["DB201", "2"], ["FT210", "2"], ["IS250", "0"], ["ML230", "1"], ["WD120", "1"]], "The null-padded IS250 row is preserved.", marks=(2,)),
], "COUNT(*) would count the padded IS250 row as 1. Count the non-NULL enrollment identifier instead.")

figure("ch04_filters", "## 4. Conditions in `ON` and `WHERE`", "A left-join filter can change which courses survive", [
    panel("Grade filter in ON", ["Course with no qualifying match", "Result"], [["IS250 (no enrollment)", "Retained with NULL"]], "Keep all courses; attach only A or A- enrollments."),
    panel("Grade filter in WHERE", ["Test after padding", "Result"], [["NULL IN ('A', 'A-')", "UNKNOWN: removed"]], "Retain only rows whose post-join predicate is TRUE."),
], "This uses the lab's temporary IS250 course. Moving the condition changes meaning, not just performance.")

figure("ch05_ranks", "## 4. Ranking Functions", "Ties distinguish the three ranking functions", [
    panel("Same scores, different numbering", ["Student", "Score", "RANK", "DENSE_RANK", "ROW_NUMBER"], [["S101", "92", "1", "1", "1"], ["S102", "92", "1", "1", "2"], ["S103", "84", "3", "2", "3"], ["S104", "84", "3", "2", "4"]], "ROW_NUMBER uses student_id to order tied scores."),
], "RANK leaves a gap after a tie; DENSE_RANK does not. ROW_NUMBER gives each detail row a different number.")

figure("ch05_recursive", "## 3. Recursive CTEs", "Follow prerequisite edges until no new pair appears", [
    panel("Base: direct prerequisites", ["Course", "Prerequisite"], [["DB201", "WD120"], ["FT210", "DB201"], ["ML230", "DB201"]]),
    panel("Next round: added pairs", ["Course", "Prerequisite"], [["FT210", "WD120"], ["ML230", "WD120"]]),
    panel("Following round", ["New pairs", "Total distinct pairs"], [["0", "5"]], "Stop for this graph and complete-row UNION."),
], "A changing depth column can make rows distinct on a cycle. UNION alone is not a termination proof for every recursive query.", arrows=True)

figure("ch05_trigger", "## 2. Row-Level Audit Trigger", "One grade change and its audit row", [
    panel("Before update", ["Enrollment", "Grade"], [["S103 / DB201 / 115-1", "B"]]),
    panel("After update", ["Enrollment", "Grade"], [["S103 / DB201 / 115-1", "B+"]]),
    panel("Audit insert", ["old_grade", "new_grade"], [["B", "B+"]], "The trigger uses OLD and NEW from this row change."),
], "The grade update and audit insert belong to the same transaction. Rolling it back removes both changes.", arrows=True)

figure("ch06_cardinality", "## 5. Cardinality and Participation", "Read a relationship in both directions", [
    panel("For one Department", ["Related Students"], [["0, 1, 2, ..."]], "A department may have no students."),
    panel("For one Student", ["Major Department"], [["Exactly 1"]], "Every student must have one major under this rule."),
], "One-to-many does not state the minimum by itself. The minimum distinguishes optional from required participation.")

figure("ch06_mapping", "## 8. Mapping to Relations", "Carry the section's complete identity into enrollment", [
    panel("Course", ["Primary key"], [["course_id"]]),
    panel("Section", ["Primary key components"], [["course_id (also FK to Course)"], ["term"], ["section_no"]]),
    panel("Enrollment", ["Key components and references"], [["student_id: FK to Student"], ["course_id + term + section_no: FK to Section"]], "The complete four-column key identifies enrollment; grade is descriptive."),
], "Unlike the simplified Ch2 case, the Ch6 design distinguishes separate sections of the same course and term.", arrows=True)

figure("ch07_closure", "## 3. Attribute Closure and Candidate Keys", "Grow the closure from the two identifiers", [
    panel("Start", ["Known attributes"], [["student_id"], ["course_id"]]),
    panel("Apply stated dependencies", ["Determinant", "Add"], [["student_id", "student_name, dept_code"], ["dept_code", "dept_name"], ["course_id", "course_title, credits"], ["Both IDs", "grade"]]),
    panel("Closure", ["Outcome"], [["All 8 attributes"]], "Removing either identifier loses required facts."),
], "The pair is a candidate key under these dependencies. Closure follows rules, not accidental sample uniqueness.", arrows=True)

figure("ch07_lossy", "## 4. Lossless Decomposition", "Joining on a non-key name invents false combinations", [
    panel("Original rows", ["Employee", "Name", "City"], [["E1", "Kim", "Taipei"], ["E2", "Kim", "Tainan"]], "Salary is omitted from this display only."),
    panel("Join the name-based projections", ["Employee", "City", "In original?"], [["E1", "Taipei", "Yes"], ["E1", "Tainan", "No"], ["E2", "Taipei", "No"], ["E2", "Tainan", "Yes"]], "Name matches both detail rows.", marks=(1, 2)),
], "Two original rows become four reconstructed rows. A shared column is not enough to make a decomposition lossless.", arrows=True)

figure("ch14_composite", "## 4. Composite Indexes", "Column order determines how entries are grouped", [
    panel("(customer_id, ordered_at)", ["Customer", "Date"], [["C0042", "2026-01-01"], ["C0042", "2026-06-01"], ["C0043", "2026-01-01"]], "One customer's dates are adjacent.", marks=(0, 1)),
    panel("(ordered_at, customer_id)", ["Date", "Customer"], [["2026-01-01", "C0042"], ["2026-01-01", "C0043"], ["2026-06-01", "C0042"]], "One date's customers are adjacent.", marks=(0, 2)),
], "Illustrative entries, not an extract of the 20,000-row lab. Inspect the actual plan before claiming a faster query.")

figure("ch14_covering", "## 5. Covering Index", "Can the index supply every required column?", [
    panel("Query needs", ["Filter and order", "Output"], [["customer_id, ordered_at", "ordered_at, amount"]]),
    panel("Two-column index", ["Available", "Missing"], [["customer_id, ordered_at", "amount"]], "A table lookup may still be needed."),
    panel("Three-column index", ["Available"], [["customer_id, ordered_at, amount"]], "Covers this query. Adding status to the output changes that conclusion."),
], "Covering depends on the specific query. Extra index columns also cost storage and write work.")

figure("ch15_plans", "## 2. Logical Operation, Physical Operator, and Plan", "Two access paths, the same requested row", [
    panel("Plan A: scan", ["Work"], [["Read course rows"], ["Test title"], ["Return matching columns"]]),
    panel("Plan B: index search", ["Work"], [["Search title index"], ["Fetch matching row"], ["Return matching columns"]]),
    panel("Same result", ["course_id", "title"], [["C04999", "Course 04999"]]),
], "These are schematic access paths for the lab. Plan evidence is not a measurement of elapsed time.")

figure("ch15_join_order", "## 4. Reading a Join Plan", "A selective outer lookup drives the inner lookup", [
    panel("1. Find Department 042", ["Index predicate"], [["dept_name = 'Department 042'"]], "Search by department name."),
    panel("2. Use its department ID", ["Join condition"], [["course.dept_id = department.dept_id"]], "Search the course department index."),
    panel("3. Return course rows", ["Output"], [["course_id, title"]], "Keep the same matching rule."),
], "This is the indexed plan described by the lab. Removing the department-name filter requires a new plan check.", arrows=True)

figure("ch16_selectivity", "## 3. Statistics and Selectivity", "An estimate is not the observed distribution", [
    panel("Uniform estimate", ["Event type", "Rows"], [["COMMON", "5000"], ["RARE", "5000"]], "10,000 rows divided by 2 distinct values."),
    panel("Actual teaching data", ["Event type", "Rows", "Share"], [["COMMON", "9900", "99%"], ["RARE", "100", "1%"]], "The two frequencies are very different."),
], "The same uniform estimate overestimates RARE and underestimates COMMON. A small match count alone does not guarantee index use.")

figure("ch16_equivalence", "## 2. Result Equivalence as a Guardrail", "Equal sets and total counts can hide different duplicates", [
    panel("Illustrative SQL result A", ["Value"], [["x"], ["x"], ["y"]]),
    panel("Illustrative SQL result B", ["Value"], [["x"], ["y"], ["y"]]),
    panel("Count each value", ["Value", "A count", "B count"], [["x", "2", "1"], ["y", "1", "2"]], "The SQL results are not equal as multisets."),
], "Both EXCEPT differences are empty and both totals are 3. Compare grouped counts when duplicates are possible.")

figure("ch17_transfer", "## 1. Transaction and ACID", "Keep both account changes or neither", [
    panel("Before transfer", ["Account", "Balance"], [["A", "1000"], ["B", "2000"]], "Total = 3000"),
    panel("After both updates", ["Account", "Balance"], [["A", "950"], ["B", "2050"]], "Transfer 50; total = 3000"),
    panel("If rolled back", ["Account", "Balance"], [["A", "1000"], ["B", "2000"]], "Neither uncommitted change remains."),
], "Commit keeps the completed transfer; rollback restores the prior state. Correctness still depends on the business rules.")

figure("ch17_conflicts", "## 3. Schedules and Conflicts", "A precedence graph records conflicting operation order", [],
       "r1(A) before w2(A) gives T1 to T2; r2(B) before w1(B) gives T2 to T1. This schedule is not conflict serializable.", kind="precedence")

figure("ch18_locks", "## 1. Shared and Exclusive Locks", "Another reader can proceed; a writer must wait", [
    panel("Compatibility", ["Held by another", "Request S", "Request X"], [["S", "Grant", "Wait"], ["X", "Wait", "Wait"]]),
    panel("Two readers hold S(A)", ["Holder", "Lock"], [["T1", "S(A)"], ["T2", "S(A)"]], "T3 requests X(A)."),
    panel("Who still blocks T3?", ["Event", "Result"], [["T1 releases", "Still waits for T2"], ["T2 releases", "May receive X(A)"]]),
], "The example assumes different transactions and the same protected item. An X lock conflicts with both S and X.")

figure("ch18_deadlock", "## 2. Wait-For Graphs and Deadlock", "A wait-for graph points from waiter to holder", [],
       "T1 holds X(A), T2 holds X(B), and each requests the other's item. The two waiting edges form a deadlock cycle.", kind="wait_for")

figure("ch19_log", "## 2. Log Records", "Read the old and new values from an update record", [
    panel("Stable update record", ["Transaction", "Item", "Old", "New"], [["T1", "C", "700", "600"]]),
    panel("Choose using transaction status", ["Status and need", "Value to apply"], [["Incomplete; undo its change", "Old: 700"], ["Committed; update missing on disk", "New: 600"]]),
], "This is the chapter's simplified value-based example. A value already on disk does not prove the transaction committed.")

figure("ch19_wal", "## 3. Write-Ahead Logging", "Persist the log before the protected action", [
    panel("Before a data-page write", ["First", "Then"], [["Make update log stable", "Flush changed data page"]]),
    panel("Before reporting commit", ["First", "Then"], [["Make prior log and commit record stable", "Acknowledge commit"]]),
], "These are two ordering requirements, not a requirement to flush every data page before commit acknowledgement.")

figure("ch19_recovery", "## 4. Simplified Redo and Undo", "Restore logged history, then undo incomplete work", [
    panel("Disk at crash", ["A", "B", "C"], [["950", "2000", "600"]], "Stable log: T0 committed; T1 incomplete."),
    panel("After redo", ["A", "B", "C"], [["950", "2050", "600"]], "Apply logged new values in order."),
    panel("After undo T1", ["A", "B", "C"], [["950", "2050", "700"]], "Restore T1's old C value."),
], "This follows the supplied recovery simulator, not a complete production recovery algorithm.", arrows=True)


def _text(x, y, value, size=24, color="#18252b", weight=400):
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(str(value))}</text>'


@lru_cache(maxsize=32)
def _font(size, weight=400):
    return ImageFont.truetype("arialbd.ttf" if weight >= 600 else "arial.ttf", size)


def _lines(value, width, size, weight=400):
    font = _font(size, weight)
    lines = []
    line = ""
    for word in str(value).split():
        candidate = (line + " " + word).strip()
        if font.getlength(candidate) <= width:
            line = candidate
            continue
        if line:
            lines.append(line)
            line = ""
        while font.getlength(word) > width:
            end = max(i for i in range(1, len(word) + 1) if font.getlength(word[:i]) <= width)
            boundaries = [i + 1 for i, char in enumerate(word[:end]) if char in "_@./,"]
            if boundaries:
                end = boundaries[-1]
            lines.append(word[:end])
            word = word[end:]
        line = word
    if line:
        lines.append(line)
    return lines or [""]


def _paragraph(x, y, value, width, size=24, color="#18252b", weight=400):
    lines = _lines(value, width, size, weight)
    return "\n".join(_text(x, y + size * 1.35 * i, line, size, color, weight) for i, line in enumerate(lines)), len(lines) * size * 1.35


def _panel(x, y, width, data, color, title_height):
    parts = []
    title, used = _paragraph(x, y + 26, data["title"], width, 25, color, 700)
    parts.append(title)
    top = y + title_height + 24
    columns = len(data["headers"])
    column_width = width / columns
    for row_index, row in enumerate([data["headers"], *data["rows"]]):
        font = 22 if columns <= 3 else 21
        weight = 700 if row_index == 0 else 400
        while font > 18 and any(_font(font, weight).getlength(word) > column_width - 24
                               for value in row for word in str(value).replace("_", " ").split()):
            font -= 1
        wrapped = [_lines(value, column_width - 24, font, weight) for value in row]
        height = max(len(lines) for lines in wrapped) * font * 1.35 + 24
        background = "#e9eff2" if row_index == 0 else "#ffffff"
        marked = row_index - 1 in data["marks"]
        if marked:
            background = "#e3f2ee"
        parts.append(f'<rect x="{x}" y="{top}" width="{width}" height="{height}" fill="{background}" stroke="#9eafb8"/>')
        if marked:
            parts.append(f'<rect x="{x + 2}" y="{top + 2}" width="{width - 4}" height="{height - 4}" fill="none" stroke="{color}" stroke-width="3"/>')
        for col, lines in enumerate(wrapped):
            if col:
                parts.append(f'<line x1="{x + col * column_width}" y1="{top}" x2="{x + col * column_width}" y2="{top + height}" stroke="#9eafb8"/>')
            for line_index, line in enumerate(lines):
                parts.append(_text(x + col * column_width + 12, top + font + 10 + line_index * font * 1.35,
                                   line, font, weight=700 if row_index == 0 else 400))
        top += height
    if data["note"]:
        note, used = _paragraph(x, top + 34, data["note"], width, 23)
        parts.append(note)
        top += used + 24
    return "\n".join(parts), top


def render(name):
    data = FIGURES[name]
    title, height = _paragraph(45, 48, data["title"], 1110, 32, weight=700)
    parts = [title, _text(45, height + 80, "Original teaching illustration | Read with the worked example", 20, "#48616c")]
    y = height + 115
    if data["kind"] == "network":
        graph = data["graph"]
        for edge in graph["edges"]:
            x1, y1, x2, y2, label, lx, ly = edge
            marker = ' marker-end="url(#tip)"' if graph.get("directed", True) else ""
            parts.append(f'<path d="M {x1} {y+y1} L {x2} {y+y2}" fill="none" stroke="#48616c" stroke-width="3"{marker}/>')
            if label:
                label_text, _ = _paragraph(lx, y + ly, label, 420, 23, "#245e9c", 600)
                parts.append(label_text)
        for x, top, width, height, label in graph["nodes"]:
            parts.append(f'<rect class="network-node" x="{x}" y="{y+top}" width="{width}" height="{height}" fill="#e3f2ee" stroke="#17665d" stroke-width="3"/>')
            content, _ = _paragraph(x+18, y+top+35, label, width-36, 25, weight=600)
            parts.append(content)
        bottom = y + graph["height"]
    elif data["kind"] in {"precedence", "wait_for"}:
        is_wait = data["kind"] == "wait_for"
        parts.append(_text(55, y + 15, "Wait-for graph" if is_wait else "Precedence graph", 26, weight=700))
        for x, label in [(260, "T1"), (940, "T2")]:
            parts.append(f'<circle cx="{x}" cy="{y + 175}" r="76" fill="#e3f2ee" stroke="#17665d" stroke-width="3"/>')
            parts.append(_text(x - 25, y + 185, label, 34, weight=700))
        parts.append(f'<path d="M 320 {y+130} Q 600 {y-10} 880 {y+130}" fill="none" stroke="#245e9c" stroke-width="4" marker-end="url(#tip)"/>')
        parts.append(f'<path d="M 880 {y+225} Q 600 {y+365} 320 {y+225}" fill="none" stroke="#a13251" stroke-width="4" marker-end="url(#tip)"/>')
        parts.append(_text(395, y + 40, "T1 waits for T2's X(B)" if is_wait else "r1(A) precedes w2(A)", 25, "#245e9c", 700))
        parts.append(_text(395, y + 330, "T2 waits for T1's X(A)" if is_wait else "r2(B) precedes w1(B)", 25, "#a13251", 700))
        bottom = y + 365
    else:
        count = len(data["panels"])
        gap = 65 if data["arrows"] else 32
        width = (1110 - gap * (count - 1)) / count
        title_height = max(len(_lines(p["title"], width, 25, 700)) * 25 * 1.35 for p in data["panels"])
        bottom = y
        for index, p in enumerate(data["panels"]):
            x = 45 + index * (width + gap)
            content, end = _panel(x, y, width, p, COLORS[index % len(COLORS)], title_height)
            parts.append(content)
            bottom = max(bottom, end)
            if data["arrows"] and index < count - 1 and (data["arrows"] is True or index in data["arrows"]):
                parts.append(f'<path d="M {x+width+8} {y+125} L {x+width+gap-12} {y+125}" fill="none" stroke="#48616c" stroke-width="3" marker-end="url(#tip)"/>')
    conclusion, used = _paragraph(45, bottom + 65, data["conclusion"], 1110, 25, weight=600)
    parts.extend([f'<line x1="45" y1="{bottom+30}" x2="1155" y2="{bottom+30}" stroke="#9eafb8"/>', conclusion])
    total = int(bottom + used + 90)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{total}" viewBox="0 0 1200 {total}" role="img">
<title>{escape(data['title'])}</title><desc>{escape(data['conclusion'])}</desc>
<defs><marker id="tip" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4 Z" fill="#48616c"/></marker></defs>
<rect width="1200" height="{total}" fill="#fafcfc"/>{''.join(parts)}</svg>'''


def definitions(chapter_id):
    return [dict(generator=name, filename=name + ".png", title=data["title"],
                 alt=data["title"] + ". " + data["conclusion"], after_heading=data["heading"],
                 caption=data["conclusion"])
            for name, data in FIGURES.items() if name.startswith(chapter_id + "_")]


from simple_examples import EXAMPLES
from opening_figures import FIGURES as OPENING_FIGURES

FIGURES.update(OPENING_FIGURES)

for _name, _example in EXAMPLES.items():
    figure(_name, _example["heading"], _example["title"], _example["panels"],
           _example["interpretation"].split(". ", 1)[0].rstrip(".") + ".", arrows=False)
    if "graph" in _example:
        FIGURES[_name].update(kind="network", graph=_example["graph"])
