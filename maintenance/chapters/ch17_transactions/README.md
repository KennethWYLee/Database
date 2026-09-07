# Chapter 17: Transactions

This directory contains the selected Chapter 17 teaching material for one meeting.

- `student_guide.md`: self-contained transaction concepts, worked schedules, SQL lab,
  practice, and checking criteria.
- `student_lab.sql`: reproducible SQLite atomicity, rollback, commit, and constraint
  activities.
- `schedule_examples.json`: original schedules used by the analysis activity.
- `schedule_analyzer.py`: executable conflict-graph, recoverability, and
  cascadelessness analysis.
- `instructor/coverage_and_verification.md`: source alignment, scope, and release
  limits.
- `instructor/verify_ch17.py`: clean-database and schedule-analysis checks.

Run the SQL lab:

```powershell
sqlite3 ch17_lab.db ".read student_lab.sql"
```

Run the schedule analysis:

```powershell
py -3 schedule_analyzer.py schedule_examples.json
```

Run verification from the course root:

```powershell
py -3 maintenance/chapters/ch17_transactions/instructor/verify_ch17.py
```

The database demonstrations verify observed SQLite 3.45.3 behavior. SQL transaction
syntax, defaults, isolation controls, and concurrent behavior differ among DBMSs.
