# Chapter 19: Recovery System

This directory contains the selected Chapter 19 teaching material for the second half
of the shared Chapter 18-19 meeting.

- `student_guide.md`: failure classes, log records, WAL, undo/redo, checkpoints,
  backup/log recovery, worked examples, and practice.
- `recovery_case.json`: original crash and archival-backup recovery case.
- `recovery_simulator.py`: executable redo/undo and backup-plus-log demonstration.
- `wal_scenarios.json`: valid and invalid log/data flush timelines.
- `wal_checker.py`: executable write-ahead logging checks.
- `instructor/coverage_and_verification.md`: source alignment, scope, and release
  limits.
- `instructor/verify_ch19.py`: clean execution and expected-result checks.

Run the student activities:

```powershell
py -3 recovery_simulator.py recovery_case.json
py -3 wal_checker.py wal_scenarios.json
```

Run verification from the course root:

```powershell
py -3 maintenance/chapters/ch19_recovery_system/instructor/verify_ch19.py
```

The programs implement a deliberately small physical logging model. They are not an
ARIES implementation and do not reproduce a particular DBMS recovery subsystem.
