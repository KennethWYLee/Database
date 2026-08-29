# Course Repository Build

This directory builds the unified Database Management repository. The generated course
repository does not separate instructor and student navigation, and it does not create
weekly or chapter subdirectories.

## Maintained Files

- `repository_config.json`: chapter sources and the 18-week schedule.
- `course_home.md`: source for the generated root `README.md`.
- `build_course_repository.py`: builds, executes, and verifies every notebook.
- `notebook_figures.py`: generates original SVG teaching diagrams with the Python
  standard library.

The chapter guides, SQL, diagrams, data, and simulation programs remain the maintained
content sources. The builder combines them into one self-contained notebook per selected
chapter.

## Generated Structure

```text
README.md
SYLLABUS.md
SCHEDULE.md
ch02.ipynb
...
ch19.ipynb
```

SQL and Python examples are embedded in the notebook that uses them. Existing PNG
diagrams and Python-generated SVG figures are stored as notebook attachments. SQL
notebooks guide the reader through connection, table creation, data loading, schema
inspection, integrity checks, and chapter queries. The current build therefore needs no
`assets/` directory, separate lab runner, or external data file.

## Build and Verify

From the course repository root:

```powershell
python working_materials/course_repository/build_course_repository.py --verify
```

The generated preview is written to:

```text
working_materials/course_repository/output/database_course_repository/
```

The output directory is ignored by Git. Publishing, replacing a Git branch, or changing
repository visibility remains a separate version-control action.
