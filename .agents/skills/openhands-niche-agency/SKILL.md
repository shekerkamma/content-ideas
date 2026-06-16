---
name: openhands-niche-agency
description: >
  Full business-model kit for the "Done-For-You AI Engineering Team" micro-agency
  model. Takes a niche (real estate, dental, law, etc.) and produces: validated
  vertical score, top 5 use cases, pricing tiers, tech stack blueprint, AGENTS.md
  template, landing page copy, and 7-day first-client plan. Monetization focus —
  designed to generate $2k–$5k/mo per client running OpenHands + subagents + MCPs.
triggers:
  - openhands-niche-agency
  - done-for-you AI engineering
  - ai engineering team for
  - smb ai agency
  - openhands agency
version: "1.0"
validated_on: "runs/2026-06-16-openhands-smb-use-cases (8 verticals scored, 25 use cases, 3 RE pitches)"
chained_from: "standalone — or chain output into ikigai-gamma-slidedeck for personal BD positioning"
---

# openhands-niche-agency

Builds a complete "Done-For-You AI Engineering Team" business-model kit for any
SMB niche. One person can run this. Two-person team scales to $50k/mo.

**The model in one line:** Self-host OpenHands + specialist subagents + 14k+ MCP
servers → sell as a managed AI engineering team to SMBs at $2k–$5k/month.

## When To Use

- User wants to start or evaluate the OpenHands micro-agency model for a specific niche
- User asks "how do I build an AI engineering team for [niche]"
- After a `/vertical-scorer` or `/ikigai` run that surfaces an SMB niche as a GO
- User wants landing page copy, AGENTS.md, or pricing for this model

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| `niche` | Yes | e.g. "real estate brokerages", "dental practices", "law firms" |
| `operator_name` | Optional | e.g. "Srikumar V R" — for personalizing the AGENTS.md + launch plan |
| `existing_research` | Optional | Path to prior vertical score or use-case file if already run |

## Outputs

All artifacts land in `runs/YYYY-MM-DD-<niche>-openhands-agency/`:

| File | Description |
|---|---|
| `vertical-score.md` | Niche score (load from cache or generate) |
| `top-5-use-cases.md` | Top 5 use cases for the niche with full structured details |
| `business-model.md` | Pricing tiers + positioning + objection handling |
| `tech-stack.md` | OpenHands + subagents + MCP server blueprint for the niche |
| `AGENTS.md` | Ready-to-deploy AGENTS.md template for the niche |
| `landing-page.md` | Full landing page copy (H1 → CTA) in buyer's language |
| `gtm-plan.md` | 7-day first-client acquisition plan + 10 content post ideas |
| `run-log.md` | Run summary with delivery status |

---

## Pipeline Overview

```
Niche Input
      │
      ▼
[Stage 1] Vertical Score           ← load from cache or run vertical-scorer
      │   GO / CONDITIONAL / NO-GO
      │
      ▼
[Stage 2] Top 5 Use Cases          ← load from cache or generate per niche
      │   Wave 1 priority · structured format
      │
      ▼
[Stage 3] Business Model Design    ← pricing tiers, positioning, objections
      │
      ▼
[Stage 4] Tech Stack Blueprint     ← OpenHands + subagents + MCP servers
      │
      ▼
[Stage 5] AGENTS.md Template       ← deploy-ready file for the niche
      │
      ▼
[Stage 6] Landing Page Copy        ← H1 → problem → solution → pricing → CTA
      │
      ▼
[Stage 7] GTM + Launch Plan        ← 7-day plan + 10 content post ideas
      │
      ▼
[Stage 8] Run Log + Optional Deck  ← pptxkit deck if user wants a pitch asset
```

---

## Stage 1 — Vertical Score

**Check cache first:**
- `runs/2026-06-16-openhands-smb-use-cases/vertical-scores.md` contains scores for:
  Real Estate (33/35 GO), E-Commerce (29/35), Accounting (27/35), Marketing Agencies (27/35),
  Dental (26/35), Law (26/35), Med Spa (26/35), HVAC (24/35)

If the niche is in the cache, load the score and rationale. Do NOT re-run the scorer.

If the niche is NOT in the cache, run `/vertical-scorer` for the niche using the
7-dimension framework (Intelligence Ratio, Outsourcing Readiness, TAM Accessibility,
Data Moat Potential, Regulatory Friction, Incumbent Vulnerability, Mirage PMF Risk).

**Score interpretation for this model:**
- 30–35: GO — start here, own this vertical first
- 25–29: CONDITIONAL — viable with the right framing (watch the flagged risk)
- Below 25: CAUTION — either regulatory ceiling is too high or revenue per client is too low

---

## Stage 2 — Top 5 Use Cases

**Check cache first:**
- `runs/2026-06-16-openhands-smb-use-cases/top-25-use-cases.md` contains 25 scored use cases
- Filter to the target niche and load the top 5 (prioritize Wave 1, combined score ≥ 9)

If fewer than 3 use cases exist for the niche, generate additional ones using this format:

```
## #[N] — [Use Case Name]
**Vertical:** [specific niche]
**The Pain:** [1 sentence — what they're doing manually or with broken tools today]
**The Build:** [what OpenHands actually ships — specific app/tool/integration]
**MCP Servers Used:** [GitHub + Stripe/Twilio/Postgres/Calendly/etc.]
**Subagent Type:** [e.g. crm-specialist, hipaa-auditor, document-automation]
**Monthly Value to Client:** [$X saved or $Y generated]
**Buyer Line:** [exact sentence the SMB owner says — their words, not yours]
**Urgency Score:** [1–10, with reason]
**Wave:** [1 = ship now | 2 = ship after first client proves model]
```

**Scoring criteria (rank Wave 1 highest):**
1. Frequency of pain (how many SMBs have this exact problem)
2. Specificity of build (can OpenHands ship this in a week)
3. Stickiness (client can't easily leave once it's live)
4. Niche dominance potential (can I own "AI engineering for [vertical]")
5. Replicability (same build works for 10+ clients in same vertical)

**Real estate pitches already exist** (for reference pattern):
- `runs/2026-06-16-openhands-smb-use-cases/re-triplet-pitch/01-transaction-coordinator-bot.md`
- `runs/2026-06-16-openhands-smb-use-cases/re-triplet-pitch/02-listing-description-mls-autopost.md`
- `runs/2026-06-16-openhands-smb-use-cases/re-triplet-pitch/03-lead-scoring-crm-drip.md`

---

## Stage 3 — Business Model Design

Generate `business-model.md` with:

### Positioning Statement

"[Your AI Engineering Team for (Niche)]" — replace jargon entirely.
- BAD: "OpenHands instance with 131 subagents and MCP integrations"
- GOOD: "Your AI engineering team for dental practices"

Use the buyer's language from the Buyer Line field in use cases.

### Pricing Tiers

| Tier | Price | What's Included | Ideal Client |
|---|---|---|---|
| Starter | $1,500/mo | 1 use case deployed · 3 MCP integrations · email support · monthly check-in | Testing the model before committing |
| Growth ★ | $2,500/mo | 2 use cases · full MCP stack · Slack/text support · bi-weekly call | Active practice/firm with clear pain, ready to commit |
| Scale | $4,500/mo | 3 use cases · dedicated subagents per workflow · weekly strategy call · quarterly expansion | Multi-location or volume-heavy SMB |
| Enterprise | Custom | Full platform build · custom subagents · white-label · referral program | Franchises, multi-location chains |

One-time setup fee: $500 (covers configuration, onboarding call, AGENTS.md deployment).

### Why This Price Point Works

- $2,500/mo vs $15,000/mo dev shop → 6× cheaper
- $2,500/mo vs $25,000/mo junior developer (all-in) → 10× cheaper
- No hiring risk, no sick days, no handoff friction, works 24/7
- Client breaks even the moment one use case saves or generates $2,500

### Objection Handling

| Objection | Response |
|---|---|
| "How is this different from Zapier?" | Zapier connects existing apps. This builds you custom software that didn't exist — specific to how you work, not how a template works. |
| "What if the AI makes a mistake?" | You supervise. The agent does the work; you approve the exceptions. Same model as a human team — you wouldn't not hire a person because they might make a mistake. |
| "Can I cancel if it doesn't work?" | 30 days notice, no long-term contract. I'm not interested in keeping clients who aren't seeing value. |
| "Why can't I just build this myself?" | You can. It would take 6-12 months to learn the stack, and you'd spend it on software instead of [running your practice/business]. Or I can have it running in a week. |
| "Is this going to replace my staff?" | No — it replaces the tasks your staff hates doing. They focus on what matters; the agent handles the paperwork. |

---

## Stage 4 — Tech Stack Blueprint

Generate `tech-stack.md` with:

### OpenHands Setup

```
VPS Spec: $20/mo DigitalOcean Droplet (4 vCPU / 8GB RAM / 80GB SSD)
OS: Ubuntu 22.04
Docker: yes (OpenHands runs in Docker)
Setup time: 1 afternoon with Claude Code
Maintenance: ~2 hours/week (monitoring, exception handling)
Cost: $20/mo VPS + ~$50-100/mo API costs (Claude/GPT per task) = ~$100-150/mo
Margin on $2,500/mo client: ~$2,300+/mo per client
```

### Subagents (per niche)

Map the niche to VoltAgent subagent types. For each use case, list:
- Primary subagent type
- Secondary subagents (if needed)
- How they chain

**Reference subagent catalog:**
```
crm-specialist         → lead scoring, CRM updates, drip sequences
document-automation    → contract generation, PDF extraction, e-sign workflows
hipaa-auditor          → healthcare compliance check, PHI handling rules
mls-integration        → MLS API connections, listing syndication
billing-specialist     → invoice generation, payment follow-up, reconciliation
patient-recall-agent   → appointment reminders, recall sequences, no-show recovery
content-writer         → listing descriptions, email copy, social captions
legal-researcher       → case research, document review summary
```

### MCP Server Stack (per niche)

For each niche, select 6-8 MCP servers from the 14k+ available:

| Category | Server | When to Use |
|---|---|---|
| Core infrastructure | GitHub | All builds — code storage, version control |
| Communication | Gmail / Twilio | Notifications, reminders, follow-ups |
| Scheduling | Google Calendar / Calendly | Appointment management |
| Payments | Stripe | Invoicing, payment collection |
| Database | Postgres / Airtable | Client records, transaction tracking |
| Storage | Google Drive / Notion | Document management, deal files |
| CRM | Zapier (bridge) | Connect to existing CRM (Follow Up Boss, etc.) |
| Niche-specific | [varies] | MLS API, Dentrix API, Clio API, QuickBooks API |

---

## Stage 5 — AGENTS.md Template

Generate a niche-specific `AGENTS.md` file. This is what OpenHands reads to understand
the agent's role, capabilities, and constraints. It is the operational heart of the product.

```markdown
# AI Engineering Team — [NICHE]
## Role
You are a specialized AI engineering team for [niche] businesses. Your job is to
build, maintain, and operate custom software workflows that replace manual, repetitive
tasks — so the [niche] owner can focus on [core value of the niche, e.g. "closing deals",
"treating patients", "practicing law"].

## Capabilities
- Read and edit code in this repository
- Run tests and validate outputs before delivering
- Open pull requests for review
- Connect to MCP servers: [list the 6-8 servers for this niche]
- Process documents: [specific doc types for the niche]
- Communicate via [email/SMS/Slack] when workflows complete or exceptions occur

## Active Workflows
[List the use cases from Stage 2 — one section per use case]

### [Use Case 1 Name]
- Trigger: [what starts this workflow]
- Input: [what the agent reads/receives]
- Process: [step-by-step what the agent does]
- Output: [what gets delivered to the client or their clients]
- Exception: [when to pause and notify the human supervisor]

## Constraints
- Never take irreversible actions without human confirmation
  (e.g., don't send mass emails, don't delete records, don't charge cards)
- Flag any PHI / PII and apply [niche-specific] compliance rules
- All outputs go to staging for review before going live — unless the operator
  explicitly enables autopilot for a specific workflow
- Log every action to [Notion/Postgres/Google Sheet] for the weekly review

## Escalation Protocol
If any workflow encounters an unexpected state, stop and notify the supervisor via
[Slack/email/SMS] with: workflow name, step where it stopped, and the data it was
processing. Do not retry without explicit confirmation.

## Quality Standard
Before marking any task complete: verify the output matches the expected format,
check that all required fields are populated, and confirm the downstream system
received the data. If verification fails, log the failure and escalate.
```

---

## Stage 6 — Landing Page Copy

Generate `landing-page.md` with full copy in buyer's language:

### Structure

```
H1: [Niche-specific claim — not tech jargon]
   e.g. "Your AI Engineering Team for Real Estate Brokerages"
   or   "We Build the Software Your Dental Practice Has Been Waiting For"

SUBHEADING: [Pain in their language]
   e.g. "Custom software you need. Developer costs you can't afford. Not anymore."

SOCIAL PROOF BAR: [3 proof points — use real data from the use case math]
   e.g. "Replaces $2,000/mo TC fees · Works 24/7 · No long-term contract"

PROBLEM SECTION (3 pains)
   Headline: "Here's the software problem you've been living with"
   Pain 1: [Buyer Line from Use Case #1]
   Pain 2: [Buyer Line from Use Case #2]
   Pain 3: [Buyer Line from Use Case #3]

SOLUTION SECTION (3 capabilities, in plain language)
   Headline: "Here's what we build for you"
   [Capability 1]: [Plain English, 2 sentences, niche language]
   [Capability 2]: [Plain English, 2 sentences, niche language]
   [Capability 3]: [Plain English, 2 sentences, niche language]

HOW IT WORKS (4 steps)
   1. Discovery call (30 min) — you describe the problem in plain English
   2. We build it in OpenHands — takes 1-2 weeks for a Wave 1 use case
   3. You review + approve before it goes live — you're in control
   4. We maintain it, update it, and expand it as you grow

PRICING TABLE
   [From Stage 3 pricing tiers]

FAQ (5 questions)
   [From Stage 3 objection handling]

CTA:
   Primary: "Book a free 30-minute discovery call"
   Secondary: "See what we've built for [niche] businesses →"
```

---

## Stage 7 — GTM + Launch Plan

Generate `gtm-plan.md` with:

### 7-Day First Client Acquisition Plan

```
Day 1-2 — Build the Evidence Base
□ List 5 Wave 1 use cases for the niche (from Stage 2)
□ Write the ROI math for each: what does this save/generate per month?
□ Draft the one-page pitch for Use Case #1 (the highest urgency score)
□ Create a simple Notion page or Google Doc with the use case + pricing

Day 3 — Activate the Warm Network
□ List 10 people in the niche you already know (or 1 degree of separation)
□ Message each with a specific problem statement:
  "I'm building a [use case name] for [niche] businesses. Would a 20-minute
   call be useful — I want to see if this matches what you're experiencing?"
□ Do NOT pitch. The goal is discovery calls, not immediate sales.

Day 4-5 — Create One Piece of Content
□ Post on LinkedIn/X: describe the problem, explain the ROI math
   Format: "Here's the software [niche] businesses pay $X for every month
   and don't have to. [breakdown] [what I built instead] [price]"
□ No jargon. No "AI agents". No "OpenHands". Buyer language only.
□ Record a 3-min demo video if you have something running (even a prototype)

Day 6 — Run Discovery Calls
□ 3 discovery calls booked from warm network outreach
□ Agenda: What's the biggest operational headache right now?
  What would it be worth to have that just... handled?
  What does your current solution cost (in time + money)?
□ Listen for "I know" moments — that's when they already tried to solve this

Day 7 — Convert One
□ Send a 1-page pitch within 24 hours of each call
□ Include: the specific build for their pain, the ROI math, the price, the
   setup timeline, and a 30-day cancel clause
□ Target: 1 signed contract at $2,000-$3,000/mo by Day 7
□ If no conversion: 3 follow-ups scheduled, next 10 warm contacts listed
```

### Content Strategy (X / LinkedIn / YouTube)

**Content angle:** "What my AI engineering team built this week for [niche]"

**10 opening post ideas for [niche]:**
[Generate 10 specific, concrete post openings using the use cases from Stage 2.
Each must: start with a buyer pain statement, use buyer language, include ROI math,
be written for a [niche] owner scrolling their feed — not for a tech audience.]

**Format template:**
```
Here's what [specific niche pain] is costing [niche] businesses every month:

[Break it down with numbers]

I built a [plain-English description of the tool] that:
- [Specific result 1]
- [Specific result 2]
- [Specific result 3]

It costs [price]. It replaces [what it replaces].

If you're a [niche] and this is your life, DM me.
```

**Channel priority for [niche]:**
- Where buyers actually are (Facebook groups? LinkedIn? local networking?)
- Identify the 2-3 niche-specific communities and forums
- One piece of content per week minimum; one case study per month once you have a client

---

## Stage 8 — Run Log

Write `run-log.md`:

```markdown
# [Niche] OpenHands Niche Agency — Run Log

Status: `<complete | in-progress>`
Date: YYYY-MM-DD

## Niche
[niche name]

## Vertical Score
[score]/35 · [verdict] · [key rationale line]

## Top 5 Use Cases (Wave 1)
1. [name] — Urgency [X]/10
2. [name] — Urgency [X]/10
3. [name] — Urgency [X]/10
(+ 2 Wave 2 use cases identified)

## Pricing Model
Starter: $X · Growth: $X · Scale: $X

## Tech Stack
VPS: $20/mo
Subagents: [list]
MCP Servers: [list]
Monthly cost: ~$100-150/mo
Margin per client at Growth tier: ~$2,300+/mo

## Artifacts Delivered
- [ ] vertical-score.md
- [ ] top-5-use-cases.md
- [ ] business-model.md
- [ ] tech-stack.md
- [ ] AGENTS.md
- [ ] landing-page.md
- [ ] gtm-plan.md
- [ ] deck (optional)

## Next Action
[First call to book, first post to publish, first build to start]
```

---

## Optional: PPTX Pitch Deck

If the user wants a deck (e.g., to pitch to a partner, investor, or potential client):

Use `branded-pptx-deck` skill with this structure:
- Slide 1: Cover — "[Niche] AI Engineering Team"
- Slide 2: The Problem — 3 pains in buyer language
- Slide 3: The Model — "Open source is the new wholesale"
- Slide 4: What We Build — Top 3 use cases
- Slide 5: Tech Stack — OpenHands + subagents + MCP (visualized simply)
- Slide 6: Pricing — 3-tier table
- Slide 7: ROI Math — one use case, full breakdown
- Slide 8: The Operator Model — 1-person setup → $50k/mo team
- Slide 9: Your Vertical Score — why [niche] is the right place to start
- Slide 10: Next Step — discovery call + 7-day launch plan

---

## Do Not

- Pitch the tech stack to SMB buyers — never say "OpenHands", "subagents", "MCP"
  in client-facing copy. Use buyer language: "our AI engineering team", "the bot", "the system"
- Pick a niche that scores below 25/35 without a clear moat strategy
- Run more than one niche simultaneously in the first 90 days — own one vertical first
- Build more than 1-2 Wave 1 use cases before getting the first paying client
- Ignore the compliance ceiling for healthcare/legal niches — HIPAA + BAA required before deploying any patient/client data

## Success Criteria

- Vertical score loaded or generated
- 5 niche-specific use cases documented in full structured format
- AGENTS.md ready to deploy on first client's VPS
- Landing page copy is in buyer language — no jargon, no tech terms
- 7-day launch plan is actionable (named targets, specific messages, clear next step)
- Run log completed with all artifacts checked off

## Resources

- Prior vertical research: `runs/2026-06-16-openhands-smb-use-cases/`
  - `vertical-scores.md` — 8 verticals scored
  - `top-25-use-cases.md` — 25 use cases across all verticals
  - `re-triplet-pitch/` — 3 detailed real estate client pitches (reference pattern)
  - `playbook.md` — original skill chain map
- OpenHands docs: `https://docs.openhands.dev/`
- OpenHands repo: `https://github.com/All-Hands-AI/OpenHands`
- pptxkit: `~/.claude/skills/branded-pptx-deck/scripts/pptxkit.py`
- Branded deck: `~/.claude/skills/branded-pptx-deck/SKILL.md`
