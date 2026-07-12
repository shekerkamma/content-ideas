#!/usr/bin/env python3
"""
Builder: Claude Code Agents 2026 — Professional Branded PPTX
Source: runs/2026-06-19-claude-code-agents-deck/claude-code-agents-research.md
Deck:   runs/2026-06-19-claude-code-agents-deck/claude-code-agents-deck.pptx
"""
import sys
sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")

from pptxkit import Brand, Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor, hx

# ── Brand override (tokens.json values) ──
brand = Brand(
    NAVY     = hx("0F172A"),   # Slate 900
    NAVY_2   = hx("1E293B"),   # Slate 800
    TEAL     = hx("22D3EE"),   # Cyan 400 (accent)
    ACCENT   = hx("0891B2"),   # Cyan 700 (darker)
    DARK_TEAL= hx("0E7490"),
    LIGHT_TEAL=hx("ECFEFF"),   # Cyan 50
    GOLD     = hx("F59E0B"),   # Amber 500
    AMBER    = hx("F59E0B"),
    CORAL    = hx("EF4444"),   # Red 500
    WHITE    = hx("FFFFFF"),
    SOFT     = hx("F8FAFC"),   # Slate 50
    INK      = hx("0F172A"),   # Slate 900
    MUTED    = hx("94A3B8"),   # Slate 400
    GRID     = hx("E2E8F0"),   # Slate 200
    FONT     = "Calibri",
    FONT_H   = "Calibri",
    HX_TEAL  = "#22D3EE",
    HX_TEALD = "#0891B2",
    HX_NAVY  = "#0F172A",
    HX_INK   = "#0F172A",
    HX_MUTED = "#94A3B8",
    HX_GRID  = "#E2E8F0",
    HX_GOLD  = "#F59E0B",
)

# Convenience
GREEN   = hx("10B981")   # Emerald 500
AMBER   = hx("F59E0B")
VIOLET  = hx("8B5CF6")   # Violet 500
ORANGE  = hx("F97316")   # Orange 500
SLATE200= hx("E2E8F0")
SLATE300= hx("CBD5E1")
SLATE700= hx("334155")
MONO    = "Consolas"

OUT = "/home/shekerk/content-ideas/runs/2026-06-19-claude-code-agents-deck/claude-code-agents-deck.pptx"
TOTAL = 18
FOOTER = "Claude Code Agents 2026  ·  Nate Herk × Cole  ·  Confidential"

d = Deck(brand=brand, footer=FOOTER)
b = d.b
W, H, M, CW = d.W, d.H, d.M, d.CW

# ── helpers ─────────────────────────────────────────────────────────────────

def col_rect(s, col_idx, num_cols, *, top=Inches(1.5), height=Inches(5.3),
             gap=Inches(0.18), fill=None, line=None, radius=0.02):
    """Evenly-spaced column card."""
    total_gap = gap * (num_cols - 1)
    cw = (CW - total_gap) / num_cols
    left = M + col_idx * (cw + gap)
    if fill is not None:
        d.rect(s, left, top, cw, height, fill, line=line, radius=radius)
    return left, top, cw, height

def stat_block(s, left, top, width, number, unit, label, *, n_color=None):
    n_color = n_color or b.TEAL
    d.rect(s, left, top, width, Inches(1.46), b.SOFT, line=SLATE200, radius=0.02)
    d.text(s, number, left + Inches(0.15), top + Inches(0.10), width - Inches(0.3), Inches(0.78),
           size=40, color=n_color, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, unit, left + Inches(0.1), top + Inches(0.72), width - Inches(0.2), Inches(0.28),
           size=12, color=b.MUTED, align=PP_ALIGN.CENTER)
    d.text(s, label, left + Inches(0.1), top + Inches(1.0), width - Inches(0.2), Inches(0.38),
           size=10.5, color=b.INK, align=PP_ALIGN.CENTER, bold=True)

def section_tag(s, text, *, color=None):
    color = color or b.TEAL
    d.rect(s, M, Inches(0.14), Inches(2.4), Inches(0.22), color)
    d.text(s, text, M + Inches(0.08), Inches(0.14), Inches(2.3), Inches(0.22),
           size=9.5, color=b.WHITE, bold=True, font=MONO)

def dot_row(s, label, detail, top, dot_color, *, left=None, width=None):
    left = left or M
    width = width or CW
    d.rect(s, left, top + Inches(0.08), Inches(0.14), Inches(0.14), dot_color, radius=0.5)
    d.text(s, label, left + Inches(0.22), top, Inches(1.3), Inches(0.3),
           size=12.5, color=b.INK, bold=True)
    d.text(s, detail, left + Inches(1.6), top, width - Inches(1.6), Inches(0.3),
           size=11, color=b.MUTED)

def flow_node(s, left, top, w, h, num_str, title, detail=None, *, fill=None, num_color=None):
    fill = fill or b.SOFT
    num_color = num_color or b.TEAL
    d.rect(s, left, top, w, h, fill, line=SLATE200, radius=0.02)
    d.text(s, num_str, left + Inches(0.16), top + Inches(0.12), Inches(0.5), Inches(0.35),
           size=22, color=num_color, bold=True, font=MONO)
    d.text(s, title, left + Inches(0.7), top + Inches(0.12), w - Inches(0.9), Inches(0.35),
           size=14, color=b.INK, bold=True)
    if detail:
        d.text(s, detail, left + Inches(0.2), top + Inches(0.52), w - Inches(0.4), h - Inches(0.68),
               size=10.5, color=b.MUTED, ls=1.3, wrap=True)

def hline(s, top, *, color=None, left=None, width=None):
    color = color or SLATE200
    left = left or M
    width = width or CW
    d.rect(s, left, top, width, Pt(1.5), color)

def bullet_lines(s, items, *, left, top, width, dot_color=None, size=12.5, gap=0.34):
    dot_color = dot_color or b.TEAL
    for i, (bold_part, rest) in enumerate(items):
        y = top + Inches(gap * i)
        d.rect(s, left, y + Inches(0.10), Inches(0.12), Inches(0.12), dot_color, radius=0.5)
        d.text(s, [
            {"text": bold_part + "  ", "bold": True, "color": b.INK, "size": size},
            {"text": rest, "bold": False, "color": SLATE700, "size": size - 0.5},
        ], left + Inches(0.22), y, width - Inches(0.22), Inches(0.30), size=size)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE (dark)
# ════════════════════════════════════════════════════════════════════════════
s1 = d.slide(fill=b.NAVY)

# Teal top bar
d.rect(s1, 0, 0, W, Inches(0.14), b.TEAL)

# Eyebrow
d.text(s1, "AI Automation · Nate Herk × Cole  ·  2026", M, Inches(0.3), CW, Inches(0.35),
       size=12, color=hx("94A3B8"), font=MONO)

# Main title
d.text(s1, "From Using Claude Code\nto Directing It",
       M, Inches(1.1), CW, Inches(1.9),
       size=46, color=b.WHITE, bold=True, font=b.FONT_H, ls=1.12, shrink=True)

# Cyan accent stripe
d.rect(s1, M, Inches(3.1), Inches(2.4), Inches(0.07), b.TEAL)

# Subtitle
d.text(s1, "The 4 skills that turn Claude Code into a reliable, repeatable engine\nfor any business — not just software.",
       M, Inches(3.3), Inches(9.0), Inches(0.85),
       size=17.5, color=hx("CBD5E1"), ls=1.5)

# Key stat strip
d.rect(s1, M, Inches(4.55), Inches(3.6), Inches(0.9), hx("1E293B"))
d.text(s1, '"You\'re getting ~20% out of Claude Code,\nand it\'s not about coding skill."',
       M + Inches(0.2), Inches(4.65), Inches(3.3), Inches(0.7),
       size=12, color=hx("CBD5E1"), italic=True, ls=1.4)

d.rect(s1, M + Inches(4.0), Inches(4.55), Inches(3.6), Inches(0.9), hx("1E293B"))
d.text(s1, "92% first-pass accuracy\nvs 65% without verification",
       M + Inches(4.2), Inches(4.65), Inches(3.2), Inches(0.7),
       size=12, color=hx("CBD5E1"), italic=False, ls=1.4)

# Bottom source line
d.text(s1, "Source: youtube.com/watch?v=RzLV8sfFdMM", M, Inches(7.1), CW, Inches(0.28),
       size=9, color=hx("475569"))
d.footer(s1, 1, TOTAL, dark=True)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — EXECUTIVE SUMMARY (dark, standalone briefing page)
# ════════════════════════════════════════════════════════════════════════════
s_exec = d.slide(fill=b.NAVY)
d.rect(s_exec, 0, 0, W, Inches(0.08), b.TEAL)

# Eyebrow tag
d.rect(s_exec, M, Inches(0.14), Inches(2.0), Inches(0.22), b.TEAL)
d.text(s_exec, "EXECUTIVE SUMMARY", M + Inches(0.08), Inches(0.14), Inches(1.9), Inches(0.22),
       size=9.5, color=b.WHITE, bold=True, font=MONO)

# Headline
d.text(s_exec, "The 4 Skills That Unlock\nClaude Code's Full Potential",
       M, Inches(0.50), Inches(7.8), Inches(1.3),
       size=34, color=b.WHITE, bold=True, font=b.FONT_H, ls=1.15, shrink=True)
d.rect(s_exec, M, Inches(1.88), Inches(1.8), Inches(0.06), b.TEAL)

# Left: Problem + Fix narrative
lw = Inches(4.5)
d.rect(s_exec, M, Inches(2.06), lw, Inches(4.72), hx("0E1E34"), line=hx("1E3A5A"), radius=0.02)

d.text(s_exec, "THE PROBLEM", M + Inches(0.22), Inches(2.20), lw - Inches(0.44), Inches(0.26),
       size=9.5, color=hx("EF4444"), bold=True, font=MONO)
d.text(s_exec,
       "Most teams treat Claude Code like a slot machine — prompt and pray. "
       "The result: random outputs, no system, no memory. "
       "You're unlocking ~20% of what's possible.",
       M + Inches(0.22), Inches(2.52), lw - Inches(0.44), Inches(1.06),
       size=12.5, color=hx("CBD5E1"), ls=1.55, wrap=True)

d.rect(s_exec, M + Inches(0.22), Inches(3.66), lw - Inches(0.44), Pt(1.5), hx("1E3A5A"))

d.text(s_exec, "THE FIX", M + Inches(0.22), Inches(3.82), lw - Inches(0.44), Inches(0.26),
       size=9.5, color=b.TEAL, bold=True, font=MONO)
d.text(s_exec,
       "Four skills transform Claude Code from a tool you prompt "
       "into a system you direct. Same loop, repeatable results, "
       "compounding improvement every week.",
       M + Inches(0.22), Inches(4.14), lw - Inches(0.44), Inches(1.06),
       size=12.5, color=hx("CBD5E1"), ls=1.55, wrap=True)

d.rect(s_exec, M + Inches(0.22), Inches(5.28), lw - Inches(0.44), Pt(1.5), hx("1E3A5A"))

# Outcome stat
d.rect(s_exec, M + Inches(0.22), Inches(5.44), Inches(1.3), Inches(0.66),
       hx("0E2030"), line=hx("EF4444"), radius=0.02)
d.text(s_exec, "65%", M + Inches(0.22), Inches(5.50), Inches(1.3), Inches(0.36),
       size=26, color=hx("EF4444"), bold=True, align=PP_ALIGN.CENTER)
d.text(s_exec, "without verify", M + Inches(0.22), Inches(5.84), Inches(1.3), Inches(0.22),
       size=9, color=hx("94A3B8"), align=PP_ALIGN.CENTER, font=MONO)

d.text(s_exec, "→", M + Inches(1.62), Inches(5.58), Inches(0.5), Inches(0.36),
       size=22, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)

d.rect(s_exec, M + Inches(2.22), Inches(5.44), Inches(1.3), Inches(0.66),
       hx("0E2030"), line=GREEN, radius=0.02)
d.text(s_exec, "92%", M + Inches(2.22), Inches(5.50), Inches(1.3), Inches(0.36),
       size=26, color=GREEN, bold=True, align=PP_ALIGN.CENTER)
d.text(s_exec, "with 4 skills", M + Inches(2.22), Inches(5.84), Inches(1.3), Inches(0.22),
       size=9, color=hx("94A3B8"), align=PP_ALIGN.CENTER, font=MONO)

d.text(s_exec, "first-pass accuracy", M + Inches(3.64), Inches(5.58), Inches(0.8), Inches(0.50),
       size=10, color=hx("94A3B8"), italic=True, ls=1.4)

# Right: 4 skill cards stacked
rx = M + lw + Inches(0.32)
rw = CW - lw - Inches(0.32)

exec_skills = [
    (AMBER,        "01",  "PLAN FIRST",
     "Write PLAN.md before every task.", "Goal · Tasks · Validation in one doc"),
    (GREEN,        "02",  "MANAGE CONTEXT",
     "Feed the right info — not all of it.", "6 techniques to stay out of the dumb zone"),
    (b.TEAL,       "03",  "VERIFY THE WORK",
     "Auto-validate before human review.", "65% → 92% accuracy with one verify step"),
    (hx("3B82F6"), "04",  "BUILD THE SYSTEM",
     "Turn every bug into a permanent rule.", "Floor keeps rising; system compounds weekly"),
]

card_h = Inches(1.08)
gap = Inches(0.08)
for i, (col, num, name, action, outcome) in enumerate(exec_skills):
    cy = Inches(2.06) + i * (card_h + gap)
    d.rect(s_exec, rx, cy, rw, card_h, hx("0E1E34"), line=hx("1E3A5A"), radius=0.02)
    d.rect(s_exec, rx, cy, Inches(0.06), card_h, col, radius=0.01)
    # Num badge
    d.rect(s_exec, rx + Inches(0.16), cy + Inches(0.26), Inches(0.40), Inches(0.40), col, radius=0.5)
    d.text(s_exec, num, rx + Inches(0.16), cy + Inches(0.26), Inches(0.40), Inches(0.40),
           size=12, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, font=MONO)
    # Skill name
    d.text(s_exec, name, rx + Inches(0.68), cy + Inches(0.10), rw - Inches(0.84), Inches(0.34),
           size=14, color=col, bold=True, font=b.FONT_H)
    # Action
    d.text(s_exec, action, rx + Inches(0.68), cy + Inches(0.46), rw - Inches(0.84), Inches(0.26),
           size=11, color=hx("CBD5E1"))
    # Outcome divider + text
    d.rect(s_exec, rx + Inches(0.68), cy + Inches(0.74), rw - Inches(0.84), Pt(1.0), hx("1E3A5A"))
    d.text(s_exec, outcome, rx + Inches(0.68), cy + Inches(0.80), rw - Inches(0.84), Inches(0.22),
           size=9.5, color=hx("94A3B8"), font=MONO)

d.footer(s_exec, 2, TOTAL, dark=True)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — THE 4 SKILLS: FOCAL DIAGRAM (light, 2×2 quadrant cycle)
# ════════════════════════════════════════════════════════════════════════════
s_loop = d.slide(fill=b.SOFT)
d.rect(s_loop, 0, 0, W, Inches(0.08), b.TEAL)
d.rect(s_loop, M, Inches(0.14), Inches(2.8), Inches(0.22), b.NAVY)
d.text(s_loop, "THE 4-SKILL FRAMEWORK", M + Inches(0.1), Inches(0.14), Inches(2.7), Inches(0.22),
       size=9.5, color=b.WHITE, bold=True, font=MONO)

d.text(s_loop, "The Loop That Replaces Random Outcomes",
       M, Inches(0.50), Inches(8.0), Inches(0.54),
       size=26, color=b.INK, bold=True, font=b.FONT_H, shrink=True)
d.text(s_loop, "Each skill is a stage in a repeatable cycle. Run all four and the system compounds.",
       M, Inches(1.08), CW, Inches(0.30),
       size=13, color=b.MUTED)

# ── 2×2 grid of focal cards ──
# Card dims
qw = Inches(5.7)
qh = Inches(2.66)
gap_x = Inches(0.26)
gap_y = Inches(0.18)
top_row_y = Inches(1.52)
bot_row_y = top_row_y + qh + gap_y
left_col_x = M
right_col_x = M + qw + gap_x

focal_cards = [
    # (x, y, col, num, name, tagline, what_it_is, key_action, key_metric)
    (left_col_x,  top_row_y, AMBER,        "01", "PLAN FIRST",
     "The north star before every task",
     "Write PLAN.md with goal, codebase analysis, integration points, rules, task list, and validation strategy.",
     "Key action:  /prime → research → /plan → edit → fresh context → execute",
     "Cheapest place to be wrong"),

    (right_col_x, top_row_y, GREEN,        "02", "MANAGE CONTEXT",
     "Right info, not all info",
     "Effective quality degrades after 100–250K tokens depending on model. Load only what the agent needs, when it needs it.",
     "Key action:  separate sessions · specialized /prime · subagents · on-demand docs",
     "Dumb zone: 100–250K tokens"),

    (left_col_x,  bot_row_y, b.TEAL,       "03", "VERIFY THE WORK",
     "Gate every output before shipping",
     "Never trust the first pass. Auto-validate with checks + lint + tests, then human review, then real-world confirm.",
     "Key action:  /validate → [fail = fix + re-run] → review → ships",
     "65% → 92% first-pass accuracy"),

    (right_col_x, bot_row_y, hx("3B82F6"), "04", "BUILD THE SYSTEM",
     "Every bug is a permanent upgrade",
     "When anything goes wrong, don't just fix it. Write a rule, update a reference doc, create a /command. The floor rises.",
     "Key action:  bug → rule → reference doc → /command → skill (staircase)",
     "Floor rises weekly; compounds over months"),
]

for (qx, qy, col, num, name, tagline, body, action, metric) in focal_cards:
    # Card background
    d.rect(s_loop, qx, qy, qw, qh, b.WHITE, line=SLATE200, radius=0.02)
    # Color top bar
    d.rect(s_loop, qx, qy, qw, Inches(0.07), col)

    # Number circle
    d.rect(s_loop, qx + Inches(0.18), qy + Inches(0.14), Inches(0.44), Inches(0.44), col, radius=0.5)
    d.text(s_loop, num, qx + Inches(0.18), qy + Inches(0.14), Inches(0.44), Inches(0.44),
           size=14, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, font=MONO)

    # Skill name (large)
    d.text(s_loop, name, qx + Inches(0.74), qy + Inches(0.14), qw - Inches(0.94), Inches(0.44),
           size=18, color=b.INK, bold=True, font=b.FONT_H)

    # Tagline
    d.text(s_loop, tagline, qx + Inches(0.18), qy + Inches(0.64), qw - Inches(0.36), Inches(0.24),
           size=11.5, color=col, bold=True, italic=True)

    # Divider
    d.rect(s_loop, qx + Inches(0.18), qy + Inches(0.92), qw - Inches(0.36), Pt(1.2), SLATE200)

    # Body
    d.text(s_loop, body, qx + Inches(0.18), qy + Inches(1.04), qw - Inches(0.36), Inches(0.78),
           size=11.5, color=SLATE700, ls=1.45, wrap=True, shrink=True)

    # Action strip
    d.rect(s_loop, qx + Inches(0.18), qy + Inches(1.88), qw - Inches(0.36), Inches(0.50),
           b.SOFT, line=SLATE200, radius=0.01)
    d.text(s_loop, action, qx + Inches(0.26), qy + Inches(1.96), qw - Inches(0.52), Inches(0.34),
           size=10, color=b.MUTED, font=MONO, wrap=True, shrink=True)

    # Metric badge
    d.rect(s_loop, qx + Inches(0.18), qy + Inches(2.42), qw - Inches(0.36), Inches(0.18), col)
    d.text(s_loop, metric, qx + Inches(0.22), qy + Inches(2.44), qw - Inches(0.44), Inches(0.14),
           size=9.5, color=b.WHITE, bold=True, font=MONO)

# Center connecting arrows (cycle indicators between cards)
cx = M + qw + gap_x / 2  # horizontal center gap
cy_mid = top_row_y + qh + gap_y / 2  # vertical center gap

# Arrow: right side, top→bottom
d.text(s_loop, "↓", cx - Inches(0.14), cy_mid - Inches(0.22), Inches(0.28), Inches(0.44),
       size=18, color=SLATE300, bold=True, align=PP_ALIGN.CENTER)

# Loop annotation
d.text(s_loop, "↺  same result · on purpose",
       cx - Inches(0.80), cy_mid + Inches(0.26), Inches(1.6), Inches(0.28),
       size=9, color=b.TEAL, bold=True, font=MONO, align=PP_ALIGN.CENTER)

d.footer(s_loop, 3, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — FRAMEWORK OVERVIEW (was SLIDE 2)
# ════════════════════════════════════════════════════════════════════════════
s2 = d.slide(fill=b.SOFT)
d.rect(s2, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s2, "THE FRAMEWORK", color=b.NAVY)
d.header(s2, "The 4-Skill Framework", "Same 4 skills whether Claude Code runs your software, content engine, or business ops", band=False)

cards = [
    ("01", "THE SHIFT",        ORANGE, "Stop pulling the lever. Direct a repeatable loop instead of random outcomes."),
    ("02", "PLAN FIRST",       AMBER,  "Make it plan first. PLAN.md is the north star. Cheapest place to be wrong."),
    ("03", "MANAGE CONTEXT",   GREEN,  "Right info, not all info. Attention is scarce. Control the window carefully."),
    ("04", "VERIFY THE WORK",  b.TEAL, "Don't trust the first pass. Gate every output — code, content, or data."),
]

card_w = (CW - Inches(0.5)) / 4
for i, (num, title, color, body) in enumerate(cards):
    lx, ty, cw, ch = col_rect(s2, i, 4, top=Inches(1.6), height=Inches(4.85), fill=b.WHITE, line=SLATE200)
    # color top bar
    d.rect(s2, lx, ty, cw, Inches(0.08), color)
    # num
    d.text(s2, num, lx + Inches(0.16), ty + Inches(0.18), cw - Inches(0.32), Inches(0.34),
           size=10, color=color, bold=True, font=MONO)
    # title
    d.text(s2, title, lx + Inches(0.16), ty + Inches(0.52), cw - Inches(0.32), Inches(0.60),
           size=14.5, color=b.INK, bold=True, font=b.FONT_H, shrink=True)
    # body
    d.text(s2, body, lx + Inches(0.16), ty + Inches(1.22), cw - Inches(0.32), Inches(2.2),
           size=11.5, color=SLATE700, ls=1.45, wrap=True, shrink=True)

# +5th: Build The System
d.rect(s2, M, Inches(6.58), CW, Inches(0.70), b.NAVY, radius=0.02)
d.text(s2, "+  BUILD THE SYSTEM  —  Evolve the system, don't just fix the bug. Every bug = a permanent upgrade.",
       M + Inches(0.3), Inches(6.64), CW - Inches(0.6), Inches(0.58),
       size=12.5, color=b.WHITE, bold=True)

d.footer(s2, 4, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — THE SHIFT
# ════════════════════════════════════════════════════════════════════════════
s3 = d.slide(fill=b.SOFT)
d.rect(s3, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s3, "01 · THE SHIFT")
d.header(s3, "Stop Pulling the Lever", "Direct a repeatable loop — same result, on purpose", band=False)

# Left card: Old way
lx = M
lw = Inches(5.6)
d.rect(s3, lx, Inches(1.58), lw, Inches(5.0), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s3, lx, Inches(1.58), lw, Inches(0.08), hx("EF4444"))
d.text(s3, "🎰  Vibe Coding / Slot Machine", lx + Inches(0.2), Inches(1.72), lw - Inches(0.4), Inches(0.36),
       size=14, color=hx("EF4444"), bold=True)

old_items = [
    ("Pull the prompt lever", "and hope for a good result"),
    ("Re-roll", "when it fails; random outcomes"),
    ("No system,", "no memory — fragile"),
    ("~20% of potential", "unlocked"),
]
for i, (b1, b2) in enumerate(old_items):
    y = Inches(2.22) + Inches(0.52) * i
    d.rect(s3, lx + Inches(0.18), y + Inches(0.09), Inches(0.12), Inches(0.12), hx("EF4444"), radius=0.5)
    d.text(s3, b1 + "  " + b2, lx + Inches(0.42), y, lw - Inches(0.6), Inches(0.30),
           size=12.5, color=b.INK)

# Arrow
d.text(s3, "→", Inches(6.3), Inches(3.7), Inches(0.7), Inches(0.6),
       size=36, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)

# Right card: New way — 4-step loop
rx = Inches(7.1)
rw = CW - Inches(5.6) - Inches(0.7)
d.rect(s3, rx, Inches(1.58), rw, Inches(5.0), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s3, rx, Inches(1.58), rw, Inches(0.08), b.TEAL)
d.text(s3, "🎼  Director / Conductor", rx + Inches(0.2), Inches(1.72), rw - Inches(0.4), Inches(0.36),
       size=14, color=b.TEAL, bold=True)

loop_steps = [
    ("①", "Plan",    AMBER,  "PLAN.md · north star · cheapest to be wrong"),
    ("②", "Context", GREEN,  "right info · lean window · /prime · subagents"),
    ("③", "Verify",  b.TEAL, "auto-checks → lint → tests → review → ships"),
    ("④", "Evolve",  VIOLET, "system upgrade · rule → doc → cmd → skill"),
]
for i, (num, title, col, detail) in enumerate(loop_steps):
    ny = Inches(2.18) + Inches(1.06) * i
    d.rect(s3, rx + Inches(0.18), ny, Inches(0.34), Inches(0.34), col, radius=0.5)
    d.text(s3, num, rx + Inches(0.18), ny, Inches(0.34), Inches(0.34),
           size=11, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s3, title, rx + Inches(0.62), ny, Inches(1.3), Inches(0.34),
           size=14, color=b.INK, bold=True)
    d.text(s3, detail, rx + Inches(2.0), ny, rw - Inches(2.2), Inches(0.34),
           size=11, color=b.MUTED)
    if i < 3:
        d.rect(s3, rx + Inches(0.28), ny + Inches(0.37), Pt(2), Inches(0.67), SLATE200)

# Quote at bottom
d.rect(s3, M, Inches(6.6), CW, Inches(0.65), b.LIGHT_TEAL, radius=0.02)
d.text(s3, '"You\'re not learning to code, you\'re learning to direct."',
       M + Inches(0.2), Inches(6.68), CW - Inches(0.4), Inches(0.50),
       size=12, color=b.ACCENT, italic=True)

d.footer(s3, 5, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — PLAN FIRST
# ════════════════════════════════════════════════════════════════════════════
s4 = d.slide(fill=b.SOFT)
d.rect(s4, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s4, "02 · PLAN FIRST", color=AMBER)
d.header(s4, "Make It Plan First", "PLAN.md is the north star — cheapest place to be wrong", band=False)

# Left: PLAN.md card
lw = Inches(5.8)
d.rect(s4, M, Inches(1.58), lw, Inches(4.9), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s4, M, Inches(1.58), lw, Inches(0.08), AMBER)
d.rect(s4, M + Inches(0.18), Inches(1.72), Inches(1.0), Inches(0.30), AMBER, radius=0.02)
d.text(s4, "PLAN.md", M + Inches(0.22), Inches(1.73), Inches(0.96), Inches(0.28),
       size=10, color=b.WHITE, bold=True, font=MONO)
d.text(s4, "= the north star", M + Inches(1.3), Inches(1.74), Inches(2.0), Inches(0.28),
       size=11, color=b.MUTED, italic=True)

plan_items = [
    "goal + success criteria",
    "codebase + docs analysis",
    "integration points",
    "task-specific rules",
    "granular task list",
    "validation strategy",
]
for i, item in enumerate(plan_items):
    y = Inches(2.18) + Inches(0.56) * i
    d.rect(s4, M + Inches(0.18), y + Inches(0.09), Inches(0.11), Inches(0.11), AMBER, radius=0.5)
    d.text(s4, item, M + Inches(0.40), y, lw - Inches(0.6), Inches(0.30),
           size=13, color=b.INK)

d.rect(s4, M + Inches(0.18), Inches(5.56), lw - Inches(0.36), Pt(1.5), SLATE200)
d.text(s4, '"The plan is the cheapest place to be wrong."',
       M + Inches(0.18), Inches(5.65), lw - Inches(0.36), Inches(0.40),
       size=11.5, color=AMBER, italic=True)

# Right: Workflow steps
rx = M + lw + Inches(0.3)
rw = CW - lw - Inches(0.3)
d.rect(s4, rx, Inches(1.58), rw, Inches(4.9), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s4, rx, Inches(1.58), rw, Inches(0.08), b.TEAL)
d.text(s4, "Workflow", rx + Inches(0.2), Inches(1.72), rw - Inches(0.4), Inches(0.34),
       size=13.5, color=b.INK, bold=True)

wf_steps = [
    (ORANGE, "/prime",       "docs · structure · git log"),
    (AMBER,  "research",     "subagents = 3 options"),
    (GREEN,  "/plan",        "writes the document"),
    (b.TEAL, "edit live",    "add e2e · fix scope"),
    (VIOLET, "fresh context","new session"),
    (hx("3B82F6"), "execute","task by task"),
]
for i, (col, cmd, detail) in enumerate(wf_steps):
    ny = Inches(2.22) + Inches(0.76) * i
    d.rect(s4, rx + Inches(0.18), ny + Inches(0.06), Inches(0.22), Inches(0.22), col, radius=0.5)
    if i < len(wf_steps) - 1:
        d.rect(s4, rx + Inches(0.27), ny + Inches(0.30), Pt(2), Inches(0.54), SLATE200)
    d.text(s4, cmd, rx + Inches(0.52), ny + Inches(0.02), rw - Inches(0.7), Inches(0.26),
           size=13, color=b.INK, bold=True, font=MONO)
    d.text(s4, detail, rx + Inches(0.52), ny + Inches(0.28), rw - Inches(0.7), Inches(0.24),
           size=10.5, color=b.MUTED)

d.rect(s4, M, Inches(6.6), CW, Inches(0.65), b.LIGHT_TEAL, radius=0.02)
d.text(s4, '"Sandwich the delegation of coding between planning and validation."',
       M + Inches(0.2), Inches(6.68), CW - Inches(0.4), Inches(0.50),
       size=12, color=b.ACCENT, italic=True)

d.footer(s4, 6, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — MANAGE CONTEXT
# ════════════════════════════════════════════════════════════════════════════
s5 = d.slide(fill=b.SOFT)
d.rect(s5, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s5, "03 · MANAGE CONTEXT", color=GREEN)
d.header(s5, "Right Info, Not All Info", "Attention is scarce — the dumb zone is real", band=False)

# Left: Dumb zone
lw = Inches(5.6)
d.rect(s5, M, Inches(1.58), lw, Inches(2.5), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s5, M, Inches(1.58), lw, Inches(0.08), hx("EF4444"))
d.text(s5, "The Context Window Dumb Zone", M + Inches(0.2), Inches(1.72), lw - Inches(0.4), Inches(0.34),
       size=13.5, color=hx("EF4444"), bold=True)

dz_rows = [
    ("Opus 4.8",   "~250,000 tokens", hx("EF4444")),
    ("Opus 4.7",   "~200,000 tokens", ORANGE),
    ("Sonnet 4.6", "~100–125K tokens", AMBER),
]
for i, (model, threshold, col) in enumerate(dz_rows):
    ry = Inches(2.24) + Inches(0.6) * i
    d.rect(s5, M + Inches(0.18), ry, lw - Inches(0.36), Inches(0.50), b.SOFT, line=SLATE200, radius=0.01)
    d.text(s5, model, M + Inches(0.36), ry + Inches(0.09), Inches(2.2), Inches(0.30),
           size=12.5, color=b.INK, bold=True)
    d.text(s5, threshold, M + Inches(0.36) + Inches(2.5), ry + Inches(0.09), Inches(2.0), Inches(0.30),
           size=12.5, color=col, bold=True, font=MONO)

d.text(s5, "1M context ≠ 1M usable tokens. Attention degrades in the middle.",
       M + Inches(0.18), Inches(4.22), lw - Inches(0.36), Inches(0.34),
       size=10.5, color=b.MUTED, italic=True)

# Left: cluttered vs lean visual
d.rect(s5, M, Inches(4.2), lw, Inches(1.86), b.WHITE, line=SLATE200, radius=0.02)
d.text(s5, "Context window visualized:", M + Inches(0.18), Inches(4.30), lw - Inches(0.36), Inches(0.28),
       size=11, color=b.MUTED)
bar_colors_cluttered = [hx("EF4444"), ORANGE, AMBER, ORANGE, hx("EF4444")]
bar_colors_lean      = [b.TEAL, GREEN]
for i, col in enumerate(bar_colors_cluttered):
    d.rect(s5, M + Inches(0.18) + Inches(0.28)*i, Inches(4.68), Inches(0.24), Inches(0.28), col)
d.text(s5, "cluttered", M + Inches(0.18), Inches(5.02), Inches(1.5), Inches(0.20),
       size=9, color=hx("EF4444"), font=MONO)
d.text(s5, "→", M + Inches(1.82), Inches(4.64), Inches(0.36), Inches(0.36),
       size=22, color=b.TEAL, bold=True)
for i, col in enumerate(bar_colors_lean):
    d.rect(s5, M + Inches(2.28) + Inches(0.28)*i, Inches(4.68), Inches(0.24), Inches(0.28), col)
d.text(s5, "lean + sharp", M + Inches(2.28), Inches(5.02), Inches(1.5), Inches(0.20),
       size=9, color=GREEN, font=MONO)

# Right: 6 ways
rx = M + lw + Inches(0.3)
rw = CW - lw - Inches(0.3)
d.rect(s5, rx, Inches(1.58), rw, Inches(4.9), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s5, rx, Inches(1.58), rw, Inches(0.08), GREEN)
d.text(s5, "6 Ways to Control the Window", rx + Inches(0.2), Inches(1.72), rw - Inches(0.4), Inches(0.34),
       size=13.5, color=b.INK, bold=True)

ways = [
    (ORANGE, "Separate sessions",  "plan & build in different chats"),
    (AMBER,  "/prime first",        "docs, structure, git log on session start"),
    (GREEN,  "Specialized primes", "-frontend / -backend / -db"),
    (b.TEAL, "On-demand context",  "load reference docs only when needed"),
    (VIOLET, "Git log = memory",   "clean commits summarize context"),
    (hx("3B82F6"), "Subagents",    "delegate research; main stays clean"),
]
for i, (col, name, detail) in enumerate(ways):
    ny = Inches(2.22) + Inches(0.74) * i
    d.rect(s5, rx + Inches(0.18), ny + Inches(0.07), Inches(0.14), Inches(0.14), col, radius=0.5)
    d.text(s5, name, rx + Inches(0.42), ny, rw - Inches(0.6), Inches(0.26),
           size=12.5, color=b.INK, bold=True)
    d.text(s5, detail, rx + Inches(0.42), ny + Inches(0.26), rw - Inches(0.6), Inches(0.26),
           size=10.5, color=b.MUTED)

d.rect(s5, M, Inches(6.6), CW, Inches(0.65), b.LIGHT_TEAL, radius=0.02)
d.text(s5, '"Needle-in-a-haystack: information buried mid-context gets lost."',
       M + Inches(0.2), Inches(6.68), CW - Inches(0.4), Inches(0.50),
       size=12, color=b.ACCENT, italic=True)

d.footer(s5, 7, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — VERIFY THE WORK
# ════════════════════════════════════════════════════════════════════════════
s6 = d.slide(fill=b.SOFT)
d.rect(s6, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s6, "04 · VERIFY THE WORK", color=b.TEAL)
d.header(s6, "Don't Trust the First Pass", "Gate every output — code, content, or data", band=False)

# Left: pipeline
lw = Inches(5.8)
d.rect(s6, M, Inches(1.58), lw, Inches(5.0), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s6, M, Inches(1.58), lw, Inches(0.08), b.TEAL)

# Start
d.rect(s6, M + Inches(2.4), Inches(1.72), Inches(1.0), Inches(0.32), SLATE200, radius=0.02)
d.text(s6, "Agent Output", M + Inches(2.42), Inches(1.74), Inches(0.96), Inches(0.28),
       size=9.5, color=SLATE700, align=PP_ALIGN.CENTER)
d.rect(s6, M + Inches(2.87), Inches(2.05), Pt(2), Inches(0.26), SLATE200)

# Auto section
d.text(s6, "AUTOMATED  /validate", M + Inches(0.2), Inches(2.33), lw - Inches(0.4), Inches(0.24),
       size=9, color=GREEN, bold=True, font=MONO)

pipeline_auto = [
    ("①", "Auto-Checks", AMBER,  "lint, type check, format"),
    ("②", "Rules / Lint", GREEN,  "project-specific checks"),
    ("③", "Tests",        b.TEAL, "unit + integration"),
]
for i, (num, title, col, sub) in enumerate(pipeline_auto):
    py = Inches(2.58) + Inches(0.76) * i
    d.rect(s6, M + Inches(0.18), py, lw - Inches(0.36), Inches(0.58), b.SOFT, line=SLATE200, radius=0.01)
    d.rect(s6, M + Inches(0.18), py, Inches(0.42), Inches(0.58), col, radius=0.01)
    d.text(s6, num, M + Inches(0.18), py + Inches(0.12), Inches(0.42), Inches(0.34),
           size=12, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s6, title, M + Inches(0.7), py + Inches(0.06), lw - Inches(1.0), Inches(0.26),
           size=12.5, color=b.INK, bold=True)
    d.text(s6, sub, M + Inches(0.7), py + Inches(0.32), lw - Inches(1.0), Inches(0.22),
           size=10, color=b.MUTED)
    if i < 2:
        d.rect(s6, M + Inches(0.35), py + Inches(0.60), Pt(2), Inches(0.16), SLATE200)

# Fail loop text
d.rect(s6, M + lw - Inches(1.7), Inches(2.58), Inches(1.52), Inches(2.28), hx("FEF2F2"), line=hx("EF4444"))
d.text(s6, "fail →\nfix +\nre-run ↺", M + lw - Inches(1.58), Inches(2.72),
       Inches(1.3), Inches(2.0), size=11.5, color=hx("EF4444"), bold=True, align=PP_ALIGN.CENTER, ls=1.5)

# Human section
d.text(s6, "HUMAN + AGENT", M + Inches(0.2), Inches(4.86), lw - Inches(0.4), Inches(0.24),
       size=9, color=VIOLET, bold=True, font=MONO)
d.rect(s6, M + Inches(2.87), Inches(4.67), Pt(2), Inches(0.22), SLATE200)

pipeline_human = [
    ("④", "Review",          VIOLET, "human + agent code review"),
    ("⑤", "Real-World Check",hx("3B82F6"), "deploy to staging / verify live"),
]
for i, (num, title, col, sub) in enumerate(pipeline_human):
    py = Inches(5.10) + Inches(0.66) * i
    d.rect(s6, M + Inches(0.18), py, lw - Inches(0.36), Inches(0.50), b.SOFT, line=SLATE200, radius=0.01)
    d.rect(s6, M + Inches(0.18), py, Inches(0.42), Inches(0.50), col, radius=0.01)
    d.text(s6, num, M + Inches(0.18), py + Inches(0.08), Inches(0.42), Inches(0.34),
           size=12, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s6, title, M + Inches(0.7), py + Inches(0.04), lw - Inches(1.0), Inches(0.22),
           size=12.5, color=b.INK, bold=True)
    d.text(s6, sub, M + Inches(0.7), py + Inches(0.26), lw - Inches(1.0), Inches(0.20),
           size=10, color=b.MUTED)
    if i < 1:
        d.rect(s6, M + Inches(0.35), py + Inches(0.52), Pt(2), Inches(0.16), SLATE200)

d.rect(s6, M + Inches(0.18), Inches(6.46), lw - Inches(0.36), Inches(0.30), hx("DCFCE7"), radius=0.02)
d.text(s6, "✓  SHIPS", M + Inches(0.18), Inches(6.46), lw - Inches(0.36), Inches(0.30),
       size=12, color=GREEN, bold=True, align=PP_ALIGN.CENTER)

# Right: stats
rx = M + lw + Inches(0.3)
rw = CW - lw - Inches(0.3)

stat_block(s6, rx, Inches(1.62), rw, "65%", "without verify", "First-pass accuracy\nwithout verification", n_color=hx("EF4444"))
d.text(s6, "↓ improves with /validate ↓", rx, Inches(3.22), rw, Inches(0.36),
       size=11, color=b.MUTED, italic=True, align=PP_ALIGN.CENTER)
stat_block(s6, rx, Inches(3.62), rw, "92%", "with verification", "First-pass accuracy\nwith verification pipeline", n_color=GREEN)

d.rect(s6, rx, Inches(5.18), rw, Inches(1.36), b.LIGHT_TEAL, radius=0.02)
d.text(s6, '"We only care about what we see when control comes back to us."',
       rx + Inches(0.15), Inches(5.28), rw - Inches(0.3), Inches(1.1),
       size=12, color=b.ACCENT, italic=True, ls=1.45, wrap=True)

d.footer(s6, 8, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — BUILD THE SYSTEM
# ════════════════════════════════════════════════════════════════════════════
s7 = d.slide(fill=b.SOFT)
d.rect(s7, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s7, "05 · BUILD THE SYSTEM", color=hx("3B82F6"))
d.header(s7, "Evolve the System, Don't Just Fix the Bug", "Every bug is a permanent upgrade opportunity", band=False)

# Left: bug → upgrade list
lw = Inches(5.8)
d.rect(s7, M, Inches(1.58), lw, Inches(5.0), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s7, M, Inches(1.58), lw, Inches(0.08), ORANGE)
d.text(s7, "When a Bug Appears →", M + Inches(0.2), Inches(1.72), lw - Inches(0.4), Inches(0.34),
       size=13.5, color=ORANGE, bold=True)

d.rect(s7, M + Inches(0.18), Inches(2.18), Inches(0.26), Inches(0.26), hx("EF4444"), radius=0.5)
d.text(s7, "Bug detected", M + Inches(0.56), Inches(2.18), lw - Inches(0.76), Inches(0.26),
       size=12, color=hx("EF4444"), italic=True)

bug_items = [
    (ORANGE,  "+  rule",          '"use @/ aliases"  →  prevents import path errors'),
    (AMBER,   "+  reference doc", "auth-flow.md  →  agent reads it next time"),
    (GREEN,   "+  update plan",   '"always add tests"  →  encoded in PLAN.md'),
    (hx("3B82F6"), "+  new /command", "reuse the fix pattern  →  forever"),
]
for i, (col, action, result) in enumerate(bug_items):
    ay = Inches(2.68) + Inches(0.78) * i
    d.rect(s7, M + Inches(0.18), ay, lw - Inches(0.36), Inches(0.62), b.SOFT, line=SLATE200, radius=0.01)
    d.text(s7, action, M + Inches(0.32), ay + Inches(0.08), Inches(1.4), Inches(0.26),
           size=12.5, color=col, bold=True, font=MONO)
    d.text(s7, result, M + Inches(1.78), ay + Inches(0.08), lw - Inches(2.0), Inches(0.26),
           size=11, color=SLATE700)
    if i < 3:
        d.rect(s7, M + Inches(0.36), ay + Inches(0.64), Pt(2), Inches(0.14), SLATE200)

d.rect(s7, M + Inches(0.18), Inches(5.96), lw - Inches(0.36), Inches(0.42), b.TEAL, radius=0.02)
d.text(s7, "Every bug = a permanent upgrade", M + Inches(0.18), Inches(5.96), lw - Inches(0.36), Inches(0.42),
       size=13, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)

# Right: staircase
rx = M + lw + Inches(0.3)
rw = CW - lw - Inches(0.3)
d.rect(s7, rx, Inches(1.58), rw, Inches(5.0), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s7, rx, Inches(1.58), rw, Inches(0.08), hx("3B82F6"))
d.text(s7, "The Rising Floor", rx + Inches(0.2), Inches(1.72), rw - Inches(0.4), Inches(0.34),
       size=13.5, color=b.INK, bold=True)

stair_steps = [
    (ORANGE, "rule",  28),
    (AMBER,  "doc",   55),
    (b.TEAL, "cmd",   82),
    (hx("3B82F6"), "skill", 108),
]
base_y = Inches(5.52)
sw = Inches(0.82)
gap = Inches(0.14)
total_sw = len(stair_steps) * (sw + gap) - gap
start_x = rx + (rw - total_sw) / 2

for i, (col, label, h_pts) in enumerate(stair_steps):
    bx = start_x + i * (sw + gap)
    bh = Pt(h_pts)
    by = base_y - bh
    d.rect(s7, bx, by, sw, bh, col, radius=0.01)
    d.text(s7, label, bx, by + Inches(0.08), sw, Inches(0.28),
           size=11, color=b.WHITE, bold=True, font=MONO, align=PP_ALIGN.CENTER)
    d.text(s7, f"week {(i+1)*2}" if i < 3 else "month 2",
           bx, base_y + Inches(0.06), sw, Inches(0.22),
           size=9, color=b.MUTED, align=PP_ALIGN.CENTER)

d.text(s7, "floor keeps rising\n+ smarter every week",
       rx + Inches(0.2), Inches(3.0), rw - Inches(0.4), Inches(0.72),
       size=12, color=b.MUTED, ls=1.4, align=PP_ALIGN.CENTER, italic=True)

d.rect(s7, M, Inches(6.6), CW, Inches(0.65), b.LIGHT_TEAL, radius=0.02)
d.text(s7, '"Same workflow, taller building. Only the ceiling changes."',
       M + Inches(0.2), Inches(6.68), CW - Inches(0.4), Inches(0.50),
       size=12, color=b.ACCENT, italic=True)

d.footer(s7, 9, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — AGENT = MODEL + HARNESS (dark)
# ════════════════════════════════════════════════════════════════════════════
s8 = d.slide(fill=b.NAVY)
d.rect(s8, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s8, "ARCHITECTURE", color=b.TEAL)
d.text(s8, "Agent = Model + Harness", M, Inches(0.42), CW, Inches(0.72),
       size=32, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
d.rect(s8, M, Inches(1.18), Inches(1.6), Inches(0.06), b.TEAL)
d.text(s8, "Same skills, bigger building — only the ceiling changes",
       M, Inches(1.3), CW, Inches(0.38), size=14, color=hx("94A3B8"))

# Concentric ring visual using layered rects (rounded)
cx = Inches(1.8)
cy = Inches(1.8)
# Outer ring (AI Layer) — large rounded rect
d.rect(s8, cx, cy, Inches(5.5), Inches(4.4), hx("0E2030"), line=b.TEAL, radius=0.04)
d.text(s8, "THE AI LAYER  (You BUILD)", cx + Inches(0.18), cy + Inches(0.14),
       Inches(5.0), Inches(0.30), size=10.5, color=b.TEAL, bold=True, font=MONO)
d.text(s8, "CLAUDE.md · Skills · Hooks · MCP · LSP",
       cx + Inches(0.18), cy + Inches(0.44), Inches(5.0), Inches(0.24),
       size=9.5, color=hx("67E8F9"), italic=True)

# Mid ring (Harness)
d.rect(s8, cx + Inches(0.7), cy + Inches(0.88), Inches(4.1), Inches(3.06), hx("0A1A28"),
       line=hx("3B82F6"), radius=0.04)
d.text(s8, "THE HARNESS  (You PICK)", cx + Inches(0.9), cy + Inches(1.02),
       Inches(3.6), Inches(0.28), size=10, color=hx("93C5FD"), bold=True, font=MONO)
d.text(s8, "Claude Code · Codex · Cursor",
       cx + Inches(0.9), cy + Inches(1.30), Inches(3.6), Inches(0.24),
       size=9.5, color=hx("93C5FD"), italic=True)

# Inner (Model)
d.rect(s8, cx + Inches(1.5), cy + Inches(1.82), Inches(2.5), Inches(1.58), hx("100820"),
       line=hx("A78BFA"), radius=0.04)
d.text(s8, "The Model", cx + Inches(1.5), cy + Inches(2.06),
       Inches(2.5), Inches(0.36), size=15, color=hx("C4B5FD"), bold=True, align=PP_ALIGN.CENTER)
d.text(s8, "(You PICK)", cx + Inches(1.5), cy + Inches(2.46),
       Inches(2.5), Inches(0.26), size=11, color=hx("A78BFA"), align=PP_ALIGN.CENTER, italic=True)

# Right: bullet points
rx = cx + Inches(5.8)
rw = W - rx - M

d.rect(s8, rx, Inches(1.68), rw, Inches(1.56), hx("0E2030"), line=hx("22D3EE"), radius=0.02)
d.text(s8, "You BUILD → The AI Layer", rx + Inches(0.16), Inches(1.76), rw - Inches(0.32), Inches(0.28),
       size=11, color=b.TEAL, bold=True, font=MONO)
d.text(s8, "CLAUDE.md  ·  custom rules\nSkills  ·  Hooks  ·  MCP servers",
       rx + Inches(0.16), Inches(2.06), rw - Inches(0.32), Inches(1.0),
       size=11, color=hx("CBD5E1"), ls=1.5)

d.rect(s8, rx, Inches(3.42), rw, Inches(1.56), hx("0E2030"), line=hx("3B82F6"), radius=0.02)
d.text(s8, "You PICK → The Harness", rx + Inches(0.16), Inches(3.50), rw - Inches(0.32), Inches(0.28),
       size=11, color=hx("93C5FD"), bold=True, font=MONO)
d.text(s8, "Claude Code  ·  Codex  ·  Cursor\nWraps the model with tools + context",
       rx + Inches(0.16), Inches(3.80), rw - Inches(0.32), Inches(1.0),
       size=11, color=hx("CBD5E1"), ls=1.5)

d.rect(s8, rx, Inches(5.16), rw, Inches(1.0), hx("0E2030"), line=hx("A78BFA"), radius=0.02)
d.text(s8, "The Model → Claude", rx + Inches(0.16), Inches(5.24), rw - Inches(0.32), Inches(0.28),
       size=11, color=hx("C4B5FD"), bold=True, font=MONO)
d.text(s8, "You pick the right model for the task",
       rx + Inches(0.16), Inches(5.54), rw - Inches(0.32), Inches(0.50),
       size=11, color=hx("CBD5E1"))

d.footer(s8, 10, TOTAL, dark=True)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — RALF LOOP
# ════════════════════════════════════════════════════════════════════════════
s9 = d.slide(fill=b.SOFT)
d.rect(s9, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s9, "ADVANCED · HARNESS ENGINEERING", color=VIOLET)
d.header(s9, "The RALF Loop", "Multi-session orchestration for large tasks — deterministic, not chaotic", band=False)

# 3 session boxes
sessions = [
    ("SESSION 01", "PLANNER",     AMBER,  "Reads the full spec. Defines phase list. Creates detailed handoff document.","→ handoff.md"),
    ("SESSION 02", "IMPLEMENTER", b.TEAL, "Reads handoff. Executes phase. Stays in clean context. One phase at a time.","→ exec-report.md"),
    ("SESSION 03", "VALIDATOR",   GREEN,  "Reads execution report. Runs code review. Validates outputs against spec.", "→ ships ✓"),
]
nw = (CW - Inches(0.8)) / 3

for i, (sess, role, col, body, out) in enumerate(sessions):
    sx = M + i * (nw + Inches(0.4))
    d.rect(s9, sx, Inches(1.6), nw, Inches(4.0), b.WHITE, line=SLATE200, radius=0.02)
    d.rect(s9, sx, Inches(1.6), nw, Inches(0.08), col)
    d.text(s9, sess, sx + Inches(0.18), Inches(1.74), nw - Inches(0.36), Inches(0.26),
           size=9, color=b.MUTED, bold=True, font=MONO)
    d.text(s9, role, sx + Inches(0.18), Inches(2.02), nw - Inches(0.36), Inches(0.40),
           size=17, color=col, bold=True, font=b.FONT_H)
    d.rect(s9, sx + Inches(0.18), Inches(2.48), Inches(1.0), Pt(2), col)
    d.text(s9, body, sx + Inches(0.18), Inches(2.6), nw - Inches(0.36), Inches(2.0),
           size=12, color=SLATE700, ls=1.5, wrap=True, shrink=True)
    d.rect(s9, sx + Inches(0.18), Inches(5.18), nw - Inches(0.36), Inches(0.30), b.SOFT, line=col, radius=0.01)
    d.text(s9, out, sx + Inches(0.18), Inches(5.18), nw - Inches(0.36), Inches(0.30),
           size=11, color=col, bold=True, font=MONO, align=PP_ALIGN.CENTER)
    # Arrow between sessions
    if i < 2:
        ax = sx + nw + Inches(0.1)
        d.text(s9, "→", ax, Inches(3.36), Inches(0.24), Inches(0.30),
               size=18, color=SLATE300, bold=True, align=PP_ALIGN.CENTER)

# Context loop note
d.rect(s9, M, Inches(5.7), CW, Inches(0.70), b.WHITE, line=SLATE200, radius=0.02)
d.text(s9, "Why RALF?  One session hits the dumb zone (~250K tokens). RALF breaks work into fresh-context sessions with clean handoff docs.",
       M + Inches(0.2), Inches(5.78), CW - Inches(3.2), Inches(0.54),
       size=11.5, color=SLATE700, ls=1.45, wrap=True, shrink=True)
d.rect(s9, W - Inches(2.8), Inches(5.70), Inches(2.2), Inches(0.70), b.LIGHT_TEAL, line=b.TEAL, radius=0.02)
d.text(s9, "Archon Project\nOpen-source RALF harness\nby Cole (GitHub)", W - Inches(2.7), Inches(5.78),
       Inches(2.0), Inches(0.54), size=10, color=b.ACCENT, ls=1.4)

d.rect(s9, M, Inches(6.6), CW, Inches(0.65), b.LIGHT_TEAL, radius=0.02)
d.text(s9, '"Build Claude Code into a system instead of having Claude Code try to orchestrate everything."',
       M + Inches(0.2), Inches(6.68), CW - Inches(0.4), Inches(0.50),
       size=12, color=b.ACCENT, italic=True)

d.footer(s9, 11, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — SECURITY MINDSET
# ════════════════════════════════════════════════════════════════════════════
s10 = d.slide(fill=b.SOFT)
d.rect(s10, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s10, "SECURITY", color=hx("EF4444"))
d.header(s10, "The Security Mindset", "Prompts are not a permission layer — infrastructure is", band=False)

# Warning card
hw = (CW - Inches(0.3)) / 2
d.rect(s10, M, Inches(1.6), hw, Inches(4.7), hx("FEF2F2"), line=hx("EF4444"), radius=0.02)
d.rect(s10, M, Inches(1.6), hw, Inches(0.08), hx("EF4444"))
d.text(s10, "⚠  False Security", M + Inches(0.2), Inches(1.74), hw - Inches(0.4), Inches(0.34),
       size=13.5, color=hx("EF4444"), bold=True)

bad_items = [
    '"Never wipe the database" → it still will',
    '"Don\'t delete the folder" → it writes a script that does',
    "Prompt instructions are not enforced at runtime",
    "Proactive agents will touch anything readable",
    "Real incident: agent sent discount email to full list",
]
for i, item in enumerate(bad_items):
    y = Inches(2.28) + Inches(0.56) * i
    d.rect(s10, M + Inches(0.2), y + Inches(0.1), Inches(0.12), Inches(0.12), hx("EF4444"), radius=0.5)
    d.text(s10, item, M + Inches(0.44), y, hw - Inches(0.64), Inches(0.3),
           size=12, color=hx("7F1D1D"), ls=1.4, wrap=True, shrink=True)

# Safe card
rx = M + hw + Inches(0.3)
d.rect(s10, rx, Inches(1.6), hw, Inches(4.7), hx("F0FDF4"), line=GREEN, radius=0.02)
d.rect(s10, rx, Inches(1.6), hw, Inches(0.08), GREEN)
d.text(s10, "✓  Real Protection", rx + Inches(0.2), Inches(1.74), hw - Inches(0.4), Inches(0.34),
       size=13.5, color=GREEN, bold=True)

safe_items = [
    "Scoped API keys (read-only, limited write scope)",
    "Infrastructure-level permissions, not just prompts",
    "Assume: anything readable or touchable, it WILL touch",
    "Include security scanning in verification pipeline",
    "Supabase keys leaked → databases wiped → act now",
]
for i, item in enumerate(safe_items):
    y = Inches(2.28) + Inches(0.56) * i
    d.rect(s10, rx + Inches(0.2), y + Inches(0.1), Inches(0.12), Inches(0.12), GREEN, radius=0.5)
    d.text(s10, item, rx + Inches(0.44), y, hw - Inches(0.64), Inches(0.3),
           size=12, color=hx("14532D"), ls=1.4, wrap=True, shrink=True)

d.rect(s10, M, Inches(6.6), CW, Inches(0.65), b.LIGHT_TEAL, radius=0.02)
d.text(s10, '"Anything the agent can read or touch, you have to assume that it will — even if you never ask it to."',
       M + Inches(0.2), Inches(6.68), CW - Inches(0.4), Inches(0.50),
       size=12, color=b.ACCENT, italic=True, shrink=True)

d.footer(s10, 12, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — KEY PRINCIPLES (dark)
# ════════════════════════════════════════════════════════════════════════════
s11 = d.slide(fill=b.NAVY)
d.rect(s11, 0, 0, W, Inches(0.08), b.TEAL)
d.text(s11, "10 Principles Worth Keeping", M, Inches(0.30), CW, Inches(0.60),
       size=30, color=b.WHITE, bold=True, font=b.FONT_H)
d.text(s11, "Distilled from 68 minutes with Cole + Nate Herk", M, Inches(0.92), CW, Inches(0.30),
       size=13, color=hx("94A3B8"), italic=True)
d.rect(s11, M, Inches(1.26), Inches(1.6), Inches(0.05), b.TEAL)

quotes_data = [
    (AMBER,  '"The plan is the cheapest place to be wrong."'),
    (ORANGE, '"You\'re getting ~20% out of Claude Code — not about coding skill."'),
    (GREEN,  '"Attention is scarce. Don\'t throw everything at the window."'),
    (b.TEAL, '"Every bug = a permanent upgrade."'),
    (hx("3B82F6"), '"Same workflow, taller building. Only the ceiling changes."'),
    (VIOLET, '"We only care about what we see when control comes back to us."'),
    (hx("F472B6"), '"You\'re not learning to code, you\'re learning to direct."'),
    (hx("EF4444"), '"Anything the agent can touch, you must assume it will."'),
]

qw = (CW - Inches(0.3)) / 2
for i, (col, text) in enumerate(quotes_data):
    row, column = divmod(i, 2)
    qx = M + column * (qw + Inches(0.3))
    qy = Inches(1.48) + Inches(1.26) * row
    d.rect(s11, qx, qy, qw, Inches(1.12), hx("0E1E34"), line=hx("1E3A5A"), radius=0.02)
    d.rect(s11, qx, qy, Inches(0.06), Inches(1.12), col, radius=0.01)
    d.text(s11, text, qx + Inches(0.18), qy + Inches(0.14),
           qw - Inches(0.3), Inches(0.84), size=11, color=hx("CBD5E1"), italic=True, ls=1.4,
           wrap=True, shrink=True)

d.footer(s11, 13, TOTAL, dark=True)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — WHAT'S NEXT (dark)
# ════════════════════════════════════════════════════════════════════════════
s12 = d.slide(fill=b.NAVY)
d.rect(s12, 0, 0, W, Inches(0.08), b.TEAL)

d.text(s12, "Start Directing.\nStop Vibe Coding.",
       M, Inches(0.34), Inches(7.0), Inches(1.5),
       size=40, color=b.WHITE, bold=True, font=b.FONT_H, ls=1.15, shrink=True)

d.rect(s12, M, Inches(1.9), Inches(2.0), Inches(0.06), b.TEAL)

d.text(s12, "Apply the 4 skills. Run the loop. Let every bug become a permanent upgrade.",
       M, Inches(2.06), Inches(9.0), Inches(0.44),
       size=15.5, color=hx("CBD5E1"))

# 3 action cards
next_cards = [
    (AMBER,    "Write a PLAN.md",
               "Before your next Claude Code task. Include goal, success criteria, integration points, and validation strategy."),
    (b.TEAL,   "Add One Verify Step",
               "Pick your most common task. Add an auto-check so Claude validates its own output before returning to you."),
    (GREEN,    "Fix Bugs Permanently",
               "Next time a bug appears — write a rule, a reference doc, or a /command. The floor keeps rising."),
]
nw2 = (CW - Inches(0.6)) / 3
for i, (col, title, body) in enumerate(next_cards):
    nx = M + i * (nw2 + Inches(0.3))
    d.rect(s12, nx, Inches(2.74), nw2, Inches(3.8), hx("0E1E34"), line=hx("1E3A5A"), radius=0.02)
    d.rect(s12, nx, Inches(2.74), nw2, Inches(0.08), col)
    d.rect(s12, nx + Inches(0.18), Inches(2.92), Inches(0.30), Inches(0.30), col, radius=0.5)
    d.text(s12, str(i + 1), nx + Inches(0.18), Inches(2.92), Inches(0.30), Inches(0.30),
           size=13, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s12, title, nx + Inches(0.18), Inches(3.32), nw2 - Inches(0.36), Inches(0.44),
           size=14.5, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
    d.text(s12, body, nx + Inches(0.18), Inches(3.84), nw2 - Inches(0.36), Inches(2.4),
           size=12, color=hx("94A3B8"), ls=1.5, wrap=True, shrink=True)

# Source strip
d.rect(s12, M, Inches(6.6), CW, Inches(0.65), hx("0E1E34"), radius=0.02)
d.text(s12,
       "Source: Nate Herk × Cole · youtube.com/watch?v=RzLV8sfFdMM  ·  Archon Project: github.com/coleam00/archon",
       M + Inches(0.2), Inches(6.68), CW - Inches(0.4), Inches(0.50),
       size=10, color=hx("475569"))

d.footer(s12, 14, TOTAL, dark=True)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — BUSINESS USE CASES (Beyond Code)
# ════════════════════════════════════════════════════════════════════════════
s13 = d.slide(fill=b.SOFT)
d.rect(s13, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s13, "BUSINESS APPLICATIONS", color=ORANGE)
d.header(s13, "Not Just For Software Teams", "The same 4 skills work for any business operation", band=False)

use_cases = [
    (ORANGE, "B2B Quote Automation",
     "Research inventory agent\n→ Price comparison agent\n→ PDF draft agent\n→ Formatting agent",
     "4 agents, clean handoffs, zero copy-paste"),
    (b.TEAL, "Knowledge Work / Second Brain",
     "Research → summarize → organize\n→ retrieve → synthesize\n→ deliver briefings",
     "Claude Code as your operating system for thinking"),
    (GREEN, "Business Operations",
     "Invoicing · client comms\nProposal drafting\nContract review · scheduling",
     "Non-technical teams can direct agents with PLAN.md"),
    (VIOLET, "Content Pipeline",
     "Competitor research\n→ ideation feed\n→ brief writing\n→ draft → publish",
     "Same loop; content is just another output type"),
]

ucw = (CW - Inches(0.54)) / 4
for i, (col, title, steps, outcome) in enumerate(use_cases):
    ux = M + i * (ucw + Inches(0.18))
    d.rect(s13, ux, Inches(1.6), ucw, Inches(4.85), b.WHITE, line=SLATE200, radius=0.02)
    d.rect(s13, ux, Inches(1.6), ucw, Inches(0.08), col)
    d.rect(s13, ux + Inches(0.16), Inches(1.76), Inches(0.24), Inches(0.24), col, radius=0.5)
    d.text(s13, title, ux + Inches(0.16), Inches(2.1), ucw - Inches(0.32), Inches(0.5),
           size=13, color=b.INK, bold=True, font=b.FONT_H, shrink=True, wrap=True)
    d.rect(s13, ux + Inches(0.16), Inches(2.66), ucw - Inches(0.32), Pt(1.5), SLATE200)
    d.text(s13, "Pipeline Steps:", ux + Inches(0.16), Inches(2.78), ucw - Inches(0.32), Inches(0.24),
           size=9, color=b.MUTED, bold=True, font=MONO)
    d.text(s13, steps, ux + Inches(0.16), Inches(3.06), ucw - Inches(0.32), Inches(1.6),
           size=11, color=SLATE700, ls=1.5, wrap=True, shrink=True)
    d.rect(s13, ux + Inches(0.16), Inches(4.82), ucw - Inches(0.32), Inches(0.52), b.LIGHT_TEAL, radius=0.02)
    d.text(s13, outcome, ux + Inches(0.2), Inches(4.88), ucw - Inches(0.4), Inches(0.44),
           size=10.5, color=b.ACCENT, italic=True, ls=1.35, wrap=True, shrink=True)

d.rect(s13, M, Inches(6.6), CW, Inches(0.65), b.NAVY, radius=0.02)
d.text(s13,
       "Rule of thumb:  if the output repeats every week and has a pattern, it can be a directed loop.",
       M + Inches(0.2), Inches(6.68), CW - Inches(0.4), Inches(0.50),
       size=12, color=b.TEAL, bold=True)
d.footer(s13, 15, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — PLAN.md DEEP DIVE
# ════════════════════════════════════════════════════════════════════════════
s14 = d.slide(fill=b.SOFT)
d.rect(s14, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s14, "PLAN.md — DEEP DIVE", color=AMBER)
d.header(s14, "Anatomy of a Great PLAN.md", "The document that transforms a prompt into a project", band=False)

# Left: section breakdown
lw = Inches(5.6)
d.rect(s14, M, Inches(1.6), lw, Inches(5.0), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s14, M, Inches(1.6), lw, Inches(0.08), AMBER)
d.text(s14, "6 Required Sections", M + Inches(0.2), Inches(1.74), lw - Inches(0.4), Inches(0.34),
       size=13.5, color=b.INK, bold=True)

plan_sections = [
    (AMBER,  "Goal + Success Criteria",
             "What done looks like. Measurable. Not 'build a feature' — 'user can log in with Google and reach dashboard in <2s'."),
    (ORANGE, "Codebase + Docs Analysis",
             "Agent reads the repo first. Key files, folder structure, patterns already in use."),
    (GREEN,  "Integration Points",
             "What external systems, APIs, or services touch this work? Auth providers, databases, third-party APIs."),
    (b.TEAL, "Task-Specific Rules",
             "Anti-patterns to avoid. 'Use @/ aliases.' 'Never import from /lib/utils.ts.' 'Always write tests.'"),
    (VIOLET, "Granular Task List",
             "Numbered. One action per item. The agent ticks these off. Include verification steps inline."),
    (hx("3B82F6"), "Validation Strategy",
             "How we know it worked. Test commands. Manual checks. Screenshot targets. CI pipeline checks."),
]

for i, (col, section_title, desc) in enumerate(plan_sections):
    sy = Inches(2.2) + Inches(0.72) * i
    d.rect(s14, M + Inches(0.18), sy, Inches(0.22), Inches(0.22), col, radius=0.5)
    d.text(s14, section_title, M + Inches(0.52), sy, lw - Inches(0.72), Inches(0.24),
           size=12.5, color=b.INK, bold=True)
    d.text(s14, desc, M + Inches(0.52), sy + Inches(0.24), lw - Inches(0.72), Inches(0.38),
           size=10.5, color=b.MUTED, ls=1.3, wrap=True, shrink=True)

# Right: Pro tips card
rx = M + lw + Inches(0.3)
rw = CW - lw - Inches(0.3)

d.rect(s14, rx, Inches(1.6), rw, Inches(2.46), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s14, rx, Inches(1.6), rw, Inches(0.08), b.TEAL)
d.text(s14, "Pro Tips", rx + Inches(0.2), Inches(1.74), rw - Inches(0.4), Inches(0.30),
       size=13, color=b.INK, bold=True)
tips = [
    "Write it in a separate planning session",
    "Have the agent generate 3 options first",
    "Edit live — add e2e, fix scope",
    "Use fresh context to execute from it",
]
for i, tip in enumerate(tips):
    ty = Inches(2.18) + Inches(0.46) * i
    d.rect(s14, rx + Inches(0.18), ty + Inches(0.1), Inches(0.12), Inches(0.12), b.TEAL, radius=0.5)
    d.text(s14, tip, rx + Inches(0.42), ty, rw - Inches(0.62), Inches(0.30),
           size=12, color=SLATE700)

d.rect(s14, rx, Inches(4.2), rw, Inches(2.38), b.WHITE, line=SLATE200, radius=0.02)
d.rect(s14, rx, Inches(4.2), rw, Inches(0.08), ORANGE)
d.text(s14, "When to Write It", rx + Inches(0.2), Inches(4.34), rw - Inches(0.4), Inches(0.28),
       size=13, color=b.INK, bold=True)
timing_items = [
    "Any task > 1 hour of expected work",
    "Anything touching 3+ files",
    "Any external API or data source",
    "New features (not bug patches)",
]
for i, item in enumerate(timing_items):
    iy = Inches(4.76) + Inches(0.42) * i
    d.rect(s14, rx + Inches(0.18), iy + Inches(0.09), Inches(0.11), Inches(0.11), ORANGE, radius=0.5)
    d.text(s14, item, rx + Inches(0.40), iy, rw - Inches(0.60), Inches(0.30),
           size=11.5, color=SLATE700)

d.rect(s14, M, Inches(6.6), CW, Inches(0.65), b.LIGHT_TEAL, radius=0.02)
d.text(s14, '"With coding agents, you spend more time planning than you actually do building."',
       M + Inches(0.2), Inches(6.68), CW - Inches(0.4), Inches(0.50),
       size=12, color=b.ACCENT, italic=True)
d.footer(s14, 16, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — YOUR FIRST WEEK ACTION PLAN
# ════════════════════════════════════════════════════════════════════════════
s15 = d.slide(fill=b.SOFT)
d.rect(s15, 0, 0, W, Inches(0.08), b.TEAL)
section_tag(s15, "GETTING STARTED", color=GREEN)
d.header(s15, "Your First Week Action Plan", "Seven days from vibe coding to directing a reliable loop", band=False)

week_items = [
    ("Day 1",  hx("3B82F6"), "Write your first PLAN.md",
     "Pick a task you've already done with Claude. Write a PLAN.md with 6 sections. Compare the output to your previous approach."),
    ("Day 2",  AMBER,        "Add /prime to your workflow",
     "Before any new session, /prime with project docs + git log. Notice how much less re-explanation you need."),
    ("Day 3",  GREEN,        "Add one verification step",
     "After Claude delivers output, add a /validate command — linter, test runner, or a simple 'confirm X is true' check."),
    ("Day 4",  b.TEAL,       "Create your first /command",
     "When you find yourself repeating a prompt 3 times, turn it into a slash command. Reuse forever."),
    ("Day 5",  VIOLET,       "Write one rule from a bug",
     "When a bug appears today, don't just fix it — write a rule in CLAUDE.md that prevents it permanently."),
    ("Day 6",  ORANGE,       "Try a subagent for research",
     "Delegate a research task to a subagent. Let the main context stay clean for the actual implementation work."),
    ("Day 7",  hx("EF4444"), "Run a full 4-step loop",
     "Pick a medium task. Plan → Context → Execute → Verify. Note the accuracy difference vs. your baseline."),
]

ww = (CW - Inches(0.9)) / 4
for i, (day, col, title, body) in enumerate(week_items):
    # two rows: 4 top, 3 bottom
    if i < 4:
        wx = M + i * (ww + Inches(0.3))
        wy = Inches(1.6)
        card_h = Inches(2.26)
    else:
        j = i - 4
        # 3 in bottom row, centered
        bottom_total_w = 3 * ww + 2 * Inches(0.3)
        start_x = M + (CW - bottom_total_w) / 2
        wx = start_x + j * (ww + Inches(0.3))
        wy = Inches(4.04)
        card_h = Inches(2.26)

    d.rect(s15, wx, wy, ww, card_h, b.WHITE, line=SLATE200, radius=0.02)
    d.rect(s15, wx, wy, ww, Inches(0.08), col)
    d.text(s15, day, wx + Inches(0.14), wy + Inches(0.12), ww - Inches(0.28), Inches(0.24),
           size=9, color=col, bold=True, font=MONO)
    d.text(s15, title, wx + Inches(0.14), wy + Inches(0.38), ww - Inches(0.28), Inches(0.52),
           size=12.5, color=b.INK, bold=True, font=b.FONT_H, wrap=True, shrink=True)
    d.text(s15, body, wx + Inches(0.14), wy + Inches(1.0), ww - Inches(0.28), card_h - Inches(1.12),
           size=10.5, color=b.MUTED, ls=1.45, wrap=True, shrink=True)

d.rect(s15, M, Inches(6.46), CW, Inches(0.78), b.NAVY, radius=0.02)
d.text(s15,
       "After week 1:  you'll have a PLAN.md template · /prime workflow · /validate command · 1 custom rule · first /command",
       M + Inches(0.2), Inches(6.54), CW - Inches(0.4), Inches(0.60),
       size=12, color=b.TEAL, bold=True, wrap=True, shrink=True)
d.footer(s15, 17, TOTAL)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — SYSTEM SUMMARY DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
s16 = d.slide(fill=b.NAVY)
d.rect(s16, 0, 0, W, Inches(0.08), b.TEAL)
d.text(s16, "The Complete System — at a Glance", M, Inches(0.28), CW, Inches(0.60),
       size=28, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
d.rect(s16, M, Inches(0.94), Inches(2.0), Inches(0.06), b.TEAL)

# 5 skill summary rows
summary_rows = [
    (AMBER,         "01  PLAN FIRST",       "PLAN.md before every task",
     "Goal · Codebase · Integration · Rules · Tasks · Validation", "Cheapest place to be wrong"),
    (GREEN,         "02  MANAGE CONTEXT",   "Right info, not all info",
     "Separate sessions · /prime · subagents · on-demand docs",    "65K-250K dumb zone threshold"),
    (b.TEAL,        "03  VERIFY THE WORK",  "Gate every output",
     "Auto-checks → Lint → Tests → [fail=fix+re-run] → Review",   "65% → 92% accuracy improvement"),
    (hx("3B82F6"),  "04  BUILD THE SYSTEM", "Every bug = permanent upgrade",
     "Bug → Rule → Doc → /Command → Skill  (staircase)",          "Floor keeps rising weekly"),
    (VIOLET,        "RALF  MULTI-SESSION",  "For large tasks: fresh context",
     "Planner → Implementer → Validator chain via handoff docs",   "Archon: open-source harness"),
]

rh = Inches(1.16)
for i, (col, skill, tagline, details, outcome) in enumerate(summary_rows):
    ry = Inches(1.1) + (rh + Inches(0.04)) * i
    d.rect(s16, M, ry, CW, rh, hx("0E1E34"), line=hx("1E3A5A"), radius=0.02)
    d.rect(s16, M, ry, Inches(0.06), rh, col, radius=0.01)
    # Skill name
    d.text(s16, skill, M + Inches(0.2), ry + Inches(0.1), Inches(2.6), Inches(0.34),
           size=12.5, color=col, bold=True, font=MONO)
    # Tagline
    d.text(s16, tagline, M + Inches(0.2), ry + Inches(0.48), Inches(2.6), Inches(0.28),
           size=11, color=hx("94A3B8"), italic=True)
    # Divider
    d.rect(s16, M + Inches(2.92), ry + Inches(0.22), Pt(1.5), rh - Inches(0.44), hx("1E3A5A"))
    # Details
    d.text(s16, details, M + Inches(3.06), ry + Inches(0.12), Inches(6.5), Inches(0.68),
           size=11, color=hx("CBD5E1"), ls=1.45, wrap=True, shrink=True)
    # Divider 2
    d.rect(s16, M + Inches(9.68), ry + Inches(0.22), Pt(1.5), rh - Inches(0.44), hx("1E3A5A"))
    # Outcome
    d.text(s16, outcome, M + Inches(9.82), ry + Inches(0.22), Inches(2.5), Inches(0.72),
           size=10.5, color=col, bold=True, wrap=True, shrink=True)

# Footer credits
d.rect(s16, M, Inches(7.06), CW, Inches(0.26), hx("0E1E34"), radius=0.01)
d.text(s16, "Source: Nate Herk × Cole · \"How to Build Effective Claude Code Agents in 2026\" · youtube.com/watch?v=RzLV8sfFdMM",
       M + Inches(0.1), Inches(7.08), CW - Inches(0.2), Inches(0.22),
       size=8.5, color=hx("475569"))
d.footer(s16, 18, TOTAL, dark=True)

# ════════════════════════════════════════════════════════════════════════════
# SAVE + VALIDATE
# ════════════════════════════════════════════════════════════════════════════
d.save(OUT)
print(f"\nDeck ready: {OUT}")
