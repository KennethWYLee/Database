# September 10 First-Meeting Release

Publication update: only Ch1, Ch2 and Ch3 are now published on main. Ch5/Ch8
and under_revision files mentioned in this historical record are retained
locally but ignored; the current entry is the root README and syllabus.

## Current Chapter Order

September 10, 2026: the instructor now requires today's Ch1/Ch2 only, followed
by Ch3-9 and Ch14-19 in order. Ch3/Ch4 remain required; Ch15/Ch18/Ch19 are
restored as selected teaching, and Ch20 is not scheduled. Ch5/Ch8 move to Weeks
4/8. Earlier dates, scope exclusions, and first-meeting directions below are
historical where they conflict. See the
[current revision record](full_source_audit.md#chapter-order-and-expanded-scope).
This schedule change does not complete the remaining prescribed-book notebooks.

Date: September 8, 2026. Baseline: `a9bc1a8` on `main`.
The instructor authorized the first batch, including verification, commit, and push
to the existing origin. The branch matched `origin/main` after fetching at the start.
Existing textbook-correction and audit changes were present and preserved.

## Scope

September 10 continuation: Ch5 now includes the second meeting after the preserved
opening stop, and a separate Ch8 algebra notebook is available. This record describes
the original opening batch. See the [later revision](full_source_audit.md#relational-foundations-revision)
for the current four-notebook checks and remaining limits.

- Historical entry: [syllabus](../../Intro%20DB/syllabus.md), then
  [Ch1](../../Intro%20DB/ch01.ipynb), [Ch2](../../Intro%20DB/ch02.ipynb), and
  Ch5 opening (`Intro DB/ch05.ipynb`, now local only), in that order.
- Ch1 and Ch2 stop at Chapter Summary; Ch5 stops at First-Meeting Summary and Practice.
  The instructor may stop earlier. These are selected topics, not three full chapters
  to complete before class. No separate Week 1 notebook or new assignment is introduced.
- All student prose is English. Sixteen original diagrams and small synthetic input
  tables support prediction, explanation, checking, and practice. Code is supplied
  for observation; first-day SQL/Python authoring is not required.
- The twelve previous notebooks are preserved in `Intro DB/under_revision/`, not
  deleted. Their banner and folder README state that they are not assigned and that
  their chapter/week/exam labels are historical. Current files use the prescribed
  Elmasri/Navathe chapter numbers; old Ch2 was not simply renamed as new Ch2.
- Calendar, travel week, chapter selection, three exams at 30% each, Class Performance
  at 10%, and the five classroom comparisons are unchanged. Actual exam questions and
  the classroom response system are not delivered in this batch.

## Maintained Sources

The three new guides are maintained under `maintenance/chapters/`:
`ch01_database_introduction`, `ch02_database_architecture`, and `ch05_relational_model`.
`opening_figures.py` maintains the sixteen original figure definitions and uses the
existing font-measured Python renderer. The builder rasterizes them as PNG attachments;
students need no separate image folder or drawing packages.

`repository_config.json` keeps `chapters` and `weeks` as historical old-book metadata;
`current_chapters` identifies the three current selections. Builder destinations are
explicitly separate even where old/new chapter IDs coincide. Both sets are built
before any output is replaced. Syllabus and both navigation READMEs are maintained,
not generated. Unexpected files stop the build without deletion.

New Ch5 code uses explicit NOT NULL for its supplied text identifier declarations.
The existing ER mapping schema's NULL-key defect remains open in the old materials;
it is not reused or claimed fixed by this release. Existing completed old-book SQL
corrections and their scoped records are preserved with their sources and generated
copies, not represented as full verification against the prescribed book.

## Source Correspondence

Prescribed private PDF: `private_references/book_Fundamental of Database Systems.pdf`.
SHA-256: `002eceecdb5e47b050e61b30d13a8f207fb44cea4f927b98d864308c026288a5`.
The PDF remains ignored and untracked. The book's official slides have not been
obtained; no slide-reading claim is made. The other book's historical audits remain
historical evidence only.

The locators below refer to inspected body passages, including the earlier bounded
reads documented in the correspondence record and the further reads for this batch.
This is **source checking of taught selections, not complete chapter auditing**.
Exercises use new synthetic examples, not copied textbook solutions.

| Current guide section | Prescribed source, printed page / one-based PDF page | Adaptation, example, and check |
|---|---|---|
| Ch1 1: Data, Software, and a Database System | 1.1-1.2, pp.4-7 / 35-38; Fig.1.1 p.7 / 38 | Original request/DBMS/data diagram; locate email versus request-processing software; distinguish embedded SQLite from a separate server. |
| Ch1 2: Two Files Can Disagree | 1.6.1, pp.17-19 / 48-50; 1.6.8 p.21 / 52 | Two emails for S101; outside confirmation is stated, not inferred from a majority or a DBMS. Practice asks what evidence remains missing. |
| Ch1 3: The Catalog Describes the Data | 1.3.1, pp.10-11 / 41-42; Fig.1.3 | Simplified attribute/type metadata beside a stored row; do not equate type validity with factual correctness. |
| Ch1 4: Different Users Need Different Views | 1.3.3, p.13 / 44 and Fig.1.5 p.14 / 45 | Three synthetic students produce a contact list and IM=2/FIN=1 summary. A view illustration does not enforce permissions. |
| Ch1 5: Sharing Still Needs Rules | 1.3.4 pp.13-14 / 44-45; 1.6.2 p.19 / 50; 1.6.8 p.21 / 52 | Stated contact-officer/summary-reader policy, permitted versus prohibited requests, and factual-validation limit. No account implementation or concurrency algorithm required. |
| Ch2 1: A Model Describes What We Represent | 2.1.1, pp.32-33 / 63-64 | Conceptual fact, relational pair, explicitly invented storage location. The concept panel is not claimed to be an ER diagram. |
| Ch2 2: Schema and Database State | 2.1.2, pp.34-35 / 65-66; 5.1.1 p.152 / 183 | Insert, value correction, ADD COLUMN. Exact row/attribute outputs are checked. Use database state; explain the alternative instance terminology. |
| Ch2 3: Three Schema Levels | 2.2.1, pp.36-37 / 67-68; Fig.2.2 | External/conceptual/internal descriptions linked by mappings; not three data copies. Real systems need not expose three explicit components. |
| Ch2 4: Data Independence Has Conditions | 2.2.2, pp.37-38 / 68-69 | Preserved external contact view after conceptual split versus unchanged conceptual schema after internal access change. Diagram-based conditions, not measured performance or proof for every application. |
| Ch2 5: Database Languages Express Different Requests | 2.3.1, pp.39-40 / 70-71 | DDL/DML request comparison; retrieval does not redefine a table. Supplied syntax is illustrative, not a first-day writing exercise. |
| Ch2 6: Client/Server and Embedded Databases | 2.5, pp.46-49 / 77-80; SQLite source below | Separate client/server processes versus Python calling SQLite in-process. Distinguish architecture from memory/file persistence. |
| Ch5 1: Read One Student Table | 5.1-5.1.1, pp.150-153 / 181-184; Fig.5.1 | Original four-row/four-attribute table and annotated tuple/value diagram. SQL set-versus-bag limit stated; code checks 4 tuples, 4 attributes. |
| Ch5 2: A Domain Is More Than This Sample | 5.1.1 p.151 / 182; 5.2.1 p.158 / 189 | Whole credits 1-6; observed 2/3 does not exclude allowed 5. Reject 2.5 and 7 under the stated domain, not solely a declared SQLite type. |
| Ch5 3: One Phone Value at a Time | 5.1.2 p.155 / 186; adjacent atomicity definitions | Two phones for S101, one for S102, three distinct associations. Atomicity is relative to the model. Full normalization/mapping is not taught here. |
| Ch5 4: Display Order and Repeated Values | 5.1.2 pp.154-155 / 185-186, Figs.5.2-5.3 | Reversed IDs, repeated IM values, DISTINCT result, unchanged stored row count. Attribute-value correspondence must remain intact. |
| Ch5 5: Why Identifiers Matter | 5.2.2 pp.158-159 / 189-190, prerequisite motivation only | Two verified distinct students named Kai Wu; one ID rule. Do not infer universal uniqueness from the sample. Formal key definitions deferred. |

The relevant opening passages were read, not only their contents headings. Additional
Ch1 benefits at pp.20-23 / PDF 51-54 were inspected for limits, not all assigned.
Ch5 pp.150-159 / PDF 181-190 were inspected, including relevant figures in extracted
text; any separate visual source-figure checks are recorded below. No original
textbook figure is distributed. Complete prescribed-book chapter audits remain zero.

Implementation references inspected September 8:
[SQLite serverless architecture](https://www.sqlite.org/serverless.html),
[in-memory databases](https://www.sqlite.org/inmemorydb.html), and
[CREATE TABLE constraints](https://www.sqlite.org/lang_createtable.html).
SQLite-specific behavior is not attributed to the textbook's generic SQL descriptions.

## Verification and Publication

The first-meeting selections are source-checked, built, executed, and locally rendered.
They have not been instructor-reviewed or tested with a class. Complete prescribed-book
chapter audits remain zero. No earlier report's pass substitutes for these checks.

Environment: Windows, Python 3.12.9, SQLite 3.45.3, nbformat 5.10.4, nbclient 0.10.4,
ipykernel 7.2.0, markdown-it-py 4.0.0, resvg-py 0.5.0, Pillow 12.1.1, and PyMuPDF
1.27.2.2. Browser previews use Playwright with installed Google Chrome.
Commands below run from the course root; `python` means the recorded Python runtime.

| Command | Result and scope |
|---|---|
| `git fetch origin` and `git rev-list --left-right --count HEAD...origin/main` | Start matched the remote, 0 ahead / 0 behind; existing work preserved. |
| `python maintenance/course_repository/build_course_repository.py --verify` | PASS: 15 notebooks built and executed by the builder, manifest/content checks passed; 17 public course files including both maintained Markdown files. |
| `python maintenance/course_repository/test_repository_layout.py` | PASS: 16 tests, including layout, assessment, chapter labels, raw notebook schema, examples, and failure-preservation behavior. |
| `python maintenance/course_repository/verify_first_meeting.py` | PASS: exact source-to-notebook rebuild comparison, three fresh kernels, three teaching code cells, 16 images, 32 relative links, independent small-data checks, and both actual Ch5 DDL declarations rejecting NULL and duplicate identifiers. Ch1 has no teaching code cells; its fresh kernel is not an SQL test. |
| `node maintenance/course_repository/render_first_meeting.cjs` | PASS: home, syllabus, and all three new notebooks at 1440 and 390 pixels; no broken images, page overflow, or overflowing text. All 16 figure geometry checks passed. |
| `python maintenance/chapters/ch02_relational_model/instructor/verify_week1.py` | PASS for the preserved old notebook's seven demonstrations and meeting boundaries; not the current first-meeting source audit. |
| `python maintenance/chapters/ch02_relational_model/instructor/verify_ch02.py` | PASS for existing relational-model SQL corrections, including key NULL rejection and whole-number credit constraints. |
| `python maintenance/chapters/ch03_introduction_to_sql/instructor/verify_ch03.py` | PASS for existing SQL corrections and counterexamples, including empty aggregates, LIKE, NULL, and EXISTS. |
| `python maintenance/student_sqlite_package/build_package.py --verify` | PASS: fresh extraction, manifest hashes, and all 10 packaged activities; repeated builds produced the same ZIP hash. This is historical material and does not test every failure case. |
| `git check-ignore` for private references and local QA outputs; `git ls-files private_references` | PASS: private book and QA outputs remain ignored; private references have no tracked files. |

Notebook SHA-256 values (generated UTF-8/LF files):

| File | SHA-256 |
|---|---|
| `Intro DB/ch01.ipynb` | `f83b8f38453f35c8d4544db6217cdeab68ba08c172e4deefac89c387fba8e71a` |
| `Intro DB/ch02.ipynb` | `1bc98960038340e60ceae2f79da3bdb8a92ac16f66687bea4a6c4f479ddcbe85` |
| `Intro DB/ch05.ipynb` | `677313d40c55b4cd596925a66142e7c79aa1629aa7736c2f6728750ce2d81faf` |

Historical ZIP SHA-256:
`9aebdf1c8f48e68909bc8200fa0f208fb5f0553950aa13d30e0ab06d235aaa30`.
An additional Python `zipfile`/`hashlib` check compared its complete membership to the
18-source allow-list plus README, runner, and manifest. Every copied source matched
byte-for-byte. The 21 files contain no PDF, instructor file, cache, or prebuilt database.
The approved PNG/SVG teaching diagrams remain included.

Manual visual inspection covered the local home preview, the original request/DBMS,
three-schema, client/server versus embedded, and tuple/attribute figures. Private PDF
pages 38, 67, and 184 were rendered and inspected to check the corresponding source
figures; none is included in published course material. The official calendar PDF
was downloaded again from the syllabus link, its first page extracted and visually
inspected: September 7 opening, November 2-6 midterms, December 31 make-up holiday,
and January 4-8 finals match the maintained schedule. The web reader timed out for
the PDF, but direct retrieval succeeded. These checks do not establish remote GitHub
rendering; that is checked separately after the authorized push.

Failures found and resolved during verification:

- The new verification helper initially passed a raw list-valued notebook source to
  nbclient. Loading through `nbformat.reads` fixed the helper; fresh-kernel checks then
  passed. This was not a failure of a teaching SQL example.
- An ad hoc ZIP suffix check initially omitted the already approved PNG/SVG files.
  Checking the actual allow-list and supported image types resolved that test error;
  no package source was removed or newly approved.
- Final wording review corrected the logical-independence explanation, changed Ch5's
  prediction prompt from three to four outputs, and described its supplied code as
  creating and printing the table. Sources were rebuilt, fresh-kernel checked, and
  rendered again after these changes.

Publication is authorized to the existing `origin/main`, without force, history
rewriting, or a new remote. Git history records the resulting commit; the delivery
message records its hash and remote verification. Local render files and source-page
images stay in ignored output directories, not in the public commit.
Before committing, `git diff --cached --check` passed. A pattern-based scan of the
54 staged files found no private-reference PDF, prebuilt database, QA output, or
credential pattern; the three staged notebook hashes matched those above. Such a
scan is not proof that every possible sensitive value has been detected.

## Remaining Work

Only the selected first-meeting content is delivered in this batch. Ch5's formal
keys/constraints and the following chapter selections still need development and
source checks. The prior ER schema defect remains a correctness blocker before
reassigning that material. This batch does not establish whole-course readiness,
teacher review, actual student workload, or full-book source auditing.
