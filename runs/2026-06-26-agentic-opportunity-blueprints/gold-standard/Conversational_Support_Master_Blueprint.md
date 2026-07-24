---
status: reviewed
use_case: "Conversational Support"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: medium-high
  implementation: medium-high
---

# Conversational Support Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** VP Customer Experience, Head of Support, COO, or CFO at a
mid-market ecommerce or subscription business with 10,000+ monthly support
contacts, an existing Zendesk/Freshdesk/Intercom/Gorgias stack, and at least
two high-volume deterministic workflows such as order status, returns, refund
status, subscription changes, or billing explanation.

**Later ICPs:** travel, marketplaces, consumer fintech, telecom, insurance, and
regulated customer operations after the support-policy and compliance guardrails
are proven in lower-risk ecommerce/subscription workflows.

**Pain wedge:** Companies pay twice for routine support: per-seat help desk
software plus human/BPO capacity for repetitive contacts such as order status,
refund status, billing explanation, account access, subscription change, and
appointment rescheduling.

**Incumbent weakness:** Zendesk, Freshdesk, Salesforce Service Cloud, Intercom,
Gorgias, NICE, Genesys, Five9, and BPO providers are optimized around human
agent capacity. AI add-ons are improving, but the buyer still faces seat
pricing, enterprise configuration, implementation cycles, governance concerns,
and poor customer trust when bots become gatekeepers.

**Agentic disruption thesis:** Do not replace the help desk on day one. Attach
to it as a resolution layer and price around verified outcomes. The system of
record can remain; the expensive tier-1 labor and seat expansion get compressed.

**Why now:** Public pricing is already shifting from seats to outcome pricing
through Intercom Fin and Gorgias AI Agent. Zendesk has also moved toward
verified-resolution pricing. Customer expectations have moved faster than
support operations: Zendesk CX Trends 2026 reports high expectations for 24/7,
faster service, and AI-decision explanations. The market is ready for a more
accountable agentic wedge, but only if it is narrow, measurable, auditable, and
human-fallback-safe.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 27/30**

This score is inferred from the scorecard, public market evidence, and current
pricing/competitor research. It should be confirmed with at least three buyer
interviews before being used as a validated sales claim.

- Problem realness: 10/10
- Solution fit: 9/10
- Buying signal + reachability: 8/10

**Who has the problem:** Support leaders and CX operators at companies with high
routine ticket volume, especially ecommerce/retail, travel, marketplaces,
consumer fintech, insurance, telecom, and SaaS. The scorecard names
customer-facing examples such as Mercedes MBUX, Wendy's FreshAI, Home Depot
Magic Apron, and Macy's Ask Macy's as proof that branded tier-1 agents are
already deployed in production-like customer workflows.

**Last-time/recency evidence:** Routine contacts happen daily. Zendesk CX Trends
2026 reports customers expect faster responses and 24/7 service because of AI.
The market evidence is current as of June 26, 2026: Intercom, Freshdesk,
Gorgias, Salesforce, and Zendesk all publicly sell or position AI support
capabilities.

**Current workaround:** Buyers either add more help desk seats, buy AI add-ons,
expand BPO capacity, create macros and brittle workflow automations, or deploy
chatbot builders that still fail outside scripted flows. The imported teardown
summarizes the exposed layer as per-seat help desks plus QA-scoring tools and
the lower tier of BPO.

**Switching reason:** The buyer does not need a new help desk. They need fewer
human touches for deterministic tier-1 contacts and a clearer economic model:
pay for verified resolution, not for every seat, bot builder, admin, or
outsourced hour.

**Payment signal:** Intercom Fin publicly prices at about `$0.99` per outcome.
Gorgias prices AI Agent around `$0.90-$1.00` per resolved conversation depending
on tier. Freshdesk adds usage-based AI sessions on top of seat plans. Zendesk's
AI pricing is sales-led and reported as tied to verified resolutions. This is a
real buying signal: vendors are already teaching buyers to think in outcomes.

**30-day reachability:** High. The ICP is easy to identify via visible support
stack, ticket volume proxies, ecommerce platform, support hiring, BPO usage, or
public help center maturity. A focused outreach list of 100 support/CX leaders
is feasible in 30 days.

**Verdict: PROCEED.** This is one of the best first portfolio wedges because the
economic contrast is legible: per-seat/per-hour support versus verified tier-1
outcomes.

## 2. The 30-Day Scope Definition

**Project name:** Verified Resolution Layer

**Validated problem:** Routine tier-1 contacts consume human agent and BPO
capacity even when the underlying answer or action is deterministic.

**Target user:** Head of Support or CX Operations leader managing 10,000+
monthly contacts in a company already using Zendesk, Freshdesk, Salesforce
Service Cloud, Intercom, Gorgias, or a BPO partner.

**Core hypothesis:** A narrow agentic layer can resolve two high-volume support
workflows at a lower cost per verified resolution than expanding seats or BPO
hours, while preserving customer trust through transparent fallback.

### In Scope

1. **Workflow selection and evaluation set**
   - Acceptance criterion: buyer can select two workflows and upload at least
     200 representative historic tickets per workflow for shadow evaluation.
2. **Knowledge and SOP ingestion**
   - Acceptance criterion: help-center articles, macros, escalation rules, and
     policy docs are ingested and each generated answer cites source material.
3. **Help desk connector**
   - Acceptance criterion: system can read tickets/conversations and write an
     internal note, proposed reply, tag, and escalation summary in one selected
     help desk.
4. **Two deterministic workflow routines**
   - Acceptance criterion: agent can complete the selected workflows using
     approved tools or produce an escalation with missing-data reason.
5. **Human fallback and review queue**
   - Acceptance criterion: low-confidence, sentiment-risk, regulated, or
     money-moving cases route to a human with summary and proposed next action.
6. **Audit and evaluation dashboard**
   - Acceptance criterion: support manager can view resolution rate, escalation
     rate, policy-failure rate, latency, and cost per verified resolution.

### Explicitly Out Of Scope

- Replacing Zendesk/Freshdesk/Salesforce/Intercom/Gorgias as system of record.
- Voice support, workforce management, QA scoring, full omnichannel migration,
  and contact-center telephony.
- Autonomous refunds, credits, cancellations, account closures, medical advice,
  credit decisions, insurance coverage decisions, or regulated eligibility
  decisions without human approval.
- Full BPO vendor replacement in the pilot.
- Training a custom foundation model.
- Open-ended agent access to every internal system.
- Full multilingual support.
- Customer authentication redesign.
- Long-running complaint handling or legal dispute resolution.
- Fully automated knowledge-base writing without review.

### Week-By-Week Milestones

- **Week 1:** Pick two workflows, ingest historic tickets/macros/help docs,
  define success/failure labels, and build a 200-500 case test set.
- **Week 2:** Connect one help desk and two operational tools, such as Shopify,
  Stripe, Recharge, CRM, subscription system, order management, or appointment
  scheduler. Implement retrieval, redaction, and source citation.
- **Week 3:** Ship the agent in shadow mode. It drafts responses/actions but
  does not send them to customers. Compare against human outcomes and tune
  escalation rules.
- **Week 4:** Run limited live traffic on the safest workflow. Report verified
  resolution rate, escalation rate, customer-visible transparency, policy
  failures, handle-time savings, and cost per verified resolution.

**Dependencies:** Help desk API access, knowledge base export, representative
historic tickets, approved customer-facing policies, safe operational API
credentials, DPA/security review, and a named support operations owner.

**Acceptance test:** The pilot passes if the agent safely resolves at least 30%
of selected workflow traffic in limited live mode, keeps policy failures below
an agreed threshold, routes all low-confidence/money-moving cases to humans, and
shows credible cost-per-resolution improvement against the current baseline.

**Top risks and mitigations:**

- **Bad bot experience:** disclose AI, show fallback, and avoid gatekeeper
  behavior.
- **Tool misuse:** start read-heavy; approval-gate refunds, credits, and account
  changes.
- **Unsupported ROI claims:** model ROI with ranges and verified resolution
  counts, not generic deflection claims.

## 3. Tech Stack + Architecture Design

### Recommended Stack

- **Frontend:** Next.js App Router + TypeScript for the operator console,
  review queue, evaluations, and analytics.
- **Backend:** Python FastAPI for agent/workflow APIs and webhook handlers.
- **Agent orchestration:** LangGraph or a small explicit state-machine for
  deterministic support workflows. Use a graph because escalation, tool calls,
  confidence checks, and policy gates must be inspectable.
- **LLM layer:** provider-routed models with a low-latency model for
  classification/summarization and a stronger model for complex explanation.
  Keep model choice replaceable.
- **Retrieval/data layer:** Postgres with pgvector or a managed vector store for
  support docs, macros, SOPs, and resolved-ticket examples.
- **Database:** Postgres for tenants, workflows, policies, cases, audit events,
  evaluation results, and tool-call logs.
- **Queue:** Redis/Celery, Cloud Tasks, or equivalent for webhook processing,
  eval runs, and async ticket updates.
- **Auth:** SSO/SAML or OAuth for enterprise buyers; role-based access for
  support admin, reviewer, and auditor.
- **Observability:** OpenTelemetry traces, structured logs, eval dashboard, and
  model/tool-call cost tracking.
- **Hosting:** Vercel for UI plus Cloud Run/Fly/Render/AWS ECS for backend, or
  buyer VPC deployment for regulated accounts.

### Architecture

**System boundary:** The product is a layer above the incumbent help desk and
operational systems. The help desk remains the system of record for customer
conversation history. The resolution layer stores only the minimum data needed
for evaluation, audit, and workflow execution.

**Core agent loop:**

1. Ticket webhook or batch import enters the intake service.
2. PII/payment/secret redaction runs before model calls where possible.
3. Intent classifier maps the case to supported workflow, unsupported workflow,
   or immediate escalation.
4. Retrieval fetches relevant help docs, macros, SOPs, past resolved cases, and
   policy constraints.
5. Workflow state-machine calls approved tools, such as order lookup or
   subscription status, under least-privilege credentials.
6. Policy guard checks confidence, customer sentiment, regulated content,
   refund/credit threshold, and source coverage.
7. Agent drafts answer/action or creates escalation packet.
8. Review queue or live sender writes back to help desk.
9. Audit event records source docs, model, prompt version, tool calls, outcome,
   reviewer, latency, and cost.

**Human-in-the-loop points:** Workflow activation, policy edits, knowledge-base
source approval, refund/credit thresholds, low-confidence cases, negative
sentiment, regulated content, customer complaints, and first 1-2 weeks of live
traffic.

**Integration endpoints:** Help desk webhooks, ticket read/write APIs, knowledge
base export, CRM/customer profile, order/subscription/billing API, identity
provider, and analytics export.

**Failure handling:** If the help desk API, order API, billing API, or retrieval
service times out, the agent escalates instead of guessing. If source coverage
is incomplete, the agent says it cannot verify and routes to a human. If a
customer requests a regulated or high-risk action, the workflow blocks and
requires reviewer approval.

### Critical Design Decisions

1. **Resolution layer, not help desk replacement**
   - Alternatives: build a full help desk, chatbot widget, or CCaaS module.
   - Rationale: incumbent data gravity is strong; the wedge is economics, not
     system-of-record migration.
   - Reconsider if: buyer lacks a usable help desk or wants a greenfield support
     platform.
2. **State-machine workflows before open-ended autonomy**
   - Alternatives: free-form agent with broad tool access.
   - Rationale: support combines untrusted customer input with privileged tools;
     constrained workflows are safer and easier to evaluate.
   - Reconsider if: evals show stable performance across many workflows and
     buyer risk tolerance is high.
3. **Verified outcome pricing**
  - Alternatives: per-seat SaaS, token usage, or monthly platform fee only.
  - Rationale: buyer pain is tied to per-seat and per-hour capacity. Outcome
    pricing makes the wedge obvious.
  - Reconsider if: workflows have high variance or outcome attribution is
    disputed.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/support/intake` | Ingest ticket webhooks or batch cases | Ticket payload, source system, tenant ID | Accepted case ID | Service token + tenant auth | Return 4xx on malformed payload; queue retry on transient failure |
| GET | `/api/support/cases/:caseId` | Fetch workflow state and audit trail | Case ID | Current state, source citations, action log | RBAC session | 404 if missing; 403 on tenant mismatch |
| POST | `/api/support/cases/:caseId/review` | Send draft for human approval | Draft text, action request, reviewer note | Approval state | Reviewer role | Block writeback if required fields are missing |
| POST | `/api/support/cases/:caseId/escalate` | Escalate unsafe or low-confidence cases | Escalation reason, queue target | Escalation packet ID | Support admin or reviewer | No-op if case already closed |
| POST | `/api/support/evals/run` | Run offline evals on tickets/macros | Workflow ID, eval set, policy version | Eval summary | Admin token | Fail closed if eval set is incomplete |

### Folder / Module Structure

- `app/(console)/support/` for the operator console, queue, and case detail views.
- `app/api/support/` for intake, review, escalation, and eval endpoints.
- `services/support-agent/` for orchestration, policy checks, and response drafting.
- `services/connectors/zendesk/`, `services/connectors/shopify/`, `services/connectors/stripe/` for least-privilege adapters.
- `workers/evals/` for offline replay, regression tests, and safety checks.
- `lib/policies/` for workflow rules, thresholds, and approval gates.
- `lib/audit/` for source citation, prompt version, and tool-call logging.
- `tests/support/` for edge cases, data-boundary tests, and smoke tests.

### Environment Variables

- `DATABASE_URL`: Postgres connection for cases, policies, and audit events.
- `REDIS_URL`: queue and async job backend.
- `MODEL_ROUTER_API_KEY`: provider-router credential.
- `MODEL_ROUTER_BASE_URL`: model gateway endpoint.
- `ZENDESK_SUBDOMAIN`: help desk tenant identifier.
- `ZENDESK_API_TOKEN`: help desk read/write token.
- `SHOPIFY_API_KEY`: order and fulfillment lookup access.
- `STRIPE_SECRET_KEY`: subscription and billing lookup access.
- `SENTRY_DSN`: error tracking.
- `OTEL_EXPORTER_OTLP_ENDPOINT`: traces and metrics export.
- `APP_BASE_URL`: callback and webhook target for the console.

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Help desk system of record | High | Existing Zendesk/Freshdesk/Salesforce/Intercom/Gorgias licenses already own the history | BUY/KEEP | Do not rebuild ticketing, routing, permissions, reporting, and conversation history in the MVP. |
| Resolution workflow layer | Medium | Incumbent AI is improving but tied to vendor roadmap, pricing, and workflow constraints | BUILD | This is the strategic wedge: narrow workflows, explicit policy gates, and outcome economics. |
| Knowledge retrieval | Low-Medium | Generic KB bots exist, but support needs policy-aware source citation and workflow-specific retrieval | BUILD | Retrieval quality directly determines trust and safe escalation. |
| Customer/order/billing integrations | Medium | Native connectors exist but usually support generic automations | HYBRID | Use APIs and existing tools, but build workflow-specific adapters and permissions. |
| Human review queue | Low-Medium | Help desks have internal notes and assignment queues | HYBRID | Use the help desk for final record, but build a focused review surface for evals/audit. |
| Analytics and evaluation | Medium | Help desk reports are seat/ticket oriented; AI vendors report deflection/resolution | BUILD | Need verified resolution, escalation reason, policy failure, cost, and source coverage. |
| BPO labor | High recurring | Quote-based, delayed onboarding, ongoing management | REPLACE PARTIALLY | MVP targets tier-1 routine volume, not all support operations. |

**Bottom line:**

- **Annual SaaS spend if buying everything:** depends on seat count and vendor,
  but public examples show seat-based plans ranging from Freshdesk Growth at
  `$19/agent/month` to Salesforce Service Cloud Enterprise at
  `$165/user/month`, before BPO labor or AI usage.
- **One-time MVP build estimate:** 4-week pilot build with one help desk, two
  workflows, two operational systems, and evaluation/audit layer.
- **Recommended split:** keep incumbent help desk and operational systems; build
  the resolution layer, evaluation harness, policy gates, and outcome reporting.
- **Payback period:** should be modeled per buyer. Strong candidate if the
  selected workflows exceed 2,000 monthly contacts and current cost per contact
  is materially above expected verified-resolution cost plus review overhead.

## 5. MVP ROI Business Case

### Current-State Cost Model

Use ranges; do not overstate precision.

- **Help desk software:** public seat pricing examples include Freshdesk at
  `$19-$89/agent/month`, Salesforce Service Cloud at `$25-$165/user/month`, and
  Intercom plans around `$19-$132/seat/month` depending tier and promotion.
- **AI add-ons/outcome tools:** Intercom Fin is priced around `$0.99` per
  outcome; Gorgias AI Agent is around `$0.90-$1.00` per resolved conversation;
  Freshdesk includes some Freddy AI sessions and then usage add-ons.
- **Labor:** internal agents or BPO staff handle routine contacts, with cost
  driven by handle time, QA, management, training, shrinkage, and staffing
  coverage.
- **Error/rework:** repeated customer story, bad bot handoff, incorrect policy
  promises, and escalations that lack context.

### Agentic MVP Cost Model

- **Build:** fixed 30-day pilot cost covering connector, retrieval, workflow
  routines, review queue, audit logs, and eval dashboard.
- **Monthly run:** model/API calls, vector retrieval, hosting, observability,
  and support.
- **Maintenance:** workflow tuning, source refresh, policy updates, eval set
  expansion, and new integration upkeep.

### Pricing Options

1. **Low-risk pilot:** fixed fee for first 1,000 verified resolutions or 30-day
   shadow/live pilot, with agreed success metrics.
2. **Usage/outcome model:** per verified resolution, with non-billable
   escalations and policy-failure exclusions.
3. **Enterprise package:** monthly platform minimum plus lower per-resolution
   fee, including compliance controls, custom integrations, and evaluation
   reporting.

### Scenario Model

Use buyer-specific inputs where available. Default formulas:

```text
Current monthly tier-1 cost =
  eligible contacts * current cost per handled contact

Agentic monthly cost =
  platform minimum + (verified resolutions * outcome fee)
  + (escalated contacts * human review cost)

Monthly value =
  current monthly tier-1 cost avoided - agentic monthly cost

Payback period =
  pilot/build cost / monthly value
```

Illustrative assumptions, not universal claims:

- Loaded human/BPO cost per handled tier-1 contact: `$2.50-$6.00`.
- Outcome fee target: `$0.75-$1.25` per verified resolution, benchmarked
  against public AI-support outcome pricing around `$0.90-$0.99`.
- Review cost for escalated contacts: buyer-specific; assume human review
  remains for low-confidence, regulated, refund/credit, or complaint cases.
- Pilot/build cost: set by commercial offer; model examples below assume
  `$25K-$45K` for a focused 30-day pilot.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | 2,000 eligible contacts/mo, 20% verified resolution, `$3.00` current cost/contact, `$1.00` outcome fee, high review overhead, `$25K` pilot | Slow | 9-18 months | Keep as learning pilot only if strategic account is valuable. |
| Base | 5,000 eligible contacts/mo, 40% verified resolution, `$4.00` current cost/contact, `$1.00` outcome fee, moderate review overhead, `$35K` pilot | Moderate | 3-6 months | Credible first commercial case if buyer has meaningful BPO/internal labor cost. |
| Upside | 10,000+ eligible contacts/mo, 60%+ verified resolution, `$5.00` current cost/contact, `$0.90` outcome fee, stable evals, `$45K` pilot | Fast | 1-3 months | Strong wedge for renewal/renegotiation against seats or BPO expansion. |

**No-go condition:** If the selected workflows cannot produce at least 1,000
monthly eligible contacts, cannot be verified objectively, or require
unreviewed money-moving/regulatory decisions, the MVP should not be sold as an
outcome-priced automation pilot.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Zendesk | Help desk system of record | Enterprise ticketing, knowledge base, routing, analytics, AI agents | Sales-led AI details; heavy implementation/admin burden in many accounts | Public pricing plus contact-sales AI agent detail; outcome-based AI pricing reported | Zendesk pricing, TechRadar |
| Intercom / Fin | Help desk + AI agent | Clear outcome pricing and standalone Fin | Still has seat-based help desk plans and minimums | Fin about `$0.99/outcome`; seats for help desk plans | Intercom pricing |
| Freshdesk / Freddy AI | Help desk + AI sessions | Transparent seat pricing and SMB/midmarket reach | AI sessions added to existing plan economics | `$19-$89/agent/month`; AI sessions add-on | Freshworks pricing |
| Salesforce Service Cloud | Enterprise CRM/service suite | Deep CRM integration and enterprise trust | High per-user enterprise pricing and implementation complexity | `$25-$165/user/month` public tiers | Salesforce pricing |
| Gorgias AI Agent | Ecommerce support | Strong vertical workflow fit and volume pricing | More ecommerce-specific; still platform-bound | ticket-volume plans plus AI resolved conversation pricing | Gorgias pricing |
| Ada | AI-native support agent | Enterprise AI support positioning and automation focus | Sales-led pricing and platform adoption motion | Pricing/demo funnel | Ada |
| NICE / Genesys / Five9 | CCaaS/contact-center | Voice, routing, workforce, QA, telephony depth | Heavier enterprise contact-center footprint; not a narrow tier-1 resolution wedge | Enterprise sales-led | Vendor category research |
| BPO providers | Human labor | Operational accountability and staffing | Slow ramp, quote-based pricing, less scalable economics for repetitive contacts | Quote/transaction/hour/outcome models | Helpware, SupportNinja |

**Direct threats:** Intercom Fin and Gorgias AI Agent are the most direct
commercial threats because they already sell the outcome-pricing language.
Zendesk and Salesforce remain the system-of-record threats because they control
procurement and customer data.

**Table-stakes features to copy:** source-grounded replies, human fallback,
ticket history awareness, workflow integrations, admin analytics, and clear
resolution reporting.

**Things not to build:** a new help desk, new CCaaS platform, generic chatbot
builder, full BPO operations layer, or open-ended customer-facing agent with
unbounded tools.

**Three exploitable gaps:**

1. Outcome economics that help buyers renegotiate seat/BPO spend.
2. Faster narrow-workflow deployment than enterprise suite AI modules.
3. Better auditability and fallback design than generic chatbot deployments.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| Workflow classification | 200 labeled historic tickets per selected workflow | Eval job runs | At least agreed precision/recall threshold is met before live traffic | Eval dashboard confusion matrix |
| Source-grounded answer | Customer asks supported policy question | Agent drafts reply | Reply cites approved source and does not invent policy | Source citation in audit log |
| Tool-backed resolution | Customer asks order/refund/status question | Agent calls approved system | Agent uses current system data and records tool result | Tool-call log and help desk note |
| Human fallback | Confidence below threshold or negative sentiment detected | Agent processes ticket | Ticket escalates with summary and recommended next action | Help desk tag/internal note |
| Money-moving guard | Refund/credit/cancel threshold exceeded | Agent reaches action step | Agent blocks autonomous action and requests approval | Audit event and reviewer queue |
| Live pilot reporting | 7 days of limited traffic completes | Manager opens dashboard | Resolution, escalation, failure, latency, and cost metrics are visible | Dashboard export |

**Edge cases:**

- **Empty state:** missing customer profile or order ID routes to human or asks
  a clarifying question.
- **Error state:** help desk/API failure creates internal note and escalates.
- **Invalid input:** abusive, prompt-injection, or irrelevant customer text is
  sanitized and routed according to policy.
- **Slow dependency:** if an operational API exceeds timeout, do not hallucinate
  status; escalate with timeout reason.
- **Concurrent action:** duplicate webhooks must not issue duplicate responses
  or repeated refunds; enforce idempotency keys per ticket/action.
- **Auth/data boundary:** user A's ticket must never expose user B's profile,
  order, subscription, or billing data.

## 8. Data Architecture Lite

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| Tickets/conversations | Help desk API/webhook | Minimal case cache + audit log | Help desk | Webhook plus backfill | Tenant and ticket ID checks |
| Knowledge docs/macros | Help center/export | Document store + embeddings | Approved help center/SOP repo | Scheduled refresh | Source approval and versioning |
| Customer profile | CRM/help desk | Read-through cache | CRM/help desk | API lookup | Customer ID match |
| Orders/subscriptions/billing | Shopify/Stripe/Recurly/etc. | Tool-call result only unless needed | Operational system | On-demand | No stale money-moving decisions |
| Agent outputs | Resolution layer | Postgres audit/event tables | Resolution layer | Per action | Prompt/model/source/tool trace |
| Evaluation labels | Historic tickets + reviewer labels | Postgres eval tables | Buyer-approved eval set | Manual/batch | Label owner and version |

**Analytics questions:**

1. Which workflows produce verified resolutions at acceptable risk?
   - Event: `case_resolved_verified`
   - Attributes: workflow, source coverage, tool calls, confidence, latency.
2. Why do cases escalate?
   - Event: `case_escalated`
   - Attributes: reason, missing data, confidence, sentiment, regulated flag.
3. What is the cost per verified resolution?
   - Event: `case_cost_recorded`
   - Attributes: model cost, tool cost, review time, workflow.
4. Where is the knowledge base weak?
   - Event: `source_gap_detected`
   - Attributes: question type, missing source, escalation outcome.
5. Is customer experience improving or degrading?
   - Event: `post_resolution_feedback`
   - Attributes: CSAT/tNPS proxy, reopened ticket, complaint, fallback.

**Privacy/security:** support tickets may contain PII, payment references,
health/financial/insurance context, complaints, credentials, or protected
customer data. Apply tenant isolation, role-based access, encryption, retention
limits, redaction before model calls when possible, source snapshots, and
customer data deletion workflows. For regulated accounts, require DPA/BAA or
equivalent contract review and approved model/data-retention settings.

## 9. Deployment Sequencing

**Pre-deploy checklist:**

- Confirm selected workflows and out-of-scope policies.
- Confirm help desk and operational API scopes are least privilege.
- Confirm no production customer messages are sent during shadow mode.
- Confirm redaction, audit logs, idempotency, and escalation are tested.
- Confirm eval set has human-approved labels.

**Staging:**

- Use sandbox help desk or copied non-production ticket data.
- Run historic ticket evals and adversarial prompt-injection tests.
- Verify source citations, timeout behavior, and fallback paths.
- Verify no secrets, payment details, or cross-customer data leak into logs.

**Production sequence:**

1. Connect production help desk with read-only and internal-note permissions.
2. Run shadow mode on selected workflows for at least one week or agreed volume.
3. Review eval dashboard with buyer support lead.
4. Enable live responses for the safest workflow and limited percentage of
   traffic.
5. Keep money-moving actions approval-gated.
6. Increase volume only after policy-failure and escalation rates are stable.

**Smoke test:**

- Create test ticket for selected workflow.
- Confirm source-grounded answer.
- Confirm operational lookup.
- Confirm escalation on missing data.
- Confirm human handoff summary.
- Confirm audit log includes source, model, prompt version, tool call, and
  reviewer/live status.

**Rollback:**

- Disable live response flag.
- Keep internal-note/shadow mode available.
- Remove write scopes if needed.
- Export audit logs and failed cases for review.
- Notify support leads with customer-facing messaging if any bad response was
  sent.

## 10. Post-Launch Iteration Plan

**Metrics:**

- **Activation:** percent of selected workflow tickets processed in shadow/live
  mode with complete source and tool context.
- **Retention:** weekly usage by support managers/reviewers and continued
  workflow expansion requests.
- **Revenue/willingness-to-pay:** buyer agrees to pay per verified resolution,
  fixed pilot extension, or expanded workflow package.

**Week 1 after launch:** Fix bugs, eval failures, source gaps, and escalation
quality. No new workflows.

**Week 2:** Interview 5 support agents/managers who reviewed escalations. Find
the highest-friction unresolved reason.

**Week 3:** Improve one workflow or add one adjacent deterministic workflow.
Do not expand channels, voice, or languages yet.

**Week 4:** Measure whether verified resolution rate increased without raising
policy failures, bad handoffs, or customer complaints.

**Pivot signals:**

- Less than 20% verified resolution on selected workflows after sufficient
  tuning means the workflows are not deterministic enough or source/tool access
  is inadequate.
- More than 5% policy-failure or unsafe-action rate in shadow mode means the
  workflow must remain human-assist only.
- Buyer refuses outcome pricing after seeing verified results means the wedge
  should shift to agent-assist, QA, or BPO-renegotiation analytics.

## Source Notes

- Intercom Pricing - https://www.intercom.com/pricing - accessed 2026-06-26 -
  Fin outcome pricing and help desk seat tiers.
- Freshdesk Pricing - https://www.freshworks.com/freshdesk/pricing/ - accessed
  2026-06-26 - seat pricing and Freddy AI session economics.
- Salesforce Service Cloud Pricing -
  https://www.salesforce.com/products/service-cloud/pricing/ - accessed
  2026-06-26 - user-based Service Cloud tiers.
- Gorgias Pricing - https://www.gorgias.com/pricing - accessed 2026-06-26 -
  ticket-volume and AI Agent resolved-conversation pricing.
- Zendesk Pricing - https://www.zendesk.com/pricing/ - accessed 2026-06-26 -
  help desk and AI positioning.
- Zendesk CX Trends 2026 - https://cxtrends.zendesk.com/ - accessed
  2026-06-26 - customer expectations and AI explanation data.
- Helpware CX Pricing - https://helpware.com/cx/pricing - accessed
  2026-06-26 - BPO pricing model friction and hiring lead time.
- SupportNinja Pricing - https://www.supportninja.com/pricing - accessed
  2026-06-26 - quote-based BPO pricing friction.
- Ada pricing funnel - https://www.ada.cx/pricing/ - accessed 2026-06-26 -
  AI support vendor sales-led pricing motion.
- OWASP Top 10 for LLM Applications -
  https://owasp.org/www-project-top-10-for-large-language-model-applications/ -
  LLM security risks relevant to customer-facing agents.
- NIST AI Risk Management Framework -
  https://airc.nist.gov/airmf-resources/airmf/ - AI governance reference.
- Kagan, Hathaway, Dada, "Deploying Chatbots in Customer Service" -
  https://arxiv.org/abs/2504.06145 - chatbot gatekeeper aversion and trust
  design.
- Gupta et al., "Building Customer Support AI Agents at 100M-User Scale" -
  https://arxiv.org/abs/2606.08867 - production support-agent deployment
  evidence.
- TechRadar, Zendesk outcome-based AI pricing -
  https://www.techradar.com/pro/zendesk-links-ai-pricing-to-verified-resolution-outcomes -
  outcome-pricing market signal.
- ITPro, AI agent rollback/governance survey coverage -
  https://www.itpro.com/technology/artificial-intelligence/ai-agents-arent-cutting-it-in-customer-service -
  governance risk signal.
