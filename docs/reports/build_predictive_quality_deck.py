#!/usr/bin/env python3
"""Build client-facing UC05 Predictive Quality deck for Hyundai manufacturing."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/branded-pptx-deck/scripts"))
from pptxkit import Deck, Inches, Pt, PP_ALIGN, MSO_ANCHOR

TOTAL = 12
d = Deck(footer="Predictive Quality AI · Hyundai Manufacturing | June 2026")
b = d.b

# ═══════════════════════════════════════════════════════════════════════════════
# S1 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.NAVY)
# right strip
d.rect(s, Inches(11.4), 0, Inches(1.933), d.H, b.NAVY_2)
d.rect(s, Inches(11.4), 0, Inches(0.08), d.H, b.TEAL)
# kicker
d.text(s, "USE-CASE REALIZATION · UC05", d.M, Inches(1.0), Inches(7), Inches(0.4),
       size=14, color=b.TEAL, bold=True)
# title
d.text(s, "Predictive Quality\nfor Automotive Manufacturing",
       d.M, Inches(1.6), Inches(9), Inches(2.0),
       size=48, color=b.WHITE, bold=True, font=b.FONT_H, shrink=True)
# rule
d.rect(s, d.M, Inches(3.8), Inches(1.2), Inches(0.06), b.TEAL)
# subtitle
d.text(s, "Sensor-driven defect prediction with AI engineering acceleration",
       d.M, Inches(4.1), Inches(8), Inches(0.5), size=18, color=b.MUTED)
# chips
chips = ["OpenHands", "SAP QM/PM", "XGBoost + SHAP", "ADK + AG-UI"]
x = d.M
for chip in chips:
    d.rect(s, x, Inches(5.2), Inches(2.1), Inches(0.45), b.NAVY_2, radius=0.08)
    d.text(s, chip, x + Inches(0.15), Inches(5.24), Inches(1.8), Inches(0.38),
           size=11, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER,
           anchor=MSO_ANCHOR.MIDDLE)
    x += Inches(2.3)
d.footer(s, 1, TOTAL, dark=True)

# ═══════════════════════════════════════════════════════════════════════════════
# S2 — EXECUTIVE SUMMARY (BLUF)
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Predict Defective Parts Mid-Line Before They Become Scrap",
         "Executive summary — the answer first")
# BLUF banner
d.rect(s, d.M, Inches(1.6), d.CW, Inches(1.0), b.NAVY, radius=0.04)
d.text(s, "We deliver a 4-week pilot that predicts out-of-spec parts using in-process sensor "
       "data, flags defects before end-of-line inspection, and integrates directly with SAP QM/PM — "
       "at 50-70% less cost than traditional consulting.",
       Inches(0.85), Inches(1.68), Inches(11.5), Inches(0.88),
       size=14, color=b.WHITE, shrink=True)

# three columns
col_w = Inches(3.7)
cols = [
    ("SITUATION", b.CORAL,
     "Automotive plants lose millions annually to scrap and rework. "
     "Defects are caught at end-of-line — too late to prevent upstream batch failures. "
     "Sensor data exists but sits unused in historians."),
    ("INSIGHT", b.TEAL,
     "In-process sensor signals (welding current, torque curves, paint thickness) "
     "contain early warning patterns. XGBoost on featurized traces reaches useful "
     "precision with as little as 3 months of labeled inspection data from SAP QM."),
    ("RECOMMENDATION", b.GOLD,
     "Start a single-station pilot ($40-60K, 4 weeks). Validate the model in shadow mode "
     "alongside existing inspection. Scale to additional lines at ~$20K each. "
     "Monthly retainer $8-12K covers monitoring, retraining, and dashboard support."),
]
for i, (title, color, body) in enumerate(cols):
    left = d.M + i * (col_w + Inches(0.3))
    d.rect(s, left, Inches(2.9), col_w, Inches(0.06), color)
    d.text(s, title, left, Inches(3.05), col_w, Inches(0.35),
           size=12, color=color, bold=True)
    d.text(s, body, left, Inches(3.45), col_w, Inches(2.5),
           size=12, color=b.INK, shrink=True)

# THE ASK strip
d.rect(s, d.M, Inches(6.3), d.CW, Inches(0.55), b.GOLD, radius=0.03)
d.text(s, "THE ASK:  Approve a 4-week, $40-60K pilot on one welding or torque station with historian + SAP QM access",
       Inches(0.85), Inches(6.33), Inches(11.5), Inches(0.48),
       size=13.5, color=b.NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.footer(s, 2, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S3 — THE PROBLEM
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Defects Are Caught Too Late — Upstream Data Goes Unused",
         "The quality gap in automotive manufacturing")

problems = [
    ("End-of-Line Detection", "Defects found at final inspection after the damage is done. "
     "Entire batches may be scrapped if a process drifted early."),
    ("Sensor Data Silos", "Welding robots, torque tools, paint booths, and CNC machines generate "
     "rich time-series data — but it sits in historians, disconnected from quality outcomes."),
    ("Reactive, Not Predictive", "Quality teams investigate after failures. No automated link between "
     "in-process sensor patterns and downstream defect types."),
    ("Slow, Expensive Solutions", "Traditional consulting engagements take 6-12 months and $200K+. "
     "Platform vendors (Sight Machine, PTC) lock you into expensive annual contracts."),
]
for i, (title, body) in enumerate(problems):
    top = Inches(1.75) + i * Inches(1.3)
    # number chip
    d.rect(s, d.M, top, Inches(0.5), Inches(0.5), b.NAVY, radius=0.1)
    d.text(s, str(i + 1), d.M + Inches(0.05), top + Inches(0.02), Inches(0.4), Inches(0.45),
           size=18, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, title, Inches(1.3), top, Inches(3.5), Inches(0.4),
           size=16, color=b.NAVY, bold=True)
    d.text(s, body, Inches(1.3), top + Inches(0.42), Inches(11), Inches(0.7),
           size=12, color=b.INK, shrink=True)
d.footer(s, 3, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S4 — SOLUTION OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Predict Defects Mid-Line Using Existing Sensor Infrastructure",
         "Sensor-to-SAP predictive quality pipeline")

# data flow boxes
steps = [
    ("Sensors\n& PLCs", b.NAVY_2, b.WHITE),
    ("OPC-UA /\nMQTT", b.NAVY_2, b.WHITE),
    ("Historian\n(InfluxDB/MII)", b.ACCENT, b.WHITE),
    ("Feature\nEngineering", b.TEAL, b.WHITE),
    ("XGBoost\nModel", b.TEAL, b.WHITE),
    ("SHAP\nExplainability", b.GOLD, b.NAVY),
    ("SAP PM\nNotification", b.CORAL, b.WHITE),
]
box_w = Inches(1.5)
gap = Inches(0.18)
total_w = len(steps) * box_w + (len(steps) - 1) * gap
start_x = int((d.W - total_w) / 2)
arrow_y = Inches(2.8)
for i, (label, fill, tc) in enumerate(steps):
    x = start_x + i * (box_w + gap)
    d.rect(s, x, Inches(1.95), box_w, Inches(1.1), fill, radius=0.06, shadow=True)
    d.text(s, label, x + Inches(0.08), Inches(2.0), box_w - Inches(0.16), Inches(1.0),
           size=11, color=tc, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
           shrink=True)
    if i < len(steps) - 1:
        ax = x + box_w + Inches(0.02)
        d.text(s, "→", ax, Inches(2.25), gap - Inches(0.04), Inches(0.5),
               size=18, color=b.MUTED, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# key points below
points = [
    "Tap the historian layer — never touch PLCs (plant safety preserved)",
    "Sensor traces featurized: mean, std, skew, kurtosis, FFT peaks, rate-of-change",
    "Labels from SAP QM inspection results (pass/fail/defect-type per part)",
    "Model outputs defect probability per part per station — threshold tuned to cost tradeoff",
    "SAP PM notification auto-created when model flags a part or detects process drift",
]
for i, pt in enumerate(points):
    d.text(s, [{"text": pt, "bullet": True, "space_before": 6, "size": 13}],
           Inches(1.2), Inches(3.4) + i * Inches(0.55), Inches(10.8), Inches(0.5),
           shrink=True)
d.footer(s, 4, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S5 — ML PIPELINE ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "XGBoost Baseline Delivers Fast ROI — Deep Learning Upgrade Path Ready",
         "ML pipeline architecture")

# two columns
col_left = d.M
col_right = Inches(7.0)
col_w2 = Inches(5.5)

# left: baseline
d.rect(s, col_left, Inches(1.7), Inches(5.8), Inches(0.5), b.TEAL, radius=0.03)
d.text(s, "BASELINE: XGBoost on Tabular Features", col_left + Inches(0.2), Inches(1.73),
       Inches(5.4), Inches(0.45), size=14, color=b.WHITE, bold=True,
       anchor=MSO_ANCHOR.MIDDLE)

baseline = [
    "Statistical summaries per sensor trace (mean, std, skew, kurtosis)",
    "Frequency-domain features (FFT peaks, dominant frequencies)",
    "Rate-of-change and trend features",
    "Fast to train, interpretable, good enough for pilot validation",
    "SHAP values show which signals drive each prediction",
]
for i, item in enumerate(baseline):
    d.text(s, [{"text": item, "bullet": True, "space_before": 6, "size": 12}],
           col_left + Inches(0.2), Inches(2.35) + i * Inches(0.5),
           Inches(5.4), Inches(0.45), shrink=True)

# right: upgrade
d.rect(s, col_right, Inches(1.7), col_w2, Inches(0.5), b.GOLD, radius=0.03)
d.text(s, "UPGRADE: LSTM / 1D-CNN on Raw Traces", col_right + Inches(0.2), Inches(1.73),
       Inches(5.1), Inches(0.45), size=14, color=b.NAVY, bold=True,
       anchor=MSO_ANCHOR.MIDDLE)

upgrade = [
    "Learns temporal patterns directly from raw sensor waveforms",
    "Higher accuracy on complex, multi-signal defect modes",
    "Requires larger training dataset (6+ months of labeled data)",
    "Justified once baseline proves value and data volume grows",
]
for i, item in enumerate(upgrade):
    d.text(s, [{"text": item, "bullet": True, "space_before": 6, "size": 12}],
           col_right + Inches(0.2), Inches(2.35) + i * Inches(0.5),
           Inches(5.1), Inches(0.45), shrink=True)

# sensor types row
d.rect(s, d.M, Inches(5.2), d.CW, Inches(0.06), b.GRID)
d.text(s, "SENSOR COVERAGE", d.M, Inches(5.4), Inches(3), Inches(0.35),
       size=11, color=b.MUTED, bold=True)
sensors = ["Welding: current, voltage,\nwire feed, gas flow",
           "Torque: angle curves,\ntorque profiles",
           "Paint: thickness, temp,\nhumidity",
           "CNC/Press: vibration,\nforce, position"]
sw = Inches(2.8)
for i, sensor in enumerate(sensors):
    sx = d.M + i * (sw + Inches(0.2))
    d.rect(s, sx, Inches(5.75), sw, Inches(0.95), b.SOFT, radius=0.04)
    d.text(s, sensor, sx + Inches(0.15), Inches(5.8), sw - Inches(0.3), Inches(0.85),
           size=11, color=b.INK, shrink=True, anchor=MSO_ANCHOR.MIDDLE,
           align=PP_ALIGN.CENTER)
d.footer(s, 5, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S6 — OPENHANDS AGENT STACK
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "OpenHands Cuts Delivery By 50% — AI Generates The Pipeline Code",
         "AI engineering accelerator, not runtime inference")

agents = [
    ("Sensor-Fusion Agent", "Generates data ingestion code:\nOPC-UA/MQTT connectors, historian\nqueries, part-ID correlation", b.TEAL),
    ("Feature-Engineering Agent", "Generates featurization pipelines\nfrom sensor schema: statistical,\nfrequency-domain, rate-of-change", b.TEAL),
    ("Model-Training Agent", "Scaffolds training notebooks,\nhyperparameter sweeps, MLflow\nexperiment tracking", b.ACCENT),
    ("Explainability Agent", "Generates SHAP/LIME dashboards\nshowing which sensor signals drove\neach prediction", b.GOLD),
    ("SAP-PM Agent", "Generates MCP connectors for\nSAP QM (read) and SAP PM (write)\nvia OData APIs", b.CORAL),
]
card_w = Inches(2.2)
card_h = Inches(2.8)
total_cw = len(agents) * card_w + (len(agents) - 1) * Inches(0.2)
cx = int((d.W - total_cw) / 2)
for i, (name, desc, color) in enumerate(agents):
    left = cx + i * (card_w + Inches(0.2))
    d.rect(s, left, Inches(1.8), card_w, card_h, b.SOFT, radius=0.05, shadow=True)
    # color top bar
    d.rect(s, left, Inches(1.8), card_w, Inches(0.08), color)
    d.text(s, name, left + Inches(0.15), Inches(2.05), card_w - Inches(0.3), Inches(0.7),
           size=12, color=b.NAVY, bold=True, shrink=True)
    d.text(s, desc, left + Inches(0.15), Inches(2.75), card_w - Inches(0.3), Inches(1.6),
           size=10.5, color=b.INK, shrink=True)

# stat bar
d.rect(s, d.M, Inches(5.0), d.CW, Inches(0.65), b.NAVY, radius=0.03)
stats = [("~60%", "boilerplate code\nauto-generated"), ("8-12 → 4 wks", "delivery\nacceleration"),
         ("Human Focus", "feature selection, model\ntuning, domain validation")]
sw2 = Inches(3.5)
for i, (num, label) in enumerate(stats):
    sx2 = d.M + Inches(0.3) + i * (sw2 + Inches(0.3))
    d.text(s, num, sx2, Inches(5.05), Inches(1.4), Inches(0.55),
           size=20, color=b.GOLD, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, label, sx2 + Inches(1.45), Inches(5.05), Inches(1.8), Inches(0.55),
           size=10, color=b.WHITE, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

d.text(s, "OpenHands is the delivery accelerator — the human ML engineer makes the critical decisions.",
       d.M, Inches(5.9), d.CW, Inches(0.4), size=12, color=b.MUTED, italic=True,
       align=PP_ALIGN.CENTER)
d.footer(s, 6, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S7 — SAP INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Deep SAP Integration Via OData — No Joule, No Lock-In",
         "Three SAP touchpoints for a closed-loop quality system")

sap_modules = [
    ("SAP QM", "READ", "Inspection lots + results (pass/fail/defect-code per part). "
     "Training label source.\nOData: API_INSPECTIONLOT_SRV or custom CDS view.", b.TEAL),
    ("SAP PM", "WRITE", "Quality notifications when model flags a part. "
     "Triggers maintenance workflow on process drift.\nOData: API_MAINTNOTIFICATION_SRV.", b.GOLD),
    ("SAP MII/ME", "CONTEXT", "Real-time production order context — which part is at which station. "
     "Improves part-ID correlation.\nOptional but valuable.", b.ACCENT),
]
for i, (module, rw, desc, color) in enumerate(sap_modules):
    top = Inches(1.75) + i * Inches(1.55)
    # left badge
    d.rect(s, d.M, top, Inches(1.6), Inches(1.25), color, radius=0.05)
    d.text(s, module, d.M + Inches(0.1), top + Inches(0.15), Inches(1.4), Inches(0.5),
           size=16, color=b.WHITE, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, rw, d.M + Inches(0.1), top + Inches(0.7), Inches(1.4), Inches(0.4),
           size=11, color=b.WHITE, align=PP_ALIGN.CENTER, bold=True)
    # description
    d.text(s, desc, Inches(2.5), top + Inches(0.1), Inches(9.5), Inches(1.1),
           size=12.5, color=b.INK, shrink=True)

# integration stack bar
d.rect(s, d.M, Inches(6.0), d.CW, Inches(0.7), b.NAVY, radius=0.03)
d.text(s, "INTEGRATION STACK:  Gemini + ADK + MCP → SAP OData     |     No Joule  ·  No RFC/BAPI  ·  No Vendor Lock-In",
       Inches(0.85), Inches(6.03), Inches(11.5), Inches(0.64),
       size=14, color=b.TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.footer(s, 7, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S8 — EXPLAINABILITY DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Quality Engineers See Why — Not Just What — The Model Predicts",
         "Generative UI dashboard with SHAP explainability + natural-language queries")

views = [
    ("Real-Time Alert View", "Parts flagged as high defect probability, ranked by confidence. "
     "Top 3 contributing sensor signals highlighted per part (e.g., 'welding current spike "
     "at station 4 contributed 62%'). SHAP waterfall charts.", b.CORAL),
    ("Process Drift View", "Time-series trends of key process parameters with control limits. "
     "Shows when a parameter is drifting toward out-of-spec before crossing threshold. "
     "SPC charts enhanced with ML-detected anomalies.", b.GOLD),
    ("Root-Cause Analysis", "For a selected defect type, shows which sensor signals and stations "
     "are most correlated. Helps quality engineers investigate systemic issues, not just "
     "individual parts.", b.TEAL),
]
for i, (title, desc, color) in enumerate(views):
    top = Inches(1.75) + i * Inches(1.45)
    d.rect(s, d.M, top, d.CW, Inches(1.2), b.SOFT, radius=0.05)
    d.rect(s, d.M, top, Inches(0.08), Inches(1.2), color)
    d.text(s, title, Inches(0.9), top + Inches(0.08), Inches(4), Inches(0.4),
           size=15, color=b.NAVY, bold=True)
    d.text(s, desc, Inches(0.9), top + Inches(0.48), Inches(11.2), Inches(0.65),
           size=12, color=b.INK, shrink=True)

# tech stack note
d.rect(s, d.M, Inches(6.25), d.CW, Inches(0.5), b.NAVY, radius=0.03)
d.text(s, 'Built with ADK + AG-UI (CopilotKit frontend, Gemini backend)  ·  Ask: "Why did station 4 flag 12 parts today?"',
       Inches(0.85), Inches(6.28), Inches(11.5), Inches(0.44),
       size=12.5, color=b.WHITE, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.footer(s, 8, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S9 — 4-WEEK DELIVERY TIMELINE
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "From Data to Validated Model in 4 Weeks — Not 4 Months",
         "Aggressive but proven single-station pilot timeline")

weeks = [
    ("WEEK 1", "Data Discovery\n& Connectivity",
     "Connect to historian\nPull sensor data\nValidate part-ID correlation\nPull SAP QM results",
     "Data quality report\n+ feature schema", b.TEAL),
    ("WEEK 2", "Feature Engineering\n& Baseline Model",
     "Build feature pipelines\nTrain XGBoost baseline\nValidate vs. historical defects",
     "Model accuracy metrics\n+ SHAP analysis", b.ACCENT),
    ("WEEK 3", "Dashboard &\nSAP Integration",
     "Build explainability dashboard\nConnect SAP QM read\nConnect SAP PM write",
     "Working dashboard\nwith live data", b.GOLD),
    ("WEEK 4", "Validation\n& Handoff",
     "Shadow mode alongside inspection\nMeasure precision/recall\nTune threshold",
     "Pilot results report\n+ scale-up proposal", b.CORAL),
]
cw3 = Inches(2.8)
gap3 = Inches(0.22)
for i, (wk, title, tasks, deliverable, color) in enumerate(weeks):
    left = d.M + i * (cw3 + gap3)
    d.rect(s, left, Inches(1.75), cw3, Inches(4.5), b.SOFT, radius=0.05, shadow=True)
    d.rect(s, left, Inches(1.75), cw3, Inches(0.55), color, radius=0.05)
    d.text(s, wk, left + Inches(0.15), Inches(1.8), cw3 - Inches(0.3), Inches(0.45),
           size=14, color=b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, title, left + Inches(0.15), Inches(2.4), cw3 - Inches(0.3), Inches(0.65),
           size=13, color=b.NAVY, bold=True, shrink=True)
    d.text(s, tasks, left + Inches(0.15), Inches(3.15), cw3 - Inches(0.3), Inches(1.6),
           size=11, color=b.INK, shrink=True)
    # deliverable
    d.rect(s, left + Inches(0.1), Inches(5.0), cw3 - Inches(0.2), Inches(0.95),
           b.NAVY, radius=0.04)
    d.text(s, "DELIVERABLE", left + Inches(0.2), Inches(5.0), cw3 - Inches(0.4), Inches(0.3),
           size=8, color=b.TEAL, bold=True)
    d.text(s, deliverable, left + Inches(0.2), Inches(5.3), cw3 - Inches(0.4), Inches(0.6),
           size=10, color=b.WHITE, shrink=True)

# comparison note
d.text(s, "Traditional consulting: 8-12 weeks, $120K-180K  →  Our pilot: 4 weeks, $40-60K",
       d.M, Inches(6.55), d.CW, Inches(0.4), size=14, color=b.NAVY, bold=True,
       align=PP_ALIGN.CENTER)
d.footer(s, 9, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S10 — PRICING & VALUE
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "50-70% Cheaper and 3x Faster Than Traditional Alternatives",
         "Investment summary with clear expansion path")

# KPI boxes
kpis = [
    ("$40-60K", "Pilot\n(4 weeks, single station)", b.TEAL),
    ("$8-12K/mo", "Retainer\n(monitoring + support)", b.GOLD),
    ("~$20K", "Per Additional Line\n(mostly configuration)", b.ACCENT),
]
kw = Inches(3.6)
for i, (num, label, color) in enumerate(kpis):
    left = d.M + i * (kw + Inches(0.3))
    d.rect(s, left, Inches(1.75), kw, Inches(1.8), b.NAVY, radius=0.05, shadow=True)
    d.text(s, num, left + Inches(0.2), Inches(1.9), kw - Inches(0.4), Inches(0.8),
           size=36, color=color, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    d.text(s, label, left + Inches(0.2), Inches(2.7), kw - Inches(0.4), Inches(0.7),
           size=13, color=b.WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

# value anchoring
d.text(s, "VALUE ANCHORING", d.M, Inches(3.9), Inches(3), Inches(0.35),
       size=12, color=b.MUTED, bold=True)

anchors = [
    "Traditional consulting (Accenture, McKinsey): $200K-400K+ over 6+ months",
    "SaaS platforms (Sight Machine, Uptake): $100K+ annual license, long implementation",
    "Our pilot: working prototype in 4 weeks, not a strategy deck in 6 months",
    "Multi-plant deployment is the scale play — each new plant builds on proven models",
]
for i, item in enumerate(anchors):
    d.text(s, [{"text": item, "bullet": True, "space_before": 8, "size": 13}],
           d.M + Inches(0.2), Inches(4.3) + i * Inches(0.55), Inches(11), Inches(0.5),
           shrink=True)
d.footer(s, 10, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S11 — COMPETITIVE DIFFERENTIATION
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "We Win on Speed, Cost, and Openness — Not Vendor Lock-In",
         "Competitive positioning")

# comparison table
competitors = [
    ("", "Us", "Sight Machine", "Accenture/\nMcKinsey", "PTC ThingWorx/\nSiemens"),
    ("Timeline", "4 weeks", "3-6 months", "6-12 months", "6+ months"),
    ("Cost", "$40-60K pilot", "$100K+ annual", "$200K-400K+", "Complex\nlicensing"),
    ("Deliverable", "Working\nprototype", "SaaS platform\naccess", "Strategy deck\n+ build", "IoT platform\n+ ML add-on"),
    ("Lock-in", "Open-source\nstack", "Proprietary\nplatform", "Consulting\ndependency", "Vendor\nplatform"),
    ("Explainability", "SHAP-first\ndashboard", "Platform\nanalytics", "Custom\nbuild", "Limited\nbuilt-in"),
]
col_w4 = Inches(2.3)
row_h = Inches(0.85)
label_w = Inches(1.9)
for r, row in enumerate(competitors):
    top = Inches(1.75) + r * row_h
    for c, cell in enumerate(row):
        if c == 0:
            left = d.M
            w = label_w
            fc = b.MUTED if r > 0 else b.NAVY
            bg = b.WHITE
            bld = r == 0
        else:
            left = d.M + label_w + Inches(0.1) + (c - 1) * (col_w4 + Inches(0.1))
            w = col_w4
            if r == 0:
                bg = b.TEAL if c == 1 else b.NAVY
                fc = b.WHITE
                bld = True
            else:
                bg = b.LIGHT_TEAL if c == 1 else b.SOFT
                fc = b.INK
                bld = c == 1
        if r > 0 or c > 0:
            d.rect(s, left, top, w, row_h - Inches(0.06), bg, radius=0.03)
        d.text(s, cell, left + Inches(0.1), top + Inches(0.04), w - Inches(0.2),
               row_h - Inches(0.14), size=11, color=fc, bold=bld,
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shrink=True)
d.footer(s, 11, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# S12 — RISK MITIGATION & NEXT STEPS
# ═══════════════════════════════════════════════════════════════════════════════
s = d.slide(fill=b.WHITE)
d.header(s, "Every Major Risk Has a Built-In Mitigation — Week 1 Is the Gate",
         "Risk management and proposed next steps")

risks = [
    ("Data Quality", "Week 1 data discovery gate — if data is unusable, pivot or exit before model-build spend", b.CORAL),
    ("IT/OT Access", "Historian read-only (no PLC writes). Architecture review with OT team in Week 0 pre-kick", b.GOLD),
    ("Label Quality", "Focus on objective defect types first (dimensional, torque) — not subjective (cosmetic)", b.AMBER),
    ("Model Accuracy", "Week 4 shadow mode validates before any process changes. Data infra + dashboard have standalone value", b.ACCENT),
    ("Change Mgmt", "Explainability dashboard is the trust-building mechanism. Start advisory, not automatic", b.TEAL),
]
for i, (risk, mitigation, color) in enumerate(risks):
    top = Inches(1.7) + i * Inches(0.88)
    d.rect(s, d.M, top, Inches(2.0), Inches(0.7), color, radius=0.04)
    d.text(s, risk, d.M + Inches(0.12), top + Inches(0.02), Inches(1.76), Inches(0.66),
           size=12, color=b.WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER,
           shrink=True)
    d.text(s, mitigation, Inches(2.85), top + Inches(0.05), Inches(9.5), Inches(0.6),
           size=12, color=b.INK, anchor=MSO_ANCHOR.MIDDLE, shrink=True)

# next steps
d.rect(s, d.M, Inches(6.1), d.CW, Inches(1.05), b.NAVY, radius=0.04)
d.text(s, "NEXT STEPS", d.M + Inches(0.25), Inches(6.15), Inches(2), Inches(0.3),
       size=11, color=b.TEAL, bold=True)
next_steps = [
    "1. Technical discovery call: confirm historian platform, SAP version, OData availability",
    "2. Week 0 pre-kick: OT architecture review, data access provisioning, inspection data sample",
    "3. Pilot kickoff: 4-week sprint on a single station (welding or torque recommended)",
]
for i, step in enumerate(next_steps):
    d.text(s, step, d.M + Inches(0.25), Inches(6.45) + i * Inches(0.22),
           Inches(11.5), Inches(0.22), size=11, color=b.WHITE, shrink=True)
d.footer(s, 12, TOTAL)

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
out = d.save("docs/reports/hyundai-predictive-quality-uc05.pptx")
print(f"\nDeck ready: {out}")
