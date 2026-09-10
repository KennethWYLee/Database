# Prescribed Textbook and Existing Material Correspondence

## Current Chapter Order

September 10, 2026: the instructor now requires today's Ch1/Ch2 only, followed
by Ch3-9 and Ch14-19 in order. Ch3/Ch4 remain required; Ch15/Ch18/Ch19 are
restored as selected teaching, and Ch20 is not scheduled. Ch5/Ch8 move to Weeks
4/8. Earlier dates, scope exclusions, and first-meeting directions below are
historical where they conflict. See the
[current revision record](full_source_audit.md#chapter-order-and-expanded-scope).
This schedule change does not complete the remaining prescribed-book notebooks.

Reviewed: September 8, 2026. Repository baseline: `a9bc1a8`, branch `main`.
This record reviews the existing uncommitted version, not only that commit.

This is the correspondence snapshot before the subsequent first-meeting release.
Its source hashes and missing-introduction findings describe that earlier version.
See [the first-meeting release record](first_meeting_release.md) for the later Ch1/Ch2/Ch5
opening work; the remaining chapter gaps and ER schema defect are still outstanding.

## September 10 Relational Foundations Update

The Ch5 continuation and separate Ch8 algebra notebook now supersede their earlier
missing-material findings. Ch1/Ch2 remain introductory selections. See the
[topic-by-topic record](full_source_audit.md#relational-foundations-revision)
for assigned-scope source locations, original examples, and verification.
Other gaps, including the old ER schema defect, remain unresolved.

## September 10 EER Schedule Update

The instructor requested full EER teaching and chapter numbers with textbook titles.
The current plan now includes Ch4 Sections 4.1-4.7 and Ch9 Sections 9.1-9.2 in the
Weeks 7-11 design sequence. Normalization through 3NF moves to Week 13 and Exam 3;
Exam 2 covers taught ER, EER, and mapping. BCNF and Ch15 are now optional.
Dates, travel, holidays, and 30/30/30/10 weights are unchanged.

The older scope and correspondence below are historical where they conflict with
this update. Ch4/9.2 still need a complete teaching-point correspondence and source
audit; no newly assigned EER notebook is claimed complete. Complete prescribed-book
chapter audits remain zero. See [the revision record](full_source_audit.md#eer-schedule-revision-record)
for the bounded source checks and schedule verification. The instructor subsequently authorized synchronizing the related local files and
committing and pushing this revision to the existing origin/main. Older no-publication
statements below describe their original audit steps.

## Conclusion and Limits

The approved syllabus can use substantial parts of the existing SQL, algebra, ER,
index, and transaction examples. It cannot use the existing notebook chapter numbers
as references to the prescribed textbook. Introductory architecture, stepwise
normalization, and parts of ER mapping need additional teaching material.

This is a **topic correspondence and gap review**, not a complete source audit or a
student-ready declaration. Complete chapter audits of the prescribed book remain
**zero**. No notebook, SQL source, figure, build configuration, assessment, or schedule
was changed during this step. No files were staged, committed, or pushed.

Authority: [current syllabus](../../Intro%20DB/syllabus.md),
[course plan](../COURSE_PLAN.md), and [current decisions](../../PROJECT.md).
All new chapter references below mean Elmasri and Navathe, *Fundamentals of Database
Systems*, seventh edition. The private source is
`private_references/book_Fundamental of Database Systems.pdf`; it is not a public
download and must not be included in a notebook or package.

The word **existing** identifies located content, not verified alignment. An item
marked **reuse after revision** has an explanation or example worth retaining;
its new source citations, context, exercises, and outputs still require verification.
**Add** means a complete treatment was not located in the inspected maintained
sources. It does not mean the concept is absent from every private historical file.

Each completed topic must ultimately have a plain-language explanation, a small
original example, a checkable prediction, a diagram or executable/checkable operation,
result interpretation, a limitation or counterexample, and a practice response to
retain. Each chapter also needs a summary and prerequisite/next-chapter connections.
The tables below identify what can supply those elements and what still needs work;
they do not certify all those elements as complete.

## Source Reading and Locators

Printed pages and one-based PDF pages are distinguished below. Section-start
locators were checked against the PDF outline. A section locator is a place to
continue reading, **not evidence that the entire section has been read**.

The body passages inspected for this correspondence include printed pp.4, 6,
10-12, 17-18, 32-41, 46-49, 63, 65, 73, 79, 88-89, 475-477, 479-481,
483-484, 487, 489, 517-518, 619-620, 622-623, 758, and 773-774.
These correspond to PDF pp.35, 37, 41-43, 48-49, 63-72, 77-80, 94, 96,
104, 110, 119-120, 506-508, 510-512, 514-515, 518, 520, 548-549,
650-651, 653-654, 789, and 804-805. This was text inspection; it is not a
complete visual check of those textbook figures. Earlier bounded reading of mapping,
closure, decomposition, indexing, and transactions remains recorded in
[the audit progress record](full_source_audit.md).

Full source comparison remains outstanding for every chapter, including the SQL and
algebra topics whose existing examples are substantial. No old-book page numbers in
`simple_examples.py` or a guide should be replaced without reading the corresponding
new-book passage. Original teaching data must not be described as the book's COMPANY
or UNIVERSITY example.

## Chapters 1-2: Introduction

Week 1; Exam 1. Existing source:
[old Ch2 guide](../chapters/ch02_relational_model/student_guide.md), especially
`Why Keep a Database?`, `Worked Example: Two Copies Disagree`, and
`Comparing the Three Changes`.

| Required topic and source locator | Existing explanation, example, or figure | Required action |
|---|---|---|
| Database, DBMS, and database system; 1.1-1.2, section starts printed 4/6, PDF 35/37 | Database/DBMS explanation; conflicting email input table and practice; `ch02_files`, `ch02_dbms` | Reuse after revision. Add a clearly labeled database-system diagram including software and data; do not imply every database must be a server or that software establishes factual truth. |
| Characteristics and benefits; 1.3 and 1.6, printed 10/17, PDF 41/48 | Shared email example explains one redundancy problem | Add short catalog/metadata and different-user-view examples. Show a schema description beside actual rows, and two views of the same underlying facts. Existing email consistency alone does not cover self-description, independence, or multiple views. |
| Models, schema, and database state; 2.1, printed 32, PDF 63 | Row/value/schema changes with preserved outputs; `ch02_changes` | Reuse state-change examples. Add one conceptual/relational/physical representation comparison. Introduce the book's preferred term database state or snapshot and explain the existing use of instance; avoid treating these as incompatible facts. |
| Three-schema architecture and data independence; 2.2, printed 36, PDF 67 | Schema changes are demonstrated, but no full three-schema or independence example was located | Add external/conceptual/internal diagrams and one logical versus one physical change with explicit unchanged interfaces. Adding a column alone does not demonstrate that every application is unaffected. |
| Database languages; 2.3, printed 38, PDF 69; DDL/DML body printed 39-40, PDF 70-71 | Supplied CREATE/SELECT/INSERT/UPDATE examples exist in the opening guide and old SQL guide | Reuse a few statements as illustrations, not an early syntax assessment. Distinguish defining structure from retrieving/changing values; no extra language taxonomy exercise is needed. |
| Basic client/server architecture; 2.5, printed 46, PDF 77 | Python-to-SQLite explanation, but no complete client/server comparison | Add a request/result diagram and explicitly distinguish the provided embedded SQLite environment from a server DBMS. Do not turn this into web-system development or require server installation. |

## Chapter 5: Relational Model and Constraints

Weeks 1-2; Exam 1. Existing source:
[old Ch2 guide and inline examples](../chapters/ch02_relational_model/student_guide.md),
[setup SQL](../chapters/ch02_relational_model/course_registration_setup.sql), and
[algebra SQL](../chapters/ch02_relational_model/student_lab.sql).

| Required topic and source locator | Existing explanation, example, or figure | Required action |
|---|---|---|
| Relation, tuple, attribute, domain, schema, and state; 5.1, printed 150, PDF 181 | `Reading a Relation`, domains, atomic values, same-name students, phone example; `ch02_table_anatomy`, `ch02_domains`, `ch02_phones` | Reuse after source/terminology revision. Preserve the small input tables and predictions. Distinguish formal relations from unrestricted SQL tables and a domain from values merely observed in a sample. |
| Tuple order, repeated values, and duplicate tuples; 5.1 | Two display orders and DISTINCT comparison; `ch02_order`, `ch02_duplicates` | Reuse. Make clear that query deduplication does not remove stored duplicates, and that explicit SQL ordering is a display request. |
| Candidate, primary, composite keys and superkeys; 5.2, printed 157, PDF 188 | `Keys`, Student and cross-term Enrollment examples; `ch02_keys`, `ch02_composite` | Reuse stated business rules, minimality counterexamples, and rejected inserts. Change old-book references; do not infer a key solely from uniqueness in four rows. Formal definitions remain Week 2. |
| Entity integrity and referential integrity; 5.2 | Missing/repeated key and nonexistent LAW department tests; `ch02_references` | Reuse the corrected old Ch2 implementation. Contrast a missing key, a duplicate key, and a missing referenced row; check each rule separately. |
| INSERT/DELETE/UPDATE violations; 5.3, printed 165, PDF 196 | Insert rejection in old Ch2; delete/cascade/update cases in old SQL guides | Combine small before/request/after tables to cover all three operations. Reuse SQL as supplied observation code before students are asked to author it. Do not introduce formal transaction theory here. |

## Chapter 6: Basic SQL

Week 3 and selected Week 5 checks; Exam 1. Existing sources:
[old Ch3 guide](../chapters/ch03_introduction_to_sql/student_guide.md),
[old Ch3 lab](../chapters/ch03_introduction_to_sql/student_lab.sql),
[old Ch4 constraints](../chapters/ch04_intermediate_sql/student_guide.md), and
[small examples](simple_examples.py).

| Required topic and source locator | Existing explanation, example, or figure | Required action |
|---|---|---|
| Create and inspect a database/table; 6.1, printed 179, PDF 210 | Existing notebook setup plus `Defining Structure`; `ch03_small_definition` | Reuse, but introduce connection, table creation, inserted input rows, schema inspection, and first SELECT in reading order. Explain memory-only versus saved-file use without requiring a new service. |
| Data types and constraints; 6.1-6.2, printed 179/184, PDF 210/215 | Capacity/range examples, explicit NOT NULL, `ch04_small_constraints`, `ch04_small_cascade` | Reuse after checking all copied schemas. INTEGER affinity is not a whole-number guarantee in an ordinary SQLite table. NULL primary-key finding below must be fixed before the affected ER schema is reused. |
| SELECT/FROM/WHERE, expressions, aliases, and duplicates; 6.3, printed 187, PDF 218 | `Basic Queries`, `Duplicates and Expressions`; `ch03_small_filter`, `ch03_small_distinct` | Reuse input-to-output examples and prediction questions; replace old chapter locators. Preserve distinction between computed output and UPDATE. |
| Patterns, ranges, and ordering; 6.3 | LIKE/BETWEEN/ORDER examples; `ch03_small_patterns` | Reuse; retain explicit ordering and product-specific LIKE qualifications. Match each exercise to its displayed input rows. |
| SQL set operations; 6.3, with algebra in 8.2 | `SQL Set Operations`; `ch03_small_sets` | Reuse as the SQL expression of previously taught operations, not a second introduction. Contrast UNION and UNION ALL; show why reversing EXCEPT changes the answer. |
| INSERT/DELETE/UPDATE; 6.4, printed 198, PDF 229 | `Data Modification`; `ch03_small_modify`, lab modifications | Reuse, showing target rows before each change and observed rows afterward. Supplied savepoints are reset machinery here, not a new required early transaction topic. |

## Chapter 7: More SQL

Weeks 4-5; Exam 1. Existing sources:
[old Ch3 guide](../chapters/ch03_introduction_to_sql/student_guide.md),
[old Ch4 guide](../chapters/ch04_intermediate_sql/student_guide.md),
[old Ch5 trigger section](../chapters/ch05_advanced_sql/student_guide.md), and
[old Ch2 schema-change example](../chapters/ch02_relational_model/student_guide.md).

| Required topic and source locator | Existing explanation, example, or figure | Required action |
|---|---|---|
| NULL and three-valued logic; 7.1, printed 207, PDF 238 | NULL predicates and truth discussion; `ch03_null` | Reuse, retaining a concrete unknown grade and comparison output. Connect WHERE rejection of UNKNOWN to later NOT IN and outer-join examples. |
| Aggregates, GROUP BY/HAVING; 7.1 | Empty/nonempty aggregate cases, `Aggregation and Grouping`; `ch03_groups`, `ch04_small_outer_count` | Reuse. Teach COUNT(*) versus COUNT(column), NULL handling, and row filtering versus group filtering with small tables before query variations. |
| IN/EXISTS and selected subqueries; 7.1 | IN, correlated EXISTS, NOT IN with NULL; `ch03_small_subquery` | Reuse. Trace one named outer row and compare an extra matching inner row. Optional CTE material must not become a hidden prerequisite. |
| Inner joins, left joins, ON versus WHERE; 7.1 | Worked joins and unmatched course; `ch04_small_inner`, `ch04_small_natural`, `ch04_outer`, `ch04_filters` | Reuse. Keep unmatched rows visible and compare complete result tables. USING/NATURAL material is supporting explanation, not an expansion into every SQL join variant. |
| Views; 7.3, printed 228, PDF 259 | `Views`, base-row change and view output; `ch04_small_view` | Reuse basic CREATE VIEW/query/update-of-base demonstration. Do not require INSTEAD OF triggers or general view-update theory. |
| One simple trigger; 7.2, printed 225, PDF 256 | `Row-Level Audit Trigger`; `ch05_trigger`, `ch05_small_trigger_null` | Reuse one grade-change example after NULL has been taught. Explain event, old/new values, action, and unchanged-grade case. Label SQLite syntax; no stored-function/procedure prerequisite or assertion implementation. |
| Basic schema changes; 7.4, printed 232, PDF 263 | Old Ch3 has brief prose; old Ch2 actually executes ADD COLUMN with a default | Reuse the existing small ALTER TABLE example instead of falsely treating the topic as entirely missing. Add syntax explanation and before/after schema/data checks for Week 5; qualify SQLite capabilities. |

## Chapter 8: Relational Algebra

Week 2; Exam 1. Existing source:
[old Ch2 guide](../chapters/ch02_relational_model/student_guide.md), its inline SQL,
and [original algebra figures](teaching_figures.py).

| Required topic and source locator | Existing explanation, example, or figure | Required action |
|---|---|---|
| Selection and projection; 8.1, printed 241, PDF 272 | `Selection`, `Projection`, `Composition`; `ch02_selection`, `ch02_projection`, `ch02_composition` | Reuse. Map symbols to the new book and retain hand-computed intermediate tables. SQL used for projection must retain the intended set semantics. |
| Union/intersection/difference; 8.2, printed 246, PDF 277 | `Set Operations`; `ch02_sets` | Reuse compatible-input examples and reversed-difference check. Define compatibility before using the operation. |
| Cartesian product and joins; 8.2-8.3, printed 246/251, PDF 277/282 | `Cartesian Product`, `Theta Join`; `ch02_product`, `ch02_join` | Reuse pair enumeration and selected matches; explain how natural/equijoin cases fit without adding division. |
| A composed query; 8.5, printed 265, PDF 296 | `ch02_algebra_pipeline` and composition SQL | Adapt the original course example to the assigned operators and new-book notation. Do not present it as a reproduced textbook exercise. Rename/assignment and equivalence proofs remain outside the required core. |

## Chapter 3: ER Design

Weeks 7-8; Exam 2. Existing source:
[old Ch6 guide](../chapters/ch06_er_design/student_guide.md),
[business rules](../chapters/ch06_er_design/course_registration_rules.md), and
[small examples](simple_examples.py).

| Required topic and source locator | Existing explanation, example, or figure | Required action |
|---|---|---|
| Requirements and conceptual design; 3.1-3.2, printed 60/62, PDF 91/93 | `Design Stages`, `Redundancy and Incompleteness`; `ch06_small_stages`, `ch06_small_separate` | Reuse the original registration case. Keep an entity diagram distinct from an implemented table diagram; identify constraints supplied by the case rather than inferred from sample rows. |
| Entities, entity types/sets, attributes, keys; 3.3, printed 63, PDF 94 | `Entities and Attributes`; `ch06_small_attributes` | Revise terminology to distinguish one entity, its entity type, and the current entity set. Retain simple/composite, multivalued, stored/derived examples; do not merely replace every occurrence of set with type. |
| Relationships, degree, and roles; 3.4, printed 72, PDF 103 | `Relationships, Roles, and Degree`; `ch06_small_roles` | Reuse recursive prerequisite roles and binary examples. Explain a relationship instance versus its type. Ternary explanation is only a paragraph and needs the complete example below. |
| Cardinality and participation; 3.4 | Department/Student min-max example; `ch06_cardinality` | Reuse business rules and directional reading. Add a consistent legend for the new book's ER notation; show legal and illegal small populations, not just arrows or unexplained min-max labels. |
| Weak entities and partial keys; 3.5, printed 79, PDF 110 | Course/Section owner and identifying relationship; `ch06_small_weak` | Reuse, replacing the primary explanatory term discriminator with the book's ER term partial key. Explain why existence dependency alone does not make an entity weak; preserve composite owner/term/section identity. |
| Refine and draw an ER model; 3.6-3.7, printed 80/81, PDF 111/112 | Design choices, full case, existing mapping diagram | Revise into requirements-to-ER practice before mapping is assessed. Supply an interpretable ER legend, a worked design, and a separate small practice case. Do not require UML or EER. |
| One simple ternary relationship; 3.9, printed 88, PDF 119 | Brief Instructor/Student/Project sentence, no complete ternary input-to-diagram treatment located | Add a few explicitly permitted triples, a ternary diagram, and a prediction about a missing triple. Show why three pairwise facts do not necessarily establish that triple. Reuse this exact case in 9.1 rather than adding a second case. |

## Chapter 9: ER-to-Relational Mapping

Weeks 8 and 10; Exam 2. **Section 9.1 only**; Ch3 and Ch5 are prerequisites.
The section starts at printed p.290 / PDF p.321 and ends before 9.2 at printed p.298 /
PDF p.329. Existing source:
[old Ch6 Mapping to Relations](../chapters/ch06_er_design/student_guide.md) and
[mapped schema SQL](../chapters/ch06_er_design/mapped_schema.sql).

| Required topic and source locator | Existing explanation, example, or figure | Required action |
|---|---|---|
| Regular entities; 9.1 Step 1 | `Strong Entity and Complex Attributes`, department/student/course tables | Reuse flattened attributes and keys after the NULL-primary-key defect is fixed. Add diagram-to-columns annotations and candidate-key checks. |
| Weak entities; 9.1 Step 2 | `Weak Entity`, section table, `ch06_mapping` | Reuse owner key plus partial key. Test missing owner, repeated complete identity, and the same section number under a different owner/term. |
| Binary 1:1; 9.1 Step 3 | Old Ch4 feedback uniqueness provides only a constraint fragment; no full 1:1 mapping lesson located | Add one case with stated participation, a chosen FK location, UNIQUE, and NOT NULL where warranted. Show what those constraints enforce and what they do not; a FK alone does not establish 1:1 or total participation on both sides. |
| Binary 1:N; 9.1 Step 4 | `One-to-Many Relationship`, student's department FK | Reuse. Place the FK on the many side and distinguish optional from required participation. Show one rejected reference and one permitted repeated department. |
| Binary M:N; 9.1 Step 5 | `Many-to-Many Relationship`, enrollment; `ch06_small_many` | Reuse complete section identity and the relationship attribute grade. Keep course-versus-section business rules consistent across the ER model and SQL. |
| Multivalued attributes; 9.1 Step 6 | `student_phone` and composite primary key | Reuse with a tiny owner/phone input table. Retain no-phone and duplicate-phone cases; do not store a comma-separated phone list as the mapped attribute. |
| One ternary relationship; 9.1 Step 7 | No complete mapped ternary table or associated tests located | Add the same Ch3 case, its three references, relationship attributes if needed, and a key justified by stated cardinality rules. Do not assert that every ternary relationship necessarily needs all three keys in its candidate key. |

## Chapter 14: Dependencies and Normalization

Week 11 covers 14.1-14.4 through 3NF, using supplied candidate keys; Exam 2.
Week 13 covers introductory 14.5 BCNF; Exam 3. Existing source:
[old Ch7 guide](../chapters/ch07_normalization/student_guide.md),
[old Ch7 SQL](../chapters/ch07_normalization/student_lab.sql), and
[normalization examples](simple_examples.py).

| Required topic and source locator | Existing explanation, example, or figure | Required action |
|---|---|---|
| Meaning of attributes and update anomalies; 14.1, printed 461, PDF 492 | `Mixed Facts and Anomalies`; `ch07_small_anomaly` | Reuse mixed course/enrollment facts and insert/delete/update consequences. Identify exactly which fact is lost or repeated, rather than saying only that the design is bad. |
| Functional dependencies; 14.2, printed 471, PDF 502 | `Functional Dependencies`; `ch07_small_dependency` | Reuse formal and small-table explanations. State business-rule FDs separately from observations: two rows can refute a proposed FD but a small valid sample cannot establish it for every legal state. |
| 1NF; 14.3.4, printed 477, PDF 508 | Old Ch2 phone/atomic-value example is reusable background, but no explicit normalization lesson located | Add a named 1NF explanation and before/after table mapping. Discuss atomicity in the declared model, not a claim that a string can never contain punctuation. Connect to Ch3 multivalued attributes and Ch9 mapping. |
| 2NF and partial/full dependency; 14.3.5, printed 481, PDF 512; 14.4.1, printed 484, PDF 515 | No complete 2NF/partial-dependency treatment located in guides or example/figure sources | Add a composite-key enrollment example with supplied keys/FDs, dependency arrows, decomposition, and a near-miss practice case. Include all candidate keys in the general definition; a single-column chosen primary key alone does not settle 2NF. |
| 3NF and transitive dependency; 14.3.6 and 14.4, printed 483, PDF 514 | Existing 3NF general definition and prime-attribute exception; `ch07_small_third` | Rewrite the teaching order: ordinary transitive-dependency example first, then the general definition with supplied candidate keys. The existing prime-attribute exception is not a substitute for a step-by-step 1NF-to-3NF lesson. Do not require closure before Exam 2. |
| BCNF; 14.5, printed 487, PDF 518 | `Boyce-Codd Normal Form`; `ch07_small_bcnf`; existing 3NF-not-BCNF example | Reuse after closure/candidate-key practice in Week 13. Move the corresponding predictions, practice, and assessment labels together; no BCNF questions on Exam 2. |

Do not follow the old guide's order of closure, lossless decomposition, BCNF, then
3NF. The new order is a syllabus requirement, not a cosmetic chapter renumbering.
Do not insert minimal cover, schema synthesis, 4NF, or 5NF to fill space.

## Chapter 15: Selected Relational Design Theory

Week 13; Exam 3. Existing source:
[old Ch7 guide](../chapters/ch07_normalization/student_guide.md) and its closure and
decomposition demonstrations. This is **not** the existing `ch15.ipynb`, which is
about query processing under the other book.

| Required topic and source locator | Existing explanation, example, or figure | Required action |
|---|---|---|
| Attribute closure and simple candidate-key checks; 15.1.1, section starts printed 505, PDF 536; closure algorithm printed 508, PDF 539 | `Attribute Closure and Candidate Keys`; `ch07_closure`, `ch07_small_closure` | Reuse explicit FD sets and stepwise closure table. Check sufficiency and minimality separately; use the result before BCNF. Do not add inference-rule proofs or minimal-cover procedures. |
| Spurious tuples and binary lossless join; selected 15.2, printed 513, PDF 544; binary discussion 15.2.4 printed 517, PDF 548, referring to 14.5.1 | `Lossless Decomposition`; `ch07_lossy`, `ch07_small_lossless`, two-row/four-row reconstruction | Reuse small lossless and lossy examples. Distinguish reconstructing this sample from the FD-based guarantee for all legal states. Limit the formal test to two relations; no general chase/tableau procedure. |

## Chapters 16-17: Index Foundations and Indexing

Week 14; Exam 3. Ch16 is background only, not another full required chapter.
Existing sources: [old Ch14 indexing](../chapters/ch14_indexing/student_guide.md),
[old Ch15 query-plan discussion](../chapters/ch15_query_processing/student_guide.md),
and [index/plan examples](simple_examples.py).

| Required topic and source locator | Existing explanation, example, or figure | Required action |
|---|---|---|
| Records, blocks, and simple file organization; selected Ch16, 16.4 printed 560/PDF 591, 16.6-16.7 printed 567-568/PDF 598-599 | Index descriptions mention records/pages, but no complete prerequisite example located | Add a few records placed in numbered blocks and a heap-versus-ordered-file lookup comparison. Mark this as a simplified storage illustration. No disk hardware calculations, RAID, or buffer-management algorithms. |
| Index purpose and ordered/multilevel access; 17.1-17.2, printed 602/613, PDF 633/644 | `Index and Search Key`; `ch14_small_search_key` | Reuse nonunique search values. Introduce index entries and pointers before trees. New-book primary/clustering/secondary index definitions depend on physical ordering; do not equate any SQL primary-key index with the book's primary index. |
| B+ tree equality/range search; 17.3, printed 617, PDF 648; 17.3.2 printed 622, PDF 653 | `B+ Tree Access`, equality/range sections; `ch14_small_range` | Reuse a small tree and linked leaves, checking separator inequalities against the chosen convention. The book explicitly permits an alternative equality convention; a difference is not automatically a bug. No split/merge implementation or fan-out derivation required. |
| Composite-column order; 17.4, printed 631, PDF 662 | `Composite Indexes`; `ch14_composite` | Reuse lexicographically sorted tiny tuples and alternative query predicates. Distinguish a conceptual prefix example from absolute claims about every optimizer's possible access path. |
| Read/update/storage considerations; 17.7, printed 643, PDF 674 | `Workload Evidence`; `ch14_small_writes`; covering-index illustration | Reuse changed index entries and concrete query requirements. Explain which columns an index contains before any covering example; keep additional index taxonomy optional. Large synthetic labs must follow small explanations, not replace them. |
| CREATE INDEX and query-plan evidence; instructor-approved SQLite supplement | Old index lab; old query-processing `SCAN and SEARCH`, `Evidence and Limits`; `ch15_small_evidence`, `ch15_plans` | Reuse only the bounded before/after result-and-plan comparison. Check exact output in the target SQLite version. A SCAN can also use an index; SEARCH does not establish elapsed-time superiority. Do not restore optimizer algorithms as a required chapter. |

## Chapter 20: Transaction Basics

Week 15; Exam 3. Existing source:
[old Ch17 guide](../chapters/ch17_transactions/student_guide.md),
[transaction SQL](../chapters/ch17_transactions/student_lab.sql), and
[small examples](simple_examples.py).

| Required topic and source locator | Existing explanation, example, or figure | Required action |
|---|---|---|
| Logical unit and transaction boundary; 20.1, printed 746, PDF 777 | `Transaction and ACID`, account transfer 1000/2000 to 950/2050; `ch17_transfer` | Reuse both-account before/after tables and an incomplete-transfer contrast. Define the business invariant before judging the transaction. |
| Transaction lifecycle and ACID; 20.2-20.3, printed 753/757, PDF 784/788 | Transaction states; `ch17_small_logic`, `ch17_small_states` | Reuse a limited successful/aborted path and consistency example. Avoid making schedule graphs or recovery-log details prerequisites. Give enough facts for ACID questions; a missing order header can violate more than one property depending on how it happened. |
| COMMIT/ROLLBACK; selected 20.6, printed 773, PDF 804 | `SQL Transaction Activity`, successful/rolled-back transfer | Reuse SQLite execution with explicit connection mode. Distinguish the book's SQL discussion from SQLite BEGIN and autocommit behavior. Test a rejected statement inside an active transaction; do not assume every error rolls back the whole transaction. |
| Simple interfering updates; selected 20.1, with 20.3 context | Lost-update discussion and isolation illustrations in old Ch17 | Build one small read/change/write interleaving table with a checkable final balance. Label it conceptual unless reproduced with declared SQLite connections/settings. Exclude formal schedule classification, precedence-graph proofs, and concurrency/recovery protocols. |

## Confirmed Defect and Other Revision Boundaries

### NULL primary key in the mapped schema

The existing mapped schema declares `department.dept_code`, `student.student_id`,
and `course.course_id` as `TEXT PRIMARY KEY` without explicit NOT NULL in ordinary
SQLite tables. The stated ER identities require values. A fresh in-memory execution
of the maintained schema accepted a department with a NULL identifier even with
foreign-key enforcement enabled. `PRAGMA foreign_key_check` returned no violations;
that pragma is not an entity-integrity test.

This is a reproduced defect, not just a textbook-label mismatch. The
[SQLite PRIMARY KEY documentation](https://www.sqlite.org/lang_createtable.html#the_primary_key)
explains the exception. Revise the maintained schema and add missing-key tests before
reusing its generated notebook or packaged copy. Similar declarations found in other
labs need purpose-specific inspection; do not automatically rewrite an intentionally
unconstrained demonstration. This mapping step has not fixed the defect.

### Preserve but do not assign the old advanced scope

- Existing old Ch5 functions/procedures, recursive CTEs, and windows remain optional
  supplements, not required prerequisites for the one trigger example.
- Existing old Ch15/Ch16 processing and optimization material is not the new book's
  Ch15/Ch16. Only the bounded query-plan supplement is identified for required reuse.
- Existing old Ch17 schedule classification/graphs and old Ch18/Ch19 concurrency and
  recovery simulations are not required under the current syllabus. Preserve the
  sources and historical results; do not silently include their objectives in Exam 3.
- New Ch9 uses 9.1 only. Missing 1:1 or ternary examples do not justify adding EER,
  Ch4, or 9.2.
- Existing diagram and example identifiers retain old chapter numbers for now.
  Any later reorganization must update generator dispatch, heading anchors, tests,
  notebook names, package allow-list, and navigation together. Do not edit generated
  notebooks as independent maintained sources.
- Every chapter's summary and forward/back references still need the new book's
  teaching order. Existing Week 1/Week 2 labels inside old Ch2 are not new-book sections.
- Calendar, three examinations at 30% each, Class Performance at 10%, and the five
  comparison activities remain unchanged. This record adds no submissions or grading.

## Version Evidence

SHA-256 values identify the reviewed bytes; Git line-ending normalization can change
file hashes without changing teaching content.

| Source | SHA-256 |
|---|---|
| Prescribed private PDF | `002eceecdb5e47b050e61b30d13a8f207fb44cea4f927b98d864308c026288a5` |
| Current syllabus | `cbee66f894e02192f5bf5cccf5b2f68bf1181077ddf66e8faf48b2ec66bfbcc9` |
| Current course plan | `7f1759345060fa116ba9611afb991d2d83b8357e7be714f6eb5ae42067152ccd` |
| `simple_examples.py` | `5b3ecab19c9f77eb2e1eb56bb73539a7884013745b3a3804283f11007e3bcffa` |
| `teaching_figures.py` | `71eeb8226c66321b7388d2bc0f121e82b7aa4ddcba7dc14eeadaac21ef6daa6b` |
| `mapped_schema.sql` | `6a7c4df40996b84754c47bb8c93440d5708c986941400608cadeebc1bdb44b13` |

The complete ER, normalization, introductory SQL, intermediate SQL, indexing, and
transaction guides were inspected for this mapping. Relevant sections of old Ch2,
old Ch5, and old Ch15, the mapped SQL, figure definitions, and the small-example
catalog were also inspected. This is not a claim that every line of all twelve
notebooks and supporting programs was audited in this step.

## Checks Performed

Environment: Windows; Python 3.12.9; SQLite 3.45.3. Existing working changes were
present before this step and preserved. `git status --short --branch`,
`git log -3 --format="%h %s"`, and `git remote -v` confirmed `main`, baseline
`a9bc1a8`, and the existing `KennethWYLee/Database` origin. No fetch or remote-state
comparison was needed for this local mapping; no claim of remote synchronization.

Source/inventory commands used Get-Content, rg, Python AST parsing of example calls,
PyMuPDF PDF text/outline inspection, and Get-FileHash. Keyword searches were followed
by reading relevant sections; missing-topic findings are bounded to the inspected
maintained sources, not based on absent keywords alone.

The defect reproduction executed the entire mapped schema in a new in-memory database,
then inserted `(NULL, 'Missing identifier', 'Test')` into `department`. It printed:

```text
Python 3.12.9 SQLite 3.45.3
foreign_keys 1
NULL department key accepted: [(None, 'Missing identifier')]
foreign_key_check: []
```

No live course database was opened or changed. This is a successful reproduction of
an unwanted result, **not a passing schema test**. No other complete lab execution,
fresh-kernel notebook run, package rebuild, or new textbook-figure rendering is claimed.
SQLite documentation was inspected for primary keys, transactions, and query plans:
[CREATE TABLE](https://www.sqlite.org/lang_createtable.html),
[transactions](https://www.sqlite.org/lang_transaction.html), and
[EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html).

Final document checks:

- `python -X utf8 maintenance/course_repository/output/verify_correspondence.py`:
  passed UTF-8 and 39 relative-link target checks across the four affected Markdown
  records. Checked 60 topic rows across all 11 coverage groups, all 62 referenced
  example/figure identifiers, quoted guide headings, and six source hashes.
  These checks establish traceability and table structure, not pedagogical sufficiency.
  An initial helper run failed on a dynamic figure-registration call; the helper was
  corrected to inspect literal registrations separately from example IDs, then passed.
- `python -X utf8 maintenance/course_repository/test_repository_layout.py`: all
  16 tests passed, including schedule/weight agreement, notebook structure, figure
  anchors, and the existing executable small-example checks. This does not test every
  schema edge case; the separately reproduced missing-key defect remains open.
- `node maintenance/course_repository/output/render_correspondence.cjs`: local
  Chrome previews passed at 1440px and 390px. All 12 tables had consistent cell counts;
  no page-level horizontal overflow or zero-height cells. Desktop mapping and mobile
  opening screenshots were inspected. Wide tables scroll within their containers.
- The two QA helpers and HTML/screenshots remain ignored under `output/`. They are
  local review aids, not new course files for students. Public GitHub rendering was
  not changed or tested after upload because no upload occurred.

## Primary Next Action

**Fix the reproduced entity-integrity defect in the maintained ER schema and its
verification tests before reusing that schema.** This takes priority over authoring
the first new-book notebook because there is now an observed correctness failure,
not merely missing coverage. The expected result is a corrected maintained SQL source,
negative tests for each mandatory identifier, and regenerated affected notebook/package
outputs. Completion requires rejected missing keys, unchanged legal-case outputs,
passing affected checks, and a record of the exact revised version. Do not change
course policy or publish while doing that work without separate authorization.

The broader textbook revision remains necessary: after that defect is resolved,
the earliest teaching gap is the Ch1-2 introduction, then the corresponding Ch5
opening examples. The map is not authorization to call any rewritten chapter
source-checked before its full prescribed-source review is complete.
