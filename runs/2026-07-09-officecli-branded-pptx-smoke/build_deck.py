#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "skills/branded-pptx-deck/scripts"))

from pptxkit import Deck, Inches, PP_ALIGN


OUT = RUN / "officecli-branded-pptx-smoke-draft.pptx"


def cover(d: Deck):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(11.55), 0, Inches(1.78), d.H, b.NAVY_2)
    d.rect(s, Inches(11.55), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "BRANDED PPTX SMOKE", d.M, Inches(0.9), Inches(7.8), Inches(0.35),
           size=14, color=b.TEAL, bold=True)
    d.text(s, "OfficeCLI closes the blind spot in deck QA",
           d.M, Inches(1.5), Inches(8.7), Inches(1.45),
           size=42, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.18), Inches(1.5), Inches(0.06), b.TEAL)
    d.text(s,
           "A native, editable PowerPoint built with pptxkit, then validated through the shared OfficeCLI render gate.",
           d.M, Inches(3.45), Inches(8.2), Inches(0.7),
           size=17, color=b.LIGHT_TEAL, shrink=True)
    labels = ["Native PPTX", "Editable text", "OfficeCLI QA"]
    for i, label in enumerate(labels):
        x = d.M + Inches(i * 2.0)
        d.rect(s, x, Inches(4.62), Inches(1.65), Inches(0.42), b.NAVY_2, line=b.TEAL, radius=0.12)
        d.text(s, label, x + Inches(0.13), Inches(4.74), Inches(1.38), Inches(0.16),
               size=10.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.footer(s, 1, 3, dark=True)


def qa_flow(d: Deck):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, "Reviewed Decks Now Get A Real Render Loop",
             "Build native slides, then capture evidence before the reviewed filename is allowed.")
    steps = [
        ("1", "Build", "pptxkit composes native editable shapes and validates the OpenXML package."),
        ("2", "Preview", "The lightweight contact sheet catches common text collisions before external render."),
        ("3", "Render", "OfficeCLI validates, scans issues, writes HTML, and screenshots the final PPTX."),
    ]
    for i, (num, title, body) in enumerate(steps):
        x = d.M + Inches(i * 4.15)
        d.rect(s, x, Inches(2.0), Inches(3.75), Inches(3.0), b.SOFT, line=b.GRID, radius=0.1, shadow=True)
        d.rect(s, x + Inches(0.24), Inches(2.26), Inches(0.48), Inches(0.48), b.TEAL, radius=0.2)
        d.text(s, num, x + Inches(0.39), Inches(2.37), Inches(0.18), Inches(0.12),
               size=12, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, title, x + Inches(0.24), Inches(2.98), Inches(3.1), Inches(0.38),
               size=22, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.24), Inches(3.55), Inches(3.18), Inches(0.95),
               size=13, color=b.INK, shrink=True)
    d.rect(s, d.M, Inches(5.5), d.CW, Inches(0.82), b.NAVY, radius=0.06)
    d.text(s, "Decision rule: reviewed delivery requires real screenshot evidence.",
           d.M + Inches(0.24), Inches(5.73), d.CW - Inches(0.48), Inches(0.32),
           size=12.0, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 2, 3)


def scorecard(d: Deck):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, "OfficeCLI Adds The Missing QA Evidence", "What the practical run should prove.")
    rows = [
        ("OpenXML validity", "pptxkit", "OfficeCLI", "Passed"),
        ("Layout visibility", "Contact sheet", "Screenshot", "Passed"),
        ("Delivery status", "Draft", "Reviewed gate", "Evidence required"),
    ]
    x0, y0 = d.M, Inches(2.0)
    widths = [3.2, 2.7, 2.7, 3.0]
    headers = ["Check", "Before", "After", "Status"]
    for i, h in enumerate(headers):
        x = x0 + Inches(sum(widths[:i]))
        d.rect(s, x, y0, Inches(widths[i]), Inches(0.48), b.NAVY if i == 0 else b.TEAL)
        d.text(s, h, x + Inches(0.12), y0 + Inches(0.14), Inches(widths[i] - 0.24), Inches(0.2),
               size=10.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    for r, row in enumerate(rows):
        y = y0 + Inches(0.48 + r * 0.72)
        for c, value in enumerate(row):
            x = x0 + Inches(sum(widths[:c]))
            fill = b.SOFT if r % 2 == 0 else b.WHITE
            d.rect(s, x, y, Inches(widths[c]), Inches(0.72), fill, line=b.GRID)
            color = b.NAVY if c == 0 else b.INK
            bold = c == 0 or c == 3
            d.text(s, value, x + Inches(0.14), y + Inches(0.24), Inches(widths[c] - 0.28), Inches(0.18),
                   size=12.5, color=color, bold=bold, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "Editability mode: PPT-native editable diagrams and text.",
           d.M, Inches(5.02), d.CW, Inches(0.34), size=15, color=b.NAVY, bold=True)
    d.text(s, "This smoke deck intentionally uses only native PowerPoint shapes, text boxes, and fills. No flat screenshot is used as a primary slide visual.",
           d.M, Inches(5.47), d.CW, Inches(0.42), size=13.5, color=b.MUTED, shrink=True)
    d.footer(s, 3, 3)


def main():
    d = Deck(footer="OfficeCLI Branded PPTX Smoke | 2026")
    cover(d)
    qa_flow(d)
    scorecard(d)
    d.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
