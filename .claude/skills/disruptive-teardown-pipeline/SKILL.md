---
name: disruptive-teardown-pipeline
description: Use when mapping agentic use cases against incumbent SaaS/BPO/workflow vendors to expose pricing friction, onboarding friction, feature bloat, and the disruptive agentic wedge before blueprint generation.
argument-hint: "[use-case-name|all|category]"
permissions:
  network: true
  file_read:
    - "runs/2026-06-26-agentic-opportunity-blueprints/**"
  file_write:
    - "runs/2026-06-26-agentic-opportunity-blueprints/**"
---

# Disruptive Teardown Pipeline

This skill is the market-mapping stage before Master Implementation Blueprints.
The job is to name the incumbents, expose the economic and workflow friction,
and define the disruptive agentic wedge. It does **not** build the use case.
It produces research-backed dossiers that feed implementation-ready capability
blueprints.

## Runtime Preamble

I will map the incumbent landscape, pricing/onboarding friction, and agentic
wedge before any blueprint generation. The output is a competitor teardown
dossier, not product implementation.

## Inputs

Default run root:
`runs/2026-06-26-agentic-opportunity-blueprints/`

Read, in order:

1. `source/Agent_Use_Cases_Phase1.md`
2. `source/Agent_Use_Cases_Phase2.md`
3. Existing `source/*_Competitor_Teardown.md` as prior drafts only.
4. GBrain recall for recurring companies, categories, and verticals.
5. Fresh web/deep research for current competitor, pricing, onboarding, buyer
   complaints, regulatory constraints, and implementation signals.

## Source / Tool Order

1. Local scorecard and prior teardown files.
2. GBrain recall before external research.
3. `you-com-search` or Hermes You.com backend for current-web search,
   livecrawl, research, and finance research when available.
4. Specialist research plugins/MCPs or deep research agents when available,
   especially Exa for semantic/source discovery and Firecrawl for page capture.
5. Official vendor product, docs, and pricing pages.
6. Regulatory sources, public filings, review sites, analyst pages, credible
   customer/community complaints, and implementation docs.
7. Generic web search only as fallback/source discovery.

Do not fabricate exact enterprise pricing. If pricing is sales-led or hidden,
state that plainly and treat opacity as buyer friction.

## Workflow

1. Resolve target use case or category.
2. Extract the scorecard row: agent type, SaaS affected, proof, verdict, and
   vertical.
3. Discover incumbents:
   - 5-10 direct competitors.
   - Adjacent workflow/platform incumbents.
   - BPO/services/manual-work alternatives where relevant.
4. For each incumbent, capture:
   - Product category and positioning.
   - Top features/workflows.
   - Pricing signal: public tiers, usage pricing, per-seat model, sales-led
     pricing, minimum commitments, add-ons, or implementation/services burden.
   - Onboarding friction: implementation time, admin burden, data migration,
     workflow configuration, integration complexity, training, procurement.
   - Strengths: what makes the incumbent sticky.
   - Weaknesses: feature bloat, per-seat tax, human middleware, opacity,
     brittle configuration, slow deployment, poor UX, or poor fit for messy
     unstructured work.
5. Define the disruptive strategy:
   - Direct threats.
   - Table-stakes features to copy.
   - What **not** to build.
   - What system of record to keep.
   - Agentic wedge.
   - 30-day capability proof.
6. Write output to:
   `runs/2026-06-26-agentic-opportunity-blueprints/teardowns/<UseCase>_Disruptive_Teardown.md`
7. Update or reference the teardown from the corresponding Master Blueprint.

## Output Template

```markdown
---
status: draft | reviewed | blocked
use_case: "<name>"
last_updated: "YYYY-MM-DD"
source_confidence:
  competitor: low | medium | high
  pricing: low | medium | high
  workflow: low | medium | high
---

# <Use Case> Disruptive Competitor Teardown

## Market Frame
- Workflow:
- Target buyer:
- Existing spend category:
- Incumbent economic model:
- Agentic wedge:

## Incumbent Map
| Incumbent | Category | Buyer | Pricing Signal | Onboarding / Admin Friction | Strength | Weakness |
|---|---|---|---|---|---|---|

## Direct Threats
1. ...
2. ...

## Adjacent / Hidden Competitors
- BPO/manual work:
- Internal tools:
- Horizontal platforms:
- System of record:

## Pricing Friction
- Public pricing:
- Sales-led/hidden pricing:
- Add-ons/minimums:
- Implementation/services burden:

## Onboarding And Workflow Friction
- Setup burden:
- Admin burden:
- Data/integration burden:
- User friction:
- Procurement friction:

## What Not To Build
- ...

## What To Keep
- System of record:
- Existing vendor APIs:
- Human approval points:

## Agentic Wedge
- Wedge statement:
- Why it wins:
- Why now:
- 30-day proof:

## Blueprint Inputs
- Scope implication:
- Architecture implication:
- Build-vs-buy implication:
- ROI implication:
- QA/deployment implication:

## Source Notes
- <source> - <url> - accessed YYYY-MM-DD - claim supported
```

## Gotchas

- Do not position this as immediate product build work.
- Do not use "$100K-tier" as the offer language. The positioning is AI-native
  operator rigor compressing slow traditional discovery.
- Do not say the agent "crushes" incumbents in client-facing assets. Use
  "exposes," "compresses," "bypasses," "renegotiates," or "disrupts."
- Do not build a new system of record unless the use case truly requires one.
  Most wedges sit on top of the incumbent system and collapse seat/admin/BPO
  economics.
- Pricing opacity is evidence, but do not invent the hidden price.

## Skill Relationships

### Category
Data & Analysis

### Dependencies
- `agentic-blueprint-pipeline` consumes this skill's teardown dossiers.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `agentic-blueprint-pipeline` | Sequential downstream | always for implementation-ready blueprints | `teardowns/*_Disruptive_Teardown.md` |
| `branded-pptx-deck` | Sequential downstream | after reviewed teardowns and blueprints exist | deck-ready summaries |

### Host Compatibility
Canonical source is `.claude/skills/disruptive-teardown-pipeline/SKILL.md`.
Codex/OpenHands can use the repo-local wrapper at
`skills/disruptive-teardown-pipeline/SKILL.md`.
