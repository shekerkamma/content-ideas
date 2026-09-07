---
skill: /architecture-decision-record
pack: solution-delivery
chains-from: /solution-blueprint
chains-into: /solution-blueprint (updated), /raid-log
---

# Prompt Template: Architecture Decision Record

**When to use:** Any time a major technical decision is made during delivery — one ADR per significant decision. Typical triggers: model selection, data storage architecture, integration pattern, build-vs-buy for a component.

## Copy-paste prompt

```
Run /architecture-decision-record for [CLIENT NAME]:

Decision title: [SHORT TITLE — e.g. "Vector database selection for enterprise RAG"]

Context:
- What problem are we solving: [BRIEF]
- Why this decision matters now: [BRIEF]
- What are the constraints: [LIST — e.g. "Must run in Azure, must be enterprise-supported, budget < £X/month"]

Options under consideration:
1. [OPTION A] — [brief description]
2. [OPTION B] — [brief description]
3. [OPTION C, if any]

Our current lean:
- Preferred option: [A / B / C / UNDECIDED]
- Reason for lean: [BRIEF]

Stakeholders who need to ratify this decision:
- [ROLE] — [organisation] — [stance: informed / consulted / decision-maker]
```

## Expected output
ADR document in standard format: context, options with pros/cons, decision, rationale, consequences, open questions, and review trigger condition.

## Chain next
- Update `/solution-blueprint` where the decision affects the design
- Add any risks identified during the decision to `/raid-log`
