# Chapter 17: Transactions

## Core Question

When one business operation uses several data changes and several transactions run at the
same time, how can we judge whether the overall result is complete, serializable, and
recoverable?

## Connection to Other Chapters

Chapters 14-16 explained execution of one query. This chapter studies groups of queries
and updates that may interleave or fail. Chapter 18 introduces locks and deadlock; Chapter
19 introduces log-based recovery.

## Teaching Summary

| Topic | Worked example and practice | Evidence to retain |
|---|---|---|
| ACID and transaction states | Account transfer with commit or rollback | State sequence and final balances |
| Conflicts and serializability | Interleaved read/write schedule | Prediction, precedence graph, and cycle check |
| Recoverability | Read-from and commit order | Separate property decisions |
| Isolation and SQL activity | Concurrent-seat scenario and SQLite lab | Observed result and model limitation |

## Prerequisites

You should be able to read basic SQL, keys, and constraints and distinguish a schema from
its current data.

## Learning Objectives

After completing this chapter, you should be able to:

1. Explain atomicity, consistency, isolation, and durability through one transaction.
2. Identify active, partially committed, failed, aborted, and committed states.
3. Identify conflicting operations in a small schedule.
4. Build a precedence graph and test it for a cycle.
5. Distinguish serializability, recoverability, and cascadelessness.
6. Recognize dirty read, nonrepeatable read, and phantom scenarios.
7. Execute and verify basic `COMMIT` and `ROLLBACK` behavior.

Locking, timestamp ordering, and multiversion implementation are bridges to Chapter 18,
not major operations in this chapter.

## 1. Transaction and ACID

A transaction is one execution unit that may read and update several data items. A bank
transfer from A to B can be represented as:

```text
read(A)
A := A - 50
write(A)
read(B)
B := B + 50
write(B)
```

With A=1000 and B=2000, a correct final state is A=950 and B=2050, with total 3000.

| Property | Meaning in this example |
|---|---|
| Atomicity | Both account changes occur or neither occurs |
| Consistency | A correct transaction preserves stated rules such as nonnegative balances and total funds |
| Isolation | Concurrent transactions do not treat a partial transfer as a final state |
| Durability | A committed transfer remains after a system failure |

The DBMS cannot make incorrect application logic correct merely by committing it.
Durability also requires recovery evidence; reopening a file after a normal close is not
a crash-recovery test.

### Practice

Match each case to its main ACID concern and explain the data effect:

1. One of two concurrent edits disappears.
2. A reported successful order is missing after restart.
3. Order detail exists without its required order header.
4. Inventory becomes negative because no rule prevents it.

The main answers are isolation, durability, atomicity, and consistency.

## 2. Transaction States

```text
active -> partially committed -> committed
   |               |
   +-----> failed <-+
             |
             v
          aborted -> terminated
             |
             +-----> active when a safe retry is allowed
```

- **Active:** execution is in progress.
- **Partially committed:** the last statement finished, but durable commit is not yet
  established.
- **Committed:** the system accepts the transaction as successfully completed.
- **Failed:** execution cannot continue normally.
- **Aborted:** effects have been removed.

A deadlock victim may be safe to retry. Invalid SQL, a permanent constraint violation,
or incorrect application logic usually requires correction rather than identical retry.
Statement-error behavior differs among DBMS products and drivers.

### Practice

Write a state path for a successful commit, a deadlock victim that is safely retried, and
a failure after the last statement but before commit becomes durable.

## 3. Schedules and Conflicts

A **schedule** records the order of important operations from several transactions while
preserving each transaction's own operation order. A serial schedule completes one
transaction before the next. A serializable schedule may interleave operations but has an
effect equivalent to a serial order.

Two operations conflict when they:

1. belong to different transactions;
2. access the same data item; and
3. include at least one write.

Read-read does not conflict. Read-write, write-read, and write-write on the same item do.

### Acyclic Example

```text
r1(A), w1(A), r2(A), r2(B), w2(B)
```

`w1(A)` precedes `r2(A)`, giving edge `T1 -> T2`. The graph has no cycle, so the schedule
is conflict serializable with order T1, T2.

### Cyclic Example

```text
r1(A), r2(B), w1(B), w2(A)
```

The B conflict gives `T2 -> T1`; the A conflict gives `T1 -> T2`. The cycle means the
schedule is not conflict serializable.

### Practice

Analyze:

```text
r1(A), r2(A), w2(A), r1(B), w1(B), c2, c1
```

The A conflict gives `T1 -> T2`. There is no reverse conflict edge, so the graph is
acyclic and T1, T2 is a serial order. Commit order need not equal serialization order.

## 4. Recoverability and Cascadelessness

Serializability concerns the interleaved result. Recoverability concerns commit order
after one transaction reads another transaction's write.

If Tj reads a value written by Ti, a recoverable schedule requires `commit(Ti)` before
`commit(Tj)`. A cascadeless schedule requires the stronger order `commit(Ti)` before the
dependent read by Tj.

```text
S1: w1(A), r2(A), c2, a1
S2: w1(A), r2(A), c1, c2
S3: w1(A), c1, r2(A), c2
```

- S1 is nonrecoverable.
- S2 is recoverable but not cascadeless.
- S3 is cascadeless and therefore recoverable.

Practice: move only `r2(X)` in `w1(X), r2(X), c1, c2` to make the schedule cascadeless.
The result is `w1(X), c1, r2(X), c2`.

## 5. Isolation Phenomena

- **Dirty read:** a transaction reads another transaction's uncommitted value, which may
  later be rolled back.
- **Nonrepeatable read:** the same row is read twice and a committed update changes its
  value between reads.
- **Phantom:** the same predicate query returns a different set because another
  transaction inserts, deletes, or updates a matching row.
- **Lost update:** one transaction's update overwrites another update based on an older
  value.

### Textbook Isolation-Level Model

| Level | Main promise and remaining risk |
|---|---|
| Serializable | Execution must satisfy a serializable result |
| Repeatable read | Committed row values repeat, but phantoms may remain |
| Read committed | No dirty read; repeated values and predicate sets may change |
| Read uncommitted | Dirty, nonrepeatable, and phantom reads may occur |

Product behavior can differ even when names match. Check official documentation and run
a concurrent multi-connection test before making a product claim.

### Phantom Example

T1 runs:

```sql
SELECT COUNT(*)
FROM instructor
WHERE salary > 90000;
```

T2 inserts a matching instructor and commits before T1 repeats the query. The result set
changes even though the new row was not part of T1's first read.

## 6. SQL Transaction Activity

The course SQLite lab uses:

```sql
BEGIN;
-- statements
COMMIT;

BEGIN;
-- statements
ROLLBACK;
```

Transaction-start syntax, autocommit, and isolation-setting syntax are product and driver
specific.

### Worked Result

The first lab transaction temporarily changes A to 950 and then rolls back, restoring
A=1000 and B=2000. The second changes both accounts and writes one transfer-log row before
commit. The final values are A=950, B=2050, total 3000, and one committed log row.

### Practice

Add checks that both accounts exist, the source has enough balance, and account changes
and log insertion commit or roll back together. Test both a successful transfer and an
insufficient-funds case. "No SQL error" is not sufficient evidence.

## 7. Schedule Analyzer

```powershell
py -3 schedule_analyzer.py schedule_examples.json
```

The program finds conflicts, builds a precedence graph, attempts a topological order, and
tracks the most recent preceding write for the supplied small schedules.

| Schedule | Conflict serializable | Recoverable | Cascadeless |
|---|---:|---:|---:|
| `acyclic` | Yes | Yes | Yes |
| `cycle` | No | Yes | Yes |
| `recoverable_but_not_cascadeless` | Yes | Yes | No |
| `nonrecoverable` | Yes | No | No |
| `cascadeless` | Yes | Yes | Yes |

The `cycle` example has no read-from dependency, so its recoverability checks pass even
though it is not serializable. These are different properties.

The analyzer is a teaching model. It does not implement predicate reads, versions,
conditional writes, or complete SQL semantics.

## Common Errors

1. Treating serial and serializable as synonyms.
2. Drawing a graph edge without checking different transactions, same item, and a write.
3. Calling every acyclic schedule recoverable.
4. Treating recoverable and cascadeless as the same property.
5. Treating commit as proof of correct business logic.
6. Treating repeatable read as protection from every phantom.
7. Assuming that snapshot isolation is automatically serializable.
8. Generalizing one SQLite connection to concurrent DBMS behavior.

## Discussion and Individual Evidence

Analyze two users who both read one remaining seat and then create separate orders. State
the initial operations, final state, and whether a legal serial order could produce it.

Retain ACID answers, one acyclic and one cyclic graph, recoverability decisions, isolation
examples, lab rollback/commit output, analyzer output, and one explicit model limitation.

## Chapter Summary

A transaction groups data operations under ACID expectations. A precedence graph tests
conflict serializability, while recoverability and cascadelessness inspect read-from and
commit order. Isolation levels permit different anomalies and must be verified in the
actual DBMS. Chapter 18 turns these requirements into lock and deadlock decisions.

## After-Class Continuation

Construct one short nonserial schedule and evaluate conflict serializability,
recoverability, and cascadelessness separately. Retain the precedence graph, read-from
relationships, commit order, and one limitation of the analysis model.
