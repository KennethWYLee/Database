# Photographed Exercise Answer Release

Date: 2026-09-20. Instructor authorization: exercise answers may be public for
every scheduled chapter. Ordinary teaching material remains Ch1-3 only.
The syllabus, assessment weights and assigned sections are unchanged.

## Released Coverage

| PDF | Questions | Pages | Source status |
|---|---:|---:|---|
| ch02_answer.pdf | 2.1-2.15 | 16 | Newly authored against photographed pp.85-86 and relevant chapter passages |
| ch03_answer.pdf | 3.1-3.35 | 55 | Existing source-checked version, unchanged; verifier rerun |
| ch04_answer.pdf | 4.1-4.33 | 62 | Existing source-checked version, unchanged; verifier rerun; publication restored |
| ch05_answer.pdf | 5.1-5.20 | 21 | Newly authored against photographed pp.200-204 and Figures 5.1, 5.5-5.8 |
| ch06_answer.pdf | 6.1-6.16 | 19 | Newly authored against photographed pp.233-235 and referenced schemas |
| ch07_answer.pdf | 7.1-7.9 | 13 | Newly authored against photographed pp.266-268 and referenced schemas |

Total: 128 numbered answers, 186 PDF pages. This is not a claim that every
question has one uniquely correct design, that every native-tool lab was run,
or that the entire textbook was read sentence by sentence in this task.

Ch1, Ch8-9 and Ch14-19 are authorized but blocked by missing photographed
questions and referenced figures. A different PDF is not substituted for them.

## Source Records

The photographed files remain private. Their SHA256 identifiers are:

| Chapter | SHA256 |
|---|---|
| 2 | dd0d024f7d771c674d5a674d8d111d57fe147ec29b19e6171eac2cdb11672bfc |
| 3 | 55366a1faa7718dd1b89bdb95a938db5c5e7b00886f99aeb88a16086409e72c7 |
| 4 | 6a89e99b4e81233f0afc673d5a4c80a73492f57bf2628f8123836722736d9c9b |
| 5 | 861034acd69cd319fdec4e3ba11233bf9162f28ea067c1e90ac4d2f9c213c491 |
| 6 | 69deee881ae13090c8c5d866eac2640eba42972d328f39a705881441075b1028 |
| 7 | be8b151624db7c5ec5a0e567a99a791e45c6da6d4c74e8ea522dd4d05bca8baa |

Each newly authored answer carries a printed-page locator. The source modules
and detailed QA remain in the existing private source boundary:
`private_references/semester_answers/`. Existing Ch3/Ch4 source records are
retained in their respective solution directories. No publisher solutions,
photographed pages or full question statements are added to the public tree.

## Important Interpretations

- Figure 2.1 explicitly supplies the schema for Figure 1.2. University SQL
  tests use original, labeled rows, not claimed Figure 1.2 result data.
- 5.13 has an undefined `Product_section#`; keys are given only under explicit
  row-meaning and uniqueness assumptions.
- 5.17 has no outgoing AGENT foreign key. The answer distinguishes a duplicate
  agent key from a referential-integrity violation and supplies all four tables.
- 5.19 retains `Local_phone` and `Cell_phone`, not Figure 5.1's other phone roles.
- 6.10 uses the printed salary threshold 3000 and explains the mismatch between
  `Computerisation` in the question and `Computerization` in the data.
- 6.12 follows the printed `Class=1`, despite the word junior; completed work
  is explicitly interpreted as a non-NULL grade.
- Figure 5.6 has NULL Hours for Borg, while Figure 6.1 declares Hours NOT NULL.
  The COMPANY test fixture preserves the photographed state and discloses this
  deliberate difference from the later DDL.
- 6.15 separates the isolated supervision cascade from the retained manager
  foreign key whose SET DEFAULT target is itself being deleted.
- 7.5(b) shows both defensible readings of the male-count condition.
- 7.6 specifies the handling of no courses and unknown grades.
- 7.8 reports known-hour sums without treating an unknown contribution as zero.
- 7.9 rejects direct aggregate-view writes, including a zero-match deletion.

## Verification

Environment: Python 3.12.9, SQLite 3.45.3; ReportLab generation, PyMuPDF text
inspection, Poppler rendering. The maintained builder runs verification first.

```powershell
python private_references/semester_answers/verify.py
python private_references/semester_answers/build.py
python private_references/semester_answers/qa_pdf.py
python private_references/ch03_solutions/verify.py
python private_references/ch04_solutions/verify.py
# From maintenance/course_repository in the public release checkout:
python -m unittest test_repository_layout test_ch03_er test_second_meeting
```

- 80 new checks: complete question numbering; every authored executable SQL
  block; independently specified query results; all eleven independent updates;
  all four requested views; empty groups/projects, NULLs, tied salaries;
  seven/nine/seven-table DDL; foreign-key, duplicate-key and date failures;
  cascade success and constraint-blocked rollback; grouped-view write rejection.
- Ch3: 19 existing tests passed. Ch4: 27 existing tests passed, including its
  separate-process rebuild and model counterexamples. Their PDF hashes match
  the previously checked exports; neither answer PDF was changed.
- All 69 newly generated pages rendered. Full-page contact sheets and enlarged
  table/SQL pages were inspected; numbering, text bounds, no embedded files,
  no local paths in student PDFs, metadata and byte-identical rebuilding checked.
- Initial layout checks found orphan paragraphs and narrow result columns;
  these were repaired without reducing font size. A stale-render page-count
  failure was fixed by using hash-specific QA directories. An apartment test
  initially mixed sequential insertions; independent starts now isolate the FK
  failure correctly.
- Public release checks use the existing explicit PDF allow-list, exact PDF
  and notebook hashes, expected file set and README links. No private branch
  is pushed or merged into the release history.
- The public suite reported 69 tests run, no failures and 4 explicit skips:
  three checks require absent legacy sources, and the Ch5/Ch8 teaching-test
  class requires unreleased local sources. The published answer checks passed;
  these skips do not refer to the new Ch5-7 answer SQL verification.

Limits: SQL execution is SQLite-specific, not a multi-DBMS certification.
MongoDB was not run. Textbook assertions and unsupported SQL syntax are discussed
but not reported as successful executions. Ch3 Q3.31-3.35 and Ch4 Q4.28-4.33
native modeling-tool tasks remain conceptually answered, not completed in ERwin
or Rational Rose. Open-ended assumptions still benefit from instructor review.

## Next Action

Supply the missing photographed exercise pages and every referenced figure for
Ch1, Ch8-9 and Ch14-19. Completion means that each remaining question number,
subpart and required schema/data figure is readable and source-locatable; only
then can its worked answer be checked and released.
