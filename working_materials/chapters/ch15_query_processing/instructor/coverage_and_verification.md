# Chapter 15 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: draft, source-checked against the complete Chapter 15 text and
  official Chapter 15 slides
- Case: original 100-department, 5,000-course SQLite workload
- Executable verification: passed again on August 27, 2026, using Python 3.12.9 and
  SQLite 3.45.3
- Publication: not approved

## Source scope checked

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 15, printed pages 689-735, Sections 15.1-15.9. Exercises and further reading
  were inspected for context but not copied.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch15.pdf`, slides
  15.1-15.74.
- Current governance, revised syllabus, chapter-material prompt, Chapters 2-7 and 14
  materials, and SQLite 3.45.3 plan behavior.

## Scope decision

Required instruction covers parsing/translation, optimization, and evaluation; logical
versus physical operations; query-execution plans; basic cost meaning; file and index
scans; join order; nested-loop and indexed nested-loop concepts; a short conceptual
comparison to merge/hash joins; and materialization versus pipelining.

Complete external sorting, selection variants A1-A10, block-transfer/seek formulas,
complete block/merge/hash/spatial join algorithms, duplicate/set/aggregation operator
algorithms, iterator implementation, continuous streams, cache-conscious processing,
query compilation, and column-store internals are supplementary.

## Source and implementation cautions

1. SQL specifies results, not a mandatory physical plan.
2. Query cost is an estimate of resources; actual response time depends on cache,
   concurrency, storage, memory, and implementation.
3. A secondary index can be worse than a scan when many scattered records match.
4. SQLite automatic indexes are disabled so the lab's before/after access paths remain
   attributable to the maintained DDL.
5. The indexed join plan is a practical nested-loop interpretation of SQLite's plan;
   the compact output does not expose every internal buffer or I/O operation.
6. A plan line reporting a temporary B-tree supports the conclusion that this plan
   performs extra ordering work, not a precise byte count or disk-write claim.
7. Materialization and pipelining are textbook concepts; the compact SQLite plan does
   not expose every pipeline edge.

## Teaching-point alignment

| ID | Teaching point | Primary source | Worked example | Student action and feedback |
|---|---|---|---|---|
| C15.01 | processing steps | 15.1, pp. 689-692; slides 15.3-15.5 | title lookup through three steps | assign syntax/plan/read events |
| C15.02 | logical vs physical plan | 15.1, pp. 690-691 | scan and index plans | annotate actual plan terms |
| C15.03 | cost meaning and limits | 15.2, pp. 692-695; slides 15.6-15.8 | one-row versus many-row selection | critique two timing runs |
| C15.04 | file/index scan | 15.3.1-15.3.2, pp. 695-699; slides 15.9-15.17 | course title before/after index | compare plans and credits selectivity |
| C15.05 | nested/indexed nested-loop | 15.5.1-15.5.3, pp. 704-708; slides 15.28-15.33 | department-course join | identify outer/inner access |
| C15.06 | join alternatives (supplementary) | 15.5.4-15.5.5, pp. 708-718; slides 15.34-15.55 | merge/hash conceptual contrast | state applicable equality/order inputs |
| C15.07 | join order/cardinality | 15.1, 15.5, pp. 690-691, 704-708 | unique department then 50 courses | revise after credits predicate |
| C15.08 | materialization/pipelining (supplementary) | 15.7.1-15.7.2, pp. 724-730; slides 15.58-15.65 | filter-join-project flow | identify ORDER BY blocking work |

Every required teaching point has explanation, a complete example, student practice,
and a stated checking or feedback criterion.

## Teaching summary

The shared Chapter 15-16 class begins with one SQL query and distinguishes its logical
meaning from scan, index-search, and join choices. Students execute the before/after
selection lab, trace a department-course join, and record what the plan can and cannot
support. Materialization, pipelining, and detailed join alternatives remain available
for after-class reading.

## Verification command

```powershell
py -3 working_materials/chapters/ch15_query_processing/instructor/verify_ch15.py
```

## Remaining limits before student release

- Instructor must confirm bilingual versus English-only student prose.
- SQLite 3 is the course DBMS; these materials are verified with SQLite 3.45.3.
- The combined Chapter 15/16 classroom workload has not been observed with students.
- `COURSE_PLAN.md` governs the required Chapter 15 scope and assessment boundary.

## Chapter delivery status

- Files created: student guide, SQL lab, instructor source/alignment record, and
  verifier.
- Source verification: complete for textbook printed pages 689-735 and slides
  15.1-15.74.
- Executed content: deterministic data generation; selection scan and index-search
  plans; identical join results before/after index creation; two-search indexed join;
  temporary ORDER BY work; and all foreign keys.
- Unexecuted content: full sorting/join algorithms and other supplementary topics.
- Progression decision: the chapter meets the source, explanation, worked-example,
  practice, plan-evidence, and executable-check conditions required to begin Chapter
  16. It remains a draft until the instructor reviews language and classroom workload.
