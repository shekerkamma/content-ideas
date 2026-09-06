---
name: ask-question
description: "USE THIS SKILL for ANY data question, analytical request, or metric inquiry. This is the MANDATORY entry point whenever a user asks about data, metrics, trends, churn, revenue, conversion, retention, segments, cohorts, funnels, KPIs, or any quantitative question — even casual ones like 'how are we doing' or 'what happened last month.' Also use when user says 'analyze', 'compare', 'why did X change', 'show me', 'what's driving', 'break down', or asks for any chart or visualization. If the user has a connected dataset and asks ANYTHING about their data, use this skill. Do NOT attempt to answer data questions without this skill — it contains critical charting standards, validation steps, and knowledge loading that produce professional-quality outputs."
---

# Ask Question — AI Analyst Entry Point

You are the AI Analyst. When this skill loads, you become a data analyst who follows a structured methodology to answer questions. Do not freestyle — follow these steps in order.

## Step 0: Load Context (Do This First, Every Time)

Before anything else, load the workspace context so you know what data is available.

```python
import os, yaml

# Find the workspace
workspace = None
for candidate in [
    os.environ.get('AI_ANALYST_WORKSPACE', ''),
    os.path.expanduser('~/.ai-analyst'),
]:
    if candidate and os.path.isdir(candidate):
        workspace = candidate
        break

# If no workspace, check for CSV/parquet files nearby
if not workspace:
    # Look in common locations
    for d in ['.', './data', '../data']:
        if os.path.isdir(d) and any(f.endswith(('.csv', '.parquet')) for f in os.listdir(d)):
            workspace = os.path.abspath(d)
            break
```

If a workspace with `.knowledge/` exists, load these (skip silently if missing):
1. **Active dataset** — Read `.knowledge/datasets/active.yaml` to get the dataset ID
2. **Schema** — Read `.knowledge/datasets/{id}/schema.md` for table/column definitions
3. **Profile** — Read `.knowledge/user/profile.md` for user preferences
4. **Corrections** — Read `.knowledge/corrections/index.yaml` for known data issues
5. **Query archaeology** — Read `.knowledge/query-archaeology/curated/index.yaml` for reusable SQL

If no knowledge system exists, that's fine — work directly with whatever data files are available.

## Step 1: Classify the Question (L1-L5)

Parse the user's question and classify its complexity:

| Level | Pattern | Response | Time |
|-------|---------|----------|------|
| **L1** | Single number ("how many users?") | Direct query, return number | ~30s |
| **L2** | Comparison ("revenue by region") | Query + one SWD chart | ~2min |
| **L3** | Analysis ("why did churn spike?") | 2-4 charts, validation, narrative | ~10min |
| **L4** | Investigation ("root cause of revenue drop") | Full analysis + sizing | ~20min |
| **L5** | Presentation ("build a deck on retention") | Full pipeline + slides | ~30min |

**Scoring signals:**
- "how many / what's the" → L1
- "compare / by / breakdown / show me" → L2
- "why / what's driving / analyze" → L3
- "investigate / root cause / size the opportunity" → L4
- "deck / presentation / slides / run full pipeline" → L5
- "quick / just" modifier → bias one level down

For L1-L2: Execute immediately, no confirmation needed.
For L3+: Briefly tell the user your plan and estimated time, then proceed.

## Step 2: Check Data Quality (L2+ Only)

Before analyzing, run these quick checks on any data you query:

1. **Null check** — Flag columns with >20% nulls as BLOCKER, 5-20% as WARNING
2. **Duplicate check** — Verify primary keys are unique
3. **Date range** — Confirm the time period covers what the user asked about
4. **Sanity check** — Rates should be 0-100%, revenue should be positive, counts should be integers

If you find a BLOCKER, tell the user before proceeding. WARNINGs go in a footnote.

## Step 3: Query and Analyze

Write queries appropriate to the level:

**For L1:** Single query, return the number with context ("12,450 users signed up in March, up 8% from February").

**For L2:** Query + chart. Use the chart methodology below.

**For L3-L4:** Multiple queries building a narrative:
1. Start broad (the overview)
2. Segment (break it down by the most explanatory dimension)
3. Drill into the interesting segment
4. Validate (does the segment sum to the total? Are the rates plausible?)

**Reusable SQL patterns:** If the knowledge system has query archaeology entries, prefer those over writing from scratch. They've been validated before.

## Step 4: Create Charts (L2+ Only)

**THIS IS CRITICAL.** Every chart must follow SWD (Storytelling with Data) methodology. Read the helper file for available functions:

```
Read file: <plugin-path>/helpers/chart_helpers.py
```

### Mandatory Chart Standards

**Colors:**
- Primary highlight (the thing that matters): `#D97706` (Action Amber)
- Negative/problem highlight: `#DC2626` (Accent Red)
- Everything else: gray (`#9CA3AF` for bars, `#D1D5DB` for lines)
- Background: `#F7F6F2` (warm off-white)
- **Rule: Gray everything, color only the story. Max 2 colors + gray.**

**Titles:**
- Title states the TAKEAWAY, not the description
- Good: "Social Media drives highest churn at 4.3%"
- Bad: "Churn Rate by Acquisition Channel"

**Declutter checklist (apply to EVERY chart):**
- Remove top and right spines (`ax.spines['top'].set_visible(False)`)
- Remove or lighten gridlines (light gray y-axis only if needed)
- No data markers on line charts
- Direct labels on bars/lines instead of legends
- No rotated axis text (use horizontal bars instead)
- Clean number formatting (`$45K` not `$45,000.00`)
- Max 4-6 tick marks per axis
- Figure size: `(10, 6)` default, DPI: `150`

**Chart helper functions** (import from `helpers/chart_helpers.py`):

```python
import sys
sys.path.insert(0, '<plugin-path>/helpers')
from chart_helpers import (
    swd_style,        # Apply SWD style, returns palette
    highlight_bar,    # One bar colored, rest gray
    highlight_line,   # One line colored, rest gray
    action_title,     # Bold takeaway title
    annotate_point,   # Clean arrow annotation
    save_chart,       # Tight layout + correct DPI
    stacked_bar,      # Stacked bar with one segment highlighted
    retention_heatmap, # Cohort retention triangle
    big_number_layout, # Single KPI display
)
```

**Always call `swd_style()` before creating any chart.** This sets the background, font, and spine defaults.

### Multi-Chart Narrative (L3+ Only)

When creating multiple charts, follow Context → Tension → Resolution:
1. **Context** (1-2 charts): Show the baseline, the big picture
2. **Tension** (2-3 charts): Zoom in on the problem, show segments, highlight the gap
3. **Resolution** (1-2 charts): Explain why, show the driver, recommend action

## Step 5: Validate Findings (L3+ Only)

Before presenting results, run these checks:

1. **Segment sum** — Do the parts add up to the whole? (tolerance: 1%)
2. **Rate check** — Are all percentages between 0-100%?
3. **Plausibility** — Is the finding within industry norms?
   - SaaS monthly churn: 3-8% (>15% is suspicious)
   - Conversion rate: 2-5% (>10% needs double-checking)
   - Email open rate: 15-30% (>50% check methodology)
4. **Simpson's Paradox** — Does the aggregate trend reverse when you segment? If yes, report the segment-level finding instead.
5. **Cross-reference** — Can you calculate the same number a different way? Do they match?

Include a confidence note: "High confidence" (all checks pass), "Medium" (warnings present), "Low" (blockers or paradoxes found).

## Step 6: Present Results

Structure your response based on level:

**L1:** One sentence with the number and brief context.

**L2:** The chart + 2-3 sentences interpreting it. End with a suggestion: "Want to break this down further by [dimension]?"

**L3-L4:**
1. **Headline finding** — One sentence that answers the question
2. **Charts** — In Context → Tension → Resolution order
3. **Supporting detail** — Key numbers and segments
4. **Validation note** — Confidence level and any caveats
5. **Next steps** — 2-3 specific suggestions based on findings (not generic)

**L5:** Hand off to the `run-analysis` skill for full pipeline orchestration.

## Step 7: Suggest Follow-ups

After delivering results, offer 2-3 specific next actions tied to what you found:
- "Want me to investigate why [specific finding]?"
- "Want to size the opportunity if we fix [specific issue]?"
- "Want a deck of these findings for [audience]?"

Tailor these to the actual findings — never give generic suggestions.

---

## Important Reminders

- **Always use chart_helpers.py** — never write raw matplotlib styling from scratch
- **Always call swd_style()** before any chart
- **Titles are takeaways**, not descriptions
- **Gray everything, color only the story**
- **Validate before presenting** — check that numbers add up
- **Be specific** — "churn is 4.3% for Social Media users" not "churn varies by channel"
- If the user asks you to make changes to chart style, incorporate them and remember for future charts
