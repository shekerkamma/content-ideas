# Goal Loop Orchestrator: Brainstorm / Discovery Notes
Date: 2026-06-30 · Goal: Review and finalize a Claude Code + Codex skill that refines goals, chains skills, loops execution, and verifies outputs.

## Structured context
- **Topic type**: process
- **Topic string**: Cross-agent meta-skill for goal refinement, skill chaining, compound skill execution loops, and verification.
- **Entities**: Claude Code, Codex, Vercel Labs skills CLI, find-skills, local repo skills.
- **Prospect/account**: n/a
- **Target buyer**: Agentic workflow builders, AI engineers, consultants, and power users managing repeatable skill-based workflows.
- **Verticals**: developer tooling, AI agents, workflow automation.
- **Open decisions**: final skill name; whether to create only the skill spec or implement repo-local skill files now; exact install/discovery policy for external skills.

## Summary / key decisions
- The skill should not be a simple "find skills" wrapper.
- The core primitive is the user goal.
- The workflow should refine the goal, define acceptance criteria, select a skill chain, execute looped passes, verify outputs, and stop only when done or blocked.
- "Find skills" becomes one internal step, not the product.
- The skill must work for both Claude Code and Codex by relying on shared `SKILL.md` conventions and host-aware paths.
- Grill-me review conclusion: the skill should be framed as a loop controller, not a catalog search tool. It must prevent three common failures: loading too many skills, chaining skills without handoff contracts, and marking work done before verification.

## Grill-me review
### Stress test 1 — vague user goals
- Risk: The agent jumps straight to tools before the outcome is clear.
- Decision: Always refine the goal into outcome, artifacts, constraints, acceptance criteria, verification, and stop conditions before selecting skills.

### Stress test 2 — too many skills
- Risk: The orchestrator loads every plausible skill and bloats context.
- Decision: Use progressive disclosure. Inventory metadata first, load only the next required skill body, and defer optional skills until the loop needs them.

### Stress test 3 — weak handoffs
- Risk: One skill's output is too vague for the next skill to use.
- Decision: Every skill pass must emit a handoff with inputs used, artifacts produced, decisions made, open flags, and next recommended action.

### Stress test 4 — premature completion
- Risk: The agent stops after generation instead of checking whether the goal is satisfied.
- Decision: Completion requires explicit acceptance criteria checks and available verification commands or review passes.

### Stress test 5 — host mismatch
- Risk: The skill assumes Claude Code-only paths or Codex-only tools.
- Decision: Write the core as host-neutral `SKILL.md` instructions. Use Claude Code `.claude/skills/`, Codex `.agents/skills/` / `~/.codex/skills/`, and repo-local `skills/` as discoverable roots.

### Stress test 6 — unsafe external installs
- Risk: The orchestrator installs unknown external skills just because search found them.
- Decision: Prefer local skills first. Search external skills only when local coverage is insufficient. Ask before installing. Score candidates by source reputation, install count, repo activity, local availability, and goal fit.

### Finalized direction
- Skill name: `goal-loop-orchestrator`.
- Role: refine goals, compose skill chains, execute iterative loops, verify results, and preserve reusable workflow recipes.
- Internal phases: goal contract, skill inventory, chain plan, loop execution, verification, handoff/write-back.

## Q&A log
### Q1 — Implementation approval
- Asked: Whether to proceed from finalized design into repo-local skill creation.
- Captured: User said "go ahead", meaning create the `goal-loop-orchestrator` skill now.
- Flags: external install/symlink into global Claude Code/Codex paths remains optional -> user

### Q2 — Loop termination
- Asked: Implied design review while implementing the skill.
- Captured: User emphasized that the orchestrator must not get into an infinite loop.
- Flags: add explicit loop budget, no-progress detection, and hard stop rules -> assistant

### Q3 — Research tooling standard
- Asked: Implied design review after testing the skill on real estate SaaS wedges.
- Captured: User said simple web search will not produce useful data moat. The skill should codify use/triggering of Reddit, Exa, Firecrawl CLI/tools and spawn subagents for deep research.
- Flags: make strategy research capability probing mandatory; simple web search only fallback; subagents required when available for deep strategy/moat work -> assistant

### Q4 — Grill-me refinement request
- Asked: User asked to use `grill-me` again to further refine the skill.
- Captured: Need stress-test the updated `goal-loop-orchestrator` beyond the current research policy and identify remaining design decisions before another patch.
- Flags: decide strictness level for subagents/deep-research requirements -> user

### Q5 — Strategy research strictness correction
- Asked: Whether deep Reddit/Exa/Firecrawl/subagent research should be mandatory for every strategy run or only validated moat/wedge outputs. Recommended answer was "only validated moat/wedge outputs."
- Captured: User rejected that recommendation: "the whole purpose of getting real data is lost." Decision: for strategy/moat/wedge/pipeline work, the default must be real-data research using available deep research routes. Lightweight/hypothesis mode is allowed only when tools are unavailable, blocked, or the user explicitly chooses a fast scan.
- Flags: patch `goal-loop-orchestrator` so strategy work must not default to lightweight scans -> assistant

### Q6 — Data synthesis and deck routing
- Asked: Codify that `ai-analyst` is always upstream for data synthesis, and slide-deck requests always use the client-ready PPTX skills.
- Captured: Decision: any data question, quantitative analysis, metrics, charts, synthesis from datasets, or validated finding should route through `ai-analyst` before downstream strategy/deck rendering. Any PowerPoint/slide deck/client deck request must route through `branded-pptx-deck` and its branded QA workflow, not ad hoc slides.
- Flags: patch `goal-loop-orchestrator` relationships and routing rules -> assistant

## Open flags (pending input)
- Decide whether to install/symlink into global Claude Code/Codex paths after repo-local skill is created -> user
