# Course Repository Build

This directory builds the current Ch1, Ch2, and Ch5 first-meeting selections directly
in `Intro DB/` and twelve previous notebooks in `Intro DB/under_revision/` on `main`.
Local and GitHub tracked paths are identical. It does not publish a separate preview
branch or create weekly notebooks.

**September 8 syllabus revision:** The [current syllabus](../../Intro%20DB/syllabus.md)
and [course plan](../COURSE_PLAN.md) now use Elmasri/Navathe's seventh edition, with
three exams at 30% each and Class Performance at 10%. The chapter IDs and weekly
material mapping in this builder still describe the other textbook's existing
notebooks. They are marked historical in the configuration and are not the current
teaching schedule. A successful build does not establish alignment with the revised
syllabus. The `current_chapters` configuration separately identifies the three
prescribed-book opening selections. See the [first-meeting release](first_meeting_release.md).
Do not rename remaining notebooks or replace source locators without content review.

The [prescribed-textbook correspondence](textbook_material_correspondence.md) now
maps the required topics to existing guides, examples, and figures. It records
missing instruction and a reproduced NULL-primary-key defect in the ER mapped schema;
it does not certify revised notebooks or complete chapter source audits.

## Maintained Files

- `repository_config.json`: existing chapter sources, historical weekly material mapping,
  and the path to the current course plan.
- `build_course_repository.py`: builds, executes, and verifies every notebook.
- `review_notebook.py`: validates raw JSON and executes Ch2 in three fresh kernels;
  `--all-chapters` additionally executes each remaining chapter in its own fresh kernel.
- `test_repository_layout.py`: checks layout, path safety, links, protected files, and
  agreement between the current syllabus and course plan, including assessment weights.
- `notebook_figures.py`: dispatches original SVG teaching diagrams and renders PNGs.
- `teaching_figures.py`: maintains topic-specific diagrams with font-measured layouts.
- `opening_figures.py`: sixteen original diagrams for the prescribed-book opening selections.
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
with the syllabus and selections from Chapters 1-2 plus Chapter 5's opening concepts.

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
  ch05.ipynb
  under_revision/
    README.md
    ch02.ipynb
    ...
    ch19.ipynb
```

`Intro DB/syllabus.md` is the maintained syllabus, including schedule, assessment,
notebook links, and opening instructions. The root `README.md` is maintained navigation.
Neither file is generated or overwritten. The under_revision README is also maintained.
The builder only replaces the fifteen named notebooks after all executions succeed;
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

The fifteen notebooks are explicitly allowed by `.gitignore` and should be committed with
their source changes when authorized. The manifest and local QA files remain under ignored
`maintenance/course_repository/output/`. The older Ch2-only `review_notebook.py` and
the 96-figure `verify_teaching_figures.py`/renderer still describe the earlier twelve
notebooks and are not the current first-meeting acceptance checks. Their source and
results are retained, not silently claimed as rerun after the layout change.
The previous flat preview there is historical
and is not refreshed. The fresh-kernel review needs `nbformat`, `nbclient`, `nbconvert`,
and `ipykernel`; these are review tools, not additional imports in the student notebooks.
Commit, push, and repository visibility changes still require explicit authorization.
