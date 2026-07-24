# Full Strategy: Manufacturing Predictive Maintenance

## Bottom line
Manufacturing predictive maintenance is worth pursuing as an AI engineering service lane when the offer is framed as SAP-native operational reliability, orchestrated through a reusable OpenHands-based delivery layer, not as a generic machine-learning project.

## Why this lane is attractive
- The pain is measurable and recurring: downtime, scrap, technician productivity, and maintenance backlog.
- The buyer already owns core systems: SAP PM, MES, historians, IoT gateways, and asset master data.
- There are live proof points that scaled automotive deployments are possible.
- Outsourcing appetite is high in the exact disciplines required to deliver the solution.

## Beachhead offer
Sell a 6- to 10-week pilot for one asset class:
- Scope: robotic cells, conveyors, presses, or another downtime-critical line segment.
- Deliverables: sensor ingestion, anomaly scoring, health dashboard, SAP PM work-order integration, and technician feedback loop.
- Success metrics: reduction in unplanned downtime, mean time to detect, mean time to repair, false positive rate, and maintenance plan compliance.

## Recommended architecture
1. Ingest sensor and PLC/robot data through IoT gateways or historian feeds.
2. Normalize telemetry and work-order history into a plant reliability feature layer.
3. Use OpenHands SDK agents and skills to orchestrate anomaly analysis, root-cause summarization, and maintenance decision support.
4. Connect SAP PM, historians, and supporting enterprise systems through MCP or equivalent integration adapters where appropriate.
5. Push approved events into SAP PM or APM for planner action.
6. Capture technician outcome labels to improve thresholds and prioritization.

## Why OpenHands belongs in the stack
- The OpenHands SDK gives a composable agent runtime instead of forcing a one-off app architecture for each plant workflow.
- CLI and headless modes fit scheduled maintenance jobs, incident-response playbooks, and CI-style validation of agent behavior.
- Skills and repository agents support manufacturing-specific guardrails and reusable operating procedures.
- MCP support is directly aligned with the PDF's thesis that enterprise connectivity is the hard part of delivery.
- Enterprise self-hosting in a VPC is strategically relevant for plants with OT security, network segmentation, and data-control requirements.

## Commercial model
- Pilot fee: fixed-scope implementation with integration milestones.
- Expansion: per-plant rollout and managed monitoring retainer.
- Upsell path: visual inspection, predictive quality, safety monitoring, and digital traceability.
- Delivery leverage: reusable OpenHands skills, agent templates, and integration wrappers lower marginal rollout effort across plants.

## Key risks and controls
- Risk: alert fatigue.
  - Control: start with assisted triage and conservative thresholds.
- Risk: weak maintenance data quality.
  - Control: use a single asset family with good service history.
- Risk: OT security objections.
  - Control: edge-first architecture and plant-network segmentation review.
- Risk: unclear ownership between IT, OT, and maintenance.
  - Control: require a named plant sponsor and maintenance lead before pilot start.

## 90-day roadmap
- Days 1-15: asset selection, failure mode review, integration map, security review.
- Days 16-45: telemetry ingestion, baseline analytics, SAP PM workflow design.
- Days 46-75: pilot alerts, technician workflow, false-positive tuning.
- Days 76-90: ROI readout, expansion case, cross-plant deployment template.
