# Chapter 3 Full Source Audit

**Source correction, 2026-09-08:** The instructor confirmed Elmasri and Navathe's
*Fundamentals of Database Systems*, seventh edition, as the prescribed text. This
record instead reviews *Database System Concepts*. It is preserved as historical
source and execution evidence, not a completed Ch3 audit of the prescribed book.
Its former next-step recommendation is superseded by the
[current audit status](../../../course_repository/full_source_audit.md).

Date: 2026-09-08. Baseline: `a9bc1a8` on `main`, with this audit's Ch2 corrections.
This is a source-to-material review, not a claim that every textbook exercise has been
solved or that every SQL product implements the book's syntax.

## Source Identity and Reading Extent

- *Database System Concepts*, seventh edition, local private PDF, SHA-256
  `6759169c44277578465d0aeebd50be0e70e832076a7e7a7a45b4e98ce4151d8c`.
- All 60 Ch3 pages were read in order: printed pp.65-124, one-based PDF pp.90-149.
  This includes all subsections, query code, outputs, formula notation, footnotes 1-13,
  Notes 3.1-3.3, summary, review terms, exercises 3.1-3.35, tools, further reading,
  bibliography and credits. A full reading is not a new solution manual.
- All Figures 3.1-3.20, the three notes, and questionable formula/query pages were
  inspected as rendered pages. The original inputs in Figs.2.1, 2.6 and 2.7 were
  revisited where Ch3 results depend on them. Fig.3.15's four groups are consistent:
  Biology's offerings are in summer and Electrical Engineering's is in 2017, not
  Spring 2018. Those rows must not be added to the displayed result.
- All 62 local official Ch3 slides were read. Slides 21-23, 26, 32, 41, 43, 50, 57
  and 61 were rendered to check image tables, mathematical operators and apparent
  code errors. In particular, the not-equivalent signs on slides 41/43 are present
  in the image even though extraction loses the slash. Slide SHA-256:
  `557f38c4f959f2f66652d02c11af34ef026b38713ed6f99975764a8391904cd5`.
- The [author errata](https://www.db-book.com/errata-dir/db-errata.pdf), dated
  December 4, 2025, were retrieved and both pages visually inspected. Ch3 entries
  qualify the ID in aggregates on pp.94/96 and correct the instructor ID in prose
  on pp.99/102. These are distinguished from additional observations below.

Textbook/slides/errata copies and rendered source pages remain private and ignored.
No full source figure, chapter transcription or textbook solution is published here.

## Section-to-Material Correspondence

Guide references mean [student_guide.md](../student_guide.md); E numbers mean examples
in [student_lab.sql](../student_lab.sql). Small examples and original diagrams are
maintained in `maintenance/course_repository/simple_examples.py` and
`maintenance/course_repository/teaching_figures.py`. All eight small examples, their
inputs, outputs, questions, interpretations and ten Ch3 diagrams were reviewed.

| Source: printed / PDF pages | Source content checked | Current material and executable evidence | Disposition |
| --- | --- | --- | --- |
| 3.1, 65-66 / 90-91 | SQL history, DDL/DML and other language parts; implementation differences | Core Question; Section 1; summary | Retained. Historical standard/version and product-coverage statements are not repeated as current facts. |
| 3.2 introduction, 66-67 / 91-92 | Schema, domain, constraints, index/authorization/physical declarations | Section 1, prerequisites; Ch14 continuation for indexes | Selected teaching unchanged; reading the rest does not introduce extra requirements. |
| 3.2.1, 67-68 / 92-93 | Character, integer, fixed/floating-point types; precision/scale and implementation caveats | SQLite TEXT/INTEGER note; E1; `ch03_small_definition` | Clarified ordinary SQLite affinity and fractional capacity. The range-only demonstration is not described as full whole-number validation. |
| 3.2.2, 68-71 / 93-96; Fig.3.1 | CREATE, keys, NOT NULL, references, INSERT, DELETE versus DROP, ALTER | Section 1; E1 study groups/members; existing key regressions | Original course schema; explicit NOT NULL and enabled foreign keys. CHECK anticipates selected Ch4 constraints, not a claim it appears in the Ch3 syntax list. |
| 3.3.1, 71-74 / 96-99; Figs.3.2-3.4 | SELECT, duplicate retention, DISTINCT/ALL, expressions, filtering | Connection table; Section 2; E2-E5; small filter/distinct | Set projection now maps to SELECT DISTINCT. Multiplier 18 is labeled an illustrative assumption, not an institutional rule. |
| 3.3.2, 74-79 / 99-104; Figs.3.5-3.7 | Multiple relations, qualification, product, matching, query meaning versus actual execution | Multiple Inputs; E6; 4 x 6 = 24 example | Retained. Source cardinality inconsistency recorded below. Comma joins are followed by explicit joins in Ch4. |
| 3.4.1, 79,81-82 / 104,106-107 | Aliases and self-uses of a relation | E2/E6; small distinct; Ch2 optional rename | Retained. No assumption that aliases permanently rename stored tables. |
| Note 3.1, 80 / 105 | Bag multiplicities, projected duplicates, product multiplicity, translation notation | Duplicate discussion; formal bag notation remains extension | Read in full. Course's logical reading order is not a physical plan. |
| 3.4.2, 82-83 / 107-108 | LIKE wildcards, ESCAPE, case handling, string operations | Section 3; E7; small patterns | Corrected default SQLite case behavior; Unicode and other engines not generalized. String-function catalog remains outside required scope. |
| 3.4.3-3.4.4, 83-84 / 108-109 | Asterisk, explicit ordering, multiple sort keys, ASC/DESC | E2-E8 and small examples | Retained. No inference of stable unordered output. |
| 3.4.5, 84-85 / 109-110 | Inclusive BETWEEN, tuple comparison, row constructors | Section 3, E7; row comparison excluded | BETWEEN retained. A lexicographic counterexample is verified separately below; no extra row-value lesson added. |
| 3.5.1-3.5.3, 85-89 / 110-114; Figs.3.8-3.12 | UNION/INTERSECT/EXCEPT, ALL multiplicities and compatibility | Section 4; E8a-c; small sets; reverse-direction practice | Retained. SQLite accepts mixed storage classes, so portability and meaningful comparison are explicit. Unsupported ALL forms remain labeled. |
| 3.6, 89-90 / 114-115 | NULL arithmetic/comparisons, three-valued logic, WHERE, DISTINCT's NULL treatment | Section 5; E9; `ch03_null`; original A/F/NULL practice | Retained. UNKNOWN is rejected by WHERE, not redefined as FALSE. The three-row figure is illustrative, not the six-row lab dataset. |
| 3.7.1, 91-92 / 116-117 | Five aggregates, duplicates and DISTINCT, COUNT(*) | Section 6; E10; verified 4/2/3/11/2.75 | Retained. Source duplicate-average calculation qualified below. |
| 3.7.2, 92-94 / 117-119; Figs.3.13-3.15 | Groups, one row per group, grouped average/count, invalid bare attributes | GROUP BY; E11; fresh SQLite checks | Retained with existing nonportable SQLite bare-column warning. Author's qualified-ID correction applied when interpreting source, not copied source SQL. |
| 3.7.3, 95-96 / 120-121; Fig.3.16 | HAVING versus WHERE; logical evaluation and allowed attributes | WHERE/HAVING; E12; `ch03_groups` | Retained. Figure yields IM=2 for the declared course input; not an execution-order guarantee. |
| 3.7.4, 96 / 121 | Ignoring NULL; aggregates on empty/all-NULL inputs | E9/E10 and Section 6 | Added empty-input boundary: one aggregate row without grouping, zero group rows with grouping. No new assignment. |
| Note 3.2, 97 / 122 | Extended algebra aggregate operator and bag operators | Formal algebra extension; simple logical grouping explanation | Fully read, not required syntax. |
| 3.8 introduction/3.8.1, 98-99 / 123-124 | Nested queries; IN/NOT IN and multi-column membership | Section 7; E13/E15-E16; original enrollment inputs | Clarified separate inner-query execution as a checking method. Non-NULL outer ID and set guarantees stated. |
| 3.8.2, 99-101 / 124-126 | SOME/ANY/ALL, empty sets, comparisons and equivalence boundaries | Explicit extension, not core SQL lab | Fully read; no claim these operators execute in SQLite. Removed irrelevant 3.8.2 locator from the small EXISTS example. |
| 3.8.3, 101-102 / 126-127 | EXISTS, correlation, NOT EXISTS, set containment | E14/E16; small subquery; no-enrollment variation | Clarified removal of the grade condition. Preserving outer duplicates differs from INTERSECT; source counterexample below. |
| 3.8.4, 103 / 128 | UNIQUE subquery predicate, duplicates/NULL, COUNT alternatives | Explicit extension | Fully read, not confused with a CREATE TABLE UNIQUE constraint or presented as SQLite syntax. |
| 3.8.5, 104-105 / 129-130 | FROM subqueries, aliases, derived aggregates, LATERAL | E17 optional; Section 7 boundary | Existing FROM example is executed; LATERAL remains excluded. SQLite syntax uses output aliases inside SELECT. |
| 3.8.6, 105-106 / 130-131 | WITH and multiple named intermediates | E18, small CTE; original department-count figure | Retained; no materialization promise. Source maximum-budget SELECT differs from its prose, recorded below. |
| 3.8.7-3.8.8, 106-107 / 131-132 | Scalar cardinality, correlation, no-FROM expressions, integer division | E19 optional; added cardinality qualification | COUNT without grouping supplies exactly one value. SQLite's multirow behavior differs from the book; no general guarantee inferred. |
| Note 3.3, 108 / 133 | Semijoin/antijoin, rewriting limits, lack of direct basic-algebra subquery operator | EXISTS intuition; later query processing | Fully read, formal operators remain extension. |
| 3.9.1, 108-110 / 133-135 | Deletion, target predicates, subqueries, stable statement meaning | Section 8; E20; small modification | Original reversible target example retained. No claim to have run every textbook self-referencing delete across vendors. |
| 3.9.2, 110-111 / 135-136 | INSERT columns/values, INSERT SELECT, evaluation-before-insertion | E1/E20; modification practice | Basic forms retained; bulk INSERT SELECT source read but not required. |
| 3.9.3, 111-114 / 136-139 | Updates, ordering of statements, CASE, scalar update and empty SUM | E20, optional scalar boundary and small rollback example | Basic forms retained. Conditional payroll/update catalog not added to syllabus. |
| 3.10/Review Terms, 114-115 / 139-140 | Summary and terminology | Objectives, errors, summary, retained evidence | Checked against chapter detail, not used instead of it. |
| Practice 3.1-3.11, 115-119 / 140-144; Figs.3.17-3.19 | Insurance, bank/employee schemas; joins/aggregation/modification conditions | Existing original P1-P6, not copied source assessments | Read all questions and schema keys. Not a claim all source solutions were produced or verified. |
| Exercises 3.12-3.35, 119-123 / 144-148; Fig.3.20 | Duplicate/NULL cases, library queries, universal membership, DML and CASE | Core/extension boundary remains unchanged | Read all questions; no textbook answers or new required exercises distributed. |
| Tools/Further Reading/Bibliography/Credits, 123-124 / 148-149 | Tools, historical references, SQL practice sites and attribution | Course remains SQLite/Jupyter | Read, not a current endorsement or full reading of cited books. |

## Source Issues and Product Boundaries

These observations are not presented as author-confirmed errata unless explicitly
identified above. The private source files are preserved unchanged.

1. **Product count, p.79 / PDF104.** The cited source tables have 12 instructors
   and 15 teaches rows, yielding 180 combinations. The printed 156 uses 13 teaches
   rows. Current Ch2 states 180; the separate course data correctly give 24.
2. **Tuple ordering, p.84 / PDF109.** Componentwise `<=` is not lexicographic `<=`.
   The original counterexample `(1,9) <= (2,0)` is true while `1<=2 AND 9<=0` is
   false. Verified by SQLite and its [row-value specification](https://www.sqlite.org/rowvalue.html),
   Section 2.1. Row comparison is not promoted into core coverage.
3. **Average illustration, pp.91-92 / PDF116-117.** Retaining all four salaries
   yields 76,750. Removing a repeated salary from both sum and count yields
   232,000/3, not 58,000. The printed 58,000 removes the repeated salary only from
   the sum while still dividing by four; it is not the result of AVG(DISTINCT).
   `verify_source_boundaries` records the three calculations separately.
4. **EXISTS versus INTERSECT, p.101 / PDF126.** The EXISTS formulation lacks
   DISTINCT. A repeated outer course can therefore survive twice, unlike INTERSECT.
   An original three-row counterexample verifies this. The current course's student
   IDs are unique; its statement about multiple inner matches remains correct.
5. **Maximum-budget query, p.105 / PDF130.** Its output is `budget`, not the department
   identifier requested in the prose. Slide 50 instead uses `department.name`, absent
   from the displayed schema. The course uses an independently checked count CTE.
6. **Slide transcription/portability issues.** Slide 26 uses `sem`, not `semester`;
   slide 57 uses `total_cred`, not `tot_cred`; slide 61 contains `takes.ID.and`.
   Slide 22's literal-percent example includes a space in its pattern. Slide 23's
   case-sensitive generalization and slide 52's multirow scalar error do not describe
   default SQLite. No slide SQL is copied verbatim into the student notebook.
7. **Dialect checks.** The [SQLite expression reference](https://www.sqlite.org/lang_expr.html)
   Sections 5, 8 and 11 supports LIKE, membership and scalar distinctions;
   [aggregate documentation](https://www.sqlite.org/lang_aggfunc.html) supports empty
   input behavior. Independently retained executions cover these exact cases in the
   course environment. Standard/product compatibility beyond SQLite was not executed.

## Maintained Corrections

- Guide: set-projection/DISTINCT mapping; range versus whole-number enforcement;
  illustrative multiplication; LIKE behavior; set-result compatibility; empty
  aggregate input; inner-query reasoning; no-enrollment predicate; non-NULL membership
  guarantees; optional scalar cardinality qualification.
- SQL lab: clarifying multiplier comment, executable default-LIKE comparison, empty
  aggregate and empty grouped-input cases within existing examples 7 and 10.
- Small examples: concrete fractional-capacity limitation and precise EXISTS locator.
- Verifier: empty/NULL/scalar/LIKE/type-affinity boundaries, different NOT EXISTS
  questions, lexicographic ordering, duplicate arithmetic and outer-duplicate examples.
- Generated Ch3 notebook and SQLite package rebuilt from those sources, not hand-edited.

The current weeks, examinations, weights, language, original exercise count and
core/optional decisions were not changed. Range-only capacity remains an explicit
teaching demonstration; converting it to a new business rule was not silently done.

## Verification

Source reading, material comparison and applicable final-version checks are complete.
Commands ran from the course root with Python 3.12.9 (`-X utf8`), SQLite 3.45.3 and
Node 24.19.0. The rendering command needs NODE_PATH pointing to the bundled Node
modules. Its first attempt without that setting failed to resolve Playwright; the
properly configured rerun passed. The failed attempt is not counted as a pass.

| Command/check | Observed result |
| --- | --- |
| `python maintenance/chapters/ch03_introduction_to_sql/instructor/verify_ch03.py` | All original and new boundary/source-counterexample assertions passed. |
| `python maintenance/course_repository/build_course_repository.py --verify` | All 12 notebooks regenerated/executed; manifest/content checks passed. |
| `python maintenance/course_repository/review_notebook.py --all-chapters` | Fourteen fresh-kernel runs passed: 12 full chapters plus separate Ch2 opening/continuation; preserved stdout matched. |
| `python maintenance/course_repository/test_repository_layout.py` | All 14 tests passed, including links, examples, scope labels and notebook structure. |
| `python maintenance/course_repository/verify_teaching_figures.py` | All 94 generated figures passed data checks; Ch3 has 10 embedded figures. |
| `node maintenance/course_repository/render_teaching_figures.cjs` | 94 SVG geometry checks passed; all 12 notebooks passed 1440/390-width image/overflow checks. All 10 unchanged Ch3 figure panels visually compared with their inputs/results. |
| `python maintenance/student_sqlite_package/build_package.py --verify` | 21-file manifest passed; fresh temporary extraction ran all 10 packaged activities successfully. |

Notebook cell 76's retained output was directly inspected: default LIKE returned
`1 | 1`, empty ungrouped aggregates returned `0 | NULL | NULL | NULL | NULL`, and the
empty grouped query printed its header with no data rows. These agree with the revised
guide. Other example outputs remained unchanged.

ZIP SHA-256: `481e50e8721c2aa253f801b56ff5fa0b30750069c76f266297bd3cc860c5cd1e`.
Two consecutive final package builds produced the same hash; each fresh extraction
passed the manifest and all packaged activities.
The earlier Ch2 ZIP hash identifies its earlier verified state, not this later rebuild.
Hashes identify working bytes before any future Git line-ending normalization.

| File | SHA-256 |
| --- | --- |
| `student_guide.md` | `1bbda88a5b121ac814a1e776c47dab59aae23bb980498aea8766eee9295e8310` |
| `student_lab.sql` | `7a0a1d861c03dc5b8a862b369a2a547396be7c0becec9bda407cf19b6bf28d21` |
| `instructor/verify_ch03.py` | `88fc69d7c2a0756d0808edc941aa48c202ee1b5e00ff6054eec080d164859e11` |
| `simple_examples.py` | `5b3ecab19c9f77eb2e1eb56bb73539a7884013745b3a3804283f11007e3bcffa` |
| `Intro DB/ch03.ipynb` | `dabcef5a7c4fb590e2a70a273b4cc505dcc1d58f01a22d48e86694f0567d24bc` |
| Private errata PDF | `46a0140a8da8018b23cfa7b8dccd8b5e704cf5ae4a64f174d24b0e741ce09791` |

No unresolved blocking source/material issue remains for continuing to Ch4.

Limitations: no full textbook solution set; no execution of unsupported vendor SQL;
no classroom/instructor acceptance trial. Self-review and repeated SQLite runs are not
independent multi-DBMS corroboration. No commit or push in this audit.
