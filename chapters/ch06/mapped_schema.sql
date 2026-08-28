-- Chapter 6: relational schema mapped from the E-R design
-- Verified with SQLite 3.45.3.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS course_prerequisite;
DROP TABLE IF EXISTS enrollment;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS student_phone;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS department;

-- Strong entity.
CREATE TABLE department (
    dept_code TEXT PRIMARY KEY,
    dept_name TEXT NOT NULL UNIQUE,
    building TEXT NOT NULL
);

-- Strong entity plus the merged total many-to-one majors_in relationship.
-- Composite name is flattened; derived completed_credits is not stored.
CREATE TABLE student (
    student_id TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dept_code TEXT NOT NULL,
    FOREIGN KEY (dept_code) REFERENCES department (dept_code)
);

-- Separate relation for the multivalued phone_number attribute.
CREATE TABLE student_phone (
    student_id TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    PRIMARY KEY (student_id, phone_number),
    FOREIGN KEY (student_id) REFERENCES student (student_id)
        ON DELETE CASCADE
);

-- Strong entity plus the merged total many-to-one offers relationship.
CREATE TABLE course (
    course_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    credits INTEGER NOT NULL CHECK (credits BETWEEN 1 AND 6),
    dept_code TEXT NOT NULL,
    FOREIGN KEY (dept_code) REFERENCES department (dept_code)
);

-- Weak entity. Owner key plus discriminator form the primary key.
CREATE TABLE section (
    course_id TEXT NOT NULL,
    term TEXT NOT NULL,
    section_no INTEGER NOT NULL CHECK (section_no > 0),
    room TEXT,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    PRIMARY KEY (course_id, term, section_no),
    FOREIGN KEY (course_id) REFERENCES course (course_id)
        ON DELETE CASCADE
);

-- Many-to-many registers relationship with descriptive attribute grade.
CREATE TABLE enrollment (
    student_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    term TEXT NOT NULL,
    section_no INTEGER NOT NULL,
    grade TEXT CHECK (
        grade IS NULL OR grade IN ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'F')
    ),
    PRIMARY KEY (student_id, course_id, term, section_no),
    FOREIGN KEY (student_id) REFERENCES student (student_id),
    FOREIGN KEY (course_id, term, section_no)
        REFERENCES section (course_id, term, section_no)
);

-- Many-to-many recursive relationship with role-based column names.
CREATE TABLE course_prerequisite (
    course_id TEXT NOT NULL,
    prereq_id TEXT NOT NULL,
    PRIMARY KEY (course_id, prereq_id),
    FOREIGN KEY (course_id) REFERENCES course (course_id),
    FOREIGN KEY (prereq_id) REFERENCES course (course_id),
    CHECK (course_id <> prereq_id)
);

INSERT INTO department VALUES
    ('FIN', 'Finance', 'Cheng Hall'),
    ('IM', 'Information Management', 'Hong Hall');

INSERT INTO student VALUES
    ('S101', 'an.chen@example.edu', 'An', 'Chen', 'IM'),
    ('S102', 'bea.lin@example.edu', 'Bea', 'Lin', 'FIN'),
    ('S103', 'kai.wu@example.edu', 'Kai', 'Wu', 'IM');

INSERT INTO student_phone VALUES
    ('S101', '0911-000-101'),
    ('S101', '02-2322-1010'),
    ('S102', '0911-000-102');

INSERT INTO course VALUES
    ('DB201', 'Database Management', 3, 'IM'),
    ('FT210', 'Financial Technology', 3, 'FIN'),
    ('ML230', 'Machine Learning', 3, 'IM');

INSERT INTO section VALUES
    ('DB201', '115-1', 1, 'H501', 45),
    ('FT210', '115-1', 1, 'C302', 40),
    ('ML230', '115-1', 1, 'H503', 45);

INSERT INTO enrollment VALUES
    ('S101', 'DB201', '115-1', 1, 'A'),
    ('S101', 'FT210', '115-1', 1, 'B+'),
    ('S102', 'FT210', '115-1', 1, 'A-'),
    ('S103', 'DB201', '115-1', 1, 'B'),
    ('S103', 'ML230', '115-1', 1, NULL);

INSERT INTO course_prerequisite VALUES
    ('ML230', 'DB201');

-- Derived completed credits: this example counts non-null grades other than F.
SELECT s.student_id,
       COALESCE(SUM(CASE
           WHEN e.grade IS NOT NULL AND e.grade <> 'F' THEN c.credits
           ELSE 0
       END), 0) AS completed_credits
FROM student AS s
LEFT JOIN enrollment AS e ON e.student_id = s.student_id
LEFT JOIN course AS c ON c.course_id = e.course_id
GROUP BY s.student_id
ORDER BY s.student_id;
