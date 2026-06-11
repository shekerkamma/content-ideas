#!/usr/bin/env python3
"""Board deck builder — AI-Native Engineering Strategy (CIOS acceptance run).
Uses the sanctioned branded pptxkit workflow. Kept in the run folder per
CIOS-GOV-003 #8. Slide contract per CIOS-OUT-005: <=5 bullets/slide,
<=12 words/bullet, speaker notes 100-150 words, footer + page number."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / ".claude/skills/branded-pptx-deck/scripts"))
from pptx.util import Inches  # noqa: E402
from pptxkit import Deck, PP_ALIGN, MSO_ANCHOR  # noqa: E402

OUT = Path(__file__).parent / "deliverables" / "ai-native-engineering-strategy-draft.pptx"
d = Deck(footer="AI-Native Engineering Strategy · CIOS acceptance run · 2026-06-10")
b = d.b
TOTAL = 11


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


def bullets(items, size=15):
    return [{"text": t, "bullet": True, "size": size, "space_before": 6} for t in items]


def card(s, left, top, w, h, title, body, *, title_color=None, body_size=12.5):
    d.rect(s, left, top, w, h, b.SOFT, radius=0.06)
    d.rect(s, left, top, Inches(0.07), h, b.TEAL)
    d.text(s, title, left + Inches(0.22), top + Inches(0.14), w - Inches(0.4), Inches(0.34),
           size=14, bold=True, color=title_color or b.NAVY)
    d.text(s, body, left + Inches(0.22), top + Inches(0.52), w - Inches(0.4), h - Inches(0.68),
           size=body_size, color=b.INK, shrink=True)


# ── 1 · Title ────────────────────────────────────────────────────────────────
s = d.slide(b.NAVY)
d.rect(s, 0, Inches(7.34), d.W, Inches(0.16), b.TEAL)
d.text(s, "AI-Native Engineering Strategy", d.M, Inches(2.5), d.CW, Inches(1.0),
       size=44, bold=True, color=b.WHITE)
d.text(s, "From copilot seats to a compounding engineering system",
       d.M, Inches(3.6), d.CW, Inches(0.5), size=20, color=b.TEAL)
d.text(s, "Board briefing · 400-developer enterprise software organization · June 2026",
       d.M, Inches(4.25), d.CW, Inches(0.4), size=13, color=b.MUTED)
d.text(s, "DRAFT — CIOS acceptance run", d.M, Inches(6.6), Inches(5), Inches(0.3),
       size=11, color=b.AMBER, bold=True)
d.footer(s, 1, TOTAL, dark=True)
notes(s, "This briefing answers one question: what should our AI-native engineering "
         "strategy be? The recommendation is not a tool purchase. It is a two-part "
         "investment: owned engineering context that any agent platform can run, and an "
         "operating model where agent autonomy is earned per use case. We will show where "
         "the organization sits on a five-rung adoption ladder, the reference architecture "
         "grounded in the open-source OpenHands platform, a 90-day gated pilot, and the "
         "governance package that makes the CISO comfortable. The decision requested today "
         "is approval of the pilot and the context-infrastructure workstream.")

# ── 2 · Executive summary ────────────────────────────────────────────────────
s = d.slide(b.WHITE)
d.header(s, "Build the system, not the seat count", "Executive summary")
card(s, d.M, Inches(1.8), Inches(3.9), Inches(4.6), "The shift",
     [{"text": t, "bullet": True, "size": 12.5, "space_before": 5} for t in [
         "Copilots raise typing speed",
         "Agents change what teams ship",
         "Context and specs are the moat",
         "Models are swappable engines"]])
card(s, d.M + Inches(4.15), Inches(1.8), Inches(3.9), Inches(4.6), "The strategy",
     [{"text": t, "bullet": True, "size": 12.5, "space_before": 5} for t in [
         "Own the context layer",
         "Adopt spec-driven delivery",
         "Earn autonomy per use case",
         "Own an open agent platform"]])
card(s, d.M + Inches(8.3), Inches(1.8), Inches(3.9), Inches(4.6), "The ask",
     [{"text": t, "bullet": True, "size": 12.5, "space_before": 5} for t in [
         "Approve 90-day gated pilot",
         "Fund context infrastructure",
         "Platform choice after pilot data",
         "Rung 4 within 12 months"]])
d.footer(s, 2, TOTAL)
notes(s, "Three columns: the shift, the strategy, the ask. The shift: autocomplete "
         "tools improve individual typing; agentic delivery changes team output — that is "
         "where competitors will compound. The strategy: four pillars detailed in this "
         "deck — owned context, specification discipline, earned autonomy, and an open "
         "platform layer we control. The ask: approve a 90-day gated pilot on two to "
         "three scoped workstreams, fund the engineering context infrastructure that every "
         "agent host can run, and defer the cloud-versus-self-hosted platform decision "
         "until the pilot produces data-residency and cost evidence.")

# ── 3 · Why now ──────────────────────────────────────────────────────────────
s = d.slide(b.WHITE)
d.header(s, "The bottleneck moved from models to context", "Why now")
rows = [
    ("Models commoditizing", "Frontier capability ships quarterly; advantage decays in weeks"),
    ("Context is scarce", "Specs, skills and memory are owned assets that compound"),
    ("Platforms matured", "Open, MIT-licensed agent stacks now run laptop to Kubernetes"),
    ("Operating model lags", "Most enterprises stalled at copilot stage without governance"),
]
y = Inches(1.9)
for title, body in rows:
    d.rect(s, d.M, y, Inches(3.3), Inches(0.92), b.NAVY, radius=0.08)
    d.text(s, title, d.M + Inches(0.2), y + Inches(0.18), Inches(3.0), Inches(0.6),
           size=14, bold=True, color=b.WHITE, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.text(s, body, d.M + Inches(3.6), y + Inches(0.18), Inches(8.5), Inches(0.6),
           size=13.5, color=b.INK, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    y += Inches(1.12)
d.footer(s, 3, TOTAL)
notes(s, "Why act now rather than wait another model cycle. First, frontier models are "
         "commoditizing — capability gaps close within weeks, so model choice is not a "
         "strategy. Second, the scarce asset is context: your specifications, skills, and "
         "institutional memory, which compound and are fully owned. Third, the platform "
         "layer matured — open, MIT-licensed agent stacks like OpenHands now deploy from a "
         "developer laptop to self-hosted Kubernetes. Fourth, the constraint at peer "
         "organizations is the operating model: most are stalled at the copilot stage "
         "because governance, not technology, is missing. That is the gap this strategy "
         "closes.")

# ── 4 · Maturity ladder ──────────────────────────────────────────────────────
s = d.slide(b.WHITE)
d.header(s, "You are at rung 2 of 5 — value starts at rung 3", "AI-native adoption ladder")
rungs = [
    ("1 · Copilot", "Autocomplete; individual productivity", False),
    ("2 · Agent-assisted", "Interactive agents, scoped tasks, engineer reviews", True),
    ("3 · Agent-executed", "Headless agents on issues and PRs, behind gates", False),
    ("4 · Agent-native", "Specs in, reviewed PRs out", False),
    ("5 · Compounding", "Context and skills versioned as engineering IP", False),
]
y = Inches(6.0)
x = d.M
w = Inches(2.28)
for i, (title, body, here) in enumerate(rungs):
    h = Inches(1.1 + i * 0.75)
    top = y - h + Inches(0.5)
    fill = b.TEAL if here else (b.NAVY if i >= 2 else b.GRID)
    tcol = b.WHITE if (here or i >= 2) else b.INK
    d.rect(s, x, top, w, h, fill, radius=0.05)
    d.text(s, title, x + Inches(0.12), top + Inches(0.1), w - Inches(0.24), Inches(0.3),
           size=12.5, bold=True, color=tcol, shrink=True)
    d.text(s, body, x + Inches(0.12), top + Inches(0.44), w - Inches(0.24), h - Inches(0.55),
           size=10.5, color=tcol, shrink=True)
    if here:
        d.text(s, "YOU ARE HERE", x, top - Inches(0.34), w, Inches(0.28),
               size=11, bold=True, color=b.DARK_TEAL, align=PP_ALIGN.CENTER)
    x += w + Inches(0.18)
d.footer(s, 4, TOTAL)
notes(s, "The adoption ladder stages the whole strategy. Rung one is copilot autocomplete. "
         "Rung two — where a 400-developer organization with copilot seats and some agent "
         "experimentation sits today — is interactive agent assistance. Rung three is where "
         "business value inflects: agents execute scoped work headlessly behind review "
         "gates and budgets. Rung four is agent-native delivery: engineers write "
         "specifications and review output. Rung five is the end state — context, skills, "
         "and specs versioned as compounding engineering IP. The 90-day pilot targets rung "
         "three; the twelve-month roadmap targets rung four. Each rung is earned with "
         "evidence, never granted platform-wide.")

# ── 5 · Strategy pillars ─────────────────────────────────────────────────────
s = d.slide(b.WHITE)
d.header(s, "Four pillars, one operating model", "Strategy")
P = [
    ("Context over model choice", "Folders-and-files brain portable across agent hosts; sub-agents are plain Markdown"),
    ("Spec-driven delivery", "Execution-grade specs let agents build without ambiguity"),
    ("Earned autonomy", "Keys not prompts: sandboxes, confirmation policies, caps"),
    ("Owned platform layer", "MIT-licensed core, multi-LLM, laptop CLI to private-VPC Kubernetes"),
]
pos = [(d.M, Inches(1.85)), (d.M + Inches(6.1), Inches(1.85)),
       (d.M, Inches(4.35)), (d.M + Inches(6.1), Inches(4.35))]
for (title, body), (x, y) in zip(P, pos):
    card(s, x, y, Inches(5.9), Inches(2.25), title, body, body_size=13)
d.footer(s, 5, TOTAL)
notes(s, "Pillar one: the durable asset is owned context — routing files, skills, specs, "
         "memory — portable across Claude Code, Codex, and OpenHands, which defines "
         "sub-agents as plain Markdown files. Pillar two: specification discipline is the "
         "new senior-engineer skill; agents scale past toy tasks when an execution-grade "
         "spec removes ambiguity. Pillar three: autonomy is earned — write actions sit "
         "behind action-confirmation policies, sandbox isolation, and budget caps; a "
         "prompt is never a permission layer. Pillar four: own the platform the way you "
         "own CI — the MIT-licensed OpenHands core is multi-LLM and deploys anywhere, "
         "which changes the buy-versus-build calculus permanently.")

# ── 6 · Reference architecture ───────────────────────────────────────────────
s = d.slide(b.WHITE)
d.header(s, "Three swappable layers, one governance wrap", "Reference architecture")
layers = [
    ("CONTEXT", "Repo brain: routing files · skills · specs · memory", b.TEAL, b.NAVY),
    ("EXECUTION", "OpenHands: SDK · CLI · Cloud · Enterprise (Helm/K8s, private VPC)", b.NAVY, b.WHITE),
    ("INTEGRATION", "MCP servers · scoped service accounts · GitHub workflows", b.NAVY_2, b.WHITE),
]
y = Inches(1.95)
for name, body, fill, tcol in layers:
    d.rect(s, d.M + Inches(1.2), y, Inches(9.8), Inches(1.05), fill, radius=0.06)
    d.text(s, name, d.M + Inches(1.45), y + Inches(0.12), Inches(2.2), Inches(0.8),
           size=15, bold=True, color=tcol, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, body, d.M + Inches(3.75), y + Inches(0.12), Inches(7.0), Inches(0.8),
           size=13, color=tcol, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    y += Inches(1.3)
d.rect(s, d.M + Inches(1.2), y, Inches(9.8), Inches(0.85), b.LIGHT_TEAL, radius=0.06)
d.text(s, "GOVERNANCE — roles/permissions · sandboxes · confirmation policies · budget caps",
       d.M + Inches(1.45), y + Inches(0.12), Inches(9.3), Inches(0.6),
       size=13, bold=True, color=b.DARK_TEAL, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.text(s, "All execution-layer primitives verified against OpenHands docs, June 2026",
       d.M, Inches(6.55), d.CW, Inches(0.3), size=10.5, color=b.MUTED, italic=True)
d.footer(s, 6, TOTAL)
notes(s, "The architecture separates three layers that swap independently. The context "
         "layer is the repo-based brain any agent host cold-starts from. The execution "
         "layer is OpenHands: SDK for codified agents, CLI for interactive work, and the "
         "Enterprise Helm chart for self-hosted Kubernetes in our VPC when data residency "
         "demands it. The integration layer reaches live systems through MCP servers with "
         "scoped service accounts — read first, write earned. Governance wraps all three: "
         "organization roles and permissions, Docker or Apptainer sandbox isolation, "
         "action-confirmation policies, and budget caps on every unattended run. Every "
         "primitive named here is documented in the OpenHands docs as of June 2026.")

# ── 7 · Buy vs build ─────────────────────────────────────────────────────────
s = d.slide(b.WHITE)
d.header(s, "Hybrid: buy the harness, own the platform",
         "Buy vs build — and the context layer is never rented")
card(s, d.M, Inches(1.85), Inches(5.9), Inches(4.4), "BUY — interactive work",
     bullets(["Commercial harnesses for developers", "Subscription economics fit interactive use",
              "Zero platform maintenance", "Swappable as models leapfrog"], size=13))
card(s, d.M + Inches(6.1), Inches(1.85), Inches(5.9), Inches(4.4), "OWN — unattended work + context",
     bullets(["MIT-licensed OpenHands core", "Self-hosted where audit and budget live",
              "Context layer is never rented", "Avoids per-seat platform lock-in"], size=13))
d.footer(s, 7, TOTAL)
notes(s, "This is not a binary buy-versus-build decision. Buy the interactive harness: "
         "commercial agent tools have the best developer experience and subscription "
         "economics for hands-on work, and they stay swappable. Own two things: first, "
         "the unattended execution layer — scheduled and event-driven agent work runs on "
         "owned OpenHands infrastructure where audit logging and budget enforcement are "
         "under our control; second, the context layer — specifications, skills, and "
         "memory are never rented, because they are the compounding asset. This hybrid "
         "keeps leverage with vendors while the moat stays in-house.")

# ── 8 · 90-day pilot ─────────────────────────────────────────────────────────
s = d.slide(b.WHITE)
d.header(s, "90-day gated pilot: prove rung 3 on scoped work", "Pilot design")
cols = [
    ("Select", ["2–3 scoped workstreams", "Objective done-definitions", "Existing test coverage",
                "PR review + TODO automation first"]),
    ("Gate", ["Agents propose, humans dispose", "Least-privilege keys", "Sandboxed execution",
              "Caps on every unattended run"]),
    ("Measure", ["Cycle time vs baseline", "Review throughput", "Defect escape rate",
                 "Cost per merged PR"]),
]
x = d.M
for title, items in cols:
    card(s, x, Inches(1.85), Inches(3.9), Inches(4.4), title, bullets(items, size=12.5))
    x += Inches(4.15)
d.footer(s, 8, TOTAL)
notes(s, "The pilot proves rung three safely. Selection uses a scoring rubric: scoped "
         "repository surface, objective definitions of done, read-mostly risk profiles, "
         "measurable cycle time, and existing test coverage. Pull-request review and TODO "
         "implementation are documented OpenHands GitHub-workflow patterns, making them "
         "natural first candidates. Gating is non-negotiable: agents propose, tests and "
         "humans dispose; least-privilege credentials; sandboxed execution; a budget cap "
         "on every unattended run. Measurement is against a pre-pilot baseline we capture "
         "in the first two weeks: cycle time, review throughput, defect escape rate, and "
         "cost per merged pull request. Pilot data drives the platform deployment decision.")

# ── 9 · Roadmap ──────────────────────────────────────────────────────────────
s = d.slide(b.WHITE)
d.header(s, "Assess → Pilot → Platform → Scale → Compound", "12-month roadmap")
phases = [
    ("Assess", "Wks 1–2", "Maturity baseline; pilot selection"),
    ("Pilot", "Wks 3–14", "Gated autonomy; metrics vs baseline"),
    ("Platform", "Wks 15–20", "Cloud vs self-hosted from pilot data"),
    ("Scale", "Mo 6–9", "Context infra; team upskilling"),
    ("Compound", "Mo 9–12", "Specs and skills as versioned IP"),
]
x = d.M
w = Inches(2.3)
for i, (name, when, body) in enumerate(phases):
    fill = b.TEAL if i == 1 else b.NAVY
    d.rect(s, x, Inches(2.2), w, Inches(0.55), fill, radius=0.1)
    d.text(s, f"{name} · {when}", x, Inches(2.3), w, Inches(0.35), size=11.5, bold=True,
           color=b.WHITE, align=PP_ALIGN.CENTER)
    d.rect(s, x, Inches(2.95), w, Inches(2.6), b.SOFT, radius=0.06)
    d.text(s, body, x + Inches(0.15), Inches(3.15), w - Inches(0.3), Inches(2.2),
           size=11.5, color=b.INK, shrink=True)
    x += w + Inches(0.16)
d.text(s, "Decision gates at each phase boundary — autonomy expands only on evidence",
       d.M, Inches(5.95), d.CW, Inches(0.35), size=12.5, color=b.DARK_TEAL, bold=True)
d.footer(s, 9, TOTAL)
notes(s, "Five phases over twelve months, each ending in a decision gate. Assess: two "
         "weeks to baseline current metrics and select pilot workstreams. Pilot: the "
         "twelve-week gated program just described. Platform: choose cloud versus "
         "self-hosted Enterprise deployment using the pilot's data-residency and cost "
         "evidence. Scale: roll the context infrastructure across teams and train "
         "engineers in specification discipline — this is where the operating-model "
         "change lands. Compound: by month twelve, specifications, skills, and context "
         "are versioned assets reused across teams — rung five behavior. Autonomy "
         "expands at each gate only on evidence, which keeps risk owned and visible.")

# ── 10 · Governance & risk ───────────────────────────────────────────────────
s = d.slide(b.WHITE)
d.header(s, "Governance the CISO can sign: keys, not prompts", "Risk management")
rows = [
    ("Ungoverned writes", "Least-privilege keys; confirmation policies; sandbox isolation"),
    ("Cost runaway", "Budget caps per unattended run; weekly spend alerting"),
    ("Context rot", "Curation SLAs; stale facts pruned on sight"),
    ("Vendor lock-in", "MIT core; folders-and-files context portable by design"),
    ("Model regressions", "Pinned versions for unattended jobs; eval gates"),
]
y = Inches(1.85)
for risk, mit in rows:
    d.rect(s, d.M, y, Inches(3.4), Inches(0.78), b.CORAL, radius=0.08)
    d.text(s, risk, d.M + Inches(0.2), y + Inches(0.12), Inches(3.0), Inches(0.54),
           size=13, bold=True, color=b.WHITE, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    d.rect(s, d.M + Inches(3.6), y, Inches(8.5), Inches(0.78), b.SOFT, radius=0.08)
    d.text(s, mit, d.M + Inches(3.8), y + Inches(0.12), Inches(8.1), Inches(0.54),
           size=12.5, color=b.INK, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
    y += Inches(0.95)
d.footer(s, 10, TOTAL)
notes(s, "Five risks, each with a structural mitigation rather than a policy memo. "
         "Ungoverned writes: agents physically cannot act beyond least-privilege keys, "
         "action-confirmation policies, and sandbox isolation — a prompt is never a "
         "permission layer. Cost runaway: every unattended run carries a budget cap and "
         "spend is alerted weekly. Context rot: curated knowledge carries freshness "
         "service levels and stale facts are pruned on sight, because agents trust stale "
         "context more than missing context. Vendor lock-in: the MIT-licensed core and "
         "plain-file context keep every layer swappable. Model regressions: unattended "
         "jobs pin model versions and pass evaluation gates before upgrades.")

# ── 11 · Decision ────────────────────────────────────────────────────────────
s = d.slide(b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
d.text(s, "Decision requested", d.M, Inches(1.4), d.CW, Inches(0.7), size=34, bold=True, color=b.WHITE)
items = [
    "Approve the 90-day gated pilot (2–3 scoped workstreams)",
    "Fund the context-infrastructure workstream",
    "Defer platform deployment choice to pilot evidence",
]
y = Inches(2.7)
for i, t in enumerate(items, 1):
    d.rect(s, d.M, y, Inches(0.5), Inches(0.5), b.TEAL, radius=0.5)
    d.text(s, str(i), d.M, y + Inches(0.07), Inches(0.5), Inches(0.36), size=16, bold=True,
           color=b.NAVY, align=PP_ALIGN.CENTER)
    d.text(s, t, d.M + Inches(0.75), y + Inches(0.05), Inches(10.5), Inches(0.45),
           size=17, color=b.WHITE, anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(0.85)
d.text(s, "Next step: pilot kickoff within two weeks of approval",
       d.M, Inches(5.6), d.CW, Inches(0.4), size=14, color=b.TEAL, bold=True)
d.footer(s, 11, TOTAL, dark=True)
notes(s, "Three approvals requested today. First, the 90-day gated pilot on two to three "
         "scoped workstreams with the gating and measurement just described. Second, "
         "funding for the context-infrastructure workstream — the repository-based brain "
         "of specifications, skills, and memory that both agents and engineers will run "
         "on; this is the asset that compounds regardless of which models win. Third, "
         "explicit deferral of the platform deployment decision — cloud versus "
         "self-hosted Kubernetes — until the pilot produces data-residency and cost "
         "evidence, so that choice is made on facts. On approval, pilot kickoff is within "
         "two weeks: baseline first, agents second.")

d.save(OUT, validate=True)
