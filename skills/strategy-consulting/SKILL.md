---
name: strategy-consulting
description: Use when someone asks to assess a business situation, map a market, build a competitive analysis, frame strategic options, construct a business case, design an operating model, run war gaming, write a decision memo, or apply any Accenture-style consulting framework. Also triggers on "strategy work", "consulting framework", "situation assessment", "competitive intel", "strategic options", "transformation roadmap", or when a user describes a strategic business problem that needs structured diagnosis and recommendation.
metadata:
  legacy-frontmatter:
    version: 1.0.0
    triggers:
    - /strategy-consulting
    - /situation-assessment
    - /growth-barriers
    - /assumption-audit
    - /market-mapping
    - /competitive-intel
    - /customer-segmentation
    - /profit-pool-analysis
    - /strategic-options
    - /business-case-builder
    - /portfolio-review
    - /pricing-strategy
    - /operating-model-design
    - /transformation-roadmap
    - /initiative-prioritizer
    - /kpi-architect
    - /risk-and-mitigation
    - /value-realization
    - /war-gaming
    - /decision-memo
    - /narrative-builder
    - /stakeholder-alignment
---

# strategy-consulting — 21 Accenture-Style Consulting Frameworks

## Narrative Frame

**This skill's job:** Produce the kind of output that changes the room when it lands on the table — not a framework summary, but a structured argument that forces a decision.

**Voice:** You are a senior partner who has run 50 of these engagements. You do not present all sides neutrally. You form a view, show your working, and defend it. Clients pay for judgment, not for balanced reports.

**Rules that apply to every framework in this suite:**
- **Situation:** The opening sentence is the problem, not the context. Not "Company X operates in a competitive market" → "Company X is losing 8 points of market share per year and the team doesn't have a shared diagnosis of why."
- **Analysis:** Every insight is a claim, not an observation. Not "Revenue has declined" → "Revenue declined 23% because the mid-market segment churned faster than enterprise expanded." Each claim is supported by one number or one named example.
- **Options:** Never list more than three. Rank them. Name the one you recommend and the reason you rejected the others.
- **Recommendation:** Action + owner + timeline + success metric. If any of those four are missing, the recommendation is not complete.
- **Executive communication (decision-memo, narrative-builder, stakeholder-alignment):** The first slide or paragraph contains the recommendation. Everything else is evidence. The reader should be able to stop after the first paragraph and know what to do.

**Anti-patterns across all 21 frameworks:**
- Balanced assessments with no recommendation
- Frameworks presented as academic structures rather than working tools
- Observations without claims ("revenue has been declining" → name the cause)
- Recommendations without named owners or dates

## When To Use

Any time you need to apply a structured consulting methodology:
- Strategy work (situation assessment, market analysis, competitive intel, strategic options)
- Financial and investment decisions (business case, portfolio review, pricing strategy)
- Execution planning (operating model design, transformation roadmap, initiative prioritization)
- Performance and risk governance (KPI architecture, risk register, value realization, war gaming)
- Executive communication (decision memo, narrative builder, stakeholder alignment)

## How To Invoke

**Single-skill invocation** (most common):
```
/situation-assessment  [context]
/war-gaming            [strategy to stress-test]
/business-case-builder [investment decision]
```

**Top-level with skill name**:
```
/strategy-consulting situation-assessment
/strategy-consulting war-gaming
```

**Without arguments** — Claude will ask which framework to apply.

## The 21 Skills

### Domain 1: Diagnosis & Framing
| Trigger | Skill | When to Use |
|---------|-------|-------------|
| `/situation-assessment` | [Situation Assessment](skills/01-diagnosis-and-framing/situation-assessment.md) | Business reviews, turnaround diagnosis, board prep |
| `/growth-barriers` | [Growth Barriers](skills/01-diagnosis-and-framing/growth-barriers.md) | Stalled growth, revenue plateau, funnel issues |
| `/assumption-audit` | [Assumption Audit](skills/01-diagnosis-and-framing/assumption-audit.md) | Board reviews, major investments, strategy pressure test |

### Domain 2: Market & Competitive Intelligence
| Trigger | Skill | When to Use |
|---------|-------|-------------|
| `/market-mapping` | [Market Mapping](skills/02-market-and-competitive-intelligence/market-mapping.md) | Market entry, expansion, TAM/SAM/SOM |
| `/competitive-intel` | [Competitive Intel](skills/02-market-and-competitive-intelligence/competitive-intel.md) | Market entry, pricing changes, product launches |
| `/customer-segmentation` | [Customer Segmentation](skills/02-market-and-competitive-intelligence/customer-segmentation.md) | ICP work, go-to-market focus, retention strategy |
| `/profit-pool-analysis` | [Profit Pool Analysis](skills/02-market-and-competitive-intelligence/profit-pool-analysis.md) | Market entry, product portfolio, channel strategy |

### Domain 3: Strategic Choice & Economics
| Trigger | Skill | When to Use |
|---------|-------|-------------|
| `/strategic-options` | [Strategic Options](skills/03-strategic-choice-and-economics/strategic-options.md) | Strategy choices, build-buy-partner decisions |
| `/business-case-builder` | [Business Case Builder](skills/03-strategic-choice-and-economics/business-case-builder.md) | Investment decisions, ROI/NPV, board cases |
| `/portfolio-review` | [Portfolio Review](skills/03-strategic-choice-and-economics/portfolio-review.md) | Capital allocation, where to invest or exit |
| `/pricing-strategy` | [Pricing Strategy](skills/03-strategic-choice-and-economics/pricing-strategy.md) | Price increases, discount leakage, packaging redesign |

### Domain 4: Operating Model & Execution
| Trigger | Skill | When to Use |
|---------|-------|-------------|
| `/operating-model-design` | [Operating Model Design](skills/04-operating-model-and-execution/operating-model-design.md) | Transformations, new BUs, functional redesigns |
| `/transformation-roadmap` | [Transformation Roadmap](skills/04-operating-model-and-execution/transformation-roadmap.md) | Transformation programs, digital transformation |
| `/initiative-prioritizer` | [Initiative Prioritizer](skills/04-operating-model-and-execution/initiative-prioritizer.md) | Annual planning, too many projects, OKR planning |

### Domain 5: Risk, Performance & Value Governance
| Trigger | Skill | When to Use |
|---------|-------|-------------|
| `/kpi-architect` | [KPI Architect](skills/05-risk-performance-and-value-governance/kpi-architect.md) | Metrics cleanup, dashboards, OKRs, performance management |
| `/risk-and-mitigation` | [Risk & Mitigation](skills/05-risk-performance-and-value-governance/risk-and-mitigation.md) | Strategy approval, launch risk, board risk review |
| `/value-realization` | [Value Realization](skills/05-risk-performance-and-value-governance/value-realization.md) | Transformation value, synergy capture, benefits tracking |
| `/war-gaming` | [War Gaming](skills/05-risk-performance-and-value-governance/war-gaming.md) | Strategy pressure test, competitive response, scenario planning |

### Domain 6: Alignment & Executive Communication
| Trigger | Skill | When to Use |
|---------|-------|-------------|
| `/decision-memo` | [Decision Memo](skills/06-alignment-and-executive-communication/decision-memo.md) | Board memos, investment recommendations |
| `/narrative-builder` | [Narrative Builder](skills/06-alignment-and-executive-communication/narrative-builder.md) | Board deck, strategy story, Pyramid Principle |
| `/stakeholder-alignment` | [Stakeholder Alignment](skills/06-alignment-and-executive-communication/stakeholder-alignment.md) | Executive buy-in, board approval, change management |

## Dispatch Logic

When this skill is invoked:

1. **Check the argument** — if a skill name was passed (e.g. `/war-gaming` or `/strategy-consulting war-gaming`), read that skill's `.md` file directly and execute it.

2. **No argument** — ask the user which domain they're working in, then which skill, then execute.

3. **Ambiguous** — if the user describes a problem ("I need to figure out why growth is stalling"), map it to the most relevant skill and confirm before proceeding.

**Execution**: Read the skill's `.md` file from `~/.claude/skills/strategy-consulting/skills/<domain>/<skill>.md`, load its Workflow and Output Format, and apply it to the user's context.

## Chaining

These skills chain naturally into `/branded-pptx-deck` for deliverable output:
- Run the consulting framework → produce structured findings
- Pass findings to `/branded-pptx-deck` to build the client-facing deck

They also chain into `/ai-strategy-researcher` (for market data) and `/grill-me` (to stress-test the strategy with follow-up questions).

## Skill Relationships

### Category
Runbook

### Dependencies
None — standalone suite. Individual sub-skill `.md` files must exist at `~/.claude/skills/strategy-consulting/skills/<domain>/<skill>.md`.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `solution-delivery` | Sequential downstream | Always — strategy outputs become implementation inputs | Strategy findings doc / decision memo |
| `ai-transformation` | Sequential downstream | When strategy reveals AI capability gaps | `/situation-assessment` findings → `/ai-maturity-assessment` |
| `engagement-management` | Sequential downstream | When engagement is being won or run | `/strategic-options` → `/win-strategy` → `/engagement-kickoff` |
| `continuous-improvement` | Sequential downstream (indirect) | Post-delivery cycle restart | `/situation-assessment` (next cycle) |
| `ai-strategy-researcher` | Sequential upstream | When market data or competitive signals are needed | Research brief → strategy framework inputs |
| `branded-pptx-deck` | Amplifier | When client-facing deck is needed from findings | Structured findings → `.pptx` deck |
| `grill-me` | Amplifier | To stress-test the strategy before delivery | Strategy draft → challenge session |

### Full Lifecycle Chain
strategy-consulting → engagement-management → ai-transformation → solution-delivery → continuous-improvement

### Runtime Preamble
At invocation, surface this if the user hasn't named a downstream step:
"Strategy outputs typically feed into `/solution-delivery` (implementation), `/ai-transformation` (AI capability gaps), or `/engagement-management` (if this is a client engagement). Run `/branded-pptx-deck` when you need a client-facing deck from findings."

## Gotchas

- **Description was human-facing, not trigger-focused:** The original description summarised the skill for humans. Updated to describe trigger conditions for the model.
- **Never present frameworks academically:** Each framework should produce a claim + evidence + recommendation, not a summary of the framework structure. The model must execute the framework, not explain it.
- **Sub-skill files must exist:** This orchestrator reads `.md` files from `skills/<domain>/<skill>.md` at execution time. If a file is missing, the skill fails silently — check the path before claiming a skill ran.
- **Don't chain blindly:** Strategy outputs are only useful downstream if they include a recommendation, named owner, and date. Findings without a verdict cannot be handed off to solution-delivery.
- **Argument routing:** `/strategy-consulting war-gaming` and `/war-gaming` both work but dispatch differently — the top-level route must still read the sub-skill `.md` file; don't execute from memory.
- **Grill-me is optional, not automatic:** Run `/grill-me` only when the user wants to stress-test before delivery, not as a default step.

## Source / Tool Order

For strategy, market, competitor, roadmap, and business-case work, use wired
research dependencies before generic search:

1. Read local artifacts, user-provided context, prior briefs, and relevant
   strategy skill outputs.
2. Run GBrain recall when available for the company, market, competitors,
   recurring prospects, and prior strategy research.
3. Use `you-com-search`, Hermes `web.search_backend: you`, or an equivalent
   You.com wrapper for current-web discovery, livecrawl, research, and finance
   research.
4. Use Exa for semantic/source discovery and Firecrawl for full-page capture
   after candidate URLs are known.
5. Use specialist MCPs/plugins for official docs, GitHub, financial data,
   regulatory sources, or internal docs when available.
6. Use generic WebSearch/search_web only when the above routes are unavailable
   or return no useful signal.

## Automated Deck Pipeline (findings.json → branded .pptx)

Before compilation, apply `pptx-visual-spec`, create and validate
`<run>/visual-spec.json`, and pass it with `findings.json` to the selected direct builder.
Strategy data and claims remain native; this orchestration layer never selects an image
provider directly.

For an end-to-end "question → client-ready deck" run, after executing the chosen
framework (above), serialize its output into the Universal Findings Schema and
compile it with the bundled `compile.py`. Use this when the user wants a deck
artifact, not just analysis.

**5-step pipe:**
1. **Route** — confirm the framework (the 21 above). With no argument, ask which domain/skill.
2. **Fact-gather** — pull market signals / competitor data with your research tools (follow the global Research Tool Order: GBrain recall → You.com / `you-com-search` → Exa → Firecrawl → …).
3. **Synthesize** — apply the senior-partner voice frame: Context → Tension → Resolution. Every finding is a claim backed by one number or one named example.
4. **Format** — read the chosen sub-skill `.md` for its exact Output Format, then map the narrative into `findings.json` (schema below).
5. **Compile** — generate the branded deck:

```bash
# python-pptx is in the base env; falls back to: uv run --with python-pptx python ...
python3 ~/.claude/skills/branded-pptx-deck/scripts/compile.py \
  findings.json \
  "${BRANDED_PPTX_TEMPLATE:-$HOME/.claude/skills/branded-pptx-deck/resources/template.pptx}" \
  <Company>-<Domain>-Deck.pptx
```

**Universal Findings Schema** (`findings.json`) — `slides[].type` ∈ `table | split | bullets | quotes_grid`:

```json
{
  "company": "TargetCompany",
  "domain": "NAME OF FRAMEWORK",
  "headline": "Declarative claim here",
  "executive_read": "2-3 sentence executive summary",
  "key_findings": ["Finding 1", "Finding 2", "Finding 3", "Finding 4"],
  "slides": [
    { "type": "table",  "title": "Fact Base", "headers": ["Col 1","Col 2","Col 3"], "rows": [["R1C1","R1C2","R1C3"]] },
    { "type": "split",  "title": "Options vs Trade-offs", "left_title": "LEFT", "left_bullets": ["Point 1"], "right_title": "RIGHT", "right_bullets": ["Point A"] },
    { "type": "bullets", "title": "Recommendation", "bullets": ["Action + owner + date 1","..."] },
    { "type": "quotes_grid", "title": "Raw OSINT Quotes", "quotes": ["Q1","Q2","Q3","Q4","Q5","Q6"] }
  ]
}
```

**Delivery-gate caveat (project rule):** `compile.py` is the *fast automation* path
and renders its own dark teal theme. For **client-facing** decks the project's PPTX
QA gate still applies — prefer the branded `pptxkit.py` workflow + `preview_pptx.py`
visual review, set `BRANDED_PPTX_TEMPLATE`, and use `draft`/`reviewed`/`blocked`
status suffixes. Don't ship a `compile.py` deck to `CLIENT_DELIVERY_DIR` as final
without that review.
