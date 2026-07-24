---
name: ikigai
description: "Use when someone asks for ikigai analysis, founder positioning, career clarity, or solo-founder niche discovery for a person — triggers on 'run ikigai for <name>', 'ikigai analysis', 'solo founder analysis', 'career positioning', 'founder positioning', 'solo founder positioning', or when a LinkedIn profile (PDF path, URL, or pasted text) is provided and the user wants a written report only (no slide deck). Also triggers on: \"solo founder positioning\". For report + deck in one command, use ikigai-gamma-slidedeck instead."
triggers:
  - ikigai
  - ikigai analysis
  - solo founder analysis
  - career positioning
  - linkedin profile
  - founder positioning
version: "1.0"
validated_on: "runs/2026-06-13-shravan-ikigai-genspark"
---

# Ikigai Skill

Turn a LinkedIn profile into a full Ikigai Pro solo-founder analysis report.

## Narrative Frame

**This skill's job:** Tell this person the niche they should own — specifically enough that they could write a cold email today and it would land.

**Voice:** You are a career strategist who has worked with 200 founders and senior operators. You do not reflect their LinkedIn back at them. You synthesize it into something they haven't said out loud yet but will recognize as true the moment they read it.

**Per-section voice rules:**
- **Ikigai columns (love/good at/world needs/paid for):** Each item is a named, specific capability — not a category. Not "leadership" → "leading a 12-person distributed team through a product pivot under funding pressure."
- **Niche statement:** One sentence. "X who helps Y achieve Z without W." Specific enough that the person could use it verbatim as a LinkedIn headline.
- **Validation score:** The score is secondary. The primary output is the one sentence that names why the score is what it is and what would make it higher.
- **Offer architecture:** Three tiers — entry, core, premium — with specific price points and a named deliverable per tier. Not "consulting packages" → "$2,500 for a 90-minute AI readiness assessment with a written recommendation report."
- **7-day launch plan:** Day 1 is a single action that takes under 2 hours and produces a visible artifact. Day 7 is the first conversation with a potential client.

**Anti-patterns:**
- Do not describe their background — synthesize it into a forward-looking position
- Do not list generic strengths — name the specific intersection that no one else in this space has
- Do not give income ranges — give income math: N clients × $X = $Y/mo, with churn assumption

## Use When

- User provides a LinkedIn profile (PDF path, URL, or pasted text)
- User asks for ikigai analysis, founder positioning, or career clarity for a person
- User says "run ikigai for <name>"

## Required Inputs

| Input | Required | Notes |
|---|---|---|
| `profile_source` | Yes | PDF path (Windows or WSL), LinkedIn URL, or pasted text |
| `person_name` | Yes | Full name or first name for the run folder |
| `context` | Optional | Any additional context the user provides about the person's goals |

## Output

- Run folder: `runs/YYYY-MM-DD-<name>-ikigai/`
- Primary artifact: `<name>-ikigai-report.md` — full structured report
- Secondary (optional): slide deck via `branded-pptx-deck` or Genspark

---

## Workflow

### Stage 1 — Ingest the Profile

1. If source is a PDF path:
   - Convert Windows path `C:\...` → WSL path `/mnt/c/...`
   - Read the PDF using the Read tool
2. If source is a LinkedIn URL: fetch and extract text
3. If source is pasted text: use as-is
4. Extract all facts: current role, company, tenure, previous roles, industries covered, geographies, notable achievements, education, skills, patents, publications, entrepreneurial ventures

### Stage 2 — Four Ikigai Columns

Derive each column from profile evidence. Do not invent — anchor every item to a specific role, achievement, or stated preference.

**What They Love**
- Activities and contexts they repeatedly return to across roles
- Entrepreneurial ventures they initiated unprompted
- Passion signals in role descriptions and summaries

**What They're Good At**
- Demonstrated outcomes (revenue growth, team sizes, products shipped, funding raised)
- Rare skill combinations that appear across multiple roles
- IIT/IIM or equivalent pedigree as analytical foundation
- Cross-industry or cross-geography pattern recognition

**What the World Needs**
- Current market problems in the industries/segments they know
- Gaps that large incumbents can't fill at the speed/price/specialization level this person can
- Timing signals: regulations, AI wave, market growth data

**What Pays**
- Pricing benchmarks for the niche (consulting retainers, advisory fees, fractional CXO rates)
- Deal sizes typical in their target segment
- Margin structure if India-based delivery is a factor

### Stage 3 — Niche Statement

Write a single crisp niche statement:
> "I [verb] for [specific buyer] who [specific pain] — delivered by someone who [unique credibility proof]."

Then derive:
- **Layer 1 — Market**: The broad segment (GCCs, ISVs, BFSI, etc.)
- **Layer 2 — Niche**: The specific sub-segment with the sharpest pain
- **Layer 3 — Problem**: The exact problem they solve that nobody else can

### Stage 4 — Validation Score

Score the niche on 6 dimensions, each out of 10:

| Dimension | Score | Evidence |
|---|---|---|
| Pain Intensity | /10 | How acute is the buyer's problem right now? |
| Purchasing Power | /10 | Can the target buyer pay $15K–$45K/month? |
| Ease to Find | /10 | How concentrated/reachable is this buyer segment? |
| Market Growth | /10 | Is this segment growing, flat, or shrinking? |
| Competition Difficulty | /10 | How hard is this position to copy? |
| Founder-Market Fit | /10 | How uniquely qualified is this person? |

Composite = sum × 1.67 (normalised to 100).

Interpret:
- 85–100: EXCEPTIONAL
- 70–84: STRONG GO
- 55–69: VIABLE with refinement
- Below 55: Needs repositioning

### Stage 5 — Market Intelligence

**Avoid** — where not to compete (wrong price tier, wrong speed, wrong buyer)

**Gap to Own** — the specific whitespace nobody currently occupies

**Timing Signals** — why now (market data, regulatory shifts, technology unlock)

**Competitor Landscape** — table: Competitor Type | Pricing | Falls Short

### Stage 6 — Offer Architecture

Design 3 tiers:

| Tier | Price/Month | What's Included | Ideal Client |
|---|---|---|---|
| Foundation | $X | Core deliverable | Entry buyer |
| Accelerator ★ | $Y | Core + async support + speed SLA | Main tier |
| Partner | $Z | Full co-development + strategy | Strategic client |

Then produce:
- **Income Math**: milestone table (first revenue → replace current comp → $100K/mo → scale)
- **7-Day Launch Plan**: Days 1–3 (build proof point) + Days 4–7 (activate network)
- **12–18 Month Trajectory**: Phase 1–4 with revenue targets

### Stage 7 — One-Liner

Write a single killer positioning sentence the person can use on LinkedIn, in intro calls, and as their profile headline.

---

## Review Gate

**Stop after Stage 2** and confirm with the user before proceeding if:
- The profile is sparse (less than 3 roles with substance)
- The four columns are thin and speculative
- There is a significant ambiguity about what segment to target

Otherwise proceed through all 7 stages automatically and present the full report.

---

## Output Format

Write the report to `runs/YYYY-MM-DD-<name>-ikigai/<name>-ikigai-report.md`.

Structure:

```
# Ikigai Pro Report — <Full Name>
<Tagline from current role/summary>

## The Core Insight
<Structural advantage in 2–3 sentences>

## Profile
<Experience summary table>

## The Four Ikigai Columns
### What They Love
### What They're Good At
### What the World Needs
### What Pays

## Niche Statement
<Layer 1 / Layer 2 / Layer 3>

## Validation Score
<Scorecard table + composite + interpretation>

## Market Intelligence
<Avoid / Gap to Own / Timing / Competitor table>

## Offer Architecture
<3-tier table + income math>

## 7-Day Launch Plan
<Days 1–3 + Days 4–7>

## 12–18 Month Trajectory

## Your One-Liner
```

---

## Framing Rule — Company vs Individual

When the person is in a BD / sales / partnerships role at a technology company (not a solo founder or independent consultant):

- **Reframe the ikigai around the company's capabilities**, not the individual's independent services
- The "What the World Needs" column must list the company's specific products, platforms, and services — not generic advice the individual could give alone
- The individual's background is the **trust and access layer** (door opener, credibility signal) — not the primary offering
- The offer architecture must describe company engagement tiers, not personal consulting rates
- The one-liner should position the individual as the trusted enabler who brings the company's capability stack to the buyer

Validated on: Srikumar V R (FPT Software) — Jun 2026

When the person IS a solo founder or independent consultant, revert to the individual-first framing (validated on Shravan Siramdas, Jun 2026).

## Do Not

- Invent achievements not evidenced in the profile
- Skip the validation score — it is the most credible output for the person
- Generate the deck without user confirmation (deck is optional Stage 8)
- Use generic consulting language — anchor every claim to profile evidence
- Mark scores higher than the evidence supports
- Position a BD/partnerships person at a company as an independent advisor — always frame around the company's capabilities first

## Success Criteria

- All 7 stages completed
- Report file exists at the correct path
- Every ikigai column item is traceable to a specific role or achievement
- Validation score has explicit evidence per dimension
- Niche statement is specific enough that the person could use it tomorrow

## Failure Handling

If profile is missing or unreadable:
- Report the exact path or URL that failed
- Ask the user for an alternative input (paste the text directly)
- Do not proceed with invented profile data

---

## Resources

- Reference implementation: `../../../runs/2026-06-13-shravan-ikigai-genspark/shravan-ikigai-report-extracted.txt`
- Skill-building playbook: `../../../docs/skill-building-playbook.md`
- **Full pipeline (report + deck in one command)**: use `ikigai-gamma-slidedeck` skill
  - Gamma MCP path (primary): generates Gamma presentation, returns gammaUrl
  - pptxkit fallback path: generates `build_deck.py` + validated .pptx + Desktop copy
  - See `.agents/skills/ikigai-gamma-slidedeck/SKILL.md`

---

## Skill Relationships

### Category
Runbook

### Dependencies
None required. Standalone — runs from a LinkedIn profile source alone.

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `ikigai-gamma-slidedeck` | Sequential downstream | always — report is the primary input for the deck pipeline | `runs/YYYY-MM-DD-<name>-ikigai/<name>-ikigai-report.md` |
| `ikigai-gamma-slidedeck` | Peer / Alternative | use this skill (report only) when deck is not needed; use ikigai-gamma-slidedeck when report + deck in one command | — |
| `gcc-roadmap` | Sequential downstream (optional) | BD/company-first framing only — invoked from ikigai-gamma-slidedeck after report | ikigai report (company capabilities section) |

### Runtime Preamble

At invocation, surface this if relevant:

> "Do you want a report only, or a report + slide deck?
> For report only: this skill. For report + deck in one command: use `/ikigai-gamma-slidedeck` instead.
> After the report is complete, you can pipe it to `/ikigai-gamma-slidedeck` to generate the deck separately."

---

## Gotchas

- **Do not invent achievements:** Every ikigai column item must be traceable to a specific role, achievement, or stated fact in the profile. Invented items destroy credibility — the person will immediately spot what isn't true.
- **Sparse profiles require a user checkpoint:** If the profile has fewer than 3 substantive roles, stop after Stage 2 and confirm with the user before proceeding. A thin profile produces a thin and speculative report that the person won't trust.
- **BD/partnerships roles must use company-first framing:** A BD/sales/partnerships person at a tech company is NOT a solo founder. Their offer architecture is the company's engagement tiers, not personal consulting rates. The framing rule is: "person = trusted door-opener; company = the product." Validated on Srikumar V R (FPT Software), Jun 2026.
- **Validation score must have explicit per-dimension evidence:** The score is secondary to the evidence. Never output a score without the evidence column populated. A score without evidence is a guess.
- **Niche statement must be specific enough to use verbatim:** If the niche statement could apply to any senior professional in the space, it failed. Test: could the person put this on their LinkedIn headline and DM 5 prospects with it today? If not, rewrite.
- **Deck is optional and requires user confirmation:** Never generate the deck without the user confirming. The report is the primary artifact. Stage 8 (deck) is not automatic.
