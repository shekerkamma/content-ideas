---
name: competitive-intel-sprint
description: >-
  Use when the user says "competitive analysis", "analyze this competitor",
  "intel sprint", "what are they doing", or provides a competitor URL/video.
  End-to-end pipeline: watch competitor's demo video → ingest their content →
  deep research → score the vertical opportunity → output executive brief.
  For a full 30-page Word strategy document rather than a sprint analysis, use `ai-strategy-researcher` instead.
user_invocable: true
---

# Competitive Intel Sprint Skill System

Orchestrator that chains five child skills to produce a complete competitive
intelligence report from a single competitor input (video, website, content).
Input: competitor name + source material. Output: scored analysis + executive brief.

## Narrative Frame

**This skill's job:** Surface the three things the competitor is doing that you are not — and the one thing you do better that they can't easily copy.

**Voice:** You are a competitor analyst who has watched 50 of these demos. You are not impressed by the marketing. You look for what's real: what they ship, who they're targeting, what's missing, where their positioning leaks.

**Per-section voice rules:**
- **Feature extraction:** "They ship X. You don't. Gap: [impact]." One line per gap. No padding.
- **Positioning analysis:** Name the ICP they're going after. Name the one message they repeat most. Name what they avoid saying.
- **Opportunity score:** Verdict first — GO / CONDITIONAL / PASS — then the score. The score is evidence, not the conclusion.
- **Executive brief:** Opens with the single most important thing you learned. Closes with the one move to make in response, named and owned.

**Anti-patterns:** Do not describe what they said in their marketing. Describe what they actually built. Do not score without a recommendation tied to the score.

## Onboarding (first run only)

If `~/.claude/skills/competitive-intel-sprint/config.json` does not exist, ask:

1. **Your company**: Who are you? → default: PeopleTech
2. **Your vertical**: Your primary market → default: AI plant operations / manufacturing
3. **Comparison depth**: Quick (3 dimensions) / Standard (6) / Deep (10+) → default: Standard
4. **Output format**: Brief only / brief + slides / full report → default: brief + slides

Save as `config.json`.

## Pipeline

### Stage 1: Watch → Observe (if video provided)
Invoke the `/watch` skill on the competitor's demo/presentation video.
- Extract their positioning, feature claims, pricing signals, target audience
- Note visual design choices, UI patterns, demo flow
- Capture exact quotes and claims for fact-checking
- If no video: skip to Stage 2 with URLs/docs instead

**Pass forward:** competitor claims + positioning + feature list + quotes

### Stage 2: Content Research → Ingest
Invoke the `/content-research` skill, enriched with deeper research tools:
- Use **`/firecrawl`** to scrape the competitor's website (product pages, pricing, case studies, job postings for tech stack clues)
- Use **Exa** (`web_search_exa` with `category:company`) for company profile, funding, leadership, recent coverage
- Use **`/hackernews`** to search for community sentiment, discussions, and complaints about the competitor
- Use **`/podscan`** to find podcast episodes mentioning the competitor (founder interviews, analyst takes)
- Use **`/content-research`** to ingest any additional sources (blog, social, docs)
- Do NOT fall back to basic WebSearch — always prefer the richer tools above
- Map their product capabilities, integrations, and tech stack
- Identify their go-to-market strategy and target segments
- Extract customer testimonials, case studies, pricing

**Pass forward:** competitor profile + capabilities map + GTM strategy + community sentiment

### Stage 3: AI Strategy Research → Contextualize
Invoke the `/ai-strategy-researcher` skill.
- Research the broader market context the competitor operates in
- Identify market trends, regulatory landscape, technology shifts
- Map where the competitor sits relative to market trajectory
- Find gaps and whitespace they aren't addressing

**Pass forward:** market context + competitor positioning + gaps identified

### Stage 4: Vertical Scorer → Evaluate
Invoke the `/vertical-scorer` skill.
- Score the competitor's vertical opportunity vs yours
- Evaluate across: market size, defensibility, AI leverage, go-to-market fit
- Produce a quantified comparison matrix
- Identify where you win, where they win, and where it's contested

**Pass forward:** scores + comparison matrix + win/loss dimensions

### Stage 5: AI Strategy Brief → Deliver
Invoke the `/ai-strategy-brief` skill.
- Generate a one-page executive brief summarizing the competitive analysis
- Frame findings as actionable intelligence (not just observations)
- Include: competitive positioning, threat assessment, recommended response
- Highlight the 3 things you should do differently based on this analysis

**Output files:**
```
<competitor>-intel-research.md
<competitor>-market-context.md
<competitor>-vertical-score.md
<competitor>-competitive-brief.md
<competitor>-intel-deck.pptx          (if slides enabled)
<competitor>-visual-spec.json         (required when slides enabled)
```

## Completion

After all stages:
1. Print the **threat level**: Low / Medium / High / Critical
2. Print **3 actionable takeaways** — what to do next
3. Show the win/loss matrix (where you beat them, where they beat you)
4. List all output files
5. Offer: "Want me to draft a counter-positioning strategy?"

## Example usage

```
/competitive-intel-sprint Siemens MindSphere https://youtube.com/watch?v=...
/competitive-intel-sprint "Rockwell Automation" — check their website and recent LinkedIn posts
/competitive-intel-sprint config
```

---

## Skill Relationships

### Category
Runbook

### Dependencies
Skills that must be installed for this skill to work:
- `watch` — for video input at Stage 1 (optional but preferred when a demo URL is given)
- `content-research` — competitor content ingestion at Stage 2
- `ai-strategy-researcher` — market context at Stage 3
- `vertical-scorer` — opportunity scoring at Stage 4
- `ai-strategy-brief` — executive brief generation at Stage 5

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `watch` | Sequential upstream (invoked) | when a competitor video URL is provided | transcript + frames passed to Stage 1 analysis |
| `content-research` | Sequential downstream (invoked) | always — Stage 2 | `<competitor>-intel-research.md` |
| `ai-strategy-researcher` | Sequential downstream (invoked) | always — Stage 3 | `<competitor>-market-context.md` |
| `vertical-scorer` | Sequential downstream (invoked) | always — Stage 4 | `<competitor>-vertical-score.md` |
| `ai-strategy-brief` | Sequential downstream (invoked) | always — Stage 5 | `<competitor>-competitive-brief.md` |
| `branded-pptx-deck` | Sequential downstream (optional) | when output format includes slides | `<competitor>-intel-deck.pptx` |
| `presales-deal-prep` | Sequential downstream (optional) | when the competitive brief feeds into a sales pursuit | `<competitor>-competitive-brief.md` handed to presales-deal-prep |
| `ai-strategy-researcher` | Alternative / Peer | same research goal, different focus — ai-strategy-researcher covers broader market without the competitor-vs-you framing | — |

### Runtime Preamble

At invocation, confirm inputs and route:

- "Do you have a competitor video/demo URL? I'll run `/watch` on it first to extract claims and positioning before the web research."
- "No video? Provide the competitor's website URL or name — I'll use Firecrawl + Exa + HackerNews for the profile."
- "Output: brief only, brief + slides, or full report? (Default from `config.json`)"
- "Downstream use: if this intel is for a sales pursuit, pipe the brief into `/presales-deal-prep` next."

---

## Gotchas

- **Stage 1 is optional but high-signal:** A competitor demo video reveals what they actually ship vs. what the marketing says. If a URL is available, always run `/watch` before web research — the transcript grounds the analysis in real claims.
- **Never fall back to WebSearch when richer tools are available:** Always prefer Firecrawl (product pages), Exa (company profile), HackerNews (community sentiment), and Podscan (founder interviews). WebSearch misses structured company data and real-world user complaints.
- **Verdict first in the brief:** The executive brief must open with the single most important finding — not a summary of stages. "They ship X. We don't. Gap: [impact]." leads every section.
- **Score is evidence, not the conclusion:** The vertical-scorer output goes into the brief as supporting data. The recommendation ("GO / CONDITIONAL / PASS") comes from the analyst's judgment, not the score alone.
- **Do not describe marketing — describe what they built:** The brief is not a paraphrase of their website copy. Extract feature claims from the video/docs and validate them against pricing pages, job postings, and GitHub repos.
When slides are enabled, apply `pptx-visual-spec` after evidence validation and pass the
validated spec to `branded-pptx-deck`. Competitor claims, rankings, logos, screenshots, and
product evidence follow the shared native/exact/approved-asset rules; image models are never
used as competitive evidence.
