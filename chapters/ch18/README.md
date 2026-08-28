# Chapter 18: Concurrency Control

## Core Question

How can a DBMS decide whether a read or write may proceed when several transactions
access the same data at the same time?

Chapter 18 and Chapter 19 share one class meeting. The classroom core is limited to
shared and exclusive locks, grant-or-wait decisions, wait-for graphs, and deadlock
detection. Detailed two-phase-locking variants, multiversion schemes, snapshot isolation,
and write skew are extensions.

## Connection to Other Chapters

Chapter 17 used conflicts and precedence graphs to judge completed schedules. This
chapter introduces rules that control operations while transactions are running.
Chapter 19 then explains how log records support recovery after an abort or crash.

## Prerequisites

You should be able to read schedule notation such as `r1(A)`, `w2(B)`, and `c1`, and
recognize a cycle in a small directed graph.

## Learning Objectives

After completing the classroom core, you should be able to:

1. Use an S/X compatibility matrix to decide whether a lock request is granted or waits.
2. Explain why a waiting transaction depends on an incompatible lock holder.
3. Build a wait-for graph from blocked requests.
4. Detect a deadlock cycle and explain why a victim transaction must be rolled back.
5. State the main limitation of the supplied lock simulator.

## Teaching Summary

| Classroom topic | Worked evidence | Evidence to retain |
|---|---|---|
| S/X compatibility | Two readers and one writer | Grant/wait decisions with reasons |
| Wait-for graph | Two transactions waiting in opposite order | Directed graph and cycle |
| Deadlock response | Victim rollback | Explanation of released locks and retry risk |

## 1. Shared and Exclusive Locks

A transaction must obtain an appropriate lock before accessing a protected item. An
incompatible request waits until the conflicting holder releases its lock.

- A **shared lock (S)** permits reading.
- An **exclusive lock (X)** permits reading and writing.

### Compatibility Matrix

| Existing lock held by another transaction | Request S | Request X |
|---|---:|---:|
| S | grant | wait |
| X | wait | wait |

Multiple readers can hold `S` on the same item. Any pair involving an `X` lock held by a
different transaction is incompatible.

### Worked Example

```text
1. T1 requests S(A) -> grant
2. T2 requests S(A) -> grant
3. T3 requests X(A) -> wait for T1 and T2
4. T1 releases S(A) -> T3 still waits for T2
5. T2 releases S(A) -> T3 may receive X(A)
```

The writer cannot proceed after Step 4 because one incompatible holder remains.

### Predict Before Checking

Current locks are `T1:S(A)`, `T2:S(A)`, and `T3:X(B)`. Decide whether each request is
granted or waits:

1. `T4:S(A)`
2. `T4:X(A)`
3. `T4:S(B)`
4. `T4:X(C)`, where C has no holder

### Check Criteria

The decisions are grant, wait, wait, and grant. For every decision, identify the holder,
item, and compatibility-matrix entry.

## 2. Wait-For Graphs and Deadlock

A deadlock occurs when transactions wait in a cycle and none of them can continue.

```text
1. T1 receives X(A)
2. T2 receives X(B)
3. T1 requests X(B) -> waits for T2
4. T2 requests X(A) -> waits for T1
```

In a wait-for graph, each vertex is a transaction. Draw `Ti -> Tj` when `Ti` is waiting
for `Tj` to release an incompatible lock.

```text
T1 -> T2
T2 -> T1
```

The cycle indicates a deadlock in the current wait-for graph. This edge direction is
different from the conflict-order meaning used in a Chapter 17 precedence graph.

### Practice

Given the edges `T1->T2`, `T2->T3`, `T3->T1`, and `T4->T2`:

1. Identify the transactions in the deadlock cycle.
2. Decide whether rolling back T4 breaks that cycle.
3. Explain what must be recomputed after T2 is rolled back and releases its locks.

### Check Criteria

T1, T2, and T3 form the cycle. T4 is not in that cycle, so rolling back T4 does not break
it. Rolling back T2 removes or changes waits involving locks held or requested by T2, and
the graph must be rebuilt from the remaining lock state.

## 3. Responding to Deadlock

Common approaches include:

- **Prevention:** restrict lock acquisition so a cycle cannot form, for example by using
  a common item order.
- **Detection and recovery:** allow waiting, detect a cycle, then roll back a victim.
- **Timeout:** roll back a transaction after a waiting threshold.

A timeout does not prove that a deadlock existed. A valid transaction may simply have
waited a long time. Victim selection may consider completed work, held locks, rollback
effects, and how often a transaction has already been selected. Repeatedly selecting the
same victim can cause starvation.

### Worked Example

If every transaction must request A before B, one transaction cannot hold B while waiting
for A as another holds A while waiting for B. The common order prevents that particular
cycle, although it may reduce flexibility or require advance knowledge of the access set.

### Discussion

When an API receives a deadlock-victim error, should it retry automatically? A complete
answer must consider whether the transaction is safe to repeat, whether an external side
effect could be duplicated, maximum retries, backoff, logging, and final failure handling.

## 4. Executable Activity

Predict each outcome before running:

```powershell
py -3 lock_simulator.py lock_scenarios.json
```

| Scenario | Main expected observation |
|---|---|
| `compatible_reads` | T1 and T2 both receive S(A) |
| `writer_waits` | T2 waits for X(A) until T1 commits |
| `deadlock` | Edges `T1->T2` and `T2->T1` form a cycle |
| `violates_two_phase` | `two_phase=false` |
| `basic_two_phase_not_strict` | `two_phase=true`, `strict_two_phase=false` |

The classroom evidence focuses on the first three scenarios. The final two support the
extension section.

The simulator models S/X compatibility, a simplified FIFO waiting rule, selected lock
release rules, and wait-for graphs. It does not implement lock upgrades, multiple
granularity, predicate locks, a production DBMS scheduler, SQL semantics, or crash
recovery. Its output is teaching-model evidence, not a measurement of a specific DBMS.

## Extension: Two-Phase Locking

Basic two-phase locking separates lock use into a growing phase, in which locks may be
acquired but not released, and a shrinking phase, in which locks may be released but no
new lock may be acquired.

```text
Legal basic 2PL:
lock-X(A), lock-S(B), unlock(A), unlock(B), commit

Violation:
lock-S(A), unlock(A), lock-X(B), commit
```

The second sequence requests a new lock after the shrinking phase begins. Basic 2PL
supports conflict serializability but can still deadlock. Strict 2PL retains exclusive
locks until commit or abort, which prevents other transactions from reading or
overwriting uncommitted writes. Detailed protocol proofs and rigorous 2PL are not part of
the Exam 3 classroom core.

## Extension: Multiversion and Snapshot Concepts

Multiversion systems retain several committed versions so a reader may use a version
visible to its snapshot. This can reduce reader-writer blocking, but correctness depends
on version-selection and validation rules.

Snapshot isolation is not automatically serializable. Two transactions can read the
same condition, update different rows, and jointly violate a constraint without a direct
write-write conflict. The supplied `mvcc_demo.py` demonstrates this write-skew pattern as
a model. It is not a test of a production DBMS implementation.

## Common Errors

1. Claiming that only one reader can hold an S lock.
2. Claiming that an X lock blocks only writers.
3. Treating one wait edge as a deadlock without finding a cycle.
4. Confusing wait-for graph direction with precedence graph direction.
5. Assuming that a timeout proves deadlock.
6. Assuming that basic two-phase locking cannot deadlock.
7. Treating the simulator as production DBMS behavior.

## Individual Learning Evidence

Retain:

1. A completed S/X compatibility matrix with reasons.
2. The four grant-or-wait decisions.
3. One wait-for graph, its cycle, and a victim explanation.
4. Output from the first three lock-simulator scenarios.
5. One explicit simulator limitation.

Extension work may include a two-phase-locking sequence and the multiversion demo, but it
is not required for the Exam 3 classroom core.

## Chapter Summary

S/S requests from different transactions are compatible; any pair involving X is not.
A wait-for edge points from a waiting transaction to an incompatible holder, and a cycle
indicates deadlock. Deadlock handling must consider rollback effects and retry safety.
Chapter 19 connects transaction failure to log-based recovery.

## After-Class Continuation

Add a three-transaction scenario that contains two levels of waiting but no cycle. Draw
the graph before running the simulator. Study two-phase-locking variants, multiversion
visibility, snapshot isolation, and write skew as extensions.
