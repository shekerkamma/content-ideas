# content-ideas repo

This repo contains **three things**. Identify which one you are touching before
doing anything else:

1. **content-ideas plugin** — a cross-host skill that turns competitor activity
   into a daily "For You" feed of content ideas. Dependency-free Python
   (stdlib only) + one self-contained HTML renderer. Lives under
   `skills/content-ideas/`. This is the published, versioned artifact.
2. **DealForge app** — an AI pre-sales copilot (Next.js + Convex + Playwright)
   built with the BuilderOS pipeline. Lives under `app/`, `convex/`,
   `components/`, `lib/`, `middleware.ts`. Spec: `docs/prd.md`,
   `docs/product-roadmap.md`, `docs/product-vision.md`. Guide: `USER-GUIDE.md`.
   Test accounts: `docs/test-accounts.md`.
3. **Vendored skill library** — reusable skills in `skills/`,
   `.claude/skills/`, and `.agents/skills/`, wired up via
   `.claude/settings.json` (Claude Code) and `.codex-plugin/plugin.json`
   (Codex, via `"skills": "./skills/"`).

The plugin rules below (stdlib-only, no pip installs) apply **only to the
plugin**, not to DealForge or tooling scripts.

## Commands — what to run when

| You changed | Run |
| --- | --- |
| Plugin / pipeline Python (`skills/*/scripts`, `tests/`) | `python3 -m pytest -q` (stdlib + pytest, no network) |
| DealForge TS/TSX (`app/`, `convex/`, `components/`, `lib/`) | `npm run typecheck && npm run lint`, then `npm run test:e2e` (KYC flow only: `npm run test:e2e:kyc`) |
| LLM Wiki Agent demo | `npm run browser:test` (headless) / `npm run browser:test:headed` |
| Plugin manifests, `SKILL.md` frontmatter, **or this file / `AGENTS.md`** | `python3 -m pytest -q tests/test_plugin_contract.py` |
| Any `SKILL.md` across the vendored skill roots (structure, security, trigger collisions) | `python3 tools/skill_evals/run_all.py` (free, stdlib, no tokens — see below) |

**Contract-pinned prose:** `tests/test_plugin_contract.py` asserts pinned
phrases inside `CLAUDE.md` and `AGENTS.md` (GBrain, Exa, and PPTX-gate wording;
whitespace-insensitive, so re-wrapping lines is safe but paraphrasing is not).
After editing either file, run the contract test before committing.

**e2e port:** `npm run test:e2e*` starts its own dev server on port `3100`
(override with `E2E_PORT`), because port 3000 is owned by the repo's
`mcp_excalidraw` server on dev machines (`playwright.config.ts`).

```bash
# exercise the plugin directly against a checkout
# scrape.py has no --help: run with no args to print usage.
# First arg is a JSON object {platform: [handles]} or the `urls` subcommand;
# flags: --pillars, --since, --days. Needs SCRAPECREATORS_API_KEY.
python3 skills/content-ideas/scripts/scrape.py
python3 skills/content-ideas/scripts/generate_feed.py --help

# DealForge dev server
npm run dev
```

## Claude Code cost guardrails

- Do not use Fable as the default implementation model. Reserve Fable for
  architecture, planning, hard debugging, high-stakes review, and final
  merge-readiness checks where better reasoning is worth API-billed tokens.
- For routine implementation, bulk edits, scraping/research ingestion, simple
  Q&A, and long-running build loops, use a cheaper Sonnet-class default and
  escalate to Fable only for the planning/review stages.
- Keep MCPs lean. GBrain should stay because it is the durable memory layer;
  optional MCPs such as Excalidraw should be enabled only when actively needed.
- Use `.claudeignore` and enforced read-deny settings to avoid loading generated
  folders (`node_modules/`, `.next/`, `dist/`, `runs/`, reports, caches) into
  context. Treat large generated files and vendored workspaces as artifacts to
  inspect selectively, not background context.
- This repo already has its own memory hooks under `~/.claude/memory`; avoid
  duplicating paid background memory extraction when Claude Code API billing is
  active.

## content-ideas plugin

### Structure
- `skills/content-ideas/SKILL.md` — canonical skill definition (the entry point).
  Resolves its own directory from the Codex cache, the Claude plugin cache, or a
  repo checkout — see "Resolve the skill directory" near the top of `SKILL.md`.
  Keep that block in sync if directory names change.
- `skills/content-ideas/scripts/scrape.py` — competitor/own-channel scraper
- `skills/content-ideas/scripts/generate_feed.py` — builds the For You HTML feed
- `skills/content-ideas/scripts/pipeline_runner.py` — feed → strategy/deal-prep pipeline stages
- `skills/content-ideas/scripts/gbrain_tool.py` — GBrain recall/write-back helper
- `skills/content-ideas/scripts/lib/` — platform fetchers, scoring, relevance, rendering
- `skills/content-ideas/assets/for-you-template.html` — renderer template
- `skills/content-ideas/references/content-strategy.md` — idea-generation guidance
- `FILE-SCHEMAS.md` — schemas for every file the skill reads and produces

### Rules
- Runtime stays dependency-free: stdlib only (`urllib`, `json`, ...). No pip
  installs at runtime.
- `skills/content-ideas/scripts/lib/__init__.py` is a bare package marker — no
  eager imports.
- Persistent state lives under `$CONTENT_HOME` (default `~/Documents/Content`),
  never the cwd.
- Credentials live in `~/.config/content/.env` (`SCRAPECREATORS_API_KEY`,
  `SETUP_COMPLETE`).
- Version is tracked in **five places** and must stay identical:
  `pyproject.toml`, `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, and the
  `version:` field of `skills/content-ideas/SKILL.md`.
  `tests/test_plugin_contract.py` enforces this.

### Cross-host packaging
- `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` — Claude Code install
- `.codex-plugin/plugin.json` (`"skills": "./skills/"`) — Codex install.
  Verified 2026-07-13 (`codex debug prompt-input` from inside the repo):
  Codex actually discovers this repo's skills from **both** `skills/` (this
  manifest) **and** `.agents/skills/` (a separate root it scans on its own),
  merged into one list with no automatic dedup — confirmed by watching a
  same-name skill get listed twice from two different roots. A genuinely
  diverged (non-wrapper) same-name copy across those two roots is therefore
  a live Codex routing risk, not just a `skill_evals` hygiene finding — keep
  running the drift-checker (`tools/skill_evals/run_trigger_evals.py`).
  Also confirmed: Codex's parser tolerates Claude-Code-only frontmatter
  fields (`argument-hint`, `user_invocable`, `triggers:` lists) without
  error.
- `AGENTS.md` — Codex / generic-agent entry point. It carries its own copy of
  the GBrain and OpenHands rules **and then includes** `@CLAUDE.md` at the end.
  If you change those rules here, update `AGENTS.md` too (and vice versa).
- `commands/content-ideas.md` — `/content-ideas` slash command
- `commands/pipeline-runner.md` — `/pipeline-runner` slash command (feed use
  case → vertical-scorer → strategy brief → research → deal prep)
- `hooks/hooks.json` — SessionStart setup preflight (one-line hint, silent when
  ready; runs `hooks/scripts/check-setup.sh`)

## DealForge app

- Stack: Next.js (App Router) + Convex + Playwright e2e. Config:
  `next.config.ts`, `playwright.config.ts` (app e2e),
  `playwright.demo.config.ts` (LLM-wiki demo).
- Source of truth is the BuilderOS spec set: read `docs/prd.md`,
  `docs/product-roadmap.md`, `docs/product-vision.md` before changing product
  behavior. `USER-GUIDE.md` documents the end-to-end test flow.
- Follow the long-running build loop: execute roadmap tasks in order, one phase
  at a time; mark roadmap checkboxes complete only after implementation **and**
  verification; run build, lint, typecheck, and e2e before reporting a goal
  achieved.
- If `docs/design.md` exists, follow it for UI. Otherwise use the brand
  guidance in `docs/product-vision.md` and keep the UI restrained. A repo-root
  `DESIGN.md` (Google Stitch format) is the design-token source — read it
  before generating or restyling any UI (this is the fix for the "generic AI"
  look). Keep its tokens in sync with the `marp` `neon` theme `:root` block.
  Workflow + resources: `references/design-md-resources.md`.

## BuilderOS Build Pipeline (successor to PLAID)

BuilderOS skills (vendored into `.claude/skills/`, `skills/`, `.agents/skills/`)
give a repeatable idea → ship system. They chain via `docs/` handoffs, and
`spar-prd-goal` inserts a per-task `/goal` layer between planning and execution:

```
idea-generator → idea-validator → product-planner → design-system → build-mvp
   product-idea    validation       vision/prd/       design.md       (whole
      .md          -report.md       roadmap.md        design.html      roadmap)
                                        │
                                        ▼  [pick one roadmap task]
                                   spar-prd-goal → /goal → build-loop-{claude-code,codex,cursor}
                                   (verifiable PRD)         (build → review → test → fix, per task)
                                        │
                                        ▼  (product built)
                                   launch-checklist → docs/launch-checklist.md
```

Routing rules:
- **Whole MVP at once** → `build-mvp`. **One task, review-gated** →
  `spar-prd-goal` (spec a `/goal` target) then a `build-loop-*` matching the host.
- `spar-prd-goal` should pre-fill from `docs/prd.md` / `docs/product-roadmap.md`
  when they exist, rather than interviewing cold.
- **BuilderOS supersedes `plaid`.** Prefer BuilderOS skills for new work; `plaid`
  remains only for continuity on in-flight builds that already use its docs
  (`vision.json`).

Legacy PLAID builds: use PLAID docs as product source of truth and `/goal` as
the execution loop — same ordering/verification rules as DealForge above.

## Cross-Host Browser Testing (LLM Wiki Agent)

- `npm run browser:test` — headless Playwright validation of the demo;
  `:headed` variant when a visible Chromium run is needed.
- `npm run browser:demo` — serve the static demo on port `8766`. Note: the
  script path is pinned to `runs/2026-07-04-fable5-llm-wiki-pattern/` — update
  `package.json` if the run folder moves.
- `npm run llm-wiki:smoke` — deterministic PDF + URL wiki ingest.
- `npm run llm-wiki:live` / `llm-wiki:live:headed` — live Chromium ingest
  (headed only when the user explicitly wants to watch).
- For live ingests: preserve downloads under `raw/` (PDFs under
  `raw/downloads/`), add source URLs and hashes to generated pages, update
  `wiki/index.md`, append `wiki/log.md`.
- If a headed browser won't open, run headless or use VS Code Simple Browser.
- If Playwright resolves Chromium to a missing cache revision, run
  `npm run test:e2e:install` and verify `chromium.executablePath()` exists
  before continuing. This can happen after a Playwright package upgrade when an
  older browser cache is still present.
- Setup details: `docs/browser-testing.md`.

## Research tool order

- Do not use simple/generic web search as the first discovery step for
  competitor analysis, strategy research, market maps, pipeline research, or
  current-company positioning work.
- For client-ready competitor analysis, use
  `skills/competitor-analysis-pipeline/SKILL.md`; it codifies the improved
  GBrain/source-order, grill-me, story-architect, GStack review, branded PPTX
  QA, interactive HTML QA, and GitHub Pages publishing pipeline.
- Prefer the strongest research tool the host exposes: Exa MCP first, then an
  MCP-connected research server, then a local Exa API wrapper
  (`https://api.exa.ai/search`), then Firecrawl, then generic web search.
- Generic web search is allowed only after that discovery pass, and only for
  targeted verification, primary-source opening, citation checks, or when no
  research plugin/MCP/API route is available. If used as fallback, state the
  reason in the run notes.
- Plugin/desktop research access is a discovery advantage — not an exception path.
  It does not replace local file generation, branded PPTX build and QA,
  repo-specific workflow rules, or the requirement that final cited sources are
  primary and current.
- OpenHands implementation details must be grounded in the source of truth —
  repo `https://github.com/OpenHands/OpenHands`, docs
  `https://docs.openhands.dev/`. Prefer verified OpenHands primitives
  (skills/microagents, MCP integration, CLI/headless workflows, deployment
  models) over invented orchestration details.

## GBrain (MCP server — persistent memory layer)

GBrain (`gbrain serve`) provides persistent knowledge-graph memory across
sessions. **These rules are mirrored in `AGENTS.md` — keep both in sync.**

- Treat GBrain as an explicit chain stage, and say so in run status:
  **GBrain Recall** before `content-research`, strategy synthesis, or pipeline
  Stage 1 work; **GBrain Write-back** after the run. Read from GBrain first
  when the task references an entity or topic that may have appeared in prior
  work, and write durable findings back after the run when they are likely to
  matter again.
- GBrain is the durable layer for recurring companies, people, prospects,
  verticals, themes, named accounts, prior research. It is **not the system of
  record** for deliverables — briefs, feed data, decks, and client artifacts
  are written to local files in the repo or run folders.
- Retrieval is embedding-backed semantic retrieval by default, not just keyword
  lookup. Escalate to synthesis (`query`/`ask`) only when the task needs merged
  interpretation.

### Location & config
- Repo: `~/gbrain` · Brain: `~/.gbrain/brain.pglite` (PGLite, zero DB cost)
- Search mode: `conservative` · Embeddings: `google:gemini-embedding-001`
  (free tier) · Synthesis: `google:gemini-3.5-flash` (free tier) · $0.00/month

### Cost guardrails
- Do NOT change search mode to `balanced`/`tokenmax` without explicit user
  approval (2.5×–5× cost).
- Dream cycle / enrichment crons stay OFF without explicit user approval.
- Prefer `search` (free) over `query`/`ask` (costs tokens) for simple lookups.
- Writes fire embeddings automatically — batch writes where possible.

```bash
gbrain search <query>   # keyword search (free)
gbrain query <question> # hybrid search + synthesis (costs tokens)
gbrain get <slug>       # read a page (free)
gbrain put <slug>       # write/update a page (embedding cost)
gbrain list --type <T>  # list pages (free)
```

Where knowledge goes: GBrain pages for cross-session entities/topics; local
files (`$CONTENT_HOME/research/`) for run artifacts and deliverables; memory
files (`~/.claude/projects/.../memory/`) for behavioral guidance.

## Client-facing deck delivery gates

- Client-facing PowerPoint must use the branded template at
  `BRANDED_PPTX_TEMPLATE` (fallback `~/.claude/templates/branded-template.pptx`)
  or the `branded-pptx-deck` / `pptxkit` workflow that wraps it. Do not generate
  client-facing `.pptx` decks from ad hoc `python-pptx` layouts or blank
  presentations. If the branded template/workflow is unavailable, **stop and
  report the PPTX as blocked** — do not ship an unbranded substitute.
- Every client-facing slide needs structured content, not title + loose
  bullets: action title, supporting structure (cards/table/scorecard/use-case
  layout), and explicit evidence, implication, or next step. Use-case decks
  include at least one branded use-case realization slide (challenge, solution,
  how-it-works, stats, stack, systems, users, organizations).
- PPTX QA is a delivery gate, not optional polish:
  1. branded builder saves successfully with validation enabled
  2. slide text checked for overlap, overflow, collisions
  3. review `preview_pptx.py` contact sheets if available; additionally run the
     `officecli-qa` skill (`skills/officecli-qa/SKILL.md`) as the shared
     validate → issues → html → screenshot gate for `.pptx`/`.docx`/`.xlsx`
  4. if no preview tooling, say the deck is unreviewed for visual QA and do not
     present it as final
  5. fix any observed overlap before delivery
  6. state delivery status explicitly: `draft`, `reviewed`, or `blocked`, with
     matching filename suffixes (`*-draft.pptx`, `*-reviewed.pptx`,
     `*-blocked.txt`)
  7. keep the deck builder script in the run folder so QA fixes are reproducible
  8. only the reviewed deck is copied to the delivery path from
     `CLIENT_DELIVERY_DIR`
  9. minimum visual checklist: no red overflow boxes in `preview_pptx.py`, no
     title/subtitle collisions, no clipped text in stat bars/callouts/panels,
     footer/page number on every slide

## ADK + AG-UI (Generative UI) rules

- Any ADK agent using CopilotKit frontend tools (`useCopilotAction` — e.g.
  `add_chart`, `update_chart`, `delete_chart`) MUST include `AGUIToolset()`
  from `ag_ui_adk` in its server-side `tools` list, or ADK throws "Tool not
  found". Import: `from ag_ui_adk import ADKAgent, AGUIToolset`.
- Frontend tools must NOT be duplicated as server-side `FunctionTool` stubs —
  they arrive via `RunAgentInput.tools` and are injected as `ClientProxyTool`
  wrappers.
- Pipeline use cases can ship working demos as a Stage 7 artifact: fork a demo
  from `~/awesome-llm-apps/generative_ui_agents/`, customize tools and
  instructions, ship as proof-of-concept (the RE dashboard is the first
  instance).
- Gemini free tier: `gemini-3.5-flash` is 20 RPM and hits limits fast in
  interactive demos — prefer `gemini-2.5-flash` for ADK agents.
- CopilotKit theming leak: shadcn `:root` token remaps miss two surfaces —
  (1) `@copilotkit/react-ui` ships its own light theme; override its
  `--copilot-kit-*` CSS vars scoped to `[class*="copilotKit"]` with
  `!important`; (2) hardcoded utilities like `bg-white` on inputs/bubbles.
  Audit both, verify with a before/after screenshot (headless chromium → repo
  dir, not `/tmp`).

## Reference repos (cloned locally)

- `~/awesome-llm-apps/generative_ui_agents/` — 7 Generative UI agent demos
  (Google ADK + CopilotKit AG-UI). Deps installed; venv at `agent/.venv/`,
  Node deps in `node_modules/`. Needs `.env` API keys (Gemini, Tavily, ...).
- `~/real-estate-dashboard-agent/` — fork customized for Summit Realty Group.
  `npm run dev`. Pushed to `github.com/shekerkamma/real-estate-dashboard-agent`.
- `~/gbrain/` — GBrain knowledge brain. Bun runtime. MCP server.

## Portable path defaults

Use env vars, never machine-specific absolute paths, for anything that must
work across Codex, Claude, and terminal hosts:

- `BRANDED_PPTX_TEMPLATE` — branded `.pptx` template
  (fallback `~/.claude/templates/branded-template.pptx`)
- `CLIENT_DELIVERY_DIR` — optional copy-out location for reviewed decks
- `SECOND_BRAIN_DIR` — optional content-research export directory
- `OBSIDIAN_VAULT_DIR` — optional vault root for content-research notes

If an env var is unset, do not invent a substitute beyond the documented
fallback — report the step as blocked or skip the optional export.

## Project-local Claude Code skills

`.claude/settings.json` registers repo-local and external skill files.
Notable project-local skills beyond the BuilderOS set:

- `.claude/skills/claude-code-director/SKILL.md` — Director Framework
  (Plan First → Manage Context → Verify The Work → Build The System). Trigger:
  `/claude-code-director`, "director mode", "plan this properly".
- `.claude/skills/skill-builder/SKILL.md` — guided skill creation and audit
  (trigger `/skill-builder`; reference in `.claude/skills/skill-builder/reference.md`).
- `.claude/skills/founders-build-stack/`, `saas-replacement-auditor/`,
  `ai-feature-integrator/` — DataStaqAI product-build skills (documented in the
  user-global CLAUDE.md; executed inline, not via the Skill tool).
- `skills/officecli-qa/SKILL.md` — OfficeCLI QA gate for Office deliverables
  (see deck delivery gates above).

## Skill evals (tools/skill_evals/)

Free, stdlib-only, no-token hygiene checks across every `SKILL.md` in
`skills/`, `.claude/skills/`, `.agents/skills/`, and
`skill-framework/.agents/skills/`. Ported from
`Shubhamsaboo/awesome-llm-apps` (`agent_skills/evals/`, July 2026) and adapted
for this repo's multi-root, mirrored-copy layout (the same skill name in two
roots is a synced copy, not a rival — the trigger/routing checker dedupes by
name and instead flags description **drift** between copies).

```bash
python3 tools/skill_evals/run_all.py            # tiers 1, 1b, 2 together
python3 tools/skill_evals/skill_lint.py <dir>    # tier 1: structural lint only
python3 tools/skill_evals/skill_scanner.py <dir> # tier 1b: security scan only
python3 tools/skill_evals/run_trigger_evals.py   # tier 2: trigger/routing collisions + drift
```

- Tier 1 (structural) and 1b (security, OWASP Agentic Skills Top 10) run
  per skill directory. Tier 2 (trigger/routing) is lexical-only — it flags
  near-colliding descriptions and same-name copies whose description text has
  diverged across roots.
- Tier 3 (behavioral, via `evals.json`/`expectations[]`) is **not** ported —
  it costs tokens and is on demand only, not part of this free tier.
- This complements `skills-analyst` rather than duplicating it:
  `skills-analyst` mines usage and classifies keep/fix/merge/delete;
  `skill_evals` is the deterministic regression check that runs on every
  change, with no transcript mining and no tokens.
- Existing findings against the current corpus are a triage backlog, not a
  CI gate — `tests/test_skill_evals.py` unit-tests the tools themselves
  against synthetic fixtures and smoke-tests `run_all.py` against the real
  repo (asserts it runs cleanly, not that findings are zero).

### Already-triaged findings (2026-07-13) — don't re-litigate these

- **7 trigger/routing "collisions" reviewed, none need edits**:
  `build-loop-claude-code`/`-codex`/`-cursor` (87–95% overlap) are the same
  job across three hosts, selected by which host you're in, not by
  description text. `aeo-orchestrator` vs `aeo-gap-analyzer`/
  `aeo-query-planner` (53–60%) is the orchestrator naming its own
  sub-stages; real usage splits on argument shape (`config.json` for a full
  run vs. `run-id` to rerun one stage). `web-design-guidelines` vs
  `writing-guidelines` (53%) is two Vercel-authored templates sharing
  boilerplate sentence structure, not real vocabulary overlap.
  `branded-pptx-deck` vs `genspark-branded-deck` (52%) already
  cross-references itself in prose and has distinct slash commands.
- **2 security CRITICALs reviewed, both accepted as-is**: `officecli-qa`'s
  `curl \| bash` installer step (ClawHavoc-shaped, but it's your own
  OfficeCLI tool) and `exa-api`'s script reading `$HOME/.hermes/.env` then
  calling the Exa API in the same file (cred+net co-occurrence — expected
  for an API-key-based skill, correctly flagged for a human glance).
- **Remaining ~8 lint errors are cosmetic**, not bugs: doc mentions of
  scripts that live in another skill/repo without qualifying the path
  (`officecli-qa`→`recalc.py`, `branded-pptx-deck`→`build_yc_deck_v2.py` in
  the external `ticketforge` repo), an illustrative citation-format example
  in `code-reviewer` (`/abs/path/app.py:42`), and one markdown file
  (`content-research/SKILL.md`) with a nested same-length code fence the
  linter can't parse — none are unfilled placeholders or broken behavior.
- If a future run of `run_all.py` shows new findings beyond this list,
  those are real and worth triaging; don't assume everything is pre-cleared.
