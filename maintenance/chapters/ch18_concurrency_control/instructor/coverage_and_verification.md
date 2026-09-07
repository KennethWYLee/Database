# Chapter 18 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: draft, source-checked against the complete Chapter 18 teaching
  text and official Chapter 18 slides
- Cases: original lock schedules, wait-for graph, version visibility, and account
  write-skew counterexample
- Executable verification: passed again on August 27, 2026, using Python 3.12.9
- Publication: not approved

## Source scope checked

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 18, printed pages 835-896, Sections 18.1-18.11. End-of-chapter material was
  inspected for context but was not copied.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch18.pdf`, all 90 PDF
  pages.
- Current governance, revised syllabus, chapter-material prompt, and completed Chapter
  17 material.

## Scope decision

Required instruction covers S/X lock meaning and compatibility; grant versus wait;
wait-for graph cycles; prevention versus detection/recovery and timeout cautions; and
victim/starvation basics. Basic, strict, and rigorous 2PL; multiversion version
selection; snapshot-isolation behavior; and the write-skew counterexample are
source-checked after-class extensions.

Lock-manager data structures, graph/tree protocols, timestamp ordering, validation
algorithms, multiple granularity, insert/delete and predicate/index locking, complete
MVCC algorithms, serializable snapshot isolation, weak consistency protocols, and
advanced concurrency topics are supplementary.

## Source and implementation cautions

1. The lock simulator is an original single-process model, not an implementation of a
   commercial lock manager. It omits lock upgrade, multiple granularity, predicate
   locks, fairness details, SQL execution, and failure recovery.
2. A granted lock request is not proof that application logic is correct.
3. Basic 2PL ensures conflict serializability but not deadlock freedom or
   cascadelessness. Strict and rigorous release rules must remain distinct.
4. A wait-for edge alone is not a deadlock; the current wait-for graph must contain a
   cycle.
5. Timeout is not deadlock detection and can abort a transaction without a deadlock.
6. Multiversioning is a family of approaches. Serializability depends on the complete
   version-selection and update protocol.
7. Snapshot isolation prevents overlapping-write lost updates under its validation
   rule but can still permit nonserializable write skew.
8. The multiversion program computes a textbook-style example and does not claim
   observed behavior from any selected course DBMS.

## Teaching-point alignment

| ID | Teaching point | Primary source | Worked example | Student action and feedback |
|---|---|---|---|---|
| C18.01 | S/X locks | 18.1.1, pp. 835-839; slides 18.3-18.8 | two readers plus writer | classify four requests by holders |
| C18.02 | compatibility/grant/wait | 18.1.1-18.1.2, pp. 835-841; slides 18.3-18.8 | X waits for two S holders | cite exact matrix cell |
| C18.03 | basic 2PL (supplementary) | 18.1.3, pp. 841-844; slides 18.9-18.15 | two valid/invalid sequences | identify first release and later request |
| C18.04 | strict and rigorous 2PL (supplementary) | 18.1.3, pp. 842-844; slide 18.10 | early X versus early S release | classify basic and strict; locate rigorous difference |
| C18.05 | deadlock/wait-for graph | 18.2, pp. 849-853; slides 18.21-18.26 | two-item cycle | locate cycle and reject irrelevant victim |
| C18.06 | handling/starvation | 18.2, pp. 849-853; slides 18.22-18.26 | common item order | compare prevention/detection/timeout |
| C18.07 | multiversion basics (supplementary) | 18.7, pp. 869-872; slides 18.53-18.60 | Q versions at 10/20/30 | compute four timestamp boundaries |
| C18.08 | snapshot isolation (supplementary) | 18.8, pp. 872-879; slides 18.61-18.69 | distinct-account withdrawals | explain write skew and missing overlap |

Every classroom-core point and retained supplementary point in the table has an
explanation, a complete example, student practice, and a stated checking or feedback
criterion.

## Teaching summary

Students complete the S/X compatibility matrix, simulate grant/wait decisions, and
build a wait-for graph for a two-item deadlock. The shared Chapter 18-19 class then moves
to log evidence and recovery. Two-phase-locking variants, multiversion, and
snapshot-isolation examples remain available for after-class reading.

## Verification command

```powershell
py -3 maintenance/chapters/ch18_concurrency_control/instructor/verify_ch18.py
```

## Remaining limits before student release

- The instructor selected English-only student prose on August 27, 2026. The rewritten
  and reduced guide still requires final instructor content and language review before
  publication.
- SQLite 3 is the course DBMS. Product-specific server lock inspection, deadlock errors,
  isolation syntax, and retry behavior are outside the required course scope.
- The program models rules rather than running true concurrent DBMS connections.
- The combined Chapter 18-19 classroom workload has not been observed with students.

## Chapter delivery status

- Files created: student guide, lock scenario data, lock simulator, multiversion demo,
  instructor source/alignment record, and verifier.
- Source range checked: complete Chapter 18 teaching text and official Chapter 18
  slides.
- Executed: five lock schedules, wait-for cycle detection, 2PL classifications,
  multiversion visibility, write skew, JSON parsing, and Python syntax compilation.
- Not executed: product-specific lock manager, actual concurrent connections,
  server-DBMS deadlock recovery, and serializable snapshot isolation.
- Chapter status: ready to proceed to Chapter 19 subject to the release limits above.
