# AEO Business Goals: Brainstorm / Discovery Notes
Date: 2026-06-29 · Goal: Re-anchor the AEO workflow kit work to a clear business objective, success criteria, buyer, and next execution path.

## Structured context
- **Topic type**: strategy
- **Topic string**: Define the business goal for AEO/AI-search workflow skills built around the Agent Replacement Scorecard and existing content/research pipelines.
- **Entities**: Agent Replacement Scorecard, AEO workflow kit, Claude Code, Codex, Profound-style agents, content-ideas repo
- **Prospect/account**: n/a
- **Target buyer**: unresolved
- **Verticals**: agentic AI, SaaS replacement, AI search/AEO, consulting/pre-sales
- **Open decisions**: primary business objective -> user; target buyer -> user; monetization path -> user; success metric -> user; whether to continue building or pause/refactor -> user

## Summary / key decisions

We need to stop implementation drift and re-anchor the work. The current code created a repo-local workflow kit for turning a scorecard/content asset into AEO audit artifacts, but the business objective was not explicitly locked before building. This session will decide what business outcome the workflow should serve.

Current strategic answer: use the AEO workflow as a **distribution intelligence layer** for the Agent Replacement Scorecard, with the business goal of generating agentic AI consulting/build conversations. Do not productize the AEO tool yet.

## Q&A log

### Q1 — Primary business objective
- Asked: What is the business objective of this AEO/AI-search workflow? Recommended answer: turn the Agent Replacement Scorecard into a pre-sales and authority asset that proves expertise in where AI agents replace SaaS, then use AEO workflows to make that asset discoverable in AI answers and convert interested buyers into consulting/product-build conversations.
- Captured: Best self-answer: the primary objective is **lead generation for agentic AI consulting/build work**, not productizing an AEO SaaS yet. The Agent Replacement Scorecard is the flagship proof asset. The AEO workflow exists to help the asset get surfaced in AI-search answers, reveal which competing sources currently win those answers, and generate concrete content/PR/source actions to improve discoverability.
- Flags: validate whether user agrees with this strategic framing -> user later; define target buyer and conversion path -> next questions.

### Q2 — Target buyer
- Asked: Who is the primary buyer or audience this should influence?
- Captured: Best self-answer: primary buyer is a founder/operator/CEO/strategy lead at a B2B SaaS, services, or vertical software company worried that AI agents will compress seat-based SaaS value. Secondary buyer is an innovation, transformation, or consulting leader who needs a credible roadmap for replacing or renegotiating SaaS with agents. This is not aimed at SEO managers first; AEO is the delivery mechanism, not the buyer's core pain.
- Flags: choose whether to narrow to one vertical first, likely B2B SaaS / agentic AI / enterprise software -> unresolved.

### Q3 — Offer shape
- Asked: What should this workflow sell or support?
- Captured: Best self-answer: the immediate offer is a **SaaS Replacement Exposure Audit**. It uses the scorecard framework to map a buyer's software stack or product category into Keep / Renegotiate / Replace, then identifies where AI-search answers already shape the category narrative. The paid work is strategy + implementation blueprint + optional build sprint, not AEO monitoring.
- Flags: package name and pricing are unresolved; likely initial offer should be a fixed-scope diagnostic, not retainer software.

### Q4 — Business success metric
- Asked: How do we know this is working?
- Captured: Best self-answer: success is not "the workflow runs." Success is: (1) scorecard appears in AI answers for at least 5 high-intent prompts, (2) those prompts map to one clear buyer problem, (3) the resulting artifact supports outreach or inbound conversations, and (4) at least one qualified consulting/build conversation is created. Technical artifacts are only leading indicators.
- Flags: need baseline real AI captures from ChatGPT, Claude, Perplexity, and Google AI Mode for 20-30 prompts -> workflow task.

### Q5 — What to do with the code already built
- Asked: Did the workflow kit help or distract?
- Captured: Best self-answer: it helped as infrastructure but became distracting because it was treated as the destination. Keep it, but demote it to **internal operator tooling**. Its job is to generate evidence for the business asset and audit offer. Do not add dashboards, automatic scraping, or product features until the consulting wedge is validated.
- Flags: mark current AEO code as V0 internal tool; next work should generate a buyer-facing diagnostic from scorecard evidence -> next action.

### Q6 — Next concrete deliverable
- Asked: What should we produce next so the work has business value?
- Captured: Best self-answer: produce a buyer-facing **Agentic SaaS Exposure Diagnostic** from the scorecard. It should be a concise Markdown/PDF/deck-ready artifact that says: which SaaS categories are most exposed, why, examples already deployed, what a buyer should replace/renegotiate/keep, and how to run a 2-week pilot. The AEO workflow should feed this by identifying prompts where the scorecard should appear and the competing sources that currently win.
- Flags: decide format after content exists; likely Markdown first, then branded PPTX only after review.

### Q7 — Stop-doing list
- Asked: What should we stop doing to avoid drift?
- Captured: Best self-answer: stop adding more AEO infrastructure until there is real buyer-facing output. Do not build automated AI-engine scraping, dashboard UI, scheduled monitoring, product packaging, or more leaf skills. Do not optimize the tool before proving the offer. The next work must convert scorecard + AEO findings into an offer artifact.
- Flags: none.

### Q8 — Revised end goal
- Asked: What is the actual end goal for this thread of work?
- Captured: Best self-answer: end goal is **a repeatable pre-sales motion**: scorecard asset -> AEO prompt audit -> exposure diagnostic -> consulting/build conversation. The workflow kit is only valuable if it helps this motion become faster, more evidence-backed, and easier to repeat across a prospect's category or software stack.
- Flags: need to choose the first prospect/category to test the motion against.

### Q9 — First execution artifact
- Asked: What concrete artifact did we produce after re-anchoring?
- Captured: Built the first buyer-facing `Agentic SaaS Exposure Diagnostic` from the scorecard. It lives at `runs/2026-06-29-agentic-saas-exposure-diagnostic/outputs/agentic-saas-exposure-diagnostic.md`. This is the correct next artifact because it translates the scorecard into a pre-sales narrative: exposure thesis, Replace/Renegotiate/Keep zones, buyer interpretation, two-week pilot path, and AEO's role as distribution intelligence.
- Flags: needs source verification before client-facing delivery if used externally; likely next step is deck-ready summary or prospect-specific version.

### Q10 — Pattern quality correction
- Asked: Identify better patterns because the current ones do not seem good.
- Captured: The current pattern set is too primitive because it over-relies on `Replace / Renegotiate / Keep`. Better patterns should explain the underlying mechanism: seat compression, add-on collapse, workflow-over-record, corpus/data moat, human-signoff boundary, interface collapse, and renewal leverage. These patterns are more useful for buyer conversations because they connect agent capability to software spend, integration boundaries, and procurement action.
- Flags: rewrite diagnostic around mechanism patterns rather than verdict buckets -> next work.

### Q11 — AEO as pattern discovery
- Asked: Should AEO help identify real patterns rather than only validate patterns we already believe?
- Captured: Yes. The AEO workflow should now be treated as a pattern-discovery engine: prompt AI systems around buyer problems, capture their answers, mine recurring mechanisms, then decide which mechanisms deserve a diagnostic, deck, or prospect-specific offer. Built `skills/aeo-pattern-miner/` to turn reviewed AEO runs into `normalized/pattern_candidates.jsonl` and `final/pattern-mining-report.md`.
- Captured output: First test run against `runs/2026-06-29-aeo-search-agent-replacement-scorecard-2/` found workflow-layer replacement and citation-authority-gap as medium-confidence candidates, plus data-moat-survival and renewal-leverage as low-confidence candidates.
- Evidence caution: That run used manually supplied/test capture text through the live-capture path. It validates the workflow mechanics, not the market truth. The next real step is collecting 20-30 dated answer captures from ChatGPT, Claude, Perplexity, and Google AI Mode for the same prompt pack.
- Flags: next diagnostic rewrite should use only patterns backed by real captures, or clearly label unvalidated thesis patterns.

## Open flags (pending input)
- Target buyer / audience -> user
- Business success metric -> user
- Whether scorecard is a lead magnet, consulting asset, product wedge, or internal research tool -> user
- First prospect/category for the diagnostic test -> user
