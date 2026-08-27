# Chapter 5 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: draft, source-checked against the complete Chapter 5 text and
  official Chapter 5 slides
- Dataset: extends the original Chapter 2 course-registration schema with prerequisite,
  audit, and practice-score relations
- Executable verification: passed again on August 27, 2026, using Python 3.12.9 and
  SQLite 3.45.3
- Publication: not approved

## Source scope checked

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 5, printed pages 183-232, Sections 5.1-5.6, plus the chapter examples and
  implementation notes needed to interpret portability limits.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch5.pdf`, slides
  5.1-5.54. The local deck ends after recursive-query material and does not contain
  the Chapter 5 advanced-aggregation slides promised by its outline.
- Current governance, revised syllabus, `COURSE_PLAN.md`, chapter-material prompt,
  Chapter 2 setup, Chapters 3-4 materials, existing SQL labs, and the historical plan.

## Scope decision

Required teaching is deliberately selected: tie-aware ranking; partitioned window
aggregates; recursive CTE base and recursive terms, fixed point, and termination; one
row-level audit trigger with `OLD`/`NEW`; stored function/procedure purpose and interface
only;
and one conditional-aggregation cross-tab.

Complete SQL/PSM control flow, table functions, external routines, statement-level
triggers, vendor pivot syntax, rollup, and cube are supplementary. JDBC, Python
database access, ODBC, and embedded SQL are read for chapter context but excluded by
the course scope. Supplementary material is not valid Exam 2 operation content unless
separately taught and practiced.

## Source and DBMS cautions

1. The textbook explicitly notes substantial DBMS variation in routine and trigger
   syntax. The SQL/PSM reference is not labeled executable; SQLite has no SQL
   `CREATE FUNCTION` or `CREATE PROCEDURE` statement.
2. The lab executes equivalent routine-body SQL only. This verifies expected data
   results, not installation or invocation of a stored routine.
3. SQLite trigger syntax uses `OLD` and `NEW` and supports row-level triggers. The
   standard transition-row syntax in the textbook is not copied as SQLite syntax.
4. The audit condition uses SQLite's null-safe `IS NOT`. A normal `<>` comparison
   would evaluate to unknown when one grade is null.
5. The official recursive-query slide has an extraction-visible trailing comma and a
   `rec_rereq` typo. The student query was rebuilt and executed rather than copied.
6. `UNION` can stop duplicate pair generation in the transitive-closure example, but
   it does not guarantee termination when recursion carries changing state such as
   depth. The guide makes this limitation explicit.
7. `ROW_NUMBER` includes a stable `student_id` tie-breaker. `RANK` and `DENSE_RANK`
   intentionally use score only so ties remain ties.
8. The guide explicitly supplies a `ROWS` frame instead of relying on a DBMS default.
9. Dedicated `PIVOT`, `ROLLUP`, `CUBE`, and `GROUPING` examples are not executable
   in the current SQLite lab. Conditional aggregation is the verified core cross-tab.

## Teaching-point alignment

| ID | Teaching point | Primary source | Worked example | Student action and feedback |
|---|---|---|---|---|
| C5.01 | function purpose/interface | 5.2-5.2.1, pp. 198-200; slides 5.30-5.33 | enrollment-count contract | Define department count; verify equivalent query |
| C5.02 | procedure purpose/interface | 5.2.1-5.2.2, pp. 200-203 | reversible credits body | Define no-match contract and constraint behavior |
| C5.03 | function/procedure/trigger distinction | 5.2-5.3, pp. 198-207 | comparison table | Classify invocation and outputs |
| C5.04 | trigger event/condition/action | 5.3.1-5.3.2, pp. 206-210; slides 5.43-5.47 | grade audit trigger | Build delete audit; inspect before/after/rollback |
| C5.05 | `OLD`/`NEW` and nullable change | 5.3.2, pp. 207-210 | B to B+ plus no-op guard | Explain why delete uses `OLD` |
| C5.06 | when not to use triggers | 5.3.3, pp. 210-213; slides 5.48-5.49 | foreign-key comparison | Select CHECK/FK action/trigger by rule |
| C5.07 | recursive base/recursive terms | 5.4.2, pp. 216-218; slides 5.50-5.54 | prerequisite closure | Query FT210 and list iterations |
| C5.08 | fixed point and termination | 5.4.1-5.4.2, pp. 214-218 | five-pair closure | Add cycle in savepoint and reason before execution |
| C5.09 | `UNION` versus `UNION ALL` | 5.4.2, pp. 217-218 | pair closure versus depth | Explain duplicate state and cycle guard |
| C5.10 | `RANK` and `DENSE_RANK` | 5.5.1, pp. 219-223 | 92/92/84/84 ties | Predict new tie and rank gap |
| C5.11 | deterministic `ROW_NUMBER` | 5.5.1, pp. 221-223 | student-ID tie-breaker | State ordering evidence |
| C5.12 | `PARTITION BY` | 5.5.1-5.5.2, pp. 220-225 | per-student running average | Show reset for each student |
| C5.13 | explicit window frame | 5.5.2, pp. 223-226 | unbounded-to-current frame | Build two-row moving frame |
| C5.14 | cross-tab/pivot concept | 5.5.3, pp. 225-227 | conditional aggregation | Add best score and diagnose new category |

Every required teaching point has explanation, a complete example, student practice, and
a stated check. Supplementary items are excluded from Exam 2 until taught.

## Teaching summary

1. Compare function, procedure, and trigger invocation and contracts.
2. Trace the unexecuted function reference and execute its equivalent query.
3. Build the audit trigger; update, inspect `OLD`/`NEW`, and roll back.
4. Compare trigger with a declarative foreign key or check constraint.
5. Hand-trace the prerequisite base term and each recursive iteration.
6. Discuss cycle behavior before any cycle query is run.
7. Predict ties, then execute `RANK`, `DENSE_RANK`, and `ROW_NUMBER`.
8. Trace partition and frame rows for a running average.
9. Build the conditional-aggregation cross-tab and discuss fixed categories.
10. Compare, rank, and individually revise the integrated SQL response.

## Student-practice guidance

1. P1 takes one department code and returns `COUNT(*)` from course for that code;
   expected IM=2, FIN=1, DES=1, missing=0.
2. P2 should define observable behavior for a zero-row update, such as a status output
   or raised condition. Credits 8 is rejected by the course `CHECK` constraint.
3. P3 is `AFTER DELETE ON enrollment`; use only `OLD` row values. Both deletion and
   audit row must disappear after rollback.
4. P4 prefers constraints for direct invariants because they are schema-visible and
   cover all relevant modifications; trigger remains appropriate for change history.
5. P5 returns DB201 depth 1 and WD120 depth 2 for FT210.
6. P6 creates a cycle ML230 -> DB201 -> WD120 -> ML230. Pair-based `UNION` reaches
   a finite set, possibly including self-reachability. Depth changes each round, so an
   unguarded depth query does not deduplicate.
7. P7 best scores become 92,92,92,84: the first three get rank 1 and dense rank 1;
   S104 gets rank 4 and dense rank 2. Row numbers follow student ID among ties.
8. P8 uses `ROWS BETWEEN 1 PRECEDING AND CURRENT ROW`; a third attempt is needed
   to distinguish it from the running frame.
9. P9 may add `MAX(score) AS best_score`; the fixed cross-tab does not add attempt 3
   automatically.

## Verification command

```powershell
py -3 working_materials/chapters/ch05_advanced_sql/instructor/verify_ch05.py
```

## Remaining limits before student release

- Instructor must confirm bilingual versus English-only student prose.
- SQLite 3 is the course DBMS and does not install stored routines through SQL; routine
  reference code is conceptual and is not a required executable activity.
- Classroom workload and accessibility have not yet been observed with actual students.
- `COURSE_PLAN.md` governs Chapter 5 scope and assessment boundaries.

## Chapter delivery status

- Files created: student guide, executable lab, non-executable SQL/PSM routine
  reference, instructor coverage record, and automated verifier.
- Source verification: complete for textbook printed pages 183-232 and slides
  5.1-5.54.
- Executed content: the complete student lab; equivalent routine-body results;
  reversible procedure-body modification; audit trigger including null-safe/no-op and
  rollback behavior; recursive closure and depth; tie-aware ranking; partitioned running
  window; and conditional aggregation.
- Unexecuted content: routine installation/call, statement-level triggers, external
  routines, dedicated pivot syntax, rollup, and cube. They are explicitly labeled.
- Main corrections made: separated routine logic from unsupported SQLite DDL; repaired
  the recursive slide example; made trigger comparison null-safe; stated cycle limits;
  and made ranking/window ordering explicit.
- Progression decision: the chapter meets the source, example, practice, alignment, and
  executable-check conditions required to begin Chapter 6. It remains a draft until the
  instructor reviews language, classroom tooling, and workload.
