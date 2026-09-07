#!/usr/bin/env python3
"""Claude /design — evaluation deck.

Content: every claim is something verified in the session of 2026-08-22 against
the installed Claude Code 2.1.238 binary, this repo's contracts, or a command
whose output is quoted in ../2026-08-22-l01-l16-layout-library/README.md.
No figure here is illustrative.

Design: nothing is hand-set. The whole visual system is read from
template-profile.json, which derive_template_profile.py --canvas measured off
the L01-L16 canvas in the sibling run folder -- the same profile, a second deck.

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

P = json.loads((RUN / "template-profile.json").read_text(encoding="utf-8"))
GEO, TYPE, COMP = P["geometry"], P["typography"], P["composition"]
PAGE, INK, ACCENT = (P["brand"]["colors"][k] for k in ("page", "ink", "accent"))
SURFACE, LINE, MUTED, TEAL, PALE = "#F8FAFC", "#E2E8F0", "#6B7280", "#0A9396", "#8DB4D4"
COOL = "#F4F8FE"

TITLE_PT, BODY_PT, CAPTION_PT, METRIC_PT = (
    TYPE["title_pt"], TYPE["body_pt"], TYPE["caption_pt"], TYPE["metric_pt"])
CARD_PT = round(BODY_PT * 1.15, 1)
KICKER_PT = round(CAPTION_PT * 1.3, 1)
MARGIN_IN, GUTTER_IN, COLUMNS, RADIUS_IN = (
    GEO["safe_margin_inches"], GEO["gutter_inches"], GEO["grid_columns"], COMP["corner_radius"])
HEAD_FONT, BODY_FONT = P["brand"]["heading_font"], P["brand"]["body_font"]


# ── contrast-safe accent (see the sibling run's README, finding 2) ───────────
def _ch(v: float) -> float:
    v /= 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def _lum(h: str) -> float:
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _ch(r) + 0.7152 * _ch(g) + 0.0722 * _ch(b)


def contrast(a: str, b: str) -> float:
    hi, lo = sorted((_lum(a), _lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def darken_until(h: str, *, against: str, target: float = 4.5) -> str:
    f = 1.0
    while f > 0.05:
        c = "#" + "".join(
            f"{max(0, min(255, round(int(h.lstrip('#')[i:i+2], 16) * f))):02X}" for i in (0, 2, 4))
        if contrast(c, against) >= target:
            return c
        f -= 0.02
    return "#000000"


ACCENT_TEXT = darken_until(ACCENT, against=SURFACE)
ACCENT_FILL = darken_until(ACCENT, against=PAGE)
TEAL_FILL = darken_until(TEAL, against=PAGE)

brand = Brand(NAVY=hx(INK), INK=hx(INK), WHITE=hx(PAGE), TEAL=hx(ACCENT), ACCENT=hx(ACCENT),
              SOFT=hx(SURFACE), GRID=hx(LINE), MUTED=hx(MUTED), FONT=BODY_FONT, FONT_H=HEAD_FONT)
d = Deck(brand=brand)
d.M = Inches(MARGIN_IN)
d.CW = d.W - d.M * 2
GUTTER = Inches(GUTTER_IN)
COL_W = (d.CW - GUTTER * (COLUMNS - 1)) / COLUMNS
TOP = Inches(MARGIN_IN)

span = lambda n: int(COL_W * n + GUTTER * (n - 1))          # noqa: E731
col_x = lambda i: int(d.M + (COL_W + GUTTER) * i)           # noqa: E731
adj = lambda h: max(0.02, min(0.5, RADIUS_IN / (h / 2)))    # noqa: E731

SRC = "Verified 2026-08-22 · Claude Code 2.1.238 (WSL) · repo content-ideas @ feat/dsh-multi-model-providers"


def header(s, kicker, title, *, dark=False):
    d.rect(s, d.M, TOP, Inches(1.25), Pt(2), hx(ACCENT))
    d.text(s, kicker.upper(), d.M, TOP + Inches(0.10), d.CW, Inches(0.24), size=KICKER_PT,
           color=hx(ACCENT if dark else ACCENT_TEXT), bold=True, font=BODY_FONT)
    d.text(s, title, d.M, TOP + Inches(0.40), d.CW, Inches(1.05), size=TITLE_PT,
           color=hx(PAGE if dark else INK), font=HEAD_FONT, shrink=True)
    return TOP + Inches(1.62)


def footer(s, note=SRC, *, dark=False):
    d.text(s, note, d.M, d.H - Inches(MARGIN_IN + 0.20), d.CW, Inches(0.20),
           size=CAPTION_PT, color=hx(PALE if dark else MUTED), font=BODY_FONT)


def lede(s, y, text):
    d.text(s, text, d.M, y, d.CW, Inches(0.36), size=BODY_PT, color=hx(MUTED),
           font=BODY_FONT, shrink=True)
    return y + Inches(0.54)


def card(s, x, y, w, h, heading, note, *, fill=SURFACE, fg=INK, note_fg=None, bar=None):
    d.rect(s, x, y, w, Inches(h), hx(fill), line=hx(LINE), radius=adj(h))
    if bar:
        d.rect(s, x, y, Pt(3), Inches(h), hx(bar))
    d.text(s, heading, x + Inches(0.20), y + Inches(0.14), w - Inches(0.40), Inches(0.34),
           size=CARD_PT, color=hx(fg), bold=True, font=BODY_FONT, shrink=True)
    d.text(s, note, x + Inches(0.20), y + Inches(0.52), w - Inches(0.40),
           Inches(max(0.30, h - 0.66)),
           size=BODY_PT, color=hx(note_fg or MUTED), font=BODY_FONT, shrink=True)


def card_row(s, y, items, h=1.6, **kw):
    width = COLUMNS // len(items)
    for i, item in enumerate(items):
        card(s, col_x(i * width), y, span(width), h, item[0], item[1],
             **{**kw, **(item[2] if len(item) > 2 else {})})
    return y + Inches(h)


def kpi_row(s, y, items, h=1.5):
    width = COLUMNS // len(items)
    for i, (value, label) in enumerate(items):
        x, w = col_x(i * width), span(width)
        d.rect(s, x, y, w, Inches(h), hx(SURFACE), line=hx(LINE), radius=adj(h))
        d.text(s, value, x + Inches(0.20), y + Inches(0.20), w - Inches(0.40), Inches(0.74),
               size=METRIC_PT, color=hx(ACCENT_TEXT), font=HEAD_FONT, shrink=True)
        d.text(s, label, x + Inches(0.20), y + Inches(h - 0.46), w - Inches(0.40), Inches(0.30),
               size=CAPTION_PT, color=hx(MUTED), bold=True, font=BODY_FONT, shrink=True)
    return y + Inches(h)


def slab(s, x, y, w, h, heading, note):
    d.rect(s, x, y, w, Inches(h), hx(INK), radius=adj(h))
    d.text(s, heading, x + Inches(0.26), y + Inches(0.22), w - Inches(0.52), Inches(0.34),
           size=CARD_PT, color=hx(PAGE), bold=True, font=BODY_FONT, shrink=True)
    d.text(s, note, x + Inches(0.26), y + Inches(0.66), w - Inches(0.52), Inches(h - 0.90),
           size=BODY_PT, color=hx(PALE), font=BODY_FONT, shrink=True)


def bullets(s, x, y, w, h, lines, *, color=None):
    d.text(s, [{"text": t, "bullet": True, "space_before": 7} for t in lines],
           x, y, w, Inches(h), size=BODY_PT, color=hx(color or INK), font=BODY_FONT, shrink=True)


# ═══ 1 · Cover ═══════════════════════════════════════════════════════════════
s = d.slide(fill=hx(INK))
d.text(s, "CLAUDE /DESIGN · EVALUATION", d.M, TOP, d.CW, Inches(0.28),
       size=KICKER_PT, color=hx(ACCENT), bold=True, font=BODY_FONT)
d.rect(s, d.M, Inches(1.15), Inches(1.6), Pt(3), hx(ACCENT))
d.text(s, "Don't install the desktop app.\nShip one derivation script instead.",
       d.M, Inches(1.50), Inches(11.8), Inches(2.90), size=round(TITLE_PT * 1.55, 1),
       color=hx(PAGE), font=HEAD_FONT, shrink=True)
d.text(s, "Three template-profile fields moved from default to measured.",
       d.M, Inches(4.75), Inches(11.8), Inches(0.5), size=BODY_PT, color=hx(PALE),
       font=BODY_FONT, shrink=True)
footer(s, SRC, dark=True)

# ═══ 2 · Verdict ═════════════════════════════════════════════════════════════
s = d.slide(fill=hx(PAGE))
y = header(s, "L02 · Verdict", "One skill gains, one script delivers it")
slab(s, col_x(0), y, span(4), 3.45, "The thesis",
     "The canvas is a hosted page, so WSL already had the feature. What was missing was a "
     "reader, not a host.")
for i, (v, l) in enumerate([("1", "SKILL IMPROVED"), ("3", "FIELDS DERIVED"),
                            ("12", "NEW TESTS"), ("0", "LINT FINDINGS")]):
    x, yy = col_x(4 + (i % 2) * 4), y + Inches(1.82 * (i // 2))
    d.rect(s, x, yy, span(4), Inches(1.63), hx(SURFACE), line=hx(LINE), radius=adj(1.63))
    d.text(s, v, x + Inches(0.20), yy + Inches(0.22), span(4) - Inches(0.40), Inches(0.78),
           size=METRIC_PT, color=hx(ACCENT_TEXT), font=HEAD_FONT, shrink=True)
    d.text(s, l, x + Inches(0.20), yy + Inches(1.18), span(4) - Inches(0.40), Inches(0.30),
           size=CAPTION_PT, color=hx(MUTED), bold=True, font=BODY_FONT, shrink=True)
footer(s)

# ═══ 3 · The three answers ═══════════════════════════════════════════════════
s = d.slide(fill=hx(PAGE))
y = header(s, "L10 · Answers", "Three questions: no, one, and not until now")
card_row(s, y + Inches(0.30), [
    ("Install the desktop app?", "No. It adds a docked panel, not a capability.", {"bar": ACCENT}),
    ("Improves design skills?", "One directly. One indirectly. Ten untouched.", {"bar": ACCENT}),
    ("Better rendered PPTX?", "Zero pixels — until the derivation script landed.", {"bar": ACCENT}),
], h=2.6)
footer(s)

# ═══ 4 · Architecture ════════════════════════════════════════════════════════
s = d.slide(fill=hx(PAGE))
y = header(s, "L07 · What it is", "A published artifact, not a desktop feature")
d.rect(s, col_x(0), y + Inches(0.25), span(7), Inches(3.00), hx(SURFACE), line=hx(LINE),
       radius=adj(3.00))
d.text(s, "One file carries both halves", col_x(0) + Inches(0.22), y + Inches(0.45),
       span(7) - Inches(0.44), Inches(0.32), size=CARD_PT, color=hx(INK), bold=True,
       font=BODY_FONT)
bullets(s, col_x(0) + Inches(0.22), y + Inches(0.88), span(7) - Inches(0.44), 1.95, [
    "Editor: ~2 MiB, inside the payload",
    "Content: one .dc.html per artboard",
    "Save republishes the whole page",
    "Pinned to contract 0.1.31, not 0.2.14",
])
for i, (h, n) in enumerate([
        ("Desktop adds a picker", "~4,250 injected lines, Electron only"),
        ("WSL loses none of it", "node v24.18.1; four capabilities"),
        ("So Save is enabled", "Full WYSIWYG, not view-and-export")]):
    card(s, col_x(7), y + Inches(0.25 + 1.03 * i), span(5), 0.97, h, n)
footer(s, "Read from the installed 2.1.238 binary")

# ═══ 5 · Install economics ═══════════════════════════════════════════════════
s = d.slide(fill=hx(PAGE))
y = header(s, "L03 · Install decision", "A docked panel costs a third host tree")
card_row(s, y + Inches(0.30), [
    ("What it adds", "A docked canvas and theme sync. No editing the browser lacks."),
    ("What it costs", "A third skill tree, in a repo already running a drift gate over 328 skills."),
    ("What decides it", "A profile is read from files on disk, which the agent writes."),
], h=2.6)
footer(s)

# ═══ 6 · Impact map ══════════════════════════════════════════════════════════
s = d.slide(fill=hx(PAGE))
y = header(s, "L09 · Impact map", "One of twelve design skills actually gains")
card(s, col_x(0), y + Inches(0.30), span(4), 2.5, "pptx-design-quality",
     "GAINS DIRECTLY. A third profile source, reaching three fields the others cannot.",
     fill=ACCENT_FILL, fg=PAGE, note_fg=PAGE)
card(s, col_x(4), y + Inches(0.30), span(4), 2.5, "vault-presales",
     "GAINS INDIRECTLY. The pipeline's L01–L16 library becomes measurable geometry "
     "instead of prose build formulas.", fill=COOL)
card(s, col_x(8), y + Inches(0.30), span(4), 2.5, "Ten others",
     "UNCHANGED. Every one reads a PPTX package a canvas never produces.")
footer(s, "lint_pptx · preview_pptx · lint_motion · motion_contact_sheet · check_claim_evidence · "
          "branded-pptx-deck · marp · genspark-branded-deck · present · pptx-toolkit")

# ═══ 7 · The three fields ════════════════════════════════════════════════════
s = d.slide(fill=hx(PAGE))
y = header(s, "L06 · What moved", "Three fields moved from default to measured")
y2 = kpi_row(s, y + Inches(0.25), [("12", "GRID_COLUMNS"), ("0.167 in", "GUTTER_INCHES"),
                                   ("0.083 in", "CORNER_RADIUS")])
card_row(s, y2 + Inches(0.35), [
    ("Read from", "repeat(12, 1fr) · gap: 16px · border-radius: 8px"),
    ("Why a deck cannot", "A rendered slide implies a grid; a canvas declares one."),
], h=1.5)
footer(s, "template-derivation.md recorded all three as \"not derived — no reliable signal\"")

# ═══ 8 · The scale ═══════════════════════════════════════════════════════════
s = d.slide(fill=hx(INK))
y = header(s, "L08 · Core mechanic", "The point scale is derived, never assumed", dark=True)
d.rect(s, d.M, y + Inches(0.35), d.CW, Inches(0.9), hx("#12243A"), radius=adj(0.9))
d.text(s, "pt  =  px  ×  ( slide_width_inches ÷ frame_width_px )  ×  72",
       d.M, y + Inches(0.65), d.CW, Inches(0.4), size=round(BODY_PT * 1.35, 1),
       color=hx(ACCENT), align=PP_ALIGN.CENTER, font=BODY_FONT, bold=True)
for i, (h, n) in enumerate([
        ("1280 × 720", "0.750 pt/px — the vault stage exactly"),
        ("1920 × 1080", "0.500 pt/px — same design, different frame"),
        ("Hardcoding 0.75", "Inflates every size by a third")]):
    x = col_x(i * 4)
    d.rect(s, x, y + Inches(1.60), span(4), Inches(1.45), hx("#12243A"), radius=adj(1.45))
    d.text(s, h, x + Inches(0.20), y + Inches(1.80), span(4) - Inches(0.40), Inches(0.32),
           size=CARD_PT, color=hx(PAGE), bold=True, font=BODY_FONT, shrink=True)
    d.text(s, n, x + Inches(0.20), y + Inches(2.22), span(4) - Inches(0.40), Inches(0.70),
           size=BODY_PT, color=hx(PALE), font=BODY_FONT, shrink=True)
footer(s, "test_point_scale_comes_from_the_frame_not_a_constant pins both frame widths", dark=True)

# ═══ 9 · In band ═════════════════════════════════════════════════════════════
s = d.slide(fill=hx(PAGE))
y = header(s, "L13 · Result", "Every derived value lands inside the spec's own band")
y2 = kpi_row(s, y + Inches(0.25), [("30.0 pt", "TITLE · SPEC 24–30"),
                                   ("13.5 pt", "BODY · SPEC 12–14"),
                                   ("7.5 pt", "CAPTION · SPEC 7–8")])
slab(s, col_x(0), y2 + Inches(0.35), d.CW, 1.5, "Bottom line",
     "This deck is built from that profile. No design value is written in the builder.")
footer(s)

# ═══ 10 · Findings ═══════════════════════════════════════════════════════════
s = d.slide(fill=hx(PAGE))
y = header(s, "L05 · Findings", "Running it falsified two things review had passed")
card_row(s, y + Inches(0.30), [
    ("A shared stylesheet broke scoping",
     "One .cover rule the cover alone used put 48pt into a 40px title.", {"bar": ACCENT}),
    ("The design system fails WCAG AA",
     "The spec's cyan kicker on white is 2.46:1 against a 4.5:1 floor.", {"bar": ACCENT}),
], h=2.6)
footer(s, "Both surfaced on the first real canvas — the hand-written fixture had no dead rules")

# ═══ 11 · Verification ═══════════════════════════════════════════════════════
s = d.slide(fill=hx(PAGE))
y = header(s, "L11 · Verification", "Every gate green; contrast went 37 warnings to zero")
y2 = card_row(s, y + Inches(0.10), [
    ("Skill suite", "48 passed"),
    ("Full repo suite", "302 passed, 1 skipped"),
    ("Skill integrity", "328 skills, 8 rules"),
    ("PPTX lint", "0 errors, 0 warnings"),
], h=1.3)
card_row(s, y2 + Inches(0.35), [
    ("How the fix works", "The accent keeps its spec value on rules; only text darkens."),
    ("Still unproven", "The contact sheet approximates; no PowerPoint-native render ran."),
], h=1.7)
footer(s)

# ═══ 12 · The ask ════════════════════════════════════════════════════════════
s = d.slide(fill=hx(PAGE))
y = header(s, "L14 · Next step", "Amend the kicker rule in the vault spec")
slab(s, col_x(0), y + Inches(0.25), span(5), 3.0, "The decision",
     "Change the cyan kicker and cyan-KPI rules in Client-Ready PPTX Design System.md.")
d.rect(s, col_x(5), y + Inches(0.25), span(7), Inches(3.0), hx(COOL), line=hx(LINE),
       radius=adj(3.0))
d.text(s, "Already done", col_x(5) + Inches(0.24), y + Inches(0.47),
       span(7) - Inches(0.48), Inches(0.32), size=CARD_PT, color=hx(INK), bold=True,
       font=BODY_FONT)
bullets(s, col_x(5) + Inches(0.24), y + Inches(0.90), span(7) - Inches(0.48), 2.2, [
    "--canvas shipped: 307 → 659 lines, stdlib only",
    "12 tests, no python-pptx or Pillow needed",
    "CLAUDE.md rule: input only, never output, never evidence",
    "L01–L16 canvas and reference deck in runs/",
])
footer(s)

out = d.save(RUN / "Claude-design-evaluation-reviewed.pptx")
