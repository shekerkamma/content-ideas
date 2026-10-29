# Four-Tier Artifact System

Every AI use case in this bundle is described at four levels of abstraction. Understanding which tier a question is operating at determines what artifact to produce or consult.

```
TIER 1 — Enterprise AI Platform Architecture
  Cross-cutting: shared security, governance, responsible AI controls, compliance posture
  Audience: CTO, CISO, CMO, Compliance, Platform Engineering
  Question: "What platform do all our AI workloads deploy into?"

  ↓ every Solution Blueprint deploys into this platform

TIER 2 — Solution Blueprint (per use case)
  HOW TO BUILD: architecture diagram, component breakdown, integration points, build-vs-buy
  Audience: Enterprise Architect, Delivery Lead, Cloud Architect
  Question: "How do I build this specific use case?"

  ↓ linked from

TIER 3 — Use Case Card (per use case)
  WHAT + WHY: business value, ROI benchmarks, hyperscaler evidence, risk/readiness
  Audience: Business Buyer, Account Executive, CDO/COO sponsor
  Question: "Should I invest in this use case?"

  ↓ implements

TIER 4 — Realization Pattern
  THE PATTERN: technical pattern spec, decision criteria, code snippets, cost model
  Audience: Data Engineer, ML Engineer, Implementer
  Question: "What pattern does this use case implement, and how?"
```

## Example: Prior Authorization Automation (Healthcare)

| Tier | Artifact | Primary audience |
|---|---|---|
| Tier 1 | Healthcare Payer Enterprise AI Platform Architecture (AWS) | CISO + CMO + Compliance |
| Tier 2 | Prior Authorization Automation — Solution Blueprint | Enterprise Architect |
| Tier 3 | Prior Authorization Automation — Use Case Card | Business Buyer / AE |
| Tier 4 | RAG (Retrieval Augmented Generation) + Multi-Agent | Implementer |

## Example: Enterprise AI Data Catalog (Cross-Industry)

| Tier | Artifact | Primary audience |
|---|---|---|
| Tier 1 | Healthcare Payer Enterprise AI Platform Architecture (GCP) | CTO + CDO |
| Tier 2 | *(Solution Blueprint pending)* | — |
| Tier 3 | Enterprise AI Data Catalog — Use Case Card | CDO + Data Stewards |
| Tier 4 | Enterprise Knowledge Graph + MCP | Data Engineer |

## How to navigate a tier-4 question from a tier-3 symptom

Business buyers ask tier-3 questions: "can we automate prior auth?" → this maps to a Tier 3 Use Case Card.
The Use Case Card references the Tier 4 pattern (e.g. RAG or multi-agent) for implementation evidence.
When the buyer agrees to proceed, the next artifact needed is the Tier 2 Solution Blueprint.
That blueprint inherits security/governance controls from the Tier 1 Platform Architecture.

Always identify the tier first. Answering a tier-3 business question with tier-4 implementation details is a common consulting mistake.

## When to write a new Tier 1 architecture

One Tier 1 document per: cloud provider × regulatory context × organization.
A single large enterprise may need 2–3: e.g., AWS (healthcare payer), GCP (analytics platform), Azure (Microsoft 365 integration).
Do not write a new Tier 1 for each use case — that defeats the purpose of a shared platform.
