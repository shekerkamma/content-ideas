#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path("/home/shekerk/content-ideas")
RUN = ROOT / "runs/2026-07-02-video-to-deck-rerun"
sys.path.insert(0, str(ROOT / "skills/branded-pptx-deck/scripts"))

from pptxkit import Deck, Inches, PP_ALIGN, RGBColor

OUT = RUN / "ai-agents-new-saas-video-deck-v8-validated-draft.pptx"


def hx(s):
    s = s.strip("#")
    return RGBColor(int(s[:2], 16), int(s[2:4], 16), int(s[4:], 16))


VISUALS = [
    {
        "section": "Market Context",
        "title": "Agent SaaS expands the market from software seats to work outcomes",
        "slug": "v3-market-context",
        "claim": "The transcript frames the opportunity as software moving from helping people do work to doing work with them.",
        "points": ["The market anchor is labor, not just software seats.", "The offer must map to work already being paid for.", "The first product should be narrow enough to explain."],
        "takeaway": "Start with the paid work, then package the software around it.",
    },
    {
        "section": "Core Thesis",
        "title": "The product is the job the customer can hand off",
        "slug": "v3-thesis-workflow",
        "claim": "A credible agent business owns a narrow workflow end to end: trigger, context, tools, decisions, and escalation.",
        "points": ["Paid workflow -> observed spec -> agent business.", "Narrow scope makes the offer explainable.", "Trust is designed into the handoff."],
        "takeaway": "If the job cannot be named, the agent cannot be sold.",
    },
    {
        "section": "Economics",
        "title": "The labor comparison sets the value anchor",
        "slug": "v3-unit-economics",
        "claim": "The speaker’s mental model is one annoying job done better than a junior employee, faster than an agency, and cheaper than headcount.",
        "points": ["Labor spend sets the buyer comparison.", "Repeated jobs make the promise easier to prove.", "Bounded work keeps pricing and quality visible."],
        "takeaway": "Price against the work being replaced, not abstract productivity.",
    },
    {
        "section": "Examples",
        "title": "The best wedges are boring service workflows with visible labor spend",
        "slug": "v3-wedge-examples",
        "claim": "Restaurants, home services, property operations, and contact centers show the repeatable pattern.",
        "points": ["Reception and dispatch already have budget.", "Missed work creates obvious pain.", "The buyer compares against headcount or agencies."],
        "takeaway": "Boring operations are better first markets than broad AI productivity.",
    },
    {
        "section": "Workflow Selection",
        "title": "Pick a workflow with a paycheck attached",
        "slug": "v3-workflow-scorecard",
        "claim": "The transcript’s selection rule is direct: start where people already pay an employee, agency, receptionist, coordinator, or dispatcher.",
        "points": ["Score 20 jobs in one niche.", "Use frequency, pain, finish line, tools, and budget owner.", "Prefer learnable edge cases over pure human judgment."],
        "takeaway": "No budget owner, no wedge.",
    },
    {
        "section": "Observation",
        "title": "Shadow the human before writing prompts",
        "slug": "v3-shadow-human",
        "claim": "The product spec is hidden in what operators check, where mistakes happen, and when cases become weird.",
        "points": ["Observe 10-20 real cases.", "Record tacit checks and exception paths.", "Convert observation into acceptance criteria."],
        "takeaway": "The detail is the product.",
    },
    {
        "section": "First Product",
        "title": "Build the minimum useful agent before chasing autonomy",
        "slug": "v3-smallest-agent",
        "claim": "The transcript says to start smaller than the fully autonomous employee fantasy.",
        "points": ["Draft and approve.", "Triage.", "Coordinator.", "Bounded action."],
        "takeaway": "Earn autonomy one bounded loop at a time.",
    },
    {
        "section": "Workflow Architecture",
        "title": "Most agent products start as predictable workflows",
        "slug": "v3-agentic-workflows",
        "claim": "The transcript cites the idea that many agent problems should start as workflows because workflows follow predictable paths.",
        "points": ["Predictable path first.", "Add judgment only where it creates value.", "Keep escalation explicit."],
        "takeaway": "Design the workflow before expanding the agent.",
    },
    {
        "section": "Trust Wrapper",
        "title": "The wrapper is what turns automation into SaaS",
        "slug": "v3-wrapper-saas",
        "claim": "Logs, approvals, controls, handoffs, analytics, and evals are the product layer customers pay to trust.",
        "points": ["The agent does the job.", "The control room proves what happened.", "Evals make quality improvable."],
        "takeaway": "A demo shows automation; the wrapper earns production trust.",
    },
    {
        "section": "Commercialization",
        "title": "Sell the pilot like labor, then productize the repeated loop",
        "slug": "v3-pilot-productize",
        "claim": "Early sales work when the buyer sees a familiar capacity purchase with a better operating model.",
        "points": ["Three same-niche customers.", "Setup plus monthly first.", "Usage or outcome pricing after proof."],
        "takeaway": "Productization starts after repetition appears.",
    },
    {
        "section": "Productization",
        "title": "Earn the software by doing the work first",
        "slug": "v3-own-workflow",
        "claim": "The transcript-supported productization path is to do the work, learn the repeated pattern, then build the product around it.",
        "points": ["Manual-plus-AI pilots expose the repeated pattern.", "Repeated scripts and checks become software.", "The product emerges from what customers repeatedly need."],
        "takeaway": "Productization starts after the repeated pattern is visible.",
    },
    {
        "section": "30-Day Plan",
        "title": "Use workflow teardowns to turn the build into distribution",
        "slug": "v4-zero-to-100-plan",
        "claim": "Show the painful old way, show the agent way, publish proof, and put spend behind the winners.",
        "points": ["Days 1-3: score jobs.", "Week 1-2: shadow and build.", "Week 3-4: pilot and publish."],
        "takeaway": "Distribution comes from making the painful workflow visible.",
    },
]


def img(slug):
    path = RUN / f"ai-agents-new-saas-{slug}.png"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def add_header(d, s, section, title):
    b = d.b
    d.rect(s, 0, 0, d.W, Inches(0.14), b.TEAL)
    d.text(s, section.upper(), d.M, Inches(0.24), Inches(4.5), Inches(0.18),
           size=9.2, color=b.DARK_TEAL, bold=True, shrink=True)
    d.text(s, title, d.M, Inches(0.52), d.CW, Inches(0.58),
           size=22.5, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.18), Inches(1.35), Inches(0.045), b.TEAL)


def add_footer(d, s, page, total):
    b = d.b
    d.text(s, f"{page} / {total}", d.W - Inches(1.28), Inches(7.04), Inches(0.72), Inches(0.20),
           size=9.2, color=b.MUTED, bold=True, align=PP_ALIGN.RIGHT)


def bullet_text(d, s, items, x, y, w, h):
    d.text(s, [{"text": item, "bullet": True, "space_before": 6, "size": 9.5} for item in items],
           x, y, w, h, size=9.5, color=d.b.INK, shrink=True)


def takeaway(d, s, text):
    b = d.b
    d.rect(s, Inches(0.72), Inches(6.20), Inches(11.90), Inches(0.56), b.NAVY, radius=0.05)
    d.text(s, "TAKEAWAY", Inches(0.92), Inches(6.38), Inches(0.96), Inches(0.12),
           size=8.2, color=b.GOLD, bold=True, shrink=True)
    d.text(s, text, Inches(1.92), Inches(6.34), Inches(10.35), Inches(0.18),
           size=10.6, color=b.WHITE, bold=True, shrink=True)


def add_visual_frame(d, s, slug):
    b = d.b
    d.rect(s, Inches(4.02), Inches(1.52), Inches(8.50), Inches(4.30), hx("0B1118"), radius=0.06, shadow=True)
    pic = s.shapes.add_picture(str(img(slug)), Inches(4.18), Inches(1.68), width=Inches(8.18))
    if pic.top + pic.height > Inches(5.64):
        scale = (Inches(5.64) - pic.top) / pic.height
        pic.width = int(pic.width * scale)
        pic.height = int(pic.height * scale)
    pic.left = int(Inches(4.02) + (Inches(8.50) - pic.width) / 2)


def add_side_panel(d, s, item):
    b = d.b
    d.rect(s, d.M, Inches(1.52), Inches(3.12), Inches(4.30), b.SOFT, line=b.GRID, radius=0.05, shadow=True)
    d.text(s, "Business implication", d.M + Inches(0.22), Inches(1.78), Inches(2.50), Inches(0.18),
           size=12.0, color=b.DARK_TEAL, bold=True, shrink=True)
    d.text(s, item["claim"], d.M + Inches(0.22), Inches(2.18), Inches(2.62), Inches(0.94),
           size=10.1, color=b.NAVY, bold=True, shrink=True)
    bullet_text(d, s, item["points"], d.M + Inches(0.22), Inches(3.42), Inches(2.60), Inches(1.50))


def build_cover(d, total):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(9.95), 0, Inches(3.38), d.H, b.NAVY_2)
    d.rect(s, Inches(9.95), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "EXECUTIVE BRIEFING", d.M, Inches(0.78), Inches(5.9), Inches(0.22),
           size=10.3, color=b.TEAL, bold=True, shrink=True)
    d.text(s, "AI Agents Are The New SaaS", d.M, Inches(1.32), Inches(8.30), Inches(0.86),
           size=35, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.36), Inches(1.45), Inches(0.055), b.TEAL)
    d.text(s, "A practical playbook for turning AI agents into workflow businesses.",
           d.M, Inches(2.70), Inches(7.80), Inches(0.44), size=13.2, color=hx("DCE6EF"), shrink=True)
    d.rect(s, Inches(7.78), Inches(3.42), Inches(4.42), Inches(2.20), hx("0B1118"), radius=0.06, shadow=True)
    pic = s.shapes.add_picture(str(img("v3-thesis-workflow")), Inches(7.94), Inches(3.56), width=Inches(4.10))
    if pic.top + pic.height > Inches(5.46):
        scale = (Inches(5.46) - pic.top) / pic.height
        pic.width = int(pic.width * scale)
        pic.height = int(pic.height * scale)
    d.text(s, "From product idea to sellable workflow wedge.",
           d.M, Inches(5.10), Inches(6.9), Inches(0.24), size=10.8, color=b.GOLD, bold=True, shrink=True)
    add_footer(d, s, 1, total)


def build_exec_summary(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    add_header(d, s, "Executive Summary", "Agent SaaS succeeds when it sells a finished job, not another tool")
    d.rect(s, d.M, Inches(1.52), d.CW, Inches(0.82), b.NAVY, radius=0.05)
    d.text(s, "BOTTOM LINE", d.M + Inches(0.22), Inches(1.78), Inches(1.16), Inches(0.12),
           size=8.5, color=b.GOLD, bold=True, shrink=True)
    d.text(s, "The strongest opportunity is a narrow, high-frequency workflow with budget, a clear finish line, and a trust wrapper.",
           d.M + Inches(1.48), Inches(1.72), d.CW - Inches(1.70), Inches(0.22),
           size=12.7, color=b.WHITE, bold=True, shrink=True)
    cols = [
        ("Where to play", "Choose a service workflow already funded by headcount, agencies, or outsourcing."),
        ("How to build", "Observe real operators, extract the workflow spec, and ship the smallest useful agent."),
        ("How to win", "Sell pilots like labor, then productize the repeated operating loop with controls and evals."),
    ]
    for i, (title, body) in enumerate(cols):
        x = d.M + Inches(i * 4.08)
        d.rect(s, x, Inches(2.86), Inches(3.72), Inches(1.70), b.SOFT, line=b.GRID, radius=0.05, shadow=True)
        d.rect(s, x, Inches(2.86), Inches(0.06), Inches(1.70), b.TEAL)
        d.text(s, title, x + Inches(0.22), Inches(3.12), Inches(3.22), Inches(0.20),
               size=12.2, color=b.NAVY, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.22), Inches(3.58), Inches(3.16), Inches(0.52),
               size=9.4, color=b.INK, shrink=True)
    d.rect(s, d.M, Inches(5.28), d.CW, Inches(0.64), hx("FFF4CF"), line=hx("F2D982"), radius=0.05)
    d.text(s, "DECISION", d.M + Inches(0.22), Inches(5.50), Inches(0.92), Inches(0.12),
           size=8.2, color=b.NAVY, bold=True, shrink=True)
    d.text(s, "Prioritize one niche and score 20 candidate workflows before committing build effort.",
           d.M + Inches(1.26), Inches(5.46), d.CW - Inches(1.48), Inches(0.18),
           size=11.1, color=b.NAVY, bold=True, shrink=True)
    add_footer(d, s, page, total)


def build_story_slide(d, page, total, item):
    s = d.slide(fill=d.b.WHITE)
    add_header(d, s, item["section"], item["title"])
    add_side_panel(d, s, item)
    add_visual_frame(d, s, item["slug"])
    takeaway(d, s, item["takeaway"])
    add_footer(d, s, page, total)


def build_conclusion(d, page, total):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.16), d.H, b.TEAL)
    d.text(s, "CONCLUSION", d.M, Inches(0.78), Inches(4.0), Inches(0.22),
           size=10.5, color=b.TEAL, bold=True, shrink=True)
    d.text(s, "The next move is to choose the workflow, not broaden the agent",
           d.M, Inches(1.30), Inches(9.2), Inches(0.74),
           size=32, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.25), Inches(1.42), Inches(0.055), b.TEAL)
    actions = [
        ("1", "Pick one niche", "Constrain the market before evaluating workflows."),
        ("2", "Score 20 jobs", "Prioritize frequency, pain, finish-line clarity, tools, and budget."),
        ("3", "Shadow operators", "Turn real work into the agent spec and trust model."),
        ("4", "Pilot the loop", "Sell the outcome first; productize after repetition appears."),
    ]
    for i, (num, title, body) in enumerate(actions):
        x = d.M + Inches((i % 2) * 4.75)
        y = Inches(3.10 + (i // 2) * 1.18)
        d.rect(s, x, y, Inches(4.22), Inches(0.86), b.NAVY_2, line=hx("244058"), radius=0.05)
        d.rect(s, x + Inches(0.18), y + Inches(0.20), Inches(0.38), Inches(0.34), b.TEAL, radius=0.04)
        d.text(s, num, x + Inches(0.18), y + Inches(0.30), Inches(0.38), Inches(0.08),
               size=9.4, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, title, x + Inches(0.76), y + Inches(0.18), Inches(3.10), Inches(0.18),
               size=12.0, color=b.WHITE, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.76), y + Inches(0.48), Inches(3.16), Inches(0.16),
               size=8.6, color=b.LIGHT_TEAL, shrink=True)
    d.text(s, "Winning agent businesses are built around work customers already understand, fund, and want off their plate.",
           d.M, Inches(6.34), Inches(9.8), Inches(0.24),
           size=12.6, color=b.GOLD, bold=True, shrink=True)
    add_footer(d, s, page, total)


def build():
    d = Deck(footer="")
    total = len(VISUALS) + 3
    build_cover(d, total)
    build_exec_summary(d, 2, total)
    for page, item in enumerate(VISUALS, start=3):
        build_story_slide(d, page, total, item)
    build_conclusion(d, total, total)
    d.save(OUT)


if __name__ == "__main__":
    build()
