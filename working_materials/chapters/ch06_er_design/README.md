# Chapter 6: Database Design Using the E-R Model

This folder contains the maintained materials for the two class meetings assigned to
Chapter 6.

## Student-facing files

- `student_guide.md`: self-contained design and mapping guide with worked examples.
- `course_registration_rules.md`: original requirements used for the diagram.
- `course_registration_er.svg`: maintained E-R diagram using entity rectangles,
  relationship diamonds, and minimum/maximum cardinalities.
- `course_registration_er.png`: rendered diagram for environments that do not display
  SVG reliably.
- `mapped_schema.sql`: executable SQLite mapping and sample data.

## Instructor-only files

- `instructor/coverage_and_verification.md`: source locations, alignment, guidance, and
  verification record.
- `instructor/verify_ch06.py`: automated schema, mapping, and constraint checks.
- `instructor/render_ch06_diagram.js`: deterministic headless Chrome renderer for the
  PNG.

## Status

- Maintained source: yes
- Student release status: draft; instructor review still required
- Database used for verification: SQLite through Python 3.12 standard library
- Diagram notation: textbook-style entities/relationships with explicit `min..max`
  labels; no claim of universal E-R notation
- Textbook figures or exercise solutions copied into the student files: none
