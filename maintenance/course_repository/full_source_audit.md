# Full Source Audit Progress

Started: 2026-09-08. Baseline: `a9bc1a8` on `main`, tracking existing `origin/main`.
The worktree was clean at the start. No commit or push is authorized for this audit.

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
