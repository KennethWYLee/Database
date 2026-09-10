# Full Source Audit Progress

Started: 2026-09-08. Baseline: `a9bc1a8` on `main`, tracking existing `origin/main`.
The worktree was clean at the start. No commit or push is authorized for this audit.

## Chapter Order and Expanded Scope

Date: September 10, 2026. Baseline: 4c445a4c7b2d5691576fc61d1fc4af546992ea59,
main tracking existing origin/main; clean at the start.
The instructor explicitly authorized replanning the syllabus, correcting related
files, and committing/pushing. No remote or publication setting is changed.

### Current Decision and Changes

Today covers Ch1/Ch2 only, then Ch3-9 and Ch14-19 in textbook order.
Ch3 ER and all substantive Ch4 sections remain required; Ch9 includes 9.1-9.2.
Ch15, Ch18, and Ch19 now have required selected teaching rather than being excluded.
Ch16 has a scheduled storage/file-organization meeting. Ch20 is not scheduled.
This supersedes the earlier first-meeting Ch5 and Week 2 Ch5/Ch8 directions.

| Weeks | Current material |
|---|---|
| 1 | Ch1/Ch2 only |
| 2 | Ch3 ER |
| 3 | Ch4 Sections 4.1-4.4 |
| 4 | Ch4 Sections 4.5-4.7, then Ch5 |
| 5 | Ch6 |
| 6 | Exam 1: taught Ch1-6 |
| 7-8 | Ch7, then Ch8 selected algebra |
| 9 | Travel; review taught Ch1-8 only |
| 10 | Ch9 Sections 9.1-9.2 |
| 11 | Ch14/Ch15 selected normalization and guided decomposition |
| 12 | Exam 2: taught Ch7-9 and Ch14-15 |
| 13-14 | Ch16, then Ch17 selections |
| 15 | Ch18/Ch19 selected processing and optimization; integrated review |
| 16 | Exam 3/final: Ch16-19 selections and cumulative taught SQL/design |
| 17-18 | Holiday, then make-up examination; no new topics |

Exam dates remain October 15, November 26, and December 24; weights remain
30/30/30/10. Travel remains November 1-8, December 31 remains a holiday,
and January 7 is the make-up. Five group comparisons and three designated AI
activities retain their weeks, with topics changed to match what has been taught.

The new scope is broad. There are twelve teaching meetings including the introduction.
Weeks 4, 11, and 15 are compressed. The detailed plan limits new requirements:
a common EER case; supplied keys/minimal cover for a small 3NF synthesis example;
one two-table query for processing and plan comparison. BCNF contrast, short
closure, decomposition properties, storage and optimizer concepts are included,
but complete algorithms/proofs/implementations are not silently required.
Actual pacing is not validated; unfinished content must not be examined without
teaching and practice or silently moved to the travel/exam weeks.

### Source Checks

Prescribed source: the instructor's private Elmasri/Navathe seventh-edition PDF,
SHA-256 002eceecdb5e47b050e61b30d13a8f207fb44cea4f927b98d864308c026288a5.
The source and uploaded dependency diagram confirm the book identity and topic
relationships. The diagram supports prerequisites; it is not a requirement that
every course follow a single ordering.

The contents at PDF pages 18-21 and 23-26 were checked for exact titles and section
numbers. Relevant newly scheduled passages were read, not just the contents:
- Ch15 printed 505, 513, 519 / PDF 536, 544, 550: FD prerequisite, decomposition
  properties, and Algorithm 15.4; its minimal-cover/key prerequisites are supplied.
- Ch16 printed 560, 567, 572 / PDF 591, 598, 603: records, heap organization,
  hashing and equality-search context.
- Ch18 printed 657, 663, 668, 681 / PDF 688, 694, 699, 712: SQL/algebra/storage/index
  prerequisites, selection methods, joins, and materialization/pipelining.
- Ch19 printed 692, 701, 710 / PDF 723, 732, 741: query trees, alternative
  plans, and cost estimates rather than guaranteed globally optimal execution.

These are bounded scheduling checks, not a complete chapter-source audit.
They do not verify every exercise, original figure, or proposed future teaching
example. Existing Ch5/Ch8 checks retain their earlier stated scope; full chapter
audit completion remains zero.

The [official NTUB calendar](https://acad.ntub.edu.tw/var/file/4/1004/img/1347/780969106.pdf)
was reopened September 10. It confirms September 7 teaching start, December 31
holiday, January 4-8 final period, and November 2-6 university midterm period.
Listed other first-semester holidays do not land on scheduled Thursdays.
The instructor's exam/travel arrangements remain distinct from university-wide
exam periods; this audit does not claim administrative approval for that difference.

### Maintained Sources and Derived Outputs

- Syllabus and COURSE_PLAN: matching 18-week schedule, chapter titles, selected
  depth, revised examination scopes, dates, and unchanged grading policy.
- README: only Ch1/Ch2 in today's entry; Ch5/Ch8 available for Weeks 4/8.
- PROJECT: newest decision plus updated current scope, first-day guidance,
  assessment and activity sections; earlier decisions explicitly historical.
- Authoring prompt: current sequence, required selections, exclusions, and limits.
- Ch2/Ch5/Ch8 maintained guides: forward/backward reading references corrected;
  Ch5 first-meeting label removed. All executable code and figures preserved.
- repository_config.json: build revision identifier; legacy chapter mapping
  remains marked historical, not repurposed as the current syllabus.
- Maintenance READMEs, first_meeting_release, textbook_material_correspondence:
  current scope notices without pretending old audit records describe this version.
- test_repository_layout.py and test_second_meeting.py: schedule, title,
  scope, first-day navigation, and chapter-transition regression checks.
- Derived ch02.ipynb, ch05.ipynb, ch08.ipynb regenerated from maintained sources.
  Ch01 and twelve historical notebooks are unchanged.

### Verification

Commands used the installed Python 3.12 and bundled Node from the course root:

```powershell
python -X utf8 maintenance/course_repository/build_course_repository.py --verify
python -X utf8 -m unittest discover -s maintenance/course_repository -p 'test*.py'
python -X utf8 maintenance/course_repository/verify_first_meeting.py
node maintenance/course_repository/render_first_meeting.cjs
```

Build/content/manifest checks passed for 16 notebooks and 18 course files.
Thirty regression tests passed, including exact Thursday dates, exam weeks 6/12/16,
30/30/30/10 weights, full textbook titles, required chapters, selected scope, today's
Ch1/Ch2-only links, and notebook transitions.
Four fresh kernels reproduced saved outputs: Python 3.12.9, SQLite 3.45.3,
with 0/1/6/10 code cells for Ch1/Ch2/Ch5/Ch8. The verifier exited zero.
A libzmq connection-reset diagnostic occurred during kernel lifecycle handling;
no teaching cell or output assertion failed. No environment packages were modified.

All 33 embedded PNGs decoded and were nonblank; no separate assets are required.
Six pages at 1440/390 pixels passed image, text-boundary, and page-overflow checks;
33 SVGs passed geometry checks. The complete desktop schedule, desktop syllabus
opening, and mobile home were visually inspected. Wide tables scroll on mobile;
date cells can wrap without losing content.
All 78 relative links in changed Markdown resolved. Exact code cells, saved outputs,
and figure attachments in Ch2/Ch5/Ch8 match the baseline. Ch1 and twelve historical
notebooks are byte-identical; instruction mirrors remain identical.
The renderer now saves a complete syllabus-table screenshot for future checks.
Private PDFs, source-page images, caches, and assessments remain excluded.

### Limits and Next Action

This completes the schedule and its related directions, not all newly scheduled
chapter notebooks. Ch3/Ch4 still require prescribed-book authoring. Old notebooks
remain explicitly unassigned, and the private textbook is not published.
The older ER mapped-schema NULL-primary-key defect remains a blocker before its
reuse. Correct and test that maintained schema as part of preparing the now-next
Ch3 ER material. Expected outcome: source-grounded ch03.ipynb with diagrams and
practice, plus missing-key rejection tests for any reused mapping SQL; no new
mapping assignment before Ch9. This becomes the immediate teaching priority
because the instructor moved ER to Week 2.

No new exams/answer keys, student data, dependencies, or private sources are added.
The commit/push is authorized to existing origin/main; the final hash and remote
synchronization are reported in Git history and the task response.


## Relational Foundations Revision

Date: September 10, 2026. Baseline: `4fc5dca28aeac637b0576a54b0984d0d0ac7dd3a`.
Branch: main, tracking existing origin/main; clean at the start.
The instructor authorized fixing the reviewed notebooks and committing/pushing
the result. No course dates, assessment weights, EER scope, or required submissions
are changed.

### Deliverables and Teaching Boundary

- Ch1 and Ch2 retain their already reviewed introductory content; rebuilding leaves
  their notebook bytes unchanged. They are not expanded into whole-chapter courses.
- Ch5 retains its first-meeting stopping point and adds Sections 6-13 of the guide:
  schema notation, keys, constraints, database setup, changes, deletion policies,
  business rules, and an introductory explicit rollback example.
- Ch8 is a separate prescribed-book notebook, not the old book's Ch8. It teaches
  selection, projection, renaming, compatible set operations, product, condition/
  equijoin/natural join, and simple composition. Division, calculus, aggregate and
  recursive algebra, and optimizer implementation are excluded.
- Original images: Ch1 5, Ch2 6, Ch5 13, Ch8 9. The 17 additions contain synthetic
  inputs and results, not copied textbook figures. The notebooks contain PNG
  attachments and saved actual stdout, with no separate student image directory.
- First meeting still stops within Ch5. Week 2 resumes there and continues to Ch8.
  SQL is supplied for observing results; independent SQL writing starts in Ch6.
  The examples and variations are not all newly required submissions.

### Source Reading and Locators

The source is the instructor's private Elmasri/Navathe seventh-edition PDF:
`private_references/book_Fundamental of Database Systems.pdf`.
SHA-256: `002eceecdb5e47b050e61b30d13a8f207fb44cea4f927b98d864308c026288a5`.
It stays ignored and is not included in the commit.

Full extracted chapter text was read in bounded, untruncated batches before
authoring: Ch5 printed 149-175 / PDF 180-206, and Ch8 printed 239-288 / PDF 270-319.
This includes the chapter summaries, exercise statements, and bibliographies.
Assigned-topic claims were compared with the locations below. Original teaching
examples and SQLite execution are distinct from the book's example results.

Visual source checks: Ch5 printed 160 / PDF 191 (Figure 5.4 keys), printed 164 /
PDF 195 (Figure 5.7 references); Ch8 printed 242 / PDF 273 (Figure 8.1 and selection
notation), printed 248 / PDF 279 (Figure 8.4 set operations), printed 252 / PDF 283
(Figure 8.6 and join notation), printed 253 / PDF 284 (equijoin/natural join).
Other original figures and all exercise solutions were not individually verified.
Consequently the earlier full-chapter audit completion count remains zero:
complete chapter text reading plus assigned-scope verification is not the requested
whole-book, every-claim/every-figure/every-exercise audit.

| Guide location | Textbook section; printed pages (PDF pages) | Teaching and checkable example |
|---|---|---|
| Ch5 opening Sections 1-5 | 5.1.1-5.1.3; 151-157 (182-188) | Preserved tuple/domain/atomic-value/order/identifier examples |
| Ch5 Section 6 | 5.1.1-5.1.3; 151-157 (182-188) | Three attributes, two tuples, missing department; schema/value practice |
| Ch5 Section 7 | 5.2.2; 158-160 (189-191) | Given unique ID/email versus repeated names; nonminimal superkey; group comparison |
| Ch5 Section 8 | 5.2.2; 158-160 (189-191) | Student/course/term key; legal retake and duplicate-triple counterexample |
| Ch5 Section 9 | 5.2.3-5.2.4; 160-165 (191-196) | Four-table arrows; mandatory/optional references; same-relation mentor |
| Ch5 Section 10 | 5.2.1-5.2.4; 158-165 (189-196), plus SQLite docs below | Fresh schema, required candidate keys, whole-number credits, enabled foreign keys |
| Ch5 Section 11 | 5.3.1-5.3.3; 166-169 (197-200) | Twenty independent INSERT/UPDATE/DELETE attempts; blocked-state comparison |
| Ch5 Section 12 | 5.3.2; 167-168 (198-199), plus SQLite docs below | Four policies with identical parent/contact inputs; retained counts and values |
| Ch5 Section 13 | 5.2.5 and 5.3.4; 165, 169 (196, 200) | Unimplemented count/transition rules; explicit rollback after failed registration |
| Ch8 Section 1 | Chapter opening and 8.1; 239-241 (270-272) | Same synthetic students/registrations; relation-valued operations |
| Ch8 Section 2 | 8.1.1; 241-243 (272-274) | IM yields two tuples; MED yields an empty relation with unchanged degree |
| Ch8 Section 3 | 8.1.2; 243-245 (274-276) | Duplicate departments versus distinct projection and projection retaining a key |
| Ch8 Section 4 | 8.1.3; 245-246 (276-277) | Select before removing department; rename output without altering values |
| Ch8 Section 5 | 8.2.1; 246-249 (277-280) | Two student-ID club relations; four set results and compatibility counterexample |
| Ch8 Section 6 | 8.2.2; 249-251 (280-282) | Three students times two courses; six pairs are not registration facts |
| Ch8 Section 7 | 8.3.1-8.3.2; 251-255 (282-286) | Equijoin retains two matching ID roles; unequal-credit theta join |
| Ch8 Section 8 | 8.3.2; 253-255 (284-286) | Shared department name wrongly removes an offering; explicit-ID/renamed comparison |
| Ch8 Section 9 | 8.1-8.3 and simple composition in 8.5; 241-255, 265-268 (272-286, 296-299) | IM/DB1/F26 intermediate relations and projection; unregistered IDs by difference |

Each numbered topic includes a named prediction, diagram or input table, worked
interpretation, specific limitation/counterexample, and practice/checking directions.
The summaries specify evidence to retain and the link to following chapters.
Paper examples do not claim database execution. The synthetic business-rule diagram
uses explicitly hypothetical additional registrations, not the initial SQL state.

SQLite-specific checks use official [CREATE TABLE documentation](https://www.sqlite.org/lang_createtable.html)
and [foreign-key documentation](https://www.sqlite.org/foreignkeys.html): primary-key
NULL exceptions, UNIQUE with NULL, per-connection enforcement, and referential actions.
These are implementation supplements, not attributed to the book's executable code.
No verified official companion code or slide package for this edition was used.

A source discrepancy was noticed outside the assigned algebra scope: Ch8 Section
8.5 Query 5, printed 267 / PDF 298, says two or more dependents but displays a
greater-than-two count test. Exactly two does not satisfy that test. This aggregation
example was not copied or assigned. Reading a source does not certify all its claims.

### Files and Verification

Maintained edits: Ch5 guide; new Ch8 guide; opening_figures.py; repository_config.json;
build_course_repository.py; verify_first_meeting.py; render_first_meeting.cjs;
new test_second_meeting.py; explicit allow-list entries; README; syllabus material
links; PROJECT; COURSE_PLAN; authoring prompt; maintenance READMEs; superseding
notices in first_meeting_release and textbook_material_correspondence; this record.
Derived edits: Intro DB/ch05.ipynb and new Intro DB/ch08.ipynb.
Ch1/Ch2 and all twelve historical notebooks remain content-identical to the baseline.

Environment: Windows; Python 3.12.9; SQLite 3.45.3; nbformat/nbclient for fresh kernels,
resvg for generated PNGs, Playwright and local Chrome for screenshots.
From the course root, these commands were executed:

```powershell
python -X utf8 maintenance/course_repository/build_course_repository.py --verify
python -X utf8 -m unittest discover -s maintenance/course_repository -p 'test*.py'
python -X utf8 maintenance/course_repository/verify_first_meeting.py
node maintenance/course_repository/render_first_meeting.cjs
```

Use the installed Python 3.12 executable and bundled Node when those are not on PATH.
Results on this revision:
- Build/content/manifest checks passed: 16 notebooks, 18 course files. Every builder
  code cell ran and authored stdout matched. A rebuild reproduced current notebooks.
- 29 tests passed, including nine new tests. They test exact authored DDL, all three
  composite-key NULL positions, eight credits boundary inputs, twenty changes,
  SET NULL/SET DEFAULT failure limits, and statement failure versus full rollback.
- Ten algebra query results were independently compared with Python sets/products;
  additional tests cover duplicate SQL results, empty results/products, and the
  natural-join shared-name trap. These share the authored input data, not its query logic.
- Four fresh notebook kernels passed: Ch1 0 code cells, Ch2 1, Ch5 6, Ch8 10.
  They matched saved outputs and created no persistent files in their fresh directories.
- A kernel-shutdown callback emitted a ZMQ 'not a socket' diagnostic after
  execution. The verifier exited zero with all output assertions passed. This is
  recorded as an environment warning, not a skipped or failed teaching cell.
- 33 PNG attachments decoded and were nonblank; 33 SVGs passed outer-boundary and
  network-node text geometry checks. All 17 added diagrams were visually inspected.
- Six preview pages at 1440/390 pixels passed image and page-overflow checks.
  Ch8 mathematical notation was visually checked at both widths. Wide SQL blocks
  and tables scroll on narrow screens; dense images may require zoom.
- Student-visible checks found no CJK prose, timing allocations, Type B label,
  internal source paths, forbidden content patterns, or unexecuted code cells.
  Relative course links passed. Public examples use synthetic records; no textbook
  pages, source screenshots, exams, answer keys, credentials, or private data are added.

The local output/first_meeting directory holds ignored verification JSON, previews,
and screenshots; source-page screenshots remain under ignored output/second_meeting.
No old SQLite ZIP was rebuilt: the new notebooks are self-contained and do not
depend on that historical package. No historical schema defect is claimed fixed.

### Remaining Work

The reviewed assigned Ch1/Ch2/Ch5/Ch8 material has no known blocking issue under
these checks. This does not establish classroom workload or complete source-audit
status. Week 2 is dense: use the displayed tables and supplied examples without
requiring students to author the helper code or submit every variation.

Primary next action remains correcting the reproduced NULL-primary-key defect in
the old ER mapping source before its reassignment. Expected result: corrected
maintained DDL, explicit missing-key rejection tests, and regenerated affected
artifacts. Completion requires rejected missing identifiers and valid mapping
examples still passing; it does not by itself finish the new Ch3/Ch4/Ch9 coverage.
Later prescribed-book notebooks, full source audits, and actual examination items
remain separate unfinished work.

Commit/push of this revision is authorized to existing origin/main. The final commit
and remote synchronization result are recorded in Git history and the task response.

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

## EER Schedule Revision Record

Date: September 10, 2026.
Baseline: `50973a4370b9db9f411e7563b29a1a1c40856e21`, branch `main`,
tracking existing `origin/main`. Worktree was clean before this revision.
The instructor requested full EER coverage, a revised schedule, and chapter numbers
with textbook titles. The instructor subsequently authorized commit and push of this revision to the
existing origin/main, after checking the related files against the displayed schedule.

### Changes and Boundaries

- Required Ch4 scope: Sections 4.1-4.7. Required Ch9 scope: Sections 9.1-9.2.
  All substantive Ch4 sections are scheduled; this does not assign every exercise.
  UML, abstraction, knowledge representation, and ontology remain introductory.
- Weeks 7-8 cover ER and ER mapping; Weeks 10-11 cover EER and its mapping.
  Week 10 includes all four specialization mappings and shared subclasses.
  Week 11 includes categories, their mappings, and the remaining Ch4 topics.
- Normalization through 3NF moves to Week 13 using supplied candidate keys.
  BCNF and Ch15 become optional to make room within the existing teaching weeks.
  There is no required closure or formal lossless-decomposition test.
- Exam 2 now assesses taught ER/EER and mapping; normalization moves to Exam 3.
  All exam dates and the 30/30/30/10 weights are unchanged.
- The normalization comparison moves from Week 11 to Week 13; five comparisons
  remain in Weeks 2, 4, 10, 13, 14. AI activities remain Weeks 4, 10, 14.
- November 1-8 travel, Week 17 holiday, Week 16 final, and Week 18 make-up remain.
  Make-up eligibility and grading are still for the instructor to announce.
- Student-facing teaching-week chapter labels use the prescribed book's full titles;
  only their dash typography is normalized to ASCII. Exam and travel-review rows also
  identify Ch numbers. Weekly topic summaries remain short. The root README now uses
  the full Ch2 and Ch5 titles without changing first-meeting reading limits.

### Source Checks

Source: Elmasri and Navathe, *Fundamentals of Database Systems*, seventh edition,
the instructor's private PDF. Its existing SHA-256 is
`002eceecdb5e47b050e61b30d13a8f207fb44cea4f927b98d864308c026288a5`.
The PDF remains ignored and is not distributed.

- Contents, PDF pages 18-30: chapter titles and section structure.
- Ch4 Section 4.4, printed page 120 / PDF page 151: category versus shared subclass.
- Ch4 Section 4.7 opening and Figure 4.10 page text, printed page 128 / PDF page 159:
  introductory discussion and UML comparison context. This was text extraction,
  not a visual verification of the textbook figure.
- Ch9 Section 9.2, printed pages 298-303 / PDF pages 329-334: specialization options
  8A-8D and conditions, shared subclasses, categories and source-key differences.

These are bounded scheduling checks, not a full Ch4 or Ch9 source audit.
Complete prescribed-book chapter audits remain zero. A larger attempted extraction
was truncated and was not counted as reading; the bounded pages above were reread.
The source establishes topic names and dependencies, not that this classroom pace
has been validated.

### Maintained Files

- `Intro DB/syllabus.md`: full chapter titles, EER schedule, exam scope, concise prose.
- `README.md`: complete chapter titles in the existing opening links.
- `maintenance/COURSE_PLAN.md`: required sections, sequence, examples, scope limits.
- `PROJECT.md`: current instructor decision and current assessment/activity facts;
  older dated decisions retained as history.
- `maintenance/database_chapter_teaching_material_prompt.md`: new authoring scope.
- `maintenance/course_repository/full_source_audit.md` and
  `textbook_material_correspondence.md`: superseding notices, not rewritten history.
- `maintenance/course_repository/test_repository_layout.py`: regression checks for
  the new titles, EER sequence, dates, scopes, weights, and concise summaries.
- This revision record.

No notebook, SQL source, assessment item, package source, or historical configuration
was changed. The syllabus is maintained directly; the HTML preview and manifest are
local ignored outputs.

### Verification

Eight targeted `RepositoryLayoutTests` passed using Python 3.12.9:
textbook/travel, scope/language, weekly agreement, weights, navigation, final/make-up
dates, full EER detailed coverage, and titles/EER sequence.

Command, from the course repository:

```powershell
python -X utf8 maintenance/course_repository/test_repository_layout.py RepositoryLayoutTests.test_textbook_details_and_updated_travel RepositoryLayoutTests.test_current_syllabus_scope_and_language RepositoryLayoutTests.test_syllabus_weekly_chapter_labels_match_plan RepositoryLayoutTests.test_current_assessment_weights RepositoryLayoutTests.test_current_navigation_links RepositoryLayoutTests.test_final_and_makeup_dates_agree RepositoryLayoutTests.test_detailed_coverage_includes_full_eer RepositoryLayoutTests.test_syllabus_chapter_titles_and_eer_sequence
```

The existing builder's `verify_content(config)` passed (15 notebooks; structural
checks only). `verify_manifest(write_manifest(config))` passed. The syllabus preview
was regenerated with `verify_first_meeting.preview` and `MARKDOWN.render`.
Headless Chrome through Playwright checked 1440x1000 and 390x1000 viewports:
document width matched viewport width, all 18 schedule rows were present, and no
missing images were reported. Full-page screenshots were visually inspected.
On mobile, both tables scroll horizontally (358-pixel wrapper, 650-pixel table);
scrolling 292 pixels exposes the last column. The EER topic rows were also visually
inspected after scrolling. This is a local Markdown preview, not a newly published
GitHub rendering.

`git diff --check` passed. Executable lessons were not rerun because no lesson code
or notebook changed. The subsequent publication request authorizes staging these
reviewed files, committing, and pushing to the existing origin/main. Final commit
identity and remote synchronization are checked after push; the Git history records
the completed publication rather than this pre-commit record claiming it in advance.

### Remaining Work

Week 8 mapping and Week 13 normalization are compressed. Use small reused examples;
do not add formal theory back into those meetings. Classroom workload is not yet
validated. New EER coverage still needs teaching-point correspondence, complete
chapter source checking, and instructional examples; scheduling it is not completing it.

The existing missing-key defect in the old ER schema remains unresolved, and that
schema remains unassigned. The primary next action is still to repair that schema's
NULL-key handling and regression tests before reusing it for ER/EER instruction.
Completion requires explicit non-null identifiers, passing missing-key tests, and
regenerated, verified affected artifacts. This correctness issue precedes adding new
EER examples; the schedule revision does not remove it.

## First-Meeting Release Update

September 9 schedule update: the instructor moved Written Exam 3 to Week 16
(December 24) and reserved Week 18 (January 7) for a make-up examination. Review
is integrated into Weeks 13-15; the core chapter selections and 30/30/30/10 weights
remain unchanged. Travel is now November 1-8. The earlier schedule statements below
and the September 8 release report are historical. The current syllabus and course
plan govern. This schedule update does not advance textbook source-audit completion.

The September 9 update covers the maintained syllabus, course plan, PROJECT,
chapter-authoring prompt, this progress notice, and layout regression tests. It also
includes the previously uncommitted textbook-information and November 1-8 edits.
The instructor explicitly authorized commit and push to the existing `origin/main`.
The historical `weeks` configuration and old notebooks retain their historical
status; the current plan, not that old mapping, controls the revised schedule.

Verification: six targeted `RepositoryLayoutTests` passed: textbook/travel details,
syllabus language/scope, weekly chapter/date agreement, assessment weights, navigation,
and final/make-up dates. `verify_content` and the refreshed local manifest passed.
The updated syllabus was rendered and checked with Playwright at 1440 and 390 pixels
with no page overflow; the Weeks 12-18 desktop table was visually inspected. No
notebook or SQL source changed, so executable lessons were not rerun for this
schedule-only revision. Make-up eligibility, scope, and grading arrangements remain
for the instructor to announce. Git history records publication; no private source,
assessment, or local rendering output is included.

The instructor subsequently authorized completing and publishing the September 10
first-meeting batch. The earlier no-push statements describe earlier turns, not this
release authorization. See [the release record](first_meeting_release.md) for the
new Ch1/Ch2/Ch5 opening selections and checks. Previous notebooks now live under
`Intro DB/under_revision/` with a not-assigned notice. The existing missing-key defect
is not in the new opening examples and remains open for the later ER revision.
Scoped passage checks do not complete an entire textbook chapter audit.

## Current Material Correspondence

The instructor subsequently requested the next step. The
[required-topic correspondence](textbook_material_correspondence.md) is now complete
as a mapping and gap review of the revised syllabus against the existing maintained
guides, examples, and figures. It records source locators and bounded passage reading;
it is not a complete chapter audit. The worktree already contained the earlier audit
and syllabus changes when this mapping step began.

The missing treatments include introductory architecture, stepwise 1NF/2NF-to-3NF,
complete 1:1 and ternary mapping examples, and storage prerequisites for indexing.
Existing ADD COLUMN code was located in the opening guide, so schema change is a
reuse-and-explain item rather than wholly missing. A fresh in-memory run also
reproduced a NULL primary key accepted by the ER mapped schema. That correctness
failure is the new reason to prioritize schema repair and negative tests before
reusing it. No SQL or generated material was changed in this mapping step.

Complete chapter audits for the prescribed book remain **zero**. The former next
action of establishing correspondence is now done at topic level; full source
audits and notebook revision remain outstanding. Nothing was staged, committed,
or pushed. See the linked record for the exact evidence and remaining boundaries.

## Current Syllabus Revision

On September 8, after discussing the corrected textbook, the instructor requested
the syllabus revision and specified **30% for each examination**. The remaining
Class Performance component is 10%. Earlier statements below about unchanged
assessment weights describe the preceding textbook-identity correction only.

The syllabus now assigns Chapters 3, 5-9, and 14 within named topic limits;
Chapters 1-2 are introductory, Chapters 15, 17, and 20 selected, and Chapter 16
prerequisite background only. Chapter 9 is limited to Section 9.1, with Chapters 3
and 5 as prerequisites; Chapter 4 and Section 9.2 are excluded. Chapters 18-19 and
21-22 are no longer independent required units. ER teaching starts in Week 7.
Week 11 covers normalization through 3NF with supplied candidate keys; closure,
BCNF, and binary lossless-decomposition checks follow in Week 13 and are on Exam 3,
not Exam 2. Week 16 is review only. Exam dates, the travel week, holiday, five
comparison activities, and AI policy remain unchanged.

Files updated for this syllabus revision:

- `Intro DB/syllabus.md`: textbook references, scope, objectives, schedule and
  30/30/30/10 assessment; removed misleading old notebook chapter links and disclosed
  that notebook revision is pending.
- `maintenance/COURSE_PLAN.md`: synchronized sequence, prerequisites and assessment;
  retired the invalid old item-level chapter percentages without inventing replacements;
  corrected the stale private-repository status.
- `PROJECT.md` and root `README.md`: recorded the current decisions and pending
  notebook revision; preserved explicitly superseded historical records.
- `maintenance/database_chapter_teaching_material_prompt.md`: replaced incorrect
  chapter scope with the approved syllabus and exclusions.
- `maintenance/course_repository/repository_config.json`: marked the existing
  material sources and weekly mapping as historical and named the current plan;
  no source, old weekly material list, or notebook ID was reassigned.
- `maintenance/course_repository/test_repository_layout.py`: compares current
  syllabus chapters and dates to the plan, not to the old notebook IDs; adds weight,
  scope and English-language checks.
- `maintenance/course_repository/README.md` and this record: describe what changed
  and distinguish syllabus completion from pending material revision.

Source work was limited to course planning: the prescribed PDF's contents and preface,
ER mapping passages at printed pp.290-297 (PDF pp.321-328), closure and decomposition
passages at pp.505-508 and 513-515 (PDF pp.536-539 and 544-546), and selected index
and transaction passages. These checks support scope and prerequisites, not a complete
chapter audit. The [official university calendar](https://acad.ntub.edu.tw/var/file/4/1004/img/1347/780969106.pdf)
was fetched again, confirming the December 31 holiday and January 4-8 final-exam
period. Travel is an instructor decision, not a calendar fact.
[SQLite's query-plan documentation](https://www.sqlite.org/eqp.html) supports the
practical supplement; it is not attributed to the textbook.

Verification on the revised files:

- Python 3.12.9, SQLite 3.45.3, markdown-it-py 4.0.0, nbformat 5.10.4.
- `python -X utf8 maintenance/course_repository/test_repository_layout.py`: all
  16 tests passed, including the existing example/layout checks and the new schedule,
  scope and 100% assessment checks.
- `python -X utf8 maintenance/course_repository/output/review_syllabus.py`: parsed
  the syllabus, plan and home page, checked relative links and UTF-8, and generated
  local HTML previews. The helper and previews are ignored QA files.
- `node maintenance/course_repository/output/render_syllabus.cjs`: headless Chrome
  checks passed at 1440px and 390px for all three documents. Desktop coverage and
  assessment screenshots and the mobile schedule were visually inspected. Tables
  scroll horizontally on mobile; no whole-page horizontal overflow was found.
  This is local preview evidence, not a claim that the unpushed GitHub page changed.
- No notebook, SQL source, figure, or SQLite package was rewritten for this revision.
  No new complete-notebook fresh-kernel or package-rebuild claim is made. Earlier
  records retain their own version and textbook-alignment limits.
- No textbook or private material was added to Git. Existing uncommitted audit work
  was preserved. Nothing was staged, committed or pushed.

At the end of the syllabus-revision step, complete-chapter audits for the prescribed
book remained **zero**, and section-to-material correspondence was the next action.
The later mapping result above supersedes that next-action status. Notebook revision,
full source audits and examination-item preparation remain outstanding.

## Textbook Confirmed by the Instructor

On 2026-09-08 the instructor explicitly confirmed Ramez Elmasri and Shamkant B.
Navathe, *Fundamentals of Database Systems*, seventh edition, and the file
`book_Fundamental of Database Systems.pdf`. This corrects the earlier source
identification; it is not an instructor decision to switch textbooks now.

The local private copy is `private_references/book_Fundamental of Database Systems.pdf`.
The original in the instructor's book library is preserved. Both copies have SHA-256
`002eceecdb5e47b050e61b30d13a8f207fb44cea4f927b98d864308c026288a5`.
The PDF has 1,273 pages; its cover, title page and copyright page were inspected.
Its printed ISBN is 978-0-13-397077-7. File identity does not establish complete reading.

**Current result: zero complete chapter source audits for the prescribed textbook.**
The Ch2/Ch3 records below concern *Database System Concepts*, not this book. They
remain historical evidence of that reading and the recorded program behavior, but
cannot be counted as textbook alignment for this course. Existing notebook numbers,
weekly chapter labels, assessment chapter labels and their citations require remapping;
same-numbered chapters across these books are not interchangeable.

Maintained corrections in this turn: PROJECT, root README, syllabus, course plan,
chapter-authoring prompt, this progress index and the two previous chapter records.
The textbook fact was corrected and unmatched chapter numbers explicitly flagged.
No chapter content, notebook filename, date, assessment weight or scope was silently
reassigned. The previous book, prior audit changes and both source PDFs are preserved.
No commit or push is authorized.

## Textbook-Correction Checks

These checks apply to the documentation correction, not a complete textbook audit.

- All eight corrected Markdown files passed UTF-8 decoding, replacement-character
  scanning and parsed relative-link target checks. Root README and the syllabus retain
  English-only prose.
- The private PDF copy matched the original SHA-256. `git check-ignore -v` confirmed
  that it is ignored; `git ls-files` confirmed that it is not tracked.
- `python -X utf8 maintenance/course_repository/test_repository_layout.py` passed all
  14 tests with Python 3.12. No notebook content or executable source was changed by
  this textbook correction, so the earlier execution records retain their original
  limited scope; no new fresh-kernel execution is claimed for this correction.
- `git diff --check` passed. Git's LF-to-CRLF notices are normalization warnings,
  not whitespace failures.
- The [Pearson educator page](https://www.pearson.com/en-us/subject-catalog/p/Elmasri-Fundamentals-of-Database-Systems-7th-Edition/P200000003546?view=educator)
  identifies the correct authors and seventh edition and lists PowerPoint supplements.
  The slide files themselves have not been obtained or inspected. A subsequent page
  fetch timed out; the resource-availability statement comes from the earlier successful
  page read, not a successful download.
- Existing uncommitted audit work is preserved. No files were staged, committed or
  pushed during this correction.

## Scope and Completion Rule

First establish the correspondence between existing teaching topics and the confirmed
Elmasri/Navathe source. Then audit each complete source chapter in the agreed sequence.
The earlier sequence Ch2-Ch7/Ch14-Ch19 belongs to the other book and is not an approved
reading sequence in this one.
Reading the full source does not add the source's omitted sections to the syllabus.
No full chapter of the confirmed book has yet been read in this audit.

For each chapter, record the source file hash, printed and PDF positions, every section,
figures/tables/equations/notes, local guide/examples/diagrams, adaptations, conflicts,
corrections and executed evidence. A chapter is complete only when its source reading,
material comparison and applicable final-version checks are complete. Merely extracting
text, listing headings or rerunning tests does not count as reading or source validation.

## Historical Progress on Database System Concepts

The entire table below concerns the earlier, incorrect primary source only.

| Chapter | Full chapter reading | Material comparison | Final-version verification | Record |
| --- | --- | --- | --- | --- |
| 2 | Completed: printed pp.37-64, PDF pp.62-89, all 29 official slides | Completed; objective corrections made | Passed; see exact versions and limits | [Ch2 record](../chapters/ch02_relational_model/instructor/full_source_audit.md) |
| 3 | Completed: printed pp.65-124, PDF pp.90-149, all 62 official slides | Completed; objective corrections made | Passed; see exact versions and limits | [Ch3 record](../chapters/ch03_introduction_to_sql/instructor/full_source_audit.md) |
| 4 | Not started in this new audit | Not completed | Not completed | Pending |
| 5 | Not started in this new audit | Not completed | Not completed | Pending |
| 6 | Not started in this new audit | Not completed | Not completed | Pending |
| 7 | Not started in this new audit | Not completed | Not completed | Pending |
| 14 | Not started in this new audit | Not completed | Not completed | Pending |
| 15 | Not started in this new audit | Not completed | Not completed | Pending |
| 16 | Not started in this new audit | Not completed | Not completed | Pending |
| 17 | Not started in this new audit | Not completed | Not completed | Pending |
| 18 | Not started in this new audit | Not completed | Not completed | Pending |
| 19 | Not started in this new audit | Not completed | Not completed | Pending |

Ch1 has only the opening-context passages listed in the Ch2 record read this time.
Ch1, Ch8-13 and Ch20 onward are not complete. Existing historical chapter reports and
the September 8 visual/example expansion remain useful evidence of their own narrower
scopes, not proof that this new full-source audit has already passed.

## Historical Working-Tree Checkpoint

This checkpoint predates the textbook confirmation and the documentation corrections
above. Its test results do not establish alignment with Elmasri/Navathe.

Ch2 and Ch3 together cover 88 complete textbook pages and 91 official slides in this
new audit. Both chapter records include section/page/figure locators, original course
examples, adaptations, corrected issues, execution evidence and final file hashes.
This is two of the twelve selected chapters, not a completed whole-course or whole-book
audit. Ch4/Ch5 notebook changes only embed Ch2's corrected shared credit constraint;
those generated changes do not count as source reviews of Ch4/Ch5.

Final working-tree checks on 2026-09-08:

- Fourteen fresh-kernel notebook runs, all 14 repository tests, all figure data and
  desktop/mobile image/overflow checks passed. Full details and limits are in the
  chapter records; execution alone does not establish the remaining chapters' sources.
- The SQLite package's 21-file allow-list/manifest and all ten packaged activities
  passed in fresh temporary extractions. Two consecutive final builds produced the
  identical ZIP hash `481e50e8721c2aa253f801b56ff5fa0b30750069c76f266297bd3cc860c5cd1e`.
- All relative links in the three new audit records resolve. Workspace and course
  AGENTS/CLAUDE pairs remain byte-identical; neither instruction pair was edited.
- `git check-ignore -v` and `git ls-files` confirmed the textbook, downloaded author
  errata and rendered source sheets remain ignored and untracked. No source PDF or
  source-page image was added to the public-material allow-list.
- `git diff --check` passed; Git reports its configured LF-to-CRLF normalization
  warnings, not whitespace errors. Maintained Ch2/Ch3 sources, verifier extensions,
  generated Ch2-Ch5 notebooks, package and progress documents account for 16 modified
  tracked files; the two chapter records and this index are three new untracked files.
- Branch remains `main` tracking the existing `origin/main`; nothing was staged,
  committed or pushed. Local audit changes are not yet on GitHub.

## Primary Next Action

Build a source-verified correspondence between existing teaching topics and the
confirmed Elmasri/Navathe chapters and sections, with explicit gaps and scope decisions.
The instructor's corrected textbook identity is the new evidence that replaces the
previous recommendation to continue the other book's Ch4. Completion requires a
verified source location or an explicit gap for each existing major teaching topic,
without silently converting book-specific chapter numbers or changing assessment policy.
Complete chapter audits follow the corrected, confirmed coverage.
