from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote


SOURCE_DIR = Path(__file__).resolve().parent
COURSE_ROOT = SOURCE_DIR.parents[1]
CONFIG_PATH = SOURCE_DIR / "repository_config.json"
SQLITE_CONFIG_PATH = SOURCE_DIR.parent / "student_sqlite_package" / "package_files.json"
SQLITE_RUNNER_PATH = SOURCE_DIR.parent / "student_sqlite_package" / "run_labs.py"
OUTPUT_DIR = SOURCE_DIR / "output"
PREVIEW_DIR = OUTPUT_DIR / "database_student_repository"
MANIFEST_PATH = OUTPUT_DIR / "student_repository_manifest.json"

TEXT_SUFFIXES = {".md", ".sql", ".py", ".json", ".svg", ".txt"}
CJK_PATTERN = re.compile(
    "["
    "\u3000-\u303f"
    "\u3040-\u30ff"
    "\u3400-\u4dbf"
    "\u4e00-\u9fff"
    "\uac00-\ud7af"
    "]"
)
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FORBIDDEN_TEXT_PATTERNS = {
    "internal working path": re.compile(r"working_materials", re.IGNORECASE),
    "instruction file": re.compile(r"\b(?:AGENTS|CLAUDE|PROJECT)\.md\b", re.IGNORECASE),
    "coverage record": re.compile(r"coverage_and_verification", re.IGNORECASE),
    "instructor audit": re.compile(r"pre_instructor_review", re.IGNORECASE),
    "internal teaching label": re.compile(r"\bType\s*B\b|\bTypeB\b", re.IGNORECASE),
    "Windows local path": re.compile(r"[A-Za-z]:\\"),
}
FORBIDDEN_NAME_PATTERN = re.compile(
    r"(?:answer|solution|grading|coverage|verification|instructor|teacher|__pycache__|\.pyc$|\.db$)",
    re.IGNORECASE,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_source(relative: str) -> Path:
    source = (COURSE_ROOT / relative).resolve()
    if not source.is_relative_to(COURSE_ROOT.resolve()) or not source.is_file():
        raise FileNotFoundError(f"Missing or unsafe source: {relative}")
    return source


def safe_target(root: Path, relative: str) -> Path:
    parts = PurePosixPath(relative).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"Unsafe target: {relative}")
    target = root.joinpath(*parts).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"Target escapes preview directory: {relative}")
    return target


def safe_remove_preview() -> None:
    resolved = PREVIEW_DIR.resolve()
    if not resolved.is_relative_to(OUTPUT_DIR.resolve()) or resolved == OUTPUT_DIR.resolve():
        raise ValueError(f"Refusing to remove unexpected directory: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def copy_file(source: Path, relative_target: str, seen: set[str]) -> None:
    normalized = PurePosixPath(relative_target).as_posix()
    if normalized in seen:
        raise ValueError(f"Duplicate target: {normalized}")
    target = safe_target(PREVIEW_DIR, normalized)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    seen.add(normalized)


def write_text(relative_target: str, content: str, seen: set[str]) -> None:
    normalized = PurePosixPath(relative_target).as_posix()
    if normalized in seen:
        raise ValueError(f"Duplicate target: {normalized}")
    target = safe_target(PREVIEW_DIR, normalized)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    seen.add(normalized)


def validate_config(config: dict) -> None:
    weeks = config["weeks"]
    numbers = [week["week"] for week in weeks]
    if numbers != list(range(1, 19)):
        raise ValueError(f"Weeks must be ordered 1 through 18; received {numbers}")

    chapter_targets = {item["target"] for item in config["chapter_readings"]}
    if len(chapter_targets) != len(config["chapter_readings"]):
        raise ValueError("Chapter reading targets must be unique")
    for target in chapter_targets:
        parts = PurePosixPath(target).parts
        if len(parts) != 3 or parts[0] != "chapters" or parts[2] != "README.md":
            raise ValueError(f"Chapter guide must target chapters/<chapter>/README.md: {target}")

    for week in weeks:
        for key in ("date", "title", "materials", "coverage"):
            if key not in week:
                raise KeyError(f"Week {week['week']} is missing {key}")
        for material in week["materials"]:
            if material["path"] not in chapter_targets:
                raise ValueError(
                    f"Week {week['week']} links an unknown chapter guide: {material['path']}"
                )


def render_schedule(config: dict) -> str:
    lines = [
        "# Course Schedule",
        "",
        "The schedule identifies the chapter and coverage for each week. A chapter guide may",
        "be used for more than one week; continue with the coverage listed in the table instead",
        "of looking for a separate weekly document.",
        "",
        "| Week | Date | Topic, material, and coverage |",
        "|---:|---|---|",
    ]
    for week in config["weeks"]:
        if week["materials"]:
            materials = ", ".join(
                f"[{item['label']}]({item['path']})" for item in week["materials"]
            )
        else:
            materials = "None"
        lines.append(
            f"| {week['week']} | {week['date']} | **{week['title']}**<br>"
            f"Material: {materials}<br>Coverage: {week['coverage']} |"
        )
    lines.extend(
        [
            "",
            "The [course syllabus](SYLLABUS.md) governs assessment, attendance, and course",
            "requirements. The [chapter index](chapters/README.md) explains the shared SQLite",
            "environment and links every selected chapter.",
            "",
            "[Back to the repository home](README.md)",
        ]
    )
    return "\n".join(lines)


def package_target_to_chapter(target: str) -> str:
    parts = PurePosixPath(target).parts
    if len(parts) < 3 or parts[0] != "materials":
        raise ValueError(f"SQLite package target does not begin with materials/: {target}")
    return PurePosixPath("chapters", *parts[1:]).as_posix()


def build_preview(config: dict, sqlite_config: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_remove_preview()
    PREVIEW_DIR.mkdir(parents=True)
    seen: set[str] = set()

    copy_file(SOURCE_DIR / "student_home.md", "README.md", seen)
    copy_file(safe_source(config["syllabus_source"]), "SYLLABUS.md", seen)
    copy_file(SOURCE_DIR / "chapters_README.md", "chapters/README.md", seen)
    copy_file(SQLITE_RUNNER_PATH.resolve(), "run_labs.py", seen)

    for item in config["chapter_readings"]:
        copy_file(safe_source(item["source"]), item["target"], seen)
    for item in sqlite_config["files"]:
        copy_file(
            safe_source(item["source"]),
            package_target_to_chapter(item["target"]),
            seen,
        )

    write_text("SCHEDULE.md", render_schedule(config), seen)

    public_gitignore = """databases/
**/__pycache__/
**/*.pyc
**/*.db
.DS_Store
"""
    write_text(".gitignore", public_gitignore, seen)


def write_manifest(config: dict) -> list[dict]:
    files = []
    for path in sorted(PREVIEW_DIR.rglob("*")):
        if not path.is_file():
            continue
        files.append(
            {
                "path": path.relative_to(PREVIEW_DIR).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    manifest = {
        "repository_name": config["repository_name"],
        "repository_version": config["repository_version"],
        "content_status": "Local student-facing preview; not published",
        "files": files,
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return files


def verify_manifest(files: list[dict]) -> None:
    listed = {item["path"]: item for item in files}
    actual = {
        path.relative_to(PREVIEW_DIR).as_posix()
        for path in PREVIEW_DIR.rglob("*")
        if path.is_file()
    }
    if actual != set(listed):
        raise RuntimeError(
            f"Manifest mismatch; missing={sorted(set(listed) - actual)}, "
            f"unexpected={sorted(actual - set(listed))}"
        )
    for relative, item in listed.items():
        path = safe_target(PREVIEW_DIR, relative)
        if path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            raise RuntimeError(f"Manifest verification failed: {relative}")


def text_files(root: Path) -> list[Path]:
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and (path.suffix.lower() in TEXT_SUFFIXES or path.name == ".gitignore")
    ]


def markdown_heading_slugs(path: Path) -> set[str]:
    slugs: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*$", line)
        if not match:
            continue
        heading = re.sub(r"[`*_~]", "", match.group(1)).lower()
        heading = re.sub(r"[^a-z0-9\s-]", "", heading)
        slug = re.sub(r"\s+", "-", heading.strip())
        if slug:
            slugs.add(slug)
    return slugs


def verify_student_content(config: dict, sqlite_config: dict) -> None:
    errors: list[str] = []
    markdown_count = 0
    for path in text_files(PREVIEW_DIR):
        relative = path.relative_to(PREVIEW_DIR).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            errors.append(f"UTF-8 decode failure in {relative}: {error}")
            continue
        if "\ufffd" in content:
            errors.append(f"Replacement character in {relative}")
        if CJK_PATTERN.search(content):
            errors.append(f"Non-English CJK text in {relative}")
        for label, pattern in FORBIDDEN_TEXT_PATTERNS.items():
            if pattern.search(content):
                errors.append(f"{label} in {relative}")
        if path.suffix.lower() == ".md":
            markdown_count += 1
            if len(re.findall(r"(?m)^```", content)) % 2:
                errors.append(f"Unbalanced code fence in {relative}")
            for match in LINK_PATTERN.finditer(content):
                target_text = match.group(1).strip()
                if target_text.startswith("<") and target_text.endswith(">"):
                    target_text = target_text[1:-1]
                if target_text.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target_parts = target_text.split("#", 1)
                target_without_anchor = unquote(target_parts[0])
                anchor = unquote(target_parts[1]).lower() if len(target_parts) == 2 else ""
                if not target_without_anchor:
                    continue
                target = (path.parent / target_without_anchor).resolve()
                if not target.is_relative_to(PREVIEW_DIR.resolve()) or not target.exists():
                    errors.append(f"Broken local link in {relative}: {target_text}")
                elif anchor and target.is_file() and target.suffix.lower() == ".md":
                    if anchor not in markdown_heading_slugs(target):
                        errors.append(f"Broken heading anchor in {relative}: {target_text}")

    for path in PREVIEW_DIR.rglob("*"):
        if path.is_file() and path.name != ".gitignore" and FORBIDDEN_NAME_PATTERN.search(path.name):
            errors.append(f"Forbidden student-facing filename: {path.relative_to(PREVIEW_DIR).as_posix()}")

    package_markdown_count = sum(
        PurePosixPath(item["target"]).suffix.lower() == ".md"
        for item in sqlite_config["files"]
    )
    expected_markdown_count = 4 + len(config["chapter_readings"]) + package_markdown_count
    if markdown_count != expected_markdown_count:
        errors.append(f"Expected {expected_markdown_count} Markdown files, found {markdown_count}")
    if (PREVIEW_DIR / "course").exists() or (PREVIEW_DIR / "resources").exists():
        errors.append("Obsolete weekly or resources directory remains in the preview")
    if not (PREVIEW_DIR / "SCHEDULE.md").is_file():
        errors.append("Missing SCHEDULE.md")
    for item in config["chapter_readings"]:
        if not safe_target(PREVIEW_DIR, item["target"]).is_file():
            errors.append(f"Missing chapter guide: {item['target']}")
    if errors:
        raise RuntimeError("Student-content verification failed:\n- " + "\n- ".join(errors))
    print(f"STUDENT_TEXT_VERIFICATION=PASS MARKDOWN_FILES={markdown_count}")


def verify_labs() -> None:
    with tempfile.TemporaryDirectory(prefix="database_student_repository_") as temp:
        temp_root = Path(temp) / "database_student_repository"
        shutil.copytree(PREVIEW_DIR, temp_root)
        runner = temp_root / "run_labs.py"
        result = subprocess.run(
            [sys.executable, str(runner), "all"],
            cwd=temp_root,
            text=True,
            capture_output=True,
            check=False,
        )
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        if result.returncode != 0:
            raise RuntimeError(f"Student repository lab verification failed with exit code {result.returncode}")
    print("CLEAN_STUDENT_REPOSITORY_LABS=PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Database Management student repository preview.")
    parser.add_argument("--verify", action="store_true", help="verify content, links, manifest, and labs")
    args = parser.parse_args()

    config = load_json(CONFIG_PATH)
    sqlite_config = load_json(SQLITE_CONFIG_PATH)
    validate_config(config)
    build_preview(config, sqlite_config)
    files = write_manifest(config)
    print(f"BUILT_FILES={len(files)}")
    print(f"PREVIEW_DIR={PREVIEW_DIR}")
    print(f"MANIFEST_PATH={MANIFEST_PATH}")
    if args.verify:
        verify_manifest(files)
        print("STUDENT_REPOSITORY_MANIFEST=PASS")
        verify_student_content(config, sqlite_config)
        verify_labs()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
