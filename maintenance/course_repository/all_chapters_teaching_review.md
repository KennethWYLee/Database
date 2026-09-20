# Chapter Teaching Review

The later instructor-requested full-source audit is tracked in
[Full Source Audit Progress](full_source_audit.md). It supersedes this report's next
action, but does not retroactively change the narrower checks recorded here.

## Version and Outcome

Revision date: 2026-09-08. Configuration: `2026.09.08-small-examples`.
Git baseline: `e4c8c545945863a41ed81500d6a40539f6cde5be` on `main`, tracking
`origin/main`. The worktree was clean when this revision began.

The twelve selected chapters retain one self-contained notebook each in `Intro DB/`.
This revision adds 51 original small worked examples: 32 executable SQL examples and
19 conceptual examples. There are 96 embedded images, including the previous 45.
The new material supplies small artificial input tables, specific predictions, an
operation or reasoning trace, a diagram, an interpretation, a practice variation,
and a check. It does not add 51 required assignments.

The syllabus, dates, travel week, three exams, assessment weights, and selected-topic
boundaries are unchanged. Ch15/16 and Ch18/19 remain restricted to their existing
classroom core. Existing extensions do not become required because an example was
added. Ch2 retains its established explanations and 19 images.

## Chapter Coverage

Each row combines retained teaching material with the new examples. The catalog's
`heading` is an exact insertion anchor in the maintained guide, and `source` records
the textbook section or product-documentation basis. The builder rejects missing or
ambiguous anchors. Use the notebook, not the catalog, for classroom reading.

| Notebook | Images | New examples | Concepts illustrated and practiced |
| --- | ---: | ---: | --- |
| [Ch2](../../Intro%20DB/ch02.ipynb) | 19 | 0 | Database/DBMS, domains, rows and attributes, schema/instance changes, repeated values and tuples, keys, foreign keys, relational algebra and set operations; retained interleaved demonstrations |
| [Ch3](../../Intro%20DB/ch03.ipynb) | 10 | 8 | Table constraints, filtering and expressions, whole-row DISTINCT, LIKE/BETWEEN/ordering, set operations, NULL, grouping/HAVING, correlated EXISTS, CTE, reversible updates |
| [Ch4](../../Intro%20DB/ch04.ipynb) | 8 | 6 | Explicit and natural joins, outer-join counting, ON/WHERE, live view results, transactions, NULL versus CHECK, foreign keys and cascading deletes |
| [Ch5](../../Intro%20DB/ch05.ipynb) | 8 | 5 | Routine input/output purpose, audit trigger and NULL transitions, recursive direction and termination, ranking ties, partitioned running totals, short conditional-aggregation extension |
| [Ch6](../../Intro%20DB/ch06.ipynb) | 10 | 7 | Requirements to schema, independent course facts, complex attributes, recursive roles, cardinality/participation, weak identity, M:N grades, ER mapping and requirement-dependent design |
| [Ch7](../../Intro%20DB/ch07.ipynb) | 8 | 6 | Anomalies, FD counterexamples, closure and key minimality, lossless reconstruction and spurious tuples, BCNF, 3NF's candidate-key condition |
| [Ch14](../../Intro%20DB/ch14.ipynb) | 6 | 3 | Nonunique search keys, B+ tree equality/range lookup, composite order, covering columns, index writes and workload evidence |
| [Ch15](../../Intro%20DB/ch15.ipynb) | 5 | 3 | Parsing/translation, logical request versus physical plan, scan/search, nested-loop matches and lookups, limits of plan evidence |
| [Ch16](../../Intro%20DB/ch16.ipynb) | 5 | 3 | Result equivalence including duplicates/NULL, uniform estimate versus frequencies, selectivity, stale/refreshed statistics, actual query-plan evidence |
| [Ch17](../../Intro%20DB/ch17.ipynb) | 7 | 5 | ACID and incorrect business logic, states, commit/rollback, conflicts, precedence graphs, recoverability/cascadelessness, isolation phenomena |
| [Ch18](../../Intro%20DB/ch18.ipynb) | 5 | 3 | S/X decisions by item, waits versus cycles, waiter-to-holder arrows, victim rollback and safe retry; existing protocol/MVCC extensions retained |
| [Ch19](../../Intro%20DB/ch19.ipynb) | 5 | 2 | Failure assumptions, memory versus persistent data, log fields and transaction status, WAL order, redo/undo and final values; existing backup extensions retained |

SQL examples start independently from the displayed tables. They do not silently rely
on edits made in a previous small example. The complete chapter labs still explain
database creation, data loading, schema inspection, and integrity checks. Supplied
Python helpers remain execution support, not a new programming objective.

Conceptual ER associations, transaction states, and waiting chains use actual node/link
diagrams where connections matter. Transformation and comparison figures use small
tables where row values are the teaching evidence. A line connecting a student and a
section represents one association and carries its grade; it is not an unexplained
cardinality arrow. Prerequisite arrows read from a course to its required course.

## Source Checks

This is an expansion of previously source-checked course materials, not a new claim of
a complete, sentence-by-sentence audit of all twelve textbook chapters. All maintained
guides affected by the expansion were read; relevant textbook passages were checked
for the additions and corrections. The earlier full-chapter coverage records remain
under each chapter's `instructor/coverage_and_verification.md`.

The local source is Silberschatz, Korth, and Sudarshan, *Database System Concepts*,
7th edition, SHA-256
`6759169c44277578465d0aeebd50be0e70e832076a7e7a7a45b4e98ce4151d8c`.
The PDF remains private and ignored. Printed pages and PDF positions do not have a
constant offset; locators below refer to printed pages, checked against page headers.

Fresh checks included these passages, not every page between separate listed locations:

| Chapter | Textbook passages checked for this revision |
| --- | --- |
| 3 | Sections 3.2-3.8: pp.66-67, 71, 73, 80-82, 85-86; existing chapter checks cover the remaining lab topics |
| 4 | Join expressions pp.125-127; views pp.137-138; constraints pp.145-148 |
| 5 | Routine interface p.199; triggers pp.207-208; recursion pp.214-215; ranking p.220; windows p.224; aggregation p.226 |
| 6 | Design and relationships pp.243, 246, 249; attributes p.251; cardinality/keys pp.254-257; redundant attributes p.261; mapping pp.264-267; design issues pp.279-281 |
| 7 | FD semantics and lossless decomposition pp.308-314; BCNF/dependency preservation/3NF pp.315-317; closure pp.323-324. Canonical-cover pp.325-326 were consulted but not added to the classroom core |
| 14 | Search-key meaning pp.623-624; B+ tree structure/query and range conditions pp.634, 637-638 |
| 15 | Processing stages p.689; cost/evidence distinction p.692; nested-loop algorithm p.705 |
| 16 | Optimization purpose p.743; estimates p.757; uniform equality estimate p.760; statistics maintenance p.761 |
| 17 | States pp.805-806; concurrency/conflicts pp.812-813; recovery/isolation pp.819-822 |
| 18 | Compatibility p.836; wait-for graph and victim recovery pp.851-853 |
| 19 | Failure/storage pp.907-909; log fields, modification, undo/redo and ordering pp.912-916, 918 |

Product-specific details were checked against SQLite's official
[CREATE TABLE documentation](https://www.sqlite.org/lang_createtable.html),
[CREATE TRIGGER documentation](https://www.sqlite.org/lang_createtrigger.html), and
[sqlite_stat1 format](https://www.sqlite.org/fileformat2.html#the_sqlite_stat1_table).
These support the SQLite primary-key exception, NULL/CHECK behavior, trigger timing,
and statistics interpretation. They do not replace the textbook for relational theory.
The data and diagrams added here are teaching adaptations, not copied textbook figures.

## Corrections

- Ch3's `study_group.group_id` now explicitly declares `NOT NULL` in both guide and
  maintained SQL. A regression check rejects NULL on INSERT and UPDATE.
- Ch5's summary says triggers run in response to an event, not necessarily after it.
- The small recursive CTE explains duplicate removal for its actual one-column node
  result, separately from the existing two-column prerequisite-pair example.
- The builder preserves actual stream output including trailing blank lines. A fresh
  Jupyter comparison found the previous trimming behavior; a regression test now covers it.
- SQL NULL is displayed as `NULL` in figure panels, not Python's `None`.
- Graph labels were repositioned where they touched edges or node boundaries. Font
  measurement also fits body words within table cells instead of unnecessarily splitting them.
- The SQLite package README's old private-repository statement was aligned with the
  already authorized September 7 public-visibility decision. No visibility change was made.

## Verification

Environment: Windows; Python 3.12.9; SQLite 3.45.3; Pillow 12.1.1;
resvg-py 0.5.0; nbformat 5.10.4; nbclient 0.10.4; nbconvert 7.17.1;
Arial/Arial Bold; installed Chrome controlled by Playwright. Commands below run from
the course root with the installed Python 3.12 interpreter and UTF-8 output.

| Command or check | Result |
| --- | --- |
| `python maintenance/course_repository/build_course_repository.py --verify` | All 12 notebooks executed; file-set, content, attachments, links and manifest checks passed |
| Repeat the notebook build and compare SHA-256 | All 12 notebook hashes identical |
| `python maintenance/course_repository/test_repository_layout.py` | 14 tests passed, including all 32 small SQL examples against authored expected output, required example fields, layout, anchors, raw schema and theoretical calculations |
| `python maintenance/course_repository/review_notebook.py --all-chapters` | 14 fresh-kernel runs passed: all 12 complete chapters plus independent Ch2 Week 1 and Week 2; exact preserved stream outputs matched |
| All `verify_*.py` scripts under `maintenance/chapters/` | 13 scripts passed, including Week 1 and the Ch3 NULL-primary-key regression |
| `python maintenance/course_repository/verify_teaching_figures.py` | SQL-backed diagram checks passed; 94 generated SVG/PNG pairs matched embedded bytes; all 96 notebook images accounted for |
| `node maintenance/course_repository/render_teaching_figures.cjs` | All 94 SVG text geometry checks passed, including network-node boundary checks; all 12 notebooks loaded their images at widths 1440 and 390 without page overflow |
| Visual inspection | All 16 gallery pages inspected; corrected NULL display, long table words, association labels and state labels inspected at full size; Ch3 desktop/mobile notebook screenshots inspected |
| `python maintenance/student_sqlite_package/build_package.py --verify` | Manifest and clean temporary extraction passed; all 10 packaged activities passed |
| Repeat package build and compare SHA-256 | Identical ZIP: `202ad1b40294f8180f859a6cfb2521020096c72b52b661bda44eb9caca700854` |
| `git diff --check` | Passed |

The separate theoretical checks calculate attribute closures, enumerate candidate keys
and implied dependencies for the 3NF/BCNF example, check wait cycles using Python's
`graphlib`, and calculate conflict, lock, commit-order and recovery outcomes. They do
not import the teaching simulators, but share the stated model assumptions. SQL tests
and fresh notebooks use the same SQLite implementation; they are not a cross-DBMS
comparison or an independent expert review.

Intermediate checks found and resolved an empty-header figure-rendering error and a
trailing-newline output mismatch. Some earlier Windows Jupyter runs emitted ZeroMQ
shutdown diagnostics after cell execution; the final 14-run pass completed with no
such diagnostics and exit status zero. No unresolved execution failure remains in
the defined checks. Local review evidence is under ignored `output/visual_review/`.

## Changed Files

- `simple_examples.py`, `teaching_figures.py`, and `build_course_repository.py`:
  maintained example data, original figures, nearby insertion, execution and outputs.
- `repository_config.json`: revision identifier only; no schedule change.
- `test_repository_layout.py`, `review_notebook.py`, `render_teaching_figures.cjs`:
  example completeness, expected outputs, separate theoretical calculations, fresh
  kernels for every chapter, and text/node boundary checks.
- Ch3 guide, lab and verifier; Ch5 guide: the objective corrections above.
- Twelve `Intro DB/chXX.ipynb` outputs are rebuilt from maintained sources.
- SQLite package ZIP is rebuilt from its unchanged allow-list after the Ch3 SQL fix.
- `PROJECT.md`, maintenance READMEs and the chapter prompt: current design and build
  responsibilities; `.gitignore`: allow only the new maintained catalog and this record.

Ignored review HTML, PNG/SVG galleries, local test outputs and unpacked package files
are not new course entry points. Private references and historical material were not
deleted, edited, or added to Git. No commit or push was made during authoring.
The instructor subsequently authorized committing this revision and pushing it to the
existing `origin/main`. That synchronization includes the maintained sources, twelve
notebooks and rebuilt SQLite ZIP; it does not expand the private-source boundary or
change the remote, history or visibility. Git history and the remote record the outcome.

## Limits and Primary Next Action

Execution and rendering do not establish student understanding or actual classroom
workload. The 19 conceptual examples are paper/model reasoning, not live concurrency
or crash tests. Stored SQL/PSM routine syntax remains non-executable in SQLite and is
explicitly labeled; only its applicable query/body behavior is exercised. No production
DBMS, actual power failure, student cohort, or classroom projector was tested. Typography
and image hashes depend on the installed fonts. Mobile figures may require zooming.

Primary next action: walk through Ch3 with the projected notebook and select the practice
variations to use in its two teaching meetings. Ch3 now represents the expanded pattern
of small inputs, predictions, executable evidence and interpretation. The outcome should
be an instructor selection of representative examples, not another required assignment
list. Completion means the selected figures are legible from the classroom and the
instructor can explain each chosen result directly from its input table and SQL.
