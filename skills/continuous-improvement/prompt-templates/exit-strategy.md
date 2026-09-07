---
skill: /exit-strategy
pack: continuous-improvement
chains-from: /hypercare-plan (end), /capability-maturity-progression
chains-into: /engagement-closeout, /operating-rhythm-design (BAU)
---

# Prompt Template: Exit Strategy

**When to use:** 4–6 weeks before the consulting team is due to exit — plan knowledge transfer, retained advisory terms, and the formal handover to BAU.

## Copy-paste prompt

```
Run /exit-strategy for [CLIENT NAME]:

Engagement: [NAME]
Target exit date: [DATE]
Consulting team exiting: [LIST roles / people]

BAU team taking ownership:
- [ROLE] — [NAME] — [current readiness: HIGH / MEDIUM / LOW]
- [ROLE] — [NAME] — [readiness]
[continue...]

Current knowledge transfer status:
- Documentation completed: [LIST what exists]
- Documentation outstanding: [LIST what still needs to be written]
- Training completed: [LIST what has been done]
- Training outstanding: [LIST]

Exit readiness for each criterion (assess honestly):
- BAU team can operate without consulting escalation: [Y / PARTIALLY / N]
- Runbook documented and validated: [Y / PARTIALLY / N]
- Operating rhythm booked and first cycle completed: [Y / PARTIALLY / N]
- Performance reporting automated: [Y / PARTIALLY / N]
- Open RAID items resolved or formally transferred: [Y / PARTIALLY / N]
- Knowledge base current and accessible: [Y / PARTIALLY / N]

Post-exit relationship commercial intent:
- Retained advisory: [DESIRED / NOT DESIRED / UNDECIDED]
- Emergency re-engagement: [DESIRED / NOT DESIRED]
- Quarterly health checks: [DESIRED / NOT DESIRED]
```

## Expected output
Exit readiness scorecard (Ready/Conditionally Ready/Not Ready), knowledge transfer plan with completion dates, retained advisory commercial model, re-engagement conditions (specific and measurable), exit sign-off template, and post-exit follow-up schedule.

## Chain next
- Commercial closeout → `/engagement-closeout`
- BAU governance → `/operating-rhythm-design` (already running or to be established)
