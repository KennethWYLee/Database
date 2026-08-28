# Chapter 7: Relational Database Design and Normalization

## Core Question

Which facts are stored repeatedly, can a decomposition reconstruct the original relation
without false rows, and does every important determinant identify a complete row?

Use this guide with `student_lab.sql`. Predict before executing, and do not infer a
business rule from one convenient sample instance.

## Scope and Connection

Chapter 6 mapped requirements to relations. This chapter is useful when an existing table,
spreadsheet, or mixed design still combines several kinds of facts.

The classroom core is anomalies, functional dependencies, attribute closure, binary
lossless decomposition, spurious tuples, and introductory 3NF/BCNF decisions. Canonical
covers and complete decomposition algorithms are extensions.

## Teaching Summary

| Topic | Worked example and practice | Evidence to retain |
|---|---|---|
| Anomalies and dependencies | Flattened course facts | Business rule and counterexample |
| Attribute closure | Candidate-key calculation | Closure steps and minimality check |
| Lossless decomposition | Reconstructing normalized relations | Both difference checks |
| 3NF and BCNF | Small dependency sets | Determinant and key reasoning |

## Prerequisites

- Relations, tuples, candidate keys, and foreign keys.
- Projection and natural join.
- Basic schema and data-modification SQL.
- Chapter 6 entity, relationship, and mapping concepts.

## Learning Objectives

After completing this chapter, you should be able to:

1. Identify update, insertion, and deletion anomalies.
2. Write a functional dependency from a stable business rule.
3. Reject an unsupported dependency with a counterexample.
4. Calculate a small attribute closure and test key minimality.
5. Test a binary decomposition for losslessness and identify spurious tuples.
6. Apply introductory BCNF and 3NF criteria.
7. Explain a basic tradeoff involving BCNF and dependency preservation.

## 1. Mixed Facts and Anomalies

Consider:

```text
course_enrollment_record(
  student_id, student_name, dept_code, dept_name,
  course_id, course_title, credits, grade
)
```

Business rules imply:

```text
student_id -> student_name, dept_code
dept_code  -> dept_name
course_id  -> course_title, credits
(student_id, course_id) -> grade
```

This relation stores Student, Department, Course, and Enrollment facts together.

- **Update anomaly:** changing one repeated department name can create inconsistent copies.
- **Insertion anomaly:** a course with no enrollment cannot be stored naturally.
- **Deletion anomaly:** deleting the last enrollment in a course can remove the only copy
  of that course's title and credits.

The problem is not the number of columns. It is the dependency structure and the resulting
operations.

### Practice

For `employee_project(employee_id, employee_name, project_id, project_name, hours)`,
identify Employee, Project, and assignment facts and one anomaly of each applicable type.

## 2. Functional Dependencies

For schema R, `alpha -> beta` means that every legal pair of tuples that agrees on all
attributes in alpha must also agree on beta. Alpha is the determinant.

A dependency such as `(student_id, course_id) -> student_id` is trivial because the right
side is included in the left. If `K -> R`, K is a superkey; if K is minimal, it is a
candidate key.

### Rule and Counterexample

The rule "each student identifier represents one student" supports:

```text
student_id -> student_name, dept_code
```

It does not support `student_id -> course_id`. The legal rows `(S101, DB201)` and
`(S101, FT210)` form a counterexample.

Practice: decide whether `course_title -> course_id` is supported. Either state a rule
that guarantees unique titles or provide two legal courses with one title and different
identifiers.

## 3. Attribute Closure and Candidate Keys

The closure `alpha+` contains every attribute functionally determined by alpha. Start with
alpha, repeatedly apply dependencies whose left sides are already present, and stop when
no new attribute can be added.

For `{student_id, course_id}`:

1. Begin with both identifiers.
2. Add student name and department code from `student_id`.
3. Add department name from department code.
4. Add course title and credits from `course_id`.
5. Add grade from the identifier pair.

The closure contains every attribute, so the pair is a superkey. Removing either
identifier prevents determination of the other entity's facts and grade, so the pair is
minimal and is therefore a candidate key.

### Practice

Given:

```text
employee_id -> employee_name
project_id -> project_name
(employee_id, project_id) -> hours
```

Calculate `{employee_id, project_id}+` and test both single-attribute removals.

## 4. Lossless Decomposition

A decomposition is lossless if projecting a legal relation into the new schemas and
joining the projections reconstructs exactly the original relation.

For a binary decomposition R into R1 and R2 under functional dependencies, the step is
lossless when the common attributes determine all attributes of R1 or all attributes of
R2:

```text
(R1 intersection R2) -> R1
or
(R1 intersection R2) -> R2
```

Having a shared column is not enough; the shared attributes must identify one side.

### Lossless Example

Split Department from the flattened relation:

```text
Department(dept_code, dept_name)
Remaining(student_id, student_name, dept_code,
          course_id, course_title, credits, grade)
```

The common attribute `dept_code` determines Department, so this step is lossless. Further
steps produce Department, Student, Course, and Enrollment relations. The lab uses
bidirectional `EXCEPT` checks for the supplied instance.

### Lossy Example

Original rows:

```text
(E1, Kim, Taipei, 60000)
(E2, Kim, Tainan, 62000)
```

Split into `EmployeeIdentity(employee_id, name)` and
`EmployeeDetails(name, city, salary)`. Name is not a key. Joining the projections produces
four rows, including two false employee-city combinations.

### Practice

Run the lossless and lossy lab sections. Retain both difference counts for the lossless
case and identify the two spurious Kim rows in the lossy case.

## 5. Boyce-Codd Normal Form

R is in BCNF when every nontrivial dependency `alpha -> beta` has a determinant alpha
that is a superkey.

In the flattened relation, `dept_code -> dept_name` is nontrivial, but department code
does not determine Student, Course, and Enrollment facts. This is a BCNF violation.

After decomposition:

- Department has key determinant `dept_code`.
- Student has key determinant `student_id`.
- Course has key determinant `course_id`.
- Enrollment has key determinant `(student_id, course_id)`.

Under the listed rules, each relation satisfies BCNF. A new business rule requires a new
check.

## 6. Third Normal Form

For every dependency `alpha -> beta`, 3NF allows the dependency when it is trivial, alpha
is a superkey, or each attribute in `beta - alpha` is prime. A prime attribute occurs in
at least one candidate key. Every BCNF relation is in 3NF, but not every 3NF relation is
in BCNF.

### 3NF but Not BCNF Example

```text
TeachingAssignment(student_id, course_id, instructor_id)

(student_id, course_id) -> instructor_id
instructor_id -> course_id
```

If every instructor teaches only one course, candidate keys are
`(student_id, course_id)` and `(student_id, instructor_id)`. All three attributes are
prime. `instructor_id -> course_id` violates BCNF because instructor ID is not a superkey,
but it satisfies the prime-attribute allowance in 3NF.

If instructors may teach several courses, the second dependency no longer holds and the
normal-form analysis changes. Normal form is a property of a schema together with its
valid dependencies.

## 7. Dependency Preservation as a Tradeoff

A dependency-preserving decomposition allows each original dependency to be checked in
individual decomposed relations without joining them.

Splitting TeachingAssignment into
`InstructorCourse(instructor_id, course_id)` and
`StudentInstructor(student_id, instructor_id)` can be lossless and BCNF under the stated
rule. However, the original dependency
`(student_id, course_id) -> instructor_id` is not contained in one relation and cannot be
checked with one local key constraint.

This example shows why a design discussion should include redundancy, losslessness,
dependency enforcement, and implementation cost rather than stopping after the label
BCNF.

## Common Errors

1. Guessing a dependency from a small sample without a business rule.
2. Treating current uniqueness as proof of a candidate key.
3. Listing decomposed tables without anomalies, dependencies, or a lossless argument.
4. Assuming that any shared attribute makes a join lossless.
5. Applying a simplified 3NF slogan without finding keys and prime attributes.
6. Assuming that BCNF always preserves every dependency.
7. Treating one successful sample join as proof for every legal instance.

## Classroom and Individual Evidence

Compare a 3NF single relation with a BCNF decomposition using the same four criteria:
repetition, losslessness, local dependency checking, and implementation cost.

Submit the original relation and rules, dependencies and key closure, one anomaly, the
decomposition and lossless reason, normal-form decisions, and one revision made after
feedback.

## Chapter Summary

Normalization converts business rules into functional dependencies and uses closure,
lossless decomposition, and normal-form criteria to evaluate a schema. A good answer
preserves both data meaning and enforceable constraints. Chapter 14 moves to physical
design and query-plan evidence after the logical design is sound.

## After-Class Continuation

Repeat the sequence "rules, dependencies, anomalies, decomposition, lossless check" on a
real table. Armstrong's axioms, canonical covers, and complete decomposition algorithms
are extensions rather than Exam 2 operations.
