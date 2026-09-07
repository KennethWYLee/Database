# Chapter 5: Advanced SQL

## Core Question

How can SQL rank rows without grouping them away, traverse a hierarchy of unknown depth,
and record an automatic audit action when data changes?

## Connection to Chapter 4

Chapter 4 used declarative constraints and transactions. This chapter adds selected
database programming and advanced query features:

- window functions calculate across related rows while retaining detail rows;
- recursive CTEs reuse prior results until no new result is produced;
- triggers respond automatically to a specified data-change event;
- stored routines are introduced only through purpose and interface.

Use a declarative key, foreign key, or `CHECK` when it directly expresses the rule. Do not
replace a visible constraint with a trigger merely because a trigger is automatic.

## Teaching Summary

| Topic | Worked example and practice | Evidence to retain |
|---|---|---|
| Routines and triggers | Routine contract and row-level audit | Contract plus before/after rows |
| Recursive CTEs | Prerequisite graph traversal | Rows produced in each round |
| Ranking functions | Scores with ties | Predicted and observed ranks |
| Window frames | Running values within a partition | Frame definition and checked output |

## Prerequisites and Setup

You should be able to use subqueries, CTEs, aggregates, views, transactions, and
constraints. Run the Chapter 2 setup and then `student_lab.sql`.

SQLite 3.45.3 supports the supplied triggers, recursive CTEs, and window functions. It
does not install stored functions or procedures through SQL statements. Therefore
`standard_routine_examples.sql` is a source-checked reference, not executed SQLite code.

## Learning Objectives

After completing this chapter, you should be able to:

1. Interpret `RANK`, `DENSE_RANK`, and `ROW_NUMBER` when ties occur.
2. Use `PARTITION BY` and an explicit window frame.
3. Separate a recursive CTE into base and recursive terms and trace new rows by round.
4. Explain how duplicates, cycles, and state columns affect termination.
5. Explain a row-level audit trigger through its event, condition, action, `OLD`, and
   `NEW` values.
6. Distinguish a function, procedure, and trigger by invocation and result.

Complete procedural SQL, external routines, statement-level triggers, product-specific
`PIVOT`, `ROLLUP`, `CUBE`, JDBC, Python database APIs, ODBC, and embedded SQL are
extensions.

## 1. Functions, Procedures, and Triggers

| Mechanism | Invocation | Main result |
|---|---|---|
| Function | Used in an expression or product-specific call | Returns a scalar or table value |
| Procedure | Explicit product-specific call | Performs statements and may expose outputs |
| Trigger | Automatic response to a table event | Performs a predefined action |

### Function Contract Example

A function that receives a course identifier and returns enrollment count has this
logical contract:

```sql
SELECT COUNT(*)
FROM enrollment
WHERE course_id = :p_course_id;
```

DB201 and FT210 return 2; ML230 and WD120 return 1. The lab verifies these data results
with an equivalent query. It does not prove that a stored function was installed.

Practice: define the input, return type, and equivalent query for
`department_course_count`. IM should return 2, FIN and DES 1, and a missing department 0.

### Procedure Contract Example

A procedure may accept a course identifier and new credits, then perform:

```sql
UPDATE course
SET credits = :p_credits
WHERE course_id = :p_course_id;
```

The interface must also define what happens if no course exists: error, returned status,
or allowed no-op. Schema constraints should still reject invalid credits instead of
hiding all validation in the procedure.

## 2. Row-Level Audit Trigger

A trigger design identifies its event, timing, row or statement level, condition, and
action. The supplied SQLite trigger records a grade change:

```sql
CREATE TRIGGER enrollment_grade_audit
AFTER UPDATE OF grade ON enrollment
FOR EACH ROW
WHEN OLD.grade IS NOT NEW.grade
BEGIN
    INSERT INTO enrollment_audit (
        action_name, student_id, course_id, term, old_grade, new_grade
    ) VALUES (
        'GRADE_UPDATE', NEW.student_id, NEW.course_id, NEW.term,
        OLD.grade, NEW.grade
    );
END;
```

Changing S103/DB201 from B to B+ records old value B and new value B+. SQLite `IS NOT`
performs a null-safe difference test. `OLD.grade <> NEW.grade` could become `UNKNOWN`
when one side is `NULL` and miss a real change.

The audit insert is in the same transaction as the original update. Rolling back the
grade change also removes its audit row.

### Practice

Design an enrollment-delete audit. A delete has an `OLD` row but no `NEW` row. Inside a
savepoint, delete one enrollment, confirm exactly one correct audit row, and roll back.

### When Not to Use a Trigger

Use a foreign key for an enrollment-to-course reference and a `CHECK` for a priority
range. A trigger is appropriate for audit history because the old and new transition
values must be recorded. Hidden trigger chains and unexpected side effects must be tested.

## 3. Recursive CTEs

The prerequisite data is:

```text
DB201 <- WD120
FT210 <- DB201
ML230 <- DB201
```

The right side is a prerequisite of the left side.

```sql
WITH RECURSIVE all_prereq(course_id, prereq_id) AS (
    SELECT course_id, prereq_id
    FROM course_prerequisite

    UNION

    SELECT ap.course_id, cp.prereq_id
    FROM all_prereq AS ap
    JOIN course_prerequisite AS cp
      ON cp.course_id = ap.prereq_id
)
SELECT course_id, prereq_id
FROM all_prereq;
```

The base term returns direct prerequisite pairs. The recursive term follows one more
edge. The first recursive round adds FT210/WD120 and ML230/WD120. The next round adds no
new pair, so the fixed point contains five pairs.

### Predict and Check

Trace FT210 only. DB201 has depth 1 and WD120 depth 2. Run the base term by itself before
running the full query. If the direction is reversed, the query answers which courses
depend on FT210, which is a different question.

### Cycles and Termination

`UNION` removes duplicate complete rows. `UNION ALL` retains them and may continue
indefinitely on a cycle without a guard. Even `UNION` may not stop a depth query if each
round creates a new depth value, because the complete row is different.

Possible controls include prohibiting cycles, retaining and checking a visited path, or
using a requirement-based maximum depth. A maximum depth limits output but does not prove
that the graph is acyclic.

## 4. Ranking Functions

The best scores are S101=92, S102=92, S103=84, and S104=84.

```sql
WITH best_score AS (
    SELECT student_id, MAX(score) AS best_score
    FROM sql_practice_score
    GROUP BY student_id
)
SELECT student_id,
       best_score,
       RANK() OVER (ORDER BY best_score DESC) AS score_rank,
       DENSE_RANK() OVER (ORDER BY best_score DESC) AS dense_score_rank,
       ROW_NUMBER() OVER (
           ORDER BY best_score DESC, student_id
       ) AS display_row
FROM best_score;
```

| Student | Score | `RANK` | `DENSE_RANK` | `ROW_NUMBER` |
|---|---:|---:|---:|---:|
| S101 | 92 | 1 | 1 | 1 |
| S102 | 92 | 1 | 1 | 2 |
| S103 | 84 | 3 | 2 | 3 |
| S104 | 84 | 3 | 2 | 4 |

`RANK` leaves a gap after a tie. `DENSE_RANK` does not. `ROW_NUMBER` assigns a unique
number to every row; the additional student identifier makes the order deterministic.

Practice: change S103 to 92 and predict all three numberings before executing the query.

## 5. Partitions and Window Frames

`PARTITION BY` restarts a window calculation for each group without collapsing detail
rows. `ORDER BY` defines sequence inside the partition, and the frame identifies the rows
used for the current calculation.

```sql
SELECT student_id,
       attempt_no,
       score,
       ROUND(
           AVG(score) OVER (
               PARTITION BY student_id
               ORDER BY attempt_no
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ),
           1
       ) AS running_average
FROM sql_practice_score;
```

S101 has running averages 78 and 85. Unlike `GROUP BY`, the result retains each attempt.

Practice: change the frame to
`ROWS BETWEEN 1 PRECEDING AND CURRENT ROW`, add a third attempt, and compare the moving
two-row average with the running average. State the frame explicitly rather than relying
on a DBMS default.

## 6. Short Extension: Conditional Aggregation

```sql
SELECT student_id,
       MAX(CASE WHEN attempt_no = 1 THEN score END) AS attempt_1,
       MAX(CASE WHEN attempt_no = 2 THEN score END) AS attempt_2
FROM sql_practice_score
GROUP BY student_id
ORDER BY student_id;
```

This fixed cross-tab does not add a new result column when attempt 3 appears. Dynamic
categories require application code or product-specific dynamic pivot features.

## Common Errors

1. Reporting reference routine code as executed SQLite code.
2. Omitting the input, output, or invocation contract of a routine.
3. Comparing nullable transition values with a non-null-safe operator.
4. Reimplementing a declarative constraint with a trigger.
5. Reversing a recursive edge.
6. Using `UNION ALL` on a cyclic graph without a guard.
7. Treating `ROW_NUMBER` as a tie-aware rank.
8. Assuming a window's internal order is the final display order.
9. Omitting a window frame while assuming running-row behavior.

## Classroom and Individual Evidence

Review three proposed solutions: a trigger that reimplements a foreign key, a recursive
CTE without a termination explanation, and a ranking that treats `ROW_NUMBER` as rank.
Judge mechanism fit, termination, tie handling, deterministic order, and execution claims.

Retain the routine contract, trigger before/after evidence, recursive rounds, ranking
prediction, window-frame result, and individually corrected solution.

## Chapter Summary

Functions return values, procedures perform explicitly requested work, and triggers run
after a specified database event. Recursive CTEs require a correct direction and a
termination argument. Ranking functions differ in tie handling, while partitions and
frames define the rows used by a window calculation. Chapter 6 returns to database
design and business rules.

## After-Class Continuation

Choose one recursive CTE or window query and vary one condition, edge, ordering column,
or frame boundary. Predict the effect first, run the revised query, and explain the result
without generalizing beyond the tested data and DBMS.
