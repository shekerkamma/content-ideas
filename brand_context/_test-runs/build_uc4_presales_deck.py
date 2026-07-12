#!/usr/bin/env python3
"""
AI Use Cases Across Industries — Pre-Sales Pitch Deck
Canva-Pro template style: teal panel + use-case realization layout
Built with pptxkit for validated output
"""

import sys
from pathlib import Path

# Add pptxkit to path
PPTXKIT_DIR = Path.home() / ".claude" / "skills" / "branded-pptx-deck" / "scripts"
sys.path.insert(0, str(PPTXKIT_DIR))

from pptxkit import Brand, Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt, Emu, hx

STOCK_DIR = Path(__file__).resolve().parent.parent / "visual-identity" / "stock-library" / "themes"

d = Deck(footer="{{brand_name}} · AI Use Cases Across Industries | 2026")
b = d.b

TOTAL = 14  # cover + 8 industry UC slides + summary + 3 extra + closer


def pick_stock(theme, idx=0):
    theme_dir = STOCK_DIR / theme
    if theme_dir.exists():
        jpgs = sorted(theme_dir.glob("*.jpg"))
        if jpgs:
            return str(jpgs[idx % len(jpgs)])
    return None


def build_cover():
    s = d.slide(fill=b.NAVY)
    # teal top band
    d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
    # right strip
    d.rect(s, d.W - Inches(0.12), 0, Inches(0.12), d.H, b.NAVY_2)
    d.rect(s, d.W - Inches(0.18), 0, Inches(0.06), d.H, b.TEAL)

    # kicker
    d.text(s, "PRE-SALES INTELLIGENCE", d.M, Inches(1.0), Inches(7), Inches(0.4),
           size=15, color=b.TEAL, bold=True)
    # title
    d.text(s, "AI Use Cases That Actually Ship",
           d.M, Inches(1.5), Inches(9), Inches(1.2),
           size=46, color=b.WHITE, bold=True, shrink=True)
    # rule
    d.rect(s, d.M, Inches(2.8), Inches(1.5), Inches(0.05), b.TEAL)
    # subtitle
    d.text(s, "18 Production Deployments · 8 Industries · Named Companies · Verified Numbers",
           d.M, Inches(3.1), Inches(9), Inches(0.5),
           size=18, color=b.MUTED)

    # stat chips
    chips = [
        ("8", "Industries"),
        ("18", "Use Cases"),
        ("73%", "Avg Efficiency Gain"),
        ("6 wk", "Median ROI Proof"),
    ]
    for i, (num, label) in enumerate(chips):
        cx = d.M + Inches(i * 2.4)
        cy = Inches(4.2)
        d.rect(s, cx, cy, Inches(2.1), Inches(1.1), b.NAVY_2, radius=0.03, shadow=True)
        d.text(s, num, cx, cy + Pt(8), Inches(2.1), Inches(0.6),
               size=32, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, cx, cy + Pt(52), Inches(2.1), Inches(0.4),
               size=12, color=b.MUTED, align=PP_ALIGN.CENTER)

    # voice line
    d.text(s, "Real numbers. Real stacks. No \"transformational AI\" nonsense.",
           d.M, Inches(5.8), Inches(9), Inches(0.4),
           size=14, color=b.LIGHT_TEAL, italic=True)

    d.text(s, "{{brand_name}}", d.M, Inches(6.8), Inches(3), Inches(0.4),
           size=13, color=b.MUTED, bold=True)
    d.footer(s, 1, TOTAL, dark=True)


def build_uc_slide(page, industry, uc_id, title, challenge, solution, stats,
                   how_it_works, stack, systems, users, source, insight):
    """Use-case realization slide — Canva template layout."""
    s = d.slide(fill=b.WHITE)
    PANEL_W = Inches(8.833)
    PHOTO_W = d.W - PANEL_W

    # teal left panel
    d.rect(s, 0, 0, PANEL_W, d.H, b.TEAL)

    # title
    label = f"{uc_id} | {industry}"
    d.text(s, label, Inches(0.4), Inches(0.15), PANEL_W - Inches(0.7), Inches(0.3),
           size=10, color=b.NAVY, bold=True)
    d.text(s, title, Inches(0.4), Inches(0.4), PANEL_W - Inches(0.7), Inches(0.45),
           size=20, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.4), Inches(0.85), Inches(2), Inches(0.03), b.NAVY)

    # CHALLENGE column
    col_w = Inches(3.85)
    y = Inches(0.98)
    d.text(s, "CHALLENGE", Inches(0.4), y, Inches(1.5), Inches(0.18),
           size=8, color=b.NAVY, bold=True)
    challenge_runs = [{"text": f"•  {c}", "size": 7.5, "color": b.NAVY, "space_before": 3} for c in challenge]
    d.text(s, challenge_runs, Inches(0.4), y + Inches(0.2), col_w, Inches(1.3))

    # SOLUTION column
    sol_x = Inches(4.4)
    d.text(s, "HOW IT'S REALIZED", sol_x, y, Inches(2), Inches(0.18),
           size=8, color=b.NAVY, bold=True)
    solution_runs = [{"text": f"•  {sl}", "size": 7.5, "color": b.NAVY, "space_before": 3} for sl in solution]
    d.text(s, solution_runs, sol_x, y + Inches(0.2), col_w, Inches(1.3))

    # STATS boxes (gold numbers)
    stat_y = Inches(2.5)
    for i, (num, label) in enumerate(stats[:4]):
        sx = Inches(0.4) + Inches(i * 2.05)
        d.rect(s, sx, stat_y, Inches(1.9), Inches(0.75), b.NAVY, radius=0.02)
        d.text(s, num, sx, stat_y + Pt(4), Inches(1.9), Inches(0.38),
               size=18, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, label, sx, stat_y + Pt(32), Inches(1.9), Inches(0.32),
               size=7, color=b.WHITE, align=PP_ALIGN.CENTER)

    # HOW IT WORKS
    hiw_y = Inches(3.45)
    d.text(s, "HOW IT WORKS", Inches(0.4), hiw_y, Inches(2), Inches(0.18),
           size=8, color=b.NAVY, bold=True)
    hiw_runs = [{"text": f"→ {h}", "size": 7, "color": b.NAVY, "space_before": 2} for h in how_it_works]
    d.text(s, hiw_runs, Inches(0.4), hiw_y + Inches(0.2), PANEL_W - Inches(0.7), Inches(0.7))

    # BRAND VOICE INSIGHT (the voice-matched line)
    ins_y = Inches(4.45)
    d.text(s, "THE ACTUAL INSIGHT", Inches(0.4), ins_y, Inches(2), Inches(0.18),
           size=8, color=b.NAVY, bold=True)
    d.text(s, insight, Inches(0.4), ins_y + Inches(0.2), PANEL_W - Inches(0.7), Inches(0.65),
           size=8, color=b.NAVY, italic=True)

    # SOLUTION STACK bar
    stack_y = Inches(5.45)
    d.rect(s, Inches(0.3), stack_y, PANEL_W - Inches(0.5), Inches(0.75), b.NAVY)
    d.text(s, "SOLUTION STACK", Inches(0.4), stack_y + Inches(0.04), Inches(2), Inches(0.16),
           size=7.5, color=b.TEAL, bold=True)
    for i, (layer, detail) in enumerate(stack[:4]):
        col_x = Inches(0.4) + Inches(i * 2.05)
        d.text(s, layer, col_x, stack_y + Inches(0.2), Inches(1.9), Inches(0.16),
               size=7, color=b.TEAL, bold=True)
        d.text(s, detail, col_x, stack_y + Inches(0.38), Inches(1.9), Inches(0.32),
               size=6.5, color=b.WHITE)

    # SYSTEMS + USERS bars
    bar_y = Inches(6.3)
    if systems:
        d.rect(s, Inches(0.3), bar_y, Inches(4), Inches(0.32), b.ACCENT)
        d.text(s, "SYSTEMS: " + "  |  ".join(systems), Inches(0.4), bar_y + Pt(3),
               Inches(3.8), Inches(0.25), size=6.5, color=b.WHITE, bold=True)
    if users:
        d.rect(s, Inches(4.5), bar_y, Inches(4), Inches(0.32), b.DARK_TEAL)
        d.text(s, "USERS: " + users, Inches(4.6), bar_y + Pt(3),
               Inches(3.8), Inches(0.25), size=6.5, color=b.WHITE, bold=True)

    # SOURCE
    d.text(s, f"Source: {source}", Inches(0.4), Inches(6.7), PANEL_W - Inches(0.7), Inches(0.2),
           size=6, color=b.ACCENT, italic=True)

    # RIGHT strip — navy with stock photo overlay or solid
    d.rect(s, PANEL_W, 0, PHOTO_W, d.H, b.NAVY_2)
    # Industry label on right strip
    d.text(s, industry.upper(), PANEL_W + Inches(0.3), Inches(0.3),
           PHOTO_W - Inches(0.6), Inches(1.5),
           size=18, color=b.TEAL, bold=True)

    d.footer(s, page, TOTAL)


def build_summary():
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)

    d.text(s, "WHAT THE WINNERS HAVE IN COMMON", d.M, Inches(0.42),
           d.CW, Inches(0.6), size=28, color=b.WHITE, bold=True)
    d.rect(s, d.M, Inches(1.1), Inches(1.5), Inches(0.05), b.TEAL)

    rules = [
        ("01", "Define the number before writing code",
         "TD Bank, C.H. Robinson, Unilever — every winner had a specific metric with a specific baseline before day 1."),
        ("02", "Automate the boring part, not the judgment",
         "Every case keeps humans on decisions. AI handles extraction, matching, triage. Lawyers still decide. Underwriters still sign."),
        ("03", "Proprietary data is the moat, not the model",
         "C.H. Robinson's 100T data points. DroneDeploy's 34M annotations. JPMorgan's 12K training contracts. Same models, different data, wildly different outcomes."),
        ("04", "Composite AI beats pure LLM",
         "European 3PL: composite hit 92% accuracy vs. 78% pure agentic. TD Bank uses deterministic tools for arithmetic. Use the right tool for each sub-task."),
        ("05", "Trust is a deployment phase, not a launch event",
         "Unilever: 6-month technician trust period. Macy's: progressive rollout. The model is ready before the org is. Budget time for humans to catch up."),
    ]

    for i, (num, title, desc) in enumerate(rules):
        ry = Inches(1.5) + Inches(i * 1.08)
        d.rect(s, d.M, ry, d.CW, Inches(0.92), b.NAVY_2, radius=0.02)
        d.text(s, num, d.M + Pt(12), ry + Pt(10), Pt(40), Pt(30),
               size=22, color=b.GOLD, bold=True)
        d.text(s, title, d.M + Inches(0.6), ry + Pt(8), d.CW - Inches(1), Inches(0.3),
               size=16, color=b.WHITE, bold=True)
        d.text(s, desc, d.M + Inches(0.6), ry + Pt(32), d.CW - Inches(1), Inches(0.45),
               size=11, color=b.MUTED)

    d.footer(s, TOTAL - 1, TOTAL, dark=True)


def build_closer():
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
    d.rect(s, d.W - Inches(0.12), 0, Inches(0.12), d.H, b.NAVY_2)
    d.rect(s, d.W - Inches(0.18), 0, Inches(0.06), d.H, b.TEAL)

    d.text(s, "The best AI project is the one that actually ships.",
           d.M, Inches(2.2), Inches(10), Inches(1.8),
           size=42, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.9), Inches(1.5), Inches(0.05), b.TEAL)
    d.text(s, "Not the one with the cleanest architecture, the most sophisticated model,\nor the biggest budget. The one that ships. With a number attached.",
           d.M, Inches(4.2), Inches(9), Inches(0.8),
           size=16, color=b.MUTED)

    d.text(s, "{{brand_name}}", d.M, Inches(5.8), Inches(3), Inches(0.5),
           size=20, color=b.TEAL, bold=True)
    d.text(s, "{{tagline}}", d.M, Inches(6.3), Inches(5), Inches(0.4),
           size=14, color=b.MUTED)
    d.footer(s, TOTAL, TOTAL, dark=True)


# ═══════════════════════════════════════════════════
# BUILD ALL SLIDES
# ═══════════════════════════════════════════════════

# 1. Cover
build_cover()

# 2. Financial Services — TD Bank
build_uc_slide(
    page=2, industry="Financial Services",
    uc_id="UC-01", title="TD Bank — Mortgage Application Processing Agent",
    challenge=[
        "Mortgage applications require 15+ hours of manual document review per case",
        "Cross-referencing borrower docs (IDs, bank statements, income proof) is error-prone",
        "Hundreds of thousands of applications annually — scale demands automation",
        "LLMs hallucinate on arithmetic tasks (annualizing income from pay stubs)",
    ],
    solution=[
        "Agentic AI reads entire borrower document packages and extracts structured data",
        "Deterministic rules-based tools handle all arithmetic (not the LLM)",
        "Cross-references fields across documents, flags inconsistencies",
        "Human adjudicator signs off on every credit decision",
    ],
    stats=[
        ("15hrs → min", "Processing Time"),
        ("$826M", "2025 Origination"),
        ("Day 1", "Risk/Compliance Built In"),
        ("Jan 2026", "Deployed"),
    ],
    how_it_works=[
        "Document ingestion → OCR/NLP extraction → Field cross-reference → Inconsistency flagging",
        "Arithmetic operations routed to deterministic tools (not LLM) → Credit summary generated",
        "Human adjudicator reviews summary → Approves/rejects with full audit trail",
    ],
    stack=[
        ("Foundation Models", "Layer 6 + Claude + GPT (selective)"),
        ("Arithmetic", "Rules-based deterministic tools"),
        ("Governance", "TD Trustworthy AI framework"),
        ("Integration", "Core banking API pipeline"),
    ],
    systems=["Core Banking", "Doc Mgmt", "Credit Bureau"],
    users="Mortgage underwriters, credit adjudicators",
    source="American Banker, May 2026",
    insight="They didn't let the LLM do math. Deterministic tools for arithmetic, LLM for document reading. One use case done right before expanding. Dead simple discipline.",
)

# 3. Healthcare — Tampa General Hospital
build_uc_slide(
    page=3, industry="Healthcare & Life Sciences",
    uc_id="UC-02", title="Tampa General Hospital — AI Sepsis Detection",
    challenge=[
        "Sepsis kills 270,000+ Americans annually — early detection is the intervention window",
        "Vital sign deterioration patterns are subtle, easily missed in busy wards",
        "Manual monitoring can't scale across hundreds of patients simultaneously",
        "Delayed detection = exponentially worse outcomes (every hour matters)",
    ],
    solution=[
        "AI-driven care coordination center integrates real-time EHR signals",
        "Predictive models detect early sepsis indicators from vital patterns",
        "Automated alerts trigger care coordination: intervention, bed allocation, discharge timing",
        "Same platform extends to throughput optimization (equivalent to adding beds)",
    ],
    stats=[
        ("700+", "Lives Saved"),
        ("37 beds", "Capacity Equivalent"),
        ("5%", "Length of Stay Reduction"),
        ("24/7", "Real-time Monitoring"),
    ],
    how_it_works=[
        "EHR data streams → ML models score vital deterioration patterns → Risk threshold triggers",
        "High-risk alerts routed to care coordination team → Intervention protocol initiated",
        "Same data layer feeds throughput optimization: discharge timing, bed allocation",
    ],
    stack=[
        ("Platform", "Palantir AIP"),
        ("Data", "Real-time EHR signals"),
        ("ML Models", "Vital pattern predictors"),
        ("Integration", "HL7/FHIR workflows"),
    ],
    systems=["EHR", "PACS", "Nursing Station", "Bed Mgmt"],
    users="Care coordinators, hospitalists, nursing staff",
    source="Becker's Hospital Review, December 2025",
    insight="Nobody asked the AI to diagnose anything. It detects deterioration patterns and sorts the priority list. The care team still decides. But 700 people walked out who otherwise wouldn't have.",
)

# 4. Manufacturing — Unilever
build_uc_slide(
    page=4, industry="Manufacturing & Industrial",
    uc_id="UC-03", title="Unilever Indaiatuba — Predictive Maintenance at Scale",
    challenge=[
        "8.2% unplanned downtime across compressors, HVAC, packaging lines",
        "$5.1M annual maintenance baseline — reactive repairs are expensive",
        "Traditional scheduled maintenance misses 40%+ of actual failure patterns",
        "Technician trust in automated predictions is the real deployment barrier",
    ],
    solution=[
        "50,000+ IoT sensors feed time-series data to Amazon SageMaker models",
        "Anomaly detection predicts failures 14-28 days in advance at 92% accuracy",
        "Auto-generates work orders with equipment ID, failure type, time-to-failure",
        "6-month technician trust-building phase with feedback loops for model improvement",
    ],
    stats=[
        ("$2.3M", "Annual Savings (45%)"),
        ("4.9%", "Downtime (was 8.2%)"),
        ("85%+", "OEE (#1 Global)"),
        ("6.5 mo", "Payback Period"),
    ],
    how_it_works=[
        "50K sensors → SageMaker processes vibration/temp/pressure time-series → Anomaly scoring",
        "Score > threshold → Auto work order (equipment, failure type, predicted date) → CMMS",
        "Technician validates → Feedback loop improves model → 6-month trust cycle",
    ],
    stack=[
        ("ML Platform", "Amazon SageMaker"),
        ("Data", "50K+ IoT sensors (OPC-UA)"),
        ("Integration", "Unilever Mfg System"),
        ("Expansion", "7+ sites by Q4 2025"),
    ],
    systems=["SCADA", "CMMS", "MES", "ERP (SAP PM)"],
    users="Maintenance technicians, plant engineers, reliability managers",
    source="NSSG Insights, March 2026",
    insight="3 years of labeled failure data eliminated the data-collection phase that kills most mfg AI. Started with the 12 machines causing 80% of downtime. But the thing nobody talks about: the model was technically ready before the humans were. Trust took 6 months.",
)

# 5. Retail — Galeries Lafayette
build_uc_slide(
    page=5, industry="Retail & E-commerce",
    uc_id="UC-04", title="Galeries Lafayette — AI-Powered Search & Personalization",
    challenge=[
        "Legacy search failing at 600K product catalog scale (350K from marketplace)",
        "One-size-fits-all ranking ignores individual visitor behavior and intent",
        "Merchandising teams need category-level control — can't hand everything to AI",
        "Search conversion directly impacts revenue across 20% YoY growth channel",
    ],
    solution=[
        "Google Vertex AI Search for Commerce replaces legacy search stack",
        "Real-time personalized ranking per visitor via behavioral signals",
        "Grid Dynamics MXP gives merchandisers override controls per category",
        "Hybrid model: AI handles individual ranking, humans control brand positioning",
    ],
    stats=[
        ("+7%", "Total Revenue"),
        ("+8%", "Basket Value"),
        ("+20%", "Online Sales YoY"),
        ("600K", "Products Ranked"),
    ],
    how_it_works=[
        "Visitor arrives → Behavioral signals scored → Personalized ranking generated per session",
        "Merchandising Studio applies category rules → AI respects brand positioning constraints",
        "Real-time inventory/pricing feeds ensure availability accuracy across 600K SKUs",
    ],
    stack=[
        ("Search/Rank", "Vertex AI Search for Commerce"),
        ("Merch Control", "Grid Dynamics MXP"),
        ("Data", "Real-time inventory + pricing"),
        ("Personalization", "Session + behavioral signals"),
    ],
    systems=["E-commerce Platform", "PIM", "Marketplace Feed", "WMS"],
    users="Online shoppers, merchandising team, category managers",
    source="Business Wire, April 2026",
    insight="Purely autonomous AI would have been blocked by merchandising teams. Give humans the override, they'll trust the system. The hybrid model drove adoption. That's the lesson most AI projects miss.",
)

# 6. Logistics — C.H. Robinson
build_uc_slide(
    page=6, industry="Logistics & Supply Chain",
    uc_id="UC-05", title="C.H. Robinson — Lean AI Operating System (30+ Agents)",
    challenge=[
        "37M shipments/year generating 100 trillion data points — manual processing impossible",
        "Price quoting: 17-20 minutes per quote, covering only 65% of inbound requests",
        "Order processing: 4 hours per order from email to system entry",
        "Freight tracking requires human phone calls — one agent captured 318K updates/month",
    ],
    solution=[
        "30+ AI agents on proprietary 100T data points via LangChain/LangGraph orchestration",
        "Email-to-order extraction automates 5,500 orders/day",
        "Freight classification, quoting, scheduling, and phone-based tracking all agentic",
        "LangSmith observability monitors agent accuracy and drift in production",
    ],
    stats=[
        ("32 sec", "Quote Time (was 17 min)"),
        ("100%", "Quote Coverage (was 65%)"),
        ("<2 min", "Order Processing (was 4hr)"),
        ("+40%", "Overall Productivity"),
    ],
    how_it_works=[
        "Email arrives → LangGraph agent extracts order fields → Validates against 100T data points",
        "Quote agent scores pricing using proprietary demand model → Response in 32 seconds",
        "Phone agent calls carriers for tracking updates → Captures 318K updates/month autonomously",
    ],
    stack=[
        ("Orchestration", "LangChain + LangGraph"),
        ("Observability", "LangSmith"),
        ("Data", "100T proprietary logistics pts"),
        ("Culture", "Builder-first, no SaaS dep"),
    ],
    systems=["TMS", "CRM", "Carrier APIs", "Email", "Phone"],
    users="Freight brokers, logistics coordinators, carrier ops",
    source="C.H. Robinson PR + The Applied, 2026",
    insight="Proprietary data moat — competitors can't replicate models trained on 37M shipments/year. They mapped AI to Lean waste concepts before building. Concentrated on quote-to-cash first. Stock price doubled during an industry downturn.",
)

# 7. Energy — Con Edison
build_uc_slide(
    page=7, industry="Energy & Utilities",
    uc_id="UC-06", title="Con Edison + C3 AI — Smart Meter Operations at Scale",
    challenge=[
        "5.3M smart meters generating 1 petabyte/year — 13 siloed data sources",
        "Meter deployment issues (configuration errors, installation failures) go undetected",
        "Small anomalies multiply into large outage and billing costs at utility scale",
        "No unified view across 13 systems — each operates independently",
    ],
    solution=[
        "C3 AI Platform consolidates 13 data sources into unified data image",
        "2 ML algorithms + 50 custom analytics on 180B rows of annual meter data",
        "Real-time anomaly detection from individual meter to system-wide view",
        "Automated flagging of deployment issues, network anomalies, performance drift",
    ],
    stats=[
        ("2,300", "Issues Found (4 months)"),
        ("$854M", "Annual Customer Benefit"),
        ("5.3M", "Meters Monitored"),
        ("13 → 1", "Data Sources Unified"),
    ],
    how_it_works=[
        "13 source systems → C3 AI unification layer → Single data image (2yr historical load)",
        "180B rows/year → 2 ML models + 50 analytics → Anomaly scoring per meter",
        "Flagged issues → Work order generation → Field crew dispatch with meter-specific context",
    ],
    stack=[
        ("Platform", "C3 AI Platform"),
        ("Application", "C3 AI AMI Operations"),
        ("Data", "180B rows/yr, 13 sources"),
        ("ML", "2 models + 50 analytics"),
    ],
    systems=["AMI/MDM", "GIS", "OMS", "Billing", "SCADA"],
    users="Grid operations, field crews, customer service, planning",
    source="The Applied, May 2026",
    insight="The 13-to-1 data consolidation was the hard part. The analytics ran on top of clean, unified data. Find configuration errors early — the math is enormous at 5.3M meter scale.",
)

# 8. Legal — Top-100 Law Firm
build_uc_slide(
    page=8, industry="Legal & Professional Services",
    uc_id="UC-07", title="Top-100 Law Firm — Contract Intelligence Platform",
    challenge=[
        "Paralegal review: 40 hours per contract across 90+ clause types",
        "M&A due diligence bottlenecked by document volume (14K+ docs per deal)",
        "300-page agreements require cross-clause reasoning that chunking breaks",
        "Outside counsel spend growing 15% annually — need to shift work internal",
    ],
    solution=[
        "Textract → Custom NER (45K training contracts) → Claude 3.5 Sonnet (200K context)",
        "Single-pass reading of 300-page agreements — no chunking, no broken cross-references",
        "Confidence gating: <0.85 routes to human review via Amazon A2I",
        "Kendra indexes 45K contracts for natural-language cross-contract search",
    ],
    stats=[
        ("70%", "Review Time Reduction"),
        ("$2.4M", "Billable Hours Recaptured"),
        ("99.1%", "Clause Extraction Accuracy"),
        ("41%", "Faster M&A Due Diligence"),
    ],
    how_it_works=[
        "PDF → Textract (layout-preserving OCR) → Custom NER identifies 90+ clause types",
        "Claude 3.5 Sonnet (200K context) → Summaries + risk flags + reasoning traces → Single pass",
        "Confidence < 0.85 → A2I routes to paralegal review → Feedback improves model",
    ],
    stack=[
        ("OCR", "Amazon Textract"),
        ("NER", "SageMaker (45K contracts)"),
        ("LLM", "Claude 3.5 Sonnet (Bedrock)"),
        ("Search", "Amazon Kendra"),
    ],
    systems=["iManage", "Aderant", "Outlook", "CLM"],
    users="Paralegals, associates, M&A partners",
    source="DreamzTech, April 2026",
    insight="Lawyers weren't spending 40 hours on judgment. They spent 28 hours finding clauses and 12 on judgment. Now they spend 12 on judgment. Everyone does what they're actually good at.",
)

# 9. Real Estate — DroneDeploy
build_uc_slide(
    page=9, industry="Real Estate & Construction",
    uc_id="UC-08", title="DroneDeploy + Barton Malow — Construction Site Intelligence",
    challenge=[
        "Manual site walks miss events and rely on superintendent's memory",
        "Safety violations go undetected — poor incident documentation industry-wide",
        "Progress reporting takes 2 days of manual compilation per project",
        "Generic computer vision doesn't understand what 'installed' means per trade",
    ],
    solution=[
        "4 AI agents: Progress, Safety, Inspection, Embodied — trained on 34M annotations",
        "Autonomous ground robots + docked drones capture sites overnight",
        "Morning reports show overnight progress by trade before the team arrives",
        "Safety AI trained on 120K labeled examples flags conditions in real time",
    ],
    stats=[
        ("34M", "Training Annotations"),
        ("+340%", "Safety Violations Caught"),
        ("48%", "Injury Reduction (BCG)"),
        ("3M+", "Sites in Production"),
    ],
    how_it_works=[
        "Overnight: autonomous robots + drones capture site from fixed vantage points",
        "Morning: Progress AI generates structured report (installed work, trade progress)",
        "Continuous: Safety AI flags violations (PPE, guardrails) → Real-time notifications",
    ],
    stack=[
        ("Vision", "34M annotation corpus"),
        ("Capture", "Ground robots + docked drones"),
        ("Agents", "Progress, Safety, Inspection, Embodied"),
        ("Integration", "Procore, PlanGrid, BIM"),
    ],
    systems=["BIM", "Procore", "PlanGrid", "GIS", "ERP"],
    users="Superintendents, project managers, safety officers",
    source="DroneDeploy Blog, April 2026; BCG, 2026",
    insight="DroneDeploy's 13-year annotation corpus — 34M labeled examples across 180 countries — is the moat. The superintendent now acts on data instead of generating it. Faster decisions, fewer surprises.",
)

# 10. Summary
build_summary()

# 11. Closer
build_closer()


# Save
OUT = Path(__file__).resolve().parent / "uc4-ai-use-cases-presales.pptx"
d.save(str(OUT))
print(f"Size: {OUT.stat().st_size / 1024:.0f} KB")
