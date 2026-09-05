# Course Repository Build

This directory builds the unified Database Management repository. The generated course
repository does not separate instructor and student navigation, and it does not create
weekly or chapter subdirectories.

## Maintained Files

- `repository_config.json`: chapter sources and the 18-week schedule.
- `course_home.md`: source for the navigation section of the generated root `README.md`.
- `build_course_repository.py`: builds, executes, and verifies every notebook.
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

## Generated Structure

```text
README.md
ch02.ipynb
...
ch19.ipynb
```

`README.md` contains the repository navigation, 18-week schedule, course information,
assessment rules, and policies. It is the only Markdown file in the generated root.

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
python working_materials/course_repository/build_course_repository.py --verify
python working_materials/chapters/ch02_relational_model/instructor/verify_week1.py
```

The renderer is a build-only dependency; notebook execution still uses Python's standard
library. Rendering uses installed fonts (Arial in the verified Windows environment), so
image hashes may differ across machines with different fonts. See the renderer's
[API reference](https://resvg-py.readthedocs.io/en/latest/api.html) for the SVG-to-PNG call.

The generated preview is written to:

```text
working_materials/course_repository/output/database_course_repository/
```

The output directory is ignored by Git. Publishing, replacing a Git branch, or changing
repository visibility remains a separate version-control action.
