---
skill: /engagement-closeout
pack: engagement-management
chains-from: /post-implementation-review, /exit-strategy
chains-into: /continuous-improvement (new cycle), /situation-assessment (next engagement)
---

# Prompt Template: Engagement Closeout

**When to use:** In the final 2 weeks of the engagement — formally close the work, capture satisfaction, and set up the next commercial opportunity.

## Copy-paste prompt

```
Run /engagement-closeout for [CLIENT NAME]:

Engagement: [NAME]
Engagement period: [START DATE] → [END DATE]
Engagement lead: [NAME]

Deliverables checklist (mark each):
- [ ] [DELIVERABLE 1] — [accepted by client: Y/N] — [sign-off date or outstanding]
- [ ] [DELIVERABLE 2] — [accepted: Y/N] — [date or outstanding]
[continue for all contractual deliverables...]

Client satisfaction (gather from sponsor and key stakeholders):
- [STAKEHOLDER / ROLE]: [1-5 score per dimension: Quality / Collaboration / Value / Commercial / Would recommend]
- [STAKEHOLDER / ROLE]: [scores]

Lessons from this engagement:
- What went well: [LIST]
- What we would do differently: [LIST]
- Reusable assets created: [LIST — e.g. "Integration accelerator, responsible AI framework template"]

Commercial context:
- Contract closed out: [Y/N] — [outstanding items if any]
- Invoice status: [PAID / OUTSTANDING — £X]
- Retention of relationship assets: [who maintains the relationship going forward]

Follow-on potential:
- Identified follow-on opportunities: [LIST]
- Client readiness for next engagement: [BRIEF]
```

## Expected output
Deliverable sign-off record, client satisfaction scorecard, reference case (anonymised for pipeline use), lessons register, follow-on opportunity brief, and relationship continuity plan.

## Chain next
- If follow-on identified → `/win-strategy` for the next pursuit
- Client moves to BAU → `continuous-improvement` operating rhythm
