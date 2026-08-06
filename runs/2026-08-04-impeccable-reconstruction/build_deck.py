#!/usr/bin/env python3
"""Build a reconstruction-first deck: dominant source visual + attached context."""

import json
import sys
from pathlib import Path

SKILL = Path("/home/sheke/content-ideas/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(SKILL))
from pptxkit import Brand, Deck, Inches, PP_ALIGN  # noqa: E402

RUN = Path(__file__).resolve().parent
OUT = RUN / "impeccable-4-video-reconstruction-draft.pptx"
items = json.loads((RUN / "reconstruction-map.json").read_text(encoding="utf-8"))["items"]
b = Brand()
d = Deck(brand=b, footer="Impeccable 4.0 · Visual reconstruction")
total = len(items) + 1

# Cover uses the source's own visual language as the dominant asset.
s = d.slide(fill=b.NAVY)
d.picture_centered(s, RUN / items[0]["assets"][0], top=0, width=d.W, max_bottom=d.H)
d.rect(s, 0, Inches(5.25), d.W, Inches(2.25), b.NAVY)
d.text(s, "IMPECCABLE 4.0", d.M, Inches(5.48), Inches(3), Inches(0.35), size=13, color=b.TEAL, bold=True)
d.text(s, "Design with range, taste, and control", d.M, Inches(5.86), Inches(9.8), Inches(0.72), size=30, color=b.WHITE, bold=True)
d.text(s, "Reconstructed from the complete visual demonstration", d.M, Inches(6.55), Inches(8.0), Inches(0.35), size=13, color=b.LIGHT_TEAL)
d.footer(s, 1, total, dark=True)

for page, item in enumerate(items, start=2):
    s = d.slide(fill=b.WHITE)
    d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
    d.text(s, item["visible_title"], d.M, Inches(0.28), d.CW, Inches(0.62), size=26, color=b.NAVY, bold=True, shrink=True)
    picture = d.picture_centered(s, RUN / item["assets"][0], top=Inches(1.02), width=Inches(11.95), max_bottom=Inches(5.95))
    picture.left = d.M
    d.rect(s, d.M, Inches(6.04), d.CW, Inches(0.82), b.NAVY, radius=0.02)
    d.text(s, item["context_summary"], d.M + Inches(0.28), Inches(6.17), d.CW - Inches(0.56), Inches(0.52), size=14, color=b.WHITE, bold=True, ls=1.08, shrink=True)
    d.footer(s, page, total)

d.save(OUT)
print(OUT)
