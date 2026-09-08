# Database Management Course Plan, Fall 2026

Updated: September 8, 2026

The instructor authorized the revised chapter selection and three examinations worth
30% each. Class Performance is 10%. This plan implements the current
[English syllabus](../Intro%20DB/syllabus.md); the syllabus's Textbook Coverage table
defines the required topics and exclusions. The first-meeting Ch1, Ch2, and Ch5
opening selections now use the prescribed book. Earlier notebooks are retained under
`Intro DB/under_revision/` and are not assigned material.

## Course Context

- Instructor: WenYi Lee; second-year Information Management students; required course.
- Three credits; Thursdays, periods 5-7, 1:30-4:15 p.m.
- Prescribed text: Ramez Elmasri and Shamkant B. Navathe, *Fundamentals of Database
  Systems*, seventh edition, Pearson.
- English-only student materials; instructor-led explanation, many diagrams, small
  input tables, worked examples, SQL practice, and ER drawing.
- SQLite 3 is required; no server DBMS or complete application-development project.
- One notebook per textbook chapter, with selected scope where applicable. A notebook
  may continue across meetings; the schedule does not require one chapter per week.

## Scope and Prerequisites

First-meeting reading order: syllabus, `Intro DB/ch01.ipynb` through Chapter Summary,
`Intro DB/ch02.ipynb` through Chapter Summary, and `Intro DB/ch05.ipynb` through
First-Meeting Summary and Practice. The instructor may stop earlier and resume.
These are selections, not three complete chapters to finish before class. Supplied
code demonstrates results; SQL/Python authoring is not a first-day requirement.
Ch5 Sections 5.2-5.3 continue in the same notebook after the first-meeting opening.

- Main chapters: 3, 5, 6, 7, 8, 9, and 14, limited to the syllabus's named topics.
- Chapters 1-2: introductory selections. Chapter 8: core relational algebra, not calculus.
- Chapter 9: **Section 9.1 only**. Chapters 3 and 5 supply its prerequisites; Chapter 4
  and Section 9.2 are not required. Teach weak entities, multivalued attributes, and
  the simple ternary relationship before their mapping examples.
- Chapter 14: Sections 14.1-14.4 in Week 11; Section 14.5 in Week 13. Week 11 uses
  supplied candidate keys; formal closure checks and BCNF are not on Exam 2.
- Chapter 15: selected attribute-closure and binary lossless-decomposition material
  from 15.1.1 and 15.2. Do not add proofs, minimal-cover procedures, general
  decomposition tests, or schema-synthesis algorithms.
- Chapter 17: selected index concepts. First supply Chapter 16's basic record, block,
  and file-organization concepts. SQLite index commands and query-plan interpretation
  are implementation supplements, not coverage of all Chapters 18-19.
- Chapter 20: transaction boundaries, ACID, COMMIT/ROLLBACK, and simple interfering
  updates. Do not add formal schedule classification or implementation protocols.
- Chapters 4, 18-19, and 21-22 are not required. Window functions, recursive CTEs,
  stored routines, advanced indexing, and higher normal forms remain optional.

## Teaching and Assessment Alignment

Every required topic needs a concept explanation, a concrete diagram or input table,
a checkable prediction, a worked example, interpretation, a common error or limitation,
and practice. A synthetic table can illustrate or refute a claim; it does not establish
a dependency or decomposition property for all legal database states.

Preserve five group-response comparisons in Weeks 2, 4, 10, 11, and 14: keys, SQL,
ER mapping, normalization, and indexes. Each group submits a reasoned response;
responses are displayed anonymously, every student compares them, the instructor
corrects technical errors, and students revise individually. Group rankings do not
directly determine grades. Fixed-answer practice need not use group comparisons.

## Weekly Schedule

| Week | Date | Textbook Chapters | Teaching Focus and Examples |
|---:|---|---|---|
| 1 | 2026-09-10 | Chapters 1-2; Chapter 5 introduction | Syllabus; database purpose, schemas/instances, basic architecture and data independence; a small student table and identifiers |
| 2 | 2026-09-17 | Chapter 5; Chapter 8 selected operations | Keys and integrity constraints; small-table selection, projection, set operations, product, and joins; key comparison |
| 3 | 2026-09-24 | Chapter 6 | Create tables, set constraints, query data, and use INSERT/UPDATE/DELETE; verify results |
| 4 | 2026-10-01 | Chapter 7 selected queries | NULL, aggregation, GROUP BY/HAVING, IN/EXISTS, selected subqueries; verify an AI-generated query |
| 5 | 2026-10-08 | Chapters 6-7 selected topics | Joins, ON/WHERE, views, constraints, schema changes, and one simple trigger |
| 6 | 2026-10-15 | Chapters 1-2, 5-8 selected topics (exam) | Written Exam 1; introductory concepts, relational model, taught algebra, and SQL; corrections |
| 7 | 2026-10-22 | Chapter 3 | Business rules to ER diagrams: entities, attributes, keys, roles, cardinality, and participation |
| 8 | 2026-10-29 | Chapter 3; Chapter 9 Section 9.1 | Weak entities, multivalued attributes, simple ternary relationship; begin regular-entity and binary-relationship mapping |
| 9 | 2026-11-05 | Chapters 1-2, 5-8 selected topics (review only) | INFORMS travel; asynchronous review of previously taught SQL and concepts; no in-person class, exam, or new content |
| 10 | 2026-11-12 | Chapter 9 Section 9.1; Chapter 3 review | Complete mapping, including the taught weak-entity, multivalued, and ternary examples; build tables and verify an AI-generated ER diagram |
| 11 | 2026-11-19 | Chapter 14 Sections 14.1-14.4 selected topics | Anomalies, FDs, and 1NF-3NF with supplied candidate keys; compare redesigns |
| 12 | 2026-11-26 | Chapter 3; Chapter 9 Section 9.1; Chapter 14 Sections 14.1-14.4 (exam) | Written Exam 2; no BCNF, closure, or formal lossless-decomposition test; corrections |
| 13 | 2026-12-03 | Chapter 14 Section 14.5; Chapter 15 selected topics | Closure and candidate keys, then BCNF and binary lossless decomposition; show spurious tuples |
| 14 | 2026-12-10 | Chapter 16 foundations; Chapter 17 selected topics | Record/block/file background; B+ tree search, composite indexes, read/update costs, and SQLite query-plan evidence; compare an AI index recommendation |
| 15 | 2026-12-17 | Chapter 20 selected topics | Transfer example, ACID, transaction boundaries, COMMIT/ROLLBACK, and interfering updates |
| 16 | 2026-12-24 | Previously taught sections only | Integrated SQL, mapping, normalization, index, and transaction review; no new required topics |
| 17 | 2026-12-31 | None | University anniversary make-up holiday; no class or new required work |
| 18 | 2027-01-07 | Chapter 14 Section 14.5; Chapters 15-17 and 20 selected topics (exam); cumulative application | Written Exam 3 / Final Examination; Chapter 16 only as index background |

## Assessment

| Assessment | Date | Weight | Scope |
|---|---|---:|---|
| Written Exam 1 | 2026-10-15 | 30% | Selected Chapters 1-2 and 5-8, as taught in Weeks 1-5 |
| Written Exam 2 | 2026-11-26 | 30% | Chapter 3, Section 9.1, and selected Sections 14.1-14.4; no EER, BCNF, closure, or formal lossless-decomposition test |
| Written Exam 3 (Final Examination) | 2027-01-07 | 30% | Section 14.5; selected Chapters 15, 17, and 20; Chapter 16 background only; cumulative taught SQL and design |
| Class Performance | Throughout the semester | 10% | Assigned practice, technical correctness, verification evidence, explanation, and revisions |
| Total | | 100% | |

Only assigned submissions contribute to Class Performance. The former internal
exam-by-chapter percentages belonged to the incorrect textbook scope and are no
longer applicable. This revision does not invent replacement item-level percentages.
Before releasing an exam, prepare and verify its items, solutions, marking criteria,
allowed resources, and version against the taught scope. Optional material must be
taught, practiced, and announced before it can be assessed.

## AI Use and Calendar

AI is permitted only in designated activities. Preserve the planned checks in Weeks
4, 10, and 14. Students must explain and verify submitted work; AI is not permitted
in the three individual written examinations. Other allowed exam resources remain
to be announced.

Exam dates and the calendar are unchanged: instructor travel November 1-7; no class
on December 31; the final exam is January 7 during the official final-exam week.
The [official calendar PDF](https://acad.ntub.edu.tw/var/file/4/1004/img/1347/780969106.pdf)
and [calendar page](https://acad.ntub.edu.tw/p/404-1004-37975.php?Lang=zh-tw) were checked
on September 8. No new content is assigned during the travel week or final-exam week.

## Materials Still to Revise

The repository is public under the instructor's earlier decision. The source PDF,
private assessments, and answers remain excluded. Existing notebooks, generators,
and their historical weekly mapping are not evidence that this new scope is already
implemented. Preserve them until their content has been mapped and revised against
the correct book; do not rename them by assuming equal chapter numbers mean equal topics.

The [topic correspondence](course_repository/textbook_material_correspondence.md)
is complete as a gap review, not a full source audit. The first-meeting release and
its scoped verification are recorded in
[the release record](course_repository/first_meeting_release.md). Ch5 continuation
and subsequent notebooks still need revision. The reproduced missing-key defect in
the previous ER schema remains a prerequisite fix before that schema is reassigned.
The classroom response system and the actual examination items still need their
separate preparation and review.
