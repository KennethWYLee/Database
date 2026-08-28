# Database Management - Instructor Source Repository

This private repository maintains the 115-1 Database Management course sources,
verification records, and student-release build process. It is not the repository that
students will be asked to navigate.

## Start Here

- [Current English syllabus](1151_database_management_revised_syllabus.md)
- [18-week course plan](COURSE_PLAN.md)
- [Course decisions and current status](PROJECT.md)
- [Pre-instructor-review audit](working_materials/pre_instructor_review_audit.md)
- [Student repository build](working_materials/student_repository/README.md)

## Main Working Areas

- `working_materials/chapters/`: maintained chapter guides, labs, diagrams, and
  instructor verification records.
- `working_materials/student_sqlite_package/`: SQLite lab allow-list, package builder,
  and approved ZIP.
- `working_materials/student_repository/`: builds the simplified 18-week student
  repository preview.

Build and verify the student preview from the repository root:

```powershell
py -3 working_materials/student_repository/build_student_repository.py --verify
```

The generated preview is local and ignored by Git. A separate public repository may be
created later from the verified preview after instructor approval. Historical materials,
textbooks, assessments, answers, grading records, and unverified sources remain private.
