#!/usr/bin/env python3
"""Build the client-ready Agent Replacement Scorecard AEO deck."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_DIR = Path("/home/shekerk/.claude/skills/branded-pptx-deck")
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from pptxkit import Deck, Inches, PP_ALIGN  # noqa: E402


RUN = Path(__file__).resolve().parents[1]
OUT = RUN / "final" / "agent-replacement-scorecard-aeo-client-reviewed.pptx"
FOOTER = "Agent Replacement Scorecard AEO | Reviewed draft | 2026-06-29"


def load_status() -> dict:
    return json.loads((RUN / "qa" / "evidence_sprint_status.json").read_text(encoding="utf-8"))


def bullets(items: list[str], size: int = 14) -> list[dict]:
    return [{"text": item, "bullet": True, "size": size, "space_before": 7} for item in items]


def chip(d: Deck, s, x, y, w, label, fill, color=None):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(0.36), fill, radius=0.12)
    d.text(
        s,
        label,
        Inches(x + 0.12),
        Inches(y + 0.075),
        Inches(w - 0.24),
        Inches(0.18),
        size=9.5,
        color=color or b.WHITE,
        bold=True,
        align=PP_ALIGN.CENTER,
        shrink=True,
    )


def card(d: Deck, s, x, y, w, h, title, body, accent=None, title_size=15, body_size=12.2):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(h), b.WHITE, line=b.GRID, radius=0.05, shadow=True)
    if accent:
        d.rect(s, Inches(x), Inches(y), Inches(0.08), Inches(h), accent)
    d.text(s, title, Inches(x + 0.22), Inches(y + 0.22), Inches(w - 0.42), Inches(0.38),
           size=title_size, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, Inches(x + 0.22), Inches(y + 0.72), Inches(w - 0.42), Inches(h - 0.92),
           size=body_size, color=b.INK, shrink=True)


def kpi(d: Deck, s, x, y, w, value, label, note, fill=None):
    b = d.b
    d.rect(s, Inches(x), Inches(y), Inches(w), Inches(1.15), fill or b.NAVY, radius=0.06)
    d.text(s, value, Inches(x + 0.18), Inches(y + 0.15), Inches(w - 0.36), Inches(0.34),
           size=21, color=b.GOLD, bold=True, shrink=True)
    d.text(s, label, Inches(x + 0.18), Inches(y + 0.52), Inches(w - 0.36), Inches(0.28),
           size=9.2, color=b.WHITE, bold=True, shrink=True)
    d.text(s, note, Inches(x + 0.18), Inches(y + 0.82), Inches(w - 0.36), Inches(0.24),
           size=7.8, color=b.LIGHT_TEAL, shrink=True)


def verdict_box(d: Deck, s, x, y, title, body, color):
    card(d, s, x, y, 2.9, 1.38, title, body, color, title_size=14.5, body_size=11.1)


def build() -> Path:
    status = load_status()
    counts = status["counts"]
    gates = status["gates"]

    d = Deck(footer=FOOTER)
    b = d.b
    total = 10

    # 1. Cover
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(11.25), 0, Inches(2.08), d.H, b.NAVY_2)
    d.rect(s, Inches(11.25), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "CLIENT READY DECISION DECK", d.M, Inches(0.86), Inches(6.5), Inches(0.28),
           size=13, color=b.TEAL, bold=True)
    d.text(s, "Agent Replacement\nScorecard", d.M, Inches(1.28), Inches(9.7), Inches(1.18),
           size=33, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "AEO evidence readout and v0 product blueprint", d.M, Inches(2.34), Inches(8.2), Inches(0.45),
           size=18, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, d.M, Inches(3.04), Inches(1.9), Inches(0.06), b.TEAL)
    d.text(
        s,
        "Reviewed draft based on partial evidence: 88 Reddit buyer-language rows and 10 independent AI-answer captures.",
        d.M,
        Inches(3.38),
        Inches(7.9),
        Inches(0.65),
        size=15.2,
        color=b.WHITE,
        shrink=True,
    )
    chip(d, s, 0.6, 4.42, 1.9, "PARTIAL EVIDENCE", b.GOLD, b.NAVY)
    chip(d, s, 2.7, 4.42, 1.35, "AEO", b.TEAL, b.NAVY)
    chip(d, s, 4.25, 4.42, 2.15, "SCORECARD V0", b.NAVY_2)
    d.text(s, "2026-06-29", d.M, Inches(6.74), Inches(2.1), Inches(0.28), size=10.5, color=b.LIGHT_TEAL)
    d.footer(s, 1, total, dark=True)

    # 2. Executive BLUF
    s = d.slide(fill=b.SOFT)
    d.header(s, "BLUF: the wedge is layer compression", "The evidence supports a sharper claim than generic SaaS replacement.")
    d.rect(s, d.M, Inches(1.86), d.CW, Inches(1.22), b.NAVY, radius=0.04)
    d.text(
        s,
        "AI agents compress workflow layers first. Systems of record, governed data, permissions, and audit trails remain defensible.",
        Inches(0.9),
        Inches(2.08),
        Inches(11.6),
        Inches(0.62),
        size=18,
        color=b.WHITE,
        bold=True,
        shrink=True,
    )
    card(d, s, 0.75, 3.35, 3.75, 2.35, "Situation",
         "Buyers are asking whether agents can replace, reduce, or renegotiate SaaS workflows.", b.TEAL)
    card(d, s, 4.78, 3.35, 3.75, 2.35, "Insight",
         "The useful unit of analysis is the exposed workflow layer, not the whole vendor.", b.GOLD)
    card(d, s, 8.8, 3.35, 3.75, 2.35, "Recommendation",
         "Launch a v0 diagnostic that scores replacement, renegotiation, enrichment, or avoid.", b.ACCENT)
    d.footer(s, 2, total)

    # 3. Evidence posture
    s = d.slide(fill=b.WHITE)
    d.header(s, "Evidence is useful, but not complete", "Treat this as a reviewed draft; do not claim full AEO validation yet.")
    kpi(d, s, 0.75, 1.85, 2.35, str(counts["reddit_buyer_language_rows"]), "Reddit rows", "Buyer language + objections")
    kpi(d, s, 3.35, 1.85, 2.35, str(counts["independent_ai_answer_captures"]), "AI captures", "Independent answer evidence")
    kpi(d, s, 5.95, 1.85, 2.35, str(counts["independent_answer_engines"]), "Engines", "Claude + Google AI Mode")
    kpi(d, s, 8.55, 1.85, 2.35, str(counts["pattern_candidates"]), "Patterns", "Need semantic review")
    kpi(d, s, 11.15, 1.85, 1.45, "2", "Gates open", "20 captures, 3 engines")
    d.text(s, "Gate status", d.M, Inches(3.48), Inches(2.2), Inches(0.3), size=17, color=b.NAVY, bold=True)
    gate_rows = [
        ("Reddit buyer-language minimum", gates["reddit_buyer_language_min_5"], "Passed"),
        ("20 independent AI-answer captures", gates["independent_ai_answer_captures_min_20"], "Open"),
        ("3 independent answer engines", gates["independent_answer_engines_min_3"], "Open"),
        ("No promoted target-seeded patterns", gates["no_promoted_target_seeded_patterns"], "Passed"),
    ]
    y = 3.95
    for name, passed, label in gate_rows:
        fill = b.LIGHT_TEAL if passed else b.SOFT
        border = b.TEAL if passed else b.AMBER
        d.rect(s, d.M, Inches(y), d.CW, Inches(0.48), fill, line=border, radius=0.03)
        d.text(s, name, Inches(0.82), Inches(y + 0.13), Inches(7.3), Inches(0.2), size=12.5, color=b.INK, bold=True)
        chip(d, s, 10.9, y + 0.06, 1.1, label.upper(), b.TEAL if passed else b.AMBER, b.NAVY)
        y += 0.62
    d.footer(s, 3, total)

    # 4. Pattern map
    s = d.slide(fill=b.SOFT)
    d.header(s, "Six patterns define the scorecard", "Use semantic patterns as decision logic, not keyword matching.")
    patterns = [
        ("Add-on collapse", "Assistant modules and point tools are exposed when agents absorb the task layer.", b.TEAL),
        ("Human sign-off boundary", "Regulated, ambiguous, sensitive, or high-risk work needs explicit accountability.", b.AMBER),
        ("Data moat survival", "Systems survive when proprietary context, records, permissions, or audit trails matter.", b.ACCENT),
        ("Pilotability", "Replacement claims need bounded tests against historical work and measurable outcomes.", b.GOLD),
        ("Renewal leverage", "Agent performance changes seat counts, add-ons, pricing, and procurement pressure.", b.CORAL),
        ("Seat compression", "Fewer users need to sit inside the SaaS interface to complete the same workflow.", b.DARK_TEAL),
    ]
    for i, (title, body, color) in enumerate(patterns):
        x = 0.72 + (i % 3) * 4.18
        y = 1.78 + (i // 3) * 2.08
        card(d, s, x, y, 3.72, 1.55, title, body, color, title_size=14.2, body_size=10.9)
    d.rect(s, d.M, Inches(6.15), d.CW, Inches(0.52), b.NAVY, radius=0.04)
    d.text(s, "Client implication: the product should score exposed layers and survivable layers separately.",
           Inches(0.9), Inches(6.31), Inches(11.4), Inches(0.2), size=13.5, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 4, total)

    # 5. Scorecard model
    s = d.slide(fill=b.WHITE)
    d.header(s, "The v0 scorecard has five decision dimensions", "Each dimension turns evidence into a client-facing diagnostic output.")
    dimensions = [
        ("1", "Workflow determinism", "Repeatable, rule-bound, high-volume work is more exposed."),
        ("2", "Data moat", "Owned records, permissions, integrations, and audit trails defend the platform."),
        ("3", "Human sign-off", "Legal, brand, customer, and financial risk preserve human accountability."),
        ("4", "Pilotability", "A credible claim needs a bounded pilot with measurable outcomes."),
        ("5", "Renewal leverage", "Seat compression and add-on collapse become procurement arguments."),
    ]
    y = 1.72
    for num, title, body in dimensions:
        d.rect(s, Inches(0.78), Inches(y), Inches(0.48), Inches(0.48), b.NAVY, radius=0.08)
        d.text(s, num, Inches(0.92), Inches(y + 0.12), Inches(0.2), Inches(0.16), size=12, color=b.WHITE, bold=True)
        d.text(s, title, Inches(1.45), Inches(y + 0.03), Inches(3.3), Inches(0.25), size=14, color=b.NAVY, bold=True)
        d.text(s, body, Inches(4.82), Inches(y + 0.03), Inches(7.6), Inches(0.34), size=11.3, color=b.INK, shrink=True)
        d.rect(s, Inches(1.45), Inches(y + 0.5), Inches(10.9), Inches(0.015), b.GRID)
        y += 0.88
    d.rect(s, d.M, Inches(6.28), d.CW, Inches(0.45), b.SOFT, line=b.GRID, radius=0.04)
    d.text(s, "Output package: exposed layer, surviving layer, human checkpoint, pilot test, and renewal talking point.",
           Inches(0.85), Inches(6.41), Inches(11.7), Inches(0.18), size=12.2, color=b.NAVY, bold=True, shrink=True)
    d.footer(s, 5, total)

    # 6. Verdict system
    s = d.slide(fill=b.SOFT)
    d.header(s, "The diagnostic should produce four verdicts", "This avoids overclaiming while still giving clients an actionable answer.")
    card(d, s, 0.85, 1.72, 5.65, 1.18, "Replace",
         "Automate the exposed workflow layer.",
         b.CORAL, title_size=14.5, body_size=11)
    card(d, s, 6.85, 1.72, 5.65, 1.18, "Renegotiate",
         "Reduce seats, add-ons, modules, or volume.",
         b.GOLD, title_size=14.5, body_size=11)
    card(d, s, 0.85, 3.12, 5.65, 1.18, "Enrich",
         "Use agents around durable platform context.",
         b.TEAL, title_size=14.5, body_size=11)
    card(d, s, 6.85, 3.12, 5.65, 1.18, "Avoid",
         "Keep humans accountable for high-risk work.",
         b.MUTED, title_size=14.5, body_size=11)
    d.text(s, "Example client deliverable", d.M, Inches(4.55), Inches(4), Inches(0.3), size=17, color=b.NAVY, bold=True)
    d.rect(s, d.M, Inches(5.0), d.CW, Inches(1.05), b.NAVY, radius=0.05)
    d.text(s, "For each workflow: score risk, name exposed/surviving layers, define checkpoint, specify pilot.",
           Inches(0.9), Inches(5.28), Inches(11.4), Inches(0.32), size=12, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 6, total)

    # 7. AEO content strategy
    s = d.slide(fill=b.WHITE)
    d.header(s, "AEO strategy: answer buyer questions", "The scorecard needs crawlable pages that match how buyers and answer engines frame the problem.")
    content = [
        ("Customer support", "Where are agents useful, where do Zendesk/Intercom seats compress, and where do humans stay?"),
        ("Document workflows", "When do summarization and drafting add-ons get replaced versus enriched?"),
        ("Pilot design", "How should teams test an AI agent before replacing a workflow tool?"),
        ("Data moats", "Which SaaS workflows survive because they own records, permissions, and governance?"),
        ("Renewal leverage", "How do teams turn agent performance into seat, add-on, and pricing negotiations?"),
    ]
    for i, (title, body) in enumerate(content):
        y = 1.78 + i * 0.86
        d.rect(s, Inches(0.78), Inches(y), Inches(2.25), Inches(0.44), b.NAVY, radius=0.04)
        d.text(s, title, Inches(0.93), Inches(y + 0.12), Inches(1.95), Inches(0.16), size=10.5, color=b.WHITE, bold=True, shrink=True)
        d.text(s, body, Inches(3.25), Inches(y + 0.06), Inches(8.95), Inches(0.3), size=11.3, color=b.INK, shrink=True)
    d.rect(s, d.M, Inches(6.25), d.CW, Inches(0.52), b.LIGHT_TEAL, line=b.TEAL, radius=0.04)
    d.text(s, "Rule: write for recommendation eligibility with examples, caveats, review boundaries, and pilot metrics.",
           Inches(0.88), Inches(6.4), Inches(11.55), Inches(0.22), size=10.9, color=b.NAVY, bold=True, shrink=True)
    d.footer(s, 7, total)

    # 8. Implementation roadmap
    s = d.slide(fill=b.SOFT)
    d.header(s, "Next 30 days: evidence into product", "Build the asset and continue capture collection in parallel.")
    roadmap = [
        ("Week 1", "Package v0 diagnostic", "Turn the five dimensions into an interactive scorecard and worksheet."),
        ("Week 2", "Publish AEO pages", "Ship non-branded pages for support, docs, data moats, pilots, and renewal leverage."),
        ("Week 3", "Expand evidence", "Add 10 more independent captures and a third answer engine."),
        ("Week 4", "Review + harden", "Promote only patterns that survive semantic review and falsification."),
    ]
    for i, (week, title, body) in enumerate(roadmap):
        x = 0.8 + i * 3.05
        d.rect(s, Inches(x), Inches(2.0), Inches(2.55), Inches(0.48), b.TEAL if i < 2 else b.AMBER, radius=0.08)
        d.text(s, week, Inches(x + 0.16), Inches(2.13), Inches(2.2), Inches(0.16), size=12, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        card(d, s, x, 2.7, 2.55, 2.35, title, body, b.NAVY, title_size=12.4, body_size=9.8)
    d.rect(s, d.M, Inches(5.85), d.CW, Inches(0.72), b.NAVY, radius=0.05)
    d.text(s, "Decision needed: launch the reviewed v0 model now; keep the evidence gate open.",
           Inches(0.9), Inches(6.08), Inches(11.5), Inches(0.24), size=14.5, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 8, total)

    # 9. Claim guardrails
    s = d.slide(fill=b.WHITE)
    d.header(s, "Claim discipline protects the strategy", "AEO work loses credibility when partial evidence is framed as full proof.")
    card(d, s, 0.78, 1.8, 5.7, 3.3, "Safe to say",
         "We have a reviewed draft based on partial evidence. The strongest supported pattern is workflow-layer compression. The v0 scorecard is ready to pilot with clients and refine through more captures.",
         b.TEAL, title_size=17, body_size=13.4)
    card(d, s, 6.85, 1.8, 5.7, 3.3, "Do not say yet",
         "Do not claim full AEO readiness, consensus across all major engines, statistical validation, or that answer engines recommend the scorecard. ChatGPT and Perplexity gates are still open.",
         b.CORAL, title_size=17, body_size=13.4)
    d.rect(s, d.M, Inches(5.75), d.CW, Inches(0.55), b.SOFT, line=b.GRID, radius=0.04)
    d.text(s, "This framing makes the deck client-ready without overstating the evidence base.",
           Inches(0.9), Inches(5.92), Inches(11.4), Inches(0.2), size=13.2, color=b.NAVY, bold=True, shrink=True)
    d.footer(s, 9, total)

    # 10. Decision ask
    s = d.slide(fill=b.NAVY)
    d.text(s, "DECISION ASK", d.M, Inches(0.75), Inches(2.2), Inches(0.28), size=13, color=b.TEAL, bold=True)
    d.text(s, "Approve the v0\nscorecard launch path", d.M, Inches(1.15), Inches(8.8), Inches(1.0),
           size=29, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.25), Inches(1.8), Inches(0.06), b.TEAL)
    asks = [
        "Use the v0 blueprint as the client-facing diagnostic model.",
        "Publish five non-branded AEO pages around buyer questions.",
        "Keep evidence status as reviewed draft until 20 captures and 3 engines pass.",
        "Run semantic review before promoting any pattern as market truth.",
    ]
    d.text(s, bullets(asks, size=13.1), d.M, Inches(2.75), Inches(7.25), Inches(2.55), color=b.WHITE, shrink=True)
    d.rect(s, Inches(8.35), Inches(2.55), Inches(3.85), Inches(2.75), b.NAVY_2, radius=0.05)
    d.text(s, "Recommended posture", Inches(8.7), Inches(2.88), Inches(3.15), Inches(0.32),
           size=15, color=b.TEAL, bold=True, shrink=True)
    d.text(s, "Launch the working model. Do not declare full evidence readiness yet.",
           Inches(8.7), Inches(3.36), Inches(3.1), Inches(1.12), size=17, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "Next gate: +10 captures + one more engine.",
           Inches(8.7), Inches(4.68), Inches(3.05), Inches(0.42), size=10.2, color=b.LIGHT_TEAL, shrink=True)
    d.footer(s, 10, total, dark=True)

    return d.save(OUT)


if __name__ == "__main__":
    build()
