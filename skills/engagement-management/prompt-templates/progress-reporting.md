---
skill: /progress-reporting
pack: engagement-management
chains-from: /engagement-kickoff, /stakeholder-cadence
chains-into: /stage-gate-review, /stakeholder-alignment
---

# Prompt Template: Progress Reporting

**When to use:** Weekly or monthly — produce the RAG status dashboard and steering pack. Run this every reporting cycle.

## Copy-paste prompt

```
Run /progress-reporting for [CLIENT NAME]:

Engagement: [NAME]
Reporting period: [WEEK/MONTH ending DATE]
Report audience: [STEERING COMMITTEE / WORKING GROUP / SPONSOR 1:1]

This period's summary:
- Overall RAG: [RED / AMBER / GREEN]
- Reason (if not Green): [BRIEF]

Milestone status (from delivery plan):
| Milestone | Target Date | Status | Comment |
|---|---|---|---|
| [MILESTONE] | [DATE] | [RAG] | [BRIEF] |
[continue for all active milestones...]

Budget status:
- Budget consumed to date: [%]
- Forecast at completion: [OVER / ON / UNDER] by [£X / %]
- Explanation if not on budget: [BRIEF]

Top 3 issues / risks this period:
1. [ISSUE/RISK] — [RAG] — [owner] — [action being taken]
2. [ISSUE/RISK] — [RAG] — [owner] — [action]
3. [ISSUE/RISK] — [RAG] — [owner] — [action]

Decisions needed from this audience:
1. [DECISION] — [needed by: DATE] — [options: BRIEF]

Highlights / wins this period:
- [BRIEF]
```

## Expected output
One-page RAG dashboard, milestone tracker with trend arrows, budget burn chart, issues/decisions register, and steering pack narrative (what's going well, what's at risk, what we need).

## Chain next
- RED items escalate to `/stakeholder-alignment` for exec intervention
- End-of-phase summary becomes the `/stage-gate-review` input
