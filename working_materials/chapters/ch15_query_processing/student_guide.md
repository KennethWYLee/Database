# Chapter 15: Query Processing

## Core Question

SQL states what result is required. How does a DBMS turn that request into work that can
actually run, and what evidence can we use to explain the chosen access path?

Use this guide with `student_lab.sql`.

Chapter 15 and Chapter 16 share one class meeting. The classroom core is deliberately
limited to reading query plans, distinguishing `SCAN` from `SEARCH`, recognizing join
order, and checking that two plans return the same result. Complete join algorithms,
materialization, pipelining, and I/O cost formulas are extensions.

## Connection to Other Chapters

Chapter 14 introduced indexes as access paths. This chapter shows how scans, index
searches, and joins appear in an executable plan. Chapter 16 then explains how an
optimizer uses statistics to choose among valid plans.

An unused index is not necessarily broken. The optimizer may estimate that another plan
will require less work.

## Prerequisites

- Explain the logical result of selection, projection, and an inner join.
- Write a basic query with `WHERE` and a join predicate.
- Recognize `SCAN`, `SEARCH`, and an index name in SQLite `EXPLAIN QUERY PLAN` output.

## Learning Objectives

After completing the classroom core, you should be able to:

1. Relate parsing, optimization, and evaluation in the query-processing workflow.
2. Distinguish a logical operation from a physical operator and an execution plan.
3. Identify a table scan, index search, and join order in a SQLite query plan.
4. Compare two plans only after confirming that their query results are equal.
5. State what a compact query plan does and does not prove.

## Teaching Summary

| Classroom topic | Worked evidence | Evidence to retain |
|---|---|---|
| SQL to execution plan | One selection before and after an index | SQL, result, and both plans |
| `SCAN` versus `SEARCH` | Title lookup in `ch15_course` | Access method and index name |
| Join order | Department-to-course lookup | Ordered plan explanation |
| Limits of plan evidence | Estimated plan versus observed result | One supported and one unsupported claim |

## 1. From SQL to Execution

A useful high-level workflow has three parts:

1. **Parsing and translation:** check syntax and names, then create an internal logical
   representation.
2. **Optimization:** compare valid alternatives and select an estimated low-cost plan.
3. **Evaluation:** execute the selected physical operators and produce the result.

Implementations differ across DBMS products, but this distinction prevents several
common mistakes. A misspelled column is a parsing problem. A legal query that uses a
table scan reflects an optimizer choice. Reading pages and producing rows are evaluation
work.

### Worked Example

```sql
SELECT course_id, title
FROM ch15_course
WHERE title = 'Course 04999';
```

The logical request is a selection followed by a projection. The SQL does not require a
particular index or join algorithm. The optimizer may choose a table scan or a title-index
search, and the execution engine performs that choice.

### Predict Before Checking

For each event, identify the stage most directly involved:

1. `course_idd` is not a valid column.
2. The query is valid, but the planner chooses a scan.
3. The DBMS reads rows and returns two columns.

### Interpretation

The answers are parsing/translation, optimization, and evaluation. Do not describe a
syntax error as an index failure.

## 2. Logical Operation, Physical Operator, and Plan

A logical operation describes the required relation. A physical operator describes how
the DBMS performs that work. A query-execution plan combines physical operators, access
paths, and their order.

The same logical selection can have different physical plans:

```text
Plan A: SCAN ch15_course -> test every title -> project two columns
Plan B: SEARCH the title index -> fetch matching row -> project two columns
```

The two plans are alternatives only if they return the same rows with the same duplicate
behavior. Their difference is physical work, not SQL meaning.

### Lab Activity

Before running the lab, predict the access method in Phase 1 and Phase 2. Then execute
both phases and record:

- `SCAN` or `SEARCH`;
- the index name, if present;
- the predicate shown by the plan;
- the query result.

### Expected Interpretation

With the verified SQLite 3.45.3 environment, Phase 1 scans `ch15_course`. After the title
index is created, Phase 2 searches that index. The result remains
`C04999, Course 04999`.

If another SQLite version prints different wording, retain the complete plan and version.
Judge the access method from the actual output instead of editing it to match this guide.

## 3. `SCAN` and `SEARCH`

A table scan examines rows from the relation and can evaluate a general condition. An
index search uses an indexed predicate to narrow the access path. An index is most likely
to help when relatively few rows match, but index presence alone does not prove that an
index is faster.

### Worked Comparison

The lab contains 5,000 courses. A title predicate matches one row:

```sql
SELECT course_id, title
FROM ch15_course
WHERE title = 'Course 04999';
```

Without the title index, the plan reports a scan. After
`ch15_idx_course_title(title)` is created and statistics are available, the plan reports
an index search.

The predicate `credits = 3` matches 1,000 of 5,000 rows. That proportion alone does not
select the best plan. Projection width, row placement, cache state, and optimizer
estimates may also matter.

### Practice

1. Retain the before-and-after plans for the title query.
2. Confirm that both phases return the same result.
3. Calculate the matching proportion for `credits = 3`.
4. Write a hypothesis about scan or index use, followed by the plan evidence still needed.

### Check Criteria

The title query must change from a scan to a search in the verified environment without
changing its result. The credits answer must remain a testable hypothesis, not an
unqualified claim that an index will be faster.

## 4. Reading a Join Plan

For a nested-loop-style plan, one input is accessed first. Matching rows then drive access
to the next input. An index on the inner lookup key can avoid repeatedly scanning the
inner relation.

### Worked Example

```sql
SELECT c.course_id, c.title
FROM ch15_department AS d
JOIN ch15_course AS c ON c.dept_id = d.dept_id
WHERE d.dept_name = 'Department 042';
```

Phase 2 creates these indexes:

```sql
CREATE UNIQUE INDEX ch15_idx_department_name
ON ch15_department(dept_name);

CREATE INDEX ch15_idx_course_dept
ON ch15_course(dept_id);
```

The plan first searches for one department by name, then searches the course index by
that department identifier. The first small result drives the second lookup.

### Predict and Run

Before execution, predict which table should appear first in the indexed plan. Run both
phases and write the access order exactly as shown. Then remove the department-name
filter conceptually and decide whether the same order is still guaranteed to be best.

### Interpretation

The verified indexed plan has two `SEARCH` operations: department name first, course
department identifier second. Removing the selective filter changes the expected input
size, so the earlier conclusion cannot be reused without new statistics and a new plan.

## 5. Evidence and Limits

An optimizer normally compares estimated resource use, not a guaranteed wall-clock
time. Estimates may include row counts, storage access, CPU work, memory, and intermediate
results. Elapsed time also depends on cache state, concurrent load, storage, and the OS.

Before claiming that one plan is better, retain:

- the SQL and schema;
- row counts and relevant indexes;
- the DBMS version and statistics state;
- both query results;
- both plans;
- repeated measurements if elapsed time is discussed.

SQLite `EXPLAIN QUERY PLAN` does not report every internal cost, actual row count, buffer
read, or memory allocation. A plan can support a claim about its displayed access path,
but not every detail of runtime behavior.

## Extension: Additional Processing Concepts

These topics support further study but are not part of the Exam 3 classroom core.

- **Materialization:** store an intermediate result before the next operator reads it.
- **Pipelining:** pass rows directly from one operator to the next when possible.
- **Blocking work:** sorting may need many or all input rows before output can continue.
- **Additional join algorithms:** block nested-loop, merge join, and hash join.
- **Detailed cost models:** page-level I/O formulas and operator-specific estimates.

If a plan reports a temporary B-tree for `ORDER BY`, it supports the conclusion that this
plan performs separate sorting work. It does not reveal every buffering or disk detail.

## Common Errors

1. Treating SQL text order as the physical execution order.
2. Assuming that a logical join has only one physical implementation.
3. Claiming that an existing index must be used.
4. Comparing time without checking equal results and plans.
5. Treating estimated rows as measured rows.
6. Applying SQLite plan labels to every DBMS.
7. Calling nested loops slow without considering outer rows and inner access.

## Discussion and Individual Evidence

Compare two anonymous plans for the same SQL. First decide whether the results are
equivalent. Then explain the access methods, order, indexes, and temporary work. End with
one statement that the plan does not support.

Retain your SQL, data counts, before-and-after plans, result-equality check, line-by-line
plan explanation, and one corrected overclaim.

## Chapter Summary

Query processing turns a logical request into a physical plan. The classroom core is to
recognize scans, index searches, and join order while preserving result equivalence.
Plan evidence supports bounded conclusions; it does not make an index universally faster
or expose every runtime detail. Chapter 16 adds statistics and selectivity to this
reasoning.

## After-Class Continuation

For two queries of your choice, retain the schema, row counts, plan, and result check.
Read about complete join algorithms, materialization, pipelining, and I/O cost formulas as
extensions; they are not required derivations for the selected Chapter 15 assessment.
