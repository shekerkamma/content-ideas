---
name: ai-strategy-council
description: 'Use when someone says "strategy council", "research and council", "evidence-based council", "get multiple AI perspectives on this", or asks a strategic question that needs market data before advisors can debate it. Chains AI strategy research with LLM Council judgment: market intelligence first, then a 5-advisor council argues over real evidence. Produces evidence + verdict + action plan. (gstack)'
allowed-tools:
- Bash
- Read
- Write
- Edit
- Glob
- Grep
- WebSearch
- WebFetch
- Agent
- AskUserQuestion
metadata:
  legacy-frontmatter:
    preamble-tier: 3
    version: 1.0.0
    argument-hint: '[strategic question or vertical -- e.g., ''Should we build an AI-native O2C platform?'']'
---

# AI Strategy Council

Evidence-based strategic decision-making. Chains market research into multi-perspective
council judgment so advisors argue over facts, not assumptions.

## Why This Exists

Running a council without evidence produces generic advice. Running research without
judgment produces a document nobody acts on. This skill chains them: research narrows
the decision space, the council pressure-tests it, then targeted follow-up research
fills the blind spots the council identifies.

## Execution Flow

### Phase 0: Parse the Input

Determine if the user provided:
- **A decision question** ("Should we build X?") -- needs research first, then council
- **A vertical/topic** ("AI-native O2C") -- needs framing as a decision, then both
- **A question with context** ("Given our SAP stack, should we...") -- frame and proceed

If the input is too vague to research or decide on, ask ONE clarifying question. Just one.

---

### Phase 1: Rapid Market Scan (4 parallel searches)

Run these simultaneously. Goal: collect hard evidence in under 60 seconds.

1. **Market signal** -- What just happened? Largest recent fundraise, acquisition, partnership, or product launch in the space
2. **Competitive proof** -- Who is winning and at what scale? Top 3-5 companies with ARR/valuation/growth metrics
3. **VC/analyst thesis** -- What are Sequoia, a16z, Emergence, Gartner, or McKinsey saying?
4. **Failure signal** -- What has failed, pivoted, or been acquired for parts? Why?

Extract from each search:
- 2-3 key data points (numbers, names, dates)
- 1 insight that would change how an advisor thinks about the question
- Source URL for attribution

**Output:** A structured evidence brief (not a document -- internal working state):

```
EVIDENCE BRIEF
==============
Market Signal: {summary + key number}
Competitive Proof: {top players + metrics}
VC Thesis: {dominant framework + who's saying it}
Failure Signal: {what died + why}
Sources: {8-12 URLs}
```

---

### Phase 2: Frame the Council Question

Using the evidence collected, write a council-ready question that includes:

1. The core decision (from user input)
2. Key evidence that constrains the answer (from Phase 1)
3. What's at stake (inferred from context)
4. Specific tensions the evidence revealed (e.g., "VCs are bullish but 3 companies failed doing exactly this")

The framing should make it IMPOSSIBLE for advisors to give generic advice. They must
engage with the specific data.

**Template:**

```
QUESTION FOR THE COUNCIL:
{The core decision}

EVIDENCE ON THE TABLE:
- Market: {key signal with number}
- Competition: {who's winning, at what scale}
- Smart money: {VC thesis or analyst view}
- Failures: {what didn't work and why}
- Sources: {count} references checked

SPECIFIC TENSIONS:
- {Tension 1: e.g., "Market is $X but leaders are only at $Y ARR -- gap or mirage?"}
- {Tension 2: e.g., "VCs say autopilot but every winner is still copilot-mode"}

What should we do, given this evidence?
```

---

### Phase 3: Convene the Council (5 sub-agents, parallel)

Spawn all 5 advisors simultaneously. Each gets their identity + the evidence-loaded
framed question.

**The Five Advisors:**

- **The Killer** -- Hunts for the fatal flaw. Assumes the idea is broken and tries to prove it using the evidence provided. Must reference specific data points.
- **The Rebuilder** -- Strips assumptions, asks "what are we actually solving?" Challenges whether the evidence supports the framing or reveals a different question entirely.
- **The Maximizer** -- Finds upside everyone else misses. What adjacent opportunity does the evidence reveal? What's being undervalued?
- **The Stranger** -- Zero context, zero tribal knowledge. Responds purely to the evidence and question as presented. Catches insider blind spots.
- **The Operator** -- "What do you do Monday morning?" Filters everything through executability. References the competitive landscape for build-vs-buy.

**Sub-agent prompt:**

```
You are {Advisor Name} on an LLM Council.

Your thinking style: {description}

A user has brought this question to the council, backed by market research:
---
{evidence-loaded framed question from Phase 2}
---

IMPORTANT: You have real market data in front of you. Reference it. Don't give generic
advice -- engage with the specific numbers, companies, and signals provided. If the
evidence contradicts your instinct, say so and explain why you still hold your position
or why you're changing it.

Keep your response between 200-350 words. No preamble. Go straight into your analysis.
```

---

### Phase 4: Peer Review (5 sub-agents, parallel)

Collect all 5 responses. Anonymize as Response A-E (randomize mapping).
Spawn 5 reviewers, each seeing all responses + the original evidence.

**Reviewer prompt:**

```
You are reviewing the outputs of an LLM Council. Five advisors independently answered
this evidence-backed strategic question:
---
{evidence-loaded framed question}
---

Here are their anonymized responses:
**Response A:** {response}
**Response B:** {response}
**Response C:** {response}
**Response D:** {response}
**Response E:** {response}

Answer these four questions. Reference responses by letter.

1. Which response engages most deeply with the EVIDENCE (not just the question)?
2. Which response has the biggest blind spot? What is it missing?
3. Where does the evidence CONTRADICT what an advisor claimed?
4. What did ALL five responses miss that the evidence suggests we should investigate?

Keep under 200 words. Be direct.
```

---

### Phase 5: Identify Research Gaps

Before the chairman synthesizes, extract from peer reviews:
- Blind spots flagged by 2+ reviewers
- Claims that contradict the evidence
- Areas where advisors said "I don't know" or hedged

Run 2-3 targeted follow-up searches on the most critical gaps. These are surgical,
not broad -- e.g., "UKM_BUSINESSPARTNER API documentation completeness" or
"{specific company} revenue 2025".

Add findings to the evidence brief as:

```
FOLLOW-UP EVIDENCE (from council blind spots):
- Gap 1: {what was missing} → Finding: {what we learned}
- Gap 2: {what was missing} → Finding: {what we learned}
```

---

### Phase 6: Chairman Synthesis

One agent gets everything: framed question, all evidence (original + follow-up),
all 5 advisor responses (de-anonymized), all 5 peer reviews.

**Chairman prompt:**

```
You are the Chairman of an LLM Council with full market evidence.

ORIGINAL QUESTION:
{user's question}

MARKET EVIDENCE:
{full evidence brief including follow-up findings}

ADVISOR RESPONSES:
**The Killer:** {response}
**The Rebuilder:** {response}
**The Maximizer:** {response}
**The Stranger:** {response}
**The Operator:** {response}

PEER REVIEWS:
{all 5 reviews}

FOLLOW-UP EVIDENCE (filling council blind spots):
{targeted research results}

Produce the council verdict:

## The Evidence Says
[What the market data clearly supports. No interpretation -- just what the numbers show.]

## Where the Council Agrees
[Points where multiple advisors converged, supported by evidence.]

## Where the Council Clashes
[Genuine disagreements. Which side does the evidence favor?]

## Blind Spots Filled
[What the follow-up research revealed. Did it confirm or overturn advisor positions?]

## The Verdict
[Clear recommendation. Reference specific evidence that tips the decision. The chairman
can overrule the majority if one dissenter's reasoning + evidence is stronger.]

## Decision Framework
[A simple 2x2 or decision tree the user can apply. Include the key variable that would
flip the recommendation if it changed.]

## The Next Three Moves
[Not one thing -- three. Sequenced. Each with a clear deliverable and timeline.]
- Move 1 (Week 1): {action} → Deliverable: {what you'll know/have}
- Move 2 (Week 2-3): {action} → Deliverable: {what you'll know/have}
- Move 3 (Week 4): {action} → Deliverable: {what you'll know/have}
```

---

### Phase 7: Generate Decision Package

Produce a single HTML report combining everything. Save to:
`D:\AppliedAICourse\Claude Cowork\OUTPUTS\llm-council\strategy-council-{YYYY-MM-DD-HHmm}.html`

Also save the full transcript as:
`D:\AppliedAICourse\Claude Cowork\OUTPUTS\llm-council\strategy-council-{YYYY-MM-DD-HHmm}.md`

**HTML structure:**
- Header: question + date + source count
- Evidence Summary (always visible -- the facts the decision rests on)
- Chairman Verdict (the main content)
- Decision Framework (visual 2x2 or decision tree)
- Next Three Moves (action-oriented, sequenced)
- Collapsible: individual advisor responses
- Collapsible: peer review highlights
- Collapsible: full evidence brief with all sources
- Footer: timestamp, advisor count, source count

**Design:** Same as council reports -- dark background (#0A0A0A), primary text (#F5F4EE),
secondary (#D6D4CB), red accent (#D93025), surface cards (#141413). No emoji.

---

## Quality Gates

Before delivering, verify:
- [ ] 8+ external sources cited with URLs
- [ ] Every advisor references at least one data point from the evidence
- [ ] Follow-up research addressed at least 1 council blind spot
- [ ] Verdict references specific evidence, not just advisor opinion
- [ ] Next Three Moves are sequenced with deliverables
- [ ] Decision Framework includes the "flip variable" (what would change the answer)

## Modes

**Full mode (default):** All 7 phases. ~15 minutes. Use for major strategic decisions.

**Speed mode** (user says "quick" or "fast"): Skip Phase 5 (follow-up research) and
compress Phase 4 (2 reviewers instead of 5). ~8 minutes. Use for time-sensitive calls.

## When NOT to Use This

- Simple factual questions (just search)
- Already have research, just need judgment (use `/llm-council` directly)
- Need a full 30-page strategy doc (use `/ai-strategy-researcher`)
- The decision has no real stakes (just answer it)

## Key Principle

**Advisors must engage with evidence.** If an advisor gives advice that ignores the
data in front of them, that's a signal their response is generic. The peer review
step catches this explicitly (Question 1: "Which response engages most deeply with
the EVIDENCE?"). This is the core differentiator from running council alone.

---

## Skill Relationships

### Category
Runbook

### Dependencies
Skills that must be installed for this skill to work (none if standalone):
- None — uses WebSearch + WebFetch + Agent sub-agents internally

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `content-research` | Sequential upstream | optional — ingest prior research before council | research notes in `$CONTENT_HOME/research/` |
| `ai-strategy-brief` | Alternative / Peer | ai-strategy-brief = single concise one-pager; council = multi-voice pressure-testing | — |
| `ai-strategy-researcher` | Alternative / Peer | ai-strategy-researcher = deep solo research doc; council = multi-advisor synthesis | — |

### Runtime Preamble
At invocation: "Have you run `/content-research` or `/ai-strategy-researcher` on this topic? Prior research shortens Phase 1. Alternatives: `/ai-strategy-brief` (concise one-pager) or `/ai-strategy-researcher` (deep solo research doc). Council is best when a major decision needs evidence-grounded multi-perspective pressure-testing."

## Gotchas

- **Advisors must engage with evidence:** If an advisor response ignores the Phase 1 data, flag it in peer review. Generic advice that ignores the evidence brief defeats the purpose of the council.
- **Speed mode skips follow-up research:** In speed mode (user says "quick" or "fast"), Phase 5 is skipped. Note this in the decision package so the reader knows blind spots were not filled.
- **Output paths are hardcoded to Windows:** The default output path `D:\AppliedAICourse\...` is Windows-specific. Resolve to the correct OS path at runtime — on Linux/Mac use `~/Documents/` or `$CONTENT_HOME`.
- **Simple questions don't need council:** If the user has a factual question, search and answer directly. The council is for decisions with genuine stakes and multiple valid perspectives.
