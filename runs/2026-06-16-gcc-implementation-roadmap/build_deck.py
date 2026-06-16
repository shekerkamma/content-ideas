#!/usr/bin/env python3
"""FPT Software — GCC Implementation Roadmap deck builder. 17 slides."""
import sys
sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Brand, Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor

OUT   = "/home/shekerk/content-ideas/runs/2026-06-16-gcc-implementation-roadmap/gcc-roadmap-deck-draft.pptx"
TOTAL = 17
FOOTER = "FPT Software · GCC Implementation Roadmap · Jun 2026"

d = Deck(footer=FOOTER)
b = d.b
W, H, M, CW = d.W, d.H, d.M, d.CW

# ── helpers ──────────────────────────────────────────────────────────────────

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

def phase_chip(s, cx, cy, cw, label, sublabel, fill=None):
    fill = fill or b.NAVY_2
    d.rect(s, cx, cy, cw, Inches(0.52), fill, radius=0.04)
    d.text(s, label, cx + Inches(0.1), cy + Inches(0.04),
           cw - Inches(0.15), Inches(0.26), size=11, color=b.TEAL, bold=True,
           align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, sublabel, cx + Inches(0.1), cy + Inches(0.28),
           cw - Inches(0.15), Inches(0.2), size=9, color=b.MUTED,
           align=PP_ALIGN.CENTER, shrink=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.rect(s, W - Inches(0.25), 0, Inches(0.25), H, b.NAVY_2)
d.rect(s, W - Inches(0.28), 0, Inches(0.06), H, b.TEAL)
d.text(s, "GCC IMPLEMENTATION ROADMAP", M, Inches(0.85), CW, Inches(0.4),
       size=13, color=b.TEAL, bold=True)
d.text(s, "FPT Software", M, Inches(1.32), CW - Inches(4), Inches(0.95),
       size=52, color=b.WHITE, bold=True, shrink=True)
d.rect(s, M, Inches(2.38), Inches(5), Inches(0.06), b.TEAL)
d.text(s, "From AI Mandate to Production AI — The Full Delivery Journey",
       M, Inches(2.55), CW - Inches(3), Inches(0.75),
       size=18, color=b.LIGHT_TEAL, shrink=True)
# Three tier chips
tiers = [
    ("AI READINESS SPRINT", "Wks 1–8 · $150K–$250K"),
    ("TRANSFORMATION PROGRAM", "$2M–$10M / Year"),
    ("STRATEGIC AI PARTNERSHIP", "$10M–$30M · Multi-Year"),
]
chip_w = (CW - Inches(0.3)) / 3
for i, (name, price) in enumerate(tiers):
    cx = M + i * (chip_w + Inches(0.15))
    d.rect(s, cx, Inches(3.62), chip_w, Inches(0.82), b.NAVY_2, radius=0.04)
    d.rect(s, cx, Inches(3.62), chip_w, Inches(0.05), b.TEAL if i < 2 else b.GOLD)
    d.text(s, name, cx + Inches(0.12), Inches(3.7), chip_w - Inches(0.2), Inches(0.32),
           size=10, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, price, cx + Inches(0.12), Inches(4.02), chip_w - Inches(0.2), Inches(0.3),
           size=10, color=b.GOLD, align=PP_ALIGN.CENTER, shrink=True)
d.text(s, "Modernize  ·  Activate  ·  Innovate", M, Inches(4.65), CW, Inches(0.38),
       size=16, color=b.TEAL, bold=True)
d.text(s, "Prepared by Srikumar V R  ·  Director Strategic BD, FPT Software  ·  Jun 2026",
       M, Inches(5.15), CW, Inches(0.32), size=12, color=b.MUTED)
d.footer(s, 1, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROMISE: 18 months to production AI
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "18 Months from AI Mandate to Strategic AI Partner Status", "Executive Summary")
promise_items = [
    (b.NAVY, b.TEAL,
     "THE PROBLEM",
     "GCC heads face a board AI mandate with an 18-month delivery expectation and no trusted technology partner who can cover legacy modernization, production AI deployment, vertical platforms, and managed services in one programme."),
    (b.ACCENT, b.WHITE,
     "THE FPT ANSWER",
     "A single integrated delivery programme spanning three phases: AI Readiness Sprint → Transformation Program → Strategic AI Partnership. Each phase builds on the last. The GCC's AI capability compounds — and so does FPT's contract value."),
    (b.NAVY_2, b.TEAL,
     "WHAT GCC LEADERSHIP PRESENTS TO GLOBAL PARENT",
     "A credible, costed implementation roadmap with stage-gates, measurable milestones, and a partner who has delivered $256M AI transformation programmes and serves 130+ Fortune 500 companies globally."),
]
for i, (fill, accent, title, body) in enumerate(promise_items):
    py = Inches(1.72) + i * Inches(1.72)
    ph = Inches(1.58)
    d.rect(s, M, py, CW, ph, fill, radius=0.03)
    d.rect(s, M, py, CW, Inches(0.05), accent)
    d.text(s, title, M + Inches(0.18), py + Inches(0.1),
           Inches(3.5), Inches(0.3), size=11, color=accent, bold=True)
    d.text(s, body, M + Inches(0.18), py + Inches(0.44),
           CW - Inches(0.3), ph - Inches(0.5),
           size=12.5, color=b.WHITE, shrink=True)
d.footer(s, 2, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — THREE LAYERS: Modernize · Activate · Innovate
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Three Capability Layers · Deployed in Sequence · Compounding in Value",
         "Implementation Architecture")
layers = [
    (b.NAVY, b.TEAL, "LAYER 1 — MODERNIZE",
     "Foundation: Remove the blockers",
     [("EMT", "End-to-end legacy modernization platform — assessment to rewrite"),
      ("xMainframe", "AI mainframe migration · 30% faster onboarding · 90% accuracy · monthly → weekly cycles"),
      ("CodeVista", "AI developer productivity · 30% efficiency gain · 6,000 man-months saved · 1.5M lines generated"),
      ("CASAN Framework", "Scalable assessment methodology · strategy to execution in one framework"),
      ("Data Readiness", "Data platform setup, cloud migration, governance layer")]),
    (b.NAVY_2, b.GOLD, "LAYER 2 — ACTIVATE",
     "Intelligence: Put AI into production",
     [("FleziPT", "Enterprise AI deployment — data readiness, model integration, monitoring, full lifecycle"),
      ("KnowMed.ai", "Healthcare & life sciences vertical AI — HIPAA compliant"),
      ("Virtual Factory", "Manufacturing AI — anomaly detection, computer vision, predictive maintenance"),
      ("Edge AI Orchestrator", "Low-latency on-device AI — automotive, IoT, Qualcomm/NVIDIA"),
      ("AI Testing Loop", "80% manual testing automated · V-Model & A-SPICE compliant")]),
    (b.ACCENT, b.WHITE, "LAYER 3 — INNOVATE",
     "Innovation: Create IP together",
     [("Co-Development", "Joint AI module development — GCC's domain expertise + FPT's engineering depth"),
      ("White-Label Packaging", "GCC owns branded AI modules built on FPT platforms — resellable IP"),
      ("CxO Quarterly Roadmap", "Bi-directional strategic planning — FPT's global pipeline feeds GCC's roadmap"),
      ("DX Garage", "Innovation studio: rapid prototyping of next-generation AI use cases"),
      ("Strategic Partnership", "Preferred technology partner status · $10M–$30M · multi-year locked-in")]),
]
col_w = (CW - Inches(0.3)) / 3
for i, (fill, accent, layer_title, subtitle, items) in enumerate(layers):
    cx = M + i * (col_w + Inches(0.15))
    cy = Inches(1.72)
    ch = Inches(5.1)
    d.rect(s, cx, cy, col_w, ch, fill, radius=0.03)
    d.rect(s, cx, cy, col_w, Inches(0.06), accent)
    d.text(s, layer_title, cx + Inches(0.12), cy + Inches(0.1),
           col_w - Inches(0.2), Inches(0.3), size=11, color=accent, bold=True, shrink=True)
    d.text(s, subtitle, cx + Inches(0.12), cy + Inches(0.42),
           col_w - Inches(0.2), Inches(0.3), size=11, color=b.LIGHT_TEAL if fill != b.ACCENT else b.WHITE)
    d.rect(s, cx + Inches(0.3), cy + Inches(0.75), col_w - Inches(0.6), Inches(0.03), accent)
    for j, (pname, pdesc) in enumerate(items):
        iy = cy + Inches(0.9) + j * Inches(0.82)
        d.rect(s, cx + Inches(0.12), iy, col_w - Inches(0.22), Inches(0.74),
               b.NAVY if fill == b.ACCENT else b.NAVY_2, radius=0.02)
        tc = b.LIGHT_TEAL if fill != b.ACCENT else b.LIGHT_TEAL
        d.text(s, pname, cx + Inches(0.2), iy + Inches(0.04),
               col_w - Inches(0.35), Inches(0.22), size=10, color=b.TEAL, bold=True, shrink=True)
        d.text(s, pdesc, cx + Inches(0.2), iy + Inches(0.26),
               col_w - Inches(0.35), Inches(0.42), size=9, color=tc, shrink=True)
d.footer(s, 3, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — MASTER ROADMAP MATRIX (centrepiece)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "GCC Implementation Roadmap — Time × Capability Matrix",
       M, Inches(0.28), CW, Inches(0.48), size=22, color=b.WHITE, bold=True, shrink=True)

# Phase header row
phase_cols = [
    ("PHASE 1\nAI READINESS SPRINT", "Wks 1–8", b.TEAL),
    ("PHASE 2\nTRANSFORMATION YR 1", "Months 3–12", b.TEAL),
    ("PHASE 3\nTRANSFORMATION YR 2", "Months 12–24", b.TEAL),
    ("PHASE 4\nSTRATEGIC PARTNERSHIP", "Year 2+", b.GOLD),
]
label_col_w = Inches(1.65)
phase_col_w = (CW - label_col_w - Inches(0.12)) / 4
header_h = Inches(0.65)
top = Inches(0.88)

# Layer label col header
d.rect(s, M, top, label_col_w, header_h, b.NAVY_2)

# Phase headers
for i, (title, sub, col) in enumerate(phase_cols):
    px = M + label_col_w + Inches(0.04) + i * (phase_col_w + Inches(0.04))
    d.rect(s, px, top, phase_col_w, header_h, b.NAVY_2, radius=0.02)
    d.rect(s, px, top, phase_col_w, Inches(0.04), col)
    d.text(s, title, px + Inches(0.06), top + Inches(0.05),
           phase_col_w - Inches(0.1), Inches(0.38),
           size=9, color=col, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, sub, px + Inches(0.06), top + Inches(0.44),
           phase_col_w - Inches(0.1), Inches(0.18),
           size=8.5, color=b.MUTED, align=PP_ALIGN.CENTER)

# Layer rows
layer_fills = [b.TEAL, b.GOLD, b.ACCENT]
layer_text_fills = [b.NAVY, b.NAVY, b.WHITE]
layer_rows_data = [
    # (label, [(phase1_content, phase2_content, phase3_content, phase4_content)])
    ("MODERNIZE\nFoundation",
     ["CASAN Assessment\nData Readiness Audit\nCloud Migration Scoping\nxMainframe Baseline",
      "EMT Legacy Modernization\nxMainframe Migration Live\nCodeVista Developer AI\nData Platform Built",
      "Modernization Complete\nLegacy Tech Debt Cleared\nCloud-Native Stack\nCodeVista at Scale",
      "Foundation Hardened\nIP Library Growing\nDev Velocity Baseline\nPlatform Lock-In"]),
    ("ACTIVATE\nIntelligence",
     ["FleziPT PoC (1 use case)\nVertical AI Scoped\nAI Testing Framework\nModel Selection",
      "FleziPT Production\nVertical AI Live\n(KnowMed / VFactory)\nAI Testing Automated",
      "2nd Vertical AI Live\nEdge AI Deployed\nAI Testing at 80%\nMLOps Pipeline Stable",
      "AI Platform as Standard\nAll Verticals Active\nSelf-Improving Models\nAI-First Operations"]),
    ("INNOVATE\nInnovation",
     ["Innovation Agenda Set\nCxO Roadmap Drafted\nIP Framework Agreed\nDX Garage Scoped",
      "First Co-Dev Sprint\nQuarterly CxO Review\nWhite-Label Module v1\nDX Garage Running",
      "Co-Dev Cycle 2\nPatent/IP Filing\nWhite-Label v2 Live\nGlobal Parent Briefed",
      "Strategic Partnership\nJoint AI Products\nResellable IP Portfolio\nPreferred Partner Status"]),
]
layer_h = (H - top - header_h - Inches(0.52) - Inches(0.08)) / 3

for ri, (layer_label, cells) in enumerate(layer_rows_data):
    ry = top + header_h + Inches(0.04) + ri * (layer_h + Inches(0.04))
    # Layer label cell
    d.rect(s, M, ry, label_col_w, layer_h, b.NAVY_2, radius=0.02)
    d.rect(s, M, ry, Inches(0.05), layer_h, layer_fills[ri])
    d.text(s, layer_label, M + Inches(0.12), ry + Inches(0.08),
           label_col_w - Inches(0.18), layer_h - Inches(0.16),
           size=10, color=layer_fills[ri], bold=True,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    # Phase cells
    for ci, cell_content in enumerate(cells):
        px = M + label_col_w + Inches(0.04) + ci * (phase_col_w + Inches(0.04))
        cell_fill = b.NAVY_2
        d.rect(s, px, ry, phase_col_w, layer_h, cell_fill, radius=0.02)
        d.rect(s, px, ry, phase_col_w, Inches(0.03), layer_fills[ri])
        d.text(s, cell_content, px + Inches(0.08), ry + Inches(0.08),
               phase_col_w - Inches(0.14), layer_h - Inches(0.16),
               size=9.5, color=b.LIGHT_TEAL, shrink=True)

d.footer(s, 4, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — PHASE 1: AI READINESS SPRINT (Weeks 1–8)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Phase 1 — AI Readiness Sprint · Weeks 1–8 · $150K–$250K",
         "The Entry Point That Opens Everything Else")
half = (CW - Inches(0.2)) / 2
left_items = [
    ("CASAN Framework Assessment",
     "FPT's structured AI readiness methodology — maps GCC's current state across data, architecture, people, and use-case pipeline. Produces a prioritised AI roadmap the GCC head can defend to global parent."),
    ("Data Readiness Audit",
     "Assess existing data infrastructure against production AI requirements. Identifies quick wins and blockers. Output: data gap report + remediation plan with FPT's data platform team."),
    ("Legacy Modernization Scoping",
     "xMainframe baseline assessment — maps mainframe workloads to AI-assisted migration paths. Quantifies the man-month savings achievable with CodeVista and EMT in Phase 2."),
    ("FleziPT Proof-of-Concept",
     "One high-value use case deployed in FleziPT within 6 weeks. Not a demo — a live PoC with real data, measurable output, and a production deployment plan. This is the artefact that justifies Phase 2 budget."),
]
right_items = [
    ("Deliverable at Week 8", "AI Transformation Roadmap (board-ready) · PoC results with production pathway · Transformation Program business case · Signed Transformation Program Statement of Work"),
    ("Who's Involved from FPT", "CASAN Framework lead · FleziPT solution architect · xMainframe specialist · Data platform engineer · Srikumar as programme sponsor and GCC relationship owner"),
    ("GCC Risk at This Stage", "Low — fixed price, fixed scope, fixed timeline. No open-ended commitment. Worst case: GCC has a credible AI roadmap and PoC results at $150K–$250K. Best case: Transformation Program signed at Week 8."),
    ("Reference Proof Points", "FPT has run 1,100+ client engagements globally. The Sprint model is validated. $10M+ contracts doubled YoY in 2025 — most originated as Readiness Sprints."),
]
for i, (title, body) in enumerate(left_items):
    iy = Inches(1.72) + i * Inches(1.2)
    d.rect(s, M, iy, half, Inches(1.12), b.SOFT, radius=0.03)
    d.rect(s, M, iy, Inches(0.06), Inches(1.12), b.TEAL)
    d.text(s, title, M + Inches(0.14), iy + Inches(0.06),
           half - Inches(0.2), Inches(0.28), size=11, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, M + Inches(0.14), iy + Inches(0.36),
           half - Inches(0.2), Inches(0.7), size=10, color=b.INK, shrink=True)
rx = M + half + Inches(0.2)
rw = half
for i, (title, body) in enumerate(right_items):
    iy = Inches(1.72) + i * Inches(1.2)
    fill = b.NAVY if i == 0 else (b.NAVY_2 if i == 1 else (b.SOFT if i == 2 else b.TEAL))
    tc = b.TEAL if fill in (b.NAVY, b.NAVY_2) else b.NAVY
    bc = b.LIGHT_TEAL if fill in (b.NAVY, b.NAVY_2) else b.INK
    d.rect(s, rx, iy, rw, Inches(1.12), fill, radius=0.03)
    d.text(s, title, rx + Inches(0.14), iy + Inches(0.06),
           rw - Inches(0.2), Inches(0.28), size=11, color=tc, bold=True, shrink=True)
    d.text(s, body, rx + Inches(0.14), iy + Inches(0.36),
           rw - Inches(0.2), Inches(0.7), size=10, color=bc, shrink=True)
d.footer(s, 5, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — PHASE 2: TRANSFORMATION PROGRAM YEAR 1 (Months 3–12)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Phase 2 — Transformation Program Year 1 · Months 3–12 · $2M–$10M ARR",
         "Modernize + Activate: Legacy Out, Production AI In")
rows = [
    ["Work Stream", "FPT Platform", "What Gets Delivered", "Milestone"],
    ["Legacy Modernization",
     "EMT + xMainframe + CodeVista",
     "AI-assisted mainframe migration · 30% faster onboarding · 90% accuracy · developer AI tooling across GCC engineering team",
     "Month 6: First workload migrated · Month 12: Legacy debt cleared"],
    ["Data Platform",
     "FleziPT data layer + cloud infra",
     "Production data pipeline · data governance · model training infrastructure · integration with GCC's existing cloud (AWS / Azure / GCP)",
     "Month 4: Data pipeline live · Month 8: Model training operational"],
    ["Production AI Deployment",
     "FleziPT",
     "2–3 AI use cases in full production · monitoring dashboards · model retraining cycles · audit trail for regulated industries",
     "Month 6: First use case live · Month 10: 2nd use case live"],
    ["Vertical AI Platform",
     "KnowMed.ai / Virtual Factory / Edge AI",
     "Industry-specific AI platform deployed inside GCC's domain (healthcare / manufacturing / automotive / energy) with domain-trained models",
     "Month 9: Vertical platform operational · Month 12: First vertical results"],
    ["AI Quality & Compliance",
     "AI Testing Loop",
     "80% manual testing automated · V-Model and A-SPICE compliance traceability · regulated industry audit readiness",
     "Month 5: Test automation live · Month 12: Full compliance coverage"],
    ["Managed Services",
     "FPT AMS team",
     "24/7 AI operations support · SLA-backed uptime · model drift monitoring · monthly performance reviews with Srikumar",
     "Month 3: AMS contract active · ongoing through Year 2+"],
]
col_w = [Inches(2.3), Inches(2.3), Inches(5.4), Inches(2.0)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(0.64), header_fill=b.NAVY, alt_fill=True, text_size=10, header_text_size=11)
d.footer(s, 6, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — PHASE 3: TRANSFORMATION YEAR 2 (Months 12–24)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Phase 3 — Transformation Program Year 2 · Months 12–24 · $6M–$15M ARR",
         "Activate at Scale + Innovate: AI Becomes the GCC's Competitive Advantage")
yr2_cards = [
    (b.NAVY, b.TEAL, "SCALE AI ACROSS VERTICALS",
     "Deploy second and third vertical AI platforms. If Year 1 was KnowMed.ai, Year 2 adds Virtual Factory or Edge AI Orchestrator. Each new vertical compounds the ROI case for the global parent."),
    (b.NAVY_2, b.TEAL, "ACTIVATE EDGE & IOT AI",
     "Edge AI Orchestrator deployed on Qualcomm/NVIDIA hardware. Low-latency on-device AI for manufacturing, automotive, and field operations. GCC becomes the AI edge competence centre for the global group."),
    (b.ACCENT, b.WHITE, "BEGIN CO-DEVELOPMENT (INNOVATE LAYER)",
     "First joint AI module built — GCC's domain expertise + FPT's engineering. Legal framework agreed. IP ownership structure set. DX Garage running rapid prototyping cycles."),
    (b.NAVY, b.TEAL, "WHITE-LABEL MODULE v1",
     "First AI module packaged for the GCC to own and potentially resell to their global parent's other subsidiaries. Turns FPT's engineering into GCC's IP. Revenue tail independent of FPT licence fees."),
    (b.NAVY_2, b.GOLD, "GLOBAL PARENT BRIEFING",
     "Srikumar leads a CxO-level presentation to the global parent. Shows 24-month results: AI in production, legacy cleared, developer velocity gains, vertical AI ROI, and the co-development IP pipeline."),
    (b.TEAL, b.NAVY, "STRATEGIC PARTNERSHIP CONVERSION",
     "$10M–$30M multi-year contract. Platform lock-in. Preferred partner status. GCC becomes a flagship reference for FPT's India GCC practice — unlocking the next 5 GCC introductions from this one."),
]
card_w = (CW - Inches(0.3)) / 3
card_h = Inches(2.3)
for i, (fill, accent, title, body) in enumerate(yr2_cards):
    col = i % 3
    row = i // 3
    cx = M + col * (card_w + Inches(0.15))
    cy = Inches(1.72) + row * (card_h + Inches(0.14))
    d.rect(s, cx, cy, card_w, card_h, fill, radius=0.03)
    d.rect(s, cx, cy, card_w, Inches(0.06), accent)
    d.text(s, title, cx + Inches(0.12), cy + Inches(0.1),
           card_w - Inches(0.2), Inches(0.32), size=10.5, color=accent, bold=True, shrink=True)
    d.text(s, body, cx + Inches(0.12), cy + Inches(0.46),
           card_w - Inches(0.2), card_h - Inches(0.55),
           size=10.5, color=b.WHITE if fill != b.TEAL else b.NAVY, shrink=True)
d.footer(s, 7, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — PHASE 4: STRATEGIC AI PARTNERSHIP (Year 2+)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "Phase 4 — Strategic AI Partnership · Year 2+ · $10M–$30M · Multi-Year",
       M, Inches(0.28), CW, Inches(0.52), size=20, color=b.WHITE, bold=True, shrink=True)
d.text(s, "The GCC is now FPT's reference client in India. FPT is the GCC's preferred AI partner globally.",
       M, Inches(0.88), CW, Inches(0.35), size=13, color=b.LIGHT_TEAL)
p4_rows = [
    ["Partnership Element", "What It Means for the GCC", "What It Means for FPT"],
    ["Multi-year MSA", "Budget certainty · no annual renegotiation · platform roadmap locked", "Predictable ARR · deepening platform dependency · flagship reference"],
    ["Co-Development Programme", "Owns jointly-developed AI modules · builds resellable IP · domain AI leadership", "Engineering capacity deployed on sticky, high-value co-creation work"],
    ["CxO Quarterly Roadmap", "GCC's AI agenda shaped by FPT's global technology pipeline · first-mover access", "Strategy influence at board level · early signal of next expansion opportunity"],
    ["Preferred Partner Status", "Global parent recognises FPT as primary AI SI for the group's India operations", "Srikumar's network effect: one GCC win → 3–5 referrals to peer GCCs"],
    ["IP Revenue Tail", "White-label AI modules generate revenue independent of FPT services", "FPT platform embedded in client-owned products → long-term ecosystem lock-in"],
    ["Innovation Access", "DX Garage running continuously · FPT R&D pipeline input · joint patent potential", "GCC acts as live lab for new FPT platform features before global rollout"],
]
col_w = [Inches(2.8), Inches(4.6), Inches(4.6)]
table_rows(s, p4_rows, M, Inches(1.42), col_w,
           row_h=Inches(0.72), header_fill=b.TEAL, alt_fill=True, text_size=10.5, header_text_size=11)
d.footer(s, 8, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — MODERNIZE LAYER DEEP DIVE
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "MODERNIZE — FPT's Legacy Modernization Stack · The Foundation Layer",
         "Why Legacy Blocks AI — and How FPT Removes the Blocker")
d.rect(s, M, Inches(1.72), CW, Inches(0.52), b.NAVY, radius=0.03)
d.text(s, "The single most common reason GCC AI initiatives fail to reach production: the underlying tech stack cannot support production AI workloads.",
       M + Inches(0.18), Inches(1.78), CW - Inches(0.3), Inches(0.4),
       size=12.5, color=b.LIGHT_TEAL, shrink=True)
mod_rows = [
    ["FPT Platform", "What It Does", "Proof Metric", "Typical Timeline"],
    ["EMT\n(Engineering Modernization Technologies)",
     "End-to-end legacy modernization lifecycle — codebase assessment, architecture analysis, automated refactoring, cloud-native rewrite, testing, deployment",
     "Proven across 1,100+ client engagements globally",
     "3–9 months depending on estate size"],
    ["xMainframe",
     "AI-powered mainframe modernization — translates COBOL/PL1 to modern languages, preserves business logic, maintains data integrity across migration",
     "30% faster onboarding · 90% code accuracy · transforms monthly data cycles to weekly",
     "6–18 months for large mainframe estate"],
    ["CodeVista",
     "AI developer productivity tooling — code generation, intelligent completion, automated review, documentation generation deployed across the GCC engineering team",
     "30% developer efficiency gain · 1.5M lines generated · 6,000 man-months saved across engagements",
     "Week 4 of Sprint → live during Transformation Yr 1"],
    ["CASAN Framework",
     "Assessment methodology — Scalable engineering + domain expertise + data + advanced AI. Maps current state, identifies gaps, sequences the modernization roadmap",
     "Used as the entry point for all FPT enterprise engagements",
     "2–4 weeks in Sprint phase"],
    ["Data Platform",
     "Cloud data infrastructure — lake, warehouse, pipeline, governance layer. Built on GCC's existing cloud provider (AWS / Azure / GCP) to avoid vendor lock-in",
     "Required foundation for FleziPT production AI deployment",
     "Months 3–6 of Transformation Yr 1"],
]
col_w = [Inches(2.4), Inches(5.2), Inches(2.8), Inches(1.7)]
table_rows(s, mod_rows, M, Inches(2.42), col_w,
           row_h=Inches(0.72), header_fill=b.NAVY, alt_fill=True, text_size=10, header_text_size=11)
d.footer(s, 9, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — ACTIVATE LAYER DEEP DIVE
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "ACTIVATE — FPT's AI Production Stack · Intelligence Layer",
         "Production AI — Not Pilots, Not Demos, Not Frameworks")
act_cards = [
    ("FleziPT", b.NAVY, b.TEAL,
     "Enterprise AI production platform: data readiness → model integration → validation → operational monitoring → retraining. Every AI use case goes through FleziPT. Gives GCC full lifecycle control — not a black box.",
     "Audit trail · compliance traceability · model drift alerts · 99.9% uptime SLA"),
    ("KnowMed.ai", b.NAVY_2, b.TEAL,
     "Healthcare & life sciences vertical AI: clinical documentation automation, patient intake AI, HIPAA-compliant data handling, hospital operations intelligence. Deployed inside GCC as a managed platform.",
     "GE Healthcare reference · hospital operations + patient care acceleration"),
    ("Virtual Factory", b.NAVY, b.TEAL,
     "Manufacturing AI: real-time computer vision for anomaly detection, predictive maintenance on plant equipment, quality inspection automation, safety surveillance. Runs on existing plant sensor infrastructure.",
     "80% cost reduction in factory safety · 70% manual monitoring effort eliminated"),
    ("Edge AI Orchestrator", b.NAVY_2, b.GOLD,
     "Multi-agent edge AI on Qualcomm/NVIDIA hardware. Low-latency on-device inference for automotive, IoT, field operations. GCC becomes the AI edge centre of excellence for the global group.",
     "Showcased at CES 2026 · automotive + industrial IoT validated"),
    ("AI Testing Loop", b.ACCENT, b.WHITE,
     "Industrialised AI testing: 80% of manual testing automated, V-Model and A-SPICE compliance traceability, regression testing across model versions, audit-ready reports for regulated industries.",
     "80% manual testing automated · AWS-based · V-Model / A-SPICE compliant"),
    ("FleziPT AI Factory", b.NAVY, b.TEAL,
     "FPT's global AI production infrastructure: 1,100B+ tokens processed, 70+ fine-tuned models, 18,000+ engineers on platform. GCC taps into this at the speed of a model API, not a build-from-scratch project.",
     "1,100B+ tokens · 70+ fine-tuned models · 43 AI cloud services"),
]
cw2 = (CW - Inches(0.3)) / 3
ch2 = Inches(2.28)
for i, (title, fill, accent, body, proof) in enumerate(act_cards):
    col = i % 3
    row = i // 3
    cx = M + col * (cw2 + Inches(0.15))
    cy = Inches(1.72) + row * (ch2 + Inches(0.14))
    d.rect(s, cx, cy, cw2, ch2, fill, radius=0.03)
    d.rect(s, cx, cy, cw2, Inches(0.06), accent)
    d.text(s, title, cx + Inches(0.12), cy + Inches(0.1),
           cw2 - Inches(0.2), Inches(0.3), size=12, color=accent, bold=True)
    d.text(s, body, cx + Inches(0.12), cy + Inches(0.44),
           cw2 - Inches(0.2), Inches(1.12), size=10, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, cx + Inches(0.2), cy + ch2 - Inches(0.52), cw2 - Inches(0.35), Inches(0.02), accent)
    d.text(s, proof, cx + Inches(0.12), cy + ch2 - Inches(0.48),
           cw2 - Inches(0.2), Inches(0.4), size=9, color=b.MUTED, shrink=True)
d.footer(s, 10, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — INNOVATE LAYER DEEP DIVE
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "INNOVATE — Co-Development, IP Creation, Strategic Partnership",
         "The Layer That Transforms FPT from Vendor to Partner")
d.rect(s, M, Inches(1.72), CW, Inches(0.48), b.NAVY, radius=0.03)
d.text(s, "Most GCC-SI relationships stay transactional. The INNOVATE layer is where they become strategic — GCC owns IP, FPT is embedded in the roadmap, and both parties have skin in each other's success.",
       M + Inches(0.18), Inches(1.78), CW - Inches(0.3), Inches(0.38),
       size=12, color=b.LIGHT_TEAL, shrink=True)
innov_items = [
    ("DX Garage", b.NAVY_2, b.TEAL,
     "FPT's innovation studio embedded inside the GCC. Rapid prototyping of next-generation AI use cases — 2-week sprints from concept to working prototype. GCC engineers participate. Domain expertise meets FPT engineering depth.",
     "Activated from Month 12 of Transformation Program"),
    ("Co-Development Programme", b.NAVY, b.TEAL,
     "Joint AI module development. Legal framework: IP ownership split agreed upfront. GCC contributes domain expertise, training data, and business validation. FPT contributes engineering, platform, and AI tooling. Output: modules the GCC owns.",
     "Year 2 onwards — structured as quarterly sprints"),
    ("White-Label AI Modules", b.NAVY_2, b.GOLD,
     "AI modules built jointly are packaged for the GCC to own and market. Can be licensed to the global parent's other subsidiaries. Turns the engagement into a revenue stream for the GCC — independent of FPT's ongoing fees.",
     "First module typically ready Month 18–24"),
    ("CxO Quarterly Roadmap", b.NAVY, b.TEAL,
     "Bi-directional strategic planning: FPT shares its global technology pipeline (what's coming in FleziPT, new vertical AI, Edge AI developments) and the GCC shapes FPT's India product roadmap. Both parties plan 12 months ahead together.",
     "Starts at contract signing — quarterly cadence"),
    ("Preferred Partner Status", b.ACCENT, b.WHITE,
     "Formalised in the Strategic AI Partnership MSA. FPT is the named preferred AI technology partner for the GCC. Global parent endorsement obtained. Srikumar's network effect activates — this GCC becomes the reference that opens the next 5.",
     "Triggered at Strategic Partnership conversion (Year 2)"),
    ("Global Patent & IP Filing", b.NAVY_2, b.TEAL,
     "Where co-development produces novel AI methods, FPT supports the GCC in joint patent filing. GCC gains IP assets. FPT gains a co-inventor relationship. Both benefit from the innovation narrative with global parent and regulators.",
     "Case-by-case — typically Year 2–3"),
]
iw = (CW - Inches(0.3)) / 3
ih = Inches(2.28)
for i, (title, fill, accent, body, note) in enumerate(innov_items):
    col = i % 3
    row = i // 3
    cx = M + col * (iw + Inches(0.15))
    cy = Inches(2.38) + row * (ih + Inches(0.14))
    d.rect(s, cx, cy, iw, ih, fill, radius=0.03)
    d.rect(s, cx, cy, iw, Inches(0.06), accent)
    d.text(s, title, cx + Inches(0.12), cy + Inches(0.1),
           iw - Inches(0.2), Inches(0.3), size=11, color=accent, bold=True, shrink=True)
    d.text(s, body, cx + Inches(0.12), cy + Inches(0.44),
           iw - Inches(0.2), Inches(1.12), size=10, color=b.WHITE if fill != b.ACCENT else b.WHITE, shrink=True)
    d.text(s, note, cx + Inches(0.12), cy + ih - Inches(0.46),
           iw - Inches(0.2), Inches(0.38), size=9, color=b.MUTED, shrink=True)
d.footer(s, 11, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — GCC OWNERSHIP MILESTONES: What the GCC owns at each stage
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "What the GCC Owns at Each Stage — The Compounding Asset Base",
         "GCC Ownership Milestones")
rows = [
    ["Stage", "GCC Owns at This Point", "Global Parent Sees"],
    ["End of Sprint\n(Week 8)",
     "AI Transformation Roadmap · PoC results with production pathway · Transformation business case · Signed partner relationship with FPT",
     "Credible AI roadmap · costed delivery plan · named technology partner · $150K–$250K invested, $2M–$10M ARR unlocked"],
    ["End of Transformation Yr 1\n(Month 12)",
     "Production AI system (2–3 live use cases) · modernised legacy stack · vertical AI platform deployed · AI testing automated · managed services SLA",
     "AI in production · legacy tech debt cleared · developer velocity improved · first measurable ROI from vertical AI · FPT delivering at pace"],
    ["End of Transformation Yr 2\n(Month 24)",
     "Multiple verticals live · edge AI deployed · first co-developed AI module · DX Garage running · white-label module v1 · joint IP framework",
     "GCC as AI innovation centre · co-owned IP · strategic asset not just cost centre · preferred partner MSA signed · $10M–$30M engagement"],
    ["Strategic Partnership\n(Year 2+)",
     "AI platform as standard · resellable IP portfolio · CxO co-design seat · preferred partner ecosystem · potential joint patents · global innovation access",
     "GCC as flagship AI Centre of Excellence for the global group · FPT embedded · reference for peer GCCs · competitive advantage through proprietary AI"],
]
col_w = [Inches(2.4), Inches(5.8), Inches(3.8)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(1.1), header_fill=b.NAVY, alt_fill=True, text_size=11, header_text_size=12)
d.footer(s, 12, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — PLATFORM-TO-PHASE MAPPING TABLE
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "FPT Platform Activation by Phase — The Full Breadth in One View",
         "Platform-to-Phase Mapping")
rows = [
    ["FPT Platform", "Layer", "Sprint\n(Wks 1–8)", "Transformation\nYr 1 (M 3–12)", "Transformation\nYr 2 (M 12–24)", "Strategic\nPartnership"],
    ["CASAN Framework", "MODERNIZE", "Full assessment", "Ongoing governance", "Continuous", "Embedded"],
    ["EMT", "MODERNIZE", "Scoping", "Full deployment", "Optimise", "Maintain"],
    ["xMainframe", "MODERNIZE", "Baseline", "Migration live", "Complete", "Managed"],
    ["CodeVista", "MODERNIZE", "Pilot", "Full team rollout", "At scale", "Standard tool"],
    ["Data Platform", "MODERNIZE", "Audit", "Build", "Expand", "Managed"],
    ["FleziPT", "ACTIVATE", "PoC", "2–3 use cases live", "Scale + new cases", "Platform standard"],
    ["KnowMed.ai / V.Factory", "ACTIVATE", "Scope", "First vertical live", "2nd vertical live", "All verticals"],
    ["Edge AI Orchestrator", "ACTIVATE", "—", "Scope", "Deploy", "Operate"],
    ["AI Testing Loop", "ACTIVATE", "—", "Live (Month 5)", "Full coverage", "Continuous"],
    ["DX Garage", "INNOVATE", "—", "—", "Running (Month 12)", "Continuous"],
    ["Co-Development", "INNOVATE", "—", "—", "Sprint 1", "Ongoing"],
    ["White-Label Modules", "INNOVATE", "—", "—", "Module v1", "Portfolio"],
    ["CxO Quarterly Roadmap", "INNOVATE", "—", "Month 3 kickoff", "Quarterly", "Bi-directional"],
]
col_w = [Inches(2.6), Inches(1.45), Inches(1.5), Inches(1.85), Inches(2.0), Inches(2.7)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(0.38), header_fill=b.NAVY, alt_fill=True, text_size=9.5, header_text_size=10.5)
d.footer(s, 13, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — GOVERNANCE & STAGE GATES
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Governance Model — Stage Gates, RAID, and CxO Cadence",
         "How FPT Keeps the Programme on Track and the GCC Head Covered")
half = (CW - Inches(0.2)) / 2
# Left: stage gates
d.rect(s, M, Inches(1.72), half, Inches(4.9), b.SOFT, radius=0.03)
d.rect(s, M, Inches(1.72), half, Inches(0.38), b.NAVY)
d.text(s, "STAGE GATES", M + Inches(0.14), Inches(1.78),
       half - Inches(0.2), Inches(0.28), size=12, color=b.TEAL, bold=True)
gates = [
    ("Gate 1 — Week 8 (End of Sprint)",
     "Go/No-Go for Transformation Program. Criteria: PoC results meet agreed KPIs · roadmap endorsed by GCC head · global parent briefed · SOW signed."),
    ("Gate 2 — Month 6 (Mid-Year 1)",
     "Programme health check. Criteria: first production use case live · data platform operational · legacy modernization on track · managed services SLA met."),
    ("Gate 3 — Month 12 (End of Year 1)",
     "Year 2 renewal decision. Criteria: 2+ use cases in production · vertical AI deployed · measurable ROI documented · GCC head satisfied · global parent review passed."),
    ("Gate 4 — Month 24 (Strategic Conversion)",
     "Go/No-Go for Strategic AI Partnership. Criteria: co-development sprint completed · white-label module v1 shipped · IP framework signed · CxO alignment on multi-year MSA."),
]
for i, (gate, desc) in enumerate(gates):
    gy = Inches(2.22) + i * Inches(1.1)
    d.rect(s, M + Inches(0.12), gy, half - Inches(0.22), Inches(1.0), b.WHITE, radius=0.02)
    d.text(s, gate, M + Inches(0.22), gy + Inches(0.06),
           half - Inches(0.38), Inches(0.26), size=10.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, desc, M + Inches(0.22), gy + Inches(0.34),
           half - Inches(0.38), Inches(0.58), size=10, color=b.INK, shrink=True)
# Right: cadence
rx = M + half + Inches(0.2)
rw = half
d.rect(s, rx, Inches(1.72), rw, Inches(4.9), b.NAVY, radius=0.03)
d.rect(s, rx, Inches(1.72), rw, Inches(0.38), b.TEAL)
d.text(s, "OPERATING CADENCE", rx + Inches(0.14), Inches(1.78),
       rw - Inches(0.2), Inches(0.28), size=12, color=b.NAVY, bold=True)
cadence = [
    ("Weekly", "FPT delivery lead + GCC programme manager · sprint reviews · blockers surfaced"),
    ("Monthly", "Srikumar + GCC VP · performance vs SLA · upcoming milestones · commercial items"),
    ("Quarterly", "CxO review · FPT technology pipeline briefing · roadmap co-planning · gate assessment"),
    ("Annually", "Global parent briefing · ROI review · Strategic Partnership expansion discussion"),
    ("RAID Log", "Risks, Assumptions, Issues, Decisions — maintained continuously by FPT delivery lead · shared with GCC weekly"),
    ("Escalation Path", "GCC Engineer → FPT Delivery Lead → Srikumar → FPT India MD → FPT Global CxO · maximum 24hr resolution SLA for P1 issues"),
]
for i, (freq, desc) in enumerate(cadence):
    cy2 = Inches(2.22) + i * Inches(0.75)
    d.rect(s, rx + Inches(0.12), cy2, Inches(1.1), Inches(0.65), b.NAVY_2, radius=0.02)
    d.text(s, freq, rx + Inches(0.14), cy2 + Inches(0.15),
           Inches(1.0), Inches(0.35), size=11, color=b.TEAL, bold=True,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, desc, rx + Inches(1.28), cy2 + Inches(0.06),
           rw - Inches(1.42), Inches(0.54), size=10, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 14, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — COMMERCIAL ARC
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The Commercial Arc — From Sprint to Strategic Partner in 24 Months",
         "Revenue Progression and FPT Proof Points")
rows = [
    ["Phase", "Timeline", "GCC Investment", "FPT Platforms Active", "Proof Benchmark"],
    ["AI Readiness Sprint", "Weeks 1–8", "$150K – $250K",
     "CASAN · FleziPT PoC · xMainframe scoping",
     "FPT has run 1,100+ client engagements; Sprint is the validated entry model"],
    ["Transformation Program Yr 1", "Months 3–12", "$2M – $5M ARR",
     "EMT + xMainframe + CodeVista + FleziPT + 1 vertical AI + AI Testing",
     "xMainframe: 30% faster onboarding, 90% accuracy; CodeVista: 6,000 man-months saved"],
    ["Transformation Program Yr 2", "Months 12–24", "$5M – $10M ARR",
     "All Yr 1 + 2nd vertical + Edge AI + DX Garage + Co-Dev",
     "Virtual Factory: 80% cost reduction; KnowMed.ai: GE Healthcare reference"],
    ["Strategic AI Partnership", "Year 2+", "$10M – $30M / multi-year",
     "Full stack + co-development + white-label + CxO co-design",
     "$256M largest AI contract (Asian energy group); $10M+ deals doubled YoY 2025"],
]
col_w = [Inches(2.4), Inches(1.5), Inches(1.8), Inches(3.5), Inches(2.8)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(0.88), header_fill=b.NAVY, alt_fill=True, text_size=10.5, header_text_size=11)
d.rect(s, M, Inches(6.1), CW, Inches(0.55), b.NAVY, radius=0.03)
stats = [
    "1,100+ global clients · 130+ Fortune 500",
    "$256M largest AI contract · $10M+ deals doubled YoY",
    "Microsoft Frontier Partner · AWS GenAI Competency",
]
sw = CW / 3
for i, text in enumerate(stats):
    d.text(s, text, M + i * sw + Inches(0.1), Inches(6.18),
           sw - Inches(0.15), Inches(0.38),
           size=10.5, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.footer(s, 15, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — WHY FPT + SRIKUMAR FOR THIS JOURNEY
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "Why FPT + Srikumar — The Two Things That Cannot Be Replicated",
       M, Inches(0.28), CW, Inches(0.52), size=24, color=b.WHITE, bold=True, shrink=True)
half = (CW - Inches(0.2)) / 2
# FPT side
d.rect(s, M, Inches(0.95), half, Inches(5.72), b.NAVY_2, radius=0.03)
d.rect(s, M, Inches(0.95), half, Inches(0.06), b.TEAL)
d.text(s, "FPT SOFTWARE — THE STACK NO ONE ELSE HAS",
       M + Inches(0.15), Inches(1.04), half - Inches(0.25), Inches(0.3),
       size=12, color=b.TEAL, bold=True)
fpt_items = [
    "End-to-end delivery: CASAN → EMT/xMainframe/CodeVista → FleziPT → KnowMed.ai / Virtual Factory → DX Garage. One partner, full lifecycle.",
    "AI-native tooling — not wrapped generic models. FleziPT, EMT, xMainframe are proprietary FPT platforms built for production.",
    "Industry partnerships: Microsoft Frontier Partner (1st Enterprise SI in SE Asia), AWS GenAI Competency, NVIDIA HGX GPU.",
    "AI Factory: 1,100B+ tokens processed, 70+ fine-tuned models, 18,000+ engineers on platform.",
    "54,000+ professionals across 30+ countries. India delivery at scale — 1,000+ technology professionals in-country.",
    "Track record: $256M largest AI contract, $10M+ deals doubled YoY 2025, 130+ Fortune 500 clients.",
]
for i, item in enumerate(fpt_items):
    iy = Inches(1.44) + i * Inches(0.75)
    d.rect(s, M + Inches(0.15), iy, half - Inches(0.28), Inches(0.65), b.NAVY, radius=0.02)
    d.text(s, item, M + Inches(0.25), iy + Inches(0.06),
           half - Inches(0.45), Inches(0.55), size=10, color=b.LIGHT_TEAL, shrink=True)
# Srikumar side
rx = M + half + Inches(0.2)
d.rect(s, rx, Inches(0.95), half, Inches(5.72), b.NAVY_2, radius=0.03)
d.rect(s, rx, Inches(0.95), half, Inches(0.06), b.GOLD)
d.text(s, "SRIKUMAR V R — THE TRUST NO ONE CAN BUY",
       rx + Inches(0.15), Inches(1.04), half - Inches(0.25), Inches(0.3),
       size=12, color=b.GOLD, bold=True)
sri_items = [
    "27 years across 5 industries and 3 countries — IIT Madras B.Tech + IIM Calcutta PGDM. Peer-level credibility with GCC MDs and VPs.",
    "3+ years building FPT GCC relationships in India — warm pipeline of 20–30 GCC contacts who know and trust him personally.",
    "Builder, not just a BD executive: BLAAST patent (IIT Tirupati), USD 1M Malaysian government grant, 300+ agent SaaS platform.",
    "Cross-industry pattern recognition: has seen the AI problem from life sciences, BFSI, manufacturing, aviation, energy simultaneously.",
    "Long-cycle deal navigation: Interserve, Virinchi, FPT — multi-stakeholder, multi-quarter complexity is his natural habitat.",
    "The Srikumar effect: one GCC win → 3–5 peer GCC introductions through his IIT Madras + IIM Calcutta alumni network in Bengaluru.",
]
for i, item in enumerate(sri_items):
    iy = Inches(1.44) + i * Inches(0.75)
    d.rect(s, rx + Inches(0.15), iy, half - Inches(0.28), Inches(0.65), b.NAVY, radius=0.02)
    d.text(s, item, rx + Inches(0.25), iy + Inches(0.06),
           half - Inches(0.45), Inches(0.55), size=10, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 16, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 17 — CLOSING / NEXT STEP
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "The Roadmap Is Proven. The Stack Is Ready. The Relationship Is Yours to Build.",
       M, Inches(0.32), CW, Inches(0.68), size=26, color=b.WHITE, bold=True, shrink=True)
col_w3 = (CW - Inches(0.3)) / 3
cols = [
    (b.NAVY_2, b.TEAL, "PHASE 1\nSTART HERE",
     "Book the AI Readiness Sprint\n\n6–8 weeks · $150K–$250K\n\nScopeable within 2 weeks of introductory call\n\nNo open-ended commitment\n\nWorst case: a board-ready AI roadmap\nBest case: Transformation Program signed at Week 8"),
    (b.TEAL, b.NAVY, "WHAT SRIKUMAR\nDOES NEXT",
     "Introductory call scheduled within 7 days from warm GCC network\n\nAgenda: hear the GCC's AI mandate in their own words\n\nNo product pitch — 20 minutes of listening\n\nGoal: qualify for Sprint or surface the right FPT specialist\n\nSrikumar owns the relationship from Sprint to Partnership"),
    (b.NAVY_2, b.GOLD, "WHAT HAPPENS\nAT MONTH 18",
     "Production AI system running\n\nLegacy stack modernised\n\nVertical AI platform deployed\n\nFirst co-developed AI module shipped\n\nGlobal parent briefed and impressed\n\nStrategic AI Partnership MSA signed\n\n$10M–$30M contract · preferred partner status"),
]
for i, (fill, accent, title, body) in enumerate(cols):
    cx = M + i * (col_w3 + Inches(0.15))
    cy = Inches(1.15)
    ch = Inches(5.35)
    d.rect(s, cx, cy, col_w3, ch, fill, radius=0.04)
    d.rect(s, cx, cy, col_w3, Inches(0.06), accent)
    d.text(s, title, cx + Inches(0.15), cy + Inches(0.12),
           col_w3 - Inches(0.25), Inches(0.65),
           size=14, color=accent, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, cx + Inches(0.4), cy + Inches(0.82), col_w3 - Inches(0.75), Inches(0.04), accent)
    d.text(s, body, cx + Inches(0.15), cy + Inches(0.98),
           col_w3 - Inches(0.25), ch - Inches(1.1),
           size=12, color=b.NAVY if fill == b.TEAL else b.LIGHT_TEAL,
           align=PP_ALIGN.CENTER, shrink=True)
d.rect(s, M, Inches(6.65), CW, Inches(0.48), b.TEAL)
d.text(s, "The GCC that starts the Sprint today is the Strategic AI Partner 18 months from now.",
       M + Inches(0.2), Inches(6.72), CW - Inches(0.3), Inches(0.35),
       size=14, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.footer(s, 17, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE + VALIDATE
# ═══════════════════════════════════════════════════════════════════════════════
d.save(OUT)
print(f"\nSlides: {d.n}")
print(f"Output: {OUT}")
