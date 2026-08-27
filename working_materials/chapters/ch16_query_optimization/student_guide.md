# Chapter 16: Query Optimization

## Core Question

How does a query optimizer use statistics to choose an estimated low-cost plan without
changing the meaning of the SQL query?

Use this guide with `student_lab.sql`.

Chapter 15 and Chapter 16 share one class meeting. The classroom core is limited to
result equivalence, basic selectivity, catalog statistics, `ANALYZE`, and plan comparison.
Formal rewrite systems, detailed join enumeration, skew analysis, and optimizer
implementation are extensions.

## Connection to Chapter 15

Chapter 15 distinguished a logical expression from a physical plan and introduced scans,
index searches, and join order. This chapter explains how statistics help an optimizer
estimate alternatives. A cost estimate is a decision input, not a measurement of actual
runtime.

## Prerequisites

- Confirm whether two queries return the same rows and duplicate counts on sample data.
- Read selections and inner or outer joins.
- Identify scans, index searches, and access order in a Chapter 15 query plan.

## Learning Objectives

After completing the classroom core, you should be able to:

1. Explain why result equivalence must be checked before performance comparison.
2. Describe how row counts, distinct values, and indexes support cost estimation.
3. Calculate a basic equality-selectivity estimate and state its assumptions.
4. Run `ANALYZE` and interpret bounded evidence from `EXPLAIN QUERY PLAN`.
5. Compare equivalent query results and plans without claiming more than the evidence
   supports.

## Teaching Summary

| Classroom topic | Worked evidence | Evidence to retain |
|---|---|---|
| Equivalence before optimization | Base and rewritten query | Bidirectional difference check |
| Statistics and selectivity | Event-type distribution | Estimated and actual row counts |
| `ANALYZE` and plan choice | SQLite statistics and plans | Statistics snapshot and plan |
| Evidence limits | Estimated versus actual behavior | One bounded conclusion |

## 1. What an Optimizer Does

An optimizer may consider logically equivalent expressions, physical access paths, and
join orders. It uses available statistics to estimate their cost and selects one plan.
The estimated lowest-cost plan is not guaranteed to be the fastest in every execution,
because statistics and modeling assumptions may be incomplete or stale.

### Worked Example

For a query joining Student, Enrollment, and Course, the optimizer may consider different
join orders and choose a scan or search for each input. These choices are acceptable only
if the resulting query preserves join predicates, duplicate behavior, `NULL` behavior,
and required output columns.

### Predict Before Checking

Before comparing plans for two SQL statements, list the properties that must remain the
same. Include the result columns, row values, duplicate counts, join types, and filters.

### Interpretation

Formatting two statements differently does not establish a useful optimization. Equal
results on one data set are necessary evidence, but they do not prove equivalence for all
legal future data.

## 2. Result Equivalence as a Guardrail

Two relational expressions are equivalent when they produce the same result for every
legal database instance. SQL usually preserves duplicates, so duplicate counts also
matter. Constraints, `NULL`, and outer joins can make an apparently simple rewrite
incorrect.

### Lab Activity

Compare the lab's `BASE QUERY` and `PUSHDOWN QUERY`:

1. Predict whether they should return the same result.
2. Run both queries.
3. Use bidirectional `EXCEPT` checks and row counts.
4. Compare the two query plans only after the result checks pass.

### Expected Interpretation

In the supplied data, both difference counts are zero and the row counts match. SQLite
may flatten the subqueries and show the same physical plan. This supports equality for
the tested data and demonstrates the observed optimizer behavior. It does not prove that
every arbitrary subquery can be removed safely.

SQLite's `EXCEPT` removes duplicate result rows. Therefore, bidirectional `EXCEPT` plus
one total row count is not a general proof that duplicate multiplicities match. When
duplicates are possible, compare grouped `COUNT(*)` values over all result columns or use
another verified comparison that preserves multiplicity.

## 3. Statistics and Selectivity

Optimizers commonly use relation row or page counts, tuple width, distinct-value counts,
index properties, and value-distribution information. Statistics may be sampled or
periodically updated, so they can become stale.

Without value-frequency information, a simple equality estimate may use a uniform
distribution assumption:

```text
estimated rows = total rows / number of distinct values
selectivity = estimated rows / total rows
```

This is an approximation, not a law about the data.

### Worked Example

An Event table has 10,000 rows and two distinct event types. A uniform estimate predicts
5,000 rows for either type. The actual counts are:

```text
COMMON: 9,900
RARE:      100
```

The estimate is wrong in opposite directions for the two values. The actual selectivity
is 99% for `COMMON` and 1% for `RARE`.

### Predict and Check

Before examining a plan, predict which value is more likely to benefit from a secondary
index lookup. Then state why the selectivity percentage still does not guarantee the
chosen plan.

### Interpretation

`RARE` is more likely to benefit because it returns fewer rows. The final choice may also
depend on whether the index covers the query, row placement, cache state, and the
optimizer's available statistics.

## 4. `ANALYZE` and Plan Evidence

SQLite `ANALYZE` records planner statistics. In this lab, selected values can be viewed
through `sqlite_stat1`:

```sql
ANALYZE;
SELECT tbl, idx, stat
FROM sqlite_stat1
ORDER BY tbl, idx;
```

SQLite's statistics format is product-specific and more compact than a full textbook
catalog. Do not treat one `stat` string as a standard format for every DBMS.

### Lab Activity

1. Record the DBMS version, schema, indexes, and row counts.
2. Run `ANALYZE` and retain the relevant statistics rows.
3. Run the base and rewritten queries.
4. Confirm equal results.
5. Explain the access order, `SCAN` or `SEARCH`, and index names shown by each plan.
6. Identify one piece of actual execution information that the compact plan omits.

### Check Criteria

A complete answer separates observed facts from inference. Examples of omitted data
include actual rows per operator, elapsed time, buffer reads, and memory use.

## 5. A Practical Optimization Record

For a defensible comparison, retain this sequence:

1. SQL, schema, indexes, row counts, and DBMS version.
2. Evidence that the query results are equal.
3. Statistics state, including whether `ANALYZE` was run.
4. Both query plans.
5. A conclusion limited to the tested data and environment.

An optimizer estimate can guide a plan choice, but it is not an actual measurement. If
elapsed time matters, repeat the measurement under controlled conditions and keep the
plans and results with the timings.

## Extensions: Rewrite Rules and Optimizer Internals

The following topics remain available for after-class reading but are not part of the
Exam 3 classroom core:

- selection and projection pushdown rules;
- detailed join reordering and Cartesian-product avoidance;
- outer-join rewrite counterexamples;
- histogram and frequent-value handling for skew;
- complete cost formulas and dynamic-programming plan enumeration;
- optimizer implementation details.

One important warning is still required: moving a right-side condition between `ON` and
`WHERE` in a left outer join can change unmatched rows because `NULL` comparisons become
`UNKNOWN`. Never apply an inner-join rewrite rule to an outer join without checking its
semantics.

### Extension Counterexample

```sql
-- Filter after the left join
FROM department AS d
LEFT JOIN student AS s ON s.dept_id = d.dept_id
WHERE s.student_id < 3

-- Filter as part of the join condition
FROM department AS d
LEFT JOIN student AS s
  ON s.dept_id = d.dept_id AND s.student_id < 3
```

A department with no student is removed by the first form and retained with a `NULL`
student by the second. This is a semantic difference, not a performance detail.

## Common Errors

1. Declaring universal equivalence from one sample result.
2. Comparing plans before checking result equality.
3. Treating estimated rows as actual rows.
4. Assuming statistics remain current after major data changes.
5. Treating low selectivity as a guarantee that an index will be used.
6. Claiming that SQL formatting changes the physical algorithm.
7. Applying an inner-join rewrite to an outer join without a counterexample check.

## Discussion and Individual Evidence

Compare a base query and a proposed rewrite. First support or reject result equivalence.
Then inspect statistics and plans. Finish with one conclusion the evidence supports and
one conclusion it does not support.

Retain the original and rewritten SQL, bidirectional difference check, statistics
snapshot, both plans, actual counts, and one unsafe-rewrite counterexample.

## Chapter Summary

Query optimization begins with meaning, then uses statistics to estimate alternatives.
The classroom core is to verify equal results, calculate simple selectivity, inspect
statistics, and interpret plans conservatively. Formal rewrite systems, skew handling,
and optimizer implementation remain extensions. Chapter 17 moves from one query plan to
transactions and concurrent schedules.

## After-Class Continuation

Create a four-part record for one query: equivalence, statistics, plan, and limitations.
Read the detailed rewrite and optimizer topics as extensions; they are not required
derivations for the selected Chapter 16 assessment.
