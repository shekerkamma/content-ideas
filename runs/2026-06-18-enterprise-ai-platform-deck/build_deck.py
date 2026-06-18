#!/usr/bin/env python3
"""Enterprise AI Platform Architecture deck builder.

Source: ~/.knowledge/ai-use-cases/ bundle
Audience: CTO · CISO · CDO at enterprise accounts
~20 slides: cover → exec summary → problem → framework → 5 domain platforms →
            use cases + ROI → realization patterns → governance → 90-day plan → CTA
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILL = Path.home() / ".claude/skills/branded-pptx-deck/scripts"
sys.path.insert(0, str(SKILL))
from pptxkit import Brand, Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt, RGBColor

OUT = Path(__file__).parent / "enterprise-ai-platform-architecture-draft.pptx"
FOOTER = "Enterprise AI Platform Architecture  |  Confidential  |  2026"
TOTAL = 20

d = Deck(footer=FOOTER)
b = d.b


# ── helpers ───────────────────────────────────────────────────────────────────

def divider(title: str, subtitle: str, page: int):
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, f"SECTION {page:02d}", Inches(0.45), Inches(2.5), Inches(10), Inches(0.38),
           size=13, color=b.TEAL, bold=True)
    d.text(s, title, Inches(0.45), Inches(3.0), Inches(11.5), Inches(1.3),
           size=44, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
    d.rect(s, Inches(0.45), Inches(4.35), Inches(2), Inches(0.06), b.TEAL)
    d.text(s, subtitle, Inches(0.45), Inches(4.55), Inches(10), Inches(0.5),
           size=18, color=b.LIGHT_TEAL, shrink=True)
    d.footer(s, page, TOTAL, dark=True)


def kpi_box(s, x, y, w, number, label, note, *, num_color=None):
    num_color = num_color or b.GOLD
    d.rect(s, x, y, w, Inches(1.55), b.NAVY, radius=0.06, shadow=True)
    d.text(s, number, x + Inches(0.18), y + Inches(0.12), w - Inches(0.36), Inches(0.7),
           size=36, color=num_color, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, label, x + Inches(0.12), y + Inches(0.78), w - Inches(0.24), Inches(0.42),
           size=12, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, note, x + Inches(0.12), y + Inches(1.22), w - Inches(0.24), Inches(0.28),
           size=9.5, color=b.MUTED, align=PP_ALIGN.CENTER, shrink=True)


def domain_card(s, x, y, w, h, cloud_color, domain, cloud, regs, lead, *, index):
    d.rect(s, x, y, w, h, b.SOFT, line=b.GRID, radius=0.05)
    d.rect(s, x, y, Inches(0.1), h, cloud_color)
    # index chip
    d.rect(s, x + Inches(0.18), y + Inches(0.12), Inches(0.36), Inches(0.28),
           b.NAVY, radius=0.08)
    d.text(s, str(index), x + Inches(0.18), y + Inches(0.12), Inches(0.36), Inches(0.28),
           size=10, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, domain, x + Inches(0.65), y + Inches(0.1), w - Inches(0.8), Inches(0.32),
           size=13, color=b.INK, bold=True, shrink=True)
    d.text(s, cloud, x + Inches(0.65), y + Inches(0.42), w - Inches(0.8), Inches(0.24),
           size=10, color=b.MUTED, shrink=True)
    d.text(s, regs, x + Inches(0.18), y + Inches(0.72), w - Inches(0.36), Inches(0.36),
           size=9, color=b.MUTED, shrink=True)
    d.text(s, lead, x + Inches(0.18), y + Inches(1.1), w - Inches(0.36), Inches(0.52),
           size=10, color=b.INK, shrink=True)


# ── SLIDE 1 — COVER ───────────────────────────────────────────────────────────

s = d.slide(fill=b.NAVY)
PANEL_W = Inches(8.8)
d.rect(s, PANEL_W, 0, d.W - PANEL_W, d.H, b.NAVY_2)
d.rect(s, PANEL_W, 0, Inches(0.06), d.H, b.TEAL)
d.text(s, "ENTERPRISE AI  ·  PRACTITIONER'S FRAMEWORK",
       d.M, Inches(0.9), Inches(8), Inches(0.38), size=13, color=b.TEAL, bold=True)
d.text(s, "Enterprise AI Platform Architecture",
       d.M, Inches(1.45), Inches(8.0), Inches(1.1), size=44, color=b.WHITE,
       bold=True, font=b.FONT_H, shrink=True)
d.text(s, "A Four-Tier Framework Across Five Domains and Three Hyperscalers",
       d.M, Inches(2.55), Inches(7.8), Inches(0.75), size=24, color=b.TEAL,
       bold=True, font=b.FONT_H, shrink=True)
d.rect(s, d.M, Inches(3.45), Inches(1.5), Inches(0.06), b.TEAL)
d.text(s, [
    {"text": "Use Case Cards · Solution Blueprints · Platform Architectures · Realization Patterns", "size": 15, "color": b.WHITE},
    {"text": "sourced from GCP 101 Blueprints · AWS Gen AI Atlas · Microsoft Azure Scenario Library", "size": 13, "color": b.LIGHT_TEAL, "space_before": 6},
], d.M, Inches(3.68), Inches(7.8), Inches(0.85), shrink=True)
sx = PANEL_W + Inches(0.42)
d.text(s, "FOR ENTERPRISE LEADERS", sx, Inches(1.8), Inches(3.8), Inches(0.3),
       size=11, color=b.TEAL, bold=True)
for i, (h, body) in enumerate([
    ("The question", "Which AI investments survive beyond the pilot?"),
    ("The framework", "Four-tier architecture for every domain."),
    ("The outcome", "90-day path to production-grade AI."),
]):
    y = Inches(2.3) + i * Inches(1.3)
    d.text(s, h.upper(), sx, y, Inches(3.8), Inches(0.28), size=11, color=b.GOLD, bold=True)
    d.text(s, body, sx, y + Inches(0.28), Inches(3.8), Inches(0.85), size=14, color=b.WHITE,
           bold=True, shrink=True)
d.text(s, FOOTER, d.M, Inches(6.9), Inches(9), Inches(0.3), size=10,
       color=RGBColor(0x6B, 0x7C, 0x8C))


# ── SLIDE 2 — EXECUTIVE SUMMARY ───────────────────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "Executive Summary", "If you read one slide, read this one")
d.rect(s, d.M, Inches(1.58), d.CW, Inches(0.95), b.NAVY, radius=0.06, shadow=True)
d.rect(s, d.M, Inches(1.58), Inches(0.12), Inches(0.95), b.TEAL)
d.text(s, "BOTTOM LINE", d.M + Inches(0.3), Inches(1.7), Inches(2.5), Inches(0.26),
       size=11, color=b.TEAL, bold=True)
d.text(s, "Fewer than 10% of enterprise AI pilots reach production. The gap is not the model — it is the platform, the governance, and the missing use-case-to-architecture chain.",
       d.M + Inches(0.3), Inches(1.98), d.CW - Inches(0.65), Inches(0.48),
       size=15.5, color=b.WHITE, bold=True, shrink=True)
cols = [
    ("THE CHALLENGE", b.TEAL, [
        "AI pilots stall: no measurable KPI, no named process owner, no production-ready platform.",
        "Each use case reinvents security, governance, and compliance — at 10× the cost.",
        "Regulated industries (healthcare, FSI, manufacturing) have non-negotiable compliance floors.",
    ]),
    ("THE FRAMEWORK", b.GOLD, [
        "Four-tier artifact system: platform → blueprint → use case card → realization pattern.",
        "Six production-ready platform architectures across five domains and three hyperscalers.",
        "Each platform: defense-in-depth, RAI governance, NIST AI RMF, pre-production checklist.",
    ]),
    ("THE OUTCOME", b.ACCENT, [
        "Select the right use case for your domain in one conversation.",
        "Deploy into a pre-built, compliance-ready platform — not from scratch.",
        "90-day path: baseline KPI → build → pilot → go/no-go with hard criteria.",
    ]),
]
gap = Inches(0.28)
cw = (d.CW - gap * 2) / 3
top = Inches(2.72)
h = Inches(2.65)
for i, (title, accent, items) in enumerate(cols):
    x = d.M + i * (cw + gap)
    d.rect(s, x, top, cw, h, b.SOFT, line=b.GRID, radius=0.05)
    d.rect(s, x, top, cw, Inches(0.48), b.NAVY, radius=0.05)
    d.rect(s, x, top, Inches(0.1), Inches(0.48), accent)
    d.text(s, title, x + Inches(0.22), top + Inches(0.09), cw - Inches(0.38), Inches(0.3),
           size=12, color=accent, bold=True)
    d.text(s, [{"text": it, "size": 11.5, "color": b.INK, "bullet": True, "space_before": 9}
               for it in items],
           x + Inches(0.22), top + Inches(0.62), cw - Inches(0.44), h - Inches(0.82),
           shrink=True, ls=1.08)
d.rect(s, d.M, Inches(5.5), d.CW, Inches(0.72), b.GOLD, radius=0.06)
d.text(s, "THE STARTING POINT", d.M + Inches(0.3), Inches(5.6), Inches(3), Inches(0.28),
       size=11, color=b.NAVY, bold=True)
d.text(s, "Pick your domain → read the platform architecture → run a 3-use-case pilot with KPI baselines",
       d.M + Inches(0.3), Inches(5.88), d.CW - Inches(0.6), Inches(0.28),
       size=14, color=b.NAVY, bold=True, shrink=True)
d.footer(s, 2, TOTAL)


# ── SLIDE 3 — SECTION DIVIDER: THE PROBLEM ───────────────────────────────────

divider("Fewer Than 10% of AI Pilots Reach Production",
        "The gap is not the model. It is the platform.", 3)


# ── SLIDE 4 — THE AI IMPERATIVE (KPI GRID) ───────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "The Opportunity Is Real. The Execution Gap Is Real.", "Enterprise AI adoption data — 2025")
bw = (d.CW - Inches(0.6)) / 4
bx = d.M
by = Inches(1.82)
kpis = [
    ("<10%", "of AI use cases\npast pilot stage", "McKinsey, June 2025", b.CORAL),
    ("80%", "of enterprises\nusing gen AI today", "McKinsey, June 2025", b.TEAL),
    ("4.2×", "ROI in Financial\nServices (Azure)", "Microsoft, 2025", b.GOLD),
    ("600+", "real-world GCP AI\ndeployments", "GCP 101 Blueprints, 2025", b.TEAL),
]
for i, (num, lbl, note, col) in enumerate(kpis):
    kpi_box(s, bx + i * (bw + Inches(0.2)), by, bw, num, lbl, note, num_color=col)

d.text(s, "ROI BY VERTICAL  (Microsoft, 2025)", d.M, Inches(3.6), d.CW, Inches(0.28),
       size=11, color=b.MUTED, bold=True)
roi_data = [
    ("Financial Services", "4.2×", 4.2),
    ("Retail & CPG",       "3.6×", 3.6),
    ("Manufacturing",      "3.4×", 3.4),
    ("Healthcare",         "3.3×", 3.3),
    ("Cross-Industry",     "2.8×", 2.8),
]
bar_w_total = d.CW
max_val = 4.2
bar_h = Inches(0.46)
by2 = Inches(4.0)
for i, (label, roi_str, val) in enumerate(roi_data):
    y = by2 + i * (bar_h + Inches(0.12))
    blen = bar_w_total * (val / (max_val * 1.25))
    d.rect(s, d.M, y, bar_w_total, bar_h, b.SOFT, radius=0.03)
    d.rect(s, d.M, y, blen, bar_h, b.TEAL if i == 0 else b.ACCENT, radius=0.03)
    d.text(s, label, d.M + Inches(0.15), y + Inches(0.08), Inches(3.5), Inches(0.3),
           size=12.5, color=b.WHITE, bold=True)
    d.text(s, roi_str, d.M + blen + Inches(0.12), y + Inches(0.08), Inches(1.2), Inches(0.3),
           size=13, color=b.GOLD, bold=True)
d.footer(s, 4, TOTAL)


# ── SLIDE 5 — SECTION DIVIDER: THE FRAMEWORK ─────────────────────────────────

divider("Four Tiers, One Platform", "From business case to production — a connected chain", 5)


# ── SLIDE 6 — FOUR-TIER ARTIFACT SYSTEM ──────────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "The Four-Tier Artifact System", "Every use case described at four levels — for four audiences")
tiers = [
    (b.TEAL,   "TIER 1",  "Enterprise AI Platform Architecture",
     "CTO · CISO · Compliance",
     "Shared security, governance, and RAI controls. Every AI workload inherits this platform. One per domain × cloud."),
    (b.ACCENT, "TIER 2",  "Solution Blueprint",
     "Enterprise Architect · Delivery Lead",
     "How to build one specific use case: architecture diagram, integration points, build-vs-buy decisions."),
    (b.GOLD,   "TIER 3",  "Use Case Card",
     "Business Buyer · Account Exec",
     "What to build and why: ROI benchmarks, hyperscaler evidence, risk/readiness, pilot KPIs."),
    (b.AMBER,  "TIER 4",  "Realization Pattern",
     "Data Engineer · Implementer",
     "The technical pattern: RAG, Knowledge Graph + MCP, Document AI, or Multi-Agent — with code."),
]
tw = (d.CW - Inches(0.6)) / 4
for i, (col, label, title, audience, desc) in enumerate(tiers):
    x = d.M + i * (tw + Inches(0.2))
    y = Inches(1.75)
    h = Inches(4.4)
    d.rect(s, x, y, tw, h, b.SOFT, line=b.GRID, radius=0.05)
    d.rect(s, x, y, tw, Inches(0.08), col)
    d.text(s, label, x + Inches(0.15), y + Inches(0.16), tw - Inches(0.3), Inches(0.25),
           size=10, color=col, bold=True)
    d.text(s, title, x + Inches(0.15), y + Inches(0.45), tw - Inches(0.3), Inches(0.6),
           size=13, color=b.INK, bold=True, shrink=True)
    d.rect(s, x + Inches(0.15), y + Inches(1.1), tw - Inches(0.3), Inches(0.04), col)
    d.text(s, audience, x + Inches(0.15), y + Inches(1.22), tw - Inches(0.3), Inches(0.32),
           size=10, color=b.MUTED, shrink=True)
    d.text(s, desc, x + Inches(0.15), y + Inches(1.65), tw - Inches(0.3), Inches(2.5),
           size=11, color=b.INK, shrink=True, ls=1.1)
    if i < 3:
        d.text(s, "↓", x + tw + Inches(0.03), y + Inches(2.0), Inches(0.2), Inches(0.3),
               size=20, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
d.text(s, "Navigate the bundle: start from Tier 3 (business case) → confirm Tier 1 platform → build to Tier 2 blueprint → implement via Tier 4 pattern",
       d.M, Inches(6.35), d.CW, Inches(0.45), size=12, color=b.MUTED, shrink=True)
d.footer(s, 6, TOTAL)


# ── SLIDE 7 — SECTION DIVIDER: PLATFORM ARCHITECTURES ────────────────────────

divider("Six Platform Architectures. Five Domains. Three Hyperscalers.",
        "One per domain × cloud — not one per use case", 7)


# ── SLIDE 8 — PLATFORM COVERAGE TABLE ────────────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "Platform Architecture Coverage", "The Tier 1 layer — shared by all workloads in that domain")

AWS_COL  = RGBColor(0xFF, 0x99, 0x00)   # AWS orange
GCP_COL  = RGBColor(0x34, 0xA8, 0x53)   # GCP green
AZ_COL   = RGBColor(0x00, 0x78, 0xD4)   # Azure blue

domains = [
    (AZ_COL,  "Healthcare (AWS)",         "AWS",   "HIPAA · NIST AI RMF · CMS Final Rule 2024",  "HealthLake FHIR R4 · Comprehend Medical · Bedrock Guardrails"),
    (GCP_COL, "Healthcare (GCP)",         "GCP",   "HIPAA · SAIF · NIST AI RMF · CMS Final Rule","Knowledge Catalog MCP · MedLM · SAIF automated controls"),
    (AWS_COL, "Financial Services (AWS)", "AWS",   "SOX · PCI-DSS · SR 11-7 · BSA/AML · FINRA", "KYC pipeline · SEC 17a-4 WORM · Bedrock + Textract"),
    (GCP_COL, "Retail & CPG (GCP)",       "GCP",   "GDPR · CCPA · PCI-DSS · EU AI Act",          "Vertex AI Search for Commerce · Knowledge Catalog product grounding"),
    (AZ_COL,  "Manufacturing (Azure)",    "Azure", "IEC 62443 · ISO 27001 · ITAR · ISO 9001",    "IoT Hub · Digital Twins · IT/OT one-way data flow · IoT Edge"),
    (AWS_COL, "Cross-Industry (AWS)",     "AWS",   "SOC 2 Type II · GDPR · CCPA · NIST AI RMF",  "Bedrock Knowledge Bases · managed RAG · starter platform"),
]
row_h = Inches(0.68)
top = Inches(1.75)
hdr_cols = ["Domain", "Cloud", "Regulatory Baseline", "Lead Capability"]
col_widths = [Inches(2.5), Inches(0.9), Inches(3.5), Inches(4.93)]
cx = d.M
d.rect(s, d.M, top, d.CW, Inches(0.4), b.NAVY)
for j, (hdr, cw) in enumerate(zip(hdr_cols, col_widths)):
    d.text(s, hdr, cx + Inches(0.1), top + Inches(0.06), cw - Inches(0.15), Inches(0.28),
           size=11, color=b.TEAL, bold=True)
    cx += cw
for i, (col, domain, cloud, regs, lead) in enumerate(domains):
    y = top + Inches(0.4) + i * row_h
    fill = b.SOFT if i % 2 == 0 else b.WHITE
    d.rect(s, d.M, y, d.CW, row_h, fill, line=b.GRID)
    d.rect(s, d.M, y, Inches(0.1), row_h, col)
    cells = [domain, cloud, regs, lead]
    cx = d.M + Inches(0.18)
    for j, (cell, cw) in enumerate(zip(cells, col_widths)):
        fw = cw - Inches(0.22) if j > 0 else cw - Inches(0.28)
        d.text(s, cell, cx, y + Inches(0.1), fw, row_h - Inches(0.16),
               size=10.5 if j != 1 else 11, color=b.INK,
               bold=(j == 0), shrink=True)
        cx += cw
d.footer(s, 8, TOTAL)


# ── SLIDE 9 — HEALTHCARE PLATFORM ────────────────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "Healthcare: Dual-Cloud Coverage", "AWS leads on HIPAA BAA breadth; GCP leads on data governance and MedLM")

for col_i, (cloud_col, cloud_name, points) in enumerate([
    (AWS_COL, "AWS — Healthcare Payer", [
        "Broadest HIPAA BAA: HealthLake, Bedrock, Textract, Comprehend Medical, Macie all sign BAA",
        "HealthLake: only cloud-native FHIR R4 store — CMS Final Rule 2024 compliant (72hr PA, denial reason)",
        "PHI tokenization: Textract → Comprehend Medical → Macie → Lambda tokenizer → HealthLake",
        "Bedrock Guardrails: PII filter + topic denial + grounding check out of the box",
        "Audit: Bedrock Invocation Logging → S3 Object Lock (7-year WORM retention)",
    ]),
    (GCP_COL, "GCP — Healthcare Payer", [
        "Knowledge Catalog MCP: agents query PHI data lineage via tool call — no custom integration",
        "VPC Service Controls perimeter wraps aiplatform, healthcare, bigquery, storage, dataplex, cloudkms",
        "SAIF 6-element framework: GCP Recommended AI Controls (NIST AI RMF automated via Security Command Center)",
        "MedLM: purpose-built clinical NLP — outperforms general LLMs on ICD, RxNorm, clinical note tasks",
        "BeyondCorp Enterprise: zero-trust access for clinical reviewer workstations",
    ]),
]):
    x = d.M + col_i * (d.CW / 2 + Inches(0.15))
    cw = d.CW / 2 - Inches(0.1)
    d.rect(s, x, Inches(1.72), cw, Inches(0.4), b.NAVY, radius=0.04)
    d.rect(s, x, Inches(1.72), Inches(0.1), Inches(0.4), cloud_col)
    d.text(s, cloud_name, x + Inches(0.22), Inches(1.79), cw - Inches(0.3), Inches(0.26),
           size=12, color=b.WHITE, bold=True, shrink=True)
    d.text(s, [{"text": p, "bullet": True, "size": 11, "color": b.INK, "space_before": 9}
               for p in points],
           x + Inches(0.15), Inches(2.22), cw - Inches(0.3), Inches(3.6),
           shrink=True, ls=1.08)

d.rect(s, d.M, Inches(5.95), d.CW, Inches(0.72), b.SOFT, line=b.GRID, radius=0.04)
d.text(s, "CHOOSE AWS WHEN: Epic/Cerner integration is critical path; deep AWS expertise in-house; Bedrock Guardrails + Automated Reasoning is the compliance preference.",
       d.M + Inches(0.2), Inches(6.05), d.CW / 2 - Inches(0.3), Inches(0.55),
       size=10.5, color=b.INK, shrink=True)
d.text(s, "CHOOSE GCP WHEN: MedLM clinical AI is a priority; existing BigQuery data estate; Knowledge Catalog MCP for grounded agents; SAIF automated controls preferred.",
       d.M + d.CW / 2 + Inches(0.1), Inches(6.05), d.CW / 2 - Inches(0.2), Inches(0.55),
       size=10.5, color=b.INK, shrink=True)
d.footer(s, 9, TOTAL)


# ── SLIDE 10 — FSI PLATFORM ───────────────────────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "Financial Services: AWS — Production-Grade Compliance Stack",
         "SOX · PCI-DSS · SR 11-7 · BSA/AML · FINRA · SEC 17a-4 · GLBA")

items_l = [
    ("Model Risk (SR 11-7)", "Every T3/T4 model requires SR 11-7 validation: model card, challenger model, independent validation, CCAR-ready documentation."),
    ("KYC Document Pipeline", "Textract → Comprehend Medical NER → Macie PII scan → Lambda tokenizer → Bedrock Claude → Validation Lambda → CRM write. 90–99% extraction recall."),
    ("AML / BSA", "Custom SageMaker transaction scoring + Bedrock Agents for SAR draft generation. 5-year audit trail. Human-in-loop escalation required."),
    ("SEC 17a-4 / FINRA 4511", "Bedrock Model Invocation Logging → S3 Object Lock (WORM, 6-year minimum). All AI-generated client communications immutably stored."),
]
items_r = [
    ("PCI-DSS Scope", "Tokenize PAN before any LLM call. Cardholder data environment (CDE) isolated from AI workload VPC. Never send raw cardholder data to Bedrock."),
    ("Reg BI (Wealth AI)", "Wealth advisory copilot: AI cannot be sole basis for advice. Recommendation explainability required. Human advisor reviews all AI output before client delivery."),
    ("Security Scoping", "SCOPE 6 (credit underwriting): VPC + KMS + SR 11-7 + ECOA/Reg B compliance + explainability. SCOPE 1 (client chatbot): Guardrails + DLP + WAF."),
    ("Model Tier Policy", "T1–T4 tiers: T4 (automated credit decision) requires CRO + Legal + Model Risk + Regulatory Affairs + Board Risk Committee sign-off."),
]
for col_i, items in enumerate([items_l, items_r]):
    x = d.M + col_i * (d.CW / 2 + Inches(0.12))
    cw = d.CW / 2 - Inches(0.06)
    for j, (title, body) in enumerate(items):
        y = Inches(1.72) + j * Inches(1.3)
        d.rect(s, x, y, cw, Inches(1.2), b.SOFT, line=b.GRID, radius=0.04)
        d.rect(s, x, y, Inches(0.1), Inches(1.2), AWS_COL)
        d.text(s, title, x + Inches(0.22), y + Inches(0.1), cw - Inches(0.35), Inches(0.26),
               size=11.5, color=b.INK, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.22), y + Inches(0.4), cw - Inches(0.35), Inches(0.72),
               size=10.5, color=b.INK, shrink=True, ls=1.05)
d.footer(s, 10, TOTAL)


# ── SLIDE 11 — RETAIL & CPG PLATFORM ─────────────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "Retail & CPG: GCP — Personalization at Catalog Scale",
         "GDPR · CCPA · PCI-DSS · EU AI Act  ·  Vertex AI Search for Commerce")

highlights = [
    ("Vertex AI Search for Commerce", "Semantic personalized search across 1M+ SKU catalogs. Handles ambiguous queries, synonyms, attribute-based filtering. Integrates with Merchant Center."),
    ("Knowledge Catalog MCP", "Product catalog grounding via MCP toolset — AI agents query AlloyDB product metadata before generating descriptions. Eliminates hallucinated product specs."),
    ("Cloud DLP + GDPR Compliance", "Customer PII scanned before any AI ingestion. GDPR Art. 22: personalization opt-out path required. AI-generated content labeled (EU AI Act transparency)."),
    ("Recommendations AI", "Collaborative filtering + session-based recs. CTR and CVR uplift validated weekly vs control group. Feature drift monitoring on purchase/browse history inputs."),
    ("VPC Service Controls", "Perimeter 'retail-ai-prod' wraps aiplatform, bigquery, storage, dataplex, cloudkms. Data exfiltration prevention even with compromised credentials."),
    ("Model Tier Policy", "T4 (dynamic real-time pricing): requires CMO + Legal + CISO + Privacy Officer sign-off AND GDPR Art. 22 assessment before activation."),
]
tw = (d.CW - Inches(0.24)) / 3
th = Inches(1.5)
for i, (title, body) in enumerate(highlights):
    row, col = divmod(i, 3)
    x = d.M + col * (tw + Inches(0.12))
    y = Inches(1.72) + row * (th + Inches(0.16))
    d.rect(s, x, y, tw, th, b.SOFT, line=b.GRID, radius=0.04)
    d.rect(s, x, y, tw, Inches(0.07), GCP_COL)
    d.text(s, title, x + Inches(0.15), y + Inches(0.16), tw - Inches(0.3), Inches(0.32),
           size=11.5, color=b.INK, bold=True, shrink=True)
    d.text(s, body, x + Inches(0.15), y + Inches(0.54), tw - Inches(0.3), Inches(0.86),
           size=10.5, color=b.INK, shrink=True, ls=1.05)
d.footer(s, 11, TOTAL)


# ── SLIDE 12 — MANUFACTURING PLATFORM ────────────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "Manufacturing: Azure — IEC 62443 + IT/OT Convergence",
         "IEC 62443 · ITAR · ISO 9001 · ISO 27001  ·  IT/OT one-way data flow enforced")

d.rect(s, d.M, Inches(1.7), d.CW, Inches(0.95), b.NAVY, radius=0.05, shadow=True)
d.rect(s, d.M, Inches(1.7), Inches(0.12), Inches(0.95), b.CORAL)
d.text(s, "CRITICAL RULE", d.M + Inches(0.3), Inches(1.82), Inches(2.5), Inches(0.26),
       size=11, color=b.CORAL, bold=True)
d.text(s, "AI models NEVER write directly to OT systems (PLCs, SCADA, DCS, SIS). Data flows one-way: OT → IT. Human confirms all OT actions via work order.",
       d.M + Inches(0.3), Inches(2.1), d.CW - Inches(0.65), Inches(0.44),
       size=15, color=b.WHITE, bold=True, shrink=True)

flow_items = ["OT Sensors / PLCs", "Azure IoT Hub\n(telemetry only)", "Azure Digital Twins\n+ Azure ML", "Technician App\n(human confirms)", "Work Order System\n(physical action)"]
fw = (d.CW - Inches(0.8)) / 5
for i, item in enumerate(flow_items):
    x = d.M + i * (fw + Inches(0.2))
    fc = b.TEAL if i == 0 else (b.ACCENT if i in [1, 2] else b.NAVY)
    d.rect(s, x, Inches(2.88), fw, Inches(0.82), fc, radius=0.04)
    d.text(s, item, x + Inches(0.08), Inches(2.94), fw - Inches(0.16), Inches(0.7),
           size=10.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    if i < 4:
        d.text(s, "→", x + fw + Inches(0.02), Inches(3.1), Inches(0.2), Inches(0.3),
               size=18, color=b.TEAL, bold=True)

az_points = [
    ("Azure IoT Hub + Digital Twins", "Device identity (X.509 certs), telemetry at scale, real-time facility simulation"),
    ("Azure ML — Predictive Maintenance", "Custom models on sensor telemetry; false negative rate < 0.1% gate before production"),
    ("Azure Computer Vision (IoT Edge)", "Visual QC at <5ms latency on production line; model updates via IoT Edge deployment manifest"),
    ("ITAR Compliance", "US-only Azure regions; Microsoft Purview classifies export-controlled technical data; no egress to non-US"),
    ("Defender for IoT", "Passive OT network monitoring (no active scanning); anomaly detection per IEC 62443 SL-2"),
    ("Model Tier Policy", "T4 (autonomous line stop): COO + Safety Board + OT Security Lead + Legal + IEC 62443 SIL assessment required"),
]
tw2 = (d.CW - Inches(0.18)) / 3
for i, (title, body) in enumerate(az_points):
    row, col = divmod(i, 3)
    x = d.M + col * (tw2 + Inches(0.09))
    y = Inches(3.88) + row * Inches(1.02)
    d.rect(s, x, y, tw2, Inches(0.94), b.SOFT, line=b.GRID, radius=0.03)
    d.rect(s, x, y, Inches(0.08), Inches(0.94), AZ_COL)
    d.text(s, title, x + Inches(0.18), y + Inches(0.07), tw2 - Inches(0.28), Inches(0.26),
           size=10.5, color=b.INK, bold=True, shrink=True)
    d.text(s, body, x + Inches(0.18), y + Inches(0.38), tw2 - Inches(0.28), Inches(0.5),
           size=9.5, color=b.INK, shrink=True, ls=1.05)
d.footer(s, 12, TOTAL)


# ── SLIDE 13 — CROSS-INDUSTRY PLATFORM ───────────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "Cross-Industry: AWS — The Starter Platform",
         "SOC 2 Type II · GDPR · CCPA  ·  Bedrock Knowledge Bases  ·  1–4 month time to value")

d.text(s, "Use this platform when your workload has no vertical-specific regulatory overlay (no HIPAA, PCI-CDE, OT/ICS). Fastest path to production.",
       d.M, Inches(1.72), d.CW, Inches(0.4), size=13, color=b.MUTED, shrink=True)

use_cases = [
    ("Enterprise Search", "RAG", "1–4 mo", "Bedrock Knowledge Bases + OpenSearch Serverless. Managed chunking + Titan Embeddings. No custom pipeline."),
    ("Document Processing", "Document AI", "2–6 mo", "Textract + Comprehend → Bedrock enrichment. 90–99% extraction recall vs 70–85% for prompted LLMs."),
    ("Meeting Summarization", "RAG", "1–3 mo", "Transcription → Bedrock Claude. Bedrock Guardrails PII filter on all meeting content before processing."),
    ("Code Generation", "RAG", "1–3 mo", "Bedrock → IDE integration. Repository context via Knowledge Bases. System prompt scoped per language/stack."),
]
tw3 = (d.CW - Inches(0.36)) / 4
for i, (title, pattern, timeline, body) in enumerate(use_cases):
    x = d.M + i * (tw3 + Inches(0.12))
    y = Inches(2.28)
    h3 = Inches(3.2)
    d.rect(s, x, y, tw3, h3, b.SOFT, line=b.GRID, radius=0.05)
    d.rect(s, x, y, tw3, Inches(0.07), AWS_COL)
    d.rect(s, x + Inches(0.15), y + Inches(0.22), tw3 - Inches(0.3), Inches(0.36),
           b.NAVY, radius=0.06)
    d.text(s, title, x + Inches(0.15), y + Inches(0.28), tw3 - Inches(0.3), Inches(0.26),
           size=12, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, f"Pattern: {pattern}", x + Inches(0.15), y + Inches(0.72), tw3 - Inches(0.3), Inches(0.24),
           size=10, color=b.TEAL, bold=True, shrink=True)
    d.text(s, f"ROI: {timeline}", x + Inches(0.15), y + Inches(0.98), tw3 - Inches(0.3), Inches(0.24),
           size=10, color=b.GOLD, bold=True, shrink=True)
    d.text(s, body, x + Inches(0.15), y + Inches(1.32), tw3 - Inches(0.3), Inches(1.72),
           size=10.5, color=b.INK, shrink=True, ls=1.08)

platform_points = [
    "Bedrock + PrivateLink: all LLM calls on private network — no public endpoints",
    "Bedrock Guardrails: topic denial, PII filter, grounding check — configured per use case",
    "SOC 2 Type II: AWS Audit Manager + CloudTrail automated evidence collection",
    "Cost anomaly detection: GuardDuty + Cost Anomaly Detection flags injection attacks as spend spikes",
]
d.rect(s, d.M, Inches(5.62), d.CW, Inches(1.15), b.SOFT, line=b.GRID, radius=0.04)
d.text(s, "PLATFORM GUARANTEES (inherited by all use cases)",
       d.M + Inches(0.2), Inches(5.72), Inches(4), Inches(0.26),
       size=11, color=b.MUTED, bold=True)
bw4 = (d.CW - Inches(0.4)) / 4
for i, pt in enumerate(platform_points):
    x = d.M + Inches(0.2) + i * (bw4 + Inches(0.06))
    d.text(s, pt, x, Inches(6.04), bw4, Inches(0.62),
           size=10, color=b.INK, shrink=True, ls=1.05)
d.footer(s, 13, TOTAL)


# ── SLIDE 14 — SECTION DIVIDER: USE CASES ────────────────────────────────────

divider("Where the Value Is", "Top use cases by vertical — with ROI timelines and realization patterns", 14)


# ── SLIDE 15 — USE CASES BY VERTICAL ─────────────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "Top Use Cases by Vertical — ROI Benchmarks",
         "Sources: GCP 101 Blueprints · AWS Gen AI Atlas · Microsoft AI Scenario Library · McKinsey 2025")

uc_rows = [
    ("Healthcare",       "Prior Authorization Automation",      "Multi-Agent + Doc AI", "6–12 mo", "3.3×", GCP_COL),
    ("Healthcare",       "Clinical Documentation (Ambient AI)", "RAG",                  "2–4 mo",  "3.3×", GCP_COL),
    ("Financial Svcs",   "KYC Document Processing",             "Document AI",          "2–6 mo",  "4.2×", AWS_COL),
    ("Financial Svcs",   "Wealth Advisory Copilot",             "RAG",                  "1–4 mo",  "4.2×", AWS_COL),
    ("Financial Svcs",   "AML Transaction Screening",           "Multi-Agent + ML",     "3–9 mo",  "4.2×", AWS_COL),
    ("Retail & CPG",     "Personalized Product Search",         "RAG + Recs AI",        "1–4 mo",  "3.6×", GCP_COL),
    ("Retail & CPG",     "Demand Forecasting",                  "Custom ML",            "2–6 mo",  "3.6×", GCP_COL),
    ("Manufacturing",    "Predictive Maintenance",              "Custom ML (Edge)",     "6–18 mo", "3.4×", AZ_COL),
    ("Manufacturing",    "Visual QC Inspection",                "Computer Vision",      "3–9 mo",  "3.4×", AZ_COL),
    ("Cross-Industry",   "Enterprise Search",                   "RAG",                  "1–4 mo",  "varies", AWS_COL),
    ("Cross-Industry",   "Meeting Summarization + Code Gen",    "RAG",                  "1–3 mo",  "varies", AWS_COL),
]
col_ws = [Inches(1.95), Inches(3.3), Inches(2.2), Inches(1.3), Inches(1.0)]
headers = ["Vertical", "Use Case", "Pattern", "Timeline", "ROI"]
top = Inches(1.72)
rh = Inches(0.45)
d.rect(s, d.M, top, d.CW, Inches(0.38), b.NAVY)
cx = d.M
for hdr, cw_h in zip(headers, col_ws):
    d.text(s, hdr, cx + Inches(0.08), top + Inches(0.05), cw_h - Inches(0.12), Inches(0.28),
           size=11, color=b.TEAL, bold=True)
    cx += cw_h

for i, (vertical, uc_name, pattern, timeline, roi, vcol) in enumerate(uc_rows):
    y = top + Inches(0.38) + i * rh
    fill = b.SOFT if i % 2 == 0 else b.WHITE
    d.rect(s, d.M, y, d.CW, rh, fill, line=b.GRID)
    d.rect(s, d.M, y, Inches(0.08), rh, vcol)
    cells = [vertical, uc_name, pattern, timeline, roi]
    cx = d.M + Inches(0.16)
    for j, (cell, cw_c) in enumerate(zip(cells, col_ws)):
        col_text = b.GOLD if j == 4 else b.INK
        fw = cw_c - Inches(0.18) if j > 0 else cw_c - Inches(0.2)
        d.text(s, cell, cx, y + Inches(0.06), fw, rh - Inches(0.1),
               size=10.5 if j != 4 else 12, color=col_text,
               bold=(j in [0, 4]), shrink=True)
        cx += cw_c
d.footer(s, 15, TOTAL)


# ── SLIDE 16 — SECTION DIVIDER: REALIZATION PATTERNS ─────────────────────────

divider("Four Patterns. One Decision Tree.",
        "Match your source data and query type to the right architecture", 16)


# ── SLIDE 17 — REALIZATION PATTERN SELECTION ─────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "Realization Pattern Selection Guide",
         "Start here before designing any AI workload — pattern determines cost, accuracy, and build time")

patterns = [
    (b.TEAL,   "RAG",
     "Retrieval Augmented Generation",
     "WHEN: Unstructured docs (PDFs, emails, policies). Semantic queries: 'what does our policy say about...'",
     "Stack: Embedding model + vector DB + LLM. Managed: Bedrock Knowledge Bases (AWS), Vertex AI Search (GCP).",
     "Setup: 2–5 days  |  Cost: ~$200–500/mo  |  Maturity: HIGH"),
    (b.ACCENT, "KG + MCP",
     "Knowledge Graph + MCP",
     "WHEN: Structured metadata (tables, schemas, lineage, data catalogs). Agents need deterministic tool calls.",
     "Stack: Enterprise catalog (GCP Knowledge Catalog native MCP / AWS Glue + Lambda / Azure Purview REST).",
     "Agent accuracy 93–97% vs ~60% RAG on catalog queries.  |  Setup: 1–4 weeks"),
    (b.GOLD,   "Doc AI",
     "Document AI",
     "WHEN: High-volume structured documents — invoices, KYC forms, contracts. Deterministic extraction.",
     "Stack: GCP Document AI (70+ processors) / AWS Textract + Comprehend / Azure Form Recognizer.",
     "Recall: 90–99% on trained models. Cost: 10–50× lower than LLM-per-page at scale."),
    (b.AMBER,  "Multi-Agent",
     "Multi-Agent Orchestration",
     "WHEN: Workflow has 3+ decision points requiring different tools, data sources, or role separations.",
     "Stack: Orchestrator (ADK / LangGraph / Bedrock Agents) + specialist subagents with scoped tools.",
     "Best for: Prior Auth, KYC onboarding, AML workflow, procurement.  |  Setup: 6–12 weeks"),
]
tw4 = (d.CW - Inches(0.36)) / 4
for i, (col, short, full, when, how, note) in enumerate(patterns):
    x = d.M + i * (tw4 + Inches(0.12))
    d.rect(s, x, Inches(1.72), tw4, Inches(5.1), b.SOFT, line=b.GRID, radius=0.05)
    d.rect(s, x, Inches(1.72), tw4, Inches(0.08), col)
    d.rect(s, x + Inches(0.15), Inches(1.9), tw4 - Inches(0.3), Inches(0.56), b.NAVY, radius=0.06)
    d.text(s, short, x + Inches(0.15), Inches(1.96), tw4 - Inches(0.3), Inches(0.28),
           size=16, color=col, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, full, x + Inches(0.15), Inches(2.58), tw4 - Inches(0.3), Inches(0.38),
           size=10.5, color=b.INK, bold=True, shrink=True)
    d.rect(s, x + Inches(0.15), Inches(3.0), tw4 - Inches(0.3), Inches(0.04), col)
    d.text(s, when, x + Inches(0.15), Inches(3.1), tw4 - Inches(0.3), Inches(1.1),
           size=10, color=b.INK, shrink=True, ls=1.08)
    d.text(s, how, x + Inches(0.15), Inches(4.28), tw4 - Inches(0.3), Inches(1.1),
           size=10, color=b.MUTED, shrink=True, ls=1.05)
    d.text(s, note, x + Inches(0.15), Inches(5.45), tw4 - Inches(0.3), Inches(0.3),
           size=9.5, color=col, bold=True, shrink=True)

d.text(s, "COMMON ANTI-PATTERN: Using a prompted LLM as the primary extractor for high-volume structured forms. Recall is 15–25 pts lower than Document AI and cost is 10–50× higher.",
       d.M, Inches(6.95), d.CW, Inches(0.38), size=11, color=b.CORAL, bold=True, shrink=True)
d.footer(s, 17, TOTAL)


# ── SLIDE 18 — RESPONSIBLE AI + GOVERNANCE ───────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "Responsible AI & Defense-in-Depth", "Governance gates and security controls — built into every platform architecture")

d.text(s, "4-STAGE RAI FRAMEWORK  (Microsoft Responsible AI Standard / NIST AI RMF)",
       d.M, Inches(1.72), d.CW, Inches(0.28), size=11, color=b.MUTED, bold=True)
rai_stages = [
    (b.TEAL,   "IDENTIFY",  "Document intended use, prohibited uses, affected populations. Classify SCOPE tier (1–6). Assign Model Tier (T1–T4)."),
    (b.ACCENT, "MEASURE",   "Accuracy benchmarks, bias evaluation, adversarial red-team. Bedrock Model Evaluation / Vertex AI Fairness Indicators."),
    (b.GOLD,   "MITIGATE",  "Implement guardrails, human-in-loop for high-risk decisions, fallback to non-AI path. Feature-flag gradual rollout."),
    (b.AMBER,  "OPERATE",   "Monthly drift monitoring, quarterly model review, usage pattern anomaly detection. Named model owner required."),
]
sw = (d.CW - Inches(0.36)) / 4
for i, (col, label, body) in enumerate(rai_stages):
    x = d.M + i * (sw + Inches(0.12))
    d.rect(s, x, Inches(2.1), sw, Inches(1.42), b.SOFT, line=b.GRID, radius=0.04)
    d.rect(s, x, Inches(2.1), sw, Inches(0.07), col)
    d.text(s, label, x + Inches(0.15), Inches(2.26), sw - Inches(0.3), Inches(0.28),
           size=13, color=col, bold=True)
    d.text(s, body, x + Inches(0.15), Inches(2.62), sw - Inches(0.3), Inches(0.85),
           size=10.5, color=b.INK, shrink=True, ls=1.06)
    if i < 3:
        d.text(s, "→", x + sw + Inches(0.01), Inches(2.55), Inches(0.15), Inches(0.4),
               size=20, color=b.TEAL, bold=True)

d.text(s, "DEFENSE-IN-DEPTH  (4 layers — every platform, every domain)",
       d.M, Inches(3.72), d.CW, Inches(0.28), size=11, color=b.MUTED, bold=True)
layers = [
    ("INPUT", b.TEAL,   "Prompt injection detection · PII/PCD scrubbing · Rate limiting · Document size limits"),
    ("MODEL", b.ACCENT, "System prompt hardening · Context isolation · Approved model list (IAM policy) · Private endpoints only"),
    ("OUTPUT", b.GOLD,  "Grounding score threshold · Hallucination flag → human review · Citation requirement · AI content labeling"),
    ("OBSERVE", b.AMBER,"Mandatory audit log (all invocations) · Model drift monitoring · Cost anomaly detection · SIEM correlation"),
]
lw = (d.CW - Inches(0.36)) / 4
for i, (label, col, body) in enumerate(layers):
    x = d.M + i * (lw + Inches(0.12))
    d.rect(s, x, Inches(4.1), lw, Inches(1.38), b.NAVY, radius=0.05)
    d.rect(s, x, Inches(4.1), lw, Inches(0.06), col)
    d.text(s, label, x + Inches(0.15), Inches(4.22), lw - Inches(0.3), Inches(0.28),
           size=12, color=col, bold=True)
    d.text(s, body, x + Inches(0.15), Inches(4.58), lw - Inches(0.3), Inches(0.82),
           size=10, color=b.WHITE, shrink=True, ls=1.08)

d.text(s, "MANDATORY AUDIT LOG: every invocation logs session_id, user_role, model_id, model_version, input_hash, output_hash, latency_ms, guardrail_action, grounding_score, rai_flags",
       d.M, Inches(5.62), d.CW, Inches(0.44), size=11, color=b.MUTED, shrink=True)
d.footer(s, 18, TOTAL)


# ── SLIDE 19 — 90-DAY PILOT BLUEPRINT ────────────────────────────────────────

s = d.slide(fill=b.WHITE)
d.header(s, "90-Day Pilot Blueprint", "Maximum 3 use cases. Measurable KPI baseline. Named process owner. Hard go/no-go criteria.")

phases = [
    (b.TEAL, "WEEKS 1–4\nFoundation",
     "• Baseline KPI measurement: current cycle time, manual FTE hours, error/NIGO rate\n"
     "• Assign SCOPE tier (1–6) and Model Tier (T1–T4) to each use case\n"
     "• Cloud environment setup: VPC, KMS, IAM roles, audit log schema, cost guardrails\n"
     "• Pre-production checklist sign-off (HIPAA/PCI/IEC 62443 as applicable)"),
    (b.ACCENT, "WEEKS 5–10\nBuild + Pilot",
     "• Build to Tier 2 Solution Blueprint for selected use case\n"
     "• Implement realization pattern (RAG / Document AI / Multi-Agent / KG+MCP)\n"
     "• Wire human-in-loop review queue and fallback path\n"
     "• Run with 1 team or 1 process — not full rollout"),
    (b.GOLD, "WEEKS 11–13\nMeasure + Decide",
     "• Measure against pre-set KPI baseline (not anecdotal wins)\n"
     "• Run RAI evaluation: bias check, fairness metrics, grounding score\n"
     "• Review audit log compliance: all mandatory fields populated?\n"
     "• Go / No-Go: hit criteria → expand. Miss criteria → fix root cause or stop."),
]
pw = (d.CW - Inches(0.24)) / 3
for i, (col, title, body) in enumerate(phases):
    x = d.M + i * (pw + Inches(0.12))
    d.rect(s, x, Inches(1.72), pw, Inches(3.9), b.SOFT, line=b.GRID, radius=0.05)
    d.rect(s, x, Inches(1.72), pw, Inches(0.07), col)
    d.text(s, title, x + Inches(0.18), Inches(1.86), pw - Inches(0.36), Inches(0.56),
           size=14, color=b.INK, bold=True, shrink=True)
    d.text(s, body, x + Inches(0.18), Inches(2.52), pw - Inches(0.36), Inches(2.95),
           size=11, color=b.INK, shrink=True, ls=1.1)

d.rect(s, d.M, Inches(5.78), d.CW, Inches(0.88), b.NAVY, radius=0.05, shadow=True)
d.rect(s, d.M, Inches(5.78), Inches(0.12), Inches(0.88), b.GOLD)
d.text(s, "GO-CRITERIA (set before week 1 — not after)",
       d.M + Inches(0.28), Inches(5.88), Inches(3.5), Inches(0.26),
       size=11, color=b.GOLD, bold=True)
d.text(s, "Extraction recall ≥ 92%  ·  Cycle time reduction ≥ 40%  ·  Zero PII leaked to LLM endpoint (audit log verified)  ·  Human review queue functional  ·  Cost within guardrails",
       d.M + Inches(0.28), Inches(6.15), d.CW - Inches(0.55), Inches(0.44),
       size=12.5, color=b.WHITE, bold=True, shrink=True)
d.footer(s, 19, TOTAL)


# ── SLIDE 20 — CALL TO ACTION ─────────────────────────────────────────────────

s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
d.text(s, "NEXT STEPS", Inches(0.45), Inches(1.1), Inches(9), Inches(0.38),
       size=13, color=b.TEAL, bold=True)
d.text(s, "Start With Your Domain.\nPick One Use Case. Set the KPI.", Inches(0.45),
       Inches(1.6), Inches(10), Inches(1.5), size=40, color=b.WHITE, bold=True,
       font=b.FONT_H, shrink=True)
d.rect(s, Inches(0.45), Inches(3.15), Inches(2), Inches(0.06), b.TEAL)
steps = [
    (b.TEAL,   "01", "Identify your domain",         "Healthcare · FSI · Retail · Manufacturing · Cross-Industry"),
    (b.ACCENT, "02", "Read the platform architecture","Open the Tier 1 doc for your domain × cloud — inherit its controls"),
    (b.GOLD,   "03", "Pick 3 use cases",              "Use Tier 3 Use Case Cards — ROI benchmarks, KPI baseline, process owner"),
    (b.AMBER,  "04", "Select the realization pattern","RAG / Document AI / Multi-Agent / Knowledge Graph + MCP"),
    (b.TEAL,   "05", "Run the 90-day blueprint",      "Foundation → Build → Measure → Go/No-Go with hard criteria"),
]
sw2 = Inches(1.95)
sx_start = Inches(0.45)
for i, (col, num, step, desc) in enumerate(steps):
    x = sx_start + i * (sw2 + Inches(0.15))
    d.rect(s, x, Inches(3.5), sw2, Inches(2.65), b.NAVY_2, radius=0.06)
    d.rect(s, x, Inches(3.5), sw2, Inches(0.07), col)
    d.rect(s, x + Inches(0.18), Inches(3.65), Inches(0.45), Inches(0.38), col, radius=0.08)
    d.text(s, num, x + Inches(0.18), Inches(3.67), Inches(0.45), Inches(0.34),
           size=14, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, step, x + Inches(0.18), Inches(4.14), sw2 - Inches(0.36), Inches(0.46),
           size=13, color=b.WHITE, bold=True, shrink=True)
    d.text(s, desc, x + Inches(0.18), Inches(4.65), sw2 - Inches(0.36), Inches(1.38),
           size=10.5, color=b.LIGHT_TEAL, shrink=True, ls=1.08)

d.text(s, "Knowledge bundle: github.com/shekerkamma/ai-use-cases-bundle  ·  6 platform architectures · 4 realization patterns · 5 verticals",
       Inches(0.45), Inches(6.7), Inches(10), Inches(0.3),
       size=11, color=RGBColor(0x6B, 0x7C, 0x8C))
d.text(s, f"20 / {TOTAL}", d.W - Inches(1.3), Inches(7.06), Inches(0.7), Inches(0.3),
       size=10, color=RGBColor(0x6B, 0x7C, 0x8C), align=PP_ALIGN.RIGHT, bold=True)


# ── SAVE + VALIDATE ───────────────────────────────────────────────────────────

d.save(OUT)
print(f"\nSlides: {d.n}")
