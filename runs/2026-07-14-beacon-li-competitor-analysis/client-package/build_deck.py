#!/usr/bin/env python3
"""Build the client-ready Beacon.li competitor analysis PPTX.

Output:
  beacon-li-competitor-analysis-draft.pptx
"""
from pathlib import Path
import sys

SKILL_SCRIPTS = Path("/home/shekerk/content-ideas/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(SKILL_SCRIPTS))

from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR  # noqa: E402

OUT_DIR = Path(__file__).parent
OUT = OUT_DIR / "beacon-li-competitor-analysis-draft.pptx"

d = Deck(footer="Beacon.li Competitor Analysis | Public-market briefing")
b = d.b
M, CW, W, H = d.M, d.CW, d.W, d.H
TOTAL = 53


def add_footer(slide, page):
    d.footer(slide, page, TOTAL)


def cover(page):
    s = d.slide(fill=b.NAVY)
    d.rect(s, W - Inches(4.25), 0, Inches(4.25), H, b.NAVY_2)
    d.rect(s, W - Inches(4.25), 0, Inches(0.08), H, b.TEAL)
    d.text(s, "COMPETITOR ANALYSIS", M, Inches(0.92), Inches(6), Inches(0.35), size=14, color=b.TEAL, bold=True)
    d.text(s, "Beacon.li", M, Inches(1.45), Inches(7.5), Inches(0.9), size=50, color=b.WHITE, bold=True)
    d.text(s, "Where Beacon wins, where it is exposed, and how to prove the wedge", M, Inches(2.42), Inches(7.6), Inches(0.8), size=22, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, M, Inches(3.45), Inches(1.5), Inches(0.05), b.TEAL)
    d.text(s, [
        {"text": "Prepared from public company pages, pricing pages, and current market signals", "size": 14, "color": b.WHITE, "space_before": 4},
        {"text": "Client-ready briefing · July 2026", "size": 13, "color": b.MUTED, "space_before": 8},
    ], M, Inches(3.82), Inches(7.4), Inches(0.9), shrink=True)
    for i, label in enumerate(["DAP incumbents", "Implementation ops", "Enterprise AI delivery"]):
        left = M + Inches(i * 2.25)
        d.rect(s, left, Inches(6.18), Inches(2.02), Inches(0.38), b.NAVY_2, radius=0.08, line=b.TEAL)
        d.text(s, label, left + Inches(0.08), Inches(6.28), Inches(1.86), Inches(0.18), size=9.5, color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def header(title, subtitle=None):
    s = d.slide(fill=b.WHITE)
    d.header(s, title, subtitle)
    return s


def divider(page, label, title, subtitle):
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), H, b.TEAL)
    d.text(s, label, Inches(0.9), Inches(2.35), Inches(5), Inches(0.35), size=14, color=b.TEAL, bold=True)
    d.text(s, title, Inches(0.9), Inches(2.82), Inches(10.6), Inches(1.0), size=38, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.9), Inches(3.88), Inches(1.4), Inches(0.05), b.TEAL)
    d.text(s, subtitle, Inches(0.9), Inches(4.18), Inches(9.5), Inches(0.62), size=15, color=b.LIGHT_TEAL, shrink=True)
    add_footer(s, page)


def bullets(s, items, top=1.8, left=0.6, width=12.1, size=14, gap=9):
    d.text(s, [{"text": item, "bullet": True, "space_before": gap, "size": size, "color": b.INK} for item in items],
           Inches(left), Inches(top), Inches(width), Inches(5.2), shrink=True)


def card(s, left, top, width, height, title, body, accent=None):
    accent = accent or b.TEAL
    d.rect(s, Inches(left), Inches(top), Inches(width), Inches(height), b.WHITE, radius=0.06, line=b.GRID, shadow=True)
    d.rect(s, Inches(left), Inches(top), Inches(0.08), Inches(height), accent)
    d.text(s, title, Inches(left + 0.22), Inches(top + 0.18), Inches(width - 0.38), Inches(0.32), size=13.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(left + 0.22), Inches(top + 0.62), Inches(width - 0.38), Inches(height - 0.82), size=11.5, color=b.MUTED, shrink=True)


def stat_card(s, left, top, num, label, color=None):
    color = color or b.NAVY
    d.rect(s, Inches(left), Inches(top), Inches(2.65), Inches(1.1), color, radius=0.08)
    d.text(s, num, Inches(left), Inches(top + 0.15), Inches(2.65), Inches(0.4), size=25, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, label, Inches(left + 0.12), Inches(top + 0.62), Inches(2.41), Inches(0.32), size=10.5, color=b.WHITE, align=PP_ALIGN.CENTER, shrink=True)


def slide_2(page):
    s = header("The Answer", "Beacon should be positioned by the job it performs, not by an incumbent category")
    d.rect(s, M, Inches(1.78), CW, Inches(1.22), b.NAVY, radius=0.08)
    d.text(s, "Beacon is strongest as an AI implementation execution layer: configure, validate, test, sequence, and support go-lives inside the product UI.", M + Inches(0.35), Inches(1.98), CW - Inches(0.7), Inches(0.72), size=16, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    card(s, 0.75, 3.15, 3.8, 1.85, "Do not lead with", "“We are a better DAP.” That frame invites WalkMe, Pendo, Whatfix, and Appcues comparisons on their strongest ground.", b.CORAL)
    card(s, 4.78, 3.15, 3.8, 1.85, "Lead with", "“We execute implementation work.” That shifts the buyer conversation from adoption guidance to go-live throughput.", b.TEAL)
    card(s, 8.82, 3.15, 3.8, 1.85, "Prove with", "A 7-day workflow POC: baseline, Beacon execution trace, human interventions, elapsed time, errors, and hypercare load.", b.GOLD)
    add_footer(s, page)


def slide_3(page):
    s = header("The Competitive Field Splits Into Three Buckets", "Each bucket solves a real adjacent job; Beacon must be clear about which job it owns")
    card(s, 0.72, 1.9, 3.85, 3.35, "1. Digital adoption", "WalkMe, Pendo, Whatfix, Appcues\n\nGuide users, measure product behavior, improve adoption, and reduce support after or around launch.", b.TEAL)
    card(s, 4.75, 1.9, 3.85, 3.35, "2. Implementation operations", "Rocketlane, GuideCX, Arrows, Dock\n\nCoordinate onboarding projects, customer collaboration, resource planning, portals, and handoffs.", b.GOLD)
    card(s, 8.78, 1.9, 3.85, 3.35, "3. Enterprise AI delivery", "Unframe AI, UiPath, automation incumbents\n\nDeliver governed AI workflows, agent orchestration, and cross-system automation across many use cases.", b.CORAL)
    d.text(s, "Beacon's wedge: execute implementation work that other buckets mostly manage, guide, measure, or automate as fragments.", M, Inches(5.9), CW, Inches(0.56), size=13.5, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_4(page):
    s = header("Beacon's Wedge Is Implementation Execution", "The strongest claim is operational, not cosmetic")
    stat_card(s, 0.85, 1.9, "60%+", "effort / timeline reduction")
    stat_card(s, 3.75, 1.9, "85%", "faster handovers")
    stat_card(s, 6.65, 1.9, "60%", "fewer config defects")
    stat_card(s, 9.55, 1.9, "30%", "lower implementation cost")
    bullets(s, [
        "Learns product logic through the UI rather than requiring backend/API access.",
        "Builds a map of configuration logic, dependencies, and best practices.",
        "Targets configuration, validation, UAT, migration sequencing, cutover, and hypercare.",
        "Enterprise posture is now publicly evidenced: no backend/API/database access, SOC 2, RBAC, SSO, audit trails, and a public trust center.",
    ], top=3.35, size=14)
    add_footer(s, page)


def slide_5(page):
    s = header("DAP Incumbents Are The Most Visible Comparisons", "They are strong, but they solve a different primary job")
    card(s, 0.72, 1.82, 3.0, 3.0, "WalkMe / SAP", "Most dangerous incumbent. Mature enterprise trust, SAP distribution, AI assistance, cross-app context, and measurable AI ROI language.", b.TEAL)
    card(s, 3.95, 1.82, 2.75, 3.0, "Pendo", "Analytics-led product experience with free entry tier and custom paid plans.", b.GOLD)
    card(s, 6.92, 1.82, 2.75, 3.0, "Whatfix", "Enterprise DAP packaging with guidance, analytics, support, training, and deployment options.", b.GOLD)
    card(s, 9.9, 1.82, 2.75, 3.0, "Appcues", "Lighter product-led onboarding, in-app messaging, email, push, and feature adoption.", b.GOLD)
    d.rect(s, M, Inches(5.38), CW, Inches(0.72), b.SOFT, radius=0.06, line=b.GRID)
    d.text(s, "Beacon response: DAPs help users adopt software; Beacon executes the implementation work needed to get customers live.", M + Inches(0.25), Inches(5.52), CW - Inches(0.5), Inches(0.42), size=12.8, color=b.NAVY, bold=True, shrink=True)
    add_footer(s, page)


def slide_6(page):
    s = header("Implementation Ops Tools Are Adjacent", "These tools often remain systems of record, so Beacon should integrate first")
    card(s, 0.75, 1.85, 3.75, 3.4, "Rocketlane", "Strongest adjacent competitor. Public seat-based pricing and credible services operations footprint: projects, portals, resource management, financials, and revenue recognition.", b.TEAL)
    card(s, 4.8, 1.85, 3.55, 3.4, "GuideCX / Arrows / Dock", "Customer collaboration, onboarding visibility, sales/customer rooms, shared plans, and handoffs. Useful when the buyer needs transparency more than execution.", b.GOLD)
    card(s, 8.65, 1.85, 3.65, 3.4, "Beacon posture", "Be the execution layer underneath the implementation system: perform configuration, validation, exception routing, and hypercare while syncing progress back.", b.NAVY)
    d.text(s, "Integration lowers adoption risk: Beacon + Rocketlane/Jira/Salesforce is more believable than rip-and-replace.", M, Inches(5.95), CW, Inches(0.54), size=12.8, color=b.ACCENT, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_7(page):
    s = header("Enterprise AI Platforms Can Absorb The Use Case", "The broad AI-delivery threat is real")
    card(s, 0.82, 1.9, 5.2, 3.55, "Unframe AI", "Managed AI transformation and AI OS: agent orchestration, knowledge fabric, AI-native data warehouse, governance, interoperability, and production-grade workflows in days/weeks.", b.TEAL)
    card(s, 6.35, 1.9, 5.2, 3.55, "UiPath and automation incumbents", "Deep enterprise automation footprint and primitives that can automate implementation tasks if the customer has process clarity and automation talent.", b.GOLD)
    d.text(s, "Beacon's counter-position: narrower, more concrete, and easier to value when the pain is delayed go-live and services margin.", M, Inches(5.96), CW, Inches(0.54), size=12.8, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_8(page):
    s = header("Where Beacon Actually Wins", "The strongest fit is narrower than generic enterprise AI")
    rows = [
        ("Complex configurable SaaS", "High fit", b.TEAL),
        ("Repeated implementation playbooks", "High fit", b.TEAL),
        ("Revenue stuck between close and go-live", "High fit", b.TEAL),
        ("Existing project tools that only coordinate", "High fit", b.TEAL),
        ("Pure product analytics or in-app guides", "Low fit", b.CORAL),
        ("Simple customer portal / shared room", "Low fit", b.CORAL),
    ]
    top = 1.82
    for i, (need, fit, color) in enumerate(rows):
        y = top + i * 0.62
        d.rect(s, M, Inches(y), CW, Inches(0.48), b.WHITE, radius=0.04, line=b.GRID)
        d.rect(s, M, Inches(y), Inches(0.08), Inches(0.48), color)
        d.text(s, need, M + Inches(0.22), Inches(y + 0.11), Inches(7.7), Inches(0.24), size=11.8, color=b.INK, bold=True, shrink=True)
        d.text(s, fit, W - Inches(3.0), Inches(y + 0.11), Inches(2.25), Inches(0.24), size=11.8, color=color, bold=True, align=PP_ALIGN.RIGHT)
    d.text(s, "Rule of thumb: if the buyer needs implementation labor reduced, Beacon belongs in the conversation. If the buyer needs adoption content or project visibility, an incumbent may be cleaner.", M, Inches(6.02), CW, Inches(0.58), size=11.5, color=b.MUTED, italic=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_9(page):
    s = header("Unofficial Quadrant View", "Beacon is a visionary in implementation execution; incumbents lead on enterprise credibility")
    left, top, width, height = Inches(1.25), Inches(1.82), Inches(10.4), Inches(4.55)
    d.rect(s, left, top, width, height, b.SOFT, line=b.GRID)
    d.rect(s, left + width/2, top, Inches(0.02), height, b.GRID)
    d.rect(s, left, top + height/2, width, Inches(0.02), b.GRID)
    d.text(s, "Enterprise adoption credibility", Inches(0.48), Inches(3.1), Inches(0.35), Inches(1.3), size=10, color=b.MUTED, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "Implementation execution depth", Inches(4.4), Inches(6.58), Inches(4.2), Inches(0.24), size=10, color=b.MUTED, bold=True, align=PP_ALIGN.CENTER)
    points = [
        ("WalkMe/SAP", 0.62, 0.78, b.NAVY),
        ("UiPath", 0.72, 0.70, b.NAVY),
        ("Beacon.li", 0.82, 0.54, b.TEAL),
        ("Unframe", 0.70, 0.58, b.TEAL),
        ("Rocketlane", 0.48, 0.60, b.GOLD),
        ("Pendo/Whatfix", 0.38, 0.66, b.GOLD),
        ("Arrows/Dock", 0.28, 0.34, b.MUTED),
    ]
    for name, x, y, color in points:
        px = left + int(width * x)
        py = top + int(height * (1-y))
        d.rect(s, px - Inches(0.06), py - Inches(0.06), Inches(0.12), Inches(0.12), color, radius=0.05)
        d.text(s, name, px + Inches(0.08), py - Inches(0.09), Inches(1.55), Inches(0.18), size=8.6, color=b.INK, bold=True, shrink=True)
    add_footer(s, page)


def slide_10(page):
    s = header("Pricing And Funding Signals", "Beacon has to overcome opacity with fast proof")
    card(s, 0.75, 1.85, 3.75, 3.35, "Transparent anchor", "Rocketlane publishes seat-based pricing, creating a concrete budget anchor for implementation operations.", b.GOLD)
    card(s, 4.82, 1.85, 3.75, 3.35, "Enterprise custom zone", "Beacon, WalkMe, Whatfix, Unframe, and broad automation vendors are mostly quote-led or enterprise-custom.", b.TEAL)
    card(s, 8.9, 1.85, 3.25, 3.35, "Capital signal", "Unframe and Rocketlane show strong 2026 funding momentum; WalkMe has SAP balance-sheet power.", b.NAVY)
    d.text(s, "Commercial implication: make value visible before price negotiation by showing implementation work removed in a workflow POC.", M, Inches(5.88), CW, Inches(0.58), size=12.6, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_11(page):
    s = header("The Pressure Test", "The claims that will get challenged first")
    card(s, 0.75, 1.85, 3.75, 3.65, "Weakest claim", "“The knowledge graph compounds.” This needs longitudinal proof that later implementations are faster or safer because of platform learning.", b.CORAL)
    card(s, 4.82, 1.85, 3.75, 3.65, "Sharpest objection", "“Is this just another coordination layer?” The answer has to be a live workflow execution trace, not a narrated demo.", b.GOLD)
    card(s, 8.9, 1.85, 3.25, 3.65, "Biggest risk", "Incumbents can reframe Beacon as a feature unless Beacon owns execution, auditability, and implementation-specific learning.", b.NAVY)
    add_footer(s, page)


def slide_12(page):
    s = header("Recommended Positioning", "Use precise category language")
    d.rect(s, M, Inches(1.85), CW, Inches(1.02), b.NAVY, radius=0.08)
    d.text(s, "Beacon executes implementation work. DAPs guide adoption. Onboarding tools coordinate delivery. RPA automates fragments. Broad AI platforms transform many workflows.", M + Inches(0.25), Inches(2.03), CW - Inches(0.5), Inches(0.56), size=13.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    bullets(s, [
        "Lead with implementation execution and revenue acceleration, not generic AI automation.",
        "Compare by workflow job: coordinate, guide, measure, automate fragments, or execute the implementation.",
        "Show Beacon alongside existing project systems as the execution layer, not a forced replacement.",
        "Make every sales conversation culminate in a real 7-day POC scorecard.",
    ], top=3.05, size=14.2)
    add_footer(s, page)


def slide_13(page):
    s = header("What To Build Next", "The fastest route to defensible differentiation")
    card(s, 0.72, 1.78, 3.78, 3.55, "1. POC scorecard", "Baseline time, Beacon time, interventions, errors, audit trail, and hypercare tickets. Turn every trial into evidence.", b.TEAL)
    card(s, 4.78, 1.78, 3.78, 3.55, "2. Competitor matrix", "Columns should show who coordinates, guides, measures, automates fragments, and executes full implementation work.", b.GOLD)
    card(s, 8.85, 1.78, 3.78, 3.55, "3. Compounding proof", "Publish evidence that implementation 50 is faster and less risky than implementation 5 because the system learned.", b.NAVY)
    add_footer(s, page)


def slide_14(page):
    s = d.slide(fill=b.NAVY)
    d.text(s, "Next Move", M, Inches(0.95), Inches(5), Inches(0.4), size=15, color=b.TEAL, bold=True)
    d.text(s, "Prove the wedge on one real implementation workflow", M, Inches(1.5), Inches(9.8), Inches(0.9), size=36, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, M, Inches(2.55), Inches(1.5), Inches(0.05), b.TEAL)
    d.text(s, [
        {"text": "Pick one workflow from an active implementation pipeline.", "bullet": True, "size": 16, "color": b.LIGHT_TEAL, "space_before": 12},
        {"text": "Run Beacon against the workflow in a 7-day POC.", "bullet": True, "size": 16, "color": b.LIGHT_TEAL, "space_before": 12},
        {"text": "Compare baseline vs execution trace, intervention count, elapsed time, error rate, and hypercare load.", "bullet": True, "size": 16, "color": b.LIGHT_TEAL, "space_before": 12},
    ], M, Inches(3.05), Inches(10.2), Inches(2.1), shrink=True)
    d.text(s, "Decision: invest in the category only after workflow-level proof, not after a generic platform demo.", M, Inches(6.1), Inches(10.8), Inches(0.38), size=15, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def simple_cards_slide(page, title, subtitle, cards):
    s = header(title, subtitle)
    positions = [(0.72, 1.82), (4.72, 1.82), (8.72, 1.82), (0.72, 4.36), (4.72, 4.36), (8.72, 4.36)]
    colors = [b.TEAL, b.GOLD, b.CORAL, b.NAVY, b.TEAL, b.GOLD]
    for idx, item in enumerate(cards[:6]):
        x, y = positions[idx]
        card(s, x, y, 3.55, 1.78, item[0], item[1], colors[idx])
    add_footer(s, page)


def competitor_profile(page, name, category, why_it_matters, beacon_angle, risk, accent=None):
    accent = accent or b.TEAL
    s = header(name, category)
    d.rect(s, M, Inches(1.76), CW, Inches(1.02), b.NAVY, radius=0.08)
    d.text(s, why_it_matters, M + Inches(0.28), Inches(1.94), CW - Inches(0.56), Inches(0.56), size=12.8, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    card(s, 0.82, 2.95, 5.25, 2.25, "Beacon's winning angle", beacon_angle, accent)
    card(s, 6.42, 2.95, 5.25, 2.25, "Competitive risk", risk, b.CORAL)
    add_footer(s, page)


def slide_15(page):
    simple_cards_slide(page, "Digital Adoption: What Buyers Actually Buy", "DAP tools are mature because they map to a well-understood adoption problem", [
        ("Buyer job", "Guide users, reduce support, improve training, and measure adoption after or around launch."),
        ("Primary budget owner", "Product, IT, digital transformation, customer success, or employee experience."),
        ("Strength", "Mature enterprise trust, review surfaces, integration depth, and established buying categories."),
        ("Weakness vs Beacon", "They usually do not perform the implementation's configuration, migration, validation, or cutover work."),
        ("Beacon move", "Do not attack guidance. Reframe the problem as pre-go-live execution."),
        ("Likely objection", "“We already have a DAP.” Answer: Beacon is not adoption content; it is implementation work removal."),
    ])


def slide_16(page):
    competitor_profile(page, "WalkMe / SAP", "Digital adoption incumbent",
                       "Most dangerous incumbent: SAP distribution, AI-assistance positioning, cross-application context, and enterprise trust.",
                       "Beacon is narrower and more implementation-specific: configuration, validation, UAT, migration sequencing, and hypercare before or around go-live.",
                       "WalkMe can move upstream from adoption into implementation workflows and bundle through SAP transformation programs.",
                       b.TEAL)


def slide_17(page):
    simple_cards_slide(page, "Pendo, Whatfix, And Appcues", "Strong products, different center of gravity", [
        ("Pendo", "Product analytics, in-app guides, sentiment, replay, orchestration, and free entry tier."),
        ("Whatfix", "Enterprise DAP with guidance, analytics, training, support, and broad deployment options."),
        ("Appcues", "Lighter customer-facing product onboarding, messaging, email, push, and feature adoption."),
        ("Beacon advantage", "Implementation labor reduction is a stronger economic claim than adoption content when go-live is delayed."),
        ("Beacon risk", "Product teams may understand and budget these tools faster than a new implementation-execution category."),
        ("Sales language", "“Keep adoption tools. Use Beacon to get customers live faster before adoption becomes the problem.”"),
    ])


def slide_18(page):
    simple_cards_slide(page, "Implementation Operations", "These tools own the project layer around Beacon's execution wedge", [
        ("Buyer job", "Coordinate customer onboarding, implementation tasks, timelines, resources, and stakeholder accountability."),
        ("Primary budget owner", "Professional services, implementation, customer success operations, and RevOps."),
        ("Strength", "They are already in the delivery workflow and may hold project, resource, and revenue-recognition context."),
        ("Weakness vs Beacon", "They manage work but generally still require humans to perform configuration, validation, and exception handling."),
        ("Beacon move", "Integrate first. Become the execution layer below the project system."),
        ("Likely objection", "“Will this replace our project system?” Answer: no, it executes work and reports progress back."),
    ])


def slide_19(page):
    competitor_profile(page, "Rocketlane", "Customer onboarding / PSA",
                       "Strongest adjacent implementation-operations vendor: project collaboration, portals, resource management, financials, revenue recognition, and public seat pricing.",
                       "Beacon should sit under Rocketlane as the worker layer: execute configuration, validation, exception routing, and hypercare while Rocketlane remains the operating view.",
                       "Rocketlane can add AI agents for repeatable services work and defend the implementation operations budget.",
                       b.GOLD)


def slide_20(page):
    simple_cards_slide(page, "GuideCX, Arrows, And Dock", "Collaboration tools win when the buyer wants visibility more than automation", [
        ("GuideCX", "Implementation management and customer accountability."),
        ("Arrows", "HubSpot-oriented sales rooms and onboarding plans; pricing based on team size and use case."),
        ("Dock", "Client-facing workspaces for sales, onboarding, and customer collaboration."),
        ("Beacon advantage", "Deeper for complex configuration, validation, UAT, and migration workflows."),
        ("Beacon risk", "Overkill when the real pain is scattered customer communication."),
        ("Sales language", "“Use customer rooms for alignment. Use Beacon for the work that blocks go-live.”"),
    ])


def slide_21(page):
    simple_cards_slide(page, "Enterprise AI Delivery: Broad Platform Threat", "These vendors can package implementation as one AI-transformation use case", [
        ("Buyer job", "Move from AI experiments to governed production workflows across the enterprise."),
        ("Primary budget owner", "CIO, transformation, data/AI, operations, and business function leaders."),
        ("Strength", "Broad scope, governance language, integrations, and ability to sell multiple use cases."),
        ("Weakness vs Beacon", "Less focused on enterprise SaaS implementation economics and post-sales delivery bottlenecks."),
        ("Beacon move", "Win by being narrower, faster to prove, and closer to revenue recognition."),
        ("Likely objection", "“Can our AI transformation partner build this?” Answer with implementation-specific data and speed."),
    ])


def slide_22(page):
    competitor_profile(page, "Unframe AI", "Managed enterprise AI delivery",
                       "Closest broad AI peer: managed AI transformation, agent orchestrator, knowledge fabric, AI-native data warehouse, governance, and production-grade workflows.",
                       "Beacon is more verticalized around SaaS implementation execution and easier to value when go-live delay is the business pain.",
                       "Unframe can sell implementation as one managed AI use case inside a broader enterprise AI program.",
                       b.TEAL)


def slide_23(page):
    competitor_profile(page, "UiPath And Automation Incumbents", "RPA / agentic automation",
                       "Deep enterprise automation footprint and budget access; capable of automating implementation fragments with enough configuration.",
                       "Beacon avoids custom bot-building by owning the implementation domain model, execution logic, and workflow-specific evidence.",
                       "Automation incumbents can bundle primitives into enterprise agreements and argue Beacon is a workflow built on top of their category.",
                       b.NAVY)


def slide_24(page):
    s = header("Pricing Implications", "Opaque enterprise pricing needs a stronger proof mechanism")
    simple_rows = [
        ("Transparent anchor", "Rocketlane publishes seat-based pricing, so it becomes a concrete budget comparison."),
        ("Custom-pricing zone", "Beacon, WalkMe, Whatfix, Unframe, and automation platforms are mostly quote-led."),
        ("Pricing risk", "Buyers may struggle to benchmark value if pricing is not tied to delivery impact."),
        ("Recommended posture", "Tie value to throughput, revenue acceleration, and services effort removed."),
        ("Best proof", "POC scorecard before pricing negotiation."),
    ]
    for i, (left_label, body) in enumerate(simple_rows):
        y = 1.82 + i * 0.78
        d.rect(s, M, Inches(y), CW, Inches(0.58), b.WHITE, radius=0.04, line=b.GRID)
        d.rect(s, M, Inches(y), Inches(0.08), Inches(0.58), b.TEAL if i % 2 == 0 else b.GOLD)
        d.text(s, left_label, M + Inches(0.22), Inches(y + 0.14), Inches(2.75), Inches(0.2), size=12.5, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, M + Inches(3.15), Inches(y + 0.08), Inches(8.55), Inches(0.38), size=10.2, color=b.MUTED, shrink=True)
    add_footer(s, page)


def slide_25(page):
    s = header("Funding And Market Momentum", "Capital is flowing to AI delivery and implementation operations")
    card(s, 0.75, 1.85, 3.75, 3.45, "WalkMe / SAP", "Acquired by SAP for $1.5B in 2024. Treat as an incumbent platform asset, not a standalone startup.", b.NAVY)
    card(s, 4.82, 1.85, 3.75, 3.45, "Unframe AI", "Reported $50M Series B in 2026, $100M total funding, and broad enterprise AI delivery positioning.", b.TEAL)
    card(s, 8.9, 1.85, 3.25, 3.45, "Rocketlane", "Reported $60M Series C in 2026 and $105M total funding, with AI services-work automation momentum.", b.GOLD)
    d.text(s, "Market implication: Beacon's category is timely, but stronger-funded adjacent vendors can crowd the narrative unless Beacon proves a narrower workflow wedge.", M, Inches(5.92), CW, Inches(0.58), size=11.8, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_26(page):
    simple_cards_slide(page, "SWOT Summary", "Beacon's opportunity is specific and valuable, but proof matters", [
        ("Strength", "Clear pain: delayed go-lives defer revenue recognition and increase delivery cost."),
        ("Strength", "UI-level learning and no-backend-access reduce adoption friction if technically reliable."),
        ("Weakness", "Public proof is mostly vendor-published and the category is new."),
        ("Weakness", "Knowledge-graph compounding is a moat claim that needs longitudinal evidence."),
        ("Opportunity", "Own implementation execution before DAP, onboarding, and automation vendors converge."),
        ("Threat", "SAP/WalkMe, Rocketlane, Unframe, and RPA incumbents can each attack from an adjacent budget."),
    ])


def slide_27(page):
    simple_cards_slide(page, "White Space To Own", "The most defensible space is where implementation knowledge becomes execution", [
        ("Execution layer", "A platform that performs configuration, validation, migration sequencing, UAT, cutover, and hypercare."),
        ("Knowledge graph", "A system that preserves implementation decisions, exceptions, and resolutions across deployments."),
        ("Audit-ready AI", "Every implementation action should explain what happened, why, under what permissions, and who approved it."),
        ("Services margin", "Beacon should connect its value to delivery capacity, consultant leverage, and lower hypercare burden."),
        ("Revenue acceleration", "The buyer cares about realized revenue, not just delivery productivity."),
        ("Category language", "Implementation execution is sharper than AI orchestration when speaking to post-sales leaders."),
    ])


def slide_28(page):
    s = header("The POC Scorecard", "Turn every sales trial into proof")
    cols = [("Baseline", b.CORAL), ("Beacon", b.TEAL), ("Decision", b.GOLD)]
    for i, (title, color) in enumerate(cols):
        x = 0.75 + i * 4.02
        d.rect(s, Inches(x), Inches(1.9), Inches(3.62), Inches(0.52), color, radius=0.04)
        d.text(s, title, Inches(x + 0.12), Inches(2.07), Inches(3.38), Inches(0.16), size=10.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    rows = [
        ("Manual elapsed time", "Beacon elapsed time", "Cycle-time compression"),
        ("Human touches", "Human interventions", "Labor removed"),
        ("Known errors", "Execution errors", "Quality delta"),
        ("Support tickets", "Hypercare load", "Post-go-live impact"),
        ("No clear trace", "Action log", "Enterprise trust"),
    ]
    for r, row in enumerate(rows):
        y = 2.62 + r * 0.58
        for c, text in enumerate(row):
            x = 0.75 + c * 4.02
            d.rect(s, Inches(x), Inches(y), Inches(3.62), Inches(0.43), b.WHITE, line=b.GRID)
            d.text(s, text, Inches(x + 0.12), Inches(y + 0.09), Inches(3.38), Inches(0.24), size=9.6, color=b.INK, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "Best next move: run the POC on one active implementation workflow and use this scorecard to decide whether Beacon owns the category.", M, Inches(6.15), CW, Inches(0.58), size=11.8, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_29(page):
    simple_cards_slide(page, "Buyer And Budget Map", "Beacon must sell across the post-sales operating model, not only to AI sponsors", [
        ("Economic buyer", "CRO, COO, Chief Customer Officer, or services leader when delayed go-lives affect revenue recognition and margin."),
        ("Functional owner", "Implementation, professional services, customer onboarding, or CS operations teams that own delivery throughput."),
        ("Technical approver", "CIO, CISO, IT, enterprise architecture, and product teams reviewing UI access, model policy, audit, and RBAC."),
        ("Budget source", "Services transformation, post-sales productivity, revenue acceleration, AI transformation, or implementation tooling."),
        ("Buying trigger", "Backlog growth, delayed go-lives, implementation margin pressure, repeated configuration work, or failed automation pilots."),
        ("Procurement friction", "Autonomous execution, customer data boundaries, proof quality, opaque pricing, and overlap with existing systems."),
    ])


def slide_30(page):
    s = header("Implementation Workflow Anatomy", "Beacon needs to show exactly where it removes work")
    steps = [
        ("1", "Requirements", "Capture customer-specific rules, data, roles, and edge cases."),
        ("2", "Configuration", "Translate requirements into product settings and dependencies."),
        ("3", "Migration", "Sequence data, mappings, validation, and exception handling."),
        ("4", "Testing", "Run UAT scenarios and compare expected vs actual outcomes."),
        ("5", "Cutover", "Coordinate go-live readiness, approvals, and rollback posture."),
        ("6", "Hypercare", "Triage defects, support questions, and adoption blockers."),
    ]
    for i, (num, title, body) in enumerate(steps):
        x = 0.75 + (i % 3) * 4.02
        y = 1.78 + (i // 3) * 2.15
        d.rect(s, Inches(x), Inches(y), Inches(3.62), Inches(1.55), b.WHITE, radius=0.06, line=b.GRID, shadow=True)
        d.rect(s, Inches(x), Inches(y), Inches(0.42), Inches(1.55), b.TEAL if i in [1, 3, 5] else b.GOLD)
        d.text(s, num, Inches(x + 0.08), Inches(y + 0.52), Inches(0.26), Inches(0.26), size=13, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, title, Inches(x + 0.62), Inches(y + 0.18), Inches(2.78), Inches(0.28), size=12.6, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, Inches(x + 0.62), Inches(y + 0.56), Inches(2.78), Inches(0.76), size=9.8, color=b.MUTED, shrink=True)
    d.text(s, "Beacon should anchor demos to one named workflow across these steps, then measure labor removed and risk reduced.", M, Inches(6.18), CW, Inches(0.38), size=11.4, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_31(page):
    s = header("Competitive Evaluation Rubric", "Use the same criteria across every vendor conversation")
    rows = [
        ("Execution depth", "Does the tool perform implementation work, or only guide/manage/measure it?"),
        ("Enterprise trust", "Security posture, auditability, RBAC, deployment flexibility, procurement fit."),
        ("System-of-record fit", "Can it integrate with project, CRM, ticketing, and PSA systems already in use?"),
        ("Proof quality", "Independent validation, customer references, before/after metrics, repeatability."),
        ("Category clarity", "Can the buyer explain what budget and job the tool owns?"),
        ("Compounding advantage", "Does it learn reusable implementation logic across deployments?"),
    ]
    for i, (criterion, question) in enumerate(rows):
        y = 1.78 + i * 0.68
        d.rect(s, M, Inches(y), CW, Inches(0.52), b.WHITE, radius=0.04, line=b.GRID)
        d.rect(s, M, Inches(y), Inches(0.08), Inches(0.52), b.TEAL if i < 3 else b.GOLD)
        d.text(s, criterion, M + Inches(0.22), Inches(y + 0.13), Inches(3.05), Inches(0.22), size=11.5, color=b.NAVY, bold=True, shrink=True)
        d.text(s, question, M + Inches(3.45), Inches(y + 0.09), Inches(8.35), Inches(0.32), size=10.2, color=b.MUTED, shrink=True)
    d.text(s, "Skeptical read: Beacon is high on execution depth, medium on enterprise proof, and currently exposed on independent validation.", M, Inches(6.18), CW, Inches(0.38), size=11.5, color=b.CORAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_32(page):
    s = header("Job-To-Be-Done Matrix", "This is the cleanest way to avoid category confusion")
    cols = ["Job", "Best-fit category", "Beacon posture"]
    x_positions = [0.75, 3.55, 7.0]
    widths = [2.55, 3.15, 5.05]
    for i, col in enumerate(cols):
        d.rect(s, Inches(x_positions[i]), Inches(1.75), Inches(widths[i]), Inches(0.5), b.NAVY, radius=0.04)
        d.text(s, col, Inches(x_positions[i] + 0.1), Inches(1.91), Inches(widths[i] - 0.2), Inches(0.16), size=10.8, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    rows = [
        ("Guide users in-product", "DAP", "Do not compete head-on unless implementation work is involved."),
        ("Measure product behavior", "Pendo / PX", "Not Beacon's core wedge."),
        ("Coordinate onboarding", "Rocketlane / GuideCX", "Integrate and report progress back."),
        ("Host customer workspace", "Dock / Arrows", "Use alongside Beacon for communication."),
        ("Automate generic workflows", "UiPath / AI platform", "Win on implementation-specific domain model."),
        ("Execute implementation", "Beacon", "Own this job and prove it workflow by workflow."),
    ]
    for r, row in enumerate(rows):
        y = 2.36 + r * 0.58
        for c, text in enumerate(row):
            d.rect(s, Inches(x_positions[c]), Inches(y), Inches(widths[c]), Inches(0.43), b.WHITE, line=b.GRID)
            d.text(s, text, Inches(x_positions[c] + 0.1), Inches(y + 0.08), Inches(widths[c] - 0.2), Inches(0.26), size=8.9, color=b.INK if c == 0 else b.MUTED, bold=(c == 0), shrink=True)
    add_footer(s, page)


def battlecard(page, competitor, category, when_seen, displace, coexist, traps, proof):
    s = header(f"Battlecard: {competitor}", category)
    card(s, 0.72, 1.75, 3.75, 1.62, "When it appears", when_seen, b.GOLD)
    card(s, 4.78, 1.75, 3.75, 1.62, "Displace only when", displace, b.TEAL)
    card(s, 8.85, 1.75, 3.75, 1.62, "Coexist when", coexist, b.NAVY)
    card(s, 0.72, 3.75, 5.75, 1.8, "Trap to avoid", traps, b.CORAL)
    card(s, 6.85, 3.75, 5.75, 1.8, "Proof that wins", proof, b.TEAL)
    add_footer(s, page)


def slide_33(page):
    battlecard(page, "WalkMe / SAP", "Digital adoption incumbent",
               "Enterprise buyer frames the problem as adoption, training, employee productivity, or AI ROI across applications.",
               "The blocker is pre-go-live implementation execution, not post-launch guidance.",
               "WalkMe remains the adoption layer while Beacon executes setup, validation, and hypercare workflows.",
               "Do not say Beacon replaces WalkMe broadly; that invites an enterprise maturity comparison Beacon may lose.",
               "A workflow trace showing Beacon performs configuration and UAT work that WalkMe would only guide or support.")


def slide_34(page):
    battlecard(page, "Rocketlane", "Implementation operations / PSA",
               "Professional services wants project visibility, customer collaboration, resource planning, or revenue operations.",
               "Manual delivery work remains the constraint after the project system is already in place.",
               "Rocketlane remains the operating layer; Beacon becomes the work-execution layer underneath it.",
               "Do not argue against project management. The buyer likely needs it and may already own it.",
               "Before/after evidence that Beacon reduces human touches, errors, and elapsed time inside active implementation tasks.")


def slide_35(page):
    battlecard(page, "Unframe AI", "Managed enterprise AI delivery",
               "CIO or transformation buyer wants broad governed AI workflows across the enterprise.",
               "The buyer's urgent pain is enterprise SaaS go-live velocity and services margin, not generic AI transformation.",
               "Unframe handles broader AI roadmap; Beacon owns the vertical implementation execution use case.",
               "Do not compete on breadth. Compete on implementation specificity and time-to-proof.",
               "A 7-day POC against a named implementation workflow with a clear revenue/margin value case.")


def slide_36(page):
    battlecard(page, "UiPath / Automation Incumbents", "RPA and agentic automation",
               "Operations or IT already has automation budget, internal bot builders, or enterprise automation contracts.",
               "Generic automation requires too much custom process mapping for repeated implementation workflows.",
               "UiPath automates horizontal tasks; Beacon manages implementation-specific logic, exceptions, and audit trails.",
               "Do not frame the wedge as browser automation alone. That is commoditizable.",
               "Show reusable implementation logic, permission-aware execution, and compounding workflow knowledge.")


def slide_37(page):
    s = header("Objection Handling", "Prepare sales for the questions that will decide credibility")
    objections = [
        ("We already have WalkMe/Pendo.", "Keep it. Beacon addresses implementation execution before adoption analytics becomes useful."),
        ("We already use Rocketlane/Jira.", "Good. Beacon should execute work and sync progress into the system of record."),
        ("Could our AI team build this?", "They can build fragments; Beacon must prove domain-specific workflow learning and speed."),
        ("Is autonomous configuration safe?", "Use audit logs, inherited RBAC, approval gates, and scoped POC execution."),
        ("Where is independent proof?", "Acknowledge the gap; offer buyer-specific POC metrics and customer references when available."),
        ("How do we budget it?", "Tie price discussion to revenue pull-forward, consultant leverage, and hypercare reduction."),
    ]
    for i, (obj, answer) in enumerate(objections):
        y = 1.72 + i * 0.68
        d.rect(s, M, Inches(y), CW, Inches(0.52), b.WHITE, radius=0.04, line=b.GRID)
        d.rect(s, M, Inches(y), Inches(0.08), Inches(0.52), b.CORAL)
        d.text(s, obj, M + Inches(0.22), Inches(y + 0.12), Inches(3.7), Inches(0.22), size=10.6, color=b.NAVY, bold=True, shrink=True)
        d.text(s, answer, M + Inches(4.1), Inches(y + 0.08), Inches(7.7), Inches(0.32), size=9.4, color=b.MUTED, shrink=True)
    add_footer(s, page)


def slide_38(page):
    s = header("Messaging House", "A client-ready way to make the positioning repeatable")
    d.rect(s, M, Inches(1.68), CW, Inches(0.72), b.NAVY, radius=0.06)
    d.text(s, "Beacon executes implementation work for complex enterprise SaaS go-lives.", M + Inches(0.25), Inches(1.9), CW - Inches(0.5), Inches(0.22), size=13.2, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    pillars = [
        ("Faster revenue", "Compress signature-to-go-live time."),
        ("Lower services cost", "Reduce repeated manual delivery work."),
        ("Safer execution", "Use scoped access, approvals, and audit trails."),
        ("Compounding knowledge", "Reuse implementation exceptions and fixes."),
    ]
    for i, (title, body) in enumerate(pillars):
        x = 0.72 + (i % 2) * 6.15
        y = 2.78 + (i // 2) * 1.72
        card(s, x, y, 5.65, 1.26, title, body, b.TEAL if i % 2 == 0 else b.GOLD)
    d.text(s, "Avoid: “better DAP,” “AI project manager,” or “generic automation.” Those labels dilute the wedge.", M, Inches(6.18), CW, Inches(0.36), size=11.4, color=b.CORAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_39(page):
    s = header("Reference Integration Architecture", "Beacon should reduce replacement fear")
    layers = [
        ("Systems of record", "CRM, PSA, project management, ticketing, data migration tools", b.NAVY),
        ("Beacon execution layer", "Configuration, validation, UAT, migration sequencing, cutover, hypercare", b.TEAL),
        ("Governance layer", "RBAC, approvals, audit logs, model policy, data boundaries", b.GOLD),
        ("Experience layer", "DAP guidance, customer portal, collaboration room, executive reporting", b.CORAL),
    ]
    for i, (title, body, color) in enumerate(layers):
        y = 1.78 + i * 1.08
        d.rect(s, Inches(1.25), Inches(y), Inches(10.8), Inches(0.76), b.WHITE, radius=0.05, line=b.GRID, shadow=True)
        d.rect(s, Inches(1.25), Inches(y), Inches(0.12), Inches(0.76), color)
        d.text(s, title, Inches(1.58), Inches(y + 0.14), Inches(2.6), Inches(0.2), size=11.4, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, Inches(4.35), Inches(y + 0.12), Inches(7.3), Inches(0.3), size=10.0, color=b.MUTED, shrink=True)
    d.text(s, "Positioning implication: Beacon does not need to replace the stack. It needs to become the trusted execution layer inside it.", M, Inches(6.15), CW, Inches(0.38), size=11.5, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_40(page):
    s = header("ROI Model Framework", "Tie the business case to implementation economics")
    rows = [
        ("Revenue pull-forward", "Days from signature to go-live", "ARR activated earlier"),
        ("Services leverage", "Consultant hours per implementation", "More projects per team"),
        ("Quality", "Configuration defects and UAT failures", "Lower rework and escalation"),
        ("Hypercare", "Tickets and support hours after go-live", "Lower post-launch burden"),
        ("Capacity", "Implementation backlog and cycle time", "More customers live per quarter"),
        ("Risk", "Audit trail completeness and approval coverage", "Procurement and CISO confidence"),
    ]
    for i, (driver, metric, value) in enumerate(rows):
        y = 1.72 + i * 0.67
        d.rect(s, M, Inches(y), CW, Inches(0.52), b.WHITE, radius=0.04, line=b.GRID)
        d.rect(s, M, Inches(y), Inches(0.08), Inches(0.52), b.TEAL if i % 2 == 0 else b.GOLD)
        d.text(s, driver, M + Inches(0.2), Inches(y + 0.12), Inches(2.5), Inches(0.22), size=10.5, color=b.NAVY, bold=True, shrink=True)
        d.text(s, metric, M + Inches(3.05), Inches(y + 0.08), Inches(4.3), Inches(0.32), size=9.4, color=b.MUTED, shrink=True)
        d.text(s, value, M + Inches(7.75), Inches(y + 0.08), Inches(4.0), Inches(0.32), size=9.4, color=b.INK, bold=True, shrink=True)
    add_footer(s, page)


def slide_41(page):
    s = header("30 / 60 / 90 Day Action Plan", "Turn the analysis into operating motion")
    card(s, 0.72, 1.78, 3.75, 3.55, "First 30 days", "Finalize category language; build battlecards; define POC scorecard; pick 2-3 integration targets; collect current sales objections.", b.TEAL)
    card(s, 4.78, 1.78, 3.75, 3.55, "Next 60 days", "Run workflow POCs; publish before/after evidence; produce ROI calculator; build reference architecture; tighten security narrative.", b.GOLD)
    card(s, 8.85, 1.78, 3.75, 3.55, "Next 90 days", "Package proof into sales assets; validate compounding claims; create customer reference motion; decide category investment level.", b.NAVY)
    d.text(s, "Decision gate: continue category-building only if POCs show measurable cycle-time, labor, quality, or hypercare improvement.", M, Inches(5.95), CW, Inches(0.58), size=11.8, color=b.CORAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_42(page):
    s = header("Source Confidence And Gaps", "Separate sourced facts from strategic inference")
    card(s, 0.72, 1.78, 3.75, 3.35, "High confidence", "455 Level 2 evidence rows; official trust/security pages; public competitor positioning; Beacon-owned case/product claims; primary consulting/analyst evidence where available.", b.TEAL)
    card(s, 4.78, 1.78, 3.75, 3.35, "Medium confidence", "Strategic category interpretation, fit scoring, grouped-vendor scoring rows, quadrant placement, likely buyer objections, and competitive response paths.", b.GOLD)
    card(s, 8.85, 1.78, 3.75, 3.35, "Open gaps", "Beacon baseline denominators; independent Beacon performance proof; actual win/loss notes; Beacon public pricing; named partner depth; longitudinal knowledge-graph compounding evidence.", b.CORAL)
    d.text(s, "Client use: treat this as a source-backed strategy briefing plus explicit hypotheses to validate in live sales and customer proof cycles.", M, Inches(5.85), CW, Inches(0.72), size=12.0, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_43(page):
    divider(page, "CONSULTING THREAT", "AI Transformation Consultancies", "Accenture, BCG, McKinsey, Deloitte, IBM, and Capgemini validate the market but raise the bar for proof.")


def slide_44(page):
    s = header("What Consultancies Are Really Selling", "The common thesis: AI value is operating-model execution, not model access")
    card(s, 0.72, 1.78, 3.75, 3.55, "Strategy and sponsorship", "C-suite alignment, transformation roadmap, use-case prioritization, board narrative, and operating-model choices.", b.NAVY)
    card(s, 4.78, 1.78, 3.75, 3.55, "Delivery machinery", "Data readiness, workflow redesign, governance, change management, integration, training, and managed execution.", b.TEAL)
    card(s, 8.85, 1.78, 3.75, 3.55, "Value realization", "ROI tracking, adoption, benefit capture, outcome pricing, and proof that pilots scale into enterprise value.", b.GOLD)
    d.text(s, "Implication: Beacon should not compete with strategy decks. It should own the repeatable execution layer that turns transformation intent into completed work.", M, Inches(5.95), CW, Inches(0.58), size=11.8, color=b.CORAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_45(page):
    simple_cards_slide(page, "Consulting Firm Archetypes", "Each firm creates a different competitive pressure and partnership path", [
        ("Accenture", "Scale and reinvention. Most dangerous services-scale threat; potential channel if Beacon becomes an execution asset."),
        ("BCG / BCG X", "Value capture and 10-20-70 change logic. Beacon must prove it operationalizes the people/process 70."),
        ("McKinsey / QuantumBlack", "Rewired operating model and C-suite authority. Beacon should sit below strategy as execution telemetry."),
        ("Deloitte", "Trustworthy AI, governance, risk, and adoption. Beacon must lead with controls and evidence."),
        ("IBM Consulting", "watsonx, Consulting Advantage, hybrid-cloud delivery. Beacon competes when SaaS implementation is too domain-specific."),
        ("Capgemini", "Industrialized AI delivery and engineering scale. Beacon must win through productized repeatability."),
    ])


def slide_46(page):
    s = header("STORM Synthesis", "Five independent lenses converged on the same strategic gap")
    rows = [
        ("Practitioner", "The gap is workflow embedding and repeatable implementation, not AI awareness."),
        ("Academic", "Evidence supports operating-model change; Beacon needs before/after workflow proof."),
        ("Skeptic", "Consultancies and generic agents can absorb Beacon unless the proof is domain-specific and audit-grade."),
        ("Economist", "Budgets are shifting to AI delivery, value tracking, and outcome accountability."),
        ("Historian", "ERP, cloud, RPA, and DAP history: durable software productizes repeated services labor."),
    ]
    for i, (lens, finding) in enumerate(rows):
        y = 1.78 + i * 0.82
        d.rect(s, M, Inches(y), CW, Inches(0.62), b.WHITE, radius=0.04, line=b.GRID)
        d.rect(s, M, Inches(y), Inches(0.08), Inches(0.62), [b.TEAL, b.GOLD, b.CORAL, b.NAVY, b.TEAL][i])
        d.text(s, lens, M + Inches(0.22), Inches(y + 0.17), Inches(2.0), Inches(0.22), size=11.2, color=b.NAVY, bold=True, shrink=True)
        d.text(s, finding, M + Inches(2.55), Inches(y + 0.12), Inches(9.3), Inches(0.34), size=10.0, color=b.MUTED, shrink=True)
    d.text(s, "Contradiction: consultancies validate Beacon's wedge, but also become the highest-credibility alternative if Beacon cannot prove execution outcomes.", M, Inches(6.08), CW, Inches(0.42), size=11.3, color=b.CORAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_47(page):
    s = header("Consultancies Validate The Execution Gap", "Their research points to the same problem Beacon wants to solve")
    card(s, 0.72, 1.78, 3.75, 3.35, "McKinsey", "AI adoption is widespread, but scaling and EBIT impact remain limited; value depends on workflow redesign, operating model, data, and adoption.", b.NAVY)
    card(s, 4.78, 1.78, 3.75, 3.35, "BCG", "AI leaders outperform laggards, but agents are not plug-and-play; process, role, and skills redesign drive value capture.", b.TEAL)
    card(s, 8.85, 1.78, 3.75, 3.35, "Deloitte", "AI access is rising faster than mature governance; agentic AI needs controls, measurement, and enterprise adoption discipline.", b.GOLD)
    d.text(s, "Beacon's opening: enterprises do not need another AI ambition layer. They need a way to execute, validate, audit, and repeat implementation work.", M, Inches(5.85), CW, Inches(0.72), size=12.0, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_48(page):
    s = header("The Consulting-Firm Threat", "The threat is delivery machinery, not PowerPoint")
    threats = [
        ("Services scale", "Accenture, IBM, Capgemini, and Deloitte can staff transformation programs globally."),
        ("Platform assets", "AI Refinery, watsonx, Consulting Advantage, BCG X, QuantumBlack, and internal assistant libraries."),
        ("Executive access", "McKinsey, BCG, and Accenture often shape the budget before tools are shortlisted."),
        ("Governance trust", "Big Four and IBM can slow adoption by framing AI execution as risk-managed transformation."),
        ("Partner ecosystems", "Hyperscalers and model providers use consultancies as enterprise deployment channels."),
    ]
    for i, (title, body) in enumerate(threats):
        y = 1.72 + i * 0.78
        d.rect(s, M, Inches(y), CW, Inches(0.58), b.WHITE, radius=0.04, line=b.GRID)
        d.rect(s, M, Inches(y), Inches(0.08), Inches(0.58), b.CORAL if i < 3 else b.GOLD)
        d.text(s, title, M + Inches(0.22), Inches(y + 0.14), Inches(2.25), Inches(0.2), size=10.7, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, M + Inches(2.8), Inches(y + 0.09), Inches(9.0), Inches(0.32), size=9.8, color=b.MUTED, shrink=True)
    add_footer(s, page)


def slide_49(page):
    s = header("Beacon's Consulting-Firm Differentiation", "The sharper line: post-consultancy execution infrastructure")
    d.rect(s, M, Inches(1.78), CW, Inches(1.0), b.NAVY, radius=0.08)
    d.text(s, "Consultancies design and govern transformation. Beacon turns transformation intent into repeatable, auditable implementation execution.", M + Inches(0.28), Inches(1.98), CW - Inches(0.56), Inches(0.52), size=14.2, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    card(s, 0.72, 3.2, 3.75, 2.05, "Do not claim", "“We replace AI transformation consulting.” That is too broad and invites a credibility fight.", b.CORAL)
    card(s, 4.78, 3.2, 3.75, 2.05, "Claim instead", "“We productize the repeated implementation work that consulting teams and post-sales teams still do manually.”", b.TEAL)
    card(s, 8.85, 3.2, 3.75, 2.05, "Prove with", "Task-level before/after evidence: elapsed time, human touches, exceptions, validation logs, and hypercare load.", b.GOLD)
    add_footer(s, page)


def slide_50(page):
    s = header("Build / Buy / Partner Implication", "Beacon should become the execution capability in a mixed sourcing model")
    rows = [
        ("Build", "Unique product rules, proprietary implementation playbooks, customer-specific configuration logic."),
        ("Buy", "Generic AI infrastructure, model access, analytics, workflow tooling, and commodity automation."),
        ("Partner", "Transformation strategy, operating-model redesign, governance program, and large-scale change management."),
        ("Beacon slot", "Buy or partner for the repeatable implementation-execution layer where delivery work is expensive and repeated."),
    ]
    for i, (decision, body) in enumerate(rows):
        y = 1.85 + i * 0.94
        d.rect(s, Inches(1.0), Inches(y), Inches(11.3), Inches(0.68), b.WHITE, radius=0.05, line=b.GRID, shadow=True)
        d.rect(s, Inches(1.0), Inches(y), Inches(0.1), Inches(0.68), [b.NAVY, b.GOLD, b.CORAL, b.TEAL][i])
        d.text(s, decision, Inches(1.32), Inches(y + 0.18), Inches(1.6), Inches(0.22), size=12, color=b.NAVY, bold=True)
        d.text(s, body, Inches(3.05), Inches(y + 0.13), Inches(8.75), Inches(0.34), size=10.0, color=b.MUTED, shrink=True)
    add_footer(s, page)


def slide_51(page):
    s = header("War Game: What Could Break The Strategy", "Pre-commit responses before consultancies or generic agents move")
    rows = [
        ("Consultancy bundles agents", "Feature risk", "Partner channel plus domain proof."),
        ("Generic agents mature", "UI execution commoditizes", "Moat shifts to validation logic and audit evidence."),
        ("Buyer picks SI first", "Excluded from budget", "Attach inside post-sales workstreams."),
        ("Governance blocks execution", "POC stalls", "Approval gates, limited scope, rollback plan."),
    ]
    for i, (scenario, impact, response) in enumerate(rows):
        y = 1.72 + i * 0.96
        d.rect(s, M, Inches(y), CW, Inches(0.78), b.WHITE, radius=0.04, line=b.GRID)
        d.rect(s, M, Inches(y), Inches(0.08), Inches(0.78), b.CORAL)
        d.text(s, scenario, M + Inches(0.2), Inches(y + 0.18), Inches(2.75), Inches(0.32), size=8.8, color=b.NAVY, bold=True, shrink=True)
        d.text(s, impact, M + Inches(3.18), Inches(y + 0.18), Inches(2.7), Inches(0.32), size=8.4, color=b.MUTED, shrink=True)
        d.text(s, response, M + Inches(6.1), Inches(y + 0.16), Inches(5.7), Inches(0.36), size=8.2, color=b.INK, shrink=True)
    d.text(s, "Defensible claim: domain automation that beats services and generic agents on the same setup tasks.", M, Inches(6.02), CW, Inches(0.42), size=10.4, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_52(page):
    s = header("Partner, Compete, Or Attach?", "The practical GTM choice by consulting-firm archetype")
    rows = [
        ("Accenture / IBM / Capgemini", "Partner", "Large programs need repeatable execution assets."),
        ("BCG / McKinsey", "Attach below strategy", "They shape the roadmap; Beacon supplies proof."),
        ("Deloitte / Big Four", "Coexist", "Lead with auditability and approvals."),
        ("Boutique AI builders", "Compete selectively", "Win when domain automation beats bespoke build time."),
    ]
    for i, (firm, posture, rationale) in enumerate(rows):
        y = 1.76 + i * 0.92
        d.rect(s, M, Inches(y), CW, Inches(0.72), b.WHITE, radius=0.04, line=b.GRID)
        d.rect(s, M, Inches(y), Inches(0.08), Inches(0.72), b.TEAL if i < 3 else b.GOLD)
        d.text(s, firm, M + Inches(0.2), Inches(y + 0.18), Inches(2.7), Inches(0.28), size=8.8, color=b.NAVY, bold=True, shrink=True)
        d.text(s, posture, M + Inches(3.1), Inches(y + 0.18), Inches(2.05), Inches(0.28), size=8.4, color=b.ACCENT, bold=True, shrink=True)
        d.text(s, rationale, M + Inches(5.45), Inches(y + 0.16), Inches(6.3), Inches(0.32), size=8.3, color=b.MUTED, shrink=True)
    add_footer(s, page)


def slide_53(page):
    s = header("Transformation Roadmap Add-On", "How Beacon should use the consulting lens in the next 90 days")
    card(s, 0.72, 1.78, 3.75, 3.3, "30 days", "Create consulting-firm battlecards; define Beacon's attach-vs-compete posture; update sales language to post-consultancy execution infrastructure.", b.TEAL)
    card(s, 4.78, 1.78, 3.75, 3.3, "60 days", "Run POCs against tasks consultancies would staff manually; package validation logs, audit trails, and before/after economics.", b.GOLD)
    card(s, 8.85, 1.78, 3.75, 3.3, "90 days", "Build a partner narrative for SIs/consultancies; publish customer evidence; decide whether to pursue channel partnerships.", b.NAVY)
    d.text(s, "Success metric: Beacon becomes the execution proof layer inside implementation workstreams, not another AI transformation narrative.", M, Inches(5.82), CW, Inches(0.7), size=11.8, color=b.CORAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def slide_54(page):
    s = header("Updated Strategic Position", "The full differentiation stack")
    d.rect(s, M, Inches(1.62), CW, Inches(0.74), b.NAVY, radius=0.06)
    d.text(s, "Beacon owns implementation execution where adjacent categories stop short.", M + Inches(0.25), Inches(1.78), CW - Inches(0.5), Inches(0.36), size=11.8, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    stack = [
        ("DAPs", "Guide adoption"),
        ("Onboarding tools", "Coordinate delivery"),
        ("RPA / generic agents", "Automate fragments"),
        ("Consultancies", "Design and govern transformation"),
        ("Beacon", "Executes implementation work with evidence"),
    ]
    for i, (layer, job) in enumerate(stack):
        y = 2.72 + i * 0.62
        d.rect(s, Inches(1.05), Inches(y), Inches(11.2), Inches(0.43), b.WHITE, line=b.GRID)
        d.rect(s, Inches(1.05), Inches(y), Inches(0.08), Inches(0.43), b.TEAL if layer == "Beacon" else b.GOLD)
        d.text(s, layer, Inches(1.25), Inches(y + 0.09), Inches(2.25), Inches(0.2), size=10.4, color=b.NAVY, bold=True, shrink=True)
        d.text(s, job, Inches(3.75), Inches(y + 0.09), Inches(7.8), Inches(0.2), size=10.2, color=b.MUTED, shrink=True)
    d.text(s, "Next client-proof requirement: run one implementation task against Beacon, a services baseline, and a generic agent baseline.", M, Inches(6.05), CW, Inches(0.5), size=11.6, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def methodology_slide(page):
    s = header("Methodology: Four Arenas, One Rubric", "The rebuild uses a consistent competitor-analysis spine")
    card(s, 0.72, 1.78, 3.75, 3.4, "Research route", "GBrain recall, Firecrawl discovery, primary/company pages, pricing pages, STORM-style lenses, and consulting-framework synthesis.", b.TEAL)
    card(s, 4.78, 1.78, 3.75, 3.4, "Competitor universe", "DAP, implementation operations, enterprise AI/automation, and AI transformation consultancies.", b.GOLD)
    card(s, 8.85, 1.78, 3.75, 3.4, "Evaluation spine", "Execution depth, trust, system fit, proof quality, distribution, pricing clarity, threat severity, and partnerability.", b.NAVY)
    d.text(s, "Decision standard: every competitor must be compared by the same buyer job and scoring dimensions, not by feature lists alone.", M, Inches(5.9), CW, Inches(0.58), size=11.8, color=b.CORAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def four_arena_slide(page):
    s = header("The Market Splits Into Four Competitive Arenas", "Each arena can pull Beacon into the wrong comparison if the buyer job is unclear")
    card(s, 0.72, 1.72, 2.9, 3.45, "Digital adoption", "WalkMe/SAP, Pendo, Whatfix, Appcues\n\nJob: guide adoption, training, support, and analytics.", b.TEAL)
    card(s, 3.82, 1.72, 2.9, 3.45, "Implementation ops", "Rocketlane, GuideCX, Arrows, Dock\n\nJob: coordinate onboarding, services, portals, and handoffs.", b.GOLD)
    card(s, 6.92, 1.72, 2.9, 3.45, "AI / automation", "Unframe, UiPath, automation platforms\n\nJob: orchestrate broader enterprise AI workflows.", b.CORAL)
    card(s, 10.02, 1.72, 2.55, 3.45, "Consultancies", "Accenture, BCG, McKinsey, Deloitte, IBM, Capgemini\n\nJob: design and govern transformation.", b.NAVY)
    d.text(s, "Beacon's claim is narrower: execute repeated implementation work with audit-grade evidence.", M, Inches(5.9), CW, Inches(0.5), size=12.4, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def heatmap_slide(page):
    s = header("Scored Competitive Heatmap", "Beacon wins on execution specificity; incumbents win on trust, distribution, or breadth")
    cols = ["Vendor", "Exec depth", "Trust", "System fit", "Proof", "Distribution", "Threat"]
    widths = [2.2, 1.35, 1.15, 1.35, 1.1, 1.45, 1.1]
    x = [0.72]
    for w_ in widths[:-1]:
        x.append(x[-1] + w_)
    for i, col in enumerate(cols):
        d.rect(s, Inches(x[i]), Inches(1.72), Inches(widths[i]), Inches(0.42), b.NAVY, radius=0.02)
        d.text(s, col, Inches(x[i] + 0.04), Inches(1.85), Inches(widths[i] - 0.08), Inches(0.12), size=7.8, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    rows = [
        ("Beacon.li", 5, 4, 4, 2, 2, 4),
        ("WalkMe/SAP", 3, 5, 5, 5, 5, 5),
        ("Rocketlane", 3, 4, 5, 4, 4, 4),
        ("Unframe AI", 4, 4, 4, 3, 4, 4),
        ("UiPath", 3, 5, 5, 4, 5, 4),
        ("Accenture/IBM", 3, 5, 5, 5, 5, 5),
        ("Pendo/Whatfix", 2, 5, 4, 5, 4, 3),
    ]
    def color(score):
        return b.TEAL if score >= 5 else b.GOLD if score >= 4 else b.SOFT if score >= 3 else b.CORAL
    for r, row in enumerate(rows):
        y = 2.25 + r * 0.48
        name, *scores = row
        d.rect(s, Inches(x[0]), Inches(y), Inches(widths[0]), Inches(0.35), b.WHITE, line=b.GRID)
        d.text(s, name, Inches(x[0] + 0.06), Inches(y + 0.08), Inches(widths[0] - 0.12), Inches(0.14), size=8.2, color=b.NAVY, bold=True, shrink=True)
        for c, score in enumerate(scores, start=1):
            d.rect(s, Inches(x[c]), Inches(y), Inches(widths[c]), Inches(0.35), color(score), line=b.WHITE)
            d.text(s, str(score), Inches(x[c]), Inches(y + 0.08), Inches(widths[c]), Inches(0.14), size=8.0, color=b.NAVY if score < 5 else b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, "Interpretation: Beacon's strategy must convert execution depth into proof quality before incumbents collapse the category around trust and distribution.", M, Inches(6.05), CW, Inches(0.48), size=11.1, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def enterprise_readiness_slide(page):
    s = header("Beacon Trust Is Now Evidenced", "Official pages improve Beacon's enterprise-readiness score")
    rows = [
        ("Beacon", "SOC 2, RBAC, SSO, audit trails, no backend/API/database access, public trust center", "Trust moves up; proof remains the bottleneck."),
        ("WalkMe / SAP", "SOC/ISO/GDPR evidence, SOC report, FedRAMP-related positioning, SAP ecosystem", "Highest DAP trust and distribution benchmark."),
        ("Whatfix / Pendo", "SOC 2, ISO/GDPR/TX-RAMP/HIPAA, SSO/SAML/MFA, trust/security pages", "Strong DAP trust; avoid adoption-category fight."),
        ("Rocketlane / GUIDEcx", "SOC 1/2, CSA STAR, ISO/GDPR, SSO/SAML, audit logs, DPA/trust references", "Credible PS/onboarding trust; integrate/coexist."),
        ("Workato / UiPath / MuleSoft / Boomi", "Governance, audit trails, RBAC/SSO, compliance certifications, data/security controls", "Broad platform threat where API-led automation fits."),
    ]
    for i, (vendor, evidence, implication) in enumerate(rows):
        y = 1.72 + i * 0.82
        d.rect(s, M, Inches(y), CW, Inches(0.62), b.WHITE, radius=0.04, line=b.GRID)
        d.rect(s, M, Inches(y), Inches(0.08), Inches(0.62), b.TEAL if i == 0 else b.GOLD)
        d.text(s, vendor, M + Inches(0.22), Inches(y + 0.14), Inches(2.15), Inches(0.28), size=9.4, color=b.NAVY, bold=True, shrink=True)
        d.text(s, evidence, M + Inches(2.62), Inches(y + 0.09), Inches(5.05), Inches(0.38), size=8.2, color=b.MUTED, shrink=True)
        d.text(s, implication, M + Inches(7.95), Inches(y + 0.09), Inches(3.8), Inches(0.38), size=8.2, color=b.INK, bold=(i == 0), shrink=True)
    d.text(s, "Client implication: stop treating Beacon security as missing. Keep the pressure on measured implementation outcomes.", M, Inches(6.12), CW, Inches(0.4), size=10.8, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def pricing_ecosystem_slide(page):
    s = header("Pricing And Ecosystem: Use As Pressure Signals", "Official data supports commercial-transparency scoring, not a hard TCO comparison")
    card(s, 0.72, 1.72, 3.75, 3.05, "Pricing evidence", "Official pricing pages surfaced for GUIDEcx, Pendo, and WalkMe. Beacon public pricing was not found. Most enterprise TCO remains quote-based or procurement-gated.", b.GOLD)
    card(s, 4.78, 1.72, 3.75, 3.05, "Ecosystem evidence", "WalkMe/SAP, Salesforce, ServiceNow, MuleSoft, Boomi, Workato, and UiPath have the strongest platform gravity. Beacon has a public partner page, but named depth is emerging.", b.TEAL)
    card(s, 8.85, 1.72, 3.75, 3.05, "Deck implication", "Score pricing as transparency and score ecosystem as route-to-market power. Do not imply exact pricing comparability where public TCO is unavailable.", b.NAVY)
    d.rect(s, M, Inches(5.35), CW, Inches(0.72), b.SOFT, radius=0.06, line=b.GRID)
    d.text(s, "Strategic read: Beacon's product wedge is clearer than its commercial proof. The next artifact should tie price to workflow-level labor removed.", M + Inches(0.28), Inches(5.52), CW - Inches(0.56), Inches(0.34), size=10.8, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def datapoint_table_slide(page, title, subtitle, rows, note):
    s = header(title, subtitle)
    cols = [("Company", 0.72, 2.0), ("Datapoint", 2.9, 4.4), ("Use In Story", 7.5, 4.3)]
    for label, x0, w0 in cols:
        d.rect(s, Inches(x0), Inches(1.72), Inches(w0), Inches(0.42), b.NAVY, radius=0.02)
        d.text(s, label, Inches(x0 + 0.08), Inches(1.86), Inches(w0 - 0.16), Inches(0.12), size=8.8, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    for i, (company, datapoint, use) in enumerate(rows):
        y = 2.25 + i * 0.58
        accent = b.TEAL if i % 2 == 0 else b.GOLD
        d.rect(s, Inches(0.72), Inches(y), Inches(2.0), Inches(0.43), b.WHITE, line=b.GRID)
        d.rect(s, Inches(0.72), Inches(y), Inches(0.07), Inches(0.43), accent)
        d.text(s, company, Inches(0.9), Inches(y + 0.08), Inches(1.65), Inches(0.23), size=8.5, color=b.NAVY, bold=True, shrink=True)
        d.rect(s, Inches(2.9), Inches(y), Inches(4.4), Inches(0.43), b.WHITE, line=b.GRID)
        d.text(s, datapoint, Inches(3.02), Inches(y + 0.06), Inches(4.16), Inches(0.28), size=7.7, color=b.INK, shrink=True)
        d.rect(s, Inches(7.5), Inches(y), Inches(4.3), Inches(0.43), b.WHITE, line=b.GRID)
        d.text(s, use, Inches(7.62), Inches(y + 0.06), Inches(4.06), Inches(0.28), size=7.7, color=b.MUTED, shrink=True)
    d.rect(s, M, Inches(6.05), CW, Inches(0.48), b.SOFT, radius=0.05, line=b.GRID)
    d.text(s, note, M + Inches(0.24), Inches(6.18), CW - Inches(0.48), Inches(0.18), size=9.3, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def beacon_datapoints_slide(page):
    datapoint_table_slide(page, "Beacon Outcome Evidence", "Public Beacon claims now need to be shown as explicit proof points", [
        ("Beacon", "60%+ reduction in implementation effort / timelines", "Core wedge: implementation execution removes delivery labor."),
        ("Darwinbox", "85% faster onboarding / implementation case", "Named proof point for complex HR module implementation."),
        ("Fintech case", "85% faster handovers; 60% fewer configuration defects; 30% lower implementation costs", "Best multi-metric Beacon proof cluster; still needs denominators."),
        ("Marketplace", "80% faster seller onboarding", "Shows wedge beyond HR/BFSI into marketplace onboarding."),
        ("Keka", "62% faster response in support-ticket deflection case", "Extends implementation-execution story into support productivity."),
        ("Beacon homepage", "90 days of hand-holding reframed as 30 days of guided self-service", "Use as value narrative; treat as vendor claim."),
    ], "Caveat: Beacon percentages are useful, but raw baselines and independent validation remain open.")


def dap_datapoints_slide(page):
    datapoint_table_slide(page, "DAP Benchmark Evidence", "WalkMe, Whatfix, and Pendo set the proof bar Beacon will be compared against", [
        ("WalkMe", "368% three-year ROI on Forrester TEI page", "Shows incumbent DAP economic proof standard."),
        ("WalkMe", "494% three-year ROI; $41.4M new annual revenue; 60% faster adoption; 87% error reduction", "Use as vendor-cited high-end DAP benchmark, with source caveat."),
        ("WalkMe", "50% IT workload reduction; 85% ROI; 87% fewer errors", "Competitive-page claim; directionally useful, not independent proof."),
        ("Whatfix", "REG: 50% faster time-to-proficiency; 83% fewer daily app-related IT tickets; three-month reduction", "Strong time-to-proficiency and support-deflection comparator."),
        ("Whatfix", "Reed: 23% reduction in support calls per user in six months", "Concrete support-productivity benchmark."),
        ("Pendo", "396% ROI; six-month payback; $1.2M team-efficiency impact", "Product-experience proof benchmark for analytics/adoption vendors."),
    ], "Implication: Beacon must prove implementation execution as rigorously as DAPs prove adoption and support outcomes.")


def implementation_datapoints_slide(page):
    datapoint_table_slide(page, "Implementation And Onboarding Benchmarks", "Adjacent tools define the operating metrics buyers already understand", [
        ("Rocketlane", "2026 PS benchmark: low utilization, cost per billable hour, margin compression", "Use these as services-margin pain indicators."),
        ("Rocketlane", "53.1% margin visibility; 90.2% PSA adoption among SaaS PS", "Supports why implementation ops already has budget gravity."),
        ("Rocketlane", "20+ concurrent projects as a segment signal", "Clarifies fit: project operations layer, not execution layer."),
        ("GUIDEcx", "TTV / TTFV positioned as core onboarding metrics", "Use as KPI spine for Beacon POC design."),
        ("GUIDEcx", "40% more time discussing business outcomes after automated progress tracking", "Shows automation shifts work from status to value conversations."),
        ("Workato / UiPath", "Agentic orchestration pages emphasize workflows, approvals, exceptions, KPIs, cost, ROI, governance", "Broad platform threat: can absorb implementation as one workflow use case."),
    ], "Implication: Beacon should map its POC to familiar PS/onboarding KPIs: TTV, utilization, margin, defects, handoffs, and hypercare.")


def ai_value_datapoints_slide(page):
    datapoint_table_slide(page, "Consulting And AI Value-Realization Evidence", "The AI market context supports Beacon's proof-first recommendation", [
        ("Accenture", "GPT-agent employee platform use case: 30-40% productivity increase", "Sets buyer expectation for agent productivity."),
        ("Accenture", "97% of executives expect GenAI to transform company/industry; 93% say investments outperform other strategic areas", "Supports urgency, not Beacon-specific proof."),
        ("Deloitte", "66% report productivity/efficiency gains from enterprise AI", "Validates productivity as primary AI benefit lens."),
        ("Deloitte", "Nearly 70% moved 30% or fewer GenAI experiments into production", "Supports production-readiness tension."),
        ("BCG", "Two-thirds dissatisfied with GenAI progress; value comes from end-to-end workflow reshaping", "Supports Beacon's workflow-execution positioning."),
        ("Gartner", "More than 50% of GenAI projects abandoned after PoC; 57% of I&O AI failures expected too much too fast", "Direct support for controlled POC thresholds."),
    ], "Implication: the recommendation should be benchmark-first: prove one implementation workflow before scaling the category claim.")


def evidence_coverage_slide(page):
    s = header("Evidence Coverage From Level 2 Livecrawl", "The artifact now uses the full extracted evidence ledger, not a small manual subset")
    stat_card(s, 0.78, 1.78, "588", "evidence rows extracted")
    stat_card(s, 3.55, 1.78, "46", "Level 2 raw files")
    stat_card(s, 6.32, 1.78, "455", "indexed source rows")
    stat_card(s, 9.09, 1.78, "216", "trust / compliance rows")
    rows = [
        ("Top vendor coverage", "WalkMe 66; Beacon 62; Rocketlane 48; Pendo 36; Workato 35; Salesforce 31; UiPath 25; Accenture 23; ServiceNow 23; Whatfix 21."),
        ("Metric coverage", "Trust/compliance 216; ROI/financial 135; time/velocity 131; support productivity 45; AI/automation 32; quality/risk 17."),
        ("Artifact change", "Data now appears in explicit evidence slides and HTML datapoint tables, with confidence caveats for vendor vs third-party claims."),
    ]
    for i, (label, body) in enumerate(rows):
        y = 3.35 + i * 0.82
        d.rect(s, M, Inches(y), CW, Inches(0.58), b.WHITE, radius=0.04, line=b.GRID)
        d.rect(s, M, Inches(y), Inches(0.08), Inches(0.58), b.TEAL if i == 0 else b.GOLD)
        d.text(s, label, M + Inches(0.22), Inches(y + 0.14), Inches(2.35), Inches(0.22), size=10.5, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, M + Inches(2.85), Inches(y + 0.1), Inches(8.95), Inches(0.3), size=9.1, color=b.MUTED, shrink=True)
    add_footer(s, page)


def expanded_beacon_evidence_slide(page):
    datapoint_table_slide(page, "Expanded Beacon Evidence Ledger", "More Beacon datapoints from the 62 extracted rows", [
        ("Customers page", "85% faster handovers; 60% fewer config defects; 30% lower implementation costs", "Use as strongest multi-metric case cluster."),
        ("Darwinbox", "85% faster implementations on Leave module; extended to Attendance and Payroll", "Shows repeatable module-specific implementation execution."),
        ("Beacon blog", "IDC baseline cited: 75% implementation delays; 57% time overrun; 43% cost overrun", "Frames market pain behind Beacon's wedge."),
        ("Retail tech", "4x feature adoption; 80% support tickets resolved autonomously", "Shows support/adoption extension beyond implementation."),
        ("BFSI", "70-80% support queries resolved; 7-day POC; no PII/API/backend access", "Connects velocity with regulated-industry trust."),
        ("Trust pages", "SOC 2, RBAC, SSO, audit trails, Trust Center, ISO/GDPR references", "Moves enterprise-readiness score upward."),
    ], "Remaining gap: raw before/after denominators and independent validation are still not public.")


def expanded_dap_evidence_slide(page):
    datapoint_table_slide(page, "Expanded DAP Evidence Ledger", "DAP incumbents have a much broader proof library than the first artifact showed", [
        ("WalkMe", "368% ROI over three years; 35% retention increase; 10% upsell growth; 20% software-spend savings signal", "Use as mature economic proof benchmark."),
        ("WalkMe", "494% three-year ROI; $41.4M new annual revenue; 60% faster adoption; 87% error reduction", "High-end vendor-cited DAP value case."),
        ("WalkMe", "FedRAMP Ready; SOC 2; ISO; SOC report; 4.5+ years / 1,000+ enterprise-service-provider trust signal", "Procurement and enterprise-trust pressure."),
        ("Whatfix", "REG: 50% faster proficiency; 83% fewer daily IT tickets; Windward: 5,500 agents, 87% support-query reduction", "Support and proficiency proof comparator."),
        ("Whatfix", "Sentry: ~$950K annual savings; 40% content-time reduction; 100 daily tickets eliminated; 94%/91% adoption metrics", "Shows DAP can produce quantified operational proof."),
        ("Pendo", "396% ROI; six-month payback; $1.2M team efficiencies; 1,100 hours of rework saved claim", "Analytics/adoption proof benchmark."),
    ], "Beacon must match this proof style with implementation-specific before/after metrics.")


def expanded_impl_ops_evidence_slide(page):
    datapoint_table_slide(page, "Expanded Implementation Ops Evidence Ledger", "Rocketlane and GUIDEcx show the metrics post-sales buyers already use", [
        ("Rocketlane", "Actabl: 88% reduction in time-to-kickoff; 76% faster delivery cycles", "Cycle-time benchmark for implementation operations."),
        ("Rocketlane", "53.1% margin visibility; 90.2% PSA adoption; satisfaction down 12% to 3.29/5", "Shows tool adoption alone does not solve delivery value."),
        ("Rocketlane", "HPOs productive in 54 days vs 65.5 days; PMO adoption 49.1% vs 37.0%", "Use to define high-performing services benchmark."),
        ("Rocketlane", "30% TTV reduction on $5M ARR services business accelerates ~$1.5M revenue recognition; teams handle 3x more projects", "Direct ROI-model input for Beacon POC."),
        ("Rocketlane", "$200K annual billable revenue consultant creates ~$16.7K/month capacity; three-month vacancy costs ~$50K", "Loaded-cost proxy for implementation capacity value."),
        ("GUIDEcx", "Discovery templates cut implementation time by 66%; automated tracking shifts 40% more time to business outcomes", "TTV and value-realization comparator."),
    ], "Beacon's scorecard should map to TTV, kickoff time, utilization, revenue recognition, project capacity, and margin visibility.")


def expanded_platform_evidence_slide(page):
    datapoint_table_slide(page, "Expanded Platform And Trust Evidence Ledger", "Enterprise platforms bring trust, governance, and ecosystem gravity", [
        ("UiPath", "57% of companies have AI agents in production; ISO/IEC 42001; FedRAMP; audit logs; data residency", "Agentic automation threat with governance credibility."),
        ("Workato", "SOC 2 Type II, SOC 3, SOC 1 Type II; pricing estimates $15K-$50K mid-market and $100K+ enterprise", "Orchestration threat plus commercial benchmark."),
        ("MuleSoft", "ISO 27001, SOC 1, SOC 2, HIPAA, PCI DSS; encryption, audit logs, identity management", "API/integration trust benchmark."),
        ("Boomi", "ISO 27001, GDPR, HIPAA, SOC 2, PCI DSS, RBAC, audit logs, API governance", "iPaaS governance pressure."),
        ("Salesforce", "Agentforce/Data Cloud/Marketing Cloud/Tableau Next FedRAMP High; vendor agents TTV 38 days vs 94 days custom", "Platform ecosystem and vendor-agent benchmark."),
        ("ServiceNow", "Annual SOC 2 Type 2 since 2013; FedRAMP High; ISO/IEC 27018 and 27001; data residency", "Workflow-platform governance benchmark."),
    ], "Beacon should compete on implementation-domain evidence, not generic enterprise-platform trust.")


def expanded_ai_value_evidence_slide(page):
    datapoint_table_slide(page, "Expanded AI Value Evidence Ledger", "Consulting and analyst datapoints justify the proof-first recommendation", [
        ("Accenture", "30-40% GPT-agent productivity lift; 97% transformation expectation; 93% investment outperformance", "Sets executive appetite and proof expectations."),
        ("Accenture", "47% data-readiness challenge; 31% significant GenAI investment; $3B AI commitment; ~77K AI pros", "Shows delivery machinery and readiness bottlenecks."),
        ("Deloitte", "Nearly 70% moved 30% or fewer experiments to production; 85% expect custom agents; 25% transformative impact", "Supports production-gap narrative."),
        ("Deloitte", "60% workforce AI-tool availability; 74% advanced AI initiatives meet/exceed ROI", "Separates access from implementation quality."),
        ("BCG", "~10% apply GenAI at scale; 10-15% productivity from tools; 22% substantial gains; 74% struggle", "Supports workflow redesign and value capture."),
        ("Gartner", ">50% GenAI PoCs abandoned; 57% I&O failures expected too much too fast; 40% agentic apps by 2026", "Justifies strict POC thresholds."),
    ], "This is why the deck should recommend benchmark-first category building, not positioning-only category building.")


def threat_priority_slide(page):
    s = header("Threat Priority Matrix", "Prioritize response by severity, not by brand familiarity")
    card(s, 0.75, 1.78, 5.55, 1.42, "High severity / immediate response", "WalkMe/SAP, Rocketlane, Accenture/IBM/Capgemini\n\nWhy: distribution, enterprise trust, and budget ownership.", b.CORAL)
    card(s, 6.65, 1.78, 5.55, 1.42, "High severity / proof response", "Unframe AI, UiPath, generic computer-use agents\n\nWhy: broad AI delivery can absorb implementation as a use case.", b.GOLD)
    card(s, 0.75, 3.55, 5.55, 1.42, "Medium severity / positioning response", "Pendo, Whatfix, Appcues\n\nWhy: strong DAP fit, but weaker for implementation execution.", b.TEAL)
    card(s, 6.65, 3.55, 5.55, 1.42, "Selective / coexist response", "GuideCX, Arrows, Dock\n\nWhy: useful collaboration layers, often easier to integrate than displace.", b.NAVY)
    d.text(s, "Immediate response: build the benchmark showing Beacon vs manual services vs generic agent execution on the same implementation task.", M, Inches(5.9), CW, Inches(0.58), size=11.5, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def proof_gap_slide(page):
    s = header("The Proof Gap Makes The POC Non-Negotiable", "Beacon's execution claim is differentiated, but it must be converted into audit-grade evidence")
    data = [
        ("Beacon.li", 3, b.TEAL),
        ("Unframe AI", 1, b.GOLD),
        ("Rocketlane", -1, b.SOFT),
        ("UiPath", -1, b.SOFT),
        ("WalkMe/SAP", -2, b.SOFT),
        ("Accenture/IBM", -2, b.SOFT),
        ("Pendo/Whatfix", -3, b.SOFT),
    ]
    d.rect(s, Inches(0.72), Inches(1.65), Inches(3.25), Inches(4.72), b.NAVY, radius=0.08)
    d.text(s, "+3", Inches(0.98), Inches(2.15), Inches(2.72), Inches(0.8), size=48, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, "Beacon proof gap", Inches(0.98), Inches(3.05), Inches(2.72), Inches(0.32), size=16, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, "Execution-depth score minus proof-quality score", Inches(1.0), Inches(3.52), Inches(2.68), Inches(0.58), size=11.2, color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, Inches(1.18), Inches(4.42), Inches(2.32), Inches(0.05), b.TEAL)
    d.text(s, "Meaning: the story is strong, but the sales motion needs benchmarked evidence before category investment.", Inches(1.02), Inches(4.82), Inches(2.64), Inches(0.72), size=10.8, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    center = Inches(8.25)
    top = Inches(1.78)
    scale = Inches(0.72)
    d.text(s, "More claim than proof", Inches(8.92), Inches(1.46), Inches(2.65), Inches(0.18), size=8.2, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "More proof than claim", Inches(4.6), Inches(1.46), Inches(2.65), Inches(0.18), size=8.2, color=b.MUTED, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, center, top - Inches(0.1), Inches(0.018), Inches(4.35), b.NAVY)
    for i in range(7):
        x = center + Inches((i - 3) * 0.72)
        d.rect(s, x, top + Inches(4.12), Inches(0.01), Inches(0.08), b.GRID)
        d.text(s, str(i - 3), x - Inches(0.1), top + Inches(4.25), Inches(0.2), Inches(0.14), size=7.8, color=b.MUTED, align=PP_ALIGN.CENTER)
    for i, (vendor, value, color) in enumerate(data):
        y = top + Inches(0.2 + i * 0.47)
        d.text(s, vendor, Inches(4.08), y + Inches(0.06), Inches(2.05), Inches(0.16), size=9.2, color=b.NAVY, bold=(vendor == "Beacon.li"), shrink=True)
        bar_color = color if value > 0 else b.MUTED
        if value >= 0:
            d.rect(s, center, y, scale * value, Inches(0.26), bar_color, radius=0.03)
            d.text(s, f"+{value}", center + scale * value + Inches(0.08), y + Inches(0.06), Inches(0.35), Inches(0.13), size=8.5, color=b.NAVY, bold=True)
        else:
            d.rect(s, center + scale * value, y, scale * abs(value), Inches(0.26), bar_color, radius=0.03)
            d.text(s, str(value), center + scale * value - Inches(0.43), y + Inches(0.06), Inches(0.35), Inches(0.13), size=8.5, color=b.MUTED, bold=True)
    d.rect(s, M, Inches(5.78), CW, Inches(0.86), b.SOFT, radius=0.06, line=b.GRID)
    d.text(s, "Client implication: keep the category story, but make the next proof artifact a scored benchmark.", M + Inches(0.28), Inches(5.94), CW - Inches(0.56), Inches(0.18), size=10.2, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "Compare manual services vs generic agent vs Beacon on the same implementation task.", M + Inches(0.28), Inches(6.2), CW - Inches(0.56), Inches(0.18), size=10.2, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def proof_benchmark_slide(page):
    s = header("The Required Proof Benchmark", "The category is not won by narrative; it is won by task-level evidence")
    cols = [("Manual services", b.CORAL), ("Generic agent", b.GOLD), ("Beacon", b.TEAL)]
    for i, (title, color_) in enumerate(cols):
        x0 = 0.78 + i * 4.02
        d.rect(s, Inches(x0), Inches(1.82), Inches(3.62), Inches(0.5), color_, radius=0.04)
        d.text(s, title, Inches(x0), Inches(1.98), Inches(3.62), Inches(0.16), size=11, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    rows = [
        ("Elapsed time", "Browser/UI execution", "Cycle-time compression"),
        ("Human touches", "Task completion rate", "Labor removed"),
        ("Known defects", "Hallucination/error rate", "Validation accuracy"),
        ("Approval trail", "Action log", "Audit-ready evidence"),
        ("Hypercare tickets", "Fallback handling", "Post-go-live impact"),
    ]
    for r, row in enumerate(rows):
        y = 2.52 + r * 0.58
        for c, text in enumerate(row):
            x0 = 0.78 + c * 4.02
            d.rect(s, Inches(x0), Inches(y), Inches(3.62), Inches(0.42), b.WHITE, line=b.GRID)
            d.text(s, text, Inches(x0 + 0.1), Inches(y + 0.08), Inches(3.42), Inches(0.2), size=9.0, color=b.INK, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "Decision gate: Beacon only owns the category if it beats both baselines on speed, quality, auditability, and repeatability.", M, Inches(6.03), CW, Inches(0.46), size=11.3, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


def final_recommendation_slide(page):
    s = d.slide(fill=b.NAVY)
    d.text(s, "FINAL RECOMMENDATION", M, Inches(0.82), Inches(5.4), Inches(0.34), size=13, color=b.TEAL, bold=True)
    d.text(s, "Back the category through proof, not positioning alone", M, Inches(1.34), Inches(10.6), Inches(0.92), size=28, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, M, Inches(2.32), Inches(1.4), Inches(0.05), b.TEAL)
    d.text(s, [
        {"text": "Rebuild the sales story around one rubric and four arenas.", "bullet": True, "size": 15, "color": b.LIGHT_TEAL, "space_before": 10},
        {"text": "Run a benchmark: manual services vs generic agent vs Beacon on one real setup task.", "bullet": True, "size": 15, "color": b.LIGHT_TEAL, "space_before": 10},
        {"text": "Use the result to decide pricing, category language, and partner strategy.", "bullet": True, "size": 15, "color": b.LIGHT_TEAL, "space_before": 10},
    ], M, Inches(2.8), Inches(10.4), Inches(1.65), shrink=True)
    d.text(s, "Strategic line: Beacon executes implementation work where guidance, coordination, consulting, and generic automation stop short.", M, Inches(5.9), Inches(10.8), Inches(0.44), size=14, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    add_footer(s, page)


cover(1)
slide_2(2)
methodology_slide(3)
four_arena_slide(4)
slide_32(5)
slide_31(6)
heatmap_slide(7)
enterprise_readiness_slide(8)
evidence_coverage_slide(9)
beacon_datapoints_slide(10)
expanded_beacon_evidence_slide(11)
dap_datapoints_slide(12)
expanded_dap_evidence_slide(13)
implementation_datapoints_slide(14)
expanded_impl_ops_evidence_slide(15)
ai_value_datapoints_slide(16)
expanded_platform_evidence_slide(17)
expanded_ai_value_evidence_slide(18)
proof_gap_slide(19)
threat_priority_slide(20)
slide_8(21)
slide_11(22)
divider(23, "CATEGORY DEEP DIVES", "The Four Competitive Arenas", "Each arena wins a different buyer job; Beacon must prove a narrower execution claim.")
slide_15(24)
slide_16(25)
slide_17(26)
slide_18(27)
slide_19(28)
slide_20(29)
slide_21(30)
slide_22(31)
slide_23(32)
slide_44(33)
slide_45(34)
slide_48(35)
slide_33(36)
slide_34(37)
slide_35(38)
slide_36(39)
slide_37(40)
slide_50(41)
slide_52(42)
slide_38(43)
slide_39(44)
slide_40(45)
pricing_ecosystem_slide(46)
proof_benchmark_slide(47)
slide_28(48)
slide_41(49)
slide_25(50)
slide_42(51)
slide_54(52)
final_recommendation_slide(53)

if d.n != TOTAL:
    raise RuntimeError(f"Expected {TOTAL} slides, got {d.n}")

d.save(OUT)
