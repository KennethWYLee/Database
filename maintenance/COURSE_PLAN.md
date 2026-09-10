# Database Management Course Plan, Fall 2026

Updated: September 10, 2026

The instructor authorized the revised chapter selection and three examinations worth
30% each. Class Performance is 10%. This plan implements the current
[English syllabus](../Intro%20DB/syllabus.md). The instructor requested a concise
student syllabus on September 9 and full EER coverage on September 10. This revision
adds Chapter 4 and Section 9.2, moves normalization to Week 13, and makes BCNF and
Chapter 15 optional to keep the existing teaching weeks and assessment weights.
The first-meeting Ch1, Ch2, and Ch5 opening selections now use the prescribed book.
Earlier notebooks are retained under
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

- Main chapters: 3, 4, 5, 6, 7, 8, 9, and 14, limited to the syllabus's named topics.
- Chapters 1-2: introductory selections. Chapter 8: core relational algebra, not calculus.
- Chapter 4: all substantive sections, 4.1-4.7. Cover inheritance, specialization,
  generalization, membership constraints, hierarchies, lattices, shared subclasses,
  categories, design choices and formal definitions, UML comparison, and the
  chapter's introductory abstraction, knowledge-representation, and ontology concepts.
  Use diagrams and small examples; this is not an ontology-engineering course.
- Chapter 9: Sections 9.1-9.2. Chapters 3 and 5 precede ER mapping; the relevant
  Chapter 4 concepts precede each EER mapping. Teach weak entities, multivalued
  attributes, and the simple ternary relationship before their mapping examples.
  Compare all four specialization options (8A-8D), their applicability conditions,
  shared-subclass mappings, and category mappings with same or different source keys.
- Chapter 14: selected Sections 14.1-14.4 in Week 13, using supplied candidate keys.
  Normalization through 3NF is on Exam 3, not Exam 2. BCNF (14.5) is optional.
- Chapter 15: optional reference, not scheduled or required for examinations.
  Attribute closure, formal binary lossless-decomposition tests, proofs, minimal-cover
  procedures, and schema-synthesis algorithms are outside the required scope.
- Chapter 17: selected index concepts. First supply Chapter 16's basic record, block,
  and file-organization concepts. SQLite index commands and query-plan interpretation
  are implementation supplements, not coverage of all Chapters 18-19.
- Chapter 20: transaction boundaries, ACID, COMMIT/ROLLBACK, and simple interfering
  updates. Do not add formal schedule classification or implementation protocols.
- Chapters 15, 18-19, and 21-22 are not required. Window functions, recursive CTEs,
  stored routines, advanced indexing, and higher normal forms remain optional.

## Detailed Coverage

The main course chapters are **3, 4, 5, 6, 7, 8, 9, and 14**, within the limits below.
Chapters **1-2** provide the introduction; Chapters **17 and 20** are selected
topics. Chapter **16** supplies only the storage concepts needed to understand indexes.
Listing a chapter does not make every section, exercise, or proof required.

| Chapter | Required Topics | Limits |
|---|---|---|
| 1-2: Introduction and Architecture | Database purpose and benefits; models, schemas, instances, data independence, languages, and basic client/server architecture | Introductory selections from 1.1-1.3, 1.6, 2.1-2.3, and 2.5; no detailed history or system classification |
| 3: ER Model | Entities, attributes, keys, relationships, roles, cardinality, participation, weak entities, and ER design; one simple ternary relationship | Core concepts from 3.1-3.7; a basic example from 3.9; UML comparison follows in 4.6 |
| 4: EER Model | Inheritance; specialization/generalization; predicate-, attribute-, and user-defined membership; disjoint/overlapping and total/partial constraints; hierarchies, lattices, shared subclasses; categories; design choices and definitions; UML comparison; abstraction, knowledge representation, and ontology concepts | Sections 4.1-4.7, with diagrams and small examples for every topic; 4.6-4.7 remain at the textbook's introductory level, without an additional software or ontology project |
| 5: Relational Model and Constraints | Relations, tuples, domains, schemas, keys, entity integrity, referential integrity, and constraint violations | Core topics from 5.1-5.3 |
| 6: Basic SQL | Data definition, data types, constraints, basic retrieval, and INSERT/DELETE/UPDATE | Core topics from 6.1-6.4, implemented with SQLite |
| 7: More SQL | NULL, joins, aggregation, GROUP BY/HAVING, IN/EXISTS, selected subqueries, views, a simple trigger, and basic schema changes | Selected topics from 7.1-7.4; recursive queries, assertions, and advanced trigger behavior are not required |
| 8: Relational Algebra | Selection, projection, union, intersection, difference, Cartesian product, and joins using small relation instances | Selected operations from 8.1-8.3 and examples from 8.5; division and relational calculus are not required |
| 9: ER- and EER-to-Relational Mapping | ER mapping; specialization options 8A-8D and their conditions; shared subclasses and categories, including surrogate keys where appropriate | Sections 9.1-9.2; teach the corresponding Ch3/Ch4 concept first; distinguish diagram constraints from constraints actually enforced by SQLite |
| 14: Functional Dependencies and Normalization | Design anomalies, functional dependencies, 1NF, 2NF, and 3NF using supplied candidate keys | Selected concepts and examples from 14.1-14.4; BCNF (14.5) is optional; 4NF and 5NF are not required |
| 16-17: Storage Foundations and Indexing | Records, blocks, and basic file organization; index purpose, B+ tree search, composite indexes, and read/update costs | Chapter 16 is prerequisite background only; selected concepts from 17.1-17.4 and 17.7, without full tree-update algorithms or cost derivations |
| 20: Transactions | Logical units of work, transaction boundaries, ACID, COMMIT/ROLLBACK, and simple interfering-update examples | Selected concepts from 20.1-20.3 and 20.6; no formal schedule classification, serializability proofs, or implementation protocols |

Chapter 15 is optional reference; Chapters 18-19 and 21-22 are not required chapters.
SQLite index commands and
basic `EXPLAIN QUERY PLAN` interpretation are practical supplements to Chapter 17,
not a separate course in query optimization. Window functions, recursive CTEs, and
stored routines are optional supplements, not required examination topics.


## Teaching and Assessment Alignment

Every required topic needs a concept explanation, a concrete diagram or input table,
a checkable prediction, a worked example, interpretation, a common error or limitation,
and practice. A synthetic table can illustrate or refute a claim; it does not establish
a dependency or decomposition property for all legal database states.

The final examination remains in Week 16. The instructor's full-EER decision uses
Weeks 7-8 for ER and Section 9.1, and Weeks 10-11 for Chapter 4 with Section 9.2.
Week 8 completes the seven ER-mapping steps with small diagrams and tables; avoid
turning each step into a separate lab. Week 10 compares all four specialization
mappings and checks shared-subclass membership. Week 11 distinguishes categories
from shared subclasses, completes category mapping, and introduces the remaining
Chapter 4 topics through a common design example. Reuse the same example when
comparing EER and UML or explaining abstraction; do not add a project.

Integrate review into the worked examples in Weeks 13-15. In Week 13, use one small
schema with supplied candidate keys to explain anomalies, dependencies, and the
successive changes through 3NF. Do not silently reintroduce closure, BCNF, or formal
lossless-decomposition tests. This is a compressed normalization meeting; actual
pace still needs classroom confirmation.
In Week 14, revisit SQL conditions and result equivalence while comparing index plans.
In Week 15, use one transfer example for boundaries, ACID, and COMMIT/ROLLBACK, plus
one simple interfering-update diagram. Reuse earlier SQL and design examples for
the integrated review; do not add a second transaction case, new submission, formal
schedule classification, or an implementation protocol. These are teaching-scope
limits, not a claim that later notebooks have already been revised or classroom
workload validated. Weeks 16-18 introduce no new required topics.

Preserve five group-response comparisons in Weeks 2, 4, 10, 13, and 14: keys, SQL,
EER mapping, normalization, and indexes. Each group submits a reasoned response;
responses are displayed anonymously, every student compares them, the instructor
corrects technical errors, and students revise individually. Group rankings do not
directly determine grades. Fixed-answer practice need not use group comparisons.

## Weekly Schedule

| Week | Date | Textbook Chapters | Teaching Focus and Examples |
|---:|---|---|---|
| 1 | 2026-09-10 | Ch1: Databases and Database Users (selected)<br>Ch2: Database System Concepts and Architecture (selected)<br>Ch5: The Relational Data Model and Relational Database Constraints (introduction) | Syllabus; database purpose, schemas/instances, architecture and data independence; a small student table and identifiers |
| 2 | 2026-09-17 | Ch5: The Relational Data Model and Relational Database Constraints<br>Ch8: The Relational Algebra and Relational Calculus (selected) | Keys and integrity constraints; small-table selection, projection, set operations, product, and joins; key comparison |
| 3 | 2026-09-24 | Ch6: Basic SQL | Create tables, set constraints, query data, and use INSERT/UPDATE/DELETE; verify results |
| 4 | 2026-10-01 | Ch7: More SQL: Complex Queries, Triggers, Views, and Schema Modification (selected) | NULL, aggregation, GROUP BY/HAVING, IN/EXISTS, selected subqueries; verify an AI-generated query |
| 5 | 2026-10-08 | Ch6: Basic SQL (review)<br>Ch7: More SQL: Complex Queries, Triggers, Views, and Schema Modification (selected) | Joins, ON/WHERE, views, constraints, schema changes, and one simple trigger |
| 6 | 2026-10-15 | Ch1-2 and Ch5-8 (taught selections) | Written Exam 1; introductory concepts, relational model, taught algebra, and SQL; corrections |
| 7 | 2026-10-22 | Ch3: Data Modeling Using the Entity-Relationship (ER) Model (selected) | Business rules to ER diagrams: entities, attributes, keys, roles, cardinality, participation, and weak entities |
| 8 | 2026-10-29 | Ch3: Data Modeling Using the Entity-Relationship (ER) Model (continued)<br>Ch9: Relational Database Design by ER- and EER-to-Relational Mapping (9.1) | Multivalued attributes and a simple ternary relationship; complete the seven ER-mapping steps using diagrams and small tables |
| 9 | 2026-11-05 | Ch1-2 and Ch5-8 (review only) | INFORMS travel; asynchronous review of previously taught SQL and concepts; no in-person class, exam, or new content |
| 10 | 2026-11-12 | Ch4: The Enhanced Entity-Relationship (EER) Model (4.1-4.3)<br>Ch9: Relational Database Design by ER- and EER-to-Relational Mapping (9.2.1-9.2.2) | Inheritance, specialization/generalization, membership constraints, hierarchies/lattices and shared subclasses; compare mappings 8A-8D and verify an AI-generated EER design |
| 11 | 2026-11-19 | Ch4: The Enhanced Entity-Relationship (EER) Model (4.4-4.7)<br>Ch9: Relational Database Design by ER- and EER-to-Relational Mapping (9.2.3) | Categories versus shared subclasses; category mappings with same/different keys; EER design choices and formal definitions; UML comparison; introductory abstraction, knowledge representation, and ontology concepts |
| 12 | 2026-11-26 | Ch3, Ch4, and Ch9 (taught selections) | Written Exam 2; taught ER, EER, and mapping; normalization is not yet assessed; corrections |
| 13 | 2026-12-03 | Ch14: Basics of Functional Dependencies and Normalization for Relational Databases (14.1-14.4 selected) | Anomalies, FDs, and 1NF-3NF with supplied candidate keys; compare redesigns; no closure, BCNF, or formal decomposition tests |
| 14 | 2026-12-10 | Ch16: Disk Storage, Basic File Structures, Hashing, and Modern Storage Architectures (background)<br>Ch17: Indexing Structures for Files and Physical Database Design (selected) | Record/block/file background; B+ tree search, composite indexes, read/update costs, and SQLite query-plan evidence; compare an AI index recommendation |
| 15 | 2026-12-17 | Ch20: Introduction to Transaction Processing Concepts and Theory (selected) | One transfer example for ACID, boundaries, and COMMIT/ROLLBACK; one interfering-update diagram; integrated review using earlier SQL, design, normalization, and index examples |
| 16 | 2026-12-24 | Ch14, Ch17, and Ch20 (selected); Ch16 background; cumulative SQL and design | Written Exam 3 / Final Examination; normalization through 3NF, indexes, transactions, and cumulative taught SQL/design; no new required topics |
| 17 | 2026-12-31 | None | University anniversary make-up holiday; no class or new required work |
| 18 | 2027-01-07 | Previously taught sections | Make-up examination, if applicable; eligibility, scope, and arrangements to be announced; no new required topics |

## Assessment

| Assessment | Date | Weight | Scope |
|---|---|---:|---|
| Written Exam 1 | 2026-10-15 | 30% | Selected Chapters 1-2 and 5-8, as taught in Weeks 1-5 |
| Written Exam 2 | 2026-11-26 | 30% | Taught Chapter 3, Sections 4.1-4.7 and 9.1-9.2; ER, EER, and mapping; no normalization |
| Written Exam 3 (Final Examination) | 2026-12-24 | 30% | Selected Sections 14.1-14.4 and Chapters 17 and 20; Chapter 16 background only; cumulative taught SQL and design; no BCNF or formal relational-design algorithms |
| Class Performance | Throughout the semester | 10% | Assigned practice, technical correctness, verification evidence, explanation, and revisions |
| Total | | 100% | |

Week 18 (January 7) is reserved for a make-up examination, not a fourth separately
weighted assessment. The instructor still needs to announce eligibility, scope,
and grading arrangements; this schedule revision does not decide those policies.

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

The instructor updated the travel period to November 1-8 on September 9. November 5
remains asynchronous review only; in-person teaching resumes November 12. The instructor
also moved the course final examination to December 24 (Week 16), with January 7
(Week 18) reserved for a make-up examination. Exams 1 and 2 remain October 15 and
November 26. December 31 remains a holiday. The university's official final-exam
period remains January 4-8; distinguish it from this course's earlier final exam.
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
records the earlier scope's gaps, not a full source audit. Its September 10 notice
identifies the additional Ch4/9.2 coverage still to map. The first-meeting release and
its scoped verification are recorded in
[the release record](course_repository/first_meeting_release.md). Ch5 continuation
and subsequent notebooks still need revision. The reproduced missing-key defect in
the previous ER schema remains a prerequisite fix before that schema is reassigned.
The classroom response system and the actual examination items still need their
separate preparation and review.
