# Visual Teaching Review

## Version and Scope

Reviewed on 2026-09-07. Configuration: `2026.09.07-visual-teaching`.
Git baseline: `ba20cda9de100fe62dee13dff17ec6efeb1159a4` on `main`.
The worktree already contained the approved Ch2 teaching corrections, schedule
wording, verifier changes, and rebuilt SQLite ZIP. Those changes were preserved.
This revision adds diagrams to existing content, not new assessment requirements.

The current notebooks contain 45 images: 19 in Ch2 and two or three in each other
chapter. The new catalog contains 41 original diagrams. Two earlier Ch2 diagrams
and the existing Ch6 ER and Ch14 B+ tree diagrams are retained. The earlier Ch2
selection/projection pipeline is replaced by a diagram that preserves full names
through every operation rather than visually expanding shortened names.

All images are embedded PNG attachments. The course remains one notebook per
chapter with no external image directory or extra student dependencies.

## Topic Coverage

| Chapter | Images | Visual content |
| --- | ---: | --- |
| 2 | 19 | Conflicting files; database versus DBMS; annotated relation; domains; phone values; row order; repeated values versus tuples; insert/update/schema changes; identifiers; keys; composite keys; references; schema; selection; projection; composition; product; join; set operations |
| 3 | 2 | NULL and counting; WHERE, GROUP BY, and HAVING |
| 4 | 2 | Inner versus left join; filtering in ON versus WHERE |
| 5 | 3 | Ranking ties; recursive prerequisite pairs; trigger audit values |
| 6 | 3 | ER diagram; relationship direction and participation; section and enrollment keys |
| 7 | 2 | Attribute closure; spurious tuples from a lossy decomposition |
| 14 | 3 | B+ tree; composite index column order; covering columns |
| 15 | 2 | Scan versus index access; indexed join lookups |
| 16 | 2 | Estimates versus skewed data; equal sets with unequal duplicate counts |
| 17 | 2 | Transfer commit/rollback; precedence graph |
| 18 | 2 | Lock compatibility; wait-for graph |
| 19 | 3 | Old/new log values; write-ahead ordering; redo then undo |

## Sources and Boundaries

Each new figure's `heading` in `teaching_figures.py` locates its corresponding
section in the chapter's maintained `student_guide.md`; the configuration identifies
the guide and SQL/Python sources. These guides and executable examples supplied
the current teaching scenarios. This revision did not repeat the complete textbook
audit. Earlier textbook locators and verification remain in each chapter's
`instructor/coverage_and_verification.md`; this record does not imply a fresh
whole-book source review or instructor approval.

Newly chosen teaching rows are explicitly illustrative where they differ from the
lab data, notably the Ch14 index-order rows and Ch16 duplicate-count counterexample.
Ch6 distinguishes its complete section identity from the simplified Ch2 example.
Recovery and access-path diagrams state their simulation or schematic limits.
No textbook figures, private records, assessment keys, or external images were added.

## Execution Evidence

Environment: Windows, Python 3.12.9, SQLite 3.45.3, resvg-py 0.5.0, Pillow 12.1.1,
Arial/Arial Bold, nbformat 5.10.4, nbclient 0.10.4, nbconvert 7.17.1, and installed
Chrome controlled through Playwright. Pillow, rendering, and notebook QA tools are
maintenance dependencies only. Commands were run from the course repository root
with the installed Python 3.12 executable and UTF-8 output enabled.

| Command/check | Result |
| --- | --- |
| `python maintenance/course_repository/build_course_repository.py --verify` | All 12 notebooks executed; content, paths, attachments, manifest and file-set checks passed |
| Rebuild and compare SHA-256 of every notebook | All 12 notebook hashes identical |
| `python maintenance/course_repository/verify_teaching_figures.py` | SQL-backed data checks passed; 43 generated SVG/PNG pairs exported; PNG bytes match attachments; all notebooks validate |
| `python maintenance/course_repository/test_repository_layout.py` | 10 tests passed, including missing/ambiguous figure anchors and per-chapter image counts |
| `python maintenance/course_repository/review_notebook.py` | Week 1, Week 2, and complete Ch2 passed in three separate fresh Jupyter kernels; actual output matches preserved output |
| Every `verify*.py` under `maintenance/chapters/` | All 13 scripts passed, including the separate Week 1 script |
| `node maintenance/course_repository/render_teaching_figures.cjs` | 43 SVG text-boundary/overlap checks passed; all 12 notebook images loaded at 1440px and 390px widths without page overflow |

The figure data verifier checks Ch2 relational operations and composite-key rows,
Ch3 NULL/grouping, Ch4 join results, Ch5 ranks/recursive pairs, Ch7 spurious tuples,
and Ch16 duplicate multiplicities against executed SQL. Additional arithmetic
checks cover selectivity and balances. Other conceptual diagrams were compared
with the maintained explanations and supported by the chapter verifiers; not every
conceptual claim is automatically proved by the figure data verifier.

All eight final figure-gallery screenshots were visually inspected. Initial
character-count wrapping split some labels awkwardly; the renderer now measures
actual font widths and aligns tables under their panel titles. Final Ch2 mobile
rendering was also inspected. Review HTML, SVG, PNG, screenshots, and geometry
results are kept under ignored `output/visual_review/`.

## Maintained Changes

- `teaching_figures.py`: new diagram catalog, original data displays, and renderer.
- `notebook_figures.py`: dispatch to the new catalog.
- `build_course_repository.py`: topic insertion, qualified H3 anchors, and captions.
- `repository_config.json`: visual teaching enabled for all chapters.
- `verify_teaching_figures.py`, `render_teaching_figures.cjs`, and
  `test_repository_layout.py`: data, layout, rendering, and regression checks.
- This directory's `README.md`: reproduction commands and build dependencies.
- Root `PROJECT.md`: instructor decision and current next action.
- `.gitignore`: explicit allowance for four new maintained files only.
- `Intro DB/ch02.ipynb` through the selected `ch19.ipynb`: regenerated notebooks.

Existing unrelated/private files were not removed or added to tracking. The SQLite
ZIP was not changed by the visual revision; its prior verified SHA-256 remains
`78a66a9b2a857bde69afdd077fe74be2b3447c091093b7e98774d1c709155508`.
No commit, push, remote creation, or visibility change occurred.

## Limits and Next Action

These checks establish execution and local rendering, not student understanding or
back-row classroom legibility. Dense fixed-format images need zooming on a phone;
the adjacent prose and tables remain available as text. Image hashes depend on
fonts and renderer versions. GitHub rendering of this new version has not been
inspected because publication has not been authorized. Ch2 is approximately 1.63 MB.

The primary next action is to inspect Ch2 with the actual classroom projector.
Expected outcome: confirm the explanatory sequence and legibility. Completion
criterion: field names, values, and arrows can be read at the intended viewing
distance, with any necessary enlargement identified. This does not require changing
course scope, workload, or assessment. Publication remains a separate authorization.
