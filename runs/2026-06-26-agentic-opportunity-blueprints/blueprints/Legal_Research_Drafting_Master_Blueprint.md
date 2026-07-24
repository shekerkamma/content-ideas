---
status: reviewed
use_case: "Legal Research & Drafting"
phase: "phase-2"
last_updated: "2026-06-26"
source_confidence: medium-high
---

# Legal Research & Drafting Master Implementation Blueprint

## Executive Positioning
- Target buyer: partner, practice group lead, or legal ops leader at a firm or in-house team with recurring drafting and research load.
- Pain wedge: routine legal research and first-draft work still burns senior time.
- Incumbent weakness: Westlaw/Lexis/Harvey are strong tools, but they remain seat-based, context-bounded, or workflow-incomplete.
- Agentic disruption thesis: build a firm-specific legal workbench that grounds every claim in the client/matter corpus and reduces associate churn on repetitive work.
- Why now: legal teams already trust AI-assisted search, but they need tighter citation control and matter isolation.

## 1. Problem-Solution Fit Diagnostic
Score 24/30
- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal + reachability: 7/10

Evidence:
- Who has the problem: litigation, commercial contracts, and in-house legal ops teams.
- Last-time/recency evidence: case law lookup and first-draft work happen every week.
- Current workaround: Westlaw/Lexis search, templates, and associate labor.
- Switching reason: reduce research time and first-draft cost without losing citation traceability.
- Payment signal: premium legal research and AI add-on budgets already exist.
- 30-day reachability: high in firms with repeatable matter types and precedent libraries.

Verdict: PROCEED

## 2. 30-Day Scope Definition
- Project name: Matter-Aware Legal Drafting Copilot
- Validated problem: routine legal research and drafting are slow, expensive, and hard to standardize.
- Target user: associate, paralegal, or legal ops reviewer.
- Core hypothesis: a matter-scoped agent can draft and cite faster than manual research while staying inside approved sources.

In scope:
1. Matter corpus ingest with citation grounding.
2. Case-law / clause retrieval with source traceability.
3. NDA/MSA first-draft generation.
4. Reviewer queue for ambiguous language.

Explicitly out of scope:
- Autonomous legal advice.
- Court filing or client send without human review.
- Cross-matter data sharing.

Week-by-week milestones:
- Week 1: ingest templates and precedent sets.
- Week 2: build retrieval and citation flow.
- Week 3: draft generation and review queue.
- Week 4: pilot on one contract type and one research workflow.

Dependencies:
- Matter corpus, approved templates, and reviewer ownership.
Acceptance test:
- output cites the corpus, flags ambiguity, and completes a first draft on a narrow matter set.
Top 3 risks + mitigations:
- citation drift - enforce source spans
- matter contamination - strict partitioning
- hallucinated advice - human review gates

## 3. Tech Stack + Architecture Design
Recommended stack:
- Frontend: Next.js reviewer console.
- Backend: Python FastAPI.
- Agent orchestration: LangGraph.
- Retrieval/data layer: Postgres + pgvector.
- Auth: SSO/RBAC.
- Database: Postgres with matter isolation.
- Observability: audit logs and citation metrics.
- Hosting: isolated VPC or buyer environment.

Architecture:
- System boundary: matter corpus -> retrieve -> draft -> review -> approve.
- Runtime topology: document ingest, retrieval, generation, reviewer workflow.
- Core agent loop: locate precedent, draft clause, cite source, flag ambiguity.
- Human-in-the-loop points: clause approval, exception handling, client send.
- Integration endpoints: DMS, document store, SSO, email.
- Failure handling: if source coverage is weak, the agent refuses to invent text.

Database schema / data model:
| Table / Entity | Purpose | Key Fields | Indexes | Security / Tenancy |
|---|---|---|---|---|
| matters | client/matter boundary | id, client_id, matter_id, type | client_id, matter_id | hard partition |
| sources | source docs | id, matter_id, uri, hash | matter_id, hash | matter-scoped |
| drafts | generated text | id, matter_id, doc_type, status | matter_id, status | approval gated |
| citations | source spans | id, draft_id, source_id, span | draft_id, source_id | immutable |

API surface:
| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | /api/matters | register matter | matter metadata | matter id | admin | reject if tenant mismatch |
| POST | /api/matters/{id}/draft | generate draft | doc type, matter id | draft | reviewer role | fail closed on missing sources |
| POST | /api/drafts/{id}/approve | approve draft | approval note | approved status | reviewer role | block if citations missing |

Integration plan:
| System | Direction | Data / Action | Auth | Failure Handling |
|---|---|---|---|---|
| DMS | inbound | matter documents | token | retry/batch |
| doc editor | outbound | draft export | user auth | queue |
| SSO | inbound | identity/RBAC | SAML/OIDC | deny by default |

Folder/module structure:
- `app/(console)/legal/`
- `app/api/matters/`
- `services/legal-agent/`
- `lib/citations/`

Environment variables:
- `DATABASE_URL`
- `MODEL_ROUTER_API_KEY`
- `MATTER_STORAGE_BUCKET`
- `SSO_ISSUER_URL`

Critical design decisions:
1. Matter isolation over shared corpora because privilege boundaries matter.
2. Citation-first drafting because legal trust is source traceability.
3. Review gating because autonomous legal advice is not the wedge.

## 4. Build vs Buy Decision Matrix
| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| Legal research | High | Westlaw/Lexis seat costs | BUILD/HYBRID | matter-specific context is the wedge |
| Generic AI legal tools | Medium | Harvey/Lexis+ AI enterprise pricing | BUY/KEEP | use as reference, not replacement |
| Matter retrieval | Medium | DMS search is weak | BUILD | source-grounded drafting requires it |

Bottom line:
- Annual SaaS spend if buying: high and seat-driven.
- One-time MVP build estimate: moderate.
- Recommended split: buy research access, build matter-aware drafting.
- Payback period: 4-9 months on repeat matters.

## 5. MVP ROI Business Case
Current-state cost model:
- Software: research seats and DMS.
- Labor: associate/paralegal time.
- Services/admin: template upkeep and review.
- Error/rework: weak citations and re-drafts.

Agentic MVP cost model:
- Build: retrieval, drafting, review queue.
- Monthly run: model and hosting.
- Maintenance: source refresh and template tuning.

Pricing options:
1. Fixed pilot per matter type.
2. Per drafted document.
3. Enterprise package by practice group.

ROI scenarios:
| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Downside | low volume, heavy review | 12-18 months | month 12+ | keep as internal tool |
| Base | repeatable matter set | 4-8 months | month 4-8 | strongest wedge |
| Upside | high reuse and large corpus | 2-4 months | month 2-4 | expand to adjacent workflows |

No-go condition: if the buyer cannot isolate matters or accept citation-based review, stop.

## 6. Competitor Product Teardown
| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Westlaw | research | depth and brand | expensive and seat-based | enterprise | Thomson Reuters |
| Lexis+ AI | research | broad legal content | sales-led and bundled | enterprise | LexisNexis |
| Harvey | AI legal | modern UX | enterprise-controlled, costly | sales-led | Harvey |

Direct threats: Westlaw and Lexis+ AI. Table stakes: citations, clause drafting, matter search, review queue. Things not to build: general legal advice, filing workflow. Gaps: matter-specific source control and first-draft speed.

## 7. Acceptance Criteria + Test Plan
| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| cited answer | approved corpus | research prompt runs | answer cites source spans | citation audit |
| first draft | template and matter docs | drafting runs | draft produced with flagged ambiguities | reviewer signoff |
| matter boundary | another matter exists | retrieval runs | no cross-matter leakage | tenancy test |

Edge cases:
- empty corpus
- conflicting sources
- stale precedent
- redline conflict
- prompt injection in uploaded docs
- unauthorized matter access

## 8. Data Architecture Lite
| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| matter docs | DMS/upload | object store + index | matter repo | batch | hash + matter id |
| citations | source spans | citation table | source doc | per run | immutable span refs |
| drafts | agent | draft table | agent | per run | reviewer approval |

Privacy/security: hard matter partitioning, encryption, retention limits, and no model training on client content.

## 9. Deployment Sequencing
Pre-deploy: confirm corpus, matter owners, and reviewer roles.
Staging: run on sanitized matters and compare citations.
Production: start read-only, then limited drafting.
Smoke test: retrieve, cite, draft, approve.
Rollback: disable drafting and keep read-only search.
Observability: logs, citations, latency, and approval rates.

## 10. Post-Launch Iteration Plan
- Metrics: adoption, reuse, and draft turnaround time.
- Week 1: fix citation gaps.
- Week 2: improve drafting templates.
- Week 3: add one more matter type.
- Week 4: measure time saved.
- Pivot signals: poor citation quality or no reviewer trust.

## Source Notes
- Westlaw - https://legal.thomsonreuters.com/en/products/westlaw - accessed 2026-06-26 - legal research incumbent.
- Lexis+ AI - https://www.lexisnexis.com/en-us/products/lexis-plus-ai.page - accessed 2026-06-26 - AI legal research incumbent.
- Harvey - https://www.harvey.ai/ - accessed 2026-06-26 - enterprise legal AI reference point.
- Bloomberg Law - https://pro.bloomberglaw.com/ - accessed 2026-06-26 - all-in-one legal research and workflow software.
- ABA Model Rules - https://www.americanbar.org/groups/professional_responsibility/publications/model_rules_of_professional_conduct/ - accessed 2026-06-26 - supervision and citation discipline context.
- WIPO Lex - https://www.wipo.int/en/web/wipolex - accessed 2026-06-26 - official IP law and treaty research context.
- EUR-Lex - https://eur-lex.europa.eu/ - accessed 2026-06-26 - official EU law and document research context.
- Leah / ContractPodAi - https://www.contractpodai.com/ - accessed 2026-06-26 - legal drafting and commercial intelligence workflow reference.
