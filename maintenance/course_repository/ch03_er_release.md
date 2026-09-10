# Ch3 ER Teaching Release

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
