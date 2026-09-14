# Ch3 ER Teaching Release

## 2026-09-14 Publication Authorization

The instructor explicitly requested commit and push after the corrections below.
This commit includes the accumulated Ch3 diagram/data corrections, fourteen new
worked figures and removal of duplicated labels, with the current 41-image,
48-page export. The hashes in the next entry remain unchanged. Earlier statements
of local-only work describe their respective editing stages, not this authorization.
Before staging, `git fetch origin` succeeded and `HEAD...origin/main` reported
0/0 at baseline `99462b4`. The default build/manifest/public-content verification
was rerun successfully. Only the twelve intentional tracked Ch3 material,
renderer, test and record files are included; no ignored source, textbook,
private record, answer change or additional chapter is part of the commit.
The target is the existing `origin/main`; no history rewrite or remote change
is authorized or needed. Git history records the resulting publication commit.

## 2026-09-14 Remove Duplicated Figure Titles and Captions

The instructor supplied a screenshot of the room-lookup example showing the
same title twice. The generated notebook cell contained a heading and caption,
while its PNG also painted the same heading and conclusion. The previous tests
did not detect this visual duplication. This local formatting correction keeps
the existing source/content decisions and all prior uncommitted work.

All 41 Ch3 figures now use `text_outside_image`: the image contains the figure
body, while the notebook/PDF supplies one visible, searchable title and one
caption. Repeated image titles, conclusions, and generic illustration subtitles
are removed. Internal panel titles, table values, diagram symbols, notes about
omitted attributes, and connections remain. SVG accessibility title/description
and notebook alternative text are retained; they are not second visible headings.

The option defaults off in the shared renderer and is enabled only for Ch3.
Ch1 and Ch2 notebook hashes remain unchanged. No change to chapter coverage,
assignments, practice, prose explanations, source assertions, syllabus, answers,
public selection or ignore rules is included. No new textbook audit is claimed.

Maintained changes in this correction: `er_figures.py`, `teaching_figures.py`,
`test_ch03_er.py`, `PROJECT.md`, and this record. Derived artifacts rebuilt:
`Intro DB/ch03.ipynb` and `Intro DB/ch03.pdf`. Earlier uncommitted corrections
to other files remain intact. Git HEAD remains `99462b4` on `main`; there was
no staging, commit, push, remote change or deletion.

Current notebook: 128 Markdown cells, 41 PNGs, no executable cells.
Notebook SHA256: `56292c5f23cc8488316cfaaaeb3de31a7b80b59f3c6ae1ebd06e8905cf15e729`.
Current PDF: 48 pages, 41 images, 1,540,664 bytes.
PDF SHA256: `299660532d91f7db220c3f3bc6e7535bb47c070c6eae72a81188cbbb7b083c0f`.
This supersedes the preceding 54-page export and its page-location list.
The room-lookup example is now on PDF page8; the grade matrix is on page22,
enrollment lines on page11, and weak-item lookup on page25.

Verification, using the environment documented in the preceding entry:

- All 70 repository tests passed, including 34 Ch3 tests. Three new tests check
  exactly one external heading/caption, no painted duplicate, preservation of
  all figure-body words compared with the previous renderer mode, and searchable
  PDF titles occurring once. Other tests retain symbol, endpoint and data checks.
- All 41 PDF images match the current notebook images in RGB pixel content.
- Three fresh-kernel notebook checks, the 9-file manifest, public boundaries and
  default build verification passed. Ch3 itself still contains no executable lab.
- All 48 PDF pages were rendered and inspected in four overviews; page8's corrected
  room figure and page20's role diagram/table were inspected at full page size.
- Desktop1440/mobile390 previews passed with no broken images, page overflow or
  detected figure-text overlap. Mobile wide tables still scroll horizontally;
  dense pictures still require zoom. Real classroom projection remains untested.
- `git diff --check` passed; line-ending conversion notices are not content failures.

```powershell
python maintenance/course_repository/build_course_repository.py
python maintenance/course_repository/export_chapter_pdfs.py --chapters ch03
python -m unittest discover -s maintenance/course_repository -p 'test_*.py'
python maintenance/course_repository/verify_first_meeting.py
node maintenance/course_repository/render_first_meeting.cjs
python maintenance/course_repository/build_course_repository.py --verify
git diff --check
git status --short --branch
```

Primary next action: check page8 against the supplied screenshot to confirm that
one heading, one table and one caption meet the instructor's intended presentation,
then continue the previously recommended three-example classroom review. The new
evidence was visual duplication, not a gap requiring further teaching content.

## 2026-09-14 More Worked Figures for Classroom Explanation

This local revision continues the uncommitted corrections below, on `main` at
`99462b47cac70829b9dd45330a2c54c4953a4deb`, tracking `origin/main`. The instructor
reports primarily explaining pictures and tables, with little use of Practice.
The current request authorizes more explained illustrations, not Git publication,
removal of practice, or changes to scope, grading, or required submissions.

### Result

Ch3 retains the existing 27 figures and adds 14 figures in 13 worked examples.
Each new example supplies concrete inputs, a checkable prediction, a displayed
figure or table, and an explanation with actual values before its Practice text.
Five new images are diagrams (four object-connection views and one ER attribute
close-up); nine are comparison tables. Additional Markdown tables explain
attribute changes, counts, role participation, and missing versus zero grades.
The contact prediction was clarified to count entities, values, and components
separately; M:N is expanded before the first new figure uses the abbreviation.

The current notebook has 128 Markdown cells and 41 embedded PNG figures; it
contains no student-executable code. The PDF has 54 pages and 41 matching images.
The 42-page/27-figure export recorded below is the preceding local version.
No new textbook topics, SQL prerequisites, required activities, or assignments
were added. Ch1, Ch2, the syllabus, answer PDFs, ignore rules and public selection
are unchanged. Other chapters have not received this visual expansion.

### Sources and Example Checks

Concepts were checked in the local searchable *Fundamentals of Database Systems*,
7th edition, Elmasri/Navathe, `private_references/book_Fundamental of Database Systems.pdf`.
Its SHA256 remains `002eceecdb5e47b050e61b30d13a8f207fb44cea4f927b98d864308c026288a5`.
Page numbers in this table are that PDF's printed page numbers, not the photographed
edition's numbers used in the student reading list. For example, printed p.79
is PDF page110 and corresponds to photographed p.109. Section numbers identify
the same concepts across the two paginations. The existing photographed-source
audit remains in force; this is not another complete chapter-by-chapter book audit.

| Figure suffix after opening_ch03_ | Source concept / local printed pages | Original teaching evidence checked |
|---|---|---|
| contact | 3.3.1, pp.65-67; notation in 3.3.2, p.68 | One student, two component pairs; double Contact oval plus component ovals. Replaces, rather than duplicates, the bare Phone variant. |
| key_lookup | 3.3.2, p.68 | A/101, A/102, B/101 produce lookup counts 2, 2, 1. The requirement supplies the key guarantee. |
| missing_values | 3.3.1, p.66 | Known zero, unfinished grade, confirmed no permit, and unchecked permit status remain separate meanings. |
| enrollment_links | 3.4, pp.74-78 | All three ENROLLMENTS facts become exact endpoint pairs; unconnected S103 and DB101/2 remain visible. Grade omission is explicit. |
| one_to_one | 3.4.3, pp.76-77 | S101/K10 and S102/K11, with S103 unconnected. Separate one-card variant, not the later multiple-card variant. |
| one_to_many | 3.4.3, pp.76-77 | The three TEACHES facts give I1 two sections and I2 one, with one instructor per section. |
| participation_changes | 3.4.3, pp.77-78 | Independent proposed states produce allowed/rejected/rejected/allowed; 0 violates a section minimum and 2 violates its maximum. |
| notation_counts | 3.7.4, p.84; Figure3.14, p.83 | Counts 2 and 1; opposite-side maximum labels versus same-side min-max, for the same binary requirements. |
| mentor_roles | 3.4.2, p.75 | One STUDENT set appears in two roles; the two lines match exactly S101/S102 and S101/S103. |
| grade_matrix | 3.4.4, p.78 | Matrix contains exactly 80, 90 and 70 at the supplied pairs, with six nonexistent enrollments. Unknown and zero are separate later states. |
| weak_lookup | 3.5, p.79 | Owner-free descriptions each leave two matching items; owner O10 plus LineNo1 leaves one. Product/Quantity do not identify an item. |
| ternary_states | 3.9.1, pp.89-91 | Adding S101/I1/CS102 changes three triples to four but all three pair sets remain identical. Later variant constraints are explicitly excluded. |
| university_staff_facts | 3.10, pp.92-94, Figure3.20 | Four sets of organization facts distinguish required employment from optional chairing; omitted attributes are identified. |
| university_enrollment_change | 3.10, pp.93-94 | Five distinct TAKES facts become four while section and student entities remain; repeated copies do not increase set cardinality. |

These tables and drawings are original adaptations with synthetic records, not
copied textbook artwork or solutions to newly released assessment questions.
The source HAS prose/figure discrepancy remains explicit and unchanged.

### Files and Verification

Maintained files changed in this expansion:

- `maintenance/chapters/ch03_er_model/student_guide.md`: explained examples and tables.
- `maintenance/course_repository/er_figures.py`: fourteen figures; reuse of the existing network and ER renderers.
- `maintenance/course_repository/test_ch03_er.py`: eight new checks, including independent count calculations and rendered endpoint-to-record checks.
- `maintenance/course_repository/test_repository_layout.py` and `verify_first_meeting.py`: current expected figure totals.
- `maintenance/course_repository/render_first_meeting.cjs`: screenshots of new worked examples at desktop/mobile widths.
- `PROJECT.md` and this record: decisions, source scope, checks and limits.

Derived files rebuilt: `Intro DB/ch03.ipynb`, `Intro DB/ch03.pdf`. Prior uncommitted
changes to `teaching_figures.py` and `export_chapter_pdfs.py` were preserved; this
expansion did not further change them. Temporary HTML, figures, page renders,
manifests and QA JSON remain ignored under `maintenance/course_repository/output/`.

Final notebook SHA256: `d9e1ffdf7057c54c654bc35bf12aced7562566c5ad286dc91c03ec6d1cf99482`.
Final PDF SHA256: `88f0a5eb23168374e5b0a72d622d90b2c70f1c001c3c89e3afb70caf0f61395b`.
PDF size: 2,324,836 bytes. Metadata records the matching notebook SHA256.

Commands run from the course root:

```powershell
python maintenance/course_repository/build_course_repository.py
python maintenance/course_repository/export_chapter_pdfs.py --chapters ch03
python -m unittest discover -s maintenance/course_repository -p 'test_*.py'
python maintenance/course_repository/verify_first_meeting.py
node maintenance/course_repository/render_first_meeting.cjs
python maintenance/course_repository/build_course_repository.py --verify
git diff --check
git status --short --branch
```

- 67 repository tests passed, including 31 Ch3 tests. The tests check actual graph
  endpoints, example counts, unchanged pair sets, matrix entries/absences, headings,
  explanations, public boundaries, and PDF/notebook RGB pixel equality for all 41 images.
- Three fresh kernels passed Ch1-Ch3 verification; Ch3 has zero code cells, so this
  is notebook/environment verification, not a claim of executing a Ch3 SQL lab.
- The default build verified 9 public files, the manifest, source/output correspondence,
  relative links and all three notebooks. Ch1/Ch2 notebook hashes remain unchanged.
- Desktop1440/mobile390 previews have no broken images, page overflow, or reported
  figure-text overlap. All fourteen new figures were visually read at full size.
- All 54 PDF pages were rendered and inspected in five overviews. After the final
  two wording changes, only page06 and page12 PNGs changed; both were reread at
  full page size. Page25's grade matrix was also read at full size. The other 52
  page PNGs matched the already inspected version byte for byte.
- English-only text, absence of time allocation and internal paths, separated
  answer publications, and unchanged public chapter selection passed existing checks.

Environment: Python3.12.9, SQLite3.45.3, Pillow12.1.1, nbformat5.10.4,
PyMuPDF1.27.2.2, resvg-py0.5.0, markdown-it-py4.0.0, BeautifulSoup4.14.3;
Chrome153.0.8010.36, Node24.15.0, Poppler26.07.0. Arial supplies figure text.

Intermediate failures are not hidden: verification initially rejected a stale
PDF after the first notebook build, then passed after regeneration. One newly
written test incorrectly parsed the phrase "Still 4" as an integer; its assertion
was corrected to test that exact display label, while a separate assertion counts
the displayed distinct participants. An earlier fresh-kernel run completed but
logged a ZMQ shutdown callback error; the final repeated run completed without
that message. No dependency changes were made to suppress it.

### Limits and Primary Next Action

This is a targeted source/content/build/render check by the same assistant, not
independent expert or instructor review. Count calculations use a different
check from figure construction but share the stated synthetic inputs. Tests do
not establish classroom comprehension. Dense images need zoom on mobile;
Markdown tables use horizontal scrolling. Real classroom projection, GitHub's
live rendering of this unpushed revision, and student learning outcomes were not tested.

Primary next action: the instructor should review the enrollment-line picture,
Grade matrix and weak-item lookup using the classroom display. They directly test
the requested change from practice-dependent explanation to visual explanation.
Completion means the instructor can explain the data, rule and conclusion from
those displays without requiring students to finish Practice first. No additional
content expansion is the priority before this feedback. No staging, commit, push,
remote change or destructive operation occurred; prior local work is preserved.

## 2026-09-14 Local Diagram Corrections

Baseline: `99462b47cac70829b9dd45330a2c54c4953a4deb`, clean `main`, tracking
`origin/main`. The instructor approved the corrections identified after using
Ch3 in class. This approval is for local editing and verification, not staging,
commit, push, or a change to the public release allow-list.

### Result and Scope

The existing 14 Ch3 tests passed on the flawed version. They did not establish
that every declared property appeared in a figure, that a before/after example
retained its names and objects, or that corresponding checks occupied one row.
Those gaps are now tested against the actual figure definitions and artifacts.

The chapter still contains 27 figures and covers the same textbook sections.
Eleven embedded PNGs changed; the other sixteen remain byte-identical to the
baseline notebook. Ch1, Ch2, the syllabus, answer PDFs, private source files,
ignore rules and grading policy are unchanged. PDF pagination changed from
41 to 42 pages because of the expanded tables, not an added teaching topic.

Maintained sources changed:

- `maintenance/chapters/ch03_er_model/student_guide.md`: explanations of Phone,
  the hypothetical fourth student, recursive roles, Product, omitted attributes,
  the same-section refinement and the combined check table.
- `maintenance/course_repository/er_figures.py`: the eleven changes below.
- `maintenance/course_repository/teaching_figures.py`: an opt-in full-width,
  vertically stacked table layout. Existing side-by-side rendering is unchanged.
- `maintenance/course_repository/test_ch03_er.py`: nine new tests, including
  figure/prose data agreement, semantic counterexamples and PDF pixel retention.
- `maintenance/course_repository/render_first_meeting.cjs`: table-text overlap
  checks as well as ER labels; screenshots target both headings and the actual
  following figures at desktop and mobile widths.
- `maintenance/course_repository/export_chapter_pdfs.py`: `--chapters ch03`
  regenerates only the selected approved teaching PDF, without rewriting others.
- `PROJECT.md` and this record: local state, results and limitations.

Derived artifacts rebuilt: `Intro DB/ch03.ipynb` and `Intro DB/ch03.pdf`.
The builder's manifest, previews, rendered PNGs and machine-readable QA results
remain in ignored `maintenance/course_repository/output/`.

### Figure-by-Figure Check

Names below are the suffixes of `opening_ch03_`. Checks compare the figure,
the stated example and surrounding prose; they are not a new full-textbook audit.

| Section / figure | Result in this version |
|---|---|
| 1 / requirements | Retained. Requirements, types and connection decisions agree; identification is explicitly left for key analysis. |
| 2 / entities | Corrected. All declared properties appear. Three students have 2, 1 and 0 recorded phone values; data match Section 3. Adding S104 is hypothetical, not a fourth displayed row. |
| 3 / attributes | Retained. Composite Name, multivalued Phone, derived EnrollmentCount and underlined StudentId agree with the profile. |
| 4 / keys | Retained. Only composite Location is underlined; neither component is independently unique. |
| 5 / domains | Clarified. Observed values 2 and 3 now appear in the figure; 5, 2.5 and 7 have the stated outcomes. |
| 6 / relationships | Completed. Grade is retained from the input; three enrollment instances give student counts 2, 1 and 0. The input rows and grouped counts are not one-to-one rows. |
| 7 / cardinality | Retained. Maximum ratios match all three variants; keys and minimum constraints are explicitly deferred. |
| 8 / participation | Retained. SECTION has required TEACHES participation; the ratio also limits it to one instructor. |
| 9 / minmax | Retained. Counts are beside the entity being counted; the single lines use the explicitly stated alternative notation. |
| 10 / roles | Corrected. Binary means two roles, not necessarily distinct students. Self-mentoring remains a separate business-rule question. |
| 11 / grade | Retained. Grade attaches to ENROLLS_IN; values 80/90 and 80/70 support both counterexamples. |
| 12 / weak | Retained. SECTION uses its owner and SectionNo within Fall 2026; symbols and total participation agree. |
| 12.1 / order_items | Completed. Product and Quantity are non-key attributes of ORDER_ITEM. OrderId belongs to ORDER; LineNo is the partial key. |
| 12.2 / strong_card | Retained. CardId is an independent key; required ownership does not make CARD weak. The multiple-card variant is explicitly distinguished. |
| 12.3 / nested_weak | Clarified. Only identifying attributes are shown; Product, Quantity and note text are expressly omitted. Owner-chain identification is unchanged. |
| 12.4 / two_owners | Completed. StudentId and CompanyId are drawn as full keys; VisitNo remains partial within the fixed pair. |
| 13 / refinement | Corrected. Three stacked tables preserve Morgan, independent I1 identification and exactly the same two DB101 sections. CS102 is explicitly outside this comparison. |
| 14 / ternary | Retained. Three types connect to one APPROVES relationship; it is not a process sequence. |
| 14 / pairs | Clarified. Visible record numbers now support the pair references; they are row labels, not a new ER key. The missing triple remains absent. |
| 14.1 / ternary_one | Retained. A fixed student-course pair permits at most one instructor; this is not an instructor-wide count. |
| 14.2 / ternary_count | Retained. (0,2) counts all approvals per instructor; the alternative pair restriction is not implied. |
| 14.3 / ternary_checks | Corrected. One table keeps each addition, pair test, before/after participation count and combined decision together. Each starts from the original three approvals. |
| 15 / complete | Retained. The declared core attribute inventory and all relationship endpoints agree; crossing lines do not define new junctions. |
| 16.1 / university_section | Retained. Globally unique SecId makes SECTION regular; SecNo is not underlined, and CRoom has Bldg/RoomNo components. |
| 16.2 / university_organization | Retained. Five relationships use the specified min-max counts; the source HAS prose/figure discrepancy remains explicit. |
| 16.3 / university_teaching | Retained. Four relationships agree with the requirements, including five distinct students per section. Attribute attachment is a stated assembly step, not silently complete in these close-ups. |
| 16.4 / university_conflicts | Corrected. Each case keeps its actual shared values and rejection reason in the same row. Independent cases, the no-combined-section assumption and limits of time equality are stated. |

The conceptual basis remains Elmasri/Navathe, *Fundamentals of Database Systems*,
7th edition, Sections 3.3-3.7, 3.9.1-3.9.2 and 3.10 as located in the earlier
photographed-source audit. These corrections preserve those definitions and
the approved synthetic requirements. No additional textbook question, UML topic,
relational mapping exercise or SQL task was introduced.

### Verification

Environment: Python 3.12.9, SQLite 3.45.3, Pillow 12.1.1, nbformat 5.10.4,
PyMuPDF 1.27.2.2, resvg-py 0.5.0, markdown-it-py 4.0.0, BeautifulSoup 4.14.3,
Node 24.15.0, Chrome 153.0.8010.36, Poppler 26.07.0.

Commands from the course root:

```powershell
python -m unittest discover -s maintenance/course_repository -p test_ch03_er.py -v
python maintenance/course_repository/build_course_repository.py
python maintenance/course_repository/export_chapter_pdfs.py --chapters ch03
python -X utf8 maintenance/course_repository/verify_first_meeting.py
node maintenance/course_repository/render_first_meeting.cjs
python -m unittest discover -s maintenance/course_repository -p 'test_*.py'
python -X utf8 maintenance/course_repository/build_course_repository.py --verify
git diff --check
git status --short --branch
```

- All 59 repository tests passed, including 23 Ch3 tests. The first focused run
  had 22 tests; exact PDF pixel matching was subsequently made a maintained test.
- Seven new content checks were also run with the baseline figure definitions
  loaded from `git show HEAD:maintenance/course_repository/er_figures.py` in
  memory. All seven detected the old omissions or conflicting presentation.
  No baseline file was restored, overwritten or committed for this check.
- Maintained-source rebuilds equal the current notebooks. Three fresh kernels
  loaded the published chapters. Ch3 contains only Markdown cells, so this is
  notebook-loading verification, not a claim of new SQL execution.
- The nine-file manifest and PDF notebook-hash provenance passed. The output
  still contains only the previously approved teaching chapters and answer PDFs.
- Ten main previews at widths 1440 and 390 had no page/text overflow or broken
  images. All 38 published figures were checked for SVG bounds; Ch3 text overlap
  checks include table text. No tested geometry failures were reported.
- All 42 PDF pages were rendered with Poppler and inspected in overview sheets.
  Changed figures were inspected at full figure resolution; PDF pages 4, 18,
  24, 29 and 40 were additionally inspected at readable page resolution.
- PDF text-token coverage, all 27 image bounds and image counts passed.
  Decoded RGB pixels of all 27 PDF images exactly match the notebook attachments.
- Chapter 1/2 outputs and both answer PDFs remain unchanged in the Git diff.
  No source textbook, private record or unapproved chapter was added to Git.

Notebook SHA256: `ee6e998965be30bff797ebf7a719b0a3dca2a0619f8e5ae6ac1cb8ade0675f8a`.
PDF SHA256: `7c2a44b4b58910d2012e0f70cd091913cbacd8d160904db9d4e5f2d92cb95e0b`.
PDF: 42 A4 pages, 27 figures, 1,556,295 bytes. PDF timestamps can change across
re-exports; notebook equality and image-pixel preservation are separately checked.

### Limits and Next Action

This corrects the identified figure/data inconsistencies; it is not independent
instructor review or a fresh sentence-by-sentence audit of the whole chapter.
The same agent performed the edits and review. Independent data reconstructions,
counterexamples and baseline-failure checks improve coverage but do not replace
external review or establish student understanding.

Dense PNG tables shrink on a 390-pixel phone display and need zooming. The preview
check establishes absence of clipping and page overflow, not comfortable reading
of every figure at that size. Real classroom projection has not been tested.
Some PDF whitespace keeps complete figures/tables together. The older figure
title/caption repetition is retained; removing it is outside this correction.

Primary next action: the instructor reviews PDF pages 4, 18, 24, 29 and 40 for
classroom explanation. The expected outcome is confirmation that the repaired
columns, same-object comparisons and per-case conclusions can be explained
directly from the figures. Completion means accepting those displays or naming
a concrete remaining defect. Commit/push requires a new explicit instruction.

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
