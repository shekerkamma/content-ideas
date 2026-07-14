OpenHands implementation source of truth for strategy/pipeline builds:
- https://github.com/OpenHands/OpenHands
- https://docs.openhands.dev/

GBrain knowledge rule:
- If `gbrain` is available as an MCP server in Claude Code, Codex, or another
  host, use it by default for cross-session memory and retrieval before
  repeating strategy or pipeline research from scratch.
- GBrain MCP topology is one shared HTTP server on
  `http://127.0.0.1:3131/mcp`. Codex reads the bearer from
  `MCP_GBRAIN_API_KEY`; Claude Code may use its existing HTTP Authorization
  header config.
  Hermes, Antigravity/Gemini, and OpenClaw should also remain HTTP clients
  using their existing token/header mechanisms.
  Do not switch Codex/Claude Code to direct stdio unless intentionally running
  single-client local mode; stdio opens PGLite directly and can conflict with
  the shared service.
- If Codex reports `MCP client for gbrain failed to start`, first run
  `scripts/gbrain-recover.sh --check`. If it reports stale PGLite locks and no
  live owner, run `scripts/gbrain-recover.sh --fix`, then restart Codex so it
  reloads MCP config.
- Treat `gbrain` as an explicit skill-chaining stage, not just a background
  preference:
  - `GBrain Recall` happens before `content-research`, strategy synthesis, or
    pipeline research begins
  - `GBrain Write-back` happens after the run when the findings are likely to
    matter again
- Use GBrain as the durable knowledge layer for recurring prospects,
  companies, people, verticals, themes, prior research, and named accounts.
- Treat GBrain retrieval as embedding-backed semantic retrieval by default, not
  just keyword lookup.
- Prefer semantic recall first; use synthesis only when the task needs merged
  interpretation rather than simple recall.
- Read from GBrain first when the task references a company, person, vertical,
  or use case that may have appeared in prior runs.
- Write durable findings back to GBrain after strategy/pipeline work when they
  are likely to matter again across sessions.
- When reporting pipeline status, call out `GBrain Recall` as completed if it
  was used to seed the run.
- GBrain is not the system of record for deliverables.
- Pipeline artifacts, briefs, decks, feed data, and client-facing outputs must
  still be written to local repo/run files.

Claude Code cost guardrails:
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

Research-plugin rule:
- Do not use simple/generic web search as the first discovery step for
  competitor analysis, strategy research, market maps, pipeline research, or
  current-company positioning work.
- In Codex Desktop or any host that exposes high-quality research plugins
  such as You.com or `exa`, prefer those plugins for source discovery and
  current web research during Stage 1 and strategy work.
- In terminal-first hosts such as Codex CLI, prefer the closest equivalent:
  an MCP-connected research server or a local CLI/API wrapper for tools such as
  You.com or Exa when available.
- Concrete terminal patterns to prefer when available:
  - repo-local `you-com-search` skill and `skills/you-com-search/scripts/search.py --level 1|2|3`
  - You.com MCP/API routes for search, livecrawl, research, and finance research
  - Exa MCP over HTTP/remote MCP
  - a local Exa API wrapper that calls `https://api.exa.ai/search`
- Use You.com before generic web search as a three-level search workflow.
  Prioritize Level 2 livecrawl evidence retrieval by default for competitor
  analysis, market maps, strategy research, and client-facing claims. Use
  Level 1 only for discovery seeding when the arena is unknown, and Level 3 for
  Research/Finance synthesis. Use Exa as the semantic/source-discovery
  specialist for official product pages, docs, GitHub repos, competitive
  signals, and current operator proof points.
- Generic WebSearch/web.run is allowed only after that discovery pass, and only
  for targeted verification, primary-source opening, citation checks, or when
  no research plugin/MCP/API route is available. If used as fallback, state the
  reason in the run notes.
- Codex Desktop plugin access is an advantage for discovery, not an exception
  to the repo workflow. The same delivery and verification rules still apply.
- This does not replace:
  - local file generation
  - branded PPTX build and QA
  - repo-specific workflow rules
  - verifying that final sources are primary and current

Playwright rule:
- Use the root `playwright.config.ts` and npm scripts for browser validation:
  - `npm run test:e2e` for all e2e specs
  - `npm run test:e2e:kyc` for the KYC workflow smoke test
  - `npm run test:e2e:headed` when a visible Chromium run is needed
- Use `playwright.demo.config.ts` for the shareable LLM Wiki Agent demo:
  - `npm run browser:test` for headless demo validation
  - `npm run browser:test:headed` for visible demo validation
  - `npm run browser:demo` for a manual local preview on port `8766`
- For the real LLM Wiki Agent ingest workflow:
  - `npm run llm-wiki:smoke` for deterministic PDF + URL fixture ingest
  - `npm run llm-wiki:live` for live Chromium URL/PDF download ingest
  - `npm run llm-wiki:live:headed` only when visible browser validation is
    explicitly requested
  - preserve live downloads under `raw/`, preserve PDFs under `raw/downloads/`,
    and log source URLs/hashes in generated wiki pages
- The Playwright config uses `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` when set,
  then falls back to cached Chromium under `~/.cache/ms-playwright` when
  present. If no browser is installed, or if Playwright's
  `chromium.executablePath()` resolves to a missing cache revision after a
  Playwright package upgrade, run `npm run test:e2e:install` and verify the
  resolved executable exists before continuing. In Codex sandboxed sessions,
  this install may require escalation because it writes outside the workspace
  to `~/.cache/ms-playwright`.
- Browser testing instructions for Codex and Claude Code are documented in
  `docs/browser-testing.md`.
- If `npm run build` was run while `npm run dev` was still active, restart the
  dev server before Playwright testing. A stale dev server can serve HTML that
  points to missing `.next` chunks such as `main-app.js`, preventing hydration.
- Keep generated `playwright-report/` and `test-results/` out of commits.

Client-facing PPTX rule:
- Always use the branded PowerPoint template resolved from
  `BRANDED_PPTX_TEMPLATE`, or fall back to
  `~/.claude/templates/branded-template.pptx` when that env var is unset
- Or use the `branded-pptx-deck` / `pptxkit` workflow that wraps that template
- Never ship a client-facing `.pptx` built from an ad hoc blank presentation
- Every slide must have structured content, not placeholder filler
- Use the branded detailed use-case realization layout when presenting a use case
- PPTX QA is mandatory before delivery
- Check text overlap/overflow/collisions before calling a deck final
- If branded preview tooling is unavailable, mark the deck unreviewed rather than silently delivering it
- Use explicit deck status: `draft`, `reviewed`, or `blocked`
- Use matching filename suffixes for deliverables
- Keep the branded builder script with the run artifacts so QA fixes are reproducible
- Copy reviewed decks only to a delivery destination resolved from
  `CLIENT_DELIVERY_DIR` when one is configured for the host

Cross-host product-build skills:
- Use repo-local skills from `skills/` for both Codex and Claude Code.
- Use `skills/aianalyst-competitor-analysis/SKILL.md` when competitor analysis
  must be treated as an AI Analyst evidence-dataset workflow: sourced claim
  ledger, dataset schema, metric definitions, data quality report, scoring
  model, confidence labels, quantitative datapoints, branded PPTX, interactive
  HTML, or GitHub Pages publication. Prefer this over the generic competitor
  pipeline when the user asks for deeper data points, KPIs, benchmarks,
  metrics-as-evidence, or AI Analyst involvement.
- Use `skills/competitor-analysis-pipeline/SKILL.md` when the user asks for
  competitor analysis, competitive landscape, battlecards, market maps,
  positioning comparisons, consulting-firm positioning comparisons, or
  client-ready competitor-analysis deliverables such as branded PPTX plus
  interactive HTML. This skill codifies the GBrain/source-order, grill-me,
  story-architect, GStack review, PPTX QA, HTML QA, and GitHub Pages publishing
  pipeline.
- Use `skills/plaid/SKILL.md` when the user says `PLAID`, `plaid build`,
  `plaid design`, `execute the roadmap`, `build the app`, asks to generate a
  PRD/product roadmap/design spec, or asks to continue a PLAID product build.
- Use `skills/karpathy-guidelines/SKILL.md` for coding, review, or refactoring
  work so assumptions are explicit, changes stay surgical, and success criteria
  are verifiable.
- Use `skills/llm-wiki-agent/SKILL.md` when the user asks to build, initialize,
  ingest into, query, or maintain an LLM wiki / second brain / markdown knowledge
  bundle. This skill implements the raw → wiki → index/log routing pattern for
  both Codex and Claude Code.
- For Codex `/goal` work, treat the existing PLAID artifacts as the build
  contract:
  - `vision.json`
  - `docs/product-idea.md`
  - `docs/validation-report.md`
  - `docs/product-vision.md`
  - `docs/prd.md`
  - `docs/product-roadmap.md`
  - `docs/design.md` when present
- Start `/goal` only after the relevant PLAID docs and roadmap scope are clear.
  Goals must name the phase/task scope, acceptance criteria, verification
  commands, constraints, and stop conditions.
- When `docs/product-roadmap.md` has unchecked tasks, route ambiguous build
  requests to PLAID Build and complete roadmap tasks in order. Mark tasks done
  only after implementation and verification.

@CLAUDE.md
