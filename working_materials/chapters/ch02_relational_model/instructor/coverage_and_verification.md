# Chapter 2 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: draft, source-checked against the complete Chapter 2 text and
  official Chapter 2 slides
- Student dataset: original course-registration example
- Executable verification: passed again on August 27, 2026, using Python 3.12.9 and
  Python's bundled SQLite library
- Publication: not approved

## Source scope checked

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 2, printed pages 37-58, including Sections 2.1-2.7 and Note 2.1.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch2.pdf`, slides
  2.1-2.29.
- Current course governance: `AGENTS.md`, `PROJECT.md`,
  `1151_database_management_revised_syllabus.md`, and
  `database_chapter_teaching_material_prompt.md`.
- Historical 18-week plan: only its Week 1-2 activity ideas were used. Its four-exam
  calendar and later chapter sequence were superseded by `COURSE_PLAN.md`.
- Existing SQLite university database and insertion scripts were inspected for available
  tables and continuity. They were not copied into the new student-facing example.

## Source conflicts and adaptations

1. The current textbook classifies relational algebra as a functional query language.
   The slide deck uses the older label "procedural language." Student material follows
   the current textbook wording and explains the three categories without reproducing
   the obsolete label.
2. Formal relations are sets and have no duplicate tuples. SQLite and SQL tables can
   retain duplicates unless constrained or `DISTINCT` is used. The student lab states
   this difference explicitly.
3. The textbook notes that atomicity depends on how a value is used. The student guide
   therefore avoids claiming that a phone-number string is inherently atomic or
   non-atomic.
4. SQL syntax in the lab is verification support, not a Ch2 memorization requirement.
   SQL instruction begins in Ch3.
5. The book's university figures and exercise solutions were not reproduced. All
   student-visible data, questions, and tables were rewritten as a course-registration
   example.

## Teaching-point alignment

| ID | Teaching point | Primary source | Explanation and worked example | Student action and feedback |
|---|---|---|---|---|
| C2.01 | relation, tuple, attribute, instance | 2.1, pp. 37-40; slides 2.3-2.5 | Student guide Sec. 1, `course` count example | Identify parts of `enrollment`; check attribute names versus values |
| C2.02 | domain and atomic values | 2.1, pp. 39-40; slide 2.4 | Student guide Sec. 2, phone-number comparison | Explain a repeated DB201 tuple under formal and SQL interpretations |
| C2.03 | unordered relations and duplicates | 2.1, pp. 39-40; slide 2.5 | Student guide Sec. 2, reordered `student` example | Distinguish display order from relation semantics |
| C2.04 | `NULL` preview | 2.1, p. 40; slide 2.4 | Student guide Sec. 2 | State why full semantics are deferred to Ch3 |
| C2.05 | schema versus instance | 2.2, pp. 41-43; slide 2.6 | Student guide Sec. 3, add row versus add attribute | Classify department update and justify |
| C2.06 | superkey, candidate key, primary key | 2.3, pp. 43-45; slide 2.7 | Student guide Sec. 4, `student` example | Compare three primary-key proposals using stated criteria |
| C2.07 | composite key | 2.3, p. 44 | Student guide Sec. 4, `enrollment` example | Include composite key in Week 1 evidence |
| C2.08 | foreign key and referential integrity | 2.3, pp. 45-46; slide 2.7 | Student guide Sec. 5, invalid LAW department | Identify both `enrollment` foreign keys |
| C2.09 | schema diagram | 2.4, pp. 46-47; slide 2.8 | Student guide Sec. 6, three-step trace | Draw arrows and label referencing/referenced sides |
| C2.10 | query-language categories | 2.5, pp. 47-48; slide 2.9 with corrected terminology | Student guide Sec. 7, IM-student request | Classify a step-by-step description |
| C2.11 | algebra input/output and composition | 2.6, pp. 48, 50 | Student guide Secs. 8 and 11 | Write expression for three-credit courses |
| C2.12 | selection | 2.6.1, p. 49; slides 2.11-2.12 | Student guide Sec. 9, IM students | Predict compound predicate and explain exclusions |
| C2.13 | projection | 2.6.2, pp. 49-50; slides 2.13-2.14 | Student guide Sec. 10, department codes | Predict buildings and remove duplicates |
| C2.14 | Cartesian product | 2.6.4, pp. 50-52; slides 2.16-2.17 | Student guide Sec. 12, 2 by 2 product | Predict full product cardinality and reject factual interpretation |
| C2.15 | theta join | 2.6.5, pp. 52-53; slides 2.18-2.20 | Student guide Sec. 13, student-enrollment join | Select relations and predicate for course-department join |
| C2.16 | union compatibility and union | 2.6.6, pp. 53-54; slides 2.21-2.22 | Student guide Sec. 14, DB201/FT210 sets | Compute operations with ML230 set |
| C2.17 | intersection and difference | 2.6.6, pp. 54-55; slides 2.23-2.24 | Student guide Sec. 14, four-result table | Explain directional difference |
| C2.18 | assignment (supplementary) | 2.6.7, pp. 55-56; slide 2.25 | Student guide Sec. 15, named student sets | Rewrite union with meaningful temporary names |
| C2.19 | rename (supplementary) | 2.6.8, pp. 56-57; slide 2.26 | Student guide Sec. 16, same-department pair | Identify self-pairs and reversed pairs |
| C2.20 | equivalent-query formal detail (supplementary) | 2.6.9, p. 58; slides 2.27-2.28 | Student guide Sec. 17, filter before/after join | Place a course predicate on a valid input relation |

All rows have an explanation, a worked example, a student action, and an explicit
checking or feedback criterion. No teaching point is represented by a term-only bullet.

## Teaching summary

### Week 1

1. Relation/table interpretation and the course-registration instance.
2. Prediction: whether row order changes a relation.
3. Schema versus instance worked example and individual classification.
4. Key definitions followed immediately by the `student` and `enrollment` examples.
5. Foreign-key violation demonstration.
6. Schema-diagram tracing and individual schema/key sheet.

### Week 2

1. Retrieval check on key types and arrow direction.
2. Query-language categories and algebra closure.
3. Selection, projection, and composition with prediction before reveal.
4. Product versus join with tuple-count check.
5. Union, intersection, and difference using the same A/B relations.
6. Assignment, rename, and equivalent-query examples.
7. Group comparison of key proposals, anonymous display, individual ranking, instructor
   feedback, and individual revision.

## Student-practice guidance

These are practice tasks, not released examination items. Accept equivalent notation if
the schema and result are correct.

1. `enrollment` identification: relation is `enrollment`; attributes are `student_id`,
   `course_id`, `term`, `grade`; the requested tuple is `(S103, ML230, 115-1, A)`.
2. Duplicate DB201: prohibited in the formal set interpretation; an unconstrained SQL
   table can store duplicates.
3. S102 department update: instance change, assuming `IM` already exists and no schema
   definition changes.
4. Enrollment foreign keys: `student_id -> student.student_id` and
   `course_id -> course.course_id`.
5. Compound selection: only S103 remains.
6. Building projection: `{Hong Hall, Cheng Hall}`.
7. Three-credit courses:
   `Π_course_id,title(σ_credits=3(course))`.
8. Full student-course product: 16 tuples, not 16 enrollment facts.
9. Course-department join: `course.dept_code = department.dept_code`.
10. With `C = {S103}`, `A union C = {S101, S103}`,
    `A intersection C = {S103}`, and `C minus A = empty set`.
11. Rename without ID inequality retains self-pairs and reversed pairs.
12. `course_id` is not an attribute of `student`; filter `enrollment` before or after the
    valid join, depending on the expression.

## Verification commands and record

Run from the course repository root:

```powershell
py -3 working_materials/chapters/ch02_relational_model/instructor/verify_ch02.py
```

Expected checks:

- row counts and schema constraints;
- duplicate primary key, duplicate candidate key, invalid foreign key, and duplicate
  composite key are rejected;
- selection, projection, product, join, union, intersection, difference, assignment,
  and rename return the documented results;
- the two equivalent-query implementations return identical results;
- `PRAGMA foreign_key_check` returns no violations.

## Remaining limits before student release

- The instructor must confirm whether student-facing terminology should remain bilingual
  or become English-only.
- The final classroom SQLite tool has not been selected; the SQL is verified through
  Python's SQLite library but student installation instructions are not final.
- `COURSE_PLAN.md`, the current syllabus, and project decisions govern this chapter.
- The official slide PDF metadata incorrectly identifies another chapter even though the
  visible deck content is Chapter 2. Source use is based on visible content.

## Chapter delivery status

- Files created: student guide, original setup data, executable student lab, instructor
  coverage and guidance, and automated verifier.
- Source verification: complete for the textbook's printed pages 37-58 and slides
  2.1-2.29.
- Executed content: all schema constraints and all executable chapter examples.
- Unexecuted content: paper-based schema-diagram and relational-algebra exercises; these
  were independently worked in the student-practice guidance but require classroom use
  to evaluate workload and student interpretation.
- Main corrections made: replaced the slide deck's obsolete query-language label,
  distinguished formal set semantics from SQL duplicate behavior, and kept SQL syntax
  outside the Ch2 memorization requirement.
- Progression decision: the chapter meets the source, example, practice, alignment, and
  executable-check conditions required to begin Chapter 3. It remains a draft until the
  instructor reviews language and classroom tooling.
