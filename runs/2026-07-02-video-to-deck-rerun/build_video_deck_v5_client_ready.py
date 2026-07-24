#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path("/home/shekerk/content-ideas")
RUN = ROOT / "runs/2026-07-02-video-to-deck-rerun"
sys.path.insert(0, str(ROOT / "skills/branded-pptx-deck/scripts"))

from pptxkit import Deck, Inches, PP_ALIGN, RGBColor

OUT = RUN / "ai-agents-new-saas-video-deck-v5-client-ready-draft.pptx"


def hx(s):
    s = s.strip("#")
    return RGBColor(int(s[:2], 16), int(s[2:4], 16), int(s[4:], 16))


def add_note(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def section_label(d, s, label):
    b = d.b
    d.text(s, label.upper(), d.M, Inches(0.26), Inches(7.3), Inches(0.22),
           size=9.8, color=b.DARK_TEAL, bold=True, shrink=True)


def action_header(d, s, label, title, subtitle=None):
    b = d.b
    d.rect(s, 0, 0, d.W, Inches(0.13), b.TEAL)
    section_label(d, s, label)
    d.text(s, title, d.M, Inches(0.50), Inches(11.75), Inches(0.76),
           size=22.0, color=b.NAVY, bold=True, shrink=True)
    d.rect(s, d.M, Inches(1.24), Inches(1.35), Inches(0.045), b.TEAL)
    if subtitle:
        d.text(s, subtitle, d.M, Inches(1.40), Inches(11.3), Inches(0.38),
               size=11.6, color=b.MUTED, shrink=True)


def footer(d, s, page, total):
    d.footer(s, page, total)


def card(d, s, x, y, w, h, title, body=None, fill=None, title_color=None, body_color=None,
         index=None, accent=True):
    b = d.b
    fill = fill or b.WHITE
    title_color = title_color or b.NAVY
    body_color = body_color or b.INK
    d.rect(s, x, y, w, h, fill, line=b.GRID, radius=0.05, shadow=True)
    if accent:
        d.rect(s, x, y, Inches(0.06), h, b.TEAL, radius=0.02)
    if index:
        d.rect(s, x + Inches(0.18), y + Inches(0.16), Inches(0.38), Inches(0.24), b.NAVY, radius=0.05)
        d.text(s, index, x + Inches(0.18), y + Inches(0.205), Inches(0.38), Inches(0.08),
               size=8.2, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        tx = x + Inches(0.68)
        tw = w - Inches(0.86)
    else:
        tx = x + Inches(0.20)
        tw = w - Inches(0.40)
    d.text(s, title, tx, y + Inches(0.15), tw, Inches(0.36),
           size=11.3, color=title_color, bold=True, shrink=True)
    if body:
        d.text(s, body, x + Inches(0.22), y + Inches(0.58), w - Inches(0.44), h - Inches(0.76),
               size=8.6, color=body_color, shrink=True)


def takeaway(d, s, text, y=6.02):
    b = d.b
    d.rect(s, d.M, Inches(y), d.CW, Inches(0.76), b.NAVY, radius=0.05)
    d.text(s, "TAKEAWAY", d.M + Inches(0.18), Inches(y + 0.25), Inches(1.0), Inches(0.18),
           size=8.4, color=b.GOLD, bold=True, shrink=True)
    d.text(s, text, d.M + Inches(1.22), Inches(y + 0.17), d.CW - Inches(1.46), Inches(0.44),
           size=9.4, color=b.WHITE, bold=True, shrink=True)


def chip(d, s, x, y, text, color=None, width=1.35):
    b = d.b
    color = color or b.NAVY_2
    d.rect(s, x, y, Inches(width), Inches(0.28), color, radius=0.08)
    d.text(s, text, x + Inches(0.10), y + Inches(0.075), Inches(width - 0.20), Inches(0.14),
           size=8.4, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)


def flow_node(d, s, x, y, w, h, title, body, fill):
    b = d.b
    d.rect(s, x, y, w, h, fill, line=hx("EEF2F5"), radius=0.05, shadow=True)
    d.text(s, title, x + Inches(0.20), y + Inches(0.18), w - Inches(0.40), Inches(0.24),
           size=11.6, color=b.WHITE, bold=True, shrink=True)
    d.text(s, body, x + Inches(0.20), y + Inches(0.58), w - Inches(0.40), h - Inches(0.74),
           size=8.7, color=b.LIGHT_TEAL, shrink=True)


def arrow_text(d, s, x, y):
    d.text(s, "→", x, y, Inches(0.38), Inches(0.22), size=22, color=d.b.DARK_TEAL,
           bold=True, align=PP_ALIGN.CENTER, shrink=True)


def bullet_list(d, s, items, x, y, w, h, size=10.5):
    d.text(s, [{"text": t, "bullet": True, "space_before": 7, "size": size} for t in items],
           x, y, w, h, size=size, color=d.b.INK, shrink=True)


def build_cover(d, total):
    b = d.b
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(10.55), 0, Inches(2.78), d.H, b.NAVY_2)
    d.rect(s, Inches(10.55), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "VIDEO-TO-DECK CLIENT DRAFT", d.M, Inches(0.82), Inches(5.4), Inches(0.20),
           size=10.5, color=b.TEAL, bold=True, shrink=True)
    d.text(s, "AI Agents Are The New SaaS", d.M, Inches(1.34), Inches(8.15), Inches(0.88),
           size=33, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.36), Inches(1.48), Inches(0.055), b.TEAL)
    d.text(s, "A founder playbook for packaging workflow outcomes as software-backed labor.",
           d.M, Inches(2.70), Inches(7.5), Inches(0.46), size=13.2, color=hx("DCE6EF"), shrink=True)
    for i, item in enumerate(["Storyboard", "Native PPTX visuals", "Hyperframe-audited", "Excalidraw sources"]):
        chip(d, s, d.M + Inches(i * 1.72), Inches(3.42), item, b.NAVY_2, width=1.52)
    d.text(s, "Source: Greg Isenberg YouTube video; transcript and 56 scene-change frames retained as audit material.",
           d.M, Inches(6.80), Inches(8.5), Inches(0.28), size=8.4, color=hx("AAB6C4"), shrink=True)
    d.text(s, f"1 / {total}", d.W - Inches(1.25), Inches(6.80), Inches(0.75), Inches(0.28),
           size=9.5, color=hx("AAB6C4"), bold=True, align=PP_ALIGN.RIGHT)
    add_note(s, "Cover: client-ready v5 rebuild. No timestamps shown on slide.")


def build_exec_summary(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "Executive summary", "Agent SaaS wins when the product is a paid workflow, not a generic bot",
                  "The video’s argument is a practical build sequence: pick a job, observe it, automate a bounded loop, then wrap it with trust.")
    d.rect(s, d.M, Inches(1.82), d.CW, Inches(0.88), b.NAVY, radius=0.05)
    d.text(s, "BLUF", d.M + Inches(0.22), Inches(2.08), Inches(0.72), Inches(0.12),
           size=9.3, color=b.GOLD, bold=True)
    d.text(s, "Do not sell another AI tool. Sell a narrow, high-frequency job that already has budget and can be handed off with controls.",
           d.M + Inches(1.05), Inches(2.02), d.CW - Inches(1.28), Inches(0.20),
           size=13.4, color=b.WHITE, bold=True, shrink=True)
    cols = [
        ("Situation", "Agents are being framed like software, but buyers care about completed work."),
        ("Insight", "The fundable wedge is a workflow with frequency, pain, a clear finish line, and a budget owner."),
        ("Recommendation", "Shadow the human first, ship a minimum useful agent, and turn trust controls into the SaaS wrapper."),
    ]
    for i, (title, body) in enumerate(cols):
        card(d, s, d.M + Inches(i * 4.1), Inches(3.05), Inches(3.78), Inches(1.72),
             title, body, fill=b.SOFT, index=str(i + 1))
    d.rect(s, d.M, Inches(5.22), d.CW, Inches(0.76), hx("FFF4CF"), line=hx("F2D982"), radius=0.05)
    d.text(s, "THE ASK", d.M + Inches(0.22), Inches(5.48), Inches(0.84), Inches(0.16),
           size=8.8, color=b.NAVY, bold=True)
    d.text(s, "Choose one niche and score 20 workflow jobs before building anything.",
           d.M + Inches(1.16), Inches(5.42), d.CW - Inches(1.40), Inches(0.30),
           size=10.5, color=b.NAVY, bold=True, shrink=True)
    footer(d, s, page, total)
    add_note(s, "Analyst synthesis: the core business decision is workflow selection before product build.")


def build_storyboard(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "Storyboard", "The talk is a build-and-sell sequence, not a collection of diagrams",
                  "This slide is the narrative spine used to organize the deck.")
    items = [
        ("Context", "Agent SaaS shifts value from seats to outcomes."),
        ("Tension", "Most founders start with generic agents instead of paid jobs."),
        ("Answer", "Pick one workflow with budget and a clear finish line."),
        ("Proof", "Shadow humans, ship a bounded agent, wrap with controls."),
        ("Action", "Sell labor-like pilots, then productize the repeated loop."),
    ]
    x0 = d.M
    for i, (title, body) in enumerate(items):
        x = x0 + Inches(i * 2.48)
        fill = b.NAVY if i == 2 else b.SOFT
        d.rect(s, x, Inches(2.00), Inches(2.12), Inches(2.62), fill, line=b.GRID, radius=0.05, shadow=True)
        d.text(s, f"0{i+1}", x + Inches(0.18), Inches(2.20), Inches(0.44), Inches(0.12),
               size=9.2, color=b.GOLD if i == 2 else b.DARK_TEAL, bold=True)
        d.text(s, title, x + Inches(0.18), Inches(2.58), Inches(1.72), Inches(0.22),
               size=13.0, color=b.WHITE if i == 2 else b.NAVY, bold=True, shrink=True)
        d.text(s, body, x + Inches(0.18), Inches(3.10), Inches(1.76), Inches(0.78),
               size=9.6, color=b.LIGHT_TEAL if i == 2 else b.INK, shrink=True)
        if i < len(items) - 1:
            arrow_text(d, s, x + Inches(2.18), Inches(3.10))
    takeaway(d, s, "The deck follows the build logic: select job -> observe work -> ship bounded agent -> wrap trust -> productize.")
    footer(d, s, page, total)
    add_note(s, "Story-architect spine. Timestamps intentionally excluded from visible slide.")


def build_product_job(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "The product is the job", "The product surface shifts from software access to workflow handoff",
                  "The buyer pays for completed work: logs, decisions, escalations, and outcomes.")
    nodes = [
        ("Paid workflow", "Eligible, funded, frequent, painful", b.NAVY),
        ("Observed spec", "Trigger, context, tools, rules, approvals", hx("163F4A")),
        ("Agent business", "Does work, logs work, asks when stuck", hx("144E40")),
    ]
    for i, (title, body, fill) in enumerate(nodes):
        x = d.M + Inches(i * 3.72)
        flow_node(d, s, x, Inches(2.15), Inches(2.82), Inches(1.58), title, body, fill)
        if i < 2:
            arrow_text(d, s, x + Inches(2.94), Inches(2.82))
    bullet_list(d, s, [
        "Frame the SKU around a job, not around model capability.",
        "Define the handoff boundary before defining the agent architecture.",
        "Trust controls are part of the product, not implementation detail.",
    ], d.M, Inches(4.34), Inches(7.4), Inches(1.00))
    card(d, s, Inches(9.05), Inches(4.08), Inches(3.08), Inches(1.34),
         "Deck implication", "Use action titles and workflow visuals; avoid screenshot dumps and generic AI iconography.", fill=b.SOFT)
    takeaway(d, s, "If the buyer cannot name the job being handed off, the agent is too vague to sell.")
    footer(d, s, page, total)
    add_note(s, "Recreates the conceptual thesis from Excalidraw source ai-agents-new-saas-v3-thesis-workflow.excalidraw as native PPTX shapes.")


def build_examples(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "Real examples", "The credible wedges are boring service workflows with visible labor spend",
                  "The examples make the model concrete: handle one annoying job faster and cheaper than incremental headcount.")
    examples = [
        ("Restaurant calls", "Answer calls, manage reservations, route VIPs, alert staff"),
        ("Home services", "Answer inbound demand, book jobs, reschedule, coordinate dispatch"),
        ("Property ops", "Triage maintenance, coordinate vendors, update residents"),
        ("Contact center", "Classify intent, draft responses, escalate exceptions"),
    ]
    for i, (title, body) in enumerate(examples):
        x = d.M + Inches((i % 2) * 4.25)
        y = Inches(1.92 + (i // 2) * 1.70)
        card(d, s, x, y, Inches(3.82), Inches(1.24), title, body, fill=b.SOFT, index=str(i + 1))
    d.rect(s, Inches(9.40), Inches(1.92), Inches(2.58), Inches(2.94), b.NAVY, radius=0.05)
    d.text(s, "Pattern", Inches(9.66), Inches(2.24), Inches(2.0), Inches(0.20),
           size=13.2, color=b.GOLD, bold=True)
    d.text(s, [{"text": t, "bullet": True, "space_before": 7, "size": 9.3} for t in [
        "High frequency",
        "Clear finish line",
        "Known tools",
        "Learnable edge cases",
        "Budget owner",
    ]], Inches(9.66), Inches(2.78), Inches(1.9), Inches(1.54), size=9.3, color=b.LIGHT_TEAL, shrink=True)
    takeaway(d, s, "The wedge is repeated work that maps to existing payroll, agency, VA, or BPO spend.")
    footer(d, s, page, total)
    add_note(s, "Uses transcript examples and visual inventory v2 wedge group.")


def build_scorecard(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "Pick a workflow with a paycheck", "Budget ownership is the forcing function for what to build first",
                  "Score jobs before writing code; pain without a budget owner is a weak wedge.")
    headers = ["Factor", "What good looks like", "Why it matters"]
    widths = [2.0, 4.1, 4.7]
    x = d.M
    y = Inches(1.92)
    for i, h in enumerate(headers):
        d.rect(s, x, y, Inches(widths[i]), Inches(0.38), b.NAVY if i == 0 else b.NAVY_2)
        d.text(s, h, x + Inches(0.12), y + Inches(0.12), Inches(widths[i] - 0.24), Inches(0.08),
               size=8.8, color=b.WHITE, bold=True, shrink=True)
        x += Inches(widths[i])
    rows = [
        ("Frequency", "Daily or hourly", "Creates enough repetitions to learn and prove ROI"),
        ("Pain", "Missed calls, slow replies, manual rework", "Buyer feels the operational cost"),
        ("Finish line", "Booked, routed, resolved, approved", "Makes success measurable"),
        ("Tools", "Email, calendar, CRM, ticketing", "Shows where the agent must operate"),
        ("Budget", "Role, agency, VA, BPO owner", "Confirms there is spend to redirect"),
    ]
    y += Inches(0.38)
    for r, row in enumerate(rows):
        x = d.M
        fill = b.SOFT if r % 2 == 0 else b.WHITE
        for i, val in enumerate(row):
            d.rect(s, x, y, Inches(widths[i]), Inches(0.56), fill, line=b.GRID)
            d.text(s, val, x + Inches(0.12), y + Inches(0.15), Inches(widths[i] - 0.24), Inches(0.14),
                   size=9.1 if i else 9.6, color=b.NAVY if i == 0 else b.INK, bold=(i == 0), shrink=True)
            x += Inches(widths[i])
        y += Inches(0.56)
    takeaway(d, s, "First rep: one niche, 20 complained-about jobs, scored before anything is built.")
    footer(d, s, page, total)
    add_note(s, "Native PPTX reconstruction of the workflow scorecard visual.")


def build_shadow(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "Shadow the human first", "The real product spec is hidden in exceptions, checks, and escalation behavior",
                  "Observe 10-20 cases before writing prompts; the details become the agent contract.")
    steps = [
        ("Trigger", "What starts the job?"),
        ("Context", "What must be known?"),
        ("Tools", "Where does work happen?"),
        ("Actions", "What can it do?"),
        ("Approvals", "Where is human review required?"),
        ("Escalation", "When does it ask for help?"),
        ("Success", "How is done defined?"),
    ]
    for i, (title, body) in enumerate(steps):
        x = d.M + Inches((i % 4) * 3.05)
        y = Inches(1.88 + (i // 4) * 1.45)
        card(d, s, x, y, Inches(2.70), Inches(1.05), title, body, fill=b.SOFT, index=str(i + 1), accent=False)
    d.rect(s, d.M, Inches(5.02), d.CW, Inches(0.68), hx("E8F8F4"), line=hx("BFECE3"), radius=0.05)
    d.text(s, "Operator shadowing turns tacit judgment into explicit acceptance criteria.",
           d.M + Inches(0.22), Inches(5.24), d.CW - Inches(0.44), Inches(0.24),
           size=10.1, color=b.DARK_TEAL, bold=True, shrink=True)
    takeaway(d, s, "Do not automate what has not been watched; the hidden work is where trust is created.")
    footer(d, s, page, total)
    add_note(s, "Derived from transcript section on screen recording and narrated shadowing.")


def build_minimum_agent(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "Build the minimum useful agent", "Autonomy should be earned one bounded loop at a time",
                  "Start with one of four useful shapes before adding broad judgment.")
    shapes = [
        ("Draft & approve", "Prepares output; human approves before send"),
        ("Triage", "Classifies, prioritizes, and routes work"),
        ("Coordinator", "Moves work across calendar, CRM, inbox, and ticketing"),
        ("Bounded action", "Executes a narrow, reversible task under policy"),
    ]
    for i, (title, body) in enumerate(shapes):
        x = d.M + Inches((i % 2) * 5.05)
        y = Inches(1.95 + (i // 2) * 1.55)
        fill = b.NAVY if i == 0 else b.SOFT
        card(d, s, x, y, Inches(4.56), Inches(1.16), title, body,
             fill=fill, title_color=b.WHITE if i == 0 else b.NAVY,
             body_color=b.LIGHT_TEAL if i == 0 else b.INK, index=str(i + 1))
    d.rect(s, Inches(10.45), Inches(2.20), Inches(1.20), Inches(2.68), b.NAVY_2, radius=0.06)
    d.text(s, "Earn autonomy", Inches(10.64), Inches(2.60), Inches(0.82), Inches(0.60),
           size=16.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "assistive\n→ bounded\n→ trusted", Inches(10.58), Inches(3.58), Inches(0.92), Inches(0.70),
           size=10.3, color=b.LIGHT_TEAL, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    takeaway(d, s, "The first version must be useful enough to sell and constrained enough to evaluate.")
    footer(d, s, page, total)
    add_note(s, "Minimum useful agent shapes from transcript section.")


def build_wrapper(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "The wrapper makes it SaaS", "The agent does the job; the control room creates the trust customers pay for",
                  "Logs, approvals, controls, analytics, and evals convert automation into a buyable product.")
    flow_node(d, s, d.M, Inches(2.05), Inches(2.35), Inches(1.28), "AI worker", "Does the job", b.NAVY)
    arrow_text(d, s, Inches(3.08), Inches(2.52))
    flow_node(d, s, Inches(3.70), Inches(1.78), Inches(3.30), Inches(1.82), "Control room", "Logs\nApprovals\nSettings\nHandoffs\nAnalytics", hx("173E3C"))
    arrow_text(d, s, Inches(7.28), Inches(2.52))
    flow_node(d, s, Inches(7.90), Inches(2.05), Inches(2.68), Inches(1.28), "Customer trust", "What happened?\nWhy?\nWhat needs review?", hx("144E40"))
    card(d, s, Inches(10.85), Inches(1.78), Inches(1.52), Inches(1.82), "Eval set", "50 real examples\nRight answers\nFailure review", fill=hx("FFF4CF"), accent=False)
    d.rect(s, d.M, Inches(4.34), d.CW, Inches(0.72), b.SOFT, line=b.GRID, radius=0.05)
    d.text(s, "Eval loop: run real work -> inspect failures -> improve controls -> re-test before expanding autonomy.",
           d.M + Inches(0.22), Inches(4.57), d.CW - Inches(0.44), Inches(0.24),
           size=9.8, color=b.NAVY, bold=True, shrink=True)
    takeaway(d, s, "A demo shows automation; the SaaS wrapper shows why production use is trustworthy.")
    footer(d, s, page, total)
    add_note(s, "Native PPTX reconstruction of wrapper and eval visual.")


def build_pilot(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "Sell the pilot like labor", "Start with three same-niche customers, then productize the repeated loop",
                  "Early pricing should match how buyers already buy capacity; sophistication comes after proof.")
    stages = [
        ("Pilot", "3 customers\nsame niche\nsame workflow", b.NAVY),
        ("Learn", "Observe edge cases\ntrack failures\ntighten handoff", hx("163F4A")),
        ("Productize", "Reusable wrapper\nrepeatable onboarding\nstandard evals", hx("144E40")),
        ("Price", "Setup + monthly\nthen usage\nthen outcomes", hx("4A3A12")),
    ]
    for i, (title, body, fill) in enumerate(stages):
        x = d.M + Inches(i * 2.95)
        flow_node(d, s, x, Inches(2.10), Inches(2.30), Inches(1.50), title, body, fill)
        if i < 3:
            arrow_text(d, s, x + Inches(2.36), Inches(2.72))
    bullet_list(d, s, [
        "Sell the result in the buyer’s existing language: receptionist, dispatcher, coordinator, support capacity.",
        "Use the pilot to discover what must be productized, not to pretend the product is finished.",
        "Move toward usage or outcome pricing only once value is observable and repeatable.",
    ], d.M, Inches(4.22), Inches(9.4), Inches(1.05))
    takeaway(d, s, "Labor-like pilots lower friction; productize only after the workflow repeats.")
    footer(d, s, page, total)
    add_note(s, "Commercialization model from transcript section on pilot and pricing.")


def build_moat(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "Own the workflow", "The moat is the operating loop, not the model call",
                  "Workflow memory compounds through context, exceptions, policy, and eval examples.")
    layers = [
        ("Workflow context", "What the customer does, checks, and values"),
        ("Exception library", "What makes cases weird and when to escalate"),
        ("Policy + controls", "What the agent may do without approval"),
        ("Eval memory", "Real examples that define quality over time"),
    ]
    for i, (title, body) in enumerate(layers):
        y = Inches(1.88 + i * 0.78)
        d.rect(s, Inches(1.15 + i * 0.45), y, Inches(8.5 - i * 0.55), Inches(0.60),
               [b.NAVY, b.NAVY_2, hx("163F4A"), hx("144E40")][i], radius=0.04)
        d.text(s, title, Inches(1.40 + i * 0.45), y + Inches(0.20), Inches(2.1), Inches(0.16),
               size=8.3, color=b.WHITE, bold=True, shrink=True)
        d.text(s, body, Inches(3.45 + i * 0.45), y + Inches(0.20), Inches(4.4), Inches(0.16),
               size=7.8, color=b.LIGHT_TEAL, shrink=True)
    card(d, s, Inches(9.40), Inches(2.04), Inches(2.70), Inches(2.18),
         "Defensibility test", "Can a competitor copy the landing page but not the operating history, edge cases, controls, and eval set?", fill=b.SOFT)
    takeaway(d, s, "The durable asset is the workflow operating system around the agent.")
    footer(d, s, page, total)
    add_note(s, "Moat synthesis from own-the-workflow segment.")


def build_plan(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "30-day plan", "Distribution comes from workflow teardowns: old way versus agent way",
                  "Publish proof from the painful workflow, then put spend behind the teardown that converts.")
    steps = [
        ("Days 1-3", "Pick one niche\nList 20 jobs\nScore pain + budget"),
        ("Week 1", "Shadow operators\nWrite trigger/context/rules\nBuild eval set"),
        ("Week 2", "Ship smallest useful agent\nDraft / triage / coordinate"),
        ("Week 3", "Sell 3 pilots\nSetup + monthly\nSame workflow"),
        ("Week 4", "Publish teardown engine\n50 posts\nAds behind winners"),
    ]
    for i, (title, body) in enumerate(steps):
        x = d.M + Inches(i * 2.40)
        fill = [b.NAVY, b.NAVY_2, hx("163F4A"), hx("144E40"), hx("4A3A12")][i]
        flow_node(d, s, x, Inches(2.00), Inches(1.92), Inches(1.80), title, body, fill)
        if i < len(steps) - 1:
            arrow_text(d, s, x + Inches(1.98), Inches(2.73))
    d.rect(s, d.M, Inches(4.42), d.CW, Inches(0.70), hx("E8F8F4"), line=hx("BFECE3"), radius=0.05)
    d.text(s, "Teardown format: painful old way -> smooth agent way -> obvious painkiller.",
           d.M + Inches(0.22), Inches(4.66), d.CW - Inches(0.44), Inches(0.20),
           size=10.1, color=b.DARK_TEAL, bold=True, shrink=True)
    takeaway(d, s, "The next action is a scored workflow shortlist and operator shadowing plan.")
    footer(d, s, page, total)
    add_note(s, "Native PPTX reconstruction of the zero-to-100 plan.")


def build_coverage(d, page, total):
    b = d.b
    s = d.slide(fill=b.WHITE)
    action_header(d, s, "Coverage and source package", "Meaningful screen changes are accounted for without inserting screenshots",
                  "The source package keeps auditability separate from the client-facing deck design.")
    metrics = [
        ("156", "dense frames"),
        ("56", "scene-change frames"),
        ("12", "Excalidraw sources"),
        ("0", "YouTube screenshots used as main visuals"),
    ]
    for i, (num, label) in enumerate(metrics):
        x = d.M + Inches(i * 3.08)
        d.rect(s, x, Inches(1.96), Inches(2.52), Inches(1.10), b.NAVY if i == 3 else b.SOFT, line=b.GRID, radius=0.05, shadow=True)
        d.text(s, num, x + Inches(0.16), Inches(2.18), Inches(0.92), Inches(0.30),
               size=25, color=b.GOLD if i == 3 else b.DARK_TEAL, bold=True, shrink=True)
        d.text(s, label, x + Inches(1.08), Inches(2.30), Inches(1.20), Inches(0.18),
               size=9.6, color=b.WHITE if i == 3 else b.INK, bold=True, shrink=True)
    files = [
        "ai-agents-new-saas-screen-change-coverage.md",
        "ai-agents-new-saas-visual-inventory-v2.md",
        "ai-agents-new-saas-analyst-story-pack.md/json",
        "ai-agents-new-saas-v*-*.excalidraw sources",
    ]
    card(d, s, d.M, Inches(3.70), Inches(5.72), Inches(1.68), "Audit artifacts", "\n".join(files), fill=b.SOFT)
    card(d, s, Inches(6.72), Inches(3.70), Inches(5.10), Inches(1.68), "Delivery status",
         "Draft deck rebuilt using branded-pptx-deck patterns. Preview QA required before promoting to reviewed.", fill=hx("FFF4CF"), accent=False)
    takeaway(d, s, "Markdown and frame files are source/audit material; the client deliverable is the branded PPTX.")
    footer(d, s, page, total)
    add_note(s, "Coverage slide replaces timestamp/source clutter in the main story.")


def build():
    d = Deck(footer="AI Agents Are The New SaaS | Video-to-deck draft")
    total = 12
    build_cover(d, total)
    build_exec_summary(d, 2, total)
    build_storyboard(d, 3, total)
    build_product_job(d, 4, total)
    build_examples(d, 5, total)
    build_scorecard(d, 6, total)
    build_shadow(d, 7, total)
    build_minimum_agent(d, 8, total)
    build_wrapper(d, 9, total)
    build_pilot(d, 10, total)
    build_moat(d, 11, total)
    build_plan(d, 12, total)
    d.save(OUT)


if __name__ == "__main__":
    build()
