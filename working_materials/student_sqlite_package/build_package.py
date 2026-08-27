from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


SOURCE_DIR = Path(__file__).resolve().parent
COURSE_ROOT = SOURCE_DIR.parents[1]
CONFIG_PATH = SOURCE_DIR / "package_files.json"
OUTPUT_DIR = SOURCE_DIR / "output"
PACKAGE_DIR = OUTPUT_DIR / "sqlite_course_package"
ZIP_PATH = OUTPUT_DIR / "sqlite_course_package.zip"
FIXED_ZIP_TIME = (2026, 8, 27, 0, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_target(root: Path, relative: str) -> Path:
    parts = PurePosixPath(relative).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"Unsafe package target: {relative}")
    target = root.joinpath(*parts).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f"Package target escapes output directory: {relative}")
    return target


def safe_remove_tree(path: Path) -> None:
    resolved = path.resolve()
    if not resolved.is_relative_to(OUTPUT_DIR.resolve()) or resolved == OUTPUT_DIR.resolve():
        raise ValueError(f"Refusing to remove unexpected directory: {resolved}")
    if resolved.exists():
        shutil.rmtree(resolved)


def copy_allowed_files(config: dict) -> list[dict]:
    copied: list[dict] = []
    seen_targets: set[str] = set()
    for item in config["files"]:
        source = (COURSE_ROOT / item["source"]).resolve()
        if not source.is_relative_to(COURSE_ROOT.resolve()) or not source.is_file():
            raise FileNotFoundError(f"Missing or unsafe source: {item['source']}")
        target_name = PurePosixPath(item["target"]).as_posix()
        if target_name in seen_targets:
            raise ValueError(f"Duplicate package target: {target_name}")
        seen_targets.add(target_name)
        target = safe_target(PACKAGE_DIR, target_name)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        copied.append(
            {
                "path": target_name,
                "chapter": item["chapter"],
                "purpose": item["purpose"],
                "bytes": target.stat().st_size,
                "sha256": sha256(target),
            }
        )
    return copied


def write_manifest(config: dict, copied: list[dict]) -> None:
    extra_files = []
    for name in ("README.md", "run_labs.py"):
        path = PACKAGE_DIR / name
        extra_files.append(
            {
                "path": name,
                "chapter": "All",
                "purpose": "Package operating file",
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    manifest = {
        "package_name": config["package_name"],
        "package_version": config["package_version"],
        "minimum_sqlite_version": config["minimum_sqlite_version"],
        "content_status": config["content_status"],
        "files": sorted(extra_files + copied, key=lambda item: item["path"]),
    }
    (PACKAGE_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_zip() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_DIR.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(PACKAGE_DIR).as_posix()
            info = zipfile.ZipInfo(f"sqlite_course_package/{relative}", FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())


def verify_manifest(package: Path) -> None:
    manifest_path = package / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    listed = {item["path"]: item for item in manifest["files"]}
    actual = {
        path.relative_to(package).as_posix()
        for path in package.rglob("*")
        if path.is_file() and path != manifest_path
    }
    if actual != set(listed):
        missing = sorted(set(listed) - actual)
        unexpected = sorted(actual - set(listed))
        raise RuntimeError(f"Manifest mismatch; missing={missing}, unexpected={unexpected}")
    for relative, item in listed.items():
        path = safe_target(package, relative)
        if path.stat().st_size != item["bytes"]:
            raise RuntimeError(f"Manifest byte count mismatch: {relative}")
        if sha256(path) != item["sha256"]:
            raise RuntimeError(f"Manifest hash mismatch: {relative}")


def verify_zip() -> None:
    with tempfile.TemporaryDirectory(prefix="sqlite_course_package_") as temp:
        temp_path = Path(temp)
        with zipfile.ZipFile(ZIP_PATH) as archive:
            archive.extractall(temp_path)
        package = temp_path / "sqlite_course_package"
        verify_manifest(package)
        print("PACKAGE_MANIFEST_VERIFICATION=PASS")
        result = subprocess.run(
            [sys.executable, str(package / "run_labs.py"), "all"],
            cwd=package,
            text=True,
            capture_output=True,
            check=False,
        )
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        if result.returncode != 0:
            raise RuntimeError(f"Clean-package verification failed with exit code {result.returncode}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Database Management SQLite student package.")
    parser.add_argument("--verify", action="store_true", help="extract the ZIP and run all labs")
    args = parser.parse_args()

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_remove_tree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir(parents=True)
    shutil.copyfile(SOURCE_DIR / "student_README.md", PACKAGE_DIR / "README.md")
    shutil.copyfile(SOURCE_DIR / "run_labs.py", PACKAGE_DIR / "run_labs.py")
    copied = copy_allowed_files(config)
    write_manifest(config, copied)
    build_zip()
    print(f"BUILT_FILES={len(copied) + 3}")
    print(f"PACKAGE_DIR={PACKAGE_DIR}")
    print(f"ZIP_PATH={ZIP_PATH}")
    print(f"ZIP_SHA256={sha256(ZIP_PATH)}")
    if args.verify:
        verify_zip()
        print("CLEAN_PACKAGE_VERIFICATION=PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
