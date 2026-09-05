# Chapter 2 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: Week 1 authoring, source checks, execution, and local rendering
  completed September 5, 2026; publication build `2026.09.05-week1-github-png`
- Student dataset: original course-registration example
- Executable verification: seven Week 1 examples and the follow-up checks passed on
  September 5, 2026, using Python 3.12.9 and SQLite 3.45.3
- Publication: the instructor subsequently authorized commit/push; the completed
  September 5 notebook and PNG compatibility fix are on the private course-materials
  branch at `5391b52`. Earlier unpublished-status entries below are historical.

## Source scope checked

The historical textbook page ranges below record the August 27 review. Early in the
September 5 revision, the complete
textbook PDF could not be relocated in the course/workspace search; a targeted Documents
search returned other books, not a verified copy of the current text. Those early checks
were not a new full-text verification. The full local official Ch2 slide deck
was re-read, and Ch1 PDF pages 2-5, 7, 10, and 12-15 support the course-introduction
context. Ch2 PDF pages 3-7 directly support Week 1's table, domain, order, schema/instance,
and identifier explanations. New data, illustrations, and examples are original teaching
adaptations, with results checked by execution rather than attributed to the textbook.

### Follow-up After Locating the Textbook

The instructor subsequently provided the source directory, and the verified seventh
edition was copied to `private_references/Database System Concepts 7th.pdf`. The follow-up
review read all of Ch2, printed pp. 37-64 (PDF pages 62-89), including its exercises and
notes, and re-read all 29 official Ch2 slides. Week 1's claims were checked against:

- Ch1, p. 1 and Section 1.2, pp. 5-8: database purpose and inconsistent file copies.
- Ch1, pp. 11-14: the surrounding explanation of schemas, instances, and constraints.
- Section 2.1, pp. 37-40: relation, tuple, attribute, domain, order, and atomic domains.
- Section 2.2, pp. 41-43: schema/instance and the distinction between a course and a
  particular offering. Figure 2.6, p. 42, puts room information in `section`.
- Section 2.3, pp. 43-45: identifying tuples from declared rules, not sample uniqueness.
- Section 2.6, p. 48, and Ch3, pp. 72-73: stored duplicates versus duplicate elimination
  in query results.

The three approved corrections clarify query-result deduplication, replace the course
`room` exercise with one catalog `description` per course, and give atomic values a
complete before/after phone-table example. The phone data and lookup are original paper
examples, independently checked by the instructor verifier; they are not textbook data
or new student code cells. This follow-up reviews Week 1, not the teaching quality of
all Week 2 content or other chapters. The textbook remains excluded from Git and releases.

SQLite documentation checked during the earlier revision:

- [In-memory databases](https://www.sqlite.org/inmemorydb.html): a private in-memory
  database lasts until its connection closes, not until a notebook browser tab closes.
- [ALTER TABLE, ADD COLUMN](https://www.sqlite.org/lang_altertable.html): adding a column
  with a non-null default, as used in the worked example.

Historical full-text source locations:

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 2, printed pages 37-58, including Sections 2.1-2.7 and Note 2.1.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch2.pdf`, all 29 PDF
  pages.
- Current course governance: `AGENTS.md`, `PROJECT.md`,
  `1151_database_management_revised_syllabus.md`, and
  `database_chapter_teaching_material_prompt.md`.
- Historical 18-week plan: only its Week 1-2 activity ideas were used. Its four-exam
  calendar and later chapter sequence were superseded by `COURSE_PLAN.md`.
- Existing SQLite university database and insertion scripts were inspected for available
  tables and continuity. They were not copied into the new student-facing example.

## Source conflicts and adaptations

1. The earlier review recorded differing query-language category wording between book
   and slides. The current guide does not teach that classification; it teaches what
   each selected operation does. Do not claim an explanation of absent categories.
2. Formal relations are sets and have no duplicate tuples. SQLite and SQL tables can
   store duplicates when no relevant constraint prohibits them. `SELECT DISTINCT`
   removes duplicates from its result, not from the stored table. The revised guide
   distinguishes these effects without introducing new Week 1 syntax requirements.
3. The textbook notes that atomicity depends on how a value is used. The student guide
   therefore avoids claiming that a phone-number string is inherently atomic or
   non-atomic.
4. SQL syntax in the lab is verification support, not a Ch2 memorization requirement.
   SQL instruction begins in Ch3.
5. The book's university figures and exercise solutions were not reproduced. All
   student-visible data, questions, and tables were rewritten as a course-registration
   example.

## Current Teaching-Point Alignment

| ID | Teaching point | Primary source | Explanation and worked example | Student action and feedback |
|---|---|---|---|---|
| C2.01 | relation, tuple, attribute, instance | 2.1, pp. 37-40; Ch2 PDF 3-5 | Sec. 1 and annotated table; four rows/four columns | Complete tuple, attribute/value distinction, then novel course instance |
| C2.02 | domain and atomic values | 2.1, pp. 39-40; Ch2 slide PDF 4 | Sec. 1.1; integer credits 1-6, two phone tables and a step-by-step individual-number lookup | Predict six domain checks and phone-table counts; draw the two-row email alternative and preserve both associations |
| C2.03 | unordered relations and duplicates | 2.1, pp. 39-40; 2.6, p. 48; Ch3, pp. 72-73; Ch2 slide PDF 5 | Sec. 1.2; reverse display, identical tuple sets; query results distinguished from stored rows | Distinguish repeated IM values from complete duplicates; reverse course row order |
| C2.05 | schema versus instance | 2.2, pp. 41-43; Ch2 PDF 6 | Sec. 2; insertion, update, added status column with preserved output | Classify three course changes; explain default-value assumptions |
| C2.06 | identifiers; superkey, candidate key, primary key | 2.3, pp. 43-45; Ch2 PDF 7 | Week 1 Sec. 2.1 same-name S101/S105; formal definitions in Week 2 Sec. 3 | Identify the missing ID before a correction; compare key proposals in Week 2 |
| C2.07 | composite key | 2.3, p. 44; Ch2 PDF 7 | Week 2 Sec. 3, enrollment example | Include the three-attribute key in Week 2 evidence |
| C2.08 | foreign key and referential integrity | 2.3, pp. 45-46; Ch2 PDF 7 | Week 2 Sec. 4, invalid LAW department | Identify both enrollment foreign keys |
| C2.09 | schema diagram | 2.4, pp. 46-47; Ch2 PDF 8 | Week 2 Sec. 4, schema figure and three-step trace | Draw arrows and label both sides |
| C2.11 | algebra input/output and composition | 2.6, pp. 48, 50; Ch2 PDF 10, 15 | Sec. 5, composition | Expression for three-credit courses |
| C2.12 | selection | 2.6.1, p. 49; Ch2 PDF 11-12 | Sec. 5, selection | Compound predicate and exclusions |
| C2.13 | projection | 2.6.2, pp. 49-50; Ch2 PDF 13-14 | Sec. 5, projection | Building values with duplicates removed |
| C2.14 | Cartesian product | 2.6.4, pp. 50-52; Ch2 PDF 16-17 | Sec. 5, two-by-two product | Full product count versus factual enrollments |
| C2.15 | theta join | 2.6.5, pp. 52-53; Ch2 PDF 18-20 | Sec. 5, student-enrollment join | Course-department predicate |
| C2.16 | union compatibility and union | 2.6.6, pp. 53-54; Ch2 PDF 21-22 | Sec. 6, DB201/FT210 sets | ML230 set operations |
| C2.17 | intersection and difference | 2.6.6, pp. 54-55; Ch2 PDF 23-24 | Sec. 6, four-result table | Direction of difference |
| C2.18 | assignment (optional) | 2.6.7, pp. 55-56; Ch2 PDF 25 | Extensions, Assignment | Named intermediate relations |
| C2.19 | rename (optional) | 2.6.8, pp. 56-57; Ch2 PDF 26 | Extensions, Rename | Self-pairs and reversed pairs |
| C2.20 | equivalence (optional) | 2.6.9, p. 58; Ch2 PDF 27-28 | Extensions, Simple Equivalence | Sample equality versus a general proof |

C2.04 (NULL) and C2.10 (query-language categories) were old coverage entries without a
corresponding explanation in the current guide. NULL is taught in Chapter 3; language
classification is not required by the approved chapter scope. They are not silently
reintroduced as Week 1 requirements. The database-purpose introduction draws on Ch1
slides and the verified Ch1 passages as orientation; it does not add Chapter 1 to the
assessed chapter list.

## Teaching summary

### Week 1

1. Database purpose, then one student table and an annotated tuple/attribute/value figure.
2. Domain decisions, atomic values, row order, and repeated values.
3. Insert, update, and add-column predictions, execution, and output-specific interpretation.
4. Same-name students illustrate the need for identifiers; formal key classification waits.
5. Complete the Week 1 response table inside the notebook, including one correction.
6. Stop at End of Week 1. Full SQL syntax and the four-table setup are not Week 1 requirements.

### Week 2

1. Recall the same-name example, introduce key types and foreign-key directions.
2. Read the original four-table data and schema diagram; introduce algebra closure.
3. Selection, projection, and composition with prediction before reveal.
4. Product versus join with tuple-count check.
5. Union, intersection, and difference using the same A/B relations.
6. Assignment, rename, and equivalent-query examples are optional extensions.
7. Group comparison of key proposals, anonymous display, individual ranking, instructor
   feedback, and individual revision.

## Student-practice guidance

These are practice tasks, not released examination items. Accept equivalent notation if
the schema and result are correct.

Week 1 final practice: three course tuples and three attributes; credits 5 is permitted,
0 is outside the range, and 3.5 is not a whole number. Adding
`(DB205, Database Management, 5)` changes the instance and makes four tuples; updating
WD120's credits from 2 to 3 changes the instance but keeps three
tuples; a description attribute changes the schema, adds a fourth attribute, and requires
verified catalog descriptions for existing courses rather than invented facts. Each
course has one catalog description under the stated rule. Each change starts from the
original three-row instance. After the insertion, DB201 and DB205 share the title
Database Management; selecting one for an update requires its course ID. The shared
credit value 3 is not a complete duplicate. Reverse display order
does not change the tuple set. The two-email example needs individually addressable
values for its stated operation: `(S103, a@example.edu)` and `(S103, b@example.edu)`.
The worked phone example has zero exact whole-cell matches before the change, one S101
match afterward, and three contact pairs for two students. Splitting the displayed
semicolon list preserves the same pairs. Responses belong in the existing notebook; no new
grading weight, submission platform, or separate worksheet is introduced.

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
py -3 working_materials/course_repository/build_course_repository.py --verify
py -3 working_materials/chapters/ch02_relational_model/instructor/verify_week1.py
```

Expected checks:

- row counts and schema constraints;
- duplicate primary key, duplicate candidate key, invalid foreign key, and duplicate
  composite key are rejected;
- selection, projection, product, join, union, intersection, difference, assignment,
  and rename return the documented results;
- the two equivalent-query implementations return identical results;
- `PRAGMA foreign_key_check` returns no violations.
- The displayed phone tables preserve three contact pairs for two students, and exact
  whole-cell lookup has the documented result in each representation.
- A separate `SELECT DISTINCT` check returns one row from two identical stored rows,
  while the stored count remains two; the generated practice uses course descriptions.

## Remaining Limits and Publication Boundaries

- The instructor selected English-only student prose on August 27, 2026 and subsequently
  delegated completion of Week 1. Its local authoring and objective checks are complete;
  instructor rereading is not an outstanding authoring task. There is no claim of
  instructor review or classroom testing. Git publication requires separate authorization.
- The current chapter notebook embeds its code, outputs, and images. Week 1 uses a
  minimal independent in-memory table; Week 2 starts again with the original four-table
  setup. The older SQLite ZIP remains optional and its sources were not changed here.
- `COURSE_PLAN.md`, the current syllabus, and project decisions govern this chapter.
- The official slide PDF metadata incorrectly identifies another chapter even though the
  visible deck content is Chapter 2. Source use is based on visible content.

## Chapter delivery status

### September 5 Revision Evidence

- Python 3.12.9, SQLite 3.45.3: the course builder executes all 12 notebooks and checks
  the manifest and 14-file output set. Ch2's inline output fences are checked against
  actual stdout; six fixed-output examples plus the version-reporting setup all run.
- `verify_week1.py` independently checks seven Week 1 examples, exact preserved output,
  the 4-by-4 to 5-by-4 to 5-by-5 changes, same-name students, closed Week 1 connection,
  stopping point, figure attachment, and a fresh Week 2 execution with original data.
- A separate local review script executed Week 1 alone, Week 2 alone, and all Ch2 with
  nbclient in three fresh Python 3.12.9 Jupyter kernels. Stored stream output matched
  each execution; nbformat validation passed. The first review attempt left an external
  kernel holding a temporary directory; explicit kernel cleanup resolved the test-harness
  failure, and all three runs then completed.
- nbconvert HTML was inspected with headless Chrome at 1440 and 390 pixels wide. The
  original 1200-by-590 table figure rendered; the annotated tuple, attribute, and value
  labels were legible with solid/dashed outlines. Example output and the response table
  were visually inspected. No whole-page horizontal overflow was found at either width;
  wide code and tables may still require their normal local horizontal scrolling.
- This is local rendered evidence, not a new check of GitHub rendering or real classroom
  workload. No repository publication is part of this revision.

Reproduction commands from the course root (substitute the installed Python executable
when `python` is not on PATH):

```powershell
python working_materials/course_repository/build_course_repository.py --verify
python working_materials/chapters/ch02_relational_model/instructor/verify_ch02.py
python working_materials/chapters/ch02_relational_model/instructor/verify_week1.py
```

The notebook kernel/HTML review scripts and screenshots are local ignored files under
`working_materials/course_repository/output/`, separate from the generated 14-file
course preview. They are not student dependencies.

### Textbook Follow-up: Final Verification

- Build version: `2026.09.05-week1-textbook-review`. The builder regenerated and executed
  all 12 notebooks; content checks, the manifest, and the exact 14-file set passed.
- Both `verify_week1.py` and `verify_ch02.py` passed with Python 3.12.9 / SQLite 3.45.3.
  The extended verifier checked the displayed phone tables, the original and revised
  exact-match results, preserved contact pairs, unchanged stored duplicate count, and
  the description-based practice. The seven student code examples remain unchanged.
- After the final student-guide edits, `output/review_week1.py` passed Week 1, Week 2,
  and complete-Ch2 execution in three fresh Jupyter kernels, comparing actual output
  with the notebook's preserved output. This final run emitted no connection error.
  The preceding advisory review had emitted a ZeroMQ connection-reset message before
  its three checks completed; no student-cell error was recorded in either run.
- `output/render_week1.cjs` rendered the new HTML with Chrome. The phone-table example
  and revised practice were inspected at desktop width; both phone tables were also
  inspected at 390-pixel mobile width. There was no whole-page overflow at 1440 or 390
  pixels. The existing relation illustration remained a readable 1200-by-590 image.
- Compared with the immediate pre-correction preview, only `ch02.ipynb` changed hash.
  The other 11 notebooks, `README.md`, and `.gitignore` are byte-identical. The manifest
  records the new version and hashes; the private PDF is not part of the output set.
- Source corrections and local checks are complete. Real classroom comprehension,
  teaching workload, and the unpublished revision's GitHub rendering remain untested.
  No commit, push, or publication was performed.

### Week 1 Completion: September 5, 2026

The instructor's latest request is to finish Week 1 without returning unfinished checks
for manual review. Version `2026.09.05-week1-complete` completes the existing scope;
it does not change the timetable, assessment, seven student code cells, or Week 2 topics.

| Existing objective | Explanation and concrete example | Prediction, practice, and feedback |
|---|---|---|
| Data and DBMS | Two fictional files disagree about S101's email; a stated identity/address confirmation resolves which value to store | Identify the conflict before the explanation; separate data, software, and confirmation in the response table |
| Relation, tuple, attribute, value, order, and duplicates | Four-student table and annotated figure; reverse display; S101/S103 versus a complete repeated S101 row | Predict counts and first/last IDs; compare complete rows, retained output, and independent course-table answers |
| Domain | Whole-number credits from 1 through 6; six tested candidates | Predict each decision; evaluate 5, 0, and 3.5 using both range and whole-number rules |
| Atomic values | Before/after phone tables retain three pairs for two students; exact whole-cell lookup changes from zero to one match | Predict matches, tuples, and students; draw two separately addressable email rows and check both associations |
| Schema and instance | Insert S105, update S102, and add status; the four-state summary matches the actual counts and definitions | Predict each change; independently add DB205, update WD120, and add a catalog-description attribute to the course table |
| Identifiers | S101 and S105 have the same name but different IDs | Identify both matches and the information needed to select one; repeat with DB201/DB205 sharing a course title |

Every objective has an explanation, worked example, checkable question or operation,
result interpretation, and practice. Limits are explicit: sample values do not define
a domain; a DBMS does not establish factual truth; parsing a phone list differs from
whole-cell equality; repeated values are not complete duplicates; unchanged counts do
not establish an unchanged instance; observed uniqueness alone is not a lasting rule.
The response table retains predictions, answers, and one correction without a new
submission system or grading rule. Classroom explanation and demonstration remain the
intended mode; preserved output supports review, not a requirement to self-teach.

Final checks run from the course root:

```powershell
python working_materials/course_repository/build_course_repository.py --verify
python working_materials/chapters/ch02_relational_model/instructor/verify_week1.py
python working_materials/chapters/ch02_relational_model/instructor/verify_ch02.py
python working_materials/course_repository/output/review_week1.py
node working_materials/course_repository/output/render_week1.cjs
```

- Environment: Python 3.12.9, SQLite 3.45.3, Node.js 24.19.0, local Chrome. The review
  script uses nbformat 5.10.4, nbclient 0.10.4, and nbconvert 7.17.1; these are review tools, not added
  student dependencies.
- The builder executed all 12 notebooks and verified the manifest, 14-file set, embedded
  assets, language, links, and forbidden-content checks. Both Ch2 verifiers passed;
  the Week 1 verifier independently checks the new summary and practice scenarios.
- Strict validation of raw JSON initially found 55 missing cell IDs in Ch2. Earlier
  nbformat loading had silently supplied them, so those earlier format checks were
  insufficient. The maintained builder now generates deterministic unique IDs and
  rejects missing, invalid, or duplicate IDs. This follows the official
  [notebook cell ID specification](https://nbformat.readthedocs.io/en/latest/format_description.html#cell-ids).
  Raw JSON schema validation now passes for all 12 notebooks without relying on repair.
  Three in-memory negative tests independently confirmed rejection of a missing ID,
  an ID containing a space, and a duplicate ID without modifying generated files.
- Week 1 alone, Week 2 alone, and complete Ch2 passed in three fresh Jupyter kernels;
  actual stream outputs match the preserved notebook outputs. Final runs emitted no
  cell or connection errors. During review-tool changes, an array-valued source and a
  JavaScript loop typo each caused a harness failure; both were fixed before these
  successful runs. Neither was a failure in student code.
- The database-purpose example, duplicate comparison, state summary, phone tables,
  final practice, and closing section were visually inspected in rendered HTML. At
  1440 and 390 pixels, the page had no horizontal overflow; the original 1200-by-590
  figure rendered, with no missing labels or overlapping text in inspected views.
- Two consecutive builds produced identical hashes for all 14 preview files and the
  manifest. Relative to the start of this completion pass, only Ch2's instructional
  content changed. Removing the newly added IDs from comparison makes the other 11
  notebooks byte-identical to that baseline; README and .gitignore are unchanged.
- No known blocking issue remains for Week 1 authoring and local verification. Actual
  classroom comprehension and the unpublished revision's GitHub rendering are not
  tested. The private textbook remains excluded. No commit or push was performed.

### Authorized GitHub Publication Follow-up

- The instructor explicitly requested commit and push after Week 1 completion. The
  completed notebook was published in `aa06046`. Actual GitHub preview then displayed
  broken SVG images even though local HTML rendering had passed.
- The maintained generator now renders its original SVG to PNG using `resvg-py 0.5.0`,
  with [the documented SVG-to-PNG API](https://resvg-py.readthedocs.io/en/latest/api.html).
  This is a build-only dependency. A trial with PyMuPDF omitted arrowheads and dashed
  lines and was rejected; those trial images were never committed or published.
- All three Ch2 diagrams remain embedded attachments. The final PNGs were inspected
  for text, arrowheads, and the solid/dashed distinction; no original lesson text or
  code changed. The Week 1 verifier checks PNG format and width in the actual notebook.
- Build `2026.09.05-week1-github-png` passed all 12 notebook executions, raw schemas,
  manifest/content checks, the Week 1 verifier, three fresh-kernel Ch2 runs, and
  byte-identical repeat builds of the 14 preview files plus manifest.
- The corrective commit `5391b52` was pushed without rewriting history. Actual GitHub
  preview now displays the Week 1 table image with its labels and solid/dashed outlines.
  GitHub's notebook text also includes the worked examples, outputs, response table,
  and End of Week 1. This is a publication check, not evidence of classroom learning.
- The main-source commit includes this follow-up. Publication remains private; the
  textbook, temporary rendering trials, and local QA files are excluded.

### Status and Limits

- Files created: student guide, original setup data, executable student lab, instructor
  coverage and guidance, and automated verifier.
- Source verification: historical textbook check on printed pages 37-58; the September 5
  follow-up located the textbook, read all Ch2 on pp. 37-64 and the supporting Ch1/Ch3
  passages listed above, and checked the revised Week 1 claims. The earlier missing-PDF
  limitation is resolved; other chapters were not newly re-audited.
- Executed content: all schema constraints and all executable chapter examples.
- Unexecuted content: paper-based schema-diagram and relational-algebra exercises; these
  were independently worked in the student-practice guidance but require classroom use
  to evaluate workload and student interpretation.
- Main corrections made: replaced the slide deck's obsolete query-language label,
  distinguished formal set semantics from SQL duplicate behavior, and kept SQL syntax
  outside the Ch2 memorization requirement.
- Progression decision: Week 1 is complete within the delegated scope, with no unfinished
  objective check assigned to the instructor. Week 2 retains its existing core and
  extensions; it was regression-tested, not redesigned or newly certified for classroom
  workload. Publication and work on later lessons remain separate tasks.
