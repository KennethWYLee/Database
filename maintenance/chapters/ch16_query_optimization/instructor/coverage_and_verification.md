# Chapter 16 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: draft, source-checked against the complete Chapter 16 text and
  official Chapter 16 slides
- Case: original student/enrollment/course optimizer workload and skewed events
- Executable verification: passed again on August 27, 2026, using Python 3.12.9 and
  SQLite 3.45.3
- Publication: not approved

## Source scope checked

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 16, printed pages 743-788, Sections 16.1-16.7. Exercises and further reading
  were inspected for context but not copied.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch16.pdf`, all 85 PDF
  pages.
- Current governance, revised syllabus, chapter-material prompt, completed Chapter 15
  material, and SQLite 3.45.3 statistics/plan behavior.

## Scope decision

Required instruction covers result equivalence before performance comparison; catalog
tuple/distinct/index statistics; a basic equality-selectivity estimate and its uniform
assumption; `ANALYZE`; and practical `EXPLAIN QUERY PLAN` interpretation.

Selection/projection pushdown, join reorder and Cartesian-product risk, outer-join
counterexamples, and detailed skew analysis remain source-checked after-class extensions.

Complete cost formulas, equivalent-plan enumeration, dynamic programming, optimizer
implementation, nested-query decorrelation, materialized views, top-K, join
minimization, update optimization, multiquery optimization, parametric plans, and
adaptive processing are supplementary.

## Source and implementation cautions

1. Equivalence is over every legal database instance; equal sample results are not a
   standalone proof.
2. SQL multiset semantics require duplicate counts to be preserved, not only distinct
   tuples.
3. Selection/projection pushdown is an equivalence under stated conditions, not a
   guarantee of lower cost.
4. Outer joins are not freely associative/commutative. Moving a right-side condition
   from `WHERE` to `ON` can preserve unmatched rows and change results.
5. Statistics may be sampled, approximate, or stale. The lab's `sqlite_stat1` average
   does not encode the displayed value skew.
6. SQLite's compact plan does not show estimated/actual rows, cost units, buffer hits,
   or complete physical operator details.
7. SQLite may flatten the explicit pushdown subqueries. Identical plans support that
   observed optimizer behavior, not a universal DBMS guarantee.
8. RARE and COMMON plans are captured but the guide does not label either plan
   universally optimal; the SQLite build lacks evidence required for that claim.

## Teaching-point alignment

| ID | Teaching point | Primary source | Worked example | Student action and feedback |
|---|---|---|---|---|
| C16.01 | optimizer alternatives/cost | 16.1, pp. 743-747; slides 16.3-16.6 | two three-table orders | list semantic conditions |
| C16.02 | expression equivalence | 16.2, pp. 747-748 | selection cascade | compare results and plans |
| C16.03 | selection pushdown (supplementary) | 16.2.1-16.2.2, pp. 748-754; slides 16.8-16.15 | student/course filters | reject unconditional early-filter rule |
| C16.04 | projection pushdown (supplementary) | 16.2.1-16.2.2, pp. 749, 754 | retain join/filter columns | find failure after removing key |
| C16.05 | join order/product risk (supplementary) | 16.2.3, pp. 754-755; slides 16.16-16.18 | 100 students to 500 enrollments | classify A-B-C orders |
| C16.06 | outer-join boundary (supplementary) | 16.2.1, pp. 750-752; slides 16.11-16.14 | Department 101 NULL row | execute WHERE/ON counterexample |
| C16.07 | catalog/statistics | 16.3.1, pp. 758-760; slides 16.36-16.42 | `ANALYZE` and `sqlite_stat1` | identify missing skew detail |
| C16.08 | basic selectivity; skew as extension | 16.3.2, pp. 760-762; slides 16.43-16.47 | 99/1 event distribution | calculate actual selectivity |
| C16.09 | plan choice/evidence | 16.4, pp. 766-774; slides 16.22-16.35 | flattened equivalent SQL plans | explain plan and missing actuals |

Every classroom-core point and retained supplementary point in the table has an
explanation, a complete example, student practice, and a stated checking or feedback
criterion.

## Teaching summary

After the Chapter 15 plan examples, students establish result equivalence, inspect
`sqlite_stat1`, calculate a basic equality-selectivity estimate, compare plans, and
revise one unsupported performance claim. Rewrite rules, the outer-join counterexample,
and detailed skew analysis remain after-class extensions.

## Verification command

```powershell
py -3 maintenance/chapters/ch16_query_optimization/instructor/verify_ch16.py
```

## Remaining limits before student release

- The instructor selected English-only student prose on August 27, 2026. The rewritten
  and reduced guide still requires final instructor content and language review before
  publication.
- SQLite 3 is the course DBMS; these materials are verified with SQLite 3.45.3.
- SQLite does not expose the richer estimated/actual evidence available in some server
  DBMSs; the course does not require those product-specific plan fields.
- The combined Chapter 15/16 classroom workload has not been observed with students.

## Chapter delivery status

- Files created: student guide, SQL lab, instructor source/alignment record, and
  verifier.
- Source verification: complete for textbook printed pages 743-788 and all 85 pages
  of the local official slide PDF.
- Executed content: deterministic four-relation data; equivalent base/pushdown
  results; equivalent access-path sequences; selected join indexes; outer-join
  counterexample; `sqlite_stat1`; skewed actual counts; RARE/COMMON plan capture;
  and all foreign keys.
- Unexecuted content: all excluded optimizer algorithms and materialized views.
- Progression decision: the chapter meets the source, equivalence, counterexample,
  statistics, plan-evidence, practice, and executable-check conditions required to
  begin Chapter 17. It remains a draft until the instructor reviews language and
  classroom workload.
