---
skill: /change-readiness-assessment
pack: solution-delivery
chains-from: /solution-blueprint, /engagement-kickoff
chains-into: /change-impact-assessment, /adoption-plan
---

# Prompt Template: Change Readiness Assessment

**When to use:** Before designing the adoption plan — understand where resistance will come from and what ADKAR stage each impacted group is at.

## Copy-paste prompt

```
Run /change-readiness-assessment for [CLIENT NAME]:

Change being implemented: [BRIEF DESCRIPTION — e.g. "Deploying AI-assisted invoice processing in Accounts Payable"]
Go-live date: [DATE]

Impacted groups:
1. [GROUP NAME] — [SIZE] people — [role/function] — [current process they will change]
2. [GROUP NAME] — [SIZE] people — [role/function] — [current process they will change]
[continue for all groups...]

Context for each group (fill what you know):
- Change communication to date: [BRIEF — e.g. "Town hall announcement 3 months ago, no follow-up"]
- Current sentiment signals: [BRIEF — e.g. "AP team concerned about job security; IT team supportive"]
- Prior change experience: [BRIEF — e.g. "Failed ERP rollout in 2023 — trust in IT is low"]
- Leadership sponsorship visibility: [BRIEF]
- Training delivered to date: [NONE / BRIEF]
- Any early adoption or pilots: [NONE / BRIEF]

Known resistance points:
- [LIST any specific objections or concerns you have already heard]
```

## Expected output
ADKAR scorecard per group (Awareness/Desire/Knowledge/Ability/Reinforcement, each 1–5), active barrier point identification, targeted interventions per barrier, readiness risk rating, and recommended sequencing.

## Chain next
- Low-scoring groups inform the `/change-impact-assessment` severity ratings
- Barrier points and interventions feed directly into the `/adoption-plan`
