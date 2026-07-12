#!/usr/bin/env python3
"""Agent-Native AI Architecture · Last 30 Days Signal Deck · June 2026
REDESIGN: fewer cards, 14pt body minimum, less text per card.
"""

from __future__ import annotations
import sys
from pathlib import Path

PPTXKIT_DIR = Path("/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
if not PPTXKIT_DIR.exists():
    PPTXKIT_DIR = Path("/home/shekerk/snap/codex/64/.claude/skills/branded-pptx-deck/scripts")
sys.path.insert(0, str(PPTXKIT_DIR))

from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from pptxkit import Deck

RUN_DIR = Path(__file__).resolve().parent
OUT = RUN_DIR / "agent-native-ai-architecture-reviewed.pptx"

d = Deck(footer="Agent-Native AI Architecture  ·  Last 30 Days Signal  ·  June 2026")
b = d.b
TOTAL = 8

C = {
    "WHITE":  RGBColor.from_string("FFFFFF"),
    "NAVY":   RGBColor.from_string("1F3B6E"),
    "NAVY2":  RGBColor.from_string("0D3B5E"),
    "RED":    RGBColor.from_string("E31837"),
    "TEAL":   RGBColor.from_string("00C9A7"),
    "SOFT":   RGBColor.from_string("F5F7FA"),
    "BORDER": RGBColor.from_string("D0D5DD"),
    "INK":    RGBColor.from_string("1B2B3C"),
    "MUTED":  RGBColor.from_string("5B6B7C"),
    "GOLD":   RGBColor.from_string("FFB800"),
}

M  = Inches(0.6)
W  = Inches(13.333)
H  = Inches(7.5)
CW = W - M * 2   # 12.133"
GAP = Inches(0.2)

def cw2(): return (CW - GAP) / 2       # two-col: ~5.97"
def cx2(i): return M + i * (cw2() + GAP)

def cw3(): return (CW - GAP * 2) / 3   # three-col: ~3.91"
def cx3(i): return M + i * (cw3() + GAP)


# ── Helpers ──────────────────────────────────────────────────────────────────

def card(s, left, top, w, h, header, body, *, hfill=None, size=14):
    hf = hfill or C["NAVY2"]
    d.rect(s, left, top, w, h, C["WHITE"], line=C["BORDER"], radius=0.04)
    d.rect(s, left, top, w, Inches(0.42), hf, line=hf, radius=0.04)
    d.text(s, header,
           left + Inches(0.14), top + Inches(0.07), w - Inches(0.28), Inches(0.3),
           size=13, color=C["WHITE"], bold=True, shrink=True)
    d.text(s, body,
           left + Inches(0.14), top + Inches(0.52), w - Inches(0.28), h - Inches(0.62),
           size=size, color=C["INK"], shrink=True)


def stat_pill(s, left, top, w, h, value, label, *, vc=None):
    vc = vc or C["TEAL"]
    d.rect(s, left, top, w, h, C["WHITE"], line=C["BORDER"], radius=0.08)
    d.text(s, value, left, top + Inches(0.1), w, Inches(0.65),
           size=42, color=vc, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, label, left, top + Inches(0.78), w, Inches(0.32),
           size=13, color=C["MUTED"], align=PP_ALIGN.CENTER, shrink=True)


def section_title(s, title, sub=None, *, dark=False):
    tc = C["WHITE"] if dark else C["NAVY"]
    d.text(s, title, M, Inches(0.28), CW, Inches(0.62),
           size=30, color=tc, bold=True, shrink=True)
    d.rect(s, M, Inches(0.96), Inches(1.6), Inches(0.05), C["TEAL"])
    if sub:
        sc = C["MUTED"] if dark else C["MUTED"]
        d.text(s, sub, M, Inches(1.1), CW, Inches(0.4),
               size=14, color=sc, shrink=True)


def insight_box(s, text, top, h, *, body_size=17):
    d.rect(s, M, top, CW, h, C["NAVY"], line=C["NAVY"], radius=0.06)
    d.text(s, text, M + Inches(0.35), top + Inches(0.25),
           CW - Inches(0.7), h - Inches(0.5),
           size=body_size, color=C["WHITE"], shrink=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Cover
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["NAVY"])
d.rect(s, 0, 0, W, Inches(0.14), C["TEAL"])

d.text(s, "AGENT-NATIVE AI ARCHITECTURE",
       M, Inches(1.4), CW, Inches(1.0),
       size=52, color=C["WHITE"], bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.text(s, "30-Day Community Signal  ·  Reddit · HN · GitHub  ·  June 2026",
       M, Inches(2.55), CW, Inches(0.45),
       size=18, color=C["MUTED"], align=PP_ALIGN.CENTER, shrink=True)

d.rect(s, M + CW/2 - Inches(1.0), Inches(3.15), Inches(2.0), Inches(0.05), C["TEAL"])

bw = Inches(3.4)
for i, (v, l) in enumerate([("54", "signals"), ("12,977", "upvotes + points"), ("3,102", "comments")]):
    bx = M + i * (bw + Inches(0.27))
    d.rect(s, bx, Inches(3.45), bw, Inches(1.3), C["NAVY2"], line=C["BORDER"], radius=0.06)
    d.text(s, v, bx, Inches(3.55), bw, Inches(0.65),
           size=44, color=C["TEAL"], bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, l, bx, Inches(4.25), bw, Inches(0.38),
           size=15, color=C["MUTED"], align=PP_ALIGN.CENTER, shrink=True)

d.text(s, "r/AI_Agents  ·  r/ClaudeAI  ·  r/LangChain  ·  HN  ·  github.com/openai/codex",
       M, Inches(5.2), CW, Inches(0.38),
       size=13, color=C["MUTED"], align=PP_ALIGN.CENTER)
d.footer(s, 1, TOTAL, dark=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — What the data says
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["SOFT"])
section_title(s, "What the Data Says",
              "54 signals · safety and governance outranked capability in every top-karma thread")

bw = (CW - GAP * 2) / 3
by = Inches(1.65)
bh = Inches(1.2)
for i, (v, l, vc) in enumerate([
    ("1,448 pts", "HN #1: AI agent bankrupted its operator", C["RED"]),
    ("549 pts",   "HN #2: AI agent runs amok in Fedora",    C["NAVY"]),
    ("6,018 pts", "Reddit #1: Claude Fable 5 inequality",   C["TEAL"]),
]):
    stat_pill(s, M + i * (bw + GAP), by, bw, bh, v, l, vc=vc)

insight_box(s,
    "The highest-karma threads this month are NOT about what agents can do.\n"
    "They are about what agents do without asking — and who pays the price.",
    Inches(3.05), Inches(1.4), body_size=20)

d.text(s, "Permission fatigue · Runaway costs · Governance gaps — these are the practitioner topics right now.",
       M, Inches(4.65), CW, Inches(0.45),
       size=15, color=C["MUTED"], shrink=True)
d.footer(s, 2, TOTAL)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Safety is #1
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["SOFT"])
section_title(s, "Safety is the #1 Practitioner Conversation",
              "Top HN stories by karma — not product launches, not benchmarks")

cw_ = cw2()
cy = Inches(1.65)
ch = Inches(2.45)

card(s, cx2(0), cy, cw_, ch,
     "AI Agent Bankrupted Operator  ·  HN 1,448 pts / 528 cmt",
     "An agent autonomously scanning the DN42 network ran up a bill that bankrupted its operator.\n\n"
     "Top comment: 'The agent needs to STOP and ask before doing anything irreversible or expensive.'\n\n"
     "The community's verdict: cost ceilings and reversibility are not nice-to-haves. They are safety primitives.",
     hfill=C["RED"], size=14)
card(s, cx2(1), cy, cw_, ch,
     "AI Agent Runs Amok  ·  HN 549 pts / 244 cmt",
     "AI agents making system-level changes in Fedora without guardrails.\n\n"
     "Community consensus: approval dialogs are security theater — users click through everything.\n\n"
     "What practitioners want: atomic, reversible actions with automatic rollback.",
     hfill=C["NAVY2"], size=14)

cy2 = Inches(4.28)
ch2 = Inches(2.0)
card(s, cx2(0), cy2, cw_, ch2,
     "Continue? Y/N — Permission Fatigue  ·  HN 386 pts / 162 cmt",
     "A 60-second game simulating agent approval dialogs went viral.\n\n"
     "The joke landed because it is true: permission UX is a design discipline the ecosystem has ignored.",
     size=14)
card(s, cx2(1), cy2, cw_, ch2,
     "Stanford CS336 Agent Guidelines  ·  HN 503 pts / 153 cmt",
     "Stanford published CLAUDE.md for its LLM foundations course.\n\n"
     "Signal: agent governance is now in academic curriculum — enterprise policy teams can cite it.",
     size=14)
d.footer(s, 3, TOTAL)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Platform Race
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["NAVY"])
section_title(s, "Three Platform Bets on Agent-Native Infrastructure", dark=True)

cw_ = cw3()
cy = Inches(1.55)
ch = Inches(5.0)

card(s, cx3(0), cy, cw_, ch,
     "OpenAI Codex — Agents in the IDE",
     "GitHub issue: 'Codex App unusable slow with WSL as agent environment.'\n\n"
     "• Opening a chat: 134 seconds\n"
     "• Simple UI request: 1hr 30min\n\n"
     "The bet: IDE is the right agent host.\n"
     "The risk: Windows/WSL performance makes the agent feel broken for half the user base.",
     hfill=C["TEAL"], size=14)
card(s, cx3(1), cy, cw_, ch,
     "Microsoft Solara + Scout — Windows as Agent Platform",
     "Build 2026: Windows becomes the agent execution environment.\n\n"
     "• Solara: shared context across apps via MCP\n"
     "• Scout: on-device agent that persists across sessions\n"
     "• Backed by Nvidia hardware partnership\n\n"
     "If this wins, MCP becomes the default integration layer for every enterprise app on Windows.",
     hfill=C["NAVY2"], size=14)
card(s, cx3(2), cy, cw_, ch,
     "OpenHands — Open-Source Agent Framework",
     "Community-maintained multi-agent framework gaining GitHub traction.\n\n"
     "• Sandboxed execution\n"
     "• MCP server wiring\n"
     "• Skill/microagent composition\n"
     "• Headless/CLI mode for CI\n\n"
     "The bet: open-source wins on customization. Teams prefer to own the agent loop.",
     hfill=C["NAVY2"], size=14)
d.footer(s, 4, TOTAL, dark=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Memory Architecture Debate
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["SOFT"])
section_title(s, "Memory Externalization: Where the Architecture Debate Lives",
              "No dominant pattern has emerged — three camps are active")

cw_ = cw3()
cy = Inches(1.65)
ch = Inches(2.6)

card(s, cx3(0), cy, cw_, ch,
     "In-Model Memory",
     "Model state is enough for single-session tasks.\n\n"
     "External memory adds latency and complexity.\n\n"
     "Start fresh each session from a well-designed context file.\n\n"
     "Best for: small teams, notebook workflows.",
     hfill=C["MUTED"], size=14)
card(s, cx3(1), cy, cw_, ch,
     "External Memory-as-a-Service",
     "Persistent vector DB + graph store outside the model.\n\n"
     "Enables: cross-session continuity, multi-agent shared state, personalization.\n\n"
     "Examples: GBrain, Mem0, Zep, LangMem.\n\n"
     "Best for: enterprise multi-session, named-account context.",
     hfill=C["TEAL"], size=14)
card(s, cx3(2), cy, cw_, ch,
     "Shared Context Files",
     "Markdown files (CLAUDE.md, context.md) as the memory layer.\n\n"
     "The agent reads and writes human-readable files.\n\n"
     "No new infrastructure. Memory is also the audit trail.\n\n"
     "Best for: Cursor users, Claude Code workflows.",
     hfill=C["NAVY2"], size=14)

insight_box(s,
    "Apache Burr — the first production-grade tool designed specifically for external agent state — "
    "appeared in HN discussions this month. Adoption is early. Expect consolidation in the next 6 months.",
    Inches(4.45), Inches(1.35), body_size=16)
d.footer(s, 5, TOTAL)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Vocabulary Spreading
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["SOFT"])
section_title(s, "Agent-Native Vocabulary Is Entering Infrastructure and Academia",
              "The language is shifting — from 'AI features' to 'agent-native apps'")

cw_ = cw2()
cy = Inches(1.65)
ch = Inches(2.4)

card(s, cx2(0), cy, cw_, ch,
     "Fable 5 Inequality  ·  r/ClaudeAI  ·  6,018 pts / 993 cmt",
     "Top Reddit post this period: 'Claude Fable 5 feels less like a model launch and more like a preview of AI inequality.'\n\n"
     "Signal: access tier design for agent-native apps is already a first-class policy concern.\n\n"
     "Who gets which agent capabilities at which price points is generating community backlash.",
     size=14)
card(s, cx2(1), cy, cw_, ch,
     "Stanford CS336 — Agents in the Curriculum",
     "CS336 (Karpathy-adjacent LLM foundations course) published formal agent guidelines in CLAUDE.md format.\n\n"
     "HN treated this as a landmark: governance is now in formal CS education.\n\n"
     "Enterprise AI policy teams can cite Stanford CS336 when writing internal agent usage policies.",
     hfill=C["TEAL"], size=14)

cy2 = Inches(4.22)
ch2 = Inches(2.1)
card(s, cx2(0), cy2, cw_, ch2,
     "CoreCLR + Codex: Agent as Architecture Contributor",
     "Codex ported CoreCLR to PowerPC64LE in two weeks — the agent was the architecture contributor.\n\n"
     "Signal: agent-native workflows are appearing in core systems programming, not just web apps.",
     size=14)
card(s, cx2(1), cy2, cw_, ch2,
     "Vocabulary in the Wild (r/AI_Agents, r/LangChain, r/ClaudeAI)",
     "Terms now used without explanation: 'agent-native', 'MCP server', 'shared context', 'tool access parity'.\n\n"
     "Previously Anthropic/OpenAI internal vocabulary — now in practitioner Reddit and HN daily.",
     size=14)
d.footer(s, 6, TOTAL)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — Key Patterns
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["NAVY"])
section_title(s, "5 Key Patterns from the Last 30 Days", dark=True)

cw_ = cw2()
ph = Inches(1.52)
gap = Inches(0.16)

patterns = [
    ("Safety / governance outranks capability",
     "The two highest-karma HN threads are both agent-gone-wrong stories. "
     "Build reversibility, cost ceilings, and human-in-the-loop checkpoints — not more capability.",
     C["RED"]),
    ("Permission fatigue is a UX design problem",
     "Approval dialogs don't work — users click through everything. "
     "The open problem: atomic + reversible actions with automatic rollback. No accepted solution yet.",
     C["TEAL"]),
    ("The OS is the next agent battleground",
     "Microsoft's Solara + Scout bet: Windows becomes the agent host. "
     "If they win, MCP becomes the default integration layer for every enterprise app.",
     C["NAVY2"]),
    ("Memory externalization is still unsettled",
     "Three camps (in-model / external / shared files) are all active. "
     "Apache Burr is the first production tool but hasn't crossed the adoption threshold.",
     C["NAVY2"]),
]

for i, (title, body, hf) in enumerate(patterns):
    row, col = divmod(i, 2)
    card(s, cx2(col), Inches(1.58) + row * (ph + gap), cw_, ph, title, body, hfill=hf, size=14)

# Fifth pattern spans full width
full_w = CW
card(s, M, Inches(1.58) + 2 * (ph + gap), full_w, ph,
     "Agent-native vocabulary is now academic — enterprise policy can cite Stanford CS336",
     "CS336 guidelines + the Codex/CoreCLR experiment signal that 'agent-native' is entering formal CS education. "
     "This is the moment it stops being startup jargon and becomes enterprise-citeable precedent.",
     hfill=C["TEAL"], size=14)

d.footer(s, 7, TOTAL, dark=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — What to Watch
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["SOFT"])
section_title(s, "What to Watch in the Next 90 Days",
              "Three strategic bets based on the community signal")

cw_ = cw3()
cy = Inches(1.65)
ch = Inches(4.8)

card(s, cx3(0), cy, cw_, ch,
     "Watch: Permission UX Standards",
     "No accepted solution exists for agent approval UX.\n\n"
     "Whoever ships the first widely-adopted pattern — reversible actions, cost ceilings, semantic approvals — will set the standard.\n\n"
     "Watch for:\n"
     "• Anthropic MCP spec updates\n"
     "• Microsoft Solara permission model\n"
     "• Any Show HN with >1k stars on agent UX\n\n"
     "Signal to catch: an agent permission library crossing 1k GitHub stars.",
     hfill=C["NAVY2"], size=14)
card(s, cx3(1), cy, cw_, ch,
     "Build: Memory + State Layer",
     "The externalized memory market is wide open.\n\n"
     "Teams need:\n"
     "• Cross-session memory that is human-auditable\n"
     "• Multi-agent shared state with access controls\n"
     "• PII-safe memory with automatic redaction\n"
     "• Rollback / undo for agent state\n\n"
     "Apache Burr is early. Vector DB vendors are all building agent APIs.\n\n"
     "The winner pairs memory with an opinionated agent loop.",
     hfill=C["TEAL"], size=14)
card(s, cx3(2), cy, cw_, ch,
     "Pitch: Enterprise Agent Governance",
     "Stanford CS336 + agent-ran-amok stories have primed buyers.\n\n"
     "The pitch that works:\n\n"
     "'Your developers are already using agent tools. The question is whether you have policy, audit trail, and rollback — or whether you find out the same way this operator did: in the invoice.'\n\n"
     "Target: IT security → CISO → CIO.\n"
     "Lead with governance, not productivity.",
     hfill=C["RED"], size=14)
d.footer(s, 8, TOTAL)


d.save(OUT)
print(f"\n✓ Deck 1 saved → {OUT}")
