---
status: reviewed
use_case: "Agentic Auto-remediation"
last_updated: "2026-06-26"
source_confidence:
  competitor: high
  pricing: medium
  workflow: high
---

# Agentic Auto-remediation Disruptive Competitor Teardown

## Market Frame
- Workflow: take a high-confidence alert and execute a bounded remediation action inside a policy envelope.
- Target buyer: SecOps, SRE, and platform teams that need faster containment without broad manual coordination.
- Existing spend category: SOAR, runbooks, incident response tooling, and services-heavy automation projects.
- Incumbent economic model: enterprise platform pricing plus implementation and playbook maintenance.
- Agentic wedge: replace static playbook authoring with a localized executor that can adapt to real-world drift.

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|
| Tines | Security automation / SOAR | Security ops | Sales-led / custom pricing | Workflow design, integrations, and approvals | Flexible automation | Still needs explicit workflow design |
| Splunk SOAR | SOAR | SecOps and SOC | Enterprise quote | Playbook authoring, connector setup, and tuning | Broad ecosystem | Heavy maintenance burden |
| Google SecOps | SIEM + SOAR | SOC leaders | Package-based, ingestion-based, contact sales | Data ingestion, parser setup, and rule selection | Unified SIEM/SOAR | Platform-first, not a targeted executor |
| ServiceNow Security Incident Response | SecOps workflow | Security and risk teams | Enterprise contract | Service mapping, workflow modeling, and CMDB alignment | Strong governance | Complex implementation and admin overhead |
| Homegrown runbooks | Scripts / wiki docs | Platform and SRE teams | Internal labor | Drift, brittle scripts, and undocumented assumptions | Cheap to start | Breaks when environment changes |

## Direct Threats
1. SOAR suites that already sit in the response path.
2. Security incident response modules inside large enterprise platforms.
3. Internal runbooks and scripts that are easy to start and hard to trust.

## Adjacent / Hidden Competitors
- Pager / alerting tools that own the trigger.
- ChatOps workflows that route approvals.
- Endpoint and cloud-control tools that perform the actual action.
- Incident-management platforms that own the audit trail.

## Pricing Friction
- SOAR vendors typically sell through sales-led enterprise motions.
- Pricing is often tied to platform size, data volume, or package scope.
- Services and implementation time are a real part of the total cost.
- The buyer pays for playbook maintenance even when the playbook is mostly repetitive.

## Onboarding And Workflow Friction
- Connecting alerts, identity, endpoint, and cloud-control systems.
- Defining blast radius, approvals, and rollback steps.
- Handling exceptions where the same action is safe in staging but unsafe in production.
- Maintaining playbooks as infrastructure and policy change.

## What Not To Build
- Do not replace the SIEM or incident platform first.
- Do not automate broad destructive actions without explicit approval gates.
- Do not create a giant generic orchestration layer.
- Do not assume a static playbook will stay correct.

## What To Keep
- System of record: the SIEM, incident system, and audit log.
- Existing change-management and approval flows.
- Human sign-off for high-risk production actions.

## Agentic Wedge
- Wedge statement: execute one approved remediation action safely, quickly, and with full auditability.
- Why it wins: less MTTR, less analyst toil, and less playbook maintenance.
- Why now: tools already expose APIs, but they still rely on brittle orchestration logic.
- 30-day proof: one remediation action, one approval flow, and one audit trail.

## Blueprint Inputs
- Scope implication: choose a single low-risk remediation action first.
- Architecture implication: durable workflow engine, approval gate, and immutable logs.
- Build-vs-buy implication: buy the SOC stack, build the bounded executor.
- ROI implication: use MTTR reduction and avoided analyst hours as the baseline.
- QA/deployment implication: shadow mode, blast-radius tests, and rollback are mandatory.

## Source Notes
- Tines Pricing - https://www.tines.com/pricing/ - accessed 2026-06-26 - security automation pricing posture.
- Splunk Enterprise Security - https://www.splunk.com/en_us/products/enterprise-security.html - accessed 2026-06-26 - SIEM and SOAR platform positioning.
- Google Security Operations - https://cloud.google.com/security/products/security-operations - accessed 2026-06-26 - ingestion-based SIEM/SOAR package structure.
- ServiceNow ITSM - https://www.servicenow.com/products/itsm.html - accessed 2026-06-26 - enterprise workflow and governance backdrop.
