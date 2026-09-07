PRAGMA foreign_keys = ON;

-- === PHASE 1: SETUP ===
DROP INDEX IF EXISTS ch14_idx_customer_date;
DROP INDEX IF EXISTS ch14_idx_customer_date_amount;
DROP TABLE IF EXISTS ch14_order_line;

CREATE TABLE ch14_order_line (
    line_id     INTEGER PRIMARY KEY,
    customer_id TEXT NOT NULL,
    ordered_at  TEXT NOT NULL,
    status      TEXT NOT NULL CHECK (status IN ('COMPLETE', 'PENDING', 'CANCELLED')),
    amount      NUMERIC NOT NULL CHECK (amount >= 0)
);

WITH RECURSIVE seq(n) AS (
    VALUES (1)
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 20000
)
INSERT INTO ch14_order_line(line_id, customer_id, ordered_at, status, amount)
SELECT n,
       printf('C%04d', ((n * 37) % 1000) + 1),
       date('2026-01-01', printf('+%d days', (n * 13) % 365)),
       CASE
           WHEN n % 10 < 8 THEN 'COMPLETE'
           WHEN n % 10 = 8 THEN 'PENDING'
           ELSE 'CANCELLED'
       END,
       round(50 + ((n * 17) % 5000) / 10.0, 2)
FROM seq;

ANALYZE;

SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT customer_id) AS customers
FROM ch14_order_line;

EXPLAIN QUERY PLAN
SELECT ordered_at, amount
FROM ch14_order_line
WHERE customer_id = 'C0042'
  AND ordered_at BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY ordered_at;

-- === PHASE 2: COMPOSITE INDEX ===
CREATE INDEX ch14_idx_customer_date
ON ch14_order_line(customer_id, ordered_at);
ANALYZE;

EXPLAIN QUERY PLAN
SELECT ordered_at, amount
FROM ch14_order_line
WHERE customer_id = 'C0042'
  AND ordered_at BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY ordered_at;

SELECT ordered_at, amount
FROM ch14_order_line
WHERE customer_id = 'C0042'
  AND ordered_at BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY ordered_at;

-- The leading customer_id predicate is absent. Record the actual plan; do not assume
-- that every DBMS/version handles this query in the same way.
EXPLAIN QUERY PLAN
SELECT COUNT(*)
FROM ch14_order_line
WHERE ordered_at BETWEEN '2026-06-01' AND '2026-06-30';

-- === PHASE 3: COVERING INDEX ===
CREATE INDEX ch14_idx_customer_date_amount
ON ch14_order_line(customer_id, ordered_at, amount);
ANALYZE;

EXPLAIN QUERY PLAN
SELECT ordered_at, amount
FROM ch14_order_line
WHERE customer_id = 'C0042'
  AND ordered_at BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY ordered_at;

-- COMPLETE matches most rows. A scan can be reasonable when a predicate is not
-- selective and the query needs a large part of the table.
EXPLAIN QUERY PLAN
SELECT line_id, customer_id, ordered_at, status, amount
FROM ch14_order_line
WHERE status = 'COMPLETE';

-- The covering index has the same leading columns as the smaller composite index.
-- Remove the redundant teaching-stage index after comparing the two plans.
DROP INDEX ch14_idx_customer_date;
