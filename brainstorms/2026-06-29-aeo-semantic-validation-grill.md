# AEO Semantic Validation Grill: Brainstorm / Discovery Notes
Date: 2026-06-29 · Goal: Verify and validate the corrected AEO workflow artifacts against the goal of semantic, evidence-backed pattern discovery and Reddit buyer-signal discovery.

## Structured context
- **Topic type**: strategy
- **Topic string**: Validate corrected AEO workflow artifacts: semantic pattern mining, subagent review, and Reddit semantic opportunity finder.
- **Entities**: AEO workflow kit, Agent Replacement Scorecard, aeo-pattern-miner, aeo-reddit-opportunity-finder, subagent reviewers, Reddit buyer-signal layer
- **Prospect/account**: n/a
- **Target buyer**: B2B SaaS founder/operator/strategy lead or AI transformation buyer
- **Verticals**: agentic AI, SaaS replacement, AI-search/AEO, Reddit buyer research, consulting/pre-sales
- **Open decisions**: whether current artifacts are validated as workflow-ready -> agent; whether current artifacts are evidence-ready -> agent; next evidence collection step -> agent/user

## Summary / key decisions

Validation result: the corrected workflow is **workflow-ready but not evidence-ready**. Semantic pattern mining now uses evidence units, semantic/concept-anchor scoring, target-seeded evidence detection, and subagent review. Reddit now produces semantic buyer-signal probes, not keyword query lists. The current test run correctly refuses to promote weak target-seeded captures into real market patterns.

Remaining limitation: no real Reddit thread evidence and no independent real AI-answer capture set have been loaded yet. The workflow is ready for a real evidence sprint; it is not yet ready for external claims, a polished deck, or outreach copy.

## Q&A log

### Q1 — Is pattern mining still keyword-led?
- Asked: Does the corrected AEO pattern miner still depend on keyword hits or matched terms?
- Captured: No. The pattern miner now writes `capture_units.jsonl`, `semantic_clusters.jsonl`, `pattern_candidates.jsonl`, `subagent-review-brief.md`, and `pattern-discovery-audit.json`. The audit says `uses_keyword_pattern_matching: false`. The remaining concept anchors are used for semantic alignment and review, not direct keyword-hit promotion.
- Flags: external embedding or LLM clustering could improve semantic grouping later -> agent/user.

### Q2 — Does weak evidence get promoted?
- Asked: Does the current test run still overclaim because it has two target-seeded captures?
- Captured: No. All pattern candidates are low confidence and marked with `target_seeded_evidence_units`. `pattern-review-summary.md` says the tested captures do not support any accepted market pattern. The adversarial reviewer rejected all candidates; the product reviewer treated two only as weak hypotheses.
- Flags: collect 20-30 independent, dated AI-answer captures before promoting patterns -> agent/user.

### Q3 — Is Reddit keyword-search based?
- Asked: Is the Reddit Opportunity Finder using keyword search as the method?
- Captured: No after correction. It now emits `reddit_semantic_probes.jsonl` with semantic probes, selection rules, and retrieval rules. It removed the stale `reddit_discovery_queries.jsonl` artifact. The run now has 212 semantic probes and targeted checks found no prompt-shaped topics like `alternatives to`, `vs`, `best`, or `vendor should`.
- Flags: actual Reddit retrieval still needs semantic search or human screening; no real Reddit evidence is loaded yet -> agent/user.

### Q4 — Is the workflow business-valid?
- Asked: Does this now support the business wedge?
- Captured: Yes as an internal operating workflow. It supports the wedge by using Reddit as buyer-signal discovery, AEO captures as answer-surface evidence, semantic pattern mining as synthesis, and subagent review as a claim filter. It is not yet business-evidence-valid because the current run lacks real Reddit evidence and independent AI-answer captures.
- Flags: next step is an evidence sprint, not a deck -> agent/user.

## Open flags (pending input)
- Real Reddit evidence not loaded yet -> agent/user.
- Real AI-answer captures still needed -> agent/user.
