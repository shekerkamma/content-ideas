---
status: reviewed
use_case: "Legacy-IT Modernization (NL to SAP)"
phase: "phase-1"
last_updated: "2026-06-26"
source_confidence: high
---

# Legacy-IT Modernization (NL to SAP) Master Implementation Blueprint

## Executive Positioning
- Target buyer: enterprise IT and business operations leaders.
- Pain wedge: SAP, mainframe, and COBOL systems are hard to query without IT intervention.
- Incumbent weakness: modernization projects are expensive, slow, and risky.
- Agentic disruption thesis: provide a natural-language read-only interface over legacy systems without migrating them.
- Why now: business users want answers faster than migration timelines.

## 1. Problem-Solution Fit Diagnostic
Score 28/30
- Problem realness: 10/10
- Solution fit: 9/10
- Buying signal + reachability: 9/10

Evidence:
- Who has the problem: enterprises with legacy SAP, mainframe, or COBOL systems.
- Last-time/recency evidence: modernization and reporting requests happen continuously.
- Current workaround: IT tickets, custom reports, and BI extracts.
- Switching reason: quick data access without migration risk.
- Payment signal: modernization consulting and backlog reduction budgets.
- 30-day reachability: one legacy system and one user workflow can prove the wedge.

Verdict: PROCEED

## 2. 30-Day Scope Definition
- Project name: Legacy Query Copilot
- Validated problem: business users need legacy data without waiting on IT.
- Target user: business analyst or ops user.
- Core hypothesis: the agent can translate NL into safe read-only queries over legacy systems.

In scope:
1. Secure connectivity.
2. NL-to-query translation.
3. Read-only chat interface.

Explicitly out of scope:
- System replacement.
- Write-back in v1.
- General ETL modernization.

Week-by-week milestones:
- Week 1: connectivity and schema mapping.
- Week 2: NL-to-query layer.
- Week 3: read-only execution and formatting.
- Week 4: business user chat deployment.

Dependencies:
- legacy database access, schema docs, and SSO.

Acceptance test:
- a business user asks a question and receives accurate data in under 10 seconds.

Top 3 risks + mitigations:
- destructive queries - read-only credentials
- schema drift - metadata mapping
- bad translations - review and clarification

## 3. Tech Stack + Architecture Design
Recommended stack:
- Frontend: Streamlit or Next.js chat UI.
- Backend: Python FastAPI.
- Agent orchestration: LangChain or Semantic Kernel.
- Retrieval/data layer: schema catalog plus query examples.
- Auth: SSO and read-only service account.
- Database: Postgres for logs and mappings.
- Observability: query success and latency metrics.
- Hosting: secure internal VPC or on-prem.

Architecture:
- System boundary: user question -> translate -> validate -> query -> answer.
- Runtime topology: chat UI -> translation layer -> read-only DB/API -> response.
- Core agent loop: interpret question, map schema, generate query, enforce read-only, return answer.
- Human-in-the-loop points: ambiguous metrics and destructive request blocks.
- Integration endpoints: SAP, mainframe APIs, internal DBs, chat UI.
- Failure handling: ambiguous questions trigger clarification, and write queries are blocked.

Database schema / data model:
| Table / Entity | Purpose | Key Fields | Indexes | Security / Tenancy |
|---|---|---|---|---|
| queries | user asks | id, tenant_id, user_id, question, ts | tenant_id, ts | tenant-scoped |
| mappings | schema metadata | id, system, table_name, column_name, alias | system, alias | versioned |
| translations | query output | id, query_id, sql, status, result_hash | query_id, status | audit tracked |
| answers | user responses | id, query_id, text, chart_ref | query_id | immutable |

API surface:
| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|
| POST | /api/questions | ask question | natural language | query_id | user auth | 400 on invalid input |
| POST | /api/questions/{id}/translate | generate SQL | question_id | sql | service auth | clarification required if ambiguous |
| POST | /api/questions/{id}/run | execute read-only query | sql | data | service auth | 403 on write attempt |

Integration plan:
| System | Direction | Data / Action | Auth | Failure Handling |
|---|---|---|---|---|
| SAP/mainframe | inbound | read-only data | service account | deny by default |
| schema catalog | inbound | metadata | service token | cache and retry |
| chat UI | outbound | answers | app auth | fallback to text |

Folder/module structure:
- `app/(console)/legacy/`
- `app/api/questions/`
- `services/translate/`
- `services/validate/`
- `services/query/`
- `services/format/`

Environment variables:
- `LEGACY_DB_URL`
- `READONLY_SERVICE_ACCOUNT`
- `SCHEMA_CATALOG_PATH`
- `CHAT_UI_URL`
- `LLM_API_KEY`

Critical design decisions:
1. Read-only access because legacy systems are fragile.
2. Clarification for ambiguity because business metrics vary.
3. Keep legacy system of record because migration is not the wedge.

## 4. Build vs Buy Decision Matrix
| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|
| NL query copilot | moderate | migration projects are huge | BUILD | fast access without migration is the wedge |
| legacy systems | low | already installed | BUY | keep SoR |
| chat UI | low | commodity | BUY/REUSE | simple interface |

Bottom line:
- Annual SaaS spend if buying: modernization consulting.
- One-time MVP build estimate: $50k-$100k equivalent effort.
- Recommended split: buy legacy systems, build translation layer.
- Payback period: under 12 months if IT backlog falls.

## 5. MVP ROI Business Case
Current-state cost model:
- Software: consulting and legacy tooling.
- Labor: IT and analyst time.
- Services/admin: report requests.
- Error/rework: slow answers and backlog.

Agentic MVP cost model:
- Build: translation and read-only query layer.
- Monthly run: queries and model usage.
- Maintenance: schema and metric tuning.

Pricing options:
1. Low-risk pilot: one business unit.
2. Usage/outcome model: per query.
3. Enterprise package: query layer plus governance.

ROI scenarios:
| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|
| Base | 40% IT backlog reduction | 6-10 months | month 8-12 | standard |
| Upside | high query volume | 3-6 months | month 4-6 | strong fit |
| Downside | schema complexity | 12-18 months | month 14+ | narrower scope |

No-go condition: if read-only access cannot be guaranteed, the agent should not query production systems.

## 6. Competitor Product Teardown
Competitor map:
| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|
| Accenture-style consulting | services | broad | expensive | project-based | `source/Legacy_IT_modernization_Competitor_Teardown.md` |
| SAP Signavio | process mining | transformation context | still migration-heavy | enterprise sales-led | `source/Legacy_IT_modernization_Competitor_Teardown.md` |
| Boomi | iPaaS | integration | not NL-first | enterprise sales-led | `source/Legacy_IT_modernization_Competitor_Teardown.md` |
| SNP Group | SAP transformation | SAP depth | heavy implementation | enterprise sales-led | `source/Legacy_IT_modernization_Competitor_Teardown.md` |
| Panaya | change intelligence | testing/support | still migration-focused | enterprise sales-led | `source/Legacy_IT_modernization_Competitor_Teardown.md` |

Direct threats: consulting firms and heavy iPaaS tools. Table stakes: security, governance, SAP compatibility. Things not to build: a SAP replacement or write-back system. Gaps: NL to legacy, automated code translation, instant process mapping.

## 7. Acceptance Criteria + Test Plan
| Feature | Given | When | Then | Verification |
|---|---|---|---|---|
| NL question | user asks | translate runs | accurate data returned | benchmark |
| destructive query | unsafe input | run starts | blocked | negative test |
| ambiguous metric | vague question | translate runs | clarification requested | UX test |

Edge cases:
- empty schema load
- source outage
- unsupported metric
- response delay
- duplicate question idempotent
- row-level separation

## 8. Data Architecture Lite
Data domains:
| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|
| schema metadata | legacy docs | catalog table | source system | batch | version control |
| queries | user | query log | chat service | realtime | redaction |
| translations | agent | translation table | agent | realtime | read-only validation |
| answers | system | answer table | system | realtime | audit log |

Retention and deletion:
- Data retained: question logs and query lineage.
- Data deleted: transient prompts and query drafts.
- Audit retained: SQL, results, and user feedback.

Analytics questions:
1. Which legacy questions are answered without IT help?
2. Which terms are most ambiguous?
3. What is the cost per successful answer?

Privacy/security:
- Legacy operational data can be sensitive; use tenant isolation, read-only service accounts, and row-level security.

## 9. Deployment Sequencing
Pre-deploy checklist:
- confirm legacy access
- confirm schema docs
- confirm read-only policy

Staging:
- run benchmark questions and verify SQL safety

Production sequence:
- start read-only, then answer-only, then optional chart rendering
- expand user group by user group

Smoke test:
- ask, translate, run, answer

Rollback:
- disable query execution and keep answer drafts only

Observability:
- Logs: prompt, SQL, result, and version.
- Metrics: accuracy, latency, clarification rate.
- Alerts: query failures and write-block attempts.
- Dashboards: usage, cost, and answer quality.

## 10. Post-Launch Iteration Plan
Metrics:
- Activation: percent of questions answered.
- Retention: weekly usage and repeat asks.
- Revenue/willingness-to-pay: pilot extension or per-query commitment.

Week-by-week:
- Week 1: fix schema tagging.
- Week 2: improve translation accuracy.
- Week 3: tune ambiguity prompts.
- Week 4: measure IT time saved.

Pivot signals:
- if metric definitions cannot be standardized or users do not trust the answers, narrow to guided reporting only.

## Source Notes
- `runs/2026-06-26-agentic-opportunity-blueprints/source/Legacy_IT_modernization_Competitor_Teardown.md` - internal teardown and incumbent mapping.
- `source/Agent_Use_Cases_Phase1.md` - use-case scorecard and scope.
- `source/original-10-skill-stack.txt` - prompt lineage.
- `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/Legacy_IT_modernization_Disruptive_Teardown.md` - incumbent map and NL-to-legacy wedge.
- Accenture homepage - https://www.accenture.com/ - accessed 2026-06-26 - consulting transformation backdrop.
- Boomi homepage - https://boomi.com/ - accessed 2026-06-26 - iPaaS and legacy integration backdrop.
- SNP Group homepage - https://www.snpgroup.com/ - accessed 2026-06-26 - SAP transformation and data conversion backdrop.
- Panaya homepage - https://www.panaya.com/ - accessed 2026-06-26 - ERP change intelligence backdrop.
