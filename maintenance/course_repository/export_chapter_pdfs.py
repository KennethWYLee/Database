"""Export the published notebooks without executing or modifying their cells."""
import base64
from collections import Counter
import html
import json
from pathlib import Path
import re
import subprocess

from bs4 import BeautifulSoup
import fitz
from markdown_it import MarkdownIt
import nbformat
from PIL import Image, ImageDraw

import build_course_repository as builder

OUT = builder.OUTPUT_DIR / "pdf"
MD = MarkdownIt("commonmark", {"html": False}).enable("table")


def make_html(chapter):
    path = builder.safe_target(chapter + ".ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    nbformat.validate(nbformat.from_dict(notebook))
    body, images = [], 0
    for cell in notebook["cells"]:
        source = "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            rendered = MD.render(source)
            for name, mime in cell.get("attachments", {}).items():
                data = mime["image/png"]
                base64.b64decode(data, validate=True)
                rendered = rendered.replace("attachment:" + name, "data:image/png;base64," + data)
                images += 1
            css = "figure-cell" if cell.get("attachments") else "text-cell"
            if source.startswith("## Chapter Summary") or source.startswith("## Textbook Reading"):
                css += " closing-section"
            body.append(f'<section class="{css}">{rendered}</section>')
        elif cell["cell_type"] == "code":
            if cell.get("execution_count") is None:
                raise ValueError(f"Unexecuted cell in {path}")
            body.append('<pre class="code">' + html.escape(source) + '</pre>')
            for output in cell.get("outputs", []):
                if output["output_type"] != "stream":
                    raise ValueError("Unsupported rich output: add an explicit renderer before exporting")
                body.append('<pre class="output">' + html.escape("".join(output["text"])) + '</pre>')
        else:
            raise ValueError("Unsupported notebook cell type")
    content = "".join(body)
    soup = BeautifulSoup(content, "html.parser")
    assert len(soup.find_all("img")) == images
    for node in soup.select("h1,h2,h3,h4,p,li,th,td,pre"):
        if not node.find("img"):
            node["data-text-check"] = "true"
    title = soup.h1.get_text()
    css = """
    @page { size: A4; margin: 17mm 16mm 18mm; }
    *{box-sizing:border-box;letter-spacing:0}
    body{margin:0;color:#18292e;background:#fff;font:10.5pt/1.5 Arial,sans-serif}
    h1{font-size:22pt;line-height:1.2;margin:0 0 18pt}
    h2{font-size:15pt;line-height:1.25;margin:22pt 0 9pt}
    h3{font-size:12pt;line-height:1.3;margin:14pt 0 7pt}
    h1,h2,h3,h4{break-after:avoid}p,li{orphans:3;widows:3}
    p{margin:7pt 0}ul,ol{padding-left:20pt}li{margin:3pt 0}
    a{color:#185e85;text-decoration:none}
    table{border-collapse:collapse;width:100%;table-layout:auto;font-size:9pt;line-height:1.4;margin:12pt 0;break-inside:avoid}
    th,td{border:0.6pt solid #aebfc5;padding:6pt;text-align:left;vertical-align:top;overflow-wrap:break-word}
    th{background:#edf4f3}thead{display:table-header-group}tr{break-inside:avoid}
    pre{white-space:pre-wrap;overflow-wrap:anywhere;font:9pt/1.4 Consolas,monospace;padding:9pt;background:#f1f4f5;break-inside:avoid}
    .output{border-left:2pt solid #327968}code{font-family:Consolas,monospace;font-size:0.94em}
    .figure-cell{break-inside:avoid;margin:12pt 0}
    .closing-section{break-inside:avoid}
    .figure-cell h3{margin-top:0}.figure-cell p{margin:5pt 0}
    img{display:block;max-width:100%;width:auto;height:auto;max-height:213mm;margin:0 auto;object-fit:contain}
    """
    target = OUT / (chapter + ".html")
    target.write_text('<!doctype html><html lang="en"><meta charset="utf-8">'
        '<title>' + html.escape(title) + '</title><style>' + css + '</style><main>'
        + str(soup) + '</main></html>', encoding="utf-8")
    return dict(chapter=chapter, title=title, images=images, notebook_sha256=builder.sha256(path))


def words(text):
    return Counter(re.findall(r"[A-Za-z0-9_]+", text))


def verify_pdf(item):
    chapter = item["chapter"]
    path = builder.safe_target(chapter + ".pdf")
    doc = fitz.open(path)
    metadata = doc.metadata
    metadata.update(author="WenYi Lee", subject="Notebook SHA256: " + item["notebook_sha256"])
    doc.set_metadata(metadata)
    doc.saveIncr()
    expected = json.loads((OUT / (chapter + "_browser.json")).read_text(encoding="utf-8"))
    text = "\n".join(page.get_text() for page in doc)
    missing = words(expected["text"]) - words(text)
    if missing:
        raise AssertionError(f"PDF text missing from {chapter}: {missing}")
    if "attachment:" in text or "file:///" in text:
        raise AssertionError("Internal URL in PDF")
    image_count = 0
    for number, page in enumerate(doc, 1):
        images = page.get_image_info()
        image_count += len(images)
        for info in images:
            rect = fitz.Rect(info["bbox"])
            assert page.rect.contains(rect), (chapter, number, rect)
            assert rect.width > 150 and rect.height > 50
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0:
                continue
            rect = fitz.Rect(block["bbox"])
            assert rect.x0 >= 10 and rect.x1 <= page.rect.width - 10, (chapter, number, rect)
            assert rect.y0 >= 5 and rect.y1 <= page.rect.height - 5, (chapter, number, rect)
        assert page.get_text().strip(), (chapter, "blank page", number)
    assert image_count == item["images"], (chapter, image_count, item["images"])
    item.update(pages=len(doc), pdf_sha256=builder.sha256(path),
                bytes=path.stat().st_size, text_coverage="PASS", embedded_images=image_count)
    doc.close()
    return item


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    config = builder.load_json(builder.CONFIG_PATH)
    items = [make_html(ch) for ch in config["published_pdf_chapters"]]
    (OUT / "inputs.json").write_text(json.dumps(items, indent=2), encoding="utf-8")
    subprocess.run(["node", str(builder.SOURCE_DIR / "print_chapter_pdfs.cjs")], check=True)
    results = [verify_pdf(item) for item in items]
    (OUT / "verification.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    for item in results:
        chapter = item["chapter"]
        pages = OUT / (chapter + "_" + item["pdf_sha256"][:10])
        pages.mkdir(exist_ok=True)
        subprocess.run(["pdftoppm", "-scale-to", "1200", "-png",
                        str(builder.safe_target(chapter + ".pdf")), str(pages / "page")], check=True)
        files = sorted(pages.glob("page-*.png"))
        assert len(files) == item["pages"]
        for start in range(0, len(files), 12):
            sheet = Image.new("RGB", (1440, 1600), "#cbd0d2")
            draw = ImageDraw.Draw(sheet)
            for index, file in enumerate(files[start:start+12]):
                with Image.open(file) as picture:
                    picture.thumbnail((342, 485))
                    x, y = 9 + (index % 4)*360, 28 + (index // 4)*530
                    sheet.paste(picture, (x,y))
                    draw.text((x,y-20), f"{chapter} page {start+index+1}", fill="black")
            sheet.save(OUT / f"{chapter}_overview_{start//12+1}.png")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
