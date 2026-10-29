# Master Implementation Blueprint Template

Use this template for each upgraded blueprint. Keep the voice strategic and
operator-grade: specific enough to prove execution capability, but not framed
as a commitment to build immediately.

```markdown
---
status: draft | reviewed | blocked
use_case: "<name>"
phase: "phase-1 | phase-2 | extra"
last_updated: "YYYY-MM-DD"
source_confidence: low | medium | high
---

# <Use Case> Master Implementation Blueprint

## Executive Positioning
- Target buyer:
- Pain wedge:
- Incumbent weakness:
- Agentic disruption thesis:
- Why now:

## 1. Problem-Solution Fit Diagnostic
Score 0-30:
- Problem realness: /10
- Solution fit: /10
- Buying signal + reachability: /10

Evidence:
- Who has the problem:
- Last-time/recency evidence:
- Current workaround:
- Switching reason:
- Payment signal:
- 30-day reachability:

Verdict: PROCEED | NEEDS WORK | KILL

## 2. 30-Day Scope Definition
- Project name:
- Validated problem:
- Target user:
- Core hypothesis:

In scope:
1. Feature - acceptance criterion

Explicitly out of scope:
- ...

Week-by-week milestones:
- Week 1:
- Week 2:
- Week 3:
- Week 4:

Dependencies:
Acceptance test:
Top 3 risks + mitigations:

## 3. Tech Stack + Architecture Design
Recommended stack:
- Frontend:
- Backend:
- Agent orchestration:
- Retrieval/data layer:
- Auth:
- Database:
- Observability:
- Hosting:

Architecture:
- System boundary:
- Runtime topology:
- Core agent loop:
- Human-in-the-loop points:
- Integration endpoints:
- Failure handling:

Database schema / data model:
| Table / Entity | Purpose | Key Fields | Indexes | Security / Tenancy |
|---|---|---|---|---|

API surface:
| Method | Path | Purpose | Input | Output | Auth | Failure Behavior |
|---|---|---|---|---|---|---|

Integration plan:
| System | Direction | Data / Action | Auth | Failure Handling |
|---|---|---|---|---|

Folder/module structure:
- `app/...`
- `services/...`
- `workers/...`
- `lib/...`

Environment variables:
- `NAME`: purpose

Critical design decisions:
1. Decision / alternatives / rationale / reconsideration trigger

## 4. Build vs Buy Decision Matrix
| Feature | Build Cost | SaaS Cost / Friction | Verdict | Reasoning |
|---|---:|---:|---|---|

Bottom line:
- Annual SaaS spend if buying:
- One-time MVP build estimate:
- Recommended split:
- Payback period:

## 5. MVP ROI Business Case
Current-state cost model:
- Software:
- Labor:
- Services/admin:
- Error/rework:

Agentic MVP cost model:
- Build:
- Monthly run:
- Maintenance:

Pricing options:
1. Low-risk pilot:
2. Usage/outcome model:
3. Enterprise package:

ROI scenarios:
| Case | Assumptions | Payback | Breakeven | Notes |
|---|---|---:|---:|---|

No-go condition:

## 6. Competitor Product Teardown
Competitor map:
| Competitor | Category | Strength | Weakness | Pricing Signal | Source |
|---|---|---|---|---|---|

Direct threats:
Table-stakes features to copy:
Things not to build:
Three exploitable gaps:

## 7. Acceptance Criteria + Test Plan
Feature test plan:
| Feature | Given | When | Then | Verification |
|---|---|---|---|---|

Edge cases:
- Empty state:
- Error state:
- Invalid input:
- Slow dependency:
- Concurrent action:
- Auth/data boundary:

## 8. Data Architecture Lite
Data domains:
| Domain | Source | Storage | Source of Truth | Sync | Quality Guardrail |
|---|---|---|---|---|---|

Retention and deletion:
- Data retained:
- Data deleted:
- Audit retained:

Analytics questions:
1. Question / event / attributes / tool

Privacy/security:
- PII/PHI/financial data:
- Retention:
- Export/delete:

## 9. Deployment Sequencing
Pre-deploy checklist:
Staging:
Production sequence:
Smoke test:
Rollback:
Observability:
- Logs:
- Metrics:
- Alerts:
- Dashboards:

## 10. Post-Launch Iteration Plan
Metrics:
- Activation:
- Retention:
- Revenue/willingness-to-pay:

Week-by-week:
- Week 1:
- Week 2:
- Week 3:
- Week 4:

Pivot signals:

## Source Notes
- <source title> - <URL> - accessed YYYY-MM-DD - claim supported
```
