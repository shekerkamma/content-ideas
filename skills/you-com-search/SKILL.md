---
name: you-com-search
description: Use when a task needs You.com Search, Research, livecrawl page retrieval, finance research, current competitor research, three-level search workflow, or high-fidelity source discovery before generic web search.
---

# You.com Search

Use this skill when a task needs current web research through You.com, especially
when the work benefits from three-level search, full-page retrieval, agentic
research, finance research, freshness filters, or domain targeting.

## Requirements

Set `YOU_API_KEY` in the environment. In Hermes/Codex-on-WSL contexts, the helper
also reads `~/.hermes/.env` if `YOU_API_KEY` is not already exported.

Do not hardcode API keys in scripts, prompts, markdown files, or repo artifacts.

Before generic web search in strategy, competitor analysis, market research, or
pipeline work, check whether this skill is available and whether `YOU_API_KEY`
is configured. If unavailable, record the failure and then use the next
approved research route such as Exa, Firecrawl, content-research, official
sources, or explicit web verification.

## Commands

The helper script lives at `scripts/search.py` relative to this `SKILL.md`.
When the skill is installed globally, run that installed copy. From this repo
root, the path is `skills/you-com-search/scripts/search.py`.

## Native API Modes

The local You.com helper supports three native API modes:

| Mode | Endpoint | Use for |
|---|---|---|
| `search` | `/v1/search` | Search result discovery, source collection, freshness filters, site include/exclude filters, and optional live crawl |
| `research` | `/v1/research` | Multi-step research synthesis where You.com plans and executes the research loop |
| `finance` | `/v1/finance/research` | Company, market, fundamentals, filings, macro, commodities, investor, and financial-news research |

Live crawl is an option on `search`, not a separate native mode. The helper
exposes it as `--livecrawl` / `--level 2` and sends You.com's accepted
`live_crawl=true` API parameter.

Naming convention is strict:

- CLI/user-facing flag: `--livecrawl`
- workflow label: `Level 2 livecrawl`
- API query parameter: `live_crawl=true`
- do not send `livecrawl=true`, `liveCrawl=true`, `live-crawl=true`, or
  `live_crawl=1`

When patching or reimplementing the helper, preserve this mapping. A common
failure mode is copying the CLI label into the API parameter name.

## Three-Level Workflow Overlay

Use You.com as a staged search tree, not as one flat query. Level 2 is the
priority/default level for competitor analysis and strategy research because it
retrieves current page content instead of relying only on snippets.

| Level | Purpose | API behavior | Use when |
|---|---|---|---|
| 1 | Discovery seed | Search API | Finding candidate competitors, domains, source types, claims, and query directions when the arena is still unknown |
| 2 | Priority evidence retrieval | Search API with `--livecrawl` (`live_crawl=true`) | Default for competitor analysis, market maps, and strategy work; pulls current page content from official/product/pricing/docs pages or source articles |
| 3 | Synthesis | Research API, or Finance Research when `--mode finance` is set | Building an interpreted research brief, market readout, financial/company research view, or complex multi-hop answer |

For competitor analysis, start with Level 2 when you already have the target,
candidate competitors, domains, or buyer arena. Use Level 1 only to seed the
landscape when those are unknown. Use Level 3 only when the question needs
synthesis beyond source collection. Save outputs under the run folder and
convert them into an evidence register before using them in a deck.

Level 2 priority source/content retrieval:

```bash
python3 skills/you-com-search/scripts/search.py "your query" --level 2
```

Level 1 discovery seed:

```bash
python3 skills/you-com-search/scripts/search.py "your query" --level 1
```

Level 3 research synthesis:

```bash
python3 skills/you-com-search/scripts/search.py "complex research query" --level 3
```

Level 3 finance/company synthesis:

```bash
python3 skills/you-com-search/scripts/search.py "finance query" --level 3 --mode finance
```

Target official/product pages and exclude noisy domains:

```bash
python3 skills/you-com-search/scripts/search.py \
  "site:beacon.li Beacon.li competitors onboarding AI implementation proof points" \
  --level 2
```

No-network regression check for the livecrawl API naming convention:

```bash
python3 skills/you-com-search/scripts/check_livecrawl_param.py
```

## Guidance

- Prefer `--level 2` for competitor analysis, market maps, strategy research,
  source validation, and any claim that may enter a client-facing artifact.
- Prefer `search` for targeted discovery and source collection.
- Prefer `--livecrawl` when the agent needs page content, not just result
  snippets.
- Prefer `research` for multi-step synthesis where You.com should plan and
  execute the research loop.
- Prefer `finance` for fundamentals, filings, market data, commodities, macro,
  financial news, and investor workflows.
- Use `--level 1`, `--level 2`, and `--level 3` labels in structured research
  notes so the run shows which part of the You.com search tree was used.
- Use `--freshness` or `--from-date`/`--to-date` when claims are time-sensitive.
- Use `--site` to constrain sources and `--exclude-site` to remove noisy
  domains.
- For competitor analysis, use You.com for source discovery and live page
  retrieval, then convert the findings into run artifacts such as
  `outputs/source-notes.md`, `outputs/company-table.csv`, or
  `outputs/evidence-register.csv`.
- Save final deliverables in repo files; search output is source material, not
  the deliverable.

## Skill Relationships

### Category
Data & Analysis

### Dependencies
None required beyond `YOU_API_KEY` for live API calls.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `competitor-analysis-pipeline` | Sequential upstream | competitor or market research needs current source discovery | `runs/<date>-<target>-competitor-analysis/outputs/source-notes.md` |
| `storm-research` | Parallel / Complement | multi-perspective research needs source discovery | `outputs/storm-brief.md` |
| `exa-api` | Parallel / Complement | semantic discovery is needed in addition to current search | discovered URL list or JSON output |
| `firecrawl` | Sequential downstream | full-page crawl/extract is needed after URL discovery | captured page JSON/markdown |
| generic web search | Fallback | only when You.com is unavailable or insufficient | failure note plus fallback query log |

## Host Compatibility

### Target Hosts
- Claude Code: yes, via `.claude/skills/you-com-search/SKILL.md` wrapper or the global `~/.claude/skills/you-com-search/` install.
- Codex/OpenAI: yes, canonical repo source is `skills/you-com-search/SKILL.md`.
- OpenHands / generic agent hosts: yes, via `.agents/skills/you-com-search/SKILL.md` wrapper.
- Antigravity IDE: yes, but it reads Windows-side copies under `C:\Users\<user>\.gemini\antigravity\skills\you-com-search\` and `C:\Users\<user>\.gemini\config\skills\you-com-search\`. Run `scripts/sync-skills-to-antigravity.sh` after editing the canonical WSL skill.

### Canonical Source
`skills/you-com-search/` is the repo-local source of truth. Host-specific
wrappers should delegate here instead of duplicating the workflow.

### Tool Mapping
- Claude `Bash` -> Codex shell command.
- Claude `Read` -> Codex shell reads or `rg`.
- If a You.com MCP/plugin exists in a host, prefer that official tool; otherwise use `scripts/search.py`.
- Antigravity's previously synced working pattern used native `--livecrawl`; Level 2 maps to that same option and the helper sends `live_crawl=true` to You.com.

## Gotchas

- Do not claim You.com-backed research when the API key is missing, network is blocked, or the command failed.
- Do not change the API parameter from `live_crawl=true`; `livecrawl` is a CLI
  label only.
- Run `scripts/check_livecrawl_param.py` after modifying `scripts/search.py`.
- If the API rejects `--site` / `--exclude-site` with live crawl, remove those parameters and put site constraints in the query text or filter results after retrieval.
- Do not paste raw JSON into client-facing decks; convert it into sourced tables, evidence registers, or concise notes.
- Do not use You.com as final proof for hard claims when primary sources are available. Follow discovered URLs into official pages, filings, docs, or source documents.
- Do not print `YOU_API_KEY` or contents of local env files.
