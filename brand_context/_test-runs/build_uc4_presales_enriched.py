#!/usr/bin/env python3
"""
AI Use Cases Across Industries — Enriched Pre-Sales Pitch Deck
Data sources: GBrain impl specs + web research (named companies) + prior pipeline runs
Layout: Canva-Pro realization template via pptxkit
"""

import sys
from pathlib import Path

PPTXKIT_DIR = Path.home() / ".claude" / "skills" / "branded-pptx-deck" / "scripts"
sys.path.insert(0, str(PPTXKIT_DIR))

from pptxkit import Brand, Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt, Emu, hx

d = Deck(footer="{{brand_name}} · AI Use Cases Across Industries | 2026")
b = d.b

TOTAL = 16


def uc_slide(page, industry, uc_id, title,
             challenge, solution, stats,
             how_it_works, stack, systems, users,
             source, insight, governance=None, competitive=None,
             buyer=None, revenue=None):
    """Full use-case realization slide — Canva template with all data fields."""
    s = d.slide(fill=b.WHITE)
    PW = Inches(8.833)
    RW = d.W - PW

    # Teal left panel
    d.rect(s, 0, 0, PW, d.H, b.TEAL)

    # Header
    d.text(s, f"{uc_id} | {industry}", Inches(0.4), Inches(0.12),
           PW - Inches(0.7), Inches(0.22), size=9, color=b.NAVY, bold=True)
    d.text(s, title, Inches(0.4), Inches(0.32), PW - Inches(0.7), Inches(0.42),
           size=19, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.4), Inches(0.72), Inches(2), Inches(0.03), b.NAVY)

    # CHALLENGE + SOLUTION columns
    col_w = Inches(3.85)
    y = Inches(0.82)
    d.text(s, "CHALLENGE", Inches(0.4), y, Inches(1.5), Inches(0.16),
           size=7.5, color=b.NAVY, bold=True)
    d.text(s, [{"text": f"•  {c}", "size": 7, "color": b.NAVY, "space_before": 2} for c in challenge],
           Inches(0.4), y + Inches(0.16), col_w, Inches(1.15))

    sol_x = Inches(4.4)
    d.text(s, "HOW IT'S REALIZED", sol_x, y, Inches(2), Inches(0.16),
           size=7.5, color=b.NAVY, bold=True)
    d.text(s, [{"text": f"•  {sl}", "size": 7, "color": b.NAVY, "space_before": 2} for sl in solution],
           sol_x, y + Inches(0.16), col_w, Inches(1.15))

    # STAT BOXES (gold)
    stat_y = Inches(2.15)
    for i, (num, label) in enumerate(stats[:4]):
        sx = Inches(0.4) + Inches(i * 2.05)
        d.rect(s, sx, stat_y, Inches(1.9), Inches(0.7), b.NAVY, radius=0.02)
        d.text(s, num, sx, stat_y + Pt(3), Inches(1.9), Inches(0.35),
               size=17, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, sx, stat_y + Pt(28), Inches(1.9), Inches(0.28),
               size=6.5, color=b.WHITE, align=PP_ALIGN.CENTER)

    # HOW IT WORKS
    hiw_y = Inches(3.0)
    d.text(s, "HOW IT WORKS", Inches(0.4), hiw_y, Inches(2), Inches(0.15),
           size=7.5, color=b.NAVY, bold=True)
    d.text(s, [{"text": f"→ {h}", "size": 6.5, "color": b.NAVY, "space_before": 2} for h in how_it_works],
           Inches(0.4), hiw_y + Inches(0.15), PW - Inches(0.7), Inches(0.55))

    # GOVERNANCE + COMPETITIVE columns
    gov_y = Inches(3.8)
    if governance:
        d.text(s, "GOVERNANCE & COMPLIANCE", Inches(0.4), gov_y, Inches(3.5), Inches(0.15),
               size=7, color=b.NAVY, bold=True)
        d.text(s, [{"text": f"•  {g}", "size": 6, "color": b.NAVY, "space_before": 1} for g in governance],
               Inches(0.4), gov_y + Inches(0.15), col_w, Inches(0.7))

    if competitive:
        d.text(s, "COMPETITIVE LANDSCAPE", sol_x, gov_y, Inches(3.5), Inches(0.15),
               size=7, color=b.NAVY, bold=True)
        d.text(s, [{"text": f"•  {c}", "size": 6, "color": b.NAVY, "space_before": 1} for c in competitive],
               sol_x, gov_y + Inches(0.15), col_w, Inches(0.7))

    # INSIGHT (brand voice)
    ins_y = Inches(4.7)
    d.text(s, "THE ACTUAL INSIGHT", Inches(0.4), ins_y, Inches(2), Inches(0.15),
           size=7, color=b.NAVY, bold=True)
    d.text(s, insight, Inches(0.4), ins_y + Inches(0.15), PW - Inches(0.7), Inches(0.5),
           size=7.5, color=b.NAVY, italic=True)

    # SOLUTION STACK bar
    stack_y = Inches(5.45)
    d.rect(s, Inches(0.3), stack_y, PW - Inches(0.5), Inches(0.7), b.NAVY)
    d.text(s, "SOLUTION STACK", Inches(0.4), stack_y + Inches(0.03), Inches(2), Inches(0.14),
           size=7, color=b.TEAL, bold=True)
    for i, (layer, detail) in enumerate(stack[:4]):
        col_x = Inches(0.4) + Inches(i * 2.05)
        d.text(s, layer, col_x, stack_y + Inches(0.18), Inches(1.9), Inches(0.14),
               size=6.5, color=b.TEAL, bold=True)
        d.text(s, detail, col_x, stack_y + Inches(0.33), Inches(1.9), Inches(0.32),
               size=6, color=b.WHITE)

    # SYSTEMS + USERS bars
    bar_y = Inches(6.25)
    if systems:
        d.rect(s, Inches(0.3), bar_y, Inches(4), Inches(0.3), b.ACCENT)
        d.text(s, "SYSTEMS: " + "  |  ".join(systems[:5]), Inches(0.4), bar_y + Pt(2),
               Inches(3.8), Inches(0.24), size=6, color=b.WHITE, bold=True)
    if users:
        d.rect(s, Inches(4.5), bar_y, Inches(4), Inches(0.3), b.DARK_TEAL)
        d.text(s, "USERS: " + users, Inches(4.6), bar_y + Pt(2),
               Inches(3.8), Inches(0.24), size=6, color=b.WHITE, bold=True)

    # BUYER + REVENUE + SOURCE
    foot_y = Inches(6.62)
    foot_parts = []
    if buyer:
        foot_parts.append(f"BUYER: {buyer}")
    if revenue:
        foot_parts.append(f"REVENUE: {revenue}")
    foot_parts.append(f"Source: {source}")
    d.text(s, "  |  ".join(foot_parts), Inches(0.4), foot_y, PW - Inches(0.7), Inches(0.2),
           size=5.5, color=b.ACCENT, italic=True)

    # RIGHT strip
    d.rect(s, PW, 0, RW, d.H, b.NAVY_2)
    d.text(s, industry.upper(), PW + Inches(0.2), Inches(0.3),
           RW - Inches(0.4), Inches(2), size=16, color=b.TEAL, bold=True)
    # Vertical score badge if available
    if revenue:
        d.rect(s, PW + Inches(0.2), Inches(2.5), RW - Inches(0.4), Inches(0.35), b.TEAL, radius=0.03)
        d.text(s, revenue, PW + Inches(0.2), Inches(2.55),
               RW - Inches(0.4), Inches(0.25), size=9, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)

    d.footer(s, page, TOTAL)


# ═══════════════════════════════════════════════════
# COVER
# ═══════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
d.rect(s, d.W - Inches(0.12), 0, Inches(0.12), d.H, b.NAVY_2)
d.rect(s, d.W - Inches(0.18), 0, Inches(0.06), d.H, b.TEAL)

d.text(s, "PRE-SALES INTELLIGENCE", d.M, Inches(0.8), Inches(7), Inches(0.35),
       size=14, color=b.TEAL, bold=True)
d.text(s, "AI Use Cases That Actually Ship",
       d.M, Inches(1.3), Inches(9), Inches(1.0),
       size=44, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(2.4), Inches(1.5), Inches(0.05), b.TEAL)
d.text(s, "Named Companies · Verified Numbers · Agent Architectures · MCP Stacks · Revenue Models",
       d.M, Inches(2.7), Inches(9), Inches(0.4), size=16, color=b.MUTED)

chips = [("8", "Industries"), ("15", "Use Cases"), ("6 Pipelines", "GBrain-Backed"),
         ("$2-10K/mo", "Revenue Per Client")]
for i, (num, label) in enumerate(chips):
    cx = d.M + Inches(i * 2.4)
    d.rect(s, cx, Inches(3.6), Inches(2.1), Inches(1.0), b.NAVY_2, radius=0.03, shadow=True)
    d.text(s, num, cx, Inches(3.65), Inches(2.1), Inches(0.5),
           size=28, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, label, cx, Inches(4.15), Inches(2.1), Inches(0.35),
           size=11, color=b.MUTED, align=PP_ALIGN.CENTER)

d.text(s, [
    {"text": "Data enrichment pipeline:", "size": 12, "color": b.LIGHT_TEAL, "bold": True},
    {"text": "GBrain recall → Exa web research → Implementation specs → Vertical scorer → pptxkit render", "size": 11, "color": b.MUTED, "space_before": 4},
    {"text": "Every use case includes: agent architecture, MCP server configs, automation flows, governance,", "size": 11, "color": b.MUTED, "space_before": 2},
    {"text": "competitive landscape, buyer profile, revenue model, and brand-voice insight.", "size": 11, "color": b.MUTED, "space_before": 2},
], d.M, Inches(5.2), Inches(9), Inches(1.5))

d.text(s, "{{brand_name}}", d.M, Inches(6.8), Inches(3), Inches(0.4),
       size=13, color=b.MUTED, bold=True)
d.footer(s, 1, TOTAL, dark=True)


# ═══════════════════════════════════════════════════
# EXEC SUMMARY
# ═══════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Portfolio: 8 Industries, 15 Use Cases, One Delivery Pattern",
         "Every use case follows the same architecture: OpenHands SDK + MCP servers + domain skills + system-of-record integration")

# Industry cards
industries = [
    ("Manufacturing", "32/35 GO", "UC01-UC08: Visual QI, Variant, Torque, SOP, PdQ, PdM, Safety, Trace", "$5-10K/mo"),
    ("Healthcare", "Viable", "Patient intake + insurance verification + scheduling", "$3-5K/mo"),
    ("Legal", "30/35 GO", "Contract generation + review (67-agent debate) + legal research", "$3-5K/mo"),
    ("Real Estate", "5 lanes", "Brokerage, leasing, commission, maintenance, title/closing", "$2-4K/mo"),
    ("Financial Svcs", "Production", "TD Bank (15hr→min), JPMorgan COIN (360K hrs saved)", "Enterprise"),
    ("Retail", "Production", "Macy's (4.75x rev/visit), Galeries Lafayette (+7% rev)", "Enterprise"),
    ("Logistics", "Production", "C.H. Robinson (100T data, 30+ agents, stock 2x)", "Enterprise"),
    ("Energy", "Production", "Con Edison ($854M benefit), ENGIE (1000+ models)", "Enterprise"),
]

for i, (name, score, desc, rev) in enumerate(industries):
    row = i // 4
    col = i % 4
    cx = d.M + Inches(col * 3.0)
    cy = Inches(1.8) + Inches(row * 2.4)
    cw = Inches(2.8)

    d.rect(s, cx, cy, cw, Inches(2.1), b.SOFT, radius=0.02, shadow=True)
    # Navy chip with industry name
    d.rect(s, cx + Pt(8), cy + Pt(8), Inches(2.4), Pt(22), b.NAVY, radius=0.02)
    d.text(s, name, cx + Pt(8), cy + Pt(9), Inches(2.4), Pt(20),
           size=9, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
    # Score badge
    badge_color = b.TEAL if "GO" in score or "Production" in score else b.AMBER
    d.text(s, score, cx + Pt(8), cy + Pt(34), Inches(1.2), Pt(16),
           size=8, color=badge_color, bold=True)
    d.text(s, rev, cx + Inches(1.4), cy + Pt(34), Inches(1.2), Pt(16),
           size=8, color=b.GOLD, bold=True, align=PP_ALIGN.RIGHT)
    # Description
    d.text(s, desc, cx + Pt(8), cy + Pt(54), cw - Pt(16), Inches(1.1),
           size=7, color=b.INK)

d.footer(s, 2, TOTAL)


# ═══════════════════════════════════════════════════
# USE CASE SLIDES
# ═══════════════════════════════════════════════════

# UC01: Manufacturing — Predictive Maintenance (GBrain + Unilever)
uc_slide(3, "Manufacturing", "UC-01",
    "Predictive Maintenance — Sensor → Anomaly → Work Order",
    challenge=[
        "Equipment downtime costs $50K-$250K/hour in manufacturing plants",
        "Calendar-based maintenance wastes 30%+ of budget on unnecessary interventions",
        "Unilever: 8.2% unplanned downtime, $5.1M annual maintenance baseline",
        "Technician trust in AI predictions is the real deployment barrier",
    ],
    solution=[
        "50K+ IoT sensors → anomaly detection 14-28 days before failure at 92% accuracy",
        "52-endpoint MCP server: FFT, envelope analysis, RUL estimation (ISO 13374)",
        "Auto-generates SAP PM work orders with equipment ID, failure type, predicted date",
        "6-month trust-building phase with technician feedback loops",
    ],
    stats=[("$2.3M", "Savings/yr (Unilever)"), ("92%", "Detection Accuracy"),
           ("52", "MCP Endpoints"), ("6.5 mo", "Payback Period")],
    how_it_works=[
        "Sensor → load_signal + analyze_spectrum + extract_features (MCP) → detect_anomalies",
        "Severity ≥ Zone C OR RUL <14 days → generate_report → create_work_order (SAP PM via OData)",
        "ISO 20816-3 vibration classification: Zone A/B/C/D → automated escalation",
    ],
    stack=[("MCP: PdM", "predictive-maintenance-mcp\n52 endpoints, ISO 13374"),
           ("MCP: SAP PM", "mcp-maintenance-cap\nOData: create_work_order"),
           ("ML", "XGBoost + LSTM\nSHAP explainability"),
           ("Deploy", "OpenHands headless\nEdge: ONNX Runtime")],
    systems=["SCADA/OPC-UA", "SAP PM", "IoT Gateway", "CMMS"],
    users="Maintenance technicians | Plant engineers | Reliability mgrs",
    source="NSSG Insights Mar 2026 + GBrain impl spec",
    insight="3 years of labeled failure data eliminated the data-collection phase. Started with 12 machines causing 80% of downtime. The model was ready before the humans were. Trust took 6 months.",
    governance=["ISO 13374 six-block diagnostic architecture", "ISO 20816-3 vibration severity", "Sensor calibration audit per ISO 6789"],
    competitive=["Sight Machine / Uptake: $100K+/yr SaaS", "McKinsey QuantumBlack: $400K+, 6+ months", "Our edge: 4 weeks, 50-70% cheaper, open-source"],
    buyer="VP Manufacturing / Plant Manager",
    revenue="$5-10K/mo per plant",
)

# UC02: Manufacturing — Visual Quality Inspection (GBrain)
uc_slide(4, "Manufacturing", "UC-02",
    "Visual Quality Inspection — Camera → CNN → SAP MES",
    challenge=[
        "15-20% false positive rate in manual inspection across production lines",
        "Inspector fatigue: accuracy drops to 72% by hour 6 of shift",
        "$2.3M average annual quality cost per plant from missed defects",
        "Inconsistent criteria across shifts — 3 inspectors, 3 standards",
    ],
    solution=[
        "YOLOv8 real-time defect detection: 640×640 input, 1.2ms edge inference",
        "Multi-camera 360° inspection at line speed (120 units/hr)",
        "Confidence >0.85 auto-reject; 0.5-0.85 → operator review; <0.5 passes",
        "Active learning: operator corrections feed continuous retraining",
    ],
    stats=[("99.2%", "Detection Accuracy"), ("85%", "FP Reduction"),
           ("$1.8M", "Annual Savings"), ("4-6 wk", "Deployment")],
    how_it_works=[
        "GigE Vision camera → Edge GPU (Jetson Orin) → YOLOv8 inference <2ms → classify: scratch/dent/weld/paint",
        "Auto-reject logged to SAP MES with defect image + coordinates + shift context → root-cause analysis",
        "Per-shift quality report auto-generated → SPC dashboard with Cpk monitoring",
    ],
    stack=[("EDGE", "GigE Vision cameras\nJetson Orin NX"),
           ("AI", "YOLOv8 + EfficientNet\nONNX Runtime"),
           ("MCP: SAP MES", "log_inspection_result\ncreate_quality_notification"),
           ("UX", "Defect heatmap\nShift dashboard")],
    systems=["SAP MES", "GigE Vision", "Jetson Orin", "MinIO"],
    users="Quality engineers | Line supervisors | Plant managers",
    source="GBrain impl spec UC-MFG-02 + Hyundai framework",
    insight="Human inspectors get tired. The camera doesn't. But they kept humans for the 0.3% the camera wasn't sure about. Best of both.",
    governance=["IEC 62443 industrial cybersecurity", "Image retention: 7 years (AES-256)", "Edge cert rotation every 90 days"],
    competitive=["Instrumental (YC W14, 80 emp)", "Landing AI (Andrew Ng)", "Ocular AI (YC W24)"],
    buyer="VP Quality / Quality Manager",
    revenue="$5-10K/mo per plant",
)

# UC03: Healthcare — Patient Intake (GBrain)
uc_slide(5, "Healthcare", "UC-03",
    "Patient Intake Automation — Form → EHR → Insurance → Booking",
    challenge=[
        "Manual intake: 12-15 min per patient, 40% of staff time consumed by paperwork",
        "Insurance verification: 270/271 EDI calls take 3-8 min per patient manually",
        "No-show rate 18-25% due to lack of automated reminders",
        "HIPAA compliance burden: every PHI access must be logged and audited",
    ],
    solution=[
        "3-agent pipeline: intake-agent → insurance-verification-agent → scheduling-agent",
        "FHIR R4 MCP server: create_patient, get_insurance_eligibility, submit_claim",
        "Automated SMS reminders via Twilio MCP: confirmation, cost estimate, 24h reminder",
        "OpenHands Docker sandbox isolates PHI — never leaves infrastructure",
    ],
    stats=[("80%", "Staff Time Saved"), ("<30 sec", "Insurance Check"),
           ("40%", "No-Show Reduction"), ("HIPAA", "Compliant by Design")],
    how_it_works=[
        "Online form → validate fields → create_patient (FHIR R4) → get_insurance_eligibility (270/271 EDI)",
        "IF eligible → calculate copay → send_sms (confirmation + cost estimate) → create_booking",
        "24h before → send_reminder → post-visit: update_patient + submit_claim (837 EDI)",
    ],
    stack=[("MCP: FHIR", "HL7 FHIR R4 APIs\ncreate/search/update patient"),
           ("MCP: Twilio", "send_sms, send_reminder\nget_message_status"),
           ("MCP: Calendly", "get_available_slots\ncreate/cancel_booking"),
           ("Security", "AES-256 at rest\nTLS 1.3 in transit")],
    systems=["EHR", "Insurance EDI", "Twilio", "Calendly"],
    users="Front desk staff | Practice managers | Billing coordinators",
    source="GBrain impl spec + AI Engineering Framework §2.1",
    insight="Prior auth is bureaucratic, not clinical. Most requests meet criteria — someone just needs to check the boxes. The AI checks the boxes. Edge cases still go to a nurse.",
    governance=["HIPAA: AES-256 at rest, TLS 1.3 in transit", "BAA required with all third-party services", "Minimum necessary principle for PHI access"],
    competitive=["Phreesia ($250M rev) — patient intake platform", "Zocdoc — scheduling but no intake automation", "Gap: no integrated intake+verify+schedule agent"],
    buyer="Practice Manager / VP Operations",
    revenue="$3-5K/mo per practice",
)

# UC04: Legal — Contract Generation & Review (GBrain)
uc_slide(6, "Legal", "UC-04",
    "Contract Generation & Review — 67-Agent Debate Protocol",
    challenge=[
        "Paralegal review: 40 hours per contract across 90+ clause types",
        "Outside counsel spend growing 15% annually — need to shift work internal",
        "Mid-market firms (<50 attorneys) priced out of Harvey ($100K+/yr)",
        "Clause extraction breaks when documents exceed LLM context windows",
    ],
    solution=[
        "3 agents: contract-generation + contract-review (67-agent debate) + legal-research",
        "open-agreements MCP: 40+ templates (NDA, MSA, SaaS, SAFE, NVCA)",
        "lavern MCP: 3-layer verification — evaluator gate → adversarial debate → 10-pass",
        "suzielaw MCP: 22 legal providers across 19 jurisdictions",
    ],
    stats=[("70%", "Review Time ↓"), ("$2.4M", "Billable Hrs Recaptured"),
           ("99.1%", "Clause Accuracy"), ("22 wk", "Build (10 wk to prod)")],
    how_it_works=[
        "Request → identify agreement type → list_templates → get_template_fields → interview → fill_template (DOCX)",
        "Review: Phase 1 (read-only planning) → Phase 2 (risk matrix + redlines + missing clause recommendations)",
        "Alternative: Lavern full adversarial (67 agents, debate protocol, citation-grounded) → executive summary memo",
    ],
    stack=[("MCP: Templates", "open-agreements v0.7.5\n40+ templates as MCP"),
           ("MCP: Review", "lavern v0.15.0\n67 agents, 21 MCP tools"),
           ("MCP: Research", "suzielaw\n22 providers, 19 jurisdictions"),
           ("LLM", "Claude 3.5 Sonnet\n200K context, single-pass")],
    systems=["iManage", "DocuSign", "CLM", "Aderant"],
    users="Paralegals | Associates | M&A partners",
    source="DreamzTech Apr 2026 + GBrain impl spec",
    insight="Lawyers spent 28 hours finding clauses and 12 on judgment. Now they spend 12 on judgment. Everyone does what they're actually good at.",
    governance=["Client-attorney privilege preserved", "Confidence gating: <0.85 → human review (A2I)", "45K-contract training on firm's own archive"],
    competitive=["Harvey: $100K+/yr, enterprise only", "Anthropic claude-for-legal: practice-area plugins", "Our edge: mid-market, open-source MCP, 50-70% cheaper"],
    buyer="Legal Ops / Managing Partner",
    revenue="$3-5K/mo per firm",
)

# UC05: Real Estate — Brokerage Automation (GBrain)
uc_slide(7, "Real Estate", "UC-05",
    "Brokerage Automation — Lead Scoring → Transaction → CMA",
    challenge=[
        "Manual lead follow-up: avg 47-hour response time loses 78% of leads",
        "Transaction coordination across CRM, docs, title, lender, compliance — all manual",
        "CMA creation takes 2-3 hours per property, done by high-cost agents",
        "Fragmented systems: CRM, DocuSign, title, lender portal — no unified workflow",
    ],
    solution=[
        "3 agents: CRM-specialist → Lease-document → Marketing (ADK + MCP orchestration)",
        "AI lead scoring prioritizes high-conversion customers in real-time",
        "Automated CMA generation from Zillow/MLS data → client-ready in minutes",
        "Generative UI renders dashboards dynamically via AG-UI protocol",
    ],
    stats=[("4x", "Faster Lead Response"), ("80%", "Doc Automation"),
           ("2hr→5min", "CMA Generation"), ("15%", "Higher Conversion")],
    how_it_works=[
        "Lead captured → AI scoring (ML model on historical conversion data) → Priority routing to agent",
        "Transaction: checklist auto-generated → milestone tracking → DocuSign integration → closing coordination",
        "CMA: Zillow API pull → comp analysis → auto-formatted report → client delivery",
    ],
    stack=[("MCP: Zillow", "Property data API\nComp analysis"),
           ("MCP: DocuSign", "Envelope creation\nE-signature flow"),
           ("MCP: Stripe", "Commission payments\nPayout automation"),
           ("UI", "AG-UI dashboards\nCopilotKit frontend")],
    systems=["CRM", "MLS/Zillow", "DocuSign", "QuickBooks"],
    users="Brokers | Agents | Transaction coordinators",
    source="GBrain real-estate-domain-use-cases + pipeline run",
    insight="The commercial wedge is speed-to-lead. Then expand into transaction coordination after workflow trust is established. Same pattern as manufacturing: prove one thing, then expand.",
    governance=["Fair Housing Act compliance on lead scoring", "RESPA compliance on referral workflows", "State-specific disclosure requirements automated"],
    competitive=["Rechat — brokerage CRM ($2M Series A)", "Lofty / kvCORE — CRM + marketing", "Gap: no integrated agent orchestration layer"],
    buyer="Broker/Owner / VP Operations",
    revenue="$2-4K/mo per brokerage",
)

# UC06: Financial Services — TD Bank (Web Research)
uc_slide(8, "Financial Services", "UC-06",
    "TD Bank — Mortgage Processing Agent (15hrs → Minutes)",
    challenge=[
        "Mortgage applications require 15+ hours of manual document review",
        "Cross-referencing borrower docs is error-prone at scale (100K+ apps/year)",
        "LLMs hallucinate on arithmetic (annualizing income from pay stubs)",
        "Risk/compliance review traditionally added 3-5 days to cycle",
    ],
    solution=[
        "Agentic AI reads entire borrower document packages, extracts structured data",
        "Deterministic rules-based tools handle all arithmetic — never the LLM",
        "Cross-references fields across documents, flags inconsistencies automatically",
        "Risk/compliance team built into the project from day 1 (not bolted on)",
    ],
    stats=[("15hr→min", "Processing Time"), ("$826M", "2025 Origination"),
           ("Jan 2026", "Production Deploy"), ("Day 1", "Compliance Built In")],
    how_it_works=[
        "Doc package ingestion → OCR/NLP extraction → Field cross-reference → Inconsistency flagging",
        "Income calc routed to deterministic tools (not LLM math) → Credit summary auto-generated",
        "Human adjudicator reviews summary → Approves/rejects with full audit trail",
    ],
    stack=[("Foundation", "Layer 6 + Claude + GPT\n(selective per task)"),
           ("Arithmetic", "Deterministic rules\nNever LLM math"),
           ("Governance", "TD Trustworthy AI\nContinuous monitoring"),
           ("Integration", "Core banking APIs\nCredit bureau feeds")],
    systems=["Core Banking", "Doc Mgmt", "Credit Bureau", "Compliance"],
    users="Mortgage underwriters | Credit adjudicators",
    source="American Banker, May 2026",
    insight="They didn't let the LLM do math. Deterministic tools for arithmetic, LLM for document reading. One use case done right before expanding. Dead simple discipline.",
    governance=["TD Trustworthy AI governance framework", "Continuous post-launch monitoring", "Human signs off on every credit decision"],
    competitive=["JPMorgan COIN: 360K attorney-hours eliminated (9 yrs)", "Blend: mortgage automation SaaS", "Our differentiation: agentic, not rules-only"],
    buyer="VP Mortgage Operations / CTO",
    revenue="Enterprise (internal deployment)",
)

# UC07: Retail — Galeries Lafayette (Web Research)
uc_slide(9, "Retail", "UC-07",
    "Galeries Lafayette — AI Search & Personalization (+7% Revenue)",
    challenge=[
        "Legacy search failing at 600K product catalog scale",
        "350K products from third-party marketplace — heterogeneous data quality",
        "One-size-fits-all ranking ignores individual visitor behavior",
        "Merchandising teams need category-level control — can't hand everything to AI",
    ],
    solution=[
        "Google Vertex AI Search for Commerce replaces legacy search entirely",
        "Real-time personalized ranking per visitor via behavioral + session signals",
        "Grid Dynamics MXP gives merchandisers override controls per category",
        "Hybrid: AI handles individual ranking, humans control brand positioning",
    ],
    stats=[("+7%", "Total Revenue"), ("+8%", "Basket Value"),
           ("+20%", "Online Sales YoY"), ("600K", "Products Ranked")],
    how_it_works=[
        "Visitor arrives → Behavioral signals scored → Personalized ranking generated per session",
        "Merchandising Studio applies category rules → AI respects brand positioning constraints",
        "Real-time inventory/pricing feeds ensure availability accuracy across 600K SKUs",
    ],
    stack=[("Search", "Vertex AI Search\nfor Commerce"),
           ("Merch Control", "Grid Dynamics MXP\nCategory overrides"),
           ("Data", "Real-time inventory\n+ pricing feeds"),
           ("Personalization", "Session + behavioral\nsignal scoring")],
    systems=["E-commerce", "PIM", "Marketplace Feed", "WMS"],
    users="Online shoppers | Merchandising team | Category managers",
    source="Business Wire, April 2026",
    insight="Purely autonomous AI would have been blocked by merchandising teams. Give humans the override, they'll trust the system. Hybrid drove adoption. That's the lesson.",
    buyer="CDO / VP E-commerce",
    revenue="Enterprise",
)

# UC08: Logistics — C.H. Robinson (Web Research)
uc_slide(10, "Logistics", "UC-08",
    "C.H. Robinson — 30+ AI Agents on 100T Data Points",
    challenge=[
        "37M shipments/year — manual processing physically impossible at scale",
        "Price quoting: 17-20 min per quote, only covering 65% of requests",
        "Order processing: 4 hours from email to system entry",
        "Freight tracking requires human phone calls — one agent handles 318K/month",
    ],
    solution=[
        "30+ AI agents via LangChain/LangGraph on 100T proprietary data points",
        "Email-to-order: LLM extracts fields, validates, enters — 5,500 orders/day automated",
        "Quote agent scores pricing against proprietary demand model → 32 seconds",
        "Phone agent calls carriers for tracking → 318K updates/month autonomously",
    ],
    stats=[("32 sec", "Quote (was 17 min)"), ("100%", "Quote Coverage"),
           ("<2 min", "Order (was 4 hr)"), ("+40%", "Productivity")],
    how_it_works=[
        "Email → LangGraph agent extracts order fields → Validates against 100T data → System entry",
        "Quote request → Demand model scores → Pricing response in 32 seconds → 100% coverage",
        "Tracking → Phone AI calls carriers → Captures updates → Status updated in TMS",
    ],
    stack=[("Orchestration", "LangChain + LangGraph\n30+ agents"),
           ("Observability", "LangSmith\nAccuracy + drift monitoring"),
           ("Data", "100T proprietary\n37M shipments/yr"),
           ("Culture", "Builder-first\nNo SaaS dependency")],
    systems=["TMS", "CRM", "Carrier APIs", "Email", "Phone"],
    users="Freight brokers | Logistics coordinators | Carrier ops",
    source="C.H. Robinson PR + The Applied, 2026",
    insight="Proprietary data moat — competitors can't replicate 37M shipments/year of training data. Stock price doubled during industry downturn. Lean AI mapped to waste concepts before building.",
    buyer="VP Logistics / COO",
    revenue="Enterprise (internal deployment)",
)

# UC09: Energy — Con Edison (Web Research)
uc_slide(11, "Energy & Utilities", "UC-09",
    "Con Edison + C3 AI — 5.3M Smart Meters, $854M Benefit",
    challenge=[
        "5.3M meters generating 1 petabyte/year across 13 siloed data sources",
        "Configuration errors and installation failures go undetected for months",
        "Small anomalies multiply into massive outage/billing costs at utility scale",
        "No unified view — each of 13 systems operates independently",
    ],
    solution=[
        "C3 AI Platform consolidates 13 sources → unified data image (2yr historical load)",
        "2 ML algorithms + 50 custom analytics on 180B rows of annual meter data",
        "Real-time anomaly detection: individual meter → system-wide view",
        "Automated work order generation with meter-specific diagnostic context",
    ],
    stats=[("2,300", "Issues (4 months)"), ("$854M", "Annual Benefit"),
           ("5.3M", "Meters Monitored"), ("13→1", "Data Unified")],
    how_it_works=[
        "13 source systems → C3 AI unification layer → Single data image (2yr load)",
        "180B rows/year → 2 ML models + 50 analytics → Anomaly score per meter",
        "Flagged → Work order (meter-specific context) → Field crew dispatch",
    ],
    stack=[("Platform", "C3 AI Platform\nUnified data image"),
           ("Application", "C3 AI AMI Operations\nMeter-level analytics"),
           ("Data", "180B rows/yr\n13 sources unified"),
           ("ML", "2 models + 50 analytics\nAnomaly detection")],
    systems=["AMI/MDM", "GIS", "OMS", "Billing", "SCADA"],
    users="Grid ops | Field crews | Customer service | Planning",
    source="The Applied, May 2026",
    insight="The 13-to-1 data consolidation was the hard part. Analytics ran on top of clean, unified data. Find config errors early — the math is enormous at 5.3M meter scale.",
    governance=["NERC CIP compliance for grid systems", "Customer data privacy (state PUC rules)", "Meter data retention per regulatory requirements"],
    competitive=["ENGIE: 1000+ PdM models (SageMaker), €800K/yr savings", "Itron / Landis+Gyr: hardware-first, weak analytics", "C3 AI: pre-built utility domain model"],
    buyer="VP Grid Operations / CTO",
    revenue="Enterprise ($854M benefit at scale)",
)

# UC10: Construction — DroneDeploy (Web Research)
uc_slide(12, "Construction", "UC-10",
    "DroneDeploy — 34M Annotations, 4 AI Agents, 3M+ Sites",
    challenge=[
        "Manual site walks miss events, rely on superintendent memory",
        "Safety violations go undetected — poor documentation industry-wide",
        "Progress reporting: 2 days of manual compilation per project",
        "Generic CV doesn't understand what 'installed' means per trade",
    ],
    solution=[
        "4 AI agents: Progress, Safety, Inspection, Embodied — trained on 34M annotations",
        "Autonomous ground robots + docked drones capture sites overnight",
        "Morning reports: overnight progress by trade before team arrives",
        "Safety AI: 120K labeled examples, flags conditions in real-time",
    ],
    stats=[("34M", "Training Annotations"), ("+340%", "Safety Catches"),
           ("48%", "Injury Reduction"), ("3M+", "Sites in Prod")],
    how_it_works=[
        "Overnight: robots + drones capture from fixed vantage points autonomously",
        "Morning: Progress AI → structured report (installed work, trade progress, deviations)",
        "Continuous: Safety AI flags PPE/guardrail violations → real-time notifications",
    ],
    stack=[("Vision", "34M annotation corpus\n770M images (2025)"),
           ("Capture", "Ground robots (Rocos)\nDocked drones"),
           ("Agents", "Progress, Safety\nInspection, Embodied"),
           ("Integration", "Procore, PlanGrid\nBIM overlay")],
    systems=["BIM", "Procore", "PlanGrid", "GIS", "ERP"],
    users="Superintendents | PMs | Safety officers",
    source="DroneDeploy Blog Apr 2026 + BCG 2026",
    insight="13-year annotation corpus — 34M labeled examples across 180 countries — is the moat. The superintendent now acts on data instead of generating it.",
    governance=["Drone flight compliance (FAA Part 107)", "Site access and privacy requirements", "Image retention per project contract terms"],
    competitive=["Buildots — indoor CV for progress tracking", "OpenSpace — 360° walk-through capture", "DroneDeploy edge: autonomous + 34M annotation moat"],
    buyer="VP Construction / Project Director",
    revenue="Enterprise (break-even Sep 2025)",
)

# UC11: Generative UI — Cross-Industry (GBrain)
uc_slide(13, "Cross-Industry", "UC-11",
    "Generative UI — Agent-Rendered Frontends for Enterprise",
    challenge=[
        "Static Fiori/portal screens can't adapt to user context or intent",
        "Building custom dashboards per use case takes 2-4 weeks each",
        "Module boundaries (HR, Finance, Procurement) fragment user experience",
        "Every new AI agent needs a new frontend — doesn't scale",
    ],
    solution=[
        "Declarative pattern: agent emits structured JSON, frontend maps to Fiori controls",
        "AG-UI protocol: bidirectional runtime between any agentic backend and UI",
        "Batch-size-1 applications: temporary, purpose-built dashboards per query",
        "Data grounded through SAP Business Data Cloud — click-through to source",
    ],
    stats=[("31/35", "Vertical Score: GO"), ("437K+", "SAP Installed Base"),
           ("$27M", "CopilotKit Series A"), ("4 adopted", "Google/MS/Amazon/Oracle")],
    how_it_works=[
        "User states intent → ADK agent processes → Emits structured JSON payload (AG-UI protocol)",
        "Frontend maps JSON to native Fiori controls → Dynamic dashboard rendered in real-time",
        "Data lineage: user clicks AI chart → sees system-of-record source → trust by transparency",
    ],
    stack=[("Backend", "Gemini + ADK\nAgent orchestration"),
           ("Protocol", "AG-UI (CopilotKit)\nBidirectional runtime"),
           ("Frontend", "React + Fiori\nComponent mapping"),
           ("Data", "SAP Business Data Cloud\nGrounded, no hallucination")],
    systems=["SAP S/4HANA", "Fiori", "Business Data Cloud", "ADK"],
    users="Business users | Operations | Management",
    source="GBrain: generative-ui-enterprise + SAP News Mar 2026",
    insight="Three patterns: Controlled (pixel-perfect, expensive), Declarative (recommended — flat token cost), Open-ended (demo-only). Enterprise needs Declarative. Everything else is theater.",
    governance=["Data grounding prevents hallucination", "Transparent lineage to system of record", "Role-based access inherited from SAP auth"],
    competitive=["SAP Joule: native but limited scope", "ServiceNow Now Assist: workflow-only", "Our edge: open protocol, any backend, any frontend"],
    buyer="VP IT / Digital Transformation Lead",
    revenue="$5-10K/mo per enterprise",
)


# ═══════════════════════════════════════════════════
# SUMMARY: WHAT WINNERS HAVE IN COMMON
# ═══════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)

d.text(s, "WHAT THE WINNERS HAVE IN COMMON", d.M, Inches(0.42),
       d.CW, Inches(0.55), size=26, color=b.WHITE, bold=True)
d.rect(s, d.M, Inches(1.0), Inches(1.5), Inches(0.05), b.TEAL)

rules = [
    ("01", "Define the number before writing code",
     "TD Bank: processing hours. C.H. Robinson: quote time. Unilever: downtime %. Not 'improve efficiency.' A metric with a baseline."),
    ("02", "Automate the boring part, not the judgment",
     "Every case keeps humans on decisions. AI handles extraction, matching, triage. Lawyers still decide. Underwriters still sign."),
    ("03", "Proprietary data is the moat, not the model",
     "C.H. Robinson 100T points. DroneDeploy 34M annotations. The law firm's 45K contracts. Same models, different data, wildly different outcomes."),
    ("04", "Composite AI beats pure LLM",
     "EU 3PL: composite hit 92% vs 78% pure agentic. TD Bank: deterministic math tools. Use the right tool for each sub-task."),
    ("05", "One architecture, many industries",
     "OpenHands SDK + MCP servers + domain skills + system-of-record integration. Same pattern: manufacturing, legal, healthcare, real estate."),
]

for i, (num, title, desc) in enumerate(rules):
    ry = Inches(1.25) + Inches(i * 1.15)
    d.rect(s, d.M, ry, d.CW, Inches(1.0), b.NAVY_2, radius=0.02)
    d.text(s, num, d.M + Pt(12), ry + Pt(10), Pt(40), Pt(28),
           size=20, color=b.GOLD, bold=True)
    d.text(s, title, d.M + Inches(0.6), ry + Pt(8), d.CW - Inches(1), Inches(0.28),
           size=15, color=b.WHITE, bold=True)
    d.text(s, desc, d.M + Inches(0.6), ry + Pt(30), d.CW - Inches(1), Inches(0.52),
           size=10, color=b.MUTED)

d.footer(s, TOTAL - 1, TOTAL, dark=True)


# ═══════════════════════════════════════════════════
# CLOSER
# ═══════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
d.rect(s, d.W - Inches(0.12), 0, Inches(0.12), d.H, b.NAVY_2)
d.rect(s, d.W - Inches(0.18), 0, Inches(0.06), d.H, b.TEAL)

d.text(s, "The best AI project is the one that actually ships.",
       d.M, Inches(2.0), Inches(10), Inches(1.8),
       size=42, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(4.0), Inches(1.5), Inches(0.05), b.TEAL)
d.text(s, "Not the one with the cleanest architecture, the most sophisticated model,\nor the biggest budget. The one that ships. With a number attached.",
       d.M, Inches(4.3), Inches(9), Inches(0.8), size=16, color=b.MUTED)

d.text(s, "{{brand_name}}", d.M, Inches(5.6), Inches(3), Inches(0.5),
       size=20, color=b.TEAL, bold=True)
d.text(s, "{{tagline}}", d.M, Inches(6.1), Inches(5), Inches(0.4),
       size=14, color=b.MUTED)
d.footer(s, TOTAL, TOTAL, dark=True)


# Save
OUT = Path(__file__).resolve().parent / "uc4-ai-use-cases-presales-enriched.pptx"
d.save(str(OUT))
print(f"Size: {OUT.stat().st_size / 1024:.0f} KB")
