# Chapter 2: Introduction to the Relational Model

## Core Question

A table is more than a grid. To query and connect tables correctly, we must know what a
row represents, which attributes identify it, how tables refer to one another, and how a
small set of relational operations describes a query.

## Teaching Summary

| Topic | Worked example and practice | Evidence to retain |
|---|---|---|
| Relation, tuple, attribute, domain, schema, and instance | Identify parts of course-registration relations | Schema identification sheet |
| Primary, candidate, and foreign keys | Compare candidate keys and follow references | Key map with reasons |
| Core relational algebra | Apply selection, projection, product, join, and set operations | Result after each operation |

Chapter 3 expresses these query ideas in SQL. This chapter focuses on structure and query
logic rather than SQL syntax. Assignment, rename, and formal equivalence proofs are
extensions and are not major Exam 1 operations.

## Connection to Chapter 3

The relational model supplies the vocabulary and operations that SQL implements. The
keys and foreign-key paths in this chapter become join conditions, while selection and
projection become common parts of a `SELECT` query.

## Prerequisites

- Read a two-dimensional table.
- Understand that a mathematical set contains one copy of each element.
- Apply equality, inequality, `AND`, and `OR` conditions.
- Follow an explicit sequence of filtering and column-selection steps.

## Learning Objectives

After completing this chapter, you should be able to:

1. Identify a relation, tuple, attribute, domain, schema, and relation instance.
2. Explain the difference between a schema and an instance.
3. Classify superkeys, candidate keys, primary keys, and composite keys from business
   rules.
4. Identify referencing and referenced relations for a foreign key.
5. Read a schema diagram and follow foreign-key connections.
6. Apply selection, projection, Cartesian product, theta join, union, intersection, and
   set difference to small relation instances.
7. Compare the purpose of two simple relational-algebra expressions.

## Course-Registration Data

### `department`

| dept_code | dept_name | building |
|---|---|---|
| DES | Digital Design | Hong Hall |
| FIN | Finance | Cheng Hall |
| IM | Information Management | Hong Hall |

### `student`

| student_id | email | student_name | dept_code |
|---|---|---|---|
| S101 | an.chen@example.edu | An Chen | IM |
| S102 | bea.lin@example.edu | Bea Lin | FIN |
| S103 | kai.wu@example.edu | Kai Wu | IM |
| S104 | mira.ho@example.edu | Mira Ho | DES |

### `course`

| course_id | title | dept_code | credits |
|---|---|---|---:|
| DB201 | Database Management | IM | 3 |
| FT210 | Financial Technology | FIN | 3 |
| ML230 | Machine Learning | IM | 3 |
| WD120 | Web Design | DES | 2 |

### `enrollment`

| student_id | course_id | term | grade |
|---|---|---|---|
| S101 | DB201 | 115-1 | A |
| S101 | FT210 | 115-1 | B+ |
| S102 | FT210 | 115-1 | A- |
| S103 | DB201 | 115-1 | B |
| S103 | ML230 | 115-1 | A |
| S104 | WD120 | 115-1 | A- |

The design uses these business rules:

- Each student has one unique, stable `student_id`.
- Each email belongs to at most one student; names may repeat.
- Each department and course has a unique code.
- A student has at most one enrollment in the same course and term.
- Student and course department codes must reference an existing department.
- Enrollment student and course identifiers must reference existing rows.

## 1. Relations, Tuples, Attributes, and Domains

- A **relation** corresponds to a table.
- A **tuple** corresponds to one row.
- An **attribute** corresponds to one column.
- A **relation instance** is the set of tuples stored at a particular time.
- A **domain** is the set of values allowed for an attribute.

For `student`, `student_id` is an attribute and
`(S101, an.chen@example.edu, An Chen, IM)` is a tuple. The four current rows form the
current relation instance.

### Worked Example

`course` has four attributes and four current tuples. Adding a course changes the
instance. Adding an `admission_year` attribute changes the schema.

### Predict and Check

In `enrollment`, identify the relation name, all attributes, and the tuple representing
S103 taking ML230. Separate attribute names from attribute values.

### Atomic Values, Order, and Duplicates

A value is atomic when the design treats it as one indivisible value. Storing several
phone numbers in one cell makes independent phone operations difficult. A clearer design
is `student_phone(student_id, phone_number)` with one phone number per row.

In the formal relational model, a relation is a set. Tuple display order is not part of
the relation, and identical duplicate tuples are not retained. SQL tables may permit
duplicates; Chapter 3 revisits this difference with `DISTINCT`.

Predict whether rearranging the four `student` rows changes the formal relation. It does
not. Required display order must be expressed by a query.

## 2. Schema and Instance

A **relation schema** describes a relation's name, attributes, domains, and constraints.
An **instance** is the current data.

```text
student(student_id, email, student_name, dept_code)
```

Changing S102 from department FIN to IM changes the instance. Adding a new attribute
changes the schema and requires a decision about values for existing rows.

## 3. Keys

Keys follow from the schema and business rules, not merely from accidental uniqueness in
the current sample.

- A **superkey** is an attribute set that uniquely identifies a tuple. It may contain
  unnecessary attributes.
- A **candidate key** is a minimal superkey.
- A **primary key** is the candidate key selected as the main identifier.
- A **composite key** contains more than one attribute.

### Worked Example: `student`

`{student_id}` and `{email}` are candidate keys under the stated rules.
`{student_id, student_name}` is a superkey but not a candidate key because
`student_name` is unnecessary. `{student_name}` is not guaranteed to be unique even
though the four sample names differ. This design selects `student_id` as the primary key.

### Worked Example: `enrollment`

Neither `student_id` nor `course_id` alone identifies an enrollment. The composite key
`{student_id, course_id, term}` does under the stated rule.

### Practice

Compare `student_name`, `email`, and `student_id` as proposed primary keys. First identify
the candidate keys. Then discuss stability, possible changes, length, and business
meaning. A design conclusion requires reasons, not a vote.

## 4. Foreign Keys and Schema Diagrams

A **foreign key** appears in the referencing relation and must match a key in the
referenced relation. For example, `student.dept_code` references
`department.dept_code`.

Adding a student with department `LAW` violates the rule unless the LAW department is
created first. A foreign key need not be unique in the referencing relation; many
students may belong to IM.

```text
department
  PK dept_code
     dept_name
     building
       ^
       | student.dept_code, course.dept_code

student                              course
  PK student_id                        PK course_id
  CK email                             FK dept_code -> department.dept_code
     student_name                         title
  FK dept_code -> department.dept_code    credits
       ^                                  ^
       |                                  |
       +---------- enrollment ------------+
                    PK/FK student_id -> student.student_id
                    PK/FK course_id  -> course.course_id
                    PK    term
                          grade
```

To find the name and course department for enrollment `(S101, DB201, 115-1, A)`, follow
`enrollment.student_id` to Student, then `enrollment.course_id` to Course, and finally
`course.dept_code` to Department.

### Evidence to Retain

Create a schema-and-key sheet containing all primary keys, every foreign key and its
direction, the two Student candidate keys, one nonminimal superkey, and one modification
that would violate referential integrity.

## 5. Relational-Algebra Operations

Each relational-algebra operation accepts one or two relations and returns a relation.
This closure property allows operations to be composed.

| Operation | Symbol | Main question |
|---|---|---|
| Selection | `σ` | Which tuples remain? |
| Projection | `Π` | Which attributes remain? |
| Cartesian product | `×` | What are all cross-relation tuple combinations? |
| Theta join | `⋈_θ` | Which combinations satisfy the join condition? |
| Union | `∪` | Which tuples occur in either input? |
| Intersection | `∩` | Which tuples occur in both inputs? |
| Set difference | `−` | Which tuples occur in the left input but not the right? |

### Selection

```text
σ_dept_code='IM'(student)
```

This keeps the complete S101 and S103 tuples. Predict the result of
`σ_dept_code='IM' AND student_id!='S101'(student)` and explain which predicate excludes
each removed tuple.

### Projection

```text
Π_dept_code(student)
```

The formal result is `{DES, FIN, IM}`. Projection removes duplicate tuples because a
formal relation is a set. Predict `Π_building(department)` and handle the repeated
`Hong Hall` value correctly.

### Composition

```text
Π_student_name(σ_dept_code='IM'(student))
```

The inner selection keeps S101 and S103; the outer projection produces
`{An Chen, Kai Wu}`. Write an expression for the identifiers and titles of three-credit
courses, and state which operation runs first in the expression.

### Cartesian Product

For `{S101, S102} × {DB201, FT210}`, the result has four pairs. These are possible
combinations, not four enrollment facts. The complete Student and Course relations have
four tuples each, so their product has 16 tuples.

### Theta Join

```text
student ⋈_student.student_id=enrollment.student_id enrollment
```

A theta join can be understood as a Cartesian product followed by a selection:

```text
r ⋈_theta s = σ_theta(r × s)
```

Projecting `student_name` and `course_id` after the join produces the six actual
enrollment pairs. Omitting the join predicate produces 24 combinations, most of which
are not enrollment facts.

Practice: identify the two relations and join predicate needed to connect a course title
to its department name.

## 6. Set Operations

Union, intersection, and difference require compatible input relations: the same number
of attributes and compatible domains in corresponding positions.

Let:

```text
A = students in DB201 = {S101, S103}
B = students in FT210 = {S101, S102}
```

| Expression | Meaning | Result |
|---|---|---|
| `A ∪ B` | In DB201 or FT210 or both | `{S101, S102, S103}` |
| `A ∩ B` | In both courses | `{S101}` |
| `A − B` | In DB201 but not FT210 | `{S103}` |
| `B − A` | In FT210 but not DB201 | `{S102}` |

Set difference has direction. `student ∪ course` is invalid because the schemas are not
compatible.

Practice: let C be the students in ML230. Write C, then calculate `A ∪ C`, `A ∩ C`, and
`C − A`.

## Extensions

### Assignment

Assignment names an intermediate relation without changing the permanent database:

```text
db_students <- Π_student_id(σ_course_id='DB201'(enrollment))
fintech_students <- Π_student_id(σ_course_id='FT210'(enrollment))
db_students ∩ fintech_students
```

### Rename

Rename distinguishes multiple uses of the same relation:

```text
ρ_s1(student)
ρ_s2(student)
```

It supports a self-comparison such as finding different students in the same department.

### Simple Equivalence

These expressions place the same Student-only filter before or after an inner join:

```text
Q1 = σ_student.dept_code='IM'(
       student ⋈_student.student_id=enrollment.student_id enrollment
     )

Q2 = (σ_dept_code='IM'(student))
     ⋈_student.student_id=enrollment.student_id enrollment
```

They express the same result under the stated conditions. Equality on one sample alone is
not a proof for every legal instance. Chapter 16 revisits equivalence as an optimization
guardrail.

## Common Errors

1. Choosing a key from accidental uniqueness in the sample.
2. Calling every superkey a candidate key.
3. Drawing a foreign-key arrow in the wrong direction.
4. Assuming tuple display order is part of a relation.
5. Forgetting duplicate removal in formal projection and set operations.
6. Treating a Cartesian product as a factual relationship.
7. Omitting the join predicate.
8. Reversing set difference.

## Discussion and Individual Evidence

For each proposed key or algebra result, state the business rule or operation that
supports the answer. Retain the schema sheet, key map, each intermediate relation, and
one corrected misconception.

## Chapter Summary

A schema defines structure and constraints; an instance contains current tuples. Keys
identify rows and foreign keys connect relations. Selection filters tuples, projection
keeps attributes, a join selects meaningful cross-relation combinations, and set
operations compare compatible results. Chapter 3 expresses these operations in SQL.

## After-Class Continuation

Recalculate one algebra expression after changing a tuple in the sample data, and explain
which intermediate relation changed. Assignment, rename, and formal equivalence proofs
are optional extensions rather than required Exam 1 derivations.
