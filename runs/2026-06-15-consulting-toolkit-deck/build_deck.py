#!/usr/bin/env python3
"""
build_deck.py — AI Consulting Toolkit Framework Reference
5 packs · 51 skills · full engagement lifecycle
Firm-agnostic: set FIRM_NAME and FIRM_EMAIL to rebrand for any consulting firm.
"""
import os, sys
from pathlib import Path

sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt

RUN_DIR = Path(__file__).parent
FIRM_NAME  = os.environ.get("FIRM_NAME",  "AI Consulting Toolkit")
FIRM_EMAIL = os.environ.get("FIRM_EMAIL", "")
OUT = RUN_DIR / "consulting-toolkit-draft.pptx"
_footer_parts = [FIRM_NAME, FIRM_EMAIL] if FIRM_EMAIL else [FIRM_NAME]
FOOTER = "  ·  ".join(_footer_parts)

# ── ALL SKILL DATA ────────────────────────────────────────────────────────────

PACKS = [
    {
        "section": "01", "n_skills": 21,
        "name": "Strategy & Advisory",
        "trigger": "/strategy-consulting",
        "tagline": "21 structured analytical frameworks for diagnosis, market intelligence, strategic choice, execution planning, risk governance, and executive communication",
        "chain": "Entry point for any engagement — outputs chain into ai-transformation and solution-delivery",
        "domains": [
            {
                "name": "Diagnosis & Framing",
                "sub": "Stabilise the fact base before deciding what to do",
                "skills": [
                    {"name": "Situation Assessment", "trigger": "/situation-assessment",
                     "when": "Business reviews, turnaround diagnosis, board prep — when the fact base is contested or unclear",
                     "produces": "Fact base table, momentum signals, key issues list, initial hypotheses"},
                    {"name": "Growth Barriers", "trigger": "/growth-barriers",
                     "when": "Revenue has plateaued or growth is below expectation — diagnose the real constraint",
                     "produces": "Barrier map (demand / supply / capability), evidence register, highest-leverage unlock"},
                    {"name": "Assumption Audit", "trigger": "/assumption-audit",
                     "when": "Before a major investment or board approval — stress-test the plan's hidden assumptions",
                     "produces": "Assumption register with confidence/impact scoring, red-flag list, pressure-test questions"},
                ],
            },
            {
                "name": "Market & Competitive Intelligence",
                "sub": "Understand the landscape before committing to a position",
                "skills": [
                    {"name": "Market Mapping", "trigger": "/market-mapping",
                     "when": "Market entry, expansion planning, or TAM/SAM/SOM sizing for an investment case",
                     "produces": "Market size (TAM/SAM/SOM), profit pool distribution, segment map, entry barriers"},
                    {"name": "Competitive Intel", "trigger": "/competitive-intel",
                     "when": "Before a product launch, pricing change, or when a competitor makes a significant move",
                     "produces": "Competitor profiles, strength/weakness matrix, differentiation map, counter-moves"},
                    {"name": "Customer Segmentation", "trigger": "/customer-segmentation",
                     "when": "Defining the ICP, designing go-to-market focus, or building a retention strategy",
                     "produces": "Segment profiles (value/need/behaviour), ICP definition, GTM priorities"},
                    {"name": "Profit Pool Analysis", "trigger": "/profit-pool-analysis",
                     "when": "Market entry, product portfolio decisions, or channel strategy evaluation",
                     "produces": "Profit pool distribution across value chain, winner characteristics, strategic implications"},
                ],
            },
            {
                "name": "Strategic Choice & Economics",
                "sub": "Generate options and quantify the economics before committing",
                "skills": [
                    {"name": "Strategic Options", "trigger": "/strategic-options",
                     "when": "Multiple credible strategic paths exist — build-buy-partner, market choices, product direction",
                     "produces": "Long-list to shortlist, evaluation against criteria, recommendation with rationale"},
                    {"name": "Business Case Builder", "trigger": "/business-case-builder",
                     "when": "An investment needs NPV/ROI quantification for board or leadership approval",
                     "produces": "Business case with NPV/IRR, cost-benefit table, scenario analysis, sensitivity table"},
                    {"name": "Portfolio Review", "trigger": "/portfolio-review",
                     "when": "Annual planning or capital allocation — where to invest, hold, or exit across the portfolio",
                     "produces": "Portfolio matrix, strategic fit vs financial contribution, reallocation recommendation"},
                    {"name": "Pricing Strategy", "trigger": "/pricing-strategy",
                     "when": "Price increase, discount leakage, packaging redesign, or new product pricing",
                     "produces": "Pricing model recommendation, discount policy, price-to-value positioning map"},
                ],
            },
            {
                "name": "Operating Model & Execution",
                "sub": "Define how the organisation executes — structure, roadmap, priorities",
                "skills": [
                    {"name": "Operating Model Design", "trigger": "/operating-model-design",
                     "when": "Transformation, new business unit, or functional redesign requiring a new structure",
                     "produces": "Target operating model, capability map, governance design, transition path"},
                    {"name": "Transformation Roadmap", "trigger": "/transformation-roadmap",
                     "when": "Major change programme requiring phased, fundable waves with clear sequencing",
                     "produces": "Phased roadmap, initiative register, dependency map, success metrics per phase"},
                    {"name": "Initiative Prioritizer", "trigger": "/initiative-prioritizer",
                     "when": "Too many competing initiatives — rank and sequence when capacity and budget are constrained",
                     "produces": "Scored initiative register, recommended portfolio, sequencing rationale, quick wins"},
                ],
            },
            {
                "name": "Risk, Performance & Value Governance",
                "sub": "Govern risk, measure performance, and prove value over time",
                "skills": [
                    {"name": "KPI Architect", "trigger": "/kpi-architect",
                     "when": "Metrics redesign, dashboard build, OKR planning, or performance management overhaul",
                     "produces": "KPI hierarchy (lagging/leading), measurement definitions, accountability map, reporting cadence"},
                    {"name": "Risk & Mitigation", "trigger": "/risk-and-mitigation",
                     "when": "Strategy approval, launch risk, or board risk review requiring a structured register",
                     "produces": "Risk register with P×I scores, mitigation plans, residual risk assessment"},
                    {"name": "Value Realization", "trigger": "/value-realization",
                     "when": "Tracking whether a transformation is delivering the promised business case",
                     "produces": "Benefits tracker, variance analysis, corrective actions register, revised forecast"},
                    {"name": "War Gaming", "trigger": "/war-gaming",
                     "when": "Pressure-test a strategy by simulating competitor and market responses",
                     "produces": "Scenario outcomes, vulnerability map, strategy adjustments, early-warning signals"},
                ],
            },
            {
                "name": "Alignment & Executive Communication",
                "sub": "Turn findings into decisions and decisions into aligned action",
                "skills": [
                    {"name": "Decision Memo", "trigger": "/decision-memo",
                     "when": "A decision requires executive or board approval — produce a structured briefing note",
                     "produces": "One-page memo: issue framing, options, recommendation, ask, risk summary"},
                    {"name": "Narrative Builder", "trigger": "/narrative-builder",
                     "when": "Building a Pyramid Principle story arc for a strategy presentation or board deck",
                     "produces": "Story arc, storyboard outline with beats, slide-by-slide narrative flow"},
                    {"name": "Stakeholder Alignment", "trigger": "/stakeholder-alignment",
                     "when": "Executive buy-in, board approval, or change management requiring a structured alignment plan",
                     "produces": "Stakeholder map, influence/interest grid, engagement plan, objection responses"},
                ],
            },
        ],
    },
    {
        "section": "02", "n_skills": 6,
        "name": "AI & Digital Transformation",
        "trigger": "/ai-transformation",
        "tagline": "6 AI-specific frameworks for maturity assessment, data readiness, use case prioritisation, operating model design, responsible AI, and build-buy-partner decisions",
        "chain": "Chains from strategy-consulting → outputs chain into solution-delivery",
        "domains": [
            {
                "name": "Maturity & Readiness",
                "sub": "Anchor the AI strategy in what is actually possible",
                "skills": [
                    {"name": "AI Maturity Assessment", "trigger": "/ai-maturity-assessment",
                     "when": "Start of any AI strategy engagement — before recommending investments or use cases",
                     "produces": "Maturity scorecard (5 dimensions × 1–4 levels), blocker analysis, priority investments"},
                    {"name": "Data Readiness Assessment", "trigger": "/data-readiness-assessment",
                     "when": "Before committing to AI use cases — assess data fitness for each planned use case",
                     "produces": "Readiness verdict per use case (Ready/Conditional/Blocked), gaps register, remediation roadmap"},
                ],
            },
            {
                "name": "Use Case & Operating Model",
                "sub": "Select the right use cases and organise the AI function",
                "skills": [
                    {"name": "AI Use Case Prioritiser", "trigger": "/ai-use-case-prioritiser",
                     "when": "Long list of AI candidates must be narrowed to a funded, sequenced delivery portfolio",
                     "produces": "Scored register, Value × Feasibility 2×2 map, Wave 1/2/3 portfolio, parking lot"},
                    {"name": "AI Operating Model", "trigger": "/ai-operating-model",
                     "when": "Organisation ready to industrialise AI — design CoE / Federated / Embedded / Hybrid model",
                     "produces": "Archetype evaluation, governance design, role requirements, capability build sequence"},
                ],
            },
            {
                "name": "Governance & Decisions",
                "sub": "Govern AI responsibly and make defensible sourcing decisions",
                "skills": [
                    {"name": "Responsible AI Framework", "trigger": "/responsible-ai-framework",
                     "when": "Before any customer-facing or high-stakes AI deployment — or when regulators require it",
                     "produces": "6-principle framework, 4-tier risk taxonomy, use case risk register, review board design"},
                    {"name": "AI Build-Buy-Partner", "trigger": "/ai-build-buy-partner",
                     "when": "Sourcing decisions needed for each AI capability — build, buy a product, or partner?",
                     "produces": "Build/Buy/Partner decision per capability, vendor shortlist, commercial model recommendation"},
                ],
            },
        ],
    },
    {
        "section": "03", "n_skills": 13,
        "name": "Solution Delivery",
        "trigger": "/solution-delivery",
        "tagline": "13 implementation frameworks covering solution design, delivery governance, change management, and value realization — from blueprint to benefits",
        "chain": "Chains from ai-transformation → outputs chain into continuous-improvement",
        "domains": [
            {
                "name": "Solution Design",
                "sub": "Translate strategy into a structured, sequenced delivery design",
                "skills": [
                    {"name": "Solution Blueprint", "trigger": "/solution-blueprint",
                     "when": "Strategic option chosen — translate it into capabilities, components, workstreams, and phases",
                     "produces": "Capability map, component register, dependency map, phased delivery plan"},
                    {"name": "Architecture Decision Record", "trigger": "/architecture-decision-record",
                     "when": "A major technical decision must be documented, challenged, and available for later review",
                     "produces": "ADR: context, options evaluated, decision, consequences, review trigger"},
                    {"name": "Integration Sequencing", "trigger": "/integration-sequencing",
                     "when": "Multiple systems must be integrated — sequence the work to de-risk delivery",
                     "produces": "Thin thread, P1/P2/P3 integration phases, dependency map, test gates, rollback positions"},
                ],
            },
            {
                "name": "Delivery Governance",
                "sub": "Track risks, gates, and accountability from kickoff to go-live",
                "skills": [
                    {"name": "RAID Log", "trigger": "/raid-log",
                     "when": "Project kickoff and ongoing weekly — maintain risks/assumptions/issues/dependencies",
                     "produces": "RAID register with RAG status, P×I risk scores (≥12 = mandatory mitigation), owner assignments"},
                    {"name": "Stage Gate Review", "trigger": "/stage-gate-review",
                     "when": "End of each delivery phase — assess whether exit criteria are met before advancing",
                     "produces": "Gate verdict (Go / Conditional Go / No-Go), exit criteria scorecard, lessons captured"},
                    {"name": "Delivery Risk Assessment", "trigger": "/delivery-risk-assessment",
                     "when": "Project start and whenever a major risk surfaces — build a structured risk register",
                     "produces": "Risk register (5 categories, P×I scored), heat map, top-5 critical risks with mitigations"},
                    {"name": "RACI Design", "trigger": "/raci-design",
                     "when": "After blueprint and operating model — assign R/A/C/I for each decision and deliverable",
                     "produces": "RACI matrix, constraint validation (one A per row), role workload summary, escalation path"},
                ],
            },
            {
                "name": "Change Management",
                "sub": "Build the will and skill to change — before, during, and after go-live",
                "skills": [
                    {"name": "Change Readiness Assessment", "trigger": "/change-readiness-assessment",
                     "when": "Before designing the adoption plan — identify where resistance will emerge by group",
                     "produces": "ADKAR scorecard per group (1–5 per dimension), active barrier point, targeted interventions"},
                    {"name": "Change Impact Assessment", "trigger": "/change-impact-assessment",
                     "when": "Assess the severity of change across process, technology, role, and behaviour dimensions",
                     "produces": "Impact severity matrix (H/M/L per dimension per group), compounding impact identification"},
                    {"name": "Adoption Plan", "trigger": "/adoption-plan",
                     "when": "Once impacts and readiness are understood — design activities that drive genuine adoption",
                     "produces": "Activity schedule, comms plan, training plan, reinforcement mechanisms, adoption metrics"},
                ],
            },
            {
                "name": "Value Realization",
                "sub": "Prove the business case was delivered — track and sustain benefits",
                "skills": [
                    {"name": "Benefits Register", "trigger": "/benefits-register",
                     "when": "Project start — translate the business case into tracked benefits with owners and milestones",
                     "produces": "Benefits register with baseline/target/owner, 30/90/180-day milestones, disbenefit register"},
                    {"name": "Post-Implementation Review", "trigger": "/post-implementation-review",
                     "when": "90 days post go-live — compare actuals against the business case, identify corrective actions",
                     "produces": "Actuals vs target table, variance root-cause (five-why), forward actions register, revised forecast"},
                    {"name": "Hypercare Plan", "trigger": "/hypercare-plan",
                     "when": "2 weeks before go-live — design the intensive support model bridging go-live and BAU",
                     "produces": "L1/L2/L3 support model, triage SLAs, KT schedule, hypercare exit criteria dashboard"},
                ],
            },
        ],
    },
    {
        "section": "04", "n_skills": 6,
        "name": "Engagement Management",
        "trigger": "/engagement-management",
        "tagline": "6 engagement lifecycle frameworks covering pursuit, delivery governance, and closeout — runs in parallel with all other packs from first pursuit conversation to final sign-off",
        "chain": "Cross-cutting — runs in parallel with all other packs throughout the full engagement",
        "domains": [
            {
                "name": "Pursuit",
                "sub": "Win the right work at the right terms before the proposal is written",
                "skills": [
                    {"name": "Win Strategy", "trigger": "/win-strategy",
                     "when": "Opportunity qualified — define competitive positioning before the proposal team starts writing",
                     "produces": "Client hot buttons, competitor analysis, 3–4 win themes, vulnerabilities neutralisation plan, Go/No-Go"},
                    {"name": "Commercial Structuring", "trigger": "/commercial-structuring",
                     "when": "Win strategy set — design the fee model, resource plan, and margin scenarios before pricing",
                     "produces": "3 commercial model options, P&L at three scenarios, negotiation brief, walk-away price"},
                ],
            },
            {
                "name": "Delivery",
                "sub": "Run the engagement — governance, stakeholders, and weekly reporting",
                "skills": [
                    {"name": "Engagement Kickoff", "trigger": "/engagement-kickoff",
                     "when": "Week before the engagement starts — plan the kick-off meeting and first 30 days",
                     "produces": "Kick-off meeting agenda, governance cadence design, ways of working charter, 30-day plan"},
                    {"name": "Stakeholder Cadence", "trigger": "/stakeholder-cadence",
                     "when": "Day 1 — design the forum architecture that governs the engagement from kick-off to closeout",
                     "produces": "Forum architecture (governance vs collaboration), agenda templates, escalation path, 90-day calendar"},
                    {"name": "Progress Reporting", "trigger": "/progress-reporting",
                     "when": "Weekly or monthly — produce the RAG status dashboard and steering committee pack",
                     "produces": "RAG dashboard with trend arrows, milestone tracker, top-3 issues, decisions needed, budget burn"},
                ],
            },
            {
                "name": "Closeout",
                "sub": "Close cleanly and secure the next commercial opportunity",
                "skills": [
                    {"name": "Engagement Closeout", "trigger": "/engagement-closeout",
                     "when": "Final 2 weeks — deliverable sign-off, satisfaction capture, reference case, follow-on pipeline",
                     "produces": "Deliverable sign-off record, client satisfaction scorecard (5 dimensions), reference case, follow-on brief"},
                ],
            },
        ],
    },
    {
        "section": "05", "n_skills": 5,
        "name": "Continuous Improvement",
        "trigger": "/continuous-improvement",
        "tagline": "5 post-delivery frameworks for BAU operating rhythm, quarterly performance reviews, improvement backlog, maturity progression, and consulting exit — closes the loop back to strategy",
        "chain": "Chains from solution-delivery → loops back to strategy-consulting (next engagement cycle)",
        "domains": [
            {
                "name": "Operations",
                "sub": "Design and run the BAU governance that sustains delivered capability",
                "skills": [
                    {"name": "Operating Rhythm Design", "trigger": "/operating-rhythm-design",
                     "when": "End of hypercare — design the BAU meeting cadence and governance that replaces consulting oversight",
                     "produces": "3-layer operating rhythm (operational/performance/strategic), forum design, CI loop, exit checklist"},
                    {"name": "Performance Review", "trigger": "/performance-review",
                     "when": "Monthly or quarterly — review KPI actuals vs targets and drive corrective actions",
                     "produces": "KPI scorecard with RAG and trend arrows, benefits update, variance root-cause, forward corrective actions"},
                ],
            },
            {
                "name": "Improvement",
                "sub": "Score, sequence, and sustain post-delivery improvements",
                "skills": [
                    {"name": "CI Backlog", "trigger": "/continuous-improvement-backlog",
                     "when": "Ongoing post go-live — capture, score, and sequence enhancement ideas before they are lost",
                     "produces": "Scored backlog (Value+Urgency+Effort+Risk), Horizon 1/2/3 roadmap, parking lot with reasons"},
                    {"name": "Capability Maturity Progression", "trigger": "/capability-maturity-progression",
                     "when": "Annual — assess maturity level and plan the investments needed to reach the next level",
                     "produces": "Maturity scorecard (CMM 1–5 per dimension), blocker analysis, progression roadmap, leading indicators"},
                ],
            },
            {
                "name": "Transition",
                "sub": "Exit with confidence — knowledge transferred, governance running",
                "skills": [
                    {"name": "Exit Strategy", "trigger": "/exit-strategy",
                     "when": "4–6 weeks before consulting exit — plan knowledge transfer, retained advisory, and BAU handover",
                     "produces": "Exit readiness scorecard (Ready/Conditional/Not Ready), KT plan, retained advisory model, re-engagement conditions"},
                ],
            },
        ],
    },
]

# ── total slide count ─────────────────────────────────────────────────────────
TOTAL = 2  # cover + chain overview
for p in PACKS:
    TOTAL += 1 + len(p["domains"])
print(f"Planning {TOTAL} slides")

# ── deck init ─────────────────────────────────────────────────────────────────
d = Deck(footer=FOOTER)
b = d.b
W, H, M, CW = d.W, d.H, d.M, d.CW

# ── skill card helpers ────────────────────────────────────────────────────────

def _card(s, sk, left, top, width, height):
    pad = Inches(0.17)
    inner_w = width - pad * 2

    d.rect(s, left, top, width, height, b.SOFT, radius=0.04, shadow=True)
    d.rect(s, left, top, width, Inches(0.09), b.TEAL)

    # trigger pill
    pill_h = Inches(0.29)
    d.rect(s, left + pad, top + Inches(0.16), inner_w, pill_h, b.NAVY, radius=0.06)
    d.text(s, sk["trigger"],
           left + pad + Inches(0.08), top + Inches(0.19),
           inner_w - Inches(0.1), pill_h - Inches(0.05),
           size=9, color=b.TEAL, bold=True, shrink=True)

    # skill name
    d.text(s, sk["name"],
           left + pad, top + Inches(0.55),
           inner_w, Inches(0.65),
           size=12.5, color=b.INK, bold=True, shrink=True, ls=1.15)

    # when
    when_h = height * 0.30
    d.text(s, sk["when"],
           left + pad, top + Inches(1.23),
           inner_w, when_h,
           size=10, color=b.MUTED, shrink=True, ls=1.2)

    # produces label + content (anchored from card bottom)
    prod_label_y = top + height - Inches(1.52)
    d.text(s, "PRODUCES",
           left + pad, prod_label_y,
           inner_w, Inches(0.2),
           size=8, color=b.TEAL, bold=True)
    d.text(s, sk["produces"],
           left + pad, prod_label_y + Inches(0.22),
           inner_w, Inches(1.12),
           size=9.5, color=b.INK, shrink=True, ls=1.15)


def skill_cards(s, skills, top=Inches(1.82), bottom=Inches(7.06)):
    n = len(skills)
    avail_h = bottom - top
    card_h = avail_h - Inches(0.06)

    if n == 1:
        card_w = CW * 0.52
        cx = M + (CW - card_w) / 2
        _card(s, skills[0], cx, top, card_w, card_h)
    else:
        gap = Inches(0.18) if n <= 3 else Inches(0.14)
        card_w = (CW - gap * (n - 1)) / n
        for i, sk in enumerate(skills):
            cx = M + i * (card_w + gap)
            _card(s, sk, cx, top, card_w, card_h)

# ── SLIDE 1: Cover ────────────────────────────────────────────────────────────
page = 1
s = d.slide(fill=b.NAVY)

d.rect(s, W - Inches(2.9), 0, Inches(2.9), H, b.NAVY_2)
d.rect(s, W - Inches(2.9), 0, Inches(0.1), H, b.TEAL)

d.text(s, "CONSULTING INTELLIGENCE TOOLKIT",
       M, Inches(1.1), CW * 0.64, Inches(0.37),
       size=11.5, color=b.TEAL, bold=True)
d.text(s, "AI Consulting\nSkill Packs",
       M, Inches(1.58), CW * 0.64, Inches(2.35),
       size=44, color=b.WHITE, bold=True, shrink=True)
d.rect(s, M, Inches(4.05), Inches(1.7), Inches(0.06), b.TEAL)
d.text(s, "5 Skill Packs  ·  51 Skills  ·  Full Engagement Lifecycle",
       M, Inches(4.22), CW * 0.64, Inches(0.42),
       size=13.5, color=b.LIGHT_TEAL)

# right stat
rx = W - Inches(2.62)
rw = Inches(2.3)
d.text(s, "51", rx, Inches(1.35), rw, Inches(1.45),
       size=92, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.text(s, "TOTAL SKILLS", rx, Inches(2.82), rw, Inches(0.33),
       size=10.5, color=b.MUTED, bold=True, align=PP_ALIGN.CENTER)
d.rect(s, rx + rw * 0.15, Inches(3.28), rw * 0.7, Inches(0.04), b.MUTED)
d.text(s, "5 PACKS  ·  17 DOMAINS", rx, Inches(3.4), rw, Inches(0.28),
       size=9.5, color=b.MUTED, align=PP_ALIGN.CENTER)

# pack chips
chip_data = [
    ("21", "strategy-consulting"),
    ("6",  "ai-transformation"),
    ("13", "solution-delivery"),
    ("6",  "engagement-mgmt"),
    ("5",  "continuous-impr."),
]
chip_w = (CW - Inches(0.18) * 4) / 5
chip_h = Inches(1.05)
chip_y = Inches(5.55)
for i, (num, nm) in enumerate(chip_data):
    cx = M + i * (chip_w + Inches(0.18))
    d.rect(s, cx, chip_y, chip_w, chip_h, b.NAVY_2, radius=0.04)
    d.rect(s, cx, chip_y, Inches(0.07), chip_h, b.TEAL)
    d.text(s, num, cx + Inches(0.14), chip_y + Inches(0.04), chip_w - Inches(0.18), Inches(0.52),
           size=26, color=b.GOLD, bold=True)
    d.text(s, nm, cx + Inches(0.14), chip_y + Inches(0.56), chip_w - Inches(0.18), Inches(0.42),
           size=9, color=b.WHITE, bold=True, shrink=True)

d.footer(s, page, TOTAL, dark=True)

# ── SLIDE 2: Chain Overview ───────────────────────────────────────────────────
page += 1
s = d.slide(fill=b.WHITE)
d.header(s, "51 Skills Covering the Full Consulting Engagement Lifecycle",
         "engagement-management runs in parallel with all other packs  ·  all other packs chain left to right")

chain_packs = [
    ("strategy-\nconsulting", "21", "Diagnose → Strategise\n→ Execute → Communicate"),
    ("ai-\ntransformation", "6",  "Maturity → Use Cases\n→ Operating Model → Governance"),
    ("solution-\ndelivery", "13", "Blueprint → Govern\n→ Change → Value Realise"),
    ("continuous-\nimprovement", "5", "Operate → Improve\n→ Mature → Exit"),
]

bx_h = Inches(2.15)
bx_w = (CW - Inches(0.16) * 3) / 4
bx_y = Inches(1.95)

for i, (nm, n, detail) in enumerate(chain_packs):
    bx = M + i * (bx_w + Inches(0.16))
    d.rect(s, bx, bx_y, bx_w, bx_h, b.NAVY, radius=0.04)
    d.rect(s, bx, bx_y, bx_w, Inches(0.09), b.TEAL)
    d.text(s, n, bx + Inches(0.12), bx_y + Inches(0.08), Inches(0.55), Inches(0.62),
           size=34, color=b.GOLD, bold=True)
    d.text(s, "skills", bx + Inches(0.12), bx_y + Inches(0.72), Inches(0.55), Inches(0.24),
           size=9, color=b.MUTED)
    d.text(s, nm, bx + Inches(0.72), bx_y + Inches(0.1), bx_w - Inches(0.82), Inches(0.8),
           size=14, color=b.WHITE, bold=True, shrink=True)
    d.text(s, detail, bx + Inches(0.12), bx_y + Inches(1.07), bx_w - Inches(0.2), Inches(0.92),
           size=10, color=b.LIGHT_TEAL, shrink=True, ls=1.25)
    if i < 3:
        d.text(s, "→", bx + bx_w + Inches(0.02), bx_y + Inches(0.88), Inches(0.13), Inches(0.38),
               size=17, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)

# engagement-management band
em_y = Inches(4.38)
em_h = Inches(1.0)
d.rect(s, M, em_y, CW, em_h, b.DARK_TEAL, radius=0.03)
d.rect(s, M, em_y, CW, Inches(0.08), b.TEAL)
d.text(s, "◀  engagement-management  ·  /win-strategy  →  /commercial-structuring  →  /engagement-kickoff  →  /stakeholder-cadence  →  /progress-reporting  →  /engagement-closeout  ▶",
       M + Inches(0.2), em_y + Inches(0.1), CW - Inches(0.4), Inches(0.44),
       size=11, color=b.WHITE, bold=True, shrink=True)
d.text(s, "Cross-cutting: runs in parallel with all other packs — from first pursuit conversation to final client sign-off",
       M + Inches(0.2), em_y + Inches(0.6), CW - Inches(0.4), Inches(0.3),
       size=10.5, color=b.LIGHT_TEAL, shrink=True)

d.text(s, "Strategy outputs chain into AI Transformation  ·  AI Transformation chains into Solution Delivery  ·  Solution Delivery chains into Continuous Improvement  ·  Continuous Improvement loops back to Strategy (next cycle)",
       M, Inches(5.6), CW, Inches(0.55),
       size=10.5, color=b.MUTED, shrink=True, ls=1.2)

d.footer(s, page, TOTAL)

# ── Sections ──────────────────────────────────────────────────────────────────
for pack in PACKS:
    # Section divider
    page += 1
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), H, b.TEAL)
    d.text(s, f"SECTION {pack['section']}",
           Inches(0.36), Inches(1.05), CW, Inches(0.35),
           size=11.5, color=b.TEAL, bold=True)
    d.text(s, pack["name"],
           Inches(0.36), Inches(1.5), CW * 0.73, Inches(1.4),
           size=42, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.36), Inches(2.98), Inches(1.5), Inches(0.06), b.TEAL)
    d.text(s, pack["tagline"],
           Inches(0.36), Inches(3.16), CW * 0.72, Inches(1.15),
           size=14, color=b.LIGHT_TEAL, shrink=True, ls=1.3)

    # trigger pill
    d.rect(s, Inches(0.36), Inches(4.45), Inches(3.6), Inches(0.37), b.NAVY_2, radius=0.05)
    d.text(s, pack["trigger"],
           Inches(0.52), Inches(4.5), Inches(3.3), Inches(0.27),
           size=12.5, color=b.AMBER, bold=True)

    # chain
    d.text(s, f"⛓  {pack['chain']}",
           Inches(0.36), Inches(5.02), CW * 0.72, Inches(0.36),
           size=11.5, color=b.MUTED)

    # skill count
    d.text(s, str(pack["n_skills"]),
           W - Inches(2.85), Inches(1.5), Inches(2.5), Inches(1.9),
           size=106, color=b.GOLD, bold=True, align=PP_ALIGN.RIGHT, shrink=True)
    d.text(s, "SKILLS",
           W - Inches(2.85), Inches(3.45), Inches(2.5), Inches(0.38),
           size=12.5, color=b.MUTED, bold=True, align=PP_ALIGN.RIGHT)
    d.text(s, f"{len(pack['domains'])} domains",
           W - Inches(2.85), Inches(3.9), Inches(2.5), Inches(0.3),
           size=11.5, color=b.MUTED, align=PP_ALIGN.RIGHT)

    d.footer(s, page, TOTAL, dark=True)

    # Domain slides
    for domain in pack["domains"]:
        page += 1
        s = d.slide(fill=b.WHITE)
        d.header(s, domain["name"],
                 f"{pack['name']}  ·  {domain['sub']}")
        skill_cards(s, domain["skills"])
        d.footer(s, page, TOTAL)

# ── save + validate ───────────────────────────────────────────────────────────
d.save(str(OUT))
print(f"\n✓ Saved: {OUT}")
