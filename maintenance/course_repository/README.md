# Course Repository Build

This directory builds the twelve chapter notebooks directly in `Intro DB/` on `main`.
Local and GitHub tracked paths are identical. It does not publish a separate preview
branch or create weekly notebooks.

## Maintained Files

- `repository_config.json`: chapter sources and the 18-week schedule.
- `build_course_repository.py`: builds, executes, and verifies every notebook.
- `review_notebook.py`: validates raw JSON and executes Ch2 in three fresh kernels.
- `test_repository_layout.py`: checks layout, path safety, links, and protected files.
- `notebook_figures.py`: generates original SVG teaching diagrams with the Python
  standard library.

The chapter guides, SQL, diagrams, data, and simulation programs remain the maintained
content sources. The builder combines them into one self-contained notebook per selected
chapter.

Ch2 opts into `executable_guide` in the configuration. Its maintained Markdown contains
Python fences beside the relevant explanations; the builder emits code cells at those
positions. Adjacent `output` fences are compared with actual stdout and are not copied
as duplicate Markdown output. The notebook preserves the executed output instead.
Week 1 ends before the full four-table setup, and Week 2 runs independently.

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
python -m pip install resvg-py==0.5.0
python -m pip install nbformat nbclient nbconvert ipykernel
python maintenance/course_repository/build_course_repository.py --verify
python maintenance/chapters/ch02_relational_model/instructor/verify_week1.py
python maintenance/course_repository/test_repository_layout.py
python maintenance/course_repository/review_notebook.py
```

The renderer is a build-only dependency; notebook execution still uses Python's standard
library. Rendering uses installed fonts (Arial in the verified Windows environment), so
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
