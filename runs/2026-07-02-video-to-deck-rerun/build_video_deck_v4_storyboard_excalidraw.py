#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path("/home/shekerk/content-ideas")
RUN = ROOT / "runs/2026-07-02-video-to-deck-rerun"
sys.path.insert(0, str(ROOT / "skills/branded-pptx-deck/scripts"))
from pptxkit import Deck, Inches, PP_ALIGN, RGBColor

OUT = RUN / "ai-agents-new-saas-video-deck-v4-storyboard-excalidraw-draft.pptx"

STORY = [
    ("00:00", "Intro", "AI Agents Are The New SaaS", "v3-thesis-workflow",
     "Agent SaaS sells work as a service; the product is the job itself, priced like labor.",
     ["Core shift: buyer pays for completed work, not software access.", "Implication: package a narrow job before building a broad platform."]),
    ("01:38", "1. The Product Is The Job", "SaaS sells software; agent SaaS sells completed work", "v3-market-context",
     "Package a job the customer's team can hand off entirely, then sell the outcome as a service.",
     ["Claim: the job becomes the product surface.", "Builder move: define the outcome, SLA, handoff, and exception policy."]),
    ("01:38", "2. Real Examples", "Slang AI and Same Day make the pattern concrete", "v3-wedge-examples",
     "Restaurants, home services, property services, and contact centers show where annoying jobs already have budget.",
     ["Named proof: reception, dispatch, reservation, and triage workflows already have spend.", "Pattern: beat junior labor on speed, consistency, and cost."]),
    ("04:11", "3. Pick A Workflow With A Paycheck", "Start with money already flowing to a role", "v3-workflow-scorecard",
     "Score frequency, pain, finish-line clarity, software touchpoints, edge cases, and budget owner.",
     ["Decision rule: no budget owner, no wedge.", "First rep: one niche, 20 annoying jobs, score before building."]),
    ("06:12", "4. Shadow The Human First", "Watch 10-20 real jobs before writing a prompt", "v3-shadow-human",
     "The hidden workflow is what they check, where mistakes happen, and what makes cases weird.",
     ["The detail is the product: hidden checks, weird cases, approvals.", "Output: trigger, context, tools, actions, approvals, escalation, success."]),
    ("09:34", "5. Build The Minimum Useful Agent", "Earn autonomy one bounded loop at a time", "v3-smallest-agent",
     "Start with draft-and-approve, triage, coordinator, or bounded action before adding judgment.",
     ["Scope discipline: start as assistive, then earn autonomy.", "Good first shapes: draft, triage, coordinate, bounded action."]),
    ("12:50", "6. Product Wrapper And Evals", "The wrapper turns automation into SaaS", "v3-wrapper-saas",
     "Logs, approvals, controls, handoff rules, analytics, and evals create the trust customers pay for.",
     ["Trust is the product wrapper, not a nice-to-have.", "Build evals from 50 real examples and improve like a gym."]),
    ("15:50", "7. Sell The Pilot Like Labor", "Three customers, one niche, one outcome", "v3-pilot-productize",
     "Charge setup plus monthly first, then move toward usage or outcome pricing as value becomes clear.",
     ["Sell the outcome first; productize after repetition appears.", "Pricing path: setup + monthly -> usage -> outcome pricing."]),
    ("18:37", "8. Own The Workflow", "The moat is the operating loop", "v3-own-workflow",
     "Context, policy, exceptions, and evals become the product's defensibility.",
     ["Moat: accumulated workflow context and exception handling.", "Defensibility comes from owning the operating loop end to end."]),
    ("21:45", "Distribution And 30-Day Plan", "Win attention with workflow teardowns", "v4-zero-to-100-plan",
     "Show the painful old way, show the smooth agent way, publish proof, then put ads behind winners.",
     ["Distribution asset: old way vs agent way teardown.", "30-day motion: niche, shadow, agent, pilots, 50 proof posts."]),
    ("24:14", "Closing Thoughts", "Start with the job; build the agent people pay for", "v3-coverage-map",
     "Dense hyperframes are accounted for; presenter-only frames are excluded from main slides.",
     ["Final recommendation: stop brainstorming agents; choose a paid job.", "Deck audit: screen changes are captured, grouped, and redrawn."]),
]


def hx(s):
    s = s.strip("#")
    return RGBColor(int(s[:2], 16), int(s[2:4], 16), int(s[4:], 16))


def board_path(slug):
    p = RUN / f"ai-agents-new-saas-{slug}.png"
    if not p.exists():
        raise FileNotFoundError(p)
    return p


def source_path(slug):
    return RUN / f"ai-agents-new-saas-{slug}.excalidraw"


def add_story_slide(d, idx, total, ts, section, title, slug, note, bullets):
    b = d.b
    s = d.slide(fill=b.WHITE)
    d.text(s, section.upper(), d.M, Inches(0.25), Inches(6.5), Inches(0.22),
           size=9.5, color=b.DARK_TEAL, bold=True, shrink=True)
    d.text(s, title, d.M, Inches(0.58), Inches(11.2), Inches(0.44),
           size=22, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.08), Inches(1.15), Inches(0.045), b.TEAL)
    s.shapes.add_picture(str(board_path(slug)), Inches(0.72), Inches(1.30), width=Inches(8.15))
    d.rect(s, Inches(9.18), Inches(1.35), Inches(3.35), Inches(4.78), hx("F4F7F8"), line=b.GRID, radius=0.07)
    d.text(s, "Synthesis", Inches(9.42), Inches(1.64), Inches(2.85), Inches(0.22),
           size=12.3, color=b.DARK_TEAL, bold=True, shrink=True)
    d.text(s, note, Inches(9.42), Inches(2.02), Inches(2.80), Inches(0.90),
           size=10.2, color=b.NAVY, bold=True, shrink=True)
    d.text(s, [{"text": item, "bullet": True, "space_before": 7, "size": 9.5} for item in bullets],
           Inches(9.42), Inches(3.18), Inches(2.78), Inches(2.35), size=9.5, color=b.INK, shrink=True)
    d.text(s, f"Editable source: {source_path(slug).name}",
           d.M, Inches(6.88), Inches(8.8), Inches(0.16), size=7.3, color=b.MUTED, shrink=True)
    d.text(s, f"{idx} / {total}", d.W - Inches(1.25), Inches(6.86), Inches(0.75), Inches(0.20),
           size=9.2, color=b.MUTED, bold=True, align=PP_ALIGN.RIGHT)


def build():
    d = Deck(footer="")
    total = len(STORY) + 1

    s = d.slide(fill=d.b.NAVY)
    d.text(s, "VIDEO-TO-DECK V4", d.M, Inches(0.68), Inches(4.6), Inches(0.24),
           size=11, color=d.b.TEAL, bold=True)
    d.text(s, "AI Agents Are The New SaaS", d.M, Inches(1.20), Inches(8.8), Inches(0.70),
           size=35, color=d.b.WHITE, bold=True, shrink=True)
    d.text(s, "Storyboard rebuilt from transcript notes, dense hyperframes, screen-change captures, and Excalidraw-created visuals.",
           d.M, Inches(2.12), Inches(7.7), Inches(0.42), size=14.4, color=hx("DCE6EF"), shrink=True)
    timeline = [
        "Intro", "Product is the job", "Workflow selection", "Shadow first",
        "Minimum agent", "Wrapper + evals", "Pilot pricing", "Own workflow", "30-day plan"
    ]
    for i, item in enumerate(timeline):
        x = Inches(0.78 + (i % 3) * 3.45)
        y = Inches(3.20 + (i // 3) * 0.68)
        d.rect(s, x, y, Inches(2.55), Inches(0.40), hx("12243A"), radius=0.08)
        d.text(s, item, x + Inches(0.12), y + Inches(0.12), Inches(2.3), Inches(0.12),
               size=9, color=d.b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, f"1 / {total}", d.W - Inches(1.25), Inches(6.86), Inches(0.75), Inches(0.20),
           size=9.2, color=hx("AAB6C4"), bold=True, align=PP_ALIGN.RIGHT)

    for idx, item in enumerate(STORY, 2):
        add_story_slide(d, idx, total, *item)

    d.save(OUT)


if __name__ == "__main__":
    build()
