# Chapter Materials

Each chapter directory contains one `README.md` student guide and its approved SQL,
Python, data, or diagram files. The [course schedule](../SCHEDULE.md) identifies which
part of a chapter is taught each week.

## Requirements

- Python 3 with the standard `sqlite3` module.
- SQLite 3.39 or later.
- No server database or third-party Python package.

## Run the Labs

List the available chapters from the repository root:

```powershell
py -3 run_labs.py --list
```

Run one or more chapters:

```powershell
py -3 run_labs.py ch03
py -3 run_labs.py ch14 ch15 ch16
```

Run every packaged lab:

```powershell
py -3 run_labs.py all
```

The examples use the standard Windows Python launcher. Use `python` on a Windows system
configured with that command, or `python3` on macOS or Linux.

Generated databases are placed in `databases/`. Each run recreates the database used by
the selected chapter, so do not keep personal work only in a generated database file.

## Materials

| Chapter | Student guide |
|---|---|
| Ch2 | [Relational Model](ch02/README.md) |
| Ch3 | [Introduction to SQL](ch03/README.md) |
| Ch4 | [Intermediate SQL](ch04/README.md) |
| Ch5 | [Advanced SQL](ch05/README.md) |
| Ch6 | [E-R Design](ch06/README.md) |
| Ch7 | [Normalization](ch07/README.md) |
| Ch14 | [Indexing](ch14/README.md) |
| Ch15 | [Query Processing](ch15/README.md) |
| Ch16 | [Query Optimization](ch16/README.md) |
| Ch17 | [Transactions](ch17/README.md) |
| Ch18 | [Concurrency Control](ch18/README.md) |
| Ch19 | [Recovery](ch19/README.md) |

Follow the current chapter guide when retaining evidence. Typical evidence includes the
statement or design being checked, a prediction, relevant output, an explanation of any
difference, and a corrected version after feedback. Do not submit a generated database
alone.

## Common Problems

- If a table is missing, run the chapter through `run_labs.py`.
- If a foreign key is not enforced, confirm that `PRAGMA foreign_keys = ON` is active.
- If a query plan differs, record the SQLite version and interpret the plan evidence
  rather than matching display text character for character.
- If personal changes disappear, save personal SQL outside `databases/`.

[Back to the repository home](../README.md)
