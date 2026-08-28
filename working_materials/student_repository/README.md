# Student Repository Build

This directory builds a clean, student-facing Database Management repository from
reviewed sources in the private course repository. The generated preview is not
published automatically.

## Maintained files

- `repository_config.json`: compact week-to-chapter schedule and chapter-guide
  allow-list.
- `student_home.md`: source for the generated root `README.md`.
- `chapters_README.md`: source for the generated `chapters/README.md`.
- `build_student_repository.py`: validates sources, generates `SCHEDULE.md`, copies one
  guide and its approved supporting files into each chapter directory, and verifies the
  complete preview.

The existing SQLite package allow-list remains authoritative for executable lab files.
The chapter `student_guide.md` files remain authoritative for chapter readings.

The generated repository does not create separate weekly documents. A chapter may be
used for one or more weeks, and `SCHEDULE.md` states the coverage for each week.

## Build and verify

From the course repository root:

```powershell
py -3 working_materials/student_repository/build_student_repository.py --verify
```

Replace `py -3` with another configured Python 3 command when necessary.

The generated preview is written to:

```text
working_materials/student_repository/output/database_student_repository/
```

The `output/` directory is ignored by Git. Publishing, creating a remote repository, or
changing repository visibility requires a separate instructor decision. The private
course repository may use a `student-preview` branch containing only the generated files
for GitHub review; that branch is derived and must not be edited as the maintained source.
