# Agent-Native Apps Architecture Guide

## What is the opportunity?
Agent-native apps are software surfaces designed for a user's own agent to use, not just for the user to click through directly. The product is useful because it exposes the right workspace, tools, and memory for an external agent to collaborate with the user in a shared loop.

---

## Architecture Overview
- **Context layer**: local files, project memory, and accumulated decisions.
- **Execution layer**: Cursor, Codex, or another agent host that owns the loop.
- **Tool layer**: MCP, CLI, API, and browser automation.
- **Shared surface**: canvas, doc, sheet, dashboard, or design tool.
- **Outcome layer**: generated work, visible feedback, and improved memory.

---

## Core Principles

### Parity
Anything a user can do in the UI should be achievable by the agent through tools.

### Granularity
Expose primitive actions, not workflow-shaped black boxes.

### Composability
New outcomes should come from new prompts and tool combinations, not hardcoded flows.

### Emergent Capability
The system should handle requests the product team did not explicitly pre-script.

### Improvement Over Time
The agent should accumulate context, so the system gets better with use.

---

## Component: Context Layer
The context layer keeps the agent grounded in the user's actual project.

- Local markdown files
- Brand and strategy notes
- Assets, screenshots, and artifacts
- A `context.md` or equivalent memory file

---

## Component: Agent Host
The agent host is the execution engine.

- Reads the available context
- Chooses the next tool call
- Maintains the loop until the outcome is complete
- Signals completion explicitly

---

## Component: Tool Layer
Tools should be atomic and complete.

- MCP for dynamic external capabilities
- CLI for local and scriptable actions
- API for reliable read/write operations
- Browser automation for surfaces that only exist in the web UI

---

## Component: Shared Surface
The shared surface is where the user and agent work at the same time.

- Canvas for design and ideation
- Docs for planning and specifications
- Sheets for structured data
- Dashboards for status and review

---

## Key Data Flow
### A typical collaboration loop
1. The user defines a job to be done.
2. The agent reads local context and memory.
3. The agent chooses the right tool primitives.
4. The app updates the shared surface visibly.
5. The user reviews, corrects, or approves.
6. The result is written back into memory.

---

## Anti-Patterns
- **Agent as router**: the agent only picks which fixed function to run.
- **Workflow-shaped tools**: a single tool hides judgment and reduces flexibility.
- **Sandboxed split-brain**: the agent writes to a separate workspace.
- **Silent actions**: state changes do not appear in the UI immediately.
- **Completion heuristics**: the system guesses the task is done instead of signaling it.

---

## Design Decisions
- **Decision**: Keep context in files and memory the agent can actually read.
- **Decision**: Prefer primitive tools over rigid workflow APIs.
- **Decision**: Treat the visible surface as part of the architecture.
- **Decision**: Make completion and progress explicit so long tasks are resumable.

---

## Build Heuristic
If a product can answer a user request only when the team prebuilt that exact feature, it is not yet agent-native. If a user can ask for an outcome within the domain and the agent can figure it out through tools and memory, the architecture is moving in the right direction.
