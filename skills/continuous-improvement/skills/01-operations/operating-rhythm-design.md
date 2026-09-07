---
name: operating-rhythm-design
description: Designs the BAU governance and operating rhythm for a capability or function post go-live — forums, reporting cadence, performance reviews, and ownership structure. Use at the end of hypercare when the organisation transitions to self-sustaining operations.
---

# Operating Rhythm Design

## When To Use

Use at the end of the hypercare period when the consulting team is transitioning to BAU. An operating rhythm is the governance equivalent of a maintenance schedule — it defines how the organisation will keep the capability running, improving, and governed without external support. Organisations that inherit a capability without an operating rhythm revert to old behaviours within 90 days.

## Consulting Approach

A sustainable operating rhythm has three layers: operational (daily/weekly run-the-business activities), performance (monthly/quarterly measure-and-improve reviews), and strategic (annual capability review and investment decision). Most organisations design only the first layer and discover the others are missing when performance starts to drift. The operating rhythm must be owned by the business, not IT or a project team.

## Workflow

1. Define the three layers of the operating rhythm: operational, performance, and strategic.
2. Design the forums for each layer: who attends, what decisions are made, what triggers escalation.
3. Define the metrics and reporting pack that feeds each forum.
4. Assign ownership: who is accountable for each layer of the rhythm.
5. Design the continuous improvement loop: how issues identified in operational forums feed into performance review and investment decisions.
6. Document the rhythm in a runbook that the organisation can execute without consulting support.

## Output Format

```markdown
# Operating Rhythm Design — [Capability / Function]
**Effective Date:** [YYYY-MM-DD]  **Owner:** [Role]

## Rhythm Overview
| Layer | Cadence | Forum | Owner | Purpose |
|---|---|---|---|---|
| Operational | Daily / Weekly | | | Run the business |
| Performance | Monthly / Quarterly | | | Measure and improve |
| Strategic | Annual | | | Invest and evolve |

## Forum Design

### Operational Forum
- **Cadence:** [e.g. Weekly, 30 min]
- **Owner:** [Role]
- **Attendees:** [Roles]
- **Standard Agenda:**
  1. Operational health check (SLAs, incidents, usage)
  2. Issues requiring escalation
  3. Upcoming events and changes
- **Triggers escalation to Performance Forum when:** [Condition]

### Performance Review Forum
- **Cadence:** [e.g. Monthly, 90 min]
- **Owner:** [Role]
- **Attendees:** [Roles]
- **Standard Agenda:**
  1. KPI review vs. targets
  2. Benefits realisation update
  3. Issue root causes and trend analysis
  4. Improvement backlog prioritisation
- **Triggers escalation to Strategic Forum when:** [Condition]

### Strategic Review Forum
- **Cadence:** [e.g. Annual or bi-annual]
- **Owner:** [Senior leader]
- **Standard Agenda:**
  1. Capability maturity assessment
  2. Benefits vs. business case
  3. Investment decisions for next period
  4. Strategic alignment check

## Metrics and Reporting Pack
| Metric | Owner | Source | Frequency | Threshold for Escalation |
|---|---|---|---|---|

## Continuous Improvement Loop
[How an issue identified in an operational forum becomes a prioritised improvement item, gets funded, is delivered, and is measured.]

## BAU Ownership Register
| Activity | Owner | Backup | Frequency | Runbook Reference |
|---|---|---|---|---|

## Consulting Exit Checklist
| Item | Status | Owner | Date |
|---|---|---|---|
| Runbook documented and handed over | | | |
| BAU team trained and signed off | | | |
| Operating rhythm booked in calendars | | | |
| Metrics reporting automated | | | |
| Escalation path tested | | | |
```

## Quality Bar

- All three rhythm layers must be designed — operational-only rhythms drift without performance and strategic reviews.
- Every forum must have a named business owner, not a technology or project owner.
- Continuous improvement loop must be closed — an issue that enters the loop must have a defined path to resolution or deferral.
- Consulting exit checklist must be signed off before the team exits — a checklist that is completed after exit is not a handover.
