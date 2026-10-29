---
name: architecture-decision-record
description: Documents a key architecture or design decision with context, alternatives, rationale, and consequences. Use when a significant technical or structural choice must be made traceable and reversible.
---

# Architecture Decision Record

## When To Use

Use when a significant decision must be locked in — technology selection, integration pattern, data model, platform choice, or organisational design — and the decision needs to be auditable, challengeable, and revisable if context changes.

## Consulting Approach

Good decisions age well when the reasoning is recorded, not just the outcome. An ADR that only records "we chose X" becomes useless the moment the team changes. Record the context that made X the right answer, the alternatives that were rejected and why, and the conditions under which the decision should be revisited.

## Workflow

1. Name the decision precisely — one sentence, verb-first (e.g. "Use event-driven integration between CRM and ERP rather than batch").
2. Document the context: what forces, constraints, or prior decisions make this choice necessary now.
3. List alternatives considered (minimum 2, including status quo).
4. State the decision and the primary rationale.
5. Identify consequences: what becomes easier, what becomes harder, what is now ruled out.
6. Set a review trigger: the condition or date under which this decision should be revisited.

## Output Format

```markdown
# ADR-[number]: [Decision Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded by ADR-X]
**Date:** [YYYY-MM-DD]
**Deciders:** [Names or roles]

## Context
[What situation, constraint, or prior decision forces this choice? What would happen if no decision were made?]

## Alternatives Considered
| Option | Upside | Downside | Verdict |
|---|---|---|---|

## Decision
[State the choice in one paragraph. Be direct.]

## Rationale
[Why this option over the others? Reference context factors explicitly.]

## Consequences
**Positive:** [What becomes easier or unlocked.]
**Negative:** [What becomes harder or foreclosed.]
**Risks:** [What could go wrong and under what conditions.]

## Review Trigger
[The condition, date, or event that should prompt revisiting this decision.]
```

## Quality Bar

- Decision title must be specific enough that someone new to the project can understand what was decided without reading the body.
- Alternatives must include at least one option that was seriously considered, not strawmen.
- Consequences section must name something negative — no decision is purely upside.
- Review trigger must be concrete, not "when the situation changes."
