#!/usr/bin/env python3
"""Build the Impeccable conservation-proof treatment from Watch assets."""

import json
import sys
from pathlib import Path

SKILL = Path("/home/sheke/content-ideas/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(SKILL))
from pptxkit import Brand, Deck, Inches, PP_ALIGN, RGBColor  # noqa: E402

RUN = Path(__file__).resolve().parent
OUT = RUN / "impeccable-watch-client-ready-draft.pptx"
items = json.loads((RUN / "visual-context-map.json").read_text(encoding="utf-8"))["items"]

WASHI = RGBColor(0xF2, 0xED, 0xE3)
PAPER = RGBColor(0xFF, 0xFC, 0xF6)
INK = RGBColor(0x20, 0x21, 0x20)
VERMILION = RGBColor(0xD8, 0x43, 0x2F)
MUTED = RGBColor(0x68, 0x65, 0x60)
RULE = RGBColor(0xC9, 0xC0, 0xB2)

b = Brand(NAVY=INK, NAVY_2=INK, TEAL=VERMILION, ACCENT=VERMILION,
          DARK_TEAL=VERMILION, LIGHT_TEAL=WASHI, CORAL=VERMILION,
          WHITE=PAPER, SOFT=WASHI, INK=INK, MUTED=MUTED, GRID=RULE)
d = Deck(brand=b, footer="Impeccable 4.0")
total = len(items) + 2


def proof_label(s, page, kind="WORKING PROOF"):
    d.text(s, kind, Inches(11.08), Inches(0.28), Inches(1.55), Inches(0.28), size=9,
           color=VERMILION, bold=True, align=PP_ALIGN.RIGHT)
    d.text(s, f"{page:02d} / {total:02d}", Inches(11.08), Inches(0.57), Inches(1.55), Inches(0.25),
           size=9, color=MUTED, align=PP_ALIGN.RIGHT)


def cover_presenter(s, x, y, w, h, note, dark=False):
    # The video presenter overlay already obscures this region; this note replaces only that overlay.
    fill = INK if dark else PAPER
    text_color = PAPER if dark else INK
    d.rect(s, x, y, w, h, fill, radius=0.02)
    d.rect(s, x, y, Inches(0.07), h, VERMILION)
    d.text(s, note, x + Inches(0.24), y + Inches(0.16), w - Inches(0.42), h - Inches(0.30),
           size=12, color=text_color, bold=True, ls=1.08, shrink=True)


# Cover — the original asset remains the field, with a paper title plate.
s = d.slide(fill=INK)
d.picture_centered(s, RUN / items[0]["asset"], top=0, width=d.W, max_bottom=d.H)
d.rect(s, Inches(0.72), Inches(0.72), Inches(5.55), Inches(2.35), PAPER, radius=0.02)
d.text(s, "IMPECCABLE 4.0", Inches(1.02), Inches(1.02), Inches(4.8), Inches(0.35), size=13, color=VERMILION, bold=True)
d.text(s, "Design with range,\ntaste, and control", Inches(1.02), Inches(1.42), Inches(4.8), Inches(1.2), size=31, color=INK, bold=True, ls=1.0)
d.text(s, "A visual reconstruction of the complete workflow", Inches(1.02), Inches(2.65), Inches(4.8), Inches(0.28), size=11, color=MUTED)
proof_label(s, 1, "FINAL PROOF")

# Executive orientation — native map, no generic cards.
s = d.slide(fill=WASHI)
d.text(s, "Impeccable is a loop, not a style button", Inches(0.75), Inches(0.62), Inches(10.2), Inches(0.7), size=31, color=INK, bold=True)
d.text(s, "The demonstration moves through five linked decisions.", Inches(0.75), Inches(1.36), Inches(8.5), Inches(0.4), size=15, color=MUTED)
steps = [("01", "GROUND", "Start from purpose"), ("02", "EXPAND", "Generate real range"), ("03", "SELECT", "Compare visually"), ("04", "DETECT", "Remove defaults"), ("05", "RECORD", "Preserve the world")]
for i, (num, head, body) in enumerate(steps):
    x = Inches(0.78 + i * 2.45)
    d.text(s, num, x, Inches(2.45), Inches(0.45), Inches(0.32), size=11, color=VERMILION, bold=True)
    d.rect(s, x, Inches(2.93), Inches(2.0), Inches(0.05), VERMILION if i == 4 else RULE)
    d.text(s, head, x, Inches(3.24), Inches(2.0), Inches(0.4), size=15, color=INK, bold=True)
    d.text(s, body, x, Inches(3.78), Inches(2.0), Inches(0.75), size=14, color=MUTED, ls=1.12)
d.text(s, "The visual assets on the following pages remain the evidence; the template improves how they are seen.", Inches(0.78), Inches(5.65), Inches(11.5), Inches(0.6), size=18, color=INK, bold=True)
proof_label(s, 2, "SEQUENCE MAP")
d.footer(s, 2, total)

for idx, item in enumerate(items[1:], start=3):
    mode = idx % 3
    s = d.slide(fill=PAPER if mode != 1 else WASHI)
    d.text(s, item["title"], Inches(0.72), Inches(0.42), Inches(9.95), Inches(0.62), size=27, color=INK, bold=True, shrink=True)
    proof_label(s, idx)
    asset = RUN / item["asset"]

    if mode == 0:  # full proof with bottom annotation overlay
        d.rect(s, Inches(0.68), Inches(1.28), Inches(11.96), Inches(5.30), WASHI)
        pic = d.picture_centered(s, asset, top=Inches(1.42), width=Inches(11.62), max_bottom=Inches(6.40))
        pic.left = Inches(0.85)
        d.rect(s, Inches(7.82), Inches(4.42), Inches(1.70), Inches(1.86), INK)
        cover_presenter(s, Inches(9.02), Inches(4.52), Inches(3.33), Inches(1.71), item["context"], dark=True)
    elif mode == 1:  # proof plus wide marginal interpretation
        d.rect(s, Inches(0.68), Inches(1.30), Inches(8.88), Inches(5.18), PAPER)
        pic = d.picture_centered(s, asset, top=Inches(1.46), width=Inches(8.58), max_bottom=Inches(6.32))
        pic.left = Inches(0.83)
        # hide only the presenter overlay inside the proof
        d.rect(s, Inches(7.72), Inches(4.34), Inches(1.86), Inches(1.94), PAPER)
        if item["id"] == "design-record":
            d.rect(s, Inches(5.55), Inches(4.22), Inches(4.03), Inches(2.06), PAPER)
            d.text(s, "DESIGN RECORD", Inches(5.82), Inches(4.48), Inches(2.8), Inches(0.3), size=10, color=VERMILION, bold=True)
            d.text(s, "Palette · typography · composition · interaction", Inches(5.82), Inches(4.94), Inches(3.35), Inches(0.78), size=15, color=INK, bold=True, ls=1.12, shrink=True)
        d.text(s, "CONTEXT", Inches(9.88), Inches(1.58), Inches(2.3), Inches(0.3), size=10, color=VERMILION, bold=True)
        d.rect(s, Inches(9.88), Inches(2.05), Inches(2.35), Inches(0.05), VERMILION)
        d.text(s, item["context"], Inches(9.88), Inches(2.38), Inches(2.4), Inches(2.65), size=17, color=INK, bold=True, ls=1.14, shrink=True)
        d.text(s, "Same evidence. Stronger focus.", Inches(9.88), Inches(5.48), Inches(2.35), Inches(0.45), size=11, color=MUTED, italic=True)
    else:  # image field with translucent-style paper ticket over the obscured corner
        d.rect(s, Inches(0.68), Inches(1.25), Inches(11.96), Inches(5.35), INK)
        pic = d.picture_centered(s, asset, top=Inches(1.39), width=Inches(11.62), max_bottom=Inches(6.43))
        pic.left = Inches(0.85)
        d.rect(s, Inches(7.82), Inches(4.36), Inches(1.70), Inches(1.90), PAPER)
        cover_presenter(s, Inches(9.02), Inches(4.45), Inches(3.33), Inches(1.79), item["context"], dark=False)
    d.footer(s, idx, total)

# Closing benchmark — explain the value of the Impeccable treatment without hiding the evidence.
s = d.slide(fill=INK)
d.text(s, "The template improved how the assets are seen", Inches(0.75), Inches(0.72), Inches(10.6), Inches(0.78), size=32, color=PAPER, bold=True)
d.text(s, "It did not replace what the video showed.", Inches(0.75), Inches(1.52), Inches(8.0), Inches(0.42), size=16, color=RULE)
results = [
    ("ASSET PROMINENCE", "Visuals occupy the field instead of becoming thumbnails."),
    ("CONTEXT BINDING", "Annotations sit on the presenter-obscured region they explain."),
    ("HIERARCHY", "Each page has one proof, one title, and one attached interpretation."),
    ("COHERENCE", "Three proof archetypes create rhythm without changing the sequence."),
]
for i, (head, body) in enumerate(results):
    x = Inches(0.78 + (i % 2) * 6.02)
    y = Inches(2.45 + (i // 2) * 1.72)
    d.text(s, head, x, y, Inches(5.25), Inches(0.32), size=11, color=VERMILION, bold=True)
    d.rect(s, x, y + Inches(0.46), Inches(5.2), Inches(0.04), VERMILION)
    d.text(s, body, x, y + Inches(0.72), Inches(5.25), Inches(0.78), size=17, color=PAPER, bold=True, ls=1.12, shrink=True)
d.text(s, "Decision: use the Impeccable treatment for client delivery.", Inches(0.78), Inches(6.05), Inches(10.2), Inches(0.5), size=20, color=PAPER, bold=True)
proof_label(s, total, "CHOSEN PROOF")
d.footer(s, total, total, dark=True)

d.save(OUT)
print(OUT)
