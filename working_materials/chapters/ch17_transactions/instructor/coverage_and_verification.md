# Chapter 17 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: draft, source-checked against the complete Chapter 17 text and
  official Chapter 17 slides
- Case: original two-account transfer, predicate query, and small schedule examples
- Executable verification: passed again on August 27, 2026, using Python 3.12.9 and
  SQLite 3.45.3
- Publication: not approved

## Source scope checked

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 17, printed pages 799-829, Sections 17.1-17.11. Practice exercises,
  exercises, review terms, and further reading were inspected for context but were not
  copied.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch17.pdf`, all 40 PDF
  pages.
- Current governance, revised syllabus, chapter-material prompt, completed Chapter 16
  material, and observed SQLite 3.45.3 transaction behavior.

## Scope decision

Required instruction covers transaction concept; the simple read/write model;
atomicity, consistency, isolation, and durability; transaction states; reasons for
concurrent execution; schedules; operation conflicts; conflict serializability and
small precedence graphs; recoverability and cascadelessness; SQL isolation levels;
SQL transaction boundaries; and the phantom phenomenon. Locking, timestamps,
multiversion, and snapshot isolation appear only as an implementation overview and
bridge to Chapter 18.

Storage hierarchy is mentioned only where it clarifies durability. View
serializability, complete serializability-testing algorithms, predicate-locking
protocols, complete timestamp rules, and complete multiversion rules are
supplementary. Lock compatibility and two-phase locking belong to Chapter 18;
log-based recovery belongs to Chapter 19.

## Source and implementation cautions

1. Consistency depends on correct transaction logic and declared constraints; ACID is
   not evidence that arbitrary committed application code is correct.
2. A partially committed transaction is not yet committed. The final statement having
   executed does not establish durability.
3. Conflict serializability and recoverability are separate requirements. Passing one
   test does not establish the other.
4. The schedule analyzer infers read-from links from the nearest preceding write in a
   small single-version teaching model. It is not valid for predicate reads, versions,
   conditional writes, or complete SQL execution.
5. Repeatable read may permit phantoms in the textbook model. Product-specific labels
   and guarantees require separate verification.
6. Snapshot isolation is not presented as equivalent to serializable isolation.
7. The SQL lab demonstrates rollback and normal commit. It does not simulate a power
   failure or prove complete durability.
8. SQLite transaction syntax and observed behavior are not generalized to other
   DBMSs. The guide identifies generic concepts separately from SQLite lab syntax.

## Teaching-point alignment

| ID | Teaching point | Primary source | Worked example | Student action and feedback |
|---|---|---|---|---|
| C17.01 | transaction/simple model | 17.1-17.2, pp. 799-803; slides 17.2-17.5 | A-to-B transfer | calculate balances and invariant |
| C17.02 | ACID | 17.1, pp. 800-802; slide 17.3 | transfer failure and bad logic | classify four failures with reasons |
| C17.03 | transaction states | 17.4, pp. 806-808; slides 17.6-17.7 | constraint failure/restart | write three state paths |
| C17.04 | concurrent executions/schedules | 17.5, pp. 808-813; slides 17.8-17.13 | interleaved reads/writes | distinguish serial and serializable |
| C17.05 | conflicts/serializability | 17.6, pp. 813-819; slides 17.14-17.24 | acyclic and cyclic graphs | list edges and serial order |
| C17.06 | basic recoverability; cascadelessness as extension | 17.7, pp. 819-821; slides 17.25-17.28 | three read/commit orders | move dependent read and justify |
| C17.07 | isolation levels/anomalies | 17.8, pp. 821-823; slides 17.29-17.32 | dirty/nonrepeatable/phantom cases | match anomaly and explain evidence |
| C17.08 | implementation overview (supplementary) | 17.9, pp. 823-826; slides 17.33-17.38 | lock/timestamp/version comparison | identify multiversion and missing evidence |
| C17.09 | SQL transaction definition | 17.10, pp. 826-828; slides 17.36, 17.39 | rollback and committed transfer | execute and verify four outputs |
| C17.10 | phantom/predicate conflict | 17.10, pp. 826-828; slide 17.39 | salary predicate plus insert | distinguish row reread from matching-set change |

Every required teaching point has explanation, a complete example, student practice,
and a stated checking or feedback criterion.

## Teaching summary

The class begins with a transfer transaction, ACID, and transaction states. Students
then identify conflicts, draw one acyclic and one cyclic precedence graph, inspect basic
recoverability and isolation phenomena, and execute rollback/commit SQL plus the
schedule analyzer. Locking, timestamps, and multiversion are retained only as a bridge
to Chapter 18 and after-class reading.

## Verification command

```powershell
py -3 working_materials/chapters/ch17_transactions/instructor/verify_ch17.py
```

## Remaining limits before student release

- The instructor selected English-only student prose on August 27, 2026. The rewritten
  guide still requires final instructor content and language review before publication.
- SQLite 3 is the course DBMS; these materials are verified with SQLite 3.45.3.
- Concurrent visibility is explained but not demonstrated with two server DBMS
  connections; such a product-specific lab is outside the required course scope.
- Crash recovery and durability require the Chapter 19 lab.
- The classroom workload has not been observed with students.

## Chapter delivery status

- Files created: student guide, SQL lab, schedule data, schedule analyzer, instructor
  source/alignment record, and verifier.
- Source range checked: complete Chapter 17 text and official Chapter 17 slides.
- Executed: complete SQL transaction checks, close/reopen persistence check, schedule
  analyzer, JSON parsing, and Python syntax compilation.
- Not executed: crash recovery, server-DBMS isolation settings, and multi-connection
  concurrent anomaly reproduction.
- Chapter status: ready to proceed to Chapter 18 subject to the release limits above.
