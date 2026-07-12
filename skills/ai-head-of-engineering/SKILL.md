---
name: ai-head-of-engineering
description: "Use when you want to run the full founder build-planning system for a custom app, MVP, or internal tool, or to route a build idea into the nine-role planning sequence. Also covers any single role: scope killer / cut MVP scope, 30-day scope architect, stack picker, build-vs-buy audit, build estimator (hours/dollars/risk), AI use-case validator, custom internal tool designer, pre-launch audit, or 30-day build roadmap."
argument-hint: "[build-idea] [constraints]"
---

# AI Head of Engineering

Use this when the user wants the planning layer for a build, not a random pile of prompts.
The job is to turn an idea into a governed, inspectable build plan using the nine specialist roles in order.

## What this system does

This system replaces the monthly planning work a senior engineering leader would normally do before code gets written:
scope cutting, 30-day scoping, stack choice, build-vs-buy decisions, estimates, AI fit validation, internal tool design, pre-launch audit, and the rollout roadmap.

It should produce two kinds of artifacts:
1. A master index for the full run.
2. One markdown file per role, so every step can be rerun, audited, or reused independently.

## Standard run order

1. Scope Killer
2. 30-Day Scope Architect
3. Stack Picker
4. Build vs Buy Auditor
5. Build Estimator
6. AI Use-Case Validator
7. Custom Internal Tool Designer
8. Pre-Launch Auditor
9. 30-Day Build Roadmap

## How to run

1. Read the founder idea, constraints, team shape, deadline, and any existing notes.
2. Create a run folder and a master index.
3. Run the roles in order. Each role's full instructions live in
   `references/roles/` — read the role file, then execute it inline:
   - `references/roles/01-scope-killer.md`
   - `references/roles/02-scope-architect.md`
   - `references/roles/03-stack-picker.md`
   - `references/roles/04-build-vs-buy-auditor.md`
   - `references/roles/05-build-estimator.md`
   - `references/roles/06-ai-use-case-validator.md`
   - `references/roles/07-custom-internal-tool-designer.md`
   - `references/roles/08-pre-launch-auditor.md`
   - `references/roles/09-30-day-build-roadmap.md`
4. Pass each role the previous role's output file.

**Single-role requests** ("just run the scope killer", "stack choice for X"):
read only that role file, execute it inline, and still write its numbered
output file so a later full run can pick up from it.
5. Write the next role's output file before moving on.
6. When a role needs external evidence, use research only there, not everywhere.

## Research rules

- Roles 4, 5, and 6 may use external research and parallel subagents if available.
- Prefer You.com search and livecrawl for current web evidence.
- Use `storm-research` only when the question genuinely needs multi-perspective source verification.
- Keep the other roles deterministic and file-driven.

## File handoff contract

Use this pattern:

- `master-index.md`
- `01-scope-killer.md`
- `02-scope-architect.md`
- `03-stack-picker.md`
- `04-build-vs-buy.md`
- `05-build-estimator.md`
- `06-ai-fit.md`
- `07-tool-designer.md`
- `08-pre-launch-audit.md`
- `09-roadmap.md`

The master index should record:
- source idea
- constraints
- status of each role
- key decisions
- open flags
- output file names
- any research or subagent notes

## Shared outputs

Shared templates and role notes live in `references/`.
Read them when you need the canonical output shape, the role map, or the scenario tests.
Use `docs/ai-head-of-engineering-use-cases.md` when the user asks why the system exists or which business use case should be targeted.

## Skill Relationships

### Category
Business Automation

### Relationships
| Pattern | What it means here | Handoff artifact |
|---|---|---|
| Sequential | Orchestrates the nine role skills in order | `master-index.md` plus role markdown files |
| Orchestrator | Calls the role skills as sub-steps | role output files |
| Amplifier | Can use `ai-analyst` upstream for quantitative inputs | analysis output file |
| Fallback | Can route to `storm-research` for evidence-heavy roles | research brief / citations |
| Domain cluster | Sits above the nine role skills in the same system | run folder |

### Host compatibility
Shared. Use the same workflow in Claude Code, Codex/OpenAI, and OpenHands.
The body instructions are the source of truth; frontmatter is an enhancement.

## Gotchas

- Do not let the chain collapse into one chat answer.
- Do not skip the master index.
- Do not run the later roles before the earlier decisions exist.
- Do not use research on every role; only the evidence-heavy ones need it.
- Do not let generated outputs stay isolated. Every role must feed the next.
