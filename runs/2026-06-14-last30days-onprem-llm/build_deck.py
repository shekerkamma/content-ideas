#!/usr/bin/env python3
"""On-Premise LLM for Compliance · Last 30 Days Signal Deck · June 2026
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
OUT = RUN_DIR / "onprem-llm-compliance-reviewed.pptx"

d = Deck(footer="On-Premise LLM for Compliance  ·  Last 30 Days Signal  ·  June 2026")
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
    "AMBER":  RGBColor.from_string("F2A83B"),
}

M   = Inches(0.6)
W   = Inches(13.333)
H   = Inches(7.5)
CW  = W - M * 2
GAP = Inches(0.2)

def cw2(): return (CW - GAP) / 2
def cx2(i): return M + i * (cw2() + GAP)

def cw3(): return (CW - GAP * 2) / 3
def cx3(i): return M + i * (cw3() + GAP)

def cw4(): return (CW - GAP * 3) / 4
def cx4(i): return M + i * (cw4() + GAP)


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
           size=38, color=vc, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, label, left, top + Inches(0.78), w, Inches(0.32),
           size=13, color=C["MUTED"], align=PP_ALIGN.CENTER, shrink=True)


def section_title(s, title, sub=None, *, dark=False):
    tc = C["WHITE"] if dark else C["NAVY"]
    d.text(s, title, M, Inches(0.28), CW, Inches(0.62),
           size=30, color=tc, bold=True, shrink=True)
    d.rect(s, M, Inches(0.96), Inches(1.6), Inches(0.05), C["TEAL"])
    if sub:
        d.text(s, sub, M, Inches(1.1), CW, Inches(0.4),
               size=14, color=C["MUTED"], shrink=True)


def insight_box(s, text, top, h, *, size=17):
    d.rect(s, M, top, CW, h, C["NAVY"], line=C["NAVY"], radius=0.06)
    d.text(s, text,
           M + Inches(0.35), top + Inches(0.25), CW - Inches(0.7), h - Inches(0.5),
           size=size, color=C["WHITE"], shrink=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Cover
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["NAVY"])
d.rect(s, 0, 0, W, Inches(0.14), C["TEAL"])

d.text(s, "ON-PREMISE LLM\nFOR COMPLIANCE",
       M, Inches(1.2), CW, Inches(1.4),
       size=52, color=C["WHITE"], bold=True, align=PP_ALIGN.CENTER, shrink=True)
d.text(s, "30-Day Community Signal  ·  Reddit · HN · GitHub  ·  June 2026",
       M, Inches(2.75), CW, Inches(0.45),
       size=18, color=C["MUTED"], align=PP_ALIGN.CENTER, shrink=True)

d.rect(s, M + CW/2 - Inches(1.0), Inches(3.3), Inches(2.0), Inches(0.05), C["TEAL"])

bw = Inches(3.4)
for i, (v, l) in enumerate([("40", "signals"), ("9,768", "Reddit upvotes"), ("2,247", "Reddit comments")]):
    bx = M + i * (bw + Inches(0.27))
    d.rect(s, bx, Inches(3.6), bw, Inches(1.3), C["NAVY2"], line=C["BORDER"], radius=0.06)
    d.text(s, v, bx, Inches(3.7), bw, Inches(0.65),
           size=44, color=C["TEAL"], bold=True, align=PP_ALIGN.CENTER, shrink=True)
    d.text(s, l, bx, Inches(4.4), bw, Inches(0.38),
           size=15, color=C["MUTED"], align=PP_ALIGN.CENTER, shrink=True)

d.text(s, "Top communities: r/LocalLLaMA  ·  r/MachineLearning  ·  r/sysadmin  ·  HN",
       M, Inches(5.35), CW, Inches(0.38),
       size=13, color=C["MUTED"], align=PP_ALIGN.CENTER)
d.footer(s, 1, TOTAL, dark=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — The Signal
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["SOFT"])
section_title(s, "What the Data Says",
              "A government action changed the on-prem narrative more than any product launch")

bw = (CW - GAP * 2) / 3
by = Inches(1.65)
bh = Inches(1.2)
for i, (v, l, vc) in enumerate([
    ("1,471 pts", "#1: Fable 5 disabled by US Gov  →  'why we need local models'", C["RED"]),
    ("3,000 t/s", "real-time inference on standard GPUs  ·  on-prem now viable",   C["TEAL"]),
    ("334 pts",   "r/sysadmin: 'shadow vibe coder in my department'",              C["AMBER"]),
]):
    stat_pill(s, M + i * (bw + GAP), by, bw, bh, v, l, vc=vc)

insight_box(s,
    "The community's framing: 'can be switched off by a third party' is now LIVED EXPERIENCE, not theory.\n"
    "Sovereignty and model independence — not GDPR compliance — is the primary emotional driver.",
    Inches(3.05), Inches(1.5), size=19)

d.text(s, "Compliance and regulation are the business justification. Model sovereignty is the emotion that closes the deal.",
       M, Inches(4.75), CW, Inches(0.45),
       size=15, color=C["MUTED"], shrink=True)
d.footer(s, 2, TOTAL)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — The Sovereignty Moment
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["NAVY"])
section_title(s, "Five Posts. One Thesis. The Sovereignty Moment.", dark=True)

cw_ = cw2()
cy = Inches(1.55)
ch = Inches(2.5)

card(s, cx2(0), cy, cw_, ch,
     "Fable 5 Disabled by US Gov  ·  1,471 pts / 489 cmt",
     "Title: 'Anthropic forced to abruptly disable Fable 5 & Mythos 5 globally by US Gov over a jailbreak. "
     "This is exactly why we need local models.'\n\n"
     "Top comment: 'Your ability to use AI tools depends entirely on Anthropic's ability and willingness to keep them running. "
     "A local model cannot be remotely disabled.'",
     hfill=C["RED"], size=14)
card(s, cx2(1), cy, cw_, ch,
     "Friendly Reminder  ·  1,578 pts / 240 cmt",
     "Companion post: a reminder that Llama, Qwen, and Mistral exist and can be downloaded NOW as insurance against future cloud shutdowns.\n\n"
     "Posted within hours of the Fable 5 ban. Community reaction: equal parts humor and genuine contingency planning.",
     hfill=C["TEAL"], size=14)

cy2 = Inches(4.22)
ch2 = Inches(2.1)
card(s, cx2(0), cy2, cw_, ch2,
     "Download Local Model After Ban  ·  1,420 pts / 131 cmt",
     "'when fable gets banned but it's ok because you've about to download qwen3.7_67b'\n\n"
     "The community treated this as both a meme and a genuine contingency playbook.",
     size=14)
card(s, cx2(1), cy2, cw_, ch2,
     "Torrent Network for Open-Source Models  ·  886 pts / 142 cmt",
     "'We should set up a torrent network for open source models' — distribution infrastructure that cannot be taken down.\n\n"
     "This is serious engineering discussion, not protest.",
     size=14)
d.footer(s, 3, TOTAL, dark=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — The Compliance Stack
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["SOFT"])
section_title(s, "The Compliance Stack Is Crystallizing",
              "Open-source tooling has converged on a repeatable VPC-isolated deployment pattern")

cw_ = cw4()
cy = Inches(1.65)
ch = Inches(2.7)

card(s, cx4(0), cy, cw_, ch,
     "ToTra",
     "GDPR + EU AI Act gateway.\n\n"
     "Handles data residency routing, consent audit logging, and high-risk AI decision audit trail (EU AI Act Art. 13).\n\n"
     "Open-source. Appeared on HN this period.",
     hfill=C["TEAL"], size=14)
card(s, cx4(1), cy, cw_, ch,
     "LiteLLM v1.89.0",
     "Routing + observability layer.\n\n"
     "Actively deployed in private Kubernetes clusters. Single API, 100+ model providers, OpenAI-compatible endpoint.\n\n"
     "Works with self-hosted models.",
     hfill=C["NAVY2"], size=14)
card(s, cx4(2), cy, cw_, ch,
     "Ollama / vLLM",
     "Local inference.\n\n"
     "Ollama: single-machine (dev laptops → small VMs).\n\n"
     "vLLM: high-throughput GPU clusters.\n\n"
     "Both serve OpenAI-compatible APIs — drop-in behind LiteLLM.",
     hfill=C["NAVY2"], size=14)
card(s, cx4(3), cy, cw_, ch,
     "Open Models",
     "Llama 3.x — Apache 2.0, enterprise-safe.\n\n"
     "Qwen 3.7 — community favourite, strong quantized perf.\n\n"
     "Mistral — EU-based, strong GDPR story.\n\n"
     "All available as GGUF — runnable on standard GPU hardware.",
     hfill=C["MUTED"], size=14)

insight_box(s,
    "One architecture covers HIPAA, GDPR, SOC2, and EU AI Act:\n"
    "VPC-isolated deployment  +  signed BAA  +  ToTra/LiteLLM gateway  +  GGUF model on GPU nodes",
    Inches(4.55), Inches(1.55), size=17)
d.footer(s, 4, TOTAL)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Inference Economics
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["NAVY"])
section_title(s, "Inference Economics: The On-Prem Cost Argument Is Winnable",
              "HN: 'Real-time LLM Inference on Standard GPUs: 3k tokens/s per request'  ·  219 pts / 97 cmt",
              dark=True)

cw_ = cw3()
cy = Inches(1.55)
ch = Inches(2.7)

card(s, cx3(0), cy, cw_, ch,
     "The Hardware Signal",
     "3,000 tokens per second per request on standard GPU.\n\n"
     "At 3k t/s, a single A100 can serve ~90 concurrent 2k-token requests/minute.\n\n"
     "GPU cloud spot pricing at this throughput is comparable to — or cheaper than — Anthropic/OpenAI API for high-volume workloads.",
     hfill=C["TEAL"], size=14)
card(s, cx3(1), cy, cw_, ch,
     "The Compliance Tax on Cloud APIs",
     "Cloud API TCO includes:\n"
     "• BAA negotiation + annual renewal\n"
     "• EU → US data egress costs\n"
     "• Vendor risk review for every cloud tool\n"
     "• Shadow AI incident response overhead\n\n"
     "Add these and on-prem TCO improves significantly.",
     hfill=C["NAVY2"], size=14)
card(s, cx3(2), cy, cw_, ch,
     "M3 MacBook Air Benchmarks",
     "Separate HN thread: viable LLM inference on M3 MacBook Air for 7B–13B models.\n\n"
     "The barrier for on-prem proof-of-concept has dropped to a $1,500 MacBook.\n\n"
     "You no longer need a $50,000 GPU server to prove the business case.",
     hfill=C["NAVY2"], size=14)

cy2 = Inches(4.42)
ch2 = Inches(2.0)
card(s, cx3(0), cy2, cw_, ch2,
     "LLM Disagreement on Facts  ·  HN 505 pts",
     "Frontier LLMs disagree on real-world fact-checks.\n\n"
     "For HIPAA clinical decisions and SOC2 audit evidence, model pinning + hallucination testing are compliance requirements. On-prem enables both; cloud APIs do not.",
     size=14)
card(s, cx3(1), cy2, cw_, ch2,
     "PoC Cost Estimate",
     "1× A100 GPU instance (~$3/hr spot)\n"
     "× 720 hours (30 days)\n"
     "= ~$2,160 total PoC cost\n\n"
     "Fully reproduces production compliance architecture at near-zero risk.",
     hfill=C["TEAL"], size=14)
card(s, cx3(2), cy2, cw_, ch2,
     "The Incumbent Risk",
     "Azure OpenAI + AWS Bedrock offer 'private deployment' — but data stays in THEIR VPC.\n\n"
     "For HIPAA and EU AI Act high-risk categories, 'cloud-provider VPC' may still fail depending on BAA language.\n\n"
     "True on-prem = customer-controlled hardware.",
     size=14)
d.footer(s, 5, TOTAL, dark=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Shadow AI Driver
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["SOFT"])
section_title(s, "Shadow AI: The Internal Driver That Gets Budgets Approved",
              "r/sysadmin — not r/LocalLLaMA — is where enterprise on-prem conversations start")

cw_ = cw2()
cy = Inches(1.65)
ch = Inches(2.4)

card(s, cx2(0), cy, cw_, ch,
     "Shadow Vibe Coder  ·  r/sysadmin  ·  334 pts / 120 cmt",
     "A sysadmin found a developer pasting proprietary code and PII into consumer ChatGPT.\n\n"
     "The thread became a community playbook: how to detect shadow AI, how to enforce policy, and whether to block or channel the behaviour.\n\n"
     "This is the incident that makes the CISO pick up the phone.",
     size=14)
card(s, cx2(1), cy, cw_, ch,
     "Detecting AI Threats via Compliance API  ·  r/netsec",
     "Detecting AI-specific threats in Claude Enterprise via the Compliance API.\n\n"
     "The defensive response: instrument the authorised AI tool to detect anomalous usage.\n\n"
     "Implication: enterprises need both an approved tool AND audit/detection tooling to make that approval meaningful.",
     hfill=C["TEAL"], size=14)

insight_box(s,
    "The pitch that gets on-prem LLM approved internally:\n\n"
    "\"Your developers are already using AI tools. The question is whether those tools have "
    "audit logging, data residency controls, and a BAA — or whether you find out about the "
    "breach the same way this sysadmin did.\"\n\n"
    "Target buyer: CISO and IT security. NOT the compliance team. Compliance ratifies — CISO feels the pain.",
    Inches(4.25), Inches(2.35), size=15)
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
    ("Sovereignty anxiety is the #1 emotional driver",
     "The Fable 5 ban is the most-discussed event in the dataset. "
     "'Can be switched off by a third party' is now lived experience. Lead every pitch with model independence before mentioning compliance.",
     C["RED"]),
    ("The compliance stack is open-source and assembly-complete",
     "ToTra + LiteLLM + Ollama/vLLM + Llama/Qwen/Mistral = a complete deployable stack with no proprietary components. "
     "The integration work is the value-add.",
     C["TEAL"]),
    ("Shadow AI is the internal trigger — not regulation",
     "r/sysadmin and r/netsec are where buying decisions originate. "
     "Frame the pitch around eliminating shadow AI risk — not GDPR checkbox.",
     C["NAVY2"]),
    ("Inference economics are no longer the blocker",
     "3k tokens/s on standard GPUs + M3 MacBook benchmarks = the 'cloud is cheaper' argument is dead for high-volume workloads when you add compliance overhead.",
     C["NAVY2"]),
]

for i, (title, body, hf) in enumerate(patterns):
    row, col = divmod(i, 2)
    card(s, cx2(col), Inches(1.58) + row * (ph + gap), cw_, ph, title, body, hfill=hf, size=14)

card(s, M, Inches(1.58) + 2 * (ph + gap), CW, ph,
     "LLM disagreement on facts is a compliance-specific risk",
     "For HIPAA and SOC2 audit evidence, model pinning + hallucination testing are compliance requirements. "
     "On-prem enables both. Cloud APIs where the model updates silently do not.",
     hfill=C["TEAL"], size=14)
d.footer(s, 7, TOTAL, dark=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — 90-Day Playbook
# ══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=C["SOFT"])
section_title(s, "90-Day On-Premise LLM Entry Playbook",
              "Three phases: discovery → proof → compliance program")

cw_ = cw3()
cy = Inches(1.65)
ch = Inches(4.85)

card(s, cx3(0), cy, cw_, ch,
     "Days 1–30: Shadow AI Audit",
     "Objective: establish the business case before touching infrastructure.\n\n"
     "• Identify which AI tools employees are using (authorized vs. shadow)\n"
     "• Catalog what data is sent to cloud AI APIs\n"
     "• Quantify compliance exposure (HIPAA, GDPR, SOC2)\n"
     "• Get one CISO or IT security stakeholder to co-own the problem\n\n"
     "Deliverable: a one-page shadow AI risk brief that makes the on-prem case without mentioning model capability.\n\n"
     "Tools: DLP logs, browser extension audit, HR policy review.",
     hfill=C["TEAL"], size=14)
card(s, cx3(1), cy, cw_, ch,
     "Days 31–60: On-Prem Proof of Concept",
     "Objective: prove the open-source stack performs at par with cloud APIs.\n\n"
     "Stack:\n"
     "• Ollama (single GPU node)\n"
     "• LiteLLM (routing + OpenAI-compat API)\n"
     "• Llama 3.1 70B or Qwen 3.7 67B\n\n"
     "• Deploy in isolated dev VPC (not production)\n"
     "• Mirror the highest-volume use case from the Shadow AI audit\n"
     "• Measure: latency, throughput, quality vs. GPT-4o\n\n"
     "Cost: ~$2,160 total on A100 spot pricing.",
     hfill=C["NAVY2"], size=14)
card(s, cx3(2), cy, cw_, ch,
     "Days 61–90: Compliance Program",
     "Objective: convert the PoC into a sanctioned program with audit trail.\n\n"
     "• Draft AI usage policy referencing the on-prem stack as the approved tool\n"
     "• Wire LiteLLM audit logs into your SIEM\n"
     "• Sign BAA with your GPU cloud provider\n"
     "• Run table-top exercise: simulate a model shutdown — verify local fallback works\n\n"
     "Optional: add model download automation to internal artifact registry — eliminates single point of failure on HuggingFace.\n\n"
     "Success metric: zero shadow AI incidents in month 4.",
     size=14)
d.footer(s, 8, TOTAL)


d.save(OUT)
print(f"\n✓ Deck 2 saved → {OUT}")
