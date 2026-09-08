# SQLite Student Package Build

**September 10 release:** This is a preserved previous-material package, not the
first-meeting distribution. Its chapter IDs belong to the other textbook. Current
reading is the syllabus and the three opening notebooks in `Intro DB/`. The known
NULL-key defect in the old ER mapped schema remains open; a successful runner does
not verify that missing-identifier case. The allow-list is unchanged.

This directory maintains the allow-list and build process for the Database Management
student SQLite package. Chapter materials remain the authoritative sources. Files under
`output/` and the ZIP archive are generated artifacts and must be rebuilt after a source
file changes.

## Maintained files

- `package_files.json`: explicit list of files allowed in the student package.
- `student_README.md`: source for the package operating guide.
- `run_labs.py`: student runner copied into the package.
- `build_package.py`: validates the allow-list, copies files, creates hashes, and builds
  the ZIP archive.

## Build and verify

From the course directory:

```powershell
py -3 maintenance/student_sqlite_package/build_package.py --verify
```

The build creates:

```text
maintenance/student_sqlite_package/output/sqlite_course_package/
maintenance/student_sqlite_package/output/sqlite_course_package.zip
```

Verification extracts the ZIP into a clean temporary directory and runs all packaged
labs. It does not rely on the original chapter directories.

## Inclusion decision

The package includes only original or synthetic student-facing SQL, data, diagrams,
JSON, and a student analysis program. It excludes:

- textbook chapters, official slides, and third-party source files;
- historical examinations, answers, rubrics, and instructor verification records;
- generated `__pycache__`, temporary databases, and local environment files;
- `maintenance/sql_labs/university_db/`, whose publication provenance has not
  been confirmed;
- Ch5 stored-routine reference code, because it is not executable in SQLite;
- Ch18-Ch19 teaching models, because they are not SQLite labs and remain separate
  chapter materials.

The instructor approved the generated package for course use on August 27, 2026, and
authorized the existing course repository to become public on September 7, 2026.
The explicit package allow-list still applies; that visibility decision does not permit
adding private sources, assessments, or student records. This build does not publish,
upload, change visibility, or expand the allow-list.

The unified notebook builder in `../course_repository/` uses the maintained chapter
sources directly and embeds the required examples. The SQLite package remains a separately
verified distribution artifact with its original `materials/` layout and runner. The
notebook build does not change the package's approval boundary.
