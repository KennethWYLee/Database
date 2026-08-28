# Course Resources

This directory contains the reviewed chapter readings and executable SQLite materials
used by the weekly course pages.

## Requirements

- Python 3 with the standard `sqlite3` module.
- SQLite 3.39 or later.
- No server database or third-party Python package.

## Run the Labs

List the available chapters:

```powershell
py -3 resources/run_labs.py --list
```

The examples use the standard Windows Python launcher. Use `python` on a Windows system
configured with that command, or `python3` on macOS or Linux.

Run one or more chapters from the repository root:

```powershell
py -3 resources/run_labs.py ch03
py -3 resources/run_labs.py ch14 ch15 ch16
```

Run every packaged lab:

```powershell
py -3 resources/run_labs.py all
```

Generated databases are placed in `resources/databases/`. Each run recreates the
database used by the selected chapter, so do not keep personal work only in a generated
database file.

## Chapter Readings and Files

| Chapter | Reading and files |
|---|---|
| Ch2 | [Relational Model](materials/ch02/README.md) |
| Ch3 | [Introduction to SQL](materials/ch03/README.md) |
| Ch4 | [Intermediate SQL](materials/ch04/README.md) |
| Ch5 | [Advanced SQL](materials/ch05/README.md) |
| Ch6 | [E-R Design](materials/ch06/README.md) |
| Ch7 | [Normalization](materials/ch07/README.md) |
| Ch14 | [Indexing](materials/ch14/README.md) |
| Ch15 | [Query Processing](materials/ch15/README.md) |
| Ch16 | [Query Optimization](materials/ch16/README.md) |
| Ch17 | [Transactions](materials/ch17/README.md) |
| Ch18 | [Concurrency Control](materials/ch18/README.md) |
| Ch19 | [Recovery](materials/ch19/README.md) |

## Evidence to Retain

Follow the current weekly page. Typical evidence includes the statement or design being
checked, a prediction, relevant output, an explanation of any difference, and a corrected
version after feedback. Do not submit a generated database alone.

## Common Problems

- If a table is missing, run the chapter through `resources/run_labs.py`.
- If a foreign key is not enforced, confirm that `PRAGMA foreign_keys = ON` is active.
- If a query plan differs, record the SQLite version and interpret the plan evidence
  rather than matching display text character for character.
- If personal changes disappear, save personal SQL outside `resources/databases/`.
