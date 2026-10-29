---
skill: /capability-maturity-progression
pack: continuous-improvement
chains-from: /performance-review (annual), /post-implementation-review
chains-into: /transformation-roadmap, /ai-maturity-assessment (next cycle)
---

# Prompt Template: Capability Maturity Progression

**When to use:** Annually — assess where the capability sits on the maturity model, identify what is blocking the next level, and plan the investments to get there.

## Copy-paste prompt

```
Run /capability-maturity-progression for [CLIENT NAME]:

Capability being assessed: [NAME — e.g. "AI-assisted invoice processing", "Predictive maintenance"]
Last assessment: [DATE or FIRST ASSESSMENT]
Last assessed level: [1-5 or N/A]

Evidence for current maturity (one statement per dimension is enough):

Process dimension:
- [e.g. "Process is documented and followed consistently by 90% of users"]

Technology dimension:
- [e.g. "System is stable, monitored, and has 99.5% uptime; model retraining is manual"]

Data dimension:
- [e.g. "Data pipeline is automated but data quality issues arise monthly without automated detection"]

Talent dimension:
- [e.g. "BAU team can operate the system but cannot diagnose model drift; depends on IT for advanced issues"]

Governance dimension:
- [e.g. "Monthly performance reviews occur but no formal KPI ownership below VP level"]

Target maturity ambition:
- Target level for 12–18 months: [1-5]
- Reason: [BRIEF — what becomes possible at the next level]

Investment constraints:
- Budget available for maturity progression: [£X / APPROXIMATE / CONSTRAINED]
- Internal capacity: [BRIEF]
```

## Expected output
Maturity scorecard (current level per dimension), overall level (minimum dimension), blocker analysis with root causes, maturity progression roadmap (quarterly), leading indicators of progression, and strategic investment case for the next level.

## Chain next
- Progression roadmap → `/transformation-roadmap` to plan and fund the investment
- AI-specific capabilities → `/ai-maturity-assessment` for the next strategy cycle
