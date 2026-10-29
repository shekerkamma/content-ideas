---
name: engagement-management
description: Use when someone needs to win, kick off, govern, or close a consulting engagement — writing a win strategy, structuring fees and commercials, designing the kickoff agenda, building the stakeholder cadence, producing progress RAG reports, or running a clean closeout. Also triggers on "win strategy", "proposal strategy", "commercial structuring", "engagement kickoff", "stakeholder cadence", "progress report", "RAG dashboard", "engagement closeout", or when a user is preparing to pursue or start running a consulting engagement.
metadata:
  legacy-frontmatter:
    version: 1.0.0
    triggers:
    - /engagement-management
    - /win-strategy
    - /commercial-structuring
    - /engagement-kickoff
    - /stakeholder-cadence
    - /progress-reporting
    - /engagement-closeout
---

# engagement-management — 6 Engagement Management Frameworks

## When To Use

Use across the full consulting engagement lifecycle — from qualifying and winning the work through delivery and closeout. These skills run in parallel with strategy-consulting and solution-delivery; they govern how the engagement operates, not what it produces.

## The 6 Skills

### Domain 1 — Pursuit
| Trigger | When to Use |
|---|---|
| `/win-strategy` | Opportunity qualified — define competitive positioning before proposal writing |
| `/commercial-structuring` | Win strategy set — design the fee model, margin analysis, negotiation brief |

### Domain 2 — Delivery
| Trigger | When to Use |
|---|---|
| `/engagement-kickoff` | Week before start — agenda, governance, ways of working, 30-day plan |
| `/stakeholder-cadence` | Kick-off — design steering / working group / sponsor 1:1 meeting architecture |
| `/progress-reporting` | Weekly / monthly — RAG dashboard, milestone tracker, decisions needed |

### Domain 3 — Closeout
| Trigger | When to Use |
|---|---|
| `/engagement-closeout` | Final 2 weeks — deliverable sign-off, client satisfaction, reference case, follow-on |

## Chain Position

```
engagement-management runs ACROSS all other packs:

/win-strategy → /commercial-structuring  (before engagement starts)
      ↓
/engagement-kickoff → /stakeholder-cadence  (Day 1)
      ↓
/progress-reporting  (every week/month throughout)
   ↕
[strategy-consulting + ai-transformation + solution-delivery running in parallel]
      ↓
/engagement-closeout  (final 2 weeks)
      ↓
continuous-improvement  (post-exit)
```

## Dispatch Logic

1. Individual trigger (e.g. `/win-strategy`) — read `skills/01-pursuit/win-strategy.md` and execute inline.
2. Top-level with argument — same as above.
3. No argument — ask which phase (Pursuit / Delivery / Closeout), then which skill, then execute.

**Execution**: Read skill `.md` from `~/.claude/skills/engagement-management/skills/<domain>/<skill>.md`, load its Workflow and Output Format, apply to user context. Do not invoke Skill tool — run inline.

## Chaining Out

- `/win-strategy` → `/narrative-builder` (strategy-consulting) to build the proposal narrative
- `/commercial-structuring` → `/business-case-builder` (strategy-consulting) for client ROI framing
- `/stakeholder-cadence` → `/stakeholder-alignment` (strategy-consulting) for exec alignment
- `/engagement-closeout` → `/post-implementation-review` (solution-delivery) for the final value read

## Skill Relationships

### Category
Business Automation

### Dependencies
None — standalone suite. Sub-skill `.md` files must exist at `~/.claude/skills/engagement-management/skills/<domain>/<skill>.md`.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `strategy-consulting` | Sequential upstream | Win strategy requires a strategy diagnosis first | `/situation-assessment` or `/strategic-options` → `/win-strategy` |
| `strategy-consulting` | Peer (parallel) | Strategy frameworks run in parallel during delivery — engagement-management governs the arc | Governance cadence wraps strategy outputs |
| `solution-delivery` | Sequential downstream | Engagement management governs the delivery programme | `/engagement-kickoff` → `/solution-blueprint` |
| `solution-delivery` | Peer (parallel governance) | Progress reporting wraps solution-delivery milestones | RAG dashboard aligned to delivery stage gates |
| `ai-transformation` | Peer (parallel governance) | Same — engagement-management wraps AI transformation delivery | Progress reports / steering cadence |
| `continuous-improvement` | Sequential downstream | Closeout hands off to post-delivery rhythm | `/engagement-closeout` → `/operating-rhythm-design` |
| `narrative-builder` | Sequential downstream | Win strategy → proposal narrative | `/win-strategy` → `/narrative-builder` |
| `post-implementation-review` | Sequential downstream | Closeout triggers final value read | `/engagement-closeout` → `/post-implementation-review` |

### Full Lifecycle Chain
strategy-consulting → engagement-management → ai-transformation → solution-delivery → continuous-improvement

### Runtime Preamble
At invocation, surface this if the user hasn't named a phase:
"Engagement management governs the full engagement arc — from winning the work to closing it out. It runs in parallel with strategy-consulting, ai-transformation, and solution-delivery. Which phase are you in? Pursuit (win-strategy, commercial-structuring), Delivery (kickoff, cadence, progress reporting), or Closeout?"

## Gotchas

- **Engagement-management governs, not produces:** This suite is about how the engagement is run — not about the strategy or solution content. Do not conflate `/stakeholder-cadence` with `/stakeholder-alignment` (strategy-consulting). They are different tools for different jobs.
- **Win strategy before proposal writing:** `/win-strategy` must run before any proposal or narrative is written. Jumping to `/narrative-builder` without a win strategy produces a generic deck with no competitive positioning.
- **Commercial structuring is not pricing:** `/commercial-structuring` covers fee model design, margin analysis, risk allocation, and negotiation brief — not just the rate card. Treat it as the financial architecture of the engagement.
- **Progress reporting is not status updates:** `/progress-reporting` produces a RAG dashboard with decisions-needed and escalations, not a bullet list of what the team did. If there are no decisions or escalations, the report format still applies.
- **Closeout is not a formality:** `/engagement-closeout` covers deliverable sign-off, client satisfaction measurement, reference case capture, and follow-on scoping. Skipping it leaves revenue and IP on the table.
- **Sub-skill files must exist at the documented path:** The dispatch reads `.md` files at runtime. Verify `~/.claude/skills/engagement-management/skills/<domain>/<skill>.md` exists before running.
