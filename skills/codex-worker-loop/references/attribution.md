# Attribution

This skill is an adaptation of an external open-source skill, via an intermediate adaptation.

- **Original skill:** `advisor-orchestrator-worker`
- **Source file:** https://github.com/Shubhamsaboo/awesome-llm-apps/blob/main/agent_skills/advisor-orchestrator-worker/SKILL.md
- **Repository:** https://github.com/Shubhamsaboo/awesome-llm-apps
- **Author:** Shubham Saboo (`Shubhamsaboo`)
- **License:** Apache License 2.0
- **Intermediate adaptation:** a Hermes Agent adaptation of the same upstream skill (`meta-loop`), authored 2026-07-10, which recast the orchestrator role, added `agy`-based worker dispatch, and added the security/degraded-mode/budget discipline this file inherits.
- **This adaptation:** rebuilt 2026-08-03 for Claude Code (orchestrator + advisor) paired with the Codex CLI / GPT-5.6 Sol (worker), replacing the Gemini-CLI-specific (`agy`) worker dispatcher with a Codex-CLI-specific one, and replacing the Hermes-specific orchestration scaffolding with plain Claude Code skill conventions.

## Upstream ideas retained (from `advisor-orchestrator-worker`, via the Hermes adaptation)

- Advisor/orchestrator/worker role separation
- Self-contained stateless worker briefs
- Mandatory advisor review before dispatch and before shipping
- `PASS` / `FIX` / `ESCALATE` result handling
- Named redispatch after failed verification
- Commitment-boundary advisor escalation
- Hard worker/advisor call budgets
- Per-worker status and verification ledger
- Argument-array process execution, environment scrubbing, timeout handling, output separation, and manifest validation
- A tool-less advisor helper that avoids `--bare`/API-key-only auth modes so subscription login still works

## Material changes in this adaptation

- Orchestrator is a Claude Code session, not a Hermes session — no `delegate_task`, no Hermes MoA, no gstack-style preamble/telemetry scaffolding.
- Worker is `codex exec` running GPT-5.6 Sol, not `agy`/Gemini. The dispatch script's subprocess argv, sandbox flag (`-s workspace-write`), model/effort config (`-c model_reasoning_effort=...`), and working-directory handling (`-C <repo_dir>`) are all Codex-CLI-specific and were rewritten from scratch against the installed `codex exec --help` surface, not ported line-for-line from the `agy`-based script.
- Brief delivery moved from an argv flag (`agy -p <brief>`) to **stdin**, since Codex CLI supports reading the prompt from stdin and this removes a security note (`agy -p` has no prompt-file option) that no longer applies.
- Workers write **directly into the real target repository** under `workspace-write`, not into an isolated empty scratch directory that the orchestrator later merges from. This matches how a real Codex/Sol build actually needs to work (it has to run and wire together the code it writes) and shifts the safety invariant from "workers are output-only" to "every worker's diff is reviewed against its declared file scope before acceptance."
- Advisor default model changed to `claude-opus-5` (not `claude-fable-5`) — Opus 5 is priced at half of Fable 5 per token and is Anthropic's stated default for agentic-coding and enterprise-judgment work; this loop's plan-review and taste-pass consults are exactly that shape of task, so there is no capability reason to pay Fable-5 rates for either the orchestrator or the advisor role.
- Removed all Hermes-specific machinery (telemetry, question-tuning, checkpoint modes, `gstack-*` preamble scripts) since none of it applies outside that host.

## License compliance

The original work is licensed under Apache-2.0. This file and the SKILL.md identify this skill as a further adaptation. Canonical license text: https://www.apache.org/licenses/LICENSE-2.0.

## Upgrade path

Check the upstream revision with:

```bash
git ls-remote https://github.com/Shubhamsaboo/awesome-llm-apps.git HEAD
```

Review upstream changes through a keep/adapt/add lens rather than overwriting the Codex-specific and Claude-Code-specific rules in this adaptation.
