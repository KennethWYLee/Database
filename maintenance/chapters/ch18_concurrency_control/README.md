# Chapter 18: Concurrency Control

This directory contains the selected Chapter 18 teaching material for the first half of
the shared Chapter 18-19 meeting.

- `student_guide.md`: shared/exclusive locks, compatibility, two-phase locking,
  deadlocks, multiversion basics, worked examples, and practice.
- `lock_scenarios.json`: original lock schedules for executable analysis.
- `lock_simulator.py`: small lock-grant, two-phase, and wait-for graph simulator.
- `mvcc_demo.py`: version-visibility and snapshot write-skew demonstration.
- `instructor/coverage_and_verification.md`: source alignment, scope, and release
  limits.
- `instructor/verify_ch18.py`: clean execution and expected-result checks.

Run the student activities:

```powershell
py -3 lock_simulator.py lock_scenarios.json
py -3 mvcc_demo.py
```

Run verification from the course root:

```powershell
py -3 maintenance/chapters/ch18_concurrency_control/instructor/verify_ch18.py
```

The programs use a deliberately small teaching model. They do not reproduce the lock
manager or multiversion implementation of any specific DBMS.
