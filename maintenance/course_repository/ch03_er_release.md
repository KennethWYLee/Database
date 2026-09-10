# Ch3 ER Teaching Release

## Photographed Source Corrections and Private Worked Answers

Date: 2026-09-10. Current version: `2026.09.10-ch03-photograph-checked`.
Baseline: `c97312d3eb9284a41e3d6ed049c9a39156b3baef`, main tracking origin/main.
The worktree already contained the authorized weak-entity/3.9.2/3.10 extension
below. The instructor now approved the review corrections, requested answers
to all photographed Ch3 questions, and authorized a local commit. No push is
requested. The course repository is public; private answers remain ignored,
pending an explicit decision about including them in this repository.

### Source and Correction Record

Photographed source: `Database pdfs/Chapter3.pdf`, 24 image-only spreads,
printed pp.89-135, with a blank facing page before p.89. All spreads were
visually read in the preceding review and relevant exercise/diagram details
were inspected again while answering. This is not an OCR-only summary check.
SHA256: `55366a1faa7718dd1b89bdb95a938db5c5e7b00886f99aeb88a16086409e72c7`.

| Finding | Correction or retained distinction |
|---|---|
| Figure 3.20, p.124; old printing p.94 | Both CCode and CoName are underlined in both copies. Corrected the earlier review error; they are independent keys, not one composite key. |
| Student reading locators | Use photographed pp.90-124 for the taught sections, keeping section numbers as the stable cross-printing reference. |
| Section 3.10 prose, p.123, versus Figure 3.20 | Retain the explicit conflict: prose assigns a primary department; HAS permits STUDENT (0,1). No silent change to the chosen figure interpretation. |
| Local and global SECTION identity | Keep the initial single-term weak SECTION separate from UNIVERSITY's regular SECTION with globally unique SecId. |

The historical tables below use the earlier printing's page numbers and record
the checks run then. They are not the new student's reading list. The current
guide's Textbook Reading table supplies the updated locators.

### Private Answer Deliverable

Original English answers cover every question 3.1-3.35: 15 review questions,
15 exercises, and 5 laboratory exercises, with all numbered subparts addressed.
There are 26 original diagrams/table figures and additional editable Markdown
tables. Source locators, assumptions, alternatives and counterexamples accompany
the answers. Question statements and scanned book figures are not reproduced.
Real credits in the selected three-movie example cite primary studio sources;
invented identifiers and the teaching lead-role classification are distinguished.

Maintained files are under ignored `private_references/ch03_solutions/`:
`solutions.md`, `build.py`, `verify.py`, and `render.cjs`.
Generated `ch03_solutions.html` and `ch03_solutions.ipynb` embed all 26 figures;
the latter has 38 Markdown cells and no executable student cells.
The generated manifest records source/output/figure SHA256 values.
No answer content is inserted into `Intro DB/ch03.ipynb` or staged for the
public course repository. UML is included only to answer question 3.30; it
does not change the approved taught scope or assessment.

### Current Verification

Commands ran from the course root using the environment listed in the extension
record below. Fresh kernels use temporary empty working directories with the
existing Python installation; dependencies were not reinstalled from scratch.

| Command | Actual result |
|---|---|
| `python -X utf8 maintenance/course_repository/build_course_repository.py --verify` | PASS: 17 notebooks, 19 course files, executions, content and manifest. Only Ch3 notebook differs from the baseline. |
| `python -X utf8 -m unittest discover -s maintenance/course_repository -p 'test_*.py'` | PASS: 44 tests, including 14 Ch3 tests. Initial source-locator regression regex falsely matched `pp.93-102`; fixed the test to distinguish `p.93` and reran all 44. |
| `python -X utf8 maintenance/course_repository/verify_first_meeting.py` | PASS: 5 fresh kernels, 60 figures, 41 relative links, 2 exact-DDL cases, maintained/generated consistency. A Windows libzmq connection-reset assertion occurred during shutdown; exit code 0 and expected notebook outputs passed. Diagnostic remains unresolved. |
| `node maintenance/course_repository/render_first_meeting.cjs` | PASS: 14 desktop/mobile previews, no page/text overflow or broken images; figure geometry reported no issues. |
| `python -X utf8 private_references/ch03_solutions/build.py` | PASS: all 35 answers, 26 figures, 38 notebook cells. |
| `python -X utf8 private_references/ch03_solutions/verify.py` | PASS: 12 checks covering numbering, hashes, image/notebook structure, source identity, answer separation, keys, counterexamples, selected movie constraints, and review requirements. These are focused checks, not an exhaustive proof of every open design. |
| `node private_references/ch03_solutions/render.cjs` | PASS: 1440/390 pixel pages show 35 question headings, 26 loaded images, no page overflow; all 26 SVGs pass text overlap/bounds checks. |

Two consecutive private builds produced byte-identical manifests and all listed
source/output hashes; the 12 private tests were rerun after that check.
`git diff --check` passed. `git check-ignore -v` confirms that the answer
notebook/source, photographed PDF and generated QA records remain excluded.
The local commit contains only the 14 intentional course source/notebook,
syllabus/plan and audit/test files; no remote change or push is performed.

Visually inspected representative weak-owner, airline, composite-key, movie
instance, UML and conference figures, plus desktop/mobile answer previews.
Diagrams scale down on mobile; detailed diagram reading may require zoom.
Local rendering does not verify GitHub's remote renderer or classroom projection.

Current student Ch3 SHA256:
`51c347b8fa2a19da3cb075e7fb425f956c5cac14b93e4b0eb05d5665d4c137d4`.
Private answer notebook SHA256:
`49c7cb69c5282f121a81296367b5e3d48938b12e751fabf55b3a637d6ab9d33c`.

### Limits and Next Action

These are original worked answers, not an official solution manual or an
independently reviewed answer key. Open designs require the assumptions stated.
ERwin/Rational Rose have not been run: model diagrams, inventories and checking
steps are supplied, but no proprietary-tool project or execution is claimed.
The unresolved old ER SQL/ZIP defect and unconverted chapters remain outside
this change. No textbook, scan, private answer, or generated QA file enters Git.

Primary next action: instructor-review the assumptions in the open design
answers before assigning or releasing any solution. The expected outcome is
an approved set of assumptions and selected examples; completion means each
chosen answer matches the instructor's intended interpretation. Course schedule,
weights and mandatory student workload remain unchanged.

## Expanded Weak Entities and Sections 3.9.2-3.10

Historical extension version: `2026.09.10-ch03-extended`, based on clean
`c97312d3eb9284a41e3d6ed049c9a39156b3baef` on main.
The instructor reported using Ch3 in class, then explicitly requested more
weak-entity examples, 3.9.2, and 3.10. This follow-up authorizes editing,
not staging, commit, push, or a changed examination schedule.
The original release record below remains historical.

### Source Check and Coverage

Reread printed p.79 and pp.90-94 of the same private textbook; inspected the
complete Figure 3.20 page visually. The original full Chapter 3 reading remains
documented below, not newly claimed for another book or all exercises.
All new records are synthetic and new layouts are drawn from maintained Python;
the textbook PDF and its rendered page remain excluded from Git.

| Guide location | Source | Added explanation, example, and check |
|---|---|---|
| 12.1 | 3.5, p.79 | Order-item owner-local identification; same partial key under different owners; duplicate under one owner |
| 12.2 | 3.5, p.79 | Required ownership versus weak identification, using globally unique access-card IDs |
| 12.3 | 3.5, p.79 | Weak owner of a weak type; order/item/note identity needs all levels |
| 12.4 | 3.5, p.79; 3.9.1, pp.90-91 | Two owners plus VisitNo; alternative with no partial key when one object per owner pair is guaranteed |
| Attribute/entity choice after 12.4 | 3.5, p.79 | Multivalued composite contact versus an entity with an independent verification relationship |
| 14.1 | 3.9.2, pp.91-92 | Fix other participants before reading a ternary 1; generalization to n-ary relationships |
| 14.2-14.3 | 3.9.2, p.92 | Count per-entity participation separately; examples that pass only one rule and a case that passes both |
| 16 and 16.1 | 3.10, pp.92-94 | Six entity types and attribute inventory; SecId makes SECTION regular; composite name and room; relationship attributes |
| 16.2-16.3 | 3.10, pp.92-94; Fig.3.20 | All nine relationship types in two original diagram groups; counts, dean/chair/employment, Grade, and minimum five students |
| 16.4 | 3.10, p.93 | Course-term-number, room-time, instructor-time uniqueness; combined-section qualification and exact-equality limit |

Each added unit includes explanation, concrete data or facts, prediction,
worked interpretation, and practice with explicit checking criteria.
The initial one-term campus model and the multi-year UNIVERSITY case remain
separate. They differ in section identification and minimum enrollment.
No Ch9 relational mapping, SQL requirement, new mandatory submission, or grading
weight was introduced. The original comparison activity is now Section 17.

### Source Differences Preserved

- The p.93 prose assigns each student to one primary department. Figure 3.20
  shows STUDENT (0,1) on HAS. The new diagram follows the figure and the text
  explicitly contrasts the (1,1) prose version. Neither is silently made the
  unique authoritative requirement for the exercise.
- Correction after photograph review: both CCode and CoName are underlined in
  Figure 3.20 in both source copies. The previous claim that only CCode was
  underlined was a review error, not a textbook inconsistency.
- The three additional SECTION uniqueness rules include related course/instructor
  identity. The guide does not redraw those identifiers as ordinary independent
  SECTION key attributes.
- Distinct time labels can overlap: the exact-equality example is not a complete
  scheduling-conflict algorithm. This limitation is a labeled teaching explanation.

### Validation and Remaining Work

Validation completed locally for this version:

- `python -X utf8 maintenance/course_repository/build_course_repository.py --verify`:
  passed; 17 notebooks and 19 course files, content and manifest checks passed.
- `python -X utf8 -m unittest discover -s maintenance/course_repository -p 'test_*.py'`:
  all 43 tests passed, including 13 Ch3 tests. Added checks independently count
  owner combinations, ternary constraints, and UNIVERSITY uniqueness conflicts.
- `python -X utf8 maintenance/course_repository/verify_first_meeting.py`:
  passed in five fresh kernels; checked 60 figures, 41 relative links, two exact
  DDL key cases, and maintained/generated consistency. Ch3 contains 27 figures
  (11 additions) and no student code cells. No other chapter notebook changed.
- `node maintenance/course_repository/render_first_meeting.cjs`: passed;
  14 previews at widths 1440 and 390 showed no page overflow, overflowing text,
  or broken images. Figure geometry checks reported no issues. Visually inspected
  all 11 new figures and six desktop/mobile topic screenshots. Wide tables use
  horizontal scrolling on mobile; these local previews do not verify GitHub's
  own renderer or establish classroom projection readability.

Environment: Python 3.12.9, SQLite 3.45.3, nbformat 5.10.4, nbclient 0.10.4,
ipykernel 7.2.0, pyzmq 27.1.0, resvg-py 0.5.0, Pillow 12.1.1,
PyMuPDF 1.27.2.2, and markdown-it-py 4.0.0. The fresh-kernel command emitted
Windows ZMQ connection-reset/not-a-socket diagnostics during shutdown; its exit
code was zero, all five kernels returned their environment values, and expected
outputs passed without notebook error cells. The environment diagnostic remains
unresolved and is not presented as a clean diagnostic log.

Ch3 notebook SHA256:
`78508bae82c1db8fafc445cf324c9fdb96976a2d7f1e446bdc263a29db597473`.
Machine-readable evidence is in the ignored
`maintenance/course_repository/output/first_meeting/verification.json` and
`rendering.json`; screenshots are in the same directory.

Changes are limited to the Ch3 guide, figure generator, generated notebook,
scope descriptions in the syllabus/plan/project/prompt, build configuration,
verification/rendering tests, and maintenance records. No source PDF, rendered
textbook page, private SQL/ZIP, or generated QA output is included in the changes.
No staging, commit, push, remote modification, or history rewrite was performed.
No whole-book audit, independent solution of every textbook exercise, instructor
review of this extension, or classroom workload validation is claimed.

The scope is substantially larger than the first 16-figure release.
Do not infer that all added reading and drawing practice fits the original
single scheduled meeting. Dates and 30/30/30/10 are unchanged.
The instructor's actual stopping point and continuation need to be established
before any schedule adjustment. Old ER SQL/ZIP limitations remain unchanged;
no old mapped SQL is reused.

## Original Release Record

Status: authored, taught-selection source-checked, built, tested, and locally rendered.
Version: `2026.09.10-ch03-er`. No unresolved Ch3 blocking error was found in these checks.
This is not a claim of instructor review or classroom-tested workload.
Baseline: `cd78de529a9c2c5b49b87843bfd55f3ee35ec2c4`, clean `main`.
Authorization: instructor requested Ch3 completion, then commit and push.

## Scope and Sources

Elmasri and Navathe, *Fundamentals of Database Systems*, seventh edition.
Private source SHA256: `002eceecdb5e47b050e61b30d13a8f207fb44cea4f927b98d864308c026288a5`.
Read the complete extracted Chapter 3 text, printed pp.59-105 (PDF pp.90-136),
including review questions, exercises, laboratory exercises, and bibliography.
Visually inspected original Figures 3.7, 3.14, 3.15, and 3.17 on printed
pp.69, 83, 85, and 89 for key, participation, min-max, and ternary notation.
The PDF and rendered source pages remain ignored and are not distributed.
No verified seventh-edition official slide deck was used or claimed as reviewed.

This is full-chapter text reading plus a source check of the taught selections,
not an independent solution of every exercise or a visual audit of every book figure.
No whole-book audit completion is claimed. Student examples and diagrams are
original synthetic campus examples, not the book's COMPANY or UNIVERSITY solutions.

## Teaching Correspondence

Guide Sections 1-15 include a prediction, worked interpretation, and practice
with checking criteria; Section 16 supplies the approved group comparison and
individual revision. These support taught Ch3 scope in Exam 1 and
the already approved classroom performance activities; no new grading weight.

| Guide Section | Source, Printed Pages | Observable Performance and Example |
|---|---|---|
| 1. Requirements | 3.1-3.2, 60-63 | Turn a campus rule into a conceptual design question; defer tables and SQL |
| 2. Entities | 3.3.1-3.3.2, 63-68 | Distinguish one student, the STUDENT type, and the current entity set |
| 3. Attributes | 3.3.1, 64-67 | Draw simple/composite, single/multivalued, stored/derived attributes using a student profile |
| 4. Keys | 3.3.2, 68-70; Fig.3.7 | Check uniqueness/minimality and underline one composite key, not separate components |
| 5. Domains and Missing Values | 3.3.1-3.3.2, 65-70 | Check allowed credits and distinguish missing from inapplicable information |
| 6. Relationships | 3.4.1-3.4.2, 72-75 | Identify an enrollment instance, type, set, and degree |
| 7. Cardinality | 3.4.3, 76-78 | Use explicit rules and small links to distinguish 1:1, 1:N, M:N |
| 8. Participation | 3.4.3, 77-78 | Check optional versus required links; distinguish minimum from maximum |
| 9. Min-Max | 3.7.4, 84-85; Fig.3.15 | Translate the same rule without reversing label placement |
| 10. Roles | 3.4.2, 73-75 | Draw a recursive mentoring relationship and name both roles |
| 11. Relationship Attributes | 3.4.4, 78 | Attach a grade to the student-section enrollment, not the student alone |
| 12. Weak Entities | 3.5, 79; Fig.3.14 | Identify a section using its course owner and partial key |
| 13. Refinement | 3.3.3, 70-72; 3.6-3.7.3, 80-84 | Replace repeated entity references with a named relationship; ask about unknown rules |
| 14. Ternary Relationships | 3.9.1, 88-91; Fig.3.17 | Read a three-part approval fact and disprove an inferred fourth fact using three pairs |
| 15. Complete Diagram | 3.6-3.7, 80-85 | Reconstruct the original core model and check each rule in both directions |
| 16. Comparison and Practice | 3.4.3, 76-78; approved Week 2 activity | Compare designs against identical requirements and revise after feedback |

Scope exclusions: detailed UML notation (3.8), higher-degree constraint theory
(3.9.2), the full additional UNIVERSITY design (3.10), and book exercise solutions.
Ch4 will teach EER; Ch9 will teach mapping. No SQL or old ER mapped-schema file is
reused. The previously documented NULL-key defect in that old SQL remains unresolved
and does not affect this conceptual notebook.

## Verification

Commands below were executed from the course root using Python 3.12.9 and Node
from the configured local installations. Fresh kernels used new empty temporary
working directories, not newly installed dependencies.

```powershell
python -X utf8 maintenance/course_repository/build_course_repository.py --verify
python -X utf8 -m unittest discover -s maintenance/course_repository -p 'test_*.py'
python -X utf8 maintenance/course_repository/verify_first_meeting.py
node maintenance/course_repository/render_first_meeting.cjs
git -c core.safecrlf=false diff --check
git fetch origin
git rev-list --left-right --count HEAD...origin/main
```

| Check | Actual result |
|---|---|
| Builder, content, manifest | PASS: 17 notebooks, 19 course files, no external asset files; every executable cell ran |
| Unit tests | PASS: 39 tests, including 9 Ch3 tests |
| Current notebook regression | PASS: Ch1/2/3/5/8 rebuilt identically and checked in 5 fresh kernels; Ch3 has zero student code cells |
| Figure attachments | PASS: 49 current figures, including 16 Ch3 PNG attachments; decoded, nonblank, expected dimensions |
| Example checks | PASS: enrollment counts 2/1/0, relationship grades, one teacher per section, owner-local section identity, composite key, ternary counterexample |
| Ternary independent calculation | Reconstructing combinations from the three observed pair sets adds exactly (S101, I1, CS102); the additional triple changes none of the pair sets |
| Diagram notation | PASS: undirected lines, weak/identifying double shapes, dashed partial-key underline, full-key underline; text fits ER shapes |
| Rendering | PASS: 14 previews at widths 1440 and 390, zero page/text overflow or broken images; zero reported SVG geometry/ER-label overlap failures |
| Visual inspection | All 16 Ch3 figures inspected; complete ER diagram re-inspected after crossing gap and label adjustment; desktop/mobile notebook samples inspected |
| Relative links | PASS: 41 links in the verifier's designated navigation/governance files |
| Source privacy | Prescribed PDF and rendered textbook pages remain ignored; AGENTS/CLAUDE remain byte-identical |
| Scope and assessment | Only Ch3 availability links added to syllabus; dates, chapter schedule, travel, and 30/30/30/10 unchanged |
| Existing notebooks | The four earlier current notebooks and twelve historical notebooks have no Git content changes |
| Git baseline | Fetch succeeded; local HEAD and origin/main had 0/0 divergence before staging |

Notebook SHA256 (UTF-8/LF generated bytes):
`caf3da69165782d4c074d8233f03dad78ad65b783605cfd21b33837546ab1606`.
Ignored machine-readable reports: `output/first_meeting/verification.json` and
`output/first_meeting/rendering.json`; screenshots remain in that output directory.

Environment: SQLite 3.45.3, nbformat 5.10.4, nbclient 0.10.4, ipykernel 7.2.0,
pyzmq 27.1.0, resvg-py 0.5.0, Pillow 12.1.1, PyMuPDF 1.27.2.2,
markdown-it-py 4.0.0. Diagrams use Arial/Arial Bold and the existing PNG pipeline.

Some fresh-kernel runs emitted Windows ZMQ control/shutdown diagnostics
(`Interrupted system call` or `not a socket`). The verification process returned
zero, all five kernels returned their environment values, all executed outputs
matched, and no notebook error output was found. The environment diagnostic is
not reported as a corrected package defect. Ch3 requires no student code execution.

## Changes and Corrections

- Added `maintenance/chapters/ch03_er_model/student_guide.md` and generated
  `Intro DB/ch03.ipynb`: 16 figures, small inputs, interpretation, practice,
  core ER diagram, and the existing Week 2 group comparison.
- Added `er_figures.py`, `test_ch03_er.py`, and this source/verification record.
- Updated the figure registry, ER renderer dispatch, chapter configuration,
  builder's current-chapter check, and fresh-kernel/visual verifiers.
- Updated `.gitignore` with explicit new-file allowances; no private source
  directory was unignored.
- Added Ch3 links to root README and syllabus. Updated PROJECT, COURSE_PLAN,
  both maintenance READMEs, and full_source_audit with current availability.
- Clarified the authoring prompt: Ch3 is conceptual ER; mapping belongs in Ch9.

Review corrections before release: removed a shared line segment that could
make TEACHES look connected to ENROLLS_IN, separated a ratio label from its line,
and added a gap where unrelated lines cross. Explicitly distinguished simplified
relationship close-ups from the final weak-entity notation; added plain-language
oval/diamond definitions. Expanded profiles and other small variants are not
silently added to the final core model. Each affected artifact was rebuilt and checked.

The student notebook contains original worked examples, not hidden assessment
solutions or teacher grading data. It has no textbook screenshots, private paths,
credentials, personal records, external data dependency, or new mandatory submission.
The maintenance tests verify the displayed examples; they are not unreleased exam keys.

## Limits and Next Action

The approximately 4,800-word guide is a complete reading resource, not a requirement
to complete every practice variation in one meeting. Actual classroom pace and
projector legibility at the back of the room remain untested. Phone-sized previews
do not overflow, but diagram text needs enlargement; equivalent rules and input
facts are available in surrounding text and tables. Local rendering is not a
claim that GitHub's UI has been visually checked after publication.

Ch4 and subsequent missing revised chapters are unfinished. The old ER SQL
NULL-key defect remains blocked from reuse and was not imported or modified.
The SQLite ZIP is historical and was neither revised nor re-certified for this Ch3
release. No official seventh-edition slide deck or independent reviewer was used.

Primary next action: prepare Ch4 Sections 4.1-4.7 in one notebook, prioritizing
4.1-4.4 for Week 3 and reusing the campus case. It is next because Ch3 now fills
the preceding scheduled gap. Completion requires source-located explanations,
diagrams, examples, predictions, interpretation, practice, and successful rebuild
and rendering checks. Ch4 work has not begun in this release.

## Git Publication

The instructor authorized committing this intentional change set and pushing it
to the existing origin/main. The commit containing this record identifies the
release. Push completion, remote-head comparison, and post-push status are reported
in the task's final response; no textbook or ignored output is included.
