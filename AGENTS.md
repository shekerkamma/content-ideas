OpenHands implementation source of truth for strategy/pipeline builds:
- https://github.com/OpenHands/OpenHands
- https://docs.openhands.dev/

Filesystem search and integrity rule:
- Do not limit searches to the current working directory when investigating
  missing, restored, corrupted, duplicated, or unavailable files and skills.
- Discover and search every relevant repository and installation root before
  drawing a conclusion. At minimum, check:
  - the full current repository, including hidden and ignored paths
  - repo-local `skills/`, `.claude/`, `.agents/`, and `plugins/` trees
  - user-level skill installations such as `~/.claude/skills/` and
    `~/.codex/skills/`
  - external or adjacent repositories referenced by repo instructions,
    symlinks, plugin manifests, or skill catalogs
- Resolve `~` and report the exact roots actually searched. Do not infer that
  restoring `/home/sheke/content-ideas` also restored an external installation
  such as `/home/sheke/.claude/skills/gstack`.
- For corruption claims, validate rather than relying on filenames or a prior
  report: inspect text/source files for invalid NUL bytes or parse failures,
  run Git integrity/status checks where applicable, and run the narrowest
  available validator or test. Exclude expected binary formats and Git object
  data from text-corruption counts.
- State the verified scope and evidence behind any file count. If permissions
  prevent checking a relevant external root, report the conclusion as partial
  instead of claiming the whole installation is healthy or corrupted.

Skill recovery, research, and porting contract:
- Keep portable skill sources in repo-local `skills/<skill>/`. Treat
  `~/.claude/skills/` and `~/.codex/skills/` as host installations, not the
  canonical or only recovery source.
- For `docx`, `pdf`, `improve`, and `storm-research`, the canonical portable
  copies are `skills/docx/`, `skills/pdf/`, `skills/improve/`, and
  `skills/storm-research/`. Preserve the complete skill directory, including
  licenses, references, templates, schemas, and scripts; exclude generated
  `__pycache__/` directories and `*.pyc` files.
- Separate detection from sourcing. Detect local corruption with byte-level,
  parse, Git, and skill-specific validation. Use web research, Exa, You.com,
  or Livecrawl Level 2 to locate authoritative recovery sources only; a web
  search cannot inspect or prove the integrity of a local filesystem.
- Prefer recovery sources in this order: a verified byte-identical local
  archive or known-good repo copy, the skill's authoritative upstream Git
  repository, then a freshly reconstructed file backed by documented evidence.
  Never replace a customized skill wholesale with a merely related upstream
  skill without validating that its interface and workflow match.
- Before replacement, stage and validate the candidate; retain a timestamped,
  recoverable backup of the installed directory; replace only the named skill;
  then compare installed files to the staged candidate and rerun validators.
- Research credentials are host-level secrets. Never copy API keys into this
  repository, a project `.env`, skill source, generated report, test fixture,
  commit, or chat output. On this WSL host, terminal research wrappers may read
  the Windows Hermes Desktop configuration through `/mnt/c` at runtime.
- Livecrawl Level 2 means search discovery followed by fresh-page extraction.
  Verify both stages and report their actual backend/status. Do not claim Level
  2 succeeded when only search results were returned or cached content was used.
- See `docs/skill-recovery-porting-contract.md` for the operational procedure
  and verification commands.

GBrain knowledge rule:
- If `gbrain` is available as an MCP server in Claude Code, Codex, or another
  host, use it by default for cross-session memory and retrieval before
  repeating strategy or pipeline research from scratch.
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

Research-plugin rule:
- In Codex Desktop or any host that exposes high-quality research plugins
  such as `exa`, prefer those plugins for source discovery and current web
  research during Stage 1 and strategy work.
- In terminal-first hosts such as Codex CLI, prefer the closest equivalent:
  an MCP-connected research server or a local CLI/API wrapper for tools such as
  Exa when available.
- Concrete terminal patterns to prefer when available:
  - Exa MCP over HTTP/remote MCP
  - a local Exa API wrapper that calls `https://api.exa.ai/search`
- Use them to improve discovery of official product pages, docs, GitHub repos,
  competitive signals, and current operator proof points.
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
- The Playwright config uses `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` when set,
  then falls back to cached Chromium under `~/.cache/ms-playwright` when
  present. If no browser is installed, run `npm run test:e2e:install`.
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

Presentation consolidation rule:
- Route presentation requests through repo-local `skills/present/`; do not add a new
  top-level presentation skill when an existing engine or support stage covers the job.
- Use `branded-pptx-deck` for native client-ready PPTX, `pptx-toolkit` for controlled
  existing-PPTX edits, `presentation` for HTML, `genspark-slides` plus
  `genspark-branded-deck` for hosted Genspark work, and `marp` for Markdown slides.
- For material builds, require `deck-brief.md`, `deck-design.json`,
  `template-profile.json`, `slide-plan.json`, and `visual-spec.json`; source-derived work
  also requires `presentation-evidence.json`.
- Keep template profiles and reusable slide archetypes in `pptx-design-quality`. Keep
  acquisition and normalization adapters in `presentation-source-bundle`.

Cross-host product-build skills:
- Use repo-local skills from `skills/` for both Codex and Claude Code.
- Use `skills/plaid/SKILL.md` when the user says `PLAID`, `plaid build`,
  `plaid design`, `execute the roadmap`, `build the app`, asks to generate a
  PRD/product roadmap/design spec, or asks to continue a PLAID product build.
- Use `skills/karpathy-guidelines/SKILL.md` for coding, review, or refactoring
  work so assumptions are explicit, changes stay surgical, and success criteria
  are verifiable.
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

Channel-to-KB skills:
- Use repo-local `skills/channel-to-kb-ytdlp/SKILL.md` (recommended default,
  free, no API key, most reliable against YouTube changes),
  `skills/channel-to-kb/SKILL.md` (free, no API key, can be IP-blocked on
  cloud hosts), or `skills/channel-to-kb-supadata/SKILL.md` (paid managed
  API via `SUPADATA_API_KEY`, no IP-blocking risk) when the user wants to
  turn a YouTube channel into an OKF (Open Knowledge Format) knowledge base
  or Karpathy-style LLM wiki — same on Codex and Claude Code.
- Each skill scaffolds its bundle under
  `$CONTENT_HOME/knowledge-bases/<channel-slug>/`, never the cwd, and ships
  its own copy of the shared OKF toolkit (`assets/okf-template/`,
  `references/pipeline-guide.md`). `uv run <skill-dir>/scripts/fetch_transcripts.py`
  installs each script's PEP 723 dependencies in an isolated environment —
  requires `uv` on PATH on whichever host runs it.
- Ported from `coleam00/cole-medin-knowledge-base`; see the "Channel-to-KB
  skills" section in `CLAUDE.md` for the re-sync procedure if upstream
  changes its shared OKF toolkit files.

@CLAUDE.md
