# Course Repository Build

## Current Publication: Chapters 1-3

The public `Intro DB/` contains `syllabus.md`, `ch01.ipynb`, `ch02.ipynb`,
`ch03.ipynb`, their three matching PDFs, and the separately authorized
`ch03_answer.pdf`. Other notebooks, their chapter sources, and the SQLite package
are ignored and kept locally. The semester scope has not changed.
`published_chapters` in `repository_config.json` controls default builds.
The manifest and default verification cover only that published selection.
Known unreleased local files are preserved, not deleted or silently published.

```powershell
python maintenance/course_repository/build_course_repository.py --verify
python -m unittest discover -s maintenance/course_repository -p 'test_*.py'
python maintenance/course_repository/verify_first_meeting.py
node maintenance/course_repository/render_first_meeting.cjs
```

A fresh checkout can run these commands with the documented dependencies.
Tests that require absent unreleased source files explicitly skip those cases;
published chapter checks do not skip missing published sources.
For local preparation only, `build_course_repository.py --include-unreleased --verify`
uses all existing local sources. This flag does not change Git ignore rules.

## Local Answer Audit, September 12

After baseline `23b5c8c`, the instructor approved checking every photographed
Ch3 question and subpart. The revised local answer PDF has 56 A4 pages,
31 original figures, and 2,060,908 bytes. Its SHA256 is
`79ecb018e4646c4ebe0ed83eae85376b4a69b22c0c9254e56c8e0015d0736c87`;
input notebook SHA256 is
`a6765354e870481bc7088a5e7ee9a52a3d8baf644378bc8b74ed086a0d9e37b3`.

The wrong-target answer to 3.5 and other omissions were corrected. All written
requirements for 3.1-3.30 were checked; 3.31-3.35 provide conceptual answers but
their modeling-application tasks remain uncompleted. Eighteen local answer tests,
48 repository tests, full text/image export checks, and desktop/mobile rendering
passed. See [the question-by-question record](ch03_er_release.md#2026-09-12-answer-requirements-audit).
The audit itself updated local files without committing or pushing. The instructor
subsequently explicitly authorized commit and push of this audited version to
`origin/main`. This commit records that authorization; the PDF hash above is
unchanged. Private sources remain ignored; public chapter selection and course
policy are unchanged.

The remainder is the historical full local-build description. Its counts of
17 notebooks/19 files and earlier tracking statements do not describe the
current GitHub release. Historical audit records remain as provenance, not
links promising that unreleased files exist in a fresh checkout.

### Initial Chapter 3 Answer PDF Publication, September 12

After baseline `7f3cc1a`, the instructor explicitly authorized publishing
`Intro DB/ch03_answer.pdf`, with commit and push. This supersedes the earlier
local-only answer decision for this PDF only. The answer Markdown, notebook,
HTML, builders, figures and photographed textbook remain ignored local files.
The existing three teaching notebooks and PDFs are unchanged.

The answer PDF contains all 35 answers (3.1-3.35), 26 original figures and tables,
in English. These are original worked answers, not the publisher's solution
manual; full question statements and photographed pages are not reproduced.
Stated alternatives and the unexecuted ERwin/Rational Rose limitation remain.
Two production-note sentences were simplified in the maintained answer Markdown
before rebuilding. No technical answer, assessment or taught scope was changed.

Local reproduction, from the course root:

```powershell
python -X utf8 private_references/ch03_solutions/build.py
python -X utf8 private_references/ch03_solutions/verify.py
python -X utf8 private_references/ch03_solutions/export_pdf.py
python maintenance/course_repository/build_course_repository.py --verify
python -m unittest discover -s maintenance/course_repository -p 'test_*.py'
```

The local exporter reuses the published HTML/PDF helpers, but its maintained
input stays private. A public checkout can validate the approved PDF's hash,
source-notebook hash metadata, numbered answers and image count; it cannot
rebuild this answer without the local source. Update the two
`published_answer_pdfs` hashes only after reviewing a regenerated answer PDF.
Regular chapter PDF exports still use only the three public notebooks.

The final answer export is 48 A4 pages, 1,789,569 bytes. Its PDF SHA256 is
`7a099ed4ecc169bb7c7f3a31fa029787760e62cd8ae2ec7588e7446cf08066e9`;
its input notebook SHA256 is
`4876675ec8f86767444cefe713ee7aecb68edecaab076e8b89e95cab49686ee8`.
The twelve local answer tests passed. Export checks passed for all HTML text
tokens, 26 embedded figures, page/image bounds, loaded images and DOM overflow.
Headings were kept with their source line and opening content; figures were
kept whole. All 48 pages were rendered with Poppler for visual review.
All page overview sheets and the composite-key/UML pages at readable resolution
were inspected; no clipping or overlapping labels were found. The repository
verifier passed for 8 published files and 3 notebooks; all 48 repository tests
passed. An initial test treated a normal PDF line wrap as missing text; whitespace
normalization fixed that check without changing the answer text.
Some whitespace remains to keep complete figures or tables together.
PDF timestamps mean byte-identical re-export is not promised.

This is export/publication verification, not a new full textbook source audit
or evidence that the instructor has reviewed each answer. The earlier source
review and conceptual-answer limits remain in `ch03_er_release.md`.

### PDF Export, September 10

The instructor authorized Ch1-Ch3 PDF conversion, commit and push after baseline
`77cc16c`. The original notebooks and saved outputs are unchanged.
`export_chapter_pdfs.py` reads their cells and attachments; `print_chapter_pdfs.cjs`
prints self-contained HTML through Chrome. No textbook PDF or private answer is
used as export input. The three explicit PDF paths are allow-listed in Git.

```powershell
python maintenance/course_repository/build_course_repository.py
python maintenance/course_repository/export_chapter_pdfs.py
python maintenance/course_repository/build_course_repository.py --verify
python -m unittest discover -s maintenance/course_repository -p 'test_*.py'
```

Export dependencies: Python with PyMuPDF, BeautifulSoup4, markdown-it-py and
nbformat; Node/Playwright, Chrome and Poppler's `pdftoppm` on PATH. Chrome/Playwright
paths can be overridden using `CHROME_PATH` / `PLAYWRIGHT_PATH`. Arial and Consolas
are the print fonts. Python 3.12.9 and Chrome 153 were used in this check.
HTML, metadata checks and 56 rendered page previews stay under ignored `output/pdf/`.

| PDF | Pages | Original figures retained |
|---|---:|---:|
| ch01.pdf | 6 | 5 |
| ch02.pdf | 9 | 6 |
| ch03.pdf | 41 | 27 |

The PDF export checks all rendered HTML text tokens against PDF text, image
counts and bounds, nonempty pages, and absence of internal attachment/file URLs.
The first pass found a wrapped INSTRUCTOR identifier; changing table word-wrap
preserved it as a whole word and the comparison passed. Short tables, figures,
and closing summaries are kept together. All 56 pages were rendered with Poppler
and inspected in overview sheets; the large ER figure and code/output page were
also inspected at readable resolution. Some pages retain whitespace to keep a
complete figure or table together. This is a static reading version, not executable.

The PDF Subject stores its notebook's SHA256, checked by the normal repository
verifier to detect stale exports. The builder now verifies 7 published files and
the same 3 notebooks; test coverage also checks PDF provenance and image counts.
PDF timestamps/Chrome serialization can change across runs; byte-identical PDF
rebuilds are not claimed. Export and course checks passed before publication.

### Earlier Publication Check

Baseline: `84b8570` on main; origin/main was `c97312d` after fetching.
The instructor requested that GitHub show only current Ch1-Ch3 materials.
Removed 102 other notebook, chapter-source and SQLite-package files from the
Git index using `git rm --cached`; every local file's SHA256 matched before
and after removal. PDFs and private exercise answers remain ignored.
Shared builders, tests, plans and historical audit records remain tracked.
No course topic, date, weight or notebook content changed in this publication pass.

Checks performed with Python 3.12.9 / SQLite 3.45.3 and the existing renderer:

- Default builder `--verify`: 3 notebooks, 4 files, manifest/content/execution passed.
- Local unittest discovery: 46 tests passed, including a regression ensuring
  a default build does not replace an unreleased local notebook.
- Export of staged tracked files into a new isolated directory: builder passed;
  37 unittest cases completed with 4 explicit skips for absent unreleased sources
  (including the Ch5/Ch8 test class). Published-source checks were not skipped.
- Fresh-kernel check in both the local and tracked-only directories: 3 chapters,
  38 figures, expected outputs and regenerated bytes passed. The isolated check
  verified 34 relative links after converting one historical Ch5 hyperlink to
  a local-only path. Windows ZMQ shutdown diagnostics remain an environment
  limitation; successful completion is not described as a quiet diagnostic log.
- Desktop/mobile render: 10 previews, no page/text overflow or broken images;
  SVG geometry check passed. Visually inspected the updated mobile homepage.
- Git index checks require exactly the syllabus and Ch1-Ch3 in Intro DB, only
  their three maintained guides under chapters, and no SQLite package or private sources.

Main is the current release target. Existing `course-materials` and
`student-preview` branches and historical commits are not deleted or rewritten;
previously published files remain retrievable there. Ignoring a file is not
retroactive removal from Git history. Future chapter release requires explicit
approval and coordinated updates to `published_chapters` and `.gitignore`.

This directory builds the current Ch1/Ch2 introductory selections, Ch3, Ch5, and selected Ch8 directly
in `Intro DB/` and twelve previous notebooks in `Intro DB/under_revision/` on `main`.
Local and GitHub tracked paths are identical. It does not publish a separate preview
branch or create weekly notebooks.

**September 8 syllabus revision:** The [current syllabus](../../Intro%20DB/syllabus.md)
and [course plan](../COURSE_PLAN.md) now use Elmasri/Navathe's seventh edition, with
three exams at 30% each and Class Performance at 10%. The chapter IDs and weekly
material mapping in this builder still describe the other textbook's existing
notebooks. They are marked historical in the configuration and are not the current
teaching schedule. A successful build does not establish alignment with the revised
syllabus. The `current_chapters` configuration separately identifies five
prescribed-book notebooks. See the [first-meeting release](first_meeting_release.md)
and [Ch5/Ch8 revision](full_source_audit.md#relational-foundations-revision), plus
the [Ch3 ER release](ch03_er_release.md).
Do not rename remaining notebooks or replace source locators without content review.

The [prescribed-textbook correspondence](textbook_material_correspondence.md) now
maps the required topics to existing guides, examples, and figures. It records
missing instruction and a reproduced NULL-primary-key defect in the ER mapped schema;
it does not certify revised notebooks or complete chapter source audits.

## Maintained Files

The current syllabus follows Ch1/Ch2, Ch3-9, then Ch14-19; only Ch1/Ch2 are
assigned today. The five available revised notebooks do not imply the remaining
chapters are ready. Ch15/Ch18/Ch19 are selected teaching, and Ch20 is not scheduled.

- `repository_config.json`: existing chapter sources, historical weekly material mapping,
  and the path to the current course plan.
- `build_course_repository.py`: builds, executes, and verifies every notebook.
- `review_notebook.py`: validates raw JSON and executes Ch2 in three fresh kernels;
  `--all-chapters` additionally executes each remaining chapter in its own fresh kernel.
- `test_repository_layout.py`: checks layout, path safety, links, protected files, and
  agreement between the current syllabus and course plan, including assessment weights.
- `notebook_figures.py`: dispatches original SVG teaching diagrams and renders PNGs.
- `teaching_figures.py`: maintains topic-specific diagrams with font-measured layouts.
- `opening_figures.py`: 33 Ch1/Ch2/Ch5/Ch8 diagrams plus the Ch3 registry, 60 total.
- `er_figures.py`: 27 original Ch3 figures and their synthetic example data;
  ER shapes and undirected connections, not relational table diagrams.
- `test_ch03_er.py`: independent participation, identification, ternary-fact,
  notation, placement, and publication-boundary checks.
- `test_second_meeting.py`: exact-DDL boundary checks and independent set-result comparisons.
- `verify_first_meeting.py` and `render_first_meeting.cjs`: verify current notebook
  outputs, source correspondence, navigation, diagrams, and local rendering.
- `simple_examples.py`: maintains 51 original small examples with input tables,
  source locators, predictions, SQL or conceptual steps, figures, interpretation, and practice.
- `verify_teaching_figures.py`: checks selected diagram data against SQL, attachment
  bytes, and notebook format; exports an ignored review gallery and notebook HTML.
- `render_teaching_figures.cjs`: uses Playwright and Chrome to check SVG text geometry,
  notebook images, and desktop/mobile page overflow, and capture review screenshots.
- `visual_teaching_review.md`: records the visual teaching revision and its evidence.
- `all_chapters_teaching_review.md`: records the September 8 expansion and final checks.
- `full_source_audit.md`: tracks the subsequent complete chapter-source audit, with
  separate reading, material-comparison and final-verification status for every chapter.
- `textbook_material_correspondence.md`: required-topic mapping, located reusable
  material, missing examples, source-reading limits, and the next correctness fix.

The chapter guides, SQL, diagrams, data, and simulation programs remain the maintained
content sources. The builder combines them into one self-contained notebook per selected
chapter.

Ch2 opts into `executable_guide` in the configuration. Its maintained Markdown contains
Python fences beside the relevant explanations; the builder emits code cells at those
positions. Adjacent `output` fences are compared with actual stdout and are not copied
as duplicate Markdown output. The notebook preserves the executed output instead.
Week 1 ends before the full four-table setup, and Week 2 runs independently.
These are historical reading sections in `under_revision/ch02.ipynb`, not first-meeting completion deadlines or
chapter references for the prescribed textbook. The revised first meeting starts
with the syllabus and selections from Chapters 1-2 only. The current chapter order
is Ch3-9 followed by Ch14-19; Ch5 and Ch8 are scheduled for Weeks 4 and 8.

Ch2 also opts into `inline_sql`. Its guide uses `<!-- sql:setup -->`,
`<!-- sql:example 4 -->` (and the other numbered examples), and `<!-- sql:checks -->`
to position the shared setup, existing lab examples, and final checks. The builder
extracts the `-- Example ...:` blocks from maintained SQL, embeds each exactly once,
and rejects missing, duplicated, or unknown markers. It does not append a second lab.
The markers are removed before notebook generation; `output` fences verify their results.

Each chapter opts into `visual_teaching`. The builder splits the guide at H2 and H3
headings and inserts diagrams beside the matching topic. Repeated H3 headings use
`## Parent / ### Subheading` anchors. Missing or ambiguous anchors stop the build.
Ch2 contains 19 images; each other chapter contains five to ten, for 96 in total.
These explain existing content without adding assignments or changing course scope.

The small-example catalog adds 32 independently executable SQL examples and 19
conceptual worked examples beside their corresponding explanations. Every SQL example
starts with its displayed artificial inputs in a fresh in-memory database. Authored
expected results are checked against execution; the notebook retains actual stdout,
including trailing blank lines. Conceptual examples use diagrams and explicitly stated
rules rather than presenting a simulated result as a live DBMS observation.
Figure panels display SQL NULL as `NULL`, not Python's `None`.

The instructor selects practice variations. These are not 51 new required submissions.
Existing chapter labs and optional extension boundaries remain intact. Source locators
in the catalog belong to maintenance; they are not injected as production notes into
student notebooks. Notebook execution still needs only Python's standard library.

The builder assigns deterministic, unique cell IDs to every notebook and verifies
their format and uniqueness. Raw notebook schema validation must run before a notebook
reader can silently repair missing fields; the local Week 1 review script follows this
order before fresh-kernel execution and HTML rendering.

## Course Structure

```text
Intro DB/
  syllabus.md
  ch01.ipynb
  ch02.ipynb
  ch03.ipynb
  ch05.ipynb
  ch08.ipynb
  under_revision/
    README.md
    ch02.ipynb
    ...
    ch19.ipynb
```

`Intro DB/syllabus.md` is the maintained syllabus, including schedule, assessment,
notebook links, and opening instructions. The root `README.md` is maintained navigation.
Neither file is generated or overwritten. The under_revision README is also maintained.
The builder only replaces the seventeen named notebooks after all executions succeed;
unexpected files cause it to stop without deletion. Old notebooks have an explicit
not-assigned notice, and new notebooks have no dependency on their code or files.
The old `course_home.md` is retained in `maintenance/archive/`, not used as build input.

SQL and Python examples are embedded in the notebook that uses them. Existing PNG
diagrams and PNG renderings of Python-generated SVG figures are notebook attachments.
The vector source remains maintained in Python; PNG makes these figures visible in
GitHub's notebook preview. No separate image files are required by students. SQL
notebooks guide the reader through connection, table creation, data loading, schema
inspection, integrity checks, and chapter queries. The current build therefore needs no
`assets/` directory, separate lab runner, or external data file.

## Build and Verify

From the course repository root:

```powershell
python -m pip install resvg-py==0.5.0 Pillow==12.1.1
python -m pip install nbformat nbclient nbconvert ipykernel
python maintenance/course_repository/build_course_repository.py --verify
python maintenance/course_repository/verify_first_meeting.py
node maintenance/course_repository/render_first_meeting.cjs
python maintenance/chapters/ch02_relational_model/instructor/verify_week1.py
python maintenance/course_repository/test_repository_layout.py
python maintenance/course_repository/review_notebook.py --all-chapters
python maintenance/course_repository/verify_teaching_figures.py
node maintenance/course_repository/render_teaching_figures.cjs
```

The renderer and Pillow are build-only dependencies; notebook execution still uses
Python's standard library. The visual review script needs Playwright available to Node
(configure `NODE_PATH` when using the bundled runtime) and installed Google Chrome.
Rendering and font measurement use Arial and Arial Bold in the verified Windows
environment; install those fonts for reproduction. Consequently,
image hashes may differ across machines with different fonts. See the renderer's
[API reference](https://resvg-py.readthedocs.io/en/latest/api.html) for the SVG-to-PNG call.

The generated notebooks are written to:

```text
Intro DB/
```

The seventeen notebooks are explicitly allowed by `.gitignore` and should be committed with
their source changes when authorized. The manifest and local QA files remain under ignored
`maintenance/course_repository/output/`. The older Ch2-only `review_notebook.py` and
the 96-figure `verify_teaching_figures.py`/renderer still describe the earlier twelve
notebooks and are not the current first-meeting acceptance checks. Their source and
results are retained, not silently claimed as rerun after the layout change.
The previous flat preview there is historical
and is not refreshed. The fresh-kernel review needs `nbformat`, `nbclient`, `nbconvert`,
and `ipykernel`; these are review tools, not additional imports in the student notebooks.
Commit, push, and repository visibility changes still require explicit authorization.
