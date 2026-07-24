---
status: reviewed
use_case: "Threat Detection / SecOps"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Threat Detection / SecOps Disruptive Competitor Teardown

## Market Frame
- Workflow: correlate security signals, triage alerts, and decide what deserves human attention.
- Target buyer: SOC leaders, security operations, and incident-response teams.
- Existing spend category: SIEM, SOAR, detection engineering, threat intelligence, and managed security services.
- Incumbent economic model: enterprise platform pricing plus ingestion, support, and implementation complexity.
- Agentic wedge: compress tier-1 alert work while keeping the SIEM as the system of record.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| Google Security Operations | SIEM + SOAR | SOC and SecOps | Ingestion-based packages; contact sales | Data pipeline, parser, and rule setup | Unified SIEM/SOAR stack | Still a platform rollout |
| Splunk Enterprise Security | SIEM | Security ops | Enterprise pricing / contact sales | Data onboarding, detections, and tuning | Strong ecosystem and detection depth | Large implementation and licensing burden |
| Microsoft Sentinel | SIEM | Security and IT | Consumption-oriented Azure model | Workspace and connector setup | Native Microsoft footprint | Still requires SIEM engineering |
| ServiceNow Security Operations | SecOps workflow | Security teams | Enterprise contract | Case management and workflow modeling | Strong enterprise workflow story | Heavy platform/admin footprint |
| Managed SOC / MSSP | Services | Security leadership | Monthly or annual retainer | Handoffs and scope definition | Immediate coverage | Human-heavy and costly at scale |

## Direct Threats
1. Enterprise SIEM platforms.
2. SOAR and security incident-response modules.
3. Managed SOC / MSSP labor.

## Adjacent / Hidden Competitors
- Detection-engineering tooling.
- Threat-intelligence feeds.
- Case-management systems.
- ChatOps and incident workflows.

## Pricing Friction
- SIEM vendors often charge by ingestion, package, or enterprise contract.
- SOAR and response add-ons are priced as platform extensions.
- The buyer pays for setup, tuning, and the ongoing maintenance of detections.

## Onboarding And Workflow Friction
- Normalizing logs and telemetry across many systems.
- Building and tuning detections with false-positive control.
- Mapping alerts to the right response and escalation path.
- Keeping analysts in the loop while reducing alert fatigue.

## What Not To Build
- Do not replace the SIEM or log lake.
- Do not attempt to auto-close every alert.
- Do not skip audit logging or incident history.
- Do not rely on a static rule set for all threats.

## What To Keep
- System of record: SIEM, case history, and incident response records.
- Existing threat-intelligence and identity tools.
- Human review for high-severity or ambiguous alerts.

## Agentic Wedge
- Wedge statement: enrich the alert, explain the risk, and hand off the right action.
- Why it wins: less alert fatigue and faster tier-1 triage.
- Why now: platforms are adding AI, but the triage burden still lives with analysts.
- 30-day proof: one alert class, one SIEM integration, and one analyst-assisted triage loop.

## Blueprint Inputs
- Scope implication: start with one alert class or one asset segment.
- Architecture implication: webhook ingestion, enrichment services, and a triage queue.
- Build-vs-buy implication: buy the SIEM, build the enrichment and triage layer.
- ROI implication: use minutes saved per alert and reduced false-positive volume.
- QA/deployment implication: shadow mode, severity controls, and analyst override are mandatory.

## Source Notes
- Google Security Operations - https://cloud.google.com/security/products/security-operations - accessed 2026-06-26 - SIEM/SOAR package and pricing structure.
- Splunk Enterprise Security - https://www.splunk.com/en_us/products/enterprise-security.html - accessed 2026-06-26 - SIEM and SecOps platform positioning.
- Microsoft Sentinel - https://www.microsoft.com/en-us/security/business/siem-and-xdr/microsoft-sentinel - accessed 2026-06-26 - SIEM product page.
- ServiceNow ITSM - https://www.servicenow.com/products/itsm.html - accessed 2026-06-26 - security operations and incident workflow backdrop.
