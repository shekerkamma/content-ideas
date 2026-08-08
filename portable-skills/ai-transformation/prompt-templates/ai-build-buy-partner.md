---
skill: /ai-build-buy-partner
pack: ai-transformation
chains-from: /ai-operating-model, /strategic-options
chains-into: /commercial-structuring, /solution-blueprint
---

# Prompt Template: AI Build-Buy-Partner

**When to use:** After the AI operating model is defined and use cases are prioritised — when sourcing decisions must be made for each capability in the portfolio.

## Copy-paste prompt

```
Run /ai-build-buy-partner for [CLIENT NAME]:

AI capabilities required (from use case portfolio):
1. [CAPABILITY] — enables: [USE CASES] — [BRIEF DESCRIPTION]
2. [CAPABILITY] — enables: [USE CASES] — [BRIEF DESCRIPTION]
[continue for all capabilities...]

Organisation context:
- Internal AI engineering team: [EXISTS / SIZE / SKILLS]
- Existing vendor relationships: [LIST — e.g. "Microsoft Azure EA, SAP licences, Salesforce"]
- IP protection priority: [HIGH / MEDIUM / LOW]
- Speed-to-value priority: [HIGH / MEDIUM / LOW — board expectation on timeline]
- Build budget available: [APPROXIMATE]
- Regulatory constraints on vendor data sharing: [BRIEF]

Strategic context:
- Which capabilities are genuinely differentiating vs. commodity: [BRIEF]
- Competitor sourcing known: [BRIEF — e.g. "Competitor uses Salesforce Einstein for this"]
```

## Expected output
Capability register with Build/Buy/Partner decision per capability, rationale for each decision, vendor shortlist for Buy/Partner capabilities with commercial model recommendation, portfolio risk assessment (single points of failure, vendor lock-in).

## Chain next
- Pass Buy/Partner commercial terms into `/commercial-structuring`
- Use Build capabilities to inform team and timeline in `/solution-blueprint`
