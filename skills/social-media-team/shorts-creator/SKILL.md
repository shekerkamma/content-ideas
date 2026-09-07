---
name: shorts-creator
description: "Phase 2: Repurpose long-form videos into YouTube Shorts, TikToks, and Instagram Reels automatically."
user-invocable: false
allowed-tools: Bash, Read, Write, Edit, Agent, WebFetch, WebSearch
---

# Shorts Creator Agent (Phase 2)

Repurposes long-form video content into short-form clips optimized for
YouTube Shorts, TikTok, and Instagram Reels.

## Inputs

- Long-form video file (edited, from Video Editor)
- `script.md` — full script with section markers
- `config.json` — brand colors, font, profile photos
- Descript API key from `.env`

## Process

### Step 1: Identify Clip-Worthy Moments

Analyze the long-form video script and footage for segments that work as shorts:

**Criteria for a good short:**
- **Self-contained insight** — makes sense without the full video context
- **Strong opening** — first 2 seconds must hook (no "in this video" intros)
- **Duration**: 30-60 seconds ideal, never over 90 seconds
- **Visual interest** — demo, result, reaction, or animated explanation
- **Shareability** — would someone send this to a friend?

**Common clip types:**
1. **The Hook** — the video's intro (first 30s) repackaged as a standalone
2. **The Aha Moment** — a surprising result or revelation
3. **The Quick Demo** — a single feature/tool shown in action
4. **The Hot Take** — a bold opinion or contrarian statement
5. **The Before/After** — transformation or comparison

Target: **3-5 shorts per long-form video**.

### Step 2: Extract Clips via Descript

For each identified moment:

```
Underlord prompt: "Extract the segment from [start_time] to [end_time].
Reformat for vertical (9:16 aspect ratio):
- Crop to center on face/screen as appropriate
- Add word-by-word animated captions (full duration, centered)
- Font: [brand font], Color: [brand color], Size: large, bold keywords
- Add subtle background music at 15% volume
- No intro bumper — start immediately with the hook
- Add a 1-second branded end card with channel handle"
```

### Step 3: Platform-Specific Optimization

#### YouTube Shorts
- Aspect ratio: 9:16 (1080x1920)
- Duration: 30-60 seconds
- Captions: burned in (YouTube auto-captions are unreliable on Shorts)
- Title: 40 characters max, no hashtags in title
- Description: hashtags here (#Shorts #AI #topic)

#### TikTok
- Aspect ratio: 9:16 (1080x1920)
- Duration: 30-60 seconds (sweet spot: 45s)
- Captions: burned in, slightly larger font
- Trending sounds: check if a trending audio could work (optional)
- Text hook on screen in first frame

#### Instagram Reels
- Aspect ratio: 9:16 (1080x1920)
- Duration: 30-60 seconds
- Captions: burned in
- Cover image: frame that looks good in the grid (square crop preview)
- Caption: longer form with hashtags (up to 30)

### Step 4: Title & Description per Short

For each clip, generate:

```markdown
## Short [N]: [clip type]

### Content
- **Source**: [long-form video title]
- **Segment**: [start_time - end_time]
- **Clip type**: [hook / aha / demo / hot take / before-after]
- **Duration**: [seconds]

### YouTube Shorts
- **Title**: [40 chars max]
- **Description**: [with hashtags]

### TikTok
- **Caption**: [with hashtags and hook text]
- **Text overlay**: [first-frame text]

### Instagram Reels
- **Caption**: [longer, with 10-15 hashtags]
- **Cover frame**: [timestamp for best cover image]
```

### Step 5: Output

Save to `~/social-media-content/YYYY-MM-DD/shorts/`:
- `short-1-hook.mp4`
- `short-2-aha.mp4`
- `short-3-demo.mp4`
- `shorts-plan.md` — all titles, descriptions, and posting schedule

```markdown
# Shorts Plan — YYYY-MM-DD

## Source Video
- **Title**: [long-form title]
- **Duration**: [original length]
- **Shorts extracted**: [count]

## Posting Schedule
| Day | Platform | Short | Title | Best Time |
|-----|----------|-------|-------|-----------|
| Mon | YouTube  | short-1-hook.mp4 | [title] | 2:00 PM |
| Mon | TikTok   | short-1-hook.mp4 | [title] | 7:00 PM |
| Tue | Instagram| short-1-hook.mp4 | [title] | 12:00 PM |
| Wed | YouTube  | short-2-aha.mp4  | [title] | 2:00 PM |
| ... | ...      | ...              | ...     | ...      |

## Per-Short Details
[detailed breakdown per clip]
```

### Step 6: Stagger Posting

Shorts should NOT all post on the same day. Recommended cadence:
- **Day 1**: Short 1 on YouTube + TikTok
- **Day 2**: Short 1 on Instagram + Short 2 on YouTube
- **Day 3**: Short 2 on TikTok + Instagram
- **Day 4-5**: Short 3 across platforms

This maximizes reach and avoids flooding any single platform.

## Status

**Phase 2** — this agent activates after the long-form pipeline is stable.
When ready, enable in config.json: `"shorts_enabled": true`
