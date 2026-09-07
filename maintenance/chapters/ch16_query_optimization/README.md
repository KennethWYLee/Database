# Chapter 16: Query Optimization

This directory contains the selected Chapter 16 teaching material for the second half
of the shared Chapter 15-16 meeting.

- `student_guide.md`: equivalent rewrites, statistics, plan interpretation, practice,
  and checking criteria.
- `student_lab.sql`: reproducible SQLite equivalent-query, outer-join counterexample,
  statistics, and plan activities.
- `instructor/coverage_and_verification.md`: source alignment, scope, and release limits.
- `instructor/verify_ch16.py`: clean-database result, statistics, and plan checks.

Run the lab:

```powershell
sqlite3 ch16_lab.db ".read student_lab.sql"
```

Run verification from the course root:

```powershell
py -3 maintenance/chapters/ch16_query_optimization/instructor/verify_ch16.py
```

The lab verifies SQLite 3.45.3 behavior. Other DBMSs expose different statistics,
costs, actual-row measurements, and plan formats.
