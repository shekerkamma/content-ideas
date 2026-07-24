---
name: agentic-blueprint-pipeline
description: Use when generating or upgrading research-backed Agentic Master Implementation Blueprints for market-positioning portfolios from use-case scorecards, competitor teardowns, and deep research.
argument-hint: "[use-case-name|all|gold-standard]"
permissions:
  network: true
  file_read:
    - "runs/2026-06-26-agentic-opportunity-blueprints/**"
  file_write:
    - "runs/2026-06-26-agentic-opportunity-blueprints/**"
---

# Agentic Blueprint Pipeline

This skill upgrades shallow opportunity sketches into research-backed Master
Implementation Blueprints. The goal is market positioning and capability
demonstration, not product implementation. We are not building these use cases
now. We are producing implementation-ready artifacts that show we can identify
the disruptive wedge, name the incumbents, quantify the economics, and bring
enough architecture detail to the table on day one that a buyer can see
immediate execution capability. A reviewed blueprint must not stop at "we know
the market"; it must show the technical path: stack, schema, APIs,
integrations, QA edges, deployment, and post-launch operating loop.

## Runtime Preamble

I will use the local scorecard, prior teardown files, GBrain recall, and fresh
deep research before drafting. I will generate Markdown first, then deck-ready
summaries after the Markdown clears the quality rubric.

## Inputs

Default run root:
`runs/2026-06-26-agentic-opportunity-blueprints/`

Read, in this order:
1. `source/Agent_Use_Cases_Phase1.md`
2. `source/Agent_Use_Cases_Phase2.md`
3. Reviewed disruptive teardown dossier from
   `teardowns/*_Disruptive_Teardown.md` when available.
4. Matching legacy `source/*_Competitor_Teardown.md` when available.
5. Existing `blueprints/*_Master_Blueprint.md` as prior draft only.
6. `source/original-10-skill-stack.txt` for the original prompt lineage.
7. GBrain recall for the use case, company names, vertical, and recurring
   themes.
8. Fresh web/deep research for current competitor, pricing, regulatory, and
   implementation claims.

## Source / Tool Order

1. Local files in the run root.
2. GBrain recall before any external lookup.
3. `you-com-search` or Hermes You.com backend for current-web search,
   livecrawl, research, and finance research when available.
4. Specialist research plugins or MCPs when available, especially Exa for
   semantic/source discovery and Firecrawl for page capture.
5. Official product pages, docs, pricing pages, regulatory sources, public
   filings, and credible review/community sources.
6. Generic web search only as fallback or for source discovery.

Write durable findings back to GBrain after the run when the findings will
matter across future portfolio/deck work.

## Workflow

1. Resolve target set:
   - `$ARGUMENTS = gold-standard`: process these five first:
     `Conversational_Support`, `HR_Onboarding_Agent`,
     `KYC_AML_Onboarding_Agent`, `Prior_Authorization_Agent`,
     `AI_code_assistant`.
   - `$ARGUMENTS = all`: process all files listed in the run manifest.
   - Otherwise process the named use case.
2. Build an evidence pack per use case:
   - Use-case scorecard row.
   - Reviewed disruptive teardown dossier when available.
   - Existing legacy competitor teardown as secondary prior art.
   - Current competitor/pricing/workflow/regulatory research.
   - Source list with URLs and dates accessed.
3. Draft the Markdown blueprint using
   `references/master-blueprint-template.md`.
4. Apply the implementation-depth checklist in
   `references/implementation-depth-checklist.md`.
5. Apply `references/quality-rubric.md`.
6. If the blueprint fails any hard gate, keep status `draft-needs-research`
   and write gaps at the top of the file.
7. Once Markdown passes, create a deck-ready one-page summary under
   `deck/` using the same evidence pack.
8. Update the run README with status and next action.

## Required 10 Artifacts

Every Master Blueprint must contain these sections with evidence-backed
specificity:

1. Problem-Solution Fit Diagnostic
2. 30-Day Scope Definition
3. Tech Stack + Architecture Design
4. Build vs Buy Decision Matrix
5. MVP ROI Business Case
6. Competitor Product Teardown
7. Acceptance Criteria + Test Plan
8. Data Architecture Lite
9. Deployment Sequencing
10. Post-Launch Iteration Plan

## Implementation Depth Standard

The phrase "implementation blueprint" means the artifact is implementation-
ready, not that implementation is starting. Every reviewed blueprint must
demonstrate the delivery approach as if walking into a buyer meeting with the
solution architecture already mapped.

At minimum, include:

- Concrete stack choices with reasoned alternatives.
- System architecture and runtime boundaries.
- Database schema or data model with table/entity names, key fields, indexes,
  tenancy/security model, and retention rules.
- API surface with method/path, input/output shape, auth requirement, and
  failure behavior.
- Integration plan for incumbent systems and third-party services.
- Folder/module structure and required environment variables.
- Acceptance criteria, edge cases, and verification method.
- Deployment sequence, smoke tests, rollback, and observability.

Use `references/implementation-depth-checklist.md` before marking a blueprint
`reviewed`.

## Skill #5 Reconstruction

The original prompt pack is missing the body of Skill #5. Use this replacement:

```text
You are an MVP ROI Business Case Analyst.

Read the validation, scope, architecture, build-vs-buy matrix, and competitor
teardown. Produce the financial argument for why this agentic wedge deserves a
30-day MVP.

Ask for or estimate:
- Target buyer and budget owner
- Current workflow cost: software, seats, services, human labor, error/rework
- Expected monthly volume
- Current cycle time and failure rate
- Price model: subscription, usage, outcome, or services-led pilot
- 30-day build cost, monthly run cost, and maintenance cost
- Sales motion and realistic time to first 3 paid pilots

Output:
- Current-state cost model
- Agentic MVP cost model
- Three pricing options
- Base/upside/downside ROI cases
- Breakeven month and payback period
- ROI risks and assumptions
- No-go rule: if base-case breakeven is later than month 36, the MVP is not
  viable as a solo wedge without a larger strategic reason.

Do not fabricate precision. Use ranges and label assumptions.
```

## Gotchas

- Do not treat the old `*_Master_Blueprint.md` files as final. Most are prior
  sketches and must be upgraded.
- Do not claim exact enterprise pricing when vendors hide it. State that the
  price is sales-led/quote-based and treat opacity as buyer friction.
- Do not recommend immediate product implementation. The deliverable is a
  positioning and capability asset with credible implementation depth.
- Never ask "shall we build it?" for the use cases. The correct next action is
  to generate, review, package, or present the blueprint artifacts.
- Do not generate a deck before the Markdown evidence pack passes the rubric.
- Do not mark a blueprint `reviewed` if it only has strategy-level technical
  sections. "Next.js + Supabase" is not enough; the file must name concrete
  schemas, endpoints, integrations, env vars, and deployment checks.
- Do not use the phrase "$100K-tier" in final positioning. The point is that
  traditional delivery is slow and bloated; our positioning is AI-native speed
  plus operator-grade rigor.

## Skill Relationships

### Category
Data & Analysis

### Dependencies
- `skill-builder` - governs cross-host skill structure.
- `karpathy-guidelines` - keeps edits scoped and verifiable.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `disruptive-teardown-pipeline` | Sequential upstream | before complete implementation-ready blueprints | `teardowns/*_Disruptive_Teardown.md` |
| `branded-pptx-deck` | Sequential downstream | after Markdown passes rubric | `deck/*.md` |
| `content-ideas` | Peer | when turning findings into social/content ideas | final blueprint summaries |

### Host Compatibility
Canonical source is `.claude/skills/agentic-blueprint-pipeline/SKILL.md`.
Codex/OpenHands can use the repo-local wrapper at
`skills/agentic-blueprint-pipeline/SKILL.md`. If `.agents/skills` is writable
in a future host, mirror this wrapper there.
