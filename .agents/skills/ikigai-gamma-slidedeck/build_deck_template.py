#!/usr/bin/env python3
"""
Ikigai Pro Report — pptxkit Deck Builder Template
=================================================
This file is a TEMPLATE. Do NOT run it directly.

When the ikigai-gamma-slidedeck skill uses the pptxkit fallback path, it copies
this file into the run folder as `build_deck.py` and substitutes all
{{VAR}} placeholders with real values extracted from the ikigai report.

Substitution variables:
  {{PERSON_NAME}}         Full name  e.g. "Srikumar V R"
  {{PERSON_SLUG}}         URL-safe slug  e.g. "srikumar"
  {{PERSON_ROLE}}         Title · Company  e.g. "Director Strategic BD, FPT Software"
  {{TAGLINE}}             One-line summary
  {{VALIDATION_SCORE}}    Integer 0–100
  {{VALIDATION_LABEL}}    EXCEPTIONAL / STRONG GO / VIABLE
  {{RUN_DATE}}            e.g. "Jun 2026"
  {{FOOTER_TEXT}}         e.g. "Srikumar V R · Ikigai Pro Report · FPT Software GCC · Jun 2026"
  {{CREDENTIAL_CHIPS}}    Python list of 4 strings e.g. ["IIT Madras","IIM Calcutta","27 Years","5 Industries"]
  {{OUT_PATH}}            Absolute output path for the .pptx

BD/company-mode extra vars (omit for individual-first runs):
  {{COMPANY_NAME}}        e.g. "FPT Software"
  {{IS_BD_RUN}}           True / False
  {{COMPANY_CAPS_CARDS}}  Python list of (title, body) tuples — 8 items
  {{KPI_DATA}}            Python list of (number, label, note) tuples — 6 items
  {{AI_BADGES}}           Python list of (title, desc) tuples — 3 items
  {{AI_STATS}}            Python list of (number, label) tuples — 5 items
  {{TESTIMONIALS}}        Python list of (client, industry, quote) tuples — 5 items
  {{USE_CASE_1}}          Dict: title, subtitle, challenge, solution, results, platform, gcc_rel
  {{USE_CASE_2}}          Dict: title, subtitle, challenge, solution, results, platform, gcc_rel
  {{PROOF_ITEMS}}         Python list of (title, body) tuples — 6 items

Content vars (both modes):
  {{QUAD_CARDS}}          Python list of 4 (fill, accent, title, body) tuples for ikigai map
  {{CAP_TABLE_ROWS}}      Python list of rows for capability table (incl. header row)
  {{CAP_COL_WIDTHS}}      Python list of 3 Inches values
  {{LOVES_BULLETS}}       Python list of 6 strings
  {{GOODAT_BULLETS}}      Python list of 6 strings
  {{NICHE_LAYERS}}        Python list of (fill, accent, label, body) tuples — 3 items
  {{SCORECARD_ROWS}}      Python list of rows for scorecard table (incl. header + composite)
  {{AVOID_BULLETS}}       Python list of 4 strings
  {{GAP_BODY}}            String
  {{TIMING_CARDS}}        Python list of (title, body) tuples — 4 items
  {{COMPETITOR_ROWS}}     Python list of rows for competitor table (incl. header + winner row)
  {{TIERS}}               Python list of (badge, name, price, includes, ideal) tuples — 3 items
  {{REVENUE_ROWS}}        Python list of rows for revenue table
  {{REVENUE_PROOF}}       String — e.g. proof stat strip
  {{MILESTONE_ROWS}}      Python list of rows for milestone table
  {{DAY13_BODY}}          String — days 1–3 content (left panel, dark)
  {{DAY47_BODY}}          String — days 4–7 content (right panel, light)
  {{PHASES}}              Python list of (label, revenue, desc) tuples — 4 items
  {{ONE_LINER_QUOTE}}     String — the positioning sentence
  {{CLOSING_COLS}}        Python list of (fill, accent, title, body) tuples — 3 items
  {{CLOSING_CTA}}         String — closing call-to-action line

Usage after substitution:
  python3 build_deck.py
"""

import sys
sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Brand, Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor

# ── CONFIGURATION (substitute these) ─────────────────────────────────────────
PERSON_NAME     = "{{PERSON_NAME}}"
PERSON_ROLE     = "{{PERSON_ROLE}}"
TAGLINE         = "{{TAGLINE}}"
SCORE           = {{VALIDATION_SCORE}}
SCORE_LABEL     = "{{VALIDATION_LABEL}}"
RUN_DATE        = "{{RUN_DATE}}"
FOOTER          = "{{FOOTER_TEXT}}"
OUT             = "{{OUT_PATH}}"
IS_BD_RUN       = {{IS_BD_RUN}}          # True for BD/company role; False for solo founder
COMPANY_NAME    = "{{COMPANY_NAME}}"     # "" if individual-first
CREDENTIAL_CHIPS = {{CREDENTIAL_CHIPS}}  # list of 4 short strings

# Slide content (substitute from report) ─────────────────────────────────────
CORE_INSIGHT_TITLE = "{{CORE_INSIGHT_TITLE}}"
CORE_INSIGHT_BODY  = [
    # dict format: {"text": "...", "size": 14, "color": None, "bold": False, "space_before": 14}
    {{CORE_INSIGHT_BODY_PARAS}}
]
QUAD_CARDS = {{QUAD_CARDS}}         # [(fill_hex, accent_hex, title, body), ...]
CAP_TABLE_ROWS = {{CAP_TABLE_ROWS}} # [["col1","col2","col3"], ...]
CAP_COL_WIDTHS = {{CAP_COL_WIDTHS}} # [Inches(x), ...]

# Proof point slides (BD/company mode)
COMPANY_CAPS_CARDS = {{COMPANY_CAPS_CARDS}}  # [(title, body), ...] × 8
KPI_DATA = {{KPI_DATA}}                       # [(number, label, note), ...] × 6
AI_BADGES = {{AI_BADGES}}                     # [(title, desc), ...] × 3
AI_STATS  = {{AI_STATS}}                      # [(number, label), ...] × 5
AI_EXTRA_NOTE = "{{AI_EXTRA_NOTE}}"
TESTIMONIALS = {{TESTIMONIALS}}               # [(client, industry, quote), ...] × 5
USE_CASE_1 = {{USE_CASE_1}}                   # dict
USE_CASE_2 = {{USE_CASE_2}}                   # dict
PROOF_ITEMS = {{PROOF_ITEMS}}                 # [(title, body), ...] × 6

# Body slides
LOVES_BULLETS    = {{LOVES_BULLETS}}
GOODAT_BULLETS   = {{GOODAT_BULLETS}}
NICHE_LAYERS     = {{NICHE_LAYERS}}
SCORECARD_ROWS   = {{SCORECARD_ROWS}}
AVOID_BULLETS    = {{AVOID_BULLETS}}
GAP_BODY         = "{{GAP_BODY}}"
TIMING_CARDS     = {{TIMING_CARDS}}
COMPETITOR_ROWS  = {{COMPETITOR_ROWS}}
TIERS            = {{TIERS}}
REVENUE_ROWS     = {{REVENUE_ROWS}}
REVENUE_PROOF    = {{REVENUE_PROOF}}    # list of strings for stat strip
MILESTONE_ROWS   = {{MILESTONE_ROWS}}
DAY13_BODY       = "{{DAY13_BODY}}"
DAY47_BODY       = "{{DAY47_BODY}}"
PHASES           = {{PHASES}}
ONE_LINER_QUOTE  = "{{ONE_LINER_QUOTE}}"
CLOSING_COLS     = {{CLOSING_COLS}}
CLOSING_CTA      = "{{CLOSING_CTA}}"

# ── DECK SETUP ────────────────────────────────────────────────────────────────
d = Deck(footer=FOOTER)
b = d.b
W, H, M, CW = d.W, d.H, d.M, d.CW

# Compute slide total: 14 fixed + 6 proof-point slides if BD run
TOTAL = 20 if not IS_BD_RUN else 26

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────

def table_rows(s, rows, left, top, col_widths, row_h=Inches(0.42),
               header_fill=None, alt_fill=None, text_size=11.5, header_text_size=12):
    for ri, row in enumerate(rows):
        is_header = (ri == 0 and header_fill is not None)
        fill = header_fill if is_header else (b.SOFT if (alt_fill and ri % 2 == 0) else b.WHITE)
        row_y = top + ri * row_h
        x = left
        for ci, (cell, cw) in enumerate(zip(row, col_widths)):
            d.rect(s, x, row_y, cw, row_h, fill, line=b.GRID)
            tc = b.WHITE if is_header else b.INK
            sz = header_text_size if is_header else text_size
            d.text(s, cell, x + Inches(0.08), row_y + Inches(0.05),
                   cw - Inches(0.16), row_h - Inches(0.05),
                   size=sz, color=tc, bold=is_header, shrink=True, anchor=MSO_ANCHOR.MIDDLE)
            x += cw

def kpi_box(s, cx, cy, bw, bh, number, label, note=None):
    d.rect(s, cx, cy, bw, bh, b.NAVY_2, radius=0.04)
    d.rect(s, cx, cy, bw, Inches(0.05), b.TEAL)
    d.text(s, number, cx + Inches(0.1), cy + Inches(0.12),
           bw - Inches(0.2), Inches(0.62),
           size=28, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, label, cx + Inches(0.1), cy + Inches(0.75),
           bw - Inches(0.2), Inches(0.32),
           size=11, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    if note:
        d.text(s, note, cx + Inches(0.1), cy + Inches(1.08),
               bw - Inches(0.2), Inches(0.28),
               size=9, color=b.MUTED, align=PP_ALIGN.CENTER, shrink=True)

def use_case_slide(s, pg, uc):
    d.rect(s, 0, 0, W, H, b.NAVY)
    d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
    d.text(s, "USE CASE", M, Inches(0.25), Inches(2), Inches(0.3), size=10, color=b.TEAL, bold=True)
    d.text(s, uc["title"], M, Inches(0.45), CW - Inches(3), Inches(0.62),
           size=24, color=b.WHITE, bold=True, shrink=True)
    d.text(s, uc["subtitle"], M, Inches(1.12), CW - Inches(3), Inches(0.35), size=13, color=b.LIGHT_TEAL)
    lw = Inches(5.8)
    for ypos, label, body in [
        (Inches(1.62), "CHALLENGE", uc["challenge"]),
        (Inches(2.92), "FPT SOLUTION", uc["solution"]),
    ]:
        h = Inches(1.18) if ypos < Inches(2) else Inches(1.28)
        d.rect(s, M, ypos, lw, h, b.NAVY_2, radius=0.03)
        d.text(s, label, M + Inches(0.15), ypos + Inches(0.1), lw - Inches(0.2), Inches(0.28),
               size=10, color=b.TEAL, bold=True)
        d.text(s, body, M + Inches(0.15), ypos + Inches(0.38), lw - Inches(0.2), h - Inches(0.45),
               size=11.5, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, M, Inches(4.32), lw, Inches(1.12), b.TEAL, radius=0.03)
    d.text(s, "RESULTS", M + Inches(0.15), Inches(4.42), lw - Inches(0.2), Inches(0.28),
           size=10, color=b.NAVY, bold=True)
    d.text(s, uc["results"], M + Inches(0.15), Inches(4.7), lw - Inches(0.2), Inches(0.66),
           size=12, color=b.NAVY, bold=True, shrink=True)
    rx = M + lw + Inches(0.2)
    rw = CW - lw - Inches(0.2)
    for ypos, label, body in [
        (Inches(1.62), "PLATFORM", uc["platform"]),
        (Inches(3.36), "GCC RELEVANCE", uc["gcc_rel"]),
    ]:
        h = Inches(1.62) if ypos < Inches(2) else Inches(2.1)
        d.rect(s, rx, ypos, rw, h, b.NAVY_2, radius=0.03)
        d.text(s, label, rx + Inches(0.15), ypos + Inches(0.1), rw - Inches(0.2), Inches(0.28),
               size=10, color=b.GOLD, bold=True)
        d.text(s, body, rx + Inches(0.15), ypos + Inches(0.38), rw - Inches(0.2), h - Inches(0.45),
               size=11, color=b.LIGHT_TEAL, shrink=True)
    d.footer(s, pg, TOTAL, dark=True)

# ── PAGE COUNTER (auto-increments) ───────────────────────────────────────────
_pg = [0]
def next_pg():
    _pg[0] += 1
    return _pg[0]

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.rect(s, W - Inches(0.25), 0, Inches(0.25), H, b.NAVY_2)
d.rect(s, W - Inches(0.28), 0, Inches(0.06), H, b.TEAL)
d.text(s, "IKIGAI PRO REPORT", M, Inches(0.85), CW, Inches(0.4), size=13, color=b.TEAL, bold=True)
d.text(s, PERSON_NAME, M, Inches(1.35), CW - Inches(4), Inches(1.1),
       size=52, color=b.WHITE, bold=True, shrink=True)
d.rect(s, M, Inches(2.55), Inches(4), Inches(0.06), b.TEAL)
d.text(s, TAGLINE, M, Inches(2.72), CW - Inches(4), Inches(0.9), size=18, color=b.LIGHT_TEAL, shrink=True)
d.rect(s, M, Inches(3.85), Inches(3.4), Inches(0.75), b.GOLD, radius=0.04)
d.text(s, f"Validation Score  {SCORE} / 100  ·  {SCORE_LABEL}",
       M + Inches(0.12), Inches(3.93), Inches(3.2), Inches(0.55),
       size=14, color=b.NAVY, bold=True, shrink=True)
d.text(s, f"{PERSON_ROLE}  ·  {RUN_DATE}", M, Inches(4.78), CW, Inches(0.35), size=13, color=b.MUTED)
for i, chip in enumerate(CREDENTIAL_CHIPS):
    cx = M + i * Inches(2.1)
    d.rect(s, cx, Inches(5.3), Inches(1.95), Inches(0.38), b.NAVY_2, radius=0.08)
    d.text(s, chip, cx + Inches(0.12), Inches(5.34), Inches(1.72), Inches(0.3),
           size=11.5, color=b.TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE)
d.footer(s, pg, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — CORE INSIGHT
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, CORE_INSIGHT_TITLE, "Core Insight")
d.text(s, CORE_INSIGHT_BODY, M, Inches(1.65), CW - Inches(3.5), Inches(4.5), shrink=True)
d.rect(s, W - Inches(3.3), Inches(1.8), Inches(2.7), Inches(1.5), b.NAVY, radius=0.04)
d.text(s, str(SCORE), W - Inches(3.1), Inches(1.95), Inches(2.5), Inches(0.7),
       size=42, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.text(s, SCORE_LABEL, W - Inches(3.1), Inches(2.68), Inches(2.5), Inches(0.4),
       size=13, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — PROFILE SNAPSHOT (generate from report career table)
# ═══════════════════════════════════════════════════════════════════════════════
# NOTE: substitute CAREER_ROWS (list of lists) and CAREER_COL_WIDTHS from report
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "{{CAREER_HEADER_SUBTITLE}}", "Profile Snapshot")
career_rows = {{CAREER_ROWS}}    # [["Company","Role","Period","Domain"], ...]
career_col_w = {{CAREER_COL_WIDTHS}}  # [Inches(2.4), Inches(2.8), Inches(1.6), Inches(5.1)]
table_rows(s, career_rows, M, Inches(1.72), career_col_w,
           row_h=Inches(0.52), header_fill=b.NAVY, alt_fill=True, text_size=10.5)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — IKIGAI MAP
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "Four Dimensions · One Intersection · One Unique Position", "Ikigai Map")
quad_w = Inches(5.9)
quad_h = Inches(2.4)
gap = Inches(0.15)
top_row = Inches(1.72)
bot_row = top_row + quad_h + gap
positions = [
    (M, top_row), (M + quad_w + gap, top_row),
    (M, bot_row), (M + quad_w + gap, bot_row),
]
for (qx, qy), (qfill, qaccent, qtitle, qbody) in zip(positions, QUAD_CARDS):
    d.rect(s, qx, qy, quad_w, quad_h, qfill, radius=0.03)
    d.rect(s, qx, qy, quad_w, Inches(0.06), qaccent)
    d.text(s, qtitle, qx + Inches(0.15), qy + Inches(0.1),
           quad_w - Inches(0.2), Inches(0.32), size=12, color=qaccent, bold=True)
    body_color = b.LIGHT_TEAL if qfill in (b.NAVY, b.NAVY_2) else b.WHITE
    d.text(s, qbody, qx + Inches(0.15), qy + Inches(0.48),
           quad_w - Inches(0.2), quad_h - Inches(0.55),
           size=10.5, color=body_color, shrink=True)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — CAPABILITY TABLE (What the World Needs)
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "{{CAP_TABLE_HEADER}}", "What the World Needs")
table_rows(s, CAP_TABLE_ROWS, M, Inches(1.68), CAP_COL_WIDTHS,
           row_h=Inches(0.54), header_fill=b.NAVY, alt_fill=True, text_size=10.5)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — CAPABILITY STACK CARDS (BD mode) / FLAGSHIP CAPABILITIES (solo mode)
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "{{CAPS_SLIDE_TITLE}}", M, Inches(0.38), CW, Inches(0.65),
       size=26, color=b.WHITE, bold=True, shrink=True)
d.text(s, "{{CAPS_SLIDE_SUBTITLE}}", M, Inches(1.22), CW, Inches(0.35), size=13, color=b.LIGHT_TEAL)
card_w = Inches(5.85)
card_h = Inches(1.22)
for i, (title, body) in enumerate(COMPANY_CAPS_CARDS):
    col = i % 2
    row = i // 2
    cx = M + col * (card_w + Inches(0.14))
    cy = Inches(1.72) + row * (card_h + Inches(0.14))
    d.rect(s, cx, cy, card_w, card_h, b.NAVY_2, radius=0.03, shadow=True)
    d.rect(s, cx, cy, Inches(0.07), card_h, b.TEAL)
    d.text(s, title, cx + Inches(0.15), cy + Inches(0.08),
           card_w - Inches(0.2), Inches(0.3), size=11, color=b.TEAL, bold=True, shrink=True)
    d.text(s, body, cx + Inches(0.15), cy + Inches(0.38),
           card_w - Inches(0.2), card_h - Inches(0.48), size=9.5, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, pg, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDES 7–12 — PROOF POINT SLIDES (BD/company mode only)
# ═══════════════════════════════════════════════════════════════════════════════
if IS_BD_RUN:
    # SLIDE 7 — Company scale KPIs
    pg = next_pg()
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
    d.text(s, f"{COMPANY_NAME} — Global Scale, Proven Delivery Track Record",
           M, Inches(0.38), CW, Inches(0.55), size=26, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "{{KPI_SLIDE_SUBTITLE}}", M, Inches(1.18), CW, Inches(0.35), size=13, color=b.LIGHT_TEAL)
    kpi_w = (CW - Inches(0.4)) / 3
    kpi_h = Inches(1.55)
    for i, (num, label, note) in enumerate(KPI_DATA):
        col = i % 3
        row = i // 3
        cx = M + col * (kpi_w + Inches(0.2))
        cy = Inches(1.68) + row * (kpi_h + Inches(0.18))
        kpi_box(s, cx, cy, kpi_w, kpi_h, num, label, note)
    d.footer(s, pg, TOTAL, dark=True)

    # SLIDE 8 — AI credentials + partnerships
    pg = next_pg()
    s = d.slide(fill=b.WHITE)
    d.header(s, f"{COMPANY_NAME} AI Credentials — First-Mover Partnerships + Production Scale",
             "AI Proof Points")
    badge_w = (CW - Inches(0.3)) / 3
    badge_h = Inches(1.1)
    for i, (title, desc) in enumerate(AI_BADGES):
        bx = M + i * (badge_w + Inches(0.15))
        d.rect(s, bx, Inches(1.72), badge_w, badge_h, b.NAVY, radius=0.04)
        d.rect(s, bx, Inches(1.72), badge_w, Inches(0.05), b.GOLD)
        d.text(s, title, bx + Inches(0.15), Inches(1.8),
               badge_w - Inches(0.25), Inches(0.42),
               size=13, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, desc, bx + Inches(0.15), Inches(2.24),
               badge_w - Inches(0.25), Inches(0.5),
               size=10, color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, M, Inches(3.0), CW, Inches(0.05), b.GRID)
    d.text(s, "PLATFORM METRICS", M, Inches(3.12), CW, Inches(0.3), size=11, color=b.MUTED, bold=True)
    stat_w = CW / len(AI_STATS)
    for i, (num, label) in enumerate(AI_STATS):
        sx = M + i * stat_w
        d.text(s, num, sx, Inches(3.5), stat_w, Inches(0.68),
               size=28, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, label, sx, Inches(4.2), stat_w, Inches(0.55),
               size=10.5, color=b.MUTED, align=PP_ALIGN.CENTER, shrink=True)
        if i < len(AI_STATS) - 1:
            d.rect(s, sx + stat_w - Inches(0.02), Inches(3.5), Inches(0.03), Inches(1.1), b.GRID)
    d.rect(s, M, Inches(5.05), CW, Inches(0.52), b.SOFT, radius=0.03)
    d.text(s, AI_EXTRA_NOTE, M + Inches(0.15), Inches(5.12), CW - Inches(0.25), Inches(0.38),
           size=11.5, color=b.INK, shrink=True)
    d.footer(s, pg, TOTAL)

    # SLIDE 9 — Client testimonials
    pg = next_pg()
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
    d.text(s, "What Global Leaders Say — From Fortune 500 to Insurance to Energy",
           M, Inches(0.38), CW, Inches(0.55), size=24, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "{{TESTIMONIALS_SUBTITLE}}", M, Inches(1.18), CW, Inches(0.35), size=13, color=b.LIGHT_TEAL)
    q_h = Inches(1.02)
    q_gap = Inches(0.12)
    for i, (client, industry, quote) in enumerate(TESTIMONIALS):
        qy = Inches(1.68) + i * (q_h + q_gap)
        d.rect(s, M, qy, CW, q_h, b.NAVY_2, radius=0.03)
        d.rect(s, M, qy, Inches(0.06), q_h, b.TEAL)
        d.text(s, client, M + Inches(0.18), qy + Inches(0.08),
               Inches(1.8), Inches(0.3), size=12, color=b.TEAL, bold=True)
        d.text(s, industry, M + Inches(0.18), qy + Inches(0.42),
               Inches(1.8), Inches(0.25), size=9.5, color=b.MUTED)
        d.text(s, quote, M + Inches(2.1), qy + Inches(0.1),
               CW - Inches(2.2), q_h - Inches(0.18),
               size=11.5, color=b.LIGHT_TEAL, italic=True, shrink=True)
    d.footer(s, pg, TOTAL, dark=True)

    # SLIDES 10–11 — Use case realization slides
    pg = next_pg()
    use_case_slide(d.slide(), pg, USE_CASE_1)

    pg = next_pg()
    use_case_slide(d.slide(), pg, USE_CASE_2)

    # SLIDE 12 — Person BD proof points
    pg = next_pg()
    s = d.slide(fill=b.WHITE)
    d.header(s, f"{PERSON_NAME.split()[0]}'s Proof Points — Why Leaders Take the First Meeting",
             "BD Experience & Credibility Evidence")
    item_h = Inches(0.82)
    for i, (title, body) in enumerate(PROOF_ITEMS):
        row = i % 3
        col = i // 3
        ix = M + col * (CW / 2 + Inches(0.1))
        iy = Inches(1.72) + row * (item_h + Inches(0.1))
        iw = CW / 2 - Inches(0.08)
        d.rect(s, ix, iy, iw, item_h, b.SOFT, radius=0.03)
        d.rect(s, ix, iy, Inches(0.06), item_h, b.TEAL)
        d.text(s, title, ix + Inches(0.14), iy + Inches(0.07),
               iw - Inches(0.2), Inches(0.26), size=11, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, ix + Inches(0.14), iy + Inches(0.34),
               iw - Inches(0.2), item_h - Inches(0.4), size=9.5, color=b.INK, shrink=True)
    d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — WHAT THEY LOVE
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "{{LOVES_SLIDE_TITLE}}", "What They Love")
paras = [{"text": t, "bullet": True, "size": 14, "color": b.INK, "space_before": 10}
         for t in LOVES_BULLETS]
d.text(s, paras, M, Inches(1.72), CW - Inches(0.3), Inches(5.0), shrink=True)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — WHAT THEY'RE GOOD AT
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "{{GOODAT_SLIDE_TITLE}}", "What They're Good At")
paras = [{"text": t, "bullet": True, "size": 14, "color": b.INK, "space_before": 10}
         for t in GOODAT_BULLETS]
d.text(s, paras, M, Inches(1.72), CW - Inches(0.3), Inches(5.0), shrink=True)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — NICHE STATEMENT
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "A Position Nobody Else Occupies in the Market", "Niche Statement")
layer_h = Inches(1.55)
for i, (fill, accent, label, body) in enumerate(NICHE_LAYERS):
    ly = Inches(1.72) + i * (layer_h + Inches(0.1))
    d.rect(s, M, ly, CW, layer_h, fill, radius=0.03)
    d.rect(s, M, ly, CW, Inches(0.05), accent)
    d.text(s, label, M + Inches(0.18), ly + Inches(0.1),
           Inches(3), Inches(0.32), size=12, color=accent, bold=True)
    d.text(s, body, M + Inches(0.18), ly + Inches(0.46),
           CW - Inches(0.3), layer_h - Inches(0.5), size=12.5, color=b.WHITE, shrink=True)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — VALIDATION SCORECARD
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, f"{SCORE}/100 — {SCORE_LABEL} Validation Across All Six Dimensions",
         "Validation Scorecard")
sc_col_w = [Inches(2.5), Inches(1.3), Inches(8.1)]
table_rows(s, SCORECARD_ROWS, M, Inches(1.72), sc_col_w,
           row_h=Inches(0.54), header_fill=b.NAVY, alt_fill=True, text_size=11)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — GAP TO OWN
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "The Position That Is Empty in the Market", "Market Intelligence")
half = (CW - Inches(0.2)) / 2
d.rect(s, M, Inches(1.72), half, Inches(4.8), b.SOFT, radius=0.03)
d.rect(s, M, Inches(1.72), half, Inches(0.42), b.CORAL)
d.text(s, "AVOID — Where Not to Compete", M + Inches(0.12), Inches(1.8),
       half - Inches(0.2), Inches(0.3), size=13, color=b.WHITE, bold=True)
ap = [{"text": t, "bullet": True, "size": 12.5, "color": b.INK, "space_before": 10}
      for t in AVOID_BULLETS]
d.text(s, ap, M + Inches(0.15), Inches(2.25), half - Inches(0.25), Inches(3.8), shrink=True)
rx = M + half + Inches(0.2)
d.rect(s, rx, Inches(1.72), half, Inches(4.8), b.NAVY, radius=0.03)
d.rect(s, rx, Inches(1.72), half, Inches(0.42), b.TEAL)
d.text(s, "GAP TO OWN — The Empty Position", rx + Inches(0.12), Inches(1.8),
       half - Inches(0.2), Inches(0.3), size=13, color=b.NAVY, bold=True)
d.text(s, GAP_BODY, rx + Inches(0.15), Inches(2.25),
       half - Inches(0.25), Inches(4.0), size=12.5, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — TIMING SIGNALS
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "{{TIMING_SLIDE_TITLE}}", M, Inches(0.38), CW, Inches(0.55),
       size=26, color=b.WHITE, bold=True, shrink=True)
d.text(s, "{{TIMING_SLIDE_SUBTITLE}}", M, Inches(1.16), CW, Inches(0.35), size=13, color=b.LIGHT_TEAL)
card_w2 = (CW - Inches(0.45)) / 2
card_h2 = Inches(2.55)
for i, (title, body) in enumerate(TIMING_CARDS):
    col = i % 2
    row = i // 2
    cx = M + col * (card_w2 + Inches(0.15))
    cy = Inches(1.65) + row * (card_h2 + Inches(0.15))
    d.rect(s, cx, cy, card_w2, card_h2, b.NAVY_2, radius=0.03)
    d.rect(s, cx, cy, card_w2, Inches(0.06), b.TEAL)
    d.text(s, title, cx + Inches(0.15), cy + Inches(0.1),
           card_w2 - Inches(0.2), Inches(0.32), size=12, color=b.TEAL, bold=True)
    d.text(s, body, cx + Inches(0.15), cy + Inches(0.48),
           card_w2 - Inches(0.2), card_h2 - Inches(0.55), size=11, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, pg, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — COMPETITOR LANDSCAPE
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "Every Competitor Falls Short on the Dimension That Matters Most",
         "Competitor Landscape")
comp_col_w = [Inches(2.5), Inches(2.3), Inches(7.1)]
# Draw all rows except winner row
table_rows(s, COMPETITOR_ROWS[:-1], M, Inches(1.72), comp_col_w,
           row_h=Inches(0.62), header_fill=b.NAVY, alt_fill=True, text_size=11)
# Winner row in teal
last_y = Inches(1.72) + (len(COMPETITOR_ROWS) - 1) * Inches(0.62)
d.rect(s, M, last_y, CW, Inches(0.62), b.TEAL, line=b.TEAL)
x = M
for cell, cw in zip(COMPETITOR_ROWS[-1], comp_col_w):
    d.text(s, cell, x + Inches(0.08), last_y + Inches(0.06),
           cw - Inches(0.12), Inches(0.5),
           size=11, color=b.NAVY, bold=True, shrink=True, anchor=MSO_ANCHOR.MIDDLE)
    x += cw
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — ENGAGEMENT MODEL
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "Three Entry Points · One Long-Term Partnership", "Engagement Model")
tier_h = Inches(1.6)
tier_fills = [b.NAVY_2, b.NAVY, b.ACCENT]
for i, (badge, name, price, includes, ideal) in enumerate(TIERS):
    ty = Inches(1.72) + i * (tier_h + Inches(0.14))
    fill = tier_fills[i]
    accent = b.TEAL if i < 2 else b.GOLD
    d.rect(s, M, ty, CW, tier_h, fill, radius=0.03)
    d.rect(s, M, ty, Inches(0.08), tier_h, accent)
    d.text(s, badge, M + Inches(0.18), ty + Inches(0.1),
           Inches(1.4), Inches(0.28), size=10, color=accent, bold=True)
    d.text(s, name, M + Inches(1.6), ty + Inches(0.06),
           Inches(3.5), Inches(0.4), size=16, color=b.WHITE, bold=True, shrink=True)
    d.text(s, price, M + Inches(5.2), ty + Inches(0.1),
           Inches(2.5), Inches(0.35), size=14, color=b.GOLD, bold=True)
    d.text(s, "Includes: " + includes, M + Inches(0.18), ty + Inches(0.52),
           Inches(7.5), Inches(0.5), size=11, color=b.LIGHT_TEAL, shrink=True)
    d.text(s, "Ideal for: " + ideal, M + Inches(0.18), ty + Inches(1.08),
           CW - Inches(0.3), Inches(0.42), size=11, color=b.MUTED, shrink=True)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — REVENUE IMPACT
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "Each Win Compounds Into a Multi-Year Revenue Stream", "Revenue Impact")
rev_col_w = [Inches(2.8), Inches(2.5), Inches(6.6)]
table_rows(s, REVENUE_ROWS, M, Inches(1.72), rev_col_w,
           row_h=Inches(0.9), header_fill=b.NAVY, alt_fill=True, text_size=12)
d.rect(s, M, Inches(5.4), CW, Inches(0.7), b.NAVY, radius=0.03)
sw = CW / len(REVENUE_PROOF)
for i, text in enumerate(REVENUE_PROOF):
    d.text(s, text, M + i * sw + Inches(0.15), Inches(5.5),
           sw - Inches(0.2), Inches(0.5), size=10.5, color=b.TEAL, bold=True,
           align=PP_ALIGN.CENTER, shrink=True)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — INCOME MATH & MILESTONES
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "{{MILESTONES_SLIDE_TITLE}}", "Income Math & Milestones")
ms_col_w = [Inches(1.3), Inches(1.7), Inches(2.4), Inches(6.5)]
table_rows(s, MILESTONE_ROWS, M, Inches(1.72), ms_col_w,
           row_h=Inches(0.84), header_fill=b.NAVY, alt_fill=True, text_size=12)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — 7-DAY ACTIVATION PLAN
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "First Meeting Booked in 7 Days — From Warm Network, Not Cold Outreach",
         "7-Day Activation Plan")
half = (CW - Inches(0.2)) / 2
d.rect(s, M, Inches(1.72), half, Inches(4.8), b.NAVY, radius=0.03)
d.rect(s, M, Inches(1.72), half, Inches(0.42), b.TEAL)
d.text(s, "DAYS 1–3 · Build the Proof Point", M + Inches(0.12), Inches(1.8),
       half - Inches(0.2), Inches(0.3), size=13, color=b.NAVY, bold=True)
d.text(s, DAY13_BODY, M + Inches(0.15), Inches(2.25),
       half - Inches(0.25), Inches(4.0), size=12, color=b.LIGHT_TEAL, shrink=True)
rx = M + half + Inches(0.2)
d.rect(s, rx, Inches(1.72), half, Inches(4.8), b.SOFT, radius=0.03)
d.rect(s, rx, Inches(1.72), half, Inches(0.42), b.ACCENT)
d.text(s, "DAYS 4–7 · Activate the Network", rx + Inches(0.12), Inches(1.8),
       half - Inches(0.2), Inches(0.3), size=13, color=b.WHITE, bold=True)
d.text(s, DAY47_BODY, rx + Inches(0.15), Inches(2.25),
       half - Inches(0.25), Inches(4.0), size=12, color=b.INK, shrink=True)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — 12–18 MONTH TRAJECTORY
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.WHITE)
d.header(s, "The Compounding Arc — {{TRAJECTORY_SLIDE_SUBTITLE}}", "12–18 Month Trajectory")
phase_w = (CW - Inches(0.45)) / 4
phase_h = Inches(4.0)
fills = [b.NAVY_2, b.NAVY, b.ACCENT, b.TEAL]
text_cols = [b.LIGHT_TEAL, b.LIGHT_TEAL, b.WHITE, b.NAVY]
for i, (label, revenue, desc) in enumerate(PHASES):
    px = M + i * (phase_w + Inches(0.15))
    py = Inches(1.72)
    d.rect(s, px, py, phase_w, phase_h, fills[i], radius=0.03)
    d.text(s, label, px + Inches(0.12), py + Inches(0.15),
           phase_w - Inches(0.2), Inches(0.7),
           size=11, color=text_cols[i], bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, revenue, px + Inches(0.08), py + Inches(0.95),
           phase_w - Inches(0.12), Inches(0.9),
           size=20, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, px + Inches(0.25), py + Inches(1.88), phase_w - Inches(0.5), Inches(0.04),
           b.TEAL if fills[i] != b.TEAL else b.NAVY)
    d.text(s, desc, px + Inches(0.12), py + Inches(2.0),
           phase_w - Inches(0.2), phase_h - Inches(2.1),
           size=10.5, color=text_cols[i], shrink=True)
    if i < 3:
        d.text(s, "→", px + phase_w - Inches(0.08), py + phase_h / 2 - Inches(0.25),
               Inches(0.25), Inches(0.5), size=18, color=b.TEAL, bold=True)
d.footer(s, pg, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — ONE-LINER
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "The Line That Opens Every Door", M, Inches(0.38), CW, Inches(0.5),
       size=22, color=b.TEAL, bold=True)
d.rect(s, M, Inches(1.05), Inches(0.1), Inches(4.2), b.TEAL)
d.text(s, f'"{ONE_LINER_QUOTE}"', M + Inches(0.3), Inches(1.1),
       CW - Inches(0.35), Inches(4.2), size=22, color=b.WHITE, italic=True, shrink=True)
d.text(s, f"— {PERSON_NAME}, {PERSON_ROLE}", M + Inches(0.3), Inches(5.5),
       CW - Inches(0.35), Inches(0.45), size=14, color=b.TEAL, bold=True)
d.footer(s, pg, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE — CLOSING
# ═══════════════════════════════════════════════════════════════════════════════
pg = next_pg()
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "{{CLOSING_SLIDE_TITLE}}", M, Inches(0.38), CW, Inches(0.65),
       size=28, color=b.WHITE, bold=True, shrink=True)
col_w3 = (CW - Inches(0.3)) / 3
for i, (fill, accent, title, body) in enumerate(CLOSING_COLS):
    cx = M + i * (col_w3 + Inches(0.15))
    cy = Inches(1.38)
    ch = Inches(5.1)
    d.rect(s, cx, cy, col_w3, ch, fill, radius=0.04)
    d.rect(s, cx, cy, col_w3, Inches(0.06), accent)
    d.text(s, title, cx + Inches(0.15), cy + Inches(0.15),
           col_w3 - Inches(0.25), Inches(0.7),
           size=14, color=accent, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, cx + Inches(0.5), cy + Inches(0.88), col_w3 - Inches(1.0), Inches(0.04), accent)
    d.text(s, body, cx + Inches(0.15), cy + Inches(1.05),
           col_w3 - Inches(0.25), ch - Inches(1.15),
           size=11, color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
d.rect(s, M, Inches(6.65), CW, Inches(0.45), b.TEAL)
d.text(s, CLOSING_CTA, M + Inches(0.2), Inches(6.7), CW - Inches(0.3), Inches(0.35),
       size=15, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.footer(s, pg, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE + VALIDATE
# ═══════════════════════════════════════════════════════════════════════════════
d.save(OUT)
print(f"\nSlides: {d.n}")
print(f"Output: {OUT}")
