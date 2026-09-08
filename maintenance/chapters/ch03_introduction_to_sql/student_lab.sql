-- Chapter 3 executable examples
-- DBMS used for this file: SQLite 3
-- First run ../ch02_relational_model/course_registration_setup.sql.
-- Run this file from top to bottom. Modification examples use savepoints and
-- restore the base data before the script ends.

-- Example 1: DDL with keys and constraints.
DROP TABLE IF EXISTS study_group_member;
DROP TABLE IF EXISTS study_group;

CREATE TABLE study_group (
    group_id TEXT NOT NULL PRIMARY KEY,
    group_name TEXT NOT NULL,
    course_id TEXT NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity BETWEEN 2 AND 8),
    FOREIGN KEY (course_id) REFERENCES course (course_id)
);

CREATE TABLE study_group_member (
    group_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    member_role TEXT NOT NULL,
    PRIMARY KEY (group_id, student_id),
    FOREIGN KEY (group_id) REFERENCES study_group (group_id),
    FOREIGN KEY (student_id) REFERENCES student (student_id)
);

INSERT INTO study_group VALUES ('G01', 'SQL Practice', 'DB201', 4);
INSERT INTO study_group_member VALUES ('G01', 'S101', 'coordinator');
INSERT INTO study_group_member VALUES ('G01', 'S103', 'member');

SELECT group_id, group_name, course_id, capacity
FROM study_group;

-- Example 2: SELECT, FROM, aliases, and deterministic display order.
SELECT student_id, student_name AS name, dept_code
FROM student
ORDER BY student_id;

-- Example 3: SQL retains duplicates unless DISTINCT is requested.
SELECT dept_code
FROM student
ORDER BY dept_code;

SELECT DISTINCT dept_code
FROM student
ORDER BY dept_code;

-- Example 4: expressions do not update stored data.
SELECT course_id, title, credits, credits * 18 AS semester_hours
FROM course
ORDER BY course_id;

-- Example 5: WHERE with comparisons and logical connectives.
SELECT student_id, student_name
FROM student
WHERE dept_code = 'IM' AND student_id <> 'S101'
ORDER BY student_id;

-- Example 6: multiple relations and a matching predicate.
-- Explicit JOIN syntax is introduced in Chapter 4. This Chapter 3 form is used
-- to connect FROM, WHERE, and relational-algebra product/selection concepts.
SELECT s.student_name, e.course_id, e.grade
FROM student AS s, enrollment AS e
WHERE s.student_id = e.student_id
ORDER BY s.student_id, e.course_id;

-- Example 7: LIKE, BETWEEN, and ORDER BY.
SELECT course_id, title, credits
FROM course
WHERE title LIKE '%Technology%' OR credits BETWEEN 1 AND 2
ORDER BY credits DESC, course_id ASC;

-- Example 8a: UNION removes duplicates.
SELECT student_id FROM enrollment WHERE course_id = 'DB201'
UNION
SELECT student_id FROM enrollment WHERE course_id = 'FT210'
ORDER BY student_id;

-- Example 8b: UNION ALL retains copies from both inputs.
SELECT student_id FROM enrollment WHERE course_id = 'DB201'
UNION ALL
SELECT student_id FROM enrollment WHERE course_id = 'FT210'
ORDER BY student_id;

-- Example 8c: INTERSECT and EXCEPT.
SELECT student_id FROM enrollment WHERE course_id = 'DB201'
INTERSECT
SELECT student_id FROM enrollment WHERE course_id = 'FT210'
ORDER BY student_id;

SELECT student_id FROM enrollment WHERE course_id = 'DB201'
EXCEPT
SELECT student_id FROM enrollment WHERE course_id = 'FT210'
ORDER BY student_id;

-- Example 9: NULL, three-valued logic, and aggregate handling.
SAVEPOINT null_demo;
UPDATE enrollment
SET grade = NULL
WHERE student_id = 'S102' AND course_id = 'FT210' AND term = '115-1';

SELECT student_id, course_id
FROM enrollment
WHERE grade IS NULL
ORDER BY student_id, course_id;

-- This intentionally returns no rows: grade = NULL is unknown, not true.
SELECT student_id, course_id
FROM enrollment
WHERE grade = NULL;

SELECT COUNT(*) AS enrollment_rows,
       COUNT(grade) AS known_grades
FROM enrollment;

ROLLBACK TO null_demo;
RELEASE null_demo;

-- Example 10: aggregate functions.
SELECT COUNT(*) AS course_count,
       MIN(credits) AS min_credits,
       MAX(credits) AS max_credits,
       SUM(credits) AS total_credits,
       AVG(credits) AS avg_credits
FROM course;

-- Example 11: GROUP BY creates one result row per group.
SELECT dept_code, COUNT(*) AS course_count, AVG(credits) AS avg_credits
FROM course
GROUP BY dept_code
ORDER BY dept_code;

-- Example 12: WHERE filters rows before grouping; HAVING filters groups.
SELECT dept_code, COUNT(*) AS course_count
FROM course
WHERE credits >= 3
GROUP BY dept_code
HAVING COUNT(*) >= 2
ORDER BY dept_code;

-- Example 13: IN subquery.
SELECT student_id, student_name
FROM student
WHERE student_id IN (
    SELECT student_id
    FROM enrollment
    WHERE course_id = 'DB201'
)
ORDER BY student_id;

-- Example 14: correlated EXISTS subquery.
SELECT s.student_id, s.student_name
FROM student AS s
WHERE EXISTS (
    SELECT 1
    FROM enrollment AS e
    WHERE e.student_id = s.student_id
      AND e.grade IN ('A', 'A-')
)
ORDER BY s.student_id;

-- Example 15: NOT IN with a NULL in the subquery returns no rows.
WITH blocked(student_id) AS (
    VALUES ('S104'), (NULL)
)
SELECT student_id
FROM student
WHERE student_id NOT IN (SELECT student_id FROM blocked)
ORDER BY student_id;

-- Example 16: NOT EXISTS expresses the intended exclusion despite the NULL.
WITH blocked(student_id) AS (
    VALUES ('S104'), (NULL)
)
SELECT s.student_id
FROM student AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM blocked AS b
    WHERE b.student_id = s.student_id
)
ORDER BY s.student_id;

-- Example 17: subquery in FROM.
SELECT course_id, enrollment_count
FROM (
    SELECT course_id, COUNT(*) AS enrollment_count
    FROM enrollment
    GROUP BY course_id
) AS counts
WHERE enrollment_count >= 2
ORDER BY course_id;

-- Example 18: the same intermediate result expressed with WITH.
WITH counts AS (
    SELECT course_id, COUNT(*) AS enrollment_count
    FROM enrollment
    GROUP BY course_id
)
SELECT course_id, enrollment_count
FROM counts
WHERE enrollment_count >= 2
ORDER BY course_id;

-- Example 19: scalar correlated subquery.
SELECT c.course_id,
       c.title,
       (
           SELECT COUNT(*)
           FROM enrollment AS e
           WHERE e.course_id = c.course_id
       ) AS enrollment_count
FROM course AS c
ORDER BY c.course_id;

-- Example 20: INSERT, UPDATE, and DELETE inside a reversible demonstration.
SAVEPOINT dml_demo;

INSERT INTO student (student_id, email, student_name, dept_code)
VALUES ('S105', 'noah.lee@example.edu', 'Noah Lee', 'IM');

UPDATE student
SET dept_code = 'FIN'
WHERE student_id = 'S105';

SELECT student_id, student_name, dept_code
FROM student
WHERE student_id = 'S105';

DELETE FROM student
WHERE student_id = 'S105';

SELECT COUNT(*) AS remaining_s105
FROM student
WHERE student_id = 'S105';

ROLLBACK TO dml_demo;
RELEASE dml_demo;

-- Student practice. Predict before executing your own statements.
-- P1. Return course_id and title for all three-credit courses.
-- P2. Return distinct department codes for students, in descending order.
-- P3. Count enrollments for each course and retain groups with at least two.
-- P4. Use EXISTS to find students enrolled in FT210.
-- P5. Inside a savepoint, insert a valid course and then restore the database.
-- P6. Explain why WHERE grade <> 'F' does not retain a NULL grade.
