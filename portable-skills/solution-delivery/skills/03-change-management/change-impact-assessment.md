---
name: change-impact-assessment
description: Maps the scope and severity of change by stakeholder group across process, technology, role, and behaviour dimensions. Use before writing the change management plan to understand what is actually changing for whom.
---

# Change Impact Assessment

## When To Use

Use when the solution blueprint is defined and the team needs to understand what is changing for each affected group — before writing communications, designing training, or planning adoption support. A change management plan written without an impact assessment either over-invests in groups that are minimally affected or under-invests in groups that are most exposed.

## Consulting Approach

Change impact is not the same as project scope. A process change that affects 500 frontline users is a larger change management challenge than a technology change that affects 5 system administrators, even if the latter is more complex to build. Assess impact from the stakeholder's lived experience: what does their day look like today, and what does it look like after go-live?

## Workflow

1. List every stakeholder group affected by the solution (from the solution blueprint or `/stakeholder-alignment` output).
2. For each group, assess impact across four dimensions: Process (workflow changes), Technology (new or changed systems), Role (responsibility or authority changes), Behaviour (new ways of working required).
3. Score severity per dimension: High (significant change, new skills required), Medium (moderate change, some adjustment needed), Low (minor change, awareness only).
4. Identify compounding impact: groups where all four dimensions score Medium or above need prioritised change support.
5. Define the specific "what's changing" for each high-impact group in plain language.
6. Map timing: when does each group first experience the change?

## Output Format

```markdown
# Change Impact Assessment — [Programme Name]
**Date:** [YYYY-MM-DD]  **Solution:** [Name]

## Impact Heat Map
| Stakeholder Group | Size | Process | Technology | Role | Behaviour | Overall Severity | First Impact Date |
|---|---|---|---|---|---|---|---|

**Severity:** H = High, M = Medium, L = Low

## Group Impact Narratives
[For each High overall severity group:]

### [Group Name]
- **Today:** [How they work today — one paragraph]
- **After go-live:** [How they will work after — one paragraph]
- **Biggest change:** [The single hardest adjustment for this group]
- **Support needed:** [Communication / Training / Coaching / Job aids / Hypercare]

## Compounding Impact Groups
[Groups where Process + Technology + Role + Behaviour are all M or H — these are the highest change risk groups.]

## Change Volume by Timing
| Month | Groups First Impacted | Cumulative Groups in Transition |
|---|---|---|
```

## Quality Bar

- Severity scores must be grounded in the group's actual workflow, not the programme team's perception of difficulty.
- Impact narratives must be written from the stakeholder's perspective, not the project's.
- Compounding impact groups must receive an explicit change management workstream, not just standard communications.
- Timing column must reflect when the group first experiences the change, not when go-live occurs for the programme.
