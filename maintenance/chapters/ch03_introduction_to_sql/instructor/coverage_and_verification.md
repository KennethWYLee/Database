# Chapter 3 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: draft, source-checked against the complete Chapter 3 text and
  official Chapter 3 slides
- Dataset: reuses the original Chapter 2 course-registration schema
- Executable verification: passed again on August 27, 2026, using Python 3.12.9 and
  SQLite 3.45.3
- Publication: not approved

## Source scope checked

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 3, printed pages 65-114, including Sections 3.1-3.10 and Notes 3.1-3.3.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch3.pdf`, all 62 PDF
  pages.
- Current course governance, revised syllabus, `COURSE_PLAN.md`, chapter-material
  prompt, Chapter 2 dataset, and historical Week 3-4 activity descriptions.

## Scope decision

Required instruction includes DDL basics; `SELECT`, `FROM`, `WHERE`; aliases;
expressions; duplicates and `DISTINCT`; string patterns; ordering; `BETWEEN`; set
operations; `NULL`; aggregates; `GROUP BY`; `HAVING`; `IN`; `EXISTS`; one correlated
query; one CTE; and basic `INSERT`, `UPDATE`, and `DELETE`.

The following textbook material is supplementary because it cannot be taught and
practiced responsibly within two meetings and several constructs are not supported by
the current SQLite environment: subqueries in `FROM`, scalar and complex correlated
subqueries, `SOME`/`ALL`, `UNIQUE`, `LATERAL`, scalar queries without `FROM`,
`INTERSECT ALL`, `EXCEPT ALL`, formal multiset-algebra notes, and advanced modification
statements. These items are not valid Exam 1 content unless the instructor later adds
explicit teaching and practice.

## Source and DBMS cautions

1. SQLite uses type affinity and does not enforce standard `VARCHAR(n)` length or
   `NUMERIC(p,d)` precision in the same way as many server DBMSs. The guide teaches
   standard type purposes and uses SQLite-compatible `TEXT`, `INTEGER`, and `CHECK`
   constraints for execution.
2. String comparison and `LIKE` case behavior depend on DBMS and collation. The guide
   does not repeat the slide deck's unconditional case-sensitivity wording.
3. SQLite permits bare non-grouped columns in some aggregate queries. The course
   requires standard SQL grouping rules instead of accepting an arbitrary SQLite value.
4. The textbook's comma-separated multi-relation syntax is used once to explain
   `FROM` plus matching predicates. Explicit `JOIN` syntax is reserved for Chapter 4.
5. The slides contain extraction-visible errors or ambiguous symbols in the
   `SOME`/`ALL` equivalence examples, a `department.name` reference, and a scalar-update
   line. None is copied into student materials.
6. The `NOT IN` plus `NULL` failure is derived from the chapter's three-valued logic and
   verified directly in SQLite. It is labeled as an executed instructional inference.

## Teaching-point alignment

| ID | Teaching point | Primary source | Worked example | Student action and feedback |
|---|---|---|---|---|
| C3.01 | DDL, DML, integrity | 3.1, pp. 65-66 | Guide Sec. 1 | Classify schema versus data operations |
| C3.02 | types and `CREATE TABLE` | 3.2.1-3.2.2, pp. 67-70 | `study_group` DDL | Design member table constraints; verifier tests failures |
| C3.03 | `DROP`, `DELETE`, `ALTER` distinction | 3.2.2, pp. 69-71 | G01 comparison | Choose predicate-preserving deletion |
| C3.04 | basic `SELECT/FROM/WHERE` | 3.3.1, pp. 71-74 | IM except S101 | Predict `AND` versus `OR` rows |
| C3.05 | duplicates, `DISTINCT`, expressions | 3.3.1, pp. 72-74 | department codes and semester hours | Explain tuple-level `DISTINCT` |
| C3.06 | multiple relations and aliases | 3.3.2, pp. 74-79; 3.4.1, pp. 79-82 | student-enrollment matching | Identify relations, aliases, and predicate |
| C3.07 | strings and `LIKE` | 3.4.2, pp. 82-83 | Technology title | Construct `%` and `_` patterns |
| C3.08 | `BETWEEN`, `ORDER BY` | 3.4.4-3.4.5, pp. 83-85 | low-credit course display | Explain inclusive endpoints and ordering |
| C3.09 | set operations and duplicates | 3.5, pp. 85-89 | DB201/FT210 sets | Reverse `EXCEPT` and explain direction |
| C3.10 | `NULL` and three-valued logic | 3.6, pp. 89-90 | temporary null grade | Evaluate A/F/NULL predicates |
| C3.11 | aggregate functions | 3.7.1, pp. 91-92 | course summary | Distinguish three `COUNT` forms |
| C3.12 | `GROUP BY` | 3.7.2, pp. 92-94 | per-department course data | Diagnose bare `title` output |
| C3.13 | `WHERE` versus `HAVING` | 3.7.3, pp. 95-96 | IM group after row filter | Place row and group conditions |
| C3.14 | `IN` subquery | 3.8.1, pp. 98-99 | DB201 student lookup | Verify inner and outer queries separately |
| C3.15 | `EXISTS`, correlation, absence | 3.8.3, pp. 101-103 | high-grade enrollment existence | Rewrite for students with no enrollment |
| C3.16 | `NOT IN` and `NULL` | 3.6 plus executed inference | blocked set with `NULL` | State when `NOT IN` is safe |
| C3.17 | CTE core; subquery in `FROM` supplementary | 3.8.5-3.8.6, pp. 104-106 | enrollment counts | Build department count layers |
| C3.18 | scalar subquery (supplementary) | 3.8.7, pp. 106-107 | count per course | Diagnose multi-row scalar result |
| C3.19 | `INSERT`, `UPDATE`, `DELETE` | 3.9, pp. 108-114 | reversible S105 lifecycle | Predict target count and validate constraints |

Every required teaching point has explanation, a complete example, student practice, and
a stated checking criterion. Supplementary items are excluded from Exam 1 until taught.

## Teaching summary

### Week 3

1. Rebuild schema and inspect DDL constraints.
2. Predict and execute basic queries, `DISTINCT`, expressions, and aliases.
3. Diagnose a missing matching predicate.
4. Practice `LIKE`, `BETWEEN`, and deterministic output ordering.
5. Compare set operations and SQL duplicate behavior.
6. Run the temporary `NULL` example and record three-valued results.

### Week 4

1. Retrieval check on duplicates and `NULL`.
2. Execute aggregate, grouping, and `HAVING` examples.
3. Validate subqueries from the inside out.
4. Compare `NOT IN` with `NOT EXISTS` when a `NULL` is present.
5. Use subquery in `FROM`, CTE, and scalar subquery on one shared task.
6. Execute reversible DML and submit the individual result record.
7. Compare and revise a query that misuses `WHERE`, `HAVING`, and `NULL`.

## Student-practice guidance

1. Member table: composite primary key `(group_id, student_id)`; both columns are
   foreign keys; `member_role` is `NOT NULL`.
2. Remove G01 only: `DELETE FROM study_group WHERE group_id = 'G01'`, subject to
   referencing rows and the configured foreign-key action.
3. `AND` to `OR`: S102, S103, and S104 satisfy at least one condition; S101 satisfies
   `dept_code='IM'` as well, so all four rows pass. This is a useful precedence check.
4. `DISTINCT dept_code, student_name` retains all four rows because the complete pairs
   differ.
5. Course-department matching uses `course.dept_code = department.dept_code`.
6. Patterns: `Data%` and `_e%` for the stated examples.
7. Reversed `EXCEPT` returns S102.
8. `grade <> 'F'`: true for A, false for F, unknown for `NULL`; only A passes `WHERE`.
9. Grouped `title` is ambiguous for IM; aggregate title, add it to grouping if the
   question needs one row per title, or remove it.
10. Three-credit filter belongs in `WHERE`; average group condition belongs in `HAVING`.
11. No-enrollment students use `NOT EXISTS` with `e.student_id = s.student_id`.
12. `NOT IN` is safe from this specific failure only if the subquery output is guaranteed
   non-null, for example by a `NOT NULL` schema constraint or an explicit `IS NOT NULL`
   filter whose logic is appropriate.
13. A scalar query selecting individual grades can return multiple rows for a course and
   is not valid in a scalar position.
14. Unqualified `UPDATE course SET credits = 4` targets all four rows; add
   `WHERE course_id = 'DB201'` after confirming with `SELECT`.

## Verification command

```powershell
py -3 maintenance/chapters/ch03_introduction_to_sql/instructor/verify_ch03.py
```

## Remaining limits before student release

- The instructor selected English-only student prose on August 27, 2026. The rewritten
  guide still requires final instructor content and language review before publication.
- The approved SQLite student package supplies the runner and SQL files; compatible
  SQLite interfaces remain acceptable as stated in the syllabus.
- Classroom workload and accessibility have not yet been observed with actual students.
- `COURSE_PLAN.md` governs Chapter 3 dates, required scope, and assessment boundaries.

## Chapter delivery status

- Files created: student guide, executable lab, instructor coverage and guidance, and
  automated verifier.
- Source verification: complete for the textbook's printed pages 65-114 and all 62
  pages of the local official slide PDF.
- Executed content: the complete student lab plus independent checks for all documented
  query results, `NULL` behavior, constraints, and reversible modifications.
- Unexecuted content: supplementary `SOME`/`ALL`, `UNIQUE`, `LATERAL`, scalar-without-
  `FROM`, `INTERSECT ALL`, and `EXCEPT ALL` examples. They are not required teaching or
  Exam 1 content.
- Main corrections made: separated SQL standard expectations from SQLite behavior,
  enforced standard grouping rules, verified the `NOT IN` plus `NULL` case, and kept
  every modification reversible.
- Progression decision: the chapter meets the source, example, practice, alignment, and
  executable-check conditions required to begin Chapter 4. It remains a draft until the
  instructor reviews language, classroom tooling, and workload.
