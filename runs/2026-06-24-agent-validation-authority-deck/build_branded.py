#!/usr/bin/env python3
"""Branded builder for the Agent Validation & Assurance Authority positioning deck.
Uses pptxkit + the Canva-Pro palette (default Brand). Content is pre-validated."""
import sys
sys.path.insert(0, "/home/shekerk/.claude/skills/branded-pptx-deck/scripts")
from pptxkit import Deck, Inches, Pt, PP_ALIGN, MSO_ANCHOR

OUT = "/home/shekerk/content-ideas/runs/2026-06-24-agent-validation-authority-deck/agent-validation-authority-branded-draft.pptx"
d = Deck(footer="Agent Validation & Assurance Authority · Positioning Thesis v1 · 2026-06-24")
b = d.b
C = PP_ALIGN.CENTER
TOTAL = 28

def card(s, x, y, w, h, title, lines, accent=None, title_color=None):
    accent = accent or b.TEAL
    d.rect(s, x, y, w, h, b.WHITE, radius=0.06, shadow=True)
    d.rect(s, x, y, Inches(0.09), h, accent)
    d.text(s, title, x+Inches(0.26), y+Inches(0.16), w-Inches(0.45), Inches(0.55),
           size=15, color=title_color or b.NAVY, bold=True, shrink=True)
    if lines:
        d.text(s, [{"text": t, "size": 11.5, "space_before": 4} for t in lines],
               x+Inches(0.26), y+Inches(0.74), w-Inches(0.48), h-Inches(0.9),
               color=b.INK, shrink=True)

def stat(s, x, y, w, h, num, label):
    d.rect(s, x, y, w, h, b.NAVY, radius=0.06, shadow=True)
    d.text(s, num, x, y+Inches(0.26), w, Inches(0.72), size=29, color=b.GOLD, bold=True, align=C, shrink=True)
    d.text(s, label, x+Inches(0.12), y+Inches(1.02), w-Inches(0.24), h-Inches(1.1),
           size=11, color=b.WHITE, align=C, shrink=True)

def grid_x(n, gap=0.25, left=None, total_w=None):
    left = d.M if left is None else left
    total_w = d.CW if total_w is None else total_w
    g = Inches(gap)
    w = (total_w - g*(n-1)) / n
    return [(left + int((w+g)*i), w) for i in range(n)]

# 1 — COVER
s = d.slide(fill=b.NAVY)
d.rect(s, Inches(11.6), 0, Inches(1.73), d.H, b.NAVY_2)
d.rect(s, Inches(11.54), 0, Inches(0.06), d.H, b.TEAL)
d.text(s, "POSITIONING THESIS · v1 · 2026-06-24", d.M, Inches(1.5), Inches(9), Inches(0.4),
       size=14, color=b.TEAL, bold=True)
d.text(s, "The Agent Validation\n& Assurance Authority", d.M, Inches(2.1), Inches(10.4), Inches(1.7),
       size=46, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(3.95), Inches(1.6), Inches(0.06), b.TEAL)
d.text(s, "The UL / SOC-2 for autonomous AI agents", d.M, Inches(4.15), Inches(10), Inches(0.5),
       size=22, color=b.LIGHT_TEAL, bold=True, shrink=True)
d.text(s, "Independent validation that lets a regulated enterprise put an AI agent into production — and survive the exam.",
       d.M, Inches(4.95), Inches(10.2), Inches(0.6), size=14.5, color=b.LIGHT_TEAL, shrink=True)
for i, chip in enumerate(["Beachhead: U.S. super-regional banks", "Vertical 2: automotive captive finance", "Vertical 2b: OEM agent fleets"]):
    cw = Inches(3.35)
    d.rect(s, d.M + int((cw+Inches(0.2))*i), Inches(5.85), cw, Inches(0.5), b.NAVY_2, radius=0.3, line=b.TEAL)
    d.text(s, chip, d.M + int((cw+Inches(0.2))*i), Inches(5.96), cw, Inches(0.3), size=11.5, color=b.TEAL, align=C, shrink=True)

# 2 — EXECUTIVE SUMMARY (BLUF one-pager)
s = d.slide(fill=b.WHITE)
d.header(s, "Build the referee for the agent economy", "Executive summary")
d.rect(s, d.M, Inches(1.55), d.CW, Inches(0.7), b.NAVY, radius=0.05)
d.text(s, "BLUF: Agents are shipping into regulated production faster than anyone can trust them. SR 26-2 left agentic AI ungoverned. We sell the independent validation that fills the vacuum.",
       d.M+Inches(0.25), Inches(1.67), d.CW-Inches(0.5), Inches(0.5), size=13.5, color=b.WHITE, bold=True, shrink=True)
cols = grid_x(3)
titles = ["Situation", "Insight", "Recommendation"]
bodies = [
    ["40%+ of agentic projects cancelled by 2027 (Gartner).", "Deployed agents (Wendy's, Mercedes, SOAR) break in untested ways.", "Trust, not capability, is the blocker."],
    ["The moat is never the model — it's validation + data + compliance.", "Labs grade themselves; the auditor can't be a player.", "Independence is the only un-copyable wedge."],
    ["Certify autonomous agents for the risk owner, examiner-ready.", "Beachhead: bank Model Risk via the SR 26-2 vacuum.", "Paid pilots force real demand; GTM owns outreach."],
]
accents = [b.CORAL, b.TEAL, b.GOLD]
for (x, w), t, body, ac in zip(cols, titles, bodies, accents):
    card(s, x, Inches(2.45), w, Inches(3.0), t, body, accent=ac)
d.rect(s, d.M, Inches(5.7), d.CW, Inches(0.7), b.GOLD, radius=0.05)
d.text(s, "THE ASK:  Fund Phase 0 only — 5 discovery calls, 1 paid pilot, 1 ex-MRM/ex-examiner insider, in 90 days.",
       d.M+Inches(0.25), Inches(5.82), d.CW-Inches(0.5), Inches(0.5), size=14, color=b.NAVY, bold=True, shrink=True)
d.footer(s, 2, TOTAL)

# 3 — the trust shift (contrast)
s = d.slide(fill=b.WHITE)
d.header(s, "Capability is commoditized; trust is the race", "The model is no longer the moat")
half = (d.CW - Inches(0.3))/2
card(s, d.M, Inches(1.7), half, Inches(3.9), "2023–24 · Capability race",
     ["Frameworks, models, demos.", "Differentiation erodes on every model drop.", "Whoever had the best demo won the meeting.", "Outcome: commoditized — the labs win this."], accent=b.CORAL)
card(s, d.M+int(half+Inches(0.3)), Inches(1.7), half, Inches(3.9), "2026 · Trust race",
     ["Predict it, audit it, roll it back.", "Non-determinism breaks the old QA playbook.", "Same prompt → two different actions.", "Trust is an infrastructure problem before a feature."], accent=b.TEAL)
d.footer(s, 3, TOTAL)

# 4 — SR 26-2 unlock
s = d.slide(fill=b.WHITE)
d.header(s, "SR 26-2 left agentic AI ungoverned", "SR 26-2 replaced the 15-year model-risk rulebook (SR 11-7)")
d.rect(s, d.M, Inches(1.75), d.CW, Inches(1.5), b.NAVY, radius=0.05, shadow=True)
d.rect(s, d.M, Inches(1.75), Inches(0.12), Inches(1.5), b.TEAL)
d.text(s, [{"text": "“Generative AI and agentic AI models are", "size": 17, "bold": True, "italic": True, "color": b.WHITE},
           {"text": "not within the scope of this guidance.”", "size": 17, "bold": True, "italic": True, "color": b.WHITE, "space_before": 3}],
       d.M+Inches(0.35), Inches(1.92), d.CW-Inches(0.7), Inches(0.8))
d.text(s, "— OCC Bulletin 2026-13 / Fed SR 26-2 / FDIC", d.M+Inches(0.35), Inches(2.75), d.CW-Inches(0.7), Inches(0.35), size=12.5, color=b.LIGHT_TEAL)
cols = grid_x(3)
card(s, cols[0][0], Inches(3.5), cols[0][1], Inches(2.5), "The vacuum",
     ["Banks own agentic-AI governance with no playbook.", "An AI-specific RFI/rulemaking is coming next."], accent=b.AMBER)
card(s, cols[1][0], Inches(3.5), cols[1][1], Inches(2.5), "The exam still happens",
     ["“What is your monitoring framework?”", "“What is your effective challenge?”"], accent=b.AMBER)
card(s, cols[2][0], Inches(3.5), cols[2][1], Inches(2.5), "The opening",
     ["First mover authors the standard.", "“Whose name is on the examination finding?”"], accent=b.GOLD)
d.footer(s, 4, TOTAL)

# 5 — pain deployed (stat grid)
s = d.slide(fill=b.WHITE)
d.header(s, "The pain is deployed — and failing", "Live, branded, autonomous — then breaking in untested ways")
cols = grid_x(4)
stats = [("80%+", "of volume handled by live agents (Wendy's FreshAI, Mercedes MBUX)"),
         ("40%+", "of agentic AI projects cancelled by 2027 (Gartner)"),
         ("~100", "scenarios manual QA covers — vs millions users trigger"),
         ("0", "independent way to certify the autonomy today")]
for (x, w), (num, lab) in zip(cols, stats):
    stat(s, x, Inches(1.9), w, Inches(2.4), num, lab)
d.rect(s, d.M, Inches(4.7), d.CW, Inches(0.85), b.SOFT, radius=0.05)
d.text(s, "'Deployed' is not 'validated.' SOAR agents act on production with no human in the loop.",
       d.M+Inches(0.25), Inches(4.85), d.CW-Inches(0.5), Inches(0.6), size=14, color=b.INK, bold=True, shrink=True)
d.footer(s, 5, TOTAL)

# 6 — nobody independent
s = d.slide(fill=b.WHITE)
d.header(s, "Nobody independent can grade the agents", "The one claim none of the incumbents can make is independence")
cols = grid_x(2, gap=0.3)
row2 = Inches(3.75)
card(s, cols[0][0], Inches(1.7), cols[0][1], Inches(1.9), "Foundation labs",
     ["Ship native guardrails — but can't certify their own ecosystem."], accent=b.CORAL)
card(s, cols[1][0], Inches(1.7), cols[1][1], Inches(1.9), "Eval vendors (Braintrust, Patronus)",
     ["Sell tooling to the builder, not assurance to the buyer."], accent=b.CORAL)
card(s, cols[0][0], row2, cols[0][1], Inches(1.9), "Big 4 / MRM consultancies",
     ["Bespoke six-figure manual reviews — slow, unrepeatable, no standard."], accent=b.CORAL)
card(s, cols[1][0], row2, cols[1][1], Inches(1.9), "In-house model risk",
     ["No agent-native method; first-line, not independent."], accent=b.CORAL)
d.text(s, "→  Independence is our wedge.", d.M, Inches(5.85), d.CW, Inches(0.4), size=15, color=b.ACCENT, bold=True)
d.footer(s, 6, TOTAL)

# 7 — 9 patterns, 8 taken (scorecard)
s = d.slide(fill=b.WHITE)
d.header(s, "9 positioning patterns — 8 are taken", "Pattern 7 (Trust) is the open lane")
taken = [("Adapter", "Glean, Cursor"), ("New primitive", "LangChain, Browserbase"),
         ("Services-as-software", "Sierra, Decagon"), ("Sub-vertical squeeze", "EvenUp, Anterior"),
         ("Replacement / autopilot", "Cognition / Devin"), ("Proprietary-data moat", "Harvey, OpenEvidence"),
         ("Interface paradigm", "Lovable, Replit"), ("Industrial intelligence", "Skild, Physical Intelligence")]
cols = grid_x(2, gap=0.3)
y0 = Inches(1.7); rh = Inches(0.62)
for i, (pat, owner) in enumerate(taken):
    col = cols[i % 2]; row = i // 2
    x = col[0]; w = col[1]; y = y0 + int(rh*1.08)*row
    d.rect(s, x, y, w, rh, b.SOFT, radius=0.08)
    d.text(s, pat, x+Inches(0.2), y+Inches(0.13), w*0.55, Inches(0.4), size=12.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, owner, x+int(w*0.55), y+Inches(0.15), int(w*0.42), Inches(0.4), size=11, color=b.MUTED, align=PP_ALIGN.RIGHT, shrink=True)
d.rect(s, d.M, Inches(5.55), d.CW, Inches(0.85), b.NAVY, radius=0.06, shadow=True)
d.rect(s, d.M, Inches(5.55), Inches(0.12), Inches(0.85), b.GOLD)
d.text(s, "OPEN — Pattern 7: Trust. Certify the agent. Nobody owns it. The grader can't also be a player.",
       d.M+Inches(0.35), Inches(5.72), d.CW-Inches(0.6), Inches(0.5), size=15, color=b.GOLD, bold=True, shrink=True)
d.footer(s, 7, TOTAL)

# 8 — where defensible money lives
s = d.slide(fill=b.WHITE)
d.header(s, "Defensible money lives in KEEP, not REPLACE", "A 25-use-case scorecard sorts every deployed agent by moat")
cols = grid_x(3)
card(s, cols[0][0], Inches(1.8), cols[0][1], Inches(3.3), "REPLACE — low moat",
     ["Commoditizing.", "Labs + incumbents win.", "Thin wrappers die.", "Don't build a standalone agent here."], accent=b.CORAL)
card(s, cols[1][0], Inches(1.8), cols[1][1], Inches(3.3), "RENEGOTIATE — medium",
     ["Co-exist with the system of record.", "Drop the bolt-on seats.", "Adapter / augment plays."], accent=b.AMBER)
card(s, cols[2][0], Inches(1.8), cols[2][1], Inches(3.3), "KEEP — high moat",
     ["Proprietary data compounds.", "The defensible zone.", "We don't build an agent in any zone — we certify the ones others ship."], accent=b.TEAL)
d.footer(s, 8, TOTAL)

# 9 — our position
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
d.text(s, "OUR POSITION", d.M, Inches(0.9), Inches(9), Inches(0.4), size=15, color=b.TEAL, bold=True)
d.text(s, "Certify the autonomous agent before it ships", d.M, Inches(1.5), Inches(11.5), Inches(1.0),
       size=34, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(2.7), Inches(1.5), Inches(0.05), b.TEAL)
cols = grid_x(2, gap=0.3)
card(s, cols[0][0], Inches(3.1), cols[0][1], Inches(2.6), "The move",
     ["Package assurance as a hiring bar for the agent: 'passed before you deployed it.'", "Sell to the risk owner, not the developer — that's where pricing power lives."], accent=b.GOLD)
card(s, cols[1][0], Inches(3.1), cols[1][1], Inches(2.6), "The mechanism",
     ["Supervised validation + adversarial red-team + counterfactual provenance.", "Output the buyer shows a regulator, a board, or a court.", "We are the referee, not another player."], accent=b.TEAL)
d.footer(s, 9, TOTAL, dark=True)

# 10 — what we are
s = d.slide(fill=b.WHITE)
d.header(s, "We are the UL / SOC-2 for AI agents", "An independent authority whose stamp the market trusts")
cols = grid_x(4)
items = [("Independent", ["We don't build agents.", "We don't resell a builder's tool."]),
         ("Authoritative", ["We author the benchmark.", "We define 'safe to deploy.'"]),
         ("Continuous", ["Pre-deploy validation +", "ongoing assurance."]),
         ("Un-copyable", ["Labs & eval vendors can't claim independence.", "It is the product."])]
for (x, w), (t, body) in zip(cols, items):
    card(s, x, Inches(1.9), w, Inches(3.2), t, body, accent=b.TEAL)
d.footer(s, 10, TOTAL)

# 11 — the product
s = d.slide(fill=b.WHITE)
d.header(s, "The examiner-ready validation dossier", "Five components, mapped to what examiners already ask")
items = [("1 · Conceptual soundness", "Design, data, guardrails, escalation paths."),
         ("2 · Outcome testing", "Vs our domain benchmark + adversarial / red-team suite."),
         ("3 · Monitoring thresholds", "Drift + re-validation triggers on prompt/model change."),
         ("4 · Counterfactual provenance", "Why it acted — and why it didn't do the near-miss."),
         ("5 · Control attestations", "Data handling, human-in-loop, fair-lending.")]
y = Inches(1.75); rh = Inches(0.82)
for i, (t, body) in enumerate(items):
    yy = y + int(rh*1.05)*i
    d.rect(s, d.M, yy, d.CW, rh, b.SOFT, radius=0.08)
    d.rect(s, d.M, yy, Inches(0.1), rh, b.TEAL)
    d.text(s, t, d.M+Inches(0.3), yy+Inches(0.16), Inches(4.2), Inches(0.5), size=14, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, d.M+Inches(4.6), yy+Inches(0.18), d.CW-Inches(4.9), Inches(0.5), size=12.5, color=b.INK, shrink=True)
d.footer(s, 11, TOTAL)

# 12 — beachhead FS
s = d.slide(fill=b.WHITE)
d.header(s, "Beachhead: the SR 26-2 vacuum in banking", "The buyer and budget already exist — Model Risk is a mandated function")
cols = grid_x(2, gap=0.3)
card(s, cols[0][0], Inches(1.8), cols[0][1], Inches(3.6), "Why FS first",
     ["Banks must self-determine agentic controls — and have nothing.", "Model-risk / AI-governance is a mandated, budgeted function.", "We slot in as the independent validation it's required to obtain.", "The coming AI RFI is the deadline."], accent=b.TEAL)
card(s, cols[1][0], Inches(1.8), cols[1][1], Inches(3.6), "Why now beats later",
     ["The vacuum is the opening.", "First mover authors the standard before the rulebook lands.", "Window: mid-2026 → mid-2027.", "Then markets consolidate to 2–3 players."], accent=b.GOLD)
d.footer(s, 12, TOTAL)

# 13 — BAU correction (contrast)
s = d.slide(fill=b.WHITE)
d.header(s, "We validate the agents MRM can't", "Skip the BAU; lead with novel autonomy + high stakes")
half = (d.CW - Inches(0.3))/2
card(s, d.M, Inches(1.7), half, Inches(3.9), "Drop (BAU / low pain)",
     ["Generic support chatbots.", "OCR / document extraction.", "Solved, low-stakes, vendor-benchmarked.", "Mild validation pain — weak wedge."], accent=b.CORAL)
card(s, d.M+int(half+Inches(0.3)), Inches(1.7), half, Inches(3.9), "Lead with (acute pain)",
     ["Advisory / action-taking agents → suitability, fair-lending.", "Agentic decisioning → credit, collections, adverse-action.", "AML / fraud investigation → SAR quality.", "SecOps auto-remediation → audit risk."], accent=b.TEAL)
d.footer(s, 13, TOTAL)

# 14 — buyer & examiner
s = d.slide(fill=b.WHITE)
d.header(s, "Sell to the CRO; the examiner judges", "Three-persona sale, one external judge")
cols = grid_x(4)
roles = [("Economic buyer", ["Head of Model Risk / CRO.", "Holds budget + personal liability."], b.GOLD),
         ("Champion", ["AI-governance lead.", "Job is impossible without us."], b.TEAL),
         ("User", ["The line of business.", "Must pass our gate to ship."], b.ACCENT),
         ("The judge", ["The bank examiner (OCC/Fed/CFPB).", "Our dossier must survive exams."], b.NAVY)]
for (x, w), (t, body, ac) in zip(cols, roles):
    card(s, x, Inches(1.9), w, Inches(3.2), t, body, accent=ac)
d.text(s, "Survive exams once → become un-switchable. That bar is the forcing function and the moat.",
       d.M, Inches(5.4), d.CW, Inches(0.4), size=13.5, color=b.INK, bold=True, shrink=True)
d.footer(s, 14, TOTAL)

# 15 — pricing
s = d.slide(fill=b.WHITE)
d.header(s, "Paid pilot first, assurance forever", "Buyer-funded, in the audit / model-risk budget line")
cols = grid_x(2, gap=0.3)
card(s, cols[0][0], Inches(1.8), cols[0][1], Inches(3.2), "Pilot (the demand test)",
     ["Fixed-fee validation of one agent → examiner-ready dossier.", "Priced like an external model validation (5-figure).", "If they won't pay, the pain isn't real."], accent=b.GOLD)
card(s, cols[1][0], Inches(1.8), cols[1][1], Inches(3.2), "Subscription (the annuity)",
     ["Annual per-agent continuous assurance.", "Drift, re-validation, exam support.", "Same arc as pen-test → continuous monitoring."], accent=b.TEAL)
d.footer(s, 15, TOTAL)

# 16 — the moat
s = d.slide(fill=b.WHITE)
d.header(s, "The moat compounds 5 ways — not the model", "A trust + data + standard flywheel")
cols = grid_x(5, gap=0.18)
moats = [("Failure corpus", "Cross-customer view no bank or lab sees."),
         ("The benchmark", "We define 'good' — the Harvey LAB playbook."),
         ("Examiner trust", "A track record of surviving exams."),
         ("Independence", "Labs & eval vendors structurally can't copy."),
         ("Workflow lock-in", "Embedded in MRM process + board packs.")]
for (x, w), (t, body) in zip(cols, moats):
    d.rect(s, x, Inches(1.95), w, Inches(3.2), b.NAVY, radius=0.06, shadow=True)
    d.rect(s, x, Inches(1.95), w, Inches(0.1), b.TEAL)
    d.text(s, t, x+Inches(0.15), Inches(2.2), w-Inches(0.3), Inches(0.8), size=13.5, color=b.GOLD, bold=True, shrink=True)
    d.text(s, body, x+Inches(0.15), Inches(3.1), w-Inches(0.3), Inches(1.9), size=11, color=b.LIGHT_TEAL, shrink=True)
d.footer(s, 16, TOTAL)

# 17 — GTM storyboard
s = d.slide(fill=b.WHITE)
d.header(s, "GTM: services-led, platform-destined", "Build nothing reusable before pilot #1 is paid")
cols = grid_x(3)
phases = [("Phase 0", ["5+ discovery calls.", "1 paid teardown.", "Buy demand evidence with real fees."]),
          ("Phase 1", ["Paid pilots seed the failure corpus.", "Reference logos.", "Draft benchmark v0."]),
          ("Phase 2", ["Productize into a platform.", "Publish the benchmark = set the standard.", "Co-deliver with Big 4 / consultancies."])]
for i, ((x, w), (t, body)) in enumerate(zip(cols, phases)):
    card(s, x, Inches(1.9), w, Inches(3.2), t, body, accent=[b.GOLD, b.TEAL, b.ACCENT][i])
    if i < 2:
        d.text(s, "→", x+w+Inches(0.02), Inches(3.2), Inches(0.22), Inches(0.5), size=24, color=b.MUTED, align=C)
d.footer(s, 17, TOTAL)

# 18 — demand signals
s = d.slide(fill=b.WHITE)
d.header(s, "Demand is already moving in banking", "Active agents AND a named model-risk function — qualified now")
cols = grid_x(3)
banks = [("KeyBank · $189B", ["40 AI POCs; hired an AI Risk Advisor.", "AI Security Architect role: 'controlled autonomy of AI agents.'", "JD names MRM + SR 11-7 + fair lending."]),
         ("Fifth Third · $210B", ["Building 'governance, kill switches' for its agents.", "Agentic commerce with Brex.", "'Third part is agentic execution.'"]),
         ("Regions · $160B", ["AI-integrated lending platform launches Q2 2026.", "AI governance framework + CDAO.", "Decisioning is our wedge."])]
for (x, w), (t, body) in zip(cols, banks):
    card(s, x, Inches(1.9), w, Inches(3.3), t, body, accent=b.TEAL)
d.text(s, "GTM owns who to call — research handed over the accounts and the signals.",
       d.M, Inches(5.45), d.CW, Inches(0.4), size=13, color=b.MUTED, italic=True)
d.footer(s, 18, TOTAL)

# 19 — vertical 2 captive finance
s = d.slide(fill=b.WHITE)
d.header(s, "Captive auto-finance is the same buyer", "One thesis, two regulated doors")
cols = grid_x(2, gap=0.3)
card(s, cols[0][0], Inches(1.8), cols[0][1], Inches(3.4), "Captive lenders = regulated",
     ["Toyota Financial Services / TMCC and Nissan Motor Acceptance / NMAC.", "Same fair-lending, adverse-action, model-risk need.", "Same SR 26-2 vacuum."], accent=b.TEAL)
card(s, cols[1][0], Inches(1.8), cols[1][1], Inches(3.4), "Why it's an expansion, not a new company",
     ["Identical buyer logic: Chief Risk / Model Risk.", "Reuses the FS playbook + benchmark.", "Lowest-friction first vertical expansion."], accent=b.GOLD)
d.footer(s, 19, TOTAL)

# 20 — vertical 2b OEM fleets
s = d.slide(fill=b.WHITE)
d.header(s, "OEM agent fleets need a referee", "TMNA runs a 'system of agents' — the governance layer is open")
cols = grid_x(3)
stat(s, cols[0][0], Inches(1.95), cols[0][1], Inches(2.3), "2,300", "dealers on Toyota's agent; 7,000+ interactions/mo")
card(s, cols[1][0], Inches(1.95), cols[1][1], Inches(3.2), "The liability",
     ["Toyota bakes legal disclaimers into the dealer agent.", "Wrong spec/price/recall info = liability.", "Multi-agent supply chain = error propagation."], accent=b.CORAL)
card(s, cols[2][0], Inches(1.95), cols[2][1], Inches(3.2), "The open lane",
     ["Govern + validate the fleet: brand safety, legal compliance, provenance.", "Avoid the crowded dealer-chat apps (Impel, Cerence).", "Same thesis, above the BAU."], accent=b.TEAL)
d.footer(s, 20, TOTAL)

# 21 — why now
s = d.slide(fill=b.WHITE)
d.header(s, "A 12-month window to author the standard", "After mid-2027, verticals consolidate to 2–3 players")
steps = [("Apr 17, 2026", "SR 26-2 creates the agentic-AI vacuum."),
         ("Next", "AI-specific RFI / rulemaking from the agencies."),
         ("Mid-2026 → mid-2027", "The window to own a vertical position."),
         ("After", "Standard-setter is decided — first mover who survives exams wins.")]
cols = grid_x(4)
for i, ((x, w), (t, body)) in enumerate(zip(cols, steps)):
    d.rect(s, x, Inches(2.2), w, Inches(0.1), b.TEAL)
    d.text(s, t, x, Inches(2.4), w, Inches(0.5), size=14, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, x, Inches(3.0), w, Inches(2.2), size=12, color=b.INK, shrink=True)
    if i < 3:
        d.text(s, "→", x+w-Inches(0.05), Inches(2.3), Inches(0.25), Inches(0.5), size=20, color=b.MUTED)
d.footer(s, 21, TOTAL)

# 22 — why us
s = d.slide(fill=b.WHITE)
d.header(s, "Why us: independence you can't fake", "The moat accrues as we operate")
cols = grid_x(2, gap=0.3)
card(s, cols[0][0], Inches(1.8), cols[0][1], Inches(3.4), "Structural advantages",
     ["No pre-existing proprietary data needed — the corpus accrues as we run.", "The auditor cannot be the builder — permanent edge.", "A small team can author a standard before incumbents productize."], accent=b.TEAL)
card(s, cols[1][0], Inches(1.8), cols[1][1], Inches(3.4), "The one non-negotiable hire",
     ["An ex-MRM / ex-examiner on the cap table.", "Credibility to examiners IS the product.", "Everything else is reversible; this hire is not."], accent=b.GOLD)
d.footer(s, 22, TOTAL)

# 23 — competition (scorecard)
s = d.slide(fill=b.WHITE)
d.header(s, "Competition — and why we win", "")
rows = [("Big 4 / MRM consultancies", "Bespoke manual reviews", "We productize + arm them as channel"),
        ("Patronus / eval vendors", "Sell evals to the builder", "We sell assurance to the buyer"),
        ("Foundation labs", "Ship native guardrails", "Can't certify their own ecosystem"),
        ("In-house model risk", "First-line build", "Lacks independence + cross-bank corpus")]
y0 = Inches(1.7); rh = Inches(0.85)
# header row
d.rect(s, d.M, y0, d.CW, Inches(0.5), b.NAVY, radius=0.04)
for lbl, fx, fw in [("Competitor", 0.0, 0.30), ("Their move", 0.30, 0.32), ("Why we win", 0.62, 0.38)]:
    d.text(s, lbl, d.M+int(d.CW*fx)+Inches(0.2), y0+Inches(0.1), int(d.CW*fw), Inches(0.3), size=13, color=b.TEAL, bold=True, shrink=True)
for i, (c, mv, win) in enumerate(rows):
    yy = y0 + Inches(0.5) + int(rh*1.02)*i
    d.rect(s, d.M, yy, d.CW, rh, b.SOFT if i % 2 == 0 else b.WHITE, radius=0.0)
    d.text(s, c, d.M+Inches(0.2), yy+Inches(0.22), int(d.CW*0.30), Inches(0.5), size=12.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, mv, d.M+int(d.CW*0.30)+Inches(0.2), yy+Inches(0.22), int(d.CW*0.32), Inches(0.5), size=12, color=b.INK, shrink=True)
    d.text(s, win, d.M+int(d.CW*0.62)+Inches(0.2), yy+Inches(0.22), int(d.CW*0.38)-Inches(0.2), Inches(0.5), size=12, color=b.ACCENT, bold=True, shrink=True)
d.footer(s, 23, TOTAL)

# 24 — risks & kill-gates
s = d.slide(fill=b.WHITE)
d.header(s, "The honest risks — and the gates", "Name the failure conditions up front")
cols = grid_x(3)
gates = [("Gate 1 — Demand", ["5 calls must surface one blocked, paying buyer.", "Else: pivot."]),
         ("Gate 2 — Pilot", ["Sign one paid teardown.", "Else: pause."]),
         ("Gate 3 — Insider", ["Commit an ex-MRM / ex-examiner.", "Else: don't approach banks."])]
for (x, w), (t, body) in zip(cols, gates):
    card(s, x, Inches(1.8), w, Inches(2.3), t, body, accent=b.AMBER)
d.rect(s, d.M, Inches(4.45), d.CW, Inches(1.1), b.SOFT, radius=0.05)
d.text(s, [{"text": "Other risks:", "size": 12.5, "bold": True, "color": b.NAVY},
           {"text": "Regulators bless self-attestation → kill signal. The 'services trap' → every engagement must templatize into the product, or stop.", "size": 12, "space_before": 4}],
       d.M+Inches(0.25), Inches(4.6), d.CW-Inches(0.5), Inches(0.85), color=b.INK, shrink=True)
d.text(s, "Pass all three in 90 days → release platform funding.", d.M, Inches(5.75), d.CW, Inches(0.4), size=13.5, color=b.ACCENT, bold=True)
d.footer(s, 24, TOTAL)

# 25 — golden rules
s = d.slide(fill=b.WHITE)
d.header(s, "Two golden rules that keep us honest", "The discipline that prevents building on a hypothesis")
cols = grid_x(2, gap=0.3)
card(s, cols[0][0], Inches(1.8), cols[0][1], Inches(3.4), "GR1 — Paid pilots force demand",
     ["Every conversation drives to a paid validation pilot.", "The fee is the demand test.", "No free pilots. Politeness isn't demand."], accent=b.GOLD)
card(s, cols[1][0], Inches(1.8), cols[1][1], Inches(3.4), "GR2 — GTM owns outreach",
     ["Research hands over qualified accounts, signals, scripts.", "GTM names and contacts the humans.", "Break either and we're back to slideware."], accent=b.TEAL)
d.footer(s, 25, TOTAL)

# 26 — 90-day plan
s = d.slide(fill=b.WHITE)
d.header(s, "90 days: 5 calls, 1 paid pilot, 1 insider", "Every milestone is observable, not aspirational")
items = [("Weeks 1–4", "5+ MRM/CRO discovery calls; find one currently blocked autonomous agent."),
         ("Weeks 1–8", "Sign 1 paid 'Agent Validation Teardown.'"),
         ("Weeks 1–8", "Commit an ex-MRM / ex-examiner advisor or co-founder."),
         ("Parallel", "Draft the FS Agent Validation Benchmark v0 — the teardown spine.")]
y = Inches(1.85); rh = Inches(0.92)
for i, (t, body) in enumerate(items):
    yy = y + int(rh*1.05)*i
    d.rect(s, d.M, yy, d.CW, rh, b.SOFT, radius=0.08)
    d.rect(s, d.M, yy, Inches(0.1), rh, b.GOLD)
    d.text(s, t, d.M+Inches(0.3), yy+Inches(0.27), Inches(2.6), Inches(0.5), size=14, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, d.M+Inches(3.1), yy+Inches(0.27), d.CW-Inches(3.4), Inches(0.5), size=12.5, color=b.INK, shrink=True)
d.footer(s, 26, TOTAL)

# 27 — the ask
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
d.text(s, "NEXT ACTION", d.M, Inches(1.2), Inches(9), Inches(0.4), size=15, color=b.TEAL, bold=True)
d.text(s, "Run the 5 discovery calls.\nSign one paid pilot. Land one insider.", d.M, Inches(1.85), Inches(11.6), Inches(1.6),
       size=34, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(3.9), d.CW, Inches(0.9), b.GOLD, radius=0.05)
d.text(s, "Everything else waits behind those three. The vacuum is open now — the standard gets written by whoever moves first and survives the exam.",
       d.M+Inches(0.3), Inches(4.1), d.CW-Inches(0.6), Inches(0.6), size=15, color=b.NAVY, bold=True, shrink=True)
d.text(s, "Let's go get the first paid pilot.", d.M, Inches(5.2), Inches(11), Inches(0.5), size=18, color=b.TEAL, bold=True)
d.footer(s, 27, TOTAL, dark=True)

# 28 — appendix evidence base
s = d.slide(fill=b.WHITE)
d.header(s, "Appendix — the evidence base", "Full chain lives in GBrain")
items = [("Pattern library", "9 patterns + emerging patterns E1–E9."),
         ("10-company dossiers", "Harvey, Sierra, Cursor, Cognition live; 6 queued."),
         ("Use-case alignment", "Mapped to the 25-use-case scorecard."),
         ("GTM packages", "FS bank targets + SR 26-2 reframe; automotive doors."),
         ("Discipline", "CEO kill-gates + two golden rules.")]
y = Inches(1.8); rh = Inches(0.74)
for i, (t, body) in enumerate(items):
    yy = y + int(rh*1.05)*i
    d.rect(s, d.M, yy, d.CW, rh, b.SOFT, radius=0.08)
    d.rect(s, d.M, yy, Inches(0.1), rh, b.TEAL)
    d.text(s, t, d.M+Inches(0.3), yy+Inches(0.2), Inches(3.6), Inches(0.4), size=13.5, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, d.M+Inches(4.0), yy+Inches(0.21), d.CW-Inches(4.3), Inches(0.4), size=12, color=b.INK, shrink=True)
d.footer(s, 28, TOTAL)

d.save(OUT)
