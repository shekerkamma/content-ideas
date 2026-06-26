---
name: nine-layer-architect
description: >
  Enforces, scaffolds, and audits the 9-Layer AI Production Architecture pattern.
  Use when the user requests "scaffold an AI project", "nine-layer architecture",
  "production-grade AI app", "architect this agent", or triggers "/nine-layer".
  It splits applications into services, prompts, agents, security, evaluation,
  observability, and context layers.
triggers:
  - nine-layer
  - production-grade AI
  - architect AI app
  - scaffold AI project
  - nine-layer-architect
  - /nine-layer
version: "1.0"
---

# Nine-Layer AI Production Architecture Specialist

## Skill Relationships & Chaining

This skill functions as the **architectural compiler** in a multi-skill development chain. It works in sequence with upstream specification skills and downstream validation skills.

```
[Upstream: spec-driven-development]
           ↓ (Outputs: .agents-cli-spec.md)
[Orchestrator: nine-layer-architect]
           ↓ (Outputs: app/ structure)
[Downstream: google-agents-cli-eval]
```

### Chaining Relationships

| Skill | Relationship Type | Condition | Hand-off Artifact |
|---|---|---|---|
| `spec-driven-development` | Upstream Dependency | Always — provides the functional spec | [spec-file](file:///.agents-cli-spec.md) |
| `nine-layer-architect` | Current Orchestrator | Consumes spec to scaffold/refactor codebase | `app/` directory |
| `google-agents-cli-eval` | Downstream Validation | Runs grade evaluations against security & logic nodes | `tests/dataset.json` |

### Chaining Execution Flow

1. **Step 1 (Ingest Spec):** The agent reads the target `.agents-cli-spec.md` to extract the agent's logic nodes, safety rules, and example use cases.
2. **Step 2 (Structure Scaffolding):** The agent executes `nine-layer-architect` to build or refactor `app/` folders matching the specification.
3. **Step 3 (Prompt Registration):** System prompt variables from the spec are written to `app/prompts/templates.py`.
4. **Step 4 (Validation Mapping):** The spec's "Example Use Cases" are parsed and compiled into `tests/dataset.json`.
5. **Step 5 (Evaluation Execution):** The agent runs `agents-cli eval generate` and `agents-cli eval grade` to verify that the graded output matches the spec success criteria.

This skill guides the agent in scaffolding, refactoring, and auditing AI workflows to conform to the **9-Layer AI Production Architecture** standard, moving away from fragile single-file prompts into decoupled, self-correcting systems.

## The Nine Layers

```
Layer 9: Agent Context (GEMINI.md / CLAUDE.md)
  ↓
Layer 6 & 8: Observability & User Feedback (Tracing, Cost, Logs)
  ↓
Layer 4: Security Boundary (Input checks, DLP PII scrubbing, Output checks)
  ↓
Layer 2: Multi-Agent Logic Graph (Decomposer, Grader, Router nodes)
  ├── Layer 3: Prompts (Versioned, typed, externalized templates)
  ├── Layer 1: Services (Semantic cache, datastores, RAG engines)
  └── Layer 5: Evaluation Loop (Golden dataset, offline traces, grading judge)
```

---

## Folder Structure Template

When scaffolding or refactoring an AI project, create the following layout under the project root:

```text
├── GEMINI.md                    # Layer 9: Agent Context and dev commands
├── agents-cli-manifest.yaml     # CLI configuration manifest
├── app/
│   ├── __init__.py
│   ├── main.py                  # Entrypoint / FastAPI server setup
│   ├── services/                # Layer 1: Data, Cache, and RAG services
│   │   ├── __init__.py
│   │   ├── datastore.py         # DB / API connectors
│   │   ├── rag_engine.py        # Chunking & vector retriever
│   │   └── semantic_cache.py    # Embedding-based cache checks
│   ├── agents/                  # Layer 2: Specialist graph nodes
│   │   ├── __init__.py
│   │   ├── classifier.py        # Intent classification node
│   │   ├── grader.py            # Self-correcting response grader
│   │   └── router.py            # Graph transition coordinator
│   ├── prompts/                 # Layer 3: Externalized prompt templates
│   │   ├── __init__.py
│   │   ├── templates.py         # Standard prompt loader and register
│   │   └── system_prompts.py    # Hardcoded prompt strings (if any) or file loaders
│   ├── security/                # Layer 4: Input / Content / Output guards
│   │   ├── __init__.py
│   │   ├── input_guards.py      # Prompt injection check
│   │   └── output_guards.py     # PII scrubber & secret check
│   └── observability/           # Layer 6: Telemetry logging & tracing
│       ├── __init__.py
│       └── tracer.py            # Custom OpenTelemetry / tracing logger
├── tests/                       # Layer 5: Evaluation dataset
│   ├── dataset.json             # Golden dataset scenarios
│   └── test_agent.py            # Integration tests
```

---

## Layer-by-Layer Scaffolding Specifications

### Layer 1: Services (`services/`)
- **Semantic Cache:** Queries must first pass through an embedding similarity check. If similarity with a past resolved query is >95%, return the cached response.
- **RAG & Datastore:** Decouple connection pool parameters and search indexing logic from the agent prompts.

### Layer 2: Agents (`agents/`)
- Implement a Graph Workflow pattern (e.g., ADK 2.0 graph workflow).
- Split logic into single-responsibility nodes. 
- *Rule:* Always include a **Grader/Evaluator Node** that checks the generated output for hallucinations, incomplete instructions, or placeholder text. If fail, route back to the generation node with a correction prompt.

### Layer 3: Prompts (`prompts/`)
- Never hardcode prompts inline inside the agent logic classes.
- Use a central register or load templates from Markdown files inside `prompts/`.
- Ensure prompts are parameterized using standard python string formatting (e.g. `.format(**variables)`).

### Layer 4: Security (`security/`)
- **Input Guard:** Run simple heuristics or a lightweight classification check to detect prompt injection signatures before the main agent runs.
- **Output Guard:** Run regular expressions to detect secrets/keys and run a lightweight text scanner to detect PII (e.g., email, phone number) before returning the response.

### Layer 5: Evaluation (`tests/`)
- Store a `dataset.json` containing 10–20 baseline evaluation test cases (Inputs, expected targets, and classification tags).
- Integrate with `agents-cli eval` loop.

---

## Step-by-Step Refactor Action Plan

When triggered to refactor an existing single-file agent (e.g., `app/agent.py`) into a 9-layer architecture:

1. **Verify environment:** Ensure `uv` and `google-agents-cli` are available.
2. **Scaffold folders:** Create the directories (`services/`, `agents/`, `prompts/`, `security/`, `observability/`).
3. **Extract Prompts:** Find all prompt strings in the original code, move them to `app/prompts/templates.py`, and export them.
4. **Decouple Data & Cache:** Move any database queries, local JSON loading, or API fetches into `app/services/datastore.py`.
5. **Decouple Security Guards:** Implement the input/output verification logic in `app/security/input_guards.py` and `output_guards.py`.
6. **Implement Graph Agents:** Split the original logic into node classes in `app/agents/` and link them in `app/main.py`.
7. **Create GEMINI.md/CLAUDE.md:** Write the Layer 9 Context file providing execution commands and file sitemaps.
8. **Verify execution:** Run the local playground or tests to confirm zero functional regression.
