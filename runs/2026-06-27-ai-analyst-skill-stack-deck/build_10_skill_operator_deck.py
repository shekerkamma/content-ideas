#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR


RUN = Path(__file__).resolve().parent
OUT = RUN / "outputs" / "10-skill-operator-stack-draft.pptx"
FOOTER = "10-Skill Operator Stack | Draft | 2026-06-27"


skills = [
    {
        "num": "01",
        "name": "Problem-Solution Fit Validation",
        "job": "Stop the founder from spending 30 days building the wrong thing.",
        "artifact": "0-30 scored verdict across problem realness, solution fit, buying signal, and reachability.",
        "gate": "Representative users, real dollar signal, and hidden regulatory or distribution constraints.",
    },
    {
        "num": "02",
        "name": "30-Day Scope Definition",
        "job": "Turn a validated problem into a contract-grade MVP scope.",
        "artifact": "1.5-2 page spec with in-scope cuts, out-of-scope list, weekly milestones, risks, and acceptance test.",
        "gate": "Founder feature creep, integration optimism, and actual weekly velocity.",
    },
    {
        "num": "03",
        "name": "Tech Stack + Architecture Design",
        "job": "Create the technical ground truth the builder can execute.",
        "artifact": "Stack, schema, RLS, auth flow, API surface, integrations, env vars, and design decisions.",
        "gate": "Generic stack advice, RLS leakage, and v1 schema choices that block v2.",
    },
    {
        "num": "04",
        "name": "Build vs Buy Decision Matrix",
        "job": "Decide what to build, buy, or hybridize.",
        "artifact": "Feature matrix with build cost, 3-year SaaS cost, lock-in risk, verdict, and payback.",
        "gate": "SaaS pricing creep, niche workflow misfit, and lock-in that appears later.",
    },
    {
        "num": "05",
        "name": "MVP ROI Business Case",
        "job": "Gate whether the MVP economics justify proceeding.",
        "artifact": "Available source rule: if base-case breakeven is past month 36, the solo MVP is not viable.",
        "gate": "Do not let excitement about the build outrun the payback logic. Source is partial.",
    },
    {
        "num": "06",
        "name": "Competitor Product Teardown",
        "job": "Name incumbents and expose where a focused MVP can win.",
        "artifact": "5-10 competitor profiles covering positioning, pricing, onboarding, strengths, weaknesses, and gaps.",
        "gate": "Non-obvious competitors, positioning patterns, and unverifiable pricing.",
    },
    {
        "num": "07",
        "name": "Acceptance Criteria + Test Plan",
        "job": "Define what shipped means before anyone declares victory.",
        "artifact": "User stories, testable criteria, edge cases, not-in-scope list, and manual test steps.",
        "gate": "Cross-feature failures, duplicate clicks, auth boundaries, and launch-night paths.",
    },
    {
        "num": "08",
        "name": "Data Architecture Lite",
        "job": "Make data and analytics part of v1, not month-12 cleanup.",
        "artifact": "Sources, storage, source of truth, sync, analytics events, and data quality guardrails.",
        "gate": "Hidden data stores, manual overrides, refunds, and source-of-truth drift.",
    },
    {
        "num": "09",
        "name": "Deployment Sequencing",
        "job": "Turn launch into a reversible sequence, not a button press.",
        "artifact": "Pre-deploy checklist, staging setup, production sequence, smoke test, and rollback plan.",
        "gate": "Env vars, live webhook secrets, redirect URLs, real payment, session persistence, and data isolation.",
    },
    {
        "num": "10",
        "name": "Post-Launch Iteration Plan",
        "job": "Keep the founder from reacting chaotically after launch.",
        "artifact": "Three metrics, feedback triage, four-week plan, and pivot signals.",
        "gate": "No new features in week 1; active-user learning drives the one retention bet.",
    },
]


def chip(d, s, label, x, y, w, color=None):
    b = d.b
    fill = color or b.NAVY_2
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(0.42), fill, radius=0.08)
    d.text(
        s,
        label,
        Inches(x + 0.08),
        Inches(y + 0.11),
        Inches(w - 0.16),
        Inches(0.26),
        size=8.6,
        color=b.WHITE,
        bold=True,
        align=PP_ALIGN.CENTER,
        shrink=True,
    )


def add_footer(d, s, page, total, dark=False):
    d.footer(s, page, total, dark=dark)


def cover(d):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(10.7), 0, Inches(2.63), d.H, b.NAVY_2)
    d.rect(s, Inches(10.68), 0, Inches(0.06), d.H, b.TEAL)
    d.text(s, "AI-NATIVE MVP OPERATING SYSTEM", d.M, Inches(0.72), Inches(7.6), Inches(0.35), size=13, color=b.TEAL, bold=True)
    d.text(
        s,
        "The 10-Skill Operator Stack for 30-Day Agentic MVPs",
        d.M,
        Inches(1.35),
        Inches(8.8),
        Inches(1.35),
        size=38,
        color=b.WHITE,
        bold=True,
        font=b.FONT_H,
        shrink=True,
    )
    d.rect(s, d.M, Inches(3.05), Inches(2.15), Inches(0.05), b.TEAL)
    d.text(
        s,
        "A repeatable system for validating, scoping, architecting, shipping, and iterating agentic opportunities.",
        d.M,
        Inches(3.35),
        Inches(8.8),
        Inches(1.0),
        size=16.5,
        color=b.LIGHT_TEAL,
        shrink=True,
    )
    for i, txt in enumerate(["10 skills", "52 reviewed opportunities", "operator-gated execution"]):
        chip(d, s, txt, 0.6 + i * 2.55, 4.65, 2.25, b.ACCENT if i == 0 else b.NAVY_2)
    d.text(s, "Draft corrected storyline", Inches(10.98), Inches(6.66), Inches(1.9), Inches(0.4), size=10, color=b.LIGHT_TEAL, bold=True, align=PP_ALIGN.RIGHT)
    return s


def thesis_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, "This is not a blueprint deck", "The use cases are proof. The operating stack is the product.")
    d.rect(s, Inches(0.9), Inches(2.0), Inches(5.35), Inches(3.55), b.SOFT, line=b.GRID, radius=0.05)
    d.text(s, "Wrong lead", Inches(1.2), Inches(2.28), Inches(4.7), Inches(0.35), size=18, color=b.CORAL, bold=True)
    d.text(
        s,
        [
            {"text": "We have implementation blueprints.", "bullet": True, "size": 14.5, "space_before": 7},
            {"text": "The deck becomes a catalog.", "bullet": True, "size": 14.5, "space_before": 7},
            {"text": "The method disappears behind use-case detail.", "bullet": True, "size": 14.5, "space_before": 7},
        ],
        Inches(1.2),
        Inches(2.85),
        Inches(4.65),
        Inches(2.05),
        shrink=True,
    )
    d.rect(s, Inches(7.05), Inches(2.0), Inches(5.35), Inches(3.55), b.LIGHT_TEAL, line=b.TEAL, radius=0.05)
    d.text(s, "Correct lead", Inches(7.35), Inches(2.28), Inches(4.7), Inches(0.35), size=18, color=b.DARK_TEAL, bold=True)
    d.text(
        s,
        [
            {"text": "We have a 10-skill operator system.", "bullet": True, "size": 14.5, "space_before": 7},
            {"text": "It replaces the dev-shop path from diagnostic to iteration.", "bullet": True, "size": 14.5, "space_before": 7},
            {"text": "52 reviewed opportunities prove repeatability.", "bullet": True, "size": 14.5, "space_before": 7},
        ],
        Inches(7.35),
        Inches(2.85),
        Inches(4.65),
        Inches(2.05),
        shrink=True,
    )
    return s


def cost_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, "The old way burns budget before proof", "Source-backed replacement targets from the original skill stack.")
    rows = [
        ("Diagnostic", "$10K-$15K"),
        ("Scope document", "$15K-$25K"),
        ("Architecture", "$20K-$40K"),
        ("Build vs buy analysis", "~$30K"),
        ("Market scan", "$15K"),
        ("Shipping definition / QA", "$20K-$35K"),
    ]
    left, top = 0.95, 1.9
    for i, (phase, cost) in enumerate(rows):
        y = top + i * 0.7
        d.rect(s, Inches(left), Inches(y), Inches(7.4), Inches(0.54), b.SOFT if i % 2 == 0 else b.WHITE, line=b.GRID)
        d.text(s, phase, Inches(left + 0.22), Inches(y + 0.12), Inches(4.8), Inches(0.28), size=12.8, color=b.INK, bold=True, shrink=True)
        d.text(s, cost, Inches(left + 5.6), Inches(y + 0.12), Inches(1.4), Inches(0.28), size=13.8, color=b.NAVY, bold=True, align=PP_ALIGN.RIGHT, shrink=True)
    d.rect(s, Inches(9.0), Inches(2.05), Inches(3.25), Inches(3.35), b.NAVY, radius=0.08)
    d.text(s, "The offer is compression, not cheapness.", Inches(9.3), Inches(2.45), Inches(2.55), Inches(1.15), size=21, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "The stack replaces slow discovery with gated decisions before a build is sold.", Inches(9.3), Inches(3.85), Inches(2.55), Inches(1.0), size=12.5, color=b.LIGHT_TEAL, shrink=True)
    return s


def flow_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, "The new way is a gated operating system", "Ten skills replace the bloated front half of the traditional dev-shop motion.")
    labels = ["Validate", "Scope", "Architect", "Build/Buy", "ROI", "Teardown", "QA", "Data", "Deploy", "Iterate"]
    x0, y0, w, h, gap = 0.62, 2.05, 1.13, 0.62, 0.13
    for i, label in enumerate(labels):
        x = x0 + i * (w + gap)
        d.rect(s, Inches(x), Inches(y0), Inches(w), Inches(h), b.TEAL if i in [0, 9] else b.NAVY, radius=0.07)
        d.text(s, label, Inches(x + 0.05), Inches(y0 + 0.22), Inches(w - 0.1), Inches(0.18), size=10.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        if i < len(labels) - 1:
            d.text(s, ">", Inches(x + w + 0.02), Inches(y0 + 0.19), Inches(0.16), Inches(0.18), size=15, color=b.MUTED, bold=True, align=PP_ALIGN.CENTER)
    d.rect(s, Inches(1.0), Inches(3.55), Inches(3.4), Inches(1.45), b.SOFT, line=b.GRID, radius=0.05)
    d.text(s, "Every skill produces an artifact.", Inches(1.25), Inches(3.78), Inches(2.9), Inches(0.75), size=14, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, Inches(4.95), Inches(3.55), Inches(3.4), Inches(1.45), b.SOFT, line=b.GRID, radius=0.05)
    d.text(s, "Every skill has a human gate.", Inches(5.2), Inches(3.78), Inches(2.9), Inches(0.75), size=14, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, Inches(8.9), Inches(3.55), Inches(3.4), Inches(1.45), b.LIGHT_TEAL, line=b.TEAL, radius=0.05)
    d.text(s, "The gates prevent false confidence.", Inches(9.15), Inches(3.78), Inches(2.9), Inches(0.75), size=14, color=b.DARK_TEAL, bold=True, shrink=True)
    return s


def skill_slide(d, item):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, f"Skill #{int(item['num'])}: {item['name']}", item["job"])
    d.rect(s, Inches(0.75), Inches(1.85), Inches(2.25), Inches(3.95), b.NAVY, radius=0.08)
    d.text(s, item["num"], Inches(1.08), Inches(2.08), Inches(1.55), Inches(0.9), size=42, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, "OPERATOR\nGATE", Inches(1.05), Inches(3.1), Inches(1.62), Inches(0.62), size=16, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "AI drafts. The operator catches the failure mode.", Inches(1.0), Inches(4.18), Inches(1.78), Inches(0.95), size=9.8, color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
    panels = [
        ("Job", item["job"], b.SOFT, b.NAVY),
        ("Artifact", item["artifact"], b.SOFT, b.NAVY),
        ("Gate", item["gate"], b.LIGHT_TEAL, b.DARK_TEAL),
    ]
    for i, (title, body, fill, accent) in enumerate(panels):
        y = 1.9 + i * 1.25
        d.rect(s, Inches(3.45), Inches(y), Inches(8.7), Inches(0.95), fill, line=b.GRID, radius=0.05)
        d.rect(s, Inches(3.45), Inches(y), Inches(0.08), Inches(0.95), accent)
        d.text(s, title, Inches(3.72), Inches(y + 0.13), Inches(1.0), Inches(0.28), size=10.8, color=accent, bold=True, shrink=True)
        d.text(s, body, Inches(4.85), Inches(y + 0.15), Inches(6.9), Inches(0.5), size=12.8, color=b.INK, shrink=True)
    return s


def operator_moat(d):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.text(s, "THE OPERATOR GATE IS THE MOAT", d.M, Inches(0.62), d.CW, Inches(0.35), size=13, color=b.TEAL, bold=True)
    d.text(s, "Raw AI can generate documents. The operator system asks the sharper questions.", d.M, Inches(1.15), Inches(10.5), Inches(1.2), size=23, color=b.WHITE, bold=True, shrink=True)
    questions = [
        "Is the buyer real?",
        "Is the scope honest?",
        "Is the architecture safe?",
        "Is SaaS lock-in priced?",
        "Is competitor data verified?",
        "Is done testable?",
        "Is data truth protected?",
        "Is launch reversible?",
        "Is post-launch learning disciplined?",
    ]
    for i, q in enumerate(questions):
        col = i % 3
        row = i // 3
        x = 0.8 + col * 4.15
        y = 2.45 + row * 1.05
        d.rect(s, Inches(x), Inches(y), Inches(3.55), Inches(0.9), b.NAVY_2, line=b.ACCENT, radius=0.05)
        d.text(s, q, Inches(x + 0.18), Inches(y + 0.2), Inches(3.15), Inches(0.48), size=9.5, color=b.WHITE, bold=True, shrink=True)
    return s


def proof_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, "The 52-opportunity portfolio proves breadth", "The portfolio is evidence that the same stack repeats across categories.")
    d.rect(s, Inches(0.8), Inches(1.95), Inches(3.3), Inches(3.4), b.NAVY, radius=0.08)
    d.text(s, "52", Inches(1.08), Inches(2.35), Inches(2.7), Inches(0.95), size=58, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, "implementation-reviewed opportunities", Inches(1.12), Inches(3.45), Inches(2.6), Inches(0.7), size=13.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "The catalog is proof. The operating system is the offer.", Inches(1.1), Inches(4.45), Inches(2.65), Inches(0.58), size=10.8, color=b.LIGHT_TEAL, align=PP_ALIGN.CENTER, shrink=True)
    domains = [
        "Support", "HR", "Compliance", "Security",
        "Legal", "Finance", "Healthcare", "Retail",
        "Logistics", "Marketing", "Product", "Operations",
    ]
    for i, name in enumerate(domains):
        col = i % 4
        row = i // 4
        x = 4.85 + col * 1.82
        y = 2.05 + row * 0.86
        d.rect(s, Inches(x), Inches(y), Inches(1.5), Inches(0.56), b.SOFT, line=b.GRID, radius=0.06)
        d.text(s, name, Inches(x + 0.08), Inches(y + 0.16), Inches(1.34), Inches(0.24), size=9.2, color=b.INK, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, Inches(4.85), Inches(5.05), Inches(7.1), Inches(0.6), b.LIGHT_TEAL, line=b.TEAL, radius=0.05)
    d.text(s, "Use cases sit after the 10-skill explanation, not before it.", Inches(5.05), Inches(5.16), Inches(6.65), Inches(0.34), size=11.5, color=b.DARK_TEAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    return s


def claims_slide(d):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.header(s, "Claim what is proven; caveat what is not", "This protects the deck from overclaiming market mapping completeness.")
    d.rect(s, Inches(0.9), Inches(2.0), Inches(5.45), Inches(3.45), b.LIGHT_TEAL, line=b.TEAL, radius=0.05)
    d.text(s, "Strong claim", Inches(1.2), Inches(2.3), Inches(4.8), Inches(0.3), size=18, color=b.DARK_TEAL, bold=True)
    d.text(s, "We have a complete 10-skill operator stack and 52 implementation-reviewed opportunities that demonstrate repeatability.", Inches(1.2), Inches(2.9), Inches(4.75), Inches(1.35), size=15.5, color=b.INK, bold=True, shrink=True)
    d.rect(s, Inches(7.0), Inches(2.0), Inches(5.45), Inches(3.45), b.SOFT, line=b.GRID, radius=0.05)
    d.text(s, "Careful claim", Inches(7.3), Inches(2.3), Inches(4.8), Inches(0.3), size=18, color=b.AMBER, bold=True)
    d.text(s, "Competitor teardown is a required Skill #6 gate. External publication needs source-backed incumbent and pricing evidence per use case.", Inches(7.3), Inches(2.9), Inches(4.75), Inches(1.42), size=15, color=b.INK, bold=True, shrink=True)
    return s


def offer_slide(d):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.text(s, "THE MARKET-FACING OFFER", d.M, Inches(0.64), d.CW, Inches(0.35), size=13, color=b.TEAL, bold=True)
    d.text(s, "Do not sell vague AI transformation. Do not start by selling a build.", d.M, Inches(1.25), Inches(9.5), Inches(1.0), size=25, color=b.WHITE, bold=True, shrink=True)
    steps = ["Validate", "Scope", "Architect", "Decide", "Gate ROI", "Teardown", "QA", "Wire Data", "Deploy", "Iterate"]
    for i, step in enumerate(steps):
        x = 0.72 + (i % 5) * 2.48
        y = 2.75 + (i // 5) * 1.08
        d.rect(s, Inches(x), Inches(y), Inches(2.0), Inches(0.66), b.NAVY_2, line=b.TEAL if i in [0, 9] else b.ACCENT, radius=0.06)
        d.text(s, step, Inches(x + 0.12), Inches(y + 0.2), Inches(1.76), Inches(0.28), size=9.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "Bring the operating system to the table on day one.", d.M, Inches(5.55), Inches(8.6), Inches(0.56), size=18, color=b.GOLD, bold=True, shrink=True)
    return s


def close_slide(d):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.text(s, "CLOSING THESIS", d.M, Inches(0.76), d.CW, Inches(0.35), size=13, color=b.TEAL, bold=True)
    lines = [
        ("The 52 opportunities", "prove market surface."),
        ("The 10 skills", "prove execution discipline."),
        ("The human gates", "prove this is more than prompt automation."),
    ]
    for i, (lead, rest) in enumerate(lines):
        y = 1.65 + i * 1.35
        d.rect(s, d.M, Inches(y), Inches(0.1), Inches(0.82), b.GOLD if i == 0 else b.TEAL)
        d.text(s, lead, Inches(0.9), Inches(y + 0.05), Inches(3.3), Inches(0.3), size=18, color=b.WHITE, bold=True, shrink=True)
        d.text(s, rest, Inches(5.25), Inches(y + 0.05), Inches(5.3), Inches(0.48), size=15.5, color=b.LIGHT_TEAL, shrink=True)
    d.text(s, "Draft status: corrected storyline, visual QA required before final delivery.", d.M, Inches(6.72), Inches(8.5), Inches(0.24), size=10.5, color=b.MUTED)
    return s


def main():
    d = Deck(footer=FOOTER)
    slides = []
    slides.append(cover(d))
    slides.append(thesis_slide(d))
    slides.append(cost_slide(d))
    slides.append(flow_slide(d))
    for item in skills:
        slides.append(skill_slide(d, item))
    slides.append(operator_moat(d))
    slides.append(proof_slide(d))
    slides.append(claims_slide(d))
    slides.append(offer_slide(d))
    slides.append(close_slide(d))

    total = len(slides)
    for idx, slide in enumerate(slides, 1):
        if idx not in {1, total}:
            add_footer(d, slide, idx, total, dark=False)

    d.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
