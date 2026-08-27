# Chapter 4 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: draft, source-checked against the complete Chapter 4 text and
  official Chapter 4 slides
- Dataset: reuses the original Chapter 2 course-registration schema
- Executable verification: passed again on August 27, 2026, using Python 3.12.9 and
  SQLite 3.45.3
- Publication: not approved

## Source scope checked

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 4, printed pages 125-174, including Sections 4.1-4.7 and the summary.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch4.pdf`, all 58 PDF
  pages.
- Current `AGENTS.md`, `PROJECT.md`, revised syllabus, `COURSE_PLAN.md`, chapter-material
  prompt, Chapter 2 setup, Chapter 3 lab, existing SQL labs, and historical plan.

## Scope decision

Required instruction includes explicit inner joins; `ON` and `USING`; the risk of
`NATURAL JOIN`; left outer joins; `ON` versus `WHERE` with outer joins; view definition
and querying; live base-data reflection; basic transaction boundaries;
atomicity; `NOT NULL`, `UNIQUE`, `CHECK`, foreign
keys, and referential actions.

Materialized views, deferred constraints, assertions, and authorization are conceptual
supplements. Date/time, large objects, user-defined types, domains, catalogs, and schemas
are not required in this one-meeting chapter. Index definition moves to Chapter 14.
These supplementary items are not valid Exam 1 operation questions unless separately
taught and practiced.

## Source and DBMS cautions

1. The textbook presents natural join before explicit `ON`; the course emphasizes
   explicit matching because the textbook itself demonstrates how an extra shared
   attribute can silently remove valid rows (Section 4.1.1, pp. 128-130).
2. `ON` and `WHERE` may be interchangeable for a simple inner join but are not
   interchangeable for outer joins (Section 4.1.3, pp. 134-135). The lab executes both.
3. SQLite added right and full outer joins in 3.39. The lab records a minimum version
   instead of treating the syntax as available in every SQLite installation or DBMS.
4. A normal view stores a query definition. Materialized-view syntax and refresh policy
   are DBMS-specific and are not executed in SQLite.
5. The textbook gives general conditions under which some SQL views may be updatable.
   SQLite views are read-only unless an `INSTEAD OF` trigger is defined. The aggregate
   view failure is labeled as SQLite behavior, not a universal rule.
6. The SQL standard's implicit transaction start and implementation defaults differ from
   tools that autocommit each statement. The lab uses savepoints so examples are
   reversible; the verifier separately uses explicit `BEGIN` and `ROLLBACK`.
7. A `CHECK` rejects `FALSE`, not `UNKNOWN`; therefore it does not exclude `NULL`
   without `NOT NULL` (Section 4.4.4, p. 147). The lab executes this edge case.
8. The textbook notes that subqueries in `CHECK`, assertions, and deferred constraints
   are unavailable in many implementations. They are not presented as executable
   SQLite features.
9. The official slide deck says `UNIQUE` attributes form a candidate key while also
   permitting nulls. The textbook more precisely describes them as a superkey while
   noting that null is allowed unless separately prohibited. The guide follows the
   textbook and avoids equating nullable `UNIQUE` directly with a primary key.

## Teaching-point alignment

| ID | Teaching point | Primary source | Worked example | Student action and feedback |
|---|---|---|---|---|
| C4.01 | explicit inner join and `ON` | 4.1.2, pp. 130-131; slides 4.14-4.17 | three-relation enrollment query | Add email and course department; expect six rows |
| C4.02 | `USING` | 4.1.1, pp. 129-130; slides 4.4-4.5 | course-department query | Rewrite with `ON`; compare four rows |
| C4.03 | `NATURAL JOIN` risk | 4.1.1, pp. 128-130; slides 4.5-4.7 | cross-department enrollment disappears | Explain five versus six rows |
| C4.04 | inner versus outer join | 4.1.3-4.1.4, pp. 131-136; slides 4.8-4.17 | unmatched IS250 | Add unmatched student; expect count zero |
| C4.05 | right and full outer join | 4.1.3, pp. 132-135; slide 4.9 | planned-student tables | Identify matched, left-only, and right-only rows |
| C4.06 | outer join `ON` versus `WHERE` | 4.1.3, pp. 134-135 | A/A- courses | Explain five versus four rows using `NULL` |
| C4.07 | view definition and use | 4.2.1-4.2.2, pp. 137-140; slides 4.18-4.24 | course summary view | Create and query `im_course` |
| C4.08 | view reflects base data | 4.2.2, pp. 139-140 | DB201 count 2, then 3, then 2 | Add and roll back base row |
| C4.09 | view modification limits | 4.2.4, pp. 140-143; slides 4.29-4.32 | failed aggregate-view update | Compare simple and aggregate views |
| C4.10 | transaction, commit, rollback | 4.3, pp. 143-145; slides 4.33-4.34 | S101 course swap | Verify before/after/rollback rows |
| C4.11 | transaction atomicity | 4.3, pp. 143-145 | failed second step scenario | Explain why both statements share a boundary |
| C4.12 | `NOT NULL` and `UNIQUE` | 4.4.1-4.4.3, pp. 145-147; slides 4.35-4.38 | waitlist schema | Classify separate invalid rows |
| C4.13 | `CHECK` and `NULL` | 4.4.4, pp. 147-149; slides 4.39 | priority and check-only tables | Explain `UNKNOWN`; verifier checks both cases |
| C4.14 | foreign keys | 4.4.5, pp. 149-150; slides 4.40-4.41 | waitlist parents | Design composite feedback reference |
| C4.15 | referential actions | 4.4.5, pp. 150-151; slide 4.42 | temporary S105 cascade | Choose reject/cascade/set-null from business rule |

Every required teaching point has explanation, a complete example, student practice, and
a stated checking criterion. Supplementary items are excluded from Exam 1 until taught.

## Teaching summary

1. Rebuild the schema and trace the two conditions in a three-relation inner join.
2. Compare `ON`, `USING`, and the executed `NATURAL JOIN` failure.
3. Predict left/right/full outer-join rows with matched and unmatched inputs.
4. Run the `ON`-versus-`WHERE` example and explain the role of `NULL`.
5. Create and query a view; modify a base row and observe the view result.
6. Analyze why the aggregate view update has no direct base-row interpretation.
7. Execute and roll back a two-statement course swap.
8. Create the waitlist schema and classify independent constraint failures.
9. Execute the cascade and `CHECK`-with-`NULL` cases.
10. Compare and revise the integrated SQL response; retain individual evidence.

## Student-practice guidance

1. P1 joins `student` to `enrollment` on `student_id`, `enrollment` to `course` on
   `course_id`, and `course` to `department` on `dept_code`. It returns six rows and
   shows Finance for S101/FT210.
2. P2 uses `ON c.dept_code = d.dept_code` and returns the same four selected rows.
3. P3 groups by student ID/name and counts `e.course_id`, not `COUNT(*)`; a temporary
   no-enrollment student must have zero.
4. P4 keeps IS250 when the grade predicate is in `ON`; `WHERE` removes it because the
   null-padded grade does not make the predicate true.
5. P5 view definition filters `course.dept_code = 'IM'`; current three-credit result is
   DB201 and ML230.
6. P6 must record the same starting and final rows after `ROLLBACK`; both modifications
   must occur inside one boundary.
7. P7 can use `(student_id, course_id, term)` as both a primary key and a composite
   foreign key referencing `enrollment`, plus `rating INTEGER NOT NULL CHECK
   (rating BETWEEN 1 AND 5)`. A separate nullable comment is acceptable.

## Verification command

```powershell
py -3 working_materials/chapters/ch04_intermediate_sql/instructor/verify_ch04.py
```

## Remaining limits before student release

- The instructor selected English-only student prose on August 27, 2026. The rewritten
  guide still requires final instructor content and language review before publication.
- The approved SQLite student package supplies the runner and SQL files. Executed
  right/full join examples require SQLite 3.39 or later but are supplementary.
- Classroom workload and accessibility have not yet been observed with actual students.
- `COURSE_PLAN.md` governs Chapter 4 scope and assessment dates.

## Chapter delivery status

- Files created: student guide, executable lab, instructor coverage and guidance, and
  automated verifier.
- Source verification: complete for the textbook's printed pages 125-174 and all 58
  pages of the local official slide PDF.
- Executed content: the complete student lab; explicit, `USING`, and natural joins;
  left, right, and full outer joins; `ON` versus `WHERE`; view re-evaluation and the
  failed aggregate-view update; explicit transaction rollback; independent constraint
  failures; cascade behavior; and the `CHECK` plus `NULL` edge case.
- Unexecuted content: materialized-view refresh, updatable views on another DBMS,
  deferred constraints, assertions, authorization, and DBMS-specific date/time/type
  syntax. They are supplementary and not required Exam 1 operations.
- Main corrections made: gave explicit joins priority while retaining the textbook's
  natural-join warning; separated standard view concepts from SQLite restrictions;
  made all data modifications reversible; and paired `CHECK` with a tested `NULL` case.
- Progression decision: the chapter meets the source, example, practice, alignment, and
  executable-check conditions required to begin Chapter 5. It remains a draft until the
  instructor reviews language, classroom tooling, and workload.
