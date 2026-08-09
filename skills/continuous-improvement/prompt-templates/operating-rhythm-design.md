---
skill: /operating-rhythm-design
pack: continuous-improvement
chains-from: /hypercare-plan, /post-implementation-review
chains-into: /performance-review, /stakeholder-cadence (if consulting is still present)
---

# Prompt Template: Operating Rhythm Design

**When to use:** At the end of hypercare, when the solution transitions to BAU — design the meeting cadence and governance forums that will sustain performance.

## Copy-paste prompt

```
Run /operating-rhythm-design for [CLIENT NAME]:

Solution / capability entering BAU: [NAME]
Hypercare end date: [DATE]
BAU owner team: [ROLE / TEAM NAME] — [SIZE]

Performance context:
- KPIs that must be tracked: [LIST from /benefits-register]
- Reporting currently in place: [BRIEF — e.g. "Manual weekly email report; no automated dashboard"]
- Current issues open: [LIST]

Stakeholders who must stay engaged in BAU:
- [ROLE] — [interest level: operational / strategic] — [availability]
- [ROLE] — [interest] — [availability]

Constraints on the BAU operating model:
- [e.g. "BAU team has limited bandwidth — max 3 recurring meetings per week"]
- [e.g. "Executive sponsor wants quarterly visibility only going forward"]
- [e.g. "Need a mechanism to capture improvement ideas from front-line users"]

Prior CI experience:
- Does this team have an existing improvement process? [Y/N / BRIEF]
- What has worked well in previous BAU models? [BRIEF]
```

## Expected output
Three-layer operating rhythm (operational daily/weekly, performance monthly/quarterly, strategic annual), forum design for each layer with purpose/attendees/agenda template, CI loop design, exit checklist from consulting to BAU, and documentation requirements.

## Chain next
- Performance forum → `/performance-review` to run the monthly/quarterly cycle
- If improvement opportunities surfaced → `/continuous-improvement-backlog`
