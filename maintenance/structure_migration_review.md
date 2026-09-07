# September 7 Repository Layout Review

## Scope and Status

Base commit: `cb29dbe` on `main`. Build version: `2026.09.07-unified-main-layout`.
The instructor approved one local/GitHub layout and the Week 1 response-instruction fix.
This is a local reorganization, not authorization to stage, commit, push, delete branches,
or change repository visibility. Local validation is complete with no known blocking
layout or Week 1 regression issue. No course-policy or weekly-schedule change was made.

## File Responsibilities

- Root README: short course entry point.
- Root PROJECT: course-specific facts and decisions.
- Root AGENTS and CLAUDE: unchanged, byte-identical tool instructions.
- Intro DB/syllabus.md: the moved, single maintained syllabus, with navigation added.
- Intro DB/chXX.ipynb: twelve generated notebooks, explicitly eligible for Git alongside
  their maintained sources on main.
- maintenance/: the former working_materials directory, moved without deleting contents;
  root course plan and authoring prompt are now here too.
- maintenance/archive/: superseded COURSES and preview-home records, plus local ignored
  historical analysis/workplan files. Historical text is retained, not current navigation.

The complete directory move preserved all 182 file hashes before subsequent authorized
edits. Private references and historical source directories outside it were not moved.
The moved private assessment/SQL directories and temporary outputs remain ignored.

## Content Change

Week 1 now accepts either a correction or an explanation of why the prediction was correct.
The seven existing code demonstrations, chapter scope, dates, and grading remain unchanged.
The syllabus navigation replaces the proposed weekly file; it does not remove the relational
model lesson from Week 1. No week1.ipynb is created.

## Verification

Environment: Python 3.12.9, SQLite 3.45.3, resvg-py 0.5.0, nbformat 5.10.4,
nbclient 0.10.4, nbconvert 7.17.1, Node.js 24.19.0, local Chrome.

Commands run from the course root:

```powershell
python maintenance/course_repository/build_course_repository.py --verify
python maintenance/course_repository/test_repository_layout.py
python maintenance/chapters/ch02_relational_model/instructor/verify_week1.py
python maintenance/course_repository/review_notebook.py
python maintenance/student_sqlite_package/build_package.py --verify
```

- All twelve `maintenance/chapters/*/instructor/verify_chXX.py` programs passed.
- The builder executed twelve notebooks, verified the exact 13-file Intro DB set,
  manifest hashes, language/content exclusions, links, and embedded attachments.
- Seven layout tests pass, covering exact root/course files, instruction mirrors, navigation links,
  raw notebook schema, invalid IDs, path traversal, preserved syllabus and notebook
  files after a simulated build failure, and unexpected-file protection.
- The first build exposed an overbroad moved-path filter: the ordinary term "maintenance"
  in Ch6/Ch14 was incorrectly treated as a private path. The filter now requires a path
  separator, and a regression test distinguishes ordinary prose from internal paths.
  The corrected build passes; no teaching terminology was removed to satisfy the check.
- Week 1, Week 2, and complete Ch2 each passed in a fresh Jupyter kernel with outputs
  equal to the saved outputs. The standalone Week 1 verifier also passed.
- Relative to the immediately preceding PNG notebooks, only one Ch2 practice Markdown
  cell changed. All Ch2 code/output cells and all other eleven notebook files are
  unchanged. Syllabus content from Course Information onward is byte-for-byte text
  equivalent after line-ending normalization; only navigation and revision date changed.
- Two consecutive builds returned identical hashes for thirteen course files, the
  maintained root README, and the manifest. The builder did not overwrite the syllabus
  or README. PNG rendering remains dependent on installed fonts across different hosts.
- The optional SQLite ZIP rebuilt and passed all ten packaged labs from a fresh extraction.
  Its SHA-256 stayed `15f6847ad7163db552536231427010f68ef1731606726ba05bf298ce40001e05`.
- All 100 previously tracked files still exist at their mapped locations and remain
  eligible for Git. The sixteen additional eligible files are twelve notebooks, the
  archive README, two review/test scripts, and this record; no private source was added.
  All 732 checked private/reference/assessment/SQL/QA paths remain ignored.
- nbconvert HTML was rendered with headless Chrome at 1440 and 390 pixels. The new
  root navigation, syllabus opening, Week 1 practice, and embedded table diagram were
  inspected; checked pages have no whole-page horizontal overflow. Links were resolved
  against the actual repository paths, separately from the temporary HTML location.
  The local rendering harness and screenshots remain in ignored output storage.

The reorganization does not re-audit textbook claims in every chapter or test actual
classroom workload. Those are distinct from path, execution, and rendering checks.

Final source checks passed: 26 active Markdown local links resolve, maintained Python
and JSON files parse, UTF-8 decoding has no replacement characters, and `git diff --check`
reports no whitespace errors. Nothing was staged; Git therefore still reports moved
files as old-path deletions and new-path untracked files until a later authorized staging.

## Boundaries

The instructor subsequently authorized commit and push of this reorganization to main.
The maintained sources, generated Intro DB files, and this record are submitted together;
actual synchronization is established by Git history and remote commit comparison.
The earlier no-staging statements describe the completed local editing phase.
Old preview branches and repository visibility remain unchanged. Local ignored private
files are not intended to synchronize. No new live GitHub rendering check is claimed.
