---
status: reviewed
use_case: "Dynamic Competitor Pricing Agent"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence: high
---

# Dynamic Competitor Pricing Agent Master Implementation Blueprint

## Executive Positioning
- Target buyer: ecommerce pricing and growth leaders.
- Pain wedge: manual repricing lags competitor moves.
- Incumbent weakness: repricing tools break when DOMs change or rules get stale.
- Agentic disruption thesis: monitor competitor prices and update shop prices within margin guardrails.
- Why now: buy-box competition rewards responsiveness.

## 1. Problem-Solution Fit Diagnostic
Score 26/30
- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 9/10

Evidence:
- Who has the problem: ecommerce operators managing many SKUs.
- Last-time/recency evidence: repricing tools and scraping discussions remain active.
- Current workaround: manual price checks.
- Switching reason: faster response and buy-box protection.
- Payment signal: repricing software and margin management.
- 30-day reachability: one SKU set and one competitor list can prove the wedge.

Verdict: PROCEED

## 2. 30-Day Scope Definition
- Project name: Reprice Copilot
- Validated problem: competitor prices and stock status change frequently.
- Target user: ecommerce pricing manager.
- Core hypothesis: the agent can scrape competitor pages and adjust prices safely.

In scope:
1. Competitor monitoring.
2. Price comparison and floor-margin validation.
3. Shopify price updates.

Explicitly out of scope:
- Full marketplace optimization.
- Autonomous promo strategy without review.
- Violating legal or site policy constraints.

Week-by-week milestones:
- Week 1: top 3 competitor scrapers.
- Week 2: validation logic.
- Week 3: alerting system.
- Week 4: automated updates for limited SKUs.

Dependencies:
- competitor URLs, pricing floors, and Shopify API.

Acceptance test:
- competitor price and stock are identified correctly and margin floors are respected.

Top 3 risks + mitigations:
- DOM changes - agentic parsing
- margin erosion - floor guardrails
- policy issues - compliance checks

## 3. Tech Stack + Architecture Design
Recommended stack:
- Frontend: pricing dashboard.
- Backend: Python FastAPI.
- Agent orchestration: Apify/Playwright plus LLM validation.
- Retrieval/data layer: Postgres for pricing history.
- Auth: Shopify and admin SSO.
- Database: Postgres for SKUs, prices, and competitor snapshots.
- Observability: scrape health and price-change logs.
- Hosting: containerized service with browser workers.

Architecture:
- System boundary: competitor page -> scrape -> validate -> update Shopify.
- Runtime topology: scheduler -> browser fetch -> parse -> compare -> writeback.
- Core agent loop: detect competitor price, verify stock, compare margin floor, decide update.
- Human-in-the-loop points: aggressive price moves and exceptions.
- Integration endpoints: Shopify, competitor URLs, alerting.
- Failure handling: if scrape confidence is low, hold price and alert.

Database schema / data model:
| Table / Entity | Purpose | Key Fields | Indexes | Security / Tenancy |
|---|---|---|---|---|
| skus | products | id, tenant_id, sku, floor_price | tenant_id, sku | tenant-scoped |
| competitor_snapshots | scraped prices | id, sku_id, competitor, price, stock, ts | sku_id, competitor, ts | audit tracked |
| reprices | update log | id, sku_id, old_price, new_price, reason | sku_id, ts | immutable |
| alerts | exceptions | id, sku_id, issue, status | sku_id, status | reviewable |

API surface:
| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | /api/snapshots/run | scrape competitors | sku set | snapshot batch | service auth | partial on scrape fail |
| POST | /api/prices/decide | decide repricing | sku, snapshot | decision | service auth | hold if low confidence |
| POST | /api/prices/apply | update store price | approved decision | status | service auth | queue on Shopify outage |

Integration plan:
| System | Direction | Data / Action | Auth | Failure Handling |
|---|---|---|---|---|
| competitor sites | inbound | price/stock scrape | browser worker | re-run or alert |
| Shopify | outbound | price update | API token | queue if unavailable |
| alerting | outbound | exceptions | API key | retry later |

Folder/module structure:
- `app/api/`
- `services/scrape/`
- `services/compare/`
- `services/price/`
- `services/alert/`

Environment variables:
- `SHOPIFY_API_TOKEN`
- `CRAWL_QUEUE_URL`
- `MARGIN_FLOOR_RULES`
- `ALERT_CHANNEL`
- `LLM_API_KEY`

Critical design decisions:
1. Margin floor first because revenue protection matters.
2. Browser workers because DOMs change.
3. Hold when uncertain because bad repricing is worse than stale pricing.

## 4. Build vs Buy Decision Matrix
| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| repricing agent | moderate | % of revenue repricers take a cut | Build | fixed-cost compute is the wedge |
| commerce platform | low | already used | Buy | keep SoR |
| scrapers | low | existing browser tooling | Buy/Reuse | don't overbuild |

Bottom line:
- Annual SaaS spend if buying: repricers and monitoring tools.
- One-time MVP build estimate: $40k-$80k equivalent effort.
- Recommended split: buy commerce platform, build repricing worker.
- Payback period: under 12 months if conversions lift.

## 5. MVP ROI Business Case
Current-state cost model:
- Software: repricing tools.
- Labor: merchandiser time.
- Services/admin: manual price checks.
- Error/rework: missed buy-box opportunities.

Agentic MVP cost model:
- Build: one scrape/compare/update pipeline.
- Monthly run: browser and API usage.
- Maintenance: selector and margin tuning.

Pricing options:
1. Low-risk pilot: one SKU set.
2. Usage/outcome model: per update.
3. Enterprise package: repricing plus analytics.

ROI scenarios:
| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Base | +15% lift | 6-10 months | month 8-12 | standard |
| Upside | strong buy-box gains | 3-6 months | month 4-6 | high SKU count |
| Downside | unstable competitor sites | 12-18 months | month 14+ | narrower scope |

No-go condition: if competitor scraping is not reliable, the system should remain alert-only.

## 6. Competitor Product Teardown
Competitor map:
| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| enterprise repricers | repricing | turnkey | revenue share | % of revenue | market standard |
| scraping bots | scraping | fast | brittle | usage-based | market standard |
| manual checks | labor | controlled | slow | labor-only | market standard |

Direct threats:
- repricing SaaS
- scraping tools
- manual price checks

Table-stakes features to copy:
- competitor monitoring
- stock check
- floor-margin validation

Things not to build:
- marketplace
- tax engine
- arbitrary price automation

Three exploitable gaps:
- DOM drift
- margin guardrails
- stock-aware pricing

## 7. Acceptance Criteria + Test Plan
Feature test plan:
| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| competitor price | page changes | scrape runs | price captured | fixture test |
| stock status | out-of-stock item | scrape runs | no race to bottom | negative test |
| Shopify update | valid decision | update runs | price changes | integration test |

Edge cases:
- Empty state: no competitor URLs.
- Error state: scraper failure alerts.
- Invalid input: unsupported SKU rejected.
- Slow dependency: update held.
- Concurrent action: duplicate SKU idempotent.
- Auth/data boundary: tenant store isolated.

## 8. Data Architecture Lite
Data domains:
| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| competitor data | web scrape | snapshot table | competitor site | scheduled | confidence threshold |
| floor rules | merchant | rules table | merch | versioned | approval |
| prices | store | price table | Shopify | realtime | audit log |
| alerts | system | alert table | alerting | realtime | immutable log |

Retention and deletion:
- Data retained: price history and snapshots.
- Data deleted: transient scrape artifacts.
- Audit retained: repricing decisions.

Analytics questions:
1. Which SKUs benefit most from dynamic repricing?

Privacy/security:
- legal/scrape compliance
- margin floor enforcement
- tenant isolation

## 9. Deployment Sequencing
Pre-deploy checklist:
- URLs approved
- margin floor rules loaded
- Shopify credentials verified

Staging:
- top 3 competitors only.

Production sequence:
- shadow -> alert-only -> automated updates.

Smoke test:
- one SKU updates correctly.

Rollback:
- disable updates and keep alerts.

Observability:
- Logs: scrape, compare, update, alert.
- Metrics: scrape success, price moves, conversion lift.
- Alerts: scrape failure, floor breach, Shopify error.
- Dashboards: by SKU set.

## 10. Post-Launch Iteration Plan
Metrics:
- Activation: SKUs tracked.
- Retention: repeat use.
- Revenue/willingness-to-pay: conversion and margin.

Week-by-week:
- Week 1: add more competitors.
- Week 2: improve stock handling.
- Week 3: add shipping cost inputs.
- Week 4: widen SKU coverage.

Pivot signals:
- if scrape reliability is weak, stay on alerts
- if margin erosion is high, tighten floor rules
- if conversion impact is low, narrow to hero SKUs

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Dynamic_Competitor_Pricing_Disruptive_Teardown.md` - upstream teardown dossier for the pricing-intelligence wedge.
- Official reference points reviewed: Pricefx, Competera, Omnia Retail, and Revionics product pages.
- Shopify - https://www.shopify.com/ - accessed 2026-06-26 - store backdrop.
- Apify - https://apify.com/ - accessed 2026-06-26 - scraping backdrop.
