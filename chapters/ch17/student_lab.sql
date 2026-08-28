PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS transfer_log;
DROP TABLE IF EXISTS account;

CREATE TABLE account (
    account_id TEXT PRIMARY KEY,
    balance INTEGER NOT NULL CHECK (balance >= 0)
);

CREATE TABLE transfer_log (
    transfer_id INTEGER PRIMARY KEY,
    from_account TEXT NOT NULL REFERENCES account(account_id),
    to_account TEXT NOT NULL REFERENCES account(account_id),
    amount INTEGER NOT NULL CHECK (amount > 0),
    status TEXT NOT NULL CHECK (status IN ('COMMITTED'))
);

INSERT INTO account(account_id, balance)
VALUES ('A', 1000), ('B', 2000);

.print 'PREDICT 1: What balances will remain after ROLLBACK?'
BEGIN;
UPDATE account SET balance = balance - 50 WHERE account_id = 'A';
SELECT 'inside_before_rollback' AS phase, account_id, balance
FROM account
ORDER BY account_id;
ROLLBACK;
SELECT 'after_rollback' AS phase, account_id, balance
FROM account
ORDER BY account_id;

.print 'PREDICT 2: Will the total change after the committed transfer?'
BEGIN IMMEDIATE;
UPDATE account
SET balance = balance - 50
WHERE account_id = 'A' AND balance >= 50;
UPDATE account
SET balance = balance + 50
WHERE account_id = 'B';
INSERT INTO transfer_log(from_account, to_account, amount, status)
VALUES ('A', 'B', 50, 'COMMITTED');
COMMIT;

SELECT 'after_commit' AS phase, account_id, balance
FROM account
ORDER BY account_id;
SELECT 'total_after_commit' AS check_name, SUM(balance) AS total_balance
FROM account;
SELECT 'committed_log_count' AS check_name, COUNT(*) AS row_count
FROM transfer_log;

.print 'PRACTICE: Replace 5000 with a valid amount, then write one transaction that updates both accounts and the log.'
.print 'CHECK: A and B must remain nonnegative; the total must remain 3000; exactly one new COMMITTED log row must appear.'

-- Practice starting point; remove the comment markers only after adding complete
-- insufficient-funds handling and an expected-result check.
-- BEGIN;
-- UPDATE account SET balance = balance - 5000
-- WHERE account_id = 'A' AND balance >= 5000;
-- ROLLBACK;
