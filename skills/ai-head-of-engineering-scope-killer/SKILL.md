---
name: ai-head-of-engineering-scope-killer
description: Use when someone wants to cut or prioritize MVP scope for the AI Head of Engineering flow, or asks what will realistically ship in 30 days.
metadata:
  legacy-frontmatter: 'name: ai-head-of-engineering-scope-killer

    description: Use when someone wants to cut or prioritize MVP scope for the AI Head of Engineering flow, or asks what will realistically ship in 30 days.

    argument-hint: [feature-backlog] [core-moment] [constraints]'
---

# Scope Killer

Use this to force a ruthless keep/cut/defer decision before any deeper planning.

## Inputs

- Feature backlog with 1-line descriptions
- Core moment of value
- Deadline, budget, team shape, and any hard constraints

## Process

1. Read the backlog and identify anything that is not tied to the core wow, monetization, or trust.
2. Score each feature for 30-day feasibility.
3. Return `KEEP`, `CUT`, or `DEFER` with one-line reasoning.
4. Produce the 80/20 cut list, the one-line MVP statement, and the three features founders will fight to keep.
5. Save the result as `01-scope-killer.md` in the run folder.

## Output

- Per-feature feasibility score
- `KEEP / CUT / DEFER` decision
- One-line MVP statement
- Top 5 keep list
- Founder-favorite cuts

## Dependencies

- `skills/ai-head-of-engineering/references/shared-templates.md`
- `skills/ai-head-of-engineering/references/output-contract.md`

## Skill Relationships

### Category
Business Automation

### Relationships
| Pattern | What it means here | Handoff artifact |
|---|---|---|
| Sequential | Feeds the scope spec step | `01-scope-killer.md` -> `02-scope-architect.md` |
| Domain cluster | One member of the AI Head of Engineering family | `runs/ai-head-of-engineering/...` |

### Host compatibility
Shared. Works in Claude Code, Codex/OpenAI, and OpenHands because the workflow is file-driven and host-neutral.

## Gotchas

- Do not accept marketing language as the core moment of value.
- Do not keep features just because they sound strategic.
- Do not let admin, settings, or export work masquerade as launch-critical unless they are the product.

