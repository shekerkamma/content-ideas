#!/usr/bin/env python3
"""Build presales deal-prep deck for Hyundai UC05 Predictive Quality."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/branded-pptx-deck/scripts"))
from pptxkit import Deck, Inches, Pt, PP_ALIGN, MSO_ANCHOR

TOTAL = 11
d = Deck(footer="Presales Deal Prep · Hyundai Predictive Quality | June 2026")
b = d.b

# helper: small card with colored left spine
def spine_card(s, left, top, w, h, spine_color, title, body, *, title_size=13, body_size=11):
    d.rect(s, left, top, w, h, b.SOFT, radius=0.04, shadow=True)
    d.rect(s, left, top + Inches(0.05), Inches(0.07), h - Inches(0.1), spine_color)
    d.text(s, title, left + Inches(0.2), top + Inches(0.08), w - Inches(0.35), Inches(0.35),
           size=title_size, color=b.NAVY, bold=True, shrink=True)
    d.text(s, body, left + Inches(0.2), top + Inches(0.45), w - Inches(0.35), h - Inches(0.55),
           size=body_size, color=b.INK, shrink=True)

# ═══════════════════════════════════════════════════════════════════════════════
# S1 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
d.rect(s, Inches(11.4), 0, Inches(1.933), d.H, b.NAVY_2)
d.rect(s, Inches(11.4), 0, Inches(0.08), d.H, b.TEAL)
d.text(s, "PRESALES DEAL PREP · INTERNAL", d.M, Inches(1.0), Inches(7), Inches(0.4),
       size=14, color=b.TEAL, bold=True)
d.text(s, "Hyundai Manufacturing\nPredictive Quality Pilot",
       d.M, Inches(1.6), Inches(10), Inches(2.5),
       size=44, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
d.rect(s, d.M, Inches(4.3), Inches(1.2), Inches(0.06), b.TEAL)
d.text(s, "Sales toolkit: ROI framework, objection handling,\nbattle cards, mutual action plan",
       d.M, Inches(4.55), Inches(8), Inches(0.6), size=16, color=b.MUTED, shrink=True)
chips = ["UC05 Predictive Quality", "VP Mfg / VP Quality", "$40-60K Pilot", "4-Week Sprint"]
x = d.M
for chip in chips:
    d.rect(s, x, Inches(5.2), Inches(2.3), Inches(0.45), b.NAVY_2, radius=0.08)
    d.text(s, chip, x + Inches(0.1), Inches(5.24), Inches(2.1), Inches(0.38),
           size=11, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    x += Inches(2.5)
d.footer(s, 1, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# S2 — ACCOUNT SNAPSHOT
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Know Your Buyer Before The First Call",
         "Account snapshot — Hyundai manufacturing context")

# Left column: account facts
facts = [
    ("Industry", "Automotive manufacturing — high-volume production lines"),
    ("Target Buyer", "VP Manufacturing / VP Quality / Plant Manager"),
    ("Decision Style", "Plant-level autonomy for pilot budgets; corporate for multi-plant rollout"),
    ("Pain Signal", "Scrap/rework costs, end-of-line defect rates, SPC limitations"),
    ("IT Landscape", "SAP QM + PM, plant historians (InfluxDB/PI/MII), OPC-UA infrastructure"),
    ("Budget Range", "Plant ops budgets typically allow $50-100K pilot without corporate approval"),
]
for i, (label, value) in enumerate(facts):
    top = Inches(1.7) + i * Inches(0.82)
    d.rect(s, d.M, top, Inches(2.2), Inches(0.65), b.NAVY, radius=0.04)
    d.text(s, label, d.M + Inches(0.15), top + Inches(0.02), Inches(1.9), Inches(0.6),
           size=11, color=b.TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    d.text(s, value, Inches(3.05), top + Inches(0.05), Inches(9.2), Inches(0.55),
           size=12, color=b.INK, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

# Key insight strip
d.rect(s, d.M, Inches(6.35), d.CW, Inches(0.5), b.GOLD, radius=0.03)
d.text(s, "KEY INSIGHT:  Plant managers want a working prototype, not a strategy deck. Lead with the 4-week timeline and shadow-mode validation.",
       Inches(0.85), Inches(6.38), Inches(11.5), Inches(0.44),
       size=12, color=b.NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.footer(s, 2, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S3 — DISCOVERY AGENDA
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Eight Questions That Determine If This Deal Is Real",
         "First-call discovery agenda — qualify before you pitch")

questions = [
    ("What are your top 3\ndefect types by cost?", "Tells us which station to pilot.\nObjective defects (dimensional, torque)\nare easier wins than cosmetic.", b.TEAL),
    ("What's your current\nscrap/rework rate?", "Anchors the ROI calc. Even 2-3%\nscrap on a high-volume line is\nmillions annually.", b.TEAL),
    ("Which historian platform\ndo you run?", "InfluxDB vs SAP MII vs OSIsoft PI\ndetermines our connector strategy.\nConfirm OPC-UA availability.", b.ACCENT),
    ("What SAP version\nand OData services?", "S/4HANA has better OData coverage.\nECC needs custom CDS views.\nThis scopes integration effort.", b.ACCENT),
    ("How are inspection\nresults recorded?", "SAP QM inspection lots = training\nlabels. Need 6+ months of history\nwith part-ID correlation.", b.GOLD),
    ("Who owns the\nhistorian/OT layer?", "IT/OT politics is risk #2.\nEarly OT alignment prevents\nWeek 1 access blockers.", b.GOLD),
    ("Have you tried ML\nfor quality before?", "If yes: what failed and why.\nIf no: gauge appetite for\nAI-driven decisions.", b.CORAL),
    ("What's the approval\npath for a pilot?", "Plant-level sign-off vs.\ncorporate. Determines our\nchampion strategy.", b.CORAL),
]
cw = Inches(2.85)
ch = Inches(2.35)
gap = Inches(0.18)
for i, (q, insight, color) in enumerate(questions):
    row, col = divmod(i, 4)
    left = d.M + col * (cw + gap)
    top = Inches(1.7) + row * (ch + Inches(0.15))
    d.rect(s, left, top, cw, ch, b.SOFT, radius=0.05, shadow=True)
    d.rect(s, left, top, cw, Inches(0.07), color)
    # question number
    d.text(s, f"Q{i+1}", left + Inches(0.1), top + Inches(0.15), Inches(0.4), Inches(0.3),
           size=10, color=color, bold=True)
    d.text(s, q, left + Inches(0.1), top + Inches(0.4), cw - Inches(0.2), Inches(0.7),
           size=12, color=b.NAVY, bold=True, shrink=True)
    d.text(s, insight, left + Inches(0.1), top + Inches(1.15), cw - Inches(0.2), Inches(1.05),
           size=10, color=b.MUTED, shrink=True)
d.footer(s, 3, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S4 — ROI FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Even A 20% Scrap Reduction Pays For The Pilot In Weeks",
         "ROI framework — conservative assumptions, plant-manager math")

# Assumptions box
d.rect(s, d.M, Inches(1.7), Inches(5.5), Inches(2.8), b.SOFT, radius=0.05)
d.text(s, "CONSERVATIVE ASSUMPTIONS", d.M + Inches(0.2), Inches(1.78), Inches(5), Inches(0.35),
       size=11, color=b.MUTED, bold=True)
assumptions = [
    ("Parts/day per line:", "500 - 2,000"),
    ("Average part cost:", "$50 - $200"),
    ("Current scrap rate:", "2% - 5%"),
    ("Daily scrap cost:", "$500 - $20,000 per line"),
    ("Annual scrap (1 line):", "$130K - $5.2M"),
    ("Defect reduction target:", "20% (conservative pilot goal)"),
    ("Annual savings (1 line):", "$26K - $1.04M"),
]
for i, (label, value) in enumerate(assumptions):
    yt = Inches(2.2) + i * Inches(0.3)
    d.text(s, label, d.M + Inches(0.25), yt, Inches(2.5), Inches(0.28),
           size=11.5, color=b.INK, bold=True)
    d.text(s, value, Inches(3.3), yt, Inches(2.5), Inches(0.28),
           size=11.5, color=b.TEAL, bold=True)

# Payback box
d.rect(s, Inches(6.6), Inches(1.7), Inches(5.95), Inches(2.8), b.NAVY, radius=0.05, shadow=True)
d.text(s, "PAYBACK SCENARIOS", Inches(6.85), Inches(1.78), Inches(5.5), Inches(0.35),
       size=11, color=b.TEAL, bold=True)

scenarios = [
    ("Low-Volume Line", "500 parts/day × $50 × 2% scrap\n= $500/day scrap cost\n20% reduction = $100/day saved\nPilot payback: ~400 days", b.MUTED),
    ("Mid-Volume Line", "1,000 parts/day × $100 × 3% scrap\n= $3,000/day scrap cost\n20% reduction = $600/day saved\nPilot payback: ~80 days", b.GOLD),
    ("High-Volume Line", "2,000 parts/day × $150 × 4% scrap\n= $12,000/day scrap cost\n20% reduction = $2,400/day saved\nPilot payback: ~20 days", b.TEAL),
]
for i, (title, calc, color) in enumerate(scenarios):
    yt2 = Inches(2.25) + i * Inches(0.78)
    d.text(s, title, Inches(6.85), yt2, Inches(2.0), Inches(0.3),
           size=11, color=color, bold=True)
    d.text(s, calc, Inches(8.9), yt2, Inches(3.4), Inches(0.7),
           size=10, color=b.WHITE, shrink=True)

# Bottom insight
d.rect(s, d.M, Inches(4.8), d.CW, Inches(0.55), b.GOLD, radius=0.03)
d.text(s, 'TALK TRACK:  "On a mid-volume line, scrap costs ~$3K/day. A 20% reduction saves $600/day — the pilot pays for itself in under 3 months."',
       Inches(0.85), Inches(4.83), Inches(11.5), Inches(0.48),
       size=12, color=b.NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

# Secondary value drivers
d.text(s, "SECONDARY VALUE DRIVERS (harder to quantify, mention but don't lead with)",
       d.M, Inches(5.6), Inches(8), Inches(0.35), size=11, color=b.MUTED, bold=True)
secondary = [
    "Reduced warranty claims from escaped defects reaching customers",
    "Lower inspection labor — model pre-screens, humans verify flagged parts only",
    "Process optimization insights from root-cause analysis (systemic, not per-part)",
    "Faster new-product ramp — model learns new part signatures in days, not months",
]
for i, item in enumerate(secondary):
    d.text(s, [{"text": item, "bullet": True, "space_before": 4, "size": 11.5}],
           d.M + Inches(0.2), Inches(5.95) + i * Inches(0.38), Inches(11), Inches(0.35),
           shrink=True)
d.footer(s, 4, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S5 — OBJECTION HANDLING (part 1: top 3)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Anticipate These Five Objections — Here's How To Respond",
         "Objection handling — tested responses for the most common pushback")

objections_1 = [
    ("We already have SPC and\nstatistical process control",
     "REFRAME — SPC detects drift after it happens. Our model predicts defects before the part "
     "reaches end-of-line. SPC sets control limits; we tell you which specific part is likely "
     "defective and why. They're complementary — our dashboard enhances your existing SPC charts "
     "with ML-detected anomalies.",
     "Don't attack SPC — position as an upgrade layer on top of it.", b.TEAL),
    ("Our data isn't clean enough\nfor machine learning",
     "VALIDATE — That's exactly why Week 1 is a dedicated data discovery gate. We connect, pull, "
     "and assess data quality before any model-build spend. If data is unusable, we pivot scope "
     "or exit — you don't pay for a model that can't work. We also start with objective defect "
     "types (dimensional, torque) where labels are cleanest.",
     "Week 1 gate is the trust-builder. Show you're not afraid to walk away.", b.GOLD),
    ("IT/OT won't give us\naccess to the historian",
     "PROACTIVE — We present the architecture to the OT team in a Week 0 pre-kick session before "
     "the pilot starts. Our approach is historian read-only — we never touch PLCs, never write to "
     "OT systems. We can even run on a replicated historian if the primary is off-limits.",
     "Name the OT concern before they do. Read-only access is the key phrase.", b.CORAL),
]
card_h = Inches(1.6)
for i, (objection, response, coaching, color) in enumerate(objections_1):
    top = Inches(1.7) + i * (card_h + Inches(0.15))
    # objection panel
    d.rect(s, d.M, top, Inches(3.0), card_h, color, radius=0.04)
    d.text(s, f'OBJECTION {i+1}', d.M + Inches(0.15), top + Inches(0.08), Inches(1.5), Inches(0.25),
           size=9, color=b.WHITE, bold=True)
    d.text(s, f'"{objection}"', d.M + Inches(0.15), top + Inches(0.38), Inches(2.7), Inches(1.1),
           size=13, color=b.WHITE, bold=True, shrink=True)
    # response
    d.text(s, response, Inches(3.25), top + Inches(0.05), Inches(7.4), card_h - Inches(0.45),
           size=11.5, color=b.INK, shrink=True)
    # coaching note
    d.text(s, coaching, Inches(3.25), top + card_h - Inches(0.35), Inches(7.4), Inches(0.3),
           size=10, color=b.MUTED, italic=True, shrink=True)
d.footer(s, 5, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S6 — OBJECTION HANDLING (part 2: remaining 2)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Two More Objections You'll Hear — And How To Turn Them",
         "Objection handling continued")

objections_2 = [
    ("We tried ML for quality\nbefore and it didn't work",
     "DIAGNOSE — Ask what failed: data quality? model accuracy? adoption? Most ML quality projects "
     "fail on change management, not algorithms. Our explainability-first approach (SHAP dashboards "
     "showing exactly why each prediction was made) is specifically designed to build operator trust. "
     "We start in advisory mode — the model recommends, humans decide. No black boxes.",
     "Get specifics on what failed. Usually it's adoption, not tech — that's our sweet spot.", b.GOLD),
    ("$40-60K is too expensive\nfor a pilot",
     "ANCHOR HIGH — Traditional consulting (Accenture, McKinsey) charges $200-400K+ for a 6-month "
     "engagement that delivers a strategy deck, not a working prototype. SaaS platforms (Sight Machine) "
     "cost $100K+/year in licensing alone. Our pilot delivers a working, validated model in 4 weeks "
     "at a fraction of the cost. If a mid-volume line scraps $3K/day, the pilot pays for itself in "
     "under 3 months.",
     "Always anchor against the expensive alternative first, then show the payback math.", b.CORAL),
]
card_h2 = Inches(2.0)
for i, (objection, response, coaching, color) in enumerate(objections_2):
    top = Inches(1.7) + i * (card_h2 + Inches(0.2))
    d.rect(s, d.M, top, Inches(3.0), card_h2, color, radius=0.04)
    d.text(s, f'OBJECTION {i+4}', d.M + Inches(0.15), top + Inches(0.08), Inches(1.5), Inches(0.25),
           size=9, color=b.WHITE, bold=True)
    d.text(s, f'"{objection}"', d.M + Inches(0.15), top + Inches(0.4), Inches(2.7), Inches(1.3),
           size=14, color=b.WHITE, bold=True, shrink=True)
    d.text(s, response, Inches(3.25), top + Inches(0.05), Inches(7.4), card_h2 - Inches(0.5),
           size=12, color=b.INK, shrink=True)
    d.text(s, coaching, Inches(3.25), top + card_h2 - Inches(0.38), Inches(7.4), Inches(0.32),
           size=10.5, color=b.MUTED, italic=True, shrink=True)

# coaching summary
d.rect(s, d.M, Inches(6.15), d.CW, Inches(0.55), b.NAVY, radius=0.03)
d.text(s, "COACHING:  Never argue — validate the concern, then reframe. The Week 1 data gate and SHAP explainability are your two strongest trust signals.",
       Inches(0.85), Inches(6.18), Inches(11.5), Inches(0.48),
       size=12, color=b.TEAL, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.footer(s, 6, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S7 — COMPETITIVE BATTLE CARD
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Position Against Each Competitor Differently — Here's How",
         "Competitive battle card — when they mention a name, use this response")

competitors = [
    ("vs. Sight Machine",
     "They're a SaaS platform — $100K+/year, rigid, long implementation. You're renting their "
     "platform, not owning your solution.",
     "WE WIN ON: cost (4x cheaper), speed (4 weeks vs 3-6 months), ownership (open-source "
     "stack, you keep the models and code).",
     "WATCH OUT: they have deep manufacturing-specific features. Don't claim we match "
     "their platform breadth — we beat them on speed-to-value for a focused use case.", b.TEAL),
    ("vs. Accenture / McKinsey",
     "6+ months, $200-400K+, delivers a strategy deck and a team of consultants. "
     "By the time they finish scoping, we've delivered a working prototype.",
     "WE WIN ON: speed (4 weeks vs 6+ months), cost (50-70% cheaper), deliverable "
     "(working model, not a PowerPoint).",
     "WATCH OUT: they have enterprise relationships. If the buyer values brand safety "
     "over speed, we may need to position as a complementary specialist.", b.GOLD),
    ("vs. PTC ThingWorx / Siemens MindSphere",
     "Industrial IoT platforms with ML bolt-ons. Deep plant integration but vendor "
     "lock-in, complex licensing, and the ML is a secondary capability.",
     "WE WIN ON: ML-first approach, explainability (SHAP > their built-in analytics), "
     "no platform lock-in, and we integrate with their IoT layer if it's already there.",
     "WATCH OUT: if they're already deployed as the historian, position us as the "
     "intelligence layer on top, not a replacement.", b.CORAL),
]
card_h3 = Inches(1.55)
for i, (name, profile, win, watch, color) in enumerate(competitors):
    top = Inches(1.65) + i * (card_h3 + Inches(0.12))
    # competitor name badge
    d.rect(s, d.M, top, Inches(2.0), card_h3, color, radius=0.04)
    d.text(s, name, d.M + Inches(0.12), top + Inches(0.05), Inches(1.76), card_h3 - Inches(0.1),
           size=15, color=b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER,
           shrink=True)
    # profile + win + watch
    d.text(s, profile, Inches(2.25), top + Inches(0.03), Inches(4.0), Inches(0.65),
           size=10.5, color=b.INK, shrink=True)
    d.text(s, win, Inches(2.25), top + Inches(0.72), Inches(4.0), Inches(0.7),
           size=10.5, color=b.TEAL, bold=True, shrink=True)
    d.text(s, watch, Inches(6.5), top + Inches(0.03), Inches(5.8), card_h3 - Inches(0.1),
           size=10.5, color=b.MUTED, italic=True, shrink=True)
d.footer(s, 7, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S8 — PRICING OPTIONS
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Three Packaging Options — Lead With 'Better', Upsell to 'Best'",
         "Good / Better / Best pricing — recommended anchor is the middle tier")

packages = [
    ("GOOD", "$40K", "Single-Station Pilot",
     ["4-week sprint, 1 station", "XGBoost baseline model",
      "Basic SHAP dashboard", "SAP QM read integration",
      "Pilot results report"],
     "Data discovery + model + dashboard.\nProves feasibility on one station.",
     b.ACCENT, b.WHITE),
    ("BETTER", "$55K", "Pilot + SAP Closed Loop",
     ["Everything in Good, plus:", "SAP PM write (notifications)",
      "Process drift SPC dashboard", "Natural-language query interface",
      "Scale-up proposal with ROI calc"],
     "Full closed-loop system.\nQuality team can act on predictions.",
     b.TEAL, b.WHITE),
    ("BEST", "$75K", "Pilot + Multi-Station Ready",
     ["Everything in Better, plus:", "2nd station model (parallel)",
      "Cross-station correlation analysis", "MLflow experiment tracking",
      "Handoff documentation + training"],
     "Proves scale economics.\nDe-risks the multi-line expansion.",
     b.GOLD, b.NAVY),
]
pkg_w = Inches(3.7)
pkg_gap = Inches(0.3)
for i, (tier, price, subtitle, features, note, color, price_color) in enumerate(packages):
    left = d.M + i * (pkg_w + pkg_gap)
    # card
    d.rect(s, left, Inches(1.7), pkg_w, Inches(5.0), b.SOFT, radius=0.06, shadow=True)
    # tier header
    d.rect(s, left, Inches(1.7), pkg_w, Inches(1.3), color, radius=0.06)
    # fix bottom corners of header (overlay rect)
    d.rect(s, left, Inches(2.55), pkg_w, Inches(0.45), color)
    d.text(s, tier, left + Inches(0.2), Inches(1.78), pkg_w - Inches(0.4), Inches(0.3),
           size=12, color=price_color, bold=True)
    d.text(s, price, left + Inches(0.2), Inches(2.05), pkg_w - Inches(0.4), Inches(0.55),
           size=36, color=price_color, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, subtitle, left + Inches(0.2), Inches(2.6), pkg_w - Inches(0.4), Inches(0.3),
           size=11, color=price_color)
    # features
    for j, feat in enumerate(features):
        bld = j == 0 and i > 0  # "Everything in X, plus:" is bold
        d.text(s, [{"text": feat, "bullet": not bld, "space_before": 5, "size": 11,
                     "bold": bld}],
               left + Inches(0.2), Inches(3.15) + j * Inches(0.35),
               pkg_w - Inches(0.4), Inches(0.32), shrink=True)
    # note at bottom
    d.text(s, note, left + Inches(0.2), Inches(5.95), pkg_w - Inches(0.4), Inches(0.55),
           size=10, color=b.MUTED, italic=True, shrink=True)

# retainer note
d.rect(s, d.M, Inches(6.7), d.CW, Inches(0.5), b.NAVY, radius=0.03)
d.text(s, "ALL TIERS:  +$8-12K/month retainer after pilot (monitoring, retraining, support)  ·  Each additional line: ~$20K add-on",
       Inches(0.85), Inches(6.73), Inches(11.5), Inches(0.44),
       size=12, color=b.TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.footer(s, 8, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S9 — INDUSTRY PROOF POINTS
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "The Industry Is Moving — Predictive Quality Is Table Stakes By 2028",
         "Proof points and industry validation")

# KPI boxes
proof_kpis = [
    ("35-50%", "scrap reduction reported\nby early adopters of\npredictive quality ML", b.TEAL),
    ("$1.8T", "global cost of poor quality\nin manufacturing annually\n(ASQ estimate)", b.GOLD),
    ("73%", "of manufacturers plan\nto invest in AI-driven quality\nby 2027 (Deloitte)", b.CORAL),
    ("10-25x", "typical ROI on predictive\nquality investments over\n3-year horizon", b.ACCENT),
]
kw = Inches(2.7)
for i, (num, label, color) in enumerate(proof_kpis):
    left = d.M + i * (kw + Inches(0.3))
    d.rect(s, left, Inches(1.75), kw, Inches(1.5), b.NAVY, radius=0.05, shadow=True)
    d.text(s, num, left + Inches(0.15), Inches(1.85), kw - Inches(0.3), Inches(0.6),
           size=30, color=color, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, label, left + Inches(0.15), Inches(2.5), kw - Inches(0.3), Inches(0.65),
           size=10.5, color=b.WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

# analogies
d.text(s, "ANALOGIES THAT LAND WITH PLANT MANAGERS", d.M, Inches(3.55),
       Inches(6), Inches(0.35), size=11, color=b.MUTED, bold=True)

analogies = [
    ('"It\'s like cruise control for quality"',
     "SPC is the speedometer — you see you're speeding after the fact. "
     "Predictive quality is cruise control — it adjusts before you drift."),
    ('"We\'re not replacing inspectors — we\'re giving them a head start"',
     "The model pre-screens 100% of parts. Inspectors focus attention on the 5% "
     "that the model flagged. Same team, higher catch rate, less fatigue."),
    ('"Shadow mode means zero risk"',
     "For the first 2 weeks after pilot, the model runs alongside your existing "
     "process. It makes predictions but doesn't change anything. You validate "
     "against actual results — only go live when you trust the numbers."),
]
for i, (quote, explanation) in enumerate(analogies):
    top = Inches(3.95) + i * Inches(0.95)
    d.rect(s, d.M, top, d.CW, Inches(0.78), b.SOFT, radius=0.04)
    d.rect(s, d.M, top + Inches(0.05), Inches(0.07), Inches(0.68), b.TEAL)
    d.text(s, quote, Inches(0.85), top + Inches(0.05), Inches(4.5), Inches(0.35),
           size=12, color=b.NAVY, bold=True, italic=True, shrink=True)
    d.text(s, explanation, Inches(5.5), top + Inches(0.05), Inches(6.8), Inches(0.68),
           size=11, color=b.INK, shrink=True)
d.footer(s, 9, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S10 — MUTUAL ACTION PLAN
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "From First Call To Running Pilot In 6 Weeks — Here's The Path",
         "Mutual action plan — shared timeline builds commitment")

milestones = [
    ("WEEK -2", "Discovery\nCall", "Qualify the opportunity.\nRun the 8 discovery questions.\nConfirm budget and timeline.", b.TEAL),
    ("WEEK -1", "Technical\nDiscovery", "Confirm historian, SAP version,\nOData availability.\nOT architecture review.", b.ACCENT),
    ("WEEK 0", "Pre-Kick\n& Access", "OT team alignment.\nHistorian access provisioned.\nSAP QM data sample pulled.", b.GOLD),
    ("WEEK 1-4", "Pilot\nSprint", "Data → Model → Dashboard →\nSAP integration → Shadow\nmode validation.", b.CORAL),
    ("WEEK 5", "Results &\nScale Decision", "Pilot results report.\nScale-up proposal + ROI.\nMulti-line roadmap.", b.NAVY),
]
mw = Inches(2.15)
m_gap = Inches(0.22)
total_mw = len(milestones) * mw + (len(milestones) - 1) * m_gap
mx = int((d.W - total_mw) / 2)
# connecting line
d.rect(s, mx + Inches(0.3), Inches(2.65), total_mw - Inches(0.6), Inches(0.04), b.GRID)
for i, (week, title, tasks, color) in enumerate(milestones):
    left = mx + i * (mw + m_gap)
    # circle node on timeline
    d.rect(s, left + Inches(0.85), Inches(2.45), Inches(0.45), Inches(0.45), color, radius=0.5)
    d.text(s, str(i + 1), left + Inches(0.88), Inches(2.48), Inches(0.4), Inches(0.4),
           size=14, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # week label above
    d.text(s, week, left, Inches(1.85), mw, Inches(0.35),
           size=10, color=color, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, title, left, Inches(2.15), mw, Inches(0.4),
           size=13, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER, shrink=True)
    # card below
    d.rect(s, left, Inches(3.15), mw, Inches(1.8), b.SOFT, radius=0.04, shadow=True)
    d.rect(s, left, Inches(3.15), mw, Inches(0.06), color)
    d.text(s, tasks, left + Inches(0.1), Inches(3.3), mw - Inches(0.2), Inches(1.55),
           size=10.5, color=b.INK, shrink=True)

# commitment ask
d.rect(s, d.M, Inches(5.3), d.CW, Inches(0.85), b.NAVY, radius=0.04)
d.text(s, "WHAT WE NEED FROM YOU", d.M + Inches(0.25), Inches(5.35), Inches(3), Inches(0.25),
       size=10, color=b.TEAL, bold=True)
needs = [
    "A named champion (VP Quality or Plant Manager) who owns the pilot internally",
    "Historian read access + SAP QM data sample provisioned by Week 0",
    "30-minute OT architecture review in Week -1 to de-risk access",
    "Decision meeting at Week 5 to review results and approve scale-up",
]
for i, need in enumerate(needs):
    d.text(s, [{"text": need, "bullet": True, "space_before": 2, "size": 11}],
           d.M + Inches(0.25), Inches(5.65) + i * Inches(0.22),
           Inches(11.5), Inches(0.22), color=b.WHITE, shrink=True)
d.footer(s, 10, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S11 — PRE-CALL CHECKLIST
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Don't Walk Into The Call Without These — Pre-Call Checklist",
         "Preparation gate before the first meeting")

# two columns
col1_items = [
    ("MUST CONFIRM", b.CORAL, [
        "Plant location and which lines/stations are candidates",
        "Current scrap rate (even a rough % is enough to anchor ROI)",
        "Historian platform in use (InfluxDB, OSIsoft PI, SAP MII)",
        "SAP version (S/4HANA vs ECC) and available OData services",
        "Who owns OT/historian access (name + role)",
        "Budget authority: plant-level or corporate approval needed?",
    ]),
    ("MUST BRING", b.TEAL, [
        "UC05 Realization Deck (the client-facing deck we built)",
        "ROI calculator with their scrap rate plugged in",
        "Architecture diagram (sensors → historian → model → SAP)",
        "Shadow mode explanation (zero-risk validation approach)",
        "Reference: 4-week timeline with weekly deliverables",
        "Competitive comparison (if they mention a specific vendor)",
    ]),
]
for ci, (section_title, color, items) in enumerate(col1_items):
    left = d.M + ci * Inches(6.2)
    cw2 = Inches(5.8)
    d.rect(s, left, Inches(1.7), cw2, Inches(0.45), color, radius=0.03)
    d.text(s, section_title, left + Inches(0.2), Inches(1.73), cw2 - Inches(0.4), Inches(0.4),
           size=13, color=b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    for j, item in enumerate(items):
        yt = Inches(2.3) + j * Inches(0.55)
        d.rect(s, left + Inches(0.15), yt, Inches(0.35), Inches(0.35), b.SOFT, radius=0.05)
        d.text(s, "☐", left + Inches(0.17), yt - Inches(0.02), Inches(0.32), Inches(0.35),
               size=14, color=b.MUTED, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        d.text(s, item, left + Inches(0.6), yt + Inches(0.02), cw2 - Inches(0.8), Inches(0.32),
               size=11.5, color=b.INK, shrink=True)

# bottom strip
d.rect(s, d.M, Inches(6.0), d.CW, Inches(0.7), b.NAVY, radius=0.03)
d.text(s, [
    {"text": "GOLDEN RULE: ", "size": 12, "color": b.GOLD, "bold": True},
    {"text": "If you can't confirm the scrap rate and historian platform before the call, ", "size": 12, "color": b.WHITE},
    {"text": "reschedule the call. ", "size": 12, "color": b.GOLD, "bold": True},
    {"text": "Discovery without data context wastes both sides' time.", "size": 12, "color": b.WHITE},
], d.M + Inches(0.25), Inches(6.05), d.CW - Inches(0.5), Inches(0.6),
   anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.footer(s, 11, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
out = d.save("docs/reports/hyundai-deal-prep-uc05.pptx")
print(f"\nDeck ready: {out}")
