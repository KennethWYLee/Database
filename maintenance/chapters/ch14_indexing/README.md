# Chapter 14: Indexing

This directory contains the student-facing material and executable SQLite lab for the
selected Chapter 14 topics.

## Student files

- `student_guide.md`: explanations, worked examples, practice, and checking criteria.
- `bplus_tree_example.svg` and `bplus_tree_example.png`: an original B+ tree lookup,
  range-scan, and split diagram.
- `student_lab.sql`: reproducible table-scan, composite-index, and covering-index plans.

## Instructor files

- `instructor/coverage_and_verification.md`: source map, scope decisions, and release
  limits.
- `instructor/verify_ch14.py`: clean-database plan and artifact checks.
- `instructor/render_ch14_diagram.js`: rebuilds the PNG from the maintained SVG.

Run the student lab with the SQLite command-line program:

```powershell
sqlite3 ch14_lab.db ".read student_lab.sql"
```

Run automated verification from the course root:

```powershell
py -3 maintenance/chapters/ch14_indexing/instructor/verify_ch14.py
```

The exact wording of an `EXPLAIN QUERY PLAN` result is DBMS- and version-dependent.
Students should interpret access method, index name, and covered predicates rather
than memorize a plan string.
