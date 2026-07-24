---
status: reviewed
use_case: "AI Shopping / Sales Consultant"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# AI Shopping / Sales Consultant Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** ecommerce and merchandising leaders.

**Later ICPs:** conversion teams once one storefront proves the guided-selling
flow.

**Pain wedge:** static recommendation widgets miss conversational intent.

**Incumbent weakness:** guided-selling SaaS is rules-heavy and not truly
personalized.

**Agentic disruption thesis:** turn live conversation into in-stock, context-
aware recommendations.

**Why now:** storefront AI is expected, and conversion gains are measurable.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 27/30**

The score is inferred from common recommendation spend, storefront AI
expectations, and the gap between static widgets and conversational intent.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

**Who has the problem:** ecommerce teams wanting higher conversion and AOV.

**Current workaround:** static "customers also bought" widgets and manual merch
rules.

**Switching reason:** better conversion and cross-sell performance.

**Payment signal:** recommendation SaaS and merchandising teams.

**30-day reachability:** one storefront and one catalog can prove the wedge.

**Verdict: PROCEED, but keep recommendations in stock.**

## 2. The 30-Day Scope Definition

**Project name:** Storefront Sales Copilot

**Validated problem:** shoppers need personalized product guidance in context.

**Target user:** shopper and ecommerce merchandiser.

**Core hypothesis:** the agent can recommend in-stock bundles from natural-
language intent.

### In Scope

1. **Conversational intent**
   - Acceptance criterion: shopper can ask for help in natural language.
2. **In-stock recommendations**
   - Acceptance criterion: recommended items are available and priced.
3. **Cart support**
   - Acceptance criterion: the agent can produce a cart-ready recommendation.

### Explicitly Out Of Scope

- Building a massive visual rule builder.
- Offline recommendation-only widgets.
- Out-of-stock or non-verifiable recommendations.
- Replacing the storefront.

### Week-By-Week Milestones

- **Week 1:** connect one storefront and one catalog.
- **Week 2:** build intent parsing and guardrails.
- **Week 3:** generate recommendations and cart support.
- **Week 4:** pilot one conversion path.

**Dependencies:** storefront API, catalog feed, and merch owner.

**Acceptance test:** one shopper conversation produces a valid in-stock
recommendation set.

**Top risks:** stale inventory, wrong fit, and conversion trust.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: storefront chat widget.
- Backend: FastAPI or Node service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for catalog and rules.
- Auth: storefront / SSO plus catalog API credentials.
- Database: Postgres for conversations, products, carts, and feedback.
- Observability: OpenTelemetry and conversion metrics.
- Hosting: cloud app with queue worker.

**Architecture:** conversation -> intent -> retrieve -> rank -> verify -> cart.
The agent is a contextual recommendation layer, not a static widget.

**Critical design decisions:**

1. Keep recommendations in stock.
2. Do not build a giant rules editor.
3. Use conversational intent plus live catalog data.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/shop/query` | ingest shopper intent | message payload | session id | service token | retry queue |
| POST | `/api/shop/recommend` | generate recommendations | session id | ranked items | service token | fallback to browse |
| POST | `/api/shop/cart` | prepare cart | session id, item ids | cart payload | service token | block on missing stock |

### Folder / Module Structure

- `app/shop/`
- `app/api/shop/`
- `services/intent/`
- `services/rank/`
- `workers/cart/`
- `lib/catalog/`

### Environment Variables

- `STORE_API_KEY`
- `CATALOG_API_KEY`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `ANALYTICS_KEY`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Guided selling | medium | rules-heavy and not personal | BUILD | core wedge |
| Catalog / storefront | high | already exists | BUY / REUSE | source of truth already exists |
| Recommendation ranker | medium | static widgets are weak | BUILD | high leverage |

**Bottom line:** reuse storefront and catalog, build the conversational sales
copilot.

## 5. MVP ROI Business Case

**Current-state cost model:** conversion losses, merch rule maintenance, and
manual support.

**Agentic MVP cost model:** intent handling, catalog lookups, ranking, and
chat support.

**Pricing options:**

1. Fixed pilot.
2. Per active storefront.
3. Enterprise conversion package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low traffic | 12-18 months | month 14+ | learning only |
| Base | measurable AOV lift | 6-9 months | month 8-12 | strong fit |
| Upside | high conversion improvement | 3-5 months | month 4-6 | strong leverage |

**Formulas**

```text
Monthly value =
  conversion lift + AOV lift + support reduction
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if inventory cannot be verified in real time, do not
present cart-ready recommendations.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Salesforce CPQ / Revenue Cloud | CPQ | CRM integration | migration / SI burden | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/GuidedSelling_CPQ_Competitor_Teardown.md` |
| DealHub | guided selling | modern CPQ | expensive scaling | per-user | `runs/2026-06-26-agentic-opportunity-blueprints/source/GuidedSelling_CPQ_Competitor_Teardown.md` |
| Conga | document / CPQ | pricing governance | complex enterprise pricing | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/GuidedSelling_CPQ_Competitor_Teardown.md` |
| Oracle CPQ | CPQ | enterprise depth | high friction | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/GuidedSelling_CPQ_Competitor_Teardown.md` |

**Direct threats:** DealHub and Salesforce Revenue Cloud.

**What not to build:** a massive visual rule builder.

**Agentic wedge:** conversational quoting with live, in-stock recommendations.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| intent parse | shopper asks for help | agent runs | intent recognized | scenario test |
| in-stock recs | catalog loaded | rank runs | recommended items available | stock test |
| cart | shopper accepts | cart runs | items added successfully | integration test |

### Edge Cases

- Out-of-stock item.
- Conflicting style preferences.
- Price mismatch.
- Duplicate intent.
- Catalog outage.
- Cart restriction.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| conversations | storefront chat | session table | storefront | realtime | validation |
| catalog | product feed | catalog table | catalog system | batch / realtime | freshness |
| recommendations | agent | rec table | agent | realtime | stock verification |
| carts | storefront | cart table | storefront | realtime | idempotency |

**Retention and deletion:** retain conversion lineage and recommendation logs,
delete transient prompts after retention, and keep merchandising feedback.

**Privacy/security:** commerce data should be tenant-separated and logged with
inventory / pricing provenance.

**Analytics questions:** which conversational intents convert best and which
recommendation patterns create the most abandoned carts?

## 9. Deployment Sequencing

**Pre-deploy checklist:** one storefront, one catalog, merch owner, rollback
flag.

**Staging:** chat-only, then recommendation-only.

**Production sequence:** one conversion path, one catalog feed, one approval
owner.

**Smoke test:** one shopper query returns a valid in-stock recommendation.

**Rollback:** disable cart support and keep chat guidance only.

**Observability:**

- Logs: intent, ranking, stock check, cart action.
- Metrics: conversion, AOV, abandonment, rec rate.
- Alerts: stock mismatch, catalog failure, cart error.
- Dashboards: recommended-to-purchased and abandonment hotspots.

## 10. Post-Launch Iteration Plan

**Metrics:** conversion lift, AOV lift, and support reduction.

**Week-by-week:**

- Week 1: add one more catalog segment.
- Week 2: improve ranking quality.
- Week 3: tighten stock verification.
- Week 4: package for adjacent storefronts.

**Pivot signals:** keep it in-stock only if trust drops, and avoid rule-editor
scope creep.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/GuidedSelling_CPQ_Competitor_Teardown.md` - guided-selling incumbent map and conversational-quoting wedge.
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/GuidedSelling_CPQ_Disruptive_Teardown.md` - incumbent map and conversational quoting wedge.
- Salesforce homepage - https://www.salesforce.com/ - accessed 2026-06-26 - CPQ and Revenue Cloud backdrop.
- DealHub - https://dealhub.io/ - accessed 2026-06-26 - agentic quote-to-revenue and CPQ reference.
- Oracle CPQ - https://www.oracle.com/cx/sales/cpq/ - accessed 2026-06-26 - enterprise CPQ reference.
- Best Buy - https://www.bestbuy.com/ - accessed 2026-06-26 - retail sales-assist backdrop.
- These incumbents reinforce that the wedge is conversational intent and in-stock recommendations, not a giant visual rule builder.
- The storefront must remain the system of record; the agent sits in front of catalog and cart data.
- A conversion agent should optimize for accurate product fit, inventory truth, and cart readiness before any upsell logic.
- In practice, the buyer wants fewer abandoned sessions and less merch-rule maintenance, not a second CPQ admin console.
- This also means product truth has to dominate persuasion: if the catalog says the item is unavailable or incompatible, the agent should say that plainly.
- The best proof is a narrow conversion path with measured lift, not a broad merchandising rewrite.
- Conversion confidence matters as much as recommendation quality, because shoppers abandon faster when the bot over-promises or hides stock constraints.
