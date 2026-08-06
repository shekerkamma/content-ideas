#!/usr/bin/env python3
"""Reproducible branded builder for the Impeccable anti-slop deck."""

import sys
from pathlib import Path

SKILL = Path("/home/sheke/content-ideas/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(SKILL))
from pptxkit import Brand, Deck, PP_ALIGN, Inches, Pt  # noqa: E402

RUN = Path(__file__).resolve().parent
OUT = RUN / "impeccable-ai-slop-deck-draft.pptx"
ASSETS = RUN / "assets"
b = Brand()
d = Deck(brand=b, footer="Impeccable × Client-ready presentations")
TOTAL = 12

CORAL = b.CORAL


def rule(s, y, color=None):
    d.rect(s, d.M, y, d.CW, Pt(1.5), color or b.TEAL)


def evidence(page, title, image_name, annotation, decision, mirror=False):
    s = d.slide(fill=b.WHITE)
    d.header(s, title)
    image_left = Inches(6.75) if mirror else d.M
    text_left = d.M if mirror else Inches(7.05)
    pic = d.picture_centered(s, ASSETS / image_name, top=Inches(1.58), width=Inches(5.75), max_bottom=Inches(5.05))
    pic.left = image_left
    d.text(s, "OBSERVATION", text_left, Inches(1.72), Inches(5.0), Inches(0.32), size=11, color=b.TEAL, bold=True)
    d.text(s, annotation, text_left, Inches(2.12), Inches(5.0), Inches(1.8), size=22, color=b.NAVY, bold=True, ls=1.12, shrink=True)
    d.rect(s, text_left, Inches(4.3), Inches(5.0), Inches(1.25), b.SOFT, radius=0.03)
    d.text(s, decision, text_left + Inches(0.24), Inches(4.48), Inches(4.5), Inches(0.9), size=14, color=b.INK, ls=1.14, shrink=True)
    d.text(s, "Captured from the supplied demonstration", image_left, Inches(5.25), Inches(5.75), Inches(0.3), size=9, color=b.MUTED, italic=True)
    d.footer(s, page, TOTAL)


# 1 — cover
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.text(s, "CAN IMPECCABLE", d.M, Inches(0.95), d.CW, Inches(0.42), size=15, color=b.TEAL, bold=True)
d.text(s, ["take the AI slop", "out of slides?"], d.M, Inches(1.42), Inches(10.9), Inches(2.25), size=46, color=b.WHITE, bold=True, ls=1.02)
d.rect(s, Inches(11.45), Inches(3.15), Inches(0.58), Inches(0.58), CORAL, radius=0.0)
rule(s, Inches(4.18), b.TEAL)
d.text(s, "A design-direction experiment for client-ready presentations", d.M, Inches(4.42), Inches(9.2), Inches(0.78), size=17, color=b.LIGHT_TEAL, shrink=True)
d.text(s, "DECISION BRIEF  ·  AUGUST 2026", d.M, Inches(6.3), Inches(5), Inches(0.35), size=10, color=b.WHITE, bold=True)
d.footer(s, 1, TOTAL, dark=True)

# 2 — answer
s = d.slide(fill=b.WHITE)
d.header(s, "Impeccable works—but only as a workflow")
d.text(s, "YES", d.M, Inches(1.55), Inches(3.0), Inches(1.35), size=62, color=b.TEAL, bold=True)
d.text(s, "Impeccable removes recognizable defaults by expanding the option set and forcing a committed design direction.", Inches(4.15), Inches(1.68), Inches(8.0), Inches(1.25), size=23, color=b.NAVY, bold=True, ls=1.1, shrink=True)
conditions = [("01", "Choose a world", "Commit before composing."), ("02", "Compare alternatives", "Select visually, not verbally."), ("03", "Review the finish", "Detect patterns, then QA delivery.")]
for i, (num, head, body) in enumerate(conditions):
    x = d.M + i * Inches(4.05)
    d.text(s, num, x, Inches(3.45), Inches(0.6), Inches(0.42), size=12, color=b.TEAL, bold=True)
    rule(s, Inches(3.92), CORAL if i == 1 else b.TEAL)
    d.text(s, head, x, Inches(4.15), Inches(3.65), Inches(0.55), size=19, color=b.NAVY, bold=True)
    d.text(s, body, x, Inches(4.78), Inches(3.65), Inches(0.7), size=14, color=b.INK)
d.rect(s, d.M, Inches(5.72), d.CW, Inches(0.72), b.NAVY, radius=0.02)
d.text(s, "It cannot repair weak evidence, a vague narrative, or missing PowerPoint QA.", d.M + Inches(0.28), Inches(5.9), d.CW - Inches(0.56), Inches(0.38), size=15, color=b.WHITE, bold=True)
d.footer(s, 2, TOTAL)

evidence(3, "The demonstration attacks sameness", "evidence-13.jpg", "The product is framed as a system of commands and review behaviors—not a library of decorative slide skins.", "Implication: adapt the method to presentations; do not simply copy a website aesthetic.")
evidence(4, "A committed world breaks the default", "evidence-09.jpg", "A broad visual-world library gives the model a concrete grammar before it starts composing.", "Decision: add visual-world selection after evidence capture and before the slide plan.", mirror=True)
evidence(5, "Live comparison changes the task", "evidence-31.jpg", "Seeing alternatives side by side changes the task from accepting an answer to choosing a direction.", "Decision: require at least two materially different directions for high-stakes decks.")
evidence(6, "Outside references add specificity", "evidence-43.jpg", "A reference library supplies proportion, type, rhythm, and interaction cues that prose alone underspecifies.", "Guardrail: borrow visual grammar; never copy gallery layouts, artwork, or brand assets.", mirror=True)

# 7 — process
s = d.slide(fill=b.NAVY)
d.text(s, "The anti-slop loop has five deliberate gates", d.M, Inches(0.72), d.CW, Inches(0.72), size=30, color=b.WHITE, bold=True)
stages = [("1", "TRUTH", "Capture evidence"), ("2", "WORLD", "Commit direction"), ("3", "RANGE", "Compare options"), ("4", "DETECT", "Remove patterns"), ("5", "SHIP", "Render + QA")]
for i, (num, head, body) in enumerate(stages):
    x = d.M + i * Inches(2.42)
    d.rect(s, x, Inches(2.15), Inches(1.05), Inches(1.05), b.TEAL if i < 4 else CORAL, radius=0.5)
    d.text(s, num, x, Inches(2.33), Inches(1.05), Inches(0.6), size=25, color=b.NAVY if i < 4 else b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    if i < 4:
        d.rect(s, x + Inches(1.1), Inches(2.66), Inches(1.22), Pt(2), b.LIGHT_TEAL)
    d.text(s, head, x, Inches(3.48), Inches(2.15), Inches(0.4), size=13, color=b.TEAL, bold=True)
    d.text(s, body, x, Inches(3.94), Inches(2.15), Inches(0.85), size=16, color=b.WHITE, bold=True, ls=1.12)
d.text(s, "Remove any gate and the workflow can still produce polished-looking slop.", d.M, Inches(5.65), d.CW, Inches(0.55), size=18, color=b.LIGHT_TEAL, bold=True)
d.footer(s, 7, TOTAL, dark=True)

# 8 — scorecard
s = d.slide(fill=b.WHITE)
d.header(s, "Explicit criteria make slop detectable")
checks = ["Committed visual world", "Non-default hierarchy", "No gradient cliché", "No nested-card maze", "No pill/icon confetti", "Authentic evidence", "Varied archetypes", "Readable density", "Clear decision"]
for i, check in enumerate(checks):
    col, row = i % 3, i // 3
    x, y = d.M + col * Inches(4.05), Inches(1.72) + row * Inches(1.4)
    d.text(s, f"0{i+1}", x, y, Inches(0.45), Inches(0.35), size=10, color=b.TEAL, bold=True)
    d.rect(s, x + Inches(0.55), y, Inches(0.42), Inches(0.42), b.TEAL, radius=0.5)
    d.text(s, "✓", x + Inches(0.55), y + Inches(0.02), Inches(0.42), Inches(0.32), size=13, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, check, x + Inches(1.12), y - Inches(0.02), Inches(2.75), Inches(0.55), size=15, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, x, y + Inches(0.62), Inches(3.65), Pt(1), b.GRID)
d.rect(s, d.M, Inches(5.92), d.CW, Inches(0.58), CORAL, radius=0.02)
d.text(s, "Pass/fail criteria turn taste from a vague preference into a delivery gate.", d.M + Inches(0.25), Inches(6.06), d.CW - Inches(0.5), Inches(0.32), size=14, color=b.WHITE, bold=True)
d.footer(s, 8, TOTAL)

# 9 — limits
s = d.slide(fill=b.WHITE)
d.header(s, "Four failures remain outside Impeccable’s reach")
limits = [("01", "Bad evidence", "Beautifully presented uncertainty is still uncertainty."), ("02", "Weak argument", "A visual world cannot create a decision narrative."), ("03", "Blind copying", "Reference sites are inputs, not reusable templates."), ("04", "Broken delivery", "Overflow, collisions, and missing fonts still need QA.")]
for i, (num, head, body) in enumerate(limits):
    y = Inches(1.62) + i * Inches(1.18)
    d.text(s, num, d.M, y, Inches(0.65), Inches(0.4), size=12, color=CORAL, bold=True)
    d.text(s, head, Inches(2.0), y - Inches(0.03), Inches(3.0), Inches(0.48), size=19, color=b.NAVY, bold=True)
    d.text(s, body, Inches(5.15), y, Inches(7.0), Inches(0.48), size=15, color=b.INK, shrink=True)
    d.rect(s, d.M, y + Inches(0.66), d.CW, Pt(1), b.GRID)
d.text(s, "Design discipline complements content discipline; it never substitutes for it.", d.M, Inches(6.25), d.CW, Inches(0.4), size=16, color=b.TEAL, bold=True)
d.footer(s, 9, TOTAL)

evidence(10, "A design record makes the chosen world reusable", "evidence-38.jpg", "Capturing design decisions converts a one-off result into a system that can survive the next slide or deck.", "Decision: every material deck keeps its brief, design contract, slide plan, visual spec, and QA record.")
evidence(11, "The improvement is range plus control", "evidence-46.jpg", "The strongest result comes after reference, iteration, and finish review—not from the first generated composition.", "Measure success by fewer recognizable defaults and better decision clarity, not visual novelty.", mirror=True)

# 12 — recommendation
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, Inches(0.18), d.H, CORAL)
d.text(s, "RECOMMENDATION", d.M, Inches(0.95), d.CW, Inches(0.35), size=13, color=b.TEAL, bold=True)
d.text(s, "Make visual-world selection a standard deck stage.", d.M, Inches(1.48), Inches(10.8), Inches(1.4), size=38, color=b.WHITE, bold=True, ls=1.06)
d.text(s, "WATCH  →  TRUTH  →  WORLD  →  BUILD  →  REVIEW  →  QA", d.M, Inches(3.35), d.CW, Inches(0.55), size=17, color=b.LIGHT_TEAL, bold=True)
rule(s, Inches(4.15), b.TEAL)
d.text(s, "Start now", d.M, Inches(4.48), Inches(2.4), Inches(0.45), size=14, color=b.TEAL, bold=True)
d.text(s, "Use the scorecard on every material deck. Reject any direction that cannot name its visual world.", Inches(3.15), Inches(4.34), Inches(8.7), Inches(1.28), size=19, color=b.WHITE, bold=True, ls=1.1, shrink=True)
d.footer(s, 12, TOTAL, dark=True)

d.save(OUT)
print(OUT)
