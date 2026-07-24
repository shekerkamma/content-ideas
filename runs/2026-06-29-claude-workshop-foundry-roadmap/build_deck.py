#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "branded-pptx-deck" / "scripts"
sys.path.insert(0, str(SKILL))

from pptxkit import Deck, Inches, PP_ALIGN  # noqa: E402


OUT_DIR = Path(__file__).resolve().parent
OUT = OUT_DIR / "claude-foundry-agent-roadmap-reviewed.pptx"
FRAME_SHEET = Path("/tmp/watch-ggwyd4vc/contact_sheet.jpg")


def bullet(text, size=14, color=None, bold=False, space=7):
    spec = {"text": text, "bullet": True, "size": size, "bold": bold, "space_before": space}
    if color is not None:
        spec["color"] = color
    return spec


def label_card(d, s, x, y, w, h, label, body, idx=None, fill=None):
    b = d.b
    d.rect(s, x, y, w, h, fill or b.WHITE, line=b.GRID, radius=0.08, shadow=True)
    if idx:
        d.rect(s, x + Inches(0.18), y + Inches(0.18), Inches(0.45), Inches(0.34), b.NAVY, radius=0.05)
        d.text(s, idx, x + Inches(0.18), y + Inches(0.225), Inches(0.45), Inches(0.18),
               size=10, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
        tx = x + Inches(0.75)
        tw = w - Inches(0.95)
    else:
        tx = x + Inches(0.24)
        tw = w - Inches(0.48)
    d.text(s, label, tx, y + Inches(0.18), tw, Inches(0.28), size=13.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, x + Inches(0.24), y + Inches(0.62), w - Inches(0.48), h - Inches(0.78),
           size=11.2, color=b.INK, shrink=True)


def chip(d, s, x, y, text, fill=None, width=1.45):
    b = d.b
    d.rect(s, x, y, Inches(width), Inches(0.34), fill or b.NAVY_2, radius=0.08)
    d.text(s, text, x + Inches(0.08), y + Inches(0.08), Inches(width - 0.16), Inches(0.16),
           size=9.5, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)


def safe_header(d, s, title, subtitle):
    b = d.b
    d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
    d.text(s, title, d.M, Inches(0.38), d.CW, Inches(0.9), size=24,
           color=b.NAVY, bold=True, font=b.FONT_H, shrink=True)
    d.rect(s, d.M, Inches(1.2), Inches(1.45), Inches(0.05), b.TEAL)
    d.text(s, subtitle, d.M, Inches(1.36), d.CW, Inches(0.46), size=11.5,
           color=b.MUTED, shrink=True)


def section(d, s, number, title, subtitle):
    b = d.b
    d.rect(s, 0, 0, Inches(0.2), d.H, b.TEAL)
    d.text(s, f"SECTION {number}", Inches(0.72), Inches(1.65), d.CW, Inches(0.28),
           size=13, color=b.TEAL, bold=True)
    d.text(s, title, Inches(0.72), Inches(2.05), Inches(9.4), Inches(1.1),
           size=42, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, Inches(0.72), Inches(3.35), Inches(1.4), Inches(0.05), b.TEAL)
    d.text(s, subtitle, Inches(0.72), Inches(3.6), Inches(8.8), Inches(0.8),
           size=17, color=b.LIGHT_TEAL, shrink=True)


def add_footer_all(d):
    total = d.n
    for i, slide in enumerate(d.prs.slides, 1):
        dark = i in {1, 4, 13}
        d.footer(slide, i, total, dark=dark)


def build():
    d = Deck(footer="Claude + Microsoft Foundry implementation roadmap | draft based on public workshop materials")
    b = d.b

    # 1. Cover
    s = d.slide(fill=b.NAVY)
    d.rect(s, Inches(10.25), 0, Inches(3.08), d.H, b.NAVY_2)
    d.rect(s, Inches(10.25), 0, Inches(0.08), d.H, b.TEAL)
    d.text(s, "IMPLEMENTATION SOLUTION", d.M, Inches(0.78), Inches(5.8), Inches(0.3),
           size=13.5, color=b.TEAL, bold=True)
    d.text(s, "Claude Agents In Microsoft Foundry", d.M, Inches(1.28), Inches(8.7), Inches(1.55),
           size=36, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(2.85), Inches(1.7), Inches(0.06), b.TEAL)
    d.text(s, "A 90-day roadmap to move from workshop prototype to governed enterprise agent service.",
           d.M, Inches(3.18), Inches(7.7), Inches(0.7), size=19, color=b.LIGHT_TEAL, shrink=True)
    x = d.M
    for txt, w in [("Claude reasoning", 1.7), ("Foundry Agent Service", 2.1), ("MCP + tools", 1.45), ("Prod controls", 1.55)]:
        chip(d, s, x, Inches(4.45), txt, width=w)
        x += Inches(w + 0.16)
    d.text(s, "Source basis: public LinkedIn workshop clip + aka.ms/claude-workshop launcher + Microsoft Learn Agent Service docs.",
           d.M, Inches(6.25), Inches(8.4), Inches(0.38), size=10.5, color=b.MUTED, shrink=True)

    # 2. Executive summary
    s = d.slide(fill=b.WHITE)
    safe_header(d, s, "The Answer: Treat The Workshop As A Production Blueprint",
                "The practical move is not another demo; it is a governed agent program with a narrow first use case.")
    d.rect(s, d.M, Inches(1.78), d.CW, Inches(0.86), b.NAVY, radius=0.06)
    d.text(s, "BLUF: Stand up a Foundry-hosted Claude agent in 30 days, connect enterprise tools in 60, and graduate one measurable workflow to production by day 90.",
           d.M + Inches(0.28), Inches(1.98), d.CW - Inches(0.56), Inches(0.42), size=13.2, color=b.WHITE, bold=True, shrink=True)
    cols = [
        ("Situation", "Agent work is shifting from chat responses to systems that plan, use long context, invoke tools, and operate inside enterprise controls."),
        ("Insight", "Microsoft Foundry provides the control plane: Agent Service, model deployment, tools, security, observability, evaluation, and publishing paths."),
        ("Recommendation", "Anchor the program on one workflow where Claude reasoning plus Foundry governance can show measurable cycle-time or quality improvement.")
    ]
    for i, (h, body) in enumerate(cols):
        label_card(d, s, d.M + Inches(i * 4.1), Inches(3.0), Inches(3.82), Inches(2.28), h, body, idx=f"0{i+1}")
    d.rect(s, d.M, Inches(5.72), d.CW, Inches(0.62), b.GOLD, radius=0.06)
    d.text(s, "THE ASK: approve a 90-day pilot with a named business owner, one production integration path, and a governance gate at each phase.",
           d.M + Inches(0.24), Inches(5.86), d.CW - Inches(0.48), Inches(0.32), size=11.7, color=b.NAVY, bold=True, shrink=True)

    # 3. Why now
    s = d.slide(fill=b.WHITE)
    safe_header(d, s, "Why This Is Ready For Enterprise Implementation",
                "The core constraints are no longer model access; they are tool access, controls, measurement, and ownership.")
    points = [
        ("Reasoning", "Claude is positioned in the workshop as the reasoning layer for planning, long context, and multi-step agent behavior."),
        ("Control plane", "Foundry gives teams a place to deploy models, build agents, add tools, evaluate behavior, trace runs, and operate at scale."),
        ("Enterprise stack", "Microsoft identity, security, governance, and publishing paths reduce the gap between prototype and production."),
        ("Adoption wedge", "The workshop flow is concrete enough to convert into a field implementation package: deploy, connect, test, govern, scale.")
    ]
    for i, (h, body) in enumerate(points):
        x = d.M + Inches((i % 2) * 6.15)
        y = Inches(1.82 + (i // 2) * 2.2)
        label_card(d, s, x, y, Inches(5.7), Inches(1.65), h, body, idx=str(i + 1))
    d.text(s, "Design principle: the pilot must prove operating capability, not just model capability.",
           d.M, Inches(6.18), d.CW, Inches(0.32), size=15, color=b.ACCENT, bold=True)

    # 4. Source capture
    s = d.slide(fill=b.NAVY)
    section(d, s, "01", "Public Workshop Signal", "What the source material verifies, and what remains an implementation assumption.")

    # 5. Source evidence
    s = d.slide(fill=b.WHITE)
    safe_header(d, s, "The Workshop Verifies A Practical Build Sequence",
                "The public clip and launcher validate the direction; the private Skillable lab steps were not exposed.")
    if FRAME_SHEET.exists():
        d.picture_centered(s, FRAME_SHEET, top=Inches(1.7), width=Inches(6.05), max_bottom=Inches(6.25))
        d.rect(s, Inches(6.92), Inches(1.72), Inches(0.04), Inches(4.65), b.TEAL)
        left = Inches(7.18)
    else:
        left = d.M
    d.text(s, [
        bullet("Workshop title: Build AI Agents using Claude in Microsoft Foundry.", size=12.7),
        bullet("Stated outcomes: deploy Claude models in Foundry, plug the model into an agent, and give that agent tools.", size=12.7),
        bullet("Platform claims in the clip: Foundry models, Agent Service, tools/integrations, enterprise security, observability, governance, and 1,400+ connectors/MCP tools.", size=12.7),
        bullet("Public launcher: aka.ms/claude-workshop redirects to Skillable/LabOnDemand room with Microsoft branding, but current event sign-in returns page-not-found.", size=12.7),
    ], left, Inches(1.85), Inches(5.45), Inches(3.7), shrink=True)
    d.rect(s, left, Inches(5.38), Inches(5.45), Inches(0.78), b.SOFT, line=b.GRID, radius=0.05)
    d.text(s, "Caveat: private lab steps were not exposed; this roadmap is built from verified public materials.",
           left + Inches(0.16), Inches(5.58), Inches(5.12), Inches(0.26), size=8.0, color=b.MUTED, bold=True, shrink=True)

    # 6. Solution architecture
    s = d.slide(fill=b.WHITE)
    safe_header(d, s, "Target Architecture: A Governed Agent Service Around Claude",
                "The production design separates user channels, agent orchestration, tools, knowledge, controls, and observability.")
    lanes = [
        ("Channels", "Teams, Copilot, web app, API"),
        ("Agent runtime", "Foundry Agent Service / Responses API"),
        ("Model layer", "Claude models deployed through Foundry"),
        ("Tools", "MCP servers, built-in tools, enterprise connectors"),
        ("Data", "RAG indexes, system APIs, business records"),
        ("Controls", "Identity, approvals, policy, evals, tracing")
    ]
    y = Inches(1.72)
    for i, (h, body) in enumerate(lanes):
        x = d.M + Inches(i * 2.05)
        d.rect(s, x, y, Inches(1.78), Inches(3.1), b.SOFT if i % 2 == 0 else b.WHITE, line=b.GRID, radius=0.05)
        d.text(s, h, x + Inches(0.14), y + Inches(0.22), Inches(1.5), Inches(0.42), size=13, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, body, x + Inches(0.16), y + Inches(1.04), Inches(1.46), Inches(1.2), size=10.4, color=b.INK, align=PP_ALIGN.CENTER, shrink=True)
        if i < len(lanes) - 1:
            d.text(s, "→", x + Inches(1.82), y + Inches(1.28), Inches(0.22), Inches(0.28), size=18, color=b.ACCENT, bold=True)
    d.rect(s, d.M, Inches(5.32), d.CW, Inches(0.68), b.NAVY, radius=0.06)
    d.text(s, "Architecture decision: keep enterprise data and tools behind governed connectors; let the agent reason over tasks, not bypass system-of-record controls.",
           d.M + Inches(0.24), Inches(5.48), d.CW - Inches(0.48), Inches(0.34), size=11.2, color=b.WHITE, bold=True, shrink=True)

    # 7. Use-case realization
    s = d.slide(fill=b.WHITE)
    safe_header(d, s, "Detailed Use Case: Enterprise Support Resolution Agent",
                "A realistic first workflow for proving Claude reasoning plus Foundry operating controls.")
    d.rect(s, d.M, Inches(1.72), Inches(3.05), Inches(4.8), b.TEAL, radius=0.04)
    d.text(s, "Challenge", d.M + Inches(0.22), Inches(1.98), Inches(2.6), Inches(0.25), size=16, color=b.NAVY, bold=True)
    d.text(s, "Support teams lose time triaging tickets, searching policy, drafting replies, and escalating incomplete cases across systems.",
           d.M + Inches(0.22), Inches(2.42), Inches(2.55), Inches(1.3), size=10.7, color=b.NAVY, shrink=True)
    d.text(s, "How it is realized", d.M + Inches(0.22), Inches(4.0), Inches(2.6), Inches(0.25), size=16, color=b.NAVY, bold=True)
    d.text(s, "Claude plans the resolution path. Foundry manages tools, identity, tracing, evaluation, and deployment. Humans approve sensitive actions.",
           d.M + Inches(0.22), Inches(4.38), Inches(2.55), Inches(1.18), size=10.7, color=b.NAVY, shrink=True)
    steps = [
        ("1. Intake", "Classify ticket, retrieve context, detect missing fields"),
        ("2. Reason", "Plan answer or escalation using policy + history"),
        ("3. Act", "Draft reply, update CRM, open follow-up task"),
        ("4. Govern", "Log trace, score response, route exceptions")
    ]
    for i, (h, body) in enumerate(steps):
        x = Inches(4.02 + (i % 2) * 3.92)
        y = Inches(1.82 + (i // 2) * 1.62)
        label_card(d, s, x, y, Inches(3.58), Inches(1.25), h, body)
    d.rect(s, Inches(4.02), Inches(5.14), Inches(7.55), Inches(0.72), b.NAVY, radius=0.05)
    d.text(s, "Stack: Claude in Foundry + Agent Service + MCP/tool connectors + RAG + Microsoft identity/security + eval/tracing dashboards",
           Inches(4.24), Inches(5.32), Inches(7.1), Inches(0.36), size=8.8, color=b.WHITE, bold=True, shrink=True)

    # 8. Roadmap
    s = d.slide(fill=b.WHITE)
    safe_header(d, s, "90-Day Roadmap: From Lab To Production-Ready Agent",
                "Gates are designed to kill weak pilots early and scale only what can be operated.")
    phases = [
        ("0-15 days", "Foundation", "Confirm workflow, success metric, data access, risk class, and business owner."),
        ("16-30 days", "Prototype", "Deploy Claude model, create first Foundry agent, connect sandbox tools, define eval set."),
        ("31-60 days", "Pilot", "Add enterprise connectors, human approval, telemetry, prompt/tool hardening, and UAT."),
        ("61-90 days", "Production gate", "Security review, monitoring, runbook, release plan, KPI baseline, and scale decision.")
    ]
    for i, (time, h, body) in enumerate(phases):
        x = d.M + Inches(i * 3.06)
        d.rect(s, x, Inches(1.9), Inches(2.72), Inches(3.55), b.SOFT, line=b.GRID, radius=0.05, shadow=True)
        d.rect(s, x, Inches(1.9), Inches(2.72), Inches(0.52), b.NAVY if i < 3 else b.GOLD, radius=0.05)
        d.text(s, time, x + Inches(0.14), Inches(2.08), Inches(2.44), Inches(0.14), size=10.5,
               color=b.WHITE if i < 3 else b.NAVY, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, h, x + Inches(0.2), Inches(2.7), Inches(2.32), Inches(0.42), size=15, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, body, x + Inches(0.25), Inches(3.45), Inches(2.22), Inches(1.08), size=11, color=b.INK, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, "Exit criteria: named use case, working agent, tool traces, evaluation results, control evidence, production decision.",
           d.M, Inches(5.96), d.CW, Inches(0.34), size=11.8, color=b.ACCENT, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    # 9. Workstreams
    s = d.slide(fill=b.WHITE)
    safe_header(d, s, "Implementation Workstreams And Ownership",
                "The program needs product, platform, security, data, and change management from day one.")
    rows = [
        ("Product", "Use-case scope, user journey, acceptance criteria", "Business owner + PM"),
        ("Platform", "Foundry project, model deployment, agent runtime, environments", "AI platform lead"),
        ("Tools/data", "MCP/connectors, RAG, API permissions, test fixtures", "Integration + data owners"),
        ("Governance", "Risk review, human-in-loop, logging, policy, security gate", "Security + compliance"),
        ("Adoption", "Pilot cohort, training, feedback loop, rollout comms", "Ops lead + enablement")
    ]
    x0, y0 = d.M, Inches(1.82)
    widths = [2.1, 6.15, 3.7]
    headers = ["Workstream", "Deliverables", "Owner"]
    x = x0
    for w, h in zip(widths, headers):
        d.rect(s, x, y0, Inches(w), Inches(0.58), b.NAVY, radius=0.02)
        d.text(s, h, x + Inches(0.12), y0 + Inches(0.17), Inches(w - 0.24), Inches(0.2), size=9.4, color=b.WHITE, bold=True)
        x += Inches(w)
    for r, row in enumerate(rows):
        y = y0 + Inches(0.58 + r * 0.68)
        x = x0
        for c, (w, val) in enumerate(zip(widths, row)):
            d.rect(s, x, y, Inches(w), Inches(0.68), b.SOFT if r % 2 == 0 else b.WHITE, line=b.GRID)
            d.text(s, val, x + Inches(0.12), y + Inches(0.17), Inches(w - 0.24), Inches(0.22),
                   size=10.7 if c else 11.2, color=b.NAVY if c == 0 else b.INK, bold=(c == 0), shrink=True)
            x += Inches(w)
    d.rect(s, d.M, Inches(6.02), d.CW, Inches(0.38), b.SOFT, line=b.GRID)
    d.text(s, "Practical staffing: 1 product lead, 1 Foundry/AI engineer, 1 integration engineer, 1 security/compliance partner, 5-10 pilot users.",
           d.M + Inches(0.16), Inches(6.09), d.CW - Inches(0.32), Inches(0.22), size=9.6, color=b.MUTED, bold=True, shrink=True)

    # 10. Tool strategy
    s = d.slide(fill=b.WHITE)
    safe_header(d, s, "Tool Strategy: Start Narrow, Then Expand Through Governed Connectors",
                "A useful agent needs real tools, but tool access must be staged by business risk.")
    stages = [
        ("Read-only", "Search knowledge base, retrieve policy, inspect ticket context", b.TEAL),
        ("Draft actions", "Prepare reply, suggest next task, create proposed record update", b.ACCENT),
        ("Approved writes", "Human-reviewed updates into CRM, ITSM, email, or workflow tools", b.GOLD),
        ("Autonomous loops", "Only after eval thresholds, monitoring, rollback, and exception routing", b.CORAL)
    ]
    for i, (h, body, col) in enumerate(stages):
        y = Inches(1.85 + i * 0.94)
        d.rect(s, d.M, y, Inches(2.05), Inches(0.58), col, radius=0.05)
        d.text(s, h, d.M + Inches(0.14), y + Inches(0.2), Inches(1.77), Inches(0.12), size=10.8,
               color=b.NAVY if col == b.GOLD else b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, body, Inches(3.05), y + Inches(0.16), Inches(8.9), Inches(0.2), size=12.2, color=b.INK, shrink=True)
    d.rect(s, d.M, Inches(5.85), d.CW, Inches(0.52), b.NAVY, radius=0.05)
    d.text(s, "Rule: every tool gets a purpose, permission boundary, test fixture, abuse case, trace requirement, and rollback path before pilot use.",
           d.M + Inches(0.2), Inches(5.98), d.CW - Inches(0.4), Inches(0.28), size=10.2, color=b.WHITE, bold=True, shrink=True)

    # 11. Governance and measurement
    s = d.slide(fill=b.WHITE)
    safe_header(d, s, "Governance: Measure The Agent Before Scaling It",
                "The roadmap should make operational evidence visible before production approval.")
    metrics = [
        ("Quality", "Resolution accuracy, citation quality, policy adherence, escalation correctness"),
        ("Safety", "Tool-call violations, PII exposure, unauthorized action attempts, human override rate"),
        ("Operations", "Latency, cost per case, trace completeness, incident count, fallback rate"),
        ("Business", "Cycle time, first-contact resolution, user CSAT, avoided rework, adoption")
    ]
    for i, (h, body) in enumerate(metrics):
        x = d.M + Inches((i % 2) * 6.05)
        y = Inches(1.85 + (i // 2) * 1.8)
        label_card(d, s, x, y, Inches(5.62), Inches(1.32), h, body, idx=str(i + 1))
    d.text(s, [
        bullet("Evaluation pack: golden tasks, adversarial prompts, tool-call expectations, red-team cases, and regression tests.", size=12),
        bullet("Release gates: no production release without trace visibility, human approval path, KPI baseline, and exception runbook.", size=12),
    ], d.M, Inches(5.65), d.CW, Inches(0.82), shrink=True)

    # 12. Commercial pitch / ask
    s = d.slide(fill=b.WHITE)
    safe_header(d, s, "Pilot Offer: A Fixed-Scope Agent Implementation Sprint",
                "Package the workshop into an executive-ready adoption motion with clear deliverables.")
    deliverables = [
        ("Week 1", "Use-case framing, architecture, data/tool readiness, governance plan"),
        ("Weeks 2-4", "Foundry project, Claude deployment, prototype agent, sandbox tools, eval harness"),
        ("Weeks 5-8", "Pilot workflow, enterprise integrations, telemetry, user feedback, hardening"),
        ("Weeks 9-12", "Production gate, runbook, KPI readout, scale recommendation, backlog")
    ]
    for i, (h, body) in enumerate(deliverables):
        label_card(d, s, d.M + Inches((i % 2) * 6.05), Inches(1.85 + (i // 2) * 1.62),
                   Inches(5.62), Inches(1.18), h, body)
    d.rect(s, d.M, Inches(5.35), Inches(3.7), Inches(0.88), b.GOLD, radius=0.05)
    d.text(s, "Decision needed", d.M + Inches(0.2), Inches(5.53), Inches(3.3), Inches(0.24), size=10.8, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, "Select use case + business owner + pilot cohort", d.M + Inches(0.22), Inches(5.83), Inches(3.26), Inches(0.24), size=7.8, color=b.NAVY, align=PP_ALIGN.CENTER, shrink=True)
    d.rect(s, Inches(4.7), Inches(5.35), Inches(7.05), Inches(0.88), b.NAVY, radius=0.05)
    d.text(s, "Next step: run a 2-hour implementation design workshop and produce a signed 90-day delivery plan.",
           Inches(4.96), Inches(5.58), Inches(6.55), Inches(0.34), size=9.6, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, shrink=True)

    # 13. Sources
    s = d.slide(fill=b.NAVY)
    section(d, s, "02", "Sources And Assumptions", "Facts are separated from implementation recommendations.")
    d.text(s, [
        bullet("LinkedIn public embed: John Peslar post and 8:53 workshop video; analyzed via direct MP4 and auto-caption SRT exposed in the embed HTML.", size=11.6, color=b.LIGHT_TEAL),
        bullet("Workshop short link: https://aka.ms/claude-workshop redirects to https://skill.info/cupcakes and a Skillable/LabOnDemand Microsoft workshop launcher.", size=11.6, color=b.LIGHT_TEAL),
        bullet("Microsoft Learn: Azure AI Foundry Agent Service overview, updated June 2, 2026, used for current platform framing.", size=11.6, color=b.LIGHT_TEAL),
        bullet("Assumption: enterprise client wants a governed 90-day pilot that can graduate to production; use case and integrations should be finalized in discovery.", size=11.6, color=b.LIGHT_TEAL),
    ], Inches(0.88), Inches(4.25), Inches(11.6), Inches(1.95), shrink=True)

    add_footer_all(d)
    d.save(OUT)


if __name__ == "__main__":
    build()
