# Database Management

Unified course materials for **Database Management** at National Taipei University of Business.

## Start Here

1. Review the [course schedule](#course-schedule) below.
2. Find the current week and open the linked chapter notebook.
3. Follow the coverage listed for that week. One notebook may continue for two weeks.
4. Run the cells in the order given for that meeting, recording predictions before execution.
5. Retain the evidence requested in the notebook.

For the first meeting, open `ch02.ipynb` and stop at **End of Week 1**. Use the same
notebook for Week 2, starting at **Week 2: Keys and Relational Algebra**.

The schedule, course information, assessment rules, and policies are all included in this
README. The remaining course files are the chapter notebooks.

## Chapter Notebooks

| Notebook | Chapter |
|---|---|
| [ch02.ipynb](ch02.ipynb) | Relational Model |
| [ch03.ipynb](ch03.ipynb) | Introduction to SQL |
| [ch04.ipynb](ch04.ipynb) | Intermediate SQL |
| [ch05.ipynb](ch05.ipynb) | Advanced SQL |
| [ch06.ipynb](ch06.ipynb) | E-R Design |
| [ch07.ipynb](ch07.ipynb) | Normalization |
| [ch14.ipynb](ch14.ipynb) | Indexing |
| [ch15.ipynb](ch15.ipynb) | Query Processing |
| [ch16.ipynb](ch16.ipynb) | Query Optimization |
| [ch17.ipynb](ch17.ipynb) | Transactions |
| [ch18.ipynb](ch18.ipynb) | Concurrency Control |
| [ch19.ipynb](ch19.ipynb) | Recovery |

Each notebook contains its reading, original diagrams, executable SQL or Python
demonstrations, database-creation guidance where applicable, practice, and reproducibility
checks. Images and example data are embedded, so there is no separate lab runner or
required data directory.

## Requirements

- Python 3 with the standard `sqlite3` module.
- SQLite 3.39 or later for the SQL notebooks.
- Jupyter Notebook, JupyterLab, Google Colab, or another compatible notebook interface.
- No server database or third-party Python package.

## Course Schedule

Each chapter has one self-contained notebook. A notebook may be used for more than
one week; follow the coverage in this table rather than looking for a weekly file.

| Week | Date | Topic, notebook, and coverage |
|---:|---|---|
| 1 | 2026-09-10 | **Course Introduction and Relational Structure**<br>Notebook: [CH02 Relational Model](ch02.ipynb)<br>Coverage: Read through End of Week 1: database purpose, one relation, tuples, attributes, domains, schema/instance changes, and why identifiers are needed. Complete the Week 1 response table. |
| 2 | 2026-09-17 | **Keys and Relational Algebra**<br>Notebook: [CH02 Relational Model](ch02.ipynb)<br>Coverage: Begin at Week 2: Keys and Relational Algebra. Superkeys, candidate/primary/composite/foreign keys, schema diagrams, selection, projection, product, join, and set operations; four-table database demonstration. |
| 3 | 2026-09-24 | **Basic SQL**<br>Notebook: [CH03 Introduction to SQL](ch03.ipynb)<br>Coverage: DDL basics; SELECT, FROM, WHERE, aliases, expressions, duplicates, patterns, ordering, and set operations. |
| 4 | 2026-10-01 | **NULL, Aggregation, and Selected Subqueries**<br>Notebook: [CH03 Introduction to SQL](ch03.ipynb)<br>Coverage: Three-valued logic, aggregation, GROUP BY, HAVING, selected subqueries, CTEs, and reversible modifications. |
| 5 | 2026-10-08 | **Intermediate SQL**<br>Notebook: [CH04 Intermediate SQL](ch04.ipynb)<br>Coverage: Explicit and outer joins, ON and WHERE, views, constraints, reference actions, and basic transactions. |
| 6 | 2026-10-15 | **Written Exam 1**<br>Notebook: [CH02 Relational Model](ch02.ipynb), [CH03 Introduction to SQL](ch03.ipynb), [CH04 Intermediate SQL](ch04.ipynb)<br>Coverage: Written Exam 1 on the selected classroom material from Chapters 2-4. |
| 7 | 2026-10-22 | **Selected Advanced SQL**<br>Notebook: [CH05 Advanced SQL](ch05.ipynb)<br>Coverage: Ranking and window functions, recursive CTEs, one audit trigger, and stored-routine purpose and interface. |
| 8 | 2026-10-29 | **E-R Design Foundations**<br>Notebook: [CH06 E-R Design](ch06.ipynb)<br>Coverage: Requirements, entities, attributes, relationships, roles, cardinality, participation, keys, and weak entities. |
| 9 | 2026-11-05 | **Asynchronous Review**<br>Notebook: [CH02 Relational Model](ch02.ipynb), [CH03 Introduction to SQL](ch03.ipynb), [CH04 Intermediate SQL](ch04.ipynb), [CH05 Advanced SQL](ch05.ipynb)<br>Coverage: No class, examination, or new material; asynchronous review while the instructor attends INFORMS. |
| 10 | 2026-11-12 | **E-R Design and Relational Mapping**<br>Notebook: [CH06 E-R Design](ch06.ipynb)<br>Coverage: Redundancy, design choices, E-R-to-relational mapping, keys, foreign keys, and mapped-schema verification. |
| 11 | 2026-11-19 | **Normalization**<br>Notebook: [CH07 Normalization](ch07.ipynb)<br>Coverage: Anomalies, functional dependencies, closure, lossless decomposition, spurious tuples, and introductory 3NF and BCNF. |
| 12 | 2026-11-26 | **Written Exam 2**<br>Notebook: [CH05 Advanced SQL](ch05.ipynb), [CH06 E-R Design](ch06.ipynb), [CH07 Normalization](ch07.ipynb)<br>Coverage: Written Exam 2 on the selected classroom material from Chapters 5-7. |
| 13 | 2026-12-03 | **Indexing**<br>Notebook: [CH14 Indexing](ch14.ipynb)<br>Coverage: Index purpose, B+ tree access, composite-column order, covering indexes, and query-plan evidence. |
| 14 | 2026-12-10 | **Query Processing and Optimization**<br>Notebook: [CH15 Query Processing](ch15.ipynb), [CH16 Query Optimization](ch16.ipynb)<br>Coverage: Scans and searches, join access order, equivalence checks, selectivity, statistics, ANALYZE, and plan interpretation. |
| 15 | 2026-12-17 | **Transactions**<br>Notebook: [CH17 Transactions](ch17.ipynb)<br>Coverage: Transaction boundaries, ACID, states, schedules, conflicts, precedence graphs, recoverability, and isolation phenomena. |
| 16 | 2026-12-24 | **Concurrency Control, Recovery, and Review**<br>Notebook: [CH18 Concurrency Control](ch18.ipynb), [CH19 Recovery](ch19.ipynb)<br>Coverage: S/X locks, grant and wait, deadlock, log records, WAL, simplified redo and undo, and integrated review. |
| 17 | 2026-12-31 | **University Anniversary Make-Up Holiday**<br>Notebook: None<br>Coverage: No class, examination, assignment, or new material. |
| 18 | 2027-01-07 | **Written Exam 3**<br>Notebook: [CH14 Indexing](ch14.ipynb), [CH15 Query Processing](ch15.ipynb), [CH16 Query Optimization](ch16.ipynb), [CH17 Transactions](ch17.ipynb), [CH18 Concurrency Control](ch18.ipynb), [CH19 Recovery](ch19.ipynb)<br>Coverage: Written Exam 3 on selected Chapters 14-19 and cumulative application of taught SQL and database-design concepts. |

## Course Syllabus

Revised: September 5, 2026

### Course Information

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

### Course Objectives

This course develops the core knowledge and practical skills required to use, design, and evaluate relational databases. Students will begin with the relational model, keys, relational algebra, and SQL before progressing to entity-relationship modeling, relational schemas, functional dependencies, normalization, indexing, query processing, transactions, concurrency control, and recovery. By the end of the course, students should be able to write and verify SQL queries, explain query results, construct and evaluate ER diagrams, map an ER model to a relational schema, identify design anomalies, explain how indexes and query plans affect database performance, and analyze transaction and recovery behavior using appropriate technical concepts.

When permitted, students may use AI tools to assist with initial drafts. However, they must be able to verify whether generated SQL is semantically correct, whether a schema contains appropriate keys and constraints, whether ER cardinalities match the stated business rules, and whether database recommendations are supported by query plans and transaction behavior. Students remain responsible for the SQL, models, diagrams, and conclusions they submit.

### Course Content and Teaching Approach

The course combines textbook concepts, worked examples, SQL labs, E-R modeling, database design, query-plan interpretation, and transaction analysis. Classes alternate concept explanation, individual prediction or practice, comparison of solutions, instructor feedback, and revision. Each required topic is supported by an explanation, a complete example, a student exercise, and a stated way to check the result.

Five structured group-response and whole-class comparison activities will be conducted during the semester. They address key and schema decisions, SQL correction, E-R design and schema mapping, normalization, and AI-supported index recommendations. For each activity, every group will submit one response supported by reasons. Responses will be displayed anonymously, each student will compare all responses, and the instructor will correct technical errors before students submit individual revisions.

Comparisons are used to develop judgment and explanation skills. A group's average position will not directly determine its course grade. Class performance will instead be evaluated through assigned work, technical correctness, verification evidence, explanation, and revision following feedback.

SQLite is the required lab environment. Topics that SQLite does not implement or expose fully, including stored routines, server-side isolation behavior, deadlock inspection, and recovery internals, will be taught through conceptual examples, schedules, logs, or verified instructional programs. Students are not required to install a server DBMS.

All official student-facing course materials use English prose and standard database terminology.


### Assessment

| Assessment | Weight | Scope and Abilities Assessed |
|---|---:|---|
| Written Exam 1 | 25% | Core topics from Chapters 2-4: relational model, core relational algebra, SQL queries, joins, views, constraints, and basic transaction statements |
| Written Exam 2 | 25% | Core selected topics from Chapters 5-7: window and recursive SQL, trigger interpretation, E-R modeling, schema mapping, functional dependencies, lossless decomposition, and introductory 3NF/BCNF decisions |
| Written Exam 3 (Final Examination) | 30% | Core selected topics from Chapters 14-19: index and query-plan evidence, transaction schedules, locks and deadlocks, and basic log-based recovery, with cumulative application of taught SQL and database design concepts |
| Class Performance | 20% | Assigned SQL labs, database design exercises, E-R diagrams, relational schemas, normalization exercises, query-plan activities, individual responses, verification evidence, and revisions |
| Total | 100% | |

The three written examinations are completed individually and are used to verify each student's understanding of database concepts, SQL, database design, performance, and transaction processing. Class performance is based on assigned work, technical correctness, verification evidence, explanation, and revisions following feedback. Results from classroom comparisons are used for discussion and do not directly affect grades. Extended topics may be assessed only if they are later taught, practiced, and announced before the examination.

### Use of AI Tools

Students may use AI tools to assist with SQL, E-R diagrams, schemas, or index recommendations only when an activity explicitly permits such use. They must retain the required verification evidence and be able to explain the input, output, revisions, and remaining risks. AI-generated work cannot replace an individual examination, and students must not submit material that they cannot explain or that they have not executed or checked. AI tools are not permitted during the three written examinations; other permitted resources will be announced separately.

### Calendar and Scope Notes

- According to the official university calendar, classes begin on September 7, 2026. The midterm examination period is November 2-6, 2026, and the final examination period is January 4-8, 2027.
- Because the instructor will travel from November 1 through November 7, no synchronous class, examination, or new required content is scheduled for Thursday, November 5.
- December 31 is a university anniversary make-up holiday. Written Exam 3 is scheduled for January 7 during the official final examination week.
- Chapters 8-9 are not part of the required sequence. Selected topics from Chapters 14-19 are included because they support practical understanding of database performance, transaction correctness, concurrency, and recovery.

Official calendar sources:

- National Taipei University of Business Academic Affairs calendar: `https://acad.ntub.edu.tw/p/404-1004-37975.php?Lang=zh-tw`
- Academic Year 115 calendar PDF: `https://acad.ntub.edu.tw/var/file/4/1004/img/1347/780969106.pdf`
