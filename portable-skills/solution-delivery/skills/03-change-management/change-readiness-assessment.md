---
name: change-readiness-assessment
description: Scores stakeholder groups on the five ADKAR dimensions — Awareness, Desire, Knowledge, Ability, Reinforcement — to identify where change management effort is most needed before go-live. Use after /stakeholder-alignment when the solution is defined and the adoption risk is unknown.
---

# Change Readiness Assessment

## When To Use

Use after the solution blueprint is defined and before the change management plan is written. If you do not know where stakeholders sit on the ADKAR curve, a change management plan is guesswork. Run the assessment 6–8 weeks before go-live and again 2 weeks before cutover.

## Consulting Approach

Prosci ADKAR defines five building blocks of individual change: Awareness (why the change is needed), Desire (motivation to support it), Knowledge (how to change), Ability (skills to demonstrate new behaviours), and Reinforcement (mechanisms to sustain the change). Each dimension is a barrier point — a stakeholder group that scores low on Desire will not respond to more training (Knowledge). The assessment identifies the active barrier point for each group.

## Workflow

1. Identify 4–8 stakeholder groups affected by the change (segment by role and degree of change, not seniority).
2. For each group, score each ADKAR dimension on a 1–5 scale using a combination of survey data, manager interviews, and observed behaviour.
3. Identify the lowest-scoring dimension per group — this is the active barrier point.
4. Classify overall readiness: Ready (all dimensions ≥ 4), At Risk (any dimension 2–3), Not Ready (any dimension ≤ 1).
5. Define targeted interventions for each group's active barrier point.
6. Set a re-assessment date to track movement before go-live.

## Output Format

```markdown
# Change Readiness Assessment — [Programme Name]
**Date:** [YYYY-MM-DD]  **Go-Live Target:** [YYYY-MM-DD]

## Stakeholder Group Summary
| Group | Size | Degree of Change (H/M/L) | A | D | K | A | R | Overall Readiness | Active Barrier |
|---|---|---|---|---|---|---|---|---|---|

**Score guide:** 1 = No readiness, 2 = Minimal, 3 = Partial, 4 = Substantial, 5 = Full readiness

## Group Deep-Dives
[For each At Risk or Not Ready group:]

### [Group Name]
- **Active barrier:** [ADKAR dimension]
- **Root cause:** [Why this dimension is low]
- **Evidence:** [Survey data, interview signal, observed behaviour]
- **Intervention:** [Targeted action — sponsor visibility / coaching / training / reinforcement mechanism]
- **Owner:** [Named individual]
- **Target score by go-live:** [n]

## Readiness Dashboard
| Group | Current | Target | Gap | Intervention | Due |
|---|---|---|---|---|---|

## Re-Assessment Schedule
[Date and method for next readiness check.]
```

## Quality Bar

- Score every ADKAR dimension for every group — "we don't know" is a valid score of 1, not a reason to skip.
- Interventions must address the active barrier point, not the easiest or most familiar intervention.
- Overall readiness classifications must be defensible to the programme sponsor — document the evidence.
- Re-assessment date must be before go-live, not after.
