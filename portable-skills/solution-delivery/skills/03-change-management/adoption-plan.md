---
name: adoption-plan
description: Builds the integrated adoption plan: communications, training, coaching, and reinforcement activities sequenced against go-live milestones. Use after /change-readiness-assessment and /change-impact-assessment to convert findings into a delivery schedule.
---

# Adoption Plan

## When To Use

Use when the change readiness and impact assessments are complete and the programme needs a concrete schedule of adoption activities. The adoption plan is the change management delivery instrument — it translates ADKAR gaps and impact severity into timed, owned actions. Without it, change management is intent, not execution.

## Consulting Approach

Adoption is not a go-live event — it is a curve. Most programmes treat the day users start using the new system as the adoption milestone. The Prosci model treats it as the midpoint: the work before go-live builds Awareness, Desire, and Knowledge; the work after go-live builds Ability and Reinforcement. An adoption plan that ends at go-live will have a reinforcement gap and a backslide risk.

## Workflow

1. Import ADKAR scores from `/change-readiness-assessment` and impact severity from `/change-impact-assessment`.
2. For each stakeholder group with ADKAR gaps, identify the activity type needed: Awareness campaign, sponsorship action, training, coaching, job aid, peer network, or reinforcement mechanism.
3. Sequence activities on a timeline: 8 weeks pre go-live → go-live → 4 weeks post go-live (hypercare).
4. Assign an owner for each activity and confirm resource availability.
5. Define success measures for adoption: usage metrics, survey scores, support ticket volume, manager observation.
6. Set checkpoint dates to assess adoption progress and course-correct before reinforcement is withdrawn.

## Output Format

```markdown
# Adoption Plan — [Programme Name]
**Go-Live Date:** [YYYY-MM-DD]  **Hypercare End:** [YYYY-MM-DD]

## Activity Schedule
| Week | Activity | Type | Audience Group | Owner | ADKAR Target | Success Signal |
|---|---|---|---|---|---|---|

## Communications Plan
| Message | Audience | Channel | Sender | Date | Goal |
|---|---|---|---|---|---|

## Training Plan
| Module | Audience | Format | Duration | Facilitator | Date | Completion Target |
|---|---|---|---|---|---|---|

## Reinforcement Mechanisms
| Mechanism | Audience | Start Date | Owner | Measure |
|---|---|---|---|---|

## Adoption Metrics
| Metric | Baseline | Target at Go-Live | Target at 30 Days | Target at 90 Days | Owner |
|---|---|---|---|---|---|

## Checkpoint Schedule
| Date | Assessment Method | Decision Point |
|---|---|---|
```

## Quality Bar

- Activities must be tied to ADKAR gaps — if an activity does not address a named gap, question whether it belongs in the plan.
- Reinforcement activities must extend at least 4 weeks past go-live; plans that end at cutover will have backslide risk.
- Training completion targets must be set before go-live, not aspirational.
- Adoption metrics must be measurable without a survey — system usage data, completion rates, or observable behaviour.
