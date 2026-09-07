# Attribution

This portable cross-host skill is adapted from the Hermes `meta-loop` installation maintained for Sheker Kamma and from Shubham Saboo's Apache-2.0 `advisor-orchestrator-worker` skill:

`https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/agent_skills/advisor-orchestrator-worker`

Material changes in this port:

- Claude Code Opus replaces Hermes as the sole orchestrator and aggregator.
- Codex CLI replaces `agy`/Gemini as the worker runtime.
- Adapters use current `claude` and `codex exec` interfaces.
- The portable skill uses only standard-library Python at runtime.

Preserve this attribution and the Apache-2.0 provenance when redistributing or modifying the port.
