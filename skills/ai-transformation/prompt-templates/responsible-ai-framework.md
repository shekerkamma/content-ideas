---
skill: /responsible-ai-framework
pack: ai-transformation
chains-from: /ai-use-case-prioritiser, /risk-and-mitigation
chains-into: /solution-blueprint, /raid-log
---

# Prompt Template: Responsible AI Framework

**When to use:** Before any customer-facing or high-stakes AI deployment, or when a board, regulator, or enterprise risk function requires a documented AI governance position.

## Copy-paste prompt

```
Run /responsible-ai-framework for [CLIENT NAME]:

Organisation context:
- Industry: [INDUSTRY — flag if regulated: financial services, healthcare, public sector]
- Regulatory environment: [e.g. "EU AI Act applies, GDPR, FCA regulated"]
- Existing ethics or data governance policies: [EXISTS / NONE / BRIEF]
- Board / risk committee AI governance requirements: [BRIEF]

AI use cases in scope:
1. [USE CASE] — [customer-facing Y/N] — [automated decision Y/N] — [sensitive data Y/N]
2. [USE CASE] — [customer-facing Y/N] — [automated decision Y/N] — [sensitive data Y/N]
[continue...]

Known risk concerns:
- [e.g. "Credit decisioning use case — risk of discriminatory outcomes"]
- [e.g. "Customer service chatbot — risk of hallucinated responses affecting advice"]

Governance preferences:
- Existing review bodies we can leverage: [LIST]
- Preference for lightweight vs. comprehensive governance: [BRIEF]
```

## Expected output
Responsible AI principles with "what we will not do" statements, risk tier taxonomy (Low/Medium/High/Critical), use case risk register, governance requirements per tier, review board design, monitoring cadence, and regulatory mapping.

## Chain next
- Use risk tier classifications to inform `/solution-blueprint` design decisions
- Add High/Critical use case risks to the `/raid-log`
