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

### Skill source and porting contract

- Treat `skills/content-ideas/`, `skills/pipeline-runner/`,
  `skills/second-brain/`, `skills/plaid/`, and
  `skills/karpathy-guidelines/`, and `skills/meta-loop/` as canonical shared sources.
- Treat `skills/docx/`, `skills/pdf/`, `skills/improve/`, and
  `skills/storm-research/` as canonical shared recovery sources for those
  skills. They must remain portable across Claude Code and Codex and must not
  contain generated Python bytecode or host credentials.
- Keep matching copies under `plugins/content-ideas/skills/` byte-identical.
- `skills/meta-loop/` runs Claude Code Opus as the sole aggregator and isolated
  Codex CLI models as workers; keep its host installations synchronized with
  the canonical repo copy and never place credentials in worker briefs.
- Keep Claude-only UI fields as enhancements; repeat critical safety and
  fallback behavior in skill bodies for Codex and OpenHands.
- Before shipping skill changes, run the plugin contract, the three
  `skill-builder` audit scripts, and the full pytest suite.

### Evidence-ranking rules for research-bearing skills

Any skill that recommends a tool, vendor, library, stack, or comparable
project carries an editable `## Judgment rules` section stating these three.
Keep the policy on the page and tunable — never hardcode it into step
instructions. Currently applied in `skills/plaid/SKILL.md` and
`.claude/skills/saas-replacement-auditor/SKILL.md`; extend to
`ai-head-of-engineering-build-vs-buy-auditor`, `ai-head-of-engineering-stack-picker`,
and `investor-competitive-dossier` when they are next touched.

- **Popularity is not fit.** Never rank options by GitHub stars, download
  counts, or social popularity alone. Stars are a bookmark count that only
  increases: they record that people liked something once, not that it fits
  this problem. Rank on fit to stated constraints, then on maintenance
  signals carrying an exact date. This is the same failure the
  `last30days` skill deliberately inverts — that skill treats stars as a
  trend signal on purpose, and is the one documented exception.
- **Split every comparable in two: what transfers, and what exists only
  because that project got big.** A mature project's plugin system,
  multi-tenancy, or infrastructure reflects its team size, scale, and
  deployment history — not ours. Copying the second half imports complexity
  without the reasons for it, and sizing a build against it inflates cost
  estimates until sound candidates fail. State which half each
  recommendation rests on.
- **Cost every vendor at three points, not one:** during build with zero
  users, the first day real users arrive, and at 10x that. "Free to start"
  is not "cheap to operate." A per-seat or per-active-user price invisible
  in month one is a roadmap constraint by month six; a tool inside a free
  tier today becomes a replacement candidate the month it crosses the cap.
  Name the cap and the crossing point, not just today's invoice.

Adapted from `AaravKashyap12/advise-project-approach` (MIT) rather than
installed — this repo already owns that workflow four times over in `plaid`,
`saas-replacement-auditor`, `ai-head-of-engineering-build-vs-buy-auditor`,
and `deep-research`, and that skill does external research without honoring
the global Research Tool Order.

## Channel-to-KB skills (ported from coleam00/cole-medin-knowledge-base)

Three peer skills that turn any YouTube channel into an OKF (Open Knowledge
Format) knowledge base / Karpathy-style LLM wiki, differing only in how they
fetch transcripts:
- `skills/channel-to-kb/SKILL.md` — pytubefix + youtube_transcript_api, free,
  no API key, can be IP-blocked on cloud hosts.
- `skills/channel-to-kb-ytdlp/SKILL.md` — yt-dlp, free, no API key, most
  reliable against YouTube changes. Recommended default.
- `skills/channel-to-kb-supadata/SKILL.md` — Supadata managed API, paid
  (`SUPADATA_API_KEY`), no IP-blocking risk.

Each skill bundles its own copy of the shared OKF toolkit under
`assets/okf-template/` (`SCHEMA.md`, `lint.py`, `scripts/build_indexes.py`)
and `references/pipeline-guide.md` — these four files must stay
byte-identical across all three skill directories (mirrors the
`plugins/content-ideas/skills/` byte-identical convention above). Output
bundles scaffold under `$CONTENT_HOME/knowledge-bases/<channel-slug>/`, never
the cwd. If upstream (`coleam00/cole-medin-knowledge-base`) changes its
`SCHEMA.md`, `lint.py`, `scripts/build_indexes.py`, or
`.claude/references/pipeline-guide.md`, re-port them into all three skills'
`assets/okf-template/` and `references/` and re-verify the scaffold lints
clean on an empty bundle before shipping.

## Shared Product-Build Skills
- `skills/plaid/SKILL.md` — Product Led AI Development: idea, validation,
  planning, `docs/design.md`, launch, and roadmap execution.
- `skills/karpathy-guidelines/SKILL.md` — coding guardrails: think before
  coding, keep solutions minimal, edit surgically, and verify success criteria.

## Presentation system

- `skills/present/SKILL.md` is the single public router for presentation work.
- Keep output engines distinct: native PPTX uses `branded-pptx-deck`, controlled
  existing-PPTX edits use `pptx-toolkit`, HTML uses `presentation`, hosted Genspark uses
  `genspark-slides` plus `genspark-branded-deck`, and Markdown slides use `marp`.
- Keep template profiles and slide archetypes inside `pptx-design-quality`; do not create
  another top-level presentation skill for each template, layout, critic, or adapter.
- Keep acquisition utilities inside `presentation-source-bundle`; web/PDF/OneDrive intake
  is evidence normalization, not a presentation renderer.
- When a reference deck exists, draft `template-profile.json` and `slide-plan.json` from it
  instead of hand-authoring from the blank template: `pptx-design-quality/scripts/
  derive_template_profile.py` (brand colors, fonts, geometry) and `pptx-visual-spec/
  scripts/draft_slide_plan.py` (per-slide archetype and evidence links). Both write a
  distinctly named draft only — never the canonical contract file — and still require
  tailoring plus the normal validators before build. Adapted from analyzing
  `pamelafox/presentation-skills`'s ingestion skills against this repo's contract-owning
  skills, not ported 1:1; see `skills/pptx-design-quality/references/template-derivation.md`.
- For an evidence-derived deck, run `pptx-design-quality/scripts/check_claim_evidence.py`
  as a fast mechanical pre-pass (unsourced-number scan against cited evidence) before the
  richer `video-to-deck` Grill-Me or Genspark factual-integrity review; it does not replace
  either.
- Impeccable (`pbakaus/impeccable`, MIT... Apache 2.0) is installed for the HTML-based
  surfaces only: `.claude/skills/impeccable/`, `.agents/skills/impeccable/`, and
  `.github/skills/impeccable/` (one copy per detected harness, installed via
  `npx impeccable skills install`; hooks wired into `.claude/settings.local.json`
  (gitignored, machine-local), `.codex/hooks.json`, and `.github/hooks/impeccable.json`).
  It does not understand native `.pptx` — never install or invoke it as a substitute for
  `pptx-design-quality/scripts/lint_pptx.py`, which already covers the PPTX-native
  equivalent checks (overflow, overlap, contrast, font/color-count caps, DPI, layout
  repetition) with its own `qa.ignore_rules`/`qa.waivers` waiver mechanism.
  `scripts/design-qa-detect.sh` is the pinned wrapper (`impeccable@3.5.0`, requires
  Node >= 24) that `marp` and `genspark-branded-deck` run against authored HTML before
  PPTX export; bump the pin there and in this file together when upgrading.

## Claude Code Director Skill
- `.claude/skills/claude-code-director/SKILL.md` — Director Framework (Cole Medin):
  Plan First → Manage Context → Verify The Work → Build The System. Generates
  PLAN.md, context budget, verification harness, and system evolution notes.
- Trigger: `/claude-code-director` or "director mode", "plan this properly",
  "stop vibe coding", "apply the director framework"

Claude Code project settings are in `.claude/settings.json` and point at these
repo-local skill files. Codex discovers the packaged copies after installing
the repo marketplace plugin, whose `.codex-plugin/plugin.json` exposes
`"skills": "./skills/"`. `AGENTS.md` remains the repo-level fallback before
plugin installation.

For long-running app builds, use PLAID as the product source of truth and
Codex/Claude `/goal` as the execution loop:
1. Read `vision.json`, `docs/product-vision.md`, `docs/prd.md`, and
   `docs/product-roadmap.md`.
2. If `docs/design.md` is present, follow it for UI. If it is missing, use the
   brand guidance in `docs/product-vision.md` and keep the UI restrained.
3. Execute roadmap tasks in order, one phase at a time.
4. Mark roadmap checkboxes complete only after implementation and verification.
5. Run available build, lint, test, and manual verification before reporting a
   goal achieved.

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
```

## Rules
- Runtime stays dependency-free: stdlib only (`urllib`, `json`, ...). No pip installs at runtime.
- `skills/content-ideas/scripts/lib/__init__.py` is a bare package marker — no eager imports.
- Persistent state lives under `$CONTENT_HOME` (default `~/Documents/Content`), never the cwd.
- Credentials live in `~/.config/content/.env` (`SCRAPECREATORS_API_KEY`, `SETUP_COMPLETE`).
- API keys used by this project's skills follow a two-layer pattern, because
  Claude Code and Codex have no shared secrets mechanism:
  - **`.claude/settings.local.json`'s `env` block** — Claude-Code-specific.
    Injected directly into every session for this project regardless of how
    the session was launched; works even in non-interactive Bash tool calls,
    which don't source `~/.bashrc`. Gitignored (`.gitignore` has the
    `.claude/settings.local.json` pattern) — never the committed
    `.claude/settings.json`.
  - **`~/.bashrc` `export`** — the cross-host baseline. Codex reads secrets
    from its own process environment directly (e.g. `bearer_token_env_var`
    in `~/.codex/config.toml` for the gbrain MCP server); it has no
    settings.local.json equivalent, so this layer is what Codex — and any
    interactively-launched Claude Code session — actually relies on.
  - Write to both layers together; neither replaces the other. Never put a
    real key in `~/.config/content/.env`'s tracked convention notes, a
    commit, or any file under version control.
  - Currently configured this way: `SUPADATA_API_KEY`, `GBRAIN_REMOTE_TOKEN`,
    `OPENAI_API_KEY`, `EXA_API_KEY`, `GOOGLE_GENERATIVE_AI_API_KEY`,
    `GROQ_API_KEY`. When hunting for an already-configured key before asking
    the user for a new one, check beyond this repo and beyond WSL paths —
    Windows-side app configs (e.g. `/mnt/c/Users/<user>/AppData/Local/hermes/.env`,
    `/mnt/c/Users/<user>/.config/watch/.env`, `/mnt/c/Users/<user>/.fcc/.env`,
    `/mnt/c/Users/<user>/.cli-proxy-api/config.yaml`) have held real values
    that their WSL-side namesakes didn't.
- Local AI-gateway/router proxies on the Windows side are common places to
  find already-configured provider keys and model routing before assuming a
  tool is broken or asking for new credentials:
  - **`free-claude-code` (fcc)** — `~/.fcc/.env` (provider keys plus
    `MODEL`/`MODEL_OPUS`/`MODEL_SONNET`/`MODEL_HAIKU` routing), binaries at
    `~/.local/bin/fcc-*.exe`. Actively developed upstream — before trusting a
    hard failure, check whether the installed build predates the commit that
    fixed it (`fcc-server --version`), and update via the installer one-liner
    in its README before debugging further.
  - **OmniRoute** — dashboard/API on `127.0.0.1:20128`; the gateway API key
    lives in its SQLite-backed dashboard, not `.env` (`~/OmniRoute/.env` only
    holds server-runtime secrets like `INITIAL_PASSWORD`/`JWT_SECRET`). Use
    the bundled `omniroute` CLI (`providers list`, `models <provider>`,
    `usage logs`, `setup-claude`, `setup-kilo`, `launch --profile <name>`)
    instead of the dashboard when a CLI path exists — no login needed.
    `providers list` / `models` catalog entries are not proof a model ID is
    actually routable, and `auto/*` combos can silently pick a different
    provider than expected — confirm with a real `/v1/chat/completions` call
    and cross-check `omniroute usage logs` for the provider/status that
    actually served it.
  - **cli-proxy-api** (`router-for-me/CLIProxyAPI`, often bundled inside
    another tool's `bin/`, e.g. Hermes) — config at
    `~/.cli-proxy-api/config.yaml`, OAuth credentials as
    `<provider>-<email>.json` in the same directory. Must be launched with an
    explicit `-config <path>` flag; it does not reliably resolve the config
    path from a WSL-launched process's working directory. Stored OAuth
    tokens refresh lazily on the next proxied request, not on a timer — a
    stale `expired` timestamp with the process not currently running is not
    itself a bug.
  - **Hermes Agent** (NousResearch, git install) — `~/AppData/Local/hermes/`.
    `hermes skills list-modified` lists real user-customized skills by name;
    a noisy `git status` in its `hermes-agent` checkout (e.g. from a botched
    update stash/restore) does not by itself threaten them — Hermes tracks
    skill customizations separately from raw git diff state.
- PowerShell or native `.exe` processes launched from a WSL Bash shell
  inherit the WSL cwd, which Windows renders as a `\\wsl.localhost\<distro>\...`
  UNC path — cmd.exe refuses it outright, and some native exes silently
  resolve relative config paths against it and fail instead of erroring
  clearly. Pass an explicit Windows working directory or absolute paths
  rather than relying on the invoked process's own relative-path resolution.
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
- Version is tracked in `pyproject.toml`, `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, and the
  `version:` field of `SKILL.md` — keep them identical. `tests/test_plugin_contract.py` enforces this.

## GBrain (MCP server — persistent memory layer)

GBrain is wired as an MCP server for this project, reachable over HTTP (not
stdio) at `http://127.0.0.1:3131/mcp` with a per-agent bearer token.
It provides persistent knowledge-graph memory across sessions.

### Location & config
- Repo: `~/gbrain` (cloned from `github.com/garrytan/gbrain`)
- Brain: `~/.gbrain/brain.pglite` (local embedded Postgres, zero DB cost)
- Engine: PGLite
- Search mode: `conservative` (cheapest tier)
- Embeddings: `google:gemini-embedding-001`, 768 dims (requires
  `GOOGLE_GENERATIVE_AI_API_KEY` — get one at
  `https://aistudio.google.com/apikey`; this is a different credential from
  the Gemini CLI's OAuth-personal login and cannot be substituted for it)
- Chat/synthesis: `google:gemini-2.0-flash-exp` (chat), `google:gemini-2.0-flash`
  (query expansion)
- Cost: **$0.00/month** on free tier

### Running it — systemd user service, not an ad hoc background process
- Server process: `~/.config/systemd/user/gbrain.service` runs
  `gbrain serve --http --port 3131` with `Restart=on-failure`.
- `systemctl --user enable gbrain.service` is set, and
  `loginctl enable-linger sheke` is enabled, so the service survives both a
  closed terminal and a full logout — it starts on WSL boot, not just on
  login.
- To check it: `systemctl --user status gbrain.service` /
  `curl http://127.0.0.1:3131/health`.
- `gbrain reinit-pglite` (or any full reinit) wipes the auth-tokens table —
  every connected host's bearer token goes invalid at once and needs
  `gbrain auth create <name>` + `gbrain connect ... --install --force` again
  per host.
- MCP registration is **project-scoped per working directory**, not global —
  `gbrain connect --install` only updates the entry for whatever directory
  you ran it from. Re-run it from `content-ideas` specifically after any
  token rotation, or other projects silently keep the stale token.

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

### GBrain commands (via MCP or CLI)
```bash
gbrain search <query>        # keyword search (free)
gbrain query <question>      # hybrid search + synthesis (costs tokens)
gbrain get <slug>            # read a page (free)
gbrain put <slug>            # write/update a page (embedding cost)
gbrain list --type <T>       # list pages (free)
```

## Reference repos (cloned locally)

- `~/awesome-llm-apps/generative_ui_agents/` — 7 Generative UI agent demos
  (Google ADK + CopilotKit AG-UI). All deps installed. Each project has its
  own Python venv at `agent/.venv/` and Node deps in `node_modules/`.
  Requires `.env` with API keys (Gemini, Tavily, etc.) to run.
- `~/real-estate-dashboard-agent/` — forked from ai-dashboard-canvas-agent,
  customized for Summit Realty Group (DFW brokerage). Run with `npm run dev`.
  Pushed to `github.com/shekerkamma/real-estate-dashboard-agent`.
- `~/gbrain/` — GBrain knowledge brain. Bun runtime. 50 skills. MCP server.

## ADK + AG-UI (Generative UI) rules

- When building or forking any ADK agent that uses CopilotKit frontend tools
  (`useCopilotAction` — e.g. `add_chart`, `update_chart`, `delete_chart`),
  the agent's server-side `tools` list MUST include `AGUIToolset()` from
  `ag_ui_adk`. Without it, the AG-UI middleware cannot inject frontend tool
  definitions at runtime and ADK throws "Tool not found." Import:
  `from ag_ui_adk import ADKAgent, AGUIToolset`
- Frontend-side tools (registered via `useCopilotAction` in React) must NOT
  be duplicated as server-side `FunctionTool` stubs. They arrive via the
  `RunAgentInput.tools` payload and are injected as `ClientProxyTool` wrappers
  through the `AGUIToolset` → `ClientProxyToolset` substitution.
- Pipeline use cases can produce working demos as a Stage 7 artifact:
  pipeline use case → fork a generative UI demo from
  `~/awesome-llm-apps/generative_ui_agents/` → customize with domain-specific
  tools and instructions → ship as proof-of-concept. The RE dashboard is the
  first instance of this pattern.
- Gemini free tier rate limits: `gemini-3.5-flash` has 20 RPM, hits limits
  fast during interactive demos. Prefer `gemini-2.5-flash` for ADK agents.

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
