# OpenHands × SMB "Done-For-You AI Engineering Team" — Master Playbook
**Run:** 2026-06-16  
**Concept:** Self-host OpenHands + 131 subagents + 14,000+ MCP servers → sell as a managed AI engineering team to SMBs at $2k–$5k/month  
**Goal:** Identify Top 25 use cases in structured format

---

## PART 1 — THE PROMPT
*Use this prompt in any Claude/ChatGPT/Gemini session to generate the 25 use cases directly.*

---

**ROLE:** You are a B2B product strategist and SMB go-to-market expert specializing in AI services.

**CONTEXT:**
I am building a "done-for-you AI engineering team" service using OpenHands (open-source AI agent runtime, 75k+ GitHub stars) + 131 free specialist subagents + 14,000+ MCP server integrations. I self-host on a $20/mo VPS. I charge SMBs $2,000–$5,000/month — 5x cheaper than a dev shop, works 24/7.

OpenHands agents can: read codebases, write and edit files, run tests, open PRs, integrate APIs, deploy apps, and operate autonomously with minimal supervision.

**THE BUSINESS MODEL:**
1. Self-host OpenHands on a $20/mo VPS — Claude Code walks you through setup in an afternoon
2. Pick one niche: real estate brokerages, dental practices, law firms, marketing agencies — SMBs that need custom software but can't afford a developer
3. Wrap it in their language: "your AI engineering team for dental practices" not "an OpenHands instance with 131 subagents"
4. Install relevant subagents from VoltAgent: crm-specialist for real estate, hipaa-auditor for healthcare, document-automation for law firms
5. Plug in MCP servers from the 14k+ available: GitHub, Stripe, Twilio, Postgres, Calendly — now your AI team can ship, deploy, integrate, and notify
6. Charge $2,000–$5,000/month per client — nothing compared to a $15k/mo dev shop or a $25k/mo junior hire
7. Build one landing page, one onboarding call, record the AGENTS.md setup once — the rest is supervision
8. Become "the AI engineering team for [niche]" on X, LinkedIn, YouTube — share what your agents shipped this week
9. Reinvest profits into vertical-specific agents: patient-intake-automator for dental, lease-document-generator for real estate

**TARGET BUYERS:** SMBs that need custom software but can't afford developers:
- Dental practices
- Law firms
- Real estate brokerages
- Marketing agencies
- HVAC/plumbing contractors
- Med spas / aesthetic clinics
- Accounting firms
- E-commerce brands
- Property management companies
- Mortgage brokers
- Insurance agencies
- Restaurants / hospitality

**TASK:**
Generate the **Top 25 Use Cases** for this service. Each use case must be a specific, concrete software project an SMB would pay $2k–$5k/month for — not a generic AI feature.

**OUTPUT FORMAT (strictly follow for all 25):**

```
## #[N] — [Use Case Name]
**Vertical:** [specific niche]
**The Pain:** [1 sentence — what they're doing manually or with broken tools today]
**The Build:** [what OpenHands actually ships — specific app/tool/integration]
**MCP Servers Used:** [GitHub + Stripe/Twilio/Postgres/Calendly/etc.]
**Subagent Type:** [e.g. crm-specialist, hipaa-auditor, document-automation]
**Monthly Value to Client:** [$X saved or $Y generated]
**Buyer Line:** [exact sentence the SMB owner says when they describe this pain — their words, not yours]
**Urgency Score:** [1–10, with reason]
```

**SCORING CRITERIA — rank by:**
1. Frequency of pain (how many SMBs have this exact problem)
2. Specificity of build (can OpenHands ship this in a week)
3. Stickiness (client can't easily leave once it's live)
4. Niche dominance potential (can I own "AI engineering for [vertical]")
5. Replicability (same build works for 10+ clients in same vertical)

**CONSTRAINTS:**
- No generic "chatbot" or "AI assistant" use cases
- Each must require actual custom software — not a SaaS subscription
- Must be something a solo operator could deliver with OpenHands + supervision
- Prioritize use cases where the SMB has tried to hire a developer and failed or been burned

Go.

---

## PART 2 — SKILL CHAIN MAP
*Run this chain in Claude Code to generate, score, and validate the 25 use cases using all available skills and tools.*

```
INPUT: "Done-for-you AI engineering team" concept
         │
         ▼
[1] last30days:last30days          ← recent signals (OpenHands traction,
    trigger: /last30days               SMB AI adoption, pricing benchmarks)
    query: "OpenHands SMB AI engineering done-for-you 2026"
         │
         ▼
[2] content-research               ← deep ingest: OpenHands docs/GitHub,
    trigger: /content-research         VoltAgent subagents, MCP registry,
                                       SMB pain-point forums/threads
         │
         ▼
[3] vertical-scorer                ← score 8 SMB niches on attractiveness
    trigger: /vertical-scorer          (dental, legal, RE, mktg, HVAC,
                                       med spa, accounting, e-comm)
         │
         ▼
[4] ai-use-case-prioritiser        ← per vertical: map specific software
    trigger: /ai-use-case-prioritiser  gaps → OpenHands build candidates
         │
         ▼
[5] content-ideas:plaid            ← PLAID Idea phase: structure as
    trigger: /goal (loaded)            validated product opportunities
    phase: Idea → Validate
         │
         ▼
[6] ai-strategy-brief              ← synthesise into one-pager per top
    trigger: /ai-strategy-brief        3 verticals (optional downstream)
         │
         ▼
OUTPUT: Top 25 use cases — structured markdown + optional PPTX deck
```

---

## PART 3 — TOOL POINTERS

| Tool / Skill | Trigger | Role in This Run |
|---|---|---|
| `last30days:last30days` | `/last30days` | Market signals — what's being said about OpenHands + SMB AI in last 30 days |
| `content-research` | `/content-research` | Deep ingest — OpenHands GitHub, subagent registry, SMB pain blogs |
| `vertical-scorer` | `/vertical-scorer` | Score + rank 8 SMB verticals before generating use cases |
| `ai-use-case-prioritiser` | `/ai-use-case-prioritiser` | Map pain → build per vertical; score on frequency, stickiness, replicability |
| `content-ideas:plaid` | `/goal` (loaded) | Idea + Validate phase — pressure-test each use case as a product opportunity |
| `ai-strategy-brief` | `/ai-strategy-brief` | One-pager synthesis for top 3 verticals |
| `ai-strategy-researcher` | `/ai-strategy-researcher` | Deep research on OpenHands ecosystem + competitive moat |
| `branded-pptx-deck` | `/branded-pptx-deck` | Deliver output as a PPTX pitch deck |
| `strategy-consulting` | `/ai-use-case-prioritiser` | Impact × feasibility × strategic fit matrix |
| `ai-transformation` | `/ai-use-case-prioritiser` | AI-specific use case scoring framework |
| `GBrain MCP` | (auto via CLAUDE.md) | Recall any prior research on OpenHands / SMB verticals |
| `Exa MCP` | `mcp__claude_ai_Exa__web_search_exa` | Current web research — primary discovery tool |
| `WebSearch` | (built-in) | Fallback web research |
| `TodoWrite` | (built-in) | Track chain progress |

---

## PART 4 — PROMPT TEMPLATES IN PLAY

| Template File | Skill | When to Use |
|---|---|---|
| `skills/plaid/references/idea.md` | PLAID | Generating use case candidates |
| `skills/plaid/references/validate.md` | PLAID | Pressure-testing each use case (Strong / Weak / Pivot) |
| `skills/vertical-scorer/` | vertical-scorer | Scoring rubric: market size, pain acuity, AI fit, niche dominance, replicability |
| `skills/ai-transformation/skills/02-use-case-and-operating-model/ai-use-case-prioritiser.md` | ai-use-case-prioritiser | Impact × feasibility × strategic fit matrix |
| `skills/strategy-consulting/skills/02-market-and-competitive-intelligence/customer-segmentation.md` | customer-segmentation | SMB buyer profiling per vertical |
| `skills/strategy-consulting/skills/03-strategic-choice-and-economics/strategic-options.md` | strategic-options | Niche selection — which vertical to own first |
| `content-ideas/references/content-strategy.md` | content-ideas | Packaging use cases as LinkedIn/YouTube content angles |
| `skills/gstack/ai-strategy-brief/SKILL.md` | ai-strategy-brief | One-pager synthesis per top vertical |

---

## PART 5 — EXECUTION ORDER

```bash
# Step 1 — GBrain recall (auto, via CLAUDE.md rules)
# Check for prior OpenHands / SMB research before new research

# Step 2 — Last 30 days signals
/last30days OpenHands SMB AI engineering done-for-you

# Step 3 — Content research
/content-research https://github.com/All-Hands-AI/OpenHands

# Step 4 — Vertical scoring
/vertical-scorer
# Input: dental, legal, real estate, marketing, HVAC, med spa, accounting, e-commerce

# Step 5 — Use case prioritisation
/ai-use-case-prioritiser
# Input: top 3 scored verticals + OpenHands capabilities

# Step 6 — PLAID Idea → Validate
# (already loaded via /goal)
# Run against top 5 use case candidates

# Step 7 — Synthesise Top 25
# Apply the PART 1 prompt to structured research outputs

# Step 8 — Optional: PPTX deck
/branded-pptx-deck
# Input: Top 25 use cases markdown → client-facing deck
```

---

## PART 6 — OUTPUT STRUCTURE (when run completes)

```
runs/2026-06-16-openhands-smb-use-cases/
├── playbook.md                    ← this file
├── research-signals.md            ← last30days + content-research output
├── vertical-scores.md             ← scored SMB niches
├── use-case-longlist.md           ← all candidates before Top 25 cut
├── top-25-use-cases.md            ← final structured output
└── deck/
    └── openhands-smb-deck.pptx   ← optional branded deck
```

---

*Type `go` to kick off the full chain, or `/last30days` to start with live market signals.*
