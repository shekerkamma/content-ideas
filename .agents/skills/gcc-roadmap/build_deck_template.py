#!/usr/bin/env python3
"""GCC Implementation Roadmap — parameterized deck builder. 17 slides.
Substitute ALL {{VAR}} sections at the top before running.
Generate from ikigai report data or standalone company context.
"""
import sys
sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Brand, Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION — substitute these from the ikigai report or user context
# ══════════════════════════════════════════════════════════════════════════════

COMPANY_NAME   = "{{COMPANY_NAME}}"      # e.g. "FPT Software"
BD_PERSON_NAME = "{{BD_PERSON_NAME}}"   # e.g. "Srikumar V R"
BD_PERSON_ROLE = "{{BD_PERSON_ROLE}}"   # e.g. "Director Strategic BD, FPT Software"
RUN_DATE       = "{{RUN_DATE}}"          # e.g. "Jun 2026"

# Engagement tier names and pricing
TIER_SPRINT_NAME     = "{{TIER_SPRINT_NAME}}"     # e.g. "AI READINESS SPRINT"
TIER_SPRINT_PRICE    = "{{TIER_SPRINT_PRICE}}"    # e.g. "Wks 1–8 · $150K–$250K"
TIER_SPRINT_DETAIL   = "{{TIER_SPRINT_DETAIL}}"   # e.g. "$150K–$250K"
TIER_TRANSFORM_NAME  = "{{TIER_TRANSFORM_NAME}}"  # e.g. "TRANSFORMATION PROGRAM"
TIER_TRANSFORM_PRICE = "{{TIER_TRANSFORM_PRICE}}" # e.g. "$2M–$10M / Year"
TIER_PARTNER_NAME    = "{{TIER_PARTNER_NAME}}"    # e.g. "STRATEGIC AI PARTNERSHIP"
TIER_PARTNER_PRICE   = "{{TIER_PARTNER_PRICE}}"   # e.g. "$10M–$30M · Multi-Year"

# Output path
OUT   = "{{OUT_PATH}}"  # e.g. "/home/.../gcc-roadmap-deck-draft.pptx"
TOTAL = 17
FOOTER = f"{COMPANY_NAME} · GCC Implementation Roadmap · {RUN_DATE}"

# ── LAYER 1: MODERNIZE platforms (5 items) ──
# Each: (platform_name, one-line description)
LAYER1_PLATFORMS = [
    ("{{L1_P1_NAME}}", "{{L1_P1_DESC}}"),  # e.g. EMT
    ("{{L1_P2_NAME}}", "{{L1_P2_DESC}}"),  # e.g. xMainframe
    ("{{L1_P3_NAME}}", "{{L1_P3_DESC}}"),  # e.g. CodeVista
    ("{{L1_P4_NAME}}", "{{L1_P4_DESC}}"),  # e.g. CASAN Framework
    ("{{L1_P5_NAME}}", "{{L1_P5_DESC}}"),  # e.g. Data Readiness
]

# ── LAYER 2: ACTIVATE platforms (5 items) ──
LAYER2_PLATFORMS = [
    ("{{L2_P1_NAME}}", "{{L2_P1_DESC}}"),  # e.g. FleziPT
    ("{{L2_P2_NAME}}", "{{L2_P2_DESC}}"),  # e.g. KnowMed.ai
    ("{{L2_P3_NAME}}", "{{L2_P3_DESC}}"),  # e.g. Virtual Factory
    ("{{L2_P4_NAME}}", "{{L2_P4_DESC}}"),  # e.g. Edge AI Orchestrator
    ("{{L2_P5_NAME}}", "{{L2_P5_DESC}}"),  # e.g. AI Testing Loop
]

# ── LAYER 3: INNOVATE platforms (5 items) ──
LAYER3_PLATFORMS = [
    ("{{L3_P1_NAME}}", "{{L3_P1_DESC}}"),  # e.g. DX Garage
    ("{{L3_P2_NAME}}", "{{L3_P2_DESC}}"),  # e.g. Co-Development
    ("{{L3_P3_NAME}}", "{{L3_P3_DESC}}"),  # e.g. White-Label Modules
    ("{{L3_P4_NAME}}", "{{L3_P4_DESC}}"),  # e.g. CxO Quarterly Roadmap
    ("{{L3_P5_NAME}}", "{{L3_P5_DESC}}"),  # e.g. Strategic Partnership
]

# ── Proof stats (slide 15 bottom bar, 3 items) ──
PROOF_STATS = [
    "{{PROOF_STAT_1}}",  # e.g. "1,100+ global clients · 130+ Fortune 500"
    "{{PROOF_STAT_2}}",  # e.g. "$256M largest AI contract · $10M+ deals doubled YoY"
    "{{PROOF_STAT_3}}",  # e.g. "Microsoft Frontier Partner · AWS GenAI Competency"
]

# ── Why Company (slide 16 left panel) ──
COMPANY_ITEMS = [
    "{{COMPANY_ITEM_1}}",
    "{{COMPANY_ITEM_2}}",
    "{{COMPANY_ITEM_3}}",
    "{{COMPANY_ITEM_4}}",
    "{{COMPANY_ITEM_5}}",
    "{{COMPANY_ITEM_6}}",
]

# ── Why BD Person (slide 16 right panel) ──
BD_ITEMS = [
    "{{BD_ITEM_1}}",
    "{{BD_ITEM_2}}",
    "{{BD_ITEM_3}}",
    "{{BD_ITEM_4}}",
    "{{BD_ITEM_5}}",
    "{{BD_ITEM_6}}",
]

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD — do not modify below this line unless changing slide structure
# ═══════════════════════════════════════════════════════════════════════════════

d = Deck(footer=FOOTER)
b = d.b
W, H, M, CW = d.W, d.H, d.M, d.CW

# ── helpers ───────────────────────────────────────────────────────────────────

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

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.rect(s, W - Inches(0.25), 0, Inches(0.25), H, b.NAVY_2)
d.rect(s, W - Inches(0.28), 0, Inches(0.06), H, b.TEAL)
d.text(s, "GCC IMPLEMENTATION ROADMAP", M, Inches(0.85), CW, Inches(0.4),
       size=13, color=b.TEAL, bold=True)
d.text(s, COMPANY_NAME, M, Inches(1.32), CW - Inches(4), Inches(0.95),
       size=52, color=b.WHITE, bold=True, shrink=True)
d.rect(s, M, Inches(2.38), Inches(5), Inches(0.06), b.TEAL)
d.text(s, "From AI Mandate to Production AI — The Full Delivery Journey",
       M, Inches(2.55), CW - Inches(3), Inches(0.75),
       size=18, color=b.LIGHT_TEAL, shrink=True)
tiers = [
    (TIER_SPRINT_NAME, TIER_SPRINT_PRICE),
    (TIER_TRANSFORM_NAME, TIER_TRANSFORM_PRICE),
    (TIER_PARTNER_NAME, TIER_PARTNER_PRICE),
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
d.text(s, f"Prepared by {BD_PERSON_NAME}  ·  {BD_PERSON_ROLE}  ·  {RUN_DATE}",
       M, Inches(5.15), CW, Inches(0.32), size=12, color=b.MUTED)
d.footer(s, 1, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROMISE
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "18 Months from AI Mandate to Strategic AI Partner Status", "Executive Summary")
promise_items = [
    (b.NAVY, b.TEAL,
     "THE PROBLEM",
     f"GCC heads face a board AI mandate with an 18-month delivery expectation and no trusted technology partner who can cover legacy modernization, production AI deployment, vertical platforms, and managed services in one programme."),
    (b.ACCENT, b.WHITE,
     f"THE {COMPANY_NAME.upper()} ANSWER",
     f"A single integrated delivery programme spanning three phases: {TIER_SPRINT_NAME} → {TIER_TRANSFORM_NAME} → {TIER_PARTNER_NAME}. Each phase builds on the last. The GCC's AI capability compounds — and so does the contract value."),
    (b.NAVY_2, b.TEAL,
     "WHAT GCC LEADERSHIP PRESENTS TO GLOBAL PARENT",
     f"A credible, costed implementation roadmap with stage-gates, measurable milestones, and a partner who has delivered at scale."),
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
# SLIDE 3 — THREE LAYERS
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Three Capability Layers · Deployed in Sequence · Compounding in Value",
         "Implementation Architecture")
layers = [
    (b.NAVY, b.TEAL, "LAYER 1 — MODERNIZE",
     "Foundation: Remove the blockers",
     LAYER1_PLATFORMS),
    (b.NAVY_2, b.GOLD, "LAYER 2 — ACTIVATE",
     "Intelligence: Put AI into production",
     LAYER2_PLATFORMS),
    (b.ACCENT, b.WHITE, "LAYER 3 — INNOVATE",
     "Innovation: Create IP together",
     LAYER3_PLATFORMS),
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
        d.text(s, pname, cx + Inches(0.2), iy + Inches(0.04),
               col_w - Inches(0.35), Inches(0.22), size=10, color=b.TEAL, bold=True, shrink=True)
        d.text(s, pdesc, cx + Inches(0.2), iy + Inches(0.26),
               col_w - Inches(0.35), Inches(0.42), size=9, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 3, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — MASTER ROADMAP MATRIX (centrepiece)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "GCC Implementation Roadmap — Time × Capability Matrix",
       M, Inches(0.28), CW, Inches(0.48), size=22, color=b.WHITE, bold=True, shrink=True)
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
d.rect(s, M, top, label_col_w, header_h, b.NAVY_2)
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
layer_fills = [b.TEAL, b.GOLD, b.ACCENT]
layer_rows_data = [
    ("MODERNIZE\nFoundation",
     ["CASAN Assessment\nData Readiness Audit\nCloud Migration Scoping\n" + LAYER1_PLATFORMS[1][0] + " Baseline",
      "EMT Legacy Modernization\n" + LAYER1_PLATFORMS[1][0] + " Migration Live\n" + LAYER1_PLATFORMS[2][0] + " Developer AI\nData Platform Built",
      "Modernization Complete\nLegacy Tech Debt Cleared\nCloud-Native Stack\n" + LAYER1_PLATFORMS[2][0] + " at Scale",
      "Foundation Hardened\nIP Library Growing\nDev Velocity Baseline\nPlatform Lock-In"]),
    ("ACTIVATE\nIntelligence",
     [LAYER2_PLATFORMS[0][0] + " PoC (1 use case)\nVertical AI Scoped\nAI Testing Framework\nModel Selection",
      LAYER2_PLATFORMS[0][0] + " Production\nVertical AI Live\n(" + LAYER2_PLATFORMS[1][0] + " / " + LAYER2_PLATFORMS[2][0] + ")\nAI Testing Automated",
      "2nd Vertical AI Live\nEdge AI Deployed\nAI Testing at 80%\nMLOps Pipeline Stable",
      "AI Platform as Standard\nAll Verticals Active\nSelf-Improving Models\nAI-First Operations"]),
    ("INNOVATE\nInnovation",
     ["Innovation Agenda Set\nCxO Roadmap Drafted\nIP Framework Agreed\n" + LAYER3_PLATFORMS[0][0] + " Scoped",
      "First Co-Dev Sprint\nQuarterly CxO Review\nWhite-Label Module v1\n" + LAYER3_PLATFORMS[0][0] + " Running",
      "Co-Dev Cycle 2\nPatent/IP Filing\nWhite-Label v2 Live\nGlobal Parent Briefed",
      "Strategic Partnership\nJoint AI Products\nResellable IP Portfolio\nPreferred Partner Status"]),
]
layer_h = (H - top - header_h - Inches(0.52) - Inches(0.08)) / 3
for ri, (layer_label, cells) in enumerate(layer_rows_data):
    ry = top + header_h + Inches(0.04) + ri * (layer_h + Inches(0.04))
    d.rect(s, M, ry, label_col_w, layer_h, b.NAVY_2, radius=0.02)
    d.rect(s, M, ry, Inches(0.05), layer_h, layer_fills[ri])
    d.text(s, layer_label, M + Inches(0.12), ry + Inches(0.08),
           label_col_w - Inches(0.18), layer_h - Inches(0.16),
           size=10, color=layer_fills[ri], bold=True,
           align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    for ci, cell_content in enumerate(cells):
        px = M + label_col_w + Inches(0.04) + ci * (phase_col_w + Inches(0.04))
        d.rect(s, px, ry, phase_col_w, layer_h, b.NAVY_2, radius=0.02)
        d.rect(s, px, ry, phase_col_w, Inches(0.03), layer_fills[ri])
        d.text(s, cell_content, px + Inches(0.08), ry + Inches(0.08),
               phase_col_w - Inches(0.14), layer_h - Inches(0.16),
               size=9.5, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 4, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — PHASE 1: AI READINESS SPRINT
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, f"Phase 1 — {TIER_SPRINT_NAME} · {TIER_SPRINT_PRICE}",
         "The Entry Point That Opens Everything Else")
half = (CW - Inches(0.2)) / 2
left_items = [
    ("CASAN Framework Assessment",
     f"Structured AI readiness methodology — maps GCC's current state across data, architecture, people, and use-case pipeline. Produces a prioritised AI roadmap the GCC head can defend to global parent."),
    ("Data Readiness Audit",
     "Assess existing data infrastructure against production AI requirements. Identifies quick wins and blockers. Output: data gap report + remediation plan."),
    ("Legacy Modernization Scoping",
     f"{LAYER1_PLATFORMS[1][0]} baseline assessment — maps workloads to AI-assisted migration paths. Quantifies the man-month savings achievable in Phase 2."),
    (f"{LAYER2_PLATFORMS[0][0]} Proof-of-Concept",
     f"One high-value use case deployed in {LAYER2_PLATFORMS[0][0]} within 6 weeks. Not a demo — a live PoC with real data, measurable output, and a production deployment plan."),
]
right_items = [
    ("Deliverable at Week 8", "AI Transformation Roadmap (board-ready) · PoC results with production pathway · Transformation Program business case · Signed Statement of Work"),
    (f"Who's Involved from {COMPANY_NAME}", f"CASAN Framework lead · {LAYER2_PLATFORMS[0][0]} solution architect · {LAYER1_PLATFORMS[1][0]} specialist · Data platform engineer · {BD_PERSON_NAME} as programme sponsor"),
    ("GCC Risk at This Stage", f"Low — fixed price, fixed scope, fixed timeline. No open-ended commitment. Worst case: a credible AI roadmap and PoC at {TIER_SPRINT_DETAIL}. Best case: Transformation Program signed at Week 8."),
    ("Reference Proof Points", f"{COMPANY_NAME} has run engagements globally. The Sprint model is validated. {TIER_PARTNER_PRICE} contracts have originated as Readiness Sprints."),
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
# SLIDE 6 — PHASE 2: TRANSFORMATION YEAR 1
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, f"Phase 2 — {TIER_TRANSFORM_NAME} Year 1 · Months 3–12 · {TIER_TRANSFORM_PRICE}",
         "Modernize + Activate: Legacy Out, Production AI In")
rows = [
    ["Work Stream", "Platform", "What Gets Delivered", "Milestone"],
    ["Legacy Modernization",
     f"{LAYER1_PLATFORMS[0][0]} + {LAYER1_PLATFORMS[1][0]} + {LAYER1_PLATFORMS[2][0]}",
     "AI-assisted modernization · faster onboarding · improved accuracy · developer AI tooling across GCC engineering team",
     "Month 6: First workload migrated · Month 12: Legacy debt cleared"],
    ["Data Platform",
     f"{LAYER2_PLATFORMS[0][0]} data layer + cloud infra",
     "Production data pipeline · data governance · model training infrastructure · integration with GCC's existing cloud",
     "Month 4: Data pipeline live · Month 8: Model training operational"],
    ["Production AI Deployment",
     LAYER2_PLATFORMS[0][0],
     "2–3 AI use cases in full production · monitoring dashboards · model retraining cycles · audit trail for regulated industries",
     "Month 6: First use case live · Month 10: 2nd use case live"],
    ["Vertical AI Platform",
     f"{LAYER2_PLATFORMS[1][0]} / {LAYER2_PLATFORMS[2][0]} / {LAYER2_PLATFORMS[3][0]}",
     "Industry-specific AI platform deployed inside GCC's domain with domain-trained models",
     "Month 9: Vertical platform operational · Month 12: First vertical results"],
    ["AI Quality & Compliance",
     LAYER2_PLATFORMS[4][0],
     "80% manual testing automated · compliance traceability · regulated industry audit readiness",
     "Month 5: Test automation live · Month 12: Full compliance coverage"],
    ["Managed Services",
     f"{COMPANY_NAME} AMS team",
     "24/7 AI operations support · SLA-backed uptime · model drift monitoring · monthly performance reviews",
     "Month 3: AMS contract active · ongoing through Year 2+"],
]
col_w = [Inches(2.3), Inches(2.3), Inches(5.4), Inches(2.0)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(0.64), header_fill=b.NAVY, alt_fill=True, text_size=10, header_text_size=11)
d.footer(s, 6, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — PHASE 3: TRANSFORMATION YEAR 2
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, f"Phase 3 — {TIER_TRANSFORM_NAME} Year 2 · Months 12–24 · Scaling to Innovation",
         "Activate at Scale + Innovate: AI Becomes the GCC's Competitive Advantage")
yr2_cards = [
    (b.NAVY, b.TEAL, "SCALE AI ACROSS VERTICALS",
     f"Deploy second and third vertical AI platforms. Each new vertical compounds the ROI case for the global parent."),
    (b.NAVY_2, b.TEAL, f"ACTIVATE EDGE & IOT AI",
     f"{LAYER2_PLATFORMS[3][0]} deployed on hardware. Low-latency on-device AI. GCC becomes the AI edge competence centre for the global group."),
    (b.ACCENT, b.WHITE, "BEGIN CO-DEVELOPMENT (INNOVATE LAYER)",
     f"First joint AI module built — GCC's domain expertise + {COMPANY_NAME}'s engineering. IP ownership structure set. {LAYER3_PLATFORMS[0][0]} running rapid prototyping cycles."),
    (b.NAVY, b.TEAL, "WHITE-LABEL MODULE v1",
     f"First AI module packaged for the GCC to own and potentially resell. Turns {COMPANY_NAME}'s engineering into GCC's IP."),
    (b.NAVY_2, b.GOLD, "GLOBAL PARENT BRIEFING",
     f"{BD_PERSON_NAME} leads a CxO-level presentation to the global parent. Shows 24-month results: AI in production, legacy cleared, vertical AI ROI, and the co-development IP pipeline."),
    (b.TEAL, b.NAVY, "STRATEGIC PARTNERSHIP CONVERSION",
     f"{TIER_PARTNER_PRICE} multi-year contract. Platform lock-in. Preferred partner status. GCC becomes a flagship reference for {COMPANY_NAME}'s India GCC practice."),
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
# SLIDE 8 — PHASE 4: STRATEGIC AI PARTNERSHIP
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, f"Phase 4 — {TIER_PARTNER_NAME} · {TIER_PARTNER_PRICE}",
       M, Inches(0.28), CW, Inches(0.52), size=20, color=b.WHITE, bold=True, shrink=True)
d.text(s, f"The GCC is now {COMPANY_NAME}'s reference client in India. {COMPANY_NAME} is the GCC's preferred AI partner globally.",
       M, Inches(0.88), CW, Inches(0.35), size=13, color=b.LIGHT_TEAL, shrink=True)
p4_rows = [
    ["Partnership Element", "What It Means for the GCC", f"What It Means for {COMPANY_NAME}"],
    ["Multi-year MSA", "Budget certainty · no annual renegotiation · platform roadmap locked", "Predictable ARR · deepening platform dependency · flagship reference"],
    ["Co-Development Programme", "Owns jointly-developed AI modules · builds resellable IP · domain AI leadership", "Engineering capacity deployed on sticky, high-value co-creation work"],
    ["CxO Quarterly Roadmap", f"GCC's AI agenda shaped by {COMPANY_NAME}'s global technology pipeline · first-mover access", "Strategy influence at board level · early signal of next expansion opportunity"],
    ["Preferred Partner Status", f"Global parent recognises {COMPANY_NAME} as primary AI SI for the group's India operations", f"{BD_PERSON_NAME}'s network effect: one GCC win → 3–5 referrals to peer GCCs"],
    ["IP Revenue Tail", "White-label AI modules generate revenue independent of services", f"{COMPANY_NAME} platform embedded in client-owned products → long-term ecosystem lock-in"],
    ["Innovation Access", f"{LAYER3_PLATFORMS[0][0]} running continuously · {COMPANY_NAME} R&D pipeline input · joint patent potential", "GCC acts as live lab for new platform features before global rollout"],
]
col_w = [Inches(2.8), Inches(4.6), Inches(4.6)]
table_rows(s, p4_rows, M, Inches(1.42), col_w,
           row_h=Inches(0.72), header_fill=b.TEAL, alt_fill=True, text_size=10.5, header_text_size=11)
d.footer(s, 8, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — MODERNIZE LAYER DEEP DIVE
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, f"MODERNIZE — {COMPANY_NAME}'s Legacy Modernization Stack · The Foundation Layer",
         "Why Legacy Blocks AI — and How We Remove the Blocker")
d.rect(s, M, Inches(1.72), CW, Inches(0.52), b.NAVY, radius=0.03)
d.text(s, "The single most common reason GCC AI initiatives fail to reach production: the underlying tech stack cannot support production AI workloads.",
       M + Inches(0.18), Inches(1.78), CW - Inches(0.3), Inches(0.4),
       size=12.5, color=b.LIGHT_TEAL, shrink=True)
mod_rows = [
    ["Platform", "What It Does", "Proof Metric", "Typical Timeline"],
] + [
    [name, desc, "Proven in enterprise engagements globally", "3–18 months depending on scope"]
    for name, desc in LAYER1_PLATFORMS
]
col_w = [Inches(2.4), Inches(5.2), Inches(2.8), Inches(1.7)]
table_rows(s, mod_rows, M, Inches(2.42), col_w,
           row_h=Inches(0.72), header_fill=b.NAVY, alt_fill=True, text_size=10, header_text_size=11)
d.footer(s, 9, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — ACTIVATE LAYER DEEP DIVE
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, f"ACTIVATE — {COMPANY_NAME}'s AI Production Stack · Intelligence Layer",
         "Production AI — Not Pilots, Not Demos, Not Frameworks")
act_cards = []
fills_accents = [(b.NAVY, b.TEAL), (b.NAVY_2, b.TEAL), (b.NAVY, b.TEAL),
                 (b.NAVY_2, b.GOLD), (b.ACCENT, b.WHITE)]
for j, (name, desc) in enumerate(LAYER2_PLATFORMS):
    fill, accent = fills_accents[min(j, 4)]
    act_cards.append((name, fill, accent, desc, f"Enterprise-validated platform"))
# Add 6th card (AI Factory or platform summary)
act_cards.append((f"{COMPANY_NAME} AI Factory", b.NAVY, b.TEAL,
    f"{COMPANY_NAME}'s global AI production infrastructure. GCC taps into this at the speed of a model API, not a build-from-scratch project.",
    "Validated at scale across global enterprise clients"))
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
           cw2 - Inches(0.2), Inches(0.3), size=12, color=accent, bold=True, shrink=True)
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
         "The Layer That Transforms the SI from Vendor to Partner")
d.rect(s, M, Inches(1.72), CW, Inches(0.48), b.NAVY, radius=0.03)
d.text(s, f"Most GCC-SI relationships stay transactional. The INNOVATE layer is where they become strategic — GCC owns IP, {COMPANY_NAME} is embedded in the roadmap, and both parties have skin in each other's success.",
       M + Inches(0.18), Inches(1.78), CW - Inches(0.3), Inches(0.38),
       size=12, color=b.LIGHT_TEAL, shrink=True)
innov_fills = [(b.NAVY_2, b.TEAL), (b.NAVY, b.TEAL), (b.NAVY_2, b.GOLD),
               (b.NAVY, b.TEAL), (b.ACCENT, b.WHITE), (b.NAVY_2, b.TEAL)]
iw = (CW - Inches(0.3)) / 3
ih = Inches(2.28)
for i, (name, desc) in enumerate(LAYER3_PLATFORMS):
    fill, accent = innov_fills[min(i, 5)]
    col = i % 3
    row = i // 3
    cx = M + col * (iw + Inches(0.15))
    cy = Inches(2.38) + row * (ih + Inches(0.14))
    d.rect(s, cx, cy, iw, ih, fill, radius=0.03)
    d.rect(s, cx, cy, iw, Inches(0.06), accent)
    d.text(s, name, cx + Inches(0.12), cy + Inches(0.1),
           iw - Inches(0.2), Inches(0.3), size=11, color=accent, bold=True, shrink=True)
    d.text(s, desc, cx + Inches(0.12), cy + Inches(0.44),
           iw - Inches(0.2), Inches(1.12), size=10, color=b.WHITE, shrink=True)
    d.text(s, "Activated from Month 12 of Transformation Program", cx + Inches(0.12), cy + ih - Inches(0.46),
           iw - Inches(0.2), Inches(0.38), size=9, color=b.MUTED, shrink=True)
d.footer(s, 11, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — GCC OWNERSHIP MILESTONES
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "What the GCC Owns at Each Stage — The Compounding Asset Base",
         "GCC Ownership Milestones")
rows = [
    ["Stage", "GCC Owns at This Point", "Global Parent Sees"],
    ["End of Sprint\n(Week 8)",
     f"AI Transformation Roadmap · PoC results with production pathway · Transformation business case · Signed partner relationship with {COMPANY_NAME}",
     f"Credible AI roadmap · costed delivery plan · named technology partner · {TIER_SPRINT_DETAIL} invested, {TIER_TRANSFORM_PRICE} ARR unlocked"],
    ["End of Transformation Yr 1\n(Month 12)",
     "Production AI system (2–3 live use cases) · modernised legacy stack · vertical AI platform deployed · AI testing automated · managed services SLA",
     "AI in production · legacy tech debt cleared · developer velocity improved · first measurable ROI from vertical AI"],
    ["End of Transformation Yr 2\n(Month 24)",
     "Multiple verticals live · edge AI deployed · first co-developed AI module · innovation studio running · white-label module v1 · joint IP framework",
     "GCC as AI innovation centre · co-owned IP · strategic asset not just cost centre · preferred partner MSA signed"],
    ["Strategic Partnership\n(Year 2+)",
     "AI platform as standard · resellable IP portfolio · CxO co-design seat · preferred partner ecosystem · potential joint patents · global innovation access",
     "GCC as flagship AI Centre of Excellence for the global group · partner embedded · reference for peer GCCs"],
]
col_w = [Inches(2.4), Inches(5.8), Inches(3.8)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(1.1), header_fill=b.NAVY, alt_fill=True, text_size=11, header_text_size=12)
d.footer(s, 12, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — PLATFORM-TO-PHASE MAPPING
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, f"{COMPANY_NAME} Platform Activation by Phase — The Full Breadth in One View",
         "Platform-to-Phase Mapping")
rows = [
    ["Platform", "Layer", "Sprint\n(Wks 1–8)", "Transformation\nYr 1 (M 3–12)", "Transformation\nYr 2 (M 12–24)", "Strategic\nPartnership"],
]
for name, _ in LAYER1_PLATFORMS:
    rows.append([name, "MODERNIZE", "Scoping/Audit", "Full deployment", "Optimise/Scale", "Managed/Standard"])
for name, _ in LAYER2_PLATFORMS:
    rows.append([name, "ACTIVATE", "PoC/Scope", "Live (Months 5–9)", "Scale + new cases", "Platform standard"])
for name, _ in LAYER3_PLATFORMS:
    rows.append([name, "INNOVATE", "—", "Scoped/Kickoff", "Running (Month 12+)", "Ongoing/Portfolio"])
col_w = [Inches(2.6), Inches(1.45), Inches(1.5), Inches(1.85), Inches(2.0), Inches(2.7)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(0.38), header_fill=b.NAVY, alt_fill=True, text_size=9.5, header_text_size=10.5)
d.footer(s, 13, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — GOVERNANCE & STAGE GATES
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Governance Model — Stage Gates, RAID, and CxO Cadence",
         f"How {COMPANY_NAME} Keeps the Programme on Track and the GCC Head Covered")
half = (CW - Inches(0.2)) / 2
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
rx = M + half + Inches(0.2)
rw = half
d.rect(s, rx, Inches(1.72), rw, Inches(4.9), b.NAVY, radius=0.03)
d.rect(s, rx, Inches(1.72), rw, Inches(0.38), b.TEAL)
d.text(s, "OPERATING CADENCE", rx + Inches(0.14), Inches(1.78),
       rw - Inches(0.2), Inches(0.28), size=12, color=b.NAVY, bold=True)
cadence = [
    ("Weekly", f"{COMPANY_NAME} delivery lead + GCC programme manager · sprint reviews · blockers surfaced"),
    ("Monthly", f"{BD_PERSON_NAME} + GCC VP · performance vs SLA · upcoming milestones · commercial items"),
    ("Quarterly", f"CxO review · {COMPANY_NAME} technology pipeline briefing · roadmap co-planning · gate assessment"),
    ("Annually", "Global parent briefing · ROI review · Strategic Partnership expansion discussion"),
    ("RAID Log", f"Risks, Assumptions, Issues, Decisions — maintained continuously by {COMPANY_NAME} delivery lead · shared with GCC weekly"),
    ("Escalation", f"GCC Engineer → {COMPANY_NAME} Delivery Lead → {BD_PERSON_NAME} → {COMPANY_NAME} MD → {COMPANY_NAME} Global CxO · maximum 24hr resolution SLA for P1 issues"),
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
         "Revenue Progression and Proof Points")
rows = [
    ["Phase", "Timeline", "GCC Investment", "Platforms Active", "Proof Benchmark"],
    [TIER_SPRINT_NAME, "Weeks 1–8", TIER_SPRINT_DETAIL,
     f"{LAYER1_PLATFORMS[3][0]} · {LAYER2_PLATFORMS[0][0]} PoC · {LAYER1_PLATFORMS[1][0]} scoping",
     f"Sprint is the validated entry model — fixed price, fixed scope"],
    [f"{TIER_TRANSFORM_NAME} Yr 1", "Months 3–12", TIER_TRANSFORM_PRICE,
     f"{LAYER1_PLATFORMS[0][0]} + {LAYER1_PLATFORMS[1][0]} + {LAYER1_PLATFORMS[2][0]} + {LAYER2_PLATFORMS[0][0]} + 1 vertical AI",
     f"{LAYER1_PLATFORMS[1][0]} and {LAYER1_PLATFORMS[2][0]} proof metrics from live engagements"],
    [f"{TIER_TRANSFORM_NAME} Yr 2", "Months 12–24", "Scaling ARR",
     f"All Yr 1 + 2nd vertical + Edge AI + {LAYER3_PLATFORMS[0][0]} + Co-Dev",
     f"{LAYER2_PLATFORMS[2][0]} and {LAYER2_PLATFORMS[1][0]} ROI references"],
    [TIER_PARTNER_NAME, "Year 2+", TIER_PARTNER_PRICE,
     "Full stack + co-development + white-label + CxO co-design",
     f"Largest contracts have originated as Readiness Sprints"],
]
col_w = [Inches(2.4), Inches(1.5), Inches(1.8), Inches(3.5), Inches(2.8)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(0.88), header_fill=b.NAVY, alt_fill=True, text_size=10.5, header_text_size=11)
d.rect(s, M, Inches(6.1), CW, Inches(0.55), b.NAVY, radius=0.03)
sw = CW / 3
for i, text in enumerate(PROOF_STATS):
    d.text(s, text, M + i * sw + Inches(0.1), Inches(6.18),
           sw - Inches(0.15), Inches(0.38),
           size=10.5, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.footer(s, 15, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — WHY COMPANY + BD PERSON
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, f"Why {COMPANY_NAME} + {BD_PERSON_NAME} — The Two Things That Cannot Be Replicated",
       M, Inches(0.28), CW, Inches(0.52), size=24, color=b.WHITE, bold=True, shrink=True)
half = (CW - Inches(0.2)) / 2
d.rect(s, M, Inches(0.95), half, Inches(5.72), b.NAVY_2, radius=0.03)
d.rect(s, M, Inches(0.95), half, Inches(0.06), b.TEAL)
d.text(s, f"{COMPANY_NAME.upper()} — THE STACK NO ONE ELSE HAS",
       M + Inches(0.15), Inches(1.04), half - Inches(0.25), Inches(0.3),
       size=12, color=b.TEAL, bold=True, shrink=True)
for i, item in enumerate(COMPANY_ITEMS):
    iy = Inches(1.44) + i * Inches(0.75)
    d.rect(s, M + Inches(0.15), iy, half - Inches(0.28), Inches(0.65), b.NAVY, radius=0.02)
    d.text(s, item, M + Inches(0.25), iy + Inches(0.06),
           half - Inches(0.45), Inches(0.55), size=10, color=b.LIGHT_TEAL, shrink=True)
rx = M + half + Inches(0.2)
d.rect(s, rx, Inches(0.95), half, Inches(5.72), b.NAVY_2, radius=0.03)
d.rect(s, rx, Inches(0.95), half, Inches(0.06), b.GOLD)
d.text(s, f"{BD_PERSON_NAME.upper()} — THE TRUST NO ONE CAN BUY",
       rx + Inches(0.15), Inches(1.04), half - Inches(0.25), Inches(0.3),
       size=12, color=b.GOLD, bold=True, shrink=True)
for i, item in enumerate(BD_ITEMS):
    iy = Inches(1.44) + i * Inches(0.75)
    d.rect(s, rx + Inches(0.15), iy, half - Inches(0.28), Inches(0.65), b.NAVY, radius=0.02)
    d.text(s, item, rx + Inches(0.25), iy + Inches(0.06),
           half - Inches(0.45), Inches(0.55), size=10, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 16, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 17 — CLOSING
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "The Roadmap Is Proven. The Stack Is Ready. The Relationship Is Yours to Build.",
       M, Inches(0.32), CW, Inches(0.68), size=26, color=b.WHITE, bold=True, shrink=True)
col_w3 = (CW - Inches(0.3)) / 3
cols = [
    (b.NAVY_2, b.TEAL, "PHASE 1\nSTART HERE",
     f"Book the {TIER_SPRINT_NAME}\n\n{TIER_SPRINT_PRICE}\n\nScopeable within 2 weeks of introductory call\n\nNo open-ended commitment\n\nWorst case: a board-ready AI roadmap\nBest case: Transformation Program signed at Week 8"),
    (b.TEAL, b.NAVY, f"WHAT {BD_PERSON_NAME.split()[0].upper()}\nDOES NEXT",
     "Introductory call scheduled within 7 days from warm GCC network\n\nAgenda: hear the GCC's AI mandate in their own words\n\nNo product pitch — 20 minutes of listening\n\nGoal: qualify for Sprint or surface the right specialist\n\nRelationship owned from Sprint to Partnership"),
    (b.NAVY_2, b.GOLD, "WHAT HAPPENS\nAT MONTH 18",
     "Production AI system running\n\nLegacy stack modernised\n\nVertical AI platform deployed\n\nFirst co-developed AI module shipped\n\nGlobal parent briefed and impressed\n\nStrategic AI Partnership MSA signed\n\n" + TIER_PARTNER_PRICE + " · preferred partner status"),
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
