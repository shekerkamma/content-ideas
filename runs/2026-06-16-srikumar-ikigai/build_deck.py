#!/usr/bin/env python3
"""Srikumar V R — Ikigai Pro Report · FPT Software GCC deck builder. v2 — 26 slides."""
import sys
sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Brand, Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor

OUT = "/home/shekerk/content-ideas/runs/2026-06-16-srikumar-ikigai/srikumar-ikigai-deck-draft.pptx"
TOTAL = 26
FOOTER = "Srikumar V R · Ikigai Pro Report · FPT Software GCC · Jun 2026"

d = Deck(footer=FOOTER)
b = d.b
W, H, M, CW = d.W, d.H, d.M, d.CW

# ── helpers ──────────────────────────────────────────────────────────────────

def table_rows(s, rows, left, top, col_widths, row_h=Inches(0.42),
               header_fill=None, alt_fill=None, text_size=11.5, header_text_size=12):
    for ri, row in enumerate(rows):
        is_header = (ri == 0 and header_fill is not None)
        fill = header_fill if is_header else (
            b.SOFT if (alt_fill and ri % 2 == 0) else b.WHITE)
        row_y = top + ri * row_h
        x = left
        for ci, (cell, cw) in enumerate(zip(row, col_widths)):
            d.rect(s, x, row_y, cw, row_h, fill, line=b.GRID)
            tc = b.WHITE if is_header else b.INK
            sz = header_text_size if is_header else text_size
            pad = Inches(0.08)
            d.text(s, cell, x + pad, row_y + Inches(0.05),
                   cw - pad * 2, row_h - Inches(0.05),
                   size=sz, color=tc, bold=is_header, shrink=True,
                   anchor=MSO_ANCHOR.MIDDLE)
            x += cw

def kpi_box(s, cx, cy, bw, bh, number, label, note=None, num_color=None):
    num_color = num_color or b.GOLD
    d.rect(s, cx, cy, bw, bh, b.NAVY_2, radius=0.04)
    d.rect(s, cx, cy, bw, Inches(0.05), b.TEAL)
    d.text(s, number, cx + Inches(0.1), cy + Inches(0.12),
           bw - Inches(0.2), Inches(0.62),
           size=28, color=num_color, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, label, cx + Inches(0.1), cy + Inches(0.75),
           bw - Inches(0.2), Inches(0.32),
           size=11, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    if note:
        d.text(s, note, cx + Inches(0.1), cy + Inches(1.08),
               bw - Inches(0.2), Inches(0.28),
               size=9, color=b.MUTED, align=PP_ALIGN.CENTER, shrink=True)

def use_case_slide(s, pg, title, subtitle, challenge, solution, results, platform, clients):
    d.rect(s, 0, 0, W, H, b.NAVY)
    d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
    d.text(s, "USE CASE", M, Inches(0.25), Inches(2), Inches(0.3),
           size=10, color=b.TEAL, bold=True)
    d.text(s, title, M, Inches(0.45), CW - Inches(3), Inches(0.62),
           size=24, color=b.WHITE, bold=True, shrink=True)
    d.text(s, subtitle, M, Inches(1.12), CW - Inches(3), Inches(0.35),
           size=13, color=b.LIGHT_TEAL)
    # left column
    lw = Inches(5.8)
    d.rect(s, M, Inches(1.62), lw, Inches(1.18), b.NAVY_2, radius=0.03)
    d.text(s, "CHALLENGE", M + Inches(0.15), Inches(1.72),
           lw - Inches(0.2), Inches(0.28), size=10, color=b.TEAL, bold=True)
    d.text(s, challenge, M + Inches(0.15), Inches(2.0),
           lw - Inches(0.2), Inches(0.72), size=11.5, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, M, Inches(2.92), lw, Inches(1.28), b.NAVY_2, radius=0.03)
    d.text(s, "FPT SOLUTION", M + Inches(0.15), Inches(3.02),
           lw - Inches(0.2), Inches(0.28), size=10, color=b.TEAL, bold=True)
    d.text(s, solution, M + Inches(0.15), Inches(3.3),
           lw - Inches(0.2), Inches(0.82), size=11.5, color=b.LIGHT_TEAL, shrink=True)
    # results strip
    d.rect(s, M, Inches(4.32), lw, Inches(1.12), b.TEAL, radius=0.03)
    d.text(s, "RESULTS", M + Inches(0.15), Inches(4.42),
           lw - Inches(0.2), Inches(0.28), size=10, color=b.NAVY, bold=True)
    d.text(s, results, M + Inches(0.15), Inches(4.7),
           lw - Inches(0.2), Inches(0.66), size=12, color=b.NAVY, bold=True, shrink=True)
    # right column
    rx = M + lw + Inches(0.2)
    rw = CW - lw - Inches(0.2)
    d.rect(s, rx, Inches(1.62), rw, Inches(1.62), b.NAVY_2, radius=0.03)
    d.text(s, "PLATFORM", rx + Inches(0.15), Inches(1.72),
           rw - Inches(0.2), Inches(0.28), size=10, color=b.GOLD, bold=True)
    d.text(s, platform, rx + Inches(0.15), Inches(2.0),
           rw - Inches(0.2), Inches(1.12), size=11, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, rx, Inches(3.36), rw, Inches(2.1), b.NAVY_2, radius=0.03)
    d.text(s, "GCC RELEVANCE", rx + Inches(0.15), Inches(3.46),
           rw - Inches(0.2), Inches(0.28), size=10, color=b.GOLD, bold=True)
    d.text(s, clients, rx + Inches(0.15), Inches(3.74),
           rw - Inches(0.2), Inches(1.58), size=11, color=b.LIGHT_TEAL, shrink=True)
    d.footer(s, pg, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.rect(s, W - Inches(0.25), 0, Inches(0.25), H, b.NAVY_2)
d.rect(s, W - Inches(0.28), 0, Inches(0.06), H, b.TEAL)
d.text(s, "IKIGAI PRO REPORT", M, Inches(0.85), CW, Inches(0.4),
       size=13, color=b.TEAL, bold=True)
d.text(s, "Srikumar V R", M, Inches(1.35), CW - Inches(4), Inches(1.1),
       size=52, color=b.WHITE, bold=True, shrink=True)
d.rect(s, M, Inches(2.55), Inches(4), Inches(0.06), b.TEAL)
d.text(s, "Empowering GCCs in India with FPT Software's AI-First Capability Stack",
       M, Inches(2.72), CW - Inches(4), Inches(0.9),
       size=18, color=b.LIGHT_TEAL, shrink=True)
d.rect(s, M, Inches(3.85), Inches(3.4), Inches(0.75), b.GOLD, radius=0.04)
d.text(s, "Validation Score  88 / 100  ·  EXCEPTIONAL",
       M + Inches(0.12), Inches(3.93), Inches(3.2), Inches(0.55),
       size=14, color=b.NAVY, bold=True, shrink=True)
d.text(s, "Greater Bengaluru  ·  FPT Software  ·  Jun 2026",
       M, Inches(4.78), CW, Inches(0.35), size=13, color=b.MUTED)
for i, chip in enumerate(["IIT Madras", "IIM Calcutta", "27 Years", "5 Industries"]):
    cx = M + i * Inches(2.1)
    d.rect(s, cx, Inches(5.3), Inches(1.95), Inches(0.38), b.NAVY_2, radius=0.08)
    d.text(s, chip, cx + Inches(0.12), Inches(5.34), Inches(1.72), Inches(0.3),
           size=11.5, color=b.TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE)
d.footer(s, 1, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 2 — CORE INSIGHT
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The Trusted Human Bridge — FPT's Stack + Srikumar's Trust Equity", "Core Insight")
body_paras = [
    {"text": "FPT Software has world-class AI platforms: FleziPT for production AI, EMT/xMainframe for legacy modernization, CodeVista for developer velocity, and vertical-specific tools for healthcare, manufacturing, and automotive.",
     "size": 14, "color": b.INK},
    {"text": "The gap is not capability. The gap is trust at GCC leadership level in India.",
     "size": 15, "color": b.NAVY, "bold": True, "space_before": 14},
    {"text": "GCC heads are fatigued by vendor pitches. They need someone with peer-level credibility — a BD leader who has built companies, held patents, and spent 27 years across 5 industries and 3 countries. When Srikumar introduces FPT's capability stack, GCC leaders listen differently.",
     "size": 14, "color": b.INK, "space_before": 14},
    {"text": "That is the structural advantage. FPT's world-class capability delivered through Srikumar's irreplaceable trust equity.",
     "size": 14, "color": b.ACCENT, "bold": True, "space_before": 14},
]
d.text(s, body_paras, M, Inches(1.65), CW - Inches(3.5), Inches(4.5), shrink=True)
d.rect(s, W - Inches(3.3), Inches(1.8), Inches(2.7), Inches(1.5), b.NAVY, radius=0.04)
d.text(s, "88/100", W - Inches(3.1), Inches(1.95), Inches(2.5), Inches(0.7),
       size=42, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.text(s, "EXCEPTIONAL", W - Inches(3.1), Inches(2.68), Inches(2.5), Inches(0.4),
       size=13, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
d.footer(s, 2, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 3 — PROFILE SNAPSHOT
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "27 Years · 5 Industries · 3 Countries · IIT Madras + IIM Calcutta", "Profile Snapshot")
rows = [
    ["Company", "Role", "Period", "Domain"],
    ["FPT Software", "Director, Strategic BD", "2023–Present", "GCC enablement · AI transformation · life sciences, BFSI, manufacturing"],
    ["MaxedS", "VP Client Relationship", "2021–2023", "UAV · EV · Utilities · Retail · Healthcare"],
    ["OPUSTAYZ Hospitality", "Director & CEO", "2016–2020", "Hospitality tech · BLAAST Patent (COVID air sterilizer, IIT Tirupati)"],
    ["KC Travel Solutions", "Director & COO", "2014–2015", "SaaS travel platform · 300+ agents · AI/AR/VR personalization concept (Ci2Te2)"],
    ["Interserve Travel", "VP Strategy & Operations", "2008–2014", "Airline sales · portal · 150+ agency rollout"],
    ["Intelligent Media Tech", "Director", "2006–2008", "Digital signage i-Screen · Malaysia & India · USD 1M Malaysian govt grant"],
    ["Virinchi / Starspot", "VP / Director", "2001–2008", "Enterprise software · Bollywood distribution · SE Asia · 50-engineer team"],
    ["Education", "IIM Calcutta PGDM (Marketing/Finance/HR)  +  IIT Madras B.Tech Chemical Engineering", "", ""],
]
col_w = [Inches(2.4), Inches(2.8), Inches(1.6), Inches(5.1)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(0.52), header_fill=b.NAVY, alt_fill=True, text_size=10.5)
d.footer(s, 3, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 4 — IKIGAI MAP
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Four Dimensions · One Intersection · One Unique Position", "Ikigai Map")
quad_w = Inches(5.9)
quad_h = Inches(2.4)
gap = Inches(0.15)
top_row = Inches(1.72)
bot_row = top_row + quad_h + gap
left_col = M
right_col = M + quad_w + gap
quads = [
    (left_col, top_row, b.NAVY, b.TEAL, "WHAT HE LOVES",
     "Building ventures from scratch · Cross-industry strategic partnerships · Enabling GCC transformation · Emerging tech as business lever · Being the connector · Watching partners win"),
    (right_col, top_row, b.NAVY_2, b.TEAL, "WHAT HE'S GOOD AT",
     "Opening GCC CXO doors · Translating FPT's tech depth into business outcomes · Cross-industry pattern matching · Multi-geography BD (India + Malaysia + SE Asia) · IIT+IIM rigor · Long-cycle enterprise deals"),
    (left_col, bot_row, b.ACCENT, b.WHITE, "WHAT THE WORLD NEEDS",
     "FPT's AI-first stack delivered to GCCs with board AI mandates · FleziPT in production · Legacy modernization via xMainframe/EMT · Vertical AI: KnowMed.ai, Virtual Factory · India delivery at scale"),
    (right_col, bot_row, b.NAVY, b.GOLD, "WHAT PAYS",
     "$2M–$10M/year Transformation Programs · $10M–$30M Strategic AI Partnerships · Managed services renewal tails · Platform licensing (FleziPT, KnowMed.ai) · FPT $10M+ contracts doubled YoY"),
]
for (qx, qy, qfill, qaccent, qtitle, qbody) in quads:
    d.rect(s, qx, qy, quad_w, quad_h, qfill, radius=0.03)
    d.rect(s, qx, qy, quad_w, Inches(0.06), qaccent)
    d.text(s, qtitle, qx + Inches(0.15), qy + Inches(0.1),
           quad_w - Inches(0.2), Inches(0.32), size=12, color=qaccent, bold=True)
    d.text(s, qbody, qx + Inches(0.15), qy + Inches(0.48),
           quad_w - Inches(0.2), quad_h - Inches(0.55),
           size=10.5, color=b.LIGHT_TEAL if qfill in (b.NAVY, b.NAVY_2) else b.WHITE, shrink=True)
d.rect(s, M + quad_w - Inches(0.55), top_row + quad_h - Inches(0.2),
       Inches(1.25), Inches(0.55), b.GOLD, radius=0.06)
d.text(s, "IKIGAI\nINTERSECTION", M + quad_w - Inches(0.48), top_row + quad_h - Inches(0.15),
       Inches(1.1), Inches(0.45), size=8, color=b.NAVY, bold=True,
       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.footer(s, 4, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 5 — FPT CAPABILITY TABLE
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "GCCs Have the Mandate · FPT Has Every Piece of the Stack",
         "What the World Needs — FPT Software Capabilities")
rows = [
    ["GCC Need", "FPT Capability", "Platform / Product"],
    ["AI in production — not just pilots", "Enterprise AI deployment with full lifecycle management", "FleziPT"],
    ["Legacy stack blocking AI adoption", "AI-powered mainframe modernization — 30% faster onboarding, 90% accuracy", "EMT + xMainframe"],
    ["Developer velocity without headcount", "AI productivity tooling — 30% efficiency gain, 6,000 man-months saved", "CodeVista"],
    ["Healthcare GCC AI", "Industry-specific AI platform for life sciences & HIPAA-compliant workflows", "KnowMed.ai"],
    ["Manufacturing GCC AI", "Anomaly detection, computer vision, predictive maintenance at plant level", "Virtual Factory"],
    ["Automotive / IoT AI", "Multi-agent edge AI on Qualcomm/NVIDIA — low-latency on-device intelligence", "Edge AI Orchestrator"],
    ["Strategy to execution in one partner", "Assessment + delivery framework — from roadmap to measurable impact", "CASAN Framework"],
    ["Testing automation (regulated industries)", "80% manual testing automated · V-Model and A-SPICE compliant", "AI Testing Loop"],
]
col_w = [Inches(3.2), Inches(6.2), Inches(2.5)]
table_rows(s, rows, M, Inches(1.68), col_w,
           row_h=Inches(0.54), header_fill=b.NAVY, alt_fill=True, text_size=10.5)
d.footer(s, 5, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 6 — FPT CAPABILITY STACK (8 cards)
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "FPT's AI-First Platform Stack — Built for Enterprise GCC Deployment",
       M, Inches(0.38), CW, Inches(0.65),
       size=26, color=b.WHITE, bold=True, shrink=True)
d.rect(s, M, Inches(1.08), Inches(1.2), Inches(0.05), b.TEAL)
d.text(s, "Eight platforms. One integrated stack. Production-grade for GCC environments.",
       M, Inches(1.22), CW, Inches(0.35), size=13, color=b.LIGHT_TEAL)
cap_cards = [
    ("FleziPT", "AI production platform: data readiness, model integration, validation, traceability & operational monitoring"),
    ("xMainframe", "AI mainframe migration · 30% faster onboarding · 90% accuracy · transforms monthly cycles to weekly"),
    ("CodeVista", "AI developer productivity · 30% efficiency gain · 1.5M lines generated · 6,000 man-months saved"),
    ("EMT", "Engineering Platform & Modernization Technologies — full legacy modernization lifecycle from assessment to rewrite"),
    ("KnowMed.ai", "Healthcare & life sciences vertical AI · HIPAA-compliant · reduces patient intake friction · premium tier upsell"),
    ("Virtual Factory", "Manufacturing AI: anomaly detection, computer vision, predictive maintenance · real-time plant monitoring"),
    ("CASAN Framework", "Scalable engineering + domain expertise + data + advanced AI · strategy-to-execution in one framework"),
    ("AI Testing Loop", "80% manual testing automated · V-Model & A-SPICE compliance traceability · industrialised validation on AWS"),
]
card_w = Inches(5.85)
card_h = Inches(1.22)
for i, (title, body) in enumerate(cap_cards):
    col = i % 2
    row = i // 2
    cx = M + col * (card_w + Inches(0.14))
    cy = Inches(1.72) + row * (card_h + Inches(0.14))
    d.rect(s, cx, cy, card_w, card_h, b.NAVY_2, radius=0.03, shadow=True)
    d.rect(s, cx, cy, Inches(0.07), card_h, b.TEAL)
    d.text(s, title, cx + Inches(0.15), cy + Inches(0.08),
           card_w - Inches(0.2), Inches(0.3), size=11, color=b.TEAL, bold=True, shrink=True)
    d.text(s, body, cx + Inches(0.15), cy + Inches(0.38),
           card_w - Inches(0.2), card_h - Inches(0.48),
           size=9.5, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 6, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 7 — FPT BY THE NUMBERS  [NEW — PROOF POINT]
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "FPT Software — Global Scale, Proven Delivery Track Record",
       M, Inches(0.38), CW, Inches(0.55), size=26, color=b.WHITE, bold=True, shrink=True)
d.rect(s, M, Inches(1.02), Inches(1.2), Inches(0.05), b.TEAL)
d.text(s, "Numbers that GCC heads and their global parents can take to the board.",
       M, Inches(1.18), CW, Inches(0.35), size=13, color=b.LIGHT_TEAL)
# 6 KPI boxes in 3x2 grid
kpi_w = (CW - Inches(0.4)) / 3
kpi_h = Inches(1.55)
kpis = [
    ("1,100+", "Global Clients", "incl. 130+ Fortune 500"),
    ("54,000+", "Professionals", "80+ nationalities, 30+ countries"),
    ("$256M", "Largest AI Contract", "5-year AI transformation, Asian energy group"),
    ("22%", "Q1 2026 Contract Growth", "Newly signed international IT services"),
    ("$10M+", "Deals Doubled YoY", "2025 vs 2024 — FPT's enterprise momentum"),
    ("30,000+", "Certified Engineers", "Largest in Vietnam; AI-augmented delivery"),
]
for i, (num, label, note) in enumerate(kpis):
    col = i % 3
    row = i // 3
    cx = M + col * (kpi_w + Inches(0.2))
    cy = Inches(1.68) + row * (kpi_h + Inches(0.18))
    kpi_box(s, cx, cy, kpi_w, kpi_h, num, label, note)
d.footer(s, 7, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 8 — FPT AI CREDENTIALS  [NEW — PROOF POINT]
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "FPT's AI Credentials — First-Mover Partnerships + Production Scale",
         "AI Proof Points")
# 3 partnership badges top row
badge_w = (CW - Inches(0.3)) / 3
badge_h = Inches(1.1)
badges = [
    ("Microsoft\nFrontier Partner",
     "First Enterprise System Integrator in Southeast Asia to achieve this status"),
    ("AWS Generative AI\nCompetency",
     "Recognised for production-grade GenAI delivery on AWS infrastructure"),
    ("NVIDIA HGX\nGPU Partnership",
     "Advanced GPU infrastructure for AI Factory — 70+ fine-tuned models running"),
]
for i, (title, desc) in enumerate(badges):
    bx = M + i * (badge_w + Inches(0.15))
    d.rect(s, bx, Inches(1.72), badge_w, badge_h, b.NAVY, radius=0.04)
    d.rect(s, bx, Inches(1.72), badge_w, Inches(0.05), b.GOLD)
    d.text(s, title, bx + Inches(0.15), Inches(1.8),
           badge_w - Inches(0.25), Inches(0.42),
           size=13, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, desc, bx + Inches(0.15), Inches(2.24),
           badge_w - Inches(0.25), Inches(0.5),
           size=10, color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)

# AI Factory stats row
d.rect(s, M, Inches(3.0), CW, Inches(0.05), b.GRID)
d.text(s, "AI FACTORY METRICS", M, Inches(3.12), CW, Inches(0.3),
       size=11, color=b.MUTED, bold=True)
ai_stats = [
    ("1,100B+", "Tokens processed\nby AI Factory"),
    ("70+", "Fine-tuned AI\nmodels in production"),
    ("18,000+", "Engineers on\nglobal AI platform"),
    ("43", "AI cloud services\nsupported"),
    ("~30%", "Productivity gains\ndelivered to clients"),
]
stat_w = CW / len(ai_stats)
for i, (num, label) in enumerate(ai_stats):
    sx = M + i * stat_w
    d.text(s, num, sx, Inches(3.5), stat_w, Inches(0.68),
           size=28, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, label, sx, Inches(4.2), stat_w, Inches(0.55),
           size=10.5, color=b.MUTED, align=PP_ALIGN.CENTER, shrink=True)
    if i < len(ai_stats) - 1:
        d.rect(s, sx + stat_w - Inches(0.02), Inches(3.5),
               Inches(0.03), Inches(1.1), b.GRID)

# CES 2026 note
d.rect(s, M, Inches(5.05), CW, Inches(0.52), b.SOFT, radius=0.03)
d.text(s, "CES 2026: FPT showcased FleziPT, Virtual Factory, Edge AI Orchestrator, and AI Testing Loop — validating AI-first strategy at the world's largest tech showcase.",
       M + Inches(0.15), Inches(5.12), CW - Inches(0.25), Inches(0.38),
       size=11.5, color=b.INK, shrink=True)
d.footer(s, 8, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 9 — CLIENT VOICES  [NEW — PROOF POINT]
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "What Global Leaders Say — From Fortune 500 to Insurance to Energy",
       M, Inches(0.38), CW, Inches(0.55), size=24, color=b.WHITE, bold=True, shrink=True)
d.rect(s, M, Inches(1.02), Inches(1.2), Inches(0.05), b.TEAL)
d.text(s, "Clients across every GCC-relevant vertical have validated FPT's delivery.",
       M, Inches(1.18), CW, Inches(0.35), size=13, color=b.LIGHT_TEAL)
testimonials = [
    ("GE Healthcare", "Healthcare",
     '"Accelerate AI-driven solutions improving hospital operations and patient care — building a connected healthcare ecosystem."'),
    ("Schaeffler", "Manufacturing",
     '"Flexibility and speed of people drive digital transformation success — FPT\'s teams deliver at the pace our business demands."'),
    ("RWE", "Energy & Utilities",
     '"We receive innovative ideas to support our core business with IT — FPT brings strategic thinking, not just execution."'),
    ("ITOCHU Corporation", "Trading / Conglomerate",
     '"We avoid long proof-of-concept phases and move directly into production — FPT makes AI real, not theoretical."'),
    ("Davies Insurance", "Financial Services",
     '"Move to market faster with 7 product teams adhering to our standards — FPT scaled our delivery without sacrificing quality."'),
]
q_h = Inches(1.02)
q_gap = Inches(0.12)
for i, (client, industry, quote) in enumerate(testimonials):
    qy = Inches(1.68) + i * (q_h + q_gap)
    d.rect(s, M, qy, CW, q_h, b.NAVY_2, radius=0.03)
    d.rect(s, M, qy, Inches(0.06), q_h, b.TEAL)
    d.text(s, client, M + Inches(0.18), qy + Inches(0.08),
           Inches(1.8), Inches(0.3), size=12, color=b.TEAL, bold=True)
    d.text(s, industry, M + Inches(0.18), qy + Inches(0.42),
           Inches(1.8), Inches(0.25), size=9.5, color=b.MUTED)
    d.text(s, quote, M + Inches(2.1), qy + Inches(0.1),
           CW - Inches(2.2), q_h - Inches(0.18),
           size=11.5, color=b.LIGHT_TEAL, italic=True, shrink=True)
d.footer(s, 9, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 10 — USE CASE: INSURANCE & FINANCIAL SERVICES GCC  [NEW]
# ═══════════════════════════════════════════════════════════════════════
use_case_slide(
    s=d.slide(),
    pg=10,
    title="Use Case — Insurance & Financial Services GCC",
    subtitle="AI underwriting · RPA automation · ServiceNow low-code · faster product delivery",
    challenge="Insurance and BFSI GCCs face board mandates to embed AI into underwriting, claims, compliance, and customer operations — but lack the domain-specific AI expertise and engineering capacity to deliver in production without 18-month hiring cycles.",
    solution="FPT deploys AI underwriting systems, RPA for health insurance processing, ServiceNow low-code for workflow automation, and AI-augmented engineering teams that integrate with existing BFSI tech stacks (SAP, Microsoft Dynamics 365, core insurance platforms).",
    results="600% boost in underwriting efficiency · $1.5M turnaround on health insurance RPA (EpiSource) · 70% effort saved in workflow automation (ServiceNow) · 7 product teams shipping faster (Davies Insurance)",
    platform="FleziPT (AI production)\nSAP + Microsoft Dynamics 365 integration\nAI Testing Loop (compliance)\nServiceNow low-code / no-code\nCASAN Framework (strategy to execution)",
    clients="Life insurance GCCs with AI underwriting mandate\nHealth insurance GCCs with claims automation backlog\nBFSI GCCs needing faster product delivery without adding headcount\nRegulated GCCs requiring audit-trail AI (V-Model / A-SPICE compliance)\nInsurance AMS ISVs building AI renewal automation for their GCC clients"
)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 11 — USE CASE: MANUFACTURING & HEALTHCARE GCC  [NEW]
# ═══════════════════════════════════════════════════════════════════════
use_case_slide(
    s=d.slide(),
    pg=11,
    title="Use Case — Manufacturing & Healthcare GCC",
    subtitle="Factory AI · predictive maintenance · hospital operations · patient care automation",
    challenge="Manufacturing and healthcare GCCs are under pressure to deploy AI that reduces operational cost, improves safety, and delivers measurable ROI to global parents — without disrupting existing plant systems or violating HIPAA/regulatory constraints.",
    solution="FPT deploys Virtual Factory (anomaly detection, computer vision, real-time plant monitoring) for manufacturing GCCs, and KnowMed.ai (HIPAA-compliant, AI-driven hospital and patient workflow automation) for healthcare GCCs — both production-ready, not pilot-grade.",
    results="80% cost reduction in factory safety surveillance · 70% reduction in manual monitoring effort · GE Healthcare: AI accelerating hospital operations and patient care · Schaeffler: digital transformation at pace",
    platform="Virtual Factory (computer vision + anomaly detection + predictive maintenance)\nKnowMed.ai (healthcare AI + HIPAA compliance)\nEdge AI Orchestrator (low-latency on-device AI)\nFleziPT (production AI deployment layer)\nAI Testing Loop (80% manual testing automated)",
    clients="Manufacturing GCCs with 'add AI to plant operations' on board roadmap\nHealthcare GCCs under pressure to reduce patient intake friction and clinical admin burden\nEnergy GCCs with asset monitoring and predictive maintenance requirements\nAny GCC in a regulated industry needing AI with compliance traceability\nGlobal parents whose India GCC is the designated AI innovation centre for the group"
)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 12 — SRIKUMAR BD PROOF POINTS  [NEW]
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Srikumar's Proof Points — Why GCC Leaders Take the First Meeting",
         "BD Experience & Credibility Evidence")
proof_items = [
    ("FPT Software (2023–Present)",
     "3+ years building GCC relationships across life sciences, BFSI, aviation, manufacturing, energy and mobility in India. "
     "Enabled GCCs to accelerate innovation and scale operations through FPT's AI-first capability stack."),
    ("KC Travel Solutions (2014–2015)",
     "Built and scaled a SaaS travel platform to 300+ travel agents. Conceptualized Ci2Te2 — an AI/AR/VR-powered travel personalization engine — in 2014, "
     "a decade before generative AI became mainstream. Proof of early technology conviction."),
    ("Intelligent Media Technologies, Malaysia (2006–2008)",
     "Built the digital signage solution i-Screen from scratch, forged alliance with Screenaxx Media, launched pilots in Malaysia and India with a 6-person team. "
     "Secured USD 1M grant from Malaysian Government — first Indian media venture to achieve this."),
    ("BLAAST Patent (2016–2020)",
     "Invented a Thermal Air Sterilizer for airborne COVID-19 in collaboration with Dr Sunil Kumar, IIT Tirupati. "
     "Took a scientific concept to a working product and filed patent. Proof that Srikumar doesn't just advise — he builds."),
    ("Interserve Travel (2008–2014)",
     "Achieved stellar airline revenue growth 2010–2012. Rolled out portal and credit policy across 150+ travel agency users. "
     "Multi-year enterprise relationship management at P&L level."),
    ("IIT Madras B.Tech + IIM Calcutta PGDM",
     "Engineering analytical rigour (IIT Madras, Chemical Engineering, 1993–1997) combined with commercial strategic thinking "
     "(IIM Calcutta, Marketing/Finance/HR, 1997–1999). The pedigree that opens CFO and CTO doors in India's GCC community."),
]
item_h = Inches(0.82)
for i, (title, body) in enumerate(proof_items):
    row = i % 3
    col = i // 3
    ix = M + col * (CW / 2 + Inches(0.1))
    iy = Inches(1.72) + row * (item_h + Inches(0.1))
    iw = CW / 2 - Inches(0.08)
    d.rect(s, ix, iy, iw, item_h, b.SOFT, radius=0.03)
    d.rect(s, ix, iy, Inches(0.06), item_h, b.TEAL)
    d.text(s, title, ix + Inches(0.14), iy + Inches(0.07),
           iw - Inches(0.2), Inches(0.26), size=11, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, ix + Inches(0.14), iy + Inches(0.34),
           iw - Inches(0.2), item_h - Inches(0.4),
           size=9.5, color=b.INK, shrink=True)
d.footer(s, 12, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 13 — WHAT HE LOVES
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Serial Founder Energy at the Heart of Every Engagement", "What He Loves")
bullets = [
    "Co-creating transformation outcomes — enabling GCC success, not selling a product; every role has been about enabling others' growth",
    "Cross-industry strategic partnerships — Screenaxx in Malaysia, Celcom mobile content, FPT GCC co-creation; pattern of building alliances that multiply reach",
    "Emerging technology as a real business lever — Ci2Te2 (AI/AR/VR travel personalization in 2014), BLAAST patent, Generative AI certification; early mover throughout career",
    "Building from zero — OPUSTAYZ Hospitality, KC Travel SaaS platform (300+ agents), digital signage pilots in 2 countries, USD 1M Malaysian government grant",
    "Being the connector — Ma Foi Pulse editor, Strategy Ambassador, community participation; consistently the person who brings the right people together",
    "Watching partner companies win because of what he helped enable — the recurring reward that drives every engagement",
]
paras = [{"text": t, "bullet": True, "size": 14, "color": b.INK, "space_before": 10} for t in bullets]
d.text(s, paras, M, Inches(1.72), CW - Inches(0.3), Inches(5.0), shrink=True)
d.footer(s, 13, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 14 — WHAT HE'S GOOD AT
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The Rare Combination: IIT+IIM Rigor + Builder Track Record + CXO Access",
         "What He's Good At")
bullets = [
    "Opening GCC CXO doors — 3+ years at FPT building relationships across BFSI, life sciences, aviation, manufacturing; IIT+IIM pedigree signals rigor to CFOs approving vendor spend",
    "Translating FPT's technical depth into GCC buyer language — converting FleziPT, EMT, xMainframe into business outcomes GCC heads can justify to global parents",
    "Cross-industry pattern matching — seeing that a manufacturing GCC's AI problem looks like one a healthcare GCC solved six months ago; FPT has solutions for both",
    "Multi-geography relationship building — India + Malaysia + SE Asia CXO networks; useful for GCCs whose global parents have SE Asia operations FPT also serves",
    "IIT Madras + IIM Calcutta pedigree — engineering problem-solving brain married to MBA-level commercial thinking; rare combination for a BD leader at this level",
    "Long-cycle enterprise deal navigation — Interserve, Virinchi, FPT all involved multi-stakeholder, multi-quarter complexity; GCC transformation programs are exactly that shape",
]
paras = [{"text": t, "bullet": True, "size": 14, "color": b.INK, "space_before": 10} for t in bullets]
d.text(s, paras, M, Inches(1.72), CW - Inches(0.3), Inches(5.0), shrink=True)
d.footer(s, 14, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 15 — NICHE STATEMENT
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "A Position Nobody Else Occupies in the India GCC Market", "Niche Statement")
layers = [
    (b.NAVY, b.TEAL, "LAYER 1 — MARKET",
     "GCCs in India across BFSI, life sciences, healthcare, manufacturing, energy and aviation\n$64B+ annual spend · growing from 1,700 to 2,400+ GCCs by 2030 · 12–15% CAGR"),
    (b.NAVY_2, b.GOLD, "LAYER 2 — NICHE",
     "GCC VPs and MDs at multinationals ($500M–$5B parent revenue) with approved AI transformation budgets but no trusted technology partner who can deliver in production — not just advisory"),
    (b.ACCENT, b.WHITE, "LAYER 3 — PROBLEM",
     "Every SI has pitched them. They need production-grade AI + legacy modernization + vertical platforms + India delivery + an advisor with cross-industry credibility and no single-vendor agenda to protect"),
]
layer_h = Inches(1.55)
for i, (fill, accent, label, body) in enumerate(layers):
    ly = Inches(1.72) + i * (layer_h + Inches(0.1))
    d.rect(s, M, ly, CW, layer_h, fill, radius=0.03)
    d.rect(s, M, ly, CW, Inches(0.05), accent)
    d.text(s, label, M + Inches(0.18), ly + Inches(0.1),
           Inches(3), Inches(0.32), size=12, color=accent, bold=True)
    d.text(s, body, M + Inches(0.18), ly + Inches(0.46),
           CW - Inches(0.3), layer_h - Inches(0.5),
           size=12.5, color=b.WHITE, shrink=True)
d.footer(s, 15, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 16 — VALIDATION SCORECARD
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "88/100 — Exceptional Validation Across All Six Dimensions", "Validation Scorecard")
rows = [
    ["Dimension", "Score", "Evidence"],
    ["Pain Intensity", "9 / 10", "GCC AI mandate is board-level in 2026; legacy systems are #1 blocker — FPT's specialty"],
    ["Purchasing Power", "9 / 10", "GCCs budget $1M–$10M+/year for tech transformation; FPT $10M+ deals doubled YoY 2025"],
    ["Ease to Find", "8 / 10", "NASSCOM GCC Council, GCC Summit, LinkedIn India GCC groups — Srikumar already inside this world"],
    ["Market Growth", "10 / 10", "1,700 → 2,400+ GCCs by 2030; AI spend inside GCCs doubling annually; Q1 2026 FPT +22% contracts"],
    ["Competition Difficulty", "8 / 10", "FPT's AI-native tooling (FleziPT, EMT, CodeVista) not easily replicated; trust equity not acquirable quickly"],
    ["Founder-Market Fit", "9 / 10", "IIT+IIM + 27 years + patent + 3 years at FPT in GCC world + SE Asia multilateral network"],
    ["COMPOSITE", "88 / 100", "EXCEPTIONAL — FPT's AI-first stack at the right moment, delivered by the right BD leader"],
]
col_w = [Inches(2.5), Inches(1.3), Inches(8.1)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(0.54), header_fill=b.NAVY, alt_fill=True, text_size=11)
d.rect(s, W - Inches(2.2), Inches(6.35), Inches(1.6), Inches(0.75), b.GOLD, radius=0.05)
d.text(s, "88/100\nEXCEPTIONAL", W - Inches(2.1), Inches(6.4), Inches(1.4), Inches(0.65),
       size=14, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.footer(s, 16, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 17 — GAP TO OWN
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The Position That Is Empty in India's GCC Ecosystem", "Market Intelligence")
half = (CW - Inches(0.2)) / 2
d.rect(s, M, Inches(1.72), half, Inches(4.8), b.SOFT, radius=0.03)
d.rect(s, M, Inches(1.72), half, Inches(0.42), b.CORAL)
d.text(s, "AVOID — Where Not to Compete", M + Inches(0.12), Inches(1.8),
       half - Inches(0.2), Inches(0.3), size=13, color=b.WHITE, bold=True)
avoid = [
    "Competing on price with dev shops — wrong positioning for FPT's AI-native stack",
    "Chasing SI-sized $100M+ deals at SI speed — wrong sales cycle for GCC agility",
    "Generic 'digital transformation' language — GCC heads are fatigued by vague pitches",
    "Single-vertical positioning — FPT's cross-industry strength is the core advantage",
]
ap = [{"text": t, "bullet": True, "size": 12.5, "color": b.INK, "space_before": 10} for t in avoid]
d.text(s, ap, M + Inches(0.15), Inches(2.25), half - Inches(0.25), Inches(3.8), shrink=True)
rx = M + half + Inches(0.2)
d.rect(s, rx, Inches(1.72), half, Inches(4.8), b.NAVY, radius=0.03)
d.rect(s, rx, Inches(1.72), half, Inches(0.42), b.TEAL)
d.text(s, "GAP TO OWN — The Empty Position", rx + Inches(0.12), Inches(1.8),
       half - Inches(0.2), Inches(0.3), size=13, color=b.NAVY, bold=True)
gap_body = ("Production-grade AI platforms (FleziPT — not consulting frameworks) + industry-specific "
            "vertical solutions (KnowMed.ai, Virtual Factory, Edge AI Orchestrator) + legacy modernization "
            "tooling that delivers in weeks not months (xMainframe/EMT/CodeVista) + India delivery centre "
            "with 1,000+ technology professionals + GCC-peer credibility from a BD leader with a founder's "
            "track record and an IIT+IIM pedigree.\n\nThis combination does not exist anywhere else in the "
            "India GCC market today.")
d.text(s, gap_body, rx + Inches(0.15), Inches(2.25),
       half - Inches(0.25), Inches(4.0), size=12.5, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 17, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 18 — TIMING SIGNALS
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "Why FPT + Srikumar · Why GCCs · Why Now",
       M, Inches(0.38), CW, Inches(0.55), size=26, color=b.WHITE, bold=True, shrink=True)
d.rect(s, M, Inches(1.0), Inches(1.2), Inches(0.05), b.TEAL)
d.text(s, "Four converging signals that make 2026 the pivotal year.",
       M, Inches(1.16), CW, Inches(0.35), size=13, color=b.LIGHT_TEAL)
timing_cards = [
    ("FPT AI Momentum",
     "22% growth in newly signed contracts Q1 2026\n$10M+ contracts doubled YoY in 2025\n$256M largest single AI contract (5-year, Asian energy group)\nCES 2026: FleziPT, Virtual Factory, Edge AI Orchestrator showcased"),
    ("GCC AI Deadline",
     "Global parent boards demanding AI roadmaps by Q4 2026\nGCC heads without a production AI partner are exposed\nAI feature pressure is existential for GCCs in 2026\n70%+ of enterprise software incorporating AI by 2027"),
    ("Legacy Modernization Window",
     "Most GCCs run on stacks built 10–15 years ago\nFPT's EMT / xMainframe / CodeVista land at exactly the right moment\nxMainframe: 30% faster onboarding, 90% accuracy, monthly → weekly cycles\nCodeVista: 1.5M lines generated, 6,000 man-months saved"),
    ("Srikumar's First-Mover Advantage",
     "3 years of FPT GCC relationship depth in India\nWarm pipeline of 20–30 GCC contacts who know and trust him\nIIT Madras + IIM Calcutta alumni network in Bengaluru — GCC MD/VP access\nFirst-mover advantage before competitors realize FPT India has matured"),
]
card_w2 = (CW - Inches(0.45)) / 2
card_h2 = Inches(2.55)
for i, (title, body) in enumerate(timing_cards):
    col = i % 2
    row = i // 2
    cx = M + col * (card_w2 + Inches(0.15))
    cy = Inches(1.65) + row * (card_h2 + Inches(0.15))
    d.rect(s, cx, cy, card_w2, card_h2, b.NAVY_2, radius=0.03)
    d.rect(s, cx, cy, card_w2, Inches(0.06), b.TEAL)
    d.text(s, title, cx + Inches(0.15), cy + Inches(0.1),
           card_w2 - Inches(0.2), Inches(0.32), size=12, color=b.TEAL, bold=True)
    d.text(s, body, cx + Inches(0.15), cy + Inches(0.48),
           card_w2 - Inches(0.2), card_h2 - Inches(0.55),
           size=11, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 18, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 19 — COMPETITOR LANDSCAPE
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Every Competitor Falls Short on the Dimension That Matters Most",
         "Competitor Landscape")
rows = [
    ["Competitor", "Positioning", "Falls Short vs FPT + Srikumar"],
    ["Accenture / TCS / Infosys", "Large SI", "Too slow, too expensive, no AI-native platform — wrap generic models; no FleziPT equivalent"],
    ["Wipro / HCL", "Mid-size SI", "No proprietary AI modernization tooling at FPT's depth (no EMT, no xMainframe, no CodeVista)"],
    ["AWS / Azure / GCP", "Cloud hyperscaler", "No vertical AI solutions; no legacy modernization; GCCs need an integrator, not a platform vendor"],
    ["Boutique AI consultancies", "AI advisory", "Can advise but cannot deliver at scale; no 30,000+ certified engineers; no CASAN-to-execution methodology"],
    ["FPT Software + Srikumar ★", "AI-first tech partner + GCC trust",
     "FleziPT + EMT/xMainframe/CodeVista + KnowMed.ai + Virtual Factory + 130+ Fortune 500 clients + India delivery + founder-level BD credibility"],
]
col_w = [Inches(2.5), Inches(2.3), Inches(7.1)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(0.62), header_fill=b.NAVY, alt_fill=True, text_size=11)
last_y = Inches(1.72) + 5 * Inches(0.62)
d.rect(s, M, last_y, CW, Inches(0.62), b.TEAL, line=b.TEAL)
x = M
for cell, cw in zip(rows[-1], col_w):
    d.text(s, cell, x + Inches(0.08), last_y + Inches(0.06),
           cw - Inches(0.12), Inches(0.5),
           size=11, color=b.NAVY, bold=True, shrink=True, anchor=MSO_ANCHOR.MIDDLE)
    x += cw
d.footer(s, 19, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 20 — FPT GCC ENGAGEMENT MODEL
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Three Entry Points · One Long-Term Partnership", "FPT GCC Engagement Model")
tiers = [
    ("TIER 1", "AI Readiness Sprint", "6–8 weeks · $150K–$250K",
     "CASAN Framework assessment + FleziPT proof-of-concept on 1 priority use case",
     "GCC heads who need a credible AI roadmap for global parent within 90 days"),
    ("TIER 2 ★", "Transformation Program", "$2M–$10M / year",
     "Full stack: legacy modernization (EMT/xMainframe) + cloud migration + FleziPT deployment + vertical AI platform + managed services",
     "GCCs with active AI mandate, approved transformation budget, $200M+ parent"),
    ("TIER 3", "Strategic AI Partnership", "$10M–$30M · multi-year",
     "Co-development + embedded AI-augmented engineering + quarterly CxO roadmap + white-label AI module packaging",
     "Large GCCs ($1B+ parent) treating FPT as primary long-term technology partner"),
]
tier_h = Inches(1.6)
tier_fills = [b.NAVY_2, b.NAVY, b.ACCENT]
for i, (badge, name, price, includes, ideal) in enumerate(tiers):
    ty = Inches(1.72) + i * (tier_h + Inches(0.14))
    fill = tier_fills[i]
    d.rect(s, M, ty, CW, tier_h, fill, radius=0.03)
    d.rect(s, M, ty, Inches(0.08), tier_h, b.TEAL if i < 2 else b.GOLD)
    d.text(s, badge, M + Inches(0.18), ty + Inches(0.1),
           Inches(1.4), Inches(0.28), size=10, color=b.TEAL if i < 2 else b.GOLD, bold=True)
    d.text(s, name, M + Inches(1.6), ty + Inches(0.06),
           Inches(3.5), Inches(0.4), size=16, color=b.WHITE, bold=True, shrink=True)
    d.text(s, price, M + Inches(5.2), ty + Inches(0.1),
           Inches(2.5), Inches(0.35), size=14, color=b.GOLD, bold=True)
    d.text(s, "Includes: " + includes, M + Inches(0.18), ty + Inches(0.52),
           Inches(7.5), Inches(0.5), size=11, color=b.LIGHT_TEAL, shrink=True)
    d.text(s, "Ideal for: " + ideal, M + Inches(0.18), ty + Inches(1.08),
           CW - Inches(0.3), Inches(0.42), size=11, color=b.MUTED, shrink=True)
d.footer(s, 20, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 21 — REVENUE IMPACT
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Each GCC Win Srikumar Opens Compounds Into a Multi-Year Revenue Stream",
         "Revenue Impact per GCC Win")
rows = [
    ["Engagement Type", "Year 1 Revenue to FPT", "Year 2–3 Tail"],
    ["AI Readiness Sprint", "$150K – $250K", "High conversion to Transformation Program; case study unlocks next 5 GCC intros"],
    ["Transformation Program", "$2M – $10M ARR", "Managed services renewal + platform licensing (FleziPT, KnowMed.ai, Virtual Factory)"],
    ["Strategic AI Partnership", "$10M – $30M", "Multi-year locked-in; platform dependency; quarterly CxO co-development; referral to global parent peers"],
]
col_w = [Inches(2.8), Inches(2.5), Inches(6.6)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(0.9), header_fill=b.NAVY, alt_fill=True, text_size=12)
d.rect(s, M, Inches(5.4), CW, Inches(0.7), b.NAVY, radius=0.03)
stats = [
    "$256M — FPT's largest single AI contract · Asian energy group",
    "$10M+ deals doubled YoY · 2025 momentum",
    "22% growth Q1 2026 · confirmed buyer conversion",
]
sw = CW / 3
for i, text in enumerate(stats):
    d.text(s, text, M + i * sw + Inches(0.15), Inches(5.5),
           sw - Inches(0.2), Inches(0.5), size=10.5, color=b.TEAL, bold=True,
           align=PP_ALIGN.CENTER, shrink=True)
d.footer(s, 21, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 22 — MILESTONES
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "First Revenue in 90 Days · $10M ARR by Month 18", "Income Math & Milestones")
rows = [
    ["Phase", "Timeline", "Revenue Target", "Milestone"],
    ["Phase 1", "Months 1–3", "$300K – $750K", "2–3 AI Readiness Sprints signed · validate Sprint as GCC entry vehicle · first case study"],
    ["Phase 2", "Months 3–6", "$2M – $5M ARR", "1 Transformation Program converted from Sprint · FleziPT in production · vertical AI deployed"],
    ["Phase 3", "Months 6–12", "$6M – $15M ARR", "3 active Transformation Programs · managed services tail · CodeVista/xMainframe at 2+ GCCs"],
    ["Phase 4", "Months 12–18", "$10M – $20M", "1 Strategic AI Partnership · multi-year contract · platform lock-in · CxO co-development"],
]
col_w = [Inches(1.3), Inches(1.7), Inches(2.4), Inches(6.5)]
table_rows(s, rows, M, Inches(1.72), col_w,
           row_h=Inches(0.84), header_fill=b.NAVY, alt_fill=True, text_size=12)
d.footer(s, 22, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 23 — 7-DAY ACTIVATION PLAN
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "First Meeting Booked in 7 Days — From Warm Network, Not Cold Outreach",
         "7-Day Activation Plan")
half = (CW - Inches(0.2)) / 2
d.rect(s, M, Inches(1.72), half, Inches(4.8), b.NAVY, radius=0.03)
d.rect(s, M, Inches(1.72), half, Inches(0.42), b.TEAL)
d.text(s, "DAYS 1–3 · Build the Proof Point", M + Inches(0.12), Inches(1.8),
       half - Inches(0.2), Inches(0.3), size=13, color=b.NAVY, bold=True)
d13 = [
    "Identify sharpest GCC pain FPT solves now: legacy modernization → xMainframe (30% faster, 90% accuracy)",
    "Build 1-page FPT GCC capability brief using CES 2026 FleziPT showcase as proof material — not a brochure",
    "Record 3-min LinkedIn video: 'How do I make AI real, not just a pilot?' — insight first, no product pitch",
    "The goal: one compelling story that any GCC head would forward to a peer",
]
p13 = [{"text": t, "bullet": True, "size": 12, "color": b.LIGHT_TEAL, "space_before": 10} for t in d13]
d.text(s, p13, M + Inches(0.15), Inches(2.25), half - Inches(0.25), Inches(4.0), shrink=True)
rx = M + half + Inches(0.2)
d.rect(s, rx, Inches(1.72), half, Inches(4.8), b.SOFT, radius=0.03)
d.rect(s, rx, Inches(1.72), half, Inches(0.42), b.ACCENT)
d.text(s, "DAYS 4–7 · Activate the Network", rx + Inches(0.12), Inches(1.8),
       half - Inches(0.2), Inches(0.3), size=13, color=b.WHITE, bold=True)
d47 = [
    "List 10 GCC heads from FPT India relationship base — VPs and MDs who know Srikumar from last 3 years",
    "Personal outreach (not a template): 'I've been mapping the AI delivery gap across GCCs in [their vertical] — 20 minutes?'",
    "Book 3 discovery calls — goal: hear exact language about AI bottleneck; those words become next month's content",
    "Identify 1 pilot GCC for AI Readiness Sprint at reference-client rate → case study + testimonial at month 2",
]
p47 = [{"text": t, "bullet": True, "size": 12, "color": b.INK, "space_before": 10} for t in d47]
d.text(s, p47, rx + Inches(0.15), Inches(2.25), half - Inches(0.25), Inches(4.0), shrink=True)
d.footer(s, 23, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 24 — TRAJECTORY
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "AI Readiness Sprint → Transformation Program → Strategic Partnership",
         "12–18 Month Trajectory — The Compounding Arc")
phases = [
    ("PHASE 1\nMonths 1–3", "$300K–\n$750K", "2–3 AI Readiness Sprints · first case study · validate GCC entry model"),
    ("PHASE 2\nMonths 3–6", "$2M–\n$5M ARR", "1 Transformation Program · FleziPT in production · vertical AI platform deployed"),
    ("PHASE 3\nMonths 6–12", "$6M–\n$15M ARR", "3 active programs · managed services tail · xMainframe at 2+ GCCs"),
    ("PHASE 4\nMonths 12–18", "$10M–\n$20M", "1 Strategic AI Partnership · multi-year · platform lock-in · CxO co-development"),
]
phase_w = (CW - Inches(0.45)) / 4
phase_h = Inches(4.0)
fills = [b.NAVY_2, b.NAVY, b.ACCENT, b.TEAL]
text_cols = [b.LIGHT_TEAL, b.LIGHT_TEAL, b.WHITE, b.NAVY]
for i, (label, revenue, desc) in enumerate(phases):
    px = M + i * (phase_w + Inches(0.15))
    py = Inches(1.72)
    d.rect(s, px, py, phase_w, phase_h, fills[i], radius=0.03)
    d.text(s, label, px + Inches(0.12), py + Inches(0.15),
           phase_w - Inches(0.2), Inches(0.7),
           size=11, color=text_cols[i], bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, revenue, px + Inches(0.08), py + Inches(0.95),
           phase_w - Inches(0.12), Inches(0.9),
           size=20, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, px + Inches(0.25), py + Inches(1.88), phase_w - Inches(0.5), Inches(0.04),
           b.TEAL if fills[i] != b.TEAL else b.NAVY)
    d.text(s, desc, px + Inches(0.12), py + Inches(2.0),
           phase_w - Inches(0.2), phase_h - Inches(2.1),
           size=10.5, color=text_cols[i], shrink=True)
    if i < 3:
        d.text(s, "→", px + phase_w - Inches(0.08), py + phase_h / 2 - Inches(0.25),
               Inches(0.25), Inches(0.5), size=18, color=b.TEAL, bold=True)
d.footer(s, 24, TOTAL)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 25 — ONE-LINER
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "The Line That Opens Every GCC Door", M, Inches(0.38), CW, Inches(0.5),
       size=22, color=b.TEAL, bold=True)
d.rect(s, M, Inches(1.05), Inches(0.1), Inches(4.2), b.TEAL)
quote = (
    '"FPT Software brings production-grade AI, legacy modernization tooling that\'s '
    'saved over 6,000 man-months, and vertical platforms built for healthcare, '
    'manufacturing, and BFSI — and I work with GCC heads in India to find the specific '
    'capability that closes the gap between their AI mandate and what they can actually '
    'deliver today."'
)
d.text(s, quote, M + Inches(0.3), Inches(1.1), CW - Inches(0.35), Inches(4.2),
       size=22, color=b.WHITE, italic=True, shrink=True)
d.text(s, "— Srikumar V R, Director Strategic BD, FPT Software",
       M + Inches(0.3), Inches(5.5), CW - Inches(0.35), Inches(0.45),
       size=14, color=b.TEAL, bold=True)
d.footer(s, 25, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════
# SLIDE 26 — CLOSING
# ═══════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, W, Inches(0.18), b.TEAL)
d.text(s, "The Stack Is Ready. The Market Is Ready. The Relationships Are Ready.",
       M, Inches(0.38), CW, Inches(0.65),
       size=28, color=b.WHITE, bold=True, shrink=True)
d.rect(s, M, Inches(1.12), Inches(2), Inches(0.05), b.TEAL)
col_w3 = (CW - Inches(0.3)) / 3
cols_data = [
    (b.NAVY_2, b.TEAL, "FPT HAS\nTHE AI STACK",
     "FleziPT · EMT + xMainframe\nCodeVista · KnowMed.ai\nVirtual Factory\nEdge AI Orchestrator\nCASAN Framework\nAI Testing Loop\n1,100+ clients · 130+ Fortune 500\n$256M largest AI contract"),
    (b.ACCENT, b.WHITE, "GCCs HAVE\nTHE MANDATE",
     "1,700+ GCCs in India today\n2,400+ by 2030\n$64B+ annual market\nAI delivery urgency\nQ4 2026 board deadlines\nAI spend doubling annually\nLegacy stacks ready to modernize\nBFSI · Healthcare · Manufacturing"),
    (b.NAVY_2, b.GOLD, "SRIKUMAR HAS\nTHE TRUST",
     "27 years · 5 industries\n3 countries\nIIT Madras + IIM Calcutta\n3 years FPT GCC relationships\nBLAAST Patent (IIT Tirupati)\nUSD 1M govt grant winner\nCross-industry peer credibility\nBuilder — not just an advisor"),
]
for i, (fill, accent, title, body) in enumerate(cols_data):
    cx = M + i * (col_w3 + Inches(0.15))
    cy = Inches(1.38)
    ch = Inches(5.1)
    d.rect(s, cx, cy, col_w3, ch, fill, radius=0.04)
    d.rect(s, cx, cy, col_w3, Inches(0.06), accent)
    d.text(s, title, cx + Inches(0.15), cy + Inches(0.15),
           col_w3 - Inches(0.25), Inches(0.7),
           size=14, color=accent, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, cx + Inches(0.5), cy + Inches(0.88), col_w3 - Inches(1.0), Inches(0.04), accent)
    d.text(s, body, cx + Inches(0.15), cy + Inches(1.05),
           col_w3 - Inches(0.25), ch - Inches(1.15),
           size=11, color=b.LIGHT_TEAL if fill != b.ACCENT else b.WHITE,
           align=PP_ALIGN.CENTER, shrink=True)
d.rect(s, M, Inches(6.65), CW, Inches(0.45), b.TEAL)
d.text(s, "The only question is which GCC head to call first.",
       M + Inches(0.2), Inches(6.7), CW - Inches(0.3), Inches(0.35),
       size=15, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.footer(s, 26, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════
# SAVE + VALIDATE
# ═══════════════════════════════════════════════════════════════════════
d.save(OUT)
print(f"\nSlides: {d.n}")
print(f"Output: {OUT}")
