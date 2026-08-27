-- Chapter 5 reference: illustrative SQL/PSM-style routines
-- NOT EXECUTABLE IN SQLITE. Stored-routine syntax differs across DBMS products.
-- These examples show the interface and logic taught in the student guide.

-- Function: one input value and one returned scalar value.
CREATE FUNCTION course_enrollment_count(p_course_id VARCHAR(10))
RETURNS INTEGER
BEGIN
    DECLARE result_count INTEGER;
    SELECT COUNT(*) INTO result_count
    FROM enrollment
    WHERE course_id = p_course_id;
    RETURN result_count;
END;

-- Intended use after installation in a DBMS with adapted syntax:
-- SELECT course_id,
--        course_enrollment_count(course_id) AS enrollment_count
-- FROM course;

-- Procedure: performs a database action when invoked explicitly.
CREATE PROCEDURE change_course_credits(
    IN p_course_id VARCHAR(10),
    IN p_credits INTEGER
)
BEGIN ATOMIC
    UPDATE course
    SET credits = p_credits
    WHERE course_id = p_course_id;
END;

-- Intended call after installation in a DBMS with adapted syntax:
-- CALL change_course_credits('DB201', 4);
