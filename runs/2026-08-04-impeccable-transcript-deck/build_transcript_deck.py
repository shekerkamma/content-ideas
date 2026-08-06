#!/usr/bin/env python3
"""Build the transcript-led, client-ready Impeccable 4.0 deck."""

from pathlib import Path
import sys

sys.path.insert(0, "/home/sheke/content-ideas/skills/branded-pptx-deck/scripts")
from pptxkit import Brand, Deck, Inches, Pt, PP_ALIGN  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402

RUN = Path(__file__).resolve().parent
ASSETS = RUN / "assets"
OUT = RUN / "impeccable-4-transcript-led-draft.pptx"

b = Brand()
d = Deck(brand=b, footer="Impeccable 4.0 · transcript-led briefing")
TOTAL = 15
def rgb(value):
    return RGBColor.from_string(value)


PAPER = rgb("F2EDE3")
INK = rgb("202220")
RED = rgb("E33D2E")
MOSS = rgb("315C4A")
TAN = rgb("C8A46B")
SOFT = rgb("DED6C8")
MUTED = rgb("6E6A63")


def footer(slide, page, dark=False):
    d.text(slide, f"{page} / {TOTAL}", Inches(11.75), Inches(7.02), Inches(0.9), Inches(0.22),
           size=8, color=rgb("B9B5AE") if dark else MUTED, align=PP_ALIGN.RIGHT)


def title(slide, text, page, dark=False, sub=None):
    color = rgb("F7F2E9") if dark else INK
    d.text(slide, text, Inches(0.7), Inches(0.55), Inches(11.55), Inches(0.75), size=28,
           color=color, bold=True, shrink=True)
    if sub:
        d.text(slide, sub, Inches(0.72), Inches(1.23), Inches(10.8), Inches(0.36), size=12,
               color=rgb("D0CBC3") if dark else MUTED, shrink=True)
    footer(slide, page, dark)


def line(slide, x1, y, w, color=RED, h=2):
    d.rect(slide, x1, y, w, Pt(h), color)


def proof_slide(page, heading, asset, statement, detail, mirror=False, panorama=False):
    s = d.slide(fill=PAPER)
    title(s, heading, page)
    if panorama:
        picture = d.picture_centered(s, ASSETS / asset, top=Inches(1.48), width=Inches(11.9), max_bottom=Inches(6.58))
        picture.left = Inches(0.7)
        d.rect(s, Inches(0.7), Inches(5.15), Inches(11.9), Inches(1.43), INK)
        line(s, Inches(1.02), Inches(5.48), Inches(2.1))
        d.text(s, statement, Inches(1.02), Inches(5.7), Inches(5.35), Inches(0.55), size=18, color=rgb("F8F3EA"), bold=True, shrink=True)
        d.text(s, detail, Inches(6.72), Inches(5.46), Inches(5.45), Inches(0.78), size=12, color=rgb("CBC5BC"), ls=1.12, shrink=True)
        return s
    picture = d.picture_centered(s, ASSETS / asset, top=Inches(1.55), width=Inches(8.0), max_bottom=Inches(6.65))
    picture.left = Inches(4.63) if mirror else Inches(0.7)
    note_x = Inches(0.7) if mirror else Inches(8.95)
    d.rect(s, note_x, Inches(1.55), Inches(3.68), Inches(5.1), INK)
    line(s, note_x + Inches(0.3), Inches(2.15), Inches(2.95))
    d.text(s, statement, note_x + Inches(0.3), Inches(2.45), Inches(2.95), Inches(1.65), size=20,
           color=rgb("F8F3EA"), bold=True, ls=1.08, shrink=True)
    d.text(s, detail, note_x + Inches(0.3), Inches(4.45), Inches(2.95), Inches(1.15), size=12,
           color=rgb("CBC5BC"), ls=1.18, shrink=True)
    return s


# 1 — cover
s = d.slide(fill=INK)
d.rect(s, 0, 0, Inches(0.16), d.H, RED)
d.text(s, "IMPECCABLE 4.0", Inches(0.78), Inches(0.62), Inches(3.5), Inches(0.35), size=12, color=RED, bold=True)
d.text(s, "Taste becomes\nan operating system.", Inches(0.78), Inches(1.32), Inches(10.9), Inches(2.1), size=48,
       color=rgb("F6F0E7"), bold=True, ls=0.98, shrink=True)
d.text(s, "A source-led briefing on Worlds, Live Mode, iteration, and design control",
       Inches(0.82), Inches(4.15), Inches(8.8), Inches(0.8), size=18, color=rgb("CDC6BD"), shrink=True)
d.rect(s, Inches(10.45), Inches(4.18), Inches(1.25), Inches(1.25), RED)
d.text(s, "4.0", Inches(10.45), Inches(4.48), Inches(1.25), Inches(0.52), size=25, color=rgb("FFFFFF"), bold=True, align=PP_ALIGN.CENTER)
d.text(s, "CLIENT BRIEFING · AUGUST 2026", Inches(0.82), Inches(6.45), Inches(4.0), Inches(0.3), size=9, color=rgb("AFAAA2"), bold=True)
footer(s, 1, True)

# 2 — executive thesis
s = d.slide(fill=PAPER)
title(s, "Impeccable changes the decision system—not just the styling", 2)
d.text(s, "The old loop", Inches(0.8), Inches(1.72), Inches(2.3), Inches(0.4), size=13, color=MUTED, bold=True)
d.text(s, "PROMPT", Inches(0.82), Inches(2.25), Inches(2.0), Inches(0.45), size=20, color=INK, bold=True)
d.text(s, "→", Inches(2.75), Inches(2.23), Inches(0.5), Inches(0.45), size=22, color=RED, bold=True)
d.text(s, "OUTPUT", Inches(3.25), Inches(2.25), Inches(2.0), Inches(0.45), size=20, color=INK, bold=True)
d.text(s, "Accept the first plausible answer.", Inches(0.82), Inches(3.05), Inches(4.5), Inches(0.75), size=17, color=MUTED)
d.rect(s, Inches(5.65), Inches(1.6), Pt(2), Inches(4.7), SOFT)
d.text(s, "The Impeccable loop", Inches(6.05), Inches(1.72), Inches(3.5), Inches(0.4), size=13, color=RED, bold=True)
steps = [("EXPAND", "See materially different worlds"), ("SELECT", "Commit to one direction"), ("ITERATE", "Compare variants visually"), ("REVIEW", "Detect drift and defects")]
for i, (head, body) in enumerate(steps):
    y = Inches(2.2 + i * 0.95)
    d.rect(s, Inches(6.05), y, Inches(0.38), Inches(0.38), RED, radius=0.5)
    d.text(s, str(i + 1), Inches(6.05), y + Inches(0.05), Inches(0.38), Inches(0.25), size=12, color=rgb("FFFFFF"), bold=True, align=PP_ALIGN.CENTER)
    d.text(s, head, Inches(6.62), y - Inches(0.02), Inches(1.65), Inches(0.35), size=13, color=INK, bold=True)
    d.text(s, body, Inches(8.35), y - Inches(0.02), Inches(3.8), Inches(0.42), size=13, color=MUTED, shrink=True)
d.text(s, "The product is a feedback architecture for taste.", Inches(6.05), Inches(6.0), Inches(6.0), Inches(0.55), size=18, color=MOSS, bold=True)

# 3 — convergence
s = d.slide(fill=INK)
title(s, "The failure mode is convergence", 3, True, "Different prompts repeatedly settle on the same recognizable defaults.")
labels = ["purple gradient", "rounded card grid", "icon confetti", "generic hero", "soft-glow chrome", "same hierarchy"]
for i, lab in enumerate(labels):
    x = Inches(0.85 + (i % 3) * 4.05); y = Inches(2.0 + (i // 3) * 1.55)
    d.text(s, lab.upper(), x, y, Inches(3.35), Inches(0.55), size=15, color=rgb("F2ECE4"), bold=True, align=PP_ALIGN.CENTER)
    line(s, x + Inches(0.2), y + Inches(0.72), Inches(2.95), rgb("5C5F5B"), 1)
for i in range(3):
    x = Inches(2.15 + i * 4.05)
    d.text(s, "↘", x, Inches(4.67), Inches(0.7), Inches(0.5), size=24, color=RED, bold=True, align=PP_ALIGN.CENTER)
d.rect(s, Inches(4.45), Inches(5.35), Inches(4.45), Inches(0.72), RED)
d.text(s, "PLAUSIBLE, POLISHED, INTERCHANGEABLE", Inches(4.45), Inches(5.55), Inches(4.45), Inches(0.32), size=12, color=rgb("FFFFFF"), bold=True, align=PP_ALIGN.CENTER)

# 4 — two changes
s = d.slide(fill=PAPER)
title(s, "Version 4.0 adds two decisive control surfaces", 4)
d.text(s, "WORLDS", Inches(0.82), Inches(1.72), Inches(4.4), Inches(0.7), size=34, color=INK, bold=True)
d.text(s, "Expand the option space before committing.", Inches(0.85), Inches(2.55), Inches(4.7), Inches(0.8), size=20, color=MOSS, bold=True)
d.text(s, "177", Inches(0.82), Inches(3.72), Inches(2.2), Inches(1.05), size=58, color=RED, bold=True)
d.text(s, "high-rated visual worlds\nshown against the actual project", Inches(2.65), Inches(3.88), Inches(2.9), Inches(0.9), size=15, color=MUTED, shrink=True)
d.rect(s, Inches(6.1), Inches(1.6), Pt(2), Inches(4.9), SOFT)
d.text(s, "LIVE MODE", Inches(6.52), Inches(1.72), Inches(5.2), Inches(0.7), size=34, color=INK, bold=True)
d.text(s, "Move local iteration from terminal text to visual choice.", Inches(6.55), Inches(2.55), Inches(5.1), Inches(0.8), size=20, color=MOSS, bold=True)
for i, word in enumerate(["PICK", "REQUEST", "COMPARE", "ACCEPT"]):
    x = Inches(6.55 + (i % 2) * 2.55); y = Inches(3.75 + (i // 2) * 1.0)
    d.text(s, word, x, y, Inches(2.25), Inches(0.48), size=14, color=INK, bold=True)
    line(s, x, y + Inches(0.56), Inches(2.1), RED if i == 3 else TAN, 2)

# 5 — worlds proof
proof_slide(5, "Worlds make direction selection concrete", "worlds.jpg",
            "Choose the visual grammar before building the page.",
            "A world governs composition, type, material, rhythm, and interaction—not merely color.")

# 6 — two-level funnel
s = d.slide(fill=PAPER)
title(s, "Direction selection happens twice", 6, sub="First choose among worlds. Then compare variants inside the chosen world.")
d.text(s, "MANY POSSIBLE WORLDS", Inches(0.85), Inches(1.82), Inches(3.1), Inches(0.35), size=12, color=RED, bold=True)
worlds = ["Editorial archive", "Technical dossier", "Civic poster", "Field notebook", "Quiet utility"]
for i, w in enumerate(worlds):
    y = Inches(2.35 + i * 0.68)
    width = Inches(4.8 - i * 0.42)
    d.rect(s, Inches(0.85 + i * 0.21), y, width, Inches(0.45), TAN if i % 2 == 0 else SOFT)
    d.text(s, w, Inches(1.05 + i * 0.21), y + Inches(0.08), width - Inches(0.4), Inches(0.25), size=11, color=INK, bold=True)
d.text(s, "COMMIT", Inches(5.48), Inches(3.77), Inches(1.25), Inches(0.4), size=12, color=RED, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "→", Inches(5.65), Inches(4.18), Inches(0.9), Inches(0.6), size=34, color=RED, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "ONE WORLD, MULTIPLE EXPRESSIONS", Inches(7.0), Inches(1.82), Inches(4.5), Inches(0.35), size=12, color=RED, bold=True)
variants = [("A", "Constellation"), ("B", "Dossier split"), ("C", "Find the why")]
for i, (letter, name) in enumerate(variants):
    y = Inches(2.42 + i * 1.12)
    d.rect(s, Inches(7.0), y, Inches(0.62), Inches(0.62), RED if i == 2 else MOSS)
    d.text(s, letter, Inches(7.0), y + Inches(0.13), Inches(0.62), Inches(0.32), size=13, color=rgb("FFFFFF"), bold=True, align=PP_ALIGN.CENTER)
    d.text(s, name, Inches(7.9), y + Inches(0.1), Inches(3.2), Inches(0.42), size=18, color=INK, bold=True)
d.text(s, "Range first. Refinement second.", Inches(7.0), Inches(5.9), Inches(4.7), Inches(0.45), size=17, color=MOSS, bold=True)

# 7 — tradeoff
s = d.slide(fill=INK)
title(s, "Generality trades a higher ceiling for a lower floor", 7, True)
d.text(s, "ONE-TRICK STYLE SKILL", Inches(0.85), Inches(1.75), Inches(4.8), Inches(0.45), size=14, color=rgb("C8C2BA"), bold=True)
d.text(s, "Predictable", Inches(0.85), Inches(2.35), Inches(4.5), Inches(0.55), size=28, color=rgb("F6F0E7"), bold=True)
d.text(s, "Narrow range\nLower operator burden\nRecognizable signature", Inches(0.88), Inches(3.15), Inches(4.1), Inches(1.6), size=18, color=rgb("C8C2BA"), ls=1.38)
d.rect(s, Inches(5.95), Inches(1.6), Pt(2), Inches(4.9), rgb("565954"))
d.text(s, "IMPECCABLE", Inches(6.45), Inches(1.75), Inches(4.8), Inches(0.45), size=14, color=RED, bold=True)
d.text(s, "Adaptable", Inches(6.45), Inches(2.35), Inches(4.5), Inches(0.55), size=28, color=rgb("F6F0E7"), bold=True)
d.text(s, "Wide range\nHigher judgment burden\nPotentially distinctive result", Inches(6.48), Inches(3.15), Inches(5.0), Inches(1.6), size=18, color=rgb("C8C2BA"), ls=1.38)
d.text(s, "The system creates room for taste; it does not supply taste automatically.", Inches(0.85), Inches(5.85), Inches(11.3), Inches(0.55), size=19, color=RED, bold=True)

# 8 — one shot
s = d.slide(fill=PAPER)
title(s, "One-shot generation is the wrong mental model", 8)
nodes = [("BRIEF", "Define intent"), ("WORLD", "Choose direction"), ("BUILD", "Create a first pass"), ("LIVE", "Tune components"), ("REVIEW", "Close defects")]
for i, (head, body) in enumerate(nodes):
    x = Inches(0.72 + i * 2.5)
    d.text(s, head, x, Inches(2.35), Inches(1.85), Inches(0.42), size=15, color=INK, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, body, x, Inches(2.95), Inches(1.85), Inches(0.62), size=12, color=MUTED, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, x + Inches(0.67), Inches(3.9), Inches(0.5), Inches(0.5), RED if i in (1, 3) else MOSS, radius=0.5)
    if i < len(nodes) - 1:
        d.rect(s, x + Inches(1.38), Inches(4.14), Inches(1.15), Pt(2), TAN)
d.text(s, "ITERATE  ·  ITERATE  ·  ITERATE", Inches(2.2), Inches(5.25), Inches(8.9), Inches(0.7), size=30, color=RED, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "The first complete composition is a baseline, not a verdict.", Inches(2.7), Inches(6.08), Inches(7.9), Inches(0.4), size=15, color=MOSS, bold=True, align=PP_ALIGN.CENTER)

# 9 — Live proof
proof_slide(9, "Live Mode turns local changes into visual decisions", "live-comparison.jpg",
            "Select an element. Generate one to four variants. Tune. Accept.",
            "Commands such as bolder, quieter, polish, and typeset can be applied to the selected region.", panorama=True)

# 10 — altitude
s = d.slide(fill=PAPER)
title(s, "Use the right interface for the altitude of change", 10)
d.rect(s, Inches(0.8), Inches(1.72), Inches(11.75), Inches(1.82), MOSS)
d.text(s, "MACRO", Inches(1.12), Inches(2.0), Inches(1.5), Inches(0.45), size=17, color=rgb("FFFFFF"), bold=True)
d.text(s, "Terminal", Inches(3.05), Inches(1.94), Inches(2.4), Inches(0.55), size=26, color=rgb("FFFFFF"), bold=True)
d.text(s, "New direction · layout reset · reference-driven rebuild", Inches(6.05), Inches(2.05), Inches(5.7), Inches(0.5), size=16, color=rgb("E8E3DA"), shrink=True)
d.rect(s, Inches(0.8), Inches(3.9), Inches(11.75), Inches(1.82), RED)
d.text(s, "MICRO", Inches(1.12), Inches(4.18), Inches(1.5), Inches(0.45), size=17, color=rgb("FFFFFF"), bold=True)
d.text(s, "Live Mode", Inches(3.05), Inches(4.12), Inches(2.4), Inches(0.55), size=26, color=rgb("FFFFFF"), bold=True)
d.text(s, "Component variants · typography · polish · small adjustments", Inches(6.05), Inches(4.23), Inches(5.7), Inches(0.5), size=16, color=rgb("FFE8E3"), shrink=True)
d.text(s, "Escalate when the problem is direction—not detail.", Inches(0.82), Inches(6.18), Inches(7.6), Inches(0.45), size=18, color=INK, bold=True)

# 11 — memory and quality
s = d.slide(fill=INK)
title(s, "Taste becomes durable through memory and independent review", 11, True)
for i, (head, body, color) in enumerate([
    ("DETECT", "Name recurring AI-default and production-defect patterns.", RED),
    ("DESIGN.MD", "Preserve colors, components, controls, and the chosen visual grammar.", TAN),
    ("FINISH REVIEW", "Use a fresh context as a second set of eyes before delivery.", MOSS),
]):
    y = Inches(1.75 + i * 1.48)
    d.rect(s, Inches(0.88), y, Inches(1.75), Inches(0.68), color)
    d.text(s, head, Inches(0.88), y + Inches(0.2), Inches(1.75), Inches(0.28), size=11, color=rgb("FFFFFF") if color != TAN else INK, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, body, Inches(3.05), y + Inches(0.02), Inches(8.65), Inches(0.65), size=19, color=rgb("F4EEE5"), bold=True, shrink=True)
    line(s, Inches(3.05), y + Inches(0.85), Inches(8.65), rgb("50534F"), 1)
d.text(s, "A design system is the record of decisions—not the residue of a single output.", Inches(0.88), Inches(6.16), Inches(11.25), Inches(0.48), size=18, color=RED, bold=True)

# 12 — references proof
proof_slide(12, "References are the escape hatch for a wrong direction", "references.jpg",
            "When the world is wrong, stop polishing it.",
            "Supply a real reference, reset the macro direction in the terminal, then return to Live Mode for local refinement.", mirror=True)

# 13 — operating model
s = d.slide(fill=PAPER)
title(s, "A practical operating model for teams", 13)
stages = [
    ("BRIEF", "Truth and constraints"), ("WORLDS", "Expand directions"), ("SELECT", "Commit visibly"),
    ("BUILD", "Create the baseline"), ("LIVE", "Refine locally"), ("DETECT", "Remove defaults"),
    ("RECORD", "Preserve decisions"), ("REVIEW", "Fresh-context QA"),
]
for i, (head, body) in enumerate(stages):
    col, row = i % 4, i // 4
    x = Inches(0.78 + col * 3.08); y = Inches(1.68 + row * 2.25)
    d.text(s, head, x, y, Inches(2.55), Inches(0.38), size=14, color=RED if i in (1, 4, 5) else INK, bold=True)
    line(s, x, y + Inches(0.52), Inches(2.55), TAN if row == 0 else MOSS, 2)
    d.text(s, body, x, y + Inches(0.72), Inches(2.55), Inches(0.75), size=14, color=MUTED, shrink=True)
    if col < 3:
        d.text(s, "→", x + Inches(2.63), y + Inches(0.42), Inches(0.36), Inches(0.35), size=14, color=SOFT, bold=True)
d.rect(s, Inches(0.78), Inches(6.23), Inches(11.55), Inches(0.42), INK)
d.text(s, "Human judgment is present at every commitment point.", Inches(0.78), Inches(6.31), Inches(11.55), Inches(0.22), size=11, color=rgb("FFFFFF"), bold=True, align=PP_ALIGN.CENTER)

# 14 — what it cannot do
s = d.slide(fill=PAPER)
title(s, "What Impeccable does not solve", 14)
limits = [
    ("Weak truth", "A visual world cannot repair missing evidence."),
    ("Weak narrative", "A design system cannot decide what the audience must understand."),
    ("Blind imitation", "A reference is visual grammar—not permission to copy."),
    ("Absent judgment", "More options only help when someone is willing to choose."),
]
for i, (head, body) in enumerate(limits):
    y = Inches(1.58 + i * 1.2)
    d.rect(s, Inches(0.82), y, Inches(0.48), Inches(0.48), RED, radius=0.5)
    d.text(s, f"{i+1}", Inches(0.82), y + Inches(0.08), Inches(0.48), Inches(0.28), size=15, color=rgb("FFFFFF"), bold=True, align=PP_ALIGN.CENTER)
    d.text(s, head, Inches(1.62), y - Inches(0.02), Inches(2.35), Inches(0.48), size=20, color=INK, bold=True)
    d.text(s, body, Inches(4.25), y, Inches(7.55), Inches(0.48), size=16, color=MUTED, shrink=True)
    line(s, Inches(1.62), y + Inches(0.7), Inches(10.2), SOFT, 1)
d.text(s, "Design discipline complements content discipline. It never replaces it.", Inches(0.82), Inches(6.42), Inches(11.2), Inches(0.35), size=16, color=MOSS, bold=True)

# 15 — conclusion
s = d.slide(fill=INK)
d.rect(s, 0, 0, Inches(0.16), d.H, RED)
d.text(s, "THE TAKEAWAY", Inches(0.82), Inches(0.72), Inches(3), Inches(0.35), size=12, color=RED, bold=True)
d.text(s, "Impeccable does not remove taste from the process.", Inches(0.82), Inches(1.42), Inches(11), Inches(1.12), size=37, color=rgb("F6F0E7"), bold=True, shrink=True)
d.text(s, "It gives taste somewhere to operate.", Inches(0.82), Inches(2.85), Inches(10.5), Inches(0.85), size=32, color=TAN, bold=True, shrink=True)
line(s, Inches(0.82), Inches(4.15), Inches(11.1), RED, 2)
d.text(s, "Expand options  →  commit visibly  →  iterate at the right altitude  →  record the system  →  review independently",
       Inches(0.82), Inches(4.46), Inches(11), Inches(1.28), size=22, color=rgb("F6F0E7"), bold=True, ls=1.16, shrink=True)
d.text(s, "Prepared from the supplied Impeccable 4.0 demonstration", Inches(0.82), Inches(6.45), Inches(5.2), Inches(0.25), size=8, color=rgb("999B96"))
footer(s, 15, True)

d.save(OUT)
print(OUT)
