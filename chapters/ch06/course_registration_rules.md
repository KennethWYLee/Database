# Course Registration Requirements

These requirements define the original example used in the Chapter 6 materials.

1. A department is identified by `dept_code` and has one name and one building.
2. A student is identified by `student_id`. The university also requires each email to
   be unique. A student's name has `first_name` and `last_name` components.
3. A student may have zero or more phone numbers. A phone number belongs to one
   student in this database.
4. Every student has exactly one major department. A department may have zero or
   more students.
5. A course is identified by `course_id` and has one title and a credit value.
6. Every course is offered by exactly one department. A department may offer zero or
   more courses.
7. A section cannot exist without its course. Within one course, the combination of
   `term` and `section_no` identifies a section.
8. A course may have zero or more sections; every section belongs to exactly one course.
9. A student may register for zero or more sections, and a section may have zero or
   more students.
10. Each registration may have one grade. Before grading, the grade is unknown.
11. A course may have zero or more prerequisite courses and may itself be a prerequisite
    for zero or more courses. A course cannot be its own direct prerequisite.
12. Completed credits are derived from completed registrations and course credits; the
    value is not stored as an independent student attribute in this design.

## Questions to resolve before changing the design

- Can a student have two major departments in the future?
- Must a phone number be unique across all students, or only within one student's list?
- Can the same section number be reused in another term?
- Which grade values count as successful completion?
- Must prerequisite cycles be prohibited, and where will that rule be enforced?
