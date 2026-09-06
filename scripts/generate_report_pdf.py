"""Generate report/report.pdf from report/report.md using only the standard library."""

from __future__ import annotations

import re
import textwrap
from pathlib import Path

PAGE_WIDTH = 595
PAGE_HEIGHT = 842
MARGIN = 50
BOTTOM_MARGIN = 50
NORMAL_SIZE = 10
CODE_SIZE = 8.5


def escape_pdf_text(text: str) -> str:
    """Escape characters that have special meaning in PDF text strings."""

    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def strip_markdown_inline(text: str) -> str:
    """Remove simple inline Markdown markers for PDF rendering."""

    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = text.replace("**", "")
    text = text.replace("*", "")
    return text


def parse_markdown(markdown: str) -> list[tuple[str, str]]:
    """Convert Markdown into simple block tuples for the custom PDF writer."""

    blocks: list[tuple[str, str]] = []
    in_code_block = False
    code_lines: list[str] = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_code_block:
                blocks.append(("code", "\n".join(code_lines)))
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        if not line:
            blocks.append(("blank", ""))
        elif line.startswith("# "):
            blocks.append(("title", strip_markdown_inline(line[2:].strip())))
        elif line.startswith("## "):
            blocks.append(("heading", strip_markdown_inline(line[3:].strip())))
        elif line.startswith("- "):
            blocks.append(("bullet", strip_markdown_inline(line[2:].strip())))
        elif line.startswith("|"):
            blocks.append(("code", line))
        else:
            blocks.append(("paragraph", strip_markdown_inline(line)))

    if code_lines:
        blocks.append(("code", "\n".join(code_lines)))
    return blocks


def wrap_block(kind: str, text: str) -> list[tuple[str, str, float]]:
    """Wrap parsed blocks into renderable PDF lines."""

    if kind == "blank":
        return [("blank", "", 6)]
    if kind == "title":
        return [("title", text, 20), ("blank", "", 8)]
    if kind == "heading":
        return [("heading", text, 15), ("blank", "", 5)]
    if kind == "bullet":
        wrapped = textwrap.wrap(text, width=88) or [""]
        lines = [("normal", f"- {wrapped[0]}", NORMAL_SIZE + 3)]
        for continuation in wrapped[1:]:
            lines.append(("normal", f"  {continuation}", NORMAL_SIZE + 3))
        return lines
    if kind == "code":
        result: list[tuple[str, str, float]] = []
        for code_line in text.splitlines() or [""]:
            wrapped = textwrap.wrap(
                code_line,
                width=92,
                replace_whitespace=False,
                drop_whitespace=False,
            ) or [""]
            for part in wrapped:
                result.append(("code", part, CODE_SIZE + 3))
        result.append(("blank", "", 4))
        return result

    wrapped = textwrap.wrap(text, width=90) or [""]
    return [("normal", part, NORMAL_SIZE + 3) for part in wrapped] + [("blank", "", 3)]


def build_pages(lines: list[tuple[str, str, float]]) -> list[list[tuple[str, str, float]]]:
    """Split renderable lines into pages."""

    pages: list[list[tuple[str, str, float]]] = []
    current_page: list[tuple[str, str, float]] = []
    y = PAGE_HEIGHT - MARGIN

    for kind, text, leading in lines:
        if y - leading < BOTTOM_MARGIN and current_page:
            pages.append(current_page)
            current_page = []
            y = PAGE_HEIGHT - MARGIN
        current_page.append((kind, text, leading))
        y -= leading

    if current_page:
        pages.append(current_page)
    return pages


def text_command(kind: str, text: str, y: float) -> str:
    """Return one PDF text drawing command."""

    if kind == "blank":
        return ""

    if kind == "title":
        font, size = "F2", 16
    elif kind == "heading":
        font, size = "F2", 13
    elif kind == "code":
        font, size = "F3", CODE_SIZE
    else:
        font, size = "F1", NORMAL_SIZE

    escaped = escape_pdf_text(text)
    return f"BT /{font} {size} Tf {MARGIN} {y:.2f} Td ({escaped}) Tj ET\n"


def build_content_stream(page_lines: list[tuple[str, str, float]], page_number: int) -> bytes:
    """Build PDF drawing commands for a single page."""

    y = PAGE_HEIGHT - MARGIN
    commands = []
    for kind, text, leading in page_lines:
        commands.append(text_command(kind, text, y))
        y -= leading

    footer = f"Page {page_number}"
    commands.append(
        f"BT /F1 8 Tf {PAGE_WIDTH / 2 - 15:.2f} 28 Td ({escape_pdf_text(footer)}) Tj ET\n"
    )
    return "".join(commands).encode("latin-1", errors="replace")


def write_pdf(markdown_path: Path, output_path: Path) -> None:
    """Write a simple multi-page PDF report."""

    markdown = markdown_path.read_text(encoding="utf-8")
    blocks = parse_markdown(markdown)
    render_lines: list[tuple[str, str, float]] = []
    for kind, text in blocks:
        render_lines.extend(wrap_block(kind, text))

    pages = build_pages(render_lines)
    objects: list[bytes] = []

    catalog_id = 1
    pages_id = 2
    font_regular_id = 3
    font_bold_id = 4
    font_mono_id = 5
    next_object_id = 6

    page_object_ids: list[int] = []
    content_object_ids: list[int] = []
    page_contents: list[bytes] = []
    for page_number, page_lines in enumerate(pages, start=1):
        page_object_ids.append(next_object_id)
        content_object_ids.append(next_object_id + 1)
        page_contents.append(build_content_stream(page_lines, page_number))
        next_object_id += 2

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    kids = " ".join(f"{page_id} 0 R" for page_id in page_object_ids)
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(page_object_ids)} >>".encode())
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")

    for page_id, content_id, content in zip(page_object_ids, content_object_ids, page_contents):
        page_object = (
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R "
            f"/F3 {font_mono_id} 0 R >> >> /Contents {content_id} 0 R >>"
        ).encode()
        content_object = b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"endstream"
        objects.append(page_object)
        objects.append(content_object)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as file:
        file.write(b"%PDF-1.4\n")
        offsets = [0]
        for object_number, payload in enumerate(objects, start=1):
            offsets.append(file.tell())
            file.write(f"{object_number} 0 obj\n".encode())
            file.write(payload)
            file.write(b"\nendobj\n")

        xref_offset = file.tell()
        file.write(f"xref\n0 {len(objects) + 1}\n".encode())
        file.write(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            file.write(f"{offset:010d} 00000 n \n".encode())
        file.write(
            (
                "trailer\n"
                f"<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
                "startxref\n"
                f"{xref_offset}\n"
                "%%EOF\n"
            ).encode()
        )


def main() -> None:
    """Generate the academic report PDF."""

    project_root = Path(__file__).resolve().parents[1]
    write_pdf(project_root / "report" / "report.md", project_root / "report" / "report.pdf")


if __name__ == "__main__":
    main()
