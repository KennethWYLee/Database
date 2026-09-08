# Chapter 2: Introduction to the Relational Model

## Core Question

What does one row represent, and how can we change the data without confusing it with
the structure of the table? The opening section answers this question using one student
table. The next section connects tables through keys and describes queries with
relational algebra.

## Teaching Summary

| Meeting | Reading and demonstrations | Practice |
|---|---|---|
| First meeting, September 10 | Syllabus first, then an introduction using the opening student-table examples | Discuss the examples introduced by the instructor |
| Chapter continuation | Finish the opening examples as needed, then study keys, schema diagrams, and relational algebra | Response table, key map, schema diagram, and intermediate algebra results as assigned |

The **Week 1** and **Week 2** headings separate the introductory material from keys and
algebra. They do not require you to finish every example in one meeting. The instructor
will indicate where to stop and resume. The four-table database follows the introduction;
assignment, rename, and formal equivalence are optional extensions. Keep using this
notebook as the chapter continues.

In class, the instructor explains each idea and demonstrates the supplied examples.
Pause at the prediction and practice questions to record your own reasoning. The
explanations and preserved outputs also support review after class.

Week 1 draws on Chapter 2, Sections 2.1-2.2, and the reason for identifying tuples at
the start of Section 2.3. Formal key definitions belong to Week 2.

Chapter 3 expresses these query ideas in SQL. This chapter focuses on structure and query
logic rather than SQL syntax. Assignment, rename, and formal equivalence proofs are
extensions and are not major Exam 1 operations.

## Prerequisites

- For Week 1, read a row and a column and compare two values.
- For Week 2, recall that a set contains one copy of each element and use equality,
  inequality, `AND`, and `OR` conditions.
- Python and SQL syntax are not prerequisites for Week 1. Use the supplied code to
  observe the tables; writing SQL begins in Chapter 3.

## Learning Objectives

After completing the opening section, you should be able to:

1. Distinguish the stored data from the DBMS that manages it.
2. Identify a relation, tuple, attribute, and value; distinguish repeated values from
   duplicate tuples and row display order from the facts represented.
3. Check a proposed value against a stated domain, including a value absent from the sample.
4. Show how one phone number per row supports finding an individual number.
5. Explain which instance or schema changes when a row, value, or attribute changes.
6. Use two same-name students to explain why an identifying attribute is needed.

After completing the core chapter sections, you should also be able to classify keys from business rules,
follow foreign-key arrows, and calculate selection, projection, product, join, and set
operations on small relations.

## Week 1: Reading and Changing One Table

### Why Keep a Database?

A registration office needs to record students, courses, and enrollments. To contact a
student, it needs an email address. To check a registration, it needs to identify the
student and the course. These questions require agreed meanings for the stored values.

A **database** is an organized collection of related data. A **database management
system (DBMS)** is software used to define, store, retrieve, and update that data.
Here, SQLite is the DBMS, and Python sends it commands. A displayed table is one view
of the stored data, not the DBMS itself.

### Worked Example: Two Copies Disagree

Two offices keep separate files containing the same student's email. In this synthetic
example, their entries disagree:

| File | student_id | email |
|---|---|---|
| Registration file | S101 | an.chen@example.edu |
| Contact file | S101 | an.old@example.edu |

Before continuing, identify the conflicting value. Can either file alone establish
which address is current?

Both entries identify S101, but they give different email addresses. Neither file has
evidence of which address the student currently uses. For this worked example, assume
the office verifies S101's identity and the student confirms `an.chen@example.edu`.
The office can then record that confirmed address in the shared database. Both offices
can retrieve the same stored record instead of maintaining independent copies.

The email is data; SQLite is the software that stores and retrieves it. Verification
of the address came from the stated confirmation, not from SQLite. A shared database
still needs rules for identifying students and accepting updates. It does not make
an unverified email factually correct just because it can store it.

Practice: in that example, identify the fact being stored, the software managing it, and
the disagreement that must be resolved before contacting the student. Record your answer
in the Week 1 response table.

## 1. Reading a Relation

Every row below describes **one student**, not one course enrollment. This is an original,
synthetic teaching dataset, not a university student record. Department abbreviations are
DES (Digital Design), FIN (Finance), and IM (Information Management).

| student_id | email | student_name | dept_code |
|---|---|---|---|
| S101 | an.chen@example.edu | An Chen | IM |
| S102 | bea.lin@example.edu | Bea Lin | FIN |
| S103 | kai.wu@example.edu | Kai Wu | IM |
| S104 | mira.ho@example.edu | Mira Ho | DES |

A table representing a set of rows is a **relation**. Each complete row is a **tuple**,
and each named column is an **attribute**. `student_name` is an attribute name; `Kai Wu`
is a value of that attribute. The S103 tuple includes all four values, not just its ID.

### Predict Before Running

Write the number of tuples and attributes that the output should contain. Then write
the complete S103 tuple, including its email address. Do not count the header as a tuple.

The next cell creates a small SQLite table and inserts the four synthetic students.
`show_students()` displays its current columns, rows, and counts. Treat the setup as
supplied code; the lesson is how to read its output. This Week 1 table deliberately
omits key and foreign-key enforcement, which is introduced in the Week 2 database.

Run the Week 1 cells in order. To repeat the changes, restart the kernel and begin here
again. The examples use memory only and never open or modify a database file.

```python
import sqlite3
import sys

print(f"Python {sys.version.split()[0]}; SQLite {sqlite3.sqlite_version}")
week1_db = sqlite3.connect(":memory:", isolation_level=None)
week1_db.execute("""CREATE TABLE student (
    student_id TEXT, email TEXT, student_name TEXT, dept_code TEXT
)""")
week1_db.executemany("INSERT INTO student VALUES (?, ?, ?, ?)", [
    ("S101", "an.chen@example.edu", "An Chen", "IM"),
    ("S102", "bea.lin@example.edu", "Bea Lin", "FIN"),
    ("S103", "kai.wu@example.edu", "Kai Wu", "IM"),
    ("S104", "mira.ho@example.edu", "Mira Ho", "DES"),
])

def show_students():
    result = week1_db.execute("SELECT * FROM student ORDER BY student_id")
    columns = [column[0] for column in result.description]
    rows = result.fetchall()
    print(" | ".join(columns))
    for row in rows:
        print(" | ".join(str(value) for value in row))
    print(f"Tuples: {len(rows)}; attributes: {len(columns)}")

show_students()
```

### Read the Output

The output contains four tuples and four attributes. Its S103 tuple is
`(S103, kai.wu@example.edu, Kai Wu, IM)`. These four complete tuples form the current
**relation instance**, the data at this point in the example. The display contains 16
attribute values; it does not describe 16 students.

Practice: identify the attribute whose S102 value is `FIN`, and write the complete S104
tuple. Check your tuple against all four column headings before continuing.

## A Row, a Column, and a Value

Read the annotated student table below. The solid rectangle surrounds one complete
tuple. The dashed rectangle surrounds the `dept_code` attribute, including its heading.
Their intersection contains S103's `IM` value. The outlines identify different parts of
the table; they do not add attributes or change any stored data.

Practice: name a different tuple and a different attribute, then state the value at their
intersection. Explain why one value does not describe the whole student.

## 1.1 Domains and Atomic Values

Which values would be allowed even if they do not appear in the sample? A **domain** is
the set of values allowed for an attribute. For a course's `credits` attribute, this
teaching design allows whole numbers from 1 through 6. A sample containing only 2 and 3
does not limit the domain to those two observed values.

Under that rule, 5 is allowed even though it is absent from the sample. Zero and 7 are
outside the range, and 2.5 is not a whole number. A storage type such as a number or text
does not, by itself, describe every application rule.

### Predict Before Running

For the candidate values `1`, `4`, `6`, `0`, `7`, and `2.5`, predict the printed decision.
The rule and checking procedure stay fixed; only the candidate value changes.

```python
for value in [1, 4, 6, 0, 7, 2.5]:
    allowed = type(value) is int and 1 <= value <= 6
    print(f"{value}: {'allowed' if allowed else 'outside the stated domain'}")
```

```output
1: allowed
4: allowed
6: allowed
0: outside the stated domain
7: outside the stated domain
2.5: outside the stated domain
```

### Read the Output

The check accepts 1, 4, and 6 and rejects 0, 7, and 2.5 under the declared rule. It is a
Python check of the teaching rule, not evidence that a SQLite column automatically
enforces it. Database constraints are taught later. This check does not attempt to
convert text such as `"4"` into a number.

Practice: propose one allowed value absent from the original sample and one disallowed
value. Explain each decision using the rule, not the frequency of values in the sample.

An **atomic value** is treated as one indivisible value for the operations we need.
Whether a value is treated as atomic depends on its intended use, not its punctuation.
A name containing a space is not automatically non-atomic.

### Worked Example: One Phone Number per Row

An office must find the student associated with the individual phone number `555-0102`.
These fictional contact values form a separate paper example; they are not inserted
into the Week 1 database. A student may have more than one phone number.

In the first table, each row describes one student's list of phone numbers. A semicolon
separates numbers within the list.

| student_id | phone_numbers |
|---|---|
| S101 | 555-0101;555-0102 |
| S102 | 555-0103 |

**Predict before reading the result:** how many complete `phone_numbers` cells equal
`555-0102`? If we place one student-phone pair in each row, how many rows and distinct
students will the new table contain?

1. Compare each complete cell with `555-0102`. Neither complete cell equals that value:
   S101's cell contains a two-number list, and S102's cell contains a different number.
   Zero exact matches does not mean that the requested number is absent from the list.
2. Read the two numbers separated by the semicolon for S101. Keep `555-0101` and
   `555-0102` associated with S101; keep `555-0103` associated with S102.
3. Write one student-phone pair per row. Each `phone_number` value now holds one number
   that this application treats as an indivisible contact value.

| student_id | phone_number |
|---|---|
| S101 | 555-0101 |
| S101 | 555-0102 |
| S102 | 555-0103 |

The second table has three tuples but still describes two students. Exactly one row has
`phone_number` equal to `555-0102`, and its student is S101. Repeating S101 preserves
the two phone associations; it does not describe an extra student or an identical tuple.
The original list could also be searched by parsing its entries, but whole-cell equality
alone does not search inside that list. We have changed how the same contact facts are
represented, not discovered new contact information. No SQL is needed for this example.

Practice: if an application must message each address separately, explain the difficulty
with storing `a@example.edu;b@example.edu` for S103 in one email cell. Draw the alternative
two-row table and state what each row represents. Check that both addresses remain
associated with S103 and that a complete email cell can be compared with either address.

## 1.2 Row Order and Repeated Values

Does rearranging rows change the facts? A formal relation is a set of tuples, so row
display order is not part of the relation. Repeated values in a single column, such as
`IM`, are allowed. Identical complete tuples are not repeated in a formal set. SQL tables
can store identical rows when no relevant constraint forbids them. Removing duplicates
from a query result does not remove rows from the stored table. Chapter 3 examines this
distinction and the SQL syntax for producing distinct results.

### Predict Before Running

Predict the first and last IDs when the original students are displayed in reverse ID
order. Predict whether any complete tuple is added or removed. Only display order changes.

```python
ascending = week1_db.execute("SELECT * FROM student ORDER BY student_id").fetchall()
descending = week1_db.execute("SELECT * FROM student ORDER BY student_id DESC").fetchall()
print("Displayed IDs:", ", ".join(row[0] for row in descending))
print("Same complete tuples:", set(ascending) == set(descending))
print("Tuples:", len(descending))
```

```output
Displayed IDs: S104, S103, S102, S101
Same complete tuples: True
Tuples: 4
```

### Read the Output

S104 is now first and S101 is last, but all four complete tuples are unchanged. `True`
confirms equality of the two sets for this example. The formal set definition, rather
than one successful experiment, explains why display order is irrelevant.

Practice: S101 and S103 both have department `IM`. Identify the values that distinguish
their complete tuples. Explain why a repeated department value is not a duplicate tuple.

### Worked Comparison: Repeated Value or Repeated Tuple?

Compare these two cases with the original four-student table. Before reading the
explanation, decide whether the complete row is repeated in each case.

- S101 and S103 both have `IM`. Their IDs, emails, and names differ, so they are two
  distinct tuples even though one attribute value repeats.
- A second copy of `(S101, an.chen@example.edu, An Chen, IM)` repeats all four values
  of the original S101 row. It contributes no new tuple to a formal set. A SQL table
  without a constraint prohibiting that duplicate could nevertheless store the copy.

This comparison does not insert another row into the Week 1 database. The original
table still has four students; the example separates two different meanings of repetition.

## 2. Schema and Instance

A **relation schema** specifies the structure: the relation name and its attributes,
with their domains and applicable constraints. The short notation below lists the name
and attributes; domain and constraint details need additional rules. A database schema
describes the collection of relations. An **instance** contains the current data.

```text
student(student_id, email, student_name, dept_code)
```

Our three demonstrations change the same student table in sequence. Track both the
stored values and the definition: unchanged row counts alone cannot establish that the
instance is unchanged.

### Add a Student

S105 joins the university with email `an.second@example.edu`, name `An Chen`, and
department `FIN`. This is a fifth synthetic student, different from S101. Predict the
new number of tuples and attributes before running the insertion.

```python
week1_db.execute("INSERT INTO student VALUES (?, ?, ?, ?)",
                 ("S105", "an.second@example.edu", "An Chen", "FIN"))
show_students()
```

```output
student_id | email | student_name | dept_code
S101 | an.chen@example.edu | An Chen | IM
S102 | bea.lin@example.edu | Bea Lin | FIN
S103 | kai.wu@example.edu | Kai Wu | IM
S104 | mira.ho@example.edu | Mira Ho | DES
S105 | an.second@example.edu | An Chen | FIN
Tuples: 5; attributes: 4
```

The output has five tuples and the original four attributes. Adding S105 changes the
instance, while the definition of each attribute stays fixed.

Practice: if a sixth student is recorded with those same four attributes, what changes?
State both counts and identify whether a new attribute is needed.

### Change One Attribute Value

S102 moves from Finance to Information Management. Predict S102's new `dept_code`, the
tuple count, and the attribute count. The other students and all column definitions stay fixed.

```python
week1_db.execute("UPDATE student SET dept_code = 'IM' WHERE student_id = 'S102'")
show_students()
```

```output
student_id | email | student_name | dept_code
S101 | an.chen@example.edu | An Chen | IM
S102 | bea.lin@example.edu | Bea Lin | IM
S103 | kai.wu@example.edu | Kai Wu | IM
S104 | mira.ho@example.edu | Mira Ho | DES
S105 | an.second@example.edu | An Chen | FIN
Tuples: 5; attributes: 4
```

S102 now has `IM`, while the table still contains five tuples and four attributes. The
instance changed because one tuple has a different value. The schema did not change.

Practice: explain why correcting an existing student's email address can change the
instance without changing either count. Identify the two snapshots you would compare.

### Add an Attribute

The office now wants a `status` attribute. For this demonstration, it explicitly assigns
the text `active` to all five existing students. This is an assumption of the example,
not information inferred from their other values. Predict the two counts and the value
of the new attribute for S103.

```python
week1_db.execute("ALTER TABLE student ADD COLUMN status TEXT NOT NULL DEFAULT 'active'")
show_students()
```

```output
student_id | email | student_name | dept_code | status
S101 | an.chen@example.edu | An Chen | IM | active
S102 | bea.lin@example.edu | Bea Lin | IM | active
S103 | kai.wu@example.edu | Kai Wu | IM | active
S104 | mira.ho@example.edu | Mira Ho | DES | active
S105 | an.second@example.edu | An Chen | FIN | active
Tuples: 5; attributes: 5
```

There are still five students, but each tuple now has a fifth value. The schema changed
by adding `status`, and the existing tuples are represented using the extended schema.
Do not conclude that adding an attribute leaves every aspect of the instance unchanged.
Choosing a default is a separate decision from choosing the attribute name.

Practice: an office proposes an `admission_year` attribute but has no verified years for
the existing students. Explain why assigning one guessed year to everyone is not a
valid way to establish those facts. Identify the information the office must obtain.

### Comparing the Three Changes

These are consecutive states from the examples above, not three independent databases.

| State | Tuples | Attributes | What changed from the preceding state? |
|---|---:|---:|---|
| Original student table | 4 | 4 | Starting instance and schema |
| After adding S105 | 5 | 4 | The instance gains one tuple; the schema stays the same |
| After changing S102 from FIN to IM | 5 | 4 | The instance changes one value; the schema stays the same |
| After adding status | 5 | 5 | The schema gains an attribute; every existing tuple includes its assigned active value |

Compare actual values as well as counts. The two middle states have the same counts but
different data. Adding `status` changes the definition, even though no student is added.

## 2.1 Why Do Students Need Identifiers?

Which An Chen should receive a correction? The original four names happened to differ.
After the insertion, S101 and S105 are both named An Chen. Our business rule allows
shared names but gives each student a unique, stable ID. A current sample alone cannot
establish that a name will always identify a student.

Predict how many rows the name `An Chen` matches and which IDs appear.

```python
matches = week1_db.execute(
    "SELECT student_id, student_name, dept_code FROM student "
    "WHERE student_name = 'An Chen' ORDER BY student_id"
).fetchall()
print("student_id | student_name | dept_code")
for row in matches:
    print(" | ".join(row))
print("Rows matching the name:", len(matches))
week1_db.close()
```

```output
student_id | student_name | dept_code
S101 | An Chen | IM
S105 | An Chen | FIN
Rows matching the name: 2
```

The query matches two students. A request naming only An Chen does not say which record
to correct. Ask for the student ID before applying the change. IDs resolve this request
under the stated uniqueness rule; the minimal Week 1 table has not yet enforced that
rule as a constraint. Week 2 introduces primary and candidate keys and their enforcement.

Practice: write a request that unambiguously changes S105's email, and explain why using
S101 instead would modify another student's record. No update is required here.

## Week 1 Practice

Use this separate synthetic course instance for the final practice. Each row describes
one course, `course_id` is unique by rule, and titles are allowed to repeat. Credits are
whole numbers from 1 through 6. This instance has not been inserted into the Week 1 database.
If a `description` attribute is added, it will hold one catalog description per course.

| course_id | title | credits |
|---|---|---:|
| DB201 | Database Management | 3 |
| ML230 | Machine Learning | 3 |
| WD120 | Web Design | 2 |

For the change questions, use `(DB205, Database Management, 5)` as the new course, and
change WD120's credits from 2 to 3. Start from the original three-row table for each
change, not from the result of the preceding question. For the new description attribute,
assume verified catalog text will be supplied for each course; do not invent its content.

Add a Markdown response below this table in your notebook. Include one prediction, the
observed result, and either your correction or an explanation of why your prediction was
correct. These are practice
responses; submit them only when the instructor designates them for Class Performance.

| Prompt | Your response | What to inspect |
|---|---|---|
| Explain the role of the DBMS in the conflicting-email example. | ... | Separate the stored fact, software, and unresolved disagreement. |
| State the tuple and attribute counts of the course instance. Copy one complete tuple and name one attribute value. | ... | Match each value to a heading; exclude the header from the tuple count. |
| Evaluate proposed credits 5, 0, and 3.5. | ... | Apply both the whole-number and range rules. |
| Starting from this course instance each time: add DB205; change WD120's credits from 2 to 3; add a description attribute. What changes in each case? | ... | Compare values, column definitions, and both counts. Explain why descriptions require catalog information rather than guessed text. |
| After adding DB205, which two courses are titled Database Management? What information is needed before changing one of them? | ... | Use the declared rule and identify both possible records. |
| Give one example of a repeated column value that does not make two complete tuples duplicates. | ... | Compare every attribute of the two rows. |
| What would reverse row display order change? | ... | Distinguish display position from stored facts. |
| Show the two-row email alternative from Section 1.1 and explain the original cell's limitation. | ... | Preserve both S103-address pairs; explain which complete cell can match an individual address. |
| Record one prediction, its observed result, and your correction or reason for agreement. | ... | Cite a particular row, column, count, or printed decision. |

Before finishing, check that every conclusion names a rule or a displayed value. A
statement such as "the schema changes" needs the name of the definition that changed.
Compare your reasoning with the worked examples; the final practice uses a different table.

## End of Week 1

The DBMS manages stored data, but storing a value does not establish that it is true.
Read each tuple as a complete row of attribute values, and use the stated domain to
judge proposed values. Reordering the display does not change the relation; changing
S102's department changes the instance even when the counts stay the same. Adding
`status` changes the schema. The two An Chen records show why an identifier must follow
a declared rule rather than the names that happen to occur in one sample.

Keep your practice responses and your comparison between a prediction and an observed
result in this notebook. Week 2 builds on these distinctions to define keys and connect
several relations.

**Introductory reading checkpoint.** This is not a first-meeting completion deadline.
The Week 1 database connection is closed. Week 2 creates a
separate four-table database from the original data: S105 and the extra `status` column
do not carry over. Continue at the following heading when the instructor introduces keys.

## Week 2: Keys and Relational Algebra

Recall why two same-name students cannot be distinguished by name alone. We now use
formal key definitions and connect students to departments, courses, and enrollments.
The tables below use the original synthetic data. Assignment, rename, and formal
equivalence remain optional extensions.

Use the supplied code to observe results. You do not need to write the Python setup or
transaction-control statements in this chapter. Focus on the tables, rules, and query
results; writing SQL begins in Chapter 3.

## Course-Registration Data

### `department`

| dept_code | dept_name | building |
|---|---|---|
| DES | Digital Design | Hong Hall |
| FIN | Finance | Cheng Hall |
| IM | Information Management | Hong Hall |

### `student`

| student_id | email | student_name | dept_code |
|---|---|---|---|
| S101 | an.chen@example.edu | An Chen | IM |
| S102 | bea.lin@example.edu | Bea Lin | FIN |
| S103 | kai.wu@example.edu | Kai Wu | IM |
| S104 | mira.ho@example.edu | Mira Ho | DES |

### `course`

| course_id | title | dept_code | credits |
|---|---|---|---:|
| DB201 | Database Management | IM | 3 |
| FT210 | Financial Technology | FIN | 3 |
| ML230 | Machine Learning | IM | 3 |
| WD120 | Web Design | DES | 2 |

### `enrollment`

| student_id | course_id | term | grade |
|---|---|---|---|
| S101 | DB201 | 115-1 | A |
| S101 | FT210 | 115-1 | B+ |
| S102 | FT210 | 115-1 | A- |
| S103 | DB201 | 115-1 | B |
| S103 | ML230 | 115-1 | A |
| S104 | WD120 | 115-1 | A- |

The design uses these business rules:

- Each student has one unique, stable `student_id`.
- Every student has an email; each email belongs to at most one student. Names may repeat.
- Each department and course has a unique code.
- Course credits are whole numbers from 1 through 6.
- A student has at most one enrollment in the same course and term.
- Student and course department codes must reference an existing department.
- Enrollment student and course identifiers must reference existing rows.

Before studying keys, identify all attributes of `enrollment` and copy the tuple for
S103 taking ML230. Apply the Week 1 distinction between an attribute name and its value.

Before running the setup, predict the table names and row counts from the four tables
above: how many departments, students, courses, and enrollments should be stored?
The supplied SQL creates these tables; Chapter 3 will explain how to write this syntax.
Its credits constraint checks both the stored integer type and the permitted range.
In SQLite, declaring an `INTEGER` column alone does not reject every fractional value.

<!-- sql:setup -->

The output lists 3 departments, 4 students, 4 courses, and 6 enrollments. Its
foreign-key check reports `PASS`. This checks stored references, not whether every
business rule of a real university has been captured. Predict which four student IDs
the next query will display.

<!-- sql:example 1 -->
```output
student_id | email | student_name | dept_code
S101 | an.chen@example.edu | An Chen | IM
S102 | bea.lin@example.edu | Bea Lin | FIN
S103 | kai.wu@example.edu | Kai Wu | IM
S104 | mira.ho@example.edu | Mira Ho | DES
```

The output restores the original four students. It does not contain the extra student
or `status` column from the introductory demonstrations.

## 3. Keys

Keys follow from the schema and business rules, not merely from accidental uniqueness in
the current sample.

- A **superkey** is an attribute set that uniquely identifies a tuple. It may contain
  unnecessary attributes.
- A **candidate key** is a minimal superkey.
- A **primary key** is the candidate key selected as the main identifier.
- A **composite key** contains more than one attribute.

### Worked Example: `student`

`{student_id}` and `{email}` are candidate keys under the stated rules.
`{student_id, student_name}` is a superkey but not a candidate key because
`student_name` is unnecessary. `{student_name}` is not guaranteed to be unique even
though the four sample names differ. This design selects `student_id` as the primary key.

A primary-key value must be present and unique. In this SQLite schema, `NOT NULL`
explicitly enforces presence for the text identifiers. Do not assume that a declaration
of `TEXT PRIMARY KEY` alone enforces this in an ordinary SQLite table.

Predict whether each proposed student will be accepted: one has no identifier, while
the other reuses S101 with a new email. Neither proposal should add a student.

```python
for label, values in [
    ("Missing student ID", (None, "missing@example.edu", "New Student", "IM")),
    ("Repeated student ID", ("S101", "new@example.edu", "New Student", "IM")),
]:
    connection.execute("SAVEPOINT key_example")
    try:
        connection.execute("INSERT INTO student VALUES (?, ?, ?, ?)", values)
        print(label + ": accepted")
    except sqlite3.IntegrityError:
        print(label + ": rejected")
    finally:
        connection.execute("ROLLBACK TO key_example")
        connection.execute("RELEASE key_example")
```
```output
Missing student ID: rejected
Repeated student ID: rejected
```

Both proposals are rejected. The first lacks an identifier; the second duplicates one.
These two checks support the stated rules for this schema; they do not make names unique.

### Worked Example: `enrollment`

Neither `student_id` nor `course_id` alone identifies an enrollment. The composite key
`{student_id, course_id, term}` does under the stated rule.

Why not use just `{student_id, course_id}`? In this synthetic example, the rules permit
a student to enroll in the same course in another term. Temporarily add S101 taking
DB201 in `115-2`, with no grade recorded yet. Predict the two rows for this student and
course. Then predict whether another copy of `(S101, DB201, 115-2)` is allowed.

```python
connection.execute("SAVEPOINT term_example")
try:
    connection.execute("INSERT INTO enrollment VALUES ('S101', 'DB201', '115-2', NULL)")
    run_sql_script(connection, """
SELECT student_id, course_id, term, grade
FROM enrollment
WHERE student_id = 'S101' AND course_id = 'DB201'
ORDER BY term;
""")
    try:
        connection.execute("INSERT INTO enrollment VALUES ('S101', 'DB201', '115-2', NULL)")
        print("Repeated student/course/term: accepted")
    except sqlite3.IntegrityError:
        print("Repeated student/course/term: rejected")
finally:
    connection.execute("ROLLBACK TO term_example")
    connection.execute("RELEASE term_example")
```
```output
student_id | course_id | term | grade
S101 | DB201 | 115-1 | A
S101 | DB201 | 115-2 | NULL
Repeated student/course/term: rejected
```

The two rows share the student and course, but differ in `term`. The repeated triple
is rejected. `NULL` here marks the unrecorded grade; it is not a missing key value.
The example restores the original six enrollments before the next activity.

To check minimality, consider removing each attribute from the proposed key:

| Attribute removed | Remaining attributes | Permitted rows that cannot be distinguished |
|---|---|---|
| `term` | `student_id, course_id` | S101 taking DB201 in 115-1 and 115-2 |
| `course_id` | `student_id, term` | S101 taking DB201 and FT210 in 115-1 |
| `student_id` | `course_id, term` | S101 and S103 taking DB201 in 115-1 |

Each smaller pair can repeat under the rules. The rule allows at most one row for the
complete triple, so this triple is a candidate key, not just a large superkey.

### Practice

Compare `student_name`, `email`, and `student_id` as proposed primary keys. First identify
the candidate keys. Then discuss stability, possible changes, length, and business
meaning. A design conclusion requires reasons, not a vote.

## 4. Foreign Keys and Schema Diagrams

A **foreign key** is an attribute or attribute set in the referencing relation.
In the textbook's Chapter 2 definition, its values must match a primary-key value in
the referenced relation. For example, `student.dept_code` references
`department.dept_code`.

All references in this example target primary keys. SQLite also permits a reference
to an appropriately declared unique key; that implementation rule is broader than
the Chapter 2 definition. Neither rule permits a reference to arbitrary repeated values.

Adding a student with department `LAW` violates the rule unless the LAW department is
created first. In these tables the referencing identifiers are required; more generally,
SQL foreign keys may allow missing values unless a constraint forbids them.
A foreign key need not be unique in the referencing relation; many
students may belong to IM.

Predict whether this new student's department can be found in `department`.

```python
connection.execute("SAVEPOINT reference_example")
try:
    connection.execute("INSERT INTO student VALUES ('S106', 'law@example.edu', 'New Student', 'LAW')")
    print("Department LAW: accepted")
except sqlite3.IntegrityError:
    print("Department LAW: rejected")
finally:
    connection.execute("ROLLBACK TO reference_example")
    connection.execute("RELEASE reference_example")
```
```output
Department LAW: rejected
```

`LAW` has no referenced department row. The new ID and email do not fix that missing
reference. Trace the required arrow in the diagram before proposing a valid change.

```text
department
  PK dept_code
     dept_name
     building
       ^
       | student.dept_code, course.dept_code

student                              course
  PK student_id                        PK course_id
  CK email                             FK dept_code -> department.dept_code
     student_name                         title
  FK dept_code -> department.dept_code    credits
       ^                                  ^
       |                                  |
       +---------- enrollment ------------+
                    PK/FK student_id -> student.student_id
                    PK/FK course_id  -> course.course_id
                    PK    term
                          grade
```

To find the name and course department for enrollment `(S101, DB201, 115-1, A)`, follow
`enrollment.student_id` to Student, then `enrollment.course_id` to Course, and finally
`course.dept_code` to Department.

This is a relational schema diagram: its boxes are tables with attributes and keys.
It is not an E-R diagram. Chapter 6 introduces entities and relationships before
mapping them to tables; similar-looking boxes and lines can have different meanings.

### Evidence to Retain

Create a schema-and-key sheet containing all primary keys, every foreign key and its
direction, the two Student candidate keys, one nonminimal superkey, and one modification
that would violate referential integrity.

## 5. Relational-Algebra Operations

Each relational-algebra operation accepts one or two relations and returns a relation.
This closure property allows operations to be composed.

| Operation | Symbol | Main question |
|---|---|---|
| Selection | `σ` | Which tuples remain? |
| Projection | `Π` | Which attributes remain? |
| Cartesian product | `×` | What are all cross-relation tuple combinations? |
| Theta join | `⋈_θ` | Which combinations satisfy the join condition? |
| Union | `∪` | Which tuples occur in either input? |
| Intersection | `∩` | Which tuples occur in both inputs? |
| Set difference | `−` | Which tuples occur in the left input but not the right? |

### Selection

```text
σ_dept_code='IM'(student)
```

Before running the selection, list the student IDs whose `dept_code` is IM. Will it
remove columns or only rows?

<!-- sql:example 2 -->
```output
student_id | email | student_name | dept_code
S101 | an.chen@example.edu | An Chen | IM
S103 | kai.wu@example.edu | Kai Wu | IM
```

The output keeps the complete S101 and S103 tuples, including all four attributes.
Predict the result of
`σ_dept_code='IM' AND student_id!='S101'(student)` and explain which predicate excludes
each removed tuple.

### Projection

```text
Π_dept_code(student)
```

Projection removes duplicate tuples because a formal relation is a set. Predict how
many distinct department codes remain from the four students; IM appears twice.

<!-- sql:example 3 -->
```output
dept_code
DES
FIN
IM
```

The formal result is `{DES, FIN, IM}`: three tuples with one attribute each. SQL uses
`DISTINCT` to match this duplicate removal. The student table still has four rows.
Predict `Π_building(department)` and handle the repeated
`Hong Hall` value correctly.

### Composition

```text
Π_student_name(σ_dept_code='IM'(student))
```

Predict the intermediate student IDs, then the final distinct names. Which operation
must be evaluated first?

<!-- sql:example 4 -->
```output
student_name
An Chen
Kai Wu
```

The inner selection keeps S101 and S103; the outer projection produces
`{An Chen, Kai Wu}`. Now predict the final names if another IM student is also named
An Chen. Only the input data changes; the query stays the same.

```python
connection.execute("SAVEPOINT same_name_example")
try:
    connection.execute("INSERT INTO student VALUES ('S106', 'second.an@example.edu', 'An Chen', 'IM')")
    run_sql_script(connection, SQL_EXAMPLE_4)
finally:
    connection.execute("ROLLBACK TO same_name_example")
    connection.execute("RELEASE same_name_example")
```
```output
student_name
An Chen
Kai Wu
```

The output still has two distinct names, although the temporary selected input has three
students. Formal projection keeps one copy of the name, not one row per person. A plain
SQL `SELECT` without `DISTINCT` would repeat An Chen. The temporary student is removed.

Write an expression for the identifiers and titles of three-credit
courses, and state which operation runs first in the expression.

### Cartesian Product

Before executing `{S101, S102} × {DB201, FT210}`, predict the number of pairs and list
them. Does a product check whether each student enrolled in each course?

<!-- sql:example 5 -->
```output
student_id | course_id
S101 | DB201
S101 | FT210
S102 | DB201
S102 | FT210
```

The result has four pairs. These are possible combinations, not four enrollment facts:
S102 taking DB201 does not appear in the enrollment table. The complete Student and Course relations have
four tuples each, so their product has 16 tuples.

### Theta Join

```text
student ⋈_student.student_id=enrollment.student_id enrollment
```

A theta join can be understood as a Cartesian product followed by a selection:

Here, `r` and `s` are the input relations, and `theta` is a condition on their
attributes. The join retains every attribute from both inputs; qualifying a repeated
name, such as `student.student_id`, identifies which input it came from.

```text
r ⋈_theta s = σ_theta(r × s)
```

Predict the number of matching rows when four students are joined to six enrollments
on student ID. Compare it with the number of rows in the product without that condition.
The demonstration displays the student name, course ID, and term from each match.

<!-- sql:example 6 -->
```output
student_name | course_id | term
An Chen | DB201 | 115-1
An Chen | FT210 | 115-1
Bea Lin | FT210 | 115-1
Kai Wu | DB201 | 115-1
Kai Wu | ML230 | 115-1
Mira Ho | WD120 | 115-1
```

There are six matches in this instance, one per enrollment. Unlike the product example,
there is no S102/DB201 enrollment. Omitting the join predicate produces 24 combinations, most of which
are not enrollment facts.

Practice: identify the two relations and join predicate needed to connect a course title
to its department name.

## 6. Set Operations

Union, intersection, and difference require compatible input relations: the same number
of attributes and compatible domains in corresponding positions.

Let:

```text
A = students in DB201 = {S101, S103}
B = students in FT210 = {S101, S102}
```

Predict the IDs in the union, intersection, and A-minus-B results before running the
three queries. Pay attention to S101, which belongs to both input sets.

<!-- sql:example 7a -->
```output
student_id
S101
S102
S103
```

The union has three IDs. S101 occurs once, even though it belongs to both courses.

<!-- sql:example 7b -->
```output
student_id
S101
```

The intersection contains only S101, the student present in both input sets.

<!-- sql:example 7c -->
```output
student_id
S103
```

The difference contains S103: this student is in DB201 but not FT210. Compare the
observed results with the complete table, including the reverse difference:

| Expression | Meaning | Result |
|---|---|---|
| `A ∪ B` | In DB201 or FT210 or both | `{S101, S102, S103}` |
| `A ∩ B` | In both courses | `{S101}` |
| `A − B` | In DB201 but not FT210 | `{S103}` |
| `B − A` | In FT210 but not DB201 | `{S102}` |

Set difference has direction. `student ∪ course` is invalid because the schemas are not
compatible.

Practice: let C be the students in ML230. Write C, then calculate `A ∪ C`, `A ∩ C`, and
`C − A`.

## Extensions

### Assignment

Assignment names an intermediate relation without changing the permanent database:

```text
db_students <- Π_student_id(σ_course_id='DB201'(enrollment))
fintech_students <- Π_student_id(σ_course_id='FT210'(enrollment))
db_students ∩ fintech_students
```

Predict whether naming the two inputs changes their intersection.

<!-- sql:example 8 -->
```output
student_id
S101
```

S101 is still the only common ID. The SQL `WITH` clause gives names to query results;
it does not insert new students or change the stored enrollment table.

### Rename

Rename distinguishes multiple uses of the same relation:

```text
ρ_s1(student)
ρ_s2(student)
```

It supports a self-comparison such as finding different students in the same department.

Predict the distinct student pair from IM. The ID comparison excludes self-pairs and
keeps only one ordering of each pair.

<!-- sql:example 9 -->
```output
student_1 | student_2 | dept_code
An Chen | Kai Wu | IM
```

An Chen and Kai Wu form the only pair in this instance. The two names `s1` and `s2`
refer to separate uses of the same table; they do not create two stored tables.

### Simple Equivalence

These expressions place the same Student-only filter before or after an inner join:

```text
Q1 = σ_student.dept_code='IM'(
       student ⋈_student.student_id=enrollment.student_id enrollment
     )

Q2 = (σ_dept_code='IM'(student))
     ⋈_student.student_id=enrollment.student_id enrollment
```

Predict the displayed name/course pairs for both queries. The same inner-join condition
and IM filter are used; only the placement of the filter changes.

<!-- sql:example 10a -->
```output
student_name | course_id
An Chen | DB201
An Chen | FT210
Kai Wu | DB201
Kai Wu | ML230
```

Filtering after the join gives four pairs. Compare them with filtering students first:

<!-- sql:example 10b -->
```output
student_name | course_id
An Chen | DB201
An Chen | FT210
Kai Wu | DB201
Kai Wu | ML230
```

Both queries display the same four pairs for this instance. The SQL demonstrations show
selected columns from Q1 and Q2, not every attribute of the joined relations.
They express the same result under the stated conditions. Equality on one sample alone is
not a proof for every legal instance. Chapter 16 revisits equivalence as an optimization
guardrail.

## Common Errors

1. Choosing a key from accidental uniqueness in the sample.
2. Calling every superkey a candidate key.
3. Drawing a foreign-key arrow in the wrong direction.
4. Assuming tuple display order is part of a relation.
5. Forgetting duplicate removal in formal projection and set operations.
6. Treating a Cartesian product as a factual relationship.
7. Omitting the join predicate.
8. Reversing set difference.

## Discussion and Individual Evidence

For each proposed key or algebra result, state the business rule or operation that
supports the answer. Retain the schema sheet, key map, each intermediate relation, and
one prediction with its observed result. Include either a correction or an explanation
of why your prediction was correct. Submit only the work assigned by the instructor.

## Chapter Summary

A schema defines structure and constraints; an instance contains current tuples. Keys
identify rows and foreign keys connect relations. Selection filters tuples, projection
keeps attributes, a join selects meaningful cross-relation combinations, and set
operations compare compatible results. Chapter 3 expresses these operations in SQL.

## After-Class Continuation

Recalculate one algebra expression after changing a tuple in the sample data, and explain
which intermediate relation changed. Assignment, rename, and formal equivalence proofs
are optional extensions rather than required Exam 1 derivations.

## Check the Database State

The temporary examples should leave the original 3 departments, 4 students, 4 courses,
and 6 enrollments unchanged. Predict whether these checks will pass after the examples.

<!-- sql:checks -->
```output
Notebook checks passed.
Database connection closed.
```

The counts and foreign-key check pass, and the connection is closed. These checks cover
the database state, not your written explanations. Restart from the four-table setup
to repeat this part of the chapter; the introductory database is not required.
