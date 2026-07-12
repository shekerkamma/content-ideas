# Synthesis: Agentic Workflows — From Chains to Autonomous Loops

## Q1: What is the core difference between prompt chains and autonomous agent loops?

Prompt chains are fixed, linear sequences where each step feeds the next — predictable but brittle, with no self-correction. Autonomous agent loops introduce a feedback cycle: agents perceive state, plan actions, call tools, observe results, and iterate. The key addition is **self-correction via tool feedback**, which makes loops robust to unanticipated failures but more complex to debug (non-linear traces). Chains have a low capability ceiling (only what was designed for); loops have a high ceiling (can handle emergent sub-problems). The tradeoff: loops require mitigation for "runaway behavior" — step budgets, reversibility gates, checkpointing, and human escalation paths.

## Q2: What are the four main loop patterns?

1. **ReAct Loop** — Agent alternates reasoning trace + tool call. Effective for retrieval-augmented tasks. The dominant pattern in production today.
2. **Plan-and-Execute** — Agent produces a multi-step plan first, then an executor sub-agent runs each step. Better for long-horizon tasks (>10 steps) where upfront planning reduces wasted tool calls.
3. **Reflection Loop** — A critic agent evaluates output after each cycle; the main agent revises. Used in Reflexion and GPT-Researcher. Adds quality at the cost of latency.
4. **Multi-Agent Orchestration** — Specialized agents own domains (research, coding, QA); an orchestrator routes tasks. Used in OpenHands multi-agent mode and enterprise CIOS architectures.

## Q3: How does tool calling define the capability ceiling?

Tool calling is the fundamental mechanism that connects agents to the real world. The set of available tools **is** the agent's action space — nothing else. An agent with `search` + `summarize` can only retrieve and compress. An agent with `read_file`, `write_file`, `run_tests`, `git_commit` can autonomously develop software. MCP (Anthropic, 2024) standardizes tool definitions across providers. OpenHands implements this as CodeActAgent — bash/Python actions run in a sandboxed runtime, returning stdout/stderr as observations. Tool calls also provide the discrete, observable steps required for monitoring, rollback, and reliability mitigation.

## Q4: The five-level autonomy spectrum — where do enterprises sit?

| Level | Name | Description |
|---|---|---|
| L0 | Manual | LLM advises; human does everything |
| L1 | Copilot | LLM suggests; human approves each step |
| L2 | Supervised | LLM executes; human reviews outcomes |
| L3 | Delegated | LLM handles task class; human handles exceptions |
| L4 | Autonomous | LLM runs 24/7; human sets policy |

Most enterprise deployments sit at **L2–L3** today. L4 is emerging in software engineering (Devin, OpenHands) and content workflows. The gap between L3 and L4 is primarily a **trust and observability gap**, not a capability gap — the tools exist, but governance frameworks do not yet support full autonomy at scale.

## Q5: Agent swarms and event-driven agents — the emerging frontier

**Agent Swarms**: Many lightweight agents run in parallel on sub-problems; an orchestrator merges results. Enables horizontal scaling of intelligence — a research task that takes one agent 30 minutes can be distributed across 10 agents in 3 minutes. Google's A2A protocol (April 2025) standardizes handoff contracts for swarm coordination.

**Event-Driven Agents**: Agents wake on external triggers (webhook, schedule, queue message), process the event with access to persistent memory (knowledge graph, vector store), then sleep until the next trigger. This pattern enables true background automation — no human prompt required. OpenHands headless mode and Claude Code remote sessions follow this pattern.

Both patterns represent a break from "chat-native" AI interaction. The future of agentic AI is **not conversational** — it is ambient, event-driven, and operating at machine time.
