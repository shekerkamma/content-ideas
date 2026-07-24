# Goal Loop Orchestrator Smoke Test

Date: 2026-06-30

## Sample Prompt

```text
I have a rough idea for an AI support triage tool. Refine the goal, pick the
right skills, and get me to a verified PRD plus build plan.
```

## Expected Runtime Preamble

I’ll refine the goal first, then run the smallest skill chain needed and loop
until the acceptance criteria are met or a real blocker appears.

## Goal Contract

- Outcome: verified PRD and build plan for an AI support triage tool.
- Artifacts: `vision.json`, `docs/prd.md`, `docs/product-roadmap.md`, final handoff.
- Constraints: use local skills first; no external installs; do not exceed loop budget without approval.
- Acceptance criteria: PRD defines users, problem, workflows, data needs, MVP scope, risks, and roadmap; build plan has actionable checked/unchecked tasks.
- Verification: validate PLAID outputs, inspect docs for completeness, check roadmap actions are specific and testable.
- Loop budget: 3 total passes.
- Stop conditions: acceptance criteria met; budget reached; no material progress; missing product input blocks generation.
- Known inputs: rough product category = AI support triage tool.
- Missing inputs: target customer, support channels, integration requirements, compliance constraints, success metric.

## Local Skill Inventory Snapshot

- `plaid`: strong match for turning rough product idea into vision, PRD, and roadmap.
- `karpathy-guidelines`: useful overlay for making the build plan verifiable and surgical.
- `grill-me`: optional upstream if product inputs are too vague.
- `goal-loop-orchestrator`: active controller.

No external skill discovery needed.

## Skill Chain

| Phase | Skill/action | Why | Input | Output | Verification |
|---|---|---|---|---|---|
| 1 | `grill-me` or direct intake | Missing inputs materially shape the PRD | rough idea | clarified product constraints | required fields captured or flagged |
| 2 | `plaid` plan | Converts idea into source-of-truth product artifacts | clarified idea | `vision.json`, `docs/prd.md`, roadmap | PLAID validation/doc completeness |
| 3 | `karpathy-guidelines` overlay + direct review | Tightens build plan into verifiable implementation tasks | roadmap | final build handoff | tasks have success criteria and checks |

## Simulated Loop Passes

### Pass 1

- Action: refine goal and inspect local skill inventory.
- Result: goal contract and skill chain selected.
- Material change: yes.
- Acceptance criteria met: no.
- Verification status: not applicable yet; artifacts do not exist.
- Decision: continue.
- Reason: product artifacts still need creation.

### Pass 2

- Action: route to `grill-me` or direct intake because required product inputs are missing.
- Result: would ask one focused question or capture flags if user cannot answer.
- Material change: conditional.
- Acceptance criteria met: no.
- Verification status: pending clarified inputs.
- Decision: ask before proceeding if missing inputs cannot be inferred.
- Reason: target customer and integrations materially change PRD content.

### Pass 3

- Action: route to `plaid` after inputs are known.
- Result: would generate/validate `vision.json`, `docs/prd.md`, and `docs/product-roadmap.md`.
- Material change: yes if artifacts are created.
- Acceptance criteria met: only after validation passes.
- Verification status: would run PLAID validation and doc inspection.
- Decision: stop if verified; otherwise report residual gaps because loop budget is reached.
- Reason: budget is 3 total passes.

## Handoff

- Phase completed: smoke-test simulation.
- Skill/action used: `goal-loop-orchestrator` dry run.
- Inputs consumed: sample prompt and local skill metadata.
- Artifacts created/changed: this smoke-test file; `skills/goal-loop-orchestrator/SKILL.md` example section.
- Decisions made: local skills are sufficient; no external skill discovery required; loop budget prevents infinite iteration.
- Evidence/checks: chain includes goal contract, bounded loop state, stop conditions, and verification gates.
- Open flags: real execution would need product-specific inputs.
- Recommended next pass: run a real invocation against an actual product idea, or add a tiny automated contract test for the skill file.
