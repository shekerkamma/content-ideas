# content-ideas plugin

A cross-host skill that turns competitor activity into a daily "For You" feed of
content ideas. Runs the same on Claude Code and Codex (and any host that reads
`AGENTS.md`). Dependency-free Python (stdlib only) plus a single self-contained
HTML renderer.

## Structure
- `skills/content-ideas/SKILL.md` — canonical skill definition (the entry point)
- `skills/content-ideas/scripts/scrape.py` — competitor/own-channel scraper
- `skills/content-ideas/scripts/generate_feed.py` — builds the For You HTML feed
- `skills/content-ideas/scripts/lib/` — platform fetchers, scoring, relevance, rendering
- `skills/content-ideas/assets/for-you-template.html` — renderer template
- `skills/content-ideas/references/content-strategy.md` — idea-generation guidance

## Cross-host packaging
- `.claude-plugin/plugin.json` + `marketplace.json` — Claude Code install
- `.codex-plugin/plugin.json` (`"skills": "./skills/"`) — Codex install
- `AGENTS.md` → `@CLAUDE.md` — Codex / generic-agent entry point
- `commands/content-ideas.md` — Claude Code slash command
- `hooks/hooks.json` — SessionStart setup preflight (one-line hint, silent when ready)

The skill resolves its own directory from the Codex cache, the Claude plugin
cache, or a repo checkout — see the resolution block at the top of `SKILL.md`.
Keep that block in sync if directory names change.

## Commands
```bash
# run the test suite (stdlib + pytest, no network)
python3 -m pytest -q

# exercise the scraper / feed generator directly against a checkout
python3 skills/content-ideas/scripts/scrape.py --help
python3 skills/content-ideas/scripts/generate_feed.py --help
```

## Rules
- Runtime stays dependency-free: stdlib only (`urllib`, `json`, ...). No pip installs at runtime.
- `skills/content-ideas/scripts/lib/__init__.py` is a bare package marker — no eager imports.
- Persistent state lives under `$CONTENT_HOME` (default `~/Documents/Content`), never the cwd.
- Credentials live in `~/.config/content/.env` (`SCRAPECREATORS_API_KEY`, `SETUP_COMPLETE`).
- In Codex Desktop or any host that exposes stronger research plugins such as
  `exa`, prefer those plugins for discovery and current web research during
  Stage 1 research and strategy/pipeline work. Use them to find better official
  product pages, documentation, GitHub repos, competitive signals, and current
  operator proof points faster than generic search alone.
- In terminal-first hosts such as Codex CLI, prefer the closest equivalent:
  an MCP-connected research server or a local CLI/API wrapper for tools such as
  Exa when available. Treat that as the terminal analogue to desktop plugin
  access.
- Codex Desktop plugin access is a discovery advantage, not an exception path.
  The same workflow, delivery, QA, and source-verification rules still apply.
- Plugin-assisted research improves discovery; it does not replace local file generation,
  branded PPTX build and QA, repo-specific workflow rules, or the requirement to
  verify that final cited sources are primary and current.
- Client-facing PowerPoint output must use the branded PowerPoint template at
  `/home/shekerk/.claude/templates/branded-template.pptx` or the downstream
  `branded-pptx-deck` / `pptxkit` workflow that wraps it. Do not generate
  client-facing `.pptx` decks from ad hoc `python-pptx` slide layouts or blank
  presentations. If the branded template/workflow is unavailable, stop and say
  the PPTX is blocked rather than shipping an unbranded substitute.
- Every client-facing slide must contain structured content, not just a title
  and a few loose bullets. Default to a clear slide contract per page:
  action title, supporting structure (cards/table/scorecard/use-case layout),
  and explicit evidence, implication, or next-step content. For use-case decks,
  always include at least one detailed use-case realization slide using the
  branded layout (challenge, solution, how-it-works, stats, stack, systems,
  users, organizations).
- PPTX QA is a delivery gate, not an optional polish step. Before delivering any
  client-facing deck:
  1. the branded builder must save successfully with validation enabled
  2. slide text must be checked for overlap, overflow, and collisions
  3. if `preview_pptx.py` is available, its contact sheets must be reviewed
  4. if preview tooling is unavailable, say the deck is unreviewed for visual QA
     and do not present it as final
  5. if overlap is observed, fix the deck before delivery
  6. use a delivery status explicitly: `draft`, `reviewed`, or `blocked`
  7. use filename suffixes that match that status: `*-draft.pptx`,
     `*-reviewed.pptx`, `*-blocked.txt` or equivalent
  8. keep the branded deck builder script in the run folder so QA fixes are
     reproducible
  9. the reviewed deck must be the one copied to the user-facing Windows path
  10. minimum visual QA checklist:
      - no red overflow boxes in `preview_pptx.py`
      - no title/subtitle collisions
      - no clipped text in stat bars, callout strips, or side panels
      - footer/page number present on each slide
- When building strategy/pipeline outputs from use cases, content-research notes,
  or external documents that reference OpenHands, treat the OpenHands GitHub
  repo and docs as the source of truth for implementation details:
  - Repo: `https://github.com/OpenHands/OpenHands`
  - Docs: `https://docs.openhands.dev/`
  Use these to ground coding snippets, agent patterns, skills/microagents, MCP
  integration, CLI/headless workflows, deployment models, and solution-stack
  technology choices. Prefer verified OpenHands primitives over invented
  orchestration details.
- Version is tracked in `pyproject.toml`, `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, and the
  `version:` field of `SKILL.md` — keep them identical. `tests/test_plugin_contract.py` enforces this.
