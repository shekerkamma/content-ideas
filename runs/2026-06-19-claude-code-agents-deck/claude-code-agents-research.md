# How to Build Effective Claude Code Agents in 2026
**Source:** https://www.youtube.com/watch?v=RzLV8sfFdMM  
**Host:** Nate Herk | AI Automation (~800K subs)  
**Guest:** Cole (software engineer, AI YouTuber ~200K subs, building Archon open-source project)  
**Format:** 68-minute podcast with live Excalidraw dark-themed presentation  
**Extracted:** 2026-06-19

---

## Core Thesis
> "You're getting ~20% out of Claude Code, and it's not about coding skill."

The framework: **From Using Claude Code to Directing It** — 4 skills that turn Claude Code into a reliable, repeatable engine for any business (not just code).

---

## The 4-Skill Framework

### THE SHIFT
- Stop pulling the lever like a slot machine (vibe coding = prompting & praying)
- **direct it → direct the system = a loop**
- Random outcomes → directed, repeatable results
- Four steps: **1. Plan → 2. Context → 3. Verify → 4. Evolve** (same result, on purpose)

---

### PLAN FIRST
*Make it plan first; cheapest place to be wrong*

**PLAN.md = the north star**
- goal + success criteria
- codebase + docs analysis
- integration points
- task-specific rules
- granular task list
- validation strategy

**The Workflow:**
1. `/prime` → docs · structure · git log
2. `research` → subagents = 3 options
3. `/plan` → writes the doc
4. `edit live` → add e2e · fix scope
5. `= fresh context`
6. `execute` → task by task

> "The plan is the cheapest place to be wrong."
> "Sandwich the delegation of coding between planning and validation."
> "With coding agents, you spend more time planning than you actually do building."

---

### MANAGE CONTEXT
*Right info, not all info; attention is scarce*

**The dumb zone:** Context window degrades after:
- Opus 4.8: ~250,000 tokens
- Opus 4.7: ~200,000 tokens  
- Sonnet 4.6: ~100-125,000 tokens

**Window fills up fast:** cluttered + dumber → (keep only right info) → lean + sharp

**6 ways to control it:**
1. **Separate sessions** — plan & build in different chats
2. **/prime first** — docs, structure, git log
3. **Specialized primes** — `-frontend` / `-backend` / `-db`
4. **On-demand context** — load reference docs only when needed
5. **Git log = memory** — clean commits can summarize context
6. **Subagents** — delegate research; mini stays clean

> "Attention is scarce. Don't get under that false notion that you don't have to care how much you give it."
> "The needle-in-a-haystack problem: information buried in the middle of a massive context gets lost."

---

### VERIFY THE WORK
*Don't trust the first pass; gate every output (code, content, data)*

**Verification pipeline:**
- **Agent output**
  - automated /validate →
    - 1. auto-checks
    - 2. rules / lint
    - 3. tests
  - [fail = fix + re-run ↺]
  - human + agent →
    - 4. review
    - 5. real-world check/
    - **ships ✓**

> "We only care about what we see when control comes back to us."
> "Without verification checks, maybe it's 65 or 70% correct. Now you can get 92% on the first pass."
> "We don't care about the initial mess-ups. As long as it iterates by itself."

---

### BUILD THE SYSTEM
*Evolve the system, don't just fix the bug*

**What to fix when a bug appears:**
- **+ rule** → 'use @/ aliases'
- **+ reference doc** → auth-flow.md
- **+ update plan** → always add tests
- **+ new /command** → reuse it forever

> "Every bug = a permanent upgrade"

**Staircase of growth:** rule → doc → cmd → skill  
> "The floor keeps rising + smarter every week"
> "Same workflow, taller building. Only the ceiling changes."

---

## Agent = Model + Harness
*(Concentric circles architecture diagram)*

```
  ┌─────────────────────────────┐
  │    THE AI LAYER (You BUILD) │  ← rules · skills · hooks · MCP · LSP
  │  ┌─────────────────────┐    │
  │  │    THE HARNESS       │    │
  │  │  ┌─────────────┐    │    │
  │  │  │  The model  │    │    │
  │  │  │  (You PICK) │    │    │
  │  │  └─────────────┘    │    │
  │  └─────────────────────┘    │
  └─────────────────────────────┘
```

> "You PICK the tool (harness) & model. You BUILD the AI layer that wraps it."

Examples of harnesses: Claude Code, Codex, Cursor  
The AI layer you build: CLAUDE.md, skills, hooks, MCP servers, LSP integrations

---

## The RALF Loop (Harness Engineering)
Multi-session orchestration for large tasks:
1. **Session 1** (Planner): Reads spec → defines phase list → writes handoff doc
2. **Session 2** (Implementer): Reads handoff → executes phase → writes execution report
3. **Session 3** (Validator): Reads report → runs code review → validates

> "Build Claude Code into a system instead of having Claude Code trying to orchestrate everything."
> "Pick when the AI model works in a workflow instead of having it drive the whole thing."

Cole's open-source project **Archon** is building a deterministic multi-session harness for Claude Code.

---

## Security Mindset
> "If you tell it never to wipe a database, it's still going to do that."
> "If you don't allow it to delete a folder, it can still write a script to do that."
> "Anything that the agent can read or touch, you have to assume that it will — even if you never ask it to."

**Real incident (Nate's team):** Agent misinterpreted a task list item and sent a discount email to their entire list.

**Solution:** Scoped API keys + restricted permissions at the infrastructure level — not just prompt instructions.

---

## Non-Coding Use Cases
- **B2B Quote Automation:** Research inventory agent → Price comparison agent → PDF draft agent → Formatting agent
- **Second Brain / AIOS:** Using Claude Code for knowledge work, not just software
- **Business Operations:** Automating invoicing, client communications, proposals

---

## Key Quotes (Deck-Ready)
1. *"The plan is the cheapest place to be wrong."*
2. *"Attention is scarce."*
3. *"You're getting ~20% out of Claude Code, and it's not about coding skill."*
4. *"Every bug = a permanent upgrade."*
5. *"The floor keeps rising + smarter every week."*
6. *"Same workflow, taller building. Only the ceiling changes."*
7. *"We only care about what we see when control comes back to us."*
8. *"You're not learning to code, you're learning to direct."*
9. *"Sandwich the delegation of coding between planning and validation."*
10. *"Anything that the agent can read or touch, you have to assume that it will."*

---

## Deck-Usable Data Points
- 92% first-pass accuracy with verification vs 65-70% without
- Dumb zone: 250K tokens for Opus 4.8
- Claude Code has 1M token context but effective limit is ~250K for quality
- Cole went from 50K to 200K YouTube subscribers; Nate from 10K to ~800K
- Cole quit job 3 months after starting YouTube channel
- Archon project: deterministic multi-agent session orchestration (open source)
