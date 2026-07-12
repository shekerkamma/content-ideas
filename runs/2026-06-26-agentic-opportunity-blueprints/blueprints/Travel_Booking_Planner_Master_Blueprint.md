---
status: reviewed
use_case: "Travel & Booking Planner"
phase: "phase-2"
last_updated: "2026-06-26"
source_confidence:
  problem: medium-high
  competitor: medium-high
  pricing: medium-high
  implementation: medium-high
---

# Travel & Booking Planner Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** travel ops, concierge product, or booking platform leader.

**Later ICPs:** corporate travel or concierge teams once one itinerary flow
proves the intent-to-book loop.

**Pain wedge:** itinerary planning is fragmented, and live booking is still
clumsy.

**Incumbent weakness:** search-and-filter UIs and white-label portals slow the
conversion path.

**Agentic disruption thesis:** translate intent into a verified itinerary and
booking-ready cart.

**Why now:** travelers want fewer steps, not more browsing.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 23/30**

The score is inferred from fragmented booking flows, opaque travel UX, and the
fact that live availability still matters.

- Problem realness: 8/10
- Solution fit: 8/10
- Buying signal + reachability: 7/10

**Who has the problem:** consumers, travel agents, and concierge teams.

**Current workaround:** search, filters, and manual itinerary assembly.

**Switching reason:** speed and conversion.

**Payment signal:** booking and travel-tech budgets already exist.

**30-day reachability:** medium-high in OTA / concierge settings.

**Verdict: PROCEED, but keep booking verification explicit.**

## 2. The 30-Day Scope Definition

**Project name:** Intent-to-Itinerary Booking Copilot

**Validated problem:** trip planning is hard to convert into actual bookings.

**Target user:** travel concierge or platform user.

**Core hypothesis:** the agent can produce a verified itinerary from natural
language and live inventory.

### In Scope

1. **Flight and hotel search**
   - Acceptance criterion: live inventory is searched for relevant options.
2. **Constraint solving**
   - Acceptance criterion: the itinerary respects budget, timing, and policy
     constraints.
3. **Verified itinerary cart**
   - Acceptance criterion: the output is bookable or clearly marked as not yet
     verified.

### Explicitly Out Of Scope

- Autonomous cancellation handling in v1.
- Loyalty optimization engine.
- Full OTA replacement.
- Booking without live verification.

### Week-By-Week Milestones

- **Week 1:** API integrations.
- **Week 2:** constraint solver.
- **Week 3:** live availability checks.
- **Week 4:** booking-ready pilot.

**Dependencies:** travel APIs, pricing feeds, booking permission, reviewer
owner.

**Acceptance test:** itinerary fits constraints and uses live availability
checks before presentation.

**Top risks:** stale prices, impossible constraints, and booking errors.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: Next.js booking console.
- Backend: Python FastAPI.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + cached search metadata.
- Auth: SSO / OAuth.
- Database: Postgres for itineraries, quotes, approvals.
- Observability: quote freshness and booking audit.
- Hosting: cloud app with API integrations.

**Architecture:** intent -> search -> solve -> verify -> review -> book. The
agent checks live availability before rendering bookable options.

**Critical design decisions:**

1. Live verification before display because stale fares destroy trust.
2. Human approval before booking because edge cases are common.
3. Constraint solving before rendering because the user cares about fit, not
   search volume.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/trips` | create trip request | intent payload | request id | user auth | reject impossible inputs |
| POST | `/api/trips/{id}/search` | search live inventory | request id | quotes | service auth | stale-price warning |
| POST | `/api/trips/{id}/book` | confirm booking | approval note | booking status | user auth | block on missing verification |

### Folder / Module Structure

- `app/(console)/travel/`
- `app/api/trips/`
- `services/search/`
- `services/solver/`
- `workers/book/`
- `lib/availability/`

### Environment Variables

- `DATABASE_URL`
- `MODEL_ROUTER_API_KEY`
- `AMADEUS_API_KEY`
- `SABRE_API_KEY`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| OTA portal | High | existing portals are rigid | BUILD | intent-to-cart is the wedge |
| GDS access | High | API / network access already exists | BUY / INTEGRATE | reuse travel rails |
| Itinerary solver | Medium | generic search is weak | BUILD | differentiates conversion |

**Bottom line:** buy travel inventory, build intent-to-itinerary orchestration.

## 5. MVP ROI Business Case

**Current-state cost model:** portal/search software, itinerary assembly time,
manual booking support, and stale-fare rework.

**Agentic MVP cost model:** search, solve, verify, review, and model/API usage.

**Pricing options:**

1. Fixed pilot for one booking flow.
2. Per itinerary or booking.
3. Enterprise concierge package.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low booking volume | 12+ months | 12+ | learn only |
| Base | repeat requests | 4-8 months | 4-8 | good wedge |
| Upside | high conversion lift | 2-4 months | 2-4 | scale into concierge |

**Formulas**

```text
Monthly value =
  itinerary assembly time saved + conversion lift + manual support reduced
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if live inventory cannot be checked reliably, do not
present a bookable cart.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| SAP Concur | T&E | policy enforcement | old-school and clunky | custom enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/BookingItinerary_Competitor_Teardown.md` |
| Navan | corporate travel | integrated booking | workflow still portal-centric | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/BookingItinerary_Competitor_Teardown.md` |
| TravelPerk | travel platform | transactional breadth | middleman friction | transactional / subscription | `runs/2026-06-26-agentic-opportunity-blueprints/source/BookingItinerary_Competitor_Teardown.md` |
| Travefy | itinerary | planning UX | booking depth limited | flat-rate subscription | `runs/2026-06-26-agentic-opportunity-blueprints/source/BookingItinerary_Competitor_Teardown.md` |

**Direct threats:** Navan and TravelPerk.

**What not to build:** a massive, clunky dashboard.

**Agentic wedge:** invisible orchestration via chat or email, with live
availability and policy guardrails.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| budget fit | budget provided | solver runs | itinerary stays within budget | quote audit |
| live availability | search results shown | verify step runs | stale offers are blocked | freshness test |
| impossible trip | constraints impossible | solver runs | viable alternative is explained | review panel |

### Edge Cases

- No matching flight.
- Stale hotel inventory.
- Multi-city trip.
- Budget too low.
- Cancellation risk.
- Duplicate booking request.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| requests | user | request table | user | realtime | input validation |
| quotes | GDS / hotel APIs | quote table | provider | realtime | freshness timestamp |
| itineraries | solver | itinerary table | agent | per run | approval required |
| bookings | booking APIs | booking table | provider | realtime | immutable |

**Retention and deletion:** retain itinerary and quote lineage, delete
transient search state after retention, and keep approval records.

**Privacy/security:** traveler identity and payment context require tenant
isolation, encryption, and retention controls.

**Analytics questions:** which search paths convert best and which constraints
most often make trips impossible?

## 9. Deployment Sequencing

**Pre-deploy checklist:** API access confirmed, booking rules confirmed,
reviewer owner assigned.

**Staging:** test with synthetic routes and stale-price cases.

**Production sequence:** search-only -> verified cart -> booking approval.

**Smoke test:** search, solve, verify, approve, book.

**Rollback:** disable booking and keep planning only.

**Observability:**

- Logs: quote freshness, itinerary solve, booking action.
- Metrics: search-to-book conversion, retry rate.
- Alerts: stale prices, booking errors, API outages.
- Dashboards: itinerary conversion and freshness.

## 10. Post-Launch Iteration Plan

**Metrics:** search-to-book conversion, itinerary acceptance, and retry rate.

**Week-by-week:**

- Week 1: fix API coverage.
- Week 2: improve solver quality.
- Week 3: add hotel or car.
- Week 4: measure conversion lift.

**Pivot signals:** poor live-data reliability or low booking trust should push
the product toward planning-only mode.

## Source Notes
- `runs/2026-06-26-agentic-opportunity-blueprints/source/BookingItinerary_Competitor_Teardown.md` - booking incumbent map and invisible-orchestration wedge.
- `runs/2026-06-26-agentic-opportunity-blueprints/market-map-phase1-remaining.md` - phase-1 travel / booking market map backstop.
- Official reference points reviewed: Amadeus, Sabre, Expedia, Booking.com, Google Travel, and Concur product pages.
