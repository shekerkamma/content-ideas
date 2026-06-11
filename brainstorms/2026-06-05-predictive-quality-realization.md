# Predictive Quality Realization: Brainstorm / Discovery Notes
Date: 2026-06-05 · Goal: Grill out every detail of UC05 (Predictive Quality) from the AI Engineering Use Cases Framework — what it takes to actually deliver this as a service to a manufacturing client

## Structured context
- **Topic type**: deal-prep
- **Topic string**: Predictive quality AI service for automotive manufacturing using OpenHands + SAP integration
- **Entities**: OpenHands, SAP QM, SAP PM, SAP MII, Hyundai (reference client context), sensor-fusion-agent, explainability-agent, feature-engineering-agent, model-training-agent, SAP-PM-agent, Sight Machine, Uptake, Accenture, PTC ThingWorx, Siemens MindSphere, XGBoost, SHAP, ADK, AG-UI, CopilotKit, MLflow
- **Prospect/account**: Hyundai (framework reference)
- **Target buyer**: VP Manufacturing / VP Quality / Plant Manager
- **Verticals**: automotive manufacturing
- **Open decisions**: historian platform (per plant), SAP version/OData availability, pricing benchmarks

## Summary / key decisions
- **Scope**: predict out-of-spec parts mid-line using in-process sensor data (welding, torque, paint, CNC), NOT end-of-line visual inspection
- **Data path**: sensors → PLC → OPC-UA → historian (InfluxDB/SAP MII) — we tap the historian, never touch PLCs
- **ML approach**: XGBoost baseline on featurized sensor traces, labeled by SAP QM inspection results. LSTM/1D-CNN upgrade path.
- **OpenHands role**: AI engineering accelerator generating pipeline code via subagents (sensor-fusion, feature-engineering, model-training, explainability, SAP-PM). Cuts delivery 50%.
- **SAP integration**: QM (read inspection labels), PM (write quality notifications), MES/MII (production context). All via OData + MCP. No Joule.
- **Dashboard**: ADK + AG-UI generative dashboard with SHAP explainability, process drift SPC charts, root-cause drill-downs, natural-language queries
- **Delivery**: 4-week pilot (data → model → dashboard → validation in shadow mode). Traditional = 8-12 weeks.
- **Pricing**: $40-60K pilot (50-70% cheaper than big consulting), $8-12K/month retainer, $20K per additional line
- **Risks**: data quality #1, IT/OT access #2, label quality #3. Mitigated by Week 1 data discovery gate.
- **Competition**: faster/cheaper/open-source vs. Sight Machine (expensive SaaS), Uptake, Accenture (slow/costly), PTC/Siemens (vendor lock-in)

## Q&A log

### Q1 — What specific quality problem are we solving?
- Asked: What does "predictive quality" mean concretely in an automotive plant? Recommended: predicting out-of-spec parts before end-of-line inspection using in-process sensor data.
- Captured: Scope is predicting defective parts mid-line using sensor signals (welding current, torque values, paint thickness, temperature profiles). Goal: flag a part as likely defective while still on the line so it can be pulled or the process corrected before producing a batch of scrap. This is NOT end-of-line visual inspection (that's UC01) — this is upstream, sensor-driven, pre-defect prediction.
- Flags: none

### Q2 — What sensor data is available and how is it accessed?
- Asked: What sensor signals exist in a typical automotive plant and how do we get them? Recommended: PLC-connected sensors → OPC-UA/MQTT → historian (InfluxDB/PI/SAP MII). Tap the historian, not PLCs directly.
- Captured: Data sources: (1) welding robots — current, voltage, wire feed rate, gas flow via OPC-UA, (2) torque tools — angle, torque curves via tool controller APIs, (3) paint booths — thickness, temperature, humidity via MQTT, (4) CNC/press — vibration, force, position via OPC-UA. Access path: sensors → PLC → OPC-UA gateway → historian (InfluxDB or SAP MII). We connect at the historian layer — never touch PLCs directly (plant safety/OT concern). Data is typically available at 1-10 Hz, stored as time-series with part ID correlation.
- Flags: actual historian platform varies per plant -> confirm during discovery call

### Q3 — What does the ML pipeline look like?
- Asked: What's the modeling approach? Recommended: time-series classification per part — featurize sensor traces, XGBoost baseline, LSTM/1D-CNN upgrade.
- Captured: Pipeline: (1) data ingestion — pull sensor traces per part ID from historian, (2) feature engineering — statistical summaries (mean, std, skew, kurtosis per signal), frequency-domain features (FFT peaks), rate-of-change features, (3) labeling — join with end-of-line inspection results (pass/fail/defect-type from SAP QM), (4) baseline model — XGBoost on tabular features, fast to train, interpretable, good enough for pilot, (5) upgrade path — 1D-CNN or LSTM on raw traces for higher accuracy once data volume justifies it. Model outputs a defect probability per part per station. Threshold tuned to plant's cost tradeoff (false alarm cost vs. missed defect cost).
- Flags: need historical inspection data (pass/fail labels) from SAP QM for training -> confirm data access during discovery

### Q4 — How does the OpenHands agent stack deliver this?
- Asked: What role does OpenHands play — runtime inference or engineering delivery? Recommended: delivery acceleration, not runtime. OpenHands generates pipeline code via subagents.
- Captured: OpenHands is the AI engineering layer, not the inference runtime. Role: (1) sensor-fusion-agent — generates data ingestion code (OPC-UA/MQTT connectors, historian queries, part-ID correlation logic), (2) feature-engineering-agent — generates featurization pipelines from sensor schema, (3) model-training-agent — scaffolds training notebooks, hyperparameter sweeps, experiment tracking (MLflow), (4) explainability-agent — generates SHAP/LIME dashboards showing which sensor signals drove each prediction, (5) SAP-PM-agent — generates MCP connectors for SAP QM (read inspection results) and SAP PM (create quality notifications). OpenHands cuts delivery from 8-12 weeks to 4-6 weeks by auto-generating ~60% of boilerplate code. The human ML engineer focuses on feature selection, model tuning, and domain validation.
- Flags: none

### Q5 — What SAP integrations are required?
- Asked: Which SAP modules and what integration method? Recommended: QM, PM, MES/MII via OData APIs.
- Captured: Three SAP touchpoints: (1) SAP QM — read inspection lots and results (pass/fail/defect-code per part). This is the training label source. OData service: API_INSPECTIONLOT_SRV or custom CDS view. (2) SAP PM — write quality notifications when model flags a part. Triggers maintenance workflow if process parameter drift detected. OData service: API_MAINTNOTIFICATION_SRV. (3) SAP MII/ME — real-time production order context (which part is at which station). Optional but improves part-ID correlation. Integration via MCP servers wrapping OData endpoints — NOT Joule, NOT RFC/BAPI. Gemini + ADK + MCP → SAP OData is the stack.
- Flags: SAP system version and available OData services vary per plant -> confirm during technical discovery

### Q6 — What does the explainability dashboard look like?
- Asked: What does the quality team actually see? Recommended: SHAP values per signal, process drift trends, root-cause drill-downs.
- Captured: Dashboard has three views: (1) Real-time alert view — parts flagged as high defect probability, ranked by confidence, with the top 3 contributing sensor signals highlighted (e.g., "welding current spike at station 4 contributed 62% to this prediction"). Uses SHAP waterfall charts. (2) Process drift view — time-series trends of key process parameters with control limits. Shows when a parameter is drifting toward out-of-spec before it crosses the threshold. SPC-style charts enhanced with ML-detected anomalies. (3) Root-cause analysis view — for a selected defect type, shows which sensor signals and which stations are most correlated. Helps quality engineers investigate systemic issues, not just individual parts. Built as a generative UI dashboard using ADK + AG-UI pattern (CopilotKit frontend, Gemini agent backend). Quality engineer can ask natural-language questions: "why did station 4 flag 12 parts today?"
- Flags: none

### Q7 — Delivery timeline and engagement structure
- Asked: How long does a pilot take and what's the structure? Recommended: 4-week pilot (more complex than generic 2-week sprint).
- Captured: Four-phase pilot: (1) Week 1 — Data discovery + connectivity. Connect to historian, pull sensor data, validate part-ID correlation, pull SAP QM inspection results. Deliverable: data quality report + feature schema. (2) Week 2 — Feature engineering + baseline model. Build feature pipelines, train XGBoost baseline, validate against historical defects. Deliverable: model accuracy metrics + initial SHAP analysis. (3) Week 3 — Dashboard + SAP integration. Build explainability dashboard (ADK + AG-UI), connect SAP QM read + SAP PM write. Deliverable: working dashboard with live data. (4) Week 4 — Validation + handoff. Run model in shadow mode alongside existing inspection, measure precision/recall against actual defects, tune threshold. Deliverable: pilot results report + scale-up proposal. Framework says 8-12 weeks traditional → 4-6 weeks with OpenHands. Our 4-week sprint is at the aggressive end but achievable for a single-station pilot.
- Flags: none

### Q8 — Pricing and revenue model
- Asked: How do we price this? Recommended: fixed pilot fee ($40-60K) then monthly retainer ($8-12K/month).
- Captured: Two-phase pricing: (1) Pilot — fixed fee $40K-60K for the 4-week sprint. Covers data discovery, model build, dashboard, SAP integration, and validation. Value anchor: replaces 8-12 weeks of traditional consulting at $200-300/hr (= $120K-180K), so we're 50-70% cheaper AND faster. (2) Ongoing retainer — $8K-12K/month. Covers: model monitoring and retraining (monthly), dashboard hosting and support, expansion to additional stations/lines (each new station is a smaller incremental project), SAP integration maintenance. (3) Expansion upsell — each new production line is a ~$20K add-on (mostly config, not new model). Multi-plant deployment is the real scale play. Framework's $5K-10K/month estimate is conservative — the value of prevented scrap easily justifies $10K+/month.
- Flags: competitive pricing benchmarks needed -> market research

### Q9 — Risks and blockers
- Asked: What kills this engagement? Recommended: data quality #1, IT/OT politics #2.
- Captured: Five risks ranked: (1) Data quality — sensor data gaps, inconsistent sampling rates, missing part-ID correlation. Mitigation: Week 1 is entirely data discovery; if data is unusable, we pivot scope or exit before spending model-build effort. (2) IT/OT politics — plant OT team may block historian access for security reasons. Mitigation: we only read from historian (no PLC writes), present architecture to OT team in Week 0 pre-kick. (3) Label quality — SAP QM inspection results may be inconsistent (different inspectors, different criteria). Mitigation: focus on objective defect types first (dimensional, torque), not subjective ones (cosmetic). (4) Model accuracy — baseline XGBoost may not hit useful precision/recall. Mitigation: Week 4 shadow mode validates before any process changes; if model isn't good enough, we deliver the data infrastructure and dashboard as standalone value. (5) Change management — quality team may not trust or use the predictions. Mitigation: explainability dashboard is the trust-building mechanism; start as "advisory" not "automatic."
- Flags: none

### Q10 — Competitive landscape and differentiation
- Asked: Who else does this and how do we win? Recommended: Sight Machine, Uptake, big consultancies. Our edge: speed, cost, open-source.
- Captured: Competitors: (1) Sight Machine — SaaS platform for manufacturing analytics. Strength: purpose-built for manufacturing. Weakness: expensive ($100K+ annual), rigid platform, long implementation. (2) Uptake — predictive maintenance/quality platform. Similar strengths/weaknesses. (3) Accenture/McKinsey QuantumBlack — big consulting. Strength: enterprise relationships. Weakness: $400K+ engagements, 6+ month timelines, strategy-heavy, build-light. (4) PTC ThingWorx / Siemens MindSphere — industrial IoT platforms with ML add-ons. Strength: deep plant integration. Weakness: vendor lock-in, complex licensing. Our differentiation: (a) 4-week pilot vs. 6-month engagement, (b) $40-60K vs. $200K+, (c) open-source stack (OpenHands + OSS ML) = no vendor lock-in, (d) working prototype as deliverable, not a strategy deck, (e) explainability-first approach builds trust faster.
- Flags: none

## Open flags (pending input)
- Actual historian platform (InfluxDB vs SAP MII vs OSIsoft PI) -> confirm during prospect discovery call
- SAP system version and available OData services -> confirm during technical discovery
- Historical inspection data access from SAP QM -> confirm data availability and quality
- Competitive pricing benchmarks for predictive quality services -> market research needed
