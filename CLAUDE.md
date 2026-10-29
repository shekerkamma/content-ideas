# content-ideas — shared workspace rules

This plugin produces a competitor/channel content feed and hosts reusable
cross-host skills. Start with `WORKSPACE_MAP.md`; read the referenced sections
only when their task applies. They retain the original detailed contracts.
Do not import reference copies in full at startup. Their paths/commands resolve
from the project root; historical imports describe the former bootstrap.

## Core project rules

- The content-feed application runtime stays dependency-free (Python stdlib).
  `skills/content-ideas/scripts/lib/__init__.py` remains a bare package marker.
  Existing specialized skill dependencies follow their own contracts.
- Persistent content state belongs under `$CONTENT_HOME` (default
  `~/Documents/Content`), not the cwd. Task deliverables belong in the applicable
  run folder. Host credentials stay outside committed sources.
- Preserve explicit provider/model/effort and host permission requirements.
  A catalog entry is not proof of routing; verify actual provider/status when
  testing a model route. Do not enable paid recurring work or increase GBrain
  search mode without existing explicit authorization.
- Use canonical `skills/<name>/`. Preserve portable bundles, licenses, templates,
  references and scripts. Installation paths are host copies; missing-file
  investigations include external installations and symlink targets.
- Keep cross-tree mirrors/adapters under their recorded contracts. Frontmatter
  normalization must update matching plugin copies too. Keep versions aligned
  in pyproject, plugin manifests and skill metadata.
- Apply [karpathy-guidelines](skills/karpathy-guidelines/SKILL.md) to coding/review/refactoring.
  Preserve existing changes; define success, make surgical edits, validate them.
  Route roadmaps/builds through [plaid](skills/plaid/SKILL.md); read existing PLAID
  artifacts and complete unchecked tasks in order. Start a goal only when the
  relevant scope, acceptance criteria and stop conditions are clear.
- Use a saved brief for sustained/resumed work; `docs/task-brief-template.md`.
  Compare lower reasoning on representative tasks before changing defaults;
  measure accepted results, retries, total time and usage. Keep requirements
  and essential tests fixed. Do not promise savings.

## Research and memory

- If `gbrain` is available, **GBrain Recall** precedes research/strategy/pipeline
  work. Read from GBrain first with embedding-backed semantic retrieval;
  write durable findings back through **GBrain Write-back** after useful runs.
  Keep deliverables in local files. Read GBrain's cost guardrails before use.
- Prefer `exa` plugins or a terminal MCP-connected research server / wrapper
  for `https://api.exa.ai/search`. Plugin research is not an exception path and
  does not replace local file generation, primary-source verification or QA.
- Ground OpenHands implementation in https://github.com/OpenHands/OpenHands
  and https://docs.openhands.dev/. Current source evidence outranks popularity.
- Graphify LLM-capable Bash blocks start with `eval "$(graphify-pro --env)"`.
  Use `extract_corpus_parallel(files, backend=os.environ["GRAPHIFY_PRO_BACKEND"],
  root=<corpus dir>)` on Claude Sonnet 5.5 through the Claude plan, never the
  billed Gemini key. Read the graphify route before execution.

## Gemini media lane (`gemini-api`, pilot)

- `gemini-api` v0.4.4 is pinned in `~/.local/bin` (WSL). It bills the paid
  `GEMINI_API_KEY`; Google AI Pro does not cover it. Do not upgrade unasked.
- Use it to call Gemini models, generate or edit media (image, tts, music,
  video), analyze files, transcribe, or launch managed agents.
- Inspect `--help` or `--usage` to choose a command, and `--schema` when building
  a `--body` JSON payload. Preview calls with `--dry-run`.
- For JSON or `--jq` on streaming/background commands (`generate`, `agent run`,
  `agent status`), pass `--stream=false --output-format json`.
- Capture the returned file paths and interaction IDs for multi-step tasks.
  Video and Deep Research cost real money: say the estimate before running.

## Presentations and delivery

- Route through `skills/present/`; use `branded-pptx-deck` for native client PPTX
  or the established engine for the requested format. Read the full presentation
  section and contracts before a build or edit.
- Use `BRANDED_PPTX_TEMPLATE`, falling back to
  `~/.claude/templates/branded-template.pptx`. Do not generate client-facing
  PPTX from a blank presentation. Missing branding blocks delivery.
- Every slide needs structured content; use the detailed branded realization
  layout for use cases. Material builds require deck-brief.md, deck-design.json,
  template-profile.json, slide-plan.json and visual-spec.json; source-derived
  builds also require presentation-evidence.json.
- PPTX QA is a delivery gate: save with validation, check overlap/overflow and
  collisions, inspect previews (no red overflow boxes), and fix defects.
  Without preview tooling, report unreviewed visual QA; do not call it final.
  Use `draft`, `reviewed` or `blocked` and matching filename suffixes; retain
  the builder. Copy only the reviewed deck to configured `CLIENT_DELIVERY_DIR`.
- Respect configured `SECOND_BRAIN_DIR` and `OBSIDIAN_VAULT_DIR` for optional
  exports. Do not invent a host-specific destination when they are unset.
- Open generated reports/web previews in the in-app browser by default. Serve
  only their dedicated preview directory. Keep specialized native editors,
  source artifacts and existing tabs; verify opening rather than assuming.

## Validation and routing

- Use existing relevant checks; the Python suite is `uv run --frozen pytest -q`.
  Do not install dependencies into system Python. For skill changes, follow the
  plugin contract and skill-builder audit/full-suite requirements in the mapped
  cross-host packaging section.
- Use root Playwright config/scripts for browser checks; restart a dev server
  after a concurrent build before testing. Exclude generated reports from commits.
- Read `docs/codex-wsl-skill-compatibility.md` once per session before Desktop
  priority skills. Resolve scripts/templates from the canonical bundle.
- `WORKSPACE_MAP.md` routes recovery, research, presentations, GBrain, channel
  ingestion, product builds, host/provider settings, media, UI and ADK work to
  complete references. Read them before the applicable action.

## Verifying your work

- Before reporting anything as done, fixed, passing or verified, run the real
  check and paste its output: the test suite, build, gate or rendered result.
  Read the exit code before piping into `tail` or `head`.
- A check counts only if it could have failed. Where you can, run it against
  the old input or code first. Watch for empty selectors, checks built from the
  artifact they test, gitignored files and silently ignored flags.
- Never edit a test or a Proof list to make it pass.
- For non-trivial claims, especially when this session wrote the check, ask the
  `verifier` subagent (`.claude/agents/verifier.md`) and include its VERDICT line.
  It runs the checks in a fresh context and never fixes anything.

<!-- claude-reflect: learned rules (saved from the band; edit freely) -->
## Learned rules
- Don't hand the user manual steps to repeat each time; automate the fix so it works without the user running commands.
<!-- end claude-reflect -->
