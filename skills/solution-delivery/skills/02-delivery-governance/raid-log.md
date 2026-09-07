---
name: raid-log
description: Builds and maintains a structured Risks, Assumptions, Issues, Dependencies register with owners, RAG status, and response actions. Use at programme kickoff and refresh at every stage gate.
---

# RAID Log

## When To Use

Use at programme kickoff to establish the first RAID baseline, and refresh after every stage gate review or when a significant change occurs. RAID logs that are populated once and never reviewed become liabilities; the value is in the weekly triage discipline, not the initial capture.

## Consulting Approach

PRINCE2 and MSP treat RAID as the primary early-warning system for a programme. Every item must have a named owner (not a team), a response action (not just a description), and a RAG status that is updated on a defined cadence. Assumptions are the most under-managed item — an unvalidated assumption that turns false becomes an issue or risk with no owner.

## Workflow

1. Facilitate a RAID workshop with the core delivery team and workstream leads.
2. Capture all Risks (something that might happen), Assumptions (things believed true but not confirmed), Issues (things already happening), and Dependencies (things this programme needs from others).
3. For each Risk: score probability (H/M/L) and impact (H/M/L); assign owner; define response (Avoid / Reduce / Transfer / Accept).
4. For each Assumption: assign owner to validate; set validation date.
5. For each Issue: assign owner; define resolution action and target date.
6. For each Dependency: identify provider; confirm status and delivery date.
7. Set RAG status and review cadence for the full log.

## Output Format

```markdown
# RAID Log — [Programme Name]
**Version:** [n]  **Last Updated:** [YYYY-MM-DD]  **Review Cadence:** [Weekly / Fortnightly]

## Risks
| ID | Description | Probability | Impact | RAG | Owner | Response Type | Response Action | Due |
|---|---|---|---|---|---|---|---|---|

## Assumptions
| ID | Description | Owner | Validation Method | Validation Date | Status |
|---|---|---|---|---|---|

## Issues
| ID | Description | Raised Date | RAG | Owner | Resolution Action | Target Date |
|---|---|---|---|---|---|---|

## Dependencies
| ID | What We Need | From Whom | Delivery Date | Status | Escalation Path |
|---|---|---|---|---|---|

## RAG Summary
| Category | Red | Amber | Green | Total |
|---|---|---|---|---|
```

## Quality Bar

- Every item has a named individual owner, not a team or workstream label.
- Red RAG items must have a named escalation owner and an escalation deadline.
- Assumptions must have a validation date — an assumption with no validation date is an unmanaged risk.
- Dependencies with no confirmed delivery date are automatically Amber until confirmed.
