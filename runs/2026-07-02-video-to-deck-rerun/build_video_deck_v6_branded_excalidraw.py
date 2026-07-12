#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path("/home/shekerk/content-ideas")
RUN = ROOT / "runs/2026-07-02-video-to-deck-rerun"
sys.path.insert(0, str(ROOT / "skills/branded-pptx-deck/scripts"))

from pptxkit import Deck, Inches, PP_ALIGN, RGBColor

OUT = RUN / "ai-agents-new-saas-video-deck-v6-branded-excalidraw-draft.pptx"


def hx(s):
    s = s.strip("#")
    return RGBColor(int(s[:2], 16), int(s[2:4], 16), int(s[4:], 16))


VISUALS = [
    {
        "section": "Market Context",
        "title": "Agent SaaS is a packaging shift from software access to completed work",
        "slug": "v3-market-context",
        "claim": "The buyer logic changes when the output is a completed workflow rather than another seat of software.",
        "points": ["SaaS sold tools and usage.", "Agent SaaS sells work capacity.", "The wedge must map to budget already attached to a job."],
        "takeaway": "Start with the paid job, not the generic agent category.",
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
        "title": "Unit economics improve only when the workflow is repeated and bounded",
        "slug": "v3-unit-economics",
        "claim": "The economic promise depends on replacing repeated labor packets, not vaguely improving productivity.",
        "points": ["Labor spend sets the price anchor.", "Frequency creates learning data.", "Boundaries keep delivery evaluable."],
        "takeaway": "The workflow must be frequent enough to learn from and valuable enough to price.",
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
        "claim": "Frequency, pain, clarity, tools, edge cases, and budget owner decide whether the idea deserves a build.",
        "points": ["Score 20 jobs in one niche.", "Reject pain with no budget owner.", "Prefer clear finish lines over open-ended judgment."],
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
        "claim": "The first version should be useful enough to sell and constrained enough to evaluate.",
        "points": ["Draft-and-approve.", "Triage.", "Coordinator.", "Bounded action."],
        "takeaway": "Earn autonomy one bounded loop at a time.",
    },
    {
        "section": "Workflow Architecture",
        "title": "Most agent products start as predictable workflows",
        "slug": "v3-agentic-workflows",
        "claim": "The architecture should expose where judgment enters, where tools are called, and where humans approve.",
        "points": ["Predictable path first.", "Judgment only where it creates value.", "Escalation is part of the architecture."],
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
        "section": "Defensibility",
        "title": "Owning the workflow is the moat",
        "slug": "v3-own-workflow",
        "claim": "Workflow context, policy, exception handling, and eval memory compound into defensibility.",
        "points": ["Prompts are easy to copy.", "Operating memory is harder to replicate.", "Exceptions become product assets."],
        "takeaway": "The moat is the operating loop around the agent.",
    },
    {
        "section": "30-Day Plan",
        "title": "Use workflow teardowns to turn the build into distribution",
        "slug": "v4-zero-to-100-plan",
        "claim": "Show the painful old way, show the agent way, publish proof, and put spend behind the winners.",
        "points": ["Days 1-3: score jobs.", "Week 1-2: shadow and build.", "Week 3-4: pilot and publish."],
        "takeaway": "Distribution comes from making the painful workflow visible.",
    },
    {
        "section": "Coverage",
        "title": "Screen changes are accounted for without inserting YouTube screenshots",
        "slug": "v3-coverage-map",
        "claim": "Dense frames and scene-change frames are retained as audit material; meaningful visuals are redrawn as Excalidraw.",
        "points": ["156 dense frames.", "56 scene-change frames.", "Presenter-only and duplicates excluded."],
        "takeaway": "Hyperframes drive reconstruction; they are not the client-facing visual.",
    },
]


def img(slug):
    path = RUN / f"ai-agents-new-saas-{slug}.png"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def excalidraw(slug):
    return RUN / f"ai-agents-new-saas-{slug}.excalidraw"


def add_header(d, s, section, title):
    b = d.b
    d.rect(s, 0, 0, d.W, Inches(0.14), b.TEAL)
    d.text(s, section.upper(), d.M, Inches(0.24), Inches(4.5), Inches(0.18),
           size=9.2, color=b.DARK_TEAL, bold=True, shrink=True)
    d.text(s, title, d.M, Inches(0.52), d.CW, Inches(0.58),
           size=22.5, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.18), Inches(1.35), Inches(0.045), b.TEAL)


def add_footer(d, s, page, total, slug=None):
    b = d.b
    source = f"Excalidraw source: {excalidraw(slug).name}" if slug else "Video-to-deck draft"
    d.text(s, source, d.M, Inches(7.05), Inches(8.6), Inches(0.20),
           size=7.7, color=b.MUTED, shrink=True)
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
    d.text(s, "Synthesis", d.M + Inches(0.22), Inches(1.78), Inches(2.50), Inches(0.18),
           size=12.0, color=b.DARK_TEAL, bold=True, shrink=True)
    d.text(s, item["claim"], d.M + Inches(0.22), Inches(2.18), Inches(2.62), Inches(0.94),
           size=10.1, color=b.NAVY, bold=True, shrink=True)
    bullet_text(d, s, item["points"], d.M + Inches(0.22), Inches(3.42), Inches(2.60), Inches(1.50))
    d.rect(s, d.M + Inches(0.22), Inches(5.35), Inches(2.60), Inches(0.22), b.WHITE, line=b.GRID, radius=0.04)
    d.text(s, "Recreated Excalidraw visual", d.M + Inches(0.34), Inches(5.42), Inches(2.35), Inches(0.08),
           size=7.8, color=b.MUTED, bold=True, align=PP_ALIGN.CENTER, shrink=True)


def build_cover(d, total):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(9.95), 0, Inches(3.38), d.H, b.NAVY_2)
    d.rect(s, Inches(9.95), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "BRANDED EXCALIDRAW VIDEO DECK", d.M, Inches(0.78), Inches(5.9), Inches(0.22),
           size=10.3, color=b.TEAL, bold=True, shrink=True)
    d.text(s, "AI Agents Are The New SaaS", d.M, Inches(1.32), Inches(8.30), Inches(0.86),
           size=35, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.36), Inches(1.45), Inches(0.055), b.TEAL)
    d.text(s, "Client-ready storyboard with visible Excalidraw recreations, concise synthesis, and hyperframe coverage.",
           d.M, Inches(2.70), Inches(7.80), Inches(0.44), size=13.2, color=hx("DCE6EF"), shrink=True)
    d.rect(s, Inches(7.78), Inches(3.42), Inches(4.42), Inches(2.20), hx("0B1118"), radius=0.06, shadow=True)
    pic = s.shapes.add_picture(str(img("v3-thesis-workflow")), Inches(7.94), Inches(3.56), width=Inches(4.10))
    if pic.top + pic.height > Inches(5.46):
        scale = (Inches(5.46) - pic.top) / pic.height
        pic.width = int(pic.width * scale)
        pic.height = int(pic.height * scale)
    d.text(s, "No YouTube screenshots used as slide visuals.", d.M, Inches(5.02), Inches(5.9), Inches(0.20),
           size=10.4, color=b.GOLD, bold=True, shrink=True)
    d.text(s, "Transcript, dense frames, scene changes, and .excalidraw sources are retained in the run folder.",
           d.M, Inches(5.36), Inches(6.9), Inches(0.24), size=9.4, color=hx("C8D3DE"), shrink=True)
    add_footer(d, s, 1, total)


def build_story_slide(d, page, total, item):
    s = d.slide(fill=d.b.WHITE)
    add_header(d, s, item["section"], item["title"])
    add_side_panel(d, s, item)
    add_visual_frame(d, s, item["slug"])
    takeaway(d, s, item["takeaway"])
    add_footer(d, s, page, total, item["slug"])
    s.notes_slide.notes_text_frame.text = (
        f"{item['section']}: {item['claim']}\n"
        f"Visible Excalidraw visual: ai-agents-new-saas-{item['slug']}.png\n"
        f"Editable source: {excalidraw(item['slug']).name}"
    )


def build():
    d = Deck(footer="")
    total = len(VISUALS) + 1
    build_cover(d, total)
    for page, item in enumerate(VISUALS, start=2):
        build_story_slide(d, page, total, item)
    d.save(OUT)


if __name__ == "__main__":
    build()
