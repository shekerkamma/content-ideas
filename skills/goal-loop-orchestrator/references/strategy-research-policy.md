## Strategy Research Policy

Use this policy when the goal involves market maps, moats, wedges, competitive
strategy, investment theses, pipeline strategy, buyer pain, or strategic options.

Default mode is `validated-research`. A run may switch to `hypothesis` only
when required tools are unavailable/blocked or the user explicitly asks for a
fast scan. Record the mode in the goal contract and final handoff.

Research order:

1. Durable memory / prior work: GBrain, repo run artifacts, brainstorms, prior
   strategy briefs, pipeline outputs.
2. Specialist local skills: `strategy-consulting`, `disruptive-teardown-pipeline`,
   `saas-gap-analyzer`, `content-ideas` strategy mode, `pipeline-runner`, or the
   closest project-specific research skill.
3. Capability probe: before external research, check which research routes are
   available in the host:
   - CLI: `command -v exa`, `command -v firecrawl-pp-cli`,
     `command -v firecrawl`, `command -v reddit`, plus repo scripts such as
     `skills/you-com-search/scripts/search.py`,
     `skills/exa-api/scripts/exa_search.sh`,
     `skills/aeo-reddit-opportunity-finder/scripts/find_opportunities.py`,
     `skills/reddit-new-factcheck/scripts/*`, and
     `skills/reddit-seo-pipeline/scripts/*`.
   - MCP/plugin: Exa (`mcp__claude_ai_Exa__web_search_exa` or equivalent),
     Firecrawl (`mcp__firecrawl__*` or `/firecrawl`), Hermes
     `web.search_backend: you`, Reddit/browser research plugins, and
     host-provided tool discovery.
   - Subagents: Claude `Task`, Codex-discovered multi-agent tools, MCP
     subagent servers, or another available host-provided multi-agent route.
4. You.com: use `you-com-search`, Hermes `web.search_backend: you`, or an
   equivalent You.com API wrapper before generic WebSearch for broad current
   web discovery, livecrawl, research, or finance research. Treat You.com
   output as candidate source material unless the API returned full cited
   research output.
5. Exa: use Exa or an equivalent semantic search tool for source discovery when
   available. Prefer it over generic web search for competitors, categories,
   buyer-language pages, forums, docs, and market signals. In this repo, if no
   Exa MCP tool is exposed, use `exa-api/scripts/exa_search.sh` from the
   resolved helper skill path when `EXA_API_KEY` is set.
6. Firecrawl: use Firecrawl or an equivalent crawler/reader to ingest important
   pages discovered by Exa, especially vendor pricing, docs, support pages,
   changelogs, review pages, and forum threads. In this repo, prefer
   `firecrawl-pp-cli` through `skills/firecrawl/SKILL.md`; if the CLI is
   installed but sandbox networking blocks the API, request escalation or mark
   Firecrawl blocked.
7. Reddit evidence: when buyer pain, skepticism, switching triggers, comparison
   frames, or workflow language matter, use the repo's custom Reddit skill
   chain. Do not substitute simple web search or an Exa `site:reddit.com` query
   for this chain.
   - First run `aeo-reddit-opportunity-finder` to create semantic Reddit probes
     by buyer job, software failure, switching trigger, skepticism, comparison
     frame, and pattern validation. The probes define what meaning to retrieve;
     they are not evidence.
   - Then use the best available Reddit retrieval route: supplied thread URLs
     with `reddit-seo-pipeline`, logged-in Reddit/browser research,
     `you-com-search` or Exa as Reddit discovery assistants, ScrapeCreators, or
     `reddit-new-factcheck/scripts/old_reddit_evidence.py`.
   - Then run `reddit-new-factcheck` as the qualification gate against focused
     claims. Raw Reddit search output, raw old.reddit HTML, and raw thread JSON
     are discovery only.
   - Accept Reddit evidence only when it passes semantic qualification:
     relevant subreddit/source context, matching buyer/practitioner persona,
     matching workflow language, and a concrete pain, workaround, objection,
     switching trigger, comparison frame, or adoption signal.
   - Reject keyword-only matches, generic AI chatter, off-topic subreddits,
     company-name-only mentions, and broad/noisy threads even if a script marks
     them as weak support. Add a human-review note when rejection depends on
     judgment.
   - If the custom Reddit skills are unavailable or no qualified Reddit evidence
     is found, record `no qualified Reddit evidence` and keep the claim as a
     validation gap. Do not present buyer pain as Reddit-validated.
7. Subagents: for deep research, spawn focused research subagents when the host
   supports them. Use parallel subagents for independent questions such as:
   incumbent/pricing map, Reddit/buyer-pain mining, regulatory/procurement
   risk, and workflow/job-post evidence. Do not duplicate the same task across
   agents.
8. Primary sources: vendor docs, pricing pages, SEC filings, official blogs,
   regulatory filings, public datasets, court/agency documents, GitHub repos,
   customer docs, implementation guides.
9. Community and buyer-language evidence: Reddit, forums, review sites,
   customer interviews, job posts, support docs, changelogs. Use these to prove
   pain, not as the only market map.
10. Generic web search: fallback only for source discovery or when richer tools
   are unavailable. It cannot by itself satisfy strategy evidence requirements.
   If generic search is used because better tools are unavailable, switch the
   run to `hypothesis` mode and say why.

Minimum evidence bar for `validated-research` strategy:

- GBrain/prior-artifact recall attempted or completed.
- Specialist local skill selected for the strategy shape.
- Exa/semantic discovery used when available.
- Firecrawl/full-page ingestion used for important discovered pages when
  available.
- Reddit/community/operator evidence used through the custom semantic Reddit
  chain when buyer pain, switching triggers, skepticism, comparison frames, or
  workflow language are part of the claim. If the chain returns no qualified
  evidence, the run may still validate market/pricing facts from primary
  sources, but buyer-language Reddit validation remains open.
- At least one primary source backs each hard company, pricing, regulatory,
  funding, product, or date claim.
- Subagents spawned for deep research when the host supports them and the
  research has independent streams worth parallelizing.

Subagent prompt requirements:

- Scope one research question only.
- Name the target industry, buyer, workflow, and geography.
- State required source types and banned source types.
- Require exact URLs, dates/access dates, source category, confidence, and
  extracted evidence snippets.
- Require rejected leads and why they were rejected.
- Require a concise answer plus a source table, not a narrative essay.
- Treat subagent outputs as leads. The main agent must reconcile conflicts,
  verify important claims, and decide final confidence.

For moat or wedge recommendations, require at least one of:

- direct buyer/user pain evidence,
- incumbent pricing/onboarding/workflow friction,
- regulatory or procurement forcing function,
- workflow evidence from docs, support pages, reviews, forums, or job posts,
- credible proof of budget or existing spend category.

If the evidence is only vendor marketing pages, generic search results, or
unscreened community chatter, the output is `hypothesis` mode, not validated
strategy.

If You.com, Exa, Firecrawl, Reddit tools, and subagents are all unavailable, either ask
whether to proceed with a hypothesis-level scan or produce a research plan with
the exact tools/data needed. Do not present the result as a validated strategy.

### Reddit Semantic Evidence Checklist

Use this checklist whenever a strategy claim depends on buyer/operator language,
skepticism, switching behavior, workflow pain, or comparison frames:

1. Create a focused claim document. Include only the claims Reddit can validate;
   keep market-size, pricing, date, funding, and regulatory claims in the
   primary-source track.
2. Create or reuse an AEO-style run folder with:
   - `manifest.json`
   - `stage_outputs/queries.jsonl`
   - optional `normalized/pattern_candidates.jsonl`
   - optional `normalized/pattern_reviews.jsonl`
3. Run `aeo-reddit-opportunity-finder` to generate semantic probes:

   ```bash
   python3 skills/aeo-reddit-opportunity-finder/scripts/find_opportunities.py runs/<run-id>
   ```

4. Run `reddit-new-factcheck` to prepare focused claims:

   ```bash
   python3 skills/reddit-new-factcheck/scripts/prepare_factcheck.py \
     --input <focused-claims.md> \
     --topic "<topic>" \
     --out-dir runs/<reddit-factcheck-run>
   ```

5. Retrieve Reddit evidence with known thread URLs, `reddit-seo-pipeline`,
   logged-in Reddit/browser research, ScrapeCreators, or the fallback collector:

   ```bash
   python3 skills/reddit-new-factcheck/scripts/old_reddit_evidence.py \
     --claim-pack runs/<reddit-factcheck-run>/claim-pack.json \
     --out-dir runs/<reddit-factcheck-run>/reddit-evidence-raw
   ```

6. Score retrieved Reddit JSON through `reddit-new-factcheck`.
7. Review accepted evidence manually. Reject false positives when the subreddit,
   persona, workflow, or pain signal is off-topic. Record rejections in a
   `human-review.md` or equivalent artifact.
8. Report one of these statuses:
   - `qualified Reddit support`
   - `weak qualified Reddit support`
   - `contradicted by Reddit evidence`
   - `no qualified Reddit evidence`
   - `primary-source required`

Never use Reddit thread counts, raw keyword hits, generic search snippets, or
off-topic weak matches as proof of demand.
