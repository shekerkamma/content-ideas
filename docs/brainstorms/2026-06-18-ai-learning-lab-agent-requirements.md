# AI Learning Lab Agent — Requirements
Date: 2026-06-18
Status: Ready for planning

---

## Problem

Learners using the Specificity Method (`/learn-anything`) reach Step 5 (Apply & Test) and
face a mandatory context switch: copy a code prediction into a playground or Colab notebook,
set up the environment manually, run it, copy results back. This friction is high enough that
most learners skip Step 5 entirely — they "feel" like they understood but never prove it.
The same gap resurfaces in production weeks later.

**The bet:** Eliminating the context switch (auto-spinning a sandbox and returning the result
within the same learning session) is sufficient to make learning loops actually close.

---

## Primary Actors

### v1 — Solo dev / AI upskiller
- Working in Claude Code, running `/learn-anything` on a topic
- Reaches Step 5 with a prediction ("I predict that if I do X, the result will be Y")
- Currently opens a new tab and copies code into a playground
- Success: prediction is tested, result returned, session continues without leaving Claude Code

### v2 — L&D lead at a tech company
- Responsible for upskilling a dev team (10–50 people)
- Uses the tool personally (as a solo dev) in v1
- In v2 gains: team visibility, which concepts each person has proved vs only read about
- Success: can see org-level knowledge gaps without running one-on-one assessments

---

## Core Outcome (v1)

A learner states a prediction at Step 5. The system automatically:
1. Constructs a structured task description from the prediction + topic + technology context
2. Delegates execution to OpenHands (headless CLI, Docker sandbox)
3. Returns the pass/fail verdict + actual output to the learning conversation
4. Writes the result into the session file

The learner never leaves Claude Code. The loop closes in the same session.

---

## Requirements

### R1 — Task Spec Construction
learn-anything Step 5 must produce a structured `step5-task.md` containing:
- **Prediction**: what the learner expects to happen (verbatim from conversation)
- **Technology context**: inferred from topic (Python, Claude Code skills, SQL, JavaScript)
- **Minimal scaffold**: the smallest code stub needed to test the prediction
- **Success criterion**: how to evaluate pass vs fail (output matches, error raised, etc.)

The format must be MCP-compatible (forward-compatible with Approach C in v2).

### R2 — OpenHands CLI Delegation
learn-anything must be able to invoke OpenHands headlessly:
```
openhands run --task step5-task.md --output step5-result.md
```
Execution runs in an isolated Docker container. No persistent state between Step 5 calls
within a session (fresh sandbox each time) unless the learner explicitly requests persistence.

### R3 — Result Injection
After OpenHands completes, learn-anything reads `step5-result.md` and injects it into
the conversation as the Step 5 verdict:
- **Match**: "Your prediction was correct. Here's what actually happened: [output]"
- **Mismatch**: "Your prediction didn't match. Actual output: [X]. This is a new precise
  gap — feeding back to Step 1."
Mismatch triggers the Step 1 re-entry loop with the mismatch as a named Mode A gap.

### R4 — Session File Update
After Step 5 completes (with OpenHands result), the session file
(`~/Documents/Learning/{date}-{slug}.md`) must include:
- `## Test Results`: Predicted / Got / Match / What it taught us
- `## Next Step`: either "complete" or the new Mode A gap for next loop

### R5 — Technology Context Detection
learn-anything must infer the sandbox type from topic tags surfaced during Step 2
decomposition. Initial set: Python, Claude Code skills (Python subprocess), SQL (SQLite),
JavaScript (Node). Falls back to generic Bash if none detected. User can override with
an explicit tag: `/learn-anything python: sub-agents`.

### R6 — Graceful Degradation
If OpenHands is not installed or Docker is unavailable, Step 5 must degrade gracefully:
- Detect the gap at session start (not mid-session)
- Offer fallback: "OpenHands not available. I'll describe the expected test environment
  and you can run it manually. Paste results back when ready."
- Manual result paste must be accepted and trigger the same R3/R4 flow.

---

## Scope Boundaries

### In scope (v1)
- Task spec construction from Step 5 conversation state
- OpenHands CLI subprocess delegation (Approach A)
- Result injection and session file update
- Technology context detection (5 types: Python, Claude Code, SQL, JS, Bash)
- Graceful degradation when OpenHands unavailable
- Step 1 re-entry when prediction mismatches

### Deferred to v2
- graphify + GBrain write-back (knowledge graph compounding)
- Per-domain sandbox skill files (`.agents/skills/learn-sandbox-*.md`)
- OpenHands MCP server mode (Approach C) for concurrent learners
- L&D team layer: org-level gap visibility, cohort dashboards
- Persistent sandbox state across Step 5 calls within a session

### Out of scope
- LMS / curriculum management UI
- Multi-user authentication or org management
- Competing with Copilot/Cursor inline execution (different product shape)
- Building a new curriculum from scratch (learn-anything Steps 1-4 are the curriculum)

---

## Moat / Differentiation

The Specificity Method curriculum layer is the differentiation — not execution.

Copilot, Cursor, and Claude can run code. None of them run a structured gap-identification
protocol that surfaces *what the learner specifically doesn't know* before running anything.
The execution (OpenHands) is the final proof step, not the product. The product is the
path from "I don't know what I don't know" → "I proved it."

---

## Skill Wiring (v1)

```
learn-anything (Steps 1–4)
    └─ Step 5: constructs step5-task.md
         └─ OpenHands CLI (headless, Docker sandbox)
              └─ step5-result.md
                   └─ learn-anything: injects result → updates session file
                        ├─ Match → declare complete or next topic
                        └─ Mismatch → Mode A re-entry (new precise gap)
```

Existing wiring (from context pull/push) is unchanged. The OpenHands delegation sits
entirely within Step 5 — no changes to Steps 1–4 or the context pull/push blocks.

---

## Outstanding Questions

- OQ1: Does OpenHands headless CLI accept a task file path, or does it require stdin/flags?
  Must validate against `openhands --help` before planning the delegation call.
- OQ2: What is the exact Docker image OpenHands uses per runtime type? Python vs Node
  require different base images.
- OQ3: Should `step5-task.md` and `step5-result.md` be written to the repo root (cwd),
  a temp dir (`/tmp/`), or the session's `~/Documents/Learning/` folder?
- OQ4: How long does a typical OpenHands headless run take? If >30s, the UX needs a
  "running sandbox..." progress indicator.
- OQ5: For the L&D v2 layer, does each learner need their own OpenHands instance, or can
  one instance handle multiple concurrent task specs? (Determines v2 infra architecture.)

---

## Success Criteria

**v1 is done when:**
1. A learner can reach Step 5, state a prediction, and receive a verdict without leaving
   Claude Code or touching a terminal
2. A mismatch correctly re-enters Step 1 as a named Mode A gap
3. Session file `## Test Results` is populated with the OpenHands output
4. Graceful degradation works when Docker is unavailable

**v2 is done when:**
- L&D lead can see which concepts their team has proved (not just studied)
- OpenHands runs via MCP server (Approach C), enabling concurrent learner sessions
