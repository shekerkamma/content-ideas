# AEO Tested Artifacts Grill: Brainstorm / Discovery Notes
Date: 2026-06-29 · Goal: Stress-test the tested AEO workflow artifacts and outputs against the business goal of discovering real patterns that can support a diagnostic, deck, or consulting offer.

## Structured context
- **Topic type**: strategy
- **Topic string**: Grill the tested AEO workflow artifacts, pattern-mining report, audit report, and diagnostic for business usefulness, evidence quality, and next execution path.
- **Entities**: Agent Replacement Scorecard, AEO workflow kit, aeo-orchestrator, aeo-pattern-miner, Agentic SaaS Exposure Diagnostic
- **Prospect/account**: n/a
- **Target buyer**: B2B SaaS founder/operator/CEO/strategy lead or AI transformation buyer concerned about AI agents compressing SaaS spend
- **Verticals**: agentic AI, SaaS replacement, AI search/AEO, consulting/pre-sales
- **Open decisions**: whether current artifacts are client-facing -> agent; what must be fixed before deck/outreach -> agent; evidence threshold for real pattern claims -> agent

## Summary / key decisions

The tested artifacts are useful as workflow validation, not as market validation. They prove the repo can generate a file-backed AEO run, preserve captures, validate schemas, render reports, and mine candidate patterns. They do not yet prove real AI-search visibility, real competitor displacement, or real market patterns.

The main failure is evidence quality: only two short manual captures were used, and both directly mention the Agent Replacement Scorecard. That makes the 100% visibility score circular. The prompt pack also needs cleanup because competitor mapping is too generic and some generated prompts are bloated.

The right next move is a real AEO capture sprint, not a prettier deck. Clean the prompts, map competitors by category, collect 20-30 dated answers across major AI answer surfaces, rerun pattern mining, then rewrite the diagnostic around patterns that survive the evidence threshold.

## Q&A log

### Q1 — Evidence validity
- Asked: Do the tested artifacts prove real AEO visibility or real market patterns? Recommended self-answer: no; they prove that the local pipeline can ingest captures, validate contracts, and generate reports.
- Captured: The tested run has only two captures, both labeled `manual_live_capture`, and the raw answer text directly names the Agent Replacement Scorecard. This makes the 100% visibility result circular. The report validates workflow mechanics, not market evidence.
- Flags: collect real dated answer captures from ChatGPT, Claude, Perplexity, and Google AI Mode before making any external claim -> agent/user.

### Q2 — Prompt pack quality
- Asked: Are the generated queries good enough to discover real buyer/AI-answer patterns? Recommended self-answer: partially, but not yet.
- Captured: The prompt pack has breadth, but many generated queries are overstuffed with proof examples and vendor strings. Several comparison prompts use Zendesk as the competitor anchor across unrelated categories such as travel booking, legal research, document drafting, and creative generation. That will distort AI answers and hide real category competitors.
- Flags: rebuild query generation around clean buyer prompts and category-specific competitor sets -> agent.

### Q3 — QA status meaning
- Asked: Does `status: reviewed` mean the output is ready for business use? Recommended self-answer: no.
- Captured: The validator checks contracts and hard artifact gates: files exist, captures map to queries, raw text exists, and recommendations cite evidence IDs. It does not judge whether captures are real, independent, sufficiently numerous, or non-circular. `reviewed` currently means schema-reviewed, not evidence-reviewed or client-ready.
- Flags: split status into `contract_reviewed`, `evidence_reviewed`, and `client_ready` or add an evidence-grade field -> agent.

### Q4 — Pattern-miner quality
- Asked: Does the pattern miner identify real patterns well? Recommended self-answer: not yet; it identifies candidate mechanisms from text.
- Captured: The miner produced useful mechanism labels such as workflow-layer replacement and citation-authority gap, but it is currently lexical. It counts matched terms like `workflow`, `source`, and `scorecard`; it does not yet cluster themes semantically, detect contradictions, compare against competitor mentions, or separate model-originated language from our seeded thesis.
- Flags: upgrade pattern mining to require recurrence across independent captures and source diversity before medium/high confidence -> agent.

### Q5 — Diagnostic business quality
- Asked: Is the Agentic SaaS Exposure Diagnostic useful as a business artifact? Recommended self-answer: yes as an internal/pre-sales draft, no as a polished external deliverable.
- Captured: The diagnostic has a coherent thesis: agents replace workflow layers, renegotiate seat economics, and enrich high-moat systems. That is the right business frame. But it still leans heavily on the scorecard's own verdicts and proof examples without external verification, named source links, prospect-specific spend assumptions, or AI-answer evidence. It should not be packaged as a definitive market report yet.
- Flags: convert the diagnostic into a prospect-specific exposure memo only after adding verified sources and real AI-answer captures -> agent/user.

### Q6 — What was actually built
- Asked: What did the tested artifacts actually accomplish? Recommended self-answer: they built the operating skeleton for a repeatable evidence workflow.
- Captured: The useful accomplishment is file-backed workflow infrastructure: prompt generation, capture ingestion, raw text preservation, entity/visibility scoring, recommendation rendering, contract validation, and pattern candidate extraction. The weak accomplishment is the current evidence content. The system is ready to accept real captures; it has not yet produced real AEO truth.
- Flags: preserve the workflow kit but rename current outputs as `workflow-validation` where appropriate -> agent.

### Q7 — Minimum evidence bar
- Asked: What evidence bar should be required before calling something a real pattern? Recommended self-answer: at least 20-30 real dated captures across engines and prompt clusters.
- Captured: A business-facing pattern should require independent capture evidence across multiple AI systems, multiple prompt variants, and more than one category or source domain. Suggested minimum: 20-30 real answer captures, at least 4 engines or answer surfaces, 5-8 prompt clusters, capture timestamps, raw answer text, cited URLs, competitor mentions, and source-domain counts. A pattern should be promoted only if it appears across at least 3 independent captures or reveals a sharp gap between AI-answer language and our scorecard thesis.
- Flags: implement evidence-grade thresholds in validator and pattern miner -> agent.

### Q8 — Correct next step
- Asked: What should happen next? Recommended self-answer: run a real AEO capture sprint before producing more polished outputs.
- Captured: The next step is not a prettier 6-8 slide deck. The next step is a capture sprint: clean the query pack, map competitors per category, capture actual AI answers from ChatGPT/Claude/Perplexity/Google AI Mode, then rerun pattern mining. Only after that should we rewrite the diagnostic or build a deck around the strongest discovered mechanisms.
- Flags: build a clean capture protocol and evidence-grade report -> agent.

### Q9 — Keyword matching objection
- Asked: Should keyword matching be used for pattern mining? User said keyword matching should not be used and suggested subagents for semantic search.
- Captured: Correct. Keyword matching should be removed as the primary mechanism. Pattern discovery should extract evidence units, perform semantic grouping/alignment, then send candidate clusters to independent semantic/adversarial reviewers. Subagents should not be the source of truth; they should accept, reject, split, rename, or downgrade candidates against exact local evidence spans.
- Flags: replace keyword-hit miner with semantic evidence-unit workflow and subagent review brief -> agent.

### Q10 — Subagent review result
- Asked: What happens when subagents review the tested semantic artifacts?
- Captured: The subagent review worked as intended. The adversarial reviewer rejected every candidate because the evidence was target-seeded, circular, and too thin. The product-lens reviewer rejected Add-On Collapse and Seat Compression, and downgraded Data Moat Survival and Workflow Layer Replacement into weak diagnostic hypotheses with better labels. This confirms the corrected workflow prevents weak test captures from becoming external claims.
- Flags: store pattern review JSONL and summary in the run; collect independent real captures before promoting any pattern -> agent/user.

## Open flags (pending input)
- Real AI answer captures needed before client-facing claims -> agent/user.
- Query pack needs category-specific competitor mapping -> agent.
- QA status needs evidence/client-readiness distinction -> agent.
- Pattern confidence rules need stronger evidence thresholds -> agent.
- Diagnostic needs source verification and prospect specificity before external use -> agent/user.
- Current tested outputs should be labeled workflow validation, not market validation -> agent.
- Define and enforce evidence-grade thresholds -> agent.
- Build clean capture protocol before deck/outreach -> agent.
- Replace keyword-hit pattern mining with semantic evidence-unit workflow -> agent.
- Independent real captures still required before pattern promotion -> agent/user.
