# Chapter 15: Query Processing

This directory contains the selected Chapter 15 teaching material for the first half of
the shared Chapter 15-16 meeting.

- `student_guide.md`: explanations, worked examples, practice, and checking criteria.
- `student_lab.sql`: reproducible SQLite scans, selections, joins, and plan changes.
- `instructor/coverage_and_verification.md`: source map, scope, expected responses,
  and release limits.
- `instructor/verify_ch15.py`: clean-database result and plan checks.

Run the lab:

```powershell
sqlite3 ch15_lab.db ".read student_lab.sql"
```

Run verification from the course root:

```powershell
py -3 working_materials/chapters/ch15_query_processing/instructor/verify_ch15.py
```

SQLite plan text is version-dependent. Interpret the operators and access paths instead
of memorizing a particular rendering.
