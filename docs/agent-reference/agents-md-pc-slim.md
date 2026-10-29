# content-ideas — agent entrypoint

@CLAUDE.md

Read `WORKSPACE_MAP.md` before broad discovery, then only the relevant workflow
sections and canonical skill bundles. Detailed rules remain binding for their
applicable tasks. Reference copies preserve the former entrypoints; their legacy
import lines are historical, not instructions to recursively load both files.
Resolve paths and commands in those copies from the repository root.

## Efficient execution

- Complete the authorized scope and essential validation. Preserve explicit
  provider, model, effort, quality, output and permission requirements.
- Start with supplied paths; use `rg` before reading large files. Reuse findings
  and unchanged content. Do not run unrelated audits or rebuild indexes.
- Load only applicable skills and references. Keep specialist tooling and QA;
  remove redundant context only when its absence has been evaluated.
- For sustained or resumed work, use `docs/task-brief-template.md` in the run
  directory. Reuse an existing approved plan; read only the current task and
  its dependencies, not the entire backlog.
- Ask about consequential blind spots during planning/review, then execute
  against explicit acceptance criteria. Stop verification when required gates
  pass unless a change, failure or unresolved risk warrants more checks.
- Delegate only when authorized and useful. Preserve existing user edits.
  Report results, evidence, limits and next steps concisely.

## Research and durable knowledge

- When `gbrain` is available, use **GBrain Recall** before strategy/pipeline
  research. Read from GBrain first using embedding-backed semantic retrieval;
  use synthesis only when merged interpretation is needed.
- Write durable findings back to GBrain through **GBrain Write-back** after
  reusable research. GBrain is not the system of record for deliverables;
  write briefs, decks, reports and feed data to local repo/run files.
- Prefer exposed `exa` research plugins, or a MCP-connected research server
  / terminal wrapper for `https://api.exa.ai/search`. Plugin access is
  not an exception to the workflow and does not replace local generation or artifact QA.
  Verify primary, current sources. Level 2 requires fresh discovery and extraction.
- OpenHands implementation source of truth:
  https://github.com/OpenHands/OpenHands and https://docs.openhands.dev/.
- Follow the research, recovery and provider sections linked from the map.

## Output and host boundaries

- Use canonical repo `skills/<name>/` bundles. Preserve secrets in host storage;
  never copy keys into project files, reports, fixtures, commits or chat output.
- Client-facing PPTX requires `BRANDED_PPTX_TEMPLATE` or its documented fallback,
  mandatory QA and explicit `draft`, `reviewed` or `blocked` status. Copy reviewed
  decks only to configured `CLIENT_DELIVERY_DIR`. Follow the presentation route.
- Open generated reports/previews in the in-app browser by default. Serve only
  a dedicated preview directory; keep the canonical source. Reuse tabs and treat
  queued opening as pending. Specialized native editors retain their requirements.
- Skill/installation investigations must include relevant external roots and
  symlink targets, not just this repo; report exact scope and verification limits.
- Before a Desktop priority workflow, read `docs/codex-wsl-skill-compatibility.md`
  once per session. Follow `docs/codex-capability-routing.md` for tool selection.
  Discovery, authentication and successful execution are separate checks.

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
