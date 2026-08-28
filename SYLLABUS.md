# Database Management Course Syllabus, Fall 2026

Revised: August 27, 2026

## Course Information

| Item | Description |
|---|---|
| Academic Term | Fall 2026 (Academic Year 115, Semester 1) |
| Course Title | Database Management |
| Target Students | Second-year undergraduate students in Information Management |
| Credits and Contact Hours | 3 credits; 3 contact hours per week |
| Instructor | WenYi Lee |
| Class Time | Thursdays, Periods 5-7, 1:30-4:15 p.m. |
| Primary Text | *Database System Concepts*, 7th Edition |
| Lab Environment | SQLite 3; course materials have been verified with SQLite 3.45.3, and students may use a compatible SQLite interface |

## Course Objectives

This course develops the core knowledge and practical skills required to use, design, and evaluate relational databases. Students will begin with the relational model, keys, relational algebra, and SQL before progressing to entity-relationship modeling, relational schemas, functional dependencies, normalization, indexing, query processing, transactions, concurrency control, and recovery. By the end of the course, students should be able to write and verify SQL queries, explain query results, construct and evaluate ER diagrams, map an ER model to a relational schema, identify design anomalies, explain how indexes and query plans affect database performance, and analyze transaction and recovery behavior using appropriate technical concepts.

When permitted, students may use AI tools to assist with initial drafts. However, they must be able to verify whether generated SQL is semantically correct, whether a schema contains appropriate keys and constraints, whether ER cardinalities match the stated business rules, and whether database recommendations are supported by query plans and transaction behavior. Students remain responsible for the SQL, models, diagrams, and conclusions they submit.

## Course Content and Teaching Approach

The course combines textbook concepts, worked examples, SQL labs, E-R modeling, database design, query-plan interpretation, and transaction analysis. Classes alternate concept explanation, individual prediction or practice, comparison of solutions, instructor feedback, and revision. Each required topic is supported by an explanation, a complete example, a student exercise, and a stated way to check the result.

Five structured group-response and whole-class comparison activities will be conducted during the semester. They address key and schema decisions, SQL correction, E-R design and schema mapping, normalization, and AI-supported index recommendations. For each activity, every group will submit one response supported by reasons. Responses will be displayed anonymously, each student will compare all responses, and the instructor will correct technical errors before students submit individual revisions.

Comparisons are used to develop judgment and explanation skills. A group's average position will not directly determine its course grade. Class performance will instead be evaluated through assigned work, technical correctness, verification evidence, explanation, and revision following feedback.

SQLite is the required lab environment. Topics that SQLite does not implement or expose fully, including stored routines, server-side isolation behavior, deadlock inspection, and recovery internals, will be taught through conceptual examples, schedules, logs, or verified instructional programs. Students are not required to install a server DBMS.

All official student-facing course materials use English prose and standard database terminology.

## Weekly Schedule

| Week | Date | Topics and Activities | Primary Learning Evidence |
|---:|---|---|---|
| 1 | September 10, 2026 | Course introduction; database systems, relations, tuples, attributes, schemas, and domains | Schema and key identification sheet |
| 2 | September 17, 2026 | Primary, candidate, and foreign keys; schema diagrams; core relational-algebra operations using small relation instances | Key map, relational-algebra results, and individual revision |
| 3 | September 24, 2026 | SQL DDL basics; `SELECT`, `FROM`, `WHERE`, expressions, duplicates, string patterns, and ordering | SQL file and verified query results |
| 4 | October 1, 2026 | `NULL`, three-valued logic, aggregation, `GROUP BY`, `HAVING`, `IN`, `EXISTS`, and selected subqueries; verification of AI-generated SQL | SQL verification table and individual revision |
| 5 | October 8, 2026 | Explicit joins, left outer joins, `ON` and `WHERE`, views, integrity constraints, and basic transaction statements | SQL and constraint exercise |
| 6 | October 15, 2026 | Written Exam 1: Chapters 2-4; error analysis and correction | Written Exam 1 and correction sheet |
| 7 | October 22, 2026 | Selected Chapter 5 topics: window ranking, recursive CTEs, one row-level audit trigger, and the purposes of stored routines | Advanced SQL exercise and execution evidence |
| 8 | October 29, 2026 | Entities, attributes, relationships, cardinality, participation, and keys in the E-R model | E-R diagram draft |
| 9 | November 5, 2026 | Instructor travel, November 1-7; no in-person class, examination, or new content. Asynchronous review of Chapters 2-5 and an individual SQL and concept check | Asynchronous review record |
| 10 | November 12, 2026 | E-R design decisions, redundancy, E-R-to-relational mapping, and verification of an AI-generated E-R diagram | Revised E-R diagram, relational schema, and individual revision |
| 11 | November 19, 2026 | Design anomalies, functional dependencies, attribute closure, binary lossless decomposition, and introductory 3NF/BCNF decisions | Functional-dependency table, decomposition exercise, and individual revision |
| 12 | November 26, 2026 | Written Exam 2: selected topics from Chapters 5-7; error analysis and correction | Written Exam 2 and correction sheet |
| 13 | December 3, 2026 | Index use, B+ tree equality and range access, composite-column order, covering indexes, and query-plan evidence | Index design and before/after query-plan evidence |
| 14 | December 10, 2026 | Scans and index searches, query-plan access order, result-equivalence checks, basic selectivity, catalog statistics, `ANALYZE`, and verification of an AI index recommendation | Query-plan interpretation and individual revision |
| 15 | December 17, 2026 | Transaction boundaries, ACID properties, schedules, conflicts, small precedence graphs, basic recoverability, and isolation phenomena | Transaction and isolation analysis |
| 16 | December 24, 2026 | S/X lock compatibility, grant-or-wait decisions, wait-for graphs and deadlocks; log records, write-ahead logging, one simplified redo/undo case, and comprehensive review | Concurrency and recovery analysis; final review record |
| 17 | December 31, 2026 | University anniversary make-up holiday; no class | None |
| 18 | January 7, 2027 | Written Exam 3 and course final examination: selected topics from Chapters 14-19, with cumulative application of SQL and database design concepts | Written Exam 3 |

## Assessment

| Assessment | Weight | Scope and Abilities Assessed |
|---|---:|---|
| Written Exam 1 | 25% | Core topics from Chapters 2-4: relational model, core relational algebra, SQL queries, joins, views, constraints, and basic transaction statements |
| Written Exam 2 | 25% | Core selected topics from Chapters 5-7: window and recursive SQL, trigger interpretation, E-R modeling, schema mapping, functional dependencies, lossless decomposition, and introductory 3NF/BCNF decisions |
| Written Exam 3 (Final Examination) | 30% | Core selected topics from Chapters 14-19: index and query-plan evidence, transaction schedules, locks and deadlocks, and basic log-based recovery, with cumulative application of taught SQL and database design concepts |
| Class Performance | 20% | Assigned SQL labs, database design exercises, E-R diagrams, relational schemas, normalization exercises, query-plan activities, individual responses, verification evidence, and revisions |
| Total | 100% | |

The three written examinations are completed individually and are used to verify each student's understanding of database concepts, SQL, database design, performance, and transaction processing. Class performance is based on assigned work, technical correctness, verification evidence, explanation, and revisions following feedback. Results from classroom comparisons are used for discussion and do not directly affect grades. Extended topics may be assessed only if they are later taught, practiced, and announced before the examination.

## Use of AI Tools

Students may use AI tools to assist with SQL, E-R diagrams, schemas, or index recommendations only when an activity explicitly permits such use. They must retain the required verification evidence and be able to explain the input, output, revisions, and remaining risks. AI-generated work cannot replace an individual examination, and students must not submit material that they cannot explain or that they have not executed or checked. AI tools are not permitted during the three written examinations; other permitted resources will be announced separately.

## Calendar and Scope Notes

- According to the official university calendar, classes begin on September 7, 2026. The midterm examination period is November 2-6, 2026, and the final examination period is January 4-8, 2027.
- Because the instructor will travel from November 1 through November 7, no synchronous class, examination, or new required content is scheduled for Thursday, November 5.
- December 31 is a university anniversary make-up holiday. Written Exam 3 is scheduled for January 7 during the official final examination week.
- Chapters 8-9 are not part of the required sequence. Selected topics from Chapters 14-19 are included because they support practical understanding of database performance, transaction correctness, concurrency, and recovery.

Official calendar sources:

- National Taipei University of Business Academic Affairs calendar: `https://acad.ntub.edu.tw/p/404-1004-37975.php?Lang=zh-tw`
- Academic Year 115 calendar PDF: `https://acad.ntub.edu.tw/var/file/4/1004/img/1347/780969106.pdf`
