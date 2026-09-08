# Chapter 2 Full Source Audit

**Source correction, 2026-09-08:** The instructor confirmed Elmasri and Navathe's
*Fundamentals of Database Systems*, seventh edition, as the prescribed text. This
record instead reviews *Database System Concepts*. It is preserved as historical
source and execution evidence, not a completed Ch2 audit of the prescribed book.
Its former next-step recommendation is superseded by the
[current audit status](../../../course_repository/full_source_audit.md).

Date: 2026-09-08. Reviewed baseline: `a9bc1a8` on `main`.
This record supersedes blanket completion statements for this chapter, not the
historical records of what earlier revisions did. Final execution results are recorded
below after regeneration. Instructor acceptance and classroom workload are separate.

## Source Identity and Reading Extent

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, seventh edition.
- Local private PDF: 1,519 pages. SHA-256:
  `6759169c44277578465d0aeebd50be0e70e832076a7e7a7a45b4e98ce4151d8c`.
- Ch2: printed pp.37-64, one-based PDF pp.62-89. All 28 pages were read in order,
  including introductory prose, every subsection, equations, table values, captions,
  footnotes 1-4, Note 2.1, summary, terms, exercises 2.1-2.18, further reading,
  bibliography and credits. Exercises were inspected for consistency and course
  relevance; this is not a new solution manual or a claim that all exercises were solved.
- Figures 2.1-2.18 were also inspected in rendered source pages. In particular,
  underlined composite keys, all foreign-key arrows, the exceptional double-headed
  arrow, qualified product attributes, and the join/union/intersection/difference
  result tables were checked visually rather than inferred from extracted text.
- All 29 pages of the local official `ch2.pdf` slides were read. Tables, equations
  and diagrams on slides 3, 5-8, 11, 14, 17, 19-24 and 27-28 were rendered and
  inspected. Slide SHA-256:
  `9ffc78a97d536cc08cd869c36769f5ae535f2be529cb8fdc5662821767ca2113`.
- Additional opening-context passages were read: Ch1 printed p.1, pp.5-8 and
  pp.11-14 (PDF p.27, pp.31-34 and pp.37-40). This is partial Ch1 reading, not
  completion of Ch1. Chapter boundaries must not be inferred using a book-wide offset.

No textbook page, extracted chapter, slide, or third-party exercise answer is included
in the public notebook or this record. Local source renders remain ignored.

## Complete Chapter-to-Material Correspondence

Material headings below refer to `../student_guide.md`; Example numbers refer to
`../student_lab.sql`. Original diagram identifiers refer to
`../../../course_repository/teaching_figures.py` or `notebook_figures.py`.
"Retained" means the current statement agrees with the specified source and declared
teaching assumptions. It does not mean every textbook topic becomes required teaching.

| Source, printed page / PDF page | Claims and source elements checked | Material, example, learner check | Disposition |
| --- | --- | --- | --- |
| Introduction, 37 / 62 | Motivation and connections to design, query processing and formal languages | Core Question; Chapter Summary; continuation into Ch3 | Retained. Historical popularity claims are not taught or newly verified against market data. |
| 2.1, 37-39 / 62-64; Figs.2.1-2.3 | Named tables, row meaning, tuple/attribute/value, relation instance; prerequisite pair direction | Reading a Relation; annotated table; first code cell and S104 practice | Retained; original four-student data replace the source university rows. No claim that the two datasets are the same. |
| 2.1, 39-40 / 64-65; Figs.2.1/2.4 | Relation as set; tuple order immaterial | Row Order and Repeated Values; reversed IDs; `ch02_order`; repeated-value comparison | Retained; compare complete tuples, not merely a count or one repeated column. |
| 2.1, 39-40 / 64-65 | Domain is permitted values, not observed sample; atomicity depends on use | Domains and Atomic Values; six-value check; `ch02_domains`; phone/email paper exercise | Retained. Whole-number 1-6 rule is a course assumption, not the textbook's universal credit policy. SQL enforcement corrected below. |
| 2.1, 40 / 65 | NULL denotes unknown or nonexistent value; algebra initially omits NULL; structured-data limitations | Temporary enrollment's unrecorded grade; full NULL instruction deferred to Ch3 | Read, not silently added as a new required Ch2 topic. No claim that every possible value is automatically legal. |
| 2.2, 41 / 66; Fig.2.5 | Schema versus instance; attribute domains; shared attributes connect relations | Schema and Instance; insert/update/add-column sequence; comparison table | Retained; schema includes declared constraints as permitted by 2.7. Updating a value changes the instance even with unchanged counts. |
| 2.2, 42-43 / 67-68; Figs.2.6-2.7 | Course versus offering; section/teaches schemas; further university relations | Course-Registration Data; composite enrollment example | Retained as a simplified design with one enrollment per student/course/term. It is not the source's full section-level university schema. |
| 2.3, 43-44 / 68-69; footnote 1 | Superkey restriction over legal instances; minimality; several candidate keys; primary-key choice | Keys; student example; `ch02_keys`; name/email/ID comparison | Retained. Sample uniqueness does not establish a key. SQLite presence checks are separately attributed implementation behavior. |
| 2.3, 44 / 69 | Multi-attribute classroom/time-slot keys and proper-subset tests | Enrollment example; three attribute-removal counterexamples; `ch02_composite` | Retained. Repeating across terms is allowed by the course's stated rules, not inferred from a single sample. |
| 2.3, 44-45 / 69-70 | Key stability and identifier choice | Key-choice practice and same-name example | Retained. The source's social-security-number example is not reused as a current legal/administrative claim. |
| 2.3, 45-46 / 70-71; Fig.2.8 | Foreign key to primary key; referencing/referenced direction; broader referential integrity | Foreign Keys and Schema Diagrams; LAW rejection; `ch02_references` | Clarified the difference between the Ch2 definition and SQLite's eligible UNIQUE parent keys. No arbitrary nonunique target is implied. |
| 2.4, 46-47 / 71-72; Fig.2.9; footnote 2 | Schema boxes/attributes; underlined keys; reference arrows; double-headed special notation; not an E-R diagram | Schema diagram, schema-and-key sheet, three-reference trace | Added the explicit schema/E-R distinction. All four course references target primary keys; the source's special time-slot arrow is not imported. |
| 2.5, 47-48 / 72-73; footnotes 3-4 | Imperative/functional/declarative categories; algebra functional, calculus declarative; practical language mixtures | No corresponding required section | Read and excluded under approved scope. Do not teach the slides' older "procedural" label as this edition's wording. |
| 2.6 introduction, 48 / 73 | Unary/binary operations; closure; duplicates excluded in formal algebra | Relational-Algebra Operations; opening operation table; SQL DISTINCT distinction | Retained. SQL supports bags unless DISTINCT/set operators or constraints impose different behavior. |
| 2.6.1, 49 / 74; Fig.2.10 | Selection predicate, comparisons, Boolean connectives, attribute comparisons | Selection; Example 2; `ch02_selection`; compound predicate practice | Retained. Full source selection gives two Physics instructors, while the stricter salary predicate retains one. Course selection retains S101/S103 and all their attributes. |
| 2.6.2, 49-50 / 74-75; Fig.2.11 | Projection drops attributes and eliminates repeated result tuples | Projection; Example 3; building practice; `ch02_projection` | Retained. Generalized arithmetic projection was read but is not added to Ch2's required syntax. |
| 2.6.3, 50 / 75 | Output relation can be input to another operation | Composition; Example 4 and duplicate-name variation; `ch02_composition` | Retained. One copy per output tuple, not one copy per original person. |
| 2.6.4, 50-52 / 75-77; Fig.2.12 | Concatenated tuples, attribute qualification, every pair, product cardinality | Cartesian Product; Example 5; `ch02_product`; 4-by-4 count | Retained. The source product has 12 x 15 = 180 tuples and only a partial table is printed. The course's 2 x 2 demonstration is independently complete. |
| 2.6.5, 52-53 / 77-78; Fig.2.13 | Join equals selection of product, keeps both inputs' attributes, nonmatches absent | Theta Join; Example 6; `ch02_join`; course-department predicate practice | Added definitions of r/s/theta and attribute preservation. The SQL displays selected columns of six matches, not the complete algebra relation. |
| 2.6.6, 53-55 / 78-80; Figs.2.14-2.16 | Union compatibility, duplicates, intersection and directional difference | Set Operations; Examples 7a-7c; reverse-difference table; ML230 practice; `ch02_sets` | Retained. Source counts 8/1/2 follow from the 3-course and 6-course source sets with one overlap. Course results use separately declared ID sets. |
| 2.6.7, 55-56 / 80-81 | Temporary assignment, no displayed relation until final expression, no increased expressive power | Extensions / Assignment; Example 8 | Retained as optional. WITH names query results; it is an analogy, not execution of textbook algebra syntax or a permanent table update. |
| 2.6.8, 56-57 / 81-82 | Rename relation/attributes; distinguish self-uses; positional alternative | Extensions / Rename; Example 9 | Retained as optional. Current example uses names and an ID order to exclude self/reversed pairs, not the source's salary threshold example. |
| Note 2.1, 57 / 82 | Aggregation, natural-join implicit predicate/schema risk, outer-join retained rows | Ch3/Ch4 continuation rather than a Ch2 requirement | Read and explicitly deferred. |
| 2.6.9, 58 / 83 | Equivalent on all legal inputs, filter placement, optimizer may choose another execution order | Extensions / Simple Equivalence; Examples 10a/10b | Retained with sample-versus-proof qualification. For an inner join and a predicate using only left attributes, every retained pair satisfies the same join and filter predicates in either expression. |
| 2.7 and Review Terms, 58-59 / 83-84 | Summary definitions, constraints, operation vocabulary | Learning Objectives; Common Errors; Chapter Summary | Checked against preceding detail; no extra exam coverage inferred from the source's review-term list. |
| Practice 2.1-2.9, 60-61 / 85-86; Figs.2.17-2.18 | Keys, referential integrity, sample uniqueness, algebra and division definition | Existing original practice, not copied source questions | Read. Division is outside approved scope. Exercise 2.8 refers to ID absent from Fig.2.17; do not invent that field or distribute the question unchanged. |
| Exercises 2.10-2.18, 62-63 / 87-88 | Changed business rules, keys, schema arrows, NULL, languages, multiple-table queries | Original key/algebra practice and later-chapter boundaries | Read, not a claim of solving every source exercise. Exercise 2.14 repeats the absent-ID issue; note it as a source inconsistency. |
| Further Reading/Bibliography/Credits, 63-64 / 88-89 | Historical attribution, references and photo credit | No copied image, prose, solution or new historical claim | Read. Bibliography entries were inspected, not the complete cited works; market/product descriptions are not newly corroborated. |

## Additional Sources and Adaptations

- Ch1 p.1 and Section 1.2 pp.5-8 support the purpose of database systems and inconsistent
  file copies. The course's confirmed-email story is synthetic and explicitly assumes
  outside identity/address confirmation. It is not a textbook observation.
- The book's opening uses DBMS broadly for data plus programs. The course distinguishes
  stored data from the software engine as a teaching explanation; it does not quote
  that sentence as if its wording were identical. SQLite is the engine in this lab.
- Ch1 Section 1.3.4 pp.12-13 and Ch2 Section 2.2 support schema/instance distinctions.
  Choosing `active` is an explicit teaching assumption, not a value inferred by the DBMS.
- [SQLite foreign-key documentation, sections 1-3](https://www.sqlite.org/foreignkeys.html)
  was checked on 2026-09-08: enabled per connection, NULL exception, and eligible unique
  parent keys. This is product evidence, not a replacement for textbook relational theory.
- [SQLite CREATE TABLE](https://www.sqlite.org/lang_createtable.html) and
  [SQLite datatypes](https://www.sqlite.org/datatype3.html) distinguish column affinity
  from rigid type enforcement. The course-specific credit rule must check stored type
  and range. It does not require rejecting numeric text before affinity conversion.
- The [author errata](https://www.db-book.com/errata-dir/db-errata.pdf), dated
  December 4, 2025, were retrieved and visually checked during the Ch3 continuation.
  They confirm that Fig.2.9, printed p.47, needs `room_number` underlined in the
  classroom composite key. The course diagram does not reproduce that classroom
  schema. This is a recorded source correction, not a changed local key.

## Findings and Maintained Corrections

1. **Fractional credits accepted.** Baseline `course_registration_setup.sql` declared
   INTEGER plus a 1-6 range CHECK. A fresh SQLite probe accepted `2.5` and reported
   storage class `real`. This contradicted the declared whole-number domain. The
   maintained schema now checks `typeof(credits) = 'integer'` as well as the range.
   INSERT and UPDATE regression tests cover fractions, out-of-range values and
   nonnumeric text; allowed endpoints and integer-affinity conversion are retained.
2. **Source/dialect distinction missing.** Guide Section 4 now states the primary-key
   target in the textbook's definition and separates SQLite's eligible unique targets.
   The existing actual foreign keys remain unchanged.
3. **Diagram and formula interpretation.** Guide Section 4 now distinguishes relational
   schema diagrams from E-R diagrams; Section 5 defines r, s and theta and explains that
   a theta join does not itself remove duplicate-named attributes from its inputs.
4. **Source inconsistencies, not course corrections.** Slides 9-10 use older language
   categories that conflict with the book's explicit wording change; slide 27 describes
   course information while its displayed expressions only select instructors. Book
   exercises 2.8 and 2.14 request an attribute missing from their cited schema. These
   items are not copied into the course and are not silently repaired in the private PDF.

The approved schedule, first-meeting flexibility, language, required/optional boundaries,
exercise count and assessment weights are unchanged. The source is read in full even
where the course intentionally teaches only selected content.

## Verification and Remaining Work

Source reading, material correspondence and the following final-version checks are
complete. Commands run from the course root using Python 3.12.9 with `-X utf8`, SQLite
3.45.3, PyMuPDF for source reading/rendering, and the existing notebook/figure toolchain.

| Command or check | Result |
| --- | --- |
| `python maintenance/course_repository/build_course_repository.py --verify` | All 12 notebooks built and executed; content/manifest checks pass. Only Ch2-Ch5 notebook content changes because those chapters share the corrected setup. |
| Every `maintenance/chapters/**/verify_*.py` script | All 13 pass, including both Ch2 verifiers and shared-schema Ch3-Ch5 regressions. |
| `python maintenance/course_repository/test_repository_layout.py` | All 14 tests pass. |
| `python maintenance/course_repository/review_notebook.py --all-chapters` | All 12 complete chapters and separate Ch2 opening/continuation run in 14 fresh kernels; preserved stdout matches; raw format and HTML pass. |
| `python maintenance/course_repository/verify_teaching_figures.py` | Data checks pass; 19 Ch2 attachments and all 96 course images accounted for; 94 generated SVG/PNG pairs. |
| `node maintenance/course_repository/render_teaching_figures.cjs` | All 94 SVG text-geometry checks pass; all 12 notebooks load images without page overflow at 1440/390 widths. Ch2's 19 figures inspected in rendered galleries. |
| `python maintenance/student_sqlite_package/build_package.py --verify` | All 21 allow-listed files verified; clean temporary extraction executes all 10 packaged activities. |

ZIP SHA-256: `73998157ac01ef35e9b9b9998c243543c00298f290eeb5c61ff8a1f9db552f9b`.
Byte hashes below identify the reviewed working files; Git may normalize line endings
when a future authorized commit is made.

| File | SHA-256 |
| --- | --- |
| `student_guide.md` | `93854c058e4444464a238de8c1d4f18d81aa92acb1faf7d49065b1931ee3b214` |
| `course_registration_setup.sql` | `937869567256deaefdc0988dbcead758535648038a1e4e7370e37f3d07ad561b` |
| `student_lab.sql` (unchanged) | `7776dd7a2410625dfc6e69c5fe290b7301e5af39ca5707d02b0c59e8311e7129` |
| `instructor/verify_ch02.py` | `a6a50075918b229970724bdd2959d4636ace0ec1a4ef544a022f04d90f5f7b21` |
| `Intro DB/ch02.ipynb` | `63ebb2770993a863a498e64c48821c869587514b8a69e7a3f133620fd26780f4` |

Two preliminary shell probes failed before the intended reading/query: default Windows
encoding could not print a PDF ligature, and a quoted SQL command was parsed by
PowerShell. Retrying with UTF-8 and standard-input Python succeeded. These failures
were not counted as successful validation.

All final student examples execute in SQLite; abstract algebra and paper practice are
reasoned about, not presented as an algebra-engine run. Tests against the same SQLite
engine are not independent DBMS corroboration. The source's exercises/bibliography
were read, but their complete solutions/cited works were not independently reproduced.
No new student workload, live classroom trial, instructor approval, commit, push or
publication action occurred. No unresolved blocker remains for continuing to Ch3.
