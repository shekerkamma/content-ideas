---
name: exa-api
description: Use Exa semantic web search from Codex or Claude Code through a local curl-based wrapper around https://api.exa.ai/search. Use for source discovery, competitor research, market signals, buyer-language discovery, documentation discovery, and research stages where generic web search is too weak.
license: MIT
metadata:
  legacy-frontmatter:
    category: Research
    argument-hint: search <query> [num_results]
---

# Exa API

This repo-local skill provides a host-neutral Exa route when an Exa MCP tool is
not exposed. It is intentionally a thin wrapper around the official Exa API so
Claude Code and Codex can use the same research policy.

`you-com-search` is the preferred general current-web search/research route
when it is available. Use this Exa skill as the semantic/source-discovery
specialist, not as a reason to fall back to ordinary WebSearch.

## Availability

Check for `you-com-search` and an Exa MCP/plugin first. If no Exa MCP is
available, use this skill for Exa-specific semantic discovery.

```bash
if [ -n "$EXA_API_KEY" ]; then echo "EXA_API_KEY=set"; else echo "EXA_API_KEY=unset"; fi
```

The wrapper also auto-loads known local secret files when `EXA_API_KEY` is not
already exported:

1. `/mnt/c/Users/sheke/AppData/Local/hermes/.env`
2. `$HOME/.hermes/.env`

Do not print secret values. If `EXA_API_KEY` is still unset after those probes,
Exa is unavailable in this host. Do not replace it with generic search and
still call the result validated research.

## Search

Use the bundled wrapper:

```bash
skills/exa-api/scripts/exa_search.sh "agentic AI disrupting SaaS pricing" 10
```

The script emits JSON. Save important outputs under `runs/<date>-<topic>/` when
they become part of a research artifact.

## Research Usage Rules

Use You.com before generic web search for broad current-web searching,
livecrawl, research, and finance research. Use Exa before generic web search
for semantic/source discovery such as:

- competitor and category discovery,
- current market signals,
- official product/docs/pricing pages,
- forum/review/support pages,
- buyer-language and workflow evidence,
- GitHub repos and technical proof points.

Exa is discovery, not final proof by itself. For hard claims, follow discovered
URLs into primary sources and, when available, ingest important pages with
You.com livecrawl or Firecrawl.

## Failure Policy

If Exa is unavailable because the key is missing, the API is blocked, or the
host lacks network access:

1. Record the exact failure.
2. Downgrade the run from `validated-research` if Exa was required.
3. Produce an Exa query pack for a later live run.
4. Do not claim Exa-backed discovery.
5. If `you-com-search` is available, use it before generic WebSearch.
