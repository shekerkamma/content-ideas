---
name: codex-worker-loop
description: 'Use when a build is too large for one model pass and benefits from a manager/engineer split: Claude Code plans, delegates, and reviews; GPT-5.6 Sol (via Codex CLI) writes code as one or more parallel workers; a second, independent Opus 5 instance critiques the plan before dispatch and the final draft before shipping. Use when the user asks to run a manager/worker build, pair Claude with Codex/Sol, fan a build out across parallel Sol workers, or wants a verified per-worker ledger. Do not use for a single focused edit, ordinary brainstorming, or CI/test-runner parallelism.'
license: Apache-2.0
metadata:
  tags:
  - multi-model
  - orchestration
  - advisor
  - workers
  - verification
  - codex
  - sol
  related_skills:
  - codex
  source: https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills/advisor-orchestrator-worker
  legacy-frontmatter:
    version: 0.1.0
    platforms:
    - linux
    - macos
    - windows
---

# Codex Worker Loop

## Overview

Run a bounded three-role loop:

- **Orchestrator — this Claude Code session:** frame the work, write worker briefs, dispatch, verify every result against real evidence, merge, and report. The orchestrator owns the hot path and is the only role allowed to accept results or make the final call on what ships. **Run this session on Opus 5** (`/model` → `claude-opus-5`) — it is the cost-effective default for agentic coding/planning/review work; do not use Fable 5 for this role (2x the cost per token for no benefit this loop needs).
- **Workers — GPT-5.6 Sol via the Codex CLI (`codex exec`):** stateless execution units. Every dispatch gets one complete, self-contained brief and writes directly into the target repository under a declared, non-overlapping set of files. Workers do not coordinate with each other or with the advisor.
- **Advisor — a separate, tool-less Claude Code process:** critic only. It reviews the plan before dispatch and the complete diff before shipping. It never executes, edits, or dispatches. **Also runs Opus 5** by default (`CODEX_LOOP_ADVISOR_MODEL`, default `claude-opus-5`) — independent judgment doesn't require the priciest model, and using Fable 5 here would double the cost of every plan review and taste pass for no measurable gain on this task shape.

The durable product is not the model combination. It is the invariant: complete briefs, independently reviewed diffs, real verification, named retries, bounded judgment, and an auditable ledger.

This is an adaptation of Shubham Saboo's Apache-2.0 `advisor-orchestrator-worker` skill (via an intermediate Hermes-agent adaptation), rebuilt for Claude Code as orchestrator/advisor and Codex CLI / GPT-5.6 Sol as the worker pool, since neither host ships that pairing natively. Read `references/attribution.md` for full provenance.

## When to Use

Use this skill when at least one is true:

- The build naturally splits into three or more independent, file-scoped subtasks (auth, a service module, a UI surface, a scoring engine, ...).
- The user explicitly asks to pair Claude with Codex/Sol, run a manager/worker build, or fan work out across parallel Sol workers.
- Silent partial failure (a worker that "looks done" but missed the spec) would be costly enough to justify per-worker verification and an independent plan/taste review.

Do **not** use it for:

- One focused bug, one file, or a task this session can finish and verify directly.
- Brainstorming that needs variety but not independent verification.
- CI, pytest, or infrastructure parallelism.
- Sequential subtasks where each worker needs another worker's unpublished output — split into waves instead.
- Destructive, production, or credential-bearing operations without explicit user approval.

## Non-Negotiable Invariants

1. **Self-contained briefs.** A worker sees only its brief (`references/worker-brief.md`). Paste every required input; never say "use the context above."
2. **Non-overlapping file ownership.** Each worker's brief declares an explicit `IN SCOPE` file/path list and an explicit `OUT OF SCOPE` list. No two concurrently-dispatched workers may own overlapping paths.
3. **Direct writes, orchestrator-reviewed.** Unlike a stricter output-only pattern, workers here write straight into the real repo under `-s workspace-write` (that's the point — this is a build tool, not a text generator) — but every write is reviewed against `git diff` before the wave is accepted. Nothing is "done" until the orchestrator has looked at the actual diff.
4. **Real checks.** Exercise the actual deliverable: run the build, the test suite, the linter, or click through the feature. A worker's own confidence, a clean process exit, or "the file exists" is not verification.
5. **One verdict per dispatch.** Every worker result is `PASS`, `FIX`, or `ESCALATE` against its own acceptance criteria.
6. **Named retry.** A `FIX` redispatch quotes the failed criterion and the observed evidence. Never ask a worker to "improve it" with no specifics.
7. **No substantive hand-patching.** Redispatch a failed result to Sol. The orchestrator may make only mechanical merge/conflict-resolution edits after acceptance.
8. **Apply or rebut every advisor note.** Never silently drop advice.
9. **Hard budgets.** Retries and extra dispatches count against the cap. Crossing it requires a user decision.
10. **Evidence ledger.** No ship decision without per-worker verification evidence, recorded in `templates/run-ledger.md`.

## Role Resolution

Resolve capabilities before promising a run:

```bash
command -v codex >/dev/null && codex --version
command -v claude >/dev/null && claude --version
```

| Role | Primary | Default model | Auth |
|---|---|---|---|
| Orchestrator | This Claude Code session | `claude-opus-5` (set via `/model` before starting) | Whatever this session already uses |
| Worker | `codex exec` | `${CODEX_LOOP_WORKER_MODEL:-gpt-5.6-sol}` | Codex CLI subscription login (`codex login`, **not** `--with-api-key`) — check `~/.codex/auth.json` has `"auth_mode": "chatgpt"` before starting; if it doesn't, stop and tell the user to run `codex login` interactively first |
| Advisor | Separate `claude -p` process | `${CODEX_LOOP_ADVISOR_MODEL:-claude-opus-5}` | This machine's `claude` CLI login (subscription — the helper never uses `--bare`, which would force API-key auth) |

### Degraded modes

- **No `codex`:** stop. There is no worker substitute for a real Codex/Sol pairing — the entire point of this skill is that pairing. Offer ordinary single-model work instead.
- **`codex` present but `auth_mode` is not `chatgpt`:** stop and tell the user to run `codex login` (interactive OAuth) rather than `codex login --with-api-key`. Proceeding on an API key silently switches from subscription billing to per-token billing, which is the exact thing this skill exists to avoid.
- **No `claude` binary for the advisor:** the orchestrator may fill the advisor role itself, labeled `[DEGRADED: advisor]`, once the user accepts the loss of independent review. Never silently skip the plan review or final taste pass.

## Budget Contract

State this beside the success criteria before the first advisor call:

- `worker_dispatch_cap = min(20, max(subtask_count, 2 × subtask_count))`
- `worker_concurrency = min(3, subtask_count)` by default — raise only after checking Codex's own throughput and the host's CPU/IO headroom
- `advisor_consult_cap = 5`
- Two advisor calls are mandatory on a normal run: plan review and final taste pass.
- Up to three extra advisor calls are allowed only at the commitment boundaries in Step 6.

## The Loop

### 1. Frame

State, in the conversation, before writing any brief:

- One concrete deliverable (e.g. "a deployed AI sales-roleplay trainer at `<url>`")
- Three to five checkable success criteria
- The reference product / spec, if one exists, and what must NOT be copied from it (name, branding, wording)
- Worker dispatch, concurrency, and advisor budgets (Budget Contract above)
- Repo root the workers will operate in

If the goal cannot be framed without one missing fact, ask one focused question and stop.

### 2. Plan Independent Waves

Create subtasks with stable IDs (`W1`, `W2`, ...). For each, using `references/worker-brief.md`:

- One atomic goal
- Complete inputs (paste them — a worker cannot see this conversation)
- Explicit `IN SCOPE` / `OUT OF SCOPE` file paths
- Three to five acceptance criteria
- The exact verification command/check the orchestrator will run against the real repo
- Wave number (a later wave when a subtask needs an earlier one's accepted output)

Completion criterion: no two same-wave workers own overlapping paths, and no worker needs another worker's unpublished output.

### 3. Advisor Plan Review — Mandatory Consult 1

Write a consult file using `references/advisor-consult.md`, then run:

```bash
python3 "${SKILL_DIR}/scripts/consult_advisor.py" \
  --consult-file <absolute-consult-path> \
  --output-file <absolute-advisor-output-path>
```

(`SKILL_DIR` is the directory containing this SKILL.md — resolve it the same way the `watch`/`codex` skills do, from where you `Read` this file.)

Read the actual advisor output. For every note, record `APPLY` or `REBUT` with a reason in the run ledger, then revise the plan. Do not dispatch before this is done.

### 4. Dispatch One Wave

Write one brief file per subtask and one JSON manifest (schema in `references/worker-brief.md`). Validate without spending a call:

```bash
python3 "${SKILL_DIR}/scripts/dispatch_workers_codex.py" \
  --manifest <absolute-manifest-path> --dry-run
```

Then execute:

```bash
python3 "${SKILL_DIR}/scripts/dispatch_workers_codex.py" \
  --manifest <absolute-manifest-path>
```

Each worker runs as `codex exec -s workspace-write -m <model> -c model_reasoning_effort=<effort> -C <repo_dir> -` with its brief piped on stdin (never as a raw CLI argument — keeps the brief off the process list and off any shell-quoting hazard). The helper scrubs the environment to a safe allowlist (no stray API keys get forwarded), enforces a per-worker timeout, captures stdout/stderr separately, and never retries automatically — retry is your judgment call and spends budget.

Completion criterion: every dispatched ID has a nonempty output or an explicit failed-dispatch record.

### 5. Verify Every Result

For each worker, per `references/verification-ledger.md`:

1. Run `git diff` (or `git status` + targeted diffs) scoped to that worker's declared paths.
2. Check every acceptance criterion independently against that diff and against the running application (build it, run the tests, click the feature).
3. Capture concrete evidence — command + exit code + relevant output, not a paraphrase.
4. Assign `PASS`, `FIX` (redispatch once with the named failure), or `ESCALATE` (second failure, missing input, unsafe access, or budget exhaustion).

Never accept "mostly correct." A worker that built 1 of 3 requested features failed verification — send it back with the gap itemized, exactly like the video's round-two correction (two blunt notes + two screenshots of the reference beat a rewritten prompt).

### 6. Escalate Only at Commitment Boundaries

Two escalation paths exist at a commitment boundary — they are complementary, not exclusive, and neither is optional to skip past silently:

- **Ask the user directly — zero budget cost, and the one actually demonstrated end-to-end in the reference build.** When the delivered result falls short of the spec, the reference build's fix wasn't a second AI opinion — it was the human sending two blunt messages and two screenshots straight to the manager. You have that same channel open in every turn of this conversation. Use it whenever the user is present and the judgment call is theirs to make (does this match what they wanted, is a scope cut acceptable, is a caveat OK to ship with) — it's faster and it's the call only they can make.
- **An extra advisor call** (counts against `advisor_consult_cap`) when independent, tool-less critique is what's actually needed rather than the user's preference — e.g. cross-checking a plan or diff for issues neither you nor the user would necessarily think to look for.

Reach for one of these when:

- Two accepted-looking results contradict each other.
- One subtask fails verification twice.
- A judgment call falls outside the framed success criteria.
- The plan needs a structural rewrite (e.g. the first wave delivered a third of the spec, as in the reference build — that's exactly when the reference build's manager got a human correction, not an AI one).

### 7. Synthesize

The orchestrator owns the final integration. After all waves in scope are accepted, re-run the *original* end-to-end success criteria against the live result — individually-accepted worker diffs can still fail to compose.

### 8. Advisor Taste Pass — Mandatory Consult 2

Send the advisor the full diff/summary, the original success criteria, and the verification evidence. Ask for `SHIP`, `CONDITIONAL`, or `BLOCK`. Apply or rebut every note, then re-run any affected checks.

### 9. Finish

Fill in `templates/run-ledger.md` and report:

1. Deliverable / live URL / artifact paths
2. Success-criteria verdicts
3. Per-worker ledger (dispatch count, verdict, evidence)
4. Advisor notes applied/rebutted, both consults
5. Budget used vs. cap
6. Remaining risks and gaps — state them plainly, the way the reference build's "five honest caveats" did, rather than declaring silent victory

## Common Pitfalls

1. **Calling the dispatch cap "parallelism."** Report budget and concurrency separately.
2. **Passing the whole conversation to a worker.** Include only what that one subtask needs.
3. **Treating `workspace-write` as a sandbox against a hostile worker.** It's a safety net against mistakes, not a security boundary — see `references/security-boundaries.md`.
4. **Skipping the plan review because "the brief is obviously right."** The reference build's own manager caught two critical cross-tenant security holes at exactly this stage, before anything shipped.
5. **Verifying with a solo model.** A worker's self-report that it verified something is not verification — see `references/verification-ledger.md`.
6. **Using Fable 5 for orchestrator or advisor.** It's 2x the per-token cost of Opus 5 with no capability this loop's planning/review work needs; reserve it (if ever) for problems Opus 5 has actually failed on.
7. **Forgetting the auth-mode check.** If `codex`'s `auth.json` shows API-key auth instead of `chatgpt`, every worker dispatch bills per-token instead of drawing on the subscription — check this before the first dispatch, not after the bill.

## Verification Checklist

- [ ] `/model` confirmed `claude-opus-5` for this orchestrator session
- [ ] `codex --version` succeeds and `~/.codex/auth.json` shows `"auth_mode": "chatgpt"`
- [ ] `claude --version` succeeds (or `[DEGRADED: advisor]` accepted by the user)
- [ ] Deliverable and 3-5 success criteria stated before dispatch
- [ ] Budget and concurrency stated separately
- [ ] Mandatory plan-review consult completed and dispositioned
- [ ] Every brief has non-overlapping `IN SCOPE` paths
- [ ] Every worker result has PASS/FIX/ESCALATE plus a real command + evidence
- [ ] Retries name the exact failed criterion
- [ ] Integrated deliverable re-verified end to end
- [ ] Mandatory final taste-pass consult completed and dispositioned
- [ ] Final ledger reports dispatches, retries, paths, and remaining risks
