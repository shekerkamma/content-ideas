#!/usr/bin/env python3
"""Build the Decision Flight Recorder treatment from Watch evidence and written content."""
from pathlib import Path
import sys

sys.path.insert(0, "/home/sheke/content-ideas/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Brand, Inches, Pt, PP_ALIGN  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402

RUN = Path(__file__).resolve().parent
ASSETS = RUN / "assets"
OUT = RUN / "impeccable-decision-flight-recorder-draft.pptx"
TEMPLATE = Path("/home/sheke/content-ideas/skills/branded-pptx-deck/resources/template.pptx")


def c(value): return RGBColor.from_string(value)


NAVY, PANEL, WHITE = c("0B1020"), c("151C32"), c("F4F7FF")
LIME, CYAN, CORAL, VIOLET = c("D8FF3E"), c("46E6FF"), c("FF5A5F"), c("9B7CFF")
MUTED, RULE, INK = c("A8B0C7"), c("313A58"), c("111629")

d = Deck(brand=Brand(), footer="Impeccable 4.0 · adoption decision")
d.prs = Presentation(str(TEMPLATE))
d.W, d.H = Inches(13.333), Inches(7.5)
d.prs.slide_width, d.prs.slide_height = d.W, d.H
d._wipe()
TOTAL = 14


def rect(s, x, y, w, h, fill, radius=0): return d.rect(s, x, y, w, h, fill, radius=radius)


def txt(s, text, x, y, w, h, size=18, color=WHITE, bold=False, align=None, shrink=True, ls=1.1):
    return d.text(s, text, x, y, w, h, size=size, color=color, bold=bold, align=align, shrink=shrink, ls=ls)


def chrome(s, page, section, title, status="ANALYST MODEL"):
    txt(s, section.upper(), Inches(.55), Inches(.3), Inches(2.4), Inches(.24), 10, CYAN, True)
    txt(s, title, Inches(.55), Inches(.66), Inches(11.9), Inches(.7), 28, WHITE, True)
    rect(s, Inches(.55), Inches(1.4), Inches(12.22), Pt(1), RULE)
    txt(s, status, Inches(.55), Inches(7.05), Inches(3.3), Inches(.2), 8, MUTED, True)
    txt(s, f"{page:02d}  /  {TOTAL:02d}", Inches(11.72), Inches(7.03), Inches(1.0), Inches(.22), 9, MUTED, True, PP_ALIGN.RIGHT)


def tag(s, label, x, y, color):
    rect(s, x, y, Inches(1.35), Inches(.34), color, .12)
    txt(s, label, x, y + Inches(.08), Inches(1.35), Inches(.18), 9, INK, True, PP_ALIGN.CENTER)


def signal(s, x1, y, widths, colors):
    x = x1
    for w, color in zip(widths, colors):
        rect(s, x, y, Inches(w), Pt(4), color)
        x += Inches(w + .08)


# 1 — verdict
s = d.slide(fill=NAVY)
rect(s, 0, 0, Inches(.18), d.H, LIME)
txt(s, "DECISION / 01", Inches(.72), Inches(.62), Inches(2.8), Inches(.3), 11, CYAN, True)
txt(s, "PILOT THE\nDECISION SYSTEM.", Inches(.72), Inches(1.2), Inches(8.5), Inches(2.0), 48, WHITE, True, ls=.95)
txt(s, "NOT AUTONOMOUS TASTE.", Inches(.72), Inches(3.4), Inches(8.4), Inches(.55), 25, LIME, True)
txt(s, "The walkthrough shows a stronger way to choose direction, compare alternatives, and recover from a wrong visual grammar. It does not prove faster delivery, higher usability, or business lift.", Inches(.75), Inches(4.42), Inches(7.7), Inches(1.25), 18, MUTED, False, ls=1.25)
rect(s, Inches(9.15), Inches(.78), Inches(3.42), Inches(5.7), PANEL)
txt(s, "AUTHORIZATION", Inches(9.48), Inches(1.15), Inches(2.8), Inches(.3), 10, CORAL, True)
txt(s, "ONE", Inches(9.45), Inches(1.68), Inches(2.5), Inches(.85), 43, WHITE, True)
txt(s, "MATCHED-TASK\nPILOT", Inches(9.48), Inches(2.58), Inches(2.6), Inches(.9), 22, LIME, True)
signal(s, Inches(9.48), Inches(4.15), [1.7, .55, .35], [CYAN, VIOLET, CORAL])
txt(s, "Hold the brief, proof, references, model budget, and acceptance criteria constant.", Inches(9.48), Inches(4.62), Inches(2.55), Inches(1.0), 14, WHITE, True)
txt(s, "Observed demonstration + bounded analyst recommendation", Inches(.75), Inches(6.95), Inches(5.8), Inches(.22), 8, MUTED, True)

# 2 — executive readout
s = d.slide(fill=NAVY); chrome(s, 2, "Executive readout", "Three demonstrated mechanisms justify one controlled test")
rows = [
    ("01", "WORLD SELECTION", "Macro direction becomes visible before implementation variants.", CYAN, "OBSERVED"),
    ("02", "BOUNDED COMPARISON", "Local alternatives can be generated, tuned, and accepted side by side.", VIOLET, "OBSERVED"),
    ("03", "REFERENCE RESET", "A wrong visual grammar can trigger a deliberate macro departure.", CORAL, "OBSERVED"),
]
for i, (num, label, body, color, status) in enumerate(rows):
    y = Inches(1.72 + i * 1.35)
    txt(s, num, Inches(.65), y, Inches(.55), Inches(.48), 18, color, True)
    txt(s, label, Inches(1.38), y, Inches(2.7), Inches(.32), 12, WHITE, True)
    txt(s, body, Inches(4.0), y - Inches(.04), Inches(5.65), Inches(.58), 16, WHITE, True)
    tag(s, status, Inches(10.65), y - Inches(.02), color)
    rect(s, Inches(1.38), y + Inches(.68), Inches(10.62), Pt(1), RULE)
rect(s, Inches(.65), Inches(5.82), Inches(12.0), Inches(.78), LIME)
txt(s, "DECISION", Inches(.92), Inches(6.04), Inches(1.25), Inches(.28), 11, INK, True)
txt(s, "Test whether the workflow reduces major direction resets without quality or control regressions.", Inches(2.25), Inches(5.98), Inches(9.8), Inches(.42), 18, INK, True)

# 3 — hidden cost
s = d.slide(fill=WHITE); chrome(s, 3, "Problem", "A generic first draft moves the expensive decision downstream")
stages = [("PROMPT", "Fast", CYAN), ("GENERIC PAGE", "Plausible", VIOLET), ("DIRECTION DEBATE", "Late", CORAL), ("REBUILD", "Expensive", INK)]
for i, (label, sub, color) in enumerate(stages):
    x = Inches(.65 + i * 3.02)
    h = Inches(1.15 + i * .62)
    rect(s, x, Inches(5.55)-h, Inches(2.5), h, color)
    txt(s, label, x + Inches(.18), Inches(5.0)-h, Inches(2.15), Inches(.32), 12, WHITE if i else INK, True)
    txt(s, sub, x + Inches(.18), Inches(5.33)-h, Inches(2.15), Inches(.32), 15, WHITE if i else INK, True)
    if i < 3: txt(s, "→", x + Inches(2.55), Inches(4.9), Inches(.4), Inches(.4), 20, CORAL, True, PP_ALIGN.CENTER)
txt(s, "The workflow matters only if it makes macro direction explicit before teams accumulate implementation debt.", Inches(.7), Inches(6.0), Inches(11.8), Inches(.55), 20, INK, True)

# 4 — Worlds proof
s = d.slide(fill=NAVY); chrome(s, 4, "Proof / world selection", "Worlds turns ‘make it better’ into a visible macro decision", "OBSERVED DEMONSTRATION")
pic = d.picture_centered(s, ASSETS / "worlds.jpg", top=Inches(1.72), width=Inches(8.0), max_bottom=Inches(6.7)); pic.left = Inches(.55)
rect(s, Inches(8.88), Inches(1.72), Inches(3.88), Inches(4.98), PANEL)
tag(s, "WHAT CHANGED", Inches(9.18), Inches(2.08), CYAN)
txt(s, "The visual grammar becomes a named choice before local variants are built.", Inches(9.18), Inches(2.72), Inches(3.0), Inches(1.35), 21, WHITE, True)
txt(s, "Management implication", Inches(9.18), Inches(4.52), Inches(2.2), Inches(.28), 10, CORAL, True)
txt(s, "Assign a direction owner and record why the selected world fits the audience and task.", Inches(9.18), Inches(4.96), Inches(3.0), Inches(1.0), 15, MUTED, True)

# 5 — choice architecture
s = d.slide(fill=NAVY); chrome(s, 5, "Mechanism", "Value comes from commitment—not from an endless menu")
track = [("DIVERGE", "Expose genuinely different worlds", CYAN), ("COMMIT", "Name the owner and exit rule", LIME), ("CONVERGE", "Compare bounded local variants", VIOLET), ("RELEASE", "Challenge, approve, record", CORAL)]
for i, (lab, body, color) in enumerate(track):
    x = Inches(.6 + i * 3.06)
    rect(s, x, Inches(2.05), Inches(2.48), Inches(2.58), PANEL)
    rect(s, x, Inches(2.05), Inches(2.48), Inches(.13), color)
    txt(s, lab, x + Inches(.2), Inches(2.53), Inches(2.05), Inches(.36), 17, color, True)
    txt(s, body, x + Inches(.2), Inches(3.12), Inches(2.0), Inches(.95), 16, WHITE, True)
    if i < 3: txt(s, "→", x + Inches(2.56), Inches(3.0), Inches(.42), Inches(.5), 24, MUTED, True, PP_ALIGN.CENTER)
signal(s, Inches(.65), Inches(5.4), [2.2, 3.2, 2.0, 3.5], [CYAN, LIME, VIOLET, CORAL])
txt(s, "Divergence earns its keep only when the process can stop, decide, and move forward.", Inches(.65), Inches(5.82), Inches(10.8), Inches(.5), 20, WHITE, True)

# 6 — trade-off
s = d.slide(fill=WHITE); chrome(s, 6, "Trade-off", "A higher creative ceiling shifts more risk to the operator")
rect(s, Inches(.65), Inches(1.78), Inches(5.62), Inches(4.75), c("E8ECF6"))
rect(s, Inches(6.52), Inches(1.78), Inches(6.24), Inches(4.75), NAVY)
txt(s, "NARROW STYLE SKILL", Inches(1.0), Inches(2.15), Inches(4.6), Inches(.3), 11, VIOLET, True)
txt(s, "HIGHER FLOOR", Inches(1.0), Inches(2.72), Inches(4.7), Inches(.55), 28, INK, True)
txt(s, "Predictable novelty\nNarrower aesthetic range\nLower judgment burden", Inches(1.0), Inches(3.6), Inches(4.5), Inches(1.4), 19, INK, True, ls=1.4)
txt(s, "IMPECCABLE", Inches(6.92), Inches(2.15), Inches(4.5), Inches(.3), 11, LIME, True)
txt(s, "HIGHER CEILING", Inches(6.92), Inches(2.72), Inches(4.9), Inches(.55), 28, WHITE, True)
txt(s, "Broader differentiation\nGreater operator variance\nHigher governance need", Inches(6.92), Inches(3.6), Inches(4.7), Inches(1.4), 19, WHITE, True, ls=1.4)
txt(s, "Use the conventional workflow when evidence is weak, the surface is standardized, or review capacity is limited.", Inches(.75), Inches(6.1), Inches(11.8), Inches(.48), 17, CORAL, True)

# 7 — route by altitude
s = d.slide(fill=NAVY); chrome(s, 7, "Routing rule", "Change radius—not tool preference—should route the work")
txt(s, "DIRECTION CONFIDENCE", Inches(4.5), Inches(1.7), Inches(4.3), Inches(.28), 11, MUTED, True, PP_ALIGN.CENTER)
txt(s, "LOW", Inches(3.15), Inches(2.0), Inches(2.2), Inches(.25), 10, CORAL, True, PP_ALIGN.CENTER)
txt(s, "HIGH", Inches(8.15), Inches(2.0), Inches(2.2), Inches(.25), 10, LIME, True, PP_ALIGN.CENTER)
cells = [(Inches(2.1), Inches(2.4), "REFERENCE RESET", "Reopen visual grammar", CORAL), (Inches(7.0), Inches(2.4), "TERMINAL", "Change structure", CYAN), (Inches(2.1), Inches(4.55), "STOP POLISHING", "Clarify direction", VIOLET), (Inches(7.0), Inches(4.55), "LIVE MODE", "Compare local variants", LIME)]
txt(s, "LARGE\nCHANGE", Inches(.55), Inches(2.8), Inches(1.2), Inches(.65), 11, MUTED, True, PP_ALIGN.CENTER)
txt(s, "SMALL\nCHANGE", Inches(.55), Inches(4.95), Inches(1.2), Inches(.65), 11, MUTED, True, PP_ALIGN.CENTER)
for x, y, lab, body, color in cells:
    rect(s, x, y, Inches(4.1), Inches(1.55), PANEL)
    rect(s, x, y, Inches(.14), Inches(1.55), color)
    txt(s, lab, x + Inches(.32), y + Inches(.28), Inches(3.45), Inches(.35), 16, color, True)
    txt(s, body, x + Inches(.32), y + Inches(.82), Inches(3.45), Inches(.35), 14, WHITE, True)

# 8 — Live proof
s = d.slide(fill=NAVY); chrome(s, 8, "Proof / local comparison", "Live Mode compresses a bounded compare–tune–accept loop", "OBSERVED DEMONSTRATION")
rect(s, Inches(.55), Inches(1.72), Inches(3.6), Inches(4.98), PANEL)
tag(s, "BOUNDARY", Inches(.88), Inches(2.08), VIOLET)
txt(s, "Use Live only after the macro direction is accepted.", Inches(.88), Inches(2.72), Inches(2.85), Inches(1.15), 22, WHITE, True)
txt(s, "Detail wrong → Live\nStructure wrong → terminal\nDirection wrong → reference reset", Inches(.88), Inches(4.2), Inches(2.9), Inches(1.35), 15, MUTED, True, ls=1.4)
pic = d.picture_centered(s, ASSETS / "live-comparison.jpg", top=Inches(1.72), width=Inches(8.25), max_bottom=Inches(6.7)); pic.left = Inches(4.48)

# 9 — reference proof
s = d.slide(fill=NAVY); chrome(s, 9, "Proof / direction reset", "A wrong visual grammar requires a reference reset—not more polish", "OBSERVED DEMONSTRATION")
pic = d.picture_centered(s, ASSETS / "references.jpg", top=Inches(1.72), width=Inches(8.3), max_bottom=Inches(6.7)); pic.left = Inches(.55)
rect(s, Inches(9.18), Inches(1.72), Inches(3.58), Inches(4.98), PANEL)
tag(s, "ESCALATION", Inches(9.5), Inches(2.08), CORAL)
txt(s, "References reopen the macro decision when incremental refinement stalls.", Inches(9.5), Inches(2.72), Inches(2.8), Inches(1.35), 21, WHITE, True)
txt(s, "Control", Inches(9.5), Inches(4.55), Inches(1.2), Inches(.25), 10, CYAN, True)
txt(s, "Record provenance and the specific design grammar being borrowed.", Inches(9.5), Inches(4.95), Inches(2.8), Inches(1.0), 15, MUTED, True)

# 10 — judgment allocation
s = d.slide(fill=WHITE); chrome(s, 10, "Operating model", "Humans own four irreversible decisions")
cols = [("FRAME TRUTH", "Audience, evidence, constraints", "Structure the brief"), ("COMMIT DIRECTION", "Visual grammar and rationale", "Expand options"), ("RESOLVE TRADE-OFFS", "Competing priorities", "Generate + compare"), ("APPROVE RELEASE", "Independent fresh-context check", "Detect + record exceptions")]
for i, (head, human, system) in enumerate(cols):
    x = Inches(.55 + i * 3.05)
    rect(s, x, Inches(1.78), Inches(2.72), Inches(.82), NAVY)
    txt(s, head, x + Inches(.18), Inches(2.03), Inches(2.35), Inches(.35), 12, WHITE, True, PP_ALIGN.CENTER)
    txt(s, "HUMAN OWNS", x + Inches(.15), Inches(2.95), Inches(2.4), Inches(.28), 10, CORAL, True)
    txt(s, human, x + Inches(.15), Inches(3.38), Inches(2.38), Inches(.8), 17, INK, True)
    rect(s, x, Inches(4.38), Inches(2.72), Pt(2), RULE)
    txt(s, "SYSTEM SUPPORTS", x + Inches(.15), Inches(4.72), Inches(2.4), Inches(.28), 10, c("248A73"), True)
    txt(s, system, x + Inches(.15), Inches(5.15), Inches(2.35), Inches(.7), 16, c("175B4D"), True)
rect(s, Inches(.55), Inches(6.3), Inches(12.2), Inches(.45), LIME)
txt(s, "AUTOMATE REVERSIBLE WORK. REQUIRE A FRESH-CONTEXT HUMAN CHECK BEFORE RELEASE.", Inches(.75), Inches(6.41), Inches(11.8), Inches(.24), 12, INK, True, PP_ALIGN.CENTER)

# 11 — memory
s = d.slide(fill=NAVY); chrome(s, 11, "Organizational memory", "Accepted decisions matter only when they constrain the next cycle")
nodes = [("CHOSEN\nDECISIONS", CYAN), ("DESIGN\nRECORD", LIME), ("FUTURE\nCONSTRAINTS", VIOLET), ("DETECT +\nOVERRIDE", CORAL)]
for i, (label, color) in enumerate(nodes):
    x = Inches(.62 + i * 3.05)
    rect(s, x, Inches(2.28), Inches(2.35), Inches(1.45), PANEL)
    rect(s, x, Inches(2.28), Inches(2.35), Inches(.12), color)
    txt(s, label, x, Inches(2.72), Inches(2.35), Inches(.55), 17, color, True, PP_ALIGN.CENTER)
    if i < 3: txt(s, "→", x + Inches(2.5), Inches(2.72), Inches(.35), Inches(.4), 22, MUTED, True, PP_ALIGN.CENTER)
signal(s, Inches(.65), Inches(4.55), [1.2, 1.8, .6, 2.7, .5, 3.0], [CYAN, CYAN, LIME, VIOLET, CORAL, VIOLET])
txt(s, "Benefit", Inches(.65), Inches(5.05), Inches(1.2), Inches(.28), 10, LIME, True)
txt(s, "Less reinvention and lower variance across future work.", Inches(1.85), Inches(5.0), Inches(4.2), Inches(.42), 17, WHITE, True)
txt(s, "Risk", Inches(6.5), Inches(5.05), Inches(.55), Inches(.28), 10, CORAL, True)
txt(s, "Stale taste becomes an invisible default. Version the record and permit explicit resets.", Inches(7.25), Inches(5.0), Inches(5.0), Inches(.65), 17, WHITE, True)

# 12 — maturity boundary
s = d.slide(fill=WHITE); chrome(s, 12, "Evidence boundary", "The demo shows structured convergence—not measured optimization")
levels = [("0", "AD HOC", MUTED), ("1", "GUIDED", CYAN), ("2", "STRUCTURED", LIME), ("3", "CONTROLLED", VIOLET), ("4", "MEASURED", CORAL), ("5", "OUTCOME", INK)]
for i, (n, label, color) in enumerate(levels):
    x = Inches(.55 + i * 2.05)
    rect(s, x, Inches(2.15), Inches(1.72), Inches(2.3), color)
    txt(s, n, x + Inches(.15), Inches(2.38), Inches(.35), Inches(.34), 17, WHITE if i != 2 else INK, True)
    txt(s, label, x, Inches(3.25), Inches(1.72), Inches(.32), 11, WHITE if i != 2 else INK, True, PP_ALIGN.CENTER)
rect(s, Inches(.55), Inches(4.8), Inches(7.98), Inches(.42), LIME)
txt(s, "DEMONSTRATED: direction structure + elements of control", Inches(.75), Inches(4.91), Inches(7.5), Inches(.22), 12, INK, True)
rect(s, Inches(8.53), Inches(4.8), Inches(4.22), Inches(.42), CORAL)
txt(s, "UNPROVEN: productivity + outcomes", Inches(8.65), Inches(4.91), Inches(3.9), Inches(.22), 11, WHITE, True, PP_ALIGN.CENTER)
txt(s, "Treat speed, usability, quality, and business impact as pilot hypotheses—not demonstrated benefits.", Inches(.65), Inches(5.78), Inches(11.8), Inches(.55), 20, INK, True)

# 13 — experiment
s = d.slide(fill=NAVY); chrome(s, 13, "Pilot design", "A matched-task test isolates workflow value from operator enthusiasm")
txt(s, "FIXED INPUTS", Inches(.62), Inches(1.75), Inches(2.0), Inches(.3), 11, CYAN, True)
fixed = ["Same real brief", "Same copy + proof", "Same references", "Same model + time budget"]
for i, item in enumerate(fixed):
    y = Inches(2.32 + i * .76); rect(s, Inches(.65), y, Inches(.12), Inches(.38), CYAN); txt(s, item, Inches(.98), y - Inches(.03), Inches(2.7), Inches(.42), 15, WHITE, True)
rect(s, Inches(4.05), Inches(1.72), Inches(3.75), Inches(4.65), PANEL)
txt(s, "CURRENT PROCESS", Inches(4.38), Inches(2.12), Inches(3.1), Inches(.3), 11, MUTED, True)
txt(s, "Conventional prompting\nand review", Inches(4.38), Inches(2.78), Inches(3.0), Inches(.9), 24, WHITE, True)
txt(s, "Matched task\nMatched operator profile\nBlind downstream review", Inches(4.38), Inches(4.2), Inches(3.0), Inches(1.1), 15, MUTED, True, ls=1.35)
rect(s, Inches(8.08), Inches(1.72), Inches(4.68), Inches(4.65), c("232A43"))
txt(s, "IMPECCABLE WORKFLOW", Inches(8.42), Inches(2.12), Inches(3.8), Inches(.3), 11, LIME, True)
txt(s, "Worlds → commit\n→ Live refinement", Inches(8.42), Inches(2.78), Inches(3.75), Inches(.9), 24, WHITE, True)
txt(s, "PRIMARY ENDPOINT", Inches(8.42), Inches(4.35), Inches(2.3), Inches(.25), 10, CORAL, True)
txt(s, "Major direction resets before acceptance", Inches(8.42), Inches(4.78), Inches(3.7), Inches(.82), 18, WHITE, True)

# 14 — ask
s = d.slide(fill=NAVY)
txt(s, "DECISION / 14", Inches(.72), Inches(.58), Inches(2.5), Inches(.3), 11, CYAN, True)
txt(s, "EARN THE RIGHT\nTO SCALE.", Inches(.72), Inches(1.12), Inches(7.7), Inches(1.55), 44, WHITE, True, ls=.98)
txt(s, "Authorize pilot design—not enterprise rollout.", Inches(.75), Inches(3.0), Inches(7.8), Inches(.55), 24, LIME, True)
steps = [("01", "NAME THE OWNER", "One accountable lead for direction and release", CYAN), ("02", "SELECT THE TASK", "One bounded landing-page workflow with real proof", VIOLET), ("03", "LOCK THE SCORECARD", "Baseline, thresholds, blind reviewers, stop rules", CORAL)]
for i, (num, head, body, color) in enumerate(steps):
    x = Inches(.75 + i * 4.05)
    rect(s, x, Inches(4.25), Inches(3.55), Inches(1.72), PANEL)
    txt(s, num, x + Inches(.2), Inches(4.48), Inches(.5), Inches(.35), 16, color, True)
    txt(s, head, x + Inches(.82), Inches(4.48), Inches(2.4), Inches(.32), 12, color, True)
    txt(s, body, x + Inches(.2), Inches(5.12), Inches(3.0), Inches(.65), 15, WHITE, True)
signal(s, Inches(.75), Inches(6.55), [2.0, 2.0, 2.0, 2.0, 2.0, 1.5], [CYAN, LIME, VIOLET, CORAL, LIME, CYAN])
txt(s, "Expand only if resets fall without accessibility, provenance, factual, performance, or cost regressions.", Inches(.75), Inches(6.77), Inches(10.8), Inches(.32), 13, MUTED, True)

d.save(OUT)
print(OUT)
