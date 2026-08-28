-- Chapter 2 executable examples
-- DBMS used for this file: SQLite
-- Run course_registration_setup.sql first.
-- ORDER BY is used only to make displayed output reproducible. A formal
-- relation has no tuple order.

-- Example 1: display a relation instance.
SELECT student_id, email, student_name, dept_code
FROM student
ORDER BY student_id;

-- Example 2: selection, sigma dept_code = 'IM' (student).
SELECT student_id, email, student_name, dept_code
FROM student
WHERE dept_code = 'IM'
ORDER BY student_id;

-- Example 3: projection, Pi dept_code (student).
-- DISTINCT is required because formal relational-algebra projection removes
-- duplicate tuples, while SQL does not remove them unless requested.
SELECT DISTINCT dept_code
FROM student
ORDER BY dept_code;

-- Example 4: composition, Pi student_name (sigma dept_code = 'IM' (student)).
SELECT student_name
FROM student
WHERE dept_code = 'IM'
ORDER BY student_name;

-- Example 5: Cartesian product of two two-tuple relations.
WITH selected_students AS (
    SELECT student_id
    FROM student
    WHERE student_id IN ('S101', 'S102')
),
selected_courses AS (
    SELECT course_id
    FROM course
    WHERE course_id IN ('DB201', 'FT210')
)
SELECT selected_students.student_id, selected_courses.course_id
FROM selected_students CROSS JOIN selected_courses
ORDER BY selected_students.student_id, selected_courses.course_id;

-- Example 6: theta join between student and enrollment.
SELECT student.student_name, enrollment.course_id, enrollment.term
FROM student
JOIN enrollment ON student.student_id = enrollment.student_id
ORDER BY student.student_id, enrollment.course_id;

-- Example 7a: union of students enrolled in DB201 or FT210.
SELECT student_id FROM enrollment WHERE course_id = 'DB201'
UNION
SELECT student_id FROM enrollment WHERE course_id = 'FT210'
ORDER BY student_id;

-- Example 7b: intersection of students enrolled in both DB201 and FT210.
SELECT student_id FROM enrollment WHERE course_id = 'DB201'
INTERSECT
SELECT student_id FROM enrollment WHERE course_id = 'FT210'
ORDER BY student_id;

-- Example 7c: set difference, DB201 students who are not in FT210.
SELECT student_id FROM enrollment WHERE course_id = 'DB201'
EXCEPT
SELECT student_id FROM enrollment WHERE course_id = 'FT210'
ORDER BY student_id;

-- Example 8: assignment expressed with temporary names in a WITH clause.
WITH db_students AS (
    SELECT student_id FROM enrollment WHERE course_id = 'DB201'
),
fintech_students AS (
    SELECT student_id FROM enrollment WHERE course_id = 'FT210'
)
SELECT student_id FROM db_students
INTERSECT
SELECT student_id FROM fintech_students
ORDER BY student_id;

-- Example 9: rename the student relation twice to compare students in the
-- same department. The ID comparison removes self-pairs and reversed pairs.
SELECT s1.student_name AS student_1, s2.student_name AS student_2, s1.dept_code
FROM student AS s1
CROSS JOIN student AS s2
WHERE s1.dept_code = s2.dept_code
  AND s1.student_id < s2.student_id
ORDER BY s1.student_id, s2.student_id;

-- Example 10a: filter after joining.
SELECT student.student_name, enrollment.course_id
FROM student
JOIN enrollment ON student.student_id = enrollment.student_id
WHERE student.dept_code = 'IM'
ORDER BY student.student_id, enrollment.course_id;

-- Example 10b: filter student first, then join. The result must equal 10a.
WITH im_students AS (
    SELECT student_id, student_name
    FROM student
    WHERE dept_code = 'IM'
)
SELECT im_students.student_name, enrollment.course_id
FROM im_students
JOIN enrollment ON im_students.student_id = enrollment.student_id
ORDER BY im_students.student_id, enrollment.course_id;

-- Student practice: write or predict the result before running each query.
-- P1. Select Finance students and retain all student attributes.
-- P2. Project the distinct building values from department.
-- P3. Return the names of students enrolled in DB201.
-- P4. Find students enrolled in FT210 but not DB201.
-- P5. Explain why removing the join condition in P3 changes the result.
