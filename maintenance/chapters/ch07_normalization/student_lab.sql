PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS ch07_enrollment;
DROP TABLE IF EXISTS ch07_course;
DROP TABLE IF EXISTS ch07_student;
DROP TABLE IF EXISTS ch07_department;
DROP TABLE IF EXISTS ch07_course_enrollment_record;
DROP TABLE IF EXISTS ch07_employee_details;
DROP TABLE IF EXISTS ch07_employee_identity;

-- Part A: A flattened relation that stores several kinds of facts.
CREATE TABLE ch07_course_enrollment_record (
    student_id   TEXT NOT NULL,
    student_name TEXT NOT NULL,
    dept_code    TEXT NOT NULL,
    dept_name    TEXT NOT NULL,
    course_id    TEXT NOT NULL,
    course_title TEXT NOT NULL,
    credits      INTEGER NOT NULL,
    grade        TEXT,
    PRIMARY KEY (student_id, course_id)
);

INSERT INTO ch07_course_enrollment_record VALUES
    ('S101', 'An Chen',  'IM',  'Information Management', 'DB201', 'Database Management', 3, 'A'),
    ('S101', 'An Chen',  'IM',  'Information Management', 'FT210', 'Financial Technology', 3, 'B+'),
    ('S102', 'Bea Lin',  'FIN', 'Finance',                'FT210', 'Financial Technology', 3, 'A-'),
    ('S103', 'Kai Wu',   'IM',  'Information Management', 'DB201', 'Database Management', 3, 'B');

SELECT dept_code, dept_name, COUNT(*) AS repeated_rows
FROM ch07_course_enrollment_record
GROUP BY dept_code, dept_name
ORDER BY dept_code;

-- Demonstrate an update anomaly without retaining invalid data.
SAVEPOINT inconsistent_department_name;
UPDATE ch07_course_enrollment_record
SET dept_name = 'Information Systems'
WHERE student_id = 'S101' AND course_id = 'DB201';

SELECT dept_code, COUNT(DISTINCT dept_name) AS distinct_names
FROM ch07_course_enrollment_record
GROUP BY dept_code
ORDER BY dept_code;

ROLLBACK TO inconsistent_department_name;
RELEASE inconsistent_department_name;

-- Part B: Store each kind of fact once.
CREATE TABLE ch07_department (
    dept_code TEXT PRIMARY KEY,
    dept_name TEXT NOT NULL UNIQUE
);

CREATE TABLE ch07_student (
    student_id   TEXT PRIMARY KEY,
    student_name TEXT NOT NULL,
    dept_code    TEXT NOT NULL,
    FOREIGN KEY (dept_code) REFERENCES ch07_department(dept_code)
);

CREATE TABLE ch07_course (
    course_id    TEXT PRIMARY KEY,
    course_title TEXT NOT NULL,
    credits      INTEGER NOT NULL CHECK (credits BETWEEN 1 AND 6)
);

CREATE TABLE ch07_enrollment (
    student_id TEXT NOT NULL,
    course_id  TEXT NOT NULL,
    grade      TEXT CHECK (grade IS NULL OR grade IN
        ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F')),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES ch07_student(student_id),
    FOREIGN KEY (course_id) REFERENCES ch07_course(course_id)
);

INSERT INTO ch07_department VALUES
    ('IM', 'Information Management'),
    ('FIN', 'Finance');

INSERT INTO ch07_student VALUES
    ('S101', 'An Chen', 'IM'),
    ('S102', 'Bea Lin', 'FIN'),
    ('S103', 'Kai Wu', 'IM');

INSERT INTO ch07_course VALUES
    ('DB201', 'Database Management', 3),
    ('FT210', 'Financial Technology', 3),
    ('AI301', 'Artificial Intelligence', 3);

INSERT INTO ch07_enrollment VALUES
    ('S101', 'DB201', 'A'),
    ('S101', 'FT210', 'B+'),
    ('S102', 'FT210', 'A-'),
    ('S103', 'DB201', 'B');

-- AI301 can exist before any student enrolls.
SELECT c.course_id, c.course_title, COUNT(e.student_id) AS enrollment_count
FROM ch07_course AS c
LEFT JOIN ch07_enrollment AS e ON e.course_id = c.course_id
GROUP BY c.course_id, c.course_title
ORDER BY c.course_id;

-- Part C: Reconstruct the original four rows and compare in both directions.
WITH reconstructed AS (
    SELECT s.student_id, s.student_name, d.dept_code, d.dept_name,
           c.course_id, c.course_title, c.credits, e.grade
    FROM ch07_enrollment AS e
    JOIN ch07_student AS s ON s.student_id = e.student_id
    JOIN ch07_department AS d ON d.dept_code = s.dept_code
    JOIN ch07_course AS c ON c.course_id = e.course_id
)
SELECT COUNT(*) AS original_minus_reconstructed
FROM (
    SELECT * FROM ch07_course_enrollment_record
    EXCEPT
    SELECT * FROM reconstructed
);

WITH reconstructed AS (
    SELECT s.student_id, s.student_name, d.dept_code, d.dept_name,
           c.course_id, c.course_title, c.credits, e.grade
    FROM ch07_enrollment AS e
    JOIN ch07_student AS s ON s.student_id = e.student_id
    JOIN ch07_department AS d ON d.dept_code = s.dept_code
    JOIN ch07_course AS c ON c.course_id = e.course_id
)
SELECT COUNT(*) AS reconstructed_minus_original
FROM (
    SELECT * FROM reconstructed
    EXCEPT
    SELECT * FROM ch07_course_enrollment_record
);

-- Part D: A deliberately lossy decomposition using a non-key common attribute.
CREATE TABLE ch07_employee_identity (
    employee_id TEXT PRIMARY KEY,
    name        TEXT NOT NULL
);

CREATE TABLE ch07_employee_details (
    name   TEXT NOT NULL,
    city   TEXT NOT NULL,
    salary INTEGER NOT NULL,
    PRIMARY KEY (name, city)
);

INSERT INTO ch07_employee_identity VALUES
    ('E1', 'Kim'),
    ('E2', 'Kim');

INSERT INTO ch07_employee_details VALUES
    ('Kim', 'Taipei', 60000),
    ('Kim', 'Tainan', 62000);

SELECT i.employee_id, i.name, d.city, d.salary
FROM ch07_employee_identity AS i
JOIN ch07_employee_details AS d USING (name)
ORDER BY i.employee_id, d.city;
