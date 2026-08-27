# Chapter 19: Recovery System

## Core Question

After a crash, how can a DBMS preserve committed updates and remove the effects of
incomplete transactions?

Chapter 18 and Chapter 19 share one class meeting. The classroom core is limited to log
records, write-ahead logging, transaction status, and a small redo/undo case. Detailed
checkpoint algorithms, backup administration, ARIES, and production restore procedures
are extensions.

## Connection to Other Chapters

Chapter 17 defined atomicity and durability. Chapter 18 explained how transactions may
wait or be rolled back during concurrent execution. This chapter introduces the log
evidence needed to recover after an abort or system crash.

## Prerequisites

You should be able to follow transaction events in order, distinguish `COMMIT` from
`ROLLBACK`, and distinguish a memory buffer from persistent storage.

## Learning Objectives

After completing the classroom core, you should be able to:

1. Distinguish a transaction error, a system crash, and storage loss.
2. Interpret start, update, commit, and abort log records.
3. Explain the two ordering requirements of write-ahead logging.
4. Identify committed and incomplete transactions in a small stable log.
5. Apply new values for redo and old values for undo in a supplied case.
6. State the limits of the supplied recovery simulator.

## Teaching Summary

| Classroom topic | Worked evidence | Evidence to retain |
|---|---|---|
| Failure and available evidence | Transaction error versus crash | Classification with reason |
| Log records | Old and new values | One redo and one undo decision |
| Write-ahead logging | Valid and invalid event order | Corrected WAL timeline |
| Simplified recovery | One committed and one incomplete transaction | Redo/undo table and final state |

## 1. Failure and Storage Assumptions

Different failures require different evidence:

| Failure | Example | Main response |
|---|---|---|
| Transaction error | Invalid input or a failed constraint | Abort that transaction |
| System transaction error | Deadlock victim | Roll back; retry only when safe |
| System crash | Process, OS, or power failure while persistent storage remains readable | Use the stable log for restart recovery |
| Storage loss | Unreadable or lost database blocks | Restore a base copy, then use retained log data |

The classroom recovery example assumes a fail-stop system crash: volatile memory is lost,
but the persistent database and stable log remain readable. This assumption does not
cover every hardware failure.

### Predict Before Checking

Classify each event:

1. The application rolls back because an account identifier does not exist.
2. The DBMS process restarts and the persistent database remains readable.
3. A storage device loses database blocks.
4. The DBMS selects T7 as a deadlock victim.

### Check Criteria

The classifications are transaction error, system crash, storage loss, and system
transaction error. Each answer must state what persistent evidence remains available.

## 2. Log Records

A log records transaction events in order. A basic example is:

```text
<T0 start>
<T0, A, 1000, 950>
<T0, B, 2000, 2050>
<T0 commit>
```

An update record `<Ti, X, old, new>` identifies the transaction and item. The old value
supports undo; the new value supports redo.

### Worked Example

For `<T1, C, 700, 600>`:

- if T1 is incomplete and disk contains 600, undo restores 700;
- if T1 committed and disk still contains 700, redo writes 600.

Recovery applies values recorded in the log. It does not rerun arbitrary application
code, which could read different data or repeat an external side effect.

### Practice

Given `<T5, inventory, 12, 9>`, identify the value used when T5 is incomplete and the
value used when T5 committed but the data page was not written.

### Check Criteria

Undo uses 12; redo uses 9. The explanation must include transaction status.

## 3. Write-Ahead Logging

Log records may first enter a memory buffer. A crash can lose records that have not been
forced to stable storage. Write-ahead logging (WAL) therefore requires two important
orders:

1. Before a modified data page is written to persistent storage, the log information
   needed to undo or redo that update must already be stable.
2. Before the DBMS acknowledges commit, the transaction's earlier log records and commit
   record must be stable.

WAL means log evidence precedes the protected data write or commit acknowledgement. It
does not require every committed data page to be written before commit.

### Worked Timeline

```text
1. Create <T0, A, 1000, 950> in the log buffer
2. Force the update log record
3. Flush the data page containing A
4. Create <T0 commit>
5. Force the log through the commit record
6. Acknowledge commit
```

Flushing the data page before Step 2 violates the data-write ordering rule. Acknowledging
commit before Step 5 violates the commit ordering rule.

### Practice

Correct this sequence:

```text
create update log -> flush data -> create commit log -> acknowledge commit -> force log
```

### Check Criteria

At minimum, force the update log before flushing the data page and force through the
commit record before acknowledging commit.

## 4. Simplified Redo and Undo

Use the supplied log and crash state:

```text
Disk at crash: A=950, B=2000, C=600

<T0 start>
<T0, A, 1000, 950>
<T0, B, 2000, 2050>
<T0 commit>
<T1 start>
<T1, C, 700, 600>
-- crash: no T1 commit or abort
```

T0 is committed, so its updates must be present after recovery. T1 is incomplete, so its
update must not remain.

### Predict Before Running

Create a table with columns for log record, transaction status, redo action, and undo
action. Predict the final values before using the simulator.

### Worked Interpretation

Redo restores the logged history: A becomes 950, B becomes 2050, and C becomes 600.
T1 remains incomplete, so undo restores C to 700. The final database is:

```text
A=950, B=2050, C=700
```

### Additional Practice

Add the stable records:

```text
<T2 start>
<T2, A, 950, 900>
<T2 commit>
```

The final A is 900 because T2 committed. Transaction status comes from the stable log,
not from a value that happens to be present on disk at crash time.

## 5. Executable Activities

First calculate the example by hand, then run:

```powershell
py -3 recovery_simulator.py recovery_case.json
```

Check these observations:

```text
incomplete_after_redo = [T1]
redo: T0.A=950, T0.B=2050, T1.C=600
undo: T1.C=700
final_database = {A:950, B:2050, C:700}
```

Then run the WAL checker:

```powershell
py -3 wal_checker.py wal_scenarios.json
```

Expected results:

- `valid` passes;
- `invalid_data_before_log` violates the data-write order;
- `invalid_commit_before_force` acknowledges commit before the commit record is stable.

The programs use simplified, explicit rules. They do not implement page LSNs, dirty-page
tables, fuzzy checkpoints, logical undo, group commit, partial disk writes, parallel
recovery, or a production DBMS storage manager.

## Extensions: Checkpoints and Backups

A checkpoint can reduce the amount of log examined during restart, but active
transactions may still require earlier records. A checkpoint is not a backup.

A backup provides a base copy after storage loss. Retained post-backup logs may move that
copy forward to a later consistent point. A backup without needed logs may lose later
committed work; logs without a readable base copy may be insufficient to reconstruct the
database.

Detailed checkpoint algorithms, ARIES, point-in-time recovery commands, remote replicas,
and production restore administration are after-class extensions and are not part of the
Exam 3 classroom core.

## Common Errors

1. Treating a system crash and storage loss as the same failure.
2. Assuming that commit means every data page is already persistent.
3. Reversing WAL and writing the data page before its log evidence.
4. Ignoring an incomplete transaction whose update already reached disk.
5. Deciding commit status from crash-time data values rather than the stable log.
6. Treating a checkpoint as a backup.
7. Treating a simulator result as a production recovery test.

## Discussion and Individual Evidence

Discuss this case: an API reports payment success before the commit record becomes stable,
and the server then crashes. Explain which durability promise was broken and which WAL
ordering rule should have prevented it.

Retain:

1. Four failure classifications with reasons.
2. One old-value undo and one new-value redo explanation.
3. A corrected WAL timeline.
4. The hand-calculated redo/undo table and final state.
5. Output from both supplied programs.
6. One explicit limitation that prevents generalizing the model to production DBMSs.

## Chapter Summary

Recovery depends on evidence written before failure. Old values support undo, new values
support redo, and a stable commit record separates committed from incomplete work. WAL
requires recovery information to become stable before the protected data write and
before commit acknowledgement. Checkpoints, backups, and production recovery algorithms
remain extensions.

## After-Class Continuation

Add one committed transaction and one incomplete transaction to `recovery_case.json`.
Predict the final database, then run the simulator. Students interested in operations may
study a server DBMS's backup and point-in-time recovery procedure as an extension.
