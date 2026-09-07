---
name: analytics-to-comms
description: 'Use when the user says "analyze and share", "run the numbers and present", "turn this data into a presentation", "data to stakeholders", or "analytics pipeline". End-to-end pipeline: run product analytics → visualize key finding as infographic → package into slides → post summary to Slack. For a one-page decision memo without a full data pipeline, use `ai-strategy-brief` instead.'
metadata:
  legacy-frontmatter:
    user_invocable: true
---

# Analytics-to-Comms Skill System

Orchestrator that chains four child skills to turn a data question into a
stakeholder-ready communication. Input: a business question + data source.
Output: analysis + visual + slides + Slack post.

## Onboarding (first run only)

If `~/.claude/skills/analytics-to-comms/config.json` does not exist, ask:

1. **Slack channel**: Default channel for posting results → default: none (skip Slack)
2. **Audience**: Technical / executive / mixed → default: executive
3. **Visual style**: Infographic / chart-only / both → default: both
4. **Auto-post to Slack?**: Yes (post automatically) / No (draft only) → default: No

Save as `config.json`.

## Pipeline

### Stage 1: Analyze → Discover
Invoke the `/analyze` skill (ai-analyst orchestrator).
- Run the full analytics pipeline on the user's question
- Explore data, identify trends, run statistical analysis
- Produce findings with supporting evidence
- Generate charts and data visualizations

**Pass forward:** key findings + charts + supporting data + methodology

### Stage 2: Explainer Graphic → Visualize
Invoke the `/explainer-graphic` skill on the #1 finding.
- Find an analogy that makes the key insight accessible to non-technical stakeholders
- Create a visual brief or self-contained HTML infographic
- Focus on the single most important takeaway

**Pass forward:** infographic HTML + visual brief + key insight statement

### Stage 3: Presentation → Package
Invoke the `/presentation` skill.
- Build a concise slide deck (5-7 slides, not the full 10)
- Slides: question → methodology → key finding → supporting data → recommendation → next steps
- Embed the infographic concept as a visual slide
- Add speaker notes for each slide

**Pass forward:** slide deck + executive summary

### Stage 4: Distribute → Team Visibility
Distribute outputs to team systems:
- Invoke **`/slack`** to post a summary message (one-line finding, key metric, recommendation) to the configured channel
- Invoke **`/notion`** to create a team-accessible page with the full analysis, charts, and recommendation
- If Slack not configured: skip and print the message to terminal
- If Notion not configured: skip and note in output

**Output files:**
```
<topic>-analysis.md
<topic>-explainer.html
<topic>-analytics-deck.pptx
<topic>-visual-spec.json
<topic>-slack-draft.md              (if Slack not auto-posted)
+ Notion page                       (if Notion configured)
```

## Completion

After all stages:
1. Print the **headline finding** in one sentence
2. Show the key metric
3. List all output files
4. Confirm Slack status (posted / drafted / skipped)

## Example usage

```
/analytics-to-comms "Why did retention drop 15% in Q1?" data.csv
/analytics-to-comms "Which plant has the highest defect rate?" — use the ops dashboard
/analytics-to-comms config
```

---

## Skill Relationships

### Category
Business Automation

### Dependencies
Skills that must be installed for this skill to work (none if standalone):
- `analyze` (ai-analyst) — Stage 1 analytics engine
- `explainer-graphic` — Stage 2 infographic generation
- `presentation` — Stage 3 slide deck packaging
- `slack` — Stage 4 distribution (optional)
- `notion` — Stage 4 distribution (optional)

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `analyze` (ai-analyst) | Sequential upstream | always (Stage 1) | `<topic>-analysis.md` + charts |
| `branded-pptx-deck` | Sequential downstream | optional — use instead of `presentation` for branded .pptx output | `<topic>-analytics-deck.pptx` |
| `ai-strategy-brief` | Alternative / Peer | analytics-to-comms = data-driven comms pipeline; ai-strategy-brief = strategy framing one-pager | — |

### Runtime Preamble
At invocation: "Starting analytics-to-comms pipeline: analyze → visualize → package → distribute. Do you want a branded .pptx deck (run `/branded-pptx-deck` in Stage 3 instead of `presentation`) or a standard HTML deck? Slack and Notion distribution are optional — configure in `~/.claude/skills/analytics-to-comms/config.json`."

## Gotchas

- **Stage 1 must use `/analyze`, not raw data exploration:** Always invoke the `ai-analyst` orchestrator for Stage 1. Do not substitute ad-hoc analysis — the ai-analyst pipeline produces structured findings the downstream stages depend on.
- **Slack not configured defaults to draft:** If `config.json` has no Slack channel, Stage 4 prints the message to terminal and saves `<topic>-slack-draft.md`. Do not auto-post without explicit channel configuration.
- **Config on first run:** If `~/.claude/skills/analytics-to-comms/config.json` is missing, run onboarding before the pipeline. Defaults exist but channel and audience settings matter.
- **Headline finding is mandatory:** The completion summary must include a one-sentence headline finding and the key metric. Never omit these even if earlier stages were abbreviated.
When the package includes PPTX, apply `pptx-visual-spec` before Stage 3, validate the visual
spec, and pass it to `branded-pptx-deck`. Analytical data, charts, and recommendations remain
native; generated imagery cannot serve as analysis evidence.
