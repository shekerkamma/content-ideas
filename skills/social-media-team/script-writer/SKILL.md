---
name: script-writer
description: "Write video scripts in your brand voice: punchy title, strong hook, 30s scripted intro, bullet-point body, CTA."
user-invocable: false
allowed-tools: Bash, Read, Write, Edit, Agent, WebFetch, WebSearch
---

# Script Writer Agent

Writes video scripts optimized for your brand voice and the outlier topic of the day.
Produces a complete content package: title, hook, scripted intro, body outline, and CTA.

## Inputs

- `brand-voice.md` — your voice profile from Channel Analyst
- `outliers.json` — today's outlier data from Trend Scout (or a user-specified topic)
- `config.json` — brand colors, ICA, niche

## Process

### Step 1: Select Topic & Angle

If running from the daily pipeline, use `outliers.json` → `top_recommendation`.

If a topic is provided directly, research it:
- WebSearch (Exa preferred) for recent coverage
- Check if any outlier videos cover this topic
- Find the unique angle that fits your brand voice

### Step 2: Title Generation

Create 5 title options. Rules:
- **6-10 words maximum** — short and punchy
- **Match what's working** — reference outlier video titles for proven patterns
- **Include a number or specific outcome** when possible
- **No clickbait** — the video must deliver what the title promises
- **Test for curiosity gap** — does the title make you want to click?

Title formulas that work:
- "How I [Result] with [Method]"
- "I [Did Thing] for [Time Period] — Here's What Happened"
- "[Number] [Things] That [Outcome]"
- "Stop [Common Mistake] — Do This Instead"
- "The [Adjective] Way to [Desired Outcome]"

Mark the recommended title with ★.

### Step 3: Hook (First Line)

Write 3 hook options for the opening line. The hook must:
- **Relate to the ICA immediately** — they should feel "this is for me"
- **Create a curiosity gap or emotional response** in under 5 seconds
- **NOT start with "Hey guys" or "What's up"** — start with the value

Hook formulas:
- **Problem hook**: "If you're [struggling with X], you're not alone..."
- **Stat hook**: "[Shocking number] — that's how many [thing]..."
- **Contrarian hook**: "Everyone says [common advice]. They're wrong."
- **Story hook**: "Last week I [did thing] and [unexpected result]..."
- **Demo hook**: "Watch this — [describe what's about to happen]"

### Step 4: Scripted Intro (30 seconds, ~75 words)

Write the full intro script word-for-word. Structure:

1. **Hook** (0-5s): The opening line from Step 3
2. **Relate** (5-10s): Connect to the viewer's pain/desire
3. **Opportunity** (10-18s): What they'll gain / what they're missing
4. **Proof/Tease** (18-25s): Quick flash of the result or demo
5. **Transition** (25-30s): "Let me show you exactly how..."

The intro must:
- Match the brand voice (use vocabulary from `brand-voice.md`)
- Feel natural when spoken aloud — no robotic phrasing
- Include a visual note: `[SHOW: brief demo of result]` for the tease section
- Build enough momentum that the viewer doesn't click away

### Step 5: Body Outline (Bullet Points)

After the intro, switch to bullet-point format (not full script).
The creator will riff naturally from these points.

Structure:
```markdown
## Body Outline

### Section 1: [Setup / Context] (0:30 - 2:00)
- Point A — key fact or context to establish
- Point B — why this matters right now
- [SHOW: screenshot/demo of X]

### Section 2: [The Method / Demo] (2:00 - 6:00)
- Step 1 — what to do first
  - Detail: specific tool/setting/approach
  - [SHOW: screen recording of doing it]
- Step 2 — next action
  - Detail: ...
- Step 3 — ...

### Section 3: [Results / Proof] (6:00 - 8:00)
- Result 1 — what happened
- Result 2 — unexpected benefit
- [SHOW: before/after or metrics]

### Section 4: [What I'd Do Differently / Advanced Tips] (8:00 - 9:00)
- Tip 1 — ...
- Tip 2 — ...
```

Each section should have:
- Time estimate
- 2-4 bullet points (not paragraphs)
- `[SHOW: ...]` visual cues where B-roll or screen recording is needed
- A **retention hook** at section transitions: mini-cliffhanger or curiosity bridge

### Step 6: CTA

Write the call-to-action for the end of the video:
- **Primary CTA**: subscribe / like / comment prompt (match brand voice)
- **Comment prompt**: a specific question that invites engagement
  - e.g., "Drop a comment: what's ONE task you'd automate first?"
- **Next video tease**: one line teasing the next video topic

### Step 7: Recording Companion

Generate a clean, teleprompter-friendly version of just the intro:
- Large text, short lines (4-6 words per line)
- No markdown formatting
- Designed to be read naturally while looking at camera

```
If you're trying to build
income with AI
but you're spending more time
watching tutorials
than actually building...

This video is going to
change everything.

I just built a system
that does [X]
completely automatically.

Let me show you
exactly how.
```

### Step 8: Output

Save to `~/social-media-content/YYYY-MM-DD/script.md`:

```markdown
# [★ Recommended Title]

**Date**: YYYY-MM-DD
**Topic**: [from outlier or user input]
**Reference**: [outlier video URL that inspired this]
**Estimated Length**: X-Y minutes

## Title Options
1. ★ [recommended]
2. [option 2]
3. [option 3]
4. [option 4]
5. [option 5]

## Hook Options
1. ★ [recommended]
2. [option 2]
3. [option 3]

## Scripted Intro (30s)
[Full word-for-word script with [SHOW:] cues]

## Body Outline
[Bullet-point sections]

## CTA
[End-of-video call to action]

## Teleprompter
[Clean reading version of intro]

## Thumbnail Brief
[Suggested text overlay + visual concept — fed to Thumbnail Designer]
```
