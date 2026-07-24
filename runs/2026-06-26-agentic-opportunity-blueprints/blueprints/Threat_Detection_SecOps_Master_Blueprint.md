---
status: reviewed
use_case: "Threat Detection / SecOps"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Threat Detection / SecOps Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** SOC and SecOps leaders.

**Later ICPs:** adjacent incident-response teams once one alert family proves
the enrichment loop.

**Pain wedge:** tier-1 analysts drown in alert fatigue and context switching.

**Incumbent weakness:** SIEM and SOAR platforms still require manual triage and
playbook upkeep.

**Agentic disruption thesis:** enrich the alert, explain the risk, and route
the right response.

**Why now:** Google, Splunk, Microsoft, and ServiceNow are all pushing AI
security operations.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 26/30**

The score is inferred from high alert volume, broad security spend, and the
obvious toil in manual triage.

- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 9/10

**Who has the problem:** SOC teams managing large alert volumes.

**Current workaround:** manual triage and static correlation rules.

**Switching reason:** reduce triage time and improve decision quality.

**Payment signal:** SIEM, SOAR, and security-operations contracts.

**30-day reachability:** one alert class and one enrichment pipeline can prove
value.

**Verdict: PROCEED, but keep response bounded.**

## 2. The 30-Day Scope Definition

**Project name:** Alert Triage Copilot

**Validated problem:** Tier-1 alerts need context before an analyst can act.

**Target user:** SOC analyst or incident responder.

**Core hypothesis:** the agent can enrich alerts and recommend actions without
owning the SIEM.

### In Scope

1. **Alert enrichment**
   - Acceptance criterion: each alert gains read-only context from approved
     sources.
2. **Memo drafting**
   - Acceptance criterion: analyst gets a usable memo and recommendation.
3. **Case logging**
   - Acceptance criterion: analyst review state is written back with audit.

### Explicitly Out Of Scope

- New SIEM.
- Broad detection-engineering suite.
- Autonomous response without approval.
- Owning the alert source of record.

### Week-By-Week Milestones

- **Week 1:** define one alert family and data sources.
- **Week 2:** build enrichment and memo draft.
- **Week 3:** add analyst review and case logging.
- **Week 4:** pilot one queue with shadow mode.

**Dependencies:** SIEM webhook, enrichment sources, and analyst approval path.

**Acceptance test:** one alert is enriched and memoed with a full audit trail.

**Top risks:** noisy intel, webhook failure, and overbroad access.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: SOC review console.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for intel sources.
- Auth: SSO plus source-specific service credentials.
- Database: Postgres for alerts, enrichments, memos, and actions.
- Observability: OpenTelemetry, SIEM export, and memo tracing.
- Hosting: cloud app with queue worker.

**Architecture:** alert -> enrichment -> memo draft -> analyst review -> case
log. The agent enriches with approved sources and preserves provenance.

**Critical design decisions:**

1. Keep the SIEM as source of record.
2. Restrict to read-only enrichment in v1.
3. Require analyst approval before any response recommendation is executed.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/alerts/ingest` | ingest alert payload | alert event | queued alert | service token | retry queue |
| POST | `/api/alerts/enrich` | add context | alert_id | enrichment facts | service token | fallback to memo only |
| POST | `/api/alerts/review` | analyst state update | alert_id, state | case log | reviewer token | reject invalid state |

### Folder / Module Structure

- `app/secops/`
- `app/api/alerts/`
- `services/enrich/`
- `services/memo/`
- `workers/cases/`
- `lib/provenance/`

### Environment Variables

- `SIEM_WEBHOOK_TOKEN`
- `INTEL_SOURCE_TOKEN`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `CASE_LOG_URL`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| SIEM / SOAR | high | Google / Splunk / Sentinel already own it | BUY | not the wedge |
| Alert enrichment | medium | manual triage is the pain | BUILD | core wedge |
| Memo / case logging | medium | analysts still need it | BUILD | high leverage |

**Bottom line:** buy the SIEM shell and build the enrichment / memo layer.

## 5. MVP ROI Business Case

**Current-state cost model:** analyst time, triage delays, and playbook upkeep.

**Agentic MVP cost model:** webhook ingest, model usage, intel queries,
review, and audit storage.

**Pricing options:**

1. Low-risk pilot.
2. Usage / outcome model per enriched alert.
3. Enterprise package with case analytics.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | alert volume too low | 12-18 months | month 14+ | narrower scope |
| Base | 20-30% triage reduction | 6-10 months | month 8-12 | conservative |
| Upside | strong analyst adoption | 3-6 months | month 4-6 | broad enrichment coverage |

**Formulas**

```text
Monthly value =
  triage time saved + analyst context time reduced + case handling reduced
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if the SIEM cannot expose alert context via API, the
copilot cannot do more than summarize noise.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Google SecOps | SIEM / SOAR | integrated AI ops | platform rollout | ingestion packages | `runs/2026-06-26-agentic-opportunity-blueprints/source/Threat_Detection_SecOps_Disruptive_Teardown.md` |
| Splunk ES | SIEM | broad ecosystem | licensing and tuning burden | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Threat_Detection_SecOps_Disruptive_Teardown.md` |
| Microsoft Sentinel | SIEM | Azure native | configuration burden | consumption | `runs/2026-06-26-agentic-opportunity-blueprints/source/Threat_Detection_SecOps_Disruptive_Teardown.md` |
| ServiceNow SecOps | workflow | governance | heavy footprint | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Threat_Detection_SecOps_Disruptive_Teardown.md` |
| Palo Alto Cortex XSIAM | AI SOC platform | unified AI-driven SOC | platform rollout | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Threat_Detection_SecOps_Disruptive_Teardown.md` |
| Rapid7 Next-Gen SIEM | SIEM | AI-powered unified visibility | still platform-centric | package-based | `runs/2026-06-26-agentic-opportunity-blueprints/source/Threat_Detection_SecOps_Disruptive_Teardown.md` |
| IBM QRadar SIEM | SIEM | mature enterprise SIEM | old-school operations burden | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Threat_Detection_SecOps_Disruptive_Teardown.md` |

**Direct threats:** SIEMs, SOARs, managed SOC services, and platformized AI SOC products such as Cortex XSIAM and Rapid7 Next-Gen SIEM.

**What not to build:** a new SIEM, broad detection-engineering suite, or
autonomous response without approval.

**Agentic wedge:** enrich alerts, draft memos, and route the right response
while keeping the SIEM intact.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| alert memo | alert fires | agent runs | memo and recommendation appear | replay test |
| degraded intel | API timeout | memo generated | confidence is lowered and noted | fault injection |
| case update | analyst approves | action submitted | case reflects state | integration test |

### Edge Cases

- No intel available.
- SIEM webhook failure.
- Malformed alert rejected.
- Partial memo.
- Duplicate alerts idempotent.
- Tenant isolation.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| alerts | SIEM | alert table | SIEM | realtime | schema checks |
| enrichments | intel / identity / EDR | enrichment table | sources | realtime | freshness checks |
| memos | agent | memo table | agent | realtime | citations + confidence |
| actions | analyst | action table | analyst | realtime | immutable log |

**Retention and deletion:** retain alert history, memos, and analyst actions;
delete transient prompt content after the retention window; keep case history
and provenance.

**Privacy/security:** least-privilege access, no writes to SIEM in v1 beyond
case notes, and redaction of sensitive fields in logs.

**Analytics questions:** which alert families can be safely enriched first and
which intel sources produce the most false confidence?

## 9. Deployment Sequencing

**Pre-deploy checklist:** webhook verified, enrichment sources approved,
analyst review path tested.

**Staging:** shadow mode.

**Production sequence:** enrich-only -> analyst assist -> narrow response
recommendations.

**Smoke test:** one alert memo generated and attached.

**Rollback:** disable memo generation and fall back to SIEM-only workflow.

**Observability:**

- Logs: alert source, enrichment source, memo confidence.
- Metrics: time-to-triage, memo rate, analyst acceptance.
- Alerts: intel failure, webhook failure, latency spike.
- Dashboards: alert family and response time.

## 10. Post-Launch Iteration Plan

**Metrics:** alerts enriched, repeat analyst use, and triage time saved.

**Week-by-week:**

- Week 1: add a second alert family.
- Week 2: expand enrichment sources.
- Week 3: add playbook recommendations.
- Week 4: package for SOC leads.

**Pivot signals:** simplify the format if analysts ignore memos, narrow the
sources if intel data is too noisy, and sell as a sidecar only if the SIEM
blocks integration.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/Threat_Detection_SecOps_Disruptive_Teardown.md` - SIEM/SOAR incumbent map and alert-enrichment wedge.
- Google Security Operations - https://cloud.google.com/security/products/security-operations - accessed 2026-06-26 - SIEM/SOAR AI positioning.
- Splunk Enterprise Security - https://www.splunk.com/en_us/products/enterprise-security.html - accessed 2026-06-26 - SIEM and SOAR positioning.
- Microsoft Sentinel - https://www.microsoft.com/en-us/security/business/siem-and-xdr/microsoft-sentinel - accessed 2026-06-26 - SIEM product page.
- ServiceNow ITSM - https://www.servicenow.com/products/itsm.html - accessed 2026-06-26 - incident workflow backdrop.
- Palo Alto Cortex XSIAM - https://www.paloaltonetworks.com/cortex/cortex-xsiam - accessed 2026-06-26 - AI-driven SOC positioning and triage automation.
- Rapid7 Incident Command / Next-Gen SIEM - https://www.rapid7.com/products/siem/ - accessed 2026-06-26 - AI-powered next-gen SIEM positioning.
- IBM QRadar SIEM - https://www.ibm.com/products/qradar-siem - accessed 2026-06-26 - enterprise SIEM reference point.
