#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path("/home/shekerk/content-ideas")
RUN = ROOT / "runs/2026-07-02-video-to-deck-rerun"

sys.path.insert(0, str(ROOT / "skills/branded-pptx-deck/scripts"))
from pptxkit import Deck, Inches, PP_ALIGN, MSO_ANCHOR, RGBColor


OUT = RUN / "ai-agents-new-saas-video-deck-editable-draft.pptx"


def bullets(items, size=14):
    return [{"text": item, "bullet": True, "space_before": 7, "size": size} for item in items]


def source(d, s, text):
    d.rect(s, d.M, Inches(6.64), d.CW, Inches(0.26), d.b.LIGHT_TEAL, radius=0.06)
    d.text(s, text, d.M + Inches(0.12), Inches(6.69), d.CW - Inches(0.24), Inches(0.15),
           size=8.2, color=d.b.DARK_TEAL, bold=True, shrink=True)


def card(d, s, x, y, w, h, title, body, fill=None, title_color=None, body_color=None):
    b = d.b
    fill = fill or b.SOFT
    title_color = title_color or b.NAVY
    body_color = body_color or b.INK
    d.rect(s, x, y, w, h, fill, line=b.GRID, radius=0.12)
    d.text(s, title, x + Inches(0.14), y + Inches(0.12), w - Inches(0.28), Inches(0.30),
           size=12.5, color=title_color, bold=True, shrink=True)
    d.text(s, body, x + Inches(0.14), y + Inches(0.48), w - Inches(0.28), h - Inches(0.58),
           size=10.6, color=body_color, shrink=True)


def arrow(d, s, x, y, label="->"):
    d.text(s, label, x, y, Inches(0.35), Inches(0.25), size=17, color=d.b.TEAL, bold=True,
           align=PP_ALIGN.CENTER)


def build():
    d = Deck(footer="Video-to-Deck | editable recreation")
    b = d.b
    total = 10

    # 1 Cover
    s = d.slide(fill=b.NAVY)
    d.text(s, "VIDEO-TO-DECK", d.M, Inches(0.78), Inches(4.0), Inches(0.30),
           size=13, color=b.TEAL, bold=True)
    d.text(s, "AI Agents Are The New SaaS", d.M, Inches(1.24), Inches(9.4), Inches(0.78),
           size=34, color=b.WHITE, bold=True, shrink=True)
    d.text(s, "Editable branded deck rebuilt from cached transcript and hyperframes.",
           d.M, Inches(2.12), Inches(8.4), Inches(0.38), size=15, color=b.SOFT, shrink=True)
    card(d, s, Inches(0.75), Inches(3.08), Inches(4.1), Inches(2.05), "Core answer",
         "The opportunity is a narrow, repeated human workflow that can be observed, specified, piloted, and productized.",
         b.NAVY_2, b.TEAL, b.WHITE)
    card(d, s, Inches(5.25), Inches(3.08), Inches(2.1), Inches(2.05), "Included",
         "7 content hyperframes\n5 talking-head frames excluded\n0 screenshots inserted",
         b.NAVY_2, b.TEAL, b.WHITE)
    card(d, s, Inches(7.75), Inches(3.08), Inches(3.95), Inches(2.05), "Deck rule",
         "Every diagram is recreated with editable PowerPoint shapes, text, and tables.",
         b.NAVY_2, b.TEAL, b.WHITE)
    d.footer(s, 1, total, dark=True)

    # 2 Hyperframe accountability
    s = d.slide(fill=b.WHITE)
    d.header(s, "All Hyperframes Are Accounted For",
             "Content frames are recreated; presenter-only frames are excluded.")
    rows = [
        ("0001", "Unit economics diagram", "Editable slide 3"),
        ("0003", "Workflow scorecard", "Editable slide 4"),
        ("0004", "Shadow/spec/trust flow", "Editable slide 5"),
        ("0006", "Agentic workflows text slide", "Editable slide 6"),
        ("0007", "Wrapper/control-room/trust", "Editable slide 7"),
        ("0008/0009", "Pilot/pricing/product pattern", "Editable slide 8"),
        ("0002, 0005, 0010+", "Talking-head only", "Excluded"),
    ]
    x0, y0 = d.M, Inches(1.78)
    widths = [Inches(1.55), Inches(5.5), Inches(4.1)]
    d.rect(s, x0, y0, sum(widths), Inches(0.38), b.NAVY, radius=0.05)
    d.text(s, "Frame", x0 + Inches(0.1), y0 + Inches(0.09), widths[0], Inches(0.15), size=10, color=b.WHITE, bold=True)
    d.text(s, "Meaning", x0 + widths[0] + Inches(0.1), y0 + Inches(0.09), widths[1], Inches(0.15), size=10, color=b.WHITE, bold=True)
    d.text(s, "Disposition", x0 + widths[0] + widths[1] + Inches(0.1), y0 + Inches(0.09), widths[2], Inches(0.15), size=10, color=b.WHITE, bold=True)
    for i, row in enumerate(rows):
        y = y0 + Inches(0.45 + i * 0.48)
        fill = b.SOFT if i % 2 == 0 else b.WHITE
        d.rect(s, x0, y, sum(widths), Inches(0.42), fill, line=b.GRID)
        d.text(s, row[0], x0 + Inches(0.1), y + Inches(0.08), widths[0], Inches(0.18), size=8.5, color=b.INK, bold=True, shrink=True)
        d.text(s, row[1], x0 + widths[0] + Inches(0.1), y + Inches(0.08), widths[1], Inches(0.15), size=9.5, color=b.INK, shrink=True)
        d.text(s, row[2], x0 + widths[0] + widths[1] + Inches(0.1), y + Inches(0.08), widths[2], Inches(0.15), size=9.5, color=b.DARK_TEAL if "Editable" in row[2] else b.MUTED, bold="Editable" in row[2], shrink=True)
    source(d, s, "Manifest: ai-agents-new-saas-hyperframes.md")
    d.footer(s, 2, total)

    # 3 Unit economics
    s = d.slide(fill=b.WHITE)
    d.header(s, "Agents Win When Unit Economics Compress",
             "Recreated from frame_0001 as editable table and callouts.")
    d.text(s, "Cost per customer interaction", d.M, Inches(1.58), d.CW, Inches(0.25), size=16, color=b.NAVY, bold=True)
    card(d, s, Inches(0.75), Inches(2.05), Inches(2.45), Inches(1.15), "Human agent", "$3.00-$6.00\nper interaction", b.SOFT)
    arrow(d, s, Inches(3.35), Inches(2.43))
    card(d, s, Inches(3.85), Inches(2.05), Inches(2.45), Inches(1.15), "AI agent", "$0.25-$0.50\nper interaction", b.LIGHT_TEAL)
    d.text(s, "90% lower cost", Inches(6.65), Inches(2.2), Inches(2.55), Inches(0.52), size=16, color=b.TEAL, bold=True, shrink=True)
    metrics = [
        ("First response time", "Human: 6+ hrs", "AI: <4 min", "98% faster"),
        ("Resolution time", "Human: 32+ hrs", "AI: 32 min", "98% faster"),
        ("ROI year 1", "", "41%", ""),
        ("ROI year 2", "", "87%", ""),
        ("ROI year 3", "", "124%", ""),
    ]
    y = Inches(3.72)
    for i, m in enumerate(metrics):
        fill = b.SOFT if i % 2 == 0 else b.WHITE
        d.rect(s, d.M, y + Inches(i * 0.38), Inches(8.9), Inches(0.34), fill, line=b.GRID)
        d.text(s, m[0], d.M + Inches(0.12), y + Inches(i * 0.38 + 0.08), Inches(2.3), Inches(0.12), size=8.8, color=b.INK, bold=True)
        d.text(s, m[1], d.M + Inches(2.65), y + Inches(i * 0.38 + 0.08), Inches(1.8), Inches(0.12), size=8.8, color=b.MUTED)
        d.text(s, m[2], d.M + Inches(4.75), y + Inches(i * 0.38 + 0.08), Inches(1.8), Inches(0.12), size=8.8, color=b.DARK_TEAL, bold=True)
        d.text(s, m[3], d.M + Inches(6.9), y + Inches(i * 0.38 + 0.08), Inches(1.7), Inches(0.12), size=8.8, color=b.TEAL, bold=True)
    source(d, s, "Recreated from frame_0001; no screenshot embedded")
    d.footer(s, 3, total)

    # 4 Workflow scorecard
    s = d.slide(fill=b.WHITE)
    d.header(s, "Pick A Workflow With A Paycheck Attached",
             "Recreated from frame_0003 as an editable scoring board.")
    factors = [
        ("Frequency", "daily / hourly"),
        ("Pain", "missed calls\nslow replies\ndropped leads"),
        ("Pattern Lens", "booking\ntriage\napproval\nchase"),
        ("Tools", "Gmail\nSlack\ndialer\ncalendar\napp/form"),
        ("Budget", "employee\nagency\nVA\nBPO"),
    ]
    for i, (t, body) in enumerate(factors):
        x = Inches(0.75 + i * 2.35)
        card(d, s, x, Inches(2.0), Inches(2.0), Inches(1.55), t, body, b.LIGHT_TEAL if i == 4 else b.SOFT)
    d.rect(s, Inches(0.95), Inches(4.18), Inches(10.7), Inches(0.72), RGBColor(0xF4, 0xDF, 0xE8), line=b.CORAL, radius=0.08)
    d.text(s, "First rep: pick one niche -> list 20 annoying jobs -> score each one.",
           Inches(1.18), Inches(4.42), Inches(10.1), Inches(0.22), size=10.5, color=b.INK, bold=True, shrink=True)
    source(d, s, "Recreated from frame_0003; presenter crop excluded")
    d.footer(s, 4, total)

    # 5 Shadow workflow
    s = d.slide(fill=b.WHITE)
    d.header(s, "Shadow The Human Before You Build",
             "Recreated from frame_0004 as an editable three-step flow.")
    card(d, s, Inches(0.9), Inches(2.0), Inches(2.6), Inches(1.6), "Watch 10-20 runs",
         "screen record\nnarrate steps\ncopy/paste spots\nedge cases\nmanager approvals", b.SOFT)
    arrow(d, s, Inches(3.75), Inches(2.68))
    card(d, s, Inches(4.25), Inches(2.0), Inches(2.6), Inches(1.6), "Extract the spec",
         "trigger\ncontext\ntools\nrules\napproval\nescalation\nsuccess", RGBColor(0xF4, 0xEF, 0xD8))
    arrow(d, s, Inches(7.1), Inches(2.68))
    card(d, s, Inches(7.6), Inches(2.0), Inches(2.6), Inches(1.6), "Trusted agent",
         "knows the job\nknows if stuck\nknows when to ask", b.LIGHT_TEAL)
    d.text(s, "Example: home services CSR. Ready during urgency, service area, capacity, membership, financing, and job value.",
           d.M, Inches(4.45), d.CW, Inches(0.45), size=14, color=b.INK, shrink=True)
    source(d, s, "Recreated from frame_0004; no screenshot embedded")
    d.footer(s, 5, total)

    # 6 Agentic workflows text slide
    s = d.slide(fill=b.WHITE)
    d.header(s, "Agentic Workflows Need A Control Pattern",
             "Recreated from frame_0006 as an editable summary slide.")
    d.text(s, "Agentic workflows define how agents operate, communicate, hand off tasks, and collaborate.",
           d.M, Inches(1.75), d.CW, Inches(0.68), size=15, color=b.NAVY, bold=True, shrink=True)
    card(d, s, Inches(0.85), Inches(2.75), Inches(5.25), Inches(2.05), "Sequential workflows",
         "Predetermined control flow with defined execution paths. Best for repeatable processes such as document approval chains or compliance checks.",
         b.SOFT)
    card(d, s, Inches(6.55), Inches(2.75), Inches(5.25), Inches(2.05), "Hierarchical workflows",
         "Structured delegation and review. Best when work needs oversight, escalation, and quality control across agent roles.",
         b.LIGHT_TEAL)
    source(d, s, "Recreated from frame_0006; presenter crop excluded")
    d.footer(s, 6, total)

    # 7 Wrapper makes SaaS
    s = d.slide(fill=b.WHITE)
    d.header(s, "The Wrapper Turns Work Into SaaS",
             "Recreated from frame_0007 as an editable control-room model.")
    card(d, s, Inches(0.9), Inches(2.05), Inches(2.2), Inches(1.15), "AI worker does job", "Agent executes the workflow", b.SOFT)
    arrow(d, s, Inches(3.25), Inches(2.43))
    card(d, s, Inches(3.75), Inches(1.78), Inches(2.55), Inches(1.7), "Control room",
         "logs\napprovals\nsettings\nhandoffs\nanalytics\npolicy editor", RGBColor(0xF4, 0xEF, 0xD8))
    arrow(d, s, Inches(6.52), Inches(2.43))
    card(d, s, Inches(7.05), Inches(2.05), Inches(2.3), Inches(1.15), "Customer trust", "what happened?\nwhy?\nwhat needs review?\nwhere did it fail?", b.LIGHT_TEAL)
    d.rect(s, Inches(0.9), Inches(4.48), Inches(10.3), Inches(0.68), b.SOFT, line=b.GRID, radius=0.08)
    d.text(s, "Eval gym: 50 real calls / tickets / leads -> run the agent -> find failure modes -> improve.",
           Inches(1.12), Inches(4.72), Inches(9.8), Inches(0.20), size=10, color=b.INK, bold=True, shrink=True)
    source(d, s, "Recreated from frame_0007; no screenshot embedded")
    d.footer(s, 7, total)

    # 8 Pilot to product
    s = d.slide(fill=b.WHITE)
    d.header(s, "Sell The Pilot Like Labor, Then Productize",
             "Recreated from frames_0008 and 0009 as editable cards.")
    card(d, s, Inches(0.85), Inches(2.0), Inches(2.8), Inches(1.45), "Pilot promise",
         "We will answer and qualify missed calls.\n\nWe will triage maintenance requests.", b.SOFT)
    arrow(d, s, Inches(3.85), Inches(2.55))
    card(d, s, Inches(4.35), Inches(2.0), Inches(2.45), Inches(1.45), "Simple pricing",
         "$1,500 setup\n+ $1,000/mo\n\nor\n$30/booked job", RGBColor(0xE6, 0xF0, 0xF7))
    arrow(d, s, Inches(7.0), Inches(2.55))
    card(d, s, Inches(7.5), Inches(2.0), Inches(2.7), Inches(1.45), "Product pattern",
         "Same scripts\nSame rules\nSame controls\nSame emails", b.LIGHT_TEAL)
    d.text(s, "You earn the software by doing the work first.",
           d.M, Inches(4.55), d.CW, Inches(0.42), size=19, color=b.NAVY, bold=True, shrink=True)
    source(d, s, "Recreated from frames_0008 and 0009; duplicate presenter position excluded")
    d.footer(s, 8, total)

    # 9 Synthesized 30-day plan
    s = d.slide(fill=b.WHITE)
    d.header(s, "The 30-Day Path Turns Proof Into Product",
             "Synthesized from transcript, using the same editable visual language.")
    phases = [
        ("Days 1-3", "Pick niche\nShadow workflow\nWrite spec"),
        ("Week 1", "Build narrow workflow pilot\nDefine success criteria"),
        ("Weeks 2-3", "Sell two pilots\nSame niche\nSame pain"),
        ("Week 4", "Package repeated pattern\nStart productizing"),
    ]
    for i, (t, body) in enumerate(phases):
        card(d, s, Inches(0.85 + i * 2.9), Inches(2.05), Inches(2.35), Inches(1.65), t, body,
             b.LIGHT_TEAL if i % 2 else b.SOFT)
        if i < 3:
            arrow(d, s, Inches(3.22 + i * 2.9), Inches(2.68))
    d.text(s, "Decision gate: scale only after the same painful workflow repeats across buyers.",
           d.M, Inches(4.62), d.CW, Inches(0.55), size=17, color=b.NAVY, bold=True, shrink=True)
    source(d, s, "Transcript synthesis around 22:06-25:30")
    d.footer(s, 9, total)

    # 10 Artifact rule
    s = d.slide(fill=b.WHITE)
    d.header(s, "Markdown Is Source, PPTX Is Delivery",
             "The corrected workflow keeps evidence files, but ships editable slides.")
    d.text(s, bullets([
        "Research Markdown: transcript synthesis, claims, citations, speaker notes.",
        "Hyperframe manifest: every image classified and accounted for.",
        "Excalidraw: editable concept source when useful.",
        "PPTX: editable shapes, text boxes, tables, and diagrams.",
        "Screenshots: excluded from main slides unless explicitly requested as evidence."
    ], size=13.5), d.M, Inches(1.85), Inches(6.25), Inches(3.55), shrink=True)
    card(d, s, Inches(7.25), Inches(2.0), Inches(4.2), Inches(2.2), "Correct output",
         "ai-agents-new-saas-video-deck-editable-draft.pptx\n\nStatus: draft until PowerPoint review.",
         b.NAVY, b.TEAL, b.WHITE)
    source(d, s, "Workflow rule now blocks screenshot-based deck visuals")
    d.footer(s, 10, total)

    d.save(OUT)


if __name__ == "__main__":
    build()
