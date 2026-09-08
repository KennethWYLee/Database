PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS enrollment;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS department;

CREATE TABLE department (
    dept_code TEXT NOT NULL PRIMARY KEY,
    dept_name TEXT NOT NULL UNIQUE,
    building TEXT NOT NULL
);

CREATE TABLE student (
    student_id TEXT NOT NULL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    student_name TEXT NOT NULL,
    dept_code TEXT NOT NULL,
    FOREIGN KEY (dept_code) REFERENCES department (dept_code)
);

CREATE TABLE course (
    course_id TEXT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    dept_code TEXT NOT NULL,
    credits INTEGER NOT NULL
        CHECK (typeof(credits) = 'integer' AND credits BETWEEN 1 AND 6),
    FOREIGN KEY (dept_code) REFERENCES department (dept_code)
);

CREATE TABLE enrollment (
    student_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    term TEXT NOT NULL,
    grade TEXT,
    PRIMARY KEY (student_id, course_id, term),
    FOREIGN KEY (student_id) REFERENCES student (student_id),
    FOREIGN KEY (course_id) REFERENCES course (course_id)
);

INSERT INTO department (dept_code, dept_name, building) VALUES
    ('DES', 'Digital Design', 'Hong Hall'),
    ('FIN', 'Finance', 'Cheng Hall'),
    ('IM', 'Information Management', 'Hong Hall');

INSERT INTO student (student_id, email, student_name, dept_code) VALUES
    ('S101', 'an.chen@example.edu', 'An Chen', 'IM'),
    ('S102', 'bea.lin@example.edu', 'Bea Lin', 'FIN'),
    ('S103', 'kai.wu@example.edu', 'Kai Wu', 'IM'),
    ('S104', 'mira.ho@example.edu', 'Mira Ho', 'DES');

INSERT INTO course (course_id, title, dept_code, credits) VALUES
    ('DB201', 'Database Management', 'IM', 3),
    ('FT210', 'Financial Technology', 'FIN', 3),
    ('ML230', 'Machine Learning', 'IM', 3),
    ('WD120', 'Web Design', 'DES', 2);

INSERT INTO enrollment (student_id, course_id, term, grade) VALUES
    ('S101', 'DB201', '115-1', 'A'),
    ('S101', 'FT210', '115-1', 'B+'),
    ('S102', 'FT210', '115-1', 'A-'),
    ('S103', 'DB201', '115-1', 'B'),
    ('S103', 'ML230', '115-1', 'A'),
    ('S104', 'WD120', '115-1', 'A-');
