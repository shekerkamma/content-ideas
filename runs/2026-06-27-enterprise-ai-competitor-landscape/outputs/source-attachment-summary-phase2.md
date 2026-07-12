# Source Attachment Summary - Phase 2

Status: `priority_slice_enriched`

Phase 2 attaches primary pricing sources for a priority slice of the 125-company universe. It does not complete the full company universe.

## Completed

- Source-enriched pricing records: 12
- Source type: primary official pricing pages/docs
- Output table: `outputs/source-enriched-priority-companies-phase2.csv`

## Priority Companies Enriched

1. OpenAI
2. Anthropic
3. Anthropic API
4. Cohere
5. GitHub Copilot
6. Cursor
7. LangSmith
8. Salesforce Agentforce
9. Pinecone
10. Weights & Biases
11. RunPod
12. Modal

## Pricing Pattern Findings

### 1. Enterprise AI pricing is hybrid

The dominant pattern is no longer just seat pricing. Most products combine at least two of:

- seat subscriptions
- usage/token pricing
- credit systems
- compute usage
- trace/event volume
- enterprise custom contracts

### 2. Platform incumbents use bundle-and-meter models

Salesforce Agentforce is the clearest example in this slice: it combines add-on seats, user licenses, Flex Credits, and conversation pricing. This creates buyer complexity but also gives Salesforce a way to expand from existing CRM budgets.

### 3. Developer tools expose clearer self-serve pricing

Cursor, LangSmith, W&B, RunPod, Modal, and Pinecone publish more explicit entry pricing than broad enterprise platforms. This supports faster adoption but can still become usage-variable at scale.

### 4. Foundation model vendors split between API transparency and enterprise custom

Anthropic publishes detailed API token pricing. Cohere publishes custom enterprise pricing for North/Compass and dedicated Model Vault rates. OpenAI’s business page exposes business seat pricing and enterprise custom pricing, while separate API pricing should be attached in a later pass.

## Strategic Implication

The white-space around **AI pricing and ROI intelligence** is real. Buyers need help translating mixed seat/usage/credit/compute models into actual workflow-level cost.

## Remaining Work

- Attach pricing/funding/status evidence for the remaining 113 companies.
- Extract exact GitHub Copilot price rows from official docs/page top.
- Attach current private funding sources for priority private companies.
- Attach public-company status and investor-relations references for incumbents.
- Update the full `company-universe` table only after each row has source-backed evidence.
