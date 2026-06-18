#!/usr/bin/env python3
"""
bcg_to_pptx.py — Universal BCG strategy skill → branded PPTX converter.

Reads any of the 21 strategy-consulting skill output markdown files and
renders a branded, validated PowerPoint deck using pptxkit.

Usage:
    python3 bcg_to_pptx.py <skill-output.md> [--company "Apex HR"] [--out deck.pptx]
    python3 bcg_to_pptx.py --all ./test-outputs/  # batch convert all 21

Each deck gets:
  Slide 1  — Navy cover (skill name + company + date)
  Slide 2  — Executive summary / first section (BLUF)
  Slide 3+ — One slide per ## section (tables, bullets, numbered lists)
  Last     — Action items / next steps (if present)
"""

import argparse
import math
import re
import sys
import os
from pathlib import Path
from datetime import date

# Resolve pptxkit from branded-pptx-deck skill
PPTXKIT_DIR = Path.home() / ".claude/skills/branded-pptx-deck/scripts"
sys.path.insert(0, str(PPTXKIT_DIR))

try:
    from pptxkit import Brand, Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor
except ImportError as e:
    print(f"ERROR: Cannot import pptxkit from {PPTXKIT_DIR}: {e}")
    sys.exit(1)


# ── BCG brand overlay (dark navy + BCG green accent) ─────────────────────────
BCG_BRAND = Brand(
    NAVY=RGBColor(0x00, 0x18, 0x24),     # BCG dark navy
    NAVY_2=RGBColor(0x00, 0x26, 0x34),
    TEAL=RGBColor(0x00, 0x99, 0x6B),     # BCG green
    ACCENT=RGBColor(0x00, 0x77, 0x55),
    DARK_TEAL=RGBColor(0x00, 0x66, 0x44),
    LIGHT_TEAL=RGBColor(0xCC, 0xEE, 0xE4),
    GOLD=RGBColor(0xFF, 0xB8, 0x00),
    AMBER=RGBColor(0xF2, 0xA8, 0x3B),
    CORAL=RGBColor(0xE0, 0x5A, 0x6B),
    WHITE=RGBColor(0xFF, 0xFF, 0xFF),
    SOFT=RGBColor(0xF4, 0xF7, 0xF8),
    INK=RGBColor(0x1B, 0x2B, 0x3C),
    MUTED=RGBColor(0x5B, 0x6B, 0x7C),
)


# ── Markdown parser ───────────────────────────────────────────────────────────

def parse_markdown(text: str) -> dict:
    """
    Returns:
      {
        "title": str,           # first # heading
        "sections": [           # one per ## heading
          { "heading": str, "content": [block, ...] }
        ]
      }
    block types: {"type": "paragraph", "text": str}
                 {"type": "bullets",   "items": [str, ...]}
                 {"type": "numbered",  "items": [str, ...]}
                 {"type": "table",     "headers": [str], "rows": [[str], ...]}
    """
    lines = text.split("\n")
    title = ""
    sections = []
    current_section = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # h1 title
        if line.startswith("# ") and not line.startswith("## "):
            title = line[2:].strip()
            i += 1
            continue

        # h2 section heading
        if line.startswith("## "):
            if current_section:
                sections.append(current_section)
            current_section = {"heading": line[3:].strip(), "content": []}
            i += 1
            continue

        # h3 subsection — treat as bold paragraph
        if line.startswith("### "):
            if current_section is not None:
                current_section["content"].append(
                    {"type": "paragraph", "text": line[4:].strip(), "bold": True}
                )
            i += 1
            continue

        if current_section is None:
            i += 1
            continue

        # table detection (line starts with |)
        if line.strip().startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            headers, rows = _parse_table(table_lines)
            if headers:
                current_section["content"].append(
                    {"type": "table", "headers": headers, "rows": rows}
                )
            continue

        # bullet list
        if line.strip().startswith("- ") or line.strip().startswith("* "):
            items = []
            while i < len(lines) and (
                lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")
            ):
                items.append(lines[i].strip()[2:].strip())
                i += 1
            current_section["content"].append({"type": "bullets", "items": items})
            continue

        # numbered list
        if re.match(r"^\d+\.", line.strip()):
            items = []
            while i < len(lines) and re.match(r"^\d+\.", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s*", "", lines[i].strip()))
                i += 1
            current_section["content"].append({"type": "numbered", "items": items})
            continue

        # non-empty paragraph
        stripped = line.strip()
        if stripped and not stripped.startswith("---") and not stripped.startswith("```"):
            # strip inline markdown
            cleaned = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped)
            cleaned = re.sub(r"`(.+?)`", r"\1", cleaned)
            current_section["content"].append(
                {"type": "paragraph", "text": cleaned}
            )

        i += 1

    if current_section:
        sections.append(current_section)

    return {"title": title, "sections": sections}


def _parse_table(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    if len(lines) < 2:
        return [], []
    headers = [c.strip() for c in lines[0].split("|") if c.strip()]
    rows = []
    for line in lines[2:]:  # skip separator row
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if cells:
            rows.append(cells)
    return headers, rows


# ── Slide builders ────────────────────────────────────────────────────────────

def slide_cover(d: Deck, title: str, company: str, skill_label: str):
    b = d.b
    s = d.slide(fill=b.NAVY)

    # left green spine
    d.rect(s, 0, 0, Inches(0.22), d.H, b.TEAL)

    # BCG label chip
    d.rect(s, Inches(0.5), Inches(0.35), Inches(1.6), Inches(0.38), b.TEAL, radius=0.05)
    d.text(s, "BCG-STYLE", Inches(0.52), Inches(0.37), Inches(1.56), Inches(0.34),
           size=11, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)

    # skill label
    d.text(s, skill_label.upper(), Inches(0.5), Inches(0.88), d.CW, Inches(0.4),
           size=13, color=b.TEAL, bold=True)

    # title
    d.text(s, title, Inches(0.5), Inches(1.4), Inches(10.5), Inches(2.8),
           size=42, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)

    # gold rule
    d.rect(s, Inches(0.5), Inches(4.4), Inches(3.0), Inches(0.06), b.GOLD)

    # company + date
    d.text(s, company, Inches(0.5), Inches(4.65), Inches(8), Inches(0.45),
           size=18, color=b.LIGHT_TEAL)
    d.text(s, str(date.today()), Inches(0.5), Inches(5.15), Inches(8), Inches(0.38),
           size=13, color=b.MUTED)

    # "Consultant's Guide to Claude" attribution
    d.text(s, "Powered by The Consultant's Guide to Claude · 21 BCG-Style Skills",
           Inches(0.5), Inches(6.8), Inches(10), Inches(0.35),
           size=10, color=b.MUTED)


def slide_section(d: Deck, heading: str, content: list, page: int, total: int, company: str):
    b = d.b
    s = d.slide(fill=b.SOFT)

    # top teal band
    d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)

    # heading
    d.text(s, heading, d.M, Inches(0.38), d.CW, Inches(0.72),
           size=26, color=b.NAVY, bold=True, font=b.FONT_H, shrink=True)

    # teal rule under heading
    d.rect(s, d.M, Inches(1.18), Inches(1.4), Inches(0.05), b.TEAL)

    # company chip (top right)
    chip_w = Inches(2.2)
    d.rect(s, d.W - chip_w - d.M, Inches(0.28), chip_w, Inches(0.38), b.NAVY, radius=0.04)
    d.text(s, company, d.W - chip_w - d.M + Inches(0.08), Inches(0.3),
           chip_w - Inches(0.16), Inches(0.34),
           size=10.5, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)

    y = Inches(1.42)
    bottom = Inches(6.9)
    available = bottom - y

    # render content blocks
    for block in content:
        if y >= bottom:
            break

        btype = block.get("type")

        if btype == "paragraph":
            bold = block.get("bold", False)
            color = b.NAVY if bold else b.INK
            size = 15 if bold else 13
            # dynamic height: ~85 chars per line at 13pt across full slide width
            chars_per_line = 72 if bold else 85
            n_lines = max(1, math.ceil(len(block["text"]) / chars_per_line))
            line_h = Inches(0.34) if bold else Inches(0.3)
            h = line_h * n_lines + Inches(0.06)
            d.text(s, block["text"], d.M, y, d.CW, h,
                   size=size, color=color, bold=bold, shrink=True)
            y += h + Inches(0.08)

        elif btype in ("bullets", "numbered"):
            items = block["items"]
            prefix = "•  " if btype == "bullets" else None
            for idx, item in enumerate(items[:8]):
                if y >= bottom:
                    break
                bullet_text = item if btype == "bullets" else f"{idx+1}.  {item}"
                # truncate long items
                if len(bullet_text) > 120:
                    bullet_text = bullet_text[:117] + "…"
                d.text(s, bullet_text, d.M + Inches(0.12), y, d.CW - Inches(0.12),
                       Inches(0.36), size=12.5, color=b.INK, shrink=True)
                y += Inches(0.38)
            y += Inches(0.08)

        elif btype == "table":
            headers = block["headers"]
            rows = block["rows"]
            y = _render_table(d, s, headers, rows, y, bottom)
            y += Inches(0.1)

    d.footer(s, page, total)


def _render_table(d: Deck, s, headers: list, rows: list, y_start: float, bottom: float) -> float:
    b = d.b
    if not headers:
        return y_start

    n_cols = len(headers)
    col_w = d.CW / n_cols
    row_h = Inches(0.52)
    header_h = Inches(0.42)
    x0 = d.M

    # header row background
    d.rect(s, x0, y_start, d.CW, header_h, b.NAVY)
    for ci, h in enumerate(headers[:6]):
        label = h[:22] + "…" if len(h) > 22 else h
        d.text(s, label, x0 + ci * col_w + Inches(0.06), y_start + Inches(0.05),
               col_w - Inches(0.1), header_h - Inches(0.08),
               size=11, color=b.WHITE, bold=True, shrink=True)

    y = y_start + header_h

    for ri, row in enumerate(rows):
        if y + row_h > bottom:
            break
        fill = b.WHITE if ri % 2 == 0 else b.SOFT
        d.rect(s, x0, y, d.CW, row_h, fill, line=b.GRID)
        for ci, cell in enumerate(row[:6]):
            cell_str = str(cell)
            if len(cell_str) > 35:
                cell_str = cell_str[:32] + "…"
            # highlight cells containing priority keywords
            text_color = b.INK
            if any(kw in cell_str.lower() for kw in ("high", "#1", "critical", "invest", "very high")):
                text_color = b.ACCENT
            elif any(kw in cell_str.lower() for kw in ("low", "harvest", "defer", "kill")):
                text_color = b.CORAL
            d.text(s, cell_str, x0 + ci * col_w + Inches(0.06), y + Inches(0.05),
                   col_w - Inches(0.1), row_h - Inches(0.08),
                   size=10.5, color=text_color, shrink=True)
        y += row_h

    return y


def slide_exec_summary(d: Deck, section: dict, page: int, total: int, company: str):
    """Special treatment for first section — executive summary in BLUF layout."""
    b = d.b
    s = d.slide(fill=b.NAVY)

    # top green band
    d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)

    # "EXECUTIVE SUMMARY" label
    d.text(s, "EXECUTIVE SUMMARY", d.M, Inches(0.35), d.CW, Inches(0.38),
           size=12, color=b.TEAL, bold=True)

    # section heading
    d.text(s, section["heading"], d.M, Inches(0.82), d.CW, Inches(0.78),
           size=30, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)

    # gold rule
    d.rect(s, d.M, Inches(1.72), Inches(2.5), Inches(0.06), b.GOLD)

    # extract first paragraph as BLUF
    bluf = ""
    bullets = []
    for block in section["content"]:
        if block["type"] == "paragraph" and not bluf:
            bluf = block["text"]
        elif block["type"] in ("bullets", "numbered") and not bullets:
            bullets = block["items"]
        if bluf and bullets:
            break

    if bluf:
        d.text(s, bluf, d.M, Inches(1.95), d.CW, Inches(2.2),
               size=13, color=b.LIGHT_TEAL, shrink=True)

    if bullets:
        y = Inches(4.35)
        for item in bullets[:4]:
            if len(item) > 130:
                item = item[:127] + "…"
            d.rect(s, d.M, y, Inches(0.3), Inches(0.3), b.TEAL, radius=0.08)
            d.text(s, "→", d.M + Inches(0.04), y + Inches(0.02), Inches(0.22), Inches(0.26),
                   size=13, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
            d.text(s, item, d.M + Inches(0.42), y, d.CW - Inches(0.42),
                   Inches(0.36), size=13, color=b.WHITE, shrink=True)
            y += Inches(0.52)

    # company chip
    d.rect(s, d.W - Inches(2.6) - d.M, Inches(0.28), Inches(2.6), Inches(0.38),
           b.TEAL, radius=0.04)
    d.text(s, company, d.W - Inches(2.6) - d.M + Inches(0.1), Inches(0.3),
           Inches(2.4), Inches(0.34),
           size=11, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)

    d.footer(s, page, total, dark=True)


# ── Main converter ────────────────────────────────────────────────────────────

SKILL_LABELS = {
    "01": "01 / Diagnosis & Framing",
    "02": "01 / Diagnosis & Framing",
    "03": "01 / Diagnosis & Framing",
    "04": "02 / Market Intelligence",
    "05": "02 / Market Intelligence",
    "06": "02 / Market Intelligence",
    "07": "02 / Market Intelligence",
    "08": "03 / Strategic Choice",
    "09": "03 / Strategic Choice",
    "10": "03 / Strategic Choice",
    "11": "03 / Strategic Choice",
    "12": "04 / Execution",
    "13": "04 / Execution",
    "14": "04 / Execution",
    "15": "05 / Risk & Governance",
    "16": "05 / Risk & Governance",
    "17": "05 / Risk & Governance",
    "18": "05 / Risk & Governance",
    "19": "06 / Executive Comms",
    "20": "06 / Executive Comms",
    "21": "06 / Executive Comms",
}


def convert(md_path: Path, company: str, out_path: Path):
    text = md_path.read_text()
    parsed = parse_markdown(text)

    # detect skill number from filename
    num = re.match(r"^(\d+)", md_path.name)
    skill_num = num.group(1) if num else "00"
    skill_label = SKILL_LABELS.get(skill_num, "BCG Strategy Skill")

    title = parsed["title"] or md_path.stem.replace("-", " ").title()
    sections = parsed["sections"]

    if not sections:
        print(f"WARNING: No sections found in {md_path.name} — skipping")
        return None

    total_slides = 1 + len(sections)  # cover + sections

    footer_text = f"BCG Consulting Framework · {company} · {date.today()}"
    d = Deck(brand=BCG_BRAND, footer=footer_text)

    # Slide 1 — Cover
    slide_cover(d, title, company, skill_label)

    # Slide 2 — Executive Summary (first section, dark navy layout)
    slide_exec_summary(d, sections[0], 2, total_slides, company)

    # Slides 3+ — remaining sections
    for i, sec in enumerate(sections[1:], start=3):
        slide_section(d, sec["heading"], sec["content"], i, total_slides, company)

    d.save(out_path)
    print(f"  ✓ {out_path.name}  ({d.n} slides)")
    return out_path


def batch_convert(folder: Path, company: str, out_folder: Path):
    out_folder.mkdir(parents=True, exist_ok=True)
    md_files = sorted(folder.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {folder}")
        return

    print(f"\nConverting {len(md_files)} skill outputs → PPTX\n{'─'*50}")
    results = []
    for md in md_files:
        stem = md.stem
        out = out_folder / f"{stem}.pptx"
        try:
            convert(md, company, out)
            results.append(("OK", md.name))
        except Exception as e:
            print(f"  ✗ {md.name}: {e}")
            results.append(("FAIL", md.name))

    ok = sum(1 for r in results if r[0] == "OK")
    print(f"\n{'─'*50}")
    print(f"Done: {ok}/{len(md_files)} converted successfully")
    print(f"Output: {out_folder}")
    return out_folder


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BCG skill output → branded PPTX")
    parser.add_argument("input", nargs="?", help="skill output .md file, or folder with --all")
    parser.add_argument("--all", action="store_true",
                        help="batch convert all .md files in the input folder")
    parser.add_argument("--company", default="Apex HR",
                        help="company name for slide chips (default: Apex HR)")
    parser.add_argument("--out", default=None,
                        help="output .pptx path or output folder for --all")
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        sys.exit(1)

    inp = Path(args.input)

    if args.all or inp.is_dir():
        out_folder = Path(args.out) if args.out else inp / "pptx"
        batch_convert(inp, args.company, out_folder)
    else:
        if not inp.exists():
            print(f"ERROR: File not found: {inp}")
            sys.exit(1)
        out = Path(args.out) if args.out else inp.with_suffix(".pptx")
        convert(inp, args.company, out)
