# Ch3 ER Teaching Release

## Publication Authorization After the Audit

On 2026-09-12, after receiving the completed audit below, the instructor explicitly
requested commit and push. This supersedes the audit's pending-authorization next
step. The authorized change is the corrected answer PDF and five related tracked
maintenance files, targeting `origin/main`. The reviewed PDF SHA256 remains
`79ecb018e4646c4ebe0ed83eae85376b4a69b22c0c9254e56c8e0015d0736c87`.
Private sources, photographed textbook pages, other chapters, and ignore rules
are excluded. No further answer-content changes are made during publication.
The five modeling-application tasks remain uncompleted. The no-commit/no-push
statements below describe the preceding audit stage, not this later authorization.

## 2026-09-12 Answer Requirements Audit

Date: 2026-09-12. Baseline: `23b5c8c766d2a107d3280cf15255a8355a98b868`
on `main`, initially clean and equal to the local `origin/main` tracking ref.
Remote: `https://github.com/KennethWYLee/Database.git`.

The instructor approved the next step after questioning whether the published
answers directly answered the photographed exercises. This audit checks every
question and explicit subpart, corrects the local maintained answers, and rebuilds
the local answer PDF. It does not authorize or perform a new commit or push.
The syllabus, grading policy, taught scope, and Ch1-Ch3 teaching notebooks are unchanged.

### Conclusion

The baseline was not a fully verified answer set. In particular, 3.5 answered a
different comparison, 3.21 omitted specified domains, and 3.25 discussed but did
not draw the ternary ADOPTS relationship. Numbering and successful rendering did
not establish completeness of the answers.

The revised written responses to 3.1-3.30 have been checked against the complete
question requirements. For 3.31-3.35, the conceptual answers are supplied, but the
original tasks remain incomplete because no model was entered and checked in a
data-modeling application. ERwin and Rational Rose are examples in the textbook,
not the only possible tools; Python-generated figures do not establish that this
separate application requirement was performed. No tool substitution is approved
by this audit. Every lab answer now states this limitation at its start.

These are original worked answers, not official publisher solutions. Open designs
are conditional on their stated assumptions. The same agent performed the source
review and the edits; this is not independent instructor or expert review.

### Sources and Method

- Authoritative questions: instructor's `Database pdfs/Chapter3.pdf`, 24 photographed
  spreads, printed pp.89-135; SHA256
  `55366a1faa7718dd1b89bdb95a938db5c5e7b00886f99aeb88a16086409e72c7`.
- Every question and continuation on printed pp.126-134 was visually read, including
  Figures 3.21-3.25. Spreads 20-24 contain those complete questions. The summary and
  Figure 3.20 on spread 19 and the UNIVERSITY requirements on spread 18 were checked.
- Relevant explanatory passages in 3.1-3.9 were visually checked on spreads 2-18:
  definitions, domains, NULL, notation, keys, weak identification, attribute
  placement, recursive relationships, min-max versus ratios, ternary constraints,
  and UML. The audit does not claim to have reread the entire book.
- Supplement for 3.20: local `private_references/book_Fundamental of Database Systems.pdf`,
  Elmasri/Navathe, seventh edition; SHA256
  `002eceecdb5e47b050e61b30d13a8f207fb44cea4f927b98d864308c026288a5`.
  Ch1 1.4-1.5, printed pp.15-17, and Ch2 2.4.1-2.4.3, printed pp.42-46, were read
  for users, administration, design, programming, catalogs, modules, and tools.
- The entire maintained answer text was read. Each required definition, field,
  relationship, bound, subpart, requested drawing, and tool action was compared
  with its answer. Selected analytic consequences were checked using separately
  constructed data examples in `private_references/ch03_solutions/verify.py`.
  Those tests share the source interpretation with the prose; they are not a
  second independent authority or a proof that every open design is correct.
- The private baseline files were preserved before editing in
  `private_references/ch03_solutions/qa/audit_baseline_23b5c8c/`.

The locations below use numbered sections of maintained `solutions.md`, which
become the same headings in the generated notebook and PDF. Figure identifiers
refer to original drawings in its `figures/` directory, not copied textbook figures.
Question requirements are paraphrased rather than reproduced verbatim.

### Review Questions

| Question / printed page | Requirements checked | Answer location and evidence | Finding and disposition |
|---|---|---|---|
| 3.1 / 126 | Role of high-level conceptual modeling in the design process | 3.1; four-step table; q01; source 3.1, pp.90-92 | Directly answered. Requirements, communication, logical mapping, and physical implementation remain distinct. |
| 3.2 / 126 | Appropriate cases for NULL | 3.2; three cases with examples; source p.96 | Directly answered. SQL storage does not preserve the conceptual reason by itself. |
| 3.3 / 126 | All ten named definitions | 3.3; ten-row definition/example table; source 3.3-3.4 | All ten present: entity, attribute, attribute value, relationship instance, composite, multivalued, derived, complex, key, value set. |
| 3.4 / 126 | Entity type and set; contrast both with an entity | 3.4; S1/S2/S3 example; source pp.97-99 | Directly answered by schema versus current objects. |
| 3.5 / 126 | Attribute versus value set | 3.5; q05; Credits property/domain/actual-value example; source pp.99-100 | **Corrected wrong target.** Baseline compared an entity with an attribute value. New answer distinguishes property, allowed values, actual value, and current database values. |
| 3.6 / 126 | Relationship type, instance, and set | 3.6; TAKES set with three pairs; source pp.102-103 | All three present and distinguished. |
| 3.7 / 126 | Participation role; when role names are necessary | 3.7; supervisor/supervisee and q07; source pp.104-105 | Direct answer. Reversing roles changes the fact; recursive binary relationship uses the book's convention. |
| 3.8 / 126 | Two structural-constraint notations; advantages and disadvantages | 3.8; comparison and q08; source pp.106-108,114-115,121-122 | Direct answer. Minimum four is lost by ordinary 1/N plus line style; ternary key constraints differ from counts. |
| 3.9 / 126 | Conditions for moving a binary relationship attribute | 3.9; 1:1, 1:N, M:N cases; q09; source p.108 | Conditional answer correct. Two employees with different start dates refute placement on the department. Optionality/history qualifications retained. |
| 3.10 / 126 | Values of relationship-valued attributes; model family | 3.10; D, E, P(E) example; source p.104 including footnote | Clarified the entity-set and power-set domains; explicitly identifies functional data models. Removed an unnecessary object-database aside. |
| 3.11 / 126 | Recursive relationship definition and examples | 3.11; supervisor, parent, prerequisite; source p.105 | Directly answered. Roles and extra no-cycle constraints distinguished. |
| 3.12 / 126 | When weak types are used; four requested definitions | 3.12; definition/example table; q12; source p.109 | Added explicit definitions for owner type, weak type, identifying relationship, partial key; owner-local versus global identity preserved. |
| 3.13 / 126 | Can identification have degree above two; examples | 3.13; INTERVIEW q13; invented patient-clinic visit; source pp.120-121, Fig.3.19 | Added a second explicit example. Both require two owners plus the weak entity and stated local uniqueness. |
| 3.14 / 126 | ER drawing conventions | 3.14; symbol table; source pp.111-113, Fig.3.14 | Conventions covered, including independent keys versus composite keys, partial keys, roles, and participation. |
| 3.15 / 126 | Naming conventions | 3.15; construct/name/example table; source p.112 | Directly answered using the book's uppercase/singular/initial-capital/lowercase conventions. |

### Written Exercises

| Question / printed page | Requirements checked | Answer location and evidence | Finding and disposition |
|---|---|---|---|
| 3.16 / 126-127 | All a-c uniqueness rules and another plausible constraint | 3.16; rule/counterexample tables; UNIVERSITY pp.122-124 | Strengthened the answer to the question's SECTION-key wording: a/b involve TAKES and cannot be SECTION-only keys; c already follows from one teacher per SecId. Added the explicit room/term/time combination. |
| 3.17 / 127 | Nested job history, all fields, Figure 3.5 notation | 3.17; nested text and sample table; Fig.3.5 p.97 | Changed to the book's brace-around-multivalued-attribute notation. Company/date, position/month/year, pay/allowances/duration/grade all present. No unsupported position/salary pairing invented. |
| 3.18 / 127 | Alternative design using entity and relationship types | 3.18; five types, keys, q18 | All 3.17 fields retained, owners and return employment distinguished. Artificial local IDs and salary minimum explicitly assumed. |
| 3.19 / 127-128 | Precise requirements extracted from AIRLINE diagram | 3.19; eight-type inventory, eleven-relationship table, q19a-c | Tables were substantially correct. Added CAN_LAND, TYPE, ASSIGNED to the visual set. Optional actual events versus mandatory scheduled airport and aircraft assignment checked directly. |
| 3.20 / 127 | General database-environment types, relationships, ER drawing | 3.20; ten types, fourteen relationships, q20/q20b/q20c; Ch1/2 supplement | Expanded the narrow six-type baseline to include catalog, people and roles, hosts, modules, tools, development, and operation. Explicitly bounded organizational inventory with declared assumptions; not a universal vendor architecture. |
| 3.21 / 127-128 | State/member/bill/voting information, complete supplied domains, sponsors, diagram, assumptions | 3.21; attribute/domain/example tables; q21 | Added all five regions, four party categories, Yes/No bill result, first-election date meaning. Existing four vote states and sponsorship separation retained. Missing rows are not Absent votes. |
| 3.22 / 128-129 | Teams, players including nonparticipants, game-specific positions/result, chosen sport and assumptions | 3.22; q22; scores and appearance tables | Direct answer. APPEARANCE owns positions; COMPETES owns score/result. One-season roster and participating-team/roster consistency are explicit. |
| 3.23 / 129-130 | All a-f BANK requirements | 3.23; type list, q23, five-row relationship table, updates | Added explicit justification from single/double lines and 1:N/M:N labels, not just final min-max values. All attributes and three part-f changes retained. |
| 3.24 / 130 | Bounds on all three links, assumptions, HAS_PHONE redundancy | 3.24; q24; concrete derived pairs | Direct conditional answer. Maximum six follows only when HAS_PHONE equals department-phone composition and each phone has one department. |
| 3.25 / 130 | Binary bounds, missing assumptions, binary versus ternary ADOPTS, its bounds and reasons | 3.25; q25/q25b; two legal assignment states | Added actual ternary drawing and swapped-course counterexample. Instructor maximum 20 counts triples, not texts or per-course total. Course/text totals are unbounded under the declared subset interpretation. |
| 3.26 / 131 | Three composite SECTION keys and ER representation with shared components | 3.26; key/assumption table; q26 | Direct conditional answer. Offering key is given; room and teacher keys need no-conflict/no-combined-section assumptions. No reliance on the separate UNIVERSITY SecId design. |
| 3.27 / 131 | Ratios and assumptions for all ten pairs | 3.27; ten-row table | All pairs and direction checked. Product type versus order-line ITEM explicitly distinguished; maxima do not establish minima. |
| 3.28 / 131-132 | Thirteen truth judgments and justification from Fig.3.25 | 3.28; label table, q28, paired witnesses | No label changed. Added a true and false legal state for each of ten Maybe statements, including negative f/m and the quantifier in j. Added a cross-movie witness for g. |
| 3.29 / 132 | Three recent movies, instances of all four types, real relationships | 3.29; 2025 releases, credit table, six relationship sets, q29 | Rechecked official credit sources; replaced a redirected Universal URL. Corrected the false description of Hiccup as a title character. Lead classification is an explicit teaching inference; selected credits are not complete filmographies. |
| 3.30 / 133 | UML model plus all operations in a-c | 3.30; q30/q30b, class table, new a-c operation-effects table | Operations were present; added inputs/effects/constraints so each subpart has a direct answer. GPA example remains illustrative, not institution policy. |

### Explicit Subparts

| Subpart | Requirement and checked answer |
|---|---|
| 3.16(a) | One current Grade per student-section. (Sid,SecId) determines Grade on TAKES; a second conflicting grade fails. |
| 3.16(b) | No student's simultaneous sections in a term. (Sid,Sem,Year,DaysTime) determines SecId; exact equality and interval overlap are distinguished. |
| 3.16(c) | No two teachers for the same section. SecId determines instructor, already required by TEACHES. Term and Sid do not strengthen global SecId. |
| 3.16, final prompt | Additional room/term/time uniqueness is supplied, with no combined sections and exact slot assumptions. |
| 3.23(a) | BANK, ACCOUNT, LOAN, CUSTOMER are regular. |
| 3.23(b) | BANK_BRANCH is weak, Branch_no partial, BRANCHES identifying. |
| 3.23(c) | Same-bank branch-number uniqueness, exactly one bank owner, total branch identification. |
| 3.23(d) | All five relationships and both ends' min-max pairs, justified by figure line styles and ratios. |
| 3.23(e) | User requirements include identity, all displayed attributes, ownership, optionality, and joint accounts/loans. |
| 3.23(f), account | CUSTOMER in A_C becomes (1,N). |
| 3.23(f), customer loans | CUSTOMER in L_C becomes (0,2). |
| 3.23(f), branch loans | BANK_BRANCH in LOANS becomes (0,1000); unrelated bounds unchanged. |
| 3.27(1-5) | Student/card 1:1; student/teacher M:N; room/shared wall M:N; country/current president 1:1 in the assumed model; course/text M:N. |
| 3.27(6-10) | Product/order M:N; student/class M:N; class/instructor N:1; instructor/shared office N:1; auction listing/bid 1:N. Each has an assumption or alternative. |
| 3.28(a,d,g) | True, True, False respectively. Total actor participation, maximum two movie leads, and permitted producer/actor overlap across movies justify them. |
| 3.28(b,c,e,f,h,i,j,k,l,m) | All Maybe; ten paired legal states give both truth values. The verifier asserts each individual claim on those states, not only general schema validity. |
| 3.30(a) | computeGPA and add/drop majors/minors; grade/credit calculation and the two associations. |
| 3.30(b) | add/delete course and hire/terminate instructor; OFFERS/EMPLOYS with dependent-link checks. |
| 3.30(c) | assign/change grade; existing enrollment and authorized instructor; one current Grade. |

### Laboratory Requirements

| Lab / printed page | Conceptual requirements checked | Remaining requirement |
|---|---|---|
| 3.31 / 133 | UNIVERSITY six types, nine relationships, all keys/attributes, Grade/CStartDate, 3.16 constraints; q31a/b. Fig.3.20 versus prose HAS minimum conflict is disclosed; figure variant used. | Enter and verify a model in a data-modeling application. Not performed. |
| 3.32 / 133 | Employee/customer IDs, names and ZIP; part ID/name/price/stock; order ID/three dates; one employee/customer, one-or-more parts and quantity; q32. Multi-owner ORDER_LINE preserves each order-part pair. | Enter and verify the MAIL_ORDER model in an application. Not performed. |
| 3.33 / 133-134 | Movie title/year key, length **in minutes** (added), company, genres, directors, actors/roles, plot, zero-or-more quotes linked to the speaking actor's appearance; person keys and overlap; q33. | Enter and verify the MOVIE model in an application. Not performed. |
| 3.34 / 134 | Author/reviewer identities and fields; paper metadata and multiple authors; contact-author subset; 2-4 reviews; all four 1-10 scores; acceptance/rejection recommendation; two audiences' comments; q34. Completed-review check now requires both comments. | Enter and verify the CONFERENCE_REVIEW model in an application. Not performed. |
| 3.35 / 134 | Full AIRLINE inventories/three diagrams in 3.19 referenced explicitly; dated owner identity q35; optional actual departure and required assignment checked. | Rebuild and verify Fig.3.21 in an application. Not performed. |

### External Evidence for 3.29

Official pages were opened during this audit on 2026-09-12:

- [Warner Bros./DC Superman](https://www.superman.com/home/): James Gunn directs;
  Gunn/Peter Safran produce; David Corenswet and Rachel Brosnahan are selected
  performers; 2025 release and Superman/Clark Kent character identification.
- [Universal film page](https://www.universalpicturesathome.com/movies/how-to-train-your-dragon-2025)
  and [Universal final home-release press release](https://www.universalpicturesathome.com/press-release/how-to-train-your-dragon-2025-press-release):
  Dean DeBlois directs; Mason Thames plays Hiccup, Nico Parker plays Astrid;
  final ordinary producer credits identify Marc Platt and Adam Siegel.
- [Disney Snow White](https://movies.disney.com/snow-white-2025): Marc Webb directs;
  Marc Platt/Jared LeBoff produce; selected cast includes Rachel Zegler and
  Gal Gadot; the page identifies Zegler as Snow White and the 2025 release.

The previous Universal video URL redirected to a theme-park page and no longer
supported producer claims. It was replaced, not silently treated as still verified.
Advance publicity and final ordinary/executive producer credit categories are not
merged. The three selected lead roles are justified teaching classifications, not
a claim that the official sources label exactly those people as the only leads.

### Verification

Environment: Windows PowerShell; Python 3.12.9; SQLite 3.45.3; Node 24.15.0;
nbformat 5.10.4; Pillow 12.1.1; resvg-py 0.5.0; markdown-it-py 4.0.0;
PyMuPDF 1.27.2.2; Beautiful Soup 4.14.3; Poppler 26.07.0. Rendering used the
installed Google Chrome through the bundled Playwright runtime. SQLite is recorded
as an environment fact; no new SQL lab was introduced by the answer audit.

Commands were run from the course root:

| Command | Final result |
|---|---|
| `python -X utf8 private_references/ch03_solutions/build.py` | PASS: 35 answers, 31 original figures, 38 Markdown-only notebook cells. |
| `python -X utf8 private_references/ch03_solutions/verify.py` | PASS: 18 tests, including all ten Maybe pairs, the cross-movie g counterexample, domains, ternary information loss, AIRLINE relationship coverage, source identity, manifests, and review completion fields. |
| `node private_references/ch03_solutions/render.cjs` | PASS: widths 1440 and 390; 35 headings, 31 loaded images, no horizontal overflow/broken images; all 31 SVGs have no detected text overlaps or out-of-bounds text. |
| `python -X utf8 private_references/ch03_solutions/export_pdf.py` | PASS: 56 pages, all source HTML text tokens retained, 31 embedded figures, metadata/bounds checks. All pages rendered with Poppler. |
| `python -X utf8 maintenance/course_repository/build_course_repository.py --verify` | PASS: 8 public-path files; three teaching notebooks checked and executed. No teaching notebook/PDF changed. |
| `python -X utf8 -m unittest discover -s maintenance/course_repository -p 'test_*.py'` | PASS: 48 tests. |
| `git check-ignore -v` on private answers, photographed Chapter3.pdf, and Ch5 notebook | PASS: all remain ignored under existing rules. |
| `git diff --check` | PASS; only the repository's existing LF-to-CRLF notices were emitted. |
| `git ls-remote origin refs/heads/main` | Remote remains `23b5c8c766d2a107d3280cf15255a8355a98b868`; no push occurred. |

The final PDF is `Intro DB/ch03_answer.pdf`: 56 A4 pages, 2,060,908 bytes.
SHA256: `79ecb018e4646c4ebe0ed83eae85376b4a69b22c0c9254e56c8e0015d0736c87`.
Its source-notebook SHA256, also recorded in PDF metadata and repository config:
`a6765354e870481bc7088a5e7ee9a52a3d8baf644378bc8b74ed086a0d9e37b3`.
Maintained `solutions.md` SHA256:
`4d26d19027f1b7d46adce199c35030ffc710531b461db433fbf4a600b4d5a5ce`.

All five overview sheets covering all 56 final pages were visually inspected.
PDF pages 4, 20, 32, 38, 44, and 53 were additionally inspected at readable
resolution for the corrected comparison, long environment diagram, ternary
diagram, full witness table, UML labels, and conference constraints. No clipping,
overlapping labels, missing text, or broken figures was found. Some whitespace
remains to keep complete figures and tables together. Dense UML content may
require zoom for classroom projection; this is an answer reference, not a slide deck.
Final QA renders are under the ignored `qa/pdf/79ecb018e4/` directory.

The public PDF has no embedded attachments, private paths, scans, publisher
solution material, or extra chapters. Only the authorized original answers are
included. The private sources, intermediate HTML/notebook, and QA outputs stay
local. PDF timestamps prevent a promise of byte-identical re-export; the reviewed
file's recorded hash identifies this particular final output.

No final automated check failed. The five modeling-application tasks were not
executed and are not counted as passed tests. Image counts verify presence,
source hashes verify identity, paired data examples check consequences, and
visual inspection checks layout. None alone establishes pedagogical suitability.

### Changed Files and Boundaries

- Ignored maintained answers: `private_references/ch03_solutions/solutions.md`,
  `build.py`, `verify.py`, `export_pdf.py`, and `README.md`.
- Regenerated ignored outputs: figures, HTML, notebook, manifest, and QA renders.
- Local public-path output: `Intro DB/ch03_answer.pdf` only. No textbook pages,
  copied publisher diagrams, private records, or official solutions are embedded.
- Repository maintenance: this report, current status in `PROJECT.md`, a pointer
  in the build README, answer PDF/source hashes in
  `repository_config.json`, and the expected figure count in its layout test.
- Original ignored maintained sources remain ignored. A public clone can verify
  the published PDF but cannot rebuild it without the instructor's private sources.
- No stage, commit, push, remote change, pre-existing-file deletion, or history
  rewrite in this audit. The report was consolidated into this already tracked
  file; no Git ignore rule was changed to expose a new report or private source.

Final Git state: `main...origin/main`, six intentional modified tracked files
(answer PDF, PROJECT, build README, this report, repository config, layout test),
none staged. The ignored maintained-answer edits are additional local changes
and therefore do not appear in ordinary `git status`.

### Limits and Next Action

Five modeling-application deliverables remain unperformed. Open designs, the
UNIVERSITY figure/prose conflict, simplified current-state assumptions, and the
selected nonexhaustive movie instance are explicitly stated, not resolved by fiat.
No institutional grading, software requirement, or course workload was changed.

Primary next action: after instructor authorization, commit and push the corrected
answer PDF and its intentional maintenance records. The old public version contains
the confirmed wrong-target answer to 3.5. Completion means the remote commit and
downloaded answer PDF match the audited local hash. Tool-based lab completion is
a separate remaining task and must not be concealed by that publication.

The sections below preserve earlier release evidence and hashes. The current
requirements audit above supersedes their answer-completeness claims.

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
