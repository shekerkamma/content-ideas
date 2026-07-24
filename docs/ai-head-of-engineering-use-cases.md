# AI Head of Engineering Use Cases

This document is the business reason for the skill system.

The goal is not to create more prompts. The goal is to turn vague build ideas
into clear, defensible use cases with scope, architecture, cost, risk, and
delivery plan before code starts.

## What We Are Building

An AI Head of Engineering planning system for founders, enterprise operators,
and solution architects who need to decide what to build, what to buy, what to
cut, and how to ship a useful version in 30 days.

The system is implemented as:

- One orchestrator skill: `ai-head-of-engineering`
- Nine role skills that can run independently or as a chain
- File-based handoffs so every decision is inspectable
- Research only where live evidence changes the answer

## What We Accomplish

At the end of a run, we should have a clean use-case package:

- The business problem
- The core user value
- The features to keep, cut, and defer
- The 30-day scope
- The recommended stack
- Build-vs-buy decisions
- Effort and cost estimate
- AI fit decision, if relevant
- Internal tool design, if relevant
- Pre-launch risk checklist
- Week-by-week roadmap with rollback triggers

If those artifacts are not produced, the system failed.

## Clear-Cut Use Cases

### 1. Founder MVP Planning

**Business situation**
A founder has an app idea and a feature backlog, but no clear path to a
30-day build.

**Decision to make**
What can ship in 30 days, what must be cut, and what should the first build
actually do?

**Skill route**
Run the full chain:
`Scope Killer -> Scope Architect -> Stack Picker -> Build vs Buy -> Estimator -> Roadmap`.
Use `AI Use-Case Validator` only if AI is part of the product.

**Output**
A founder-ready MVP package with scope cuts, build spec, stack decision,
estimate, and sprint roadmap.

**Value**
Prevents the founder from spending weeks building features that do not create
the first moment of value.

### 2. Internal Tool Replacement

**Business situation**
A team is running a workflow in spreadsheets, email, or a generic SaaS tool
that does not fit the way the business actually operates.

**Decision to make**
Should the team build a custom internal tool, configure an existing SaaS
platform, or use a hybrid approach?

**Skill route**
Run:
`Scope Killer -> Scope Architect -> Stack Picker -> Build vs Buy -> Estimator -> Custom Internal Tool Designer -> Pre-Launch Auditor -> Roadmap`.

**Output**
A custom internal tool spec with data model, roles, permissions, approval
flows, automations, integrations, launch risks, and roadmap.

**Value**
Turns hidden operational logic into a buildable system instead of copying a
generic CRM template.

### 3. AI Feature Validation

**Business situation**
A product team wants to add an AI feature because it sounds valuable, but the
real failure cost, latency, and unit economics are unclear.

**Decision to make**
Should AI be used here at all? If yes, should it be prompt-only, RAG, tool
calling, or an agent loop?

**Skill route**
Run:
`Scope Architect -> Build Estimator -> AI Use-Case Validator -> Pre-Launch Auditor`.

Use You.com or other live research only when model pricing, provider
capability, or current benchmarks materially affect the decision.

**Output**
AI fit score, recommended pattern, model choice, cost per 1,000 uses, failure
modes, and minimum eval set.

**Value**
Stops teams from adding expensive or fragile AI where rules, workflow, or
search would solve the problem more reliably.

### 4. Build-vs-Buy Vendor Decision

**Business situation**
A team is deciding whether to build or buy auth, payments, email, file storage,
search, analytics, CRM, support, or workflow automation.

**Decision to make**
Which parts are commodity and which parts should remain custom because they
differentiate the business?

**Skill route**
Run:
`Scope Architect -> Stack Picker -> Build vs Buy Auditor`.

Use live research when vendor pricing, feature limits, or integration
constraints are current facts.

**Output**
Per-feature `BUILD / BUY / HYBRID` decision with 3-year cost, data ownership,
time-to-ship, switching cost, and integration burden.

**Value**
Avoids wasting engineering time rebuilding solved infrastructure while also
avoiding accidental SaaS lock-in.

### 5. Build Estimate and Budget Check

**Business situation**
A founder or operator has a spec but does not know whether the build fits the
available budget or timeline.

**Decision to make**
Is the scope feasible with the current team and deadline? What must be cut if
the estimate exceeds capacity?

**Skill route**
Run:
`Scope Architect -> Stack Picker -> Build vs Buy Auditor -> Build Estimator`.

**Output**
Feature-level hour ranges, dollar cost, confidence rating, risk factors, total
range, and cut list if the plan exceeds 160 hours.

**Value**
Turns vague ambition into an explicit cost and capacity conversation before
implementation starts.

### 6. Pre-Launch Go/No-Go Audit

**Business situation**
The build is almost finished, but the team has not tested real production
conditions.

**Decision to make**
Can the team launch, or should launch be blocked until critical gaps are fixed?

**Skill route**
Run:
`Pre-Launch Auditor -> 30-Day Build Roadmap` if a rollback-aware launch plan is
needed.

**Output**
Edge cases, security gaps, production readiness checklist, smoke test, launch
blockers, and rollback plan.

**Value**
Finds the defects that usually surface on launch day: auth boundaries,
webhooks, secrets, payments, empty states, and broken production config.

### 7. Enterprise POC Scoping

**Business situation**
An enterprise team wants to prove value quickly for a GenAI, workflow, or
internal automation concept.

**Decision to make**
What should the POC prove, what should it explicitly not prove, and what
evidence is needed for stakeholder approval?

**Skill route**
Run:
`Scope Killer -> Scope Architect -> Stack Picker -> Build vs Buy -> AI Use-Case Validator -> Build Estimator -> Roadmap`.

Use `ai-analyst` upstream when quantitative baselines, operational metrics, or
ROI assumptions need synthesis.

**Output**
POC scope, success criteria, solution components, cost estimate, AI risk
assessment, and stakeholder roadmap.

**Value**
Keeps enterprise pilots from becoming undefined experiments with no measurable
decision at the end.

### 8. Hermes Agent Workflow Realization

**Business situation**
A user wants to implement a Hermes-style personal or business agent workflow,
but the idea is still broad: daily brief, smart contacts, investor research,
content pipeline, signal monitoring, or self-maintenance.

**Decision to make**
Which workflow should be automated first, what data sources and tools are
needed, and where should human approval remain mandatory?

**Skill route**
Run:
`Scope Killer -> Scope Architect -> Stack Picker -> Build vs Buy -> AI Use-Case Validator -> Pre-Launch Auditor -> Roadmap`.

Use the Hermes realization document as domain input:
`docs/hermes-use-cases-and-realization.md`.

**Output**
Agent workflow scope, integration architecture, data-source plan, approval
gates, cost/risk controls, and implementation roadmap.

**Value**
Turns Hermes from a demo concept into a controlled operational workflow with
clear boundaries.

## Scenario Test Coverage

The scenario test file at
`skills/ai-head-of-engineering/references/scenarios.md` validates the main
routes:

- Founder MVP
- Internal CRM replacement
- AI feature validation
- Vendor build-vs-buy
- Launch readiness
- Single-role invocation
- Hermes workflow realization

## Success Criteria

The system is working when it can produce clear use-case packages that answer:

- What is the use case?
- Who is the buyer or operator?
- What problem does it solve?
- What gets built in 30 days?
- What is explicitly out of scope?
- What existing tools should be bought?
- What should be custom?
- What does it cost?
- What can fail?
- What proves the use case worked?
