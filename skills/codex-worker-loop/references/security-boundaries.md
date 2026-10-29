# Security Boundaries

This loop reduces context leakage and scope creep; it does not claim perfect isolation. `-s workspace-write` is Codex's own sandbox policy, not a formally verified container, and workers here write directly into the real repo by design — the isolation that matters is *scope* (non-overlapping paths, reviewed diffs), not a throwaway temp directory.

## Worker boundary

`dispatch_workers_codex.py`:

- invokes `codex exec` with an argument array, never a shell-interpolated command;
- pipes the brief on **stdin**, not as a CLI argument — keeps it off the OS process list and avoids argv length/quoting hazards;
- passes a narrow allowlist of environment variables (`PATH`, `HOME`, locale/tz vars, proxy vars) and explicitly omits anything matching `API_KEY`, `TOKEN`, `PASSWORD`, `SECRET`, `PRIVATE_KEY`, `CREDENTIAL` — Codex authenticates from `~/.codex/auth.json` (covered by `HOME`), not from an env var, so nothing sensitive needs to cross this boundary;
- captures stdout and stderr into separate files;
- enforces a per-worker timeout;
- rejects more than 20 workers, duplicate IDs/output paths, and oversized briefs.

Residual risk:

- `HOME` is available because the Codex CLI needs it for its own config/auth; a worker's shell commands can, in principle, read anything your user account can read on this machine, not just `repo_dir`.
- `-s workspace-write` restricts *filesystem* writes to the working directory and a few standard paths; it does not restrict network egress. A compromised or badly-instructed worker can still make outbound network calls.
- `codex exec` is non-interactive by design — there is no approval prompt to catch a command mid-flight. The brief's `IN SCOPE`/`OUT OF SCOPE` and the acceptance criteria are the only guardrail before the diff review.

Therefore:

1. Never put real secrets, credentials, or private keys in a worker brief — reference an env var name or a secrets-manager path instead, and only if the worker's own task genuinely needs to read it.
2. Keep `sandbox: "read-only"` for audit/investigation-only workers; reserve `workspace-write` for workers that are actually supposed to change files.
3. Do not dispatch a worker for destructive, production-deploy, payment, or credential-rotation operations — do those directly, with explicit user approval, outside this loop.
4. Review every diff before accepting a wave, even when the worker's own report claims success — this is the whole reason the orchestrator role exists.
5. If a task needs internet access you don't want Sol to have on this run, say so in the brief and instruct it not to make outbound calls beyond what's declared — Codex's sandbox does not enforce a network allowlist for you.

## Advisor boundary

`consult_advisor.py` runs `claude -p` from an empty temporary directory with:

- built-in tools disabled (`--tools ""`);
- an explicit empty MCP configuration plus `--strict-mcp-config`;
- slash commands (skills) disabled (`--disable-slash-commands`);
- session persistence disabled (`--no-session-persistence`);
- a timeout;
- the consult text supplied on stdin, not a command argument.

The helper intentionally does **not** use `--bare`: current Claude CLI behavior under `--bare` restricts Anthropic auth to `ANTHROPIC_API_KEY`/`apiKeyHelper` only, which would force per-token billing instead of this machine's subscription login. Leaving `--bare` off keeps normal OAuth/keychain auth while the model still receives only the consult material — no tools, no MCP, no memory of this or any other conversation.

## Data minimization check

Before every dispatch or consult, ask:

- Does this role need this exact input, or a smaller excerpt?
- Does the brief reveal another worker's unrelated material?
- Does a path in `IN SCOPE` grant broader access than the task requires?
- Would this brief being visible in a process list or a log file be acceptable?

If any answer is unsafe, narrow the brief or escalate to the user instead of dispatching.
