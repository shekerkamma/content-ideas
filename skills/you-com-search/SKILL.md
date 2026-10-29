---
name: you-com-search
description: Use You.com Search API for high-fidelity web search, livecrawl page retrieval, research reports, and finance research.
---

# You.com Search

Use this skill when a task needs current web research through You.com, especially
when the work benefits from full-page retrieval, agentic research, finance
research, freshness filters, or domain targeting.

## Requirements

Set `YOU_API_KEY` or `YDC_API_KEY`. In Hermes/Codex-on-WSL contexts, the helper
prefers the active Windows Hermes Desktop credential at
`/mnt/c/Users/sheke/AppData/Local/hermes/.env`, then the WSL Hermes file, and
only then an inherited shell value. This ordering prevents a stale exported key
from masking the active cross-host credential.

Do not hardcode API keys in scripts, prompts, markdown files, or repo artifacts.

## Commands

The helper script lives at `scripts/search.py` relative to this `SKILL.md`.
When the skill is installed globally, run that installed copy. From this repo
root, the path is `skills/you-com-search/scripts/search.py`.

Search the web:

```bash
python3 skills/you-com-search/scripts/search.py "your query"
```

Search with livecrawl:

```bash
python3 skills/you-com-search/scripts/search.py "your query" --livecrawl
```

Run Level 2 (You.com discovery plus current full-page Markdown extraction in
the same POST request):

```bash
python3 skills/you-com-search/scripts/level2_search.py "your query"
```

Run You.com Research API:

```bash
python3 skills/you-com-search/scripts/search.py "complex research query" --mode research
```

Run You.com Finance Research API:

```bash
python3 skills/you-com-search/scripts/search.py "finance query" --mode finance
```

## Guidance

- Prefer `search` for targeted discovery and source collection.
- Prefer `--livecrawl` when the agent needs page content, not just result
  snippets. The compatibility flag maps to You.com's current POST
  `extraction_mode: full_page` contract.
- Prefer `research` for multi-step synthesis where You.com should plan and
  execute the research loop.
- Prefer `finance` for fundamentals, filings, market data, commodities, macro,
  financial news, and investor workflows.
- Use `--freshness` or `--from-date`/`--to-date` when claims are time-sensitive.
- Use `--site` to constrain sources and `--exclude-site` to remove noisy
  domains.
- Save final deliverables in repo files; search output is source material, not
  the deliverable.
