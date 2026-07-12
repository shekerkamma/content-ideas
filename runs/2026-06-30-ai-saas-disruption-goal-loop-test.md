# Goal Loop Test: AI Market Insights on Disrupting SaaS Market

Date: 2026-06-30

Sample prompt: "AI market insights on disrupting SAAS market"

## Goal Contract

- Outcome: Test `goal-loop-orchestrator` on a broad AI/SaaS market-insight prompt using the upgraded real-research chain.
- Artifacts: This run note plus raw Exa and Firecrawl evidence files in `runs/`.
- Constraints: Use real research tools, not simple web search; use local skills first; use `ai-analyst` as the upstream synthesis/validation gate; no deck requested; bounded loop; no infinite loop.
- Acceptance criteria: Exa discovery works, Firecrawl ingestion works, GBrain recall is attempted, Reddit/community evidence is probed, source-backed insights are separated from open gaps, and the run stops within budget.
- Verification: Saved raw evidence, source table, confidence labels, and loop stop state.
- Research mode: `validated-market-pricing-thesis-with-gaps`.
- Loop budget: 3 total passes.
- Stop conditions: Stop after evidence collection, source tieout, and synthesis; do not continue chasing community evidence after two failed/weak probes.
- Known inputs: Broad SaaS market disruption prompt.
- Missing inputs: Target buyer, geography, SaaS category, and output format.

## Skill Chain

| Phase | Skill/action | Why | Input | Output | Verification |
|---|---|---|---|---|---|
| 1 | `goal-loop-orchestrator` | Refine vague prompt, bound loop, select chain | User prompt | Goal contract and research plan | Contract includes loop budget and stop conditions |
| 2 | GBrain recall | Required durable-memory stage for strategy/pipeline work | AI agents + SaaS pricing query | Blocked | `GBrain: Timed out waiting for PGLite lock.` |
| 3 | `exa-api` | Semantic discovery, preferred over generic search | SaaS disruption/pricing query | 5 high-signal sources | `runs/2026-06-30-ai-saas-disruption-exa-search.json` |
| 4 | `firecrawl` | Full-page ingestion of important pages | Vendor/pricing/analyst URLs | Live page captures | Firecrawl `meta.source=live`, status 200 on captured pages |
| 5 | `aeo-reddit-opportunity-finder` | Generate semantic Reddit probes by buyer job, failure mode, switching trigger, skepticism, and comparison frame | AEO-style query pack | 152 semantic probes | `runs/2026-06-30-ai-saas-disruption-reddit-semantic/final/reddit-opportunity-report.md` |
| 6 | `reddit-new-factcheck` + `old_reddit_evidence.py` | Retrieve and qualify Reddit evidence against focused buyer-language claims | Focused Reddit claims doc | 10 raw Reddit threads, 210 rejected rows, 0 qualified buyer-language rows | `runs/2026-06-30-ai-saas-disruption-reddit-factcheck-focused/reddit-factcheck-report.md`; human review rejects false positives |
| 7 | `ai-analyst` validation contract | Synthesize data-backed claim with source tieout | Raw evidence files | Confidence-scored insights | Claims mapped to source table below |

No `branded-pptx-deck` stage was triggered because the prompt did not ask for slides or PowerPoint.

## Evidence Files

- Exa discovery: `runs/2026-06-30-ai-saas-disruption-exa-search.json`
- Firecrawl discovery: `runs/2026-06-30-ai-saas-disruption-firecrawl-search.json`
- Early Exa Reddit probe 1: `runs/2026-06-30-ai-saas-disruption-exa-reddit-probe.json`
- Early Exa Reddit probe 2: `runs/2026-06-30-ai-saas-disruption-exa-reddit-probe-2.json`
- Reddit semantic probe run: `runs/2026-06-30-ai-saas-disruption-reddit-semantic/`
- Focused Reddit factcheck run: `runs/2026-06-30-ai-saas-disruption-reddit-factcheck-focused/`
- Focused Reddit validation claims: `runs/2026-06-30-ai-saas-disruption-reddit-claims.md`
- Salesforce Agentforce pricing: `runs/2026-06-30-ai-saas-salesforce-agentforce-firecrawl.json`
- Intercom pricing: `runs/2026-06-30-ai-saas-intercom-pricing-firecrawl.json`
- Microsoft Copilot Studio: `runs/2026-06-30-ai-saas-microsoft-copilot-studio-firecrawl.json`
- Deloitte SaaS meets AI agents: `runs/2026-06-30-ai-saas-deloitte-firecrawl.json`
- RSM SaaS pricing models: `runs/2026-06-30-ai-saas-rsm-firecrawl.json`
- Bain per-seat pricing: `runs/2026-06-30-ai-saas-bain-firecrawl.json`

## Source Table

| Source | Category | Evidence used | Confidence |
|---|---|---|---|
| Deloitte, "SaaS meets AI agents" | Analyst/market thesis | Predicts SaaS AI agents will shift SaaS toward hybrid usage/outcome pricing; says full replacement is more gradual than 2026 hype. | High for directional market framing |
| RSM, "SaaS vendors must adjust pricing models..." | Analyst/pricing thesis | States subscription/per-user pricing is under pressure as software performs work autonomously; recommends outcome-based pricing and shadow pricing models. | High for pricing-risk framing |
| Bain, "Per-Seat Software Pricing Isn't Dead..." | Analyst/pricing operating model | Finds hybrid pricing is the dominant interim strategy and says vendors need telemetry, billing, sales enablement, and customer transition support. | High for transition mechanics |
| Salesforce Agentforce pricing | Primary vendor pricing | Shows Flex Credits at $500 per 100k credits, $2 per conversation, and examples of action/credit-based pricing. | High for vendor behavior |
| Intercom pricing | Primary vendor pricing | Shows Fin at $0.99 per outcome and a no-seat-required Fin AI Agent option for existing helpdesks. | High for outcome-pricing proof |
| Microsoft Copilot Studio | Primary vendor/product | Positions Copilot Studio as a platform for creating, managing, and launching AI agents, including autonomous capabilities and usage/ROI tracking. | Medium-high for platform direction |
| `aeo-reddit-opportunity-finder` | Semantic Reddit probe generation | Generated 152 semantic probes across buyer jobs, software failure, skepticism, comparison frames, switching triggers, and pattern validation. | High for probe design, not evidence |
| `reddit-new-factcheck` + `old_reddit_evidence.py` | Reddit retrieval and qualification | Retrieved 10 raw old.reddit threads; all qualified buyer-language evidence was rejected after semantic/human review. | High for "no qualified evidence found in this run" |

## Market Insights

### 1. The disruption is not "SaaS dies"; it is "the seat stops being the clean billing unit."

The strongest supported signal is pricing-model disruption. Deloitte frames AI agents as pushing SaaS toward usage- and outcome-based pricing, while Bain says seats are not dead but are no longer the only game. RSM is more aggressive, arguing that fixed per-user subscription models are under structural pressure when software performs work independently.

Implication: the immediate wedge is not replacing entire systems of record. It is attacking categories where value can be metered by work completed: resolved tickets, completed workflows, actions, conversations, documents processed, leads qualified, invoices reconciled.

### 2. Incumbents are already defending by changing meters.

Salesforce and Intercom are not only adding AI features; they are publishing new billing units. Salesforce uses Flex Credits, action/conversation pricing, and Digital Wallet-style usage visibility. Intercom prices Fin at $0.99 per outcome and explicitly offers Fin with existing helpdesks with no seat requirement.

Implication: the market is moving from "AI add-on" to "AI work meter." Startups that pitch only cheaper seats are fighting the old game. Startups that meter completed work can align to the new buying logic.

### 3. Hybrid pricing is the transition zone.

Bain's analysis is the best operating-model counterweight: most established SaaS vendors are not jumping straight to pure outcome pricing. They are layering AI usage or outcome meters on top of existing seats because billing systems, revenue recognition, sales comp, customer procurement, and telemetry are not ready for a clean switch.

Implication: a SaaS disruptor should expect coexistence with incumbents. The best wedge is often an overlay that proves measurable work volume first, then expands into budget once the customer has pricing evidence.

### 4. The new moat is instrumentation plus trust, not just model quality.

Outcome pricing creates disputes: what counts as a resolved issue, who gets attribution, how quality is audited, and who absorbs failure. The durable moat is therefore telemetry, audit trail, workflow control, identity/permissions, ROI reporting, and contract-safe definitions of outcomes.

Implication: "agent does task" is not enough. A serious SaaS disruptor needs a billing-grade work ledger.

### 5. Customer support is the cleanest near-term wedge.

Intercom/Fin and Salesforce both expose customer-facing agent meters. Support has high volume, clear outcomes, measurable before/after cost, and fewer ambiguous attribution problems than complex ERP/CRM transformation.

Implication: if selecting a first category, prioritize support/customer operations, internal service desk, claims intake, invoice/document processing, or SDR/research workflows over full CRM/ERP replacement.

## Recommended Strategy

Build around the "work execution layer" thesis:

1. Pick a high-volume workflow with a measurable unit of work.
2. Integrate with existing SaaS rather than ask the buyer to replace it on day one.
3. Track actions, outcomes, handoffs, exceptions, quality, and cost per completed unit.
4. Price as hybrid first: low platform fee plus outcome/action meter.
5. Use the usage ledger to create renewal leverage against seat-heavy incumbents.

Best initial wedge: AI customer-ops outcome layer that resolves support/service workflows across existing helpdesk, CRM, billing, and knowledge-base systems.

## Validation Gaps

- GBrain recall was attempted but blocked by PGLite lock timeout.
- Reddit/community evidence was attempted through the repo's custom Reddit skills:
  - `aeo-reddit-opportunity-finder` generated 152 semantic probes.
  - `reddit-new-factcheck` created a focused claim pack.
  - `old_reddit_evidence.py` retrieved 10 raw old.reddit threads.
  - The qualification gate rejected the raw hits as off-topic/noisy; a human review also rejected the two weak false positives.
  - Result: no qualified Reddit buyer-language evidence found in this run.
- No customer interview, procurement conversation, or renewal-contract sample was used.
- This is market/pricing-thesis validated, not full buyer-pain validated.

## Loop State

- Pass 1: Goal refined; chain selected; capability probe updated with Exa and Firecrawl.
- Pass 2: Exa discovery and Firecrawl ingestion executed.
- Pass 3: Reddit semantic probe/factcheck pass, source tieout, synthesis, and handoff completed.

Stop: 3/3 passes used. No infinite loop.

## Handoff

For a deeper run, specialize the prompt by SaaS category and buyer:

> "Find AI disruption wedges for customer support SaaS sold to mid-market B2B software companies in the US."

Then run:

1. Exa discovery across vendor pages, pricing pages, docs, review sites, and forums.
2. Firecrawl ingestion of every primary page.
3. Reddit/thread extraction only after specific thread URLs or subreddits are found.
4. Deep research subagents split into pricing, buyer pain, incumbent product gaps, and workflow proof.
5. `ai-analyst` synthesis into a scored wedge table.
6. `branded-pptx-deck` only if a client-ready deck is requested.
