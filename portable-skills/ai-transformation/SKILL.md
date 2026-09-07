---
name: ai-transformation
description: Use when someone asks to assess AI maturity, evaluate data readiness for AI, prioritise an AI use case portfolio, design an AI operating model or CoE, build a responsible AI framework, or decide whether to build, buy, or partner on an AI capability. Also triggers on "AI maturity", "AI readiness", "AI use cases", "AI governance", "responsible AI", "AI CoE", "AI operating model", or when strategy-consulting has flagged AI capability gaps that need a dedicated AI track.
version: 1.0.0
triggers:
  - /ai-transformation
  - /ai-maturity-assessment
  - /data-readiness-assessment
  - /ai-use-case-prioritiser
  - /ai-operating-model
  - /responsible-ai-framework
  - /ai-build-buy-partner
---

# ai-transformation — 6 AI Strategy Frameworks

## When To Use

Use for any AI strategy engagement where the generic strategy-consulting frameworks are insufficient — when the question is specifically about AI maturity, use case selection, AI operating model design, or AI governance.

## The 6 Skills

### Domain 1 — Maturity & Readiness
| Trigger | When to Use |
|---|---|
| `/ai-maturity-assessment` | Start of engagement — score org across data/tech/talent/governance/culture |
| `/data-readiness-assessment` | Before committing to use cases — assess data fitness per use case |

### Domain 2 — Use Case & Operating Model
| Trigger | When to Use |
|---|---|
| `/ai-use-case-prioritiser` | Long list of use cases → funded, sequenced portfolio |
| `/ai-operating-model` | Org ready to industrialise — design CoE / federated / embedded / hybrid |

### Domain 3 — Governance & Decisions
| Trigger | When to Use |
|---|---|
| `/responsible-ai-framework` | Pre-deployment — define principles, risk tiers, governance, guardrails |
| `/ai-build-buy-partner` | Capability sourcing decisions — make vs buy vs partner per capability |

## Chain Position

```
strategy-consulting                    ai-transformation
───────────────────────────────────────────────────────
/situation-assessment       →  /ai-maturity-assessment
/strategic-options          →  /ai-use-case-prioritiser → /ai-build-buy-partner
/operating-model-design     →  /ai-operating-model
/risk-and-mitigation        →  /responsible-ai-framework
                                       ↓
                              solution-delivery
                              /solution-blueprint
                              /transformation-roadmap
```

## Dispatch Logic

1. Individual trigger (e.g. `/ai-maturity-assessment`) — read `skills/01-maturity-and-readiness/ai-maturity-assessment.md` and execute inline.
2. Top-level with argument (e.g. `/ai-transformation ai-operating-model`) — same as above.
3. No argument — ask which domain, then which skill, then execute.

**Execution**: Read skill `.md` from `~/.claude/skills/ai-transformation/skills/<domain>/<skill>.md`, load its Workflow and Output Format, apply to user context. Do not invoke Skill tool — run inline.

## Chaining Out

- `/ai-use-case-prioritiser` findings → `/solution-blueprint` to design the delivery
- `/ai-operating-model` → `/raci-design` to assign accountability
- `/responsible-ai-framework` → `/risk-and-mitigation` for the full risk register
- `/ai-build-buy-partner` → `/commercial-structuring` for vendor pricing

## Skill Relationships

### Category
Business Automation

### Dependencies
None — standalone suite. Sub-skill `.md` files must exist at `~/.claude/skills/ai-transformation/skills/<domain>/<skill>.md`.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `strategy-consulting` | Sequential upstream | Always — AI transformation follows strategy gap identification | `/situation-assessment` or `/strategic-options` findings |
| `solution-delivery` | Sequential downstream | AI use cases → implementation | `/ai-use-case-prioritiser` output → `/solution-blueprint` |
| `solution-delivery` | Peer (parallel track) | AI-specific delivery track runs alongside general delivery | AI operating model → `/raci-design` |
| `engagement-management` | Peer (parallel governance) | Engagement-management governs how the AI transformation programme is run | Progress reports / governance cadence |
| `continuous-improvement` | Sequential downstream (indirect) | Post-deployment AI capability maturity | `/ai-maturity-assessment` (re-run annually) |
| `ai-use-cases-consultant` | Alternative / Peer | Deeper enterprise use case scoping with hyperscaler architecture | When client needs GCP/AWS/Azure platform recommendations |
| `branded-pptx-deck` | Amplifier | Client-facing AI strategy deck | Maturity assessment + use case priorities → `.pptx` |
| `pptx-visual-spec` | Behavioral overlay | Any client-facing AI strategy PPTX | `<run>/visual-spec.json` |
| `commercial-structuring` | Sequential downstream | AI build-buy-partner decision → vendor negotiation | `/ai-build-buy-partner` → `/commercial-structuring` |

### Full Lifecycle Chain
strategy-consulting → engagement-management → ai-transformation → solution-delivery → continuous-improvement

### Runtime Preamble
At invocation, surface this if the user hasn't named an upstream step:
"AI transformation sits between strategy diagnosis and delivery. Have you run `/situation-assessment` or `/strategic-options` yet? Those outputs identify where AI can move the needle. After prioritising use cases here, hand off to `/solution-delivery` with `/solution-blueprint`."

## Gotchas

- **Maturity assessment first, use cases second:** Running `/ai-use-case-prioritiser` before `/ai-maturity-assessment` produces a use case list the organisation cannot execute. Maturity gaps define the execution ceiling.
- **Data readiness gates use case selection:** `/data-readiness-assessment` must run before committing to specific use cases — a use case with no data pipeline is not a use case, it's a project. Don't let clients skip this step.
- **Responsible AI is pre-deployment, not post-deployment:** `/responsible-ai-framework` must be defined before building, not after a model is in production. Retrofitting governance is expensive and often incomplete.
- **AI operating model design is not org chart design:** `/ai-operating-model` decides CoE vs federated vs embedded vs hybrid — it is a structural, cultural, and investment decision. Don't conflate it with IT org design.
- **ai-use-cases-consultant is a peer, not a duplicate:** When the client needs hyperscaler-specific architecture (GCP/AWS/Azure), use `/ai-use-cases-consultant` instead of or alongside `/ai-use-case-prioritiser`. They are complementary, not redundant.
- **Sub-skill files must exist at the documented path:** The dispatch reads `.md` files at runtime. Verify `~/.claude/skills/ai-transformation/skills/<domain>/<skill>.md` exists before running.
For a PPTX handoff, create and validate `<run>/visual-spec.json` before invoking the deck
builder. Maturity scores, use-case priorities, architectures, and evidence never route to an
image model.
