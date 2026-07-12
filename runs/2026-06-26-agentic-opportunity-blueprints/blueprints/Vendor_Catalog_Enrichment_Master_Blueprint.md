---
status: reviewed
use_case: "Vendor Catalog Enrichment"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence:
  problem: high
  competitor: high
  pricing: high
  implementation: medium-high
---

# Vendor Catalog Enrichment Master Implementation Blueprint

## Executive Positioning

**Initial ICP:** ecommerce, merchandising, and PXM leaders managing large
assortments and frequent vendor feeds.

**Later ICPs:** adjacent catalog teams once one category proves that unstructured
ingestion and automated enrichment save enough labor to matter.

**Pain wedge:** vendor data arrives as PDFs, spreadsheets, and spec sheets, and
humans still do the heavy mapping and normalization.

**Incumbent weakness:** Salsify, Akeneo, and Pimcore are strong source-of-truth
systems, but they still depend on manual mapping and standardized inputs.

**Agentic disruption thesis:** extract, normalize, and enrich catalog data
automatically from raw vendor files and write export-ready output.

**Why now:** buyers already pay for PIM / PXM, but the human middleware is the
real cost.

## 1. The Diagnostic: Problem-Solution Fit Validation

**Research-inferred score: 26/30**

The score is inferred from catalog labor costs, implementation friction, and
clear willingness to pay for PIM / PXM systems.

- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 8/10

**Who has the problem:** ecommerce ops and catalog teams with large
assortments.

**Current workaround:** manual spreadsheet entry and data cleaning.

**Switching reason:** faster time-to-shelf and lower catalog labor.

**Payment signal:** PIM / PXM spend and catalog-services spend.

**30-day reachability:** one vendor feed and one category.

**Verdict: PROCEED, but keep the taxonomy stable.**

## 2. The 30-Day Scope Definition

**Project name:** Catalog Enrichment Agent

**Validated problem:** catalog data is slow to ingest and often poor quality.

**Target user:** catalog operations and merchandising.

**Core hypothesis:** an agent can transform messy source files into clean,
enriched product records.

### In Scope

1. **Ingest raw files**
   - Acceptance criterion: PDFs, spreadsheets, and spec sheets are indexed.
2. **Extract and normalize**
   - Acceptance criterion: product attributes are mapped to the target
     taxonomy.
3. **Write export-ready output**
   - Acceptance criterion: clean catalog output is generated for review and
     downstream export.

### Explicitly Out Of Scope

- Full PIM replacement.
- Retail media optimization.
- Supplier contract management.
- Rebuilding retailer syndication workflows.

### Week-By-Week Milestones

- **Week 1:** ingest sample vendor files.
- **Week 2:** build extraction and normalization.
- **Week 3:** add enrichment and export.
- **Week 4:** pilot with one category.

**Dependencies:** vendor files, taxonomy, and approved brand rules.

**Acceptance test:** the team can produce clean product records from messy
vendor inputs with minimal manual cleanup.

**Top risks:** taxonomy mismatch, copy quality, and source noise.

## 3. Tech Stack + Architecture Design

**Recommended stack:**

- Frontend: catalog review console.
- Backend: FastAPI service.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + vector store for specs and policies.
- Auth: PIM or ERP OAuth.
- Database: Postgres for items, attributes, and approvals.
- Observability: OpenTelemetry and enrichment metrics.
- Hosting: cloud app with worker queue.

**Architecture:** source file -> parse -> extract -> normalize -> enrich ->
export. The agent reads vendor data, maps attributes, enriches copy, and writes
catalog output.

**Critical design decisions:**

1. Work from raw files first.
2. Keep manual review for taxonomy exceptions.
3. Optimize for fast shelf-ready output.

### API Surface

| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | `/api/catalog/ingest` | ingest vendor files | file bundle | ack | service token | retry queue |
| POST | `/api/catalog/extract` | extract attributes | file_id | attributes | service token | fallback review |
| POST | `/api/catalog/export` | export clean catalog | product ids | export result | service token | retry on failure |

### Folder / Module Structure

- `app/catalog/`
- `app/api/catalog/`
- `services/parse/`
- `services/enrich/`
- `workers/export/`
- `lib/taxonomy/`

### Environment Variables

- `PIM_TOKEN`
- `ERP_TOKEN`
- `DATABASE_URL`
- `MODEL_API_KEY`
- `EXPORT_BUCKET`

## 4. Build vs Buy Decision Matrix

| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| PIM / PXM | high | Salsify / Akeneo expensive | BUY | source of truth already exists |
| Parsing / extraction | medium | manual team workload | BUILD | agentic wedge |
| Enrichment / copy | medium | staffing or agencies | BUILD | high leverage |

**Bottom line:** buy the data system of record and build the enrichment
engine.

## 5. MVP ROI Business Case

**Current-state cost model:** catalog labor, data cleanup, launch delays, and
agency costs.

**Agentic MVP cost model:** ingest, extraction, enrichment, review labor, and
storage / model usage.

**Pricing options:**

1. Per feed.
2. Per SKU.
3. Enterprise bundle.

| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | small assortment, simple taxonomy | 12-18 months | month 14+ | weaker |
| Base | 40-60% less manual catalog labor | 6-9 months | month 8-12 | solid fit |
| Upside | large assortment and repeated feeds | 3-5 months | month 4-6 | very strong |

**Formulas**

```text
Monthly value =
  catalog labor avoided + data-cleanup reduced + launch delay avoided
  - monthly agent run cost

Payback period =
  pilot/build cost / monthly value
```

**No-go condition:** if the taxonomy is unstable and the merchant expects a
full PIM rebuild, the wedge is lost.

## 6. Competitor Product Teardown

| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Salsify | PXM | retailer syndication | expensive and complex | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/UC46_Vendor_Catalog_Enrichment_Competitor_Teardown.md` |
| Akeneo | PIM | flexible data model | project hell if data is dirty | enterprise | `runs/2026-06-26-agentic-opportunity-blueprints/source/UC46_Vendor_Catalog_Enrichment_Competitor_Teardown.md` |
| Pimcore | open-source PIM | customizable and API-first | technical lift | commercial / OSS | `runs/2026-06-26-agentic-opportunity-blueprints/source/UC46_Vendor_Catalog_Enrichment_Competitor_Teardown.md` |

**Direct threats:** Salsify and Akeneo.

**What not to build:** a full PIM database, retailer relationship management,
or MDM suite.

**Agentic wedge:** ingest unstructured vendor inputs, auto-write product
attributes, and turn dry specs into branded listings.

## 7. Acceptance Criteria + Test Plan

| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| File ingest | vendor PDF arrives | system parses it | file stored and indexed | parser test |
| Attribute extraction | messy spec | extraction runs | fields populated | fixture comparison |
| Export | product approved | export starts | clean feed generated | end-to-end test |

### Edge Cases

- Multiple unit measures.
- Missing dimensions.
- Conflicting vendor values.
- Duplicate SKUs.
- Brand-restricted copy.

## 8. Data Architecture + Analytics

| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| vendor inputs | PDF / XLSX / CSV | source file store | vendor | realtime | checksum |
| taxonomy | merch rules | taxonomy store | merch ops | versioned | approval state |
| enriched items | model output | item table | enrichment engine | realtime | confidence threshold |
| exports | feed generator | export store | ecommerce system | scheduled | validation |

**Retention and deletion:** retain approved item records and provenance;
delete raw vendor uploads after policy window if required; keep audit diffs for
changes.

**Privacy/security:** vendor confidentiality, tenant isolation, and least-
privilege PIM access.

**Analytics questions:** which vendors create the most mapping churn and which
categories need more taxonomy governance?

## 9. Deployment Sequencing

**Pre-deploy checklist:** vendor file sample, taxonomy map, export target,
rollback flag.

**Staging:** one category, one vendor, one export format.

**Production sequence:** parse only, then enrich, then export.

**Smoke test:** verify one SKU flows from raw spec to approved feed.

**Rollback:** disable auto-enrichment and keep review mode.

**Observability:**

- Logs: file, attribute, confidence, export state.
- Metrics: manual touch rate, enrichment rate, launch speed.
- Alerts: parse failures, taxonomy conflicts, export errors.
- Dashboards: mapping exceptions and export failures.

## 10. Post-Launch Iteration Plan

**Metrics:** manual touches removed, feed completeness, time to shelf, and
launch throughput.

**Week-by-week:**

- Week 1: expand file types.
- Week 2: improve attribute mapping.
- Week 3: refine copy rules.
- Week 4: package for adjacent categories.

**Pivot signals:** add stronger governance if taxonomy dominates, constrain
enrichment to facts only if copy is weak, and narrow integration targets if
export is unreliable.

## Source Notes

- `runs/2026-06-26-agentic-opportunity-blueprints/source/UC46_Vendor_Catalog_Enrichment_Competitor_Teardown.md` - Salsify / Akeneo / Pimcore incumbent map and implementation-friction signals.
- Salsify - https://www.salsify.com/ - accessed 2026-06-26 - PXM and product data system-of-record backdrop.
- Akeneo - https://www.akeneo.com/ - accessed 2026-06-26 - PIM and catalog workflow backdrop.
- Bynder - https://www.bynder.com/en/ - accessed 2026-06-26 - DAM system-of-record backdrop.
- Cloudinary - https://cloudinary.com/ - accessed 2026-06-26 - asset delivery and transformation backdrop.
- The wedge remains enrichment work on top of existing PIM and DAM systems, not a replacement of the catalog source of truth.
- These incumbents show why the buyer pays for governance and syndication, but still needs an agent to do the human middleware work.
- The most valuable output is publishable catalog data with provenance, not another place to store the same SKU facts.
