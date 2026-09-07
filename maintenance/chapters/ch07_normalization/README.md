# Chapter 7: Relational Database Design and Normalization

This directory contains the student-facing material and executable SQL for the selected
Chapter 7 topics used in Database Management.

## Student files

- `student_guide.md`: explanations, worked examples, practice, and checking criteria.
- `student_lab.sql`: a reproducible SQLite lab for anomalies, lossless reconstruction,
  constraints, and a deliberately lossy join.

## Instructor files

- `instructor/coverage_and_verification.md`: source map, scope decisions, expected
  responses, and release limits.
- `instructor/verify_ch07.py`: clean-database checks for the SQL examples and the
  functional-dependency reasoning used in the guide.

Run the lab in a disposable SQLite database. The script drops and recreates its own
tables.

```powershell
sqlite3 ch07_lab.db ".read student_lab.sql"
```

Run the automated verification from the course root:

```powershell
py -3 maintenance/chapters/ch07_normalization/instructor/verify_ch07.py
```

The material is a draft until the instructor approves its language, classroom workload,
and assessment use.
