PRAGMA foreign_keys = ON;
PRAGMA automatic_index = OFF;

-- === PHASE 1: SETUP WITHOUT SECONDARY INDEXES ===
DROP INDEX IF EXISTS ch15_idx_course_title;
DROP INDEX IF EXISTS ch15_idx_department_name;
DROP INDEX IF EXISTS ch15_idx_course_dept;
DROP TABLE IF EXISTS ch15_course;
DROP TABLE IF EXISTS ch15_department;

CREATE TABLE ch15_department (
    dept_id   INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL
);

CREATE TABLE ch15_course (
    course_id TEXT PRIMARY KEY,
    title     TEXT NOT NULL,
    dept_id   INTEGER NOT NULL,
    credits   INTEGER NOT NULL CHECK (credits BETWEEN 1 AND 5),
    FOREIGN KEY (dept_id) REFERENCES ch15_department(dept_id)
);

WITH RECURSIVE seq(n) AS (
    VALUES (1)
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 100
)
INSERT INTO ch15_department(dept_id, dept_name)
SELECT n, printf('Department %03d', n)
FROM seq;

WITH RECURSIVE seq(n) AS (
    VALUES (1)
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < 5000
)
INSERT INTO ch15_course(course_id, title, dept_id, credits)
SELECT printf('C%05d', n),
       printf('Course %05d', n),
       ((n - 1) % 100) + 1,
       ((n - 1) % 5) + 1
FROM seq;

ANALYZE;

SELECT COUNT(*) AS departments FROM ch15_department;
SELECT COUNT(*) AS courses FROM ch15_course;
SELECT COUNT(*) AS credit_three_courses
FROM ch15_course WHERE credits = 3;

EXPLAIN QUERY PLAN
SELECT course_id, title
FROM ch15_course
WHERE title = 'Course 04999';

EXPLAIN QUERY PLAN
SELECT c.course_id, c.title
FROM ch15_department AS d
JOIN ch15_course AS c ON c.dept_id = d.dept_id
WHERE d.dept_name = 'Department 042';

-- === PHASE 2: ADD SELECTION AND JOIN ACCESS PATHS ===
CREATE INDEX ch15_idx_course_title
ON ch15_course(title);

CREATE UNIQUE INDEX ch15_idx_department_name
ON ch15_department(dept_name);

CREATE INDEX ch15_idx_course_dept
ON ch15_course(dept_id);

ANALYZE;

EXPLAIN QUERY PLAN
SELECT course_id, title
FROM ch15_course
WHERE title = 'Course 04999';

SELECT course_id, title
FROM ch15_course
WHERE title = 'Course 04999';

EXPLAIN QUERY PLAN
SELECT c.course_id, c.title
FROM ch15_department AS d
JOIN ch15_course AS c ON c.dept_id = d.dept_id
WHERE d.dept_name = 'Department 042';

SELECT COUNT(*) AS department_042_courses
FROM ch15_department AS d
JOIN ch15_course AS c ON c.dept_id = d.dept_id
WHERE d.dept_name = 'Department 042';

-- This query needs title order. Record whether the plan reports temporary sorting.
EXPLAIN QUERY PLAN
SELECT c.course_id, c.title
FROM ch15_department AS d
JOIN ch15_course AS c ON c.dept_id = d.dept_id
WHERE d.dept_name = 'Department 042'
ORDER BY c.title;
