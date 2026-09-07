---
name: integration-sequencing
description: Orders system and process integrations by dependency, risk, and value delivery sequence. Use when a solution blueprint involves multiple connected systems and the build/test sequence is unclear.
---

# Integration Sequencing

## When To Use

Use when a solution involves more than two systems or process handoffs and the team needs to know which integrations to build first, in what order to test them, and what the rollback position is if a late-stage integration fails.

## Consulting Approach

Integrations fail at boundaries. Sequence them to surface boundary failures as early as possible, not as late as possible. Start with the data foundation, then the core transactional integrations, then the enrichment and reporting layers. Never defer a high-risk integration to the final phase — it will become the critical path.

## Workflow

1. List every integration point: system-to-system, process-to-system, data feed, API, file exchange.
2. For each integration, score two dimensions: dependency criticality (does anything else depend on this?) and technical risk (new API, legacy system, high data volume, complex mapping).
3. Identify the minimum set of integrations needed for the first end-to-end test (the "thin thread").
4. Sequence remaining integrations in dependency order, with high-risk integrations pulled earlier.
5. Define test gates: what must be verified before the next integration can begin.
6. Specify rollback position for each phase: what is the fallback if this integration cannot be completed?

## Output Format

```markdown
# Integration Sequencing Plan

## Integration Inventory
| # | From System | To System | Type | Data / Trigger | Criticality (H/M/L) | Tech Risk (H/M/L) |
|---|---|---|---|---|---|---|

## Thin Thread (Minimum End-to-End)
[Name the minimum set of integrations needed to test the core flow. This is Phase 1.]

## Sequenced Build Plan
| Phase | Integrations | Entry Criteria | Exit / Test Gate | Rollback Position |
|---|---|---|---|---|

## High-Risk Integration Detail
[For each H/H integration, describe the specific risk and the mitigation approach.]

## Dependency Map
[Diagram or list: which integration must complete before another can begin.]
```

## Quality Bar

- Every integration must be assigned an owner — "TBD" is not a valid owner.
- High-risk integrations must appear in Phase 1 or Phase 2, never in the final phase.
- Rollback position must be operationally viable, not theoretical.
- Test gates must be verifiable — a specific system state or data assertion, not "works as expected."
