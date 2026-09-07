# Chapter 14 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: draft, source-checked against the complete Chapter 14 text and
  official Chapter 14 slides
- Case: original 20,000-row order-line workload and B+ tree diagram
- Executable verification: passed again on August 27, 2026, using Python 3.12.9 and
  SQLite 3.45.3
- Diagram verification: SVG rendered to a 1200 by 620 PNG with headless Chrome;
  visual inspection confirmed readable text, distinct nodes and arrows, no overlap,
  and no clipping
- Publication: not approved

## Source scope checked

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 14, printed pages 623-678, Sections 14.1-14.11. Exercises and further reading
  were inspected for context but not copied.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch14.pdf`, all 81 PDF
  pages.
- Current governance, revised syllabus, chapter-material prompt, completed Chapters
  2-7 materials, and SQLite 3.45.3 behavior.

## Scope decision

Required instruction covers index purpose and search keys; workload-based evaluation;
B+ tree structure, equality lookup, and range traversal; composite key order; covering
indices; index selection; `CREATE INDEX`/`DROP INDEX`; and evidence-based
`EXPLAIN QUERY PLAN` interpretation. Clustering/secondary and dense/sparse distinctions,
conceptual split/merge behavior, and the ordered-versus-hash comparison are extensions.

Complete B+ tree insertion/deletion pseudocode and complexity derivations, B-tree
details, file organization, string compression, bulk loading, flash/main-memory
variants, LSM and buffer trees, bitmap indices, spatial indexing, and temporal indexing
are supplementary. Hashing is a short comparison only.

## Source and implementation cautions

1. Search key does not imply uniqueness and must not be confused with candidate or
   primary key.
2. The textbook uses primary index as a synonym for clustering index, not necessarily
   an index on a primary key. The guide consistently introduces both words.
3. Sparse indices require physical search-key order; secondary indices must be dense.
4. The B+ tree diagram is original and deliberately uses a tiny fanout. It illustrates
   invariants and traversal, not a SQLite page layout.
5. SQLite's ordinary indexes use its B-tree implementation and do not provide the
   user-created hash index needed for an executable ordered/hash comparison.
6. Composite-index use depends on leading predicates, but optimizer features such as
   skip-scan can produce version- and statistics-dependent plans.
7. `EXPLAIN QUERY PLAN` output is not a stable API. The verifier checks the access
   method, index name, and constrained columns observed in SQLite 3.45.3.
8. Runtime alone is not used as evidence. The lab fixes data generation, records row
   counts, runs `ANALYZE`, and compares plan structure.
9. The covering index duplicates the prefix of the smaller composite index only for a
   staged demonstration; the smaller index is dropped at the end.

## Teaching-point alignment

| ID | Teaching point | Primary source | Worked example | Student action and feedback |
|---|---|---|---|---|
| C14.01 | index purpose/search key | 14.1, pp. 623-625; slides 14.3-14.4 | grade as nonunique search key | distinguish course key and department index |
| C14.02 | evaluation factors | 14.1, p. 624; slide 14.4 | student lookup workload | compare read-heavy/update-heavy cases |
| C14.03 | clustering/secondary | 14.2, pp. 625-626; slide 14.5 | ID order versus department index | explain one physical order |
| C14.04 | dense/sparse | 14.2.1, pp. 626-628; slides 14.6-14.10 | three data blocks | find missing key and update block entry |
| C14.05 | B+ tree structure/balance | 14.3.1, pp. 634-637; slides 14.18-14.22 | original three-leaf diagram | trace three keys |
| C14.06 | equality/range lookup | 14.3.2, pp. 637-640; slides 14.23-14.29 | key 50 and range 45-80 | produce range 25-75 and stop condition |
| C14.07 | split/merge concept | 14.3.3-14.3.4, pp. 641-649; slides 14.30-14.45 | insert 65 and promote 60 | propagate split to a new root |
| C14.08 | ordered/hash comparison | 14.1 and 14.5, pp. 624, 658-661; slides 14.52-14.59 | modulo buckets versus range | choose for token/date queries |
| C14.09 | composite index order | 14.2.5 and 14.6.2, pp. 633-634, 662-663; slides 14.16, 14.61-14.62 | customer/date query | classify four dept/salary predicates |
| C14.10 | covering index | 14.6.3, p. 663; slide 14.63 | add amount to index | evaluate adding status |
| C14.11 | create/drop and plan | 14.7, pp. 664-665; slides 14.64-14.65 | staged SQLite plans | preserve three plans and interpret |
| C14.12 | index selection/tradeoff | 14.7, pp. 664-665 | two-index proposal | revise using plan and maintenance cost |

Every required teaching point has explanation, a complete example, student practice,
and a stated checking or feedback criterion.

## Teaching summary

1. Distinguish logical key constraints from index search keys.
2. Rank workload evidence needed before creating an index.
3. Trace dense and sparse lookup over three blocks.
4. Read the B+ tree diagram and perform equality/range lookup.
5. Insert 65, split the leaf, and preserve balance.
6. Compare B+ tree and hash for equality/range needs.
7. Predict composite-index support for four predicates.
8. Execute the no-index, composite, and covering plans.
9. Compare at most two index proposals and revise after plan evidence.

## Verification commands

```powershell
node maintenance/chapters/ch14_indexing/instructor/render_ch14_diagram.js
py -3 maintenance/chapters/ch14_indexing/instructor/verify_ch14.py
```

## Remaining limits before student release

- The instructor selected English-only student prose on August 27, 2026. The rewritten
  guide still requires final instructor content and language review before publication.
- SQLite 3 is the course DBMS; these materials are verified with SQLite 3.45.3.
- Classroom workload and students' prior tree knowledge have not been observed.
- `COURSE_PLAN.md` governs Chapter 14 scope and assessment boundaries.

## Chapter delivery status

- Files created: student guide, SQL lab, maintained SVG, PNG renderer, instructor
  source/alignment record, and verifier.
- Source verification: complete for textbook printed pages 623-678 and all 81 pages
  of the local official slide PDF.
- Executed content: deterministic data generation; no-index scan; composite
  customer/date index search; ordered result; covering-index plan; low-selectivity
  status scan; SVG parsing; PNG rendering; and visual inspection.
- Unexecuted content: hash index implementation and all supplementary structures.
- Progression decision: the chapter meets the source, explanation, worked-example,
  practice, plan-evidence, executable-check, and rendered-diagram conditions required
  to begin Chapter 15. It remains a draft until the instructor reviews language and
  classroom workload.
