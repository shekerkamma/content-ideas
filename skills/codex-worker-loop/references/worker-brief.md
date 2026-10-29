# Worker Brief and Dispatch Manifest

Each dispatch is a fresh, stateless `codex exec` call. Sol sees only this brief — it cannot ask follow-up questions, see this conversation, or see another worker's output.

## Brief template

```text
You are worker <ID> completing ONE independent subtask in a larger build.
This brief is your entire context. You cannot ask follow-up questions or use
another worker's output.

SUBTASK: <one atomic goal>
IN SCOPE (files/paths you own and may write):
- <path or glob>
OUT OF SCOPE (do not touch):
- <path or glob>
INPUTS:
<all necessary text, reference URLs, file contents, or resolvable paths>

ACCEPTANCE CRITERIA — the result fails if any criterion fails:
1. [<ID>-C1] <checkable criterion>
2. [<ID>-C2] <checkable criterion>
3. [<ID>-C3] <checkable criterion>

Rules:
- Do only this subtask; do not expand scope into files outside IN SCOPE.
- Do not modify files another worker owns.
- Wire the piece together and run it yourself before returning — fix anything
  broken in your own scope rather than handing back something untested.
- State any assumptions you made instead of stopping to ask.
- If an input is missing or contradictory, begin your final message with
  `INPUT GAP: <one line>` rather than guessing silently.
- Return a brief summary of what you changed and why; the orchestrator reviews
  the actual diff, not your summary, so don't pad it.
```

## Redispatch addendum (FIX)

A `FIX` redispatch is the same brief with this block inserted before the rules:

```text
REDISPATCH AFTER FAILED VERIFICATION:
FAILED CRITERION: <ID and exact text>
OBSERVED FAILURE: <actual command output or diff excerpt>
REQUIRED CORRECTION: <specific corrected behavior>
Do not change portions that already passed unless required by this correction.
```

For a broader miss (the reference build's "you built a third of what I asked for"), don't hand-write a fresh brief from scratch — the orchestrator's own advisor-reviewed plan already has the missing features; regenerate the worker briefs from that plan, attach evidence of the gap (a diff against the reference, screenshots, or a feature checklist), and redispatch as a new wave.

## Manifest schema

Paths may be absolute or relative to the manifest file. Output paths must be unique. `repo_dir` is required — every worker's `codex exec` runs with `-C <cwd or repo_dir>`, i.e. it can write directly into your real project.

```json
{
  "model": "gpt-5.6-sol",
  "reasoning_effort": "max",
  "concurrency": 3,
  "timeout_seconds": 1800,
  "max_brief_bytes": 100000,
  "repo_dir": "/absolute/path/to/project",
  "workers": [
    {
      "id": "W1",
      "brief_file": "briefs/W1.txt",
      "output_file": "results/W1.txt",
      "cwd": "/absolute/path/to/project",
      "sandbox": "workspace-write"
    }
  ]
}
```

`cwd` and `sandbox` are optional per-worker overrides; they default to the manifest's `repo_dir` and `workspace-write` respectively. Use `sandbox: "read-only"` for a worker that should only investigate and report (e.g. "audit the auth module and list every place tenant IDs aren't checked") rather than write code.

Run `dispatch_workers_codex.py --manifest <file> --dry-run` before execution. A valid dry run proves schema, ID uniqueness, file readability, and budget/size limits — it does not prove Codex authentication or that `repo_dir` is a real git repo.

## Dispatch result

The helper writes one stderr file beside each output (`<output>.stderr`) and prints a JSON summary containing, per worker:

- `id`
- `status`: `PASS_DISPATCH`, `FAILED_DISPATCH`, or `TIMEOUT`
- `exit_code`
- `output_bytes`
- `elapsed_seconds`
- output and stderr paths

`PASS_DISPATCH` means the process returned nonempty output. It is **not** a content-verification PASS — that's Step 5 of the loop, done by the orchestrator against the real diff.
