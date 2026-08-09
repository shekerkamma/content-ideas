---
name: solution-blueprint
description: Translates a chosen strategic option into a structured capability-component map. Use after /strategic-options or /transformation-roadmap when you need to define what will be built, by whom, in what sequence.
---

# Solution Blueprint

## When To Use

Use when a strategic option has been chosen and the team needs to define the solution architecture: what capabilities are required, what components deliver each capability, which workstreams own each component, and in what order they should be built.

## Consulting Approach

Start from outcomes, not features. Every component must trace back to a business capability; every capability must trace back to a strategic outcome from the business case. Use a layered blueprint: outcome → capability → component → workstream → phase. Make dependencies visible before sequencing.

## Workflow

1. Import the chosen option from `/strategic-options` or the transformation objective from `/transformation-roadmap`.
2. Decompose the objective into 3–7 business capabilities (what the organisation must be able to do, not what technology does).
3. For each capability, identify the components required: process changes, technology, data, people/role changes.
4. Map each component to a workstream and an accountable owner.
5. Identify cross-component dependencies and flag integration risks.
6. Sequence components into phases (Foundation → Core → Scale) based on dependency order and value delivery.

## Output Format

```markdown
# Solution Blueprint

## Strategic Objective
[One sentence from the business case or strategic options output.]

## Capability Map
| # | Capability | What It Enables | Owner |
|---|---|---|---|

## Component Register
| Capability | Component | Type (Process / Tech / Data / People) | Workstream | Phase | Depends On |
|---|---|---|---|---|---|

## Dependency Map
[Describe 3–5 critical dependencies and the risk if sequencing is violated.]

## Phasing Summary
| Phase | Name | Capabilities Delivered | Key Milestone | Duration |
|---|---|---|---|---|

## Open Design Questions
[Questions that must be resolved before detailed planning begins.]
```

## Quality Bar

- Every component traces to a capability; every capability traces to a strategic outcome.
- Dependencies are named explicitly — do not assume parallel workstreams are independent.
- Phases are defined by dependency order and value delivery, not calendar convenience.
- Flag integration risks at the boundary between workstreams.
