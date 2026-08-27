# Chapter 6 Instructor Coverage and Verification

## Artifact status

- Audience: instructor only
- Student guide status: draft, source-checked against the complete Chapter 6 text and
  official Chapter 6 slides
- Case: original course-registration requirements and E-R diagram
- Executable verification: passed again on August 27, 2026, using Python 3.12.9 and
  SQLite 3.45.3
- Diagram rendering: SVG rendered to a 1400 by 900 PNG with headless Chrome; visual
  inspection confirmed readable text, distinct entities, correct connections, no
  overlap, and no clipping
- Publication: not approved

## Source scope checked

- Silberschatz, Korth, and Sudarshan, *Database System Concepts*, 7th Edition,
  Chapter 6, printed pages 241-294, Sections 6.1-6.12. Exercises and tools were
  inspected for chapter context but not copied.
- Official slide deck `from_11001_DB/PowerPoint Presentations/ch6.pdf`, all 83 PDF
  pages.
- Current governance, revised syllabus, chapter-material prompt, existing university
  SQL data, and the completed Chapters 2-5 materials.

## Scope decision

Required instruction covers design phases; redundancy and incompleteness; entities,
attributes, and relationships; complex attributes; roles and degree; cardinality and
participation; keys; weak entities; removing redundant conceptual attributes; mapping
strong/weak entities, complex attributes, and one-to-many/many-to-many relationships;
and core design choices.

Extended E-R features, complete generalization/specialization mapping, aggregation,
alternative E-R notations, UML, workflow, and schema evolution are supplementary.
They are not valid Exam 2 operation or diagram requirements unless separately taught
and practiced.

## Source and notation cautions

1. There is no universal E-R diagram notation. The course diagram uses textbook-style
   rectangles, diamonds, weak-entity double borders, and `min..max` labels.
2. Minimum/maximum labels describe each entity's participation count. Other software,
   especially UML or crow's-foot tools, may place symbols differently; the guide requires
   translating business rules before reading symbols.
3. Primary keys belonging to a related entity should not be repeated as conceptual
   attributes. They may reappear as foreign-key columns after relational mapping.
4. The Section weak-entity choice remains semantically defensible even if a surrogate
   ID could make it technically strong; existence dependency and user meaning matter.
5. A multivalued attribute maps to a separate relation. The generated relation includes
   the owner key and value in its primary key.
6. `CHECK(course_id <> prereq_id)` blocks only a direct self-loop. It does not establish
   acyclicity of the entire recursive relationship.
7. Minimum participation on the referenced/one side is not fully enforceable by a
   foreign key in the other direction. The mapped constraints cover the stated `0..*`
   Department-side minima and the total Student/Course/Section-side participation.
8. The diagram is original and does not reproduce a textbook figure. Its SVG contains
   accessible title/description text and the PNG is a rendered derivative.

## Teaching-point alignment

| ID | Teaching point | Primary source | Worked example | Student action and feedback |
|---|---|---|---|---|
| C6.01 | design phases | 6.1.1, pp. 241-243; slides 6.3-6.4 | Section requirement through phases | Place grade rule in conceptual/logical phases |
| C6.02 | redundancy/incompleteness | 6.1.2, pp. 243-244; slide 6.5 | combined course-section table | Diagnose registration table facts |
| C6.03 | entity/entity set/attribute | 6.2.1, pp. 244-246; slides 6.8-6.11 | S101 and Student | Identify Course instance/set/key |
| C6.04 | relationships and attributes | 6.2.2, pp. 246-249; slides 6.12-6.19 | registers plus grade | Analyze guidance ternary relationship |
| C6.05 | complex attributes | 6.3, pp. 249-252; slides 6.20-6.22 | name, phones, credits | Decide Address/Phone modeling |
| C6.06 | mapping cardinalities | 6.4, pp. 252-256; slides 6.23-6.32 | Department-Student | Determine Course-Section/registers directions |
| C6.07 | total/partial participation | 6.4, pp. 255-256 | required major | Revise for optional major |
| C6.08 | entity and relationship keys | 6.5.1-6.5.2, pp. 256-259; slides 6.33-6.37 | Student and registers | Determine advisor minimal key |
| C6.09 | weak entity | 6.5.3, pp. 259-260; slides 6.38-6.42 | Section owner/discriminator | Evaluate surrogate UUID choice |
| C6.10 | remove redundant attributes | 6.6, pp. 261-264; slides 6.43-6.45 | majors_in versus dept_code | Explain Section course_id mapping |
| C6.11 | map strong/composite entities | 6.7.1-6.7.2, pp. 265-267; slides 6.46-6.48 | Student/name | Map Instructor address/certification |
| C6.12 | map multivalued/derived attributes | 6.7.2, pp. 266-267 | student_phone/credits query | Validate separate relation and calculation |
| C6.13 | map weak entity | 6.7.3, pp. 267-268 | Section composite key | Map weak Assignment |
| C6.14 | map relationship sets | 6.7.4-6.7.6, pp. 268-271; slides 6.49-6.52 | merged majors/offers and enrollment | Redesign multiple majors and prerequisite |
| C6.15 | common design mistakes | 6.9.1, pp. 279-281; slides 6.65-6.67 | redundant department key | Correct multivalued marks |
| C6.16 | entity vs attribute/relationship | 6.9.2-6.9.3, pp. 281-283; slides 6.68-6.69 | Phone and Registration | Evaluate Waitlist identity |
| C6.17 | binary vs n-ary | 6.9.4, pp. 283-285; slides 6.70-6.73 | parent vs project guidance | Preserve complete tuple semantics |

Every required teaching point has explanation, a complete example, student practice, and
a stated checking criterion. Supplementary topics are excluded from Exam 2 until taught.

## Teaching summary

### Week 8

1. Convert four requirements into entities, attributes, and relationships.
2. Diagnose redundancy and incompleteness using sample facts.
3. Classify name, phone, and completed credits.
4. Ask both cardinality directions and then add minimum participation.
5. Determine entity and relationship keys.
6. Model Section as a weak entity and compare a surrogate-key alternative.
7. Draft the E-R diagram and preserve individual reasoning.

### Week 10

1. Review the diagram against every requirement.
2. Remove conceptual foreign-key duplication.
3. Map strong entities, composite attributes, and phone values.
4. Map Section owner/discriminator and its identifying foreign key.
5. Merge total many-to-one relationships and map registers as a separate relation.
6. Execute mapped schema and independent invalid-data tests.
7. Compare a relationship/entity and binary/ternary design choice.
8. Revise the E-R diagram and relational schema after feedback.

## Student-practice guidance

1. Grade is a registration rule in the conceptual schema and a nullable `CHECK` in the
   logical schema.
2. The flattened registration table repeats student and course names and cannot store a
   student/course before registration.
3. Course is the entity set; DB201 is an entity; course ID is a candidate/primary key.
4. Phone becomes an entity when the database needs phone properties, sharing, or
   relationships beyond a value list.
5. Project guidance is ternary when the exact three-way combination matters.
6. Course-Section is one-to-many; registers is many-to-many.
7. Optional major changes Student to `0..1` and makes a merged department foreign key
   nullable.
8. One-advisor-per-student makes student ID the advisor relationship key.
9. A UUID supplies a key but does not by itself remove Section's semantic dependency.
10. Conceptual Section omits course ID; the mapped weak relation includes it as owner
    foreign key and key component.
11. Instructor address components remain columns; certification maps to a separate
    relation keyed by instructor and certification.
12. Weak Assignment key includes the complete Section key plus assignment number.
13. Multiple majors require `student_major(student_id, dept_code)` with a pair key.
14. Prerequisite uses `course_id` and `prereq_id` roles; both reference Course.
15. Waitlist is more defensibly an entity when each request has identity, changing state,
    and its own notification history.

## Verification commands

Render the diagram:

```powershell
node working_materials/chapters/ch06_er_design/instructor/render_ch06_diagram.js
```

Verify the mapped schema and artifacts:

```powershell
py -3 working_materials/chapters/ch06_er_design/instructor/verify_ch06.py
```

## Remaining limits before student release

- The instructor selected English-only student prose on August 27, 2026. The rewritten
  guide still requires final instructor content and language review before publication.
- The course's diagram editor for student submissions is not fixed.
- Classroom workload, projection readability, and accessibility have not been observed
  with actual students.
- `COURSE_PLAN.md` governs Chapter 6 scope, dates, and assessment boundaries.

## Chapter delivery status

- Files created: business rules, student guide, maintained SVG, rendered PNG, mapped
  SQL schema, renderer, instructor record, and verifier.
- Source verification: complete for textbook printed pages 241-294 and all 83 pages
  of the local official slide PDF.
- Executed content: the complete mapped schema and sample data; independent failures
  for candidate keys, parent references, multivalued duplicates, weak-entity ownership,
  registration references, grade domain, and direct prerequisite self-reference; the
  derived-credit query; SVG parsing; PNG rendering and visual inspection.
- Unexecuted content: extended E-R, generalization mapping, aggregation, UML, and other
  alternative notations. These are supplementary.
- Main corrections made: kept foreign keys out of conceptual entities; used explicit
  min/max directions; separated multivalued and derived attributes; preserved weak-
  entity owner semantics; and mapped relationship attributes to the correct relation.
- Progression decision: the chapter meets the source, example, practice, alignment,
  executable-check, and rendered-diagram conditions required to begin Chapter 7. It
  remains a draft until the instructor reviews language, classroom tooling, and workload.
