---
skill: /adoption-plan
pack: solution-delivery
chains-from: /change-readiness-assessment, /change-impact-assessment
chains-into: /benefits-register, /hypercare-plan
---

# Prompt Template: Adoption Plan

**When to use:** Once you know who is impacted (from readiness + impact assessments) — design the activity schedule, comms, training, and reinforcement mechanisms that will drive adoption.

## Copy-paste prompt

```
Run /adoption-plan for [CLIENT NAME]:

Change being implemented: [BRIEF]
Go-live date: [DATE]
Hypercare period: [N weeks post go-live]

Impacted groups (from prior assessments):
1. [GROUP] — [ADKAR barrier: AWARENESS / DESIRE / KNOWLEDGE / ABILITY / REINFORCEMENT] — [severity: H/M/L]
2. [GROUP] — [barrier] — [severity]
[continue...]

Available channels and resources:
- Comms channels: [e.g. "Email, intranet, town halls, team meetings, manager cascade"]
- Training delivery: [e.g. "E-learning platform, on-the-job coaching, peer champions"]
- Training budget: [APPROXIMATE or CONSTRAINED]
- Champion network: [EXISTS / NEEDS CREATING / N champions identified]
- Executive sponsor commitment: [BRIEF — e.g. "CPTO will record video message and attend one town hall"]

Adoption success metrics:
- [METRIC 1] — [target] — [measurement method]
- [METRIC 2] — [target] — [measurement method]
```

## Expected output
Pre/post go-live activity schedule (week-by-week), comms plan with message-audience-channel-date matrix, training plan by group, reinforcement mechanisms, adoption metrics dashboard, and go-live support model.

## Chain next
- Adoption metrics become the early indicators in `/benefits-register`
- Support model during hypercare feeds into `/hypercare-plan`
