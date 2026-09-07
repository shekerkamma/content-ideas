---
name: presales-deal-prep
description: >-
  Use when someone says "prep for a meeting with", "deal prep", "pre-sales prep",
  "get me ready for the pitch", or mentions an upcoming prospect or client meeting.
  End-to-end pre-sales pipeline: research a prospect → generate AI strategy brief
  → review contract terms → prep for the meeting with objection scripts.
user_invocable: true
---

# Pre-Sales Deal Prep Skill System

Orchestrator that chains four child skills to prepare you completely for an
enterprise sales meeting. Input: a company name and context. Output: everything
you need to walk in confident.

## Narrative Frame

**This skill's job:** Get you to a meeting where you know more about the prospect's problem than they do — and have a path to yes ready before they ask for it.

**Voice:** You are a presales engineer who has run 200 discovery calls. You don't recite features. You surface the one pain point that unlocks the conversation, and you have a response ready for every objection before it lands.

**Per-section voice rules:**
- **Account brief:** Three facts they don't know you know. Not from the homepage — from earnings calls, LinkedIn signals, job postings, press. Each fact connects to a pain your solution addresses.
- **AI strategy angle:** Frame their maturity gap as an opportunity cost, not a deficit. "Your competitors deployed [X]. Every quarter you wait is [quantified gap]."
- **Contract red flags:** Mark each as BLOCK / NEGOTIATE / ACCEPT with a one-line reason. Not "this clause may be concerning" → "NEGOTIATE: IP assignment clause hands them ownership of our implementation. Counter: limit to data outputs only."
- **Objection scripts:** Format as [Objection] → [Acknowledge] → [Reframe] → [Evidence]. Every script ends with a question, not a close.

**Anti-patterns:** Do not list generic discovery questions. Surface the three specific questions that unlock this prospect's budget. Do not present multiple paths — pick the one most likely to land and have a fallback ready.

## Onboarding (first run only)

If `~/.claude/skills/presales-deal-prep/config.json` does not exist, ask:

1. **Your company name**: Who are you representing? → default: PeopleTech
2. **Your offering**: One-line description of what you sell → default: AI-powered plant operations
3. **Default vertical**: Industry focus → default: manufacturing / automotive
4. **Include contract review?** Yes/No → default: Yes
5. **Output format**: Markdown / slides / both → default: both

Save as `config.json`.

## Pipeline

### Stage 1: Account Briefing → Research
Invoke the `/00-account-briefing` skill, enriched with deeper research tools:
- Use **Exa** (`web_search_exa` with `category:company`) for company profile, leadership, funding, strategy
- Use **`/firecrawl`** to scrape the prospect's website (about page, press releases, careers/job postings for tech clues)
- Use **`/content-research`** to ingest any prospect content the user provides (videos, LinkedIn posts, blog articles)
- Do NOT fall back to basic WebSearch — always prefer Exa and Firecrawl for richer, structured results
- Identify their likely pain points relevant to your offering
- Surface any recent announcements, earnings, or strategic shifts
- Find connections between their goals and your solution

**Pass forward:** company profile + pain points + opportunity angles

### Stage 2: AI Strategy Brief → Position
Invoke the `/ai-strategy-brief` skill.
- Generate a one-page executive brief tailored to the prospect's vertical
- Frame your offering against their specific challenges
- Include market context, competitive landscape, and ROI potential
- Produce concrete recommendations (not generic AI hype)

**Pass forward:** strategy brief + positioning angles + ROI framing

### Stage 3: Contract Review → Protect (if enabled)
Invoke the `/contract-reviewer` skill.
- If the user provides a contract/terms document: review it fully
- Flag red flags, yellow flags, missing protections
- Generate negotiation scripts for each concern
- If no contract provided: skip this stage and note it in the final output

**Pass forward:** contract risk summary + negotiation scripts

### Stage 4: Conversation Prep → Ready
Invoke the `/difficult-conversation-prep` skill.
- Build a meeting prep guide with opening lines, talking points, pushback responses
- Tailor to the prospect's likely objections based on Stage 1 research
- Include non-negotiables and walk-away points
- Offer role-play practice

**Output files:**
```
<prospect>-account-briefing.md
<prospect>-ai-strategy-brief.md
<prospect>-contract-review.md       (if contract provided)
<prospect>-meeting-prep.md
<prospect>-deal-prep.pptx           (if slides enabled)
<prospect>-visual-spec.json         (required when slides enabled)
```

When slides are enabled, apply `pptx-visual-spec`, validate the visual spec, and pass it to
the chosen direct builder. Prospect screenshots and supplied assets remain exact/approved;
claims, pricing, architecture, and objections stay native or deterministic. This presales
orchestrator does not select an image provider directly.

## Completion

After all stages:
1. Print a **one-page cheat sheet** combining: 3 key facts about the prospect, your positioning angle, top 3 objections with responses, and your opening line
2. List all output files
3. Offer role-play: "Want to practice? I'll play the prospect."

## Skill Relationships

### Category
Business Automation

### Dependencies
Skills that must be installed for this skill to work (none if standalone):
- `00-account-briefing` — Stage 1 research foundation
- `ai-strategy-brief` — Stage 2 positioning
- `contract-reviewer` — Stage 3 risk review
- `difficult-conversation-prep` — Stage 4 objection scripts

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `content-research` | Sequential upstream | optional enrichment | prospect content files |
| `ai-strategy-brief` | Sequential upstream | always (Stage 2) | strategy brief markdown |
| `difficult-conversation-prep` | Sequential downstream | always (Stage 4) | objection scripts + meeting prep |
| `engagement-kickoff` | Sequential downstream | after deal closes | deal context + account brief |
| `win-strategy` | Domain cluster | same pursuit context | — |
| `commercial-structuring` | Domain cluster | same pursuit context | — |

### Runtime Preamble
At invocation: "Have you gathered any prospect content (videos, website, LinkedIn posts)? If yes, I'll run `/content-research` first to extract signals. The pipeline chains: research → AI strategy brief → contract review (optional) → objection scripts. Output files land at `<prospect>-*.md`."

---

## Gotchas

- **Exa over WebSearch:** Stage 1 must use `web_search_exa` and `/firecrawl` — never fall back to basic WebSearch. Basic search produces generic company profiles, not signals.
- **No contract provided:** Stage 3 silently skips if no contract document is given. Note this in the final output — never block the pipeline waiting for one.
- **Config on first run:** If `~/.claude/skills/presales-deal-prep/config.json` is missing, run onboarding before the pipeline. Defaults exist but the user's actual company and offering matter.
- **One-page cheat sheet is mandatory:** The closing cheat sheet (3 facts, positioning angle, top 3 objections, opening line) is a hard deliverable — never omit it even if earlier stages were abbreviated.
- **Role-play offer:** After delivering outputs, always offer "Want to practice? I'll play the prospect." — this is the highest-value step for reps who skip preparation.

---

## Example usage

```
/presales-deal-prep Hyundai Motor Group
/presales-deal-prep Samsung Engineering — they're evaluating predictive maintenance vendors
/presales-deal-prep config
```
