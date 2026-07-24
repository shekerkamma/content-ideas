#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
KIT = Path.home() / ".claude" / "skills" / "branded-pptx-deck" / "scripts"
sys.path.insert(0, str(KIT))

from pptxkit import Deck, Brand, Inches, Pt, PP_ALIGN, RGBColor  # noqa: E402


OUT = ROOT / "storm-reports" / "ai-coding-agents-saas-implementation-consultants-reviewed.pptx"


def hx(v: str) -> RGBColor:
    v = v.lstrip("#")
    return RGBColor(int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16))


b = Brand()
d = Deck(brand=b, footer="Storm Research | Executive Briefing")


def title_slide():
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(11.95), 0, Inches(1.38), d.H, b.NAVY_2)
    d.rect(s, Inches(11.95), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "STORM RESEARCH", d.M, Inches(0.8), Inches(3.2), Inches(0.25), size=12, color=b.TEAL, bold=True)
    d.text(
        s,
        "AI coding agents compress implementation labor,\nnot SaaS consulting accountability",
        d.M,
        Inches(1.2),
        Inches(9.2),
        Inches(1.75),
        size=28,
        color=b.WHITE,
        bold=True,
        font=b.FONT_H,
        shrink=True,
    )
    d.text(
        s,
        "Executive takeaway: the first pressure is on repetitive build work and junior delivery hours; the durable value stays in validation, adoption, and cutover risk ownership.",
        d.M,
        Inches(3.1),
        Inches(8.8),
        Inches(0.8),
        size=15,
        color=b.LIGHT_TEAL,
        shrink=True,
    )
    for i, (lab, txt, color) in enumerate([
        ("WHAT CHANGED", "Agents now handle more of the repetitive delivery layer.", b.TEAL),
        ("WHAT STAYS", "Human accountability still owns business correctness.", b.GOLD),
        ("WHAT TO DO", "Reprice around outcomes, not raw hours.", b.CORAL),
    ]):
        x = Inches(0.7) + Inches(2.5) * i
        d.rect(s, x, Inches(5.45), Inches(2.2), Inches(1.05), b.NAVY_2, line=b.TEAL)
        d.text(s, lab, x + Inches(0.18), Inches(5.62), Inches(1.8), Inches(0.16), size=9, color=color, bold=True)
        d.text(s, txt, x + Inches(0.18), Inches(5.84), Inches(1.82), Inches(0.48), size=14, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 1, 8, dark=True)


def executive_summary():
    s = d.slide(fill=b.SOFT)
    d.header(s, "The answer is compression, not replacement", "Executive summary for SaaS / AI services leaders")
    cards = [
        ("What changed", "Agents can now accelerate config, migration scaffolds, test generation, and documentation.", b.TEAL),
        ("What still matters", "Implementation still fails on semantics, permissions, validation, adoption, and cutover risk.", b.GOLD),
        ("Commercial impact", "The model shifts from selling hours to selling outcome ownership and risk reduction.", b.CORAL),
    ]
    xs = [Inches(0.7), Inches(4.33), Inches(7.96)]
    for (title, body, color), x in zip(cards, xs):
        d.rect(s, x, Inches(1.95), Inches(3.42), Inches(2.6), b.WHITE, line=b.GRID, radius=0.06, shadow=True)
        d.rect(s, x, Inches(1.95), Inches(3.42), Inches(0.1), color)
        d.text(s, title, x + Inches(0.18), Inches(2.15), Inches(2.8), Inches(0.26), size=18, color=b.INK, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.18), Inches(2.55), Inches(2.95), Inches(1.2), size=15, color=b.MUTED, shrink=True)
    d.rect(s, Inches(0.7), Inches(5.0), Inches(11.93), Inches(0.62), b.NAVY)
    d.text(s, "Bottom line", Inches(0.92), Inches(5.12), Inches(1.0), Inches(0.16), size=10, color=b.TEAL, bold=True)
    d.text(s, "Buy less manual effort. Buy more outcome ownership.", Inches(1.75), Inches(5.05), Inches(10.0), Inches(0.3), size=16.5, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 2, 8)


def storyboard():
    s = d.slide(fill=b.WHITE)
    d.header(s, "The story unfolds in four beats", "Storyboard for the argument")
    beats = [
        ("1", "Shift", "AI lowers the cost of producing implementation artifacts.", b.TEAL),
        ("2", "Limit", "The hard part remains judgment, governance, and sign-off.", b.GOLD),
        ("3", "Impact", "Margin pressure hits repetitive delivery work first.", b.CORAL),
        ("4", "Response", "Reprice around outcomes and build validation gates.", b.ACCENT),
    ]
    x = Inches(0.72)
    for idx, (num, title, body, color) in enumerate(beats):
        d.rect(s, x, Inches(2.0), Inches(2.48), Inches(2.08), b.SOFT, line=b.GRID, radius=0.05)
        d.rect(s, x, Inches(2.0), Inches(2.48), Inches(0.1), color)
        d.text(s, num, x + Inches(0.15), Inches(2.15), Inches(0.4), Inches(0.2), size=22, color=color, bold=True)
        d.text(s, title, x + Inches(0.15), Inches(2.48), Inches(1.9), Inches(0.2), size=16, color=b.INK, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.15), Inches(2.82), Inches(2.12), Inches(0.95), size=13.5, color=b.MUTED, shrink=True)
        d.text(s, "→" if idx < 3 else " ", x + Inches(2.2), Inches(2.88), Inches(0.2), Inches(0.2), size=24, color=b.MUTED, bold=True)
        x += Inches(2.85)
    d.rect(s, Inches(0.7), Inches(4.7), Inches(11.95), Inches(1.05), b.NAVY)
    d.text(s, "Storyboard verdict", Inches(0.95), Inches(4.9), Inches(1.6), Inches(0.16), size=10, color=b.TEAL, bold=True)
    d.text(s, "Agents reduce delivery cost, but they do not remove accountable human ownership.", Inches(0.95), Inches(5.08), Inches(10.0), Inches(0.38), size=17, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 3, 8)


def evidence():
    s = d.slide(fill=b.SOFT)
    d.header(s, "The evidence is strongest where work is bounded", "Why the replacement claim is too broad")
    d.text(s, "Bounded tasks", Inches(0.85), Inches(1.85), Inches(4.2), Inches(0.2), size=18, color=b.TEAL, bold=True)
    d.text(s, "Messy implementations", Inches(7.0), Inches(1.85), Inches(4.2), Inches(0.2), size=18, color=b.CORAL, bold=True)
    left = [
        "Copilot and BCG-style studies show strong gains on narrow tasks.",
        "Agents can produce migration scaffolds, tests, and docs quickly.",
        "The productivity lift is real when the task is testable.",
    ]
    right = [
        "SaaS implementations fail on exceptions, permissions, and meaning.",
        "Validation and cutover still require human review.",
        "Performance degrades as context and accountability increase.",
    ]
    for i, txt in enumerate(left):
        d.rect(s, Inches(0.85), Inches(2.25 + i * 0.55), Inches(5.15), Inches(0.38), b.WHITE, line=b.GRID, radius=0.03)
        d.text(s, txt, Inches(1.02), Inches(2.33 + i * 0.55), Inches(4.75), Inches(0.18), size=13.5, color=b.INK, shrink=True)
    for i, txt in enumerate(right):
        d.rect(s, Inches(7.0), Inches(2.25 + i * 0.55), Inches(5.45), Inches(0.38), b.WHITE, line=b.GRID, radius=0.03)
        d.text(s, txt, Inches(7.17), Inches(2.33 + i * 0.55), Inches(5.05), Inches(0.18), size=13.5, color=b.INK, shrink=True)
    d.rect(s, Inches(0.85), Inches(4.55), Inches(11.6), Inches(0.95), b.NAVY_2, line=b.NAVY_2)
    d.text(s, "Implication", Inches(1.05), Inches(4.72), Inches(1.0), Inches(0.16), size=10, color=b.GOLD, bold=True)
    d.text(s, "Use AI to accelerate artifacts. Keep humans accountable for the result.", Inches(1.05), Inches(4.88), Inches(9.8), Inches(0.34), size=16.5, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 4, 8)


def commercial_impact():
    s = d.slide(fill=b.WHITE)
    d.header(s, "Junior build hours are the first thing to reprice", "Commercial impact on consulting economics")
    rows = [
        ("Junior config / build", "High exposure", "First to compress", b.CORAL),
        ("Migration scaffolding", "High exposure", "Use agents as accelerators", b.CORAL),
        ("Validation / UAT", "Medium exposure", "Keep human gates", b.GOLD),
        ("Process design / adoption", "Low exposure", "Value shifts upward", b.TEAL),
        ("Outcome pricing", "Strategic lever", "Protect margin", b.ACCENT),
    ]
    y = 2.0
    for a, b1, c, color in rows:
        d.rect(s, Inches(0.82), Inches(y), Inches(11.65), Inches(0.54), b.SOFT, line=b.GRID, radius=0.03)
        d.rect(s, Inches(0.82), Inches(y), Inches(0.12), Inches(0.54), color)
        d.text(s, a, Inches(1.05), Inches(y + 0.13), Inches(2.8), Inches(0.16), size=15, color=b.INK, bold=True)
        d.text(s, b1, Inches(4.2), Inches(y + 0.13), Inches(1.7), Inches(0.16), size=13.5, color=b.MUTED)
        d.text(s, c, Inches(7.4), Inches(y + 0.13), Inches(3.8), Inches(0.16), size=13.5, color=b.INK, bold=True, shrink=True)
        y += 0.68
    d.rect(s, Inches(0.82), Inches(5.7), Inches(11.65), Inches(0.6), b.NAVY)
    d.text(s, "Executive call", Inches(1.05), Inches(5.82), Inches(1.0), Inches(0.15), size=10, color=b.TEAL, bold=True)
    d.text(s, "The model changes before the category disappears.", Inches(2.0), Inches(5.72), Inches(9.2), Inches(0.2), size=18, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 5, 8)


def operating_response():
    s = d.slide(fill=b.SOFT)
    d.header(s, "Winning firms package outcomes, not effort", "What leaders should do now")
    items = [
        "Stop selling raw build hours as the product.",
        "Use agents for first-pass mapping, config diffs, and documentation.",
        "Build reusable implementation playbooks and validators.",
        "Price for risk reduction, milestones, and acceptance.",
        "Train consultants as agent supervisors and translators.",
    ]
    for i, txt in enumerate(items):
        d.rect(s, Inches(0.85), Inches(2.02 + i * 0.72), Inches(11.58), Inches(0.48), b.WHITE, line=b.GRID, radius=0.03)
        d.text(s, f"{i+1:02d}", Inches(1.02), Inches(2.13 + i * 0.72), Inches(0.4), Inches(0.16), size=12, color=b.TEAL, bold=True)
        d.text(s, txt, Inches(1.65), Inches(2.1 + i * 0.72), Inches(10.35), Inches(0.18), size=15, color=b.INK, bold=True, shrink=True)
    d.rect(s, Inches(0.85), Inches(5.75), Inches(11.58), Inches(0.55), b.NAVY_2)
    d.text(s, "Takeaway", Inches(1.05), Inches(5.88), Inches(1.0), Inches(0.14), size=10, color=b.GOLD, bold=True)
    d.text(s, "Turn AI into throughput while keeping human ownership of outcomes.", Inches(1.9), Inches(5.8), Inches(9.1), Inches(0.24), size=17, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 6, 8)


def claim_safety():
    s = d.slide(fill=b.WHITE)
    d.header(s, "Keep the claim discipline tight", "What to say, what to soften, what to avoid")
    cols = [
        ("SAFE TO ASSERT", b.TEAL, [
            "AI tools are strong on bounded tasks.",
            "Current agents are reliability-limited.",
            "Governance and prompt-injection risks remain real.",
        ]),
        ("SAY WITH A CAVEAT", b.GOLD, [
            "Consulting labor will compress first in junior work.",
            "Historical analogies support role migration, not certainty.",
            "Market-size signals support margin pressure.",
        ]),
        ("DO NOT ASSERT", b.CORAL, [
            "Agents will replace consultants outright.",
            "Demo speed equals production ownership.",
            "Secondary market figures are primary proof.",
        ]),
    ]
    x = Inches(0.85)
    for title, color, items in cols:
        d.rect(s, x, Inches(2.05), Inches(3.64), Inches(2.9), b.SOFT, line=b.GRID, radius=0.04)
        d.rect(s, x, Inches(2.05), Inches(3.64), Inches(0.1), color)
        d.text(s, title, x + Inches(0.15), Inches(2.18), Inches(3.0), Inches(0.16), size=11, color=color, bold=True)
        for j, item in enumerate(items):
            d.text(s, item, x + Inches(0.18), Inches(2.52 + j * 0.58), Inches(3.15), Inches(0.34), size=13.2, color=b.INK, shrink=True)
        x += Inches(3.94)
    d.footer(s, 7, 8)


def close():
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(0), Inches(0), d.W, Inches(0.18), b.TEAL)
    d.text(s, "THE ASK", d.M, Inches(1.0), Inches(1.5), Inches(0.2), size=12, color=b.TEAL, bold=True)
    d.text(s, "Reprice the implementation business around outcomes and accountability.", d.M, Inches(1.45), Inches(10.9), Inches(1.5), size=28, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "The firms that win will combine automation with explicit human ownership of business results.", d.M, Inches(3.25), Inches(10.0), Inches(0.6), size=16, color=b.LIGHT_TEAL, shrink=True)
    d.rect(s, Inches(0.7), Inches(5.55), Inches(11.9), Inches(0.75), b.NAVY_2)
    d.text(s, "Decision", Inches(0.95), Inches(5.73), Inches(0.8), Inches(0.16), size=10, color=b.GOLD, bold=True)
    d.text(s, "Use agents to compress delivery cost. Keep humans accountable for the result.", Inches(1.75), Inches(5.67), Inches(10.6), Inches(0.2), size=18, color=b.WHITE, bold=True, shrink=True)
    d.footer(s, 8, 8, dark=True)


title_slide()
executive_summary()
storyboard()
evidence()
commercial_impact()
operating_response()
claim_safety()
close()

d.save(OUT)
