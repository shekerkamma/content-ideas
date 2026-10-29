# Session continuity
- On session start, check if `~/.claude/session-handoff.md` exists. If it does, read it silently and use it as context for continuing the previous session's work. After reading, delete the file so it doesn't persist across multiple sessions.

# Memory system (store / inject / recall) — applies to ALL sessions
Persistent conversation memory lives at `~/.claude/memory/`. Hooks in
`~/.claude/settings.json` inject a frozen snapshot at SessionStart and
auto-capture every turn at Stop — do not duplicate what they already do.

- **Recall before pleading ignorance.** Before answering "I don't have context
  on that" about past work, decisions, or conversations, run
  `python3 ~/.claude/memory/scripts/search.py "<query>"`. On recall, cite date +
  source file/heading; open `~/.claude/memory/archive/<session-id>.jsonl` when
  exact wording matters. If nothing turns up, say so — never invent a memory.
- **Curated writes go through the `/memory` skill** ("remember this", "note
  that", "forget about X"). The judgment rules live inside the skill — edit
  them there, not here. Snapshot cap is 2,500 chars; snapshot writes take
  effect next session (frozen for the current one).
- **Layer arbitration — write each fact to exactly one layer:**
  conversation continuity + exact-transcript recall → `~/.claude/memory/`;
  entities/topics knowledge graph (companies, prospects, verticals, research)
  → GBrain; behavioral guidance per project → the project's auto-memory dir;
  end-of-session baton → session-handoff.
- Never store secrets (API keys, tokens, passwords) in memory files. Scripts
  that shell out to `claude -p` must set `CLAUDE_MEMORY_WORKER=1` so hooks
  skip the summarizer's own sessions.
- Model chain for memory chores is free-first (Groq → OpenRouter `:free` →
  `claude -p` Haiku); embeddings use the billing-free AI Studio key in
  `~/.claude/memory/.env`. If embeddings fail, search degrades gracefully —
  do not "fix" it by switching the chain to plan/paid models.

# Think once, run cheap — applies to ALL recurring work
When a workflow recurs, the expensive model's job is to produce the durable
artifact — a skill, runbook, judgment-rules section, or rewritten context
file — never to be the recurring executor.

- Repeated expensive reasoning with no skill → `/skills-analyst` to find the
  pattern, then `/skill-builder` to write it. Stale/contradictory context files →
  `/rule-rewriter`. Existing-skill hygiene → `/skills-analyst`.
- Every generated skill carries an editable `## Judgment rules` section (the
  policy lives on the page, tunable — never hardcoded into steps) and states
  its cost tier: the cheapest chain that can execute it (free chain → Haiku →
  Sonnet). Don't silently upgrade a skill's executor to a pricier model —
  that's a policy change, ask first.

# Voice — applies to ALL skills
When producing ANY written output from any skill (slides, briefs, reports, plans, analyses, roadmaps, summaries, code comments), read and apply `~/.claude/skills/voice.md` before writing.
- Specific beats general. Named beats unnamed. Shown beats stated.
- Verdict first, evidence second. Never hedge without a reason.
- Anti-patterns from voice.md are hard blocks — remove every instance before delivering output.
- Slide titles are verdicts, not topics. Numbers beat adjectives. Pull quotes must earn their place.

# Research Tool Order — applies to ALL skills, ALL sessions
When any skill performs external research or information lookup, follow this order. Do NOT skip steps.

1. **Read local files first** — SKILL.md, referenced `.md` files, repo artifacts. Never search for what is already local.
2. **GBrain recall** — run `gbrain search "<topic>"` before any external call. If results found, use them. Write durable findings back after the run.
3. **Exa MCP** (`mcp__claude_ai_Exa__web_search_exa`, `mcp__claude_ai_Exa__web_fetch_exa`) — MUST use if available. Exa returns current, high-signal web content with citations.
4. **Firecrawl** (`/firecrawl` skill or `mcp__firecrawl__*`) — for full-page ingestion of specific URLs, documentation sites, or competitor pages.
5. **Specialist CLIs / MCPs** — Microsoft Learn MCP for Azure/M365 docs, GitHub MCP for repo data, Notion/Google Drive MCPs for internal docs.
6. **WebSearch** — ONLY if steps 2–5 are unavailable or return no signal. NEVER call WebSearch as the first move.

A skill's own `## Source / Tool Order` section overrides this default for that skill only.
When a skill has no `## Source / Tool Order` section, this global order applies without exception.


# deep-research
- **deep-research** (`~/content-ideas.local/skill-framework/.agents/skills/deep-research/SKILL.md`) - comprehensive, citation-backed research with multi-source investigation and structured brief. Trigger: `/deep-research`
When the user types `/deep-research`, invoke the Skill tool with `skill: "deep-research"` before doing anything else.
- Also triggers on: "deep research", "research this"

# technical-writer
- **technical-writer** (`~/content-ideas.local/skill-framework/.agents/skills/technical-writer/SKILL.md`) - write READMEs, guides, API references, onboarding docs, release notes, and architecture explainers. Trigger: `/technical-writer`
When the user types `/technical-writer`, invoke the Skill tool with `skill: "technical-writer"` before doing anything else.
- Also triggers on: "write docs", "write documentation", "write a README"

# openkb
- **openkb** (`~/content-ideas/skills/openkb/SKILL.md`) - query, chat, and synthesize content from a compiled OpenKB knowledge base (wiki/concepts, entities, summaries). Trigger: `/openkb`
When the user types `/openkb`, invoke the Skill tool with `skill: "openkb"` before doing anything else.
- Also triggers on: "query my KB", "what does my knowledge base say about", "search my wiki", mentions of `.openkb/` or `wiki/` tree built by openkb

# openkb-deck-neon
- **openkb-deck-neon** (`~/content-ideas/skills/openkb-deck-neon/SKILL.md`) - generate a dark Aurora Glass HTML slide deck from compiled KB content. Trigger: `/openkb-deck-neon`
When the user types `/openkb-deck-neon`, invoke the Skill tool with `skill: "openkb-deck-neon"` before doing anything else.


# openkb-html-critic
- **openkb-html-critic** (`~/content-ideas/skills/openkb-html-critic/SKILL.md`) - review and improve HTML output generated by OpenKB. Trigger: `/openkb-html-critic`
When the user types `/openkb-html-critic`, invoke the Skill tool with `skill: "openkb-html-critic"` before doing anything else.

# second-brain
- **second-brain** (`~/content-ideas/skills/second-brain/SKILL.md`) - bootstrap and maintain a markdown-first knowledge base with raw/ → wiki/ → archive/ structure (OpenKB-style compilation pattern). Trigger: `/second-brain`
When the user types `/second-brain`, invoke the Skill tool with `skill: "second-brain"` before doing anything else.
- Also triggers on: "build my second brain", "set up knowledge base", "add to my wiki", "compile my notes"

# research-to-deck
- **research-to-deck** (`~/.claude/skills/research-to-deck/SKILL.md`) - compound pipeline: topic or URLs → deep-research/content-research → openkb compile → synthesis → HTML deck (neon or editorial) → QA. One command, fully automated. Trigger: `/research-to-deck`
When the user types `/research-to-deck`, invoke the Skill tool with `skill: "research-to-deck"` before doing anything else.
- Also triggers on: "research X and make a deck", "research to deck", "kb pipeline", "research and deck it"

# marp
- **marp** (`~/.claude/skills/marp/SKILL.md`) - write a MARP Markdown slide deck from a topic, synthesis file, or content, then export to HTML/PPTX/PDF via local Marp CLI. Three themes: neon (Aurora Glass dark, default), light, corporate. Trigger: `/marp`
When the user types `/marp`, invoke the Skill tool with `skill: "marp"` before doing anything else.
- Also triggers on: "make marp slides", "marp deck", "marp presentation", "marp slides about"

# learn-anything
- **learn-anything** (`~/.claude/skills/learn-anything/SKILL.md`) - The Specificity Method: 5-step AI learning framework (articulate gap → decompose → verify → reconstruct → test). Works for any topic. Integrates 6 master learning prompts (Feynman, 80/20, Personal Tutor, Deep Research, Learn by Doing, Mastery & Feedback). Trigger: `/learn-anything`, `/specificity`, or `/idk`
When the user types `/learn-anything`, `/specificity`, or `/idk`, invoke the Skill tool with `skill: "learn-anything"` before doing anything else.
- Also triggers on: "I don't know what I don't know about", "teach me", "help me understand", "I'm stuck on"

# graphify
- **graphify** (`~/.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, invoke the Skill tool with `skill: "graphify"` before doing anything else.

# affiliate-workflow
- **affiliate-workflow** (`~/.claude/skills/affiliate-workflow/SKILL.md`) - end-to-end AI affiliate marketing pipeline. Trigger: `/affiliate-workflow`
When the user types `/affiliate-workflow`, invoke the Skill tool with `skill: "affiliate-workflow"` before doing anything else.


# ai-graphics
- **ai-graphics** (`~/.claude/skills/ai-graphics/SKILL.md`) - design-first AI graphics via local OmniRoute: infographics, flyers, whiteboard visuals, social cards for LinkedIn/Twitter/Instagram. Writes a DESIGN SPEC, then renders via codex gpt-image (typography) or nvidia FLUX (illustration). Trigger: `/ai-graphics`
When the user types `/ai-graphics`, invoke the Skill tool with `skill: "ai-graphics"` before doing anything else.
- Also triggers on: "make an infographic", "create a flyer", "social card for", "whiteboard graphic", "recreate this image", "image for LinkedIn/Twitter"

# proposal
- **proposal** (`~/.claude/commands/proposal.md`) - present a pre-built business proposal for any scored SMB vertical (Real Estate, Dental, E-Commerce, Accounting, Marketing Agencies, Law Firms, Med Spas, HVAC/Plumbing). Includes Gamma slide deck link. Trigger: `/proposal <vertical>`
When the user types `/proposal`, read `~/.claude/commands/proposal.md` and execute its Workflow inline. Do not invoke the Skill tool.
- Also triggers on: "show me the proposal for", "pull up the proposal", "business proposal for"

# openhands-niche-agency
- **openhands-niche-agency** (`~/.claude/skills/openhands-niche-agency/SKILL.md`) - full business-model kit for the "Done-For-You AI Engineering Team" micro-agency: niche → vertical score → top 5 use cases → pricing → tech stack → AGENTS.md → landing page → 7-day GTM plan. Monetization model: OpenHands + subagents + 14k MCPs, $2k–$5k/mo per SMB client. Trigger: `/openhands-niche-agency`
When the user types `/openhands-niche-agency`, invoke the Skill tool with `skill: "openhands-niche-agency"` before doing anything else.
- Also triggers on: "done-for-you AI engineering", "ai engineering team for", "smb ai agency", "openhands agency"

# gcc-roadmap
- **gcc-roadmap** (`~/.claude/skills/gcc-roadmap/SKILL.md`) - generate a 17-slide GCC Implementation Roadmap deck (time-phased: Sprint → Transformation → Partnership) × capability-layered (Modernize → Activate → Innovate). Standalone or as Stage 3 of ikigai-gamma-slidedeck for BD/company-first profiles. Trigger: `/gcc-roadmap`
When the user types `/gcc-roadmap`, invoke the Skill tool with `skill: "gcc-roadmap"` before doing anything else.
- Also triggers on: "implementation roadmap", "gcc roadmap deck", "what happens after yes", "delivery roadmap"

# ikigai-gamma-slidedeck
- **ikigai-gamma-slidedeck** (`~/.claude/skills/ikigai-gamma-slidedeck/SKILL.md`) - compound pipeline: LinkedIn profile (PDF/URL/text) → Ikigai Pro Report (7 stages) → Gamma slide deck via Gamma MCP (primary) or branded pptxkit .pptx (fallback). Optional Stage 3: gcc-roadmap deck for BD/company-first profiles. Reusable for any person. Auto-detects framing: BD/company-first vs solo-founder-first. Trigger: `/ikigai-gamma-slidedeck`
When the user types `/ikigai-gamma-slidedeck`, invoke the Skill tool with `skill: "ikigai-gamma-slidedeck"` before doing anything else.
- Also triggers on: "run ikigai for <name>", "ikigai slide deck for <name>", "linkedin to slides"

# ikigai
- **ikigai** (`~/.claude/skills/ikigai/SKILL.md`) - run a full Ikigai Pro solo-founder or BD analysis from any LinkedIn profile (PDF, URL, or text). Produces a structured report: 4 columns, niche statement, validation score, competitor landscape, offer architecture, income math, 7-day launch plan. For report only (no deck). Trigger: `/ikigai`
When the user types `/ikigai`, invoke the Skill tool with `skill: "ikigai"` before doing anything else.
- Use `ikigai-gamma-slidedeck` instead when the user also wants a slide deck in the same run.

# branded-pptx-deck
- **branded-pptx-deck** (`~/.claude/skills/branded-pptx-deck/SKILL.md`) - build polished, branded, editable PowerPoint (.pptx) decks from data/outline via python-pptx (executive summaries, storyboards, KPI/scorecard slides, charts, use-case realization layouts). Trigger: `/branded-pptx-deck`
When the user types `/branded-pptx-deck`, invoke the Skill tool with `skill: "branded-pptx-deck"` before doing anything else.
- Prefer this skill (not `presentation`) whenever the desired output is a `.pptx` file rather than the HTML deck.

# grill-me
- **grill-me** (`~/.claude/skills/grill-me/SKILL.md`) - relentlessly interview the user about a plan, design, or topic, checkpointing every answer to a brainstorm file. Trigger: `/grill-me`
When the user types `/grill-me`, invoke the Skill tool with `skill: "grill-me"` before doing anything else.

# presales-deal-prep
- **presales-deal-prep** (`~/.claude/skills/presales-deal-prep/SKILL.md`) - end-to-end pre-sales pipeline: research a prospect, generate AI strategy brief, review contract terms, prep for the meeting with objection scripts. Trigger: `/presales-deal-prep`
When the user types `/presales-deal-prep`, invoke the Skill tool with `skill: "presales-deal-prep"` before doing anything else.

# ai-strategy-researcher
- **ai-strategy-researcher** (`~/gstack/ai-strategy-researcher/SKILL.md`) - deep AI strategy research on a topic, vertical, or market. Trigger: `/ai-strategy-researcher`
When the user types `/ai-strategy-researcher`, invoke the Skill tool with `skill: "ai-strategy-researcher"` before doing anything else.

# ai-strategy-brief
- **ai-strategy-brief** (`~/.claude/skills/ai-strategy-brief/SKILL.md`) - produce a concise AI strategy one-pager from a topic or research inputs. Trigger: `/ai-strategy-brief`
When the user types `/ai-strategy-brief`, invoke the Skill tool with `skill: "ai-strategy-brief"` before doing anything else.

# content-research
- **content-research** (`~/.claude/skills/content-research/SKILL.md`) - ingest any content (YouTube, LinkedIn, GitHub, web) → analyze → Obsidian second brain → knowledge graph. Trigger: `/content-research`
When the user types `/content-research`, invoke the Skill tool with `skill: "content-research"` before doing anything else.

# 00-account-briefing
- **00-account-briefing** (`~/.claude/skills/00-account-briefing/SKILL.md`) - generate a one-page pre-meeting briefing for an enterprise account. Trigger: `/00-account-briefing` or "brief me on <account>" or "prep for the <account> call"
When the user types `/00-account-briefing`, invoke the Skill tool with `skill: "00-account-briefing"` before doing anything else.

# competitive-intel-sprint
- **competitive-intel-sprint** (`~/.claude/skills/competitive-intel-sprint/SKILL.md`) - end-to-end pipeline: watch competitor's demo, extract insights, produce competitive analysis. Trigger: `/competitive-intel-sprint`
When the user types `/competitive-intel-sprint`, invoke the Skill tool with `skill: "competitive-intel-sprint"` before doing anything else.

# ai-analyst
- **ai-analyst** (`~/.claude/skills/ai-analyst/SKILL.md`) - AI-powered product analytics: ask a business question in plain English, get validated findings, charts, and a slide deck. Trigger: `/analyze` or any data/metrics/analytics question
When the user types `/analyze`, invoke the Skill tool with `skill: "analyze"` before doing anything else.


# contract-reviewer
- **contract-reviewer** (`~/.claude/skills/contract-reviewer/SKILL.md`) - review any contract and flag what matters before signing (NDAs, freelance contracts, leases, agreements). Trigger: `/contract-reviewer` or "review this contract"
When the user types `/contract-reviewer`, invoke the Skill tool with `skill: "contract-reviewer"` before doing anything else.

# difficult-conversation-prep
- **difficult-conversation-prep** (`~/.claude/skills/difficult-conversation-prep/SKILL.md`) - prepare for tough conversations with scripts, talking points, and responses to likely pushback. Trigger: `/difficult-conversation-prep`
When the user types `/difficult-conversation-prep`, invoke the Skill tool with `skill: "difficult-conversation-prep"` before doing anything else.

# watch
- **watch** (`~/.claude/skills/watch/SKILL.md`) - watch a video (URL or local path): download, extract frames, get transcript, answer questions about the video. Trigger: `/watch`
When the user types `/watch`, invoke the Skill tool with `skill: "watch"` before doing anything else.

# firecrawl
- **firecrawl** (`~/.claude/skills/firecrawl/SKILL.md`) - web scraping and crawling via Firecrawl API. Trigger: `/firecrawl`
When the user types `/firecrawl`, invoke the Skill tool with `skill: "firecrawl"` before doing anything else.

# architecture-to-everything
- **architecture-to-everything** (`~/.claude/skills/architecture-to-everything/SKILL.md`) - orchestrator: system description → draw.io diagram + architecture doc + pptx deck + interactive HTML + NotebookLM. Trigger: `/architecture-to-everything`
When the user types `/architecture-to-everything`, invoke the Skill tool with `skill: "architecture-to-everything"` before doing anything else.

# drawio
- **drawio** (`~/.claude/skills/drawio/SKILL.md`) - generate draw.io component-flow diagrams from system descriptions. Trigger: `/drawio`
When the user types `/drawio`, invoke the Skill tool with `skill: "drawio"` before doing anything else.

# architecture-presentation
- **architecture-presentation** (`~/.claude/skills/architecture-presentation/SKILL.md`) - generate architecture explanation doc + slide deck from a diagram or system description. Trigger: `/architecture-presentation`
When the user types `/architecture-presentation`, invoke the Skill tool with `skill: "architecture-presentation"` before doing anything else.

# workflow-visualizer
- **workflow-visualizer** (`~/.claude/skills/workflow-visualizer/SKILL.md`) - map any system or workflow as an interactive HTML diagram with clickable nodes and hover details. Trigger: `/workflow-visualizer`
When the user types `/workflow-visualizer`, invoke the Skill tool with `skill: "workflow-visualizer"` before doing anything else.

# notebooklm
- **notebooklm** (`~/.claude/skills/notebooklm/SKILL.md`) - open NotebookLM in Chrome, create a notebook, upload docs, generate briefing doc and Q&A. Trigger: `/notebooklm`
When the user types `/notebooklm`, invoke the Skill tool with `skill: "notebooklm"` before doing anything else.

# strategy-consulting
- **strategy-consulting** (`~/.claude/skills/strategy-consulting/SKILL.md`) - 21 Accenture-style consulting frameworks across 6 domains: diagnosis & framing, market & competitive intel, strategic choice & economics, operating model & execution, risk/performance/value governance, alignment & executive communication. Trigger: `/strategy-consulting` (orchestrator) or any individual skill trigger below.
When the user types `/strategy-consulting`, invoke the Skill tool with `skill: "strategy-consulting"` before doing anything else.

Individual skill triggers — each reads the corresponding `.md` from `~/.claude/skills/strategy-consulting/skills/` and executes the workflow:
- `/situation-assessment` → `01-diagnosis-and-framing/situation-assessment.md`
- `/growth-barriers` → `01-diagnosis-and-framing/growth-barriers.md`
- `/assumption-audit` → `01-diagnosis-and-framing/assumption-audit.md`
- `/market-mapping` → `02-market-and-competitive-intelligence/market-mapping.md`
- `/competitive-intel` → `02-market-and-competitive-intelligence/competitive-intel.md`
- `/customer-segmentation` → `02-market-and-competitive-intelligence/customer-segmentation.md`
- `/profit-pool-analysis` → `02-market-and-competitive-intelligence/profit-pool-analysis.md`
- `/strategic-options` → `03-strategic-choice-and-economics/strategic-options.md`
- `/business-case-builder` → `03-strategic-choice-and-economics/business-case-builder.md`
- `/portfolio-review` → `03-strategic-choice-and-economics/portfolio-review.md`
- `/pricing-strategy` → `03-strategic-choice-and-economics/pricing-strategy.md`
- `/operating-model-design` → `04-operating-model-and-execution/operating-model-design.md`
- `/transformation-roadmap` → `04-operating-model-and-execution/transformation-roadmap.md`
- `/initiative-prioritizer` → `04-operating-model-and-execution/initiative-prioritizer.md`
- `/kpi-architect` → `05-risk-performance-and-value-governance/kpi-architect.md`
- `/risk-and-mitigation` → `05-risk-performance-and-value-governance/risk-and-mitigation.md`
- `/value-realization` → `05-risk-performance-and-value-governance/value-realization.md`
- `/war-gaming` → `05-risk-performance-and-value-governance/war-gaming.md`
- `/decision-memo` → `06-alignment-and-executive-communication/decision-memo.md`
- `/narrative-builder` → `06-alignment-and-executive-communication/narrative-builder.md`
- `/stakeholder-alignment` → `06-alignment-and-executive-communication/stakeholder-alignment.md`

When the user types any of the individual skill triggers above, read the corresponding `.md` file from `~/.claude/skills/strategy-consulting/skills/` and execute its Workflow and Output Format on the user's context. Do not invoke the Skill tool — read the file directly and run the skill inline.

# solution-delivery
- **solution-delivery** (`~/.claude/skills/solution-delivery/SKILL.md`) - 13 implementation and realization frameworks that chain directly from strategy-consulting outputs: solution design, delivery governance, change management, and value realization. Trigger: `/solution-delivery` (orchestrator) or any individual skill trigger below.
When the user types `/solution-delivery`, invoke the Skill tool with `skill: "solution-delivery"` before doing anything else.

Individual skill triggers — each reads the corresponding `.md` from `~/.claude/skills/solution-delivery/skills/` and executes the workflow:
- `/solution-blueprint` → `01-solution-design/solution-blueprint.md`
- `/architecture-decision-record` → `01-solution-design/architecture-decision-record.md`
- `/integration-sequencing` → `01-solution-design/integration-sequencing.md`
- `/raid-log` → `02-delivery-governance/raid-log.md`
- `/stage-gate-review` → `02-delivery-governance/stage-gate-review.md`
- `/delivery-risk-assessment` → `02-delivery-governance/delivery-risk-assessment.md`
- `/raci-design` → `02-delivery-governance/raci-design.md`
- `/change-readiness-assessment` → `03-change-management/change-readiness-assessment.md`
- `/change-impact-assessment` → `03-change-management/change-impact-assessment.md`
- `/adoption-plan` → `03-change-management/adoption-plan.md`
- `/benefits-register` → `04-value-realization/benefits-register.md`
- `/post-implementation-review` → `04-value-realization/post-implementation-review.md`
- `/hypercare-plan` → `04-value-realization/hypercare-plan.md`

When the user types any of the individual skill triggers above, read the corresponding `.md` file from `~/.claude/skills/solution-delivery/skills/` and execute its Workflow and Output Format on the user's context. Do not invoke the Skill tool — read the file directly and run the skill inline.

# ai-transformation
- **ai-transformation** (`~/.claude/skills/ai-transformation/SKILL.md`) - 6 AI-specific consulting frameworks: maturity assessment, data readiness, use case prioritisation, AI operating model, responsible AI, and build-buy-partner. Chains between strategy-consulting and solution-delivery. Trigger: `/ai-transformation` (orchestrator) or individual skill triggers below.
When the user types `/ai-transformation`, invoke the Skill tool with `skill: "ai-transformation"` before doing anything else.

Individual skill triggers — each reads the corresponding `.md` from `~/.claude/skills/ai-transformation/skills/` and executes the workflow:
- `/ai-maturity-assessment` → `01-maturity-and-readiness/ai-maturity-assessment.md`
- `/data-readiness-assessment` → `01-maturity-and-readiness/data-readiness-assessment.md`
- `/ai-use-case-prioritiser` → `02-use-case-and-operating-model/ai-use-case-prioritiser.md`
- `/ai-operating-model` → `02-use-case-and-operating-model/ai-operating-model.md`
- `/responsible-ai-framework` → `03-governance-and-decisions/responsible-ai-framework.md`
- `/ai-build-buy-partner` → `03-governance-and-decisions/ai-build-buy-partner.md`

When the user types any of the individual skill triggers above, read the corresponding `.md` file from `~/.claude/skills/ai-transformation/skills/` and execute its Workflow and Output Format on the user's context. Do not invoke the Skill tool — read the file directly and run the skill inline.

# engagement-management
- **engagement-management** (`~/.claude/skills/engagement-management/SKILL.md`) - 6 consulting engagement management frameworks: win strategy, commercial structuring, kick-off, stakeholder cadence, progress reporting, and closeout. Runs across all engagement phases. Trigger: `/engagement-management` (orchestrator) or individual skill triggers below.
When the user types `/engagement-management`, invoke the Skill tool with `skill: "engagement-management"` before doing anything else.

Individual skill triggers — each reads the corresponding `.md` from `~/.claude/skills/engagement-management/skills/` and executes the workflow:
- `/win-strategy` → `01-pursuit/win-strategy.md`
- `/commercial-structuring` → `01-pursuit/commercial-structuring.md`
- `/engagement-kickoff` → `02-delivery/engagement-kickoff.md`
- `/stakeholder-cadence` → `02-delivery/stakeholder-cadence.md`
- `/progress-reporting` → `02-delivery/progress-reporting.md`
- `/engagement-closeout` → `03-closeout/engagement-closeout.md`

When the user types any of the individual skill triggers above, read the corresponding `.md` file from `~/.claude/skills/engagement-management/skills/` and execute its Workflow and Output Format on the user's context. Do not invoke the Skill tool — read the file directly and run the skill inline.

# continuous-improvement
- **continuous-improvement** (`~/.claude/skills/continuous-improvement/SKILL.md`) - 5 post-delivery consulting frameworks: operating rhythm design, performance review, CI backlog, capability maturity progression, and exit strategy. Closes the loop after solution-delivery. Trigger: `/continuous-improvement` (orchestrator) or individual skill triggers below.
When the user types `/continuous-improvement`, invoke the Skill tool with `skill: "continuous-improvement"` before doing anything else.

Individual skill triggers — each reads the corresponding `.md` from `~/.claude/skills/continuous-improvement/skills/` and executes the workflow:
- `/operating-rhythm-design` → `01-operations/operating-rhythm-design.md`
- `/performance-review` → `01-operations/performance-review.md`
- `/continuous-improvement-backlog` → `02-improvement/continuous-improvement-backlog.md`
- `/capability-maturity-progression` → `02-improvement/capability-maturity-progression.md`
- `/exit-strategy` → `03-transition/exit-strategy.md`

When the user types any of the individual skill triggers above, read the corresponding `.md` file from `~/.claude/skills/continuous-improvement/skills/` and execute its Workflow and Output Format on the user's context. Do not invoke the Skill tool — read the file directly and run the skill inline.

# ai-use-cases-consultant
- **ai-use-cases-consultant** (`~/.claude/skills/ai-use-cases-consultant/SKILL.md`) - enterprise AI use case scoping, realization pattern selection (RAG vs knowledge graph vs multi-agent vs Document AI), hyperscaler recommendation (GCP/AWS/Azure), and regulated-industry platform architecture (healthcare, FSI). Sourced from GCP 101 Blueprints, AWS Gen AI Atlas, Microsoft Azure Scenario Library. Trigger: `/ai-use-cases-consultant`
When the user types `/ai-use-cases-consultant`, invoke the Skill tool with `skill: "ai-use-cases-consultant"` before doing anything else.
- Also triggers on: "which hyperscaler for", "RAG vs knowledge graph", "enterprise AI platform architecture", "prior authorization AI", "AI use case ROI"

# founders-build-stack
- **founders-build-stack** (`content-ideas/.claude/skills/founders-build-stack/SKILL.md`) - 24-agent pipeline orchestrator (Founder's Build Stack by DataStaqAI): Problem Validator → ICP Definer → Scope Auditor → Build vs Buy → Feature Prioritizer → Timeline → Architecture → MVP build → Internal Tools → AI Workflows. Shared state via COMPANY.md. Stack defaults: Next.js 14+ / Supabase / Vercel / Stripe. Trigger: `/founders-build-stack`
When the user types `/founders-build-stack`, read `/home/sheke/content-ideas/.claude/skills/founders-build-stack/SKILL.md` and execute its workflow inline. Do not invoke the Skill tool.
- Also triggers on: "start a new SaaS build", "run the build stack", "founder's pipeline", "COMPANY.md"

# saas-replacement-auditor
- **saas-replacement-auditor** (`content-ideas/.claude/skills/saas-replacement-auditor/SKILL.md`) - classify a SaaS stack into 5 buckets (KEEP/REPLACE/CONSOLIDATE/NEGOTIATE/AUDIT USAGE), run 3-year build-vs-buy math for REPLACE candidates, produce Top 3 replacement plans and 12-month action plan. Trigger: `/saas-replacement-auditor`
When the user types `/saas-replacement-auditor`, read `/home/sheke/content-ideas/.claude/skills/saas-replacement-auditor/SKILL.md` and execute its workflow inline. Do not invoke the Skill tool.
- Also triggers on: "audit my SaaS stack", "what can I replace with my own build", "SaaS cost reduction", "build vs buy for my tools"

# ai-feature-integrator
- **ai-feature-integrator** (`content-ideas/.claude/skills/ai-feature-integrator/SKILL.md`) - end-to-end design for adding an AI feature: UI surface + data flow + failure handling + cost controls + observability. Outputs API route + React component + DB migration + smoke test. Trigger: `/ai-feature-integrator`
When the user types `/ai-feature-integrator`, read `/home/sheke/content-ideas/.claude/skills/ai-feature-integrator/SKILL.md` and execute its workflow inline. Do not invoke the Skill tool.
- Also triggers on: "add AI to my product", "integrate Claude into my app", "AI feature design", "rate limit my AI calls"
