# Chapter 7 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: draft, source-checked against the complete Chapter 7 text and
  official Chapter 7 slides
- Case: original course-enrollment relation, dependencies, and decomposition
- Executable verification: passed again on August 27, 2026, using Python 3.12.9 and
  SQLite 3.45.3
- Publication: not approved

## Source scope checked

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 7, printed pages 303-352, Sections 7.1-7.11. Exercises were inspected for
  chapter context but not copied.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch7.pdf`, slides
  7.1-7.93.
- Current governance, revised syllabus, chapter-material prompt, completed Chapters
  2-6 materials, and existing SQLite lab conventions.

## Scope decision

Required instruction covers features of good relational design; update, insertion, and
deletion anomalies; functional dependencies and counterexamples; enough attribute
closure to identify keys; binary lossless decomposition; spurious tuples; BCNF; 3NF;
and the practical tradeoff among BCNF, losslessness, and dependency preservation.

Armstrong's axioms, complete FD closure, canonical covers, complete BCNF/3NF
decomposition algorithms, multivalued dependencies, 4NF and higher forms, first-normal-
form domain debates, design-process edge cases, and temporal data are supplementary.
They are not valid Exam 2 operations unless separately taught and practiced.

## Source and implementation cautions

1. A functional dependency is a schema-level constraint over every legal instance; a
   sample instance can refute an FD but cannot establish a business rule by itself.
2. FD equality is ordinary mathematical equality and assumes no null values. SQL null
   semantics are not used in the formal FD examples.
3. The binary lossless criterion based on the common attributes determining one side is
   necessary when all constraints are FDs; more general constraints are outside scope.
4. The four-table decomposition is shown as a sequence of defensible binary steps. A
   successful sample join supports the executable example but does not alone prove the
   property for all legal instances.
5. The original teaching-assignment example is 3NF but not BCNF only under the stated
   rule that each instructor teaches one course in the modeled context.
6. SQLite cannot declare arbitrary FDs. Primary keys, unique constraints, foreign keys,
   and checks implement only the constraints expressible in the lab schema.
7. The lab uses `EXCEPT` in both directions when comparing the reconstructed and
   original instances; equal row counts alone are insufficient to establish equality.

## Teaching-point alignment

| ID | Teaching point | Primary source | Worked example | Student action and feedback |
|---|---|---|---|---|
| C7.01 | good relational design | 7.1, pp. 303-307; slides 7.3-7.8 | flattened enrollment facts | classify employee/project facts |
| C7.02 | update/insertion/deletion anomalies | 7.1.1, pp. 305-306 | department, new course, last enrollment | execute reversible anomaly and explain limits |
| C7.03 | functional dependency | 7.2.2, pp. 309-312; slides 7.17-7.24 | student ID rule and course counterexample | test title-to-ID claim using requirements |
| C7.04 | closure, superkey, candidate key | 7.2.2 and 7.4.2, pp. 309-312, 322-324 | enrollment pair closure | compute employee-project closure |
| C7.05 | lossless binary decomposition | 7.1.2 and 7.2.3, pp. 306-308, 312-313; slides 7.9-7.16, 7.26-7.28 | department decomposition and two-way `EXCEPT` | interpret zero differences |
| C7.06 | lossy decomposition/spurious tuples | 7.1.2, pp. 306-308 | two employees named Kim | identify two false pairs |
| C7.07 | BCNF definition and test | 7.3.1, pp. 313-316; slides 7.29-7.37 | flattened and four decomposed relations | normalize employee-project schema |
| C7.08 | 3NF definition and prime attributes | 7.3.2, pp. 317-318; slides 7.38-7.43 | TeachingAssignment | revise conclusion after rule change |
| C7.09 | BCNF/3NF comparison | 7.3.1.2-7.3.3, pp. 315-319; slides 7.38-7.47 | dependency not local after BCNF split | compare designs using four criteria |

Every required teaching point has an explanation, complete worked example, student
practice, and a stated checking or feedback criterion.

## Teaching summary

1. Diagnose facts and three anomalies in the flattened relation.
2. Translate four business rules into FDs and reject one claim with a counterexample.
3. Compute the enrollment pair closure and establish candidate-key minimality.
4. Decompose into Department, Student, Course, and Enrollment.
5. Apply the binary lossless criterion and verify the sample reconstruction.
6. Execute the Kim decomposition to expose spurious tuples.
7. Test the original and decomposed schemas against BCNF.
8. Use TeachingAssignment to distinguish 3NF from BCNF.
9. Compare dependency preservation and implementation consequences.
10. Revise an individual decomposition after instructor feedback.

## Student-practice guidance

1. Employee, project, and assignment are distinct facts; column count is irrelevant.
2. One distinct name in current data does not establish a future FD.
3. Course title does not determine course ID unless the institution makes title unique.
4. The employee-project pair closure contains all five attributes and is minimal.
5. The normalized reconstruction has zero differences in both directions.
6. The Kim natural join has four rows; two pair the wrong employee with a city/salary.
7. Employee ID and project ID separately violate BCNF in the flattened schema.
8. Removing the one-course-per-instructor rule removes the violating FD and changes the
   candidate-key set.
9. The BCNF split is lossless but does not preserve the student-course-to-instructor FD
   in one relation.

## Verification command

```powershell
py -3 working_materials/chapters/ch07_normalization/instructor/verify_ch07.py
```

## Remaining limits before student release

- Instructor must confirm bilingual versus English-only student prose.
- Classroom workload and the amount of closure practice have not been observed with
  actual students.
- The formal notation may need a one-page handwritten worksheet for in-class use.
- `COURSE_PLAN.md` governs Chapter 7 scope and assessment boundaries.

## Chapter delivery status

- Files created: student guide, executable SQL lab, instructor source/alignment record,
  and verifier.
- Source verification: complete for textbook printed pages 303-352 and slides 7.1-7.93.
- Executed content: the complete lab; reversible anomaly transaction; independent
  course insertion; normalized reconstruction; deliberately lossy natural join;
  candidate-key closures; the 3NF-but-not-BCNF classification inputs; and all foreign
  keys.
- Unexecuted content: excluded theory, complete decomposition algorithms, higher normal
  forms, and temporal data.
- Progression decision: the chapter meets the source, explanation, worked-example,
  practice, alignment, and executable-check conditions required to begin Chapter 14.
  It remains a draft until the instructor reviews language and classroom workload.
