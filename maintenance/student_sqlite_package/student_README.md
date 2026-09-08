# Database Management SQLite Labs

**Previous material: not assigned.** This package retains older textbook chapter
numbers. They do not identify the current course's chapters, weeks, or examination
scope. For September 10, use the course syllabus and its Ch1, Ch2, and Ch5 opening
notebook links. This package is not needed for the first meeting.

This package contains the SQLite files used in Chapters 2-7 and 14-17. The data are
synthetic and may be recreated at any time.

## Requirements

- Python 3 with the standard `sqlite3` module.
- SQLite 3.39 or later. The package was verified with SQLite 3.45.3.
- No third-party Python package and no server database are required.

Check the available labs:

```powershell
py -3 run_labs.py --list
```

On macOS or Linux, replace `py -3` with `python3`.

## Run the labs

Run every packaged lab and create fresh databases:

```powershell
py -3 run_labs.py all
```

Run one or more chapters:

```powershell
py -3 run_labs.py ch03
py -3 run_labs.py ch14 ch15 ch16
```

Generated databases are placed in `databases/`. Each run recreates the database used
by the selected chapter, so do not keep personal work only in those files.

## Chapter files

| Chapter | Files and database | What to inspect |
|---|---|---|
| Ch2 | `materials/ch02/`; `course_registration.db` | Relations, keys, and relational-algebra results |
| Ch3 | `materials/ch03/`; `course_registration.db` | SQL results, `NULL`, aggregation, selected subqueries, and reversible modifications |
| Ch4 | `materials/ch04/`; `course_registration.db` | Joins, views, constraints, and basic transactions |
| Ch5 | `materials/ch05/`; `course_registration.db` | Window functions, recursive CTEs, and one audit trigger |
| Ch6 | `materials/ch06/`; `ch06_er_design.db` | Business rules, E-R diagram, mapped schema, keys, and foreign keys |
| Ch7 | `materials/ch07/`; `ch07_normalization.db` | Anomalies, normalized relations, lossless reconstruction, and a lossy counterexample |
| Ch14 | `materials/ch14/`; `ch14_indexing.db` | Index definitions and before/after query plans |
| Ch15 | `materials/ch15/`; `ch15_query_processing.db` | Scans, index searches, and join access paths |
| Ch16 | `materials/ch16/`; `ch16_query_optimization.db` | Equivalent results, outer-join counterexample, statistics, and skew |
| Ch17 | `materials/ch17/`; `ch17_transactions.db` | Rollback, commit, balances, transaction log, and schedule analysis |

Ch2-Ch5 share `course_registration.db`. When any of these chapters is selected, the
runner first rebuilds the common schema and synthetic data.

## Using another SQLite interface

You may open a generated database with a compatible SQLite command-line or graphical
interface. Run the SQL files from top to bottom and keep foreign-key enforcement on.
The exact display format may differ between tools, but row values, constraints, and
database changes should agree.

## Evidence to retain

For assigned activities, keep only the evidence requested by the instructor. Typical
evidence includes:

- the SQL statement or schema being checked;
- the relevant result rows or query-plan lines;
- the expected result written before execution;
- a short explanation of any difference;
- a corrected statement or design after feedback.

Do not submit the generated database alone. A database file does not show what you
predicted, checked, or revised.

## Common problems

- **SQLite is too old:** use a Python installation whose `sqlite3` version is 3.39 or
  later.
- **A table is missing:** run the chapter through `run_labs.py`; Ch2-Ch5 require the
  shared setup file.
- **A foreign key is not enforced:** confirm that `PRAGMA foreign_keys = ON` is active
  on the current connection.
- **Personal changes disappeared:** the runner intentionally recreates selected
  databases. Save personal SQL in a separate file.
- **A query plan looks different:** record the SQLite version and interpret scan,
  search, index, and temporary-work evidence instead of matching plan text character
  for character.
