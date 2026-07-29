#!/usr/bin/env python3
"""Build the materially redesigned 36-slide semiconductor strategy deck."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

from PIL import Image, ImageOps
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches


RUN = Path(__file__).resolve().parents[1]
os.environ["DECK_CONTENT_FILE"] = "outputs/new-deck-content.json"
os.environ["DECK_OUTPUT_FILE"] = (
    "client-package/semiconductor-startups-2026-evidence-led-strategy-draft.pptx"
)

spec = importlib.util.spec_from_file_location("legacy_builder", RUN / "build_deck.py")
base = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(base)


def cover_mosaic(d, data):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, data["kicker"], Inches(0.72), Inches(0.70), Inches(6.9), Inches(0.32), size=12, color=b.TEAL, bold=True)
    d.text(s, data["title"], Inches(0.72), Inches(1.34), Inches(6.6), Inches(1.30), size=42, color=b.WHITE, bold=True, shrink=True)
    d.text(s, data["subtitle"], Inches(0.72), Inches(2.92), Inches(6.35), Inches(1.0), size=20, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, Inches(0.72), Inches(4.30), Inches(1.42), Inches(0.06), b.GOLD)
    d.text(s, data["strapline"], Inches(0.72), Inches(4.68), Inches(6.35), Inches(0.42), size=14, color=b.GOLD, bold=True, shrink=True)
    names = ["AXELERA AI", "D-MATRIX", "LIGHTMATTER", "CORNELIS NETWORKS"]
    positions = [(7.48, 0.58), (10.22, 0.58), (7.48, 3.50), (10.22, 3.50)]
    for name, (x, y) in zip(names, positions):
        asset = base.ASSET_BY_COMPANY[name]
        source = RUN / asset["local_path"]
        derived = RUN / "assets" / "derived" / f"cover-{source.stem}.jpg"
        with Image.open(source).convert("RGB") as image:
            canvas = ImageOps.fit(image, (760, 660), Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            canvas.save(derived, quality=90)
        d.rect(s, Inches(x), Inches(y), Inches(2.45), Inches(2.62), b.NAVY_2, line=b.TEAL, radius=0.05)
        s.shapes.add_picture(str(derived), Inches(x + 0.06), Inches(y + 0.06), Inches(2.33), Inches(2.16))
        d.text(s, name, Inches(x + 0.12), Inches(y + 2.31), Inches(2.21), Inches(0.20), size=9.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    base.add_citation(d, s, data, 1, dark=True)


def decision_dashboard(d, data):
    s = d.slide(fill=d.b.SOFT)
    base.add_header(d, s, data)
    colors = [d.b.TEAL, d.b.GOLD, d.b.CORAL]
    labels = ["ACTIVATE", "VALIDATE", "MONITOR"]
    companies = ["Axelera AI · d-Matrix · Cornelis", "Tenstorrent · NextSilicon · Lightmatter · Xsight", "Fractile · Etched · MatX"]
    actions = ["Package a bounded offer", "Buy missing workload and partner proof", "Track silicon and commercialization triggers"]
    for idx, (label, names, action, color) in enumerate(zip(labels, companies, actions, colors)):
        x = 0.62 + idx * 4.05
        d.rect(s, Inches(x), Inches(2.05), Inches(3.72), Inches(3.55), d.b.WHITE, line=d.b.GRID, radius=0.08, shadow=True)
        d.rect(s, Inches(x), Inches(2.05), Inches(3.72), Inches(0.54), color, radius=0.08)
        d.text(s, label, Inches(x + 0.18), Inches(2.20), Inches(3.36), Inches(0.22), size=13, color=d.b.NAVY if label != "MONITOR" else d.b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, names, Inches(x + 0.28), Inches(2.90), Inches(3.16), Inches(0.90), size=18, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.rect(s, Inches(x + 0.35), Inches(4.05), Inches(3.02), Inches(0.03), d.b.GRID)
        d.text(s, action, Inches(x + 0.30), Inches(4.40), Inches(3.12), Inches(0.72), size=13, color=d.b.INK, align=PP_ALIGN.CENTER, shrink=True)
    base.add_citation(d, s, data, data["id"])


def portfolio_posture(d, data):
    s = d.slide(fill=d.b.WHITE)
    base.add_header(d, s, data)
    colors = {"ACT NOW": d.b.TEAL, "VALIDATE NEXT": d.b.GOLD, "MONITOR": d.b.CORAL}
    for idx, row in enumerate(data["rows"]):
        y = 2.22 + idx * 1.25
        posture, candidates, why, validate = row
        color = colors[posture]
        d.rect(s, Inches(0.62), Inches(y), Inches(2.05), Inches(1.02), color, radius=0.05)
        d.text(s, posture, Inches(0.78), Inches(y + 0.32), Inches(1.73), Inches(0.26), size=12, color=d.b.NAVY if posture != "MONITOR" else d.b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, candidates, Inches(2.92), Inches(y + 0.12), Inches(3.25), Inches(0.38), size=14, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, why, Inches(6.35), Inches(y + 0.12), Inches(2.78), Inches(0.50), size=12.2, color=d.b.INK, shrink=True)
        d.text(s, validate, Inches(9.32), Inches(y + 0.12), Inches(3.10), Inches(0.50), size=12.2, color=d.b.MUTED, shrink=True)
    d.text(s, "POSTURE", Inches(0.82), Inches(1.96), Inches(1.7), Inches(0.18), size=9.5, color=d.b.MUTED, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, "CANDIDATES", Inches(2.92), Inches(1.96), Inches(3.0), Inches(0.18), size=9.5, color=d.b.MUTED, bold=True)
    d.text(s, "WHY NOW", Inches(6.35), Inches(1.96), Inches(2.4), Inches(0.18), size=9.5, color=d.b.MUTED, bold=True)
    d.text(s, "PROOF BEFORE CHANGE", Inches(9.32), Inches(1.96), Inches(3.0), Inches(0.18), size=9.5, color=d.b.MUTED, bold=True)
    base.add_citation(d, s, data, data["id"])


def business_system(d, data):
    s = d.slide(fill=d.b.SOFT)
    base.add_header(d, s, data)
    lanes = [
        ("EDGE DEPLOYMENT", "Chip + platform", "Edge OEM / solution builder", "Partner-led deployment", d.b.TEAL),
        ("ADAPTABLE COMPUTE", "Systems + IP / accelerator", "Sovereign AI / HPC", "Direct + design-in", d.b.ACCENT),
        ("INFERENCE SPECIALISTS", "Chips + rack systems", "Frontier labs / neoclouds", "Lighthouse + co-design", d.b.GOLD),
        ("INTERCONNECT", "Components + systems", "Hyperscalers / clusters", "Long-cycle ecosystem design-in", d.b.CORAL),
    ]
    headers = ["BOTTLENECK", "BUSINESS MODEL", "PRIMARY ICP", "GTM MOTION"]
    widths = [2.45, 2.55, 3.15, 3.60]
    x_positions = [0.62, 3.17, 5.82, 9.07]
    for x, w, header in zip(x_positions, widths, headers):
        d.text(s, header, Inches(x), Inches(1.98), Inches(w), Inches(0.22), size=9.5, color=d.b.MUTED, bold=True, align=PP_ALIGN.CENTER)
    for idx, (lane, model, icp, gtm, color) in enumerate(lanes):
        y = 2.28 + idx * 0.90
        values = [lane, model, icp, gtm]
        for col, (x, w, value) in enumerate(zip(x_positions, widths, values)):
            fill = color if col == 0 else d.b.WHITE
            d.rect(s, Inches(x), Inches(y), Inches(w - 0.10), Inches(0.72), fill, line=d.b.GRID, radius=0.04)
            d.text(s, value, Inches(x + 0.12), Inches(y + 0.16), Inches(w - 0.34), Inches(0.35), size=11.5, color=d.b.NAVY if color != d.b.CORAL or col else d.b.WHITE, bold=col == 0, align=PP_ALIGN.CENTER, shrink=True)
    base.add_citation(d, s, data, data["id"])


def icp_gtm_map(d, data):
    s = d.slide(fill=d.b.WHITE)
    base.add_header(d, s, data)
    rows = [
        ("HYPERSCALERS + LABS", "Token economics, density, custom scale", "Rack-scale proof + capacity", "Co-design / design-in"),
        ("HPC + RESEARCH", "Irregular workloads, fabric behavior", "Real applications + migration", "Early access / integration"),
        ("SOVEREIGN + ENTERPRISE", "Control, programmability, SLAs", "Named-model TCO + operations", "Reference platform / SI"),
        ("EDGE OEMs", "Power, thermals, form factor", "Time-to-production + SDK", "Module / distributor / ISV"),
    ]
    labels = ["BUYER", "TRIGGER PAIN", "PROOF TO BUY", "PRIMARY MOTION"]
    xs = [0.62, 3.22, 6.22, 9.22]
    ws = [2.45, 2.85, 2.85, 3.10]
    for x, w, label in zip(xs, ws, labels):
        d.text(s, label, Inches(x), Inches(1.98), Inches(w), Inches(0.20), size=9.5, color=d.b.MUTED, bold=True, align=PP_ALIGN.CENTER)
    for idx, row in enumerate(rows):
        y = 2.28 + idx * 0.90
        for col, (x, w, value) in enumerate(zip(xs, ws, row)):
            fill = d.b.NAVY if col == 0 else (d.b.LIGHT_TEAL if idx % 2 else d.b.SOFT)
            d.rect(s, Inches(x), Inches(y), Inches(w - 0.10), Inches(0.73), fill, line=d.b.GRID, radius=0.04)
            d.text(s, value, Inches(x + 0.12), Inches(y + 0.15), Inches(w - 0.34), Inches(0.38), size=11.3, color=d.b.WHITE if col == 0 else d.b.INK, bold=col == 0, align=PP_ALIGN.CENTER, shrink=True)
    base.add_citation(d, s, data, data["id"])


def gtm_flywheel(d, data):
    s = d.slide(fill=d.b.SOFT)
    base.add_header(d, s, data)
    steps = [
        ("01", "LIGHTHOUSE", "Prove one painful workload"),
        ("02", "DESIGN-IN", "Integrate software, system, and supply"),
        ("03", "REFERENCE", "Publish repeatable architecture and support"),
        ("04", "REPLICATE", "Scale through OEM, cloud, SI, and ISV"),
    ]
    colors = [d.b.TEAL, d.b.ACCENT, d.b.GOLD, d.b.CORAL]
    for idx, (num, label, text) in enumerate(steps):
        x = 0.64 + idx * 3.07
        d.rect(s, Inches(x), Inches(2.20), Inches(2.65), Inches(2.80), d.b.WHITE, line=d.b.GRID, radius=0.12, shadow=True)
        d.rect(s, Inches(x + 0.86), Inches(2.52), Inches(0.92), Inches(0.92), colors[idx], radius=0.5)
        d.text(s, num, Inches(x + 0.86), Inches(2.81), Inches(0.92), Inches(0.25), size=13, color=d.b.NAVY if idx != 3 else d.b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, Inches(x + 0.25), Inches(3.72), Inches(2.15), Inches(0.28), size=12, color=colors[idx], bold=True, align=PP_ALIGN.CENTER)
        d.text(s, text, Inches(x + 0.27), Inches(4.20), Inches(2.11), Inches(0.55), size=12.5, color=d.b.INK, align=PP_ALIGN.CENTER, shrink=True)
        if idx < 3:
            d.text(s, "→", Inches(x + 2.66), Inches(3.25), Inches(0.42), Inches(0.45), size=24, color=d.b.MUTED, bold=True, align=PP_ALIGN.CENTER)
    d.rect(s, Inches(1.40), Inches(5.40), Inches(10.55), Inches(0.62), d.b.NAVY, radius=0.04)
    d.text(s, "The flywheel only compounds when proof, support, and commercial ownership survive each handoff.", Inches(1.75), Inches(5.58), Inches(9.85), Inches(0.25), size=13, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    base.add_citation(d, s, data, data["id"])


def partner_value(d, data):
    s = d.slide(fill=d.b.NAVY)
    base.add_kicker(d, s, data["kicker"], dark=True)
    d.text(s, data["title"], Inches(0.70), Inches(0.68), Inches(11.7), Inches(0.85), size=30, color=d.b.WHITE, bold=True, shrink=True)
    d.text(s, data["subtitle"], Inches(0.70), Inches(1.54), Inches(11.7), Inches(0.42), size=14, color=d.b.LIGHT_TEAL, shrink=True)
    items = [
        ("PROVE", "Workload benchmark", "Technical risk"),
        ("PACKAGE", "System + software offer", "Integration risk"),
        ("DEPLOY", "Reference architecture", "Execution risk"),
        ("OPERATE", "Support + lifecycle", "Adoption risk"),
    ]
    colors = [d.b.TEAL, d.b.GOLD, d.b.ACCENT, d.b.CORAL]
    for idx, (label, output, risk) in enumerate(items):
        x = 0.72 + idx * 3.07
        d.rect(s, Inches(x), Inches(2.38), Inches(2.68), Inches(2.55), d.b.NAVY_2, line=colors[idx], radius=0.08)
        d.text(s, label, Inches(x + 0.20), Inches(2.72), Inches(2.28), Inches(0.30), size=13, color=colors[idx], bold=True, align=PP_ALIGN.CENTER)
        d.text(s, output, Inches(x + 0.26), Inches(3.32), Inches(2.16), Inches(0.56), size=16, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, f"REDUCES  {risk.upper()}", Inches(x + 0.24), Inches(4.36), Inches(2.20), Inches(0.22), size=9.5, color=d.b.LIGHT_TEAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, Inches(0.72), Inches(5.34), Inches(11.89), Inches(0.68), d.b.TEAL, radius=0.05)
    d.text(s, "The highest-leverage partner converts technical advantage into a repeatable production outcome.", Inches(1.05), Inches(5.54), Inches(11.20), Inches(0.26), size=14, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    base.add_citation(d, s, data, data["id"], dark=True)


def evidence_coverage(d, data):
    s = d.slide(fill=d.b.WHITE)
    base.add_header(d, s, data)
    colors = [d.b.TEAL, d.b.GOLD, d.b.ACCENT, d.b.CORAL]
    for idx, (value, label, note) in enumerate(data["kpis"]):
        x = 0.62 + idx * 2.97
        d.rect(s, Inches(x), Inches(2.00), Inches(2.70), Inches(1.25), d.b.SOFT, line=d.b.GRID, radius=0.06)
        d.text(s, value, Inches(x + 0.18), Inches(2.22), Inches(0.78), Inches(0.42), size=25, color=colors[idx], bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, Inches(x + 1.03), Inches(2.18), Inches(1.45), Inches(0.22), size=10.5, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, note, Inches(x + 1.03), Inches(2.52), Inches(1.47), Inches(0.40), size=9.5, color=d.b.MUTED, shrink=True)
    max_value = max(value for _, value in data["coverage"])
    for idx, (name, value) in enumerate(data["coverage"]):
        col, row = idx // 5, idx % 5
        x = 0.78 + col * 6.02
        y = 3.65 + row * 0.46
        d.text(s, name, Inches(x), Inches(y), Inches(1.32), Inches(0.20), size=9.8, color=d.b.NAVY, bold=True, shrink=True)
        d.rect(s, Inches(x + 1.42), Inches(y + 0.03), Inches(3.62), Inches(0.16), d.b.GRID, radius=0.08)
        d.rect(s, Inches(x + 1.42), Inches(y + 0.03), Inches(3.62 * value / max_value), Inches(0.16), d.b.TEAL if col == 0 else d.b.GOLD, radius=0.08)
        d.text(s, str(value), Inches(x + 5.17), Inches(y - 0.01), Inches(0.38), Inches(0.20), size=9.8, color=d.b.MUTED, bold=True, align=PP_ALIGN.RIGHT)
    base.add_citation(d, s, data, data["id"])


def company_strategy(d, data):
    s = d.slide(fill=d.b.WHITE)
    base.add_header(d, s, data, title_w=Inches(8.10))
    d.rect(s, Inches(10.18), Inches(0.28), Inches(2.42), Inches(0.44), d.b.NAVY, radius=0.14)
    d.text(s, data["tag"], Inches(10.30), Inches(0.37), Inches(2.18), Inches(0.20), size=10.5, color=d.b.TEAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    base.add_site_visual(d, s, data["company"], x=8.48, y=1.92, w=4.15, h=3.86)
    d.text(s, "STRATEGIC WEDGE", Inches(0.72), Inches(2.05), Inches(1.85), Inches(0.22), size=10.5, color=d.b.TEAL, bold=True)
    d.text(s, data["profile"]["WEDGE"], Inches(0.72), Inches(2.38), Inches(7.30), Inches(0.72), size=15, color=d.b.NAVY, bold=True, shrink=True)
    d.rect(s, Inches(0.72), Inches(3.22), Inches(7.30), Inches(0.03), d.b.GRID)
    left = [
        ("BUSINESS MODEL", data["business_model"], d.b.ACCENT),
        ("PRIMARY ICP", data["icp"], d.b.GOLD),
        ("GTM MOTION", data["gtm"], d.b.TEAL),
        ("PARTNER MOVE", data["partner_move"], d.b.CORAL),
    ]
    for idx, (label, value, color) in enumerate(left):
        x = 0.72 + (idx % 2) * 3.72
        y = 3.53 + (idx // 2) * 1.00
        d.text(s, label, Inches(x), Inches(y), Inches(3.30), Inches(0.20), size=9.5, color=color, bold=True)
        d.text(s, value, Inches(x), Inches(y + 0.28), Inches(3.30), Inches(0.45), size=12.5, color=d.b.INK, bold=True, shrink=True)
    d.rect(s, Inches(0.72), Inches(5.62), Inches(7.30), Inches(0.48), d.b.SOFT, line=d.b.GRID, radius=0.04)
    risk_gate = {
        "AXELERA AI": "Repeat deployments + supply scale",
        "TENSTORRENT": "Software adoption + support ownership",
        "NEXTSILICON": "Independent workload validation",
        "FRACTILE": "Tape-out + software readiness",
        "ETCHED": "Model-architecture durability",
        "D-MATRIX": "Volume ramp + customer economics",
        "MATX": "Tape-out + real-system benchmarks",
        "CORNELIS NETWORKS": "Channel coverage + migration proof",
        "LIGHTMATTER": "Qualification + design wins",
        "XSIGHT LABS": "NOS/OEM support maturity",
    }[data["company"].upper()]
    d.text(s, "EVIDENCE / PARTNER", Inches(0.92), Inches(5.77), Inches(1.62), Inches(0.18), size=9.5, color=d.b.MUTED, bold=True)
    d.text(s, data["confidence"], Inches(2.58), Inches(5.73), Inches(1.55), Inches(0.22), size=11.0, color=d.b.NAVY, bold=True)
    d.text(s, "RISK GATE", Inches(4.22), Inches(5.77), Inches(0.75), Inches(0.18), size=9.5, color=d.b.CORAL, bold=True)
    d.text(s, risk_gate, Inches(5.02), Inches(5.73), Inches(2.72), Inches(0.22), size=10.5, color=d.b.MUTED, italic=True, shrink=True)
    base.add_citation(d, s, data, data["id"])


def partner_heatmap(d, data):
    s = d.slide(fill=d.b.WHITE)
    base.add_header(d, s, data)
    headers = ["COMPANY", "DISTRIBUTOR", "SI", "ORCHESTRATOR", "NEXT VALIDATION"]
    xs = [0.62, 2.55, 4.55, 6.25, 8.25]
    ws = [1.80, 1.85, 1.55, 1.85, 4.18]
    for x, w, label in zip(xs, ws, headers):
        d.rect(s, Inches(x), Inches(1.90), Inches(w - 0.08), Inches(0.40), d.b.NAVY)
        d.text(s, label, Inches(x + 0.06), Inches(2.02), Inches(w - 0.20), Inches(0.16), size=8.8, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    fills = {"STRONG": d.b.TEAL, "EMERGING": d.b.LIGHT_TEAL, "VALIDATE": d.b.GOLD, "MONITOR": d.b.CORAL}
    for ridx, row in enumerate(data["rows"]):
        y = 2.34 + ridx * 0.38
        for cidx, (x, w, value) in enumerate(zip(xs, ws, row)):
            fill = d.b.SOFT if cidx in (0, 4) else fills[value]
            d.rect(s, Inches(x), Inches(y), Inches(w - 0.08), Inches(0.32), fill, line=d.b.WHITE)
            d.text(s, value, Inches(x + 0.06), Inches(y + 0.08), Inches(w - 0.20), Inches(0.14), size=8.7, color=d.b.NAVY if value != "MONITOR" else d.b.WHITE, bold=cidx != 4, align=PP_ALIGN.CENTER if cidx != 4 else PP_ALIGN.LEFT, shrink=True)
    base.add_citation(d, s, data, data["id"])


def phase0(d, data):
    s = d.slide(fill=d.b.SOFT)
    base.add_header(d, s, data)
    colors = [d.b.TEAL, d.b.CORAL, d.b.GOLD]
    for idx, (company, archetype, question, lens) in enumerate(data["pilots"]):
        x = 0.62 + idx * 4.04
        d.rect(s, Inches(x), Inches(2.02), Inches(3.70), Inches(3.66), d.b.WHITE, line=d.b.GRID, radius=0.08, shadow=True)
        d.rect(s, Inches(x), Inches(2.02), Inches(3.70), Inches(0.52), colors[idx], radius=0.08)
        d.text(s, company, Inches(x + 0.18), Inches(2.17), Inches(3.34), Inches(0.20), size=12, color=d.b.NAVY if idx != 1 else d.b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, archetype, Inches(x + 0.28), Inches(2.84), Inches(3.14), Inches(0.26), size=10.5, color=colors[idx], bold=True, align=PP_ALIGN.CENTER)
        d.text(s, question, Inches(x + 0.35), Inches(3.40), Inches(3.00), Inches(1.05), size=15, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.rect(s, Inches(x + 0.38), Inches(4.80), Inches(2.94), Inches(0.04), d.b.GRID)
        d.text(s, f"PRIMARY LENS  ·  {lens}", Inches(x + 0.35), Inches(5.10), Inches(3.00), Inches(0.25), size=10, color=d.b.MUTED, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    base.add_citation(d, s, data, data["id"])


def roadmap(d, data):
    s = d.slide(fill=d.b.NAVY)
    base.add_kicker(d, s, data["kicker"], dark=True)
    d.text(s, data["title"], Inches(0.70), Inches(0.64), Inches(11.80), Inches(1.02), size=28, color=d.b.WHITE, bold=True, shrink=True)
    d.text(s, data["subtitle"], Inches(0.70), Inches(1.70), Inches(11.80), Inches(0.34), size=12.5, color=d.b.LIGHT_TEAL, shrink=True)
    items = data["plays"][:3]
    colors = [d.b.TEAL, d.b.GOLD, d.b.CORAL]
    for idx, (item, color) in enumerate(zip(items, colors)):
        x = 0.72 + idx * 4.10
        d.rect(s, Inches(x), Inches(2.34), Inches(3.62), Inches(2.80), d.b.NAVY_2, line=color, radius=0.08)
        d.text(s, item["label"], Inches(x + 0.24), Inches(2.68), Inches(3.14), Inches(0.28), size=11.5, color=color, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, item["text"], Inches(x + 0.34), Inches(3.28), Inches(2.94), Inches(1.30), size=13.5, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    output = data["plays"][3]["text"]
    d.rect(s, Inches(0.72), Inches(5.48), Inches(11.90), Inches(0.62), d.b.TEAL, radius=0.05)
    d.text(s, output, Inches(1.05), Inches(5.66), Inches(11.24), Inches(0.24), size=12.5, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    base.add_citation(d, s, data, data["id"], dark=True)


def section_new(d, data):
    s = d.slide(fill=d.b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, d.b.TEAL)
    base.add_kicker(d, s, data["kicker"], dark=True)
    d.text(s, data["title"], Inches(0.88), Inches(1.50), Inches(10.85), Inches(1.62), size=32, color=d.b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.90), Inches(3.38), Inches(1.75), Inches(0.06), d.b.GOLD)
    d.text(s, data["subtitle"], Inches(0.90), Inches(3.78), Inches(10.45), Inches(0.88), size=18, color=d.b.LIGHT_TEAL, shrink=True)
    base.add_citation(d, s, data, data["id"], dark=True)


def watchlist_new(d, data):
    s = d.slide(fill=d.b.SOFT)
    base.add_header(d, s, data)
    colors = [d.b.GOLD, d.b.CORAL, d.b.TEAL, d.b.ACCENT]
    for idx, item in enumerate(data["watch"]):
        x = 0.62 + (idx % 2) * 6.02
        y = 2.08 + (idx // 2) * 1.88
        d.rect(s, Inches(x), Inches(y), Inches(5.70), Inches(1.55), d.b.WHITE, line=d.b.GRID, radius=0.06)
        d.rect(s, Inches(x), Inches(y), Inches(1.66), Inches(1.55), colors[idx], radius=0.06)
        d.text(s, item["stage"], Inches(x + 0.14), Inches(y + 0.49), Inches(1.38), Inches(0.48), size=10.5, color=d.b.NAVY if idx != 1 else d.b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, item["companies"], Inches(x + 1.92), Inches(y + 0.28), Inches(3.44), Inches(0.34), size=13.2, color=d.b.NAVY, bold=True, shrink=True)
        d.text(s, item["event"], Inches(x + 1.92), Inches(y + 0.83), Inches(3.44), Inches(0.40), size=11.5, color=d.b.MUTED, shrink=True)
    base.add_citation(d, s, data, data["id"])


def conclusion_new(d, data):
    s = d.slide(fill=d.b.NAVY)
    base.add_kicker(d, s, data["kicker"], dark=True)
    d.text(s, data["title"], Inches(0.72), Inches(0.82), Inches(11.80), Inches(1.20), size=30, color=d.b.WHITE, bold=True, shrink=True)
    d.text(s, data["subtitle"], Inches(0.72), Inches(2.02), Inches(11.40), Inches(0.44), size=14, color=d.b.LIGHT_TEAL, shrink=True)
    moves = [
        ("PUBLIC EVIDENCE", "Prioritizes what to test"),
        ("PHASE 0", "Calibrates the rubric"),
        ("LOCAL PROFILE", "Determines who to partner with"),
    ]
    colors = [d.b.TEAL, d.b.GOLD, d.b.CORAL]
    for idx, ((label, text), color) in enumerate(zip(moves, colors)):
        x = 0.72 + idx * 4.10
        d.rect(s, Inches(x), Inches(2.90), Inches(3.62), Inches(1.36), d.b.NAVY_2, line=color, radius=0.06)
        d.text(s, label, Inches(x + 0.24), Inches(3.17), Inches(3.14), Inches(0.25), size=11, color=color, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, text, Inches(x + 0.28), Inches(3.63), Inches(3.06), Inches(0.35), size=13.5, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, Inches(0.72), Inches(4.80), Inches(11.90), Inches(0.82), d.b.TEAL, radius=0.05)
    d.text(s, data["takeaway"], Inches(1.05), Inches(5.05), Inches(11.24), Inches(0.30), size=14.5, color=d.b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    base.add_citation(d, s, data, data["id"], dark=True)


def build():
    d = base.Deck(footer="Semiconductor Startups 2026 · Evidence-Led Strategy")
    handlers = {
        "cover_mosaic": cover_mosaic,
        "decision_dashboard": decision_dashboard,
        "portfolio_posture": portfolio_posture,
        "thesis": base.thesis,
        "business_system": business_system,
        "icp_gtm_map": icp_gtm_map,
        "gtm_flywheel": gtm_flywheel,
        "partner_value": partner_value,
        "evidence_coverage": evidence_coverage,
        "comparison": base.comparison,
        "section": section_new,
        "company_strategy": company_strategy,
        "gtm-scorecard": base.gtm_scorecard,
        "partner_heatmap": partner_heatmap,
        "economics": base.economics,
        "phase0": phase0,
        "roadmap": roadmap,
        "watchlist": watchlist_new,
        "risks": base.risks,
        "conclusion": conclusion_new,
    }
    for slide in base.SLIDES:
        handlers[slide["layout"]](d, slide)
    if d.n != 36:
        raise RuntimeError(f"Expected 36 slides, built {d.n}")
    d.save(base.OUT)


if __name__ == "__main__":
    build()
