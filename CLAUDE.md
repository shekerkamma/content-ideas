# content-ideas plugin

A cross-host skill that turns competitor activity into a daily "For You" feed of
content ideas. Runs the same on Claude Code and Codex (and any host that reads
`AGENTS.md`). Dependency-free Python (stdlib only) plus a single self-contained
HTML renderer.

## Structure
- `skills/content-ideas/SKILL.md` — canonical skill definition (the entry point)
- `skills/content-ideas/scripts/scrape.py` — competitor/own-channel scraper
- `skills/content-ideas/scripts/generate_feed.py` — builds the For You HTML feed
- `skills/content-ideas/scripts/export_dashboard.py` — exports the feed as CSV/JSON tables for a hosted dashboard
- `skills/content-ideas/scripts/lib/` — platform fetchers, scoring, relevance, rendering
- `skills/content-ideas/assets/for-you-template.html` — renderer template
- `skills/content-ideas/references/content-strategy.md` — idea-generation guidance

## Cross-host packaging
- `plugin.json` (root) — Agent Plugins 1.0.0 manifest, the vendor-neutral install
- `.claude-plugin/plugin.json` + `marketplace.json` — Claude Code install
- `.codex-plugin/plugin.json` (`"skills": "./skills/"`) — Codex install
- `AGENTS.md` → `@CLAUDE.md` — Codex / generic-agent entry point
- `commands/content-ideas.md` — Claude Code slash command
- `hooks/hooks.json` — SessionStart setup preflight (one-line hint, silent when ready)
- `.claude/output-styles/eli5.md` — optional plain-English answer style (`/output-style`)

### Agent Plugins 1.0.0 conformance

The root `plugin.json` targets the vendor-neutral spec
(`https://agent-plugins.org/specification`) so any conformant client — not just
Claude Code and Codex — can install this repo. Its schema is **closed**:
`$schema` and `name` are the only required keys, and every other top-level key
must be one the spec defines (`version`, `description`, `author`, `homepage`,
`repository`, `license`, `keywords`, `extensions`). Adding a convenience field
there breaks validation, so:

- Client-specific data may live **only** under `extensions`, keyed by a
  reverse-domain namespace the client controls. No client has published one
  yet — the spec documents only the `com.example.client` placeholder and
  maintains no registry — so the Codex `interface` block stays in
  `.codex-plugin/plugin.json`, which is where Codex actually reads it. Do not
  invent a namespace to move it early.
- Components are discovered from fixed locations: skills from `skills/`, MCP
  servers from `mcp.json`. This repo ships no MCP server of its own, and a
  missing `mcp.json` is explicitly non-fatal — do not add a stub.
- `tests/test_plugin_contract.py` enforces the closed key set, the `$schema`
  constant, the name pattern, and version parity with the host manifests.
- Validate after any edit:
  `uvx check-jsonschema --schemafile <the 1.0.0 plugin schema> plugin.json`

### Skill source and porting contract

- Treat `skills/content-ideas/`, `skills/pipeline-runner/`,
  `skills/second-brain/`, `skills/plaid/`, and
  `skills/karpathy-guidelines/` as canonical shared sources.
- Treat `skills/docx/`, `skills/pdf/`, `skills/improve/`, and
  `skills/storm-research/` as canonical shared recovery sources for those
  skills. They must remain portable across Claude Code and Codex and must not
  contain generated Python bytecode or host credentials.
- Treat `skills/skill-doctor/` as the canonical source for skill-tree corruption
  detection and repair. Its host wrappers at `.claude/skills/skill-doctor/` and
  `.agents/skills/skill-doctor/` must stay byte-identical to each other and must
  contain no repair logic of their own. The executable lives at
  `scripts/audit_skill_corruption.py` (stdlib only) and generalizes the
  four-skill NUL check in `scripts/verify-recovery-skills.sh` to every skill tree.
- Treat `skills/skill-hygiene/` as the canonical library-maintenance router: it sequences
  `skill-doctor` (intact) → `skills-analyst` (earned) → `writing-for-agents` (lean) →
  `skill-builder` (rewrite). The gate order is load-bearing — `skills-analyst` reads a
  zero-filled `SKILL.md` as DELETE/ARCHIVE, so repair must precede classification. It is
  user-invoked (`disable-model-invocation: true`) and therefore costs no context load.
  Its host wrappers must stay byte-identical and carry no sweep logic.
- Keep matching copies under `plugins/content-ideas/skills/` byte-identical.
- Keep Claude-only UI fields as enhancements; repeat critical safety and
  fallback behavior in skill bodies for Codex and OpenHands.
- Before shipping skill changes, run the plugin contract, the three
  `skill-builder` audit scripts, and the full pytest suite.

## Channel-to-KB skills

Three peer skills (`skills/channel-to-kb/`, `-ytdlp/` (recommended default),
`-supadata/`) turn a YouTube channel into an OKF knowledge base under
`$CONTENT_HOME/knowledge-bases/<channel-slug>/`, never the cwd. Their
`assets/okf-template/` files and `references/pipeline-guide.md` must stay
byte-identical across all three. Details and the upstream re-port procedure:
`docs/agent-reference/channel-to-kb.md`.

## Roast Room skills

`skills/roast-room/` (advisor council on a founder decision) and `skills/newroaster/` (build a new
advisor) are ported from `github.com/nateherkai/roast-room` (MIT, licence kept in each folder).
Seats ship as plain files in `skills/roast-room/seats/` and run as `general-purpose` sub-agents, so
no agent is registered and the council runs the same on Claude Code and Codex. Bundled seats,
brains, and examples are read-only; sessions, custom seats, brains, portraits, and roster changes
live under `$ROAST_HOME` (default `$CONTENT_HOME/roast-room`). The room (`app/`) and the newroaster
scripts need Node 20+, an optional add-on outside the stdlib-only runtime rule.
`tests/test_roast_room.py` guards the paths and the quote checker.

## Shared Product-Build Skills
- `skills/plaid/SKILL.md` — Product Led AI Development: idea, validation,
  planning, `docs/design.md`, launch, and roadmap execution.
- `skills/karpathy-guidelines/SKILL.md` — coding guardrails: think before
  coding, keep solutions minimal, edit surgically, and verify success criteria.

## Presentation system

- `skills/present/SKILL.md` is the single public router for presentation work.
- Keep output engines distinct (native PPTX `branded-pptx-deck`, existing-PPTX
  edits `pptx-toolkit`, HTML `presentation`, Genspark `genspark-slides` +
  `genspark-branded-deck`, Markdown `marp`); do not add a top-level skill per
  template, layout, critic, or adapter.
- Impeccable is for HTML surfaces only; never use it in place of
  `pptx-design-quality/scripts/lint_pptx.py` for `.pptx`.
- Template derivation, claim-evidence checks, and the Impeccable pin
  (`scripts/design-qa-detect.sh`): `docs/agent-reference/presentation-system.md`.

## Repo-local Claude Code skills

- `.claude/skills/claude-code-director/` (Director Framework) and the PLAID
  `/goal` build loop for long-running app builds:
  `docs/agent-reference/claude-code-director-and-plaid.md`.
- `.claude/skills/excel-ingest/` is a wrapper for `skills/ai-analyst/excel-ingest/`, which
  turns an Excel workbook into analysis-ready CSVs (needs `pandas` and `openpyxl`, so it
  is outside the stdlib-only runtime rule). Run `--list` first. It assumes one table per
  sheet, so read stacked-table report sheets by label.

Claude Code loads `.claude/skills/` automatically. `.claude/settings.json`
registers this repo as the `content-ideas` marketplace and enables the
`content-ideas` plugin, which serves every skill under `skills/`. After
trusting the folder, each person installs it once with
`/plugin install content-ideas@content-ideas`. If you already mirror skills
into `~/.claude/skills/` with `scripts/sync-presentation-pipeline-hosts.sh` or
`scripts/sync-codex-skills.sh`, set the plugin to `false` in
`.claude/settings.local.json` instead, so skills don't load twice. Keep
machine-specific paths out of that file; personal or out-of-repo skills (for example `.agents/skills/` or a
`content-ideas.local` checkout) belong in `~/.claude/skills/` or
`.claude/settings.local.json`. Codex discovers the packaged copies after
installing the repo marketplace plugin, whose `.codex-plugin/plugin.json`
exposes `"skills": "./skills/"`. `AGENTS.md` remains the repo-level fallback
before plugin installation.

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

# mirror every ~/.claude/skills entry into ~/.codex/skills so Codex sees the
# same skill set as Claude Code (idempotent, safe to re-run after installing
# new skills on either host)
bash scripts/sync-codex-skills.sh

# synchronize the governed presentation pipeline to Claude Code and the
# Windows Hermes Desktop profile mounted into WSL; differing host copies are
# backed up before replacement
bash scripts/sync-presentation-pipeline-hosts.sh

# validate the portable recovery skills and their integrity manifest
bash scripts/verify-recovery-skills.sh

# audit every skill tree for zero-fill (all-NUL) corruption and restore from
# ranked donors (sibling host copies, then git history). Report-only without
# --apply; exits non-zero when a live skill file is corrupt with no donor.
python3 scripts/audit_skill_corruption.py ~ --git-repo .
python3 scripts/audit_skill_corruption.py ~ --git-repo . --apply
```

## Rules
- Runtime stays dependency-free: stdlib only (`urllib`, `json`, ...). No pip installs at runtime.
- `skills/content-ideas/scripts/lib/__init__.py` is a bare package marker — no eager imports.
- Persistent state lives under `$CONTENT_HOME` (default `~/Documents/Content`), never the cwd.
- Credentials live in `~/.config/content/.env` (`SCRAPECREATORS_API_KEY`, `SETUP_COMPLETE`).
- API keys follow a two-layer pattern: `.claude/settings.local.json` `env`
  block (Claude Code, gitignored) plus a `~/.bashrc` `export` (cross-host
  baseline for Codex). Write both together. Never put a real key in a commit or
  any tracked file. Configured keys, where to look for existing ones (including
  Windows-side configs and local AI-gateway proxies), and WSL/PowerShell
  pitfalls: `docs/agent-reference/local-host-setup.md`.
- If `gbrain` is available as an MCP server, use it by default for cross-session
  memory and retrieval before repeating strategy or pipeline research from
  scratch.
- Treat `gbrain` as an explicit chain stage:
  - `GBrain Recall` before `content-research`, strategy synthesis, or pipeline
    Stage 1 work
  - `GBrain Write-back` after the run when durable findings should become
    reusable memory
- Treat GBrain as the durable knowledge layer for recurring companies, people,
  prospects, verticals, themes, named accounts, and prior research findings.
- Treat GBrain retrieval as embedding-backed semantic retrieval by default, not
  just keyword lookup.
- Prefer semantic recall first; use synthesis only when the task needs merged
  interpretation rather than simple recall.
- Read from GBrain first when the task references an entity or topic that may
  have appeared in prior work, and write durable findings back after the run
  when they are likely to matter again.
- When a chained run or pipeline uses GBrain, reflect that explicitly in the
  run status instead of treating it as invisible setup.
- Do not use GBrain as the system of record for deliverables. Briefs, feed
  data, decks, and client-facing artifacts must still be written to local files
  in the repo or run folders.
- In Codex Desktop or any host that exposes stronger research plugins such as
  `exa`, prefer those plugins for discovery and current web research during
  Stage 1 research and strategy/pipeline work. Use them to find better official
  product pages, documentation, GitHub repos, competitive signals, and current
  operator proof points faster than generic search alone.
- In terminal-first hosts such as Codex CLI, prefer the closest equivalent:
  an MCP-connected research server or a local CLI/API wrapper for tools such as
  Exa when available. Treat that as the terminal analogue to desktop plugin
  access.
- Concrete terminal patterns to prefer when available:
  - Exa MCP over remote/HTTP MCP
  - a local Exa API wrapper that calls `https://api.exa.ai/search`
- Codex Desktop plugin access is a discovery advantage, not an exception path.
  The same workflow, delivery, QA, and source-verification rules still apply.
- Plugin-assisted research improves discovery; it does not replace local file generation,
  branded PPTX build and QA, repo-specific workflow rules, or the requirement to
  verify that final cited sources are primary and current.
- Host-specific paths must be configurable. Prefer environment variables over
  machine-specific absolute paths for branded templates, delivery destinations,
  second-brain exports, and vault locations.
- Client-facing PowerPoint output must use the branded PowerPoint template at
  `BRANDED_PPTX_TEMPLATE`, or fall back to
  `~/.claude/templates/branded-template.pptx`, or the downstream
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
  9. the reviewed deck must be the one copied to the user-facing delivery path
     resolved from `CLIENT_DELIVERY_DIR`
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
- Version is tracked in `pyproject.toml`, `plugin.json`,
  `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
  `.codex-plugin/plugin.json`, and the
  `version:` field of `SKILL.md` — keep them identical. `tests/test_plugin_contract.py` enforces this.

## GBrain (MCP server — persistent memory layer)

GBrain is wired as an MCP server at `http://127.0.0.1:3131/mcp` (HTTP, per-agent
bearer token) and provides persistent knowledge-graph memory across sessions.
Install location, systemd service, token rotation, and CLI commands:
`docs/agent-reference/gbrain.md`.

### When to use GBrain vs local files
- **GBrain pages**: prospects, people, companies, recurring research topics,
  verticals, use-case themes, meeting notes, deal context — anything that
  compounds across sessions and benefits from graph traversal and synthesis.
- **Local files** (`$CONTENT_HOME/research/`): pipeline run artifacts,
  feed-data.json, strategy briefs, PPTX decks — session-scoped deliverables
  that follow the pipeline-runner workflow.
- **Memory files** (`~/.claude/projects/.../memory/`): behavioral guidance,
  user preferences, project meta — things that shape how the agent works.

### Cost guardrails
- Search mode is `conservative`. Do NOT change to `balanced` or `tokenmax`
  without explicit user approval — cost scales 2.5× to 5× respectively.
- Dream cycle / enrichment crons are NOT enabled. Do not enable without
  explicit user approval — each cron job fires LLM calls.
- Prefer `search` (keyword, free) over `ask`/`query` (synthesis, costs
  tokens) for simple lookups.
- For strategy/pipeline recall, prefer embedding-backed semantic retrieval over
  plain keyword lookup when both are available. Escalate to synthesis only when
  the task needs aggregation, interpretation, or merged judgment.
- When writing pages, embeddings fire automatically. Batch writes where
  possible to reduce embedding calls.

## Generative UI demos

Reference repos (`~/awesome-llm-apps/generative_ui_agents/`,
`~/real-estate-dashboard-agent/`, `~/gbrain/`) and the ADK + AG-UI rules (always
include `AGUIToolset()`; never duplicate frontend tools server-side):
`docs/agent-reference/generative-ui.md`.

## Portable path defaults

Use these environment variables to make the same workflow portable across
Codex, Claude, and terminal hosts:

- `BRANDED_PPTX_TEMPLATE` — branded `.pptx` template path. Default fallback:
  `~/.claude/templates/branded-template.pptx`
- `CLIENT_DELIVERY_DIR` — optional copy-out location for reviewed decks
- `SECOND_BRAIN_DIR` — optional content-research export directory
- `OBSIDIAN_VAULT_DIR` — optional vault root for content-research notes

If an env var is unset, do not invent a machine-specific substitute beyond the
documented fallback. Report the step as blocked or skip the optional export.

## Skill Builder

- **skill-builder** (`.claude/skills/skill-builder/SKILL.md`) — guided skill creation and audit tool following Claude Code official best practices.
- Trigger: `/skill-builder` or "help me build a skill" or "audit this skill"
- Supports: new skill discovery interview · existing skill audit · frontmatter optimization
- Technical reference: `.claude/skills/skill-builder/reference.md`
