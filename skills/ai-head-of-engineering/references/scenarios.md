# AI Head of Engineering Scenario Tests

Use these scenarios to check whether the nine-role system routes correctly and produces the expected artifacts.

## Scenario 1 — Founder MVP with a short deadline

**Input**
- Solo founder
- New product idea
- 30-day deadline
- Small budget

**Expected route**
1. Scope Killer
2. 30-Day Scope Architect
3. Stack Picker
4. Build vs Buy Auditor
5. Build Estimator
6. AI Use-Case Validator if AI is in scope
7. Custom Internal Tool Designer only if the product is an internal tool
8. Pre-Launch Auditor
9. 30-Day Build Roadmap

**Pass criteria**
- Scope is cut ruthlessly.
- Output includes a master index and one file per role.
- No role runs before the earlier decision exists.

## Scenario 2 — Internal CRM replacement

**Input**
- Operations team wants to replace spreadsheet tracking
- Existing SaaS is too rigid
- Audit trail matters

**Expected route**
1. Scope Killer
2. 30-Day Scope Architect
3. Stack Picker
4. Build vs Buy Auditor
5. Build Estimator
6. AI Use-Case Validator only if scoring or summarization is involved
7. Custom Internal Tool Designer
8. Pre-Launch Auditor
9. 30-Day Build Roadmap

**Pass criteria**
- The custom tool designer captures business-specific fields, approvals, and audit logs.
- Generic SaaS defaults are excluded explicitly.

## Scenario 3 — AI feature in a customer-facing workflow

**Input**
- Product team wants to add AI summarization or classification
- Wrong answers are visible to users
- Cost per call matters

**Expected route**
1. Scope Killer
2. 30-Day Scope Architect
3. Stack Picker
4. Build vs Buy Auditor
5. Build Estimator
6. AI Use-Case Validator
7. Pre-Launch Auditor
8. 30-Day Build Roadmap

**Pass criteria**
- The validator chooses the smallest viable pattern.
- The result includes failure modes and a minimum eval set.
- `storm-research` is not used unless current evidence is needed.

## Scenario 4 — Build-vs-buy decision depends on live vendor pricing

**Input**
- Founder wants auth, email, search, and file storage options compared
- Vendor pricing and current product capabilities matter

**Expected route**
1. Scope Killer
2. 30-Day Scope Architect
3. Stack Picker
4. Build vs Buy Auditor

**Pass criteria**
- External research is used only for the vendor-dependent step.
- The recommendation includes 3-year cost math and integration burden.

## Scenario 5 — Launch readiness review before production

**Input**
- Build is finished
- User wants a go/no-go check before launch
- Production secrets and Stripe webhooks exist

**Expected route**
1. Pre-Launch Auditor
2. 30-Day Build Roadmap if launch needs a rollback-aware release plan

**Pass criteria**
- The smoke test includes a real production payment.
- Security boundaries are checked explicitly.
- Launch is blocked if the smoke test fails.

## Scenario 6 — User wants only one role, not the full chain

**Input**
- Ask only for stack recommendation
- Or ask only for scope cutting

**Expected route**
- Route directly to the named role skill.
- Do not run the orchestrator unless the full chain is requested.

**Pass criteria**
- Standalone role skills are discoverable.
- The orchestrator is optional, not mandatory.

## Scenario 7 — Hermes agent workflow realization

**Input**
- User wants to implement a Hermes-style workflow such as daily brief, smart contacts, investor research, signal monitoring, content pipeline, or self-maintenance
- Workflow needs data sources, memory, search, scheduled routines, and approval gates

**Expected route**
1. Scope Killer
2. 30-Day Scope Architect
3. Stack Picker
4. Build vs Buy Auditor
5. Build Estimator
6. AI Use-Case Validator
7. Pre-Launch Auditor
8. 30-Day Build Roadmap

Use `docs/hermes-use-cases-and-realization.md` as domain input.

**Pass criteria**
- The result identifies one concrete Hermes workflow, not a generic agent idea.
- The output names data sources, search provider, memory layer, scheduled jobs, approval gates, and cost controls.
- High-risk actions stay human-approved.
- The roadmap produces a controlled first implementation instead of broad autonomy.
