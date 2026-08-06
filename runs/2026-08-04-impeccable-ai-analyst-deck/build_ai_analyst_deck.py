#!/usr/bin/env python3
"""Build a client-ready, AI-Analyst-led Impeccable 4.0 decision deck."""

from pathlib import Path
import sys

sys.path.insert(0, "/home/sheke/content-ideas/skills/branded-pptx-deck/scripts")
from pptxkit import Brand, Deck, Inches, Pt, PP_ALIGN  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402

RUN = Path(__file__).resolve().parent
ASSETS = RUN / "assets"
OUT = RUN / "impeccable-4-ai-analyst-draft.pptx"


def rgb(value):
    return RGBColor.from_string(value)


b = Brand()
d = Deck(brand=b, footer="Impeccable 4.0 · executive analysis")
TOTAL = 15
PAPER, INK, RED = rgb("F2EDE3"), rgb("202220"), rgb("E33D2E")
MOSS, TAN, SOFT, MUTED = rgb("315C4A"), rgb("C8A46B"), rgb("DED6C8"), rgb("6E6A63")
WHITE, PALE, GRAY = rgb("F8F3EA"), rgb("EAE4DA"), rgb("A7A199")


def line(s, x, y, w, color=RED, h=2):
    d.rect(s, x, y, w, Pt(h), color)


def foot(s, page, dark=False, evidence=None):
    col = rgb("AFAAA2") if dark else MUTED
    if evidence:
        d.text(s, evidence, Inches(0.72), Inches(7.0), Inches(7.8), Inches(0.22), size=8, color=col)
    d.text(s, f"{page} / {TOTAL}", Inches(11.72), Inches(7.0), Inches(0.9), Inches(0.22), size=8, color=col, align=PP_ALIGN.RIGHT)


def head(s, text, page, dark=False, sub=None, evidence=None):
    d.text(s, text, Inches(0.72), Inches(0.48), Inches(11.85), Inches(0.64), size=28,
           color=WHITE if dark else INK, bold=True, shrink=True)
    if sub:
        d.text(s, sub, Inches(0.74), Inches(1.18), Inches(11.2), Inches(0.42), size=12,
               color=rgb("CAC4BB") if dark else MUTED, shrink=True)
    foot(s, page, dark, evidence)


def pill(s, text, x, y, w, fill, color=WHITE):
    d.rect(s, x, y, w, Inches(0.36), fill, radius=0.15)
    d.text(s, text, x, y + Inches(0.075), w, Inches(0.2), size=9, color=color, bold=True, align=PP_ALIGN.CENTER)


def proof(page, heading, asset, claim, implication, mirror=False):
    s = d.slide(fill=PAPER)
    head(s, heading, page, evidence="OD · observed demonstration")
    picture = d.picture_centered(s, ASSETS / asset, top=Inches(1.55), width=Inches(7.75), max_bottom=Inches(6.65))
    picture.left = Inches(4.83) if mirror else Inches(0.72)
    nx = Inches(0.72) if mirror else Inches(8.73)
    d.rect(s, nx, Inches(1.55), Inches(3.85), Inches(5.1), INK)
    line(s, nx + Inches(0.3), Inches(2.0), Inches(3.15))
    d.text(s, claim, nx + Inches(0.3), Inches(2.28), Inches(3.15), Inches(1.55), size=19, color=WHITE, bold=True, ls=1.1, shrink=True)
    d.text(s, implication, nx + Inches(0.3), Inches(4.25), Inches(3.15), Inches(1.35), size=12, color=rgb("C9C3BA"), ls=1.18, shrink=True)
    return s


# 1 — Thesis
s = d.slide(fill=INK)
d.rect(s, 0, 0, Inches(0.16), d.H, RED)
d.text(s, "IMPECCABLE 4.0 · EXECUTIVE ANALYSIS", Inches(0.82), Inches(0.65), Inches(5.6), Inches(0.32), size=11, color=RED, bold=True)
d.text(s, "AI design's bottleneck\nis judgment allocation.", Inches(0.82), Inches(1.35), Inches(11.1), Inches(1.75), size=44, color=WHITE, bold=True, ls=1.02, shrink=True)
d.text(s, "Impeccable matters when it moves human attention to the decisions with the highest leverage—before direction hardens, during local comparison, and before release.",
       Inches(0.85), Inches(3.65), Inches(9.8), Inches(1.1), size=20, color=rgb("D0C9C0"), ls=1.18, shrink=True)
d.text(s, "Decision brief", Inches(0.85), Inches(5.7), Inches(2.2), Inches(0.35), size=12, color=TAN, bold=True)
d.text(s, "Adopt as a governed accelerator—not an autonomous taste engine.", Inches(3.0), Inches(5.62), Inches(8.6), Inches(0.58), size=18, color=WHITE, bold=True, shrink=True)
d.text(s, "EVIDENCE  ·  OD observed demonstration   |   PA presenter assertion   |   AI analyst inference", Inches(0.85), Inches(6.48), Inches(9.4), Inches(0.25), size=8, color=rgb("9F9B95"), bold=True)
foot(s, 1, True, "AI · analyst synthesis from supplied walkthrough")

# 2 — convergence and downstream cost
s = d.slide(fill=PAPER)
head(s, "Plausible defaults push expensive correction downstream", 2,
     sub="The cost of generic output appears after the first draft, when direction has already accumulated work.",
     evidence="OD + AI · workflow observed; consequences are analyst inference")
stages = [
    ("GENERIC BASELINE", "Looks plausible", MOSS),
    ("LATE DIRECTION DEBATE", "Taste enters too late", TAN),
    ("MACRO REWORK", "Layout and assets reset", RED),
    ("SLOWER APPROVAL", "More cycles, less coherence", INK),
]
for i, (h, body, color) in enumerate(stages):
    x = Inches(0.75 + i * 3.05)
    d.rect(s, x, Inches(2.18), Inches(2.55), Inches(1.34), color)
    d.text(s, h, x + Inches(0.18), Inches(2.42), Inches(2.2), Inches(0.35), size=12, color=WHITE if color != TAN else INK, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, body, x + Inches(0.18), Inches(2.92), Inches(2.2), Inches(0.3), size=11, color=WHITE if color != TAN else INK, align=PP_ALIGN.CENTER, shrink=True)
    if i < 3:
        d.text(s, "→", x + Inches(2.63), Inches(2.55), Inches(0.32), Inches(0.45), size=18, color=GRAY, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "Management implication", Inches(0.78), Inches(4.35), Inches(2.5), Inches(0.35), size=12, color=RED, bold=True)
d.text(s, "Fix the decision architecture before optimizing generation speed.", Inches(0.78), Inches(4.82), Inches(10.9), Inches(0.7), size=27, color=INK, bold=True, shrink=True)
d.text(s, "A faster first draft can still increase total cycle time when it anchors the team to the wrong visual grammar.", Inches(0.8), Inches(5.72), Inches(10.6), Inches(0.55), size=15, color=MUTED, shrink=True)

# 3 — choice tension curve
s = d.slide(fill=INK)
head(s, "More choice improves taste only when it is structured", 3, True,
     sub="Too little choice creates default convergence. Too much unmanaged choice creates decision paralysis.",
     evidence="OD + PA + AI · option workflow observed; value curve is analyst model")
d.text(s, "DECISION VALUE", Inches(0.85), Inches(1.75), Inches(2.0), Inches(0.32), size=10, color=GRAY, bold=True)
d.rect(s, Inches(1.1), Inches(5.45), Inches(10.6), Pt(2), rgb("595C58"))
d.rect(s, Inches(1.1), Inches(2.0), Pt(2), Inches(3.45), rgb("595C58"))
bars = [("ONE\nDEFAULT", 1.0, GRAY), ("UNSTRUCTURED\nOPTIONS", 1.75, TAN), ("WORLDS →\nCOMMIT → VARIANTS", 3.0, RED), ("ENDLESS\nREROLLS", 1.4, GRAY)]
for i, (lab, h, color) in enumerate(bars):
    x = Inches(1.62 + i * 2.48); height = Inches(h)
    d.rect(s, x, Inches(5.43) - height, Inches(1.55), height, color)
    d.text(s, lab, x - Inches(0.15), Inches(5.68), Inches(1.85), Inches(0.65), size=10, color=WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.text(s, "The feature count is incidental.", Inches(7.1), Inches(2.03), Inches(4.5), Inches(0.42), size=17, color=TAN, bold=True, align=PP_ALIGN.RIGHT)
d.text(s, "The commitment gates create the value.", Inches(6.15), Inches(2.5), Inches(5.45), Inches(0.55), size=22, color=WHITE, bold=True, align=PP_ALIGN.RIGHT)
d.text(s, "CONCEPTUAL RELATIONSHIP · NOT MEASURED", Inches(7.2), Inches(3.15), Inches(4.4), Inches(0.3), size=9, color=GRAY, bold=True, align=PP_ALIGN.RIGHT)

# 4 — Worlds proof
proof(4, "Impeccable externalizes the macro taste decision", "worlds.jpg",
      "Worlds turn an abstract preference into a visible choice.",
      "The workflow separates divergent exploration from commitment. This reduces the burden of encoding taste entirely in a prompt.")

# 5 — commitment gates
s = d.slide(fill=PAPER)
head(s, "Four commitment gates prevent exploration from becoming drift", 5,
     evidence="AI · recommended operating model derived from observed workflow")
gates = [
    ("EVIDENCE", "Is the brief grounded in real content and constraints?", "Design owner"),
    ("WORLD", "Is the visual grammar appropriate for the audience and task?", "Brand / design lead"),
    ("VARIANT", "Is the baseline strong enough for local refinement?", "Product owner"),
    ("RELEASE", "Has an independent challenge found drift or defects?", "Reviewer + accountable human"),
]
for i, (gate, question, owner) in enumerate(gates):
    x = Inches(0.72 + i * 3.05)
    pill(s, gate, x, Inches(1.68), Inches(1.42), RED if i in (1, 3) else MOSS)
    d.text(s, question, x, Inches(2.35), Inches(2.6), Inches(1.28), size=17, color=INK, bold=True, shrink=True)
    line(s, x, Inches(3.92), Inches(2.55), TAN, 2)
    d.text(s, "OWNER", x, Inches(4.18), Inches(0.9), Inches(0.25), size=9, color=MUTED, bold=True)
    d.text(s, owner, x, Inches(4.55), Inches(2.55), Inches(0.75), size=13, color=MOSS, bold=True, shrink=True)
    d.text(s, "EXIT CRITERION", x, Inches(5.52), Inches(1.25), Inches(0.25), size=9, color=MUTED, bold=True)
    d.text(s, "Explicit yes—or return upstream", x, Inches(5.86), Inches(2.55), Inches(0.45), size=12, color=INK, shrink=True)

# 6 — ceiling/floor
s = d.slide(fill=INK)
head(s, "Generality raises the ceiling—and shifts risk to the operator", 6, True,
     evidence="PA · trade-off stated by presenter; no controlled benchmark")
d.text(s, "ONE-TRICK STYLE SKILL", Inches(0.85), Inches(1.72), Inches(4.8), Inches(0.38), size=12, color=GRAY, bold=True)
d.text(s, "Higher floor", Inches(0.85), Inches(2.25), Inches(4.6), Inches(0.55), size=27, color=WHITE, bold=True)
d.text(s, "Predictable novelty\nNarrow aesthetic range\nLower judgment burden", Inches(0.88), Inches(3.1), Inches(4.25), Inches(1.45), size=17, color=rgb("C9C3BA"), ls=1.38)
d.rect(s, Inches(5.85), Inches(1.65), Pt(2), Inches(4.85), rgb("545753"))
d.text(s, "IMPECCABLE", Inches(6.35), Inches(1.72), Inches(4.8), Inches(0.38), size=12, color=RED, bold=True)
d.text(s, "Higher ceiling", Inches(6.35), Inches(2.25), Inches(4.6), Inches(0.55), size=27, color=WHITE, bold=True)
d.text(s, "Broad differentiation\nMore operator variance\nHigher governance need", Inches(6.38), Inches(3.1), Inches(4.8), Inches(1.45), size=17, color=rgb("C9C3BA"), ls=1.38)
d.text(s, "CONVENTIONAL WORKFLOW WINS WHEN", Inches(0.88), Inches(5.25), Inches(3.2), Inches(0.3), size=10, color=TAN, bold=True)
d.text(s, "the surface is highly standardized  ·  evidence is weak  ·  review capacity is limited  ·  the team cannot own directional choices",
       Inches(0.88), Inches(5.72), Inches(10.85), Inches(0.65), size=15, color=WHITE, bold=True, shrink=True)

# 7 — routing matrix
s = d.slide(fill=PAPER)
head(s, "Change altitude determines the correct interface", 7,
     sub="Route by change radius and confidence in the current direction.",
     evidence="OD + AI · macro/micro split observed; matrix is analyst decision rule")
d.text(s, "DIRECTION CONFIDENCE", Inches(5.3), Inches(1.68), Inches(3.1), Inches(0.3), size=10, color=MUTED, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "LOW", Inches(3.35), Inches(1.88), Inches(2.5), Inches(0.3), size=10, color=RED, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "HIGH", Inches(7.35), Inches(1.88), Inches(2.5), Inches(0.3), size=10, color=MOSS, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "LARGE\nCHANGE", Inches(0.88), Inches(2.65), Inches(1.3), Inches(0.7), size=11, color=INK, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "SMALL\nCHANGE", Inches(0.88), Inches(4.85), Inches(1.3), Inches(0.7), size=11, color=INK, bold=True, align=PP_ALIGN.CENTER)
cells = [
    (Inches(2.35), Inches(2.3), "REFERENCE RESET", "Reopen the visual grammar", RED),
    (Inches(6.55), Inches(2.3), "TERMINAL", "Change layout or structure", MOSS),
    (Inches(2.35), Inches(4.55), "STOP POLISHING", "Clarify the direction first", TAN),
    (Inches(6.55), Inches(4.55), "LIVE MODE", "Compare local variants", INK),
]
for x, y, h, body, color in cells:
    d.rect(s, x, y, Inches(3.55), Inches(1.55), color)
    d.text(s, h, x + Inches(0.2), y + Inches(0.28), Inches(3.15), Inches(0.35), size=15, color=WHITE if color != TAN else INK, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, body, x + Inches(0.25), y + Inches(0.82), Inches(3.05), Inches(0.38), size=12, color=WHITE if color != TAN else INK, align=PP_ALIGN.CENTER, shrink=True)

# 8 — Live proof
proof(8, "Live Mode compresses the local judgment loop", "live-comparison.jpg",
      "Select → generate 1–4 variants → compare → tune → accept.",
      "The advantage is not visual editing alone. It reduces the distance between seeing a local problem and comparing concrete alternatives.", mirror=True)

# 9 — reference reset proof
proof(9, "When the direction is wrong, local polish compounds sunk cost", "references.jpg",
      "References are an escalation mechanism—not decoration.",
      "Reset the macro direction through references and terminal work. Return to Live Mode only after the visual grammar is sound.")

# 10 — judgment allocation model
s = d.slide(fill=PAPER)
head(s, "Human judgment belongs at four high-leverage moments", 10,
     evidence="AI · role model synthesized from the full walkthrough")
moments = ["FRAME TRUTH", "COMMIT DIRECTION", "RESOLVE TRADE-OFFS", "APPROVE RELEASE"]
human = ["Define audience, evidence, constraints", "Choose the visual grammar", "Judge variants and escalation", "Own the release decision"]
system = ["Structure the brief", "Expand materially different options", "Generate and compare alternatives", "Detect patterns and run technical QA"]
for i, m in enumerate(moments):
    x = Inches(0.72 + i * 3.05)
    d.rect(s, x, Inches(1.6), Inches(2.63), Inches(0.72), RED if i in (1, 3) else MOSS)
    d.text(s, m, x + Inches(0.15), Inches(1.82), Inches(2.33), Inches(0.28), size=11, color=WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "HUMAN DECIDES", x, Inches(2.75), Inches(2.63), Inches(0.28), size=9, color=RED, bold=True)
    d.text(s, human[i], x, Inches(3.18), Inches(2.63), Inches(0.92), size=16, color=INK, bold=True, shrink=True)
    line(s, x, Inches(4.35), Inches(2.63), TAN, 2)
    d.text(s, "SYSTEM SUPPORTS", x, Inches(4.68), Inches(2.63), Inches(0.28), size=9, color=MOSS, bold=True)
    d.text(s, system[i], x, Inches(5.08), Inches(2.63), Inches(0.92), size=14, color=MUTED, shrink=True)

# 11 — memory flywheel
s = d.slide(fill=INK)
head(s, "Taste scales only when decisions become organizational memory", 11, True,
     evidence="OD + AI · DESIGN.md and Detect observed; flywheel is analyst model")
nodes = [
    ("CHOSEN\nDECISIONS", Inches(0.95), Inches(2.4), RED),
    ("DESIGN.MD", Inches(3.75), Inches(1.75), TAN),
    ("FUTURE\nCONSTRAINTS", Inches(7.0), Inches(2.4), MOSS),
    ("DETECTION +\nOVERRIDES", Inches(4.0), Inches(4.7), rgb("59615D")),
]
for text, x, y, color in nodes:
    d.rect(s, x, y, Inches(2.15), Inches(1.0), color, radius=0.08)
    d.text(s, text, x, y + Inches(0.26), Inches(2.15), Inches(0.48), size=13, color=WHITE if color != TAN else INK, bold=True, align=PP_ALIGN.CENTER, shrink=True)
arrows = [(Inches(3.15), Inches(2.7), "→"), (Inches(6.05), Inches(2.7), "→"), (Inches(7.15), Inches(4.1), "↙"), (Inches(3.18), Inches(4.15), "↖")]
for x, y, symbol in arrows:
    d.text(s, symbol, x, y, Inches(0.6), Inches(0.5), size=23, color=RED, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "Less reinvention", Inches(9.75), Inches(2.1), Inches(2.0), Inches(0.35), size=14, color=TAN, bold=True)
d.text(s, "Lower variance", Inches(9.75), Inches(2.75), Inches(2.0), Inches(0.35), size=14, color=TAN, bold=True)
d.text(s, "Faster future cycles", Inches(9.75), Inches(3.4), Inches(2.4), Inches(0.35), size=14, color=TAN, bold=True)
d.text(s, "Risk: stale constraints become a new default. Version the record and permit explicit resets.", Inches(0.95), Inches(6.15), Inches(10.9), Inches(0.42), size=14, color=WHITE, bold=True, shrink=True)

# 12 — maker checker
s = d.slide(fill=PAPER)
head(s, "Fresh-context review is a challenge control—not proof of quality", 12,
     evidence="PA + AI · reviewer described by presenter; efficacy is unmeasured")
d.rect(s, Inches(0.8), Inches(1.82), Inches(4.55), Inches(3.55), MOSS)
d.text(s, "MAKER CONTEXT", Inches(1.15), Inches(2.18), Inches(3.85), Inches(0.35), size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "Knows the brief\nKnows every compromise\nCan rationalize its own choices", Inches(1.2), Inches(2.95), Inches(3.7), Inches(1.45), size=19, color=WHITE, bold=True, ls=1.32, align=PP_ALIGN.CENTER)
d.text(s, "→", Inches(5.56), Inches(3.07), Inches(1.0), Inches(0.65), size=32, color=RED, bold=True, align=PP_ALIGN.CENTER)
d.rect(s, Inches(6.8), Inches(1.82), Inches(4.95), Inches(3.55), INK)
d.text(s, "CHECKER CONTEXT", Inches(7.18), Inches(2.18), Inches(4.2), Inches(0.35), size=13, color=RED, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "Challenges known defaults\nSees the result without build momentum\nStill needs human adjudication", Inches(7.25), Inches(2.95), Inches(4.0), Inches(1.45), size=18, color=WHITE, bold=True, ls=1.32, align=PP_ALIGN.CENTER, shrink=True)
d.text(s, "Keep separate QA for accessibility, factual accuracy, performance, responsive behavior, and user outcomes.", Inches(0.82), Inches(5.95), Inches(10.95), Inches(0.62), size=16, color=RED, bold=True, shrink=True)

# 13 — maturity model
s = d.slide(fill=PAPER)
head(s, "The demo reaches Level 2—and shows pieces of Level 3", 13,
     sub="There is no supplied evidence for measured productivity or user outcomes.",
     evidence="AI · maturity assessment based on observed workflow")
d.text(s, "RUBRIC  ·  decision gates   |   change routing   |   design memory   |   QA control   |   measurement", Inches(0.72), Inches(1.62), Inches(11.1), Inches(0.28), size=9, color=MUTED, bold=True)
levels = [
    ("0", "AD HOC", "One-shot prompt\nSubjective approval", GRAY),
    ("1", "GUIDED", "Worlds and steering\nNamed decision owner", TAN),
    ("2", "STRUCTURED", "Macro commitment\nThen local convergence", RED),
    ("3", "CONTROLLED", "Design record\nDetect + independent QA", MOSS),
    ("4", "MEASURED", "Time, cost, rework\nQuality metrics", rgb("5D615D")),
    ("5", "OUTCOME", "Usability and business\nimpact validated", INK),
]
for i, (num, name, body, color) in enumerate(levels):
    x = Inches(0.55 + i * 2.05)
    d.rect(s, x, Inches(2.0), Inches(1.72), Inches(3.42), color)
    d.text(s, num, x + Inches(0.15), Inches(2.18), Inches(0.35), Inches(0.35), size=15, color=WHITE if color != TAN else INK, bold=True)
    d.text(s, name, x + Inches(0.15), Inches(2.72), Inches(1.42), Inches(0.35), size=10, color=WHITE if color != TAN else INK, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, body, x + Inches(0.13), Inches(3.5), Inches(1.46), Inches(0.95), size=10, color=WHITE if color != TAN else INK, align=PP_ALIGN.CENTER, shrink=True)
d.text(s, "DEMONSTRATED", Inches(3.95), Inches(5.82), Inches(3.15), Inches(0.35), size=11, color=RED, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "UNPROVEN", Inches(9.0), Inches(5.82), Inches(3.15), Inches(0.35), size=11, color=INK, bold=True, align=PP_ALIGN.CENTER)

# 14 — adoption gates
s = d.slide(fill=INK)
head(s, "Adoption should advance only when four readiness gates are green", 14, True,
     evidence="AI · recommended governance framework")
gates = [
    ("INPUT", "Real copy, proof, constraints, approved references"),
    ("DECISION", "Named owner for World and variant selection"),
    ("WORKFLOW", "Macro/micro routing and stop rules understood"),
    ("GOVERNANCE", "Versioned design record, QA, provenance controls"),
]
for i, (name, body) in enumerate(gates):
    y = Inches(1.65 + i * 1.18)
    d.rect(s, Inches(0.88), y, Inches(0.68), Inches(0.68), MOSS, radius=0.5)
    d.text(s, "✓", Inches(0.88), y + Inches(0.13), Inches(0.68), Inches(0.34), size=16, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, name, Inches(1.9), y + Inches(0.02), Inches(2.1), Inches(0.4), size=17, color=RED, bold=True)
    d.text(s, body, Inches(4.15), y + Inches(0.02), Inches(7.0), Inches(0.55), size=16, color=WHITE, bold=True, shrink=True)
    line(s, Inches(1.9), y + Inches(0.82), Inches(9.9), rgb("50534F"), 1)
d.rect(s, Inches(0.88), Inches(6.33), Inches(11.0), Inches(0.45), RED)
d.text(s, "ANY RED GATE → RUN A BOUNDED PILOT. DO NOT SCALE THE WORKFLOW.", Inches(0.88), Inches(6.43), Inches(11.0), Inches(0.24), size=11, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

# 15 — measurement and recommendation
s = d.slide(fill=PAPER)
head(s, "Success is fewer wrong-direction cycles—without quality regressions", 15,
     evidence="AI · pilot recommendation; no benchmark data supplied")
d.text(s, "PILOT OUTCOME", Inches(0.78), Inches(1.52), Inches(2.2), Inches(0.35), size=11, color=RED, bold=True)
d.text(s, "Reduce the cost of arriving at an acceptable direction.", Inches(0.78), Inches(1.98), Inches(7.3), Inches(0.72), size=28, color=INK, bold=True, shrink=True)
measures = [
    ("EFFICIENCY", "Time to direction\nTime to production-ready"),
    ("REWORK", "Major resets\nPost-approval changes"),
    ("QUALITY", "Blind brand + usability scores\nIndependent defects"),
    ("GOVERNANCE", "Unsupported claims\nReference exceptions"),
]
for i, (name, body) in enumerate(measures):
    x = Inches(0.78 + i * 3.0)
    line(s, x, Inches(3.35), Inches(2.48), RED if i == 1 else MOSS, 3)
    d.text(s, name, x, Inches(3.62), Inches(2.48), Inches(0.35), size=12, color=INK, bold=True)
    d.text(s, body, x, Inches(4.18), Inches(2.48), Inches(1.0), size=14, color=MUTED, ls=1.3, shrink=True)
d.rect(s, Inches(0.78), Inches(5.38), Inches(11.4), Inches(1.08), INK)
d.text(s, "PROPOSED GO / NO-GO  ·  confirm before launch", Inches(1.02), Inches(5.56), Inches(3.15), Inches(0.26), size=9, color=RED, bold=True)
d.text(s, "6+ matched tasks · 2+ operator profiles · ≥20% fewer major resets · quality within 5% of baseline · zero critical accessibility/provenance regressions · cost ≤ baseline +15%",
       Inches(1.02), Inches(5.93), Inches(10.9), Inches(0.38), size=11, color=WHITE, bold=True, shrink=True)

d.save(OUT)
print(OUT)
