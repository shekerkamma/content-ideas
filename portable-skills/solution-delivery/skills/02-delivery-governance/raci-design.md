---
name: raci-design
description: Builds a RACI matrix that assigns Responsible, Accountable, Consulted, and Informed roles across decisions and deliverables. Use when accountability is unclear, duplicate ownership is causing conflict, or a new workstream or governance structure is being stood up.
---

# RACI Design

## When To Use

Use when standing up a new programme, workstream, or operating model — or when delivery is stalling because multiple people believe they are accountable for the same thing, or no one believes they are accountable for anything. RACI is most valuable when produced before conflict arises, but it also resolves existing confusion when applied retroactively.

## Consulting Approach

A RACI with too many Rs is a committee in disguise. A RACI with too many As is an organisation that cannot make decisions. The discipline is in the constraints: one A per row, no more than two Rs per row, and no row where Consulted outnumbers Responsible. The test of a good RACI is whether a new team member could use it alone to know exactly what they own.

## Workflow

1. List every significant decision and deliverable for the programme or workstream (aim for 15–30 rows).
2. List every role that could plausibly hold accountability (not individual names — roles).
3. For each row, assign: one Accountable (A), one or two Responsible (R), Consulted (C) where input is genuinely needed, Informed (I) for awareness only.
4. Apply the constraint check: flag any row with more than one A, any role that is A on more than 40% of rows, and any row where C > R.
5. Resolve conflicts: hold a RACI walkthrough with role holders to confirm assignments.
6. Identify gaps: decisions with no R or no A are delivery risks.

## Output Format

```markdown
# RACI Matrix — [Programme / Workstream]
**Version:** [n]  **Date:** [YYYY-MM-DD]

## Role Register
| Role | Name (if known) | Workstream |
|---|---|---|

## RACI Matrix
| Decision / Deliverable | [Role 1] | [Role 2] | [Role 3] | [Role 4] | [Role 5] |
|---|---|---|---|---|---|

**Key:** R = Responsible, A = Accountable, C = Consulted, I = Informed

## Constraint Check
| Check | Result |
|---|---|
| Rows with > 1 Accountable | [count — target: 0] |
| Role with A on > 40% of rows | [name — target: none] |
| Rows where C > R | [count — target: 0] |
| Rows with no R or no A | [count — target: 0] |

## Conflict / Gap Log
[List any disputed assignments and the resolution needed.]
```

## Quality Bar

- Every row must have exactly one A. If the team cannot agree on one, that is the highest-priority governance issue to resolve.
- Consulted roles must be justified — if someone is C only because it avoids conflict, they should be I.
- RACI rows should be decisions and deliverables, not activities. "Runs the stand-up" is an activity; "Approves sprint scope change" is a decision.
- Produce a constraint-check summary — a RACI with unchecked constraint violations is not a governance tool.
