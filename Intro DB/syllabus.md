# Database Management Course Syllabus, Fall 2026

Revised: September 9, 2026

## Textbook

| Item | Details |
|---|---|
| Title | *Fundamentals of Database Systems* |
| Authors | Ramez Elmasri and Shamkant B. Navathe |
| Edition | 7th Edition |
| Publisher | Pearson |

All chapter and section references in this syllabus and the current course notebooks
refer to this textbook and edition. The required sections are listed under
[Textbook Coverage](#textbook-coverage) and in the weekly schedule.

## Course Materials

Each chapter uses one notebook, which may continue across meetings. In the first meeting,
begin with this syllabus, then discuss why databases are needed using a small student
table. The instructor will indicate where to stop and resume.

### First Meeting: September 10

After this syllabus, follow the reading order below. These are introductory selections,
not three complete chapters to finish before class. The instructor may stop earlier
and resume at the next meeting. Supplied code lets you observe results; writing SQL
or Python is not a first-meeting requirement.

| Order | Notebook | Textbook selection | Stop at |
|---:|---|---|---|
| 1 | [Chapter 1: Databases and Database Users](ch01.ipynb) | 1.1-1.3 and selected benefits from 1.6 | Chapter Summary |
| 2 | [Chapter 2: Concepts and Architecture](ch02.ipynb) | Introductory concepts from 2.1-2.3 and 2.5 | Chapter Summary |
| 3 | [Chapter 5: Relational Model](ch05.ipynb) | Opening concepts from 5.1 | First-Meeting Summary and Practice |

Formal keys and integrity constraints continue in Chapter 5 at the next meeting;
they are not first-day requirements. Later notebooks are still being revised.
[Previous material](under_revision/) is retained for review, not assigned reading;
its older textbook numbers and assessment references do not govern this course.

### Opening a Notebook

GitHub displays the explanations and saved outputs; it does not execute cells. Download
the notebook and open it in Jupyter Notebook, JupyterLab, or another compatible Python 3
notebook interface to run it and save your responses. Google Colab is another option if
you have access to it; upload the downloaded notebook and save a copy of your work.

Run the cells in the order given for the meeting. Record predictions before running a
cell and compare them with its output. Follow the notebook's restart instructions before
repeating changes. Use Python 3 with its standard `sqlite3` module and SQLite 3.39 or
later. The examples do not require a server database or additional Python data packages;
images and example data are already included in the notebooks.

## Course Information

| Item | Description |
|---|---|
| Academic Term | Fall 2026 (Academic Year 115, Semester 1) |
| Course Title | Database Management |
| Target Students | Second-year undergraduate students in Information Management |
| Credits and Contact Hours | 3 credits; 3 contact hours per week |
| Instructor | WenYi Lee |
| Class Time | Thursdays, Periods 5-7, 1:30-4:15 p.m. |
| Primary Text | Ramez Elmasri and Shamkant B. Navathe, *Fundamentals of Database Systems*, 7th Edition, Pearson |
| Lab Environment | SQLite 3; course materials have been verified with SQLite 3.45.3, and students may use a compatible SQLite interface |

## Course Objectives

This course develops the knowledge and practical skills needed to query and design
relational databases. By the end of the course, students should be able to:

1. Explain database purpose, schemas, database states (also called instances), keys,
   and integrity constraints.
2. Apply core relational-algebra operations to small input tables and explain the results.
3. Create a SQLite database, write SQL queries and updates, and check results involving
   joins, NULL, aggregation, subqueries, views, and constraints.
4. Draw an ER diagram from business rules and map it to tables with appropriate keys
   and constraints, using the ER constructs in Chapter 3 and the mapping in Section 9.1.
5. Identify design anomalies and functional dependencies, apply 1NF through 3NF and
   introductory BCNF, and check simple binary decompositions for a lossless join.
6. Explain basic index choices and interpret evidence of index use in a query plan.
7. Explain ACID, choose transaction boundaries, and analyze simple examples of incomplete
   or interfering updates without implementing concurrency-control or recovery algorithms.

When permitted, students may use AI tools to assist with initial drafts. However, they must be able to verify whether generated SQL is semantically correct, whether a schema contains appropriate keys and constraints, whether ER cardinalities match the stated business rules, and whether database recommendations are supported by query plans and transaction behavior. Students remain responsible for the SQL, models, diagrams, and conclusions they submit.

## Course Content and Teaching Approach

The course emphasizes instructor-led explanation, diagrams, small input tables, and
many simple worked examples. SQL labs and ER drawing exercises connect theory to
observable results. Classes also include individual prediction or practice, comparison
of solutions, instructor feedback, and revision. Each required topic is supported by
an explanation, a complete example, a student exercise, and a way to check the result.

Five structured group-response and whole-class comparison activities will be conducted during the semester. They address key and schema decisions, SQL correction, E-R design and schema mapping, normalization, and AI-supported index recommendations. For each activity, every group will submit one response supported by reasons. Responses will be displayed anonymously, each student will compare all responses, and the instructor will correct technical errors before students submit individual revisions.

Comparisons are used to develop judgment and explanation skills. A group's average position will not directly determine its course grade. Class performance will instead be evaluated through assigned work, technical correctness, verification evidence, explanation, and revision following feedback.

SQLite is the required lab environment. SQL syntax and behavior specific to SQLite
will be distinguished from the textbook's SQL descriptions. Simple transaction
interleavings may be illustrated with tables or diagrams; these illustrations are not
claims about a particular SQLite execution. Students are not required to install a
server DBMS or develop a complete application.

All official student-facing course materials use English prose and standard database terminology.

## Textbook Coverage

The main course chapters are **3, 5, 6, 7, 8, 9, and 14**, within the limits below.
Chapters **1-2** provide the introduction; Chapters **15, 17, and 20** are selected
topics. Chapter **16** supplies only the storage concepts needed to understand indexes.
Listing a chapter does not make every section, exercise, or proof required.

| Chapter | Required Topics | Limits |
|---|---|---|
| 1-2: Introduction and Architecture | Database purpose and benefits; models, schemas, instances, data independence, languages, and basic client/server architecture | Introductory selections from 1.1-1.3, 1.6, 2.1-2.3, and 2.5; no detailed history or system classification |
| 3: ER Model | Entities, attributes, keys, relationships, roles, cardinality, participation, weak entities, and ER design; one simple ternary relationship | Core concepts from 3.1-3.7; a basic example from 3.9; no EER inheritance or UML requirement |
| 5: Relational Model and Constraints | Relations, tuples, domains, schemas, keys, entity integrity, referential integrity, and constraint violations | Core topics from 5.1-5.3 |
| 6: Basic SQL | Data definition, data types, constraints, basic retrieval, and INSERT/DELETE/UPDATE | Core topics from 6.1-6.4, implemented with SQLite |
| 7: More SQL | NULL, joins, aggregation, GROUP BY/HAVING, IN/EXISTS, selected subqueries, views, a simple trigger, and basic schema changes | Selected topics from 7.1-7.4; recursive queries, assertions, and advanced trigger behavior are not required |
| 8: Relational Algebra | Selection, projection, union, intersection, difference, Cartesian product, and joins using small relation instances | Selected operations from 8.1-8.3 and examples from 8.5; division and relational calculus are not required |
| 9: ER-to-Relational Mapping | Regular and weak entities, 1:1/1:N/M:N relationships, multivalued attributes, and one simple ternary relationship | **Section 9.1 only. Section 9.2 and Chapter 4 are not required.** Prerequisites are Chapters 3 and 5 |
| 14: Functional Dependencies and Normalization | Design anomalies, functional dependencies, 1NF, 2NF, 3NF, and introductory BCNF | Selected concepts and examples from 14.1-14.5; 4NF and 5NF are not required |
| 15: Relational Design Theory | Attribute closure, simple candidate-key checks, and binary lossless decomposition with spurious-tuple examples | Selected material from 15.1.1 and 15.2; no formal proofs, minimal-cover procedures, general decomposition tests, or schema-synthesis algorithms |
| 16-17: Storage Foundations and Indexing | Records, blocks, and basic file organization; index purpose, B+ tree search, composite indexes, and read/update costs | Chapter 16 is prerequisite background only; selected concepts from 17.1-17.4 and 17.7, without full tree-update algorithms or cost derivations |
| 20: Transactions | Logical units of work, transaction boundaries, ACID, COMMIT/ROLLBACK, and simple interfering-update examples | Selected concepts from 20.1-20.3 and 20.6; no formal schedule classification, serializability proofs, or implementation protocols |

Chapters 4, 18-19, and 21-22 are not required chapters. SQLite index commands and
basic `EXPLAIN QUERY PLAN` interpretation are practical supplements to Chapter 17,
not a separate course in query optimization. Window functions, recursive CTEs, and
stored routines are optional supplements, not required examination topics.

## Weekly Schedule

Chapter references identify the assigned topics above, not complete chapter coverage.
The first two examinations cover only material taught before their examination dates.
BCNF, attribute closure, and binary lossless-decomposition checks are taught after
Written Exam 2 and belong to Written Exam 3.
Review is integrated into Weeks 13-15. Written Exam 3 takes place in Week 16;
Week 18 is reserved for a make-up examination, not new required content.

| Week | Date | Textbook Chapters | Topics and Activities | Primary Learning Evidence |
|---:|---|---|---|---|
| 1 | September 10, 2026 | Chapters 1-2; Chapter 5 introduction | Syllabus; database purpose, schemas and instances, basic architecture and data independence; a small student table introduces tuples, attributes, domains, and identifiers | Table identification, a prediction, and an explanation or correction |
| 2 | September 17, 2026 | Chapter 5; Chapter 8 selected operations | Candidate, primary, composite, and foreign keys; integrity constraints; selection, projection, set operations, Cartesian product, and joins with small input tables | Key map, algebra results, and individual revision |
| 3 | September 24, 2026 | Chapter 6 | Create a database and tables; constraints; SELECT/FROM/WHERE, expressions, duplicates, patterns, ordering, INSERT/UPDATE/DELETE | SQL statements and verified results |
| 4 | October 1, 2026 | Chapter 7 selected queries | NULL, three-valued logic, aggregation, GROUP BY/HAVING, IN/EXISTS, and selected subqueries; check an AI-generated query | SQL verification table and individual revision |
| 5 | October 8, 2026 | Chapters 6-7 selected topics | Explicit joins, left outer joins, ON versus WHERE, views, constraint checks, basic schema changes, and interpretation of one simple trigger | Join-result comparison, view query, and constraint/trigger explanation |
| 6 | October 15, 2026 | Chapters 1-2, 5-8 selected topics (exam) | Written Exam 1: introductory concepts, relational model, taught relational algebra, and SQL; error analysis and correction | Written Exam 1 and correction sheet |
| 7 | October 22, 2026 | Chapter 3 | Business rules, entities, attributes, keys, relationships, roles, cardinality, and participation; draw an ER diagram | ER diagram draft and reasons for design choices |
| 8 | October 29, 2026 | Chapter 3; Chapter 9 Section 9.1 | Weak entities, multivalued attributes, and a simple ternary relationship; begin mapping regular entities and binary relationships to tables | Annotated ER diagram and initial relational schema |
| 9 | November 5, 2026 | Chapters 1-2, 5-8 selected topics (review only) | Instructor travels abroad to attend INFORMS, November 1-8; no in-person class, examination, or new content. Asynchronous review of previously taught database concepts and SQL | Asynchronous review record |
| 10 | November 12, 2026 | Chapter 9 Section 9.1; Chapter 3 review | Complete ER-to-relational mapping, including weak entities, relationship tables, multivalued attributes, and the taught ternary example; build and check the mapped tables; verify an AI-generated ER diagram | Revised ER diagram, relational schema, SQL, and individual revision |
| 11 | November 19, 2026 | Chapter 14 Sections 14.1-14.4 selected topics | Design anomalies, functional dependencies, and 1NF through 3NF using stated business rules and supplied candidate keys; compare simple redesigns | Dependency table, normalization exercise, and individual revision |
| 12 | November 26, 2026 | Chapter 3; Chapter 9 Section 9.1; Chapter 14 Sections 14.1-14.4 (exam) | Written Exam 2: ER design, ER-to-relational mapping, dependencies, anomalies, and normalization through 3NF; no BCNF, closure, or formal lossless-decomposition test | Written Exam 2 and correction sheet |
| 13 | December 3, 2026 | Chapter 14 Section 14.5; Chapter 15 selected topics | Attribute closure and candidate-key checks; introductory BCNF; binary lossless decomposition and spurious tuples using small tables | Closure calculation, BCNF decision, and decomposition check |
| 14 | December 10, 2026 | Chapter 16 foundations; Chapter 17 selected topics | Records, blocks, and file organization as background; index purpose, B+ tree lookup, composite-column order, and update costs; SQLite index and query-plan examples; check an AI index recommendation | Index choice, before/after query-plan evidence, and individual revision |
| 15 | December 17, 2026 | Chapter 20 selected topics | Transaction boundaries, ACID, and COMMIT/ROLLBACK through one transfer example; one simple interfering-update diagram; distinguish diagrams from actual SQLite behavior. Integrated review of taught SQL, design, normalization, indexes, and transactions | Transaction-boundary decisions, explained results, and review corrections |
| 16 | December 24, 2026 | Chapter 14 Section 14.5; Chapters 15-17 and 20 selected topics (exam); cumulative application | Written Exam 3 and course final examination: taught closure, BCNF, binary lossless decomposition, indexing, and transaction concepts; Chapter 16 only as index background; cumulative SQL and database design application. No new required topics | Written Exam 3 |
| 17 | December 31, 2026 | None | University anniversary make-up holiday; no class | None |
| 18 | January 7, 2027 | Previously taught sections only (make-up) | Make-up examination, if applicable; eligibility, scope, and arrangements will be announced separately. No new required topics | Make-up examination, if applicable |

## Assessment

| Assessment | Weight | Scope and Abilities Assessed |
|---|---:|---|
| Written Exam 1 | 30% | Selected Chapters 1-2 and 5-8: database concepts, relational model and constraints, taught relational algebra, SQL queries and updates, joins, views, and simple trigger interpretation |
| Written Exam 2 | 30% | Chapter 3, Section 9.1, and selected Sections 14.1-14.4: ER modeling, schema mapping, functional dependencies, anomalies, and normalization through 3NF; no Chapter 4 or Section 9.2 |
| Written Exam 3 (Final Examination) | 30% | Section 14.5 and selected Chapters 15, 17, and 20, with Chapter 16 background only: closure, BCNF, binary lossless decomposition, indexes, query-plan evidence, and transaction basics; cumulative application of taught SQL and database design |
| Class Performance | 10% | Assigned SQL labs, database design exercises, ER diagrams, relational schemas, normalization exercises, query-plan activities, individual responses, verification evidence, and revisions |
| Total | 100% | |

Written examinations are scheduled for October 15 (Week 6), November 26 (Week 12),
and December 24 (Week 16). The make-up examination is scheduled for January 7
(Week 18); it is not a fourth separately weighted assessment. Make-up eligibility,
scope, and grading arrangements will be announced separately.

Each written examination contributes 30% of the final grade; together they contribute
90%. Class performance contributes the remaining 10%. The examinations are completed
individually. Class performance is based on assigned work, technical correctness,
verification evidence, explanation, and revisions following feedback. Classroom
comparison rankings do not directly affect grades. Only work assigned for submission
is graded. Extended topics may be assessed only if they are later taught, practiced,
and announced before the examination.

## Use of AI Tools

Students may use AI tools to assist with SQL, E-R diagrams, schemas, or index recommendations only when an activity explicitly permits such use. They must retain the required verification evidence and be able to explain the input, output, revisions, and remaining risks. AI-generated work cannot replace an individual examination, and students must not submit material that they cannot explain or that they have not executed or checked. AI tools are not permitted during the three written examinations; other permitted resources will be announced separately.

## Calendar and Scope Notes

- According to the official university calendar, classes begin on September 7, 2026. The midterm examination period is November 2-6, 2026, and the final examination period is January 4-8, 2027.
- The instructor will be abroad from November 1 through November 8, 2026, to attend INFORMS. No synchronous class, examination, or new required content is scheduled for Thursday, November 5. In-person classes resume on Thursday, November 12.
- This course's Written Exam 3 is scheduled for December 24 (Week 16), before the university's official final examination period. December 31 is a university anniversary make-up holiday. January 7 (Week 18), within the official final examination period, is reserved for a make-up examination.
- Chapter 8 is limited to the listed relational-algebra operations. Chapter 9 is limited to Section 9.1; Chapter 4 and Section 9.2 are not required.
- Chapter 16 provides index prerequisites only. Chapters 18-19 and 21-22 are not required, and Week 16 adds no new content.

Official calendar sources:

- [National Taipei University of Business Academic Affairs calendar](https://acad.ntub.edu.tw/p/404-1004-37975.php?Lang=zh-tw)
- [Academic Year 115 calendar PDF](https://acad.ntub.edu.tw/var/file/4/1004/img/1347/780969106.pdf)

Practical reference:

- [SQLite: EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)
