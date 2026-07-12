#!/usr/bin/env python3
import sys
from pathlib import Path

from pptx.enum.shapes import MSO_CONNECTOR, MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR
from pptx.util import Inches, Pt

ROOT = Path("/home/shekerk/content-ideas")
RUN = ROOT / "runs/2026-07-02-video-to-deck-rerun"

sys.path.insert(0, str(ROOT / "skills/branded-pptx-deck/scripts"))
from pptxkit import Deck, PP_ALIGN, RGBColor

OUT = RUN / "ai-agents-new-saas-video-deck-v2-native-draft.pptx"


def rgb(hex_value):
    hex_value = hex_value.strip("#")
    return RGBColor(int(hex_value[0:2], 16), int(hex_value[2:4], 16), int(hex_value[4:6], 16))


class V2:
    navy = rgb("071524")
    ink = rgb("152235")
    muted = rgb("607083")
    teal = rgb("00B89C")
    teal_dark = rgb("008F75")
    mint = rgb("E6F8F4")
    blue = rgb("E8F1FA")
    gold = rgb("FFF1C7")
    rose = rgb("FBE8EE")
    soft = rgb("F5F7FA")
    grid = rgb("D8E0E8")
    white = rgb("FFFFFF")
    slate = rgb("24364A")


def title(d, s, kicker, text):
    d.text(s, kicker.upper(), d.M, Inches(0.34), Inches(5.8), Inches(0.22),
           size=9.8, color=V2.teal_dark, bold=True, shrink=True)
    d.text(s, text, d.M, Inches(0.68), d.CW, Inches(0.82),
           size=23.0, color=V2.navy, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.52), Inches(1.25), Inches(0.05), V2.teal)


def footer(d, s, page, total, note=None, dark=False):
    col = rgb("AAB6C4") if dark else V2.muted
    if note:
        d.text(s, note, d.M, Inches(6.75), Inches(10.2), Inches(0.34),
               size=7.2, color=col, shrink=True)
    d.text(s, f"{page} / {total}", d.W - Inches(1.2), Inches(6.80), Inches(0.7), Inches(0.24),
           size=9.2, color=col, align=PP_ALIGN.RIGHT, bold=True)


def card(d, s, x, y, w, h, heading, body="", fill=None, line=None, heading_color=None):
    fill = fill or V2.white
    line = line or V2.grid
    heading_color = heading_color or V2.navy
    d.rect(s, x, y, w, h, fill, line=line, radius=0.06)
    d.text(s, heading, x + Inches(0.15), y + Inches(0.13), w - Inches(0.30), Inches(0.25),
           size=11.2, color=heading_color, bold=True, shrink=True)
    if body:
        d.text(s, body, x + Inches(0.15), y + Inches(0.50), w - Inches(0.30), h - Inches(0.62),
               size=9.4, color=V2.ink, shrink=True)


def label(d, s, x, y, text, fill=None, color=None, w=1.4):
    d.rect(s, x, y, Inches(w), Inches(0.30), fill or V2.mint, radius=0.10)
    d.text(s, text, x + Inches(0.08), y + Inches(0.075), Inches(w - 0.16), Inches(0.12),
           size=8.2, color=color or V2.teal_dark, bold=True, align=PP_ALIGN.CENTER, shrink=True)


def connector(d, s, x1, y1, x2, y2, color=None, width=2.0):
    line = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    line.line.color.rgb = color or V2.teal
    line.line.width = Pt(width)
    try:
        line.line.end_arrowhead = True
    except Exception:
        pass
    return line


def section_num(d, s, n, x, y, fill=None):
    d.rect(s, x, y, Inches(0.38), Inches(0.38), fill or V2.navy, radius=0.10)
    d.text(s, str(n), x, y + Inches(0.08), Inches(0.38), Inches(0.13),
           size=9.5, color=V2.white, bold=True, align=PP_ALIGN.CENTER)


def bullet_text(d, s, items, x, y, w, h, size=10.2, color=None):
    runs = [{"text": item, "bullet": True, "space_before": 5, "size": size} for item in items]
    d.text(s, runs, x, y, w, h, size=size, color=color or V2.ink, shrink=True)


def bar_chart(d, s, x, y, w, h, values, labels, fills):
    max_v = max(values)
    step = w / len(values)
    for i, (val, lab, fill) in enumerate(zip(values, labels, fills)):
        bh = int(h * (val / max_v))
        bx = x + int(step * i) + Inches(0.08)
        by = y + h - bh
        d.rect(s, bx, by, int(step) - Inches(0.16), bh, fill)
        d.text(s, lab, bx - Inches(0.02), y + h + Inches(0.12), int(step), Inches(0.2),
               size=7.7, color=V2.muted, align=PP_ALIGN.CENTER, shrink=True)


def build():
    d = Deck(footer="AI Agents Are The New SaaS | Video-to-deck v2 | Draft")
    total = 13

    # 1
    s = d.slide(fill=V2.navy)
    d.text(s, "VIDEO-TO-DECK V2", d.M, Inches(0.65), Inches(4.0), Inches(0.25),
           size=10.5, color=V2.teal, bold=True)
    d.text(s, "AI Agents Are The New SaaS", d.M, Inches(1.15), Inches(8.8), Inches(0.78),
           size=36, color=V2.white, bold=True, shrink=True)
    d.text(s, "The real opportunity is workflow ownership: find paid work, observe it deeply, automate the smallest useful loop, wrap it with trust controls, then productize the repeated pattern.",
           d.M, Inches(2.15), Inches(6.2), Inches(1.28), size=14.8, color=rgb("DCE6EF"), shrink=True)
    steps = [
        ("1", "Paid workflow"),
        ("2", "Observed spec"),
        ("3", "Small agent"),
        ("4", "Control room"),
        ("5", "Productized workflow"),
    ]
    for i, (num, txt) in enumerate(steps):
        x = Inches(0.72 + i * 2.35)
        section_num(d, s, num, x, Inches(4.38), V2.teal_dark if i < 4 else V2.teal)
        d.text(s, txt, x + Inches(0.48), Inches(4.40), Inches(1.62), Inches(0.28),
               size=8.5, color=V2.white, bold=True, shrink=True)
        if i < 4:
            connector(d, s, x + Inches(1.95), Inches(4.57), x + Inches(2.22), Inches(4.57), rgb("6EE7D8"))
    footer(d, s, 1, total, "Built from dense hyperframe inventory; prior sparse-frame draft rejected.", dark=True)

    # 2 market context
    s = d.slide(fill=V2.white)
    title(d, s, "Market context", "SaaS packaged repeatable work; agents can package executed work")
    card(d, s, Inches(0.72), Inches(1.70), Inches(5.1), Inches(4.35), "SaaS adoption curve", "", V2.soft)
    bar_chart(d, s, Inches(1.05), Inches(2.10), Inches(4.45), Inches(2.65),
              [9, 16, 25, 38, 55, 76, 102], ["Early", "CRM", "Collab", "FinOps", "Vertical", "AI apps", "Agents"],
              [rgb("B7D8F2"), rgb("99C7E8"), rgb("7FB8DC"), rgb("65A9D0"), rgb("4A9BC4"), rgb("21BFA6"), V2.teal_dark])
    d.text(s, "Frame coverage: market chart and SaaS-logo context are represented as clean market setup, not ignored.",
           Inches(1.05), Inches(5.04), Inches(4.45), Inches(0.52), size=8.8, color=V2.muted, shrink=True)
    card(d, s, Inches(6.25), Inches(1.70), Inches(5.8), Inches(4.35), "From software subscriptions to work outcomes", "", V2.white)
    labels = [("Shopify", V2.mint), ("Slack", V2.blue), ("Airbnb", V2.rose), ("Stripe", V2.gold)]
    for i, (lab, fill) in enumerate(labels):
        card(d, s, Inches(6.65 + (i % 2) * 2.55), Inches(2.22 + (i // 2) * 1.05), Inches(2.05), Inches(0.72), lab, "", fill)
    d.text(s, "Previous SaaS winners made workflows visible and repeatable. Agent companies can go one layer deeper: they perform the job and expose the controls buyers need to trust it.",
           Inches(6.65), Inches(4.52), Inches(4.85), Inches(0.82), size=12.5, color=V2.ink, bold=True, shrink=True)
    footer(d, s, 2, total, "Sources: dense_0001, dense_0002.")

    # 3 thesis diagram
    s = d.slide(fill=V2.white)
    title(d, s, "Core thesis", "The agent company is built around a paid workflow, not a generic bot")
    y = Inches(2.25)
    boxes = [
        ("Old SaaS job", "log\ndashboard\nreview\nmanual follow-up", V2.soft),
        ("Agent job", "draft\ntriage\ncoordinate\nact", V2.blue),
        ("Outcome", "resolved work\nfaster cycle\nclear audit trail", V2.mint),
    ]
    for i, (h, b, fill) in enumerate(boxes):
        x = Inches(1.0 + i * 3.75)
        card(d, s, x, y, Inches(2.65), Inches(1.75), h, b, fill)
        if i < 2:
            connector(d, s, x + Inches(2.65), y + Inches(0.88), x + Inches(3.35), y + Inches(0.88))
    d.rect(s, Inches(1.0), Inches(4.58), Inches(10.4), Inches(0.84), V2.navy, radius=0.08)
    d.text(s, "The wedge is workflow ownership: bounded work plus visible controls.",
           Inches(1.28), Inches(4.90), Inches(9.85), Inches(0.20), size=10.8, color=V2.white, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 3, total, "Sources: dense_0004, scene_0007, scene_0028.")

    # 4 unit economics
    s = d.slide(fill=V2.white)
    title(d, s, "Economic wedge", "Agents win where repeated labor cost and response-time pain are measurable")
    card(d, s, Inches(0.85), Inches(1.88), Inches(2.5), Inches(1.1), "Human interaction", "$3.00-$6.00\nslow queue\nbusiness-hour capacity", V2.soft)
    connector(d, s, Inches(3.55), Inches(2.43), Inches(4.18), Inches(2.43))
    card(d, s, Inches(4.35), Inches(1.88), Inches(2.5), Inches(1.1), "AI interaction", "$0.25-$0.50\nnear-immediate\nalways-on capacity", V2.mint)
    d.text(s, "90%+ cost compression", Inches(7.35), Inches(2.08), Inches(3.55), Inches(0.36), size=18, color=V2.teal_dark, bold=True, shrink=True)
    rows = [
        ("First response", "6+ hours", "<4 min", "speed wedge"),
        ("Resolution", "32+ hours", "32 min", "cycle-time wedge"),
        ("ROI path", "year 1", "year 2-3", "compound wedge"),
    ]
    for i, row in enumerate(rows):
        y = Inches(3.62 + i * 0.62)
        d.rect(s, Inches(1.0), y, Inches(10.6), Inches(0.46), V2.soft if i % 2 == 0 else V2.white, line=V2.grid)
        for j, txt in enumerate(row):
            d.text(s, txt, Inches(1.18 + j * 2.6), y + Inches(0.10), Inches(2.1), Inches(0.18),
                   size=9.6, color=V2.teal_dark if j == 2 else V2.ink, bold=j in (0, 2), shrink=True)
    footer(d, s, 4, total, "Sources: dense_0007, scene_0021. Recreated; no screenshot embedded.")

    # 5 workflow + SIT
    s = d.slide(fill=V2.white)
    title(d, s, "Search discipline", "Pick workflows with frequency, pain, software touchpoints, and budget")
    factors = [("Frequency", "daily/hourly"), ("Pain", "missed calls\nslow replies"), ("Pattern", "booking\ntriage\napproval"), ("Tools", "email\ncalendar\nCRM"), ("Budget", "employee\nagency\nBPO")]
    for i, (h, b) in enumerate(factors):
        card(d, s, Inches(0.70 + i * 2.35), Inches(1.82), Inches(1.82), Inches(1.30), h, b, V2.mint if h == "Budget" else V2.soft)
    d.text(s, "SIT software map: summarize inputs, tools, triggers, outputs, and exceptions before writing code.",
           Inches(0.80), Inches(3.72), Inches(5.15), Inches(0.66), size=11.2, color=V2.navy, bold=True, shrink=True)
    sit = [("Sources", "calls\nforms\nemails"), ("Interfaces", "CRM\ncalendar\nphone"), ("Tasks", "qualify\nschedule\nupdate"), ("Risks", "edge cases\nhandoff")]
    for i, (h, b) in enumerate(sit):
        card(d, s, Inches(6.15 + (i % 2) * 2.55), Inches(3.45 + (i // 2) * 1.08), Inches(2.15), Inches(0.82), h, b, V2.white)
    footer(d, s, 5, total, "Sources: dense_0026-0037, scene_0011, dense_0006, scene_0019.")

    # 6 wedge examples
    s = d.slide(fill=V2.white)
    title(d, s, "Wedge examples", "The video’s examples cluster around urgent, high-friction service workflows")
    examples = [
        ("Restaurants", "AI receptionist\nbooking\nmissed-call recovery", V2.gold),
        ("Home services", "dispatch\nquote triage\nemergency routing", V2.blue),
        ("Property asset", "tenant requests\nmaintenance\nstatus updates", V2.mint),
        ("Contact center", "front-door triage\nqualification\nhandoff", V2.rose),
    ]
    for i, (h, b, fill) in enumerate(examples):
        card(d, s, Inches(0.90 + (i % 2) * 5.45), Inches(1.85 + (i // 2) * 1.72), Inches(4.55), Inches(1.20), h, b, fill)
    d.rect(s, Inches(1.0), Inches(5.45), Inches(10.7), Inches(0.55), V2.navy, radius=0.08)
    d.text(s, "Use examples as evidence of where the search should start, not as screenshots.",
           Inches(1.28), Inches(5.61), Inches(10.1), Inches(0.24), size=10.6, color=V2.white, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 6, total, "Sources: Slang AI dense_0018-0019 / scene_0029-0030; home-services scene_0032-0035; Samday/contact-center dense_0023 / scene_0038-0039.")

    # 7 shadow human
    s = d.slide(fill=V2.white)
    title(d, s, "Operating method", "Shadow the human before you build the agent")
    items = [
        ("Watch 10-20 runs", "screen record\nnarrate decisions\ncapture copy/paste"),
        ("Extract the spec", "trigger\ncontext\ntools\nrules\napproval"),
        ("Define trust", "when stuck\nwhen to ask\nwhat to log"),
    ]
    for i, (h, b) in enumerate(items):
        x = Inches(1.0 + i * 3.75)
        card(d, s, x, Inches(2.15), Inches(2.65), Inches(1.62), h, b, [V2.soft, V2.gold, V2.mint][i])
        if i < 2:
            connector(d, s, x + Inches(2.65), Inches(2.95), x + Inches(3.35), Inches(2.95))
    d.text(s, "The workflow spec is observed behavior, not a prompt. This is the step that turns a demo into a sellable workflow.",
           Inches(1.0), Inches(4.65), Inches(10.0), Inches(0.56), size=15, color=V2.navy, bold=True, shrink=True)
    footer(d, s, 7, total, "Sources: dense_0038-0055, scene_0013.")

    # 8 smallest useful agent
    s = d.slide(fill=V2.white)
    title(d, s, "Build scope", "Build the smallest useful agent: draft, triage, coordinate, act")
    stages = [("Draft", "write reply\nsummarize\nprepare next step"), ("Triage", "classify\nprioritize\nroute"), ("Coordinate", "check slots\nnotify humans\nsync systems"), ("Act", "book\nupdate\nsend")]
    for i, (h, b) in enumerate(stages):
        x = Inches(0.92 + i * 2.82)
        section_num(d, s, i + 1, x, Inches(2.12), V2.teal_dark)
        card(d, s, x, Inches(2.62), Inches(2.18), Inches(1.35), h, b, [V2.soft, V2.gold, V2.blue, V2.mint][i])
        if i < 3:
            connector(d, s, x + Inches(2.18), Inches(3.30), x + Inches(2.60), Inches(3.30))
    d.rect(s, Inches(1.0), Inches(4.78), Inches(10.6), Inches(0.55), V2.rose, radius=0.08)
    d.text(s, "Good promise: answer missed calls, find roofers, and book qualified jobs.",
           Inches(1.32), Inches(4.95), Inches(9.9), Inches(0.24), size=10.8, color=V2.ink, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 8, total, "Sources: dense_0058-0069, scene_0043, scene_0045.")

    # 9 architecture
    s = d.slide(fill=V2.white)
    title(d, s, "Workflow architecture", "Agentic workflows need a control pattern, not just agent autonomy")
    card(d, s, Inches(0.90), Inches(1.95), Inches(5.15), Inches(2.35), "Sequential workflow", "Predetermined path for repeatable work.\n\nUse when the steps are stable: intake -> classify -> draft -> approve -> send.", V2.soft)
    card(d, s, Inches(6.45), Inches(1.95), Inches(5.15), Inches(2.35), "Hierarchical workflow", "Delegation and review for higher-risk work.\n\nUse when escalation, judgment, or quality gates matter.", V2.mint)
    d.text(s, "External architecture-pattern references are useful, but the deck should translate them into the founder workflow instead of copying a text-heavy reference card.",
           Inches(1.0), Inches(5.05), Inches(10.3), Inches(0.44), size=12.8, color=V2.navy, bold=True, shrink=True)
    footer(d, s, 9, total, "Sources: dense_0070, dense_0071-0072, scene_0046-0047.")

    # 10 wrapper
    s = d.slide(fill=V2.white)
    title(d, s, "Trust wrapper", "The wrapper turns agent work into SaaS")
    parts = [("AI worker", "does the job"), ("Control room", "logs\napprovals\nsettings\nhandoffs\nanalytics"), ("Customer trust", "what happened\nwhy it happened\nwhat needs review")]
    for i, (h, b) in enumerate(parts):
        x = Inches(1.0 + i * 3.75)
        card(d, s, x, Inches(2.12), Inches(2.65), Inches(1.55), h, b, [V2.blue, V2.gold, V2.mint][i])
        if i < 2:
            connector(d, s, x + Inches(2.65), Inches(2.88), x + Inches(3.35), Inches(2.88))
    d.rect(s, Inches(1.0), Inches(4.66), Inches(10.5), Inches(0.55), V2.soft, line=V2.grid, radius=0.08)
    d.text(s, "Eval gym: run real work through the flow; inspect failures; improve controls.",
           Inches(1.25), Inches(4.82), Inches(9.95), Inches(0.22), size=10.2, color=V2.ink, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 10, total, "Sources: dense_0078-0091, scene_0015, scene_0049.")

    # 11 pilot productize
    s = d.slide(fill=V2.white)
    title(d, s, "Commercialization", "Sell the pilot like labor, then productize the repeated pattern")
    parts = [("Pilot promise", "We answer and qualify missed calls.\nWe triage maintenance requests."), ("Simple pricing", "$1,500 setup\n+ $1,000/mo\nor outcome fee"), ("Product pattern", "same scripts\nsame rules\nsame controls\nsame emails")]
    for i, (h, b) in enumerate(parts):
        x = Inches(1.0 + i * 3.75)
        card(d, s, x, Inches(2.08), Inches(2.65), Inches(1.58), h, b, [V2.gold, V2.blue, V2.mint][i])
        if i < 2:
            connector(d, s, x + Inches(2.65), Inches(2.86), x + Inches(3.35), Inches(2.86))
    d.text(s, "You earn the software by doing the work first.",
           Inches(1.0), Inches(4.82), Inches(10.0), Inches(0.40), size=18, color=V2.navy, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 11, total, "Sources: dense_0096-0111, scene_0017, scene_0051, scene_0053.")

    # 12 own workflow
    s = d.slide(fill=V2.white)
    title(d, s, "Defensibility", "Own the workflow: the moat is the operating loop")
    parts = [("Old way", "human follows SOP\nmanager checks\nsoftware records"), ("Agent way", "agent performs loop\nasks when stuck\nupdates systems"), ("Context as product", "workflow memory\npolicy\nexceptions\nevaluation set")]
    for i, (h, b) in enumerate(parts):
        x = Inches(1.0 + i * 3.75)
        card(d, s, x, Inches(2.05), Inches(2.65), Inches(1.75), h, b, [V2.rose, V2.mint, V2.gold][i])
        if i < 2:
            connector(d, s, x + Inches(2.65), Inches(2.92), x + Inches(3.35), Inches(2.92))
    d.rect(s, Inches(1.0), Inches(4.72), Inches(10.4), Inches(0.62), V2.navy, radius=0.08)
    d.text(s, "Start with the job. Then build the agent people pay for.",
           Inches(1.30), Inches(4.90), Inches(9.8), Inches(0.24), size=11.2, color=V2.white, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    footer(d, s, 12, total, "Sources: dense_0113-0123, scene_0055.")

    # 13 map
    s = d.slide(fill=V2.white)
    title(d, s, "Coverage map", "Every meaningful visual beat is represented or intentionally grouped")
    rows = [
        ("Market chart + SaaS winners", "slides 2-3", "recreated / synthesized"),
        ("SIT map + workflow scorecard", "slide 5", "recreated"),
        ("Slang, home services, Samday", "slide 6", "grouped evidence"),
        ("Shadow human", "slide 7", "recreated"),
        ("Smallest useful agent", "slide 8", "recreated"),
        ("Agentic workflows + architecture ref", "slide 9", "recreated / summarized"),
        ("Wrapper + pilot + own workflow", "slides 10-12", "recreated"),
        ("Presenter-only frames", "excluded", "not used as deck visuals"),
    ]
    x0, y0 = Inches(0.78), Inches(1.80)
    widths = [Inches(5.4), Inches(2.1), Inches(3.0)]
    d.rect(s, x0, y0, sum(widths), Inches(0.34), V2.navy, radius=0.04)
    for i, h in enumerate(["Visual beat", "Deck location", "Treatment"]):
        d.text(s, h, x0 + sum(widths[:i]) + Inches(0.10), y0 + Inches(0.08),
               widths[i] - Inches(0.18), Inches(0.12), size=8.6, color=V2.white, bold=True, shrink=True)
    for r, row in enumerate(rows):
        y = y0 + Inches(0.42 + r * 0.45)
        d.rect(s, x0, y, sum(widths), Inches(0.36), V2.soft if r % 2 == 0 else V2.white, line=V2.grid)
        for i, val in enumerate(row):
            d.text(s, val, x0 + sum(widths[:i]) + Inches(0.10), y + Inches(0.09),
                   widths[i] - Inches(0.18), Inches(0.11), size=8.3,
                   color=V2.teal_dark if i == 2 and "recreated" in val else V2.ink,
                   bold=i == 0, shrink=True)
    footer(d, s, 13, total, "Inventory source: ai-agents-new-saas-visual-inventory-v2.md.")

    d.save(OUT)


if __name__ == "__main__":
    build()
