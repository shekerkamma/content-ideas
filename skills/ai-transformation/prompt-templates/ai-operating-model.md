---
skill: /ai-operating-model
pack: ai-transformation
chains-from: /ai-maturity-assessment, /operating-model-design
chains-into: /raci-design, /transformation-roadmap
---

# Prompt Template: AI Operating Model Design

**When to use:** When the organisation is moving from isolated AI pilots to systematic deployment and needs to decide how the AI function is organised, governed, and resourced.

## Copy-paste prompt

```
Run /ai-operating-model for [CLIENT NAME]:

Current AI organisational state:
- Where AI capabilities exist today: [LIST — e.g. "data science team in IT (5 FTE), AI pilot in marketing (2 FTE contractors)"]
- How AI decisions are made today: [BRIEF — e.g. "ad hoc, no central governance"]
- AI budget ownership: [BRIEF]
- Business unit AI maturity variation: [e.g. "BU1 advanced, BU2 and BU3 just starting"]

Organisation context:
- Total employees: [N]
- Number of business units: [N]
- Culture: [CENTRALISED / FEDERATED / MATRIX]
- AI maturity level: [1–4]

Use case portfolio (from /ai-use-case-prioritiser):
- Wave 1 use cases: [LIST]
- Domains covered: [LIST]

Design goals:
- [e.g. "Scale from 2 pilots to 10 use cases in 18 months"]
- [e.g. "Establish responsible AI governance before any customer-facing deployment"]
- [e.g. "Build internal capability — reduce dependence on external consultants by Year 2"]
```

## Expected output
Archetype evaluation (CoE / Federated / Embedded / Hybrid), target operating model with governance design, role requirements (hire/upskill/partner), funding model, capability build sequence, and transition plan.

## Chain next
- Pass role requirements into `/raci-design` to assign accountability
- Use capability build sequence to inform `/transformation-roadmap`
