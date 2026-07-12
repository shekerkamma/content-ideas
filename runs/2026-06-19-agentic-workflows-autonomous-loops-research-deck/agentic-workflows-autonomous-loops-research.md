# Agentic Workflows: From Chains to Autonomous Loops

## Executive Summary

The AI industry is undergoing a structural transition in how automation is designed. Early agentic systems used linear prompt chains — fixed sequences of LLM calls where each step feeds the next. Modern agentic workflows have evolved toward autonomous loops: systems where agents perceive state, plan actions, execute tool calls, observe results, and iterate — without human involvement at each step. This shift unlocks dramatically higher automation density but introduces new challenges around reliability, observability, and trust calibration.

## Key Findings

### 1. The Chain-to-Loop Transition

Prompt chains (popularized by LangChain in 2022–2023) are deterministic pipelines: input → step A → step B → output. They are predictable but brittle — a single failed step breaks the chain. Autonomous loops (ReAct, Plan-and-Execute, LATS, and OpenHands-style event loops) introduce a feedback cycle: the agent evaluates its own output and decides whether to continue, retry, or branch. This makes them robust but harder to audit.

**Chain characteristics:**
- Deterministic step order
- No self-correction
- Easy to debug (linear trace)
- Low ceiling: can only do what the designer anticipated

**Loop characteristics:**
- Dynamic step selection
- Self-correction via tool feedback
- Non-linear execution traces
- High ceiling: can handle unanticipated sub-problems

### 2. The Four Core Loop Patterns

Practitioners have converged on four reusable loop patterns:

**a) ReAct Loop** (Reason + Act): The agent alternates between producing a reasoning trace and calling a tool. Used by most LLM agents today. Introduced by Yao et al. (2022). Works well for retrieval-augmented tasks.

**b) Plan-and-Execute**: The agent first produces a multi-step plan, then executes each step in sequence with an executor sub-agent. Better for long-horizon tasks (>10 steps) where upfront planning reduces wasted tool calls.

**c) Reflection Loop**: After each execution cycle, a critic agent evaluates the output and flags errors. The main agent then revises. Used in frameworks like Reflexion (Shinn et al., 2023) and GPT-Researcher.

**d) Multi-Agent Orchestration**: Multiple specialized agents run in parallel or in sequence, each owning a domain (research, writing, coding, QA). An orchestrator routes tasks. Used by AutoGPT, OpenHands multi-agent mode, and CIOS architecture.

### 3. Tool Calling as the Foundation

Autonomous loops are only as capable as the tools available to them. Tool calling has become the central primitive: agents invoke typed functions (search, read_file, write_file, run_code, etc.) and receive structured results. MCP (Model Context Protocol, Anthropic 2024) standardizes tool definitions across providers. OpenHands implements this as a CodeActAgent — agents produce bash/Python actions that a sandboxed runtime executes, returning stdout/stderr as observations.

Key insight: **the tool surface defines the agent's action space**. An agent with only `search` and `summarize` tools can only retrieve and compress. An agent with `read_file`, `write_file`, `run_tests`, `git_commit` can autonomously develop software.

### 4. Reliability in Autonomous Loops

The primary failure mode of autonomous loops is **runaway behavior**: the agent enters a non-terminating cycle, makes irreversible changes, or pursues a subgoal that drifts from the original intent. Mitigation patterns:

- **Step budgets**: Maximum N tool calls per task (OpenHands default: 30)
- **Reversibility gates**: Destructive operations (file delete, API calls) require explicit human approval
- **Checkpointing**: Save agent state after each step; allow rollback
- **Human-in-the-loop escalation**: Agent calls `request_human_input()` when confidence < threshold
- **Observability hooks**: Every tool call + result logged to structured trace (used by LangSmith, Phoenix, OpenHands EventStream)

### 5. The Autonomy Spectrum

Practitioners use a 5-level autonomy spectrum:

| Level | Name | Description |
|---|---|---|
| L0 | Manual | Human does everything; LLM advises |
| L1 | Copilot | LLM suggests; human approves each step |
| L2 | Supervised | LLM executes; human reviews outcomes |
| L3 | Delegated | LLM handles task class autonomously; human reviews exceptions |
| L4 | Autonomous | LLM runs 24/7 on a task domain; human sets policy |

Most enterprise deployments sit at L2–L3 today. L4 is emerging in software engineering (Devin, OpenHands) and content workflows.

### 6. Emerging Patterns: Swarms and Event-Driven Agents

2025–2026 has seen two new patterns at scale:

**Agent Swarms**: Many lightweight agents run in parallel on sub-problems, results merged by an orchestrator. Used for market research, code review, document analysis. Google's A2A protocol (April 2025) defines a standard handoff contract for swarm coordination.

**Event-Driven Agents**: Agents wake on external triggers (webhook, schedule, queue message) rather than being invoked per-prompt. They maintain persistent memory (knowledge graphs, vector stores), process the event, and sleep. OpenHands headless mode and Claude Code remote sessions follow this pattern.

## Sources

1. Yao et al. (2022) — "ReAct: Synergizing Reasoning and Acting in Language Models" (arxiv.org/abs/2210.03629)
2. Shinn et al. (2023) — "Reflexion: Language Agents with Verbal Reinforcement Learning"
3. OpenHands documentation — docs.openhands.dev (CodeActAgent, EventStream, sandboxed runtime)
4. Anthropic MCP specification — modelcontextprotocol.io (Tool calling standard, November 2024)
5. Google Agent-to-Agent (A2A) protocol announcement — April 2025
6. LangChain documentation — langchain.com/docs (Chain primitives, 2022–2024)
7. OpenAI Swarm (experimental) — github.com/openai/swarm

## Open Questions

- At what autonomy level does enterprise risk management require mandatory human checkpoints?
- How do multi-agent swarms handle conflicting sub-agent outputs?
- What is the right memory architecture for persistent event-driven agents (episodic vs. semantic vs. procedural)?
- Will MCP or A2A emerge as the dominant inter-agent coordination standard?
