from __future__ import annotations

import argparse
from html import escape
from pathlib import Path


WIDTH = 1200


def _text(
    x: int,
    y: int,
    value: str,
    *,
    size: int = 22,
    weight: int = 400,
    fill: str = "#17212b",
    anchor: str = "start",
) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}">{escape(value)}</text>'
    )


def _arrow(x1: int, y1: int, x2: int, y2: int, label: str = "") -> str:
    items = [
        f'<path d="M {x1} {y1} L {x2} {y2}" stroke="#52606d" '
        'stroke-width="3" fill="none" marker-end="url(#arrow)"/>'
    ]
    if label:
        items.append(
            _text(
                (x1 + x2) // 2,
                (y1 + y2) // 2 - 10,
                label,
                size=16,
                weight=600,
                fill="#364152",
                anchor="middle",
            )
        )
    return "\n".join(items)


def _table(
    x: int,
    y: int,
    width: int,
    title: str,
    rows: list[tuple[str, str]],
    color: str,
) -> tuple[str, int]:
    header_height = 50
    row_height = 34
    height = header_height + row_height * len(rows) + 12
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="6" '
        'fill="#ffffff" stroke="#52606d" stroke-width="2"/>',
        f'<rect x="{x}" y="{y}" width="{width}" height="{header_height}" rx="6" '
        f'fill="{color}"/>',
        _text(x + 16, y + 34, title, size=24, weight=700, fill="#ffffff"),
    ]
    for index, (role, field) in enumerate(rows):
        baseline = y + header_height + 27 + index * row_height
        if index:
            line_y = y + header_height + index * row_height
            parts.append(
                f'<line x1="{x}" y1="{line_y}" x2="{x + width}" y2="{line_y}" '
                'stroke="#d9e2ec" stroke-width="1"/>'
            )
        parts.append(_text(x + 14, baseline, role, size=15, weight=700, fill="#52606d"))
        parts.append(_text(x + 68, baseline, field, size=18))
    return "\n".join(parts), height


def _svg(title: str, height: int, content: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title description">
  <title id="title">{escape(title)}</title>
  <desc id="description">Original instructional diagram for the Database Management course.</desc>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#52606d"/>
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#f7f9fb"/>
  {content}
</svg>
'''


def ch02_relational_schema() -> str:
    """Draw the synthetic course-registration relational schema."""
    department, _ = _table(
        55,
        85,
        300,
        "department",
        [("PK", "dept_code"), ("", "dept_name"), ("", "building")],
        "#147d80",
    )
    student, _ = _table(
        55,
        390,
        330,
        "student",
        [("PK", "student_id"), ("CK", "email"), ("", "student_name"), ("FK", "dept_code")],
        "#2864a6",
    )
    course, _ = _table(
        835,
        85,
        310,
        "course",
        [("PK", "course_id"), ("", "title"), ("FK", "dept_code"), ("", "credits")],
        "#a65f16",
    )
    enrollment, _ = _table(
        430,
        390,
        355,
        "enrollment",
        [
            ("PK/FK", "student_id"),
            ("PK/FK", "course_id"),
            ("PK", "term"),
            ("", "grade"),
        ],
        "#8c4f83",
    )
    content = "\n".join(
        [
            _text(55, 43, "Course-Registration Relational Schema", size=30, weight=700),
            _text(
                55,
                68,
                "Arrow direction: foreign key in the referencing table to a key in the referenced table",
                size=17,
                fill="#52606d",
            ),
            department,
            student,
            course,
            enrollment,
            _arrow(220, 390, 220, 265, "student.dept_code"),
            '<path d="M 835 220 L 755 220 L 755 145 L 355 145" stroke="#52606d" stroke-width="3" fill="none" marker-end="url(#arrow)"/>',
            _text(555, 132, "course.dept_code", size=16, weight=600, fill="#364152", anchor="middle"),
            _arrow(430, 462, 385, 462),
            _text(407, 372, "enrollment.student_id", size=16, weight=600, fill="#364152", anchor="middle"),
            _arrow(785, 496, 835, 158, "course_id"),
            _text(55, 620, "PK primary key   CK candidate key   FK foreign key", size=17, weight=600),
        ]
    )
    return _svg("Course-registration relational schema", 650, content)


def ch02_table_anatomy() -> str:
    headers = ["student_id", "email", "student_name", "dept_code"]
    rows = [
        ["S101", "an.chen@example.edu", "An Chen", "IM"],
        ["S102", "bea.lin@example.edu", "Bea Lin", "FIN"],
        ["S103", "kai.wu@example.edu", "Kai Wu", "IM"],
        ["S104", "mira.ho@example.edu", "Mira Ho", "DES"],
    ]
    xs = [60, 230, 620, 900, 1140]
    parts = [
        _text(60, 48, "Read One Student Table", size=32, weight=700),
        _text(60, 82, "Synthetic student instance: one row per student; four tuples and four attributes.", size=21),
        _text(60, 122, "Relation name: student", size=22, weight=600),
        '<rect x="60" y="150" width="1080" height="274" fill="white" stroke="#52606d" stroke-width="2"/>',
        '<rect x="60" y="150" width="1080" height="50" fill="#e5edf5"/>',
        '<rect x="900" y="200" width="240" height="224" fill="#f3eef7"/>',
        '<rect x="60" y="312" width="1080" height="56" fill="#e0f2ee"/>',
    ]
    for x in xs[1:-1]:
        parts.append(f'<line x1="{x}" y1="150" x2="{x}" y2="424" stroke="#bec8d1"/>')
    for y in [200, 256, 312, 368]:
        parts.append(f'<line x1="60" y1="{y}" x2="1140" y2="{y}" stroke="#bec8d1"/>')
    for x, header in zip(xs, headers):
        parts.append(_text(x + 16, 183, header, size=23, weight=600))
    for index, row in enumerate(rows):
        for x, value in zip(xs, row):
            parts.append(_text(x + 16, 235 + 56 * index, value, size=22))
    parts.extend([
        '<rect x="55" y="308" width="1090" height="64" fill="none" stroke="#11685a" stroke-width="4"/>',
        '<rect x="896" y="145" width="248" height="284" fill="none" stroke="#75468f" stroke-width="4" stroke-dasharray="10 6"/>',
        _text(60, 478, "Solid outline: one tuple, including all four values for S103.", size=23, weight=600),
        _text(60, 518, "Dashed outline: the dept_code attribute. Their intersection contains IM.", size=23),
        _text(60, 558, "IM is one attribute value; it does not describe the complete student.", size=22),
    ])
    return _svg("Student table: tuple, attribute, and value", 590, "\n".join(parts))


def _mini_relation(
    x: int,
    y: int,
    title: str,
    headers: list[str],
    rows: list[list[str]],
    color: str,
) -> str:
    width = 250
    row_height = 31
    height = 42 + row_height * (len(rows) + 1)
    column_width = width / len(headers)
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="6" fill="#ffffff" stroke="#52606d" stroke-width="2"/>',
        f'<rect x="{x}" y="{y}" width="{width}" height="42" rx="6" fill="{color}"/>',
        _text(x + 12, y + 28, title, size=19, weight=700, fill="#ffffff"),
    ]
    header_y = y + 42
    parts.append(
        f'<rect x="{x}" y="{header_y}" width="{width}" height="{row_height}" fill="#e9eef3"/>'
    )
    for column, header in enumerate(headers):
        center = int(x + column_width * (column + 0.5))
        parts.append(_text(center, header_y + 22, header, size=14, weight=700, anchor="middle"))
    for row_index, row in enumerate(rows):
        baseline = header_y + row_height * (row_index + 1) + 22
        for column, value in enumerate(row):
            center = int(x + column_width * (column + 0.5))
            parts.append(_text(center, baseline, value, size=14, anchor="middle"))
    return "\n".join(parts)


def ch02_algebra_pipeline() -> str:
    """Draw a selection-then-projection relational-algebra pipeline."""
    student = _mini_relation(
        35,
        110,
        "student",
        ["id", "name", "dept"],
        [
            ["S101", "An", "IM"],
            ["S102", "Bea", "FIN"],
            ["S103", "Kai", "IM"],
            ["S104", "Mira", "DES"],
        ],
        "#2864a6",
    )
    selected = _mini_relation(
        475,
        140,
        "selected rows",
        ["id", "name", "dept"],
        [["S101", "An", "IM"], ["S103", "Kai", "IM"]],
        "#147d80",
    )
    projected = _mini_relation(
        915,
        155,
        "result",
        ["student_name"],
        [["An Chen"], ["Kai Wu"]],
        "#a65f16",
    )
    content = "\n".join(
        [
            _text(35, 45, "Relational-Algebra Composition", size=30, weight=700),
            _text(35, 75, "Read the nested expression from the inside out.", size=18, fill="#52606d"),
            student,
            selected,
            projected,
            _arrow(290, 220, 465, 220),
            _arrow(730, 220, 905, 220),
            _text(378, 185, "selection", size=18, weight=700, anchor="middle"),
            _text(378, 255, "dept_code = 'IM'", size=16, anchor="middle"),
            _text(818, 185, "projection", size=18, weight=700, anchor="middle"),
            _text(818, 255, "student_name", size=16, anchor="middle"),
            _text(
                600,
                360,
                "Π_student_name(σ_dept_code='IM'(student))",
                size=23,
                weight=700,
                anchor="middle",
            ),
        ]
    )
    return _svg("Selection and projection pipeline", 400, content)


FIGURE_GENERATORS = {
    "ch02_table_anatomy": ch02_table_anatomy,
    "ch02_relational_schema": ch02_relational_schema,
    "ch02_algebra_pipeline": ch02_algebra_pipeline,
}


def generate_figure(name: str) -> str:
    try:
        return FIGURE_GENERATORS[name]()
    except KeyError as error:
        raise ValueError(f"Unknown figure generator: {name}") from error


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the original notebook SVG figures.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "output" / "figures",
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name in FIGURE_GENERATORS:
        path = args.output_dir / f"{name}.svg"
        path.write_text(generate_figure(name), encoding="utf-8", newline="\n")
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
