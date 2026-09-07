---
name: compound-engineering-skill-chaining
description: 'Use when chaining EveryInc Compound Engineering skills with Sheker''s Hyundai AI Vault skills. Trigger on: "chain Compound Engineering with vault skills", "cross-skill pipeline", "CE pipeline", "research to POC build", "use case to implementation", "debug to learning", "product pulse to strategy", "content idea to publish", "presales deck review", "session mining", "strategy grounding", or any time vault research, use-case briefs, POC assets, or client work should move into /ce-brainstorm, /ce-plan, /ce-work, /ce-debug, /ce-code-review, /ce-doc-review, /ce-compound, or /ce-product-pulse and then return to the vault.'
---

# Compound Engineering Skill Chaining

## Purpose

Route work between Sheker's vault-native skills and the Compound Engineering plugin.

Core rule:

> Vault skills decide what is worth building. Compound Engineering decides how to build it well. Vault skills package the result into wiki knowledge, POC assets, content, tasks, or pre-sales decks.

Do not use this skill for plugin installation. Use it only for cross-skill pipeline selection, handoff, and output routing.

## Operating Model

Use the **vault → engineering loop → vault** pattern:

1. Start from vault context: clippings, research notes, client discovery, UC briefs, architecture notes, project notes, or tasks.
2. Select the right upstream vault skill to shape the work.
3. Hand the buildable unit to Compound Engineering for requirements, plan, work, review, debug, or learning capture.
4. Return CE outputs to the vault: `Projects/`, `Knowledge/`, `Dev Logs/`, `Daily/`, `Boards/Work.md`, `Content/`, or `Decks/`.
5. Keep the loop small: one workflow, one demo, one feature, or one review target.

## Skill Mapping

| Compound Engineering skill | Pair with vault skill(s) | Use when |
|---|---|---|
| `/ce-strategy` | `solution-discovery`, `vault-poc-factory-pipeline` | A project needs target problem, persona, metrics, and tracks before ideation or build work. |
| `/ce-ideate` | `vault-content-ideas-pipeline`, `vault-poc-factory-pipeline` | Research or client context needs stronger build ideas before requirements. |
| `/ce-brainstorm` | `uc-brief-builder`, `uc-validator`, `vault-poc-factory-pipeline` | A validated UC or POC idea needs a right-sized requirements doc. |
| `/ce-plan` | `capability-mapper`, `vault-poc-factory-pipeline` | Requirements need implementation steps, files, risks, tests, and task boundaries. |
| `/ce-work` | `vault-poc-factory-pipeline`, GitHub workflows | A plan is ready for code, repo changes, or demo build execution. |
| `/ce-debug` | GitHub CI/debug workflows, `vault-poc-factory-pipeline` | A demo, repo, or workflow fails and needs reproduction plus root cause. |
| `/ce-code-review` | GitHub review workflows, `uc-validator` | Code needs a merge-quality gate before demo or client handoff. |
| `/ce-doc-review` | `vault-wiki-pipeline`, `vault-presales-pptx-pipeline`, `genspark-slides` | Requirements, docs, briefs, Genspark slide recoveries, or deck packets need clarity and consistency review. |
| `/ce-compound` | `vault-wiki-pipeline`, GBrain | A build, debug session, or review produced reusable lessons. |
| `/ce-product-pulse` | `vault-poc-factory-pipeline`, `vault-presales-pptx-pipeline`, `/ce-strategy` | Product usage, errors, and performance should inform strategy, next build, or proof objects. |
| `/ce-sessions` | `vault-content-research-pipeline` | Past Codex/Codex sessions contain patterns worth capturing as research notes. |
| `/ce-polish` | `vault-content-ideas-pipeline` | A content draft needs conversational UX iteration before publishing. |
| `/ce-frontend-design` | `vault-poc-factory-pipeline` | A POC demo needs production-grade UI before client handoff. |
| `/ce-simplify-code` | `vault-poc-factory-pipeline`, GitHub workflows | Code needs a parallel simplification pass with test verification before merging. |
| `/ce-optimize` | `vault-poc-factory-pipeline` | A working demo needs iterative performance optimization with quality scoring. |

## Primary Pipelines

### Research-to-POC Build

```text
Clippings/
→ vault-content-research-pipeline
→ vault-wiki-pipeline
→ vault-poc-factory-pipeline
→ /ce-brainstorm
→ /ce-plan
→ /ce-work
→ /ce-code-review
→ /ce-compound
→ vault-presales-pptx-pipeline
```

Use when a clipping, GitHub repo, article, or technical pattern should become a POC Factory asset.

### Hyundai AI Use Case to Implementation

```text
solution-discovery
→ uc-identification
→ capability-mapper
→ uc-feasibility-review
→ uc-brief-builder
→ uc-validator
→ /ce-brainstorm
→ /ce-plan
→ vault-poc-factory-pipeline
→ /ce-work
→ /ce-code-review
→ /ce-compound
→ vault-presales-pptx-pipeline
```

Use when a Hyundai AI Plant Operations UC should become a buildable demo and client-facing asset.

### Debug-to-Learning

```text
/ce-debug
→ /ce-code-review
→ /ce-compound
→ vault-wiki-pipeline
→ Dev Logs/
→ Projects/
```

Use when failures reveal patterns that future agents or engineers should not rediscover.

### Product Signal to Strategy

```text
/ce-product-pulse
→ /ce-strategy
→ /ce-ideate
→ /ce-brainstorm
→ vault-content-ideas-pipeline
```

Use when usage, errors, or performance data should change roadmap, content, or next experiments.

### Documentation Quality Gate

```text
uc-validator
→ /ce-doc-review
→ vault-wiki-pipeline
→ vault-presales-pptx-pipeline
```

Use when a UC brief, requirements doc, project note, or deck packet must be clear enough for client or team handoff.

### Content Idea to Publish

```text
vault-content-ideas-pipeline
→ /ce-brainstorm "refine content angle into a structured draft"
→ /ce-polish (auto-detects LinkedIn/X format)
→ Content/LinkedIn/ or Content/X/
→ /ce-compound (capture what resonated and why)
```

Use when a content idea from research should become a polished, publishable draft. `/ce-polish` runs conversational UX iteration and auto-detects the target format.

### Presales Deck Review

```text
vault-presales-pptx-pipeline (generates deck packet)
→ /ce-doc-review (7 persona agents: coherence, feasibility, product lens, design lens, scope guardian, security lens, adversarial)
→ fix flagged issues
→ presentations:Presentations (build reviewed editable PPTX)
→ /ce-compound (capture deck review patterns)
```

Use when a client-facing deck must survive multi-perspective scrutiny before handoff. `/ce-doc-review` runs parallel persona agents that catch framing gaps, feasibility issues, scope creep, and internal contradictions that single-pass review misses.

### Genspark Deck to Client-Ready PPTX

```text
watch-video (for YouTube/video sources)
→ Genspark AI Slides app (`_create_slide`) (create preview HTML/CSS deck)
→ genspark-slides (recover slide HTML and visual references)
→ /ce-doc-review (story, design, proof, and client-readiness critique)
→ fix flagged issues in the recovered source or deck packet
→ presentations:Presentations (rebuild as editable, brand-ready PPTX)
→ vault-presales-pptx-pipeline (route final deck to `Decks/` and `Pre-Sales/`)
→ /ce-compound (capture reusable deck recovery and polish lessons)
```

Use when the user wants Genspark to create preview slides first, or when the source material is a YouTube/video URL, Genspark agent/viewer link, Genspark slide HTML, or a visually recreated Genspark PPTX that needs to become editable, branded, or client-ready. If the source is video, run `watch-video` before Genspark so the preview deck can use timestamped visual notes. If the deck already exists, start at `genspark-slides`. If the user only needs a fast visual copy, `genspark-slides` can package rendered HTML directly; if the user asks for client-ready quality, always chain through `/ce-doc-review` and `presentations:Presentations`.

If the Genspark AI Slides app tool is not visible in the current session, use `tool_search` for `Genspark AI Slides create presentation slides` before asking the user to enable a connector.

### Session Mining to Research

```text
/ce-sessions (query past Codex/Codex/Cursor sessions)
→ vault-content-research-pipeline (enrich patterns into research notes)
→ vault-wiki-pipeline (route entities, update MOCs)
→ vault-content-ideas-pipeline (graduate strong angles)
```

Use when past agent sessions contain reusable patterns, architectural decisions, or debugging insights worth capturing as permanent vault knowledge.

### Strategy Grounding (Cross-Skill)

```text
/ce-strategy (create or update STRATEGY.md)
→ gbrain put {project-slug}-strategy (persist across sessions)
→ Projects/{project}/ (anchor in vault)
```

Read path — any downstream skill reads strategy context:
```text
gbrain search {project-slug}-strategy
→ /ce-ideate, /ce-brainstorm, /ce-plan (strategy-grounded)
→ /grill-me, /presales-deal-prep, pipeline-runner (strategy-aware)
```

Use when a project needs durable strategy context that all skills — vault-native, CE, and standalone — can read. `/ce-strategy` writes the anchor; GBrain persists it; downstream skills read it.

## Compounding Flywheel

Every pipeline should end with knowledge capture. This is the compounding mechanism — without it, each cycle starts from scratch.

```text
Any pipeline end
→ /ce-compound (what was learned, what surprised, what to do differently)
→ vault-wiki-pipeline (route to Knowledge/, project notes, MOC backlinks)
→ gbrain put {topic}-learning (persist across sessions for semantic recall)
```

### What to compound

| Signal | Compound as |
|---|---|
| A debugging session found a non-obvious root cause | Pattern note in `Knowledge/`, gbrain page |
| A review caught a recurring anti-pattern | Rule in project `AGENTS.md` or `STRATEGY.md` |
| A client conversation revealed a new objection | Objection entry in account/deal notes, gbrain page |
| A deck review flagged a framing gap | Deck-building lesson in `Knowledge/`, feed to `/ce-doc-review` |
| A POC demo exposed an integration limitation | Architecture note, risk entry in project note |
| A content draft got strong engagement | Content pattern in `Knowledge/`, feed to `vault-content-ideas-pipeline` |

### GBrain as the compounding store

GBrain is the cross-session memory that makes compounding durable:

- `/ce-compound` writes lessons → `vault-wiki-pipeline` routes to vault → `gbrain put` persists for semantic recall
- Next cycle: `gbrain search` or `gbrain query` retrieves relevant prior learnings before `/ce-brainstorm`, `/ce-plan`, or `/ce-strategy`
- Strategy context, account context, technical patterns, and review lessons all compound across sessions

Cost guardrail: use `gbrain put` (embedding cost only), not `gbrain query` (synthesis cost), for write-back. Use `gbrain search` (free keyword) for simple lookups; escalate to semantic retrieval only when the topic needs fuzzy matching.

## Tiered Review Integration

CE's multi-agent review (`/ce-code-review` = 20 agents, `/ce-doc-review` = 7 agents) replaces single-pass review at these gates:

### POC Factory quality gate

```text
/ce-work (code complete)
→ /ce-code-review (parallel: correctness, security, performance, maintainability, architecture, testing, adversarial)
→ fix findings above confidence threshold
→ /ce-simplify-code (final simplicity pass)
→ vault-presales-pptx-pipeline
```

Agents self-report confidence. Findings below threshold are flagged for human judgment, not auto-fixed. Dedup pipeline prevents redundant findings across agents.

### UC brief validation gate

```text
uc-brief-builder
→ uc-validator (vault-native structural check)
→ /ce-doc-review (parallel: coherence, feasibility, product lens, scope guardian, adversarial)
→ merge findings, fix blockers
→ /ce-brainstorm (proceed with validated brief)
```

Run `uc-validator` and `/ce-doc-review` as complementary passes: `uc-validator` checks structural completeness; `/ce-doc-review` challenges framing, feasibility, and hidden assumptions.

### Deck packet review gate

```text
vault-presales-pptx-pipeline (generate deck packet)
→ /ce-doc-review (parallel: coherence, design lens, product lens, scope guardian, security lens)
→ fix flagged issues in packet
→ presentations:Presentations (build PPTX from reviewed packet)
→ PPTX QA (preview, overlap check, visual QA)
```

The deck packet gets multi-persona review before PPTX build, not after. Fixing content in markdown is cheaper than fixing it in slides.

## Trigger Rules

Invoke Compound Engineering after vault skills when:

- A note defines a specific user, problem, data source, and outcome.
- A UC brief passes `uc-validator` or has fixable blockers.
- A POC project has named build tasks and source research.
- A failure needs reproduction, root cause, and verified fix.
- A review finding can become a reusable project lesson.

Return from Compound Engineering back to vault skills when:

- `/ce-brainstorm` creates requirements that need project/task routing.
- `/ce-plan` creates implementation steps that should update `Projects/`, `Tasks/`, or `Boards/Work.md`.
- `/ce-work` changes code or demo assets and needs dev-log propagation.
- `/ce-code-review` or `/ce-doc-review` finds issues that need wiki, project, or task updates.
- `/ce-compound` produces reusable lessons that belong in `Knowledge/`, relevant project notes, and GBrain.
- `/ce-product-pulse` produces proof, risk, or roadmap changes that feed `Pre-Sales/`, `Decks/`, or strategy notes.
- `/ce-strategy` creates or updates a strategy anchor that should persist in GBrain and project notes.
- `/ce-sessions` surfaces patterns from past sessions that should become research notes.
- `/ce-polish` produces a publishable draft that should route to `Content/LinkedIn/` or `Content/X/`.

## Output Routing

| Output | Route |
|---|---|
| CE strategy | Relevant `Projects/{project}/STRATEGY.md` or project note section. |
| CE brainstorm requirements | `Projects/{project}/requirements/` or linked project note section. |
| CE implementation plan | `Projects/{project}/plans/`, `Tasks/`, and `Boards/Work.md`. |
| CE work session | `Dev Logs/YYYY-MM-DD - {description}.md`, project note, daily note. |
| CE debug findings | Dev log, project note risk/decision section, and follow-up tasks. |
| CE code/doc review findings | PR/review notes, task list, project note, and fixes if approved. |
| CE compound lessons | `Knowledge/`, project note, relevant MOC backlinks, and `gbrain put {topic}-learning`. |
| CE strategy | `Projects/{project}/STRATEGY.md`, project note, and `gbrain put {project}-strategy`. |
| CE session patterns | `vault-content-research-pipeline` → `content-research/` and relevant MOCs. |
| CE polish output | `Content/LinkedIn/` or `Content/X/` as publishable draft. |
| CE doc-review findings | Deck packet fixes, UC brief fixes, project note updates. |
| Genspark recovered slides | `genspark-slides` output under task workspace; final client-ready PPTX routes to `Decks/` and `Pre-Sales/`. |
| Video watch report | `watch-video` output under task workspace; feed timestamped notes and frames to content research, Genspark preview, and Presentations. |
| Product pulse | `docs/pulse-reports/` in repo, then vault summary in project/pre-sales notes. |
| Client-facing proof | `vault-presales-pptx-pipeline` → `Decks/` and `Pre-Sales/`. |

## Hyundai AI Examples

### UC-01 Visual Inspection

```text
uc-validator
→ /ce-brainstorm "turn UC-01 Visual Inspection into a plant-floor defect detection demo"
→ /ce-plan
→ vault-poc-factory-pipeline
→ /ce-work
→ /ce-code-review
→ /ce-compound
→ vault-presales-pptx-pipeline
```

Expected vault outputs: project build tasks, camera/image data assumptions, edge/cloud architecture, review lessons, and use-case realization deck packet.

### UC-04 SOP Compliance

```text
uc-validator
→ /ce-brainstorm "turn UC-04 SOP Compliance into an operator workflow compliance assistant"
→ /ce-plan
→ /ce-doc-review
→ /ce-work
→ /ce-compound
```

Expected vault outputs: SOP data requirements, operator workflow, audit trail design, risk notes, and reusable compliance-agent pattern.

### UC-05 Predictive Quality

```text
capability-mapper
→ uc-feasibility-review
→ uc-brief-builder
→ /ce-brainstorm "define the minimum predictive quality demo from available plant signals"
→ /ce-plan
→ /ce-code-review
→ /ce-compound
```

Expected vault outputs: data signal map, model baseline assumptions, KPI targets, delivery risks, and project tasks.

## Guardrails

- Do not use Compound Engineering for simple note cleanup.
- Do not skip `uc-validator` before client-facing use-case work.
- Do not leave CE learnings outside the vault — always route through `vault-wiki-pipeline` and GBrain.
- Do not create broad POC projects without tasks.
- Keep one chain focused on one buildable unit.
- Follow `AGENTS.md`: terse, direct, wikilinks where useful, no marketing filler.
- Every pipeline must end with `/ce-compound` → wiki → GBrain. No exceptions. This is the compounding mechanism.
- Run `/ce-doc-review` before PPTX build, not after. Fix content in markdown, not slides.
- For new Genspark deck work, trigger Genspark AI Slides first to create preview slides, then run `genspark-slides` to capture HTML source and visual references before review/build. If the source is video, run `watch-video` before Genspark. Use `tool_search` to expose the Genspark AI Slides app tool if it is not already listed.
- Use `gbrain search` (free) before `gbrain query` (costs tokens) for strategy/learning recall.
- Do not run tiered review on trivial changes. Reserve multi-agent review for client-facing code, demos, UC briefs, and deck packets.
- `/ce-strategy` outputs must persist in both the project folder and GBrain. A strategy that only lives in one place is a strategy that gets lost.
