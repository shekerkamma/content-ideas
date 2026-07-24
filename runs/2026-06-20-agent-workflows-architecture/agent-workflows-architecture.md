# Agent Workflows — Architecture Guide

## What is Agent Workflows?

Agent Workflows are orchestration patterns that give large language models (LLMs) the ability to do more than generate text in a single pass. Instead of answering in one shot, an agent can call external tools, loop through reasoning steps, and chain intermediate results — turning a static model into a dynamic problem-solver. Three patterns dominate production deployments: Tool Calling, the ReAct Framework, and Multi-step Reasoning.

---

## Architecture Overview

| Pattern | Core Loop | When to Use |
|---|---|---|
| Tool Calling | LLM → Tool → Result → Response | Single external lookup, function execution |
| ReAct Framework | Thought → Action → Observation → (loop) | Multi-step tasks needing iteration |
| Multi-step Reasoning | Decompose → Chain → Aggregate → Synthesize | Complex reasoning requiring sequential logic |

All three share the same entry and exit: a **User Query** flows in, an **Agent Response** flows out. The difference is what happens in between.

---

## Component: Tool Calling

Tool Calling gives an LLM access to functions it can invoke by name. The model decides when to call a tool, what arguments to pass, and how to incorporate the result.

**How it works:**
- The LLM is given a list of available tools (functions) in its system prompt or context
- When the model determines a tool is needed, it emits a structured tool call (JSON)
- The host environment executes the tool and returns the result to the model
- The model incorporates the result and generates its final response

**Key sub-components:**
- **Tool registry** — named functions available to the model (search, calculator, DB query, API)
- **Tool call parser** — extracts the model's tool invocation into executable form
- **Execution layer** — runs the function with the specified arguments
- **Context injector** — appends the tool result to the conversation for the model to see

**Example:** User asks "What's the weather in Tokyo?" → LLM calls `get_weather(city="Tokyo")` → Result returned → LLM answers with live data.

---

## Component: ReAct Framework

ReAct (Reason + Act) is a loop-based pattern where the model alternates between reasoning about what to do next (Thought), taking an action (Action), and observing the result (Observation). The loop continues until the model determines it has enough information to answer.

**How it works:**
- The model generates a **Thought**: internal reasoning about the current state and what to do next
- The model generates an **Action**: a specific step to take (call a tool, look up information, calculate)
- The environment returns an **Observation**: the result of that action
- The model evaluates whether it's done. If not, it generates the next Thought and continues

**Key sub-components:**
- **Prompt template** — instructs the model to format output as Thought/Action/Observation
- **Action parser** — extracts the action from free-form model output
- **Loop controller** — detects the "Final Answer" signal to exit the loop
- **Scratchpad** — the growing transcript of Thought/Action/Observation pairs fed back each iteration
- **Max iterations guard** — safety cap to prevent infinite loops

**Example:** User asks "Find the CEO of OpenAI and their net worth." → Thought: "I need to search for the CEO first." → Action: search("OpenAI CEO") → Observation: "Sam Altman" → Thought: "Now I need his net worth." → Action: search("Sam Altman net worth") → Observation: "$1B+" → Final Answer: generated.

---

## Component: Multi-step Reasoning

Multi-step Reasoning (Chain-of-Thought) decomposes a complex problem into a sequence of sub-problems, solves each in order, and synthesizes the results into a coherent final answer. Unlike ReAct, the steps are pre-planned rather than discovered dynamically.

**How it works:**
- The model first decomposes the problem: it produces an explicit list of intermediate steps
- Each step is solved sequentially, with the result of each step passed as context to the next
- After all steps are solved, the model aggregates the intermediate results
- A final synthesis pass produces the complete answer

**Key sub-components:**
- **Decomposer** — prompt that instructs the model to break the problem into numbered steps
- **Step executor** — runs each step as a separate model call or within a long context window
- **Context chain** — passes prior step outputs as input to the next step
- **Aggregator** — collects all intermediate results
- **Synthesizer** — produces the final coherent response from aggregated results

**Example:** User asks "Compare the revenue of Apple and Microsoft for the last 3 years and identify trends." → Step 1: Retrieve Apple revenue data → Step 2: Retrieve Microsoft revenue data → Step 3: Calculate year-over-year growth for each → Step 4: Compare the two → Final: Write the analysis.

---

## Key Data Flows

### A typical Tool Calling flow
1. User submits query
2. LLM receives query + tool definitions in context
3. LLM emits a tool call (JSON: `{"tool": "search", "args": {"q": "..."}}}`)
4. Host parses and executes the tool
5. Result is appended to the conversation context
6. LLM generates final response using the tool result

### A typical ReAct flow
1. User submits query
2. LLM generates Thought: "I need to find X first"
3. LLM generates Action: calls a tool or step
4. Environment returns Observation
5. LLM evaluates: "Am I done?" — if No, go to step 2 with updated scratchpad
6. If Yes: LLM generates Final Answer

### A typical Multi-step Reasoning flow
1. User submits complex query
2. LLM decomposes into N sub-steps
3. Step 1 executes; result stored
4. Step 2 executes with Step 1 result in context; result stored
5. (Repeat for N steps)
6. Aggregator combines all results
7. Synthesizer produces final answer

---

## Design Decisions

- **Tool Calling vs ReAct:** Tool Calling is stateless and fast — one round trip. ReAct is stateful and iterative — use it when the number of steps cannot be known upfront (e.g., open-ended research tasks). ReAct costs more in tokens and latency.

- **ReAct loop safety:** Every production ReAct implementation must have a max-iteration cap. Without it, a model that fails to converge on a Final Answer will loop indefinitely. 10–15 iterations is a typical ceiling.

- **Multi-step vs ReAct:** Multi-step Reasoning requires the problem to be decomposable upfront — the model plans the full sequence before executing. ReAct discovers steps dynamically. Use Multi-step when the problem structure is known; use ReAct when it isn't.

- **Combining patterns:** Real production agents often nest these patterns. A ReAct outer loop may call a Multi-step Reasoning sub-agent for complex sub-problems, which in turn uses Tool Calling for data retrieval. This is the basis for multi-agent architectures.
