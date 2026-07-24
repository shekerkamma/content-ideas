# Research & Memory Policy (strategy mode)

**OpenHands source of truth for implementation details.** When strategy mode is
active and the use case involves agent orchestration, coding automation, MCP
integration, skills, sub-agents, or the source material explicitly references
OpenHands, verify the implementation stack against:
- `https://github.com/OpenHands/OpenHands`
- `https://docs.openhands.dev/`

Use those sources for coding snippets, framework choices, skills/microagents,
deployment patterns, CLI/headless workflows, and MCP/server integration details.
Do not invent OpenHands capabilities from analogy or generic agent-tooling lore.

**GBrain when available.** If `gbrain` is exposed as an MCP server in the host,
use it by default for cross-session memory and retrieval before repeating
strategy-mode research from scratch. Use it as the durable knowledge layer for
recurring companies, people, prospects, verticals, themes, named accounts, and
prior research findings. Read from it first when the current topic may overlap
with prior work, and write durable findings back after the run when they are
likely to matter again. Treat GBrain retrieval as embedding-backed semantic
retrieval by default, not just keyword lookup. Prefer semantic recall first;
use synthesis only when the task needs merged interpretation rather than simple
recall.

Treat this as an explicit chain step, not just a preference note:
- `GBrain Recall` before fresh strategy-mode discovery or downstream handoff
- `GBrain Write-back` after the run when the findings should become reusable
  memory for later `/pipeline-runner`, `/vertical-scorer`, or `/ai-strategy-brief`

When a run uses GBrain successfully, note that in the run status or stage
summary so the chain is auditable.

GBrain is not the system of record for pipeline deliverables. `feed-data.json`,
briefs, strategy docs, deck builders, and client-facing artifacts must still be
written to the local run folder and repo files.

**Research plugins when available.** In Codex Desktop or another host that
exposes stronger research plugins, prefer `you-com-search` first for
current-web search/research/livecrawl when available, then specialist tools
such as `exa` for semantic/source discovery and Firecrawl for page capture.
Use these during Stage 1 discovery to find better official product pages,
docs, GitHub repos, competitive signals, and current operator proof points
faster than generic search alone.

In terminal-first hosts such as Codex CLI, prefer the closest equivalent:
an MCP-connected research server or a local CLI/API wrapper for tools such as
Exa when available. Treat that as the terminal analogue to desktop plugin
access.

Concrete terminal patterns to prefer when available:
- `you-com-search` or Hermes `web.search_backend: you` before generic web
  search
- Exa MCP over remote/HTTP MCP
- a local Exa API wrapper that calls `https://api.exa.ai/search`

Codex Desktop plugin access is a discovery advantage, not an exception to the
rest of this workflow. The same local artifact-generation, branded-deck, QA,
repo-rule, and source-verification requirements still apply.

Plugin-assisted research improves source discovery, but it does **not** replace:
- local file generation
- branded PPTX build and QA
- repo-specific workflow rules
- verifying that final cited sources are primary and current

Host-specific paths must stay portable. Prefer environment-driven paths over
machine-specific absolute paths for branded templates, delivery directories,
second-brain exports, and vault locations.
