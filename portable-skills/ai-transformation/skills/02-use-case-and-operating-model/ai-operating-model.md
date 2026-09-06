---
name: ai-operating-model
description: Designs how an organisation's AI function should be structured — Centre of Excellence, federated, embedded, or hybrid — including roles, governance, funding, and capability build sequencing. Use after /ai-maturity-assessment when the organisation is ready to industrialise beyond individual pilots.
---

# AI Operating Model

## When To Use

Use when an organisation is moving from isolated AI pilots to systematic deployment and needs to decide how the AI function should be organised, governed, and resourced. Organisations that skip this step end up with fragmented AI teams, duplicated tooling, inconsistent governance, and an inability to scale what works.

## Consulting Approach

Accenture identifies four AI operating model archetypes: Centralised CoE (standard setting, shared services, platform ownership), Federated (business units own delivery, centre provides guardrails), Embedded (AI talent sits permanently inside business units), and Hybrid (platform and governance centralised; delivery federated). The right model depends on maturity, culture, and the nature of the use case portfolio. Most large organisations evolve toward Hybrid as they scale.

## Workflow

1. Assess the current AI organisational state: where do AI capabilities exist today, and where do decisions get made?
2. Evaluate the four archetypes against the organisation's maturity score, culture, and use case portfolio.
3. Select the target archetype and design the governance model: who sets standards, who funds, who delivers, who reviews.
4. Define the roles required: AI leadership, ML engineers, data scientists, AI product owners, responsible AI leads, AI translators.
5. Design the capability build sequence: what to hire, what to upskill, what to partner for.
6. Produce the transition plan from current state to target operating model.

## Output Format

```markdown
# AI Operating Model Design — [Organisation]
**Date:** [YYYY-MM-DD]  **Maturity Level (from assessment):** [n]

## Current State
[How AI is currently organised. Where capabilities exist. Decision-making fragmentation. Key tensions.]

## Archetype Evaluation
| Archetype | Fit with Culture | Fit with Maturity | Fit with Use Case Portfolio | Verdict |
|---|---|---|---|---|
| Centralised CoE | | | | |
| Federated | | | | |
| Embedded | | | | |
| Hybrid | | | **Recommended** | |

## Target Operating Model

### Structure
[Describe the recommended structure in plain language. What sits centrally, what sits in business units, how they interact.]

### Governance Design
| Decision | Who Decides | Who Advises | Cadence |
|---|---|---|---|
| AI strategy and portfolio | | | |
| Platform and tooling standards | | | |
| Use case funding | | | |
| Responsible AI review | | | |
| Talent and capability investment | | | |

### Role Requirements
| Role | Reporting Line | FTE Required | Hire vs Upskill vs Partner | Priority |
|---|---|---|---|---|

### Funding Model
[How is AI funded: central budget, business unit charge-back, product P&L, shared investment? What is the governance of the budget?]

## Capability Build Sequence
| Phase | Capability | Build Method | Timeline |
|---|---|---|---|

## Transition Plan
| From | To | Key Actions | Owner | Timeline |
|---|---|---|---|---|

## Success Metrics
| Metric | Current | 12-Month Target | 24-Month Target |
|---|---|---|---|
```

## Quality Bar

- Archetype selection must be justified against the specific organisation's maturity, not generic best practice.
- Governance design must name individuals or roles for each decision — "the AI team" is not a decision-maker.
- Capability build plan must distinguish hire, upskill, and partner explicitly — do not assume all roles are hired.
- Transition plan must account for the current organisation's politics and constraints, not just the ideal end state.
