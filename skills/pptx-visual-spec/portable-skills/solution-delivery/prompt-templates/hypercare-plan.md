---
skill: /hypercare-plan
pack: solution-delivery
chains-from: /stage-gate-review (go-live gate), /adoption-plan
chains-into: /post-implementation-review, /operating-rhythm-design, /exit-strategy
---

# Prompt Template: Hypercare Plan

**When to use:** In the 2 weeks before go-live — design the intensive support model that bridges go-live and BAU handover.

## Copy-paste prompt

```
Run /hypercare-plan for [CLIENT NAME]:

Solution: [SOLUTION NAME]
Go-live date: [DATE]
Hypercare period: [N weeks — typically 4–8]

Solution complexity:
- Number of impacted users: [N]
- Number of integrated systems: [N]
- Volume of transactions (daily): [N — e.g. "400 invoices/day"]
- Known fragile areas: [LIST — e.g. "SAP integration has had 3 test failures"]

Support team available:
- Consulting team: [N people] available [full-time / part-time] until [DATE]
- Client IT: [N people] available for [scope]
- Vendor support: [SLA description]

Previous go-live learnings (if available):
- [BRIEF — e.g. "Pilot rollout had high call volume on days 2–3; volume subsided by day 5"]

Exit criteria for hypercare:
- [CRITERION 1 — e.g. "Zero P1 incidents for 5 consecutive business days"]
- [CRITERION 2 — e.g. "Support call volume below 10/day"]
- [CRITERION 3 — e.g. "BAU team handling 80% of issues without consulting escalation"]
```

## Expected output
L1/L2/L3 support model, triage SLA table (P1/P2/P3), knowledge transfer schedule, daily/weekly check-in cadence, escalation path, hypercare exit criteria dashboard, and BAU handover plan.

## Chain next
- Once hypercare exit criteria are met, trigger `/post-implementation-review` (90 days)
- BAU governance model → `/operating-rhythm-design`
- Consulting exit → `/exit-strategy`
