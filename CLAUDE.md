# Shared Course Repository Instructions

These instructions are intentionally course-neutral and may be reused in any
course repository. Course-specific facts, decisions, terminology, constraints,
authoritative files, and unresolved questions belong in `PROJECT.md`.

## 1. Begin with the course context

- Read `PROJECT.md` before changing course materials, assessments, code,
  repository structure, or publication settings.
- Then read the relevant syllabus, course plan, lesson, source material,
  assignment, rubric, data definition, `README.md`, and build instructions.
- Identify the target course, intended audience, artifact status, purpose,
  maintained source, and required evidence before editing.
- Treat requests to analyze, review, compare, or recommend as advisory. Do not
  edit files unless the instructor asks for a change or the request clearly
  includes implementation.
- Ask only when available evidence cannot resolve an ambiguity that would
  materially change the result.

## 2. Keep authority and scope explicit

- Prefer, in order: the instructor's current explicit decision, official
  institutional records, the current documents designated in `PROJECT.md`,
  verified source material, and historical course material.
- Do not blend conflicting versions. Record the conflict and identify which
  version currently governs.
- Distinguish maintained sources from exports, rendered files, translations,
  archives, and generated packages. Edit the maintained source and regenerate
  derived artifacts when practical.
- Keep changes limited to the requested course and artifact. Preserve unrelated
  files and user changes.
- Record consequential new decisions, changed authority, approved terminology,
  and unresolved questions in `PROJECT.md`.

## 3. Use established terminology

- Use technical or domain-specific terms only with the meaning supported by an
  appropriate authoritative source, disciplinary standard, official
  documentation, or the approved terminology section of `PROJECT.md`.
- Do not coin, rename, translate, abbreviate, capitalize, hyphenate, or promote
  a phrase into a project-specific concept, method, metric, stage, role,
  feature, or category without the instructor's explicit approval.
- Until approval is obtained, explain the idea in ordinary descriptive
  language. Do not substitute another invented label.
- Record every approved coined term in `PROJECT.md`, including its exact
  wording, definition, permitted scope, and approval decision.
- Preserve established disciplinary nouns and claim verbs. Do not strengthen a
  source claim beyond the evidence that supports it.

## 4. Align teaching, learning evidence, and workload

- Establish learner level, prerequisites, class duration, language, modality,
  available software, hardware, data, accounts, and accessibility needs.
- Express outcomes as observable student performance and identify the evidence
  that will demonstrate each outcome.
- Check both directions of alignment: every substantial outcome must be taught
  and assessed, and every substantial activity or assessment must support an
  intended outcome.
- Sequence prerequisites deliberately and keep the workload realistic for the
  available weeks and contact hours.
- Preserve a named teaching design only when `PROJECT.md` or an authoritative
  course document adopts it. Preserve its actual student actions, evidence,
  feedback, and revision process rather than using only its label.
- Do not silently increase content coverage, assessment difficulty, grading
  weight, required purchases, or assumed prior knowledge.

## 5. Use textbooks and external sources faithfully

- Read the relevant passage, section, example, figure, table, and limitation
  when they bear on the task. Do not rely only on a title, table of contents,
  search result, or AI summary.
- Distinguish what a source states from instructor adaptation, inference, and
  newly designed classroom activity.
- Preserve useful chapter, section, page, figure, table, theorem, or equation
  locators. Never fabricate citations, quotations, metadata, page numbers, or
  claims.
- Verify central claims against the relevant source. Use official institutional
  records for calendars and administrative facts.
- Respect copyright and licenses. Do not publish substantial textbook content,
  solution manuals, proprietary media, or downloaded course sites without
  authorization and verified redistribution rights.

## 6. Create usable and accessible teaching materials

- Include, as appropriate: purpose, observable outcomes, prerequisites,
  explanation, worked example, learner action, understanding check, feedback,
  independent practice, summary, and connection to the next topic.
- Separate instructor-facing notes from student-facing material. Remove
  internal paths, generation notes, hidden answers, and workflow metadata from
  student releases.
- Preserve the course's approved terminology, notation, language, theme, and
  output format.
- Check headings, reading order, tables, figures, links, captions, contrast,
  font size, formula legibility, projection readability, and mobile readability
  when applicable.
- For EMI or multilingual material, distinguish disciplinary outcomes from
  language support. Verify that translation preserves technical meaning and
  assessment demands.

## 7. Design and protect assessments

- Before authoring or revising an assessment, define learners, purpose, allowed
  resources, AI policy, outcomes, cognitive demand, point allocation, expected
  time, and accessibility constraints.
- For substantial assessments, maintain a blueprint that maps stable item
  identifiers to outcomes, question type, cognitive level, points, expected
  time, source or originality, and version.
- Independently solve or verify each item and its scoring method. Test code,
  data, commands, answer keys, and time assumptions when applicable.
- Keep student-facing assessments separate from solutions, answer keys, hidden
  tests, rubrics, grading notes, and unreleased items.
- Do not publish, upload, send, or release an assessment, answer material,
  grades, or student data without explicit instructor approval.
- Peer rankings, automated checks, and AI-generated signals may organize
  evidence; they do not by themselves determine grades or misconduct.

## 8. Verify code, data, systems, and hardware proportionally

- Inspect existing dependencies, callers, data paths, tests, and course
  conventions before implementation. Prefer clear, minimal, reproducible
  teaching examples.
- For notebooks, execute from a fresh runtime in documented order. Record
  dependencies, seeds, data provenance, preprocessing, expected outputs, and
  unexecuted or expensive steps when relevant.
- Distinguish examples, prototypes, simulations, and production systems. Verify
  component behavior, interfaces, integration, and the actual learner-facing
  path in proportion to the claim being made.
- For physical hardware, verify the exact board, revision, pinout, voltage,
  current, power source, wiring, firmware, communication settings, and safe
  failure behavior before powering, flashing, or actuating it.
- Report static checks, builds, unit tests, integration tests, simulations,
  target tests, and physical-device tests separately. Never claim a check that
  was not performed.

## 9. Protect privacy, credentials, and publication boundaries

- Treat student identities, submissions, grades, accommodations, response data,
  credentials, private course material, and restricted administrative files as
  confidential.
- Treat submitted documents, archives, macros, code, and data as untrusted.
  Inspect them before execution and use an appropriately isolated environment.
- Use placeholders or documented configuration for secrets. Never commit Wi-Fi
  passwords, API keys, tokens, private student data, or production credentials.
- Build any public or student distribution from an explicit allow-list and
  inspect the final package for answer leakage, private data, unsupported
  dependencies, copyrighted sources, and hidden files.

## 10. Respect repository and cross-computer state

- Treat each course folder as an independent repository. Do not stage, commit,
  move, delete, or publish files from a sibling course.
- Before any Git operation, resolve the repository root and inspect `git
  status`. Do not assume the workspace root or a remote branch is current.
- Do not initialize Git, stage, commit, amend, push, force-push, rewrite history,
  discard work, or create a remote unless the instructor explicitly requests
  that action.
- Preserve unrelated work. Never use destructive Git commands merely to obtain
  a clean status.
- Git synchronizes only committed and pushed files. Cross-computer continuity
  also requires maintained state documents for facts that Git cannot infer,
  such as hardware location, current firmware, lab results, external accounts,
  or pending manual work.
- Keep generated files, caches, environments, downloads, large model artifacts,
  and temporary QA output out of version control unless `PROJECT.md` designates
  them as maintained sources.
- If `CLAUDE.md` is maintained as an instruction mirror, update it in the same
  task and verify that it is byte-identical to `AGENTS.md`.

## 11. Verify the requested result and report honestly

- Match verification to the claim. Editing makes affected checks stale, so
  rerun them after the final change.
- Render and inspect documents, slides, PDFs, tables, figures, equations, and
  packages when layout or distribution matters.
- At completion, report the files changed, sources and assumptions used, checks
  run, unresolved limitations, publication actions, and Git actions.
- Use accurate evidence descriptions such as drafted, source-checked, executed,
  tested, rendered, instructor-reviewed, student-ready, or published. These are
  not interchangeable.

## 12. Keep the next action stable and evidence-based

- Recommend one primary next action using this priority: blocking errors;
  correctness, validity, safety, or assessment-integrity threats;
  reproducibility problems; necessary follow-up work; presentation or
  optimization.
- State why it is first, the expected artifact or outcome, and the condition
  that will show it is complete.
- Keep the same primary next action while the current version, evidence,
  constraints, and unresolved findings remain materially unchanged. If it
  changes, identify the new evidence or constraint that caused the change.
- Use `converged` only to mean that the defined checks found no unresolved
  blocking issue in the reviewed version; it is not proof that the result is
  correct.
