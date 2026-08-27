# Chapter 4: Intermediate SQL

## Core Question

How can SQL express relationships clearly, retain unmatched rows when required, define a
reusable view, group several changes into one unit, and reject invalid data?

## Connection to Chapter 3

Chapter 3 used comma-separated inputs and a `WHERE` matching predicate. This chapter uses
explicit joins:

```sql
FROM student AS s
JOIN enrollment AS e ON e.student_id = s.student_id
```

For an inner join, a predicate in `ON` or `WHERE` may produce the same rows. For an outer
join, moving a predicate can change which unmatched rows survive.

## Teaching Summary

| Topic | Worked example and practice | Evidence to retain |
|---|---|---|
| Explicit and outer joins | Course enrollment with matched and unmatched rows | Join predicate and checked result |
| Views | Live department-query view and attempted update | Base-query comparison and error evidence |
| Transactions | Multi-statement change followed by rollback | Before, during, and after states |
| Constraints and reference actions | Feedback rules and deletion behavior | Passing and failing test cases |

## Prerequisites and Setup

You should be able to use aliases, `SELECT`, `WHERE`, grouping, `NULL`, and basic data
modification, and identify primary and foreign keys.

With the student package, run this command from the package root:

```powershell
py -3 run_labs.py ch04
```

If separate files are provided, create a new SQLite database, run the Chapter 2 setup,
and then run `student_lab.sql`. The materials were verified with SQLite 3.45.3.

## Learning Objectives

After completing this chapter, you should be able to:

1. Write explicit joins and explain every matching condition.
2. Compare `ON`, `USING`, and the risks of `NATURAL JOIN`.
3. Predict which rows an inner or left outer join retains.
4. Explain why a right-side condition in `ON` can differ from the same condition in
   `WHERE` after a left join.
5. Create and query a view and distinguish it from a stored result.
6. Use `COMMIT` and `ROLLBACK` to define a basic atomic unit of work.
7. Use `NOT NULL`, `UNIQUE`, `CHECK`, and foreign keys to express data rules.
8. Explain the effect of reject, `CASCADE`, and `SET NULL` reference actions.

Right and full outer joins, detailed view-update rules, materialized views, deferred
constraints, assertions, and authorization are extensions.

## 1. Explicit Inner Joins

An inner join retains row pairs that satisfy its join condition. Use `ON` for the
relationship between inputs and `WHERE` for additional filtering.

```sql
SELECT s.student_id, s.student_name,
       c.course_id, c.title, e.grade
FROM student AS s
JOIN enrollment AS e ON e.student_id = s.student_id
JOIN course AS c ON c.course_id = e.course_id
ORDER BY s.student_id, c.course_id;
```

The first join connects each enrollment to one student. The second connects it to one
course. The result has six rows. S101 taking FT210 remains valid even though the student
and course departments differ; department equality is not the enrollment relationship.

### Practice

List each enrollment's student email and course department name. Write the required
relations and both matching conditions before writing the complete query.

### Check Criteria

The result has six rows and retains S101/FT210 with the course department Finance. Too
many rows usually indicate a missing condition; too few may indicate an extra condition
that was not part of the requirement.

## 2. `USING` and `NATURAL JOIN`

`USING(column)` explicitly selects a same-named matching column. `NATURAL JOIN` uses all
same-named columns automatically, so a schema change or an unrelated name collision can
silently change the result.

```sql
SELECT c.course_id, c.title, d.dept_name
FROM course AS c
JOIN department AS d USING (dept_code)
ORDER BY c.course_id;
```

The result has one department for each of the four courses.

### Counterexample

```sql
SELECT student_id, student_name, course_id, title
FROM student
NATURAL JOIN enrollment
NATURAL JOIN course;
```

After the first join, both `course_id` and `dept_code` are same-named columns for the next
natural join. The query incorrectly removes S101/FT210 because the student's department
does not equal the course's department. Explicit `ON` conditions return the correct six
rows.

Practice: rewrite the `USING` example with `ON c.dept_code = d.dept_code` and compare
rows and output columns.

## 3. Inner and Outer Joins

| Join type | Unmatched rows retained |
|---|---|
| `INNER JOIN` | None |
| `LEFT JOIN` | Left input |
| `RIGHT JOIN` | Right input |
| `FULL JOIN` | Both inputs |

The classroom core uses left outer join. Right and full joins are included only for
recognition and portability awareness.

### Worked Example

The lab temporarily adds course IS250 with no enrollment:

```sql
SELECT c.course_id, c.title, COUNT(e.student_id) AS enrollment_count
FROM course AS c
LEFT JOIN enrollment AS e ON e.course_id = c.course_id
GROUP BY c.course_id, c.title
ORDER BY c.course_id;
```

IS250 remains with count 0. Use `COUNT(e.student_id)`, not `COUNT(*)`, because the latter
would count the null-padded outer-join row as one.

### Practice

List every student and enrollment count, including a temporary student with no
enrollment. The temporary student must appear once with count 0.

## 4. Conditions in `ON` and `WHERE`

For a left join, `ON` first determines matches and then preserves unmatched left rows.
`WHERE` filters the completed join result.

```sql
SELECT c.course_id, e.student_id, e.grade
FROM course AS c
LEFT JOIN enrollment AS e
  ON e.course_id = c.course_id
 AND e.grade IN ('A', 'A-');
```

This retains all courses and attaches only high-grade enrollments. If the grade condition
is moved to `WHERE`, an unmatched course has `NULL` grade, the predicate becomes
`UNKNOWN`, and that course is removed.

### Predict and Check

- Requirement A: retain all courses and attach only passing enrollments.
- Requirement B: list only courses with at least one passing enrollment.

Place the grade condition for each requirement and explain whether an unmatched course
survives. The answer must use outer-join and `NULL` reasoning, not a memorized preference
for `ON`.

## 5. Views

A view is a virtual relation defined by a query. A regular view stores its definition and
is evaluated from current base data; it is not a fixed copy of the creation-time result.

```sql
CREATE VIEW course_enrollment_summary AS
SELECT c.course_id,
       c.title,
       COUNT(e.student_id) AS enrollment_count
FROM course AS c
LEFT JOIN enrollment AS e ON e.course_id = c.course_id
GROUP BY c.course_id, c.title;
```

```sql
SELECT course_id, enrollment_count
FROM course_enrollment_summary
WHERE enrollment_count >= 2;
```

The current result includes DB201 and FT210. A temporary base-table change alters the
view result; rollback restores it.

### Practice

Create `im_course(course_id, title, credits)` for IM courses and query its three-credit
rows. A temporary IM course added to the base table should appear through the view and
disappear after rollback.

### Extension: View Modification

A join or aggregate view may not map an update to one unambiguous base row. SQLite views
are read-only unless an `INSTEAD OF` trigger is supplied, while other DBMS products may
allow selected simple-view updates. Treat this as a product-specific rule.

## 6. Transaction Boundaries

A transaction groups statements into one unit of work. `COMMIT` keeps the transaction's
changes. `ROLLBACK` removes uncommitted changes. Tool-specific autocommit settings must be
checked explicitly.

```sql
BEGIN;

DELETE FROM enrollment
WHERE student_id = 'S101'
  AND course_id = 'FT210'
  AND term = '115-1';

INSERT INTO enrollment (student_id, course_id, term, grade)
VALUES ('S101', 'ML230', '115-1', NULL);

COMMIT;
```

If the insertion fails after an independently committed deletion, the course swap is
only half complete. One transaction allows the application to roll back the whole unit.

Practice: perform a different valid course swap inside a savepoint. Retain the before,
modified, and post-rollback rows.

## 7. Integrity Constraints

```sql
CREATE TABLE waitlist_entry (
    request_id INTEGER PRIMARY KEY,
    student_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    term TEXT NOT NULL DEFAULT '115-1',
    priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 5),
    UNIQUE (student_id, course_id, term)
);
```

`UNIQUE` prevents duplicate requests for the same student, course, and term. `CHECK`
limits priority. `DEFAULT` supplies a value only when the insertion omits the column.

A `CHECK` constraint rejects `FALSE`, but a comparison with `NULL` may be `UNKNOWN`.
Therefore `CHECK (priority > 0)` does not replace `NOT NULL`.

### Practice

Predict which rule rejects a duplicate request, priority 8, and a `NULL` student
identifier. Test each failure separately; do not rely on the order in which a DBMS reports
multiple violations.

## 8. Foreign-Key Actions

```sql
FOREIGN KEY (student_id) REFERENCES student (student_id)
    ON DELETE CASCADE,
FOREIGN KEY (course_id) REFERENCES course (course_id)
```

- Reject/no action prevents deletion while dependent rows remain.
- `CASCADE` removes dependent rows.
- `SET NULL` writes `NULL`, so the referencing column must allow it.

The choice follows the data-life-cycle rule. Cascading a waitlist row after a student
leaves may be appropriate. Cascading historical enrollment rows may destroy records that
must be retained.

### Design Practice

Design `course_feedback` so rating is 1-5, each row references one existing composite
Enrollment key, and each enrollment has at most one feedback row. Test a valid row, a
rating of 6, and a reference to a missing enrollment.

## Common Errors

1. Using `NATURAL JOIN` without listing every same-named column.
2. Moving a right-side left-join condition to `WHERE` and losing unmatched rows.
3. Counting null-padded rows with `COUNT(*)`.
4. Treating a regular view as a stored snapshot.
5. Assuming that every view is updatable.
6. Depending on an unknown autocommit setting.
7. Using `CHECK` alone to reject `NULL`.
8. Selecting `CASCADE` without considering the data life cycle.

## Classroom and Individual Evidence

Review an AI-generated query containing a natural join, a left-join filter in `WHERE`, a
questionable view update, and an unexplained cascade. Judge its explicit relationship,
unmatched rows, base-row mapping, transaction boundary, and business rule.

Retain initial predictions, lab output, comparison reasons, and the individually corrected
version. Peer ranking does not directly determine the course grade.

## Chapter Summary

Explicit joins expose matching rules. Outer joins preserve selected unmatched rows, so
`ON` and `WHERE` are not interchangeable. A regular view stores a query definition.
Transactions define all-or-nothing work, and constraints make checkable data rules part of
the schema. Chapter 5 introduces selected advanced SQL features.

## After-Class Continuation

Revise one outer-join query so that its unmatched rows have a stated purpose, then design
one constraint test that should succeed and one that should fail. Retain the prediction,
observed result, and business rule represented by each test.
