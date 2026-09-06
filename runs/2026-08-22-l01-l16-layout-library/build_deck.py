#!/usr/bin/env python3
"""Build the L01-L16 layout-library deck FROM template-profile.json.

Nothing about the deck's type ramp, margin, grid, radius or palette is written
here -- every one of those is read out of the profile that
`derive_template_profile.py --canvas` measured off the design canvas. That is
the point of the run: change the canvas, re-derive, rebuild, and the rendered
slides move with it.

The three supporting neutrals (surface / line / muted) come from the design
system directly: the profile contract carries only page / ink / accent, and the
deriver's luminance classification cannot honestly produce more.

Run:  python3 build_deck.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
REPO = RUN.parents[1]
sys.path.insert(0, str(REPO / "skills/branded-pptx-deck/scripts"))

from pptxkit import Brand, Deck, Inches, PP_ALIGN, Pt, hx  # noqa: E402

PROFILE = json.loads((RUN / "template-profile.json").read_text(encoding="utf-8"))

BRAND_C = PROFILE["brand"]["colors"]
GEO = PROFILE["geometry"]
TYPE = PROFILE["typography"]
COMP = PROFILE["composition"]

# --- design-system neutrals (client-ready-pptx-design-system.md, "Color") ---
SURFACE, LINE, MUTED, TEAL, PALE = "#F8FAFC", "#E2E8F0", "#6B7280", "#0A9396", "#8DB4D4"


# --- WCAG AA: the spec's own accent fails as small text ----------------------
# "Kicker: 8-10 pt uppercase cyan" on white is 2.46:1. lint_pptx.py is right to
# flag it. The accent keeps its exact spec value on rules and bars (no text sits
# on them); TEXT gets a darkened variant of the same hue, computed here rather
# than hand-picked so a new palette recomputes instead of re-failing.

def _channel(value: float) -> float:
    value /= 255
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def _luminance(hexcode: str) -> float:
    h = hexcode.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def _scale(hexcode: str, factor: float) -> str:
    h = hexcode.lstrip("#")
    return "#" + "".join(
        f"{max(0, min(255, round(int(h[i:i + 2], 16) * factor))):02X}" for i in (0, 2, 4)
    )


def darken_until(hexcode: str, *, against: str, target: float = 4.5) -> str:
    """Walk the colour toward black until it clears `target` against `against`."""
    factor = 1.0
    while factor > 0.05:
        candidate = _scale(hexcode, factor)
        if contrast(candidate, against) >= target:
            return candidate
        factor -= 0.02
    return "#000000"


PAGE, INK, ACCENT = BRAND_C["page"], BRAND_C["ink"], BRAND_C["accent"]

# Text-safe variants. ACCENT itself is untouched and still paints every rule.
ACCENT_TEXT = darken_until(ACCENT, against=SURFACE)   # clears both PAGE and SURFACE
ACCENT_FILL = darken_until(ACCENT, against=PAGE)      # a fill that carries white text
TEAL_FILL = darken_until(TEAL, against=PAGE)

TITLE_PT = TYPE["title_pt"]
BODY_PT = TYPE["body_pt"]
CAPTION_PT = TYPE["caption_pt"]
METRIC_PT = TYPE["metric_pt"]
CARD_PT = round(BODY_PT * 1.15, 1)      # spec's card heading band, keyed off body
KICKER_PT = round(CAPTION_PT * 1.3, 1)  # spec's 8-10pt kicker band

MARGIN_IN = GEO["safe_margin_inches"]
GUTTER_IN = GEO["gutter_inches"]
COLUMNS = GEO["grid_columns"]
RADIUS_IN = COMP["corner_radius"]

HEAD_FONT = PROFILE["brand"]["heading_font"]
BODY_FONT = PROFILE["brand"]["body_font"]

brand = Brand(
    NAVY=hx(INK), INK=hx(INK), WHITE=hx(PAGE), TEAL=hx(ACCENT), ACCENT=hx(ACCENT),
    SOFT=hx(SURFACE), GRID=hx(LINE), MUTED=hx(MUTED),
    FONT=BODY_FONT, FONT_H=HEAD_FONT,
)
d = Deck(brand=brand)
d.M = Inches(MARGIN_IN)
d.CW = d.W - d.M * 2

GUTTER = Inches(GUTTER_IN)
COL_W = (d.CW - GUTTER * (COLUMNS - 1)) / COLUMNS
TOP = Inches(MARGIN_IN)


def span(n: int) -> int:
    return int(COL_W * n + GUTTER * (n - 1))


def col_x(index: int) -> int:
    return int(d.M + (COL_W + GUTTER) * index)


def adj(height_in: float) -> float:
    """pptxkit takes a rounded-rect adjustment fraction, the profile carries inches."""
    return max(0.02, min(0.5, RADIUS_IN / (height_in / 2)))


def header(s, kicker: str, title: str, *, dark: bool = False):
    fg = hx(PAGE) if dark else hx(INK)
    d.rect(s, d.M, TOP, Inches(1.25), Pt(2), hx(ACCENT))
    d.text(s, kicker.upper(), d.M, TOP + Inches(0.10), d.CW, Inches(0.24),
           size=KICKER_PT, color=hx(ACCENT if dark else ACCENT_TEXT), bold=True, font=BODY_FONT)
    d.text(s, title, d.M, TOP + Inches(0.40), d.CW, Inches(0.95),
           size=TITLE_PT, color=fg, font=HEAD_FONT, shrink=True)
    return TOP + Inches(1.55)


def footer(s, text: str, *, dark: bool = False):
    d.text(s, text, d.M, d.H - Inches(MARGIN_IN + 0.22), d.CW, Inches(0.22),
           size=CAPTION_PT, color=hx(PALE if dark else MUTED), font=BODY_FONT)


def card(s, x, y, w, h_in, heading, note, *, fill=SURFACE, fg=INK, note_color=None):
    d.rect(s, x, y, w, Inches(h_in), hx(fill), line=hx(LINE), radius=adj(h_in))
    d.text(s, heading, x + Inches(0.18), y + Inches(0.16), w - Inches(0.36), Inches(0.30),
           size=CARD_PT, color=hx(fg), bold=True, font=BODY_FONT, shrink=True)
    d.text(s, note, x + Inches(0.18), y + Inches(0.56), w - Inches(0.36), Inches(h_in - 0.74),
           size=BODY_PT, color=hx(note_color or MUTED), font=BODY_FONT, shrink=True)


def card_row(s, y, items, h_in=1.45, **kw):
    n = len(items)
    width = COLUMNS // n
    for i, (heading, note) in enumerate(items):
        card(s, col_x(i * width), y, span(width), h_in, heading, note, **kw)
    return y + Inches(h_in)


def kpi_row(s, y, items, h_in=1.45):
    n = len(items)
    width = COLUMNS // n
    for i, (value, label) in enumerate(items):
        x, w = col_x(i * width), span(width)
        d.rect(s, x, y, w, Inches(h_in), hx(SURFACE), line=hx(LINE), radius=adj(h_in))
        d.text(s, value, x + Inches(0.18), y + Inches(0.22), w - Inches(0.36), Inches(0.72),
               size=METRIC_PT, color=hx(ACCENT_TEXT), font=HEAD_FONT, shrink=True)
        d.text(s, label, x + Inches(0.18), y + Inches(h_in - 0.44), w - Inches(0.36), Inches(0.28),
               size=CAPTION_PT, color=hx(MUTED), bold=True, font=BODY_FONT)
    return y + Inches(h_in)


def node_row(s, y, labels, h_in=0.85, fill=None):
    fill = fill or TEAL_FILL
    width = COLUMNS // len(labels)
    for i, label in enumerate(labels):
        x, w = col_x(i * width), span(width)
        d.rect(s, x, y, w, Inches(h_in), hx(fill), radius=adj(h_in))
        d.text(s, label, x, y + Inches(0.26), w, Inches(0.34), size=CARD_PT,
               color=hx(PAGE), bold=True, align=PP_ALIGN.CENTER, font=BODY_FONT)
    return y + Inches(h_in)


def slab(s, x, y, w, h_in, heading, note):
    d.rect(s, x, y, w, Inches(h_in), hx(INK), radius=adj(h_in))
    d.text(s, heading, x + Inches(0.26), y + Inches(0.24), w - Inches(0.52), Inches(0.36),
           size=CARD_PT, color=hx(PAGE), bold=True, font=BODY_FONT, shrink=True)
    d.text(s, note, x + Inches(0.26), y + Inches(0.70), w - Inches(0.52), Inches(h_in - 0.94),
           size=BODY_PT, color=hx(PALE), font=BODY_FONT, shrink=True)


FOOT = "Client-Ready PPTX Design System · layout reference · derived from canvas"

# ── L01 Cover ────────────────────────────────────────────────────────────────
s = d.slide(fill=hx(INK))
d.rect(s, d.M, Inches(1.15), Inches(1.6), Pt(3), hx(ACCENT))
d.text(s, "Cover states the promise,\nnot the topic", d.M, Inches(1.50), Inches(9.4), Inches(2.1),
       size=round(TITLE_PT * 1.6, 1), color=hx(PAGE), font=HEAD_FONT, shrink=True)
d.text(s, "Engagement · audience · date", d.M, TOP, d.CW, Inches(0.32),
       size=BODY_PT, color=hx(PALE), font=BODY_FONT)
footer(s, "L01 Cover", dark=True)

# ── L02 Executive thesis ─────────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L02 · Executive thesis", "One thesis, four numbers that carry it")
slab(s, col_x(0), y, span(6), 3.55, "The thesis",
     "55/45 split: dark headline panel left, KPI grid right. The panel carries the "
     "argument; the grid carries the proof.")
kpi_row(s, y, [("41%", "MARGIN"), ("2.4x", "PIPELINE")][:2]) if False else None
for i, (value, label) in enumerate([("41%", "MARGIN"), ("2.4x", "PIPELINE"),
                                    ("18mo", "PAYBACK"), ("7", "MARKETS")]):
    x = col_x(6 + (i % 2) * 3)
    yy = y + Inches(1.87 * (i // 2))
    d.rect(s, x, yy, span(3), Inches(1.68), hx(SURFACE), line=hx(LINE), radius=adj(1.68))
    d.text(s, value, x + Inches(0.18), yy + Inches(0.26), span(3) - Inches(0.36), Inches(0.8),
           size=METRIC_PT, color=hx(ACCENT_TEXT), font=HEAD_FONT, shrink=True)
    d.text(s, label, x + Inches(0.18), yy + Inches(1.22), span(3) - Inches(0.36), Inches(0.28),
           size=CAPTION_PT, color=hx(MUTED), bold=True, font=BODY_FONT)
footer(s, FOOT)

# ── L03 Positioning ──────────────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L03 · Positioning", "Three evidence cards under one sentence")
d.text(s, "The thesis in one sentence, then the evidence that survives contact with it.",
       d.M, y, d.CW, Inches(0.34), size=BODY_PT, color=hx(MUTED), font=BODY_FONT)
card_row(s, y + Inches(0.52), [
    ("Where we win", "Named criterion, with the number that proves it."),
    ("What it costs", "Build, run, and the crossing point."),
    ("What must be true", "The assumption the case rests on."),
], h_in=2.1)
footer(s, FOOT)

# ── L04 Process chain ────────────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L04 · Process chain", "Four nodes, one outcome endpoint")
y2 = node_row(s, y + Inches(0.5), ["Intake", "Enrich", "Decide", "Act"], h_in=1.0)
slab(s, col_x(0), y2 + Inches(0.45), d.CW, 1.5, "Outcome",
     "One endpoint, annotated below the chain — never a fifth node.")
footer(s, FOOT)

# ── L05 Pillars ──────────────────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L05 · Reasons or pillars", "Four equal pillars, numbered")
card_row(s, y + Inches(0.4), [
    ("01 Speed", "Weeks, not quarters."), ("02 Cost", "Run cost named, not implied."),
    ("03 Risk", "Owner per risk."), ("04 Reach", "Markets it opens."),
], h_in=2.5)
footer(s, FOOT)

# ── L06 KPI landscape ────────────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L06 · Opportunity landscape", "Metric tiles on top, assumptions below")
y2 = kpi_row(s, y + Inches(0.3), [("$4.2M", "ADDRESSABLE"), ("31%", "ATTACH"), ("9wk", "TIME TO VALUE")])
card_row(s, y2 + Inches(0.4), [
    ("Assumption", "Stated on the slide, not in the appendix."),
    ("Sensitivity", "Which driver moves the answer most."),
], h_in=1.7)
footer(s, FOOT)

# ── L07 Solution architecture ────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L07 · Solution architecture", "Hero diagram left, capability layers right")
d.rect(s, col_x(0), y + Inches(0.3), span(7), Inches(3.4), hx(SURFACE), line=hx(LINE), radius=adj(3.4))
d.text(s, "System view", col_x(0) + Inches(0.22), y + Inches(0.5), span(7) - Inches(0.44),
       Inches(0.32), size=CARD_PT, color=hx(INK), bold=True, font=BODY_FONT)
for i, layer in enumerate(["Experience", "Orchestration", "Data"]):
    card(s, col_x(7), y + Inches(0.3 + 1.18 * i), span(5), 1.0, layer, "", fill=SURFACE)
footer(s, FOOT)

# ── L08 Technical deep dive ──────────────────────────────────────────────────
s = d.slide(fill=hx(INK))
y = header(s, "L08 · Technical deep dive", "Centered diagram on midnight", dark=True)
d.rect(s, col_x(1), y + Inches(0.35), span(10), Inches(3.3), hx("#12243A"), radius=adj(3.3))
d.text(s, "Centered system diagram", col_x(1), y + Inches(1.75), span(10), Inches(0.4),
       size=CARD_PT, color=hx(PAGE), bold=True, align=PP_ALIGN.CENTER, font=BODY_FONT)
d.text(s, "Cyan dimensions and annotations", col_x(1), y + Inches(2.2), span(10), Inches(0.32),
       size=BODY_PT, color=hx(ACCENT), align=PP_ALIGN.CENTER, font=BODY_FONT)
footer(s, FOOT, dark=True)

# ── L09 Option matrix ────────────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L09 · Product or service matrix", "Six columns, one recommended")
for i, (name, note) in enumerate([("A", "—"), ("B", "—"), ("C", "—"),
                                  ("D", "Recommended"), ("E", "—"), ("F", "—")]):
    picked = name == "D"
    card(s, col_x(i * 2), y + Inches(0.4), span(2), 2.4, name, note,
         fill=ACCENT_FILL if picked else SURFACE, fg=PAGE if picked else INK,
         note_color=PAGE if picked else MUTED)
footer(s, FOOT)

# ── L10 Competitive comparison ───────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L10 · Competitive comparison", "One clear win, one honest limitation")
card_row(s, y + Inches(0.4), [
    ("We win", "Named criterion and the margin."),
    ("We tie", "Where the field has converged."),
    ("We lose", "Stated plainly, with the plan."),
], h_in=2.5)
footer(s, FOOT)

# ── L11 Roadmap ──────────────────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L11 · Roadmap and validation", "Phases across, evidence and risk below")
y2 = node_row(s, y + Inches(0.35), ["Sprint", "Scale", "Sustain", "Transfer"])
card_row(s, y2 + Inches(0.4), [
    ("Evidence", "A gate per phase, not a status colour."),
    ("Risk", "Owner named beside every risk."),
], h_in=1.7)
footer(s, FOOT)

# ── L12 Financial evidence ───────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L12 · Financial evidence", "Table plus three aligned callouts")
y2 = kpi_row(s, y + Inches(0.3), [("+14pt", "GROSS MARGIN"), ("$1.1M", "RUN RATE"), ("0.7x", "CAC PAYBACK")])
d.rect(s, col_x(0), y2 + Inches(0.4), d.CW, Inches(1.6), hx("#F4F8FE"), line=hx(LINE), radius=adj(1.6))
d.text(s, "Units, timeframe, and whether values are actual, target or forecast — stated on the table itself.",
       col_x(0) + Inches(0.24), y2 + Inches(0.75), d.CW - Inches(0.48), Inches(0.9),
       size=BODY_PT, color=hx(INK), font=BODY_FONT, shrink=True)
footer(s, FOOT)

# ── L13 Cost clarity ─────────────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L13 · Cost or concept clarity", "Three large numbers, one implication")
y2 = kpi_row(s, y + Inches(0.3), [("$180k", "BUILD"), ("$26k/yr", "RUN"), ("$310k", "AVOIDED")])
slab(s, col_x(0), y2 + Inches(0.4), d.CW, 1.6, "Bottom line",
     "The implication, not the arithmetic — what the reader should now decide.")
footer(s, FOOT)

# ── L14 The ask ──────────────────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L14 · Ask or next step", "Midnight ask left, resourcing right")
slab(s, col_x(0), y + Inches(0.4), span(5), 3.3, "Approve phase one",
     "One decision. One owner. One date.")
d.rect(s, col_x(5), y + Inches(0.4), span(7), Inches(3.3), hx("#F4F8FE"), line=hx(LINE), radius=adj(3.3))
d.text(s, "Use of resources", col_x(5) + Inches(0.24), y + Inches(0.62), span(7) - Inches(0.48),
       Inches(0.34), size=CARD_PT, color=hx(INK), bold=True, font=BODY_FONT)
d.text(s, [{"text": t, "bullet": True, "space_before": 6} for t in
           ["Owner per workstream", "Milestone per month", "The gate that stops it"]],
       col_x(5) + Inches(0.24), y + Inches(1.1), span(7) - Inches(0.48), Inches(2.4),
       size=BODY_PT, color=hx(INK), font=BODY_FONT)
footer(s, FOOT)

# ── L15 Governance ───────────────────────────────────────────────────────────
s = d.slide(fill=hx(PAGE))
y = header(s, "L15 · Team or governance", "Leaders above, capability grid below")
y2 = card_row(s, y + Inches(0.3), [
    ("Sponsor", "Role evidence over biography."),
    ("Delivery lead", "Role evidence over biography."),
    ("Architect", "Role evidence over biography."),
], h_in=1.5)
card_row(s, y2 + Inches(0.35), [("Security", "—"), ("Data", "—"), ("Change", "—"), ("Ops", "—")], h_in=1.2)
footer(s, FOOT)

# ── L16 Closing montage ──────────────────────────────────────────────────────
s = d.slide(fill=hx(INK))
y = header(s, "L16 · Closing proof montage", "One line, then the proof", dark=True)
for i in range(4):
    x = col_x(i * 3)
    d.rect(s, x, y + Inches(0.5), span(3), Inches(2.3), hx("#12243A"), radius=adj(2.3))
    d.text(s, f"Proof {i + 1}", x + Inches(0.2), y + Inches(2.35), span(3) - Inches(0.4),
           Inches(0.3), size=CAPTION_PT, color=hx(PALE), font=BODY_FONT)
footer(s, FOOT, dark=True)

out = d.save(RUN / "L01-L16-Layout-Library-reviewed.pptx")
print(f"profile: title {TITLE_PT}pt · body {BODY_PT}pt · caption {CAPTION_PT}pt · "
      f"margin {MARGIN_IN}in · {COLUMNS}col/{GUTTER_IN}in · radius {RADIUS_IN}in")
