---
status: reviewed
use_case: "Customs and Bill of Lading Extraction"
phase: "phase-2"
last_updated: "2026-06-26"
source_confidence: high
---

# Customs and Bill of Lading Extraction Master Implementation Blueprint

## Executive Positioning
- Target buyer: logistics, customs, and freight operations leaders.
- Pain wedge: multilingual shipping docs slow down customs clearance.
- Incumbent weakness: OCR templates are brittle across vendors and languages.
- Agentic disruption thesis: extract shipping fields semantically and push structured JSON to ERP.
- Why now: port delays are expensive and documents are increasingly varied.

## 1. Problem-Solution Fit Diagnostic
Score 27/30
- Problem realness: 9/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

Evidence:
- Who has the problem: customs brokers and logistics teams.
- Last-time/recency evidence: OCR and document AI remain common in trade ops.
- Current workaround: manual data entry and templates.
- Switching reason: faster clearance and fewer demurrage fees.
- Payment signal: customs processing and trade software.
- 30-day reachability: one document class and one ERP endpoint can prove the wedge.

Verdict: PROCEED

## 2. 30-Day Scope Definition
- Project name: Trade Doc Copilot
- Validated problem: bills of lading and invoices must be structured fast.
- Target user: customs coordinator or ops analyst.
- Core hypothesis: the agent can extract fields from shipping docs and route them into ERP.

In scope:
1. Multilingual PDF ingest.
2. Key field extraction and schema validation.
3. ERP JSON push with exceptions.

Explicitly out of scope:
- Replacing customs brokers.
- Autonomous filing without review.
- Full TMS replacement.

Week-by-week milestones:
- Week 1: schema and ERP endpoint setup.
- Week 2: historical doc prompt tuning.
- Week 3: review UI for low-confidence extraction.
- Week 4: pilot on top vendor formats.

Dependencies:
- shipping docs, ERP API, and review workflow.

Acceptance test:
- multiple vendor bill-of-lading formats are extracted with high accuracy.

Top 3 risks + mitigations:
- language variance - multimodal model support
- unreadable scans - bounding-box review
- bad ERP writes - validation gate

## 3. Tech Stack + Architecture Design
Recommended stack:
- Frontend: review dashboard.
- Backend: FastAPI.
- Agent orchestration: doc extraction pipeline.
- Retrieval/data layer: Postgres and object store.
- Auth: ERP and logistics SSO.
- Database: Postgres for documents and fields.
- Observability: extraction confidence and correction rate.
- Hosting: secure cloud environment.

Architecture:
- System boundary: upload -> extract -> validate -> ERP push.
- Runtime topology: PDF upload -> vision extract -> JSON validate -> ERP.
- Core agent loop: detect document type, extract fields, validate schema, route exceptions.
- Human-in-the-loop points: illegible docs and unusual fields.
- Integration endpoints: S3/GCS, ERP APIs, review UI.
- Failure handling: bad or missing fields go to human review.

Database schema / data model:
| Table / Entity | Purpose | Key Fields | Indexes | Security / Tenancy |
|---|---|---|---|---|
| documents | source docs | id, tenant_id, uri, doc_type, hash | tenant_id, doc_type | tenant-scoped |
| fields | extracted output | id, doc_id, field_name, value, confidence | doc_id, field_name | approval gated |
| exceptions | review queue | id, doc_id, reason, status | doc_id, status | audit tracked |
| writes | ERP updates | id, doc_id, payload, status | doc_id | immutable |

API surface:
| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | /api/documents | upload doc | file | doc_id | user auth | 400 on invalid file |
| POST | /api/documents/{id}/extract | extract fields | doc_id | fields | service auth | partial with exceptions |
| POST | /api/documents/{id}/push | push to ERP | doc_id | status | service auth | queue on outage |

Integration plan:
| System | Direction | Data / Action | Auth | Failure Handling |
|---|---|---|---|---|
| S3/GCS | inbound | document upload | service token | retry and hash check |
| ERP | outbound | structured JSON | API token | queue on failure |
| review UI | outbound | exception task | app auth | preserve state |

Folder/module structure:
- `app/api/`
- `services/ingest/`
- `services/extract/`
- `services/validate/`
- `services/push/`

Environment variables:
- `DOC_BUCKET`
- `ERP_API_TOKEN`
- `REVIEW_ROLE`
- `VALIDATION_SCHEMA_PATH`
- `LLM_API_KEY`

Critical design decisions:
1. Schema validation before ERP push because shipping errors are expensive.
2. Multimodal extraction because layouts vary wildly.
3. Human review for low confidence because customs compliance matters.

## 4. Build vs Buy Decision Matrix
| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| customs extraction | moderate | OCR tools are rigid | Build | semantic extraction is the wedge |
| ERP | low | already in place | Buy | keep SoR |
| object storage | low | commodity | Buy/Reuse | no need to replace |

Bottom line:
- Annual SaaS spend if buying: OCR and customs tools.
- One-time MVP build estimate: $40k-$80k equivalent effort.
- Recommended split: buy ERP/storage, build extraction worker.
- Payback period: under 12 months if delays fall.

## 5. MVP ROI Business Case
Current-state cost model:
- Software: OCR and trade software.
- Labor: manual data entry.
- Services/admin: customs rework.
- Error/rework: port delay and fee exposure.

Agentic MVP cost model:
- Build: one extraction and validation pipeline.
- Monthly run: model and OCR usage.
- Maintenance: ERP mapping and doc tuning.

Pricing options:
1. Low-risk pilot: one vendor set.
2. Usage/outcome model: per document.
3. Enterprise package: extraction plus exception handling.

ROI scenarios:
| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Base | fewer manual entries | 6-10 months | month 8-12 | standard |
| Upside | high document volume | 3-6 months | month 4-6 | strong fit |
| Downside | many unreadable docs | 12-18 months | month 14+ | more review |

No-go condition: if ERP integration cannot accept structured output, the product stays as a review aid.

## 6. Competitor Product Teardown
Competitor map:
| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| ABBYY | OCR | established | template maintenance | enterprise | product page |
| Kofax | document AI | broad | heavy | enterprise | product page |
| manual entry | labor | flexible | slow | labor-only | market standard |

Direct threats:
- OCR suites
- document AI
- manual entry

Table-stakes features to copy:
- field extraction
- schema validation
- ERP push

Things not to build:
- customs broker replacement
- full TMS
- filing automation without review

Three exploitable gaps:
- vendor-specific templates
- multilingual docs
- exception routing

## 7. Acceptance Criteria + Test Plan
Feature test plan:
| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| bill of lading | standard docs | pipeline runs | 20+ fields extracted | fixture test |
| illegible scan | blurry doc | pipeline runs | review flagged | negative test |
| ERP push | validated JSON | push runs | payload accepted | integration test |

Edge cases:
- Empty state: no document uploaded.
- Error state: OCR failure prompts review.
- Invalid input: unsupported format rejected.
- Slow dependency: queue pending.
- Concurrent action: duplicate doc idempotent.
- Auth/data boundary: tenant isolation.

## 8. Data Architecture Lite
Data domains:
| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| docs | upload | blob store | source | realtime | hash check |
| fields | agent | field table | agent | realtime | confidence threshold |
| exceptions | agent | exception table | review | realtime | immutable log |
| writes | ERP | write table | ERP | realtime | schema validation |

Retention and deletion:
- Data retained: extracted fields and exception history.
- Data deleted: transient OCR artifacts after retention.
- Audit retained: extraction lineage.

Analytics questions:
1. Which vendors produce the most extraction exceptions?

Privacy/security:
- secure blob storage
- tenant isolation
- validation before write

## 9. Deployment Sequencing
Pre-deploy checklist:
- schema approved
- ERP API tested
- review flow ready

Staging:
- historical document replay.

Production sequence:
- shadow -> review-only -> ERP push.

Smoke test:
- one shipping doc extracts and validates.

Rollback:
- disable push and keep review only.

Observability:
- Logs: doc, field, confidence, write.
- Metrics: extraction accuracy, exception rate, throughput.
- Alerts: OCR failure, ERP outage, validation miss.
- Dashboards: by vendor.

## 10. Post-Launch Iteration Plan
Metrics:
- Activation: docs processed.
- Retention: repeat vendor use.
- Revenue/willingness-to-pay: fewer delays and lower labor.

Week-by-week:
- Week 1: add more document types.
- Week 2: improve language coverage.
- Week 3: add cross-doc validation.
- Week 4: expand ERP mappings.

Pivot signals:
- if docs are too messy, narrow to high-volume vendors
- if ERP writes are blocked, stay as review only
- if volume is low, sell as extraction service

## Source Notes
- ABBYY - https://www.abbyy.com/ - accessed 2026-06-26 - OCR backdrop.
- Kofax - https://www.kofax.com/ - accessed 2026-06-26 - document AI backdrop.
- `runs/2026-06-26-agentic-opportunity-blueprints/market-map-phase2.md` - trade-doc extraction market-map backstop.
- Official reference points reviewed: ABBYY, Kofax, Hyperscience, Rossum, and Microsoft Document Intelligence product pages.
