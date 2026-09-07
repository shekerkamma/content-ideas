---
name: ai-strategy-brief
description: 'Use when someone wants a quick AI strategy summary, executive brief, or one-page decision memo rather than a full 30-page report. Triggers on: "give me a brief on X", "quick strategy memo", "one-pager on AI in X", "decision memo", "exec summary for AI strategy", "what''s the verdict on X". Also use when content-research or ai-strategy-researcher output should be distilled into a CXO-ready single page. For a full 30-page research report, use ai-strategy-researcher. (gstack)'
allowed-tools:
- Bash
- Read
- Write
- Edit
- WebSearch
- WebFetch
- AskUserQuestion
metadata:
  legacy-frontmatter:
    preamble-tier: 3
    version: 1.0.0
    argument-hint: '[topic or vertical -- e.g., ''AI-native insurance brokerage'']'
---

# AI Strategy Brief

Generate a concise, one-page executive decision memo for an AI strategy topic.

## Narrative Frame

**This skill's job:** Give a decision-maker one page they can act on — not a survey of what's possible, but a clear recommendation with the evidence that justifies it.

**Voice:** You are a senior strategy partner with 20 minutes of the CXO's time. You do not summarize the AI landscape. You answer: "What should we do, why, and by when?"

**Structure rules:**
- **Opening line:** The recommendation first. "Adopt X for Y use case. Expected return: $Z, timeline: N months."
- **Why now:** One market signal that makes this urgent. Name it, source it, name what happens if you wait 6 months.
- **What it takes:** Three bullets — resources, dependencies, risks. Specific, not hedged: "This requires a $200K budget and a dedicated ML engineer."
- **What success looks like:** One metric + one number + one date. Not "improved efficiency" → "35% reduction in contract review time by Q3 2026."
- **The alternative rejected:** What you're recommending against, and why in one line.
- **Named next action:** Who does what by when. Not "explore further" → "[Owner] approves budget by [date], assigns tech lead by [date +1wk]."

**Anti-patterns:** Do not survey options without picking one. Do not close without a named owner and date.

## Task

Given a topic or vertical, conduct focused research and produce a single-page Word document (.docx) that a CEO or investor can read in 2 minutes and act on.

## Research (Compressed)

Run these searches in parallel — collect signal, not exhaustive data:

1. **Market signal** -- What just happened? (largest recent fundraise, acquisition, or partnership)
2. **Competitive proof** -- Who is winning and at what scale? (top 3 companies, ARR/valuation)
3. **VC thesis** -- What are Sequoia/a16z/Emergence saying about this space?
4. **Risk signal** -- What has failed and why?

Aim for 8-12 high-quality sources. Depth over breadth.

## Document Format

Generate a single-page Word document with this exact structure:

### Layout: Decision Memo

```
EXECUTIVE BRIEF: {TOPIC}
Date: {date} | Sources: {count} references

---

THE SIGNAL
One paragraph (3-4 sentences). What just happened in this market
and why it matters now. Lead with the biggest number or event.

THE OPPORTUNITY
- Bullet 1: TAM / market size with source
- Bullet 2: Growth rate or adoption curve
- Bullet 3: Key structural advantage for AI-native players

WHO IS WINNING
| Company | Stage | Key Metric | Moat |
|---------|-------|------------|------|
| ...     | ...   | ...        | ...  |
(Top 3-5 companies, one row each)

THE RISK
2-3 sentences on Mirage PMF risk and primary failure mode.
What looks like product-market fit but isn't?

FRAMEWORK FIT
- Copilot vs Autopilot: {where this lands and why}
- Intelligence Ratio: {high/medium/low} -- {one-line justification}
- Verdict: {GO / CONDITIONAL / WAIT} with one-line rationale

REFERENCES (compact)
[1] Source Name -- URL
[2] Source Name -- URL
...
```

### Document Standards
- Single page -- max 500 words of body content
- `Calibri` font, `Pt(11)` body
- One table only (Who Is Winning)
- No cover page, no TOC -- this is a memo, not a report
- Bold section headers, tight spacing
- References as numbered footnotes at bottom

### File Output
- Save as: `{topic-slug}-brief-{month}{year}.docx`
- Example: `ai-native-insurance-brief-may2026.docx`
- Clean up Python generator script after creation

## Python Dependencies

```bash
pip install python-docx
```

## Quality Checklist

Before delivering:
- [ ] Fits on one printed page (under 500 words body)
- [ ] THE SIGNAL paragraph has a concrete number or event
- [ ] WHO IS WINNING table has 3+ companies with real metrics
- [ ] Framework verdict is one of: GO / CONDITIONAL / WAIT
- [ ] 8+ referenced URLs
- [ ] No fluff, no filler, every sentence carries signal

---

## Skill Relationships

### Category
Runbook

### Dependencies
- `python-docx` pip package — required for document generation (install via `pip install python-docx`)

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `content-research` | Sequential upstream | when ingested notes should feed the brief | `$SECOND_BRAIN_DIR/<type>/<slug>.md` |
| `ai-strategy-researcher` | Sequential upstream | when a full report should be distilled into a one-pager | `{topic-slug}-strategy-{month}{year}.docx` |
| `ai-analyst` | Sequential upstream | when quantitative analysis should feed the brief | analysis output file |
| `ai-strategy-researcher` | Alternative / Peer | when a full 30-page report is needed instead | `{topic-slug}-strategy-{month}{year}.docx` |
| `ai-strategy-council` | Alternative / Peer | when a multi-model council debate is preferred over a single-author brief | — |
| `branded-pptx-deck` | Sequential downstream | when the brief should be turned into a slide deck | `{topic-slug}-brief-{month}{year}.docx` |
| `presales-deal-prep` | Sequential downstream | when the brief feeds a sales deal prep | `{topic-slug}-brief-{month}{year}.docx` |

### Runtime Preamble
When invoked, surface: "I'll produce a one-page CXO-ready decision memo with a GO/CONDITIONAL/WAIT verdict. If you have notes from `/content-research` or a report from `/ai-strategy-researcher`, share the file path and I'll distill from that instead of re-researching. After delivery, run `/branded-pptx-deck` to turn this into slides, or `/presales-deal-prep` to build a deal brief."

---

## Gotchas

- **Do not hedge the verdict:** THE FRAMEWORK FIT section must end with exactly one of `GO`, `CONDITIONAL`, or `WAIT`. Never write "it depends" or leave the verdict open — that defeats the purpose of the memo.
- **Opening line is the recommendation, not the context:** The first sentence of the doc must be the recommendation ("Adopt X for Y. Expected return: $Z."). Do not open with background or market summary.
- **Word limit is a hard constraint:** The body must fit on one printed page (under 500 words). If research yields more material, cut — do not expand the document. Use the Quality Checklist before delivery.
- **python-docx not installed:** Check with `python3 -c "import docx"` before running the generator script. Install with `pip install python-docx` if absent.
- **Do not use ai-strategy-researcher as a substitute:** If the user asks for a "brief" or "one-pager", produce the brief even if you have enough research for a full report. The formats serve different audiences.
- **Named owner and date required:** Every brief must close with a named next action — who does what by when. "Explore further" or "continue evaluation" without an owner and date is a delivery failure.
- **File naming:** Use exact slug pattern `{topic-slug}-brief-{month}{year}.docx`. Delete the Python generator script after the file is saved.
