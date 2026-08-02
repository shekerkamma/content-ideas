# Cross-skill chaining — PLAID ↔ ecosystem

PLAID doesn't live in isolation. It connects to the broader skill ecosystem at every phase. This file maps what feeds into PLAID, what PLAID feeds out, and the file contracts that make each handoff work.

## Upstream into PLAID (other skills → PLAID)

| Source skill | PLAID entry point | How it works |
|---|---|---|
| `/grill-me` (topic type = product-design) | Idea or Plan | The brainstorm's **Summary / key decisions** and **Structured context** pre-fill PLAID's intake. Read `brainstorms/{file}.md` and extract: target user, problem, proposed solution, verticals, competitive landscape. Skip questions PLAID would ask that the brainstorm already answers. |
| `/grill-me` (topic type = deal-prep) | Validate or Plan | A deal-prep brainstorm for a specific use case (e.g., UC05 Predictive Quality) maps directly to a PLAID product idea. The brainstorm's prospect, buyer, and competitive notes become validation inputs. |
| `/ai-strategy-researcher` | Plan | Strategy research identifies a viable AI direction with market sizing, competitive landscape, and technology stack. Feed the brief's key findings into PLAID Plan as pre-filled context for the vision intake. |
| `/ai-strategy-brief` | Plan | A one-page strategy brief provides the "what" and "why." PLAID Plan adds the "how" — PRD, roadmap, tech stack. |
| AI Engineering Use Cases Framework | Idea → Validate | Pick a use case from the framework document. Feed the use case description, target buyer, and delivery model into PLAID Idea as a starting candidate, then Validate it. The framework's structured format (challenge, solution, how-it-works, stack) maps cleanly to PLAID's intake questions. |
| `/vertical-scorer` | Validate | A scored vertical/lane provides attractiveness and priority ratings. Feed the top-scored lane into PLAID Validate to pressure-test it as a product idea before committing to Plan. |

### Upstream handoff contract

When chaining from an upstream skill into PLAID:

1. **Pass the source file path** explicitly (e.g., the brainstorm file, strategy brief, or use case doc).
2. PLAID reads the source and **pre-fills** its intake — it does NOT re-ask questions the source already answered.
3. PLAID writes its own `docs/product-idea.md` or `vision.json` as the canonical output — the upstream file is input context, not the system of record.

## Downstream from PLAID (PLAID → other skills)

| PLAID phase | PLAID output | Downstream skill | Handoff method |
|---|---|---|---|
| Plan | `vision.json` + `docs/prd.md` + `docs/product-vision.md` | `/branded-pptx-deck` | Chain through `/ai-strategy-brief` first to produce action-titled slides from the PRD. Then render with branded-pptx-deck. Do NOT feed raw PRD directly — it needs structuring into slide-ready content. |
| Plan | `docs/prd.md` + `docs/product-roadmap.md` | `/presales-deal-prep` | The PRD provides the solution spec and the roadmap provides the delivery timeline. Feed both into deal-prep's research phase to skip discovery and go straight to proposal generation. |
| Validate | `docs/validation-report.md` | `/presales-deal-prep` | A strong validation report strengthens the deal-prep proposal with evidence: competitive gaps confirmed, fatal flaws addressed, MVP test defined. |
| Plan | `docs/product-vision.md` + `docs/prd.md` | Generative UI demo build | Fork a demo from `~/awesome-llm-apps/generative_ui_agents/`. Use the PRD's feature spec to define ADK agent tools and CopilotKit frontend actions. The product-vision's user personas drive the dashboard design. See **Generative UI integration** below. |
| Launch | `docs/gtm.md` | `/content-ideas` | Update `$CONTENT_HOME/brand/profile.md` with the GTM's target audience, positioning, and channel strategy. Then run content-ideas to generate a content feed aligned with the launch plan. |
| Launch | `docs/gtm.md` | `/social-media-team` | The GTM's content strategy and channel strategy directly map to the social-media-team's script-writer, trend-scout, and channel-analyst agents. |
| Plan | `docs/prd.md` + `docs/product-vision.md` | `/architecture-to-everything` | The PRD's system architecture section and the product-vision's component descriptions provide the system description input. Architecture-to-everything produces 4 formats: .drawio diagram, architecture .md doc, .pptx deck, and interactive .html. Use when the product has a non-trivial multi-component architecture worth documenting visually. |
| Build | Built codebase | `/architecture-to-everything` | After Build, the actual implemented architecture can be documented. Pass the system name and a description derived from the built codebase. More accurate than Plan-stage architecture docs because it reflects what was actually built. |
| Build | Built codebase | `/graphify` | After Build completes, run `/graphify .` on the project to extract a knowledge graph of the codebase architecture. Useful for onboarding, documentation, and future maintenance. |
| Any phase | Any docs/ output | GBrain write-back | Write durable entities (product name, target user, competitors, technology choices) to GBrain for cross-session recall. |

### Downstream handoff contract

When chaining from PLAID to a downstream skill:

1. **Pass file paths explicitly** — don't rely on context. Example: `/branded-pptx-deck` needs to know where `docs/prd.md` is.
2. **Validate PLAID output first** — resolve the PLAID skill directory from its loaded `SKILL.md`, then run `node "<skill-dir>/scripts/validate-vision.js" --migrate ./vision.json` from the target project before handing off vision.json. Check that docs/ files exist and aren't empty stubs.
3. **Respect the deck skill's quality gate** — PLAID's raw PRD is developer-facing. Client-facing decks need an intermediate structuring step (ai-strategy-brief or manual outline).

## Generative UI integration pattern

PLAID Plan + Build connects to the ADK + AG-UI generative dashboard pattern established in the `awesome-llm-apps` reference repos.

**When to use**: When the PLAID product is a dashboard, analytics tool, or agent-powered UI — any product where the user interacts with AI through a visual interface.

**The pattern**:

1. **PLAID Plan** produces `docs/prd.md` with feature specs and `docs/product-roadmap.md` with build phases.
2. **Fork a generative UI demo** from `~/awesome-llm-apps/generative_ui_agents/` that's closest to the product type:
   - Dashboard/analytics → `ai-dashboard-canvas-agent`
   - Multi-step workflow → `multi-agent-researcher`
   - Chat + actions → `finance-agent` or `travel-agent`
3. **Customize** using the PRD:
   - Map PRD features → ADK agent `tools` (server-side `FunctionTool` definitions)
   - Map PRD user interactions → CopilotKit `useCopilotAction` (frontend tool registrations)
   - Map PRD personas → agent system instructions
4. **Critical rule**: include `AGUIToolset()` in the agent's server-side tools list. Without it, frontend tools fail silently. (See CLAUDE.md ADK + AG-UI rules.)
5. **PLAID Build** executes the roadmap phases against the forked + customized demo.

**Example chain**: Use case framework UC → `/grill-me` (extract details) → `/plaid validate` (pressure-test) → `/plaid` (plan PRD + roadmap) → fork generative UI demo → `/plaid build` (execute roadmap against the fork)

## Use case framework → PLAID mapping

When a use case from the AI Engineering Use Cases Framework enters PLAID:

| Framework field | PLAID intake field |
|---|---|
| Use case name + description | Product concept (opening question) |
| Target buyer / user | Target audience |
| Challenge | Problem statement |
| Solution / How-it-works | Feature spec seeds |
| Stack (technologies) | Tech stack pre-selection |
| Systems + integrations | Integration requirements |
| Delivery model (pilot timeline, pricing) | Business model + go-to-market |
| Competitive landscape | Competition section (Validate) |

This mapping means a well-structured use case can skip most of PLAID Idea and go directly to Validate or Plan with pre-filled context.
