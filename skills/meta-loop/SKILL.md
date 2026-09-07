---
name: meta-loop
description: Use when a task benefits from independent multi-model analysis, a model council, or three or more parallel reasoning subtasks. Runs Claude Code Opus as the sole orchestrator and aggregator, dispatches isolated Codex CLI workers, verifies every result with PASS/FIX/ESCALATE evidence, and returns an auditable ledger. Do not use for one focused edit, ordinary brainstorming, model-selection advice, or test-runner parallelism.
---

# Meta LOOP

Run a bounded model team with fixed role ownership:

- **Aggregator:** Claude Code Opus frames the plan, reviews worker evidence, resolves conflicts, and produces the final synthesis.
- **Workers:** Codex CLI models execute independent, stateless briefs. Workers never coordinate or merge their own outputs.
- **Host agent:** prepares files, runs the checked-in adapters, performs deterministic checks, and applies only the aggregator-approved result.

Preserve these invariants across Codex CLI and Claude Code. Read `references/attribution.md` before materially changing the workflow.

## Capability gate

Resolve the skill directory from the `SKILL.md` path supplied by the host. Before promising a run, execute:

```bash
command -v claude && claude --version
command -v codex && codex --version
```

Require authenticated CLIs. Do not infer routability from a model catalog. If a real invocation fails, report the failing role and stop calling the run multi-model.

Defaults:

- Aggregator: `${META_LOOP_AGGREGATOR_MODEL:-opus}`
- Worker: the active Codex default unless `default_model` or a per-worker `model` is set in the manifest
- Worker concurrency: `min(3, subtask_count)`
- Worker dispatch cap: `min(20, max(subtask_count, 2 × subtask_count))`
- Aggregator calls: two mandatory calls, with a hard cap of five

Do not silently substitute the current host model for Claude Opus. Do not silently substitute non-Codex workers.

For routing and regression tests derived from the Codex capability video, use
`references/video-scenario-evals.json`. Preserve its evidence labels: only
`visible_text` may be described as on-screen text; reconstructed prompts remain
labeled `transcript_reconstruction` or `visual_only`.

## Workflow

### 1. Frame

State one deliverable, three to five testable success criteria, inputs, exclusions, worker dispatch cap, concurrency, and aggregator-call cap. Stop for one genuinely blocking fact; otherwise make bounded assumptions explicit.

### 2. Plan independent waves

Create stable worker IDs (`W1`, `W2`, …). Give each worker one atomic goal, complete inputs, explicit exclusions, an exact output schema, three to five acceptance criteria, a verification method, and non-overlapping artifact ownership. Use `references/worker-brief.md`.

Workers are output-only. They may return analysis, content, or a patch, but must not modify the user's project.

### 3. Mandatory Opus plan aggregation

Write the proposed plan to a file and run:

```bash
python3 "$SKILL_DIR/scripts/run_aggregator.py" \
  --stage plan \
  --input-file <absolute-plan-path> \
  --output-file <absolute-opus-plan-path> \
  --dry-run
python3 "$SKILL_DIR/scripts/run_aggregator.py" \
  --stage plan \
  --input-file <absolute-plan-path> \
  --output-file <absolute-opus-plan-path>
```

Require Opus to return `PROCEED`, `REVISE`, or `BLOCK`. Apply or explicitly rebut every note. Do not dispatch workers until the plan is accepted.

### 4. Dispatch one Codex wave

Write one brief per worker plus a JSON manifest. Validate before spending calls:

```bash
python3 "$SKILL_DIR/scripts/dispatch_codex_workers.py" \
  --manifest <absolute-manifest-path> --dry-run
python3 "$SKILL_DIR/scripts/dispatch_codex_workers.py" \
  --manifest <absolute-manifest-path>
```

The adapter uses argument arrays, stdin prompts, isolated temporary working directories, read-only Codex sandboxes, ephemeral sessions, bounded concurrency, timeouts, and separate output/log files. A successful process is only `PASS_DISPATCH`; it is not content acceptance.

### 5. Verify every worker

For each result, check every criterion against the real source or deliverable and record evidence. Assign exactly one verdict:

- `PASS`: every criterion has current evidence.
- `FIX`: one recoverable retry remains; quote the failed criterion and observed evidence in the new brief.
- `ESCALATE`: a second failure, unsafe access, missing input, contradiction, or exhausted budget requires aggregator or user judgment.

Never accept a worker's confidence as evidence. Never retry with a vague “improve it.”

### 6. Synthesize through Opus

Pass only verified worker results, the ledger, success criteria, and remaining risks to the aggregator:

```bash
python3 "$SKILL_DIR/scripts/run_aggregator.py" \
  --stage final \
  --input-file <absolute-synthesis-packet> \
  --output-file <absolute-final-output>
```

Require `SHIP`, `CONDITIONAL`, or `BLOCK`. Opus must cite worker IDs, resolve contradictions, and account for every success criterion. Apply the approved result serially, then run end-to-end verification against the integrated deliverable.

### 7. Finish with a ledger

Return the deliverable paths, models actually used, budget used versus cap, per-worker verdicts and evidence, Opus dispositions, integration checks, and unresolved risks. Follow `references/verification-ledger.md`.

## Security boundary

Read `references/security-boundaries.md` before dispatching sensitive or tool-dependent work. The adapters reduce leakage; they are not containers. Never include credentials or secrets in briefs. Do not dispatch production, payment, identity, credential, destructive, or externally mutating operations.

## Validation

After modifying the skill, run:

```bash
python3 "$SKILL_DIR/scripts/validate_skill.py"
python3 /path/to/skill-creator/scripts/quick_validate.py "$SKILL_DIR"
```

The implementation passes only when the manifests validate, both adapters resolve their CLIs in dry-run mode, and every installed/mirrored copy matches the canonical repo skill.
