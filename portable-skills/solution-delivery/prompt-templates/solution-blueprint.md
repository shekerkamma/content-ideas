---
skill: /solution-blueprint
pack: solution-delivery
chains-from: /ai-use-case-prioritiser, /ai-build-buy-partner, /transformation-roadmap
chains-into: /architecture-decision-record, /integration-sequencing, /raci-design
---

# Prompt Template: Solution Blueprint

**When to use:** First step after the use case portfolio is set and sourcing decisions are made — translate the "what" into a structured delivery design.

## Copy-paste prompt

```
Run /solution-blueprint for [CLIENT NAME]:

Use case(s) in scope for this blueprint:
1. [USE CASE NAME] — [brief description]

Scope:
- Business domain: [e.g. "Procurement automation", "Customer service"]
- Business outcomes required: [LIST — e.g. "Reduce PO processing time by 50%", "Handle 60% of L1 support autonomously"]
- Success metrics: [LIST]
- Timeline constraint: [e.g. "Go-live by Q4 2026"]

Technical context:
- Core systems involved: [LIST — e.g. "SAP S/4HANA, Salesforce, legacy Oracle"]
- Existing AI / ML infrastructure: [BRIEF]
- Cloud platform: [AWS / Azure / GCP / hybrid]
- Integration constraints: [e.g. "Must use SAP OData APIs; no direct DB access"]
- Security / compliance requirements: [BRIEF]

Team context:
- Internal build team available: [SIZE / SKILLS]
- External partners involved: [LIST]
- Sourcing decisions made: [FROM /ai-build-buy-partner, or BRIEF]

Assumptions:
- [LIST any assumptions we are making about data, access, team, timeline]
```

## Expected output
Capability map, component register (build/buy/partner per component), workstream breakdown, phased delivery plan (thin thread first), integration overview, and design constraints register.

## Chain next
- Run `/architecture-decision-record` for any major decisions embedded in this blueprint (data storage, model selection, integration pattern)
- Run `/integration-sequencing` to plan the data and system integration order
