# Database Management Course Plan, Fall 2026

Updated: September 10, 2026. Current scope: Ch1-2 introduction, then Ch3-9 and Ch14-19.
This replaces the earlier SQL-first sequence and the separate Ch20 meeting.
The instructor authorized replanning, synchronizing related files, and commit/push.
The [English syllabus](../Intro%20DB/syllabus.md) remains the concise student version.

## Course Context

- WenYi Lee; second-year Information Management students; required course.
- Three credits; Thursdays, periods 5-7, 1:30-4:15 p.m.
- Elmasri and Navathe, *Fundamentals of Database Systems*, seventh edition, Pearson.
- English student material, instructor-led explanations, many original diagrams,
  small input tables, worked examples, SQL practice, and ER/EER drawing.
- SQLite 3; no server DBMS, paid platform, or application-development project.
- One notebook per chapter; a chapter can span meetings. Ch9 stays one notebook.
- Today's reading is the syllabus and Ch1/Ch2 only. Ch5 is not a first-day assignment.

## Scope and Prerequisites

Teach Ch3 before Ch4, Ch5 before SQL, Ch6 before Ch7, and Ch8 after the SQL examples.
Ch3/Ch4/Ch5 all precede Ch9 mapping. Reuse the same design case rather than
introducing a new project. Ch14 precedes Ch15, and Ch16/Ch17 precede Ch18/Ch19.
Ch8 supplies the logical operations needed for query trees.

## Detailed Coverage

All chapters below are in scope, but only the named selections are required.
Ch3 and Ch4 are core teaching, not optional supplements. Ch15, Ch18, and Ch19
now have explicit required examples; Ch16 is no longer only incidental background.

| Chapter | Required Topics | Limits |
|---|---|---|
| 1-2: Introduction and Architecture | Database purpose; models, schemas, states, data independence, languages, client/server architecture | Introductory selections from 1.1-1.3, 1.6, 2.1-2.3, 2.5; today only |
| 3: ER Model | Entities, attributes, keys, relationships, roles, cardinality, participation, weak entities, multivalued attributes, one ternary example | Core 3.1-3.7 and a simple 3.9 example; use one common diagram; SQL is not prerequisite |
| 4: EER Model | Inheritance; specialization/generalization; predicate-, attribute-, user-defined membership; disjoint/overlapping, total/partial constraints; hierarchies, lattices, shared subclasses, categories, design choices, definitions, UML, abstraction, knowledge representation, ontology concepts | Sections 4.1-4.7; 4.1-4.4 in Week 3, 4.5-4.7 in Week 4; remaining topics introductory, no ontology project |
| 5: Relational Model and Constraints | Relations, tuples, domains, schemas, superkeys, candidate/composite/primary/foreign keys, entity/referential integrity, updates and violations | Core 5.1-5.3 in Week 4; provided SQLite examples demonstrate rules before SQL writing; brief transaction unit from 5.3.4 only |
| 6: Basic SQL | DDL, data types, constraints, SELECT, INSERT/DELETE/UPDATE | Core 6.1-6.4; supply setup and small input tables; assess only practiced statements |
| 7: More SQL | Joins, NULL, GROUP BY/HAVING, IN/EXISTS, selected subqueries, views, one simple trigger, basic schema changes | Selected 7.1-7.4; recursive queries, assertions, advanced triggers, and stored routines excluded |
| 8: Relational Algebra | Selection, projection, rename, compatible set operations, product, condition/equi/natural joins, simple composition | Selected 8.1-8.3 and 8.5; division and relational calculus excluded |
| 9: ER/EER Mapping | Seven ER-mapping steps; specialization options 8A-8D and conditions; shared subclasses; categories with same or different source keys | Sections 9.1-9.2; one diagram with small variants; distinguish modeled rules from SQLite enforcement |
| 14: Dependencies and Normalization | Anomalies, FDs, 1NF/2NF/3NF and a simple BCNF contrast | Selected 14.1-14.5; supplied candidate keys and one common schema; 4NF and 5NF excluded |
| 15: Decomposition Design | One short attribute-closure calculation; lossless join versus spurious tuples; dependency preservation; trace 3NF synthesis using supplied minimal cover and key | Selected 15.1-15.3, including Algorithm 15.4; define minimal cover but do not require deriving it; no inference proofs, general chase, full BCNF algorithm, or 15.4-15.6 |
| 16: Storage and File Organization | Records/blocks, basic buffering, blocking factor, heap/sorted files, static hashing and collision example | Selected 16.1-16.8; simple block-access comparisons; no hardware timing derivations, dynamic-hash algorithms, RAID design, or distributed-storage architecture |
| 17: Indexing and Physical Design | Primary/clustering/secondary and dense/sparse indexes, multilevel search, B+ tree equality/range search, composite keys, read/update costs | Selected 17.1-17.4 and 17.7; one small tree, no full split/merge algorithm; SQLite CREATE INDEX and plan display are implementation supplements |
| 18: Query Processing | SQL-to-algebra translation; scan versus indexed selection; nested-loop versus indexed nested-loop join; overview of sort/hash join and materialization/pipelining | Selected 18.1, 18.3-18.4, 18.7; one two-table query; no external-sort derivations, full join implementations, or parallel algorithms |
| 19: Query Optimization | Query trees, valid selection/projection pushdown, alternative access/join plans, catalog counts, simple equality selectivity, estimated versus measured cost | Selected 19.1-19.3; supplied statistics and two candidate plans; keep join attributes, preserve results, state uniformity assumptions; no dynamic programming, cost-function derivations, Oracle internals, or optimizer implementation |

The expanded scope is broad for the available meetings. Week 11 combines Ch14/Ch15;
Week 15 combines Ch18/Ch19. These are selected teaching units, not claims of
whole-chapter coverage. Ch20-22 are not scheduled; the Ch5 rollback illustration
does not create a separate ACID, concurrency-control, or recovery requirement.

## Teaching and Assessment Alignment

Every required concept needs an explanation, original diagram or small input table,
prediction, worked result, interpretation, limitation, and practice/checking evidence.
Keep theory and SQL implementation claims separate. A successful query execution
does not prove a dependency for every legal state or establish the optimal plan.

Week 2: one ER example includes weak entities, multivalued attributes, and a simple
ternary relationship; postpone relational mapping to Ch9.
Weeks 3-4: complete EER before relational tables. Reuse that diagram for the
remaining EER topics; the Ch5 examples then introduce the different table notation.
Week 5: supplied schema and data let students focus on basic SQL, not an application.
Week 7: reuse that data for complex queries; demonstrate one trigger, not a trigger project.
Week 10: reuse the ER/EER diagram for all mapping options; each variant is a small
comparison, not another lab submission.

Week 11: use one small dependency set and supplied candidate keys to progress through
1NF-3NF and a BCNF contrast. In Ch15, work one short closure, inspect a lossless
versus lossy split, distinguish dependency preservation, and trace Algorithm 15.4
with a supplied minimal cover/key. Reuse those inputs across the explanation and
practice. Do not add deriving a minimal cover, proofs, chase, or general synthesis code.
Only taught and practiced steps are assessed on Exam 2.

Weeks 13-14: connect concrete record/block layouts to file and index choices.
Week 15: one two-table query supports Ch18 execution methods and Ch19 alternative
trees/plans. Supply statistics, compare two alternatives, and verify equivalent
results before discussing cost. Describe sort/hash joins conceptually; do not
require a DBMS implementation. Integrate review into these examples.
Actual classroom pace is unverified. If the selected core still cannot fit, report
the unfinished topics before assigning or examining them; do not silently shift
new teaching into the travel, exam, holiday, or make-up weeks.

Preserve five group comparisons in Weeks 2, 4, 10, 13, and 14: ER constraints,
EER/relational keys, mapping alternatives, file organization, and indexes.
Groups submit reasons; responses are displayed anonymously; each student compares;
the instructor gives technical feedback; students revise individually. Rankings
do not determine grades. Fixed-answer checks need not use group comparisons.
AI activities remain Weeks 4, 10, 14, now checking an EER/constraint claim, a mapping,
and an index recommendation respectively. Do not require SQL before Week 5.

## Weekly Schedule

| Week | Date | Textbook Chapters | Teaching Focus |
|---:|---|---|---|
| 1 | 2026-09-10 | Ch1: Databases and Database Users (selected)<br>Ch2: Database System Concepts and Architecture (selected) | Syllabus, database concepts, schemas, and architecture. |
| 2 | 2026-09-17 | Ch3: Data Modeling Using the Entity-Relationship (ER) Model (selected) | ER diagrams, business rules, weak entities, and relationship constraints. |
| 3 | 2026-09-24 | Ch4: The Enhanced Entity-Relationship (EER) Model (4.1-4.4) | Inheritance, specialization, generalization, constraints, shared subclasses, and categories. |
| 4 | 2026-10-01 | Ch4: The Enhanced Entity-Relationship (EER) Model (4.5-4.7)<br>Ch5: The Relational Data Model and Relational Database Constraints | EER design, UML, abstraction, ontology concepts; relational tables, keys, and constraints. |
| 5 | 2026-10-08 | Ch6: Basic SQL | Create tables; query and update data. |
| 6 | 2026-10-15 | Ch1-6 (taught selections) | Written Exam 1: introduction, ER/EER, relational model, and basic SQL. |
| 7 | 2026-10-22 | Ch7: More SQL: Complex Queries, Triggers, Views, and Schema Modification (selected) | Joins, NULL, aggregation, subqueries, views, schema changes, and a simple trigger. |
| 8 | 2026-10-29 | Ch8: The Relational Algebra and Relational Calculus (selected algebra) | Selection, projection, set operations, products, joins, and query expressions. |
| 9 | 2026-11-05 | Ch1-8 (review only) | INFORMS travel; asynchronous review only. No in-person class or new content. |
| 10 | 2026-11-12 | Ch9: Relational Database Design by ER- and EER-to-Relational Mapping (9.1-9.2) | Map ER/EER diagrams to tables; compare mapping alternatives and constraints. |
| 11 | 2026-11-19 | Ch14: Basics of Functional Dependencies and Normalization for Relational Databases (14.1-14.5 selected)<br>Ch15: Relational Database Design Algorithms and Further Dependencies (15.1-15.3 selected) | Dependencies, normalization through BCNF, and guided decomposition design. |
| 12 | 2026-11-26 | Ch7-9 and Ch14-15 (taught selections) | Written Exam 2: advanced SQL, algebra, mapping, and normalization. |
| 13 | 2026-12-03 | Ch16: Disk Storage, Basic File Structures, Hashing, and Modern Storage Architectures (selected) | Records, blocks, buffering, heap and sorted files, and hashing. |
| 14 | 2026-12-10 | Ch17: Indexing Structures for Files and Physical Database Design (selected) | Ordered indexes, B+ trees, composite indexes, and physical design choices. |
| 15 | 2026-12-17 | Ch18: Strategies for Query Processing (selected)<br>Ch19: Query Optimization (selected) | Query-processing methods, equivalent query trees, plan selection, and integrated review. |
| 16 | 2026-12-24 | Ch16-19 (selected); cumulative SQL and design | Written Exam 3: final examination, including cumulative SQL and design. |
| 17 | 2026-12-31 | None | University anniversary make-up holiday; no class. |
| 18 | 2027-01-07 | Previously taught sections | Make-up examination, if applicable; no new content. |

## Assessment

| Assessment | Date | Weight | Scope |
|---|---|---:|---|
| Written Exam 1 | 2026-10-15 | 30% | Ch1-6: taught introduction, ER/EER, relational model, and basic SQL |
| Written Exam 2 | 2026-11-26 | 30% | Ch7-9 and Ch14-15: taught SQL, algebra, mapping, normalization, and guided decomposition; earlier ER/key concepts as prerequisites |
| Written Exam 3 (Final Examination) | 2026-12-24 | 30% | Ch16-19 selected storage, indexing, processing, and optimization; cumulative taught SQL and design |
| Class Performance | Throughout the semester | 10% | Assigned practice, explanations, verification evidence, and revisions |
| Total | | 100% | |

Week 18 (January 7) is a make-up examination, not a fourth separately weighted assessment.
Eligibility, scope, and grading remain for the instructor to announce.
Exam 2 now includes taught Ch14/Ch15 rather than postponing normalization to Exam 3.
No item-level chapter weights are invented. Prepare and independently check exam
items, solutions, rubrics, permitted resources, and version before release.
Optional content needs teaching, practice, and advance notice before assessment.

## AI Use and Calendar

Written exams are individual and AI-free. Other allowed exam resources remain
to be announced. AI use in designated class activities requires explanation and verification.

Travel is November 1-8, 2026; in-person classes resume November 12.
Week 9 reviews previously taught Ch1-8 only, with no in-person class, exam, or new topic.
Final exam: December 24 (Week 16). Make-up: January 7 (Week 18).
December 31 is the university anniversary make-up holiday. Weeks 16-18 add no new topics.
The university final-exam period is January 4-8; it is distinct from this course's
earlier final. Exams 1 and 2 retain October 15 and November 26.

The [official calendar](https://acad.ntub.edu.tw/var/file/4/1004/img/1347/780969106.pdf)
was rechecked September 10. Semester teaching starts September 7. Listed September
25/28, October 9/26, December 25, and January 1 holidays do not fall on this course's
Thursday meetings. December 31 does and is excluded. The university midterm period
November 2-6 overlaps travel; retain the instructor's existing course exam dates
without claiming institution-wide policy approval.

## Materials Still to Revise

Ch1/Ch2 introductory notebooks are today's material. Ch5 and selected Ch8 notebooks
exist for Weeks 4 and 8; their reading transitions are updated to this sequence.
Ch3 now has one conceptual notebook for Week 2, with 16 original figures, small
synthetic input tables, drawing practice, and the approved comparison activity.
Its [source and verification record](course_repository/ch03_er_release.md) identifies
the taught selections and reading limits. No Ch9 mapping or SQL was added to Ch3.
Ch4 and the remaining prescribed-book notebooks still need revision.
Use the textbook until a corresponding notebook is revised.
Do not assign the twelve old-book notebooks in Intro DB/under_revision or rename
them as if chapter numbers alone establish a match.

Private textbook/assessment files remain excluded. The earlier ER mapping schema's
NULL-key defect must be corrected before reuse. Full chapter source audits, actual
exams, and the classroom response system remain unfinished.
See the [current revision record](course_repository/full_source_audit.md#chapter-order-and-expanded-scope)
for source-reading bounds, edits, checks, and publication evidence.
