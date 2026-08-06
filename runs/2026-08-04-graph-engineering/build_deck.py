#!/usr/bin/env python3
"""Branded PPTX builder for the graph-engineering video-to-deck run.
Kept in the run folder per delivery-gate convention so QA fixes are reproducible."""
import sys
from pathlib import Path

SKILL_DIR = Path.home() / ".claude/skills/branded-pptx-deck/scripts"
sys.path.insert(0, str(SKILL_DIR))
from pptxkit import Brand, Deck, PP_ALIGN, Inches, Pt  # noqa: E402

RUN = Path(__file__).parent
OUT = RUN / "graph-engineering-video-deck-draft.pptx"

b = Brand()
d = Deck(brand=b, footer="Designing AI Workflows That Can Be Trusted")

TOTAL = 14

def implication_panel(s, text, *, left, top, width, height, label="BUSINESS IMPLICATION"):
    d.rect(s, left, top, width, height, b.SOFT, radius=0.06)
    d.rect(s, left, top, Inches(0.06), height, b.TEAL)
    d.text(s, label, left + Inches(0.28), top + Inches(0.2), width - Inches(0.5), Inches(0.32),
           size=14, color=b.NAVY, bold=True)
    d.text(s, text, left + Inches(0.28), top + Inches(0.62), width - Inches(0.56), height - Inches(0.82),
           size=14, color=b.INK, ls=1.15, shrink=True)


def evidence_slide(page, title, image_path, implication, takeaway, *, mirror=False):
    s = d.slide(fill=b.WHITE)
    d.header(s, title)
    img_w = Inches(5.3)
    img_top = Inches(1.7)
    panel_width = d.CW - img_w - Inches(0.35)
    if mirror:
        panel_left = d.M
        img_left = d.M + panel_width + Inches(0.35)
    else:
        panel_left = d.M + img_w + Inches(0.35)
        img_left = d.M
    pic = d.picture_centered(s, image_path, top=img_top, width=img_w, max_bottom=Inches(4.75))
    pic.left = img_left
    implication_panel(s, implication, left=panel_left, top=img_top, width=panel_width, height=Inches(3.0))
    d.rect(s, d.M, Inches(4.95), d.CW, Inches(1.35), b.NAVY, radius=0.05)
    d.text(s, takeaway, d.M + Inches(0.35), Inches(5.15), d.CW - Inches(0.7), Inches(1.0),
           size=15, color=b.WHITE, bold=True, ls=1.2, anchor=1, shrink=True)
    d.footer(s, page, TOTAL)
    return s


# Slide 1 — cover
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
d.text(s, ["Designing AI Workflows", "That Can Be Trusted"], d.M, Inches(1.0), d.CW, Inches(2.0),
       size=44, color=b.WHITE, bold=True, ls=1.1)
d.rect(s, d.M, Inches(2.95), Inches(1.6), Inches(0.06), b.TEAL)
d.text(s, "The graph engineering pattern: jobs, arrows, and shared state — and when it earns its place",
       d.M, Inches(3.15), Inches(10.5), Inches(1.0), size=17, color=b.LIGHT_TEAL, ls=1.25)
d.footer(s, 1, TOTAL, dark=True)

# Slide 2 — executive summary (frame_0011)
evidence_slide(
    2,
    "One model, one pass — no way to check the work",
    RUN / "extracted/frame_0011-masked.png",
    "A single confident pass leaves no seam to check what evidence was used. Jobs, arrows, "
    "and shared state make the same work checkable at every step, not just at the end.",
    "Decision: run the six-condition test (slide 8) before scaling risky AI work — then "
    "start with a manual first rep, not a tooling purchase.",
)

# Slide 3 — native, hype-context
s = d.slide(fill=b.WHITE)
d.header(s, "The vocabulary is having a very contested moment")
stats = [("48 hrs", "from first post to three competing definitions"),
         ("3", "incompatible meanings of “graph” in circulation at once"),
         ("1", "widely shared founding study — confirmed fabricated")]
card_w = (d.CW - Inches(0.6)) / 3
for i, (num, cap) in enumerate(stats):
    left = d.M + i * (card_w + Inches(0.3))
    d.rect(s, left, Inches(1.8), card_w, Inches(2.1), b.SOFT, radius=0.08)
    d.text(s, num, left, Inches(2.0), card_w, Inches(1.0), size=48, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, cap, left + Inches(0.25), Inches(3.05), card_w - Inches(0.5), Inches(0.8),
           size=14, color=b.INK, align=PP_ALIGN.CENTER, ls=1.2)
d.rect(s, d.M, Inches(4.3), d.CW, Inches(1.5), b.NAVY, radius=0.05)
d.text(s, "The term is new and contested. The mechanics underneath it are not — treat the "
          "label with more skepticism than the pattern.",
       d.M + Inches(0.35), Inches(4.5), d.CW - Inches(0.7), Inches(1.1), size=16, color=b.WHITE,
       bold=True, ls=1.2, shrink=True)
d.text(s, "Source: independent industry reporting, July 2026 (see run sources)", d.M, Inches(6.15),
       Inches(8), Inches(0.35), size=10, color=b.MUTED, italic=True)
d.footer(s, 3, TOTAL)

# Slide 4 (frame_0010)
evidence_slide(
    4,
    "One active framing — not a settled progression",
    RUN / "extracted/frame_0010-masked.png",
    "Prompt engineering is about wording, context engineering about information, graph "
    "engineering about how the work is designed — three levers, not an agreed sequence.",
    "Take the mechanics (design the work, not just the prompt) without adopting the "
    "trend-cycle framing wholesale.",
    mirror=True,
)

# Slide 5 (frame_0015)
evidence_slide(
    5,
    "The vocabulary: jobs, arrows, and one shared record",
    RUN / "extracted/frame_0015-masked.png",
    "A job is one step with one owner and one output. An arrow says what has to happen "
    "before what. State is the shared record every job reads and writes. That's the entire "
    "vocabulary — nothing more exotic is required to start.",
    "This is the whole mental model. Everything else in this deck is this vocabulary "
    "applied to a real decision.",
)

# Slide 6 (frame_0013)
evidence_slide(
    6,
    "Same report format — different shape of work behind it",
    RUN / "extracted/frame_0013-masked.png",
    "A single chat and a structured graph can both hand back a report. Only one of them "
    "lets you see which claims were checked, by whom, before you trust the answer.",
    "Ask of any AI-produced recommendation: can I see the work behind it, or only the "
    "output?",
    mirror=True,
)

# Slide 7 (frame_0017)
evidence_slide(
    7,
    "Don't confuse a knowledge graph with an agent graph",
    RUN / "extracted/frame_0017-masked.png",
    "A knowledge graph maps what your data means — customers, products, relationships. "
    "An agent graph maps how work should move, get checked, and get approved. This deck is "
    "about the second one.",
    "Buying or building a knowledge graph does not give you a checkable AI workflow — "
    "they solve different problems.",
)

# Slide 8 (frame_0019)
evidence_slide(
    8,
    "The qualifying test: when a graph earns its place",
    RUN / "extracted/frame_0019-masked.png",
    "Multiple steps, multiple sources, parallel paths, real checks, real risk, required "
    "approvals — if none of these are true for a workflow, a graph is overhead, not "
    "sophistication.",
    "Run every candidate workflow through this test before reaching for any framework. "
    "Most AI work still doesn't need one.",
    mirror=True,
)

# Slide 9 (frame_0021)
evidence_slide(
    9,
    "Worked example: AI bookkeeping for Shopify?",
    RUN / "extracted/frame_0021-masked.png",
    "Three parallel researchers cover customer pain, competitors, and distribution. A "
    "skeptic attacks the findings. A merge step turns survivors into a one-page "
    "recommendation. A human picks the next move.",
    "The messy one-shot chat becomes a workflow you can actually inspect, challenge, and "
    "reuse on the next decision.",
)

# Slide 10 (frame_0023)
evidence_slide(
    10,
    "The pattern underneath: the Diamond",
    RUN / "extracted/frame_0023-masked.png",
    "Planner fans out to parallel researchers, a skeptic checks their findings, then merge "
    "and human approval close the loop. This is the one shape worth learning first — "
    "every other pattern is a variation on it.",
    "Learn this one diagram before anything else. It generalizes to support, content, and "
    "code work (next slide).",
    mirror=True,
)

# Slide 11 (frame_0027)
evidence_slide(
    11,
    "Three ready-made pipelines you can steal",
    RUN / "extracted/frame_0027-masked.png",
    "Support, content, and code workflows all follow the same rule: the checker is never "
    "the same role as the writer. That one constraint is what makes each pipeline "
    "trustworthy enough to run unattended.",
    "Pick the lane closest to your own work and copy the structure — not the specific "
    "steps — into your first graph.",
)

# Slide 12 (frame_0025)
evidence_slide(
    12,
    "Three levels of implementation — start manual",
    RUN / "extracted/frame_0025-masked.png",
    "Manual whiteboard lanes prove the shape works with no code at all. File trails make "
    "the run reusable. Real orchestration tooling only pays off after that — earn the "
    "tooling, don't start with it.",
    "Do not buy or install anything before finishing Level 1 by hand at least once.",
    mirror=True,
)

# Slide 13 — native comparison table
s = d.slide(fill=b.WHITE)
d.header(s, "Where the named tools actually fit")
rows = [
    ("LangGraph", "Stateful multi-agent logic, human-approval gates", "Needs engineering capacity"),
    ("AutoGen GraphFlow", "Parallel fan-out, conditional/looping flows", "Code-first, Python"),
    ("n8n", "Self-hostable, AI-native automation", "Needs comfort with JSON/APIs"),
    ("Make.com", "Fully-hosted, non-technical automation", "Billing punishes looping agents"),
]
top = Inches(1.85)
col_w = [Inches(2.6), Inches(5.3), Inches(4.1)]
headers = ["Tool", "Best for", "Watch for"]
x = d.M
for w, htext in zip(col_w, headers):
    d.text(s, htext, x, top, w - Inches(0.15), Inches(0.4), size=14, color=b.NAVY, bold=True)
    x += w
d.rect(s, d.M, top + Inches(0.42), d.CW, Pt(1.5), b.GRID)
row_top = top + Inches(0.58)
row_h = Inches(0.82)
for name, best, watch in rows:
    d.rect(s, d.M, row_top, d.CW, row_h - Inches(0.1), b.SOFT, radius=0.05)
    x = d.M + Inches(0.2)
    d.text(s, name, x, row_top, col_w[0] - Inches(0.3), row_h - Inches(0.1), size=14, color=b.NAVY, bold=True, ls=1.1, anchor=1, shrink=True)
    x += col_w[0]
    d.text(s, best, x, row_top, col_w[1] - Inches(0.3), row_h - Inches(0.1), size=14, color=b.INK, ls=1.1, anchor=1, shrink=True)
    x += col_w[1]
    d.text(s, watch, x, row_top, col_w[2] - Inches(0.3), row_h - Inches(0.1), size=14, color=b.MUTED, ls=1.1, anchor=1, shrink=True)
    row_top += row_h
d.text(s, "Most teams should start below all four — see “Three levels of implementation.” "
          "Source: industry reporting, July 2026.",
       d.M, row_top + Inches(0.12), d.CW, Inches(0.35), size=10, color=b.MUTED, italic=True)
d.footer(s, 13, TOTAL)

# Slide 14 — recommendation / ask
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
d.text(s, "Next move: draw one graph this week", d.M, Inches(1.3), d.CW, Inches(1.0),
       size=34, color=b.WHITE, bold=True)
steps = [
    "Pick one workflow you already run.",
    "Draw the jobs and the arrows between them.",
    "Delete the fake sequential waiting — run independent jobs in parallel.",
    "Add one skeptic step before anything ships.",
    "Run it once, by hand, before automating anything.",
]
top = Inches(2.7)
for i, step in enumerate(steps):
    d.rect(s, d.M, top, Inches(0.5), Inches(0.5), b.TEAL, radius=0.5)
    d.text(s, str(i + 1), d.M, top + Inches(0.04), Inches(0.5), Inches(0.42), size=18, color=b.NAVY,
           bold=True, align=PP_ALIGN.CENTER)
    d.text(s, step, d.M + Inches(0.7), top + Inches(0.03), Inches(10.5), Inches(0.5), size=17,
           color=b.WHITE, ls=1.15)
    top += Inches(0.72)
d.footer(s, 14, TOTAL, dark=True)

d.save(OUT)
print("done")
