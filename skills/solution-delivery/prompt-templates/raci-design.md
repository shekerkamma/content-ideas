---
skill: /raci-design
pack: solution-delivery
chains-from: /solution-blueprint, /ai-operating-model
chains-into: /engagement-kickoff, /stakeholder-cadence
---

# Prompt Template: RACI Design

**When to use:** After the solution blueprint and operating model are set — define who is responsible, accountable, consulted, and informed for each major decision and deliverable.

## Copy-paste prompt

```
Run /raci-design for [CLIENT NAME]:

Programme / workstream: [NAME]

Roles involved (list all people or role types who may appear in the RACI):
- [ROLE 1] — [organisation] — [brief description]
- [ROLE 2] — [organisation] — [brief description]
[continue for all roles...]

Major decisions and deliverables to map (from solution blueprint / programme plan):
1. [DECISION / DELIVERABLE]
2. [DECISION / DELIVERABLE]
3. [DECISION / DELIVERABLE]
[continue...]

Known constraints:
- [e.g. "Client executive sponsor only available monthly — avoid placing A on weekly operational items"]
- [e.g. "Vendor has read-only role — C or I only"]
- [e.g. "Regulatory function must be Consulted on any data governance decision"]
```

## Expected output
RACI matrix (roles × decisions/deliverables), constraint validation (one A per row, no C > R, no role A on >40% of rows), role workload summary, escalation path, and governance implications.

## Chain next
- Use the RACI to inform `/engagement-kickoff` ways of working
- Use the escalation path to design the `/stakeholder-cadence`
