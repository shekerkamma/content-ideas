#!/usr/bin/env python3
"""
Full Pipeline Pre-Sales Deck v2 — Client-Ready Enriched Edition
Data: GBrain + Exa + Web Research + Implementation Specs + Vertical Scorer + GitHub Repos
Layout: Canva-Pro realization template via pptxkit

Enrichments over v1:
  - BMW AIQX, Walmart Wally, Mastercard, Harvey AI, Bosch, C.H. Robinson production data
  - 12 slides per UC (added ROI Summary + Market Benchmark)
  - Cross-industry market context slides
  - Next Steps / Engagement Model
  - Full source appendix

Structure per UC (12 slides):
  1. UC Title/Overview
  2. Challenge (full-page detail)
  3. Solution Realization
  4. KPI / Stats Dashboard
  5. How-It-Works Flow
  6. Architecture Deep-Dive (agents + MCP)
  7. Tech Stack & GitHub Repos
  8. Governance & Compliance
  9. Competitive Landscape
  10. Insight + Buyer Profile + Revenue
  11. ROI Summary (executive view)
  12. Market Benchmark (cross-industry context)
"""

import sys
from pathlib import Path

PPTXKIT_DIR = Path.home() / ".claude" / "skills" / "branded-pptx-deck" / "scripts"
sys.path.insert(0, str(PPTXKIT_DIR))

from pptxkit import Brand, Deck, PP_ALIGN, MSO_ANCHOR, Inches, Pt, Emu, hx

d = Deck(footer="{{brand_name}} · AI Use Cases — Full Pipeline | 2026")
b = d.b

PAGE = [0]  # mutable counter


def next_page():
    PAGE[0] += 1
    return PAGE[0]


# ═══════════════════════════════════════════════════════════════
# USE CASE DATA — each UC is a comprehensive dict
# ═══════════════════════════════════════════════════════════════

USE_CASES = [
    # ─── UC-01: Manufacturing PdM ─────────────────────────
    {
        "id": "UC-01", "industry": "Manufacturing",
        "title": "Predictive Maintenance — Sensor to Anomaly to Work Order",
        "subtitle": "Unilever Indaiatuba: $2.3M saved, 92% accuracy, 6.5-month payback",
        "company": "Unilever (Brazil)",
        "deployed": "2023, expanded to 7+ sites by Q4 2025",
        "challenge_headline": "Equipment Downtime Costs $50K-$250K/Hour",
        "challenges": [
            "Equipment downtime costs $50K-$250K/hour in manufacturing plants",
            "Calendar-based maintenance wastes 30%+ of budget on unnecessary interventions",
            "Unilever baseline: 8.2% unplanned downtime, $5.1M annual maintenance spend",
            "Technician trust in AI predictions is the real deployment barrier — not model accuracy",
            "50,000+ IoT sensors generating time-series data across compressors, HVAC, packaging",
            "3 years of historical failure data needed before any model could train",
        ],
        "solution_headline": "52-Endpoint MCP Server + SAP PM Integration",
        "solutions": [
            "50K+ IoT sensors -> anomaly detection 14-28 days before failure at 92% accuracy",
            "52-endpoint MCP server: FFT, envelope analysis, RUL estimation (ISO 13374)",
            "Auto-generates SAP PM work orders with equipment ID, failure type, predicted date",
            "6-month trust-building phase with technician feedback loops before full reliance",
            "Started with 12 machines causing 80% of downtime — focused deployment",
            "Amazon SageMaker processes time-series data; ONNX Runtime for edge inference",
        ],
        "stats": [
            ("$2.3M", "Annual Savings", "45% reduction from $5.1M baseline"),
            ("92%", "Detection Accuracy", "14-28 days before predicted failure"),
            ("52", "MCP Endpoints", "ISO 13374 six-block diagnostic architecture"),
            ("6.5 mo", "Payback Period", "$1.2M investment recovered"),
            ("40%", "Downtime Reduction", "8.2% -> 4.9% unplanned downtime"),
            ("85%+", "OEE Achieved", "Highest in Unilever global network, 2 consecutive years"),
        ],
        "how_it_works": [
            "Sensor reading arrives (MQTT/OPC-UA) -> load_signal + analyze_spectrum + extract_features",
            "detect_anomalies (semi-supervised, trained on 3yr normal baseline) -> anomaly_score",
            "IF anomaly_score > threshold -> analyze_envelope (bearing-specific: BPFO/BPFI/BSF/FTF)",
            "assess_severity (ISO 20816-3 zone A/B/C/D) -> estimate_rul (linear/exponential/Weibull)",
            "IF severity >= Zone C OR rul_days < 14 -> generate_report -> create_work_order (SAP PM via OData)",
            "Work order includes: equipment_id, failure_type, predicted_date, priority, recommended_ops",
            "Technician completes -> feedback loop -> model retraining on actual vs predicted",
        ],
        "agents": [
            ("sensor-fusion-agent", "Ingests multi-signal data (vibration, temp, pressure) from MQTT/OPC-UA gateway"),
            ("anomaly-detection-agent", "ML inference (XGBoost + LSTM) + ISO 20816-3 severity classification (Zone A/B/C/D)"),
            ("explainability-agent", "SHAP-based root-cause analysis -> human-readable failure narratives for technicians"),
            ("sap-pm-agent", "Creates SAP PM work orders via OData: equipment_id, order_type, priority, operations"),
        ],
        "mcp_servers": [
            ("predictive-maintenance-mcp", "52 endpoints", "load_signal, analyze_spectrum, extract_features, detect_anomalies, analyze_envelope, assess_severity, estimate_rul, generate_report"),
            ("sap-maintenance (CAP)", "4 endpoints", "get_maintenance_orders, create_work_order, get_equipment_history, get_maintenance_order_detail"),
            ("machina-cmms", "Alternative", "machina-ai package with SapPM connector (pip install machina-ai[sap])"),
        ],
        "github_repos": [
            ("LGDiMaggio/predictive-maintenance-mcp", "v0.8.0 -- 52 endpoints, Claude Code plugin, ISO 13374 six-block diagnostic"),
            ("bernardcaldas/mcp-maintenance-cap", "PoC -- SAP CAP + OData + Claude Desktop integration for PM work orders"),
            ("machina-ai (PyPI)", "v0.1 Pre-Alpha -- SAP PM connector, ISO 14224 equipment domain model"),
            ("All-Hands-AI/OpenHands", "Agent SDK -- headless mode for batch sensor analysis + MCP config"),
            ("huggingface/transformers", "Time-series models + anomaly detection architectures"),
        ],
        "stack": [
            ("MCP: PdM", "predictive-maintenance-mcp -- 52 endpoints, ISO 13374"),
            ("MCP: SAP PM", "mcp-maintenance-cap -- OData: create_work_order, get_equipment_history"),
            ("ML", "XGBoost + LSTM ensemble -- SHAP explainability -- ONNX Runtime edge"),
            ("Deploy", "OpenHands headless batch + interactive CLI -- Edge: Jetson/ONNX"),
        ],
        "governance": [
            "ISO 13374 six-block diagnostic architecture (acquisition -> processing -> detection -> severity -> prognostics -> decision)",
            "ISO 20816-3 vibration severity classification (Zone A/B/C/D thresholds)",
            "Sensor calibration audit per ISO 6789 -- annual recertification required",
            "Model drift monitoring: weekly accuracy check against actuals",
            "Technician override logging: all manual overrides of AI predictions tracked",
        ],
        "competitive": [
            ("Siemens Senseye", "Cloud PdM SaaS", "Cloud-based, AI-powered PdM -- market leader, $2.61B market (2026). No SAP integration out-of-box"),
            ("Bosch AI Platform", "50 plants, 2K+ lines", "Zero-defect production across 50 plants. Opening platform to 3rd parties since CES 2026"),
            ("GE Vernova SmartSignal", "Enterprise APM", "Predictive analytics for power/industrial -- strong in energy, limited manufacturing MCP"),
            ("McKinsey QuantumBlack", "$400K+, 6+ months", "Consulting-led, high-touch, slow to production"),
            ("Our approach", "4 weeks, 50-70% cheaper", "Open-source MCP, pilot-first, technician trust-building baked in"),
        ],
        "insight": "3 years of labeled failure data eliminated the data-collection phase that kills most manufacturing AI. Started with 12 machines causing 80% of downtime. The model was technically ready before the humans were. Trust took 6 months to build. That's the actual timeline. Budget for trust, not just training.",
        "buyer": "VP Manufacturing / Plant Manager",
        "revenue": "$5-10K/mo per plant",
        "systems": ["SCADA/OPC-UA", "SAP PM", "IoT Gateway", "CMMS", "Historian"],
        "users": "Maintenance technicians | Plant engineers | Reliability managers",
        "source": "NSSG Insights Mar 2026 + GBrain impl spec + Unilever case study",
        "deployment": "Headless batch: sensor analysis + work orders | Interactive: operator CLI queries",
        "vertical_score": "32/35 GO",
        "roi_summary": {
            "investment": "$1.2M (sensors + ML + integration)",
            "annual_return": "$2.3M savings (45% maintenance cost reduction)",
            "payback": "6.5 months",
            "three_year_roi": "475%",
            "intangibles": "OEE 72% -> 85%+, technician upskilling, safety improvement",
        },
        "market_benchmark": {
            "market_size": "AI PdM market: $2.61B (2026) -> $19.27B (2032), 39.5% CAGR",
            "peer_comparison": "Siemens Senseye (cloud PdM leader) | Bosch: 50 plants, 2K+ lines | ENGIE: 1,000+ models, EUR 800K/yr/BU saved",
            "differentiator": "Open-source MCP vs proprietary SaaS -- 50-70% cheaper, 4-week deploy vs 6+ months",
            "source": "MarketsAndMarkets 2026 + Siemens Blog Dec 2025 + Bosch CES 2026",
        },
    },
    # ─── UC-02: Manufacturing Visual QI ─────────────────────
    {
        "id": "UC-02", "industry": "Manufacturing",
        "title": "Visual Quality Inspection -- Camera to CNN to SAP MES",
        "subtitle": "YOLOv8 at line speed: 99.2% accuracy, 85% false positive reduction",
        "company": "Hyundai Framework + Multi-Plant",
        "deployed": "Reference architecture, 4-6 week deployment",
        "challenge_headline": "Manual Inspection Fails at Scale",
        "challenges": [
            "15-20% false positive rate in manual inspection across production lines",
            "Inspector fatigue: accuracy drops to 72% by hour 6 of shift",
            "$2.3M average annual quality cost per plant from missed defects",
            "Inconsistent criteria across shifts -- 3 inspectors, 3 different standards",
            "Generic CV doesn't understand defect taxonomy per manufacturing context",
            "Edge inference latency must be <5ms to keep up with line speed (120 units/hr)",
        ],
        "solution_headline": "Edge AI + Active Learning + SAP MES Integration",
        "solutions": [
            "YOLOv8 real-time defect detection: 640x640 input, 1.2ms edge inference on Jetson Orin",
            "Multi-camera 360 deg inspection at line speed (120 units/hr) -- no throughput reduction",
            "Three-tier confidence routing: >0.85 auto-reject; 0.5-0.85 operator review; <0.5 passes",
            "Active learning pipeline: operator corrections feed continuous model retraining",
            "Defect taxonomy: surface (scratch/dent/pit/crack), dimensional, contamination, assembly",
            "Per-shift quality reports auto-generated with SPC dashboard + Cpk monitoring",
        ],
        "stats": [
            ("99.2%", "Detection Accuracy", "Across all defect categories"),
            ("85%", "FP Reduction", "From 15-20% manual FP rate"),
            ("$1.8M", "Annual Savings", "Per plant from reduced quality costs"),
            ("<2ms", "Inference Time", "YOLOv8 on Jetson Orin NX edge GPU"),
            ("4-6 wk", "Deployment", "Camera install to model trained to production"),
            ("120/hr", "Line Speed", "No throughput reduction from inspection"),
        ],
        "how_it_works": [
            "GigE Vision camera captures part at inspection station -> Image preprocessing (normalize, resize 640x640)",
            "Jetson Orin NX runs YOLOv8 inference (<2ms) -> Defect classification: scratch, dent, weld, paint, contamination",
            "Bounding box + confidence score + defect type -> Three-tier routing decision",
            "IF confidence > 0.85 AND defect: auto-reject -> log_inspection_result (SAP MES) -> catalog image (MinIO + metadata)",
            "IF 0.5-0.85: operator review with AI suggestion -> operator decision feeds active learning pipeline",
            "Per-shift aggregate -> generate_quality_report -> SPC dashboard (Cpk monitoring) -> root-cause analysis",
            "Continuous: new labeled defects feed model retraining -> OTA model update to edge devices",
        ],
        "agents": [
            ("vision-capture-agent", "GigE Vision camera control, image preprocessing, multi-camera synchronization"),
            ("inference-agent", "YOLOv8 / EfficientDet CNN -> defect classification with confidence scores"),
            ("quality-routing-agent", "Routes by confidence threshold: auto-reject, human review, or pass"),
            ("sap-mes-agent", "Logs results to SAP MES, creates quality notifications, updates production orders"),
        ],
        "mcp_servers": [
            ("vision-pipeline MCP", "5 endpoints", "capture_image, run_inference, classify_defect, get_defect_history, generate_quality_report"),
            ("sap-mes MCP (OData)", "4 endpoints", "log_inspection_result, get_production_order, update_quality_status, create_quality_notification"),
        ],
        "github_repos": [
            ("ultralytics/ultralytics", "YOLOv8 -- real-time detection, ONNX/TensorRT export, COCO pretrained"),
            ("opencv/opencv", "Camera capture, preprocessing, GigE Vision support, image pipeline"),
            ("NVIDIA/TensorRT", "Edge inference optimization for Jetson Orin -- quantization, pruning"),
            ("minio/minio", "S3-compatible object storage for defect images with metadata tagging"),
            ("streamlit/streamlit", "Quality dashboard for shift reports and SPC visualization"),
        ],
        "stack": [
            ("EDGE", "GigE Vision cameras + Jetson Orin NX -- line-speed capture + inference"),
            ("AI", "YOLOv8 + EfficientNet ensemble -- ONNX Runtime -- active learning pipeline"),
            ("MCP: SAP MES", "log_inspection_result, create_quality_notification -- OData integration"),
            ("UX", "Defect heatmap dashboard + per-shift quality reports + SPC/Cpk monitoring"),
        ],
        "governance": [
            "IEC 62443 industrial cybersecurity for connected inspection stations",
            "Image retention: 7 years minimum, AES-256 encrypted storage (MinIO)",
            "Edge device certificate rotation every 90 days (automated via PKI)",
            "Model version tracking: every deployment logged with accuracy metrics",
            "Operator override audit trail: all manual decisions vs AI recommendations tracked",
        ],
        "competitive": [
            ("BMW AIQX", "All plants globally", "95-99% accuracy, 50% inspection time reduction, 60% defect reduction. Gold standard."),
            ("Instrumental", "YC W14, 80 employees", "SaaS visual inspection -- broad but less customizable"),
            ("Landing AI", "Andrew Ng", "Data-centric AI for manufacturing -- high-touch, expensive consulting"),
            ("Cognex", "Machine vision hardware", "Hardware-first, limited AI -- strong optics, weak intelligence"),
            ("Our approach", "Open-source stack", "YOLOv8 + active learning + SAP MES integration, 4-6 week deploy, 50-70% cheaper"),
        ],
        "insight": "Human inspectors get tired. The camera doesn't. But they kept humans for the 0.3% the camera wasn't sure about. Best of both. The active learning loop is the key -- every operator correction makes the model better. The human teaches the machine, then the machine frees the human.",
        "buyer": "VP Quality / Quality Manager",
        "revenue": "$5-10K/mo per plant",
        "systems": ["SAP MES", "GigE Vision", "Jetson Orin", "MinIO", "SPC Dashboard"],
        "users": "Quality engineers | Line supervisors | Plant managers",
        "source": "GBrain impl spec UC-MFG-02 + Hyundai framework + BMW AIQX (GreenData 2026)",
        "deployment": "Edge: Jetson Orin NX per inspection station | Line-speed 120 units/hr | Model updates via OTA | Shift reports at 07:00",
        "vertical_score": "32/35 GO",
        "roi_summary": {
            "investment": "$350K (cameras + edge + integration)",
            "annual_return": "$1.8M savings per plant (quality cost reduction)",
            "payback": "2.3 months",
            "three_year_roi": "1,443%",
            "intangibles": "Consistent quality 24/7, inspector redeployed to root-cause analysis",
        },
        "market_benchmark": {
            "market_size": "AI visual inspection market: $1.8B (2026), 23% CAGR through 2030",
            "peer_comparison": "BMW AIQX: all plants globally, 95-99% accuracy | Bosch: 50 plants, 2K+ lines, 15% takt reduction",
            "differentiator": "Open-source YOLOv8 + active learning vs proprietary BMW/Bosch platforms -- deployable in 4-6 weeks",
            "source": "BMW GreenData 2026 + Bosch CES 2026",
        },
    },
    # ─── UC-03: Healthcare Patient Intake ─────────────────────
    {
        "id": "UC-03", "industry": "Healthcare",
        "title": "Patient Intake Automation -- Form to EHR to Insurance to Booking",
        "subtitle": "3-agent pipeline: 80% staff time saved, <30 sec insurance verification",
        "company": "Reference Architecture (FHIR + Twilio + Calendly)",
        "deployed": "Implementation-ready, HIPAA-compliant",
        "challenge_headline": "40% of Staff Time Consumed by Paperwork",
        "challenges": [
            "Manual intake: 12-15 minutes per patient, 40% of staff time consumed by paperwork",
            "Insurance verification: 270/271 EDI calls take 3-8 minutes per patient manually",
            "No-show rate 18-25% due to lack of automated reminders and cost transparency",
            "HIPAA compliance burden: every PHI access must be logged and audited",
            "Fragmented workflow: EHR, insurance portal, scheduling tool, SMS -- all separate systems",
            "Prior authorization is bureaucratic, not clinical -- most requests meet standard criteria",
        ],
        "solution_headline": "3 Agents + 3 MCP Servers = End-to-End Automation",
        "solutions": [
            "3-agent pipeline: intake-agent -> insurance-verification-agent -> scheduling-agent",
            "FHIR R4 MCP server: create_patient, get_insurance_eligibility, submit_claim",
            "Automated SMS reminders via Twilio MCP: confirmation, cost estimate, 24h reminder",
            "OpenHands Docker sandbox isolates PHI -- never leaves infrastructure perimeter",
            "Confidence routing: standard cases automated, edge cases to nurse review",
            "Post-visit automation: update_patient + submit_claim (837 EDI) -- closes the loop",
        ],
        "stats": [
            ("80%", "Staff Time Saved", "Intake + verification + scheduling automated"),
            ("<30 sec", "Insurance Check", "vs 3-8 min manual 270/271 EDI"),
            ("40%", "No-Show Reduction", "SMS reminders + cost transparency"),
            ("HIPAA", "Compliant by Design", "AES-256, TLS 1.3, Docker sandbox, BAA"),
            ("3", "MCP Integrations", "FHIR R4 + Twilio + Calendly"),
            ("$3-5K/mo", "Revenue Per Practice", "Per-practice subscription model"),
        ],
        "how_it_works": [
            "Patient submits online intake form -> validate fields (name, DOB, SSN format, insurance ID)",
            "create_patient (FHIR R4) -> demographics + medical history stored in EHR",
            "get_insurance_eligibility (270/271 EDI) -> IF eligible: calculate copay/deductible",
            "send_sms via Twilio (appointment confirmation + cost estimate) -> patient transparency",
            "create_booking via Calendly (get_available_slots -> create_booking -> provider notified)",
            "24h before appointment: send_reminder -> reduces no-show rate by 40%",
            "Post-visit: update_patient (FHIR) + submit_claim (837 EDI) -> billing cycle automated",
        ],
        "agents": [
            ("intake-agent", "Validates form data, creates FHIR patient resource, populates demographics + medical history"),
            ("insurance-verification-agent", "270/271 EDI eligibility check -> copay/deductible calculation -> coverage confirmation"),
            ("scheduling-agent", "Calendly slot lookup -> booking creation -> SMS confirmation + cost estimate via Twilio"),
        ],
        "mcp_servers": [
            ("FHIR R4 MCP", "5 endpoints", "create_patient, update_patient, search_patient, get_insurance_eligibility, submit_claim"),
            ("Twilio MCP", "3 endpoints", "send_sms, send_reminder, get_message_status -- appointment confirmations + cost estimates"),
            ("Calendly MCP", "3 endpoints", "get_available_slots, create_booking, cancel_booking -- provider schedule integration"),
        ],
        "github_repos": [
            ("medplum/medplum", "Open-source FHIR server + EHR platform -- full HL7 compliance"),
            ("smart-on-fhir/client-js", "SMART on FHIR authorization + data access framework"),
            ("twilio/twilio-node", "Twilio SDK for SMS/voice communication"),
            ("microsoft/presidio", "PII detection + anonymization for HIPAA compliance"),
            ("All-Hands-AI/OpenHands", "Docker sandbox for PHI isolation + confirmation mode"),
        ],
        "stack": [
            ("MCP: FHIR", "HL7 FHIR R4 APIs -- create/search/update patient, eligibility, claims"),
            ("MCP: Twilio", "send_sms, send_reminder, get_message_status -- patient communication"),
            ("MCP: Calendly", "get_available_slots, create/cancel_booking -- provider scheduling"),
            ("Security", "AES-256 at rest, TLS 1.3 in transit, Docker sandbox, PHI isolation"),
        ],
        "governance": [
            "HIPAA: AES-256 encryption at rest, TLS 1.3 in transit for all PHI",
            "BAA (Business Associate Agreement) required with Twilio, Calendly, FHIR provider",
            "Minimum necessary principle: agents access only required PHI fields per operation",
            "Audit logging: every PHI access logged with timestamp, agent, operation, data accessed",
            "OpenHands Docker sandbox: PHI never leaves infrastructure perimeter",
        ],
        "competitive": [
            ("Phreesia", "$250M revenue", "Patient intake platform -- market leader but no AI agent orchestration"),
            ("Zocdoc", "Scheduling leader", "Scheduling but no insurance verification or EHR intake automation"),
            ("Notable Health", "AI intake", "AI-powered intake but no MCP integration or agent architecture"),
            ("Gap", "No integrated agent", "Nobody offers integrated intake + verify + schedule as an agent pipeline"),
            ("Our approach", "3 agents + 3 MCPs", "Full pipeline, HIPAA by design, $3-5K/mo per practice"),
        ],
        "insight": "Prior auth is bureaucratic, not clinical. Most requests meet criteria -- someone just needs to check the boxes. The AI checks the boxes. Edge cases still go to a nurse. The 270/271 EDI call is the perfect automation target -- deterministic, structured, zero clinical judgment required.",
        "buyer": "Practice Manager / VP Operations",
        "revenue": "$3-5K/mo per practice",
        "systems": ["EHR (FHIR)", "Insurance EDI", "Twilio", "Calendly"],
        "users": "Front desk staff | Practice managers | Billing coordinators",
        "source": "GBrain impl spec + AI Engineering Framework",
        "deployment": "Docker sandbox (PHI isolation) | BAA with all 3rd parties | Confirmation mode for edge cases | Headless for batch claims",
        "vertical_score": "Viable",
        "roi_summary": {
            "investment": "$80K (integration + compliance + BAA setup)",
            "annual_return": "$180K per practice (staff reallocation + no-show reduction)",
            "payback": "5.3 months",
            "three_year_roi": "575%",
            "intangibles": "Patient satisfaction, 40% no-show reduction, billing cycle acceleration",
        },
        "market_benchmark": {
            "market_size": "Healthcare AI market: $28B (2025) -> $150B+ (2030)",
            "peer_comparison": "Phreesia: $250M revenue, market leader | Notable Health: AI intake pioneer | Zocdoc: scheduling only",
            "differentiator": "Agent pipeline (intake+verify+schedule) vs single-function SaaS -- no competitor integrates all 3",
            "source": "Grand View Research 2025",
        },
    },
    # ─── UC-04: Healthcare Clinical AI ─────────────────────
    {
        "id": "UC-04", "industry": "Healthcare",
        "title": "Clinical AI -- Sepsis Detection + Care Gap Closure",
        "subtitle": "Tampa General: 700+ lives saved | CommonSpirit: 61K care gap orders",
        "company": "Tampa General Hospital + CommonSpirit Health",
        "deployed": "Production 2025 (both)",
        "challenge_headline": "Clinical Signals Missed at Scale",
        "challenges": [
            "Sepsis: early indicators missed in high-volume EDs -- catastrophic if delayed",
            "Tampa General needed real-time vitals monitoring + care coordination across units",
            "CommonSpirit: 140+ hospitals, screening compliance inconsistent across sites",
            "Manual risk stratification cannot scale across 200+ AI-assisted clinical workflows",
            "Outcome verification: need binary, measurable results to prove clinical AI works",
            "Physician adoption barrier: clinicians won't use tools that add clicks without clear value",
        ],
        "solution_headline": "Predictive ML Integrated into Clinical Workflow",
        "solutions": [
            "TGH + Palantir: AI-driven care coordination center integrates EHR signals in real-time",
            "Predictive ML detects sepsis indicators -> automated intervention triggers within treatment window",
            "Nebraska Medicine extension: 5% shorter stays = 37 additional beds without construction",
            "CSH: AI ingests EHR data -> calculates personalized cancer screening timelines automatically",
            "Clinical orders auto-recommended at point of care with clinician review step (not bypass)",
            "200+ AI tools active across 140+ hospital system -- platform approach, not one-off",
        ],
        "stats": [
            ("700+", "Lives Saved", "Tampa General -- sepsis detection program"),
            ("5%", "LOS Reduction", "Nebraska Medicine -- equivalent to 37 beds"),
            ("61K", "Care Gap Orders", "CommonSpirit FY2025 -- 5x YoY increase"),
            ("140+", "Hospitals", "CommonSpirit deployment scale"),
            ("200+", "AI Tools Active", "Across CommonSpirit health system"),
            ("37", "Virtual Beds", "Capacity gained without construction (Nebraska)"),
        ],
        "how_it_works": [
            "TGH: EHR vitals stream -> ML detects deterioration patterns -> alerts care team -> intervention within sepsis window",
            "Sepsis signals: vital sign trends (temp, HR, BP, WBC) -> predictive model -> early warning score",
            "Care coordination: discharge timing + bed allocation + intervention triggers -- unified view",
            "CSH: Patient EHR -> risk factor extraction -> screening timeline calculation (breast, colorectal, lung)",
            "Clinical order auto-recommended -> clinician reviews -> submits order -> care gap closed",
            "Platform scales across 140+ hospitals: same model, site-specific calibration",
        ],
        "agents": [
            ("vitals-monitoring-agent", "Real-time EHR vitals stream -> sepsis risk scoring -> early warning alerts"),
            ("care-coordination-agent", "Discharge timing + bed allocation + intervention triggers -> unified care view"),
            ("screening-agent", "Patient risk factors -> personalized cancer screening timelines -> order recommendation"),
        ],
        "mcp_servers": [
            ("Palantir Platform", "EHR integration", "Real-time clinical signals aggregation -> care coordination dashboard"),
            ("EHR Integration", "FHIR/HL7", "Bidirectional: read vitals, push orders, update patient records"),
        ],
        "github_repos": [
            ("medplum/medplum", "Open-source FHIR server for EHR integration patterns"),
            ("smart-on-fhir/client-js", "SMART on FHIR authorization for clinical data access"),
            ("All-Hands-AI/OpenHands", "Agent orchestration for clinical workflow automation"),
        ],
        "stack": [
            ("Platform", "Palantir (TGH) -- EHR integration, real-time clinical signals"),
            ("ML", "Predictive vitals + risk stratification -- sepsis early warning model"),
            ("Integration", "EHR-native -- order recommendation at point of care, zero friction"),
            ("Scale", "140+ hospitals, 200+ AI tools -- platform approach, not one-off (CSH)"),
        ],
        "governance": [
            "Clinical validation: sepsis model validated against known outcomes before deployment",
            "Clinician-in-the-loop: AI recommends, clinician reviews and submits -- no autonomous clinical decisions",
            "Regulatory: FDA guidance on Clinical Decision Support (CDS) -- non-device exemption pathway",
            "Patient safety: false positive rate monitored weekly -- alert fatigue is a real risk",
        ],
        "competitive": [
            ("Palantir Foundry", "TGH partner", "Care coordination platform -- strong but expensive, enterprise-only"),
            ("Epic Sepsis Model", "Built-in EHR", "High false positive rate historically -- improved in recent versions"),
            ("Viz.ai", "Stroke/PE detection", "Narrow use case -- strong for radiology, not general clinical AI"),
            ("Our positioning", "Agent architecture", "Composable agents that integrate with any EHR via FHIR -- not locked to one platform"),
        ],
        "insight": "Sepsis has a well-defined signal set, clear intervention window, and catastrophic downside of missing it. Outcome is binary and verifiable. That's why it worked. Find the binary outcomes first. Care gap closure is the same pattern -- screening criteria are deterministic, patient data is structured, the order is standardized. Automate the matching, not the medicine.",
        "buyer": "CMO / VP Clinical Operations",
        "revenue": "Enterprise (health system deployment)",
        "systems": ["EHR", "Vitals Monitoring", "Care Coordination", "CPOE"],
        "users": "ED clinicians | Care coordinators | Oncologists | Nursing staff",
        "source": "Becker's Hospital Review Dec 2025",
        "deployment": "Real-time: continuous vitals monitoring | Batch: nightly care gap screening | Clinical workflow integration via CPOE",
        "vertical_score": "Viable",
        "roi_summary": {
            "investment": "Enterprise platform deployment (Palantir/custom)",
            "annual_return": "700+ lives saved (TGH) + 37 virtual beds (Nebraska) + 61K care gaps closed (CSH)",
            "payback": "Measured in lives and capacity, not just dollars",
            "three_year_roi": "Incalculable -- outcome is patient survival and system capacity",
            "intangibles": "Clinician trust, regulatory compliance, population health improvement",
        },
        "market_benchmark": {
            "market_size": "Clinical AI market: $8.1B (2025), 38% CAGR",
            "peer_comparison": "Epic Sepsis Model (built-in) | Viz.ai (stroke/PE) | Google Health (dermatology/ophthalmology)",
            "differentiator": "Agent architecture + any-EHR via FHIR vs platform lock-in (Epic/Palantir)",
            "source": "Becker's Hospital Review Dec 2025",
        },
    },
    # ─── UC-05: Legal Contract Review ─────────────────────
    {
        "id": "UC-05", "industry": "Legal",
        "title": "Contract Generation and Review -- 67-Agent Debate Protocol",
        "subtitle": "40hrs to 12hrs per contract, 99.1% clause accuracy, $2.4M recaptured",
        "company": "Top-100 Global Law Firm",
        "deployed": "22-week build, production by week 10",
        "challenge_headline": "60% of Billable Time on Contract Drafting and Review",
        "challenges": [
            "Paralegal review: 40 hours per contract across 90+ clause types",
            "Outside counsel spend growing 15% annually -- firms need to shift work internal",
            "Mid-market firms (<50 attorneys) priced out of Harvey AI ($100K+/yr)",
            "Clause extraction breaks when documents exceed LLM context windows",
            "Jurisdiction-specific customization: 19 jurisdictions, different rules per state/country",
            "Lawyers spent 28 hours finding clauses and only 12 on actual judgment",
        ],
        "solution_headline": "3 Agents + 5 MCP Servers + Debate Protocol",
        "solutions": [
            "3 agents: contract-generation + contract-review (67-agent debate) + legal-research",
            "open-agreements MCP: 40+ templates (NDA, MSA, SaaS, SAFE, NVCA, employment, DPA)",
            "lavern MCP: 3-layer verification -- evaluator gate, adversarial debate, 10-pass consensus",
            "suzielaw MCP: 22 legal providers across 19 jurisdictions",
            "Claude 3.5 Sonnet 200K context handles 300-page agreements in single pass -- no chunking",
            "A2I confidence gating: <0.85 confidence -> human review queue, not autonomous decision",
        ],
        "stats": [
            ("70%", "Review Time Down", "40 hrs -> 12 hrs per contract"),
            ("$2.4M", "Billable Hrs Recaptured", "Annual value redirected to judgment work"),
            ("99.1%", "Clause Accuracy", "Across 90+ clause types, 45K training contracts"),
            ("22 wk", "Full Build", "10 weeks to first production capability"),
            ("67", "Debate Agents", "Lavern adversarial review protocol"),
            ("45K", "Training Contracts", "Firm's own archive -- not generic legal text"),
        ],
        "how_it_works": [
            "Client request -> identify agreement type -> list_templates (open-agreements) -> get_template_fields",
            "Interview client for field values (grouped by section) -> fill_template -> rendered DOCX output",
            "Review Phase 1: planning agent reads contract (read-only) -> creates structured review plan",
            "Review Phase 2: execution agent -> risk assessment matrix + redlines + missing clause recommendations",
            "Alternative: Lavern full adversarial (67 agents, debate protocol, citation-grounded) -> executive memo",
            "Legal research: suzielaw searches 22 providers across 19 jurisdictions for precedent",
            "High-confidence -> auto-flag | Low-confidence (<0.85) -> A2I human review queue",
        ],
        "agents": [
            ("contract-generation-agent", "Template selection -> field interview -> fill_template -> DOCX render -> DocuSign"),
            ("contract-review-agent", "Phase 1: read-only planning -> Phase 2: risk matrix + redlines -> executive memo"),
            ("legal-research-agent", "suzielaw: jurisdiction-specific case search -- 22 providers, 19 jurisdictions"),
            ("billing-agent", "Time capture from calendar + email -> Clio time entries -> invoice generation"),
        ],
        "mcp_servers": [
            ("open-agreements MCP", "5 endpoints", "list_templates, get_template_fields, fill_template, search_templates, validate_fields"),
            ("lavern MCP", "21 MCP tools", "start_review, get_findings, approve_finding, get_verification_status, export_deliverable"),
            ("suzielaw MCP", "3 endpoints", "legal_search (19 jurisdictions), legal_get_document, legal_find_in_document"),
            ("DocuSign MCP", "3 endpoints", "create_envelope, send_for_signature, get_status -- e-signature workflow"),
            ("Clio MCP", "5 endpoints", "get_matters, get_time_entries, create_time_entry, generate_invoice, get_billing_summary"),
        ],
        "github_repos": [
            ("open-agreements/open-agreements", "v0.7.5 -- 40+ templates, MCP server, Claude Code plugin"),
            ("AnttiHero/lavern", "v0.15.0 -- 67 agents, debate protocol, 21 MCP tools, citation-grounded"),
            ("firelex/suzielaw", "160+ workflows, 19-jurisdiction legal research, 22 providers"),
            ("anylegal-ai/anylegal-oss", "Multi-LLM legal AI harness, SKILL.md compatible"),
            ("anthropics/claude-for-legal", "Practice-area plugins + MCP connectors for legal workflows"),
        ],
        "stack": [
            ("MCP: Templates", "open-agreements v0.7.5 -- 40+ templates as MCP server endpoints"),
            ("MCP: Review", "lavern v0.15.0 -- 67 agents, debate protocol, 21 MCP tools"),
            ("MCP: Research", "suzielaw -- 22 providers, 19 jurisdictions, legal search"),
            ("LLM", "Claude 3.5 Sonnet -- 200K context, single-pass for 300-page agreements"),
        ],
        "governance": [
            "Client-attorney privilege preserved: all processing within firm infrastructure",
            "A2I confidence gating: clauses with <0.85 confidence routed to human review",
            "45K-contract training on firm's own archive -- model learns firm-specific clause language",
            "Audit trail: every AI recommendation logged with confidence score and basis",
            "Jurisdictional compliance: template selection validates governing law against supported jurisdictions",
        ],
        "competitive": [
            ("Harvey AI", "$3B valuation, 3,500 lawyers/day", "Market leader for top-tier firms -- 3,500 lawyers using daily. Out of reach for mid-market ($100K+/yr)"),
            ("Thomson Reuters CoCounsel", "Established legal tech", "RAG over legal corpus -- no agent architecture or debate protocol"),
            ("Ironclad", "CLM platform", "Contract lifecycle management -- more workflow than AI intelligence"),
            ("Anthropic claude-for-legal", "Practice-area plugins", "Strong foundation but no integrated template/review/research pipeline"),
            ("Our approach", "Mid-market, open-source MCP", "50-70% cheaper, 5 MCP servers, agent debate protocol, $3-5K/mo"),
        ],
        "insight": "Lawyers spent 28 hours finding clauses and 12 on judgment. Now they spend 12 on judgment. Everyone does what they're actually good at. The 45K-contract training set from the firm's own archive is the decisive factor -- the model learned this firm's clause language, not generic legal text.",
        "buyer": "Legal Ops / Managing Partner",
        "revenue": "$3-5K/mo per firm",
        "systems": ["iManage", "DocuSign", "CLM", "Aderant", "Clio"],
        "users": "Paralegals | Associates | M&A partners | Legal ops",
        "source": "DreamzTech Apr 2026 + GBrain impl spec",
        "deployment": "Interactive: contract drafting with client interview | Headless: batch review of contract backlog | Weekly: automated billing via Clio",
        "vertical_score": "30/35 GO",
        "roi_summary": {
            "investment": "$250K (22-week build + training data prep)",
            "annual_return": "$2.4M billable hours recaptured + outside counsel reduction",
            "payback": "5.4 weeks (production by week 10)",
            "three_year_roi": "2,780%",
            "intangibles": "M&A due diligence 41% faster, deal capacity per partner +22%",
        },
        "market_benchmark": {
            "market_size": "Legal AI market: $1.7B (2025) -> $9.5B (2030)",
            "peer_comparison": "Harvey AI: $3B valuation, 3,500 lawyers daily | LexisNexis: 284% ROI (Forrester) | Thomson Reuters: CoCounsel",
            "differentiator": "Open-source MCP stack (5 servers) vs proprietary SaaS -- mid-market accessible at $3-5K/mo vs $100K+/yr",
            "source": "Grand View Research 2025 + Forrester TEI June 2025",
        },
    },
    # ─── UC-06: Financial Services — TD Bank ─────────────────────
    {
        "id": "UC-06", "industry": "Financial Services",
        "title": "TD Bank -- Mortgage Processing Agent (15hrs to Minutes)",
        "subtitle": "$826M origination volume, deployed January 2026, compliance from day 1",
        "company": "TD Bank",
        "deployed": "January 2026 -- production",
        "challenge_headline": "15+ Hours Per Mortgage Application",
        "challenges": [
            "Mortgage applications require 15+ hours of manual document review per application",
            "Cross-referencing borrower docs (ID, bank statements, pay stubs) is error-prone at scale",
            "LLMs hallucinate on arithmetic -- annualizing income from pay stubs is a known failure mode",
            "Risk and compliance review traditionally adds 3-5 days to the mortgage cycle",
            "100K+ applications per year -- manual processing is physically impossible at volume",
            "Competitive pressure: fintechs processing in days while traditional banks take weeks",
        ],
        "solution_headline": "Deterministic Math + LLM Document Reading",
        "solutions": [
            "Agentic AI reads entire borrower document packages -- purchase agreements, IDs, bank statements",
            "Deterministic rules-based tools handle ALL arithmetic -- LLM never does math",
            "Cross-references fields across documents, flags inconsistencies automatically",
            "Risk/compliance team built into the project from day 1, not bolted on after",
            "Human adjudicator reviews AI-generated credit summary -- approves/rejects with audit trail",
            "One use case done right before expanding to other banking operations",
        ],
        "stats": [
            ("15hr->min", "Processing Time", "Per mortgage application"),
            ("$826M", "2025 Origination", "U.S. residential mortgage volume"),
            ("Jan 2026", "Production Deploy", "Full production, not pilot"),
            ("Day 1", "Compliance Built In", "Risk team embedded from start"),
            ("100K+", "Applications/Year", "Scale of mortgage operation"),
            ("0", "LLM Math Operations", "All arithmetic is deterministic"),
        ],
        "how_it_works": [
            "Document package ingestion -> OCR/NLP extraction of structured fields from unstructured docs",
            "Field cross-reference: income on pay stub vs tax return vs bank deposits -> flag inconsistencies",
            "Income calculation routed to deterministic rules engine (not LLM) -> annualized income computed",
            "Credit summary auto-generated: income, assets, liabilities, DTI ratio, risk flags",
            "Human adjudicator reviews AI summary -> approves or rejects with full audit trail",
            "Continuous monitoring post-launch via TD Trustworthy AI governance framework",
        ],
        "agents": [
            ("document-extraction-agent", "OCR/NLP reads purchase agreements, IDs, bank statements, pay stubs"),
            ("cross-reference-agent", "Validates fields across documents -- flags income/asset inconsistencies"),
            ("credit-summary-agent", "Generates complete credit summary: DTI, risk flags, recommendation"),
            ("compliance-agent", "Applies TD Trustworthy AI framework -- ensures every decision has audit trail"),
        ],
        "mcp_servers": [
            ("Document Processing MCP", "4 endpoints", "ingest_document, extract_fields, cross_reference, generate_summary"),
            ("Rules Engine MCP", "3 endpoints", "calculate_income, compute_dti, apply_underwriting_rules -- deterministic math only"),
            ("Core Banking MCP", "3 endpoints", "get_credit_history, verify_identity, create_application -- system of record"),
        ],
        "github_repos": [
            ("All-Hands-AI/OpenHands", "Agent SDK for document processing pipeline with human-in-the-loop"),
            ("microsoft/presidio", "PII detection for handling sensitive financial documents"),
            ("huggingface/transformers", "Document understanding models -- LayoutLM, BERT for NER"),
            ("tesseract-ocr/tesseract", "Open-source OCR engine for document digitization"),
            ("langchain-ai/langchain", "Agent orchestration for multi-step document processing"),
        ],
        "stack": [
            ("Foundation", "Layer 6 + Claude + GPT -- selective per task, best model per subtask"),
            ("Arithmetic", "Deterministic rules engine -- NEVER let LLM do math on financial data"),
            ("Governance", "TD Trustworthy AI framework -- continuous post-launch monitoring"),
            ("Integration", "Core banking APIs + credit bureau feeds + document management"),
        ],
        "governance": [
            "TD Trustworthy AI governance framework applied from day 1 of project",
            "Continuous post-launch monitoring: model drift, accuracy degradation, bias checks",
            "Human adjudicator signs off on every credit decision -- AI recommends, human decides",
            "Full audit trail: every AI extraction logged with source document + confidence score",
            "Deterministic math: all arithmetic operations use rules engine, never LLM inference",
        ],
        "competitive": [
            ("JPMorgan COIN", "360K hours saved, 9+ years", "Purpose-built ML for contracts -- not agentic, not mortgage processing"),
            ("Mastercard Decision Intelligence", "300% detection improvement", "Fraud detection: 300% improvement, 200% FP reduction -- $5M+ saved per issuer"),
            ("Blend", "Mortgage automation SaaS", "Digital lending platform -- workflow automation, limited AI intelligence"),
            ("ICE Mortgage Technology", "Encompass", "Market leader for LOS -- workflow-centric, limited AI extraction"),
            ("Our differentiation", "Agentic + deterministic", "Best of both: LLM reads documents, rules engine does math, human decides"),
        ],
        "insight": "They didn't let the LLM do math. Deterministic tools for arithmetic, LLM for document reading. Sharp task boundaries. Human signs off on every credit decision. Risk/compliance built into the team from day one. One use case done right before expanding. Dead simple discipline. That's it.",
        "buyer": "VP Mortgage Operations / CTO",
        "revenue": "Enterprise (internal deployment)",
        "systems": ["Core Banking", "Doc Management", "Credit Bureau", "Compliance", "LOS"],
        "users": "Mortgage underwriters | Credit adjudicators | Compliance officers",
        "source": "American Banker, May 2026",
        "deployment": "Production: full mortgage pipeline | Human-in-the-loop: adjudicator review step | Continuous monitoring: TD Trustworthy AI",
        "vertical_score": "Production",
        "roi_summary": {
            "investment": "Enterprise (internal build)",
            "annual_return": "15hr->min per application x 100K+ applications/yr = massive labor reallocation",
            "payback": "Immediate on deployment (January 2026)",
            "three_year_roi": "Enterprise scale -- measured in competitive positioning, not just cost savings",
            "intangibles": "Fintech-competitive speed, compliance confidence, scalability to other banking ops",
        },
        "market_benchmark": {
            "market_size": "AI in banking: $76B (2030), 32% CAGR",
            "peer_comparison": "JPMorgan COIN: 360K hrs/yr saved, 9+ yrs | Mastercard: 300% fraud detection improvement | Blend: digital lending SaaS",
            "differentiator": "Agentic + deterministic hybrid vs pure-LLM or pure-rules -- sharp task boundaries are the innovation",
            "source": "American Banker May 2026 + Mastercard Global 2026",
        },
    },
    # ─── UC-07: Financial Services — JPMorgan COIN ─────────────────────
    {
        "id": "UC-07", "industry": "Financial Services",
        "title": "JPMorgan COIN -- 360K Attorney-Hours Saved, 9+ Years Running",
        "subtitle": "Purpose-built ML extracts 150 attributes from commercial credit agreements",
        "company": "JPMorgan Chase",
        "deployed": "June 2016, still in production (9+ years)",
        "challenge_headline": "12,000 Credit Agreements Need 150 Attributes Each",
        "challenges": [
            "12,000 commercial credit agreements per year require extraction of 150+ attributes each",
            "Multi-day manual review cycles for covenants, collateral, payment schedules, default conditions",
            "Error rate in manual extraction unacceptable at institutional lending scale",
            "Expanding scope: NDAs, custody agreements, CDS documentation -- same extraction problem",
            "900+ data scientists, $9.6B/year tech budget -- scale demands purpose-built solutions",
            "Attorneys spending time on extraction instead of negotiation and strategy",
        ],
        "solution_headline": "Purpose-Built ML -- Not an LLM",
        "solutions": [
            "Custom ML extracts 150 attributes from commercial credit agreements in seconds",
            "Trained on firm's own contract archive -- learned JPMorgan's clause language, not generic",
            "Expanded over 9 years to NDAs, custody agreements, CDS, and trade documentation",
            "Not an LLM -- purpose-built precision extraction ML on private cloud infrastructure",
            "Error rate reduced ~80% vs manual extraction across all 150 attribute types",
            "Lawyers shifted to negotiation and strategy -- not replaced, redirected to higher-value work",
        ],
        "stats": [
            ("360K", "Attorney-Hours Saved/yr", "Across commercial lending operations"),
            ("12K", "Contracts/yr", "Processed in seconds vs multi-day cycles"),
            ("~80%", "Error Rate Down", "Vs manual extraction across 150 attributes"),
            ("9+ yrs", "In Production", "Since June 2016, continuously expanded"),
            ("150", "Attributes Extracted", "Covenants, collateral, payments, defaults, jurisdictions"),
            ("$9.6B", "Annual Tech Budget", "Scale of JPMorgan technology investment"),
        ],
        "how_it_works": [
            "Contract ingestion -> layout-preserving extraction (maintains document structure)",
            "150-attribute NER model -> covenants, collateral descriptions, payment schedules",
            "Default conditions + jurisdiction identification -> structured output per agreement",
            "Flagged clauses -> human review -> corrections feed continuous model improvement",
            "Expanded scope: same pipeline applied to NDAs, custody, CDS documentation",
            "9 years of continuous refinement: model learns from every human correction",
        ],
        "agents": [
            ("extraction-agent", "Layout-preserving extraction of 150 attributes from commercial credit agreements"),
            ("classification-agent", "Covenant type, collateral category, payment structure classification"),
            ("expansion-agent", "Applies extraction patterns to new document types: NDAs, custody, CDS"),
        ],
        "mcp_servers": [
            ("COIN Platform", "Proprietary", "150-attribute extraction, continuous retraining, multi-document-type support"),
            ("Contract Management", "Internal", "Document ingestion, structured output, human review queue"),
        ],
        "github_repos": [
            ("huggingface/transformers", "LayoutLM + DocFormer for document understanding architectures"),
            ("microsoft/unilm", "LayoutLMv3 -- pre-trained multimodal for document AI"),
            ("tesseract-ocr/tesseract", "OCR foundation for document digitization"),
            ("explosion/spaCy", "NER pipeline for entity extraction from legal text"),
        ],
        "stack": [
            ("ML", "COIN proprietary -- precision extraction ML, not LLM-based"),
            ("Infrastructure", "Private cloud -- $9.6B annual tech budget, 900+ data scientists"),
            ("Training", "Firm's own contract archive -- learned JPMorgan clause language"),
            ("Scope", "Credit agreements -> NDAs -> custody -> CDS -- 9 years of expansion"),
        ],
        "governance": [
            "Private cloud infrastructure: all processing within JPMorgan security perimeter",
            "Continuous model retraining: human corrections feed improvement pipeline",
            "Audit trail: every extraction logged with confidence score and source location",
            "Regulatory compliance: meets SEC, OCC, Fed requirements for financial document processing",
        ],
        "competitive": [
            ("TD Bank", "Agentic AI (2026)", "Newer approach: LLM + deterministic tools -- different scope (mortgage vs commercial)"),
            ("Mastercard Decision Intelligence", "143B txns/yr", "300% fraud detection improvement, $5M+ saved per issuer -- different domain, same AI-first DNA"),
            ("Kira Systems (Litera)", "Contract analysis", "AI contract review -- acquired by Litera, enterprise pricing"),
            ("Our framing", "Lessons learned", "9 years proves: narrow domain + own data + continuous refinement = production endurance"),
        ],
        "insight": "Contracts follow predictable structures. Narrow domain, closed text environment, static rules. Started with single document type, 150 attributes. Lawyers shifted to negotiation and strategy -- not replaced, redirected. That's the actual work. The lesson: purpose-built ML on your own data beats general-purpose LLM on someone else's.",
        "buyer": "CTO / VP Legal Operations",
        "revenue": "Enterprise ($9.6B tech budget)",
        "systems": ["Core Banking", "Contract Management", "Credit Risk", "Legal Operations"],
        "users": "Loan officers | Attorneys | Credit analysts | Operations",
        "source": "TacticalVC Apr 2026; Finextra Sep 2025",
        "deployment": "Production: continuous processing of 12K contracts/year | Batch: quarterly portfolio reviews | Expansion: new document types via transfer learning",
        "vertical_score": "Production (9+ years)",
        "roi_summary": {
            "investment": "Part of $9.6B annual tech budget",
            "annual_return": "360K attorney-hours saved/yr + ~80% error rate reduction",
            "payback": "Recovered within first year (2016), compounding ever since",
            "three_year_roi": "9+ years of continuous production -- ROI measured in decades, not quarters",
            "intangibles": "Expanded to NDAs, custody, CDS -- platform becomes more valuable with each document type added",
        },
        "market_benchmark": {
            "market_size": "AI in financial services: $76B (2030), 32% CAGR",
            "peer_comparison": "TD Bank: agentic (2026) | Mastercard: 143B txns/yr, 300% detection | Kira/Litera: contract analysis SaaS",
            "differentiator": "9-year production track record -- proof that narrow domain ML compounds with time and data",
            "source": "TacticalVC Apr 2026 + Finextra Sep 2025 + Mastercard Global 2026",
        },
    },
    # ─── UC-08: Construction — DroneDeploy ─────────────────────
    {
        "id": "UC-08", "industry": "Construction",
        "title": "DroneDeploy -- 34M Annotations, 4 AI Agents, 3M+ Sites",
        "subtitle": "Autonomous overnight capture to morning reports, 48% injury reduction",
        "company": "DroneDeploy + Barton Malow",
        "deployed": "Production across 3M+ sites, break-even Sep 2025",
        "challenge_headline": "Construction Sites Are Unstructured and Underdocumented",
        "challenges": [
            "Manual site walks miss events, rely entirely on superintendent memory",
            "Safety violations go undetected -- poor documentation is industry-wide",
            "Progress reporting takes 2 days of manual compilation per project",
            "Generic computer vision doesn't understand what 'installed' means per trade",
            "Subcontractor management: no objective comparison across trades or sites",
            "Data center construction segment exploding: 300+ projects, users up 128% YoY",
        ],
        "solution_headline": "4 AI Agents + Autonomous Capture + 34M Annotation Corpus",
        "solutions": [
            "4 AI agents: Progress AI, Safety AI, Inspection AI, Embodied AI -- each specialized",
            "Autonomous ground robots (Rocos) + docked drones capture sites overnight automatically",
            "Morning reports: overnight progress by trade delivered before team arrives on site",
            "Safety AI trained on 120K labeled examples -- flags PPE/guardrail violations in real-time",
            "13-year annotation corpus: 34M labeled examples across 3M sites in 180 countries",
            "770M images processed in 2025 alone -- robotics missions grew 160% YoY in 2026",
        ],
        "stats": [
            ("34M", "Training Annotations", "13-year corpus across 180 countries"),
            ("+340%", "Safety Catches", "Real-time violation detection improvement"),
            ("48%", "Injury Reduction", "Over 12-month deployment period"),
            ("3M+", "Sites in Production", "Global deployment scale"),
            ("770M", "Images (2025)", "Processed in single calendar year"),
            ("Sep 2025", "Break-Even", "Company reached profitability"),
        ],
        "how_it_works": [
            "Overnight: ground robots + docked drones autonomously capture from fixed vantage points",
            "Morning: Progress AI generates structured report -- installed work, trade progress, deviations",
            "Continuous: Safety AI monitors for PPE violations, guardrail issues, zone intrusions",
            "Inspection AI: structural analysis, defect identification, compliance documentation",
            "Embodied AI: ground-level autonomous navigation for detailed site documentation",
            "All captures -> BIM overlay -> Procore/PlanGrid integration -> project management dashboard",
        ],
        "agents": [
            ("Progress AI", "Overnight capture -> structured morning report: installed work by trade, deviations from plan"),
            ("Safety AI", "Real-time: PPE detection, guardrail violations, zone intrusions (120K labeled examples)"),
            ("Inspection AI", "Structural analysis, defect identification, compliance documentation with annotations"),
            ("Embodied AI", "Ground-level autonomous navigation for detailed, close-range site documentation"),
        ],
        "mcp_servers": [
            ("DroneDeploy Platform", "Cloud API", "Image processing, annotation management, report generation, BIM overlay"),
            ("Procore Integration", "Project mgmt", "Progress updates, safety reports, inspection logs -> project management"),
            ("BIM Integration", "Model overlay", "Capture data -> BIM model comparison -> deviation detection"),
        ],
        "github_repos": [
            ("ultralytics/ultralytics", "YOLOv8 -- foundation for Safety AI object detection (PPE, guardrails)"),
            ("opencv/opencv", "Image processing pipeline for drone + robot captures"),
            ("PointCloudLibrary/pcl", "3D point cloud processing for site reconstruction -- 1,000+ projects"),
            ("openMVG/openMVG", "Structure from Motion -- 3D reconstruction from 2D images"),
            ("All-Hands-AI/OpenHands", "Agent orchestration for multi-agent site intelligence"),
        ],
        "stack": [
            ("Vision", "34M annotation corpus -- 770M images (2025) -- domain-specific CV models"),
            ("Capture", "Ground robots (Rocos) + docked drones -- autonomous overnight missions"),
            ("Agents", "Progress AI + Safety AI + Inspection AI + Embodied AI -- specialized per task"),
            ("Integration", "Procore + PlanGrid + BIM overlay -- project management ecosystem"),
        ],
        "governance": [
            "FAA Part 107 compliance for all drone flight operations -- certified pilots required",
            "Site access and privacy requirements: signed agreements for autonomous capture",
            "Image retention per project contract terms: typically 7+ years for construction records",
            "Data sovereignty: images stored in region-appropriate cloud infrastructure",
            "Safety AI accuracy monitoring: weekly false positive/negative review with safety officers",
        ],
        "competitive": [
            ("Buildots", "Indoor CV", "Progress tracking via hardhat cameras -- indoor only, no outdoor/drone"),
            ("OpenSpace", "360 walk-through", "Walk-through capture -- manual trigger, not autonomous"),
            ("Procore (Verizon/AI)", "Project management", "PM platform adding AI -- broad but not deep on CV"),
            ("Skydio", "Drone hardware", "Autonomous drone hardware -- strong flight, limited analytics"),
            ("DroneDeploy edge", "34M annotation moat", "13-year corpus across 180 countries -- competitors can't replicate the data flywheel"),
        ],
        "insight": "13-year annotation corpus -- 34M labeled examples across 180 countries -- is the moat. The superintendent now acts on data instead of generating it. Faster decisions, fewer surprises. Generic CV fails because it doesn't understand what 'installed' means for different trades. Domain-specific training on construction site data is the differentiator.",
        "buyer": "VP Construction / Project Director",
        "revenue": "Enterprise (break-even Sep 2025)",
        "systems": ["BIM", "Procore", "PlanGrid", "GIS", "ERP"],
        "users": "Superintendents | Project managers | Safety officers | Execs",
        "source": "DroneDeploy Blog Apr 2026 + BCG 2026 + PCL 1,000+ projects",
        "deployment": "Autonomous: overnight capture missions | Morning: automated reports by 07:00 | Real-time: continuous safety monitoring | Integration: Procore/PlanGrid sync",
        "vertical_score": "Production (3M+ sites)",
        "roi_summary": {
            "investment": "Enterprise SaaS (reached break-even Sep 2025)",
            "annual_return": "48% injury reduction + 340% safety catch improvement + 2-day reporting -> morning delivery",
            "payback": "Platform reached profitability Sep 2025",
            "three_year_roi": "Measured in safety outcomes and project timeline compression",
            "intangibles": "Legal liability closure, subcontractor benchmarking, data center segment +128% YoY",
        },
        "market_benchmark": {
            "market_size": "Construction AI market: $3.1B (2025) -> $12.8B (2030), 33% CAGR",
            "peer_comparison": "Buildots (indoor) | OpenSpace (manual 360) | Skydio (drone HW) | Procore (PM+AI)",
            "differentiator": "34M annotation moat = 13 years of construction-specific training data. No competitor can replicate.",
            "source": "DroneDeploy Blog Apr 2026 + BCG Executive Perspectives 2026",
        },
    },
    # ─── UC-09: Construction — BCG German DevCo ─────────────────────
    {
        "id": "UC-09", "industry": "Construction",
        "title": "BCG: AI Construction Site Assistant -- 6x ROI, 48% Injury Down",
        "subtitle": "Computer vision for risk detection, progress tracking, productivity benchmarking",
        "company": "German DevCo (BCG pilot)",
        "deployed": "Pilot on 2 live projects, BCG 2026 Executive Perspectives",
        "challenge_headline": "Poor Documentation, Manual Walks, Memory-Based Decisions",
        "challenges": [
            "Historical poor incident documentation -- site walks miss events, rely on superintendent memory",
            "Productivity benchmarking impossible without objective data across subcontractors",
            "Manual progress reporting delays corrective action by days, not hours",
            "Subcontractor management: no objective comparison metric across trades",
            "Legal liability gaps from inconsistent site documentation practices",
            "BCG models 400-700 bps margin uplift achievable across the construction vertical",
        ],
        "solution_headline": "CV Risk Detection + Automated Documentation",
        "solutions": [
            "Computer vision: real-time site risk detection from continuous image capture",
            "AI-driven progress tracking: automated documentation vs plan comparison",
            "Productivity benchmarking: objective metrics across subcontractors and trades",
            "Smart notifications: immediate alerts when risks or deviations detected",
            "AI-generated compliance tracking, task documentation, and handover reports",
            "Objective photographic record closes legal liability gaps across subcontractors",
        ],
        "stats": [
            ("6x", "ROI", "Across deployed pilot projects"),
            ("12%", "Productivity Boost", "In first 6 months of deployment"),
            ("48%", "Injury Reduction", "Over 12-month deployment period"),
            ("30%", "Timeline Compression", "Project timeline reduction modeled by BCG"),
            ("400-700", "bps Margin Uplift", "BCG model across construction vertical"),
            ("2", "Live Pilots", "German DevCo projects in production"),
        ],
        "how_it_works": [
            "Site images captured -> CV processes for risk detection -> Smart notifications within minutes",
            "Progress tracking: AI compares captures against plan -> automated deviation reports",
            "Productivity benchmarking: metrics computed per subcontractor, per trade, per period",
            "Compliance: automated tracking generates documentation for handover and audit",
            "Legal: every site state captured photographically -> objective record for liability",
            "BCG Executive Perspectives: scalable across the entire construction vertical",
        ],
        "agents": [
            ("risk-detection-agent", "Real-time CV analysis of site images -> risk identification -> smart notifications"),
            ("progress-tracking-agent", "Capture vs plan comparison -> automated deviation reports -> corrective action triggers"),
            ("benchmarking-agent", "Productivity metrics per subcontractor/trade -> objective performance comparison"),
        ],
        "mcp_servers": [
            ("CV Pipeline MCP", "Image processing", "Risk detection, progress comparison, annotation, report generation"),
            ("Project Management MCP", "BIM/ERP", "Plan data import, deviation logging, milestone tracking"),
        ],
        "github_repos": [
            ("ultralytics/ultralytics", "YOLOv8 -- object detection for construction risk identification"),
            ("opencv/opencv", "Image processing pipeline for site photo analysis"),
            ("All-Hands-AI/OpenHands", "Agent orchestration for multi-step site intelligence"),
            ("streamlit/streamlit", "Dashboard for productivity benchmarking visualization"),
        ],
        "stack": [
            ("Vision", "CV risk detection -- real-time processing of site imagery"),
            ("Automation", "Smart notifications + compliance tracking + handover report generation"),
            ("Analytics", "Productivity benchmarking -- per subcontractor, per trade, objective metrics"),
            ("ROI", "BCG model: 400-700 bps margin uplift across the construction vertical"),
        ],
        "governance": [
            "Site imagery consent: agreements with all parties for continuous capture",
            "Data retention: construction records retained per project contract terms (7+ years typical)",
            "Privacy: worker PII not stored -- detection identifies hazards, not individuals",
            "Regulatory: OSHA compliance documentation automatically generated from captures",
        ],
        "competitive": [
            ("DroneDeploy", "Market leader, 34M annotations", "Autonomous capture + AI agents -- the benchmark for construction AI"),
            ("Buildots", "Indoor progress tracking", "Hardhat cameras -- strong indoor, limited outdoor/safety"),
            ("OpenSpace", "360 capture", "Manual walk-through documentation -- not automated, not real-time"),
            ("Our positioning", "BCG-validated ROI", "BCG Executive Perspectives validates 400-700 bps margin uplift -- credible third-party"),
        ],
        "insight": "Construction has historically had poor incident documentation. AI that captures every site state photographically creates an objective record -- closes legal liability gaps, triggers faster corrective action, produces the data trail for benchmarking across subcontractors. You can't manage what you can't see. Now they can see everything.",
        "buyer": "VP Construction / COO",
        "revenue": "Enterprise (pilot -> 400-700 bps margin uplift)",
        "systems": ["BIM", "ERP", "Safety Management", "Project Management"],
        "users": "Site managers | Safety officers | Project managers | Executives",
        "source": "BCG Executive Perspectives, 2026",
        "deployment": "Real-time: continuous site monitoring | Daily: automated progress reports | Periodic: productivity benchmarking reviews | Compliance: automated documentation",
        "vertical_score": "Pilot (6x ROI validated)",
        "roi_summary": {
            "investment": "Pilot deployment (2 live projects)",
            "annual_return": "6x ROI + 12% productivity + 48% injury reduction",
            "payback": "Within pilot phase (BCG validated)",
            "three_year_roi": "BCG models 400-700 bps margin uplift across entire vertical",
            "intangibles": "Legal liability closure, subcontractor benchmarking, timeline compression 30%",
        },
        "market_benchmark": {
            "market_size": "Construction AI market: $3.1B (2025) -> $12.8B (2030), 33% CAGR",
            "peer_comparison": "DroneDeploy: 34M annotations, 3M+ sites | Buildots: indoor | OpenSpace: manual 360",
            "differentiator": "BCG Executive Perspectives validates ROI -- third-party credibility for enterprise sales conversations",
            "source": "BCG Executive Perspectives 2026",
        },
    },
    # ─── UC-10: Legal — LexisNexis ─────────────────────
    {
        "id": "UC-10", "industry": "Legal",
        "title": "LexisNexis Lexis+ AI -- 284% ROI, Payback Under 6 Months",
        "subtitle": "Forrester TEI: $1.2M benefits, 13% outside counsel reduction, source-grounded",
        "company": "LexisNexis (Forrester TEI Study)",
        "deployed": "Forrester Total Economic Impact study, June 2025",
        "challenge_headline": "In-House Teams Overwhelmed, Too Much to Outside Counsel",
        "challenges": [
            "In-house legal teams overwhelmed -- shipping too much work to expensive outside counsel",
            "Legal research hours: associates spending 25%+ time on case lookups and precedent search",
            "Hallucinated case citations are the #1 trust barrier for legal AI adoption",
            "Need to increase matters handled internally without adding headcount",
            "Outside counsel costs growing 15% annually -- unsustainable trajectory",
            "Generic AI tools not grounded in verified primary law -- fabricated citations destroy trust",
        ],
        "solution_headline": "Source-Grounded AI on Verified Primary Law Corpus",
        "solutions": [
            "Gen AI grounded in verified LexisNexis primary law corpus -- no fabricated citations possible",
            "Contract drafting assistance: suggests clauses from verified precedent, review + accept",
            "Protege personalized AI assistant: adapts to individual attorney's practice area",
            "Shifts outside-counsel work internal -- more valuable than raw efficiency gains",
            "Source-grounded citations eliminate the hallucination problem entirely",
            "Forrester TEI methodology: validated by independent third-party research firm",
        ],
        "stats": [
            ("284%", "ROI (3-Year)", "Forrester Total Economic Impact study"),
            ("$1.2M", "Total Benefits", "Over 3-year evaluation period"),
            ("13%", "Outside Counsel Down", "Reduction in external legal spend -> $602.5K saved"),
            ("<6 mo", "Payback Period", "Investment recovered in under 6 months"),
            ("25%", "Fewer Lawyer Hours", "On research inquiries -> $574.2K saved"),
            ("5%", "More Matters Internal", "Handled without adding headcount (Year 1)"),
        ],
        "how_it_works": [
            "Legal question -> AI search grounded in LexisNexis primary law corpus -> source-cited answer",
            "Every citation links to verified primary law -- judge can click through to actual case text",
            "Contract draft -> Protege assistant suggests clauses from verified precedent -> review + accept",
            "Research time reduction: associates find relevant precedent in minutes vs hours of manual search",
            "Monthly tracking: reduction in outside counsel referrals measured against baseline",
            "Platform approach: same AI assists across research, drafting, and practice management",
        ],
        "agents": [
            ("research-agent", "Legal question -> corpus search -> source-cited answer with clickable case links"),
            ("drafting-agent", "Contract clause suggestion from verified precedent -> attorney review + accept"),
            ("protege-assistant", "Personalized to attorney's practice area -- learns preferences over time"),
        ],
        "mcp_servers": [
            ("LexisNexis Corpus", "Primary law", "Verified case law, statutes, regulations -- source of truth for citations"),
            ("Protege Platform", "Personalization", "Practice-area adaptation, workflow integration, citation verification"),
        ],
        "github_repos": [
            ("run-llama/llama_index", "RAG framework -- pattern for source-grounded retrieval over legal corpus"),
            ("chroma-core/chroma", "Vector database for embedding-based legal document search"),
            ("anthropics/claude-for-legal", "Practice-area plugins for legal AI workflows"),
            ("firelex/suzielaw", "Open-source legal research across 19 jurisdictions"),
        ],
        "stack": [
            ("Foundation", "LexisNexis corpus -- verified primary law, not scraped web content"),
            ("AI", "Gen AI + RAG -- source-grounded, every citation links to actual case text"),
            ("Assistant", "Protege -- personalized to practice area, learns attorney preferences"),
            ("Measurement", "Forrester TEI -- independent validation, not self-reported metrics"),
        ],
        "governance": [
            "Source grounding: every AI citation links to verified primary law in LexisNexis corpus",
            "No hallucinated citations: retrieval-augmented generation from verified source only",
            "Practice-area boundaries: AI responses scoped to relevant jurisdiction and practice area",
            "Independent validation: Forrester TEI methodology -- auditable by third party",
        ],
        "competitive": [
            ("Harvey AI", "$3B valuation, 3,500 lawyers/day", "Strong LLM-based legal AI but not source-grounded to primary law corpus. $100K+/yr enterprise"),
            ("Westlaw Edge (Thomson Reuters)", "Competing platform", "CoCounsel AI -- similar approach, different corpus, established distribution"),
            ("Casetext (Thomson Reuters)", "CoCounsel", "Acquired by Thomson Reuters -- AI research assistant, integrated into Westlaw"),
            ("Our framing", "Source-grounding lesson", "The winner in legal AI is the one grounded in verified primary law -- hallucination kills trust"),
        ],
        "insight": "Legal AI's core problem is hallucinated case citations. Grounding in a verified primary law database eliminates fabricated citations. The right business case framing: outside-counsel reduction is more valuable than raw efficiency gains. Shifting work internal via AI beats doing existing work faster. Frame it as revenue retained, not time saved.",
        "buyer": "General Counsel / Legal Ops Director",
        "revenue": "Enterprise (SaaS subscription)",
        "systems": ["LexisNexis", "DMS", "Practice Management", "Billing"],
        "users": "In-house counsel | Associates | Legal ops | Paralegals",
        "source": "GlobeNewswire / Forrester TEI, June 2025",
        "deployment": "SaaS: browser-based access to AI-powered research + drafting | Integration: DMS + practice management | Protege: personalized assistant per attorney",
        "vertical_score": "Production (284% ROI validated)",
        "roi_summary": {
            "investment": "SaaS subscription (enterprise pricing)",
            "annual_return": "$1.2M total benefits over 3 years = ~$400K/yr",
            "payback": "Under 6 months (Forrester validated)",
            "three_year_roi": "284% (Forrester TEI)",
            "intangibles": "13% outside counsel reduction, 5% more matters internal, attorney satisfaction",
        },
        "market_benchmark": {
            "market_size": "Legal AI market: $1.7B (2025) -> $9.5B (2030)",
            "peer_comparison": "Harvey AI: $3B valuation, 3,500 lawyers/day | Thomson Reuters CoCounsel | Casetext (acquired)",
            "differentiator": "Source-grounded on verified primary law corpus -- the only approach that eliminates hallucinated citations entirely",
            "source": "Forrester TEI June 2025 + GlobeNewswire",
        },
    },
]


# ═══════════════════════════════════════════════════════════════
# SLIDE GENERATORS — 12 slides per UC
# ═══════════════════════════════════════════════════════════════

def build_uc_title(uc):
    """Slide 1: UC title/overview."""
    p = next_page()
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
    d.text(s, f"{uc['id']} | {uc['industry'].upper()}", d.M + Inches(0.2), Inches(1.5),
           Inches(8), Inches(0.3), size=14, color=b.TEAL, bold=True)
    d.text(s, uc["title"], d.M + Inches(0.2), Inches(2.0), Inches(10), Inches(1.2),
           size=36, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M + Inches(0.2), Inches(3.4), Inches(1.5), Inches(0.05), b.TEAL)
    d.text(s, uc["subtitle"], d.M + Inches(0.2), Inches(3.7), Inches(9), Inches(0.5),
           size=16, color=b.MUTED)
    d.text(s, f"{uc['company']}  |  {uc['deployed']}", d.M + Inches(0.2), Inches(4.5),
           Inches(8), Inches(0.3), size=13, color=b.LIGHT_TEAL)
    if uc.get("vertical_score"):
        d.rect(s, d.M + Inches(0.2), Inches(5.2), Inches(2.5), Inches(0.45), b.TEAL, radius=0.03)
        d.text(s, f"VERTICAL SCORE: {uc['vertical_score']}", d.M + Inches(0.2), Inches(5.25),
               Inches(2.5), Inches(0.35), size=12, color=b.NAVY, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, f"Source: {uc['source']}", d.M + Inches(0.2), Inches(6.3),
           Inches(9), Inches(0.3), size=9, color=b.MUTED, italic=True)
    d.footer(s, p, 999, dark=True)


def build_uc_challenge(uc):
    """Slide 2: Challenge deep-dive."""
    p = next_page()
    s = d.slide(fill=b.WHITE)
    d.header(s, uc["challenge_headline"],
             f"{uc['id']} | {uc['industry']} -- The Problem")
    for i, ch in enumerate(uc["challenges"]):
        cy = Inches(1.7) + Inches(i * 0.85)
        d.rect(s, d.M, cy, d.CW, Inches(0.75), b.SOFT, radius=0.02)
        d.rect(s, d.M, cy, Inches(0.08), Inches(0.75), b.CORAL)
        d.text(s, f"{i+1:02d}", d.M + Pt(16), cy + Pt(6), Pt(30), Inches(0.2),
               size=14, color=b.CORAL, bold=True)
        d.text(s, ch, d.M + Inches(0.6), cy + Pt(6), d.CW - Inches(1), Inches(0.55),
               size=10, color=b.INK)
    d.footer(s, p, 999)


def build_uc_solution(uc):
    """Slide 3: Solution realization."""
    p = next_page()
    s = d.slide(fill=b.WHITE)
    d.header(s, uc["solution_headline"],
             f"{uc['id']} | {uc['industry']} -- How It's Realized")
    for i, sol in enumerate(uc["solutions"]):
        sy = Inches(1.7) + Inches(i * 0.85)
        d.rect(s, d.M, sy, d.CW, Inches(0.75), b.SOFT, radius=0.02)
        d.rect(s, d.M, sy, Inches(0.08), Inches(0.75), b.TEAL)
        d.text(s, f"{i+1:02d}", d.M + Pt(16), sy + Pt(6), Pt(30), Inches(0.2),
               size=14, color=b.TEAL, bold=True)
        d.text(s, sol, d.M + Inches(0.6), sy + Pt(6), d.CW - Inches(1), Inches(0.55),
               size=10, color=b.INK)
    d.footer(s, p, 999)


def build_uc_stats(uc):
    """Slide 4: KPI / Stats dashboard."""
    p = next_page()
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
    d.text(s, f"KEY METRICS -- {uc['id']} | {uc['industry'].upper()}", d.M, Inches(0.3),
           d.CW, Inches(0.4), size=22, color=b.WHITE, bold=True)
    d.rect(s, d.M, Inches(0.75), Inches(1.5), Inches(0.04), b.TEAL)

    stats = uc["stats"]
    cols = min(3, len(stats))

    for i, (num, label, detail) in enumerate(stats):
        row = i // cols
        col = i % cols
        sx = d.M + Inches(col * 4.1)
        sy = Inches(1.1) + Inches(row * 2.8)

        d.rect(s, sx, sy, Inches(3.8), Inches(2.5), b.NAVY_2, radius=0.03, shadow=True)
        d.text(s, num, sx, sy + Pt(16), Inches(3.8), Inches(0.7),
               size=44, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER, shrink=True)
        d.text(s, label, sx, sy + Inches(1.0), Inches(3.8), Inches(0.35),
               size=14, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
        d.text(s, detail, sx + Pt(16), sy + Inches(1.5), Inches(3.8) - Pt(32), Inches(0.7),
               size=9, color=b.MUTED, align=PP_ALIGN.CENTER)

    d.footer(s, p, 999, dark=True)


def build_uc_flow(uc):
    """Slide 5: How-it-works flow."""
    p = next_page()
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
    d.text(s, f"HOW IT WORKS -- {uc['id']} | {uc['industry'].upper()}", d.M, Inches(0.3),
           d.CW, Inches(0.4), size=22, color=b.WHITE, bold=True)
    d.rect(s, d.M, Inches(0.75), Inches(1.5), Inches(0.04), b.TEAL)

    for i, step in enumerate(uc["how_it_works"]):
        fy = Inches(1.1) + Inches(i * 0.82)
        d.rect(s, d.M, fy, d.CW, Inches(0.72), b.NAVY_2, radius=0.02)
        step_color = b.GOLD if i == 0 else (b.TEAL if i == len(uc["how_it_works"]) - 1 else b.LIGHT_TEAL)
        d.text(s, f"STEP {i+1}", d.M + Pt(12), fy + Pt(4), Inches(0.8), Inches(0.16),
               size=7, color=step_color, bold=True)
        d.text(s, step, d.M + Inches(1), fy + Pt(4), d.CW - Inches(1.3), Inches(0.55),
               size=8.5, color=b.MUTED)
        if i < len(uc["how_it_works"]) - 1:
            d.text(s, "v", d.M + Pt(30), fy + Inches(0.72), Pt(20), Pt(12),
                   size=8, color=b.TEAL, align=PP_ALIGN.CENTER)

    d.footer(s, p, 999, dark=True)


def build_uc_architecture(uc):
    """Slide 6: Architecture deep-dive -- agents + MCP."""
    p = next_page()
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
    d.text(s, f"ARCHITECTURE -- {uc['id']} | {uc['industry'].upper()}", d.M, Inches(0.22),
           Inches(8), Inches(0.22), size=9, color=b.TEAL, bold=True)
    title_part = uc['title'].split('--')[0].strip() if '--' in uc['title'] else uc['title'][:40]
    d.text(s, f"{title_part} Agent Architecture", d.M, Inches(0.42),
           d.CW, Inches(0.4), size=22, color=b.WHITE, bold=True, shrink=True)
    d.rect(s, d.M, Inches(0.82), Inches(1.5), Inches(0.03), b.TEAL)

    col1_w = Inches(5.5)
    y = Inches(1.0)
    d.text(s, "AGENT STACK", d.M, y, Inches(2), Inches(0.18),
           size=8, color=b.GOLD, bold=True)
    for i, (name, desc) in enumerate(uc["agents"]):
        ay = y + Inches(0.22) + Inches(i * 0.48)
        d.rect(s, d.M, ay, col1_w, Inches(0.42), b.NAVY_2, radius=0.02)
        d.text(s, name, d.M + Pt(10), ay + Pt(3), Inches(2.5), Inches(0.16),
               size=7.5, color=b.TEAL, bold=True)
        d.text(s, desc, d.M + Pt(10), ay + Pt(18), col1_w - Pt(20), Inches(0.18),
               size=6, color=b.MUTED)

    col2_x = d.M + Inches(5.8)
    col2_w = Inches(6.2)
    d.text(s, "MCP SERVERS", col2_x, y, Inches(2), Inches(0.18),
           size=8, color=b.GOLD, bold=True)
    for i, (name, count, tools) in enumerate(uc["mcp_servers"]):
        my = y + Inches(0.22) + Inches(i * 0.62)
        d.rect(s, col2_x, my, col2_w, Inches(0.55), b.NAVY_2, radius=0.02)
        d.text(s, f"{name} ({count})", col2_x + Pt(10), my + Pt(3), col2_w - Pt(20), Inches(0.16),
               size=7.5, color=b.TEAL, bold=True)
        d.text(s, tools, col2_x + Pt(10), my + Pt(18), col2_w - Pt(20), Inches(0.3),
               size=5.5, color=b.MUTED)

    dep_y = Inches(5.0)
    d.rect(s, d.M, dep_y, d.CW, Inches(0.5), b.ACCENT, radius=0.02)
    d.text(s, f"DEPLOYMENT: {uc['deployment']}", d.M + Pt(12), dep_y + Pt(4),
           d.CW - Pt(24), Inches(0.38), size=7, color=b.WHITE, bold=True)

    d.text(s, "Pattern: Agent(llm, tools, mcp_config, agent_context) -> Conversation(workspace, callbacks)",
           d.M, Inches(5.7), d.CW, Inches(0.25), size=6, color=b.MUTED, italic=True)

    d.footer(s, p, 999, dark=True)


def build_uc_techstack(uc):
    """Slide 7: Tech stack & GitHub repos."""
    p = next_page()
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
    d.text(s, f"TECH STACK & GITHUB -- {uc['id']} | {uc['industry'].upper()}", d.M, Inches(0.3),
           d.CW, Inches(0.4), size=22, color=b.WHITE, bold=True)
    d.rect(s, d.M, Inches(0.75), Inches(1.5), Inches(0.04), b.TEAL)

    d.text(s, "SOLUTION STACK", d.M, Inches(1.0), Inches(2), Inches(0.18),
           size=8, color=b.GOLD, bold=True)
    for i, (layer, detail) in enumerate(uc["stack"]):
        sx = d.M + Inches(i * 3.05)
        sw = Inches(2.85)
        d.rect(s, sx, Inches(1.25), sw, Inches(1.3), b.NAVY_2, radius=0.02)
        d.text(s, layer, sx + Pt(10), Inches(1.3), sw - Pt(20), Inches(0.2),
               size=8, color=b.TEAL, bold=True)
        d.text(s, detail, sx + Pt(10), Inches(1.55), sw - Pt(20), Inches(0.8),
               size=7, color=b.MUTED)

    d.text(s, "GITHUB REPOSITORIES", d.M, Inches(2.8), Inches(3), Inches(0.18),
           size=8, color=b.GOLD, bold=True)
    for i, (repo, desc) in enumerate(uc["github_repos"]):
        ry = Inches(3.05) + Inches(i * 0.68)
        d.rect(s, d.M, ry, d.CW, Inches(0.6), b.NAVY_2, radius=0.02)
        d.text(s, repo, d.M + Pt(12), ry + Pt(4), Inches(4), Inches(0.18),
               size=8, color=b.TEAL, bold=True)
        d.text(s, desc, d.M + Inches(4.2), ry + Pt(4), d.CW - Inches(4.5), Inches(0.42),
               size=7, color=b.MUTED)

    bar_y = Inches(6.5)
    sys_text = "SYSTEMS: " + "  |  ".join(uc["systems"])
    d.rect(s, d.M, bar_y, Inches(6), Inches(0.3), b.ACCENT, radius=0.02)
    d.text(s, sys_text, d.M + Pt(8), bar_y + Pt(2), Inches(5.8), Inches(0.24),
           size=6, color=b.WHITE, bold=True)
    d.rect(s, d.M + Inches(6.2), bar_y, Inches(5.8), Inches(0.3), b.DARK_TEAL, radius=0.02)
    d.text(s, f"USERS: {uc['users']}", d.M + Inches(6.3), bar_y + Pt(2),
           Inches(5.6), Inches(0.24), size=6, color=b.WHITE, bold=True)

    d.footer(s, p, 999, dark=True)


def build_uc_governance(uc):
    """Slide 8: Governance & compliance."""
    p = next_page()
    s = d.slide(fill=b.WHITE)
    d.header(s, f"Governance & Compliance -- {uc['id']}",
             f"{uc['industry']} -- Standards, audits, and compliance requirements")
    for i, gov in enumerate(uc["governance"]):
        gy = Inches(1.7) + Inches(i * 0.95)
        d.rect(s, d.M, gy, d.CW, Inches(0.82), b.SOFT, radius=0.02)
        d.rect(s, d.M, gy, Inches(0.08), Inches(0.82), b.ACCENT)
        d.text(s, f"[check]  {gov}", d.M + Pt(20), gy + Pt(8), d.CW - Pt(40), Inches(0.6),
               size=10, color=b.INK)
    d.footer(s, p, 999)


def build_uc_competitive(uc):
    """Slide 9: Competitive landscape."""
    p = next_page()
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
    d.text(s, f"COMPETITIVE LANDSCAPE -- {uc['id']} | {uc['industry'].upper()}", d.M, Inches(0.3),
           d.CW, Inches(0.4), size=22, color=b.WHITE, bold=True)
    d.rect(s, d.M, Inches(0.75), Inches(1.5), Inches(0.04), b.TEAL)

    for i, (comp_name, comp_detail, comp_desc) in enumerate(uc["competitive"]):
        cy = Inches(1.1) + Inches(i * 1.1)
        is_ours = "our" in comp_name.lower()
        bg = b.TEAL if is_ours else b.NAVY_2
        d.rect(s, d.M, cy, d.CW, Inches(0.95), bg, radius=0.02)
        name_color = b.NAVY if is_ours else b.GOLD
        d.text(s, comp_name, d.M + Pt(16), cy + Pt(6), Inches(3), Inches(0.2),
               size=11, color=name_color, bold=True)
        d.text(s, comp_detail, d.M + Inches(3.5), cy + Pt(6), Inches(3), Inches(0.2),
               size=9, color=b.MUTED if not is_ours else b.NAVY)
        d.text(s, comp_desc, d.M + Pt(16), cy + Pt(26), d.CW - Pt(32), Inches(0.5),
               size=8, color=b.MUTED if not is_ours else b.NAVY)

    d.footer(s, p, 999, dark=True)


def build_uc_insight(uc):
    """Slide 10: Brand-voice insight + buyer + revenue."""
    p = next_page()
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
    d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)

    d.text(s, f"THE ACTUAL INSIGHT -- {uc['id']}", d.M + Inches(0.2), Inches(0.5),
           Inches(8), Inches(0.3), size=12, color=b.TEAL, bold=True)
    d.text(s, uc["insight"], d.M + Inches(0.2), Inches(1.0), Inches(10), Inches(2.5),
           size=18, color=b.WHITE, italic=True)

    card_y = Inches(4.0)
    for ci, (label, value) in enumerate([
        ("BUYER", uc["buyer"]),
        ("REVENUE MODEL", uc["revenue"]),
        ("DEPLOYMENT", uc["deployment"].split("|")[0].strip()),
    ]):
        cx = d.M + Inches(0.2) + Inches(ci * 4.0)
        cw = Inches(3.7)
        d.rect(s, cx, card_y, cw, Inches(1.5), b.NAVY_2, radius=0.03)
        d.text(s, label, cx + Pt(12), card_y + Pt(8), cw - Pt(24), Inches(0.2),
               size=8, color=b.GOLD, bold=True)
        d.text(s, value, cx + Pt(12), card_y + Pt(28), cw - Pt(24), Inches(0.9),
               size=12, color=b.WHITE)

    d.text(s, f"Source: {uc['source']}", d.M + Inches(0.2), Inches(6.0),
           Inches(10), Inches(0.3), size=9, color=b.MUTED, italic=True)

    d.footer(s, p, 999, dark=True)


def build_uc_roi(uc):
    """Slide 11: Executive ROI Summary."""
    p = next_page()
    s = d.slide(fill=b.WHITE)
    d.header(s, f"ROI Summary -- {uc['id']}",
             f"{uc['industry']} -- Executive investment view")

    roi = uc.get("roi_summary", {})
    fields = [
        ("INVESTMENT", roi.get("investment", "N/A"), b.CORAL),
        ("ANNUAL RETURN", roi.get("annual_return", "N/A"), b.TEAL),
        ("PAYBACK", roi.get("payback", "N/A"), b.GOLD),
        ("3-YEAR ROI", roi.get("three_year_roi", "N/A"), b.ACCENT),
    ]

    for i, (label, value, accent) in enumerate(fields):
        ry = Inches(1.7) + Inches(i * 1.2)
        d.rect(s, d.M, ry, d.CW, Inches(1.05), b.SOFT, radius=0.02)
        d.rect(s, d.M, ry, Inches(0.1), Inches(1.05), accent)
        d.text(s, label, d.M + Pt(24), ry + Pt(8), Inches(2.5), Inches(0.22),
               size=10, color=accent, bold=True)
        d.text(s, value, d.M + Inches(2.8), ry + Pt(8), d.CW - Inches(3.2), Inches(0.8),
               size=11, color=b.INK)

    # Intangibles strip
    intangible = roi.get("intangibles", "")
    if intangible:
        iy = Inches(6.5)
        d.rect(s, d.M, iy, d.CW, Inches(0.45), b.NAVY, radius=0.02)
        d.text(s, f"INTANGIBLES: {intangible}", d.M + Pt(12), iy + Pt(6),
               d.CW - Pt(24), Inches(0.3), size=8, color=b.LIGHT_TEAL)

    d.footer(s, p, 999)


def build_uc_market(uc):
    """Slide 12: Market Benchmark."""
    p = next_page()
    s = d.slide(fill=b.NAVY)
    d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
    d.text(s, f"MARKET BENCHMARK -- {uc['id']} | {uc['industry'].upper()}", d.M, Inches(0.3),
           d.CW, Inches(0.4), size=22, color=b.WHITE, bold=True)
    d.rect(s, d.M, Inches(0.75), Inches(1.5), Inches(0.04), b.TEAL)

    mb = uc.get("market_benchmark", {})
    rows = [
        ("MARKET SIZE", mb.get("market_size", "N/A"), b.GOLD),
        ("PEER COMPARISON", mb.get("peer_comparison", "N/A"), b.TEAL),
        ("OUR DIFFERENTIATOR", mb.get("differentiator", "N/A"), b.LIGHT_TEAL),
    ]

    for i, (label, value, accent) in enumerate(rows):
        ry = Inches(1.1) + Inches(i * 1.8)
        d.rect(s, d.M, ry, d.CW, Inches(1.6), b.NAVY_2, radius=0.02)
        d.text(s, label, d.M + Pt(16), ry + Pt(8), Inches(3), Inches(0.22),
               size=10, color=accent, bold=True)
        d.text(s, value, d.M + Pt(16), ry + Pt(32), d.CW - Pt(32), Inches(1.1),
               size=12, color=b.MUTED)

    # Source
    src = mb.get("source", "")
    if src:
        d.text(s, f"Source: {src}", d.M, Inches(6.7), d.CW, Inches(0.3),
               size=8, color=b.MUTED, italic=True)

    d.footer(s, p, 999, dark=True)


# ═══════════════════════════════════════════════════════════════
# BUILD THE DECK
# ═══════════════════════════════════════════════════════════════

# --- COVER ---
p = next_page()
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
d.rect(s, d.W - Inches(0.12), 0, Inches(0.12), d.H, b.NAVY_2)
d.rect(s, d.W - Inches(0.18), 0, Inches(0.06), d.H, b.TEAL)

d.text(s, "FULL PIPELINE -- PRE-SALES INTELLIGENCE", d.M, Inches(0.8), Inches(7), Inches(0.35),
       size=14, color=b.TEAL, bold=True)
d.text(s, "AI Use Cases That Actually Ship",
       d.M, Inches(1.3), Inches(9), Inches(1.0),
       size=44, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(2.4), Inches(1.5), Inches(0.05), b.TEAL)
d.text(s, "10 Use Cases  |  5 Industries  |  12 Slides Each  |  Agent Architectures  |  GitHub Repos  |  MCP Stacks",
       d.M, Inches(2.7), Inches(10), Inches(0.4), size=15, color=b.MUTED)

chips = [("10", "Use Cases"), ("5", "Industries"), ("12/UC", "Slides Each"),
         ("30+", "GitHub Repos"), ("8+", "MCP Servers"), ("$2-10K/mo", "Revenue")]
for i, (num, label) in enumerate(chips):
    cx = d.M + Inches(i * 2.0)
    d.rect(s, cx, Inches(3.5), Inches(1.8), Inches(0.9), b.NAVY_2, radius=0.03, shadow=True)
    d.text(s, num, cx, Inches(3.55), Inches(1.8), Inches(0.45),
           size=26, color=b.GOLD, bold=True, align=PP_ALIGN.CENTER)
    d.text(s, label, cx, Inches(4.0), Inches(1.8), Inches(0.3),
           size=10, color=b.MUTED, align=PP_ALIGN.CENTER)

d.text(s, [
    {"text": "Data pipeline:", "size": 12, "color": b.LIGHT_TEAL, "bold": True},
    {"text": "GBrain recall -> Exa research -> Web research -> Implementation specs -> GitHub repos -> Vertical scorer -> pptxkit render", "size": 10, "color": b.MUTED, "space_before": 4},
], d.M, Inches(5.0), Inches(10), Inches(0.8))

d.text(s, "{{brand_name}}", d.M, Inches(6.8), Inches(3), Inches(0.4),
       size=13, color=b.MUTED, bold=True)
d.footer(s, p, 999, dark=True)


# --- EXEC SUMMARY ---
p = next_page()
s = d.slide(fill=b.WHITE)
d.header(s, "Portfolio: 5 Industries, 10 Use Cases, One Architecture",
         "OpenHands SDK + MCP servers + domain skills + system-of-record integration")

industries_summary = [
    ("Manufacturing", "32/35 GO", "PdM (Unilever $2.3M) + Visual QI (YOLOv8, 99.2%)", "$5-10K/mo"),
    ("Healthcare", "Viable", "Patient Intake (FHIR+Twilio) + Clinical AI (TGH 700+ lives)", "$3-5K/mo"),
    ("Legal", "30/35 GO", "Contract Review (67-agent) + LexisNexis (284% ROI)", "$3-5K/mo"),
    ("Financial Svcs", "Production", "TD Bank (15hr->min) + JPMorgan (360K hrs/yr)", "Enterprise"),
    ("Construction", "Production", "DroneDeploy (34M annotations) + BCG (6x ROI)", "Enterprise"),
]

for i, (name, score, desc, rev) in enumerate(industries_summary):
    row = i // 3
    col = i % 3
    cx = d.M + Inches(col * 4.0)
    cy = Inches(1.7) + Inches(row * 2.6)
    cw = Inches(3.7)

    d.rect(s, cx, cy, cw, Inches(2.3), b.SOFT, radius=0.02, shadow=True)
    d.rect(s, cx + Pt(6), cy + Pt(6), cw - Pt(12), Pt(20), b.NAVY, radius=0.02)
    d.text(s, name, cx + Pt(6), cy + Pt(7), cw - Pt(12), Pt(18),
           size=8, color=b.TEAL, bold=True, align=PP_ALIGN.CENTER)
    badge_color = b.TEAL if "GO" in score or "Production" in score else b.AMBER
    d.text(s, score, cx + Pt(6), cy + Pt(30), Inches(1), Pt(14),
           size=7, color=badge_color, bold=True)
    d.text(s, rev, cx + Inches(1.1), cy + Pt(30), Inches(1), Pt(14),
           size=7, color=b.GOLD, bold=True, align=PP_ALIGN.RIGHT)
    d.text(s, desc, cx + Pt(6), cy + Pt(48), cw - Pt(12), Inches(1.3),
           size=7, color=b.INK)

d.footer(s, p, 999)


# --- ARCHITECTURE OVERVIEW ---
p = next_page()
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
d.text(s, "ONE ARCHITECTURE, EVERY INDUSTRY", d.M, Inches(0.3), d.CW, Inches(0.5),
       size=28, color=b.WHITE, bold=True)
d.rect(s, d.M, Inches(0.85), Inches(1.5), Inches(0.04), b.TEAL)

layers = [
    ("USER LAYER", "CLI / Generative UI (AG-UI) / Headless Batch", b.TEAL, b.NAVY),
    ("ORCHESTRATION", "OpenHands Agent(llm, tools, mcp_config, agent_context) -> Conversation", b.NAVY_2, b.TEAL),
    ("AGENT STACK", "Orchestrator -> Sub-agents -> Parallel delegation -> Confirmation gates", b.NAVY_2, b.LIGHT_TEAL),
    ("MCP SERVERS", "predictive-maintenance | sap-pm | open-agreements | lavern | suzielaw | FHIR | Twilio", b.NAVY_2, b.GOLD),
    ("DOMAIN SKILLS", "SKILL.md + KeywordTrigger -> ISO standards, workflow rules, diagnostic protocols", b.NAVY_2, b.LIGHT_TEAL),
    ("SYSTEM OF RECORD", "SAP S/4HANA | EHR/FHIR | iManage | CRM | TMS | BIM | Core Banking", b.ACCENT, b.WHITE),
]

for i, (label, desc, bg, fg) in enumerate(layers):
    ly = Inches(1.2) + Inches(i * 0.9)
    d.rect(s, d.M, ly, d.CW, Inches(0.8), bg, radius=0.02)
    d.text(s, label, d.M + Pt(16), ly + Pt(8), Inches(2.5), Inches(0.25),
           size=11, color=fg, bold=True)
    d.text(s, desc, d.M + Inches(2.8), ly + Pt(8), d.CW - Inches(3.2), Inches(0.6),
           size=8, color=b.MUTED if bg == b.NAVY_2 else b.NAVY)

d.footer(s, p, 999, dark=True)


# --- MARKET OPPORTUNITY OVERVIEW ---
p = next_page()
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
d.text(s, "MARKET OPPORTUNITY -- AI IN ENTERPRISE", d.M, Inches(0.3), d.CW, Inches(0.5),
       size=28, color=b.WHITE, bold=True)
d.rect(s, d.M, Inches(0.85), Inches(1.5), Inches(0.04), b.TEAL)

markets = [
    ("AI in Banking", "$76B by 2030", "32% CAGR", "TD Bank, JPMorgan COIN, Mastercard Decision Intelligence"),
    ("AI PdM", "$19.27B by 2032", "39.5% CAGR", "Siemens Senseye, Bosch (50 plants), GE Vernova SmartSignal"),
    ("Legal AI", "$9.5B by 2030", "33% CAGR", "Harvey AI ($3B), LexisNexis (284% ROI), Thomson Reuters"),
    ("Healthcare AI", "$150B+ by 2030", "38% CAGR", "TGH + Palantir, CommonSpirit, Epic, Viz.ai"),
    ("Construction AI", "$12.8B by 2030", "33% CAGR", "DroneDeploy (34M annotations), Buildots, Procore AI"),
]

for i, (name, size_val, cagr, players) in enumerate(markets):
    my = Inches(1.2) + Inches(i * 1.15)
    d.rect(s, d.M, my, d.CW, Inches(1.0), b.NAVY_2, radius=0.02)
    d.text(s, name, d.M + Pt(16), my + Pt(6), Inches(2.5), Inches(0.22),
           size=12, color=b.TEAL, bold=True)
    d.text(s, size_val, d.M + Inches(2.8), my + Pt(6), Inches(2), Inches(0.22),
           size=14, color=b.GOLD, bold=True)
    d.text(s, cagr, d.M + Inches(5.0), my + Pt(6), Inches(1.5), Inches(0.22),
           size=10, color=b.LIGHT_TEAL, bold=True)
    d.text(s, players, d.M + Pt(16), my + Pt(28), d.CW - Pt(32), Inches(0.5),
           size=8, color=b.MUTED)

d.text(s, "Sources: MarketsAndMarkets 2026, Grand View Research 2025, Forrester TEI 2025",
       d.M, Inches(7.0), d.CW, Inches(0.25), size=7, color=b.MUTED, italic=True)
d.footer(s, p, 999, dark=True)


# --- GENERATE 12 SLIDES PER UC ---
current_industry = None
section_num = 0

for uc in USE_CASES:
    # Section divider when industry changes
    if uc["industry"] != current_industry:
        current_industry = uc["industry"]
        section_num += 1
        p = next_page()
        s = d.slide(fill=b.NAVY)
        d.rect(s, 0, 0, Inches(0.18), d.H, b.TEAL)
        industry_ucs = [u for u in USE_CASES if u["industry"] == current_industry]
        d.text(s, f"SECTION {section_num:02d}", d.M + Inches(0.2), Inches(2.0),
               Inches(3), Inches(0.3), size=14, color=b.TEAL, bold=True)
        d.text(s, current_industry, d.M + Inches(0.2), Inches(2.5), Inches(10), Inches(1.0),
               size=40, color=b.WHITE, bold=True, shrink=True)
        d.rect(s, d.M + Inches(0.2), Inches(3.6), Inches(1.5), Inches(0.05), b.TEAL)
        uc_titles = " | ".join([u["id"] for u in industry_ucs])
        d.text(s, uc_titles, d.M + Inches(0.2), Inches(3.9), Inches(9), Inches(0.4),
               size=14, color=b.MUTED)
        d.text(s, f"{len(industry_ucs)} USE CASES x 12 SLIDES = {len(industry_ucs) * 12} SLIDES",
               d.M + Inches(0.2), Inches(4.7), Inches(4), Inches(0.3),
               size=12, color=b.GOLD, bold=True)
        d.footer(s, p, 999, dark=True)

    # 12 slides per UC
    build_uc_title(uc)
    build_uc_challenge(uc)
    build_uc_solution(uc)
    build_uc_stats(uc)
    build_uc_flow(uc)
    build_uc_architecture(uc)
    build_uc_techstack(uc)
    build_uc_governance(uc)
    build_uc_competitive(uc)
    build_uc_insight(uc)
    build_uc_roi(uc)
    build_uc_market(uc)


# --- CROSS-INDUSTRY PATTERNS ---
p = next_page()
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.12), b.TEAL)
d.text(s, "CROSS-INDUSTRY PROOF POINTS", d.M, Inches(0.3), d.CW, Inches(0.5),
       size=28, color=b.WHITE, bold=True)
d.rect(s, d.M, Inches(0.85), Inches(1.5), Inches(0.04), b.TEAL)

proof_points = [
    ("Walmart 'Wally' AI Agent", "20-25% stockout reduction, $55M waste saved (2025), 90M pallets tracked real-time by 2026, 65% store automation target", b.GOLD),
    ("Mastercard Decision Intelligence", "300% fraud detection improvement, 200% false positive reduction, 143B txns/yr, 42% of issuers saved $5M+", b.TEAL),
    ("BMW AIQX", "95-99% defect accuracy, 50% inspection time reduction, 60% defect reduction, all plants globally", b.LIGHT_TEAL),
    ("Bosch Zero-Defect AI", "50 plants worldwide, 2,000+ lines interconnected, 15% takt time reduction, platform opened to 3rd parties (CES 2026)", b.GOLD),
    ("C.H. Robinson Lean AI", "30+ agents, 100T data points, quote time 17min->32sec, stock doubled during industry downturn, 7 consecutive quarters outperformance", b.TEAL),
]

for i, (name, detail, accent) in enumerate(proof_points):
    py = Inches(1.2) + Inches(i * 1.15)
    d.rect(s, d.M, py, d.CW, Inches(1.0), b.NAVY_2, radius=0.02)
    d.rect(s, d.M, py, Inches(0.08), Inches(1.0), accent)
    d.text(s, name, d.M + Pt(20), py + Pt(6), Inches(4), Inches(0.22),
           size=12, color=accent, bold=True)
    d.text(s, detail, d.M + Pt(20), py + Pt(28), d.CW - Pt(40), Inches(0.55),
           size=9, color=b.MUTED)

d.text(s, "Sources: Walmart FinancialContent Feb 2026 | Mastercard Global 2026 | BMW GreenData 2026 | Bosch CES 2026 | C.H. Robinson Mar 2026",
       d.M, Inches(7.0), d.CW, Inches(0.25), size=6, color=b.MUTED, italic=True)
d.footer(s, p, 999, dark=True)


# --- WHAT WINNERS HAVE IN COMMON ---
p = next_page()
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)

d.text(s, "WHAT THE WINNERS HAVE IN COMMON", d.M, Inches(0.42),
       d.CW, Inches(0.55), size=26, color=b.WHITE, bold=True)
d.rect(s, d.M, Inches(1.0), Inches(1.5), Inches(0.05), b.TEAL)

rules = [
    ("01", "Define the number before writing code",
     "TD Bank: processing hours. C.H. Robinson: quote time 17min->32sec. Unilever: downtime %. Walmart: stockout rate. A metric with a baseline before day 1."),
    ("02", "Automate the boring part, not the judgment",
     "AI handles extraction, matching, triage. Lawyers still decide. Underwriters still sign. Superintendents still prioritize. BMW AIQX keeps humans for the 0.3% the camera isn't sure about."),
    ("03", "Proprietary data is the moat, not the model",
     "C.H. Robinson 100T points. DroneDeploy 34M annotations. BMW AIQX all plants globally. Same models, different data, wildly different outcomes."),
    ("04", "Composite AI beats pure LLM",
     "TD Bank: deterministic math + LLM reading. Mastercard: 300% improvement via behavioral + transactional AI. EU 3PL: composite hit 92% vs 78% pure agentic."),
    ("05", "Trust is a deployment phase, not a launch event",
     "Unilever: 6-month technician trust. Macy's: one-week progressive rollout. Mastercard: 83% of leaders say AI reduced false positives and churn. Budget time for humans to catch up."),
]

for i, (num, title, desc) in enumerate(rules):
    ry = Inches(1.25) + Inches(i * 1.15)
    d.rect(s, d.M, ry, d.CW, Inches(1.0), b.NAVY_2, radius=0.02)
    d.text(s, num, d.M + Pt(12), ry + Pt(10), Pt(40), Pt(28),
           size=20, color=b.GOLD, bold=True)
    d.text(s, title, d.M + Inches(0.6), ry + Pt(8), d.CW - Inches(1), Inches(0.28),
           size=15, color=b.WHITE, bold=True)
    d.text(s, desc, d.M + Inches(0.6), ry + Pt(30), d.CW - Inches(1), Inches(0.52),
           size=10, color=b.MUTED)

d.footer(s, p, 999, dark=True)


# --- ENGAGEMENT MODEL ---
p = next_page()
s = d.slide(fill=b.WHITE)
d.header(s, "Engagement Model -- From Pilot to Production",
         "How we take you from first conversation to deployed AI in 4-10 weeks")

phases = [
    ("WEEK 1-2", "Discovery + Scoping", "Map your highest-ROI use case. Define the metric. Identify data sources and integration points. Go/No-Go decision.", b.CORAL),
    ("WEEK 3-4", "Pilot Build", "Agent architecture + MCP integration + domain skill configuration. Working prototype on your data. First results on real workload.", b.TEAL),
    ("WEEK 5-8", "Production Hardening", "Governance framework. Confidence gating. Human-in-the-loop setup. Performance benchmarking against your baseline metric.", b.GOLD),
    ("WEEK 8-10", "Deploy + Measure", "Production deployment. Trust-building phase. Weekly accuracy reviews. First ROI measurement against pre-defined baseline.", b.ACCENT),
    ("ONGOING", "Expand + Compound", "Active learning loop. New document types. Additional MCP servers. Adjacent use cases. Data moat compounds over time.", b.NAVY),
]

for i, (phase, title, desc, accent) in enumerate(phases):
    py = Inches(1.6) + Inches(i * 1.1)
    d.rect(s, d.M, py, d.CW, Inches(0.95), b.SOFT, radius=0.02)
    d.rect(s, d.M, py, Inches(0.08), Inches(0.95), accent)
    d.text(s, phase, d.M + Pt(20), py + Pt(6), Inches(1.5), Inches(0.18),
           size=9, color=accent, bold=True)
    d.text(s, title, d.M + Inches(1.8), py + Pt(6), Inches(3), Inches(0.18),
           size=11, color=b.INK, bold=True)
    d.text(s, desc, d.M + Pt(20), py + Pt(26), d.CW - Pt(40), Inches(0.55),
           size=9, color=b.INK)

d.footer(s, p, 999)


# --- SOURCES APPENDIX ---
p = next_page()
s = d.slide(fill=b.WHITE)
d.header(s, "Sources and References",
         "All data points sourced from named companies and verified publications")

sources = [
    "Unilever PdM: NSSG Insights, March 2026",
    "BMW AIQX: GreenData Ventures 2026 + Automotive Manufacturing Solutions",
    "Walmart Wally: FinancialContent / MarketMinute, February 2026",
    "Mastercard: Mastercard Global 2026 + BankCard International Group",
    "Bosch Zero-Defect: MyBusinessFuture / CES 2026",
    "Siemens Senseye: Siemens Blog, December 2025 + MarketsAndMarkets 2026",
    "Tampa General Hospital: Becker's Hospital Review, December 2025",
    "CommonSpirit Health: Becker's Hospital Review, December 2025",
    "Top-100 Law Firm: DreamzTech, April 2026",
    "Harvey AI: Multiple sources, 2025-2026 ($3B valuation)",
    "LexisNexis Lexis+ AI: Forrester TEI / GlobeNewswire, June 2025",
    "TD Bank: American Banker, May 2026",
    "JPMorgan COIN: TacticalVC April 2026; Finextra September 2025",
    "DroneDeploy: DroneDeploy Blog, April 2026 + PCL (1,000+ projects)",
    "BCG Construction: BCG Executive Perspectives, 2026",
    "C.H. Robinson: C.H. Robinson PR March 2026; The Applied April 2026",
    "GitHub repos: ultralytics, opencv, medplum, open-agreements, lavern, suzielaw, OpenHands",
    "Market sizing: MarketsAndMarkets 2026, Grand View Research 2025",
]

col1 = sources[:9]
col2 = sources[9:]
col_w = Inches(5.8)

for i, src in enumerate(col1):
    d.text(s, f"  {src}", d.M, Inches(1.6) + Inches(i * 0.5), col_w, Inches(0.4),
           size=8, color=b.INK)

for i, src in enumerate(col2):
    d.text(s, f"  {src}", d.M + Inches(6.0), Inches(1.6) + Inches(i * 0.5), col_w, Inches(0.4),
           size=8, color=b.INK)

d.footer(s, p, 999)


# --- CLOSER ---
p = next_page()
s = d.slide(fill=b.NAVY)
d.rect(s, 0, 0, d.W, Inches(0.16), b.TEAL)
d.rect(s, d.W - Inches(0.12), 0, Inches(0.12), d.H, b.NAVY_2)
d.rect(s, d.W - Inches(0.18), 0, Inches(0.06), d.H, b.TEAL)

d.text(s, "The best AI project is the one that actually ships.",
       d.M, Inches(2.0), Inches(10), Inches(1.8),
       size=42, color=b.WHITE, bold=True, shrink=True)
d.rect(s, d.M, Inches(4.0), Inches(1.5), Inches(0.05), b.TEAL)
d.text(s, "Not the one with the cleanest architecture, the most sophisticated model,\nor the biggest budget. The one that ships. With a number attached.",
       d.M, Inches(4.3), Inches(9), Inches(0.8), size=16, color=b.MUTED)

d.text(s, f"10 use cases. 5 industries. 130+ slides of evidence. One architecture pattern.",
       d.M, Inches(5.2), Inches(9), Inches(0.4), size=14, color=b.TEAL)

d.text(s, "{{brand_name}}", d.M, Inches(5.8), Inches(3), Inches(0.5),
       size=20, color=b.TEAL, bold=True)
d.text(s, "{{tagline}}", d.M, Inches(6.3), Inches(5), Inches(0.4),
       size=14, color=b.MUTED)
d.footer(s, p, 999, dark=True)


# ═══════════════════════════════════════════════════════════════
# FIX PAGE NUMBERS — replace 999 placeholder with actual TOTAL
# ═══════════════════════════════════════════════════════════════
TOTAL = PAGE[0]
for slide in d.prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if "/ 999" in run.text:
                        run.text = run.text.replace("/ 999", f"/ {TOTAL}")

OUT = Path(__file__).resolve().parent / "uc4-full-pipeline-deck-v2.pptx"
d.save(str(OUT))
print(f"Slides: {TOTAL}")
print(f"Size: {OUT.stat().st_size / 1024:.0f} KB")
print(f"Use cases: {len(USE_CASES)} x 12 slides = {len(USE_CASES) * 12} UC slides")
print(f"+ 4 intro + 1 market + section dividers + cross-industry + winners + engagement + sources + closer")
