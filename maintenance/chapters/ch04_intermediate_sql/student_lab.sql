-- Chapter 4: Intermediate SQL
-- Verified with SQLite 3.45.3. Run Chapter 2 course_registration_setup.sql first.
-- Predict the attributes, row count, NULLs, and database changes before each block.

PRAGMA foreign_keys = ON;

-- Example 1: explicit inner joins. Six enrollment rows should be returned.
SELECT s.student_id, s.student_name, c.course_id, c.title, e.grade
FROM student AS s
JOIN enrollment AS e ON e.student_id = s.student_id
JOIN course AS c ON c.course_id = e.course_id
ORDER BY s.student_id, c.course_id;

-- Example 2: NATURAL JOIN silently uses every shared column name. The intermediate
-- result shares both course_id and dept_code with course, so the cross-department
-- S101/FT210 enrollment disappears. The explicit query above returns six rows;
-- this query returns five.
SELECT student_id, student_name, course_id, title
FROM student
NATURAL JOIN enrollment
NATURAL JOIN course
ORDER BY student_id, course_id;

-- Example 3: USING names the intended common column explicitly.
SELECT c.course_id, c.title, d.dept_name
FROM course AS c
JOIN department AS d USING (dept_code)
ORDER BY c.course_id;

-- Example 4: left outer join retains a course that has no enrollment.
SAVEPOINT unmatched_course_demo;

INSERT INTO course (course_id, title, dept_code, credits)
VALUES ('IS250', 'Information Security', 'IM', 3);

SELECT c.course_id, c.title, COUNT(e.student_id) AS enrollment_count
FROM course AS c
LEFT OUTER JOIN enrollment AS e ON e.course_id = c.course_id
GROUP BY c.course_id, c.title
ORDER BY c.course_id;

-- Example 5: a condition in ON preserves every course; the same condition in WHERE
-- removes courses without a matching A/A- enrollment.
SELECT c.course_id, e.student_id, e.grade
FROM course AS c
LEFT OUTER JOIN enrollment AS e
  ON e.course_id = c.course_id
 AND e.grade IN ('A', 'A-')
ORDER BY c.course_id, e.student_id;

SELECT c.course_id, e.student_id, e.grade
FROM course AS c
LEFT OUTER JOIN enrollment AS e ON e.course_id = c.course_id
WHERE e.grade IN ('A', 'A-')
ORDER BY c.course_id, e.student_id;

ROLLBACK TO unmatched_course_demo;
RELEASE unmatched_course_demo;

-- Example 6: right and full outer joins. SQLite 3.39 or later is required.
DROP TABLE IF EXISTS temp.planned_enrollment;
DROP TABLE IF EXISTS temp.planned_student;

CREATE TEMP TABLE planned_student (
    student_id TEXT PRIMARY KEY
);

CREATE TEMP TABLE planned_enrollment (
    student_id TEXT NOT NULL,
    course_id TEXT NOT NULL
);

INSERT INTO planned_student VALUES ('S101'), ('S105');
INSERT INTO planned_enrollment VALUES ('S101', 'DB201'), ('S999', 'AI999');

SELECT ps.student_id AS known_student,
       pe.student_id AS planned_student,
       pe.course_id
FROM planned_student AS ps
RIGHT OUTER JOIN planned_enrollment AS pe
  ON pe.student_id = ps.student_id
ORDER BY pe.student_id;

SELECT ps.student_id AS known_student,
       pe.student_id AS planned_student,
       pe.course_id
FROM planned_student AS ps
FULL OUTER JOIN planned_enrollment AS pe
  ON pe.student_id = ps.student_id
ORDER BY COALESCE(ps.student_id, pe.student_id);

-- Example 7: a view stores a query definition, not this query's current rows.
DROP VIEW IF EXISTS course_enrollment_summary;

CREATE VIEW course_enrollment_summary AS
SELECT c.course_id,
       c.title,
       COUNT(e.student_id) AS enrollment_count
FROM course AS c
LEFT OUTER JOIN enrollment AS e ON e.course_id = c.course_id
GROUP BY c.course_id, c.title;

SELECT course_id, title, enrollment_count
FROM course_enrollment_summary
ORDER BY course_id;

SAVEPOINT view_change_demo;
INSERT INTO enrollment (student_id, course_id, term, grade)
VALUES ('S102', 'DB201', '115-1', NULL);

SELECT course_id, enrollment_count
FROM course_enrollment_summary
WHERE course_id = 'DB201';

ROLLBACK TO view_change_demo;
RELEASE view_change_demo;

SELECT course_id, enrollment_count
FROM course_enrollment_summary
WHERE course_id = 'DB201';

-- Do not uncomment in a shared database. SQLite views are read-only unless an
-- INSTEAD OF trigger is supplied; the verifier confirms that this update fails.
-- UPDATE course_enrollment_summary
-- SET enrollment_count = 99
-- WHERE course_id = 'DB201';

-- Example 8: a multi-statement course swap is one transaction-sized task.
-- SAVEPOINT lets the lab show and then undo the complete unit of work.
SAVEPOINT course_swap;

DELETE FROM enrollment
WHERE student_id = 'S101'
  AND course_id = 'FT210'
  AND term = '115-1';

INSERT INTO enrollment (student_id, course_id, term, grade)
VALUES ('S101', 'ML230', '115-1', NULL);

SELECT student_id, course_id, term, grade
FROM enrollment
WHERE student_id = 'S101'
ORDER BY course_id;

ROLLBACK TO course_swap;
RELEASE course_swap;

SELECT student_id, course_id, term, grade
FROM enrollment
WHERE student_id = 'S101'
ORDER BY course_id;

-- Example 9: NOT NULL, UNIQUE, CHECK, foreign keys, a default, and a
-- deliberate ON DELETE CASCADE rule.
DROP TABLE IF EXISTS waitlist_entry;

CREATE TABLE waitlist_entry (
    request_id INTEGER PRIMARY KEY,
    student_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    term TEXT NOT NULL DEFAULT '115-1',
    priority INTEGER NOT NULL CHECK (priority BETWEEN 1 AND 5),
    UNIQUE (student_id, course_id, term),
    FOREIGN KEY (student_id) REFERENCES student (student_id)
        ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course (course_id)
);

INSERT INTO waitlist_entry (request_id, student_id, course_id, priority)
VALUES (1, 'S104', 'ML230', 2);

SELECT request_id, student_id, course_id, term, priority
FROM waitlist_entry;

-- Invalid examples are comments so the complete script continues. The verifier
-- executes each one independently and confirms rejection.
-- Duplicate request: same student_id, course_id, and term.
-- INSERT INTO waitlist_entry VALUES (2, 'S104', 'ML230', '115-1', 3);
-- Invalid range: priority 8 violates CHECK.
-- INSERT INTO waitlist_entry VALUES (3, 'S103', 'FT210', '115-1', 8);
-- Missing parent: S999 violates the student foreign key.
-- INSERT INTO waitlist_entry VALUES (4, 'S999', 'FT210', '115-1', 3);

-- Example 10: the chosen cascade deletes dependent waitlist rows. The whole
-- demonstration is rolled back, so S105 is not left in the base data.
SAVEPOINT cascade_demo;

INSERT INTO student (student_id, email, student_name, dept_code)
VALUES ('S105', 'noah.lee@example.edu', 'Noah Lee', 'IM');

INSERT INTO waitlist_entry
    (request_id, student_id, course_id, term, priority)
VALUES (5, 'S105', 'FT210', '115-1', 3);

DELETE FROM student WHERE student_id = 'S105';

SELECT COUNT(*) AS remaining_s105_waitlist_rows
FROM waitlist_entry
WHERE student_id = 'S105';

ROLLBACK TO cascade_demo;
RELEASE cascade_demo;

-- Example 11: CHECK alone does not reject NULL because UNKNOWN is not FALSE.
DROP TABLE IF EXISTS temp.check_without_not_null;
CREATE TEMP TABLE check_without_not_null (
    value INTEGER CHECK (value > 0)
);
INSERT INTO check_without_not_null VALUES (NULL);
SELECT value IS NULL AS null_was_accepted
FROM check_without_not_null;

-- Student practice. Save predictions and actual results.
-- P1. Use explicit JOIN ... ON to list every enrollment with student email and
--     department name of the course. State why each join condition is needed.
-- P2. Rewrite Example 3 using JOIN ... ON without changing its result.
-- P3. Use a left outer join to list every student and the number of courses taken.
-- P4. Predict which course rows disappear when the A/A- condition moves from ON
--     to WHERE, then verify.
-- P5. Create a view named im_course that exposes only course_id, title, and credits
--     for IM courses; query it for three-credit courses.
-- P6. Inside a savepoint, perform a different valid two-statement course swap and
--     prove that ROLLBACK restores the starting rows.
-- P7. Design course_feedback so rating is 1-5, one row exists per enrollment, and
--     feedback cannot refer to a nonexistent enrollment.
