---
status: reviewed
use_case: "Freight Quote and Routing Agent"
phase: "phase-2"
last_updated: "2026-06-26"
source_confidence: high
---

# Freight Quote and Routing Agent Master Implementation Blueprint

## Executive Positioning
- Target buyer: freight brokers and logistics ops.
- Pain wedge: quote requests sit in inboxes and slow response times.
- Incumbent weakness: TMS and broker workflows are too heavy for email-native quote handling.
- Agentic disruption thesis: read the request, query carrier APIs, and draft the best route/price.
- Why now: speed wins deals in freight.

## 1. Problem-Solution Fit Diagnostic
Score 27/30
- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

Evidence:
- Who has the problem: brokers and freight teams.
- Last-time/recency evidence: TMS modernization remains expensive.
- Current workaround: manual email/phone quoting.
- Switching reason: faster quotes and more throughput.
- Payment signal: TMS and brokerage labor.
- 30-day reachability: one customer lane and three carriers can prove the wedge.

Verdict: PROCEED

## 2. 30-Day Scope Definition
- Project name: Freight Quote Copilot
- Validated problem: freight quotes need rapid carrier comparison and draft replies.
- Target user: freight broker or logistics coordinator.
- Core hypothesis: the agent can extract shipment details and recommend a route.

In scope:
1. Email ingestion and extraction.
2. Carrier quote comparison.
3. Draft reply and booking handoff.

Explicitly out of scope:
- Replacing TMS.
- Autonomous booking for every lane.
- Complex customs or exception handling.

Week-by-week milestones:
- Week 1: email ingestion and entity extraction.
- Week 2: carrier API integration.
- Week 3: selection logic and drafting.
- Week 4: single-account pilot.

Dependencies:
- carrier APIs, email inbox, and lane rules.

Acceptance test:
- origin, destination, dimensions, and weight are extracted correctly and quotes returned quickly.

Top 3 risks + mitigations:
- missing fields - clarification reply
- carrier outage - fallback carrier set
- incorrect price - validation floor

## 3. Tech Stack + Architecture Design
Recommended stack:
- Frontend: broker inbox view.
- Backend: Python FastAPI.
- Agent orchestration: CrewAI or LangGraph.
- Retrieval/data layer: Postgres for lane and quote data.
- Auth: broker inbox and carrier API auth.
- Database: Postgres for shipments, quotes, and bookings.
- Observability: response latency and win-rate metrics.
- Hosting: cloud service near email and carrier APIs.

Architecture:
- System boundary: email request -> parse -> quote -> select -> draft response.
- Runtime topology: inbox -> extraction -> carrier query -> optimization -> reply.
- Core agent loop: read request, validate fields, query carriers, choose route, draft reply.
- Human-in-the-loop points: missing weight or ambiguous lane.
- Integration endpoints: SMTP/email, carrier APIs, TMS later.
- Failure handling: missing fields trigger a clarification email.

Database schema / data model:
| Table / Entity | Purpose | Key Fields | Indexes | Security / Tenancy |
|---|---|---|---|---|
| requests | freight requests | id, tenant_id, email_id, origin, dest | tenant_id, email_id | tenant-scoped |
| quotes | carrier quotes | id, request_id, carrier, price, transit | request_id, carrier | audit tracked |
| routes | selected lanes | id, request_id, route, confidence | request_id | reviewable |
| replies | drafted responses | id, request_id, body, status | request_id | immutable |

API surface:
| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | /api/requests | ingest freight email | email payload | request_id | service auth | 400 on invalid payload |
| POST | /api/requests/{id}/quote | query carriers | request_id | quotes | service auth | partial if carrier down |
| POST | /api/requests/{id}/reply | draft reply | request_id | email draft | service auth | hold if missing fields |

Integration plan:
| System | Direction | Data / Action | Auth | Failure Handling |
|---|---|---|---|---|
| email | inbound/outbound | freight request and reply | SMTP/API | retry and queue |
| carrier APIs | outbound | quote request | API token | fallback carriers |
| TMS | outbound | booking handoff | API token | queue later |

Folder/module structure:
- `app/api/`
- `services/extract/`
- `services/quote/`
- `services/select/`
- `services/reply/`

Environment variables:
- `EMAIL_INBOX_TOKEN`
- `CARRIER_API_KEYS`
- `TMS_API_TOKEN`
- `LANE_RULES_PATH`
- `LLM_API_KEY`

Critical design decisions:
1. Email-native intake because brokers live in inboxes.
2. Clarification over guessing because freight errors are expensive.
3. Keep TMS as SoR because dispatch history matters.

## 4. Build vs Buy Decision Matrix
| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| freight quote copilot | moderate | TMS implementations are heavy | Build | inbox-native speed is the wedge |
| TMS | low | already used | Buy | keep SoR |
| carrier APIs | low | existing | Buy/Reuse | connect, don't replace |

Bottom line:
- Annual SaaS spend if buying: TMS and brokerage software.
- One-time MVP build estimate: $50k-$100k equivalent effort.
- Recommended split: buy TMS, build inbox copilot.
- Payback period: under 12 months if quote throughput rises.

## 5. MVP ROI Business Case
Current-state cost model:
- Software: TMS and brokerage tools.
- Labor: broker time per quote.
- Services/admin: manual follow-up.
- Error/rework: delayed deals and pricing mistakes.

Agentic MVP cost model:
- Build: one inbox agent and carrier query pipeline.
- Monthly run: model and API usage.
- Maintenance: lane and carrier tuning.

Pricing options:
1. Low-risk pilot: one customer account.
2. Usage/outcome model: per quote.
3. Enterprise package: quoting plus analytics.

ROI scenarios:
| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Base | 10x throughput | 6-10 months | month 8-12 | standard |
| Upside | high win-rate lift | 3-6 months | month 4-6 | strong fit |
| Downside | carrier APIs sparse | 12-18 months | month 14+ | narrower scope |

No-go condition: if the required freight fields cannot be reliably extracted, the system becomes manual assistance only.

## 6. Competitor Product Teardown
Competitor map:
| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| TMS | transport mgmt | deep workflow | heavy | enterprise | market standard |
| brokers | labor | flexible | slow | labor-only | market standard |
| carrier portals | carrier | direct | fragmented | free/portal | market standard |

Direct threats:
- TMS suites
- manual brokers
- carrier portals

Table-stakes features to copy:
- field extraction
- carrier quote comparison
- reply drafting

Things not to build:
- TMS replacement
- full dispatch system
- autonomous booking without checks

Three exploitable gaps:
- inbox latency
- manual data entry
- quote-to-book delay

## 7. Acceptance Criteria + Test Plan
Feature test plan:
| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| freight email | complete request | parse runs | fields extracted | fixture test |
| missing weight | partial email | parse runs | clarification requested | negative test |
| quote compare | carriers respond | logic runs | best route selected | integration test |

Edge cases:
- Empty state: no carrier API available.
- Error state: malformed email rejected.
- Invalid input: missing lane info.
- Slow dependency: quote pending.
- Concurrent action: duplicate request idempotent.
- Auth/data boundary: tenant lane isolation.

## 8. Data Architecture Lite
Data domains:
| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| requests | email | request table | inbox | realtime | validation |
| quotes | carriers | quote table | carrier | realtime | freshness |
| routes | agent | route table | agent | realtime | margin floor |
| replies | agent | reply table | agent | realtime | review trail |

Retention and deletion:
- Data retained: request history and quotes.
- Data deleted: transient prompts after retention.
- Audit retained: quote and reply trail.

Analytics questions:
1. Which lanes most benefit from automation?

Privacy/security:
- tenant isolation
- carrier API security
- no quote without fields

## 9. Deployment Sequencing
Pre-deploy checklist:
- inbox connected
- carrier keys verified
- lane rules approved

Staging:
- pilot account only.

Production sequence:
- shadow -> quote-only -> reply drafting.

Smoke test:
- one freight email yields a valid quote.

Rollback:
- disable quotes and keep extraction only.

Observability:
- Logs: request, quote, route, reply.
- Metrics: quote latency, win rate, throughput.
- Alerts: carrier failure, field miss, reply error.
- Dashboards: by lane.

## 10. Post-Launch Iteration Plan
Metrics:
- Activation: requests processed.
- Retention: repeat broker use.
- Revenue/willingness-to-pay: throughput and wins.

Week-by-week:
- Week 1: add more carriers.
- Week 2: improve lane logic.
- Week 3: add booking handoff.
- Week 4: expand to more accounts.

Pivot signals:
- if carrier APIs are weak, stay quote-only
- if missing fields are common, narrow intake
- if volume is low, sell as draft helper only

## Source Notes
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/TMS_Freight_Management_Disruptive_Teardown.md` - upstream teardown dossier for the freight-routing wedge.
- FedEx APIs - https://developer.fedex.com/ - accessed 2026-06-26 - carrier integration backdrop.
- C.H. Robinson - https://www.chrobinson.com/ - accessed 2026-06-26 - brokerage backdrop.
- Official reference points reviewed: FedEx, C.H. Robinson, Uber Freight, Freightos, and Oracle Transportation Management product pages.
