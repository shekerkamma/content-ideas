---
status: reviewed
use_case: "Fraud and Risk Detection"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence: high
---

# Fraud and Risk Detection Master Implementation Blueprint

## Executive Positioning
- Target buyer: fraud operations and payments risk leaders.
- Pain wedge: false positives drain analysts and block legitimate customers.
- Incumbent weakness: black-box risk platforms are expensive to tune and hard to explain.
- Agentic disruption thesis: investigate each flagged event, explain the risk, and hand back a decision memo.
- Why now: payment platforms and risk vendors still depend on heavy instrumentation and policy tuning.

## 1. Problem-Solution Fit Diagnostic
Score 25/30
- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 8/10

Evidence:
- Who has the problem: ecommerce and fintech fraud teams with noisy review queues.
- Last-time/recency evidence: Riskified, Stripe Radar, and Sift keep selling risk automation.
- Current workaround: manual analyst review plus static rules.
- Switching reason: less review time, better explanation, fewer declines.
- Payment signal: fraud software and manual review labor.
- 30-day reachability: one flag type and one decision memo are enough to prove the wedge.

Verdict: PROCEED

## 2. 30-Day Scope Definition
- Project name: Fraud Investigation Copilot
- Validated problem: flagged transactions lack a fast, explainable decision packet.
- Target user: fraud analyst or risk reviewer.
- Core hypothesis: the agent can synthesize transaction history and outside signals into a useful memo.

In scope:
1. One event class - checkout, login, or refund fraud flags.
2. Investigation memo - customer history, device, and context.
3. Analyst review loop - approve, decline, or request more data.

Explicitly out of scope:
- Full fraud model replacement.
- Autonomous payout or account closure.
- Hidden black-box scoring without explanation.

Week-by-week milestones:
- Week 1: connect read-only event stream.
- Week 2: enrich with device and customer data.
- Week 3: generate memo and reviewer UI.
- Week 4: shadow mode against human decisions.

Dependencies:
- transaction history, device data, and review tooling.

Acceptance test:
- 100% of flagged events generate a memo and confidence score within 2 seconds.

Top 3 risks + mitigations:
- cold start risk - explicit uncertainty label
- false confidence - explanation + threshold guardrails
- data access risk - read-only connectors first

## 3. Tech Stack + Architecture Design
Recommended stack:
- Frontend: analyst review dashboard.
- Backend: Python FastAPI.
- Agent orchestration: LangGraph or similar multi-step planner.
- Retrieval/data layer: BigQuery or warehouse plus event features.
- Auth: SSO + role-based analyst access.
- Database: Postgres for cases and memo logs.
- Observability: structured logs and review outcome tracking.
- Hosting: containerized service in the merchant cloud.

Architecture:
- System boundary: read-only case enrichment and memo generation.
- Runtime topology: flagged event -> enrichment -> memo -> analyst decision.
- Core agent loop: assemble history, analyze anomalies, generate rationale, surface uncertainty.
- Human-in-the-loop points: high-value events, ambiguous cases, and threshold tuning.
- Integration endpoints: payments, identity, warehouse, chargeback tooling.
- Failure handling: missing signals produce uncertainty and fallback to analyst review.

Database schema / data model:
| Table / Entity | Purpose | Key Fields | Indexes | Security / Tenancy |
|---|---|---|---|---|
| flagged_events | incoming cases | id, tenant_id, event_type, payload, risk_score | tenant_id, event_type | tenant-scoped |
| enrichments | data gathered | id, event_id, source, facts_json | event_id | read-only provenance |
| memos | investigation output | id, event_id, rationale, confidence, recommendation | event_id, confidence | redacted where needed |
| analyst_actions | review decisions | id, memo_id, action, reviewer, ts | memo_id | audit trail |

API surface:
| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | /api/flagged-events | ingest flag | payload | event_id | service auth | 400 on invalid event |
| POST | /api/flagged-events/{id}/memo | generate memo | event_id | memo | service auth | partial memo with uncertainty |
| POST | /api/memos/{id}/decision | analyst decision | action, notes | ack | analyst auth | 409 on stale memo |
| GET | /api/memos/{id} | review memo | id | memo + evidence | analyst auth | 404 if not found |

Integration plan:
| System | Direction | Data / Action | Auth | Failure Handling |
|---|---|---|---|---|
| payment events | inbound | transaction flags | webhook token | queue on outage |
| device identity | inbound | fingerprints and links | service token | fallback to session history |
| warehouse | inbound | customer and order history | read role | cache recent extracts |
| case management | outbound | decision update | API token | retry and local log |

Folder/module structure:
- `app/api/`
- `services/enrich/`
- `services/memo/`
- `services/decision/`
- `workers/stream/`

Environment variables:
- `WAREHOUSE_CONNECTION`
- `DEVICE_RISK_API_KEY`
- `CASE_API_TOKEN`
- `RISK_THRESHOLD`
- `ANALYST_UI_URL`

Critical design decisions:
1. Explainability over a pure score because the buyer must defend the decision.
2. Read-only enrichment first because fraud teams cannot risk writes.
3. Case memo as the product because the analyst already has a queue.

## 4. Build vs Buy Decision Matrix
| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| investigation memo | moderate | risk platforms are expensive and opaque | Build | the memo is the wedge |
| fraud decisioning engine | high | vendor models already exist | Buy/Reuse | keep the scoring source |
| case management | low | existing queue in place | Buy/Reuse | do not replace review ops |

Bottom line:
- Annual SaaS spend if buying: risk platform plus review labor.
- One-time MVP build estimate: $50k-$90k equivalent effort.
- Recommended split: buy the risk scoring layer, build the memo layer.
- Payback period: under 12 months if false positives fall meaningfully.

## 5. MVP ROI Business Case
Current-state cost model:
- Software: fraud platform and review tooling.
- Labor: analyst queue time.
- Services/admin: policy tuning and manual investigation.
- Error/rework: false positives and customer friction.

Agentic MVP cost model:
- Build: one investigation flow and memo UI.
- Monthly run: feature fetches and model calls.
- Maintenance: threshold and policy updates.

Pricing options:
1. Low-risk pilot: one fraud flag class.
2. Usage/outcome model: price per memo or reviewed event.
3. Enterprise package: investigations plus tuning and reporting.

ROI scenarios:
| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Base | 25% review reduction | 6-12 months | month 8-12 | conservative |
| Upside | 40% false-positive reduction | 3-6 months | month 4-6 | stronger data access |
| Downside | low event volume | 12-18 months | month 14+ | needs broader use |

No-go condition: if the platform cannot provide read-only transaction and identity history, the copilot cannot explain itself.

## 6. Competitor Product Teardown
Competitor map:
| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Riskified | ecommerce fraud | shared intelligence | merchant-specific setup | sales-led | `runs/2026-06-26-agentic-opportunity-blueprints/source/Fraud_and_Risk_Detection_Disruptive_Teardown.md` |
| Stripe Radar | payments fraud | native to Stripe | limited outside Stripe | usage/add-on | `runs/2026-06-26-agentic-opportunity-blueprints/source/Fraud_and_Risk_Detection_Disruptive_Teardown.md` |
| Sift | risk platform | behavior signals | instrumentation burden | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/Fraud_and_Risk_Detection_Disruptive_Teardown.md` |

Direct threats: fraud decision engines, account security tools, manual review queues. Table stakes: explainable memo, confidence score, analyst decision loop. Things not to build: new payment rail, opaque score only, autonomous account lockout. Gaps: black-box explanations, cold-start ambiguity, manual review waste.

## 7. Acceptance Criteria + Test Plan
| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| memo generation | flagged transaction | agent runs | memo and rationale appear | replay against known cases |
| cold start handling | new user | missing history | uncertainty is explicit | QA case |
| decision loop | analyst review | action chosen | status updates and audit log | workflow test |

Edge cases:
- no features available
- source API failure shows partial memo
- malformed event rejected
- memo marked pending, not complete
- duplicate review updates idempotent
- tenant data isolated

## 8. Data Architecture Lite
Data domains:
| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| events | payment stream | event table | source system | realtime | schema validation |
| features | warehouse | feature store | warehouse | batch/realtime | freshness checks |
| memos | agent | memo table | agent | realtime | citation required |
| decisions | analyst | decision table | analyst | realtime | immutable log |

Retention and deletion:
- Data retained: event history, memo, and analyst decisions.
- Data deleted: transient prompts after retention window.
- Audit retained: model lineage and decision provenance.

Analytics questions:
1. Which signals are most predictive of false positives?

Privacy/security:
- least privilege read-only access
- no raw PII in logs when avoidable
- analyst review for high-risk decisions

## 9. Deployment Sequencing
Pre-deploy checklist:
- read-only access verified
- review queue available
- outcome logging configured

Staging:
- historical event replay.

Production sequence:
- shadow mode -> analyst assist -> narrow automation.

Smoke test:
- one event produces a memo and review record.

Rollback:
- disable memo generation and return to manual review.

Observability:
- Logs: features fetched, memo source, uncertainty reason.
- Metrics: review time, false-positive rate, decision accuracy.
- Alerts: missing feature, API failure, memo latency.
- Dashboards: top fraud signals.

## 10. Post-Launch Iteration Plan
Metrics:
- Activation: cases using the copilot.
- Retention: repeat analyst use.
- Revenue/willingness-to-pay: review hours and false-positive reduction.

Week-by-week:
- Week 1: add another flag class.
- Week 2: tune uncertainty presentation.
- Week 3: add chargeback drafting.
- Week 4: package for payments teams.

Pivot signals:
- if reviewers ignore memos, simplify the output
- if data access is weak, narrow to one channel
- if decisions remain uncertain, keep the product as assistive only

## Source Notes
- `runs/2026-06-26-agentic-opportunity-blueprints/source/Fraud_and_Risk_Detection_Disruptive_Teardown.md` - internal teardown and incumbent mapping.
- Riskified homepage - https://www.riskified.com/ - accessed 2026-06-26 - ecommerce fraud positioning.
- Stripe Radar - https://stripe.com/radar - accessed 2026-06-26 - payment fraud add-on positioning.
- Sift homepage - https://www.sift.com/ - accessed 2026-06-26 - fraud prevention and risk-based auth.
- Forter homepage - https://www.forter.com/ - accessed 2026-06-26 - digital fraud prevention and risk-based authentication.
- Signifyd homepage - https://www.signifyd.com/ - accessed 2026-06-26 - fraud protection and ecommerce merchant risk backdrop.
