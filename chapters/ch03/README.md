# Chapter 3: Introduction to SQL

## Core Question

How can SQL define relational structure, retrieve the intended rows, handle duplicates
and `NULL`, summarize groups, and modify data without violating constraints?

Use this guide with `student_lab.sql`. Before running it in a new SQLite database, run the
Chapter 2 `course_registration_setup.sql` file.

## Connection to Chapter 2

| Relational-algebra idea | Main SQL expression |
|---|---|
| Projection `Π` | Column list in `SELECT` |
| Selection `σ` | Predicate in `WHERE` |
| Cartesian product `×` | Multiple inputs without a matching predicate |
| Rename `ρ` | `AS` aliases |
| Union `∪` | `UNION` |
| Intersection `∩` | `INTERSECT` |
| Difference `−` | `EXCEPT` |

This table explains query meaning, not physical execution order. Chapters 15 and 16
address execution plans.

## Teaching Summary

| Topic | Worked example and practice | Evidence to retain |
|---|---|---|
| Table definition and basic queries | Course-registration tables and row filters | Executed SQL and checked rows |
| Duplicates, set operations, and `NULL` | `DISTINCT`, `EXCEPT`, and three-valued logic | Prediction and observed result |
| Grouping and subqueries | Department totals and nested enrollment queries | Intermediate and final results |
| Data modification | Reversible insert, update, and delete | Target-row check and rollback evidence |

## Prerequisites

- Identify relations, attributes, primary keys, and foreign keys.
- Apply selection, projection, product, and set operations to small relations.
- Predict whether a modification could violate a key or reference rule.

## Learning Objectives

After completing this chapter, you should be able to:

1. Create tables with data types, keys, `NOT NULL`, and simple `CHECK` constraints.
2. Use `SELECT`, `FROM`, `WHERE`, aliases, expressions, patterns, and ordering.
3. Distinguish default duplicate behavior from `DISTINCT` and SQL set operations.
4. Use `IS NULL` and explain why `UNKNOWN` does not pass `WHERE`.
5. Use aggregate functions, `GROUP BY`, and `HAVING`.
6. Use `IN`, `EXISTS`, one correlated subquery, and one CTE.
7. Explain the `NOT IN` risk when the comparison set contains `NULL`.
8. Predict and verify the effects of `INSERT`, `UPDATE`, and `DELETE`.

Before each example, predict the result columns, row count, duplicate or `NULL` behavior,
and whether the statement reads data, modifies data, or changes the schema.

## 1. Defining Structure

SQL includes data-definition statements, data-manipulation statements, and integrity
constraints. This course uses SQLite for executable work, so its examples use `TEXT` and
`INTEGER`. SQLite type affinity is not a rule for every DBMS.

```sql
CREATE TABLE study_group (
    group_id TEXT PRIMARY KEY,
    group_name TEXT NOT NULL,
    course_id TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity BETWEEN 2 AND 8),
    FOREIGN KEY (course_id) REFERENCES course (course_id)
);
```

The primary key identifies a group. Required values cannot be `NULL`. Capacity must be
between 2 and 8, inclusive, and the course must already exist.

### Practice

Design constraints for
`study_group_member(group_id, student_id, member_role)`. Prevent duplicate membership and
references to missing groups or students.

### `DELETE`, `DROP`, and `ALTER`

`DELETE` removes selected rows while retaining the table. `DROP TABLE` removes the table
and its data. `ALTER TABLE` changes a schema, with product-specific capabilities.

To remove only G01, use a `DELETE` statement with a predicate that identifies G01. Never
substitute `DROP TABLE` for a row-level removal.

## 2. Basic Queries

```sql
SELECT result_expressions
FROM input_relations
WHERE predicate;
```

For meaning, identify inputs, filter rows, and then determine output expressions. This is
not a claim about physical execution order.

### Worked Example

```sql
SELECT student_id, student_name
FROM student
WHERE dept_code = 'IM' AND student_id <> 'S101';
```

The result is `(S103, Kai Wu)`. Predict the rows if `AND` is changed to `OR`, and explain
which condition is true for each retained row.

### Duplicates and Expressions

SQL query results may contain duplicates:

```sql
SELECT dept_code FROM student;
SELECT DISTINCT dept_code FROM student;
```

The first result contains IM twice. The second returns DES, FIN, and IM. `DISTINCT`
applies to the complete result tuple.

```sql
SELECT course_id, credits, credits * 18 AS semester_hours
FROM course;
```

This expression calculates an output value; it does not modify stored credits.

### Multiple Inputs and Aliases

```sql
SELECT s.student_name, e.course_id, e.grade
FROM student AS s, enrollment AS e
WHERE s.student_id = e.student_id;
```

Without the matching predicate, four Student rows and six Enrollment rows produce 24
combinations. Chapter 4 replaces this older comma form with explicit `JOIN ... ON` syntax.

## 3. Patterns, Ranges, and Ordering

For `LIKE`, `%` matches zero or more characters and `_` matches exactly one character.

```sql
SELECT course_id, title
FROM course
WHERE title LIKE '%Technology%';
```

Case behavior depends on the DBMS and collation. `BETWEEN` includes both endpoints.

```sql
SELECT course_id, title, credits
FROM course
WHERE credits BETWEEN 1 AND 2
ORDER BY credits DESC, course_id ASC;
```

Without `ORDER BY`, do not rely on the displayed row order.

Practice: write one pattern for titles beginning with `Data` and another for titles whose
second character is `e`.

## 4. SQL Set Operations

Both query results must have the same number of columns with compatible types.

For DB students `{S101, S103}` and Financial Technology students `{S101, S102}`:

| Operation | Duplicate behavior | Result |
|---|---|---|
| `UNION` | Removes duplicates | S101, S102, S103 |
| `UNION ALL` | Retains all copies | S101, S101, S102, S103 |
| `INTERSECT` | Removes duplicates | S101 |
| `EXCEPT` | Left result minus right result | S103 |

Exchange the two sides of `EXCEPT` and predict the result. SQLite supports these forms
but not `INTERSECT ALL` or `EXCEPT ALL`.

## 5. `NULL` and Three-Valued Logic

`NULL` is not zero or an empty string. Most comparisons with `NULL` return `UNKNOWN`.

```sql
WHERE grade = NULL       -- incorrect test
WHERE grade IS NULL      -- correct test
```

`WHERE` retains only rows for which its predicate is `TRUE`; both `FALSE` and `UNKNOWN`
are removed.

| Expression | Result |
|---|---|
| `TRUE AND UNKNOWN` | `UNKNOWN` |
| `FALSE AND UNKNOWN` | `FALSE` |
| `TRUE OR UNKNOWN` | `TRUE` |
| `FALSE OR UNKNOWN` | `UNKNOWN` |
| `NOT UNKNOWN` | `UNKNOWN` |

### Worked Example

If one grade is temporarily set to `NULL`, `COUNT(*)` still counts that enrollment while
`COUNT(grade)` does not. The predicate `grade <> 'F'` also removes the row because its
truth value is `UNKNOWN`.

Practice: calculate `grade <> 'F'` for grades `A`, `F`, and `NULL`, and identify which
rows pass `WHERE`.

## 6. Aggregation and Grouping

`COUNT(*)` counts rows. `COUNT(attribute)` counts non-`NULL` values. `MIN`, `MAX`, `SUM`,
and `AVG` ignore `NULL` inputs.

```sql
SELECT COUNT(*) AS course_count,
       MIN(credits) AS min_credits,
       MAX(credits) AS max_credits,
       SUM(credits) AS total_credits,
       AVG(credits) AS avg_credits
FROM course;
```

For credits 3, 3, 3, and 2, the result is count 4, minimum 2, maximum 3, total 11, and
average 2.75.

### `GROUP BY`

```sql
SELECT dept_code,
       COUNT(*) AS course_count,
       AVG(credits) AS avg_credits
FROM course
GROUP BY dept_code
ORDER BY dept_code;
```

Nonaggregate output attributes should appear in `GROUP BY`. SQLite may accept additional
columns and choose an arbitrary value, but this course does not use that nonportable
behavior.

### `WHERE` and `HAVING`

`WHERE` filters rows before grouping. `HAVING` filters groups after aggregation.

```sql
SELECT dept_code, COUNT(*) AS course_count
FROM course
WHERE credits >= 3
GROUP BY dept_code
HAVING COUNT(*) >= 2;
```

The result is `(IM, 2)`. Practice: for the requirement "count only courses of at least
three credits and retain departments whose average is above 2.5," place each condition in
the correct clause and explain why.

## 7. Selected Subqueries

### `IN`

```sql
SELECT student_id, student_name
FROM student
WHERE student_id IN (
    SELECT student_id
    FROM enrollment
    WHERE course_id = 'DB201'
);
```

Run the inner query first. It returns S101 and S103; the outer query then retrieves their
names.

### `EXISTS` and Correlation

```sql
SELECT s.student_id, s.student_name
FROM student AS s
WHERE EXISTS (
    SELECT 1
    FROM enrollment AS e
    WHERE e.student_id = s.student_id
      AND e.grade IN ('A', 'A-')
);
```

The inner query refers to the current outer Student row. `EXISTS` asks only whether at
least one row exists. To find students with no enrollment, use `NOT EXISTS` with the same
identifier-matching predicate.

### `NOT IN` with `NULL`

```sql
SELECT student_id
FROM student
WHERE student_id NOT IN ('S104', NULL);
```

This returns no rows because the `NULL` comparison can make the predicate `UNKNOWN`.
A `NOT EXISTS` query with an explicit equality predicate avoids that problem. `NOT IN`
is acceptable when the schema or query guarantees that the comparison set cannot contain
`NULL`; state that guarantee rather than memorizing an unconditional ban.

### Common Table Expression

```sql
WITH counts AS (
    SELECT course_id, COUNT(*) AS enrollment_count
    FROM enrollment
    GROUP BY course_id
)
SELECT course_id, enrollment_count
FROM counts
WHERE enrollment_count >= 2;
```

A CTE names a query result for the current statement. It does not imply that the DBMS
must store a temporary table.

Subqueries in `FROM`, scalar subqueries, `SOME`, `ALL`, `UNIQUE`, `LATERAL`, and formal
multiset algebra are extensions unless separately taught and practiced.

## 8. Data Modification

Before modifying data, identify the target relation, affected rows, and possible key,
reference, `NOT NULL`, or `CHECK` violations.

```sql
INSERT INTO student (student_id, email, student_name, dept_code)
VALUES ('S105', 'noah.lee@example.edu', 'Noah Lee', 'IM');

UPDATE student
SET dept_code = 'FIN'
WHERE student_id = 'S105';

DELETE FROM student
WHERE student_id = 'S105';
```

The department must exist before insertion. An `UPDATE` or `DELETE` without the intended
`WHERE` clause may affect every row or violate references. Use a `SELECT` with the same
predicate to verify target rows first. The lab uses a savepoint and restores its sample
changes.

Practice: predict how many rows `UPDATE course SET credits = 4` changes. Then add a
predicate that targets only DB201 and verify it with `SELECT`.

## Common Errors

1. Expecting `SELECT` to remove duplicates automatically.
2. Omitting a matching predicate between relations.
3. Relying on row order without `ORDER BY`.
4. Using `= NULL` or `<> NULL`.
5. Confusing row filtering in `WHERE` with group filtering in `HAVING`.
6. Selecting a nonaggregate column that is not a grouping column.
7. Using `NOT IN` without checking whether the comparison set can contain `NULL`.
8. Running an `UPDATE` or `DELETE` before verifying its target rows.
9. Treating a SQLite-specific behavior as an SQL standard rule.

## Classroom and Individual Evidence

Retain:

1. Predictions and actual results for `student_lab.sql`.
2. One `NULL` error and its correction.
3. One grouped query with the role of `WHERE`, grouping, `HAVING`, and `SELECT` labeled.
4. One subquery with separately verified inner and outer results.
5. One modification completed and reversed inside a savepoint.

When comparing solutions, judge the requested result, `NULL` handling, valid grouping,
and evidence from sample data. Peer ranking does not directly determine a grade; the
individual corrected work is the retained evidence.

## Chapter Summary

DDL defines structure and constraints; DML reads or modifies rows. SQL retains duplicates
unless instructed otherwise. `NULL` introduces `UNKNOWN`, and `WHERE` retains only
`TRUE`. Aggregation forms and filters groups in distinct stages. Subqueries should be
checked from the inside out, and every modification should be preceded by a target-row
and constraint check. Chapter 4 introduces explicit joins, views, constraints, and basic
transaction statements.

## After-Class Continuation

Write one additional grouped query and one additional subquery using the course schema.
Before execution, predict the retained rows and possible effect of `NULL`; afterward,
record the result and correct any difference between the prediction and observation.
