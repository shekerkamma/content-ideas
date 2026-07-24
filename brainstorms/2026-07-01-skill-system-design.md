# Skill System Design: Brainstorm / Discovery Notes
Date: 2026-07-01 · Goal: Define how the role prompts and Hermes skills should combine into one system for your build workflow.

## Structured context
- **Topic type**: strategy
- **Topic string**: skill system for turning role prompts into a governed build workflow
- **Entities**: Hermes, Claude, role prompts, build workflow
- **Prospect/account**: n/a
- **Target buyer**: enterprise solution architect / internal build operator
- **Verticals**: automotive, enterprise software, manufacturing
- **Open decisions**: system shape, routing logic, shared resources, memory model, output artifacts

## Summary / key decisions
- Need to figure out how the nine role prompts should become a working system, not isolated prompts.
- Likely candidates are a dispatcher/router skill, role-specific skills, shared resources, and a persistence layer.
- Original product thesis: an AI Head of Engineering for founders shipping their first custom app/MVP/internal tool.
- The system replaces roughly a `200K-300K/year` full-time head of engineering plus about 3 months of onboarding before meaningful output.
- Core value proposition: provide the planning layer for free, before code is written.
- The nine roles cover the monthly planning work a senior engineering leader would normally handle:
  - cut scope
  - spec the 30-day build
  - choose stack
  - decide build vs buy
  - estimate cost/time
  - validate AI fit
  - design the internal tool
  - pre-launch audit
  - roadmap with rollback plan
- System shape decision: use a **hybrid**.
  - One top-level orchestrator routes the planning sequence and enforces dependencies.
  - Each role also exists as a standalone skill so it can be run directly when only one step is needed.
  - This preserves reuse, avoids dead-end prompts, and keeps the system usable outside the full sequence.
- Output contract decision: produce **both**.
  - A consolidated master plan/index for the full run.
  - One role-specific markdown file per role so each step can be reused, audited, and rerun independently.
- Constraint priority decision:
  1. Governance and correctness
  2. Reuse across hosts and future runs
  3. Automation convenience
- Host strategy decision: make the system cross-host by default, with Hermes as the execution target and Claude/Codex-compatible prompt text as the portable layer.
- Memory strategy decision: store durable patterns in GBrain and workspace files; keep the orchestrator state in markdown, not just chat.
- Routing strategy decision: every role consumes the previous role’s output file and produces the next artifact, so the chain is explicit and inspectable.

## Q&A log

## Open flags (pending input)
- none
