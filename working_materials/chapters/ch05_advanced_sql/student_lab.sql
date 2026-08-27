-- Chapter 5: selected Advanced SQL topics
-- Verified with SQLite 3.45.3. Run Chapter 2 course_registration_setup.sql first.
-- Predict rows, ties, NULLs, and side effects before each block.

PRAGMA foreign_keys = ON;

-- Example 1: executable baseline for the unexecuted stored-function example.
-- SQLite cannot install CREATE FUNCTION through SQL, so this query verifies the
-- expected body result for each course.
SELECT c.course_id,
       (
           SELECT COUNT(*)
           FROM enrollment AS e
           WHERE e.course_id = c.course_id
       ) AS enrollment_count
FROM course AS c
ORDER BY c.course_id;

-- Example 2: execute and roll back the body action of the procedure reference.
-- This does not create or call a stored procedure in SQLite.
SAVEPOINT procedure_body_demo;
UPDATE course
SET credits = 4
WHERE course_id = 'DB201';
SELECT course_id, credits FROM course WHERE course_id = 'DB201';
ROLLBACK TO procedure_body_demo;
RELEASE procedure_body_demo;
SELECT course_id, credits FROM course WHERE course_id = 'DB201';

-- Example 3: row-level audit trigger using SQLite OLD and NEW transition rows.
DROP TRIGGER IF EXISTS enrollment_grade_audit;
DROP TABLE IF EXISTS enrollment_audit;

CREATE TABLE enrollment_audit (
    audit_id INTEGER PRIMARY KEY,
    action_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    term TEXT NOT NULL,
    old_grade TEXT,
    new_grade TEXT
);

CREATE TRIGGER enrollment_grade_audit
AFTER UPDATE OF grade ON enrollment
FOR EACH ROW
WHEN OLD.grade IS NOT NEW.grade
BEGIN
    INSERT INTO enrollment_audit (
        action_name, student_id, course_id, term, old_grade, new_grade
    ) VALUES (
        'GRADE_UPDATE', NEW.student_id, NEW.course_id, NEW.term,
        OLD.grade, NEW.grade
    );
END;

SAVEPOINT trigger_demo;

UPDATE enrollment
SET grade = 'B+'
WHERE student_id = 'S103'
  AND course_id = 'DB201'
  AND term = '115-1';

SELECT action_name, student_id, course_id, term, old_grade, new_grade
FROM enrollment_audit
ORDER BY audit_id;

ROLLBACK TO trigger_demo;
RELEASE trigger_demo;

SELECT COUNT(*) AS audit_rows_after_rollback
FROM enrollment_audit;

-- Example 4: prerequisite relation for recursive queries.
DROP TABLE IF EXISTS course_prerequisite;

CREATE TABLE course_prerequisite (
    course_id TEXT NOT NULL,
    prereq_id TEXT NOT NULL,
    PRIMARY KEY (course_id, prereq_id),
    FOREIGN KEY (course_id) REFERENCES course (course_id),
    FOREIGN KEY (prereq_id) REFERENCES course (course_id),
    CHECK (course_id <> prereq_id)
);

INSERT INTO course_prerequisite (course_id, prereq_id) VALUES
    ('DB201', 'WD120'),
    ('FT210', 'DB201'),
    ('ML230', 'DB201');

-- Example 5: base term finds direct prerequisites. The recursive term adds one
-- level at a time. UNION removes duplicates so the fixed point can be reached.
WITH RECURSIVE all_prereq(course_id, prereq_id) AS (
    SELECT course_id, prereq_id
    FROM course_prerequisite

    UNION

    SELECT ap.course_id, cp.prereq_id
    FROM all_prereq AS ap
    JOIN course_prerequisite AS cp
      ON cp.course_id = ap.prereq_id
)
SELECT course_id, prereq_id
FROM all_prereq
ORDER BY course_id, prereq_id;

-- Example 6: recursive query for one target, with depth on the acyclic sample.
WITH RECURSIVE prereq_path(prereq_id, depth) AS (
    SELECT prereq_id, 1
    FROM course_prerequisite
    WHERE course_id = 'ML230'

    UNION ALL

    SELECT cp.prereq_id, pp.depth + 1
    FROM prereq_path AS pp
    JOIN course_prerequisite AS cp
      ON cp.course_id = pp.prereq_id
)
SELECT prereq_id, depth
FROM prereq_path
ORDER BY depth, prereq_id;

-- Example 7: practice-score data for ranking and window functions.
DROP TABLE IF EXISTS sql_practice_score;

CREATE TABLE sql_practice_score (
    student_id TEXT NOT NULL,
    attempt_no INTEGER NOT NULL CHECK (attempt_no > 0),
    score INTEGER NOT NULL CHECK (score BETWEEN 0 AND 100),
    PRIMARY KEY (student_id, attempt_no),
    FOREIGN KEY (student_id) REFERENCES student (student_id)
);

INSERT INTO sql_practice_score (student_id, attempt_no, score) VALUES
    ('S101', 1, 78),
    ('S101', 2, 92),
    ('S102', 1, 92),
    ('S103', 1, 84),
    ('S104', 1, 70),
    ('S104', 2, 84);

-- Example 8: RANK leaves gaps after ties; DENSE_RANK does not. ROW_NUMBER
-- always differs and therefore includes student_id as a deterministic tie-breaker.
WITH best_score AS (
    SELECT student_id, MAX(score) AS best_score
    FROM sql_practice_score
    GROUP BY student_id
)
SELECT student_id,
       best_score,
       RANK() OVER (ORDER BY best_score DESC) AS score_rank,
       DENSE_RANK() OVER (ORDER BY best_score DESC) AS dense_score_rank,
       ROW_NUMBER() OVER (
           ORDER BY best_score DESC, student_id
       ) AS display_row
FROM best_score
ORDER BY display_row;

-- Example 9: PARTITION BY restarts the calculation for each student. The frame
-- includes all attempts from the first through the current attempt.
SELECT student_id,
       attempt_no,
       score,
       ROUND(
           AVG(score) OVER (
               PARTITION BY student_id
               ORDER BY attempt_no
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ),
           1
       ) AS running_average
FROM sql_practice_score
ORDER BY student_id, attempt_no;

-- Example 10: conditional aggregation creates a portable two-attempt cross-tab.
SELECT student_id,
       MAX(CASE WHEN attempt_no = 1 THEN score END) AS attempt_1,
       MAX(CASE WHEN attempt_no = 2 THEN score END) AS attempt_2
FROM sql_practice_score
GROUP BY student_id
ORDER BY student_id;

-- Student practice. Save predictions and actual results.
-- P1. Define the input, returned value, and equivalent SELECT for a function named
--     department_course_count. Do not claim it was installed in SQLite.
-- P2. Explain how the change_course_credits procedure should respond if no course
--     matches. State whether the contract should report an error or affected-row count.
-- P3. Add a DELETE audit trigger for enrollment. Verify OLD values and rollback.
-- P4. Explain why a foreign key or CHECK should be used instead of a trigger when it
--     can directly express the same rule.
-- P5. Query all direct and indirect prerequisites of FT210, including depth.
-- P6. Add a cycle inside a savepoint and explain why UNION reaches a fixed point but
--     the UNION ALL depth query needs explicit cycle protection. Roll back the cycle.
-- P7. Predict RANK, DENSE_RANK, and ROW_NUMBER if S103 improves to 92.
-- P8. Compute a two-attempt moving average with ROWS BETWEEN 1 PRECEDING AND
--     CURRENT ROW, partitioned by student_id.
-- P9. Extend the conditional-aggregation cross-tab with each student's best score.
