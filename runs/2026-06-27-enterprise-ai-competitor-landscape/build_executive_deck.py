#!/usr/bin/env python3
from pathlib import Path
import csv
import sys

sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR


RUN = Path(__file__).resolve().parent
OUT = RUN / "outputs" / "enterprise-ai-competitor-landscape-draft.pptx"
CHART_DIR = RUN / "working" / "deck_charts"
FOOTER = "Enterprise AI Competitor Landscape | Strategy Draft | 2026-06-27"


BATCH_LABELS = {
    "A_foundation_models": "Foundation models",
    "B_enterprise_platforms": "Enterprise platforms",
    "C_developer_agent_tools": "Developer + agent tools",
    "D_observability_security_governance": "Obs/Sec/Gov",
    "E_vertical_ai": "Vertical AI",
    "F_knowledge_infrastructure": "Knowledge + infra",
    "G_consulting_managed_services": "Consulting + managed services",
}


def load_rows():
    path = RUN / "outputs" / "company-universe-evidence-status-phase4.csv"
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


ROWS = load_rows()
TOTAL = len(ROWS)
CATEGORIES = sorted({r["primary_category"] for r in ROWS})
EVIDENCE = {}
BATCHES = {}
CAT_COUNTS = {}
for row in ROWS:
    EVIDENCE[row["evidence_status"]] = EVIDENCE.get(row["evidence_status"], 0) + 1
    BATCHES[row["phase4_batch"]] = BATCHES.get(row["phase4_batch"], 0) + 1
    CAT_COUNTS[row["primary_category"]] = CAT_COUNTS.get(row["primary_category"], 0) + 1


leaders = ["OpenAI", "Anthropic", "NVIDIA", "Microsoft Copilot", "Salesforce Agentforce", "ServiceNow", "Databricks", "Snowflake", "GitHub Copilot", "Hugging Face", "Glean", "Cohere"]
visionaries = ["Mistral AI", "DeepSeek", "LangChain", "LlamaIndex", "Cursor", "Cognition", "Perplexity", "Harvey", "Sierra", "H Company", "Manus", "Writer"]
challengers = ["IBM watsonx", "SAP Joule", "Oracle AI", "Workday AI", "Adobe Firefly", "Datadog", "New Relic", "Dynatrace", "Accenture", "Deloitte", "McKinsey QuantumBlack", "BCG X"]
niche = ["Lakera", "Protect AI", "HiddenLayer", "Credo AI", "Patronus AI", "Pinecone", "Weaviate", "Unstructured", "Abridge", "Hippocratic AI", "EvenUp", "Artisan"]


def add_footer(d, s, page, total, dark=False):
    d.footer(s, page, total, dark=dark)


def header(d, s, title, subtitle):
    b = d.b
    d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
    d.text(s, title, d.M, Inches(0.36), d.CW, Inches(0.78), size=24, color=b.NAVY, bold=True, font=b.FONT_H, shrink=True)
    d.rect(s, d.M, Inches(1.12), Inches(1.35), Inches(0.045), b.TEAL)
    d.text(s, subtitle, d.M, Inches(1.26), d.CW, Inches(0.34), size=11.2, color=b.MUTED, shrink=True)


def card(d, s, x, y, w, h, title, body, *, fill=None, line=None, accent=None, title_color=None):
    b = d.b
    fill = fill or b.SOFT
    line = line or b.GRID
    accent = accent or b.TEAL
    title_color = title_color or b.NAVY
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), fill, line=line, radius=0.04)
    d.rect(s, Inches(x), Inches(y), Inches(0.07), Inches(h), accent)
    d.text(s, title, Inches(x + 0.22), Inches(y + 0.14), Inches(w - 0.42), Inches(0.34), size=9.8, color=title_color, bold=True, shrink=True)
    d.text(s, body, Inches(x + 0.22), Inches(y + 0.52), Inches(w - 0.42), Inches(h - 0.66), size=8.7, color=b.INK, shrink=True)


def stat(d, s, x, y, value, label, *, fill=None, dark=False):
    b = d.b
    fill = fill or (b.NAVY if dark else b.SOFT)
    d.rect(s, Inches(x), Inches(y), Inches(2.45), Inches(1.12), fill, line=None if dark else b.GRID, radius=0.05)
    d.text(s, value, Inches(x + 0.16), Inches(y + 0.16), Inches(2.1), Inches(0.38), size=23, color=b.GOLD if dark else b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, label, Inches(x + 0.16), Inches(y + 0.62), Inches(2.1), Inches(0.36), size=8.5, color=b.LIGHT_TEAL if dark else b.MUTED, bold=True, align=PP_ALIGN.CENTER, shrink=True)


def cover(d):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(10.65), 0, Inches(2.68), d.H, b.NAVY_2)
    d.rect(s, Inches(10.62), 0, Inches(0.06), d.H, b.TEAL)
    d.text(s, "ENTERPRISE AI COMPETITOR LANDSCAPE", d.M, Inches(0.72), Inches(7.6), Inches(0.34), size=13, color=b.TEAL, bold=True)
    d.text(s, "Strategy Draft With Evidence Backlog", d.M, Inches(1.25), Inches(9.15), Inches(1.48), size=36, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
    d.rect(s, d.M, Inches(2.95), Inches(1.9), Inches(0.05), b.TEAL)
    d.text(s, "A 125-company landscape across 14 Enterprise AI categories, designed to guide positioning, pricing intelligence, teardown priorities, and the next source-backed research sprint.", d.M, Inches(3.25), Inches(8.7), Inches(1.05), size=16, color=b.LIGHT_TEAL, shrink=True)
    for i, (value, label) in enumerate([("125", "companies"), ("14", "categories"), ("12", "source-enriched priority rows")]):
        stat(d, s, 0.6 + i * 2.7, 4.75, value, label, dark=True)
    d.text(s, "Status: draft-reviewed after PPTX QA", Inches(10.95), Inches(6.6), Inches(1.85), Inches(0.4), size=9.8, color=b.LIGHT_TEAL, bold=True, align=PP_ALIGN.RIGHT, shrink=True)
    return s


def executive_readout(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "The market is wide, but the wedge is narrow", "The useful output is not another AI directory; it is a source-backed positioning and teardown machine.")
    stat(d, s, 0.85, 1.95, str(TOTAL), "company universe")
    stat(d, s, 3.55, 1.95, str(len(CATEGORIES)), "primary categories")
    stat(d, s, 6.25, 1.95, "7", "source batches")
    stat(d, s, 8.95, 1.95, "113", "source backlog rows")
    card(d, s, 0.85, 3.62, 3.75, 1.55, "What is solid enough now", "The category taxonomy, competitor universe, provisional market map, quadrant-style segmentation, and strategic white-space themes.")
    card(d, s, 4.85, 3.62, 3.75, 1.55, "What is not done", "The full 125-company source attachment is not complete. Pricing, funding, and headcount should not be treated as investor-grade facts yet.", accent=b.CORAL)
    card(d, s, 8.85, 3.62, 3.75, 1.55, "What to do next", "Use the backlog to build named competitor dossiers, starting with pricing/ROI intelligence and agent governance competitors.", fill=b.LIGHT_TEAL, line=b.TEAL, accent=b.DARK_TEAL)
    return s


def market_stack(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "Enterprise AI is a stack, not one market", "The universe splits into infrastructure, builders, enterprise surfaces, governance, vertical workflows, and services.")
    lanes = [
        ("Foundation + infra", "Foundation Models\nInfrastructure\nKnowledge Management", b.NAVY),
        ("Builder layer", "Agent Frameworks\nDeveloper Platforms\nAI Development Platforms", b.TEAL),
        ("Enterprise surface", "Enterprise Platforms\nAI Operations\nVertical AI", b.GOLD),
        ("Control layer", "Observability\nSecurity\nGovernance", b.CORAL),
        ("Delivery layer", "AI Consulting\nManaged Services", b.NAVY_2),
    ]
    for i, (title, body, color) in enumerate(lanes):
        x = 0.75 + i * 2.48
        d.rect(s, Inches(x), Inches(2.0), Inches(2.1), Inches(3.3), color, radius=0.05)
        d.text(s, title, Inches(x + 0.16), Inches(2.25), Inches(1.78), Inches(0.5), size=13, color=b.WHITE if color != b.GOLD else b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, body, Inches(x + 0.16), Inches(3.12), Inches(1.78), Inches(1.42), size=12.2, color=b.WHITE if color != b.GOLD else b.NAVY, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "Implication: do not compete as a generic platform. Win by owning a specific decision layer, buyer workflow, or source-backed teardown product.", Inches(1.25), Inches(5.75), Inches(10.8), Inches(0.48), size=15, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    return s


def batch_distribution(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "Coverage is balanced enough for strategy", "Seven source batches prevent over-indexing on one slice of Enterprise AI.")
    ordered = sorted(BATCHES.items(), key=lambda item: item[1], reverse=True)
    max_value = max(BATCHES.values())
    for i, (key, value) in enumerate(ordered):
        y = 1.88 + i * 0.56
        bar_w = 4.8 * value / max_value
        d.text(s, BATCH_LABELS[key], Inches(0.9), Inches(y + 0.05), Inches(2.7), Inches(0.18), size=9.5, color=b.INK, bold=True, shrink=True)
        d.rect(s, Inches(3.8), Inches(y), Inches(4.9), Inches(0.32), b.SOFT, line=b.GRID, radius=0.04)
        d.rect(s, Inches(3.8), Inches(y), Inches(bar_w), Inches(0.32), b.TEAL if i == 0 else b.NAVY, radius=0.04)
        d.text(s, str(value), Inches(8.9), Inches(y + 0.04), Inches(0.35), Inches(0.18), size=9.8, color=b.NAVY, bold=True, align=PP_ALIGN.RIGHT)
    card(d, s, 8.85, 2.0, 3.45, 1.2, "Largest batch", "Observability, security, and governance: 25 companies.", fill=b.LIGHT_TEAL, line=b.TEAL, accent=b.DARK_TEAL)
    card(d, s, 8.85, 3.45, 3.45, 1.2, "Strategic reading", "Control-plane categories matter because enterprise buyers need trust, auditability, and deployment discipline.")
    card(d, s, 8.85, 4.9, 3.45, 1.2, "Caveat", "Batch counts are classification aids, not market-share estimates.", accent=b.CORAL)
    return s


def category_grid(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "The strongest signal is category fragmentation", "Fourteen lanes create room for focused wedge products, but weak sourcing can distort priority calls.")
    ordered = sorted(CAT_COUNTS.items(), key=lambda x: (-x[1], x[0]))
    for i, (cat, count) in enumerate(ordered):
        col = i % 4
        row = i // 4
        x = 0.75 + col * 3.1
        y = 1.9 + row * 1.12
        fill = b.LIGHT_TEAL if cat in {"Vertical AI", "Observability", "Knowledge Management", "Infrastructure"} else b.SOFT
        d.rect(s, Inches(x), Inches(y), Inches(2.72), Inches(0.84), fill, line=b.TEAL if fill == b.LIGHT_TEAL else b.GRID, radius=0.04)
        d.text(s, str(count), Inches(x + 0.12), Inches(y + 0.14), Inches(0.5), Inches(0.28), size=18, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        label = {
            "Enterprise Platforms": "Enterprise\nPlatforms",
            "Knowledge Management": "Knowledge\nMgmt",
            "AI Development Platforms": "AI Dev\nPlatforms",
        }.get(cat, cat)
        d.text(s, label, Inches(x + 0.75), Inches(y + 0.11), Inches(1.75), Inches(0.48), size=9.2, color=b.INK, bold=True, shrink=True)
    d.text(s, "Priority implication: the best wedge is where pain is high, pricing is opaque, and source-backed teardown creates buyer leverage.", Inches(0.95), Inches(6.28), Inches(11.4), Inches(0.62), size=12, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    return s


def pricing_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "Pricing opacity is a product opportunity", "Enterprise AI packaging is now a hybrid of seats, usage, tokens, credits, compute, traces, and custom contracts.")
    models = [
        ("Seats", "Enterprise copilots and workflow apps"),
        ("Usage", "API calls, events, traces, seats plus usage"),
        ("Tokens", "Model access, context, generation volume"),
        ("Credits", "AI app platforms and automation bundles"),
        ("Compute", "GPU, inference, hosting, data workloads"),
        ("Custom", "Enterprise contracts, services, managed delivery"),
    ]
    for i, (title, body) in enumerate(models):
        col = i % 3
        row = i // 3
        card(d, s, 0.9 + col * 4.05, 2.0 + row * 1.55, 3.45, 1.05, title, body, fill=b.LIGHT_TEAL if i in [1, 2, 5] else b.SOFT, line=b.TEAL if i in [1, 2, 5] else b.GRID)
    d.rect(s, Inches(1.05), Inches(5.48), Inches(11.2), Inches(0.76), b.NAVY, radius=0.04)
    d.text(s, "White-space thesis: buyers need AI pricing/ROI intelligence before platform sprawl.", Inches(1.22), Inches(5.68), Inches(10.85), Inches(0.36), size=12.4, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    return s


def evidence_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "The evidence table is honest about what is sourced", "This is the quality-control slide that prevents the deck from overselling the research state.")
    enriched = sum(v for k, v in EVIDENCE.items() if "source_attached" in k)
    backlog = EVIDENCE.get("source_backlog", 0)
    stat(d, s, 1.2, 2.0, str(enriched), "rows with attached priority evidence")
    stat(d, s, 4.25, 2.0, str(backlog), "rows in source backlog")
    stat(d, s, 7.3, 2.0, "0", "fabricated private-company claims")
    card(d, s, 1.1, 3.7, 3.5, 1.55, "Allowed use", "Internal strategy, prioritization, deck spine, and source backlog planning.", fill=b.LIGHT_TEAL, line=b.TEAL, accent=b.DARK_TEAL)
    card(d, s, 4.9, 3.7, 3.5, 1.55, "Not allowed yet", "External publication as a fully sourced market map or investor-grade database.", accent=b.CORAL)
    card(d, s, 8.7, 3.7, 3.5, 1.55, "Next QA gate", "Attach primary pricing/funding/status sources to the most commercially relevant 30-40 companies first.")
    return s


def quadrant_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "The quadrant is a prioritization device, not a Gartner claim", "Unofficial view: completeness of vision vs. ability to execute.")
    x0, y0, w, h = 0.95, 1.75, 11.45, 4.75
    d.rect(s, Inches(x0), Inches(y0), Inches(w), Inches(h), b.SOFT, line=b.GRID)
    d.rect(s, Inches(x0 + w / 2), Inches(y0), Inches(0.03), Inches(h), b.GRID)
    d.rect(s, Inches(x0), Inches(y0 + h / 2), Inches(w), Inches(0.03), b.GRID)
    quads = [
        ("Challengers", challengers, x0 + 0.25, y0 + 0.25),
        ("Leaders", leaders, x0 + w / 2 + 0.25, y0 + 0.25),
        ("Niche Players", niche, x0 + 0.25, y0 + h / 2 + 0.25),
        ("Visionaries", visionaries, x0 + w / 2 + 0.25, y0 + h / 2 + 0.25),
    ]
    for title, names, x, y in quads:
        d.text(s, title, Inches(x), Inches(y), Inches(4.9), Inches(0.28), size=13.5, color=b.NAVY, bold=True, shrink=True)
        d.text(s, ", ".join(names), Inches(x), Inches(y + 0.42), Inches(4.9), Inches(1.18), size=9.6, color=b.INK, shrink=True)
    d.text(s, "Ability to execute", Inches(0.35), Inches(3.05), Inches(0.3), Inches(1.35), size=9, color=b.MUTED, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "Completeness of vision", Inches(5.0), Inches(6.62), Inches(3.2), Inches(0.22), size=9, color=b.MUTED, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    return s


def leaders_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "Leaders own distribution; challengers own enterprise channels", "The market-facing mistake is trying to out-platform the incumbents.")
    card(d, s, 0.85, 1.95, 5.65, 3.55, "Leader pattern", "Foundation labs, hyperscalers, enterprise systems of record, and developer distribution platforms win because they already control model access, workflows, data platforms, or developer surfaces.", fill=b.LIGHT_TEAL, line=b.TEAL, accent=b.DARK_TEAL)
    card(d, s, 6.85, 1.95, 5.65, 3.55, "Challenger pattern", "Large enterprise software and consulting firms are slower, but they have procurement trust, implementation teams, and existing account control.", fill=b.SOFT, line=b.GRID, accent=b.GOLD)
    d.text(s, "Strategic rule: sell a sharper diagnostic, teardown, or implementation wedge around these platforms.", Inches(1.2), Inches(5.86), Inches(10.9), Inches(0.62), size=12.6, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    return s


def white_space_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "The best opportunities sit where buyers lack clarity", "White space is strongest where pricing, governance, and implementation proof are opaque.")
    spaces = [
        ("AI pricing + ROI intelligence", "Compare true cost, payback, and packaging risk across AI platforms."),
        ("Agent governance cockpit", "Track permissions, auditability, handoffs, and production controls."),
        ("Source-backed competitor teardown", "Turn competitor claims into buyer-specific proof and gaps."),
        ("Vertical workflow agents", "Own a narrow audited handoff, not an all-purpose assistant."),
        ("Managed implementation packages", "Package the 10-skill operator system into repeatable delivery.")
    ]
    for i, (title, body) in enumerate(spaces):
        card(d, s, 0.85 + (i % 2) * 6.0, 1.85 + (i // 2) * 1.38, 5.35, 0.98, title, body, fill=b.LIGHT_TEAL if i in [0, 1] else b.SOFT, line=b.TEAL if i in [0, 1] else b.GRID, accent=b.DARK_TEAL if i in [0, 1] else b.TEAL)
    return s


def threats_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "The threat is platform absorption, not feature competition", "Most standalone AI features will be bundled, copied, or discounted by incumbents.")
    threats = [
        ("Hyperscaler bundling", "Microsoft, Google, AWS, and Oracle can bundle AI into cloud and productivity spend."),
        ("Foundation-model gravity", "Model providers can move upward into apps, agents, and orchestration."),
        ("Enterprise system lock-in", "Salesforce, ServiceNow, SAP, Workday, and Adobe own daily workflows."),
        ("Consulting account control", "Accenture, Deloitte, McKinsey, and BCG can shape the buyer’s AI roadmap."),
    ]
    for i, (title, body) in enumerate(threats):
        card(d, s, 0.95 + (i % 2) * 6.0, 2.0 + (i // 2) * 1.62, 5.25, 1.12, title, body, accent=b.CORAL)
    d.rect(s, Inches(1.1), Inches(5.62), Inches(11.1), Inches(0.76), b.NAVY, radius=0.04)
    d.text(s, "Counter-positioning: make the offer evidence-led, source-backed, and tied to deployment decisions.", Inches(1.25), Inches(5.84), Inches(10.8), Inches(0.3), size=12, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    return s


def recommendations_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "Five recommendations turn the landscape into an operator offer", "The output should sell judgment and execution compression, not a generic AI consulting promise.")
    recs = [
        "Treat the 10-skill operator stack as the delivery differentiator.",
        "Build source-backed competitor teardown dossiers before publication.",
        "Prioritize AI pricing and ROI intelligence as the strongest wedge.",
        "Bake governance and observability into agent deployment packages.",
        "Avoid generic platform competition against hyperscalers and incumbents.",
    ]
    for i, rec in enumerate(recs):
        y = 1.95 + i * 0.82
        d.rect(s, Inches(1.0), Inches(y), Inches(0.46), Inches(0.46), b.TEAL if i < 3 else b.NAVY, radius=0.08)
        d.text(s, str(i + 1), Inches(1.11), Inches(y + 0.12), Inches(0.24), Inches(0.16), size=10, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, rec, Inches(1.75), Inches(y + 0.08), Inches(10.2), Inches(0.3), size=14, color=b.INK, bold=True, shrink=True)
    return s


def action_plan_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    header(d, s, "Next 30 days: source, teardown, package", "The immediate job is to convert draft market structure into client-facing proof.")
    weeks = [
        ("Week 1", "Source-attach top 30-40 companies by commercial relevance."),
        ("Week 2", "Build competitor teardown dossiers for pricing/ROI and governance lanes."),
        ("Week 3", "Convert white-space into 3 operator offers with buyer-facing deliverables."),
        ("Week 4", "QA, publish safe excerpts, and keep the full table as internal intelligence.")
    ]
    for i, (week, body) in enumerate(weeks):
        card(d, s, 0.95 + i * 3.05, 2.05, 2.55, 2.75, week, body, fill=b.LIGHT_TEAL if i == 0 else b.SOFT, line=b.TEAL if i == 0 else b.GRID, accent=b.DARK_TEAL if i == 0 else b.TEAL)
    d.text(s, "Stop condition: do not ship a public market map until source attachment covers every named pricing/funding/status claim.", Inches(1.1), Inches(5.55), Inches(11.1), Inches(0.45), size=13.5, color=b.CORAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    return s


def closing_slide(d):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.text(s, "BOTTOM LINE", d.M, Inches(0.78), d.CW, Inches(0.32), size=13, color=b.TEAL, bold=True)
    d.text(s, "The opportunity is not to publish a prettier AI market map. It is to productize source-backed judgment.", d.M, Inches(1.34), Inches(10.8), Inches(2.0), size=30, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(3.55), Inches(1.8), Inches(0.05), b.TEAL)
    d.text(s, "Use the landscape to choose the sharpest wedge, then use the 10-skill operator stack to prove execution discipline before anyone asks for a build.", d.M, Inches(3.9), Inches(9.8), Inches(0.9), size=17, color=b.LIGHT_TEAL, shrink=True)
    d.text(s, "Recommended next artifact: top-40 sourced teardown pack.", d.M, Inches(5.7), Inches(7.8), Inches(0.35), size=14, color=b.GOLD, bold=True, shrink=True)
    return s


def build():
    d = Deck(footer=FOOTER)
    slides = [
        cover(d),
        executive_readout(d),
        market_stack(d),
        batch_distribution(d),
        category_grid(d),
        pricing_slide(d),
        evidence_slide(d),
        quadrant_slide(d),
        leaders_slide(d),
        white_space_slide(d),
        threats_slide(d),
        recommendations_slide(d),
        action_plan_slide(d),
        closing_slide(d),
    ]
    total = len(slides)
    for idx, slide in enumerate(slides, start=1):
        if idx != 1:
            add_footer(d, slide, idx, total, dark=(idx == total))
    d.save(OUT)


if __name__ == "__main__":
    build()
