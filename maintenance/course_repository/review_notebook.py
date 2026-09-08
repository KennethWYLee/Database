"""Validate notebooks in fresh kernels and render ignored local review HTML."""

import argparse
import copy
import json
from pathlib import Path
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from jupyter_client import KernelManager


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent / "output"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-chapters", action="store_true")
    args = parser.parse_args()
    source = ROOT / "Intro DB/ch02.ipynb"
    raw = json.loads(source.read_text(encoding="utf-8"))
    errors = list(nbformat.validator.iter_validate(raw))
    if errors:
        raise AssertionError("Raw notebook schema: " + "; ".join(e.message for e in errors))
    original = nbformat.read(source, as_version=4)
    start_week2 = next(i for i, cell in enumerate(original.cells)
                      if cell.source.startswith("## Week 2: Keys and Relational Algebra"))
    OUTPUT.mkdir(exist_ok=True)
    selections = [("week1", original, original.cells[:start_week2]),
                  ("week2", original, original.cells[start_week2:]),
                  ("complete-ch02", original, original.cells)]
    if args.all_chapters:
        for path in sorted((ROOT / "Intro DB").glob("ch*.ipynb")):
            if path == source:
                continue
            raw = json.loads(path.read_text(encoding="utf-8"))
            errors = list(nbformat.validator.iter_validate(raw))
            assert not errors, (path.name, errors)
            chapter = nbformat.read(path, as_version=4)
            selections.append(("complete-" + path.stem, chapter, chapter.cells))
    for label, original, selection in selections:
        notebook = copy.deepcopy(original)
        notebook.cells = copy.deepcopy(selection)
        kernel = KernelManager(kernel_name="python3")
        kernel.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
        with tempfile.TemporaryDirectory(prefix="database_review_") as directory:
            NotebookClient(notebook, km=kernel, timeout=60,
                           resources={"metadata": {"path": directory}}).execute(cleanup_kc=True)
        for cell_index, (saved, executed) in enumerate(zip(selection, notebook.cells), start=1):
            if saved.cell_type != "code":
                continue
            old = "".join(o.get("text", "") for o in saved.outputs if o.output_type == "stream")
            new = "".join(o.get("text", "") for o in executed.outputs if o.output_type == "stream")
            assert old == new, (f"{label} cell {cell_index}: preserved output differs from fresh execution\n"
                                f"saved={old!r}\nfresh={new!r}")
            assert not any(o.output_type == "error" for o in executed.outputs)
        print(label, "FRESH_KERNEL_PASS", flush=True)
        if label in {"week1", "week2"}:
            html, _ = HTMLExporter(template_name="lab").from_notebook_node(notebook)
            (OUTPUT / f"{label}_review.html").write_text(html, encoding="utf-8")
    for name, path in [("syllabus", ROOT / "Intro DB/syllabus.md"), ("home", ROOT / "README.md")]:
        notebook = nbformat.v4.new_notebook(cells=[
            nbformat.v4.new_markdown_cell(path.read_text(encoding="utf-8"))
        ])
        html, _ = HTMLExporter(template_name="lab").from_notebook_node(notebook)
        (OUTPUT / f"{name}_review.html").write_text(html, encoding="utf-8")
    print("NOTEBOOK_FORMAT_AND_HTML_PASS")


if __name__ == "__main__":
    main()
