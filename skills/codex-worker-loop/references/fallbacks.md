# Fallbacks and Degraded Operation

Resolve role paths before planning. Never discover a missing binary or a wrong auth mode halfway through a promised wave.

## Worker fallback order

1. `codex exec` with the manifest's pinned model (default `gpt-5.6-sol`), authenticated via subscription login.
2. There is no step 2. Unlike a generic multi-agent skill, this one exists specifically to pair Claude with Codex/Sol — if `codex` is missing, or authenticated via API key instead of `codex login`, **stop and say so**. Do not silently fall back to having the orchestrator write the code itself; that's a different, simpler workflow the user didn't ask for. Offer it explicitly instead: "Codex isn't set up for subscription auth — want me to just build this directly instead of running the manager/worker loop?"

## Advisor fallback order

1. `claude -p` through `consult_advisor.py`, authenticated via this machine's subscription login.
2. Another explicitly user-approved independent Claude Code instance or profile, using the same consult template.
3. The orchestrator performs the critique itself, labeled `[DEGRADED: advisor]`, only after the user accepts the loss of independent review. Never silently skip the plan review or final taste pass — degrade it visibly instead.

## Dispatch failure handling

A nonzero exit, timeout, or empty output from `codex exec` is `FAILED_DISPATCH`, not a content `FIX`:

- Record the process evidence (exit code, stderr excerpt).
- Retry once only when the failure looks transient (e.g. a network blip) and budget allows it.
- If the subtask needs a capability the sandbox doesn't grant (e.g. it genuinely requires unrestricted network access), `ESCALATE` to the user rather than loosening the sandbox unilaterally.

## No API-key fallback, by design

This skill is subscription-first on purpose:

- The whole reason it exists is to avoid the per-token billing shown in the reference build's cost breakdown — `codex login` (ChatGPT subscription) for the worker, and this machine's own Claude Code login for both the orchestrator and the advisor.
- If either `codex` or `claude` is only available via an API key on this machine, that changes the cost model this skill was built to avoid — tell the user plainly rather than quietly proceeding on API billing.
- If an API-key path is ever genuinely needed (e.g. Sol isn't yet available on the user's ChatGPT plan tier), treat it as an explicit, separately-approved decision — not the default path this skill takes.
