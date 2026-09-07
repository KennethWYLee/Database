# Course Repository Build

This directory builds the twelve chapter notebooks directly in `Intro DB/` on `main`.
Local and GitHub tracked paths are identical. It does not publish a separate preview
branch or create weekly notebooks.

## Maintained Files

- `repository_config.json`: chapter sources and the 18-week schedule.
- `build_course_repository.py`: builds, executes, and verifies every notebook.
- `review_notebook.py`: validates raw JSON and executes Ch2 in three fresh kernels.
- `test_repository_layout.py`: checks layout, path safety, links, and protected files.
- `notebook_figures.py`: dispatches original SVG teaching diagrams and renders PNGs.
- `teaching_figures.py`: maintains topic-specific diagrams with font-measured layouts.
- `verify_teaching_figures.py`: checks selected diagram data against SQL, attachment
  bytes, and notebook format; exports an ignored review gallery and notebook HTML.
- `render_teaching_figures.cjs`: uses Playwright and Chrome to check SVG text geometry,
  notebook images, and desktop/mobile page overflow, and capture review screenshots.
- `visual_teaching_review.md`: records the visual teaching revision and its evidence.

The chapter guides, SQL, diagrams, data, and simulation programs remain the maintained
content sources. The builder combines them into one self-contained notebook per selected
chapter.

Ch2 opts into `executable_guide` in the configuration. Its maintained Markdown contains
Python fences beside the relevant explanations; the builder emits code cells at those
positions. Adjacent `output` fences are compared with actual stdout and are not copied
as duplicate Markdown output. The notebook preserves the executed output instead.
Week 1 ends before the full four-table setup, and Week 2 runs independently.
These are reading sections, not first-meeting completion deadlines. The first meeting
starts with the syllabus and an introduction to Ch2.

Ch2 also opts into `inline_sql`. Its guide uses `<!-- sql:setup -->`,
`<!-- sql:example 4 -->` (and the other numbered examples), and `<!-- sql:checks -->`
to position the shared setup, existing lab examples, and final checks. The builder
extracts the `-- Example ...:` blocks from maintained SQL, embeds each exactly once,
and rejects missing, duplicated, or unknown markers. It does not append a second lab.
The markers are removed before notebook generation; `output` fences verify their results.

Each chapter opts into `visual_teaching`. The builder splits the guide at H2 and H3
headings and inserts diagrams beside the matching topic. Repeated H3 headings use
`## Parent / ### Subheading` anchors. Missing or ambiguous anchors stop the build.
Ch2 contains 19 images; each other chapter contains two or three, for 45 in total.
These explain existing content without adding assignments or changing course scope.

The builder assigns deterministic, unique cell IDs to every notebook and verifies
their format and uniqueness. Raw notebook schema validation must run before a notebook
reader can silently repair missing fields; the local Week 1 review script follows this
order before fresh-kernel execution and HTML rendering.

## Course Structure

```text
Intro DB/
  syllabus.md
  ch02.ipynb
  ...
  ch19.ipynb
```

`Intro DB/syllabus.md` is the maintained syllabus, including schedule, assessment,
notebook links, and opening instructions. The root `README.md` is maintained navigation.
Neither file is generated or overwritten. The builder only replaces the twelve named
notebooks after all executions succeed; unexpected files cause it to stop without deletion.
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
python maintenance/chapters/ch02_relational_model/instructor/verify_week1.py
python maintenance/course_repository/test_repository_layout.py
python maintenance/course_repository/review_notebook.py
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

The twelve notebooks are explicitly allowed by `.gitignore` and should be committed with
their source changes when authorized. The manifest and local QA files remain under ignored
`maintenance/course_repository/output/`. The previous flat preview there is historical
and is not refreshed. The fresh-kernel review needs `nbformat`, `nbclient`, `nbconvert`,
and `ipykernel`; these are review tools, not additional imports in the student notebooks.
Commit, push, and repository visibility changes still require explicit authorization.
