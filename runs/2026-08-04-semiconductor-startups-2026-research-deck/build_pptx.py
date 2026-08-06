#!/usr/bin/env python3
"""Build the native, branded semiconductor-startup decision deck."""

import sys
from pathlib import Path

from pptx import Presentation

ROOT = Path("/home/sheke/content-ideas")
sys.path.insert(0, str(ROOT / "skills/branded-pptx-deck/scripts"))
from pptxkit import Brand, Deck, Inches, PP_ALIGN, Pt  # noqa: E402

RUN = Path(__file__).resolve().parent
TEMPLATE = ROOT / "skills/branded-pptx-deck/resources/template.pptx"
OUT = RUN / "semiconductor-startups-2026-decision-deck-draft.pptx"
TOTAL = 13

b = Brand()
d = Deck(brand=b, footer="Semiconductor startups 2026 · decision brief")
# The governed repo-local branded template supplies the theme/master package.
d.prs = Presentation(str(TEMPLATE))
d._wipe()
d.W = Inches(13.333)
d.H = Inches(7.5)
d.prs.slide_width = d.W
d.prs.slide_height = d.H
d.M = Inches(0.6)
d.CW = d.W - d.M * 2


def title(slide, text, subtitle=None):
    d.header(slide, text, subtitle)


def foot(slide, page, dark=False):
    d.footer(slide, page, TOTAL, dark=dark)


def card(slide, x, y, w, h, label, body, accent=None):
    accent = accent or b.TEAL
    d.rect(slide, x, y, w, h, b.WHITE, line=b.GRID, radius=0.03)
    d.rect(slide, x, y, Inches(0.08), h, accent)
    d.text(slide, label, x + Inches(0.25), y + Inches(0.18), w - Inches(0.45), Inches(0.36), size=12, color=accent, bold=True, shrink=True)
    d.text(slide, body, x + Inches(0.25), y + Inches(0.66), w - Inches(0.45), h - Inches(0.85), size=15, color=b.NAVY, bold=True, shrink=True, ls=1.1)


# 1 — cover
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.text(s, "SEMICONDUCTOR STARTUPS · 2026", d.M, Inches(0.9), d.CW, Inches(0.4), size=14, color=b.TEAL, bold=True)
d.text(s, "The race is fragmenting\naround four bottlenecks", d.M, Inches(1.45), Inches(10.8), Inches(2.0), size=42, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(3.88), Inches(1.55), Inches(0.06), b.GOLD)
d.text(s, "A buyer’s map of CRN’s ten coolest semiconductor startups", d.M, Inches(4.22), Inches(9.8), Inches(0.7), size=19, color=b.LIGHT_TEAL, shrink=True)
d.text(s, "DECISION BRIEF  ·  AUGUST 2026", d.M, Inches(6.28), Inches(5), Inches(0.35), size=10, color=b.WHITE, bold=True)
foot(s, 1, True)

# 2 — BLUF
s = d.slide(fill=b.WHITE)
title(s, "Do not evaluate these startups as one GPU-replacement race")
d.rect(s, d.M, Inches(1.55), d.CW, Inches(1.05), b.NAVY, radius=0.02)
d.text(s, "BLUF", d.M + Inches(0.28), Inches(1.82), Inches(0.8), Inches(0.35), size=12, color=b.TEAL, bold=True)
d.text(s, "Match each vendor to the bottleneck it removes—and demand proof at system level.", Inches(1.65), Inches(1.75), Inches(10.6), Inches(0.55), size=22, color=b.WHITE, bold=True, shrink=True)
for i, (lab, body) in enumerate([
    ("SITUATION", "Ten companies span compute, memory, networks, and complete racks."),
    ("INSIGHT", "Useful throughput now depends on feeding and utilizing silicon—not peak arithmetic alone."),
    ("ACTION", "Separate shipping products from 2027–2028 roadmaps before procurement."),
]):
    card(s, d.M + i * Inches(4.05), Inches(3.12), Inches(3.72), Inches(2.15), lab, body, [b.TEAL, b.GOLD, b.CORAL][i])
foot(s, 2)

# 3 — market
s = d.slide(fill=b.NAVY)
d.text(s, "A $1.3T market makes bottleneck relief commercially valuable", d.M, Inches(0.62), d.CW, Inches(0.78), size=29, color=b.WHITE, bold=True, shrink=True)
d.text(s, ">$1.3T", d.M, Inches(1.65), Inches(4.2), Inches(1.25), size=58, color=b.GOLD, bold=True)
d.text(s, "2026 global semiconductor revenue forecast cited by CRN", d.M, Inches(2.92), Inches(4.5), Inches(0.82), size=16, color=b.LIGHT_TEAL, shrink=True)
d.rect(s, Inches(5.25), Inches(1.7), Inches(0.06), Inches(3.95), b.TEAL)
d.text(s, "The strategic unit is shifting", Inches(5.75), Inches(1.7), Inches(6.6), Inches(0.45), size=14, color=b.TEAL, bold=True)
for i, txt in enumerate(["chip → completed workload", "peak FLOPS → tokens per watt", "accelerator → rack utilization", "benchmark → deployment evidence"]):
    d.text(s, txt, Inches(5.75), Inches(2.42) + i * Inches(0.78), Inches(6.1), Inches(0.5), size=21, color=b.WHITE, bold=True)
d.text(s, "Forecast, not realized revenue · CRN citing Gartner (2026)", d.M, Inches(6.47), Inches(8.5), Inches(0.3), size=9, color=b.MUTED)
foot(s, 3, True)

# 4 — four bets
s = d.slide(fill=b.WHITE)
title(s, "Four architectural bets explain the ten-company field")
bets = [
    ("01", "WORKLOAD-SPECIFIC INFERENCE", "Axelera · d-Matrix · Fractile · MatX · Etched", b.TEAL),
    ("02", "DATA MOVEMENT + INTERCONNECT", "Lightmatter · Cornelis · Xsight", b.GOLD),
    ("03", "OPEN + RECONFIGURABLE", "Tenstorrent · NextSilicon", b.ACCENT),
    ("04", "RACK-SCALE INTEGRATION", "d-Matrix · Cornelis · Tenstorrent · Xsight", b.CORAL),
]
for i, (num, head, names, col) in enumerate(bets):
    x = d.M + (i % 2) * Inches(6.05); y = Inches(1.62) + (i // 2) * Inches(2.16)
    d.rect(s, x, y, Inches(5.72), Inches(1.78), b.SOFT, radius=0.03)
    d.text(s, num, x + Inches(0.25), y + Inches(0.22), Inches(0.55), Inches(0.4), size=12, color=col, bold=True)
    d.text(s, head, x + Inches(0.92), y + Inches(0.2), Inches(4.45), Inches(0.45), size=15, color=b.NAVY, bold=True, shrink=True)
    d.text(s, names, x + Inches(0.92), y + Inches(0.82), Inches(4.4), Inches(0.58), size=14, color=b.INK, shrink=True)
d.text(s, "The categories overlap: system builders increasingly cross chip, fabric, and software boundaries.", d.M, Inches(6.18), d.CW, Inches(0.42), size=14, color=b.MUTED, italic=True)
foot(s, 4)

# 5 — inference
s = d.slide(fill=b.WHITE)
title(s, "Inference specialists trade generality for latency and efficiency")
items = [
    ("AXELERA", "Digital in-memory compute", "Edge power + cost"),
    ("d-MATRIX", "Digital in-memory compute", "Data-center latency"),
    ("FRACTILE", "In-memory compute", "Memory bandwidth"),
    ("MATX", "LLM-specific processor", "Frontier-model throughput"),
    ("ETCHED", "Transformer-specific ASIC", "Maximum specialization"),
]
for i, (name, arch, bottleneck) in enumerate(items):
    y = Inches(1.52) + i * Inches(0.96)
    d.text(s, f"0{i+1}", d.M, y, Inches(0.45), Inches(0.32), size=10, color=b.TEAL, bold=True)
    d.text(s, name, Inches(1.25), y - Inches(0.03), Inches(2.0), Inches(0.4), size=16, color=b.NAVY, bold=True)
    d.text(s, arch, Inches(3.55), y, Inches(3.5), Inches(0.38), size=14, color=b.INK)
    d.text(s, bottleneck, Inches(7.35), y, Inches(4.7), Inches(0.38), size=14, color=b.MUTED)
    d.rect(s, d.M, y + Inches(0.55), d.CW, Pt(1), b.GRID)
d.rect(s, d.M, Inches(6.25), d.CW, Inches(0.48), b.LIGHT_TEAL)
d.text(s, "Upside: efficiency  ·  Risk: workload and model architecture drift", d.M + Inches(0.25), Inches(6.36), d.CW - Inches(0.5), Inches(0.26), size=13, color=b.NAVY, bold=True)
foot(s, 5)

# 6 — interconnect metrics
s = d.slide(fill=b.NAVY)
d.text(s, "Three companies monetize the cost of idle compute", d.M, Inches(0.65), d.CW, Inches(0.7), size=30, color=b.WHITE, bold=True)
metrics = [
    ("6.4 Tbps", "LIGHTMATTER", "Passage L20 · each direction", b.TEAL),
    ("800 Gbps", "XSIGHT LABS", "E-series DPU · 64 Arm N2 cores", b.GOLD),
    ("LOSSLESS", "CORNELIS", "CN5000 scale-out fabric", b.CORAL),
]
for i, (metric, company, note, col) in enumerate(metrics):
    x = d.M + i * Inches(4.05)
    d.rect(s, x, Inches(1.75), Inches(3.7), Inches(3.25), b.NAVY_2, radius=0.03)
    d.text(s, metric, x + Inches(0.25), Inches(2.12), Inches(3.2), Inches(0.8), size=34, color=col, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, company, x + Inches(0.25), Inches(3.18), Inches(3.2), Inches(0.38), size=13, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, note, x + Inches(0.25), Inches(3.75), Inches(3.2), Inches(0.65), size=14, color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
d.text(s, "Vendor specifications; validate on customer workloads and real topology.", d.M, Inches(5.65), d.CW, Inches(0.42), size=14, color=b.LIGHT_TEAL, bold=True)
foot(s, 6, True)

# 7 — open architectures
s = d.slide(fill=b.WHITE)
title(s, "Openness is becoming a distribution strategy—not an ideology")
card(s, d.M, Inches(1.62), Inches(5.55), Inches(2.8), "TENSTORRENT", "Tensix accelerators + RISC-V CPU IP + systems + Ethernet scale-out", b.TEAL)
card(s, Inches(7.15), Inches(1.62), Inches(5.55), Inches(2.8), "NEXTSILICON", "Runtime-reconfigurable dataflow + RISC-V CPU path", b.GOLD)
d.text(s, "CUSTOMIZATION", d.M, Inches(4.72), Inches(3.55), Inches(0.3), size=11, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "↓ lock-in anxiety", d.M, Inches(5.08), Inches(3.55), Inches(0.4), size=17, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "ECOSYSTEM", Inches(4.9), Inches(4.72), Inches(3.55), Inches(0.3), size=11, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "↑ licensing reach", Inches(4.9), Inches(5.08), Inches(3.55), Inches(0.4), size=17, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "TRADE-OFF", Inches(9.2), Inches(4.72), Inches(3.5), Inches(0.3), size=11, color=b.CORAL, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "tools must mature", Inches(9.2), Inches(5.08), Inches(3.5), Inches(0.4), size=17, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
d.rect(s, d.M, Inches(5.72), d.CW, Inches(0.72), b.NAVY)
d.text(s, "Open interfaces widen options; they do not guarantee production support.", d.M + Inches(0.28), Inches(5.9), d.CW - Inches(0.56), Inches(0.38), size=15, color=b.WHITE, bold=True)
foot(s, 7)

# 8 — rack scale
s = d.slide(fill=b.WHITE)
title(s, "The commercial unit is expanding from chip to rack outcome")
stages = [("SILICON", "Compute"), ("MEMORY", "Movement"), ("FABRIC", "Utilization"), ("SOFTWARE", "Portability"), ("RACK", "Deployment")]
for i, (head, sub) in enumerate(stages):
    x = d.M + i * Inches(2.42)
    d.rect(s, x, Inches(2.05), Inches(1.86), Inches(1.0), b.TEAL if i < 4 else b.CORAL, radius=0.08)
    d.text(s, head, x, Inches(2.3), Inches(1.86), Inches(0.32), size=12, color=b.NAVY if i < 4 else b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, sub, x, Inches(3.28), Inches(1.86), Inches(0.42), size=14, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    if i < 4:
        d.text(s, "→", x + Inches(1.91), Inches(2.31), Inches(0.45), Inches(0.4), size=19, color=b.MUTED, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "d-Matrix · Cornelis · Tenstorrent · Xsight", d.M, Inches(4.42), d.CW, Inches(0.45), size=20, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "System execution is harder than chip benchmarking—and more relevant to buyers.", d.M, Inches(5.18), d.CW, Inches(0.52), size=17, color=b.MUTED, align=PP_ALIGN.CENTER)
foot(s, 8)

# 9 — maturity
s = d.slide(fill=b.WHITE)
title(s, "Commercial evidence divides the field into two procurement gates")
d.rect(s, d.M, Inches(1.55), Inches(5.85), Inches(0.58), b.TEAL)
d.rect(s, Inches(6.88), Inches(1.55), Inches(5.85), Inches(0.58), b.CORAL)
d.text(s, "CURRENT COMMERCIAL SIGNALS", d.M, Inches(1.71), Inches(5.85), Inches(0.3), size=13, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "ROADMAP-DEPENDENT PROOF", Inches(6.88), Inches(1.71), Inches(5.85), Inches(0.3), size=13, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
left = ["Axelera AI", "Cornelis", "d-Matrix", "Lightmatter", "Tenstorrent", "Xsight Labs"]
right = ["Fractile", "MatX", "NextSilicon", "Etched"]
for i, name in enumerate(left):
    y = Inches(2.45) + i * Inches(0.58)
    d.text(s, "●", Inches(1.05), y, Inches(0.25), Inches(0.25), size=10, color=b.TEAL)
    d.text(s, name, Inches(1.45), y - Inches(0.03), Inches(4.2), Inches(0.35), size=15, color=b.NAVY, bold=True)
for i, name in enumerate(right):
    y = Inches(2.45) + i * Inches(0.78)
    d.text(s, "○", Inches(7.45), y, Inches(0.25), Inches(0.25), size=11, color=b.CORAL)
    d.text(s, name, Inches(7.85), y - Inches(0.03), Inches(4.1), Inches(0.35), size=15, color=b.NAVY, bold=True)
d.text(s, "Signals include products, deployments, production status, sampling, or named customers; they are not equivalent proof.", d.M, Inches(6.18), d.CW, Inches(0.35), size=11, color=b.MUTED, italic=True, shrink=True)
foot(s, 9)

# 10 — funding
s = d.slide(fill=b.NAVY)
d.text(s, "Funding buys runway—not proof", d.M, Inches(0.72), d.CW, Inches(0.7), size=31, color=b.WHITE, bold=True)
d.text(s, "~$10.7B", d.M, Inches(1.72), Inches(4.3), Inches(1.12), size=54, color=b.GOLD, bold=True)
d.text(s, "semiconductor startup funding reported in 2026 through publication date", d.M, Inches(2.88), Inches(4.35), Inches(0.8), size=15, color=b.LIGHT_TEAL, shrink=True)
for i, (head, body, col) in enumerate([
    ("CAPITAL", "runway + investor conviction", b.GOLD),
    ("SILICON", "working chip + repeatable yield", b.TEAL),
    ("SYSTEM", "software + reliability + deployment", b.CORAL),
]):
    x = Inches(5.38) + (i % 1) * 0
    y = Inches(1.72) + i * Inches(1.22)
    d.text(s, f"0{i+1}", x, y, Inches(0.5), Inches(0.35), size=11, color=col, bold=True)
    d.text(s, head, x + Inches(0.72), y - Inches(0.03), Inches(1.4), Inches(0.4), size=15, color=b.WHITE, bold=True)
    d.text(s, body, x + Inches(2.25), y, Inches(4.75), Inches(0.42), size=15, color=b.LIGHT_TEAL)
    if i < 2: d.rect(s, x + Inches(0.2), y + Inches(0.67), Inches(6.65), Pt(1), b.MUTED)
d.text(s, "Crunchbase News (2026) · funding is an ecosystem-level estimate", d.M, Inches(6.46), Inches(8.7), Inches(0.3), size=9, color=b.MUTED)
foot(s, 10, True)

# 11 — risk
s = d.slide(fill=b.WHITE)
title(s, "Specialization creates the highest upside—and the sharpest roadmap risk")
d.text(s, "EFFICIENCY UPSIDE", d.M, Inches(1.6), Inches(2.4), Inches(0.35), size=11, color=b.TEAL, bold=True)
d.rect(s, d.M, Inches(2.08), d.CW, Inches(0.14), b.GRID)
d.rect(s, d.M, Inches(2.08), Inches(9.9), Inches(0.14), b.TEAL)
points = [(1.2, "Open / adaptable"), (5.3, "Workload tuned"), (9.9, "Architecture specific")]
for xoff, lab in points:
    d.rect(s, d.M + Inches(xoff), Inches(1.94), Inches(0.4), Inches(0.4), b.NAVY, radius=0.5)
    d.text(s, lab, d.M + Inches(xoff) - Inches(0.65), Inches(2.52), Inches(1.7), Inches(0.55), size=12, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
for i, (head, body) in enumerate([
    ("MODEL DRIFT", "Architecture, precision, or memory patterns change before volume deployment."),
    ("SOFTWARE DRAG", "Compiler, framework, and operations maturity erase theoretical gains."),
    ("SUPPLY EXECUTION", "Packaging, yield, and support determine repeatable rack delivery."),
]):
    card(s, d.M + i * Inches(4.05), Inches(3.52), Inches(3.72), Inches(1.75), head, body, b.CORAL)
d.text(s, "The more specialized the silicon, the more often the workload contract must be revalidated.", d.M, Inches(5.82), d.CW, Inches(0.42), size=15, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
foot(s, 11)

# 12 — scorecard
s = d.slide(fill=b.WHITE)
title(s, "Use one workload-matched scorecard before advancing any vendor")
criteria = ["Comparable precision + batch", "Latency + throughput", "Rack power + utilization", "Software maturity", "Reliability + supply", "Deployment lead time"]
for i, txt in enumerate(criteria):
    col, row = i % 2, i // 2
    x = d.M + col * Inches(6.05); y = Inches(1.58) + row * Inches(1.4)
    d.rect(s, x, y, Inches(0.62), Inches(0.62), b.TEAL, radius=0.5)
    d.text(s, str(i + 1), x, y + Inches(0.1), Inches(0.62), Inches(0.35), size=14, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, txt, x + Inches(0.9), y + Inches(0.04), Inches(4.75), Inches(0.55), size=17, color=b.NAVY, bold=True, shrink=True)
d.rect(s, d.M, Inches(5.92), d.CW, Inches(0.66), b.NAVY)
d.text(s, "Gate 1: available product  ·  Gate 2: roadmap silicon  ·  Never mix proof thresholds", d.M + Inches(0.25), Inches(6.09), d.CW - Inches(0.5), Inches(0.32), size=14, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
foot(s, 12)

# 13 — close
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, Inches(0.18), d.H, b.GOLD)
d.text(s, "THE DECISION", d.M, Inches(0.95), d.CW, Inches(0.35), size=13, color=b.TEAL, bold=True)
d.text(s, "Buy bottleneck relief—\nnot startup mythology.", d.M, Inches(1.48), Inches(10.2), Inches(1.55), size=42, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(3.52), Inches(1.55), Inches(0.06), b.GOLD)
d.text(s, "Benchmark the complete system. Preserve optionality. Keep roadmap claims in a separate gate.", d.M, Inches(3.92), Inches(10.6), Inches(1.1), size=21, color=b.LIGHT_TEAL, bold=True, shrink=True)
d.text(s, "Primary framing: CRN (2026) · details verified against company releases", d.M, Inches(6.28), Inches(8.8), Inches(0.3), size=9, color=b.MUTED)
foot(s, 13, True)

d.save(OUT)
print(OUT)
