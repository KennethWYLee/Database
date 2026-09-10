# Course Maintenance

The course uses one `main` branch and the same tracked paths locally and on GitHub.
Open [Intro DB](../Intro%20DB/) for the syllabus and chapter notebooks. This directory
contains preparation sources, build tools, verification records, and historical records;
it is not a second course navigation system.

## Maintained Sources

Current sequence: today's Ch1/Ch2 only, then Ch3-9 and Ch14-19. Ch5/Ch8 are
available for Weeks 4/8, not the first two meetings. See the
[current scope record](course_repository/full_source_audit.md#chapter-order-and-expanded-scope).

| File or directory | Responsibility |
|---|---|
| [PROJECT.md](../PROJECT.md) | Course facts, decisions, authoritative files, and current status |
| [syllabus.md](../Intro%20DB/syllabus.md) | The single maintained English course syllabus |
| [COURSE_PLAN.md](COURSE_PLAN.md) | Detailed teaching plan; dates and assessment must agree with the syllabus |
| [Teaching material prompt](database_chapter_teaching_material_prompt.md) | Chapter authoring and source-check requirements |
| `chapters/` | Maintained explanations, SQL, data, figures, and chapter verifiers |
| [course_repository/](course_repository/README.md) | Builds current Ch1/Ch2/Ch3/Ch5/Ch8 notebooks and preserves twelve previous notebooks under under_revision |
| `student_sqlite_package/` | Optional existing SQLite package and its explicit allow-list |
| [archive/](archive/README.md) | Superseded records, not current instructions or course decisions |
| [Migration review](structure_migration_review.md) | September 7 layout change and verification evidence |
| [Chapter teaching review](course_repository/all_chapters_teaching_review.md) | September 8 diagrams, small examples, source checks, and execution evidence |
| [First-meeting release](course_repository/first_meeting_release.md) | Opening scope, source locators, checks, limitations, and publication record |
| [Ch5/Ch8 revision](course_repository/full_source_audit.md#relational-foundations-revision) | Current continuation, algebra coverage, source locations, and checks |

Edit chapter sources, then regenerate notebooks. Do not independently edit both a source
and its generated notebook. The root README and Intro DB syllabus are maintained directly
and are never overwritten by the notebook builder. Git tracks the built notebooks so a
normal checkout includes the same files used in class.

Root `AGENTS.md` and `CLAUDE.md` remain byte-identical tool instructions. `PROJECT.md`
remains at the root for course context; the root README is the human-facing entry point.

Private textbook PDFs and historical sources stay local. Ignored `assessments/`,
`sql_labs/`, and temporary outputs remain excluded from Git; moving this directory did
not authorize their publication. Previously created preview branches are historical,
not current course entry points, and are not deleted by this change.
