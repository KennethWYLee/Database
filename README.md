# Database Management

This private repository maintains the 115-1 Database Management course, its source
checks, and the unified notebook build. Course navigation uses one self-contained
notebook per selected textbook chapter; there is no separate weekly, instructor, or
student file tree.

## Start Here

- [Current English syllabus](1151_database_management_revised_syllabus.md)
- [18-week course plan](COURSE_PLAN.md)
- [Course decisions and current status](PROJECT.md)
- [Course notebook build](working_materials/course_repository/README.md)
- [Unified course materials](https://github.com/KennethWYLee/Database/tree/course-materials)
- [Pre-instructor-review audit](working_materials/pre_instructor_review_audit.md)

## Notebook Repository

The generated course repository contains only:

```text
README.md
SYLLABUS.md
SCHEDULE.md
ch02.ipynb ... ch19.ipynb
```

Each `chXX.ipynb` combines the chapter reading, original teaching diagrams, executable
SQL or Python demonstrations, database-creation guidance, practice, and checks. Required
images and example data are embedded directly in the notebook, so the current build has
no separate `assets/`, lab runner, or chapter directory.

Build and verify all 12 notebooks from the repository root:

```powershell
python working_materials/course_repository/build_course_repository.py --verify
```

The generated preview is local and ignored by Git. Historical materials, textbooks,
assessments, answers, grading records, and source-verification notes remain private and
are not copied into the notebook repository. The private `course-materials` branch is a
generated review copy and must be rebuilt from the maintained sources on `main`.
