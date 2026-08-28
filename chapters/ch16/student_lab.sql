PRAGMA foreign_keys = ON;
PRAGMA automatic_index = OFF;

DROP INDEX IF EXISTS ch16_idx_student_dept;
DROP INDEX IF EXISTS ch16_idx_course_credits;
DROP INDEX IF EXISTS ch16_idx_enrollment_course;
DROP INDEX IF EXISTS ch16_idx_event_type;
DROP TABLE IF EXISTS ch16_enrollment;
DROP TABLE IF EXISTS ch16_student;
DROP TABLE IF EXISTS ch16_course;
DROP TABLE IF EXISTS ch16_department;
DROP TABLE IF EXISTS ch16_event;

CREATE TABLE ch16_department (
    dept_id   INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL UNIQUE
);

CREATE TABLE ch16_student (
    student_id INTEGER PRIMARY KEY,
    dept_id    INTEGER NOT NULL,
    name       TEXT NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES ch16_department(dept_id)
);

CREATE TABLE ch16_course (
    course_id INTEGER PRIMARY KEY,
    title     TEXT NOT NULL,
    credits   INTEGER NOT NULL CHECK (credits BETWEEN 1 AND 5)
);

CREATE TABLE ch16_enrollment (
    student_id INTEGER NOT NULL,
    course_id  INTEGER NOT NULL,
    grade      TEXT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES ch16_student(student_id),
    FOREIGN KEY (course_id) REFERENCES ch16_course(course_id)
);

WITH RECURSIVE seq(n) AS (
    VALUES (1)
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 101
)
INSERT INTO ch16_department(dept_id, dept_name)
SELECT n, printf('Department %03d', n)
FROM seq;

WITH RECURSIVE seq(n) AS (
    VALUES (1)
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 10000
)
INSERT INTO ch16_student(student_id, dept_id, name)
SELECT n, ((n - 1) % 100) + 1, printf('Student %05d', n)
FROM seq;

WITH RECURSIVE seq(n) AS (
    VALUES (1)
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 500
)
INSERT INTO ch16_course(course_id, title, credits)
SELECT n, printf('Course %03d', n), ((n - 1) % 5) + 1
FROM seq;

WITH RECURSIVE students(n) AS (
    VALUES (1)
    UNION ALL
    SELECT n + 1 FROM students WHERE n < 10000
), five(k) AS (VALUES (1), (2), (3), (4), (5))
INSERT INTO ch16_enrollment(student_id, course_id, grade)
SELECT n,
       ((n * 17 + k * 97) % 500) + 1,
       CASE k WHEN 1 THEN 'A' WHEN 2 THEN 'B+' WHEN 3 THEN 'B'
              WHEN 4 THEN 'A-' ELSE 'C+' END
FROM students CROSS JOIN five;

CREATE INDEX ch16_idx_student_dept ON ch16_student(dept_id);
CREATE INDEX ch16_idx_course_credits ON ch16_course(credits);
CREATE INDEX ch16_idx_enrollment_course ON ch16_enrollment(course_id);

-- A deliberately skewed column for statistics reasoning.
CREATE TABLE ch16_event (
    event_id   INTEGER PRIMARY KEY,
    event_type TEXT NOT NULL,
    amount     NUMERIC NOT NULL
);

WITH RECURSIVE seq(n) AS (
    VALUES (1)
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 10000
)
INSERT INTO ch16_event(event_id, event_type, amount)
SELECT n,
       CASE WHEN n <= 9900 THEN 'COMMON' ELSE 'RARE' END,
       round(10 + (n % 1000) / 10.0, 2)
FROM seq;

CREATE INDEX ch16_idx_event_type ON ch16_event(event_type);
ANALYZE;

SELECT COUNT(*) AS students FROM ch16_student;
SELECT COUNT(*) AS enrollments FROM ch16_enrollment;

-- === BASE QUERY ===
EXPLAIN QUERY PLAN
SELECT s.student_id, c.course_id
FROM ch16_student AS s
JOIN ch16_enrollment AS e ON e.student_id = s.student_id
JOIN ch16_course AS c ON c.course_id = e.course_id
WHERE s.dept_id = 42 AND c.credits = 5;

-- === PUSHDOWN QUERY ===
EXPLAIN QUERY PLAN
SELECT s.student_id, c.course_id
FROM (SELECT student_id FROM ch16_student WHERE dept_id = 42) AS s
JOIN ch16_enrollment AS e ON e.student_id = s.student_id
JOIN (SELECT course_id FROM ch16_course WHERE credits = 5) AS c
  ON c.course_id = e.course_id;

-- Compare equivalent results in both directions.
WITH base AS (
    SELECT s.student_id, c.course_id
    FROM ch16_student AS s
    JOIN ch16_enrollment AS e ON e.student_id = s.student_id
    JOIN ch16_course AS c ON c.course_id = e.course_id
    WHERE s.dept_id = 42 AND c.credits = 5
), pushed AS (
    SELECT s.student_id, c.course_id
    FROM (SELECT student_id FROM ch16_student WHERE dept_id = 42) AS s
    JOIN ch16_enrollment AS e ON e.student_id = s.student_id
    JOIN (SELECT course_id FROM ch16_course WHERE credits = 5) AS c
      ON c.course_id = e.course_id
)
SELECT (SELECT COUNT(*) FROM base) AS base_rows,
       (SELECT COUNT(*) FROM pushed) AS pushed_rows,
       (SELECT COUNT(*) FROM (SELECT * FROM base EXCEPT SELECT * FROM pushed))
         AS base_minus_pushed,
       (SELECT COUNT(*) FROM (SELECT * FROM pushed EXCEPT SELECT * FROM base))
         AS pushed_minus_base;

-- === OUTER JOIN COUNTEREXAMPLE ===
-- WHERE rejects the NULL-extended row for Department 101.
SELECT d.dept_id, s.student_id
FROM ch16_department AS d
LEFT JOIN ch16_student AS s ON s.dept_id = d.dept_id
WHERE s.student_id < 3
ORDER BY d.dept_id, s.student_id;

-- ON retains Department 101 with a NULL student_id.
SELECT d.dept_id, s.student_id
FROM ch16_department AS d
LEFT JOIN ch16_student AS s
  ON s.dept_id = d.dept_id AND s.student_id < 3
WHERE d.dept_id IN (1, 2, 101)
ORDER BY d.dept_id, s.student_id;

-- === STATISTICS AND SKEW ===
SELECT tbl, idx, stat
FROM sqlite_stat1
WHERE tbl IN ('ch16_student', 'ch16_course', 'ch16_enrollment', 'ch16_event')
ORDER BY tbl, idx;

SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT event_type) AS distinct_types,
       COUNT(*) / COUNT(DISTINCT event_type) AS uniform_estimate_per_type
FROM ch16_event;

SELECT event_type, COUNT(*) AS actual_rows,
       round(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ch16_event), 1)
         AS actual_percent
FROM ch16_event
GROUP BY event_type
ORDER BY event_type;

EXPLAIN QUERY PLAN
SELECT event_id, event_type, amount
FROM ch16_event
WHERE event_type = 'RARE';

EXPLAIN QUERY PLAN
SELECT event_id, event_type, amount
FROM ch16_event
WHERE event_type = 'COMMON';
