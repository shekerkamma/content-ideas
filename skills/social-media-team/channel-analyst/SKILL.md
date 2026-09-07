---
name: channel-analyst
description: "Study your YouTube channel and competitors — build brand voice profile, analyze content performance, identify positioning gaps."
user-invocable: false
allowed-tools: Bash, Read, Write, Edit, Agent, WebFetch, WebSearch
---

# Channel Analyst Agent

Studies your YouTube channel and competitor channels to build a brand voice profile,
identify what's working, and spot positioning gaps.

## Inputs

- `config.json` — channel URL, competitor URLs, niche, ICA
- YouTube Data API key from `.env`

## Process

### Step 1: Analyze Your Channel

Use YouTube Data API v3 to pull:

```bash
# Channel stats
curl -s "https://www.googleapis.com/youtube/v3/channels?part=statistics,snippet,brandingSettings&forHandle=HANDLE&key=$YOUTUBE_DATA_API_KEY"

# Recent videos (last 50)
curl -s "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=CHANNEL_ID&order=date&maxResults=50&type=video&key=$YOUTUBE_DATA_API_KEY"

# Video stats for each
curl -s "https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails,snippet&id=VIDEO_IDS&key=$YOUTUBE_DATA_API_KEY"
```

Extract:
- **Channel overview**: subscribers, total views, video count, join date
- **Top 10 performing videos**: by views, by engagement rate (likes+comments/views)
- **Average performance**: views per video, likes per video, comments per video
- **Upload frequency**: average days between uploads
- **Content themes**: categorize videos by topic, find which topics perform best
- **Title patterns**: average length, common words, question vs statement
- **Video length sweet spots**: which durations get the most views

### Step 2: Build Brand Voice Profile

From the top 10 videos, analyze (use WebFetch on video pages or transcript if available):

- **Tone**: formal/casual, energetic/calm, technical/accessible
- **Opening patterns**: how do you typically start videos?
- **Vocabulary**: recurring phrases, catchphrases, filler words
- **Teaching style**: tutorial / demo / commentary / storytelling / interview
- **Personality markers**: humor style, personal stories, relatability signals
- **CTA patterns**: how and when do you ask viewers to subscribe/like/comment

Produce a `brand-voice.md`:
```markdown
# Brand Voice Profile

## Voice Attributes
- **Tone**: [e.g., conversational, energetic, practical]
- **Teaching style**: [e.g., demo-first, explain-while-building]
- **Personality**: [e.g., relatable solopreneur, learning-in-public]

## Speech Patterns
- **Common phrases**: ["let's dive in", "here's the thing", ...]
- **Intro style**: [e.g., problem → promise → proof]
- **CTA style**: [e.g., casual ask at end, mid-roll prompt]

## Content Patterns
- **Best performing topics**: [ranked list]
- **Ideal video length**: [X-Y minutes]
- **Upload cadence**: [X videos/week]

## Audience
- **Who they are**: [from ICA + comment analysis]
- **What they want**: [from top video topics]
- **Their language**: [terms they use in comments]
```

### Step 3: Competitor Analysis

For each competitor channel, pull the same data and extract:

- **Channel size**: subscribers, views, video count
- **Content strategy**: posting frequency, video length, topics
- **Top 5 videos**: what popped and why
- **Differentiation**: how they position vs others in the niche
- **Gaps**: topics they cover that you don't (and vice versa)

**Prioritize smaller creators** (under 50K subscribers) whose videos are outperforming their channel average — these are the hidden gems.

Produce a `competitor-analysis.md`:
```markdown
# Competitor Analysis

## Channel Comparison Table
| Channel | Subs | Avg Views | Upload Freq | Top Topic | Outlier Score |
|---------|------|-----------|-------------|-----------|---------------|

## Per-Channel Breakdown
### [Channel Name]
- **Positioning**: ...
- **What works**: ...
- **Gap opportunity**: ...

## Your Competitive Advantages
- ...

## Topics You Should Cover
- ... (based on competitor success + your voice fit)
```

### Step 4: Save Outputs

Write to:
- `~/social-media-content/brand-voice.md`
- `~/social-media-content/competitor-analysis.md`

## Refresh Cadence

- **Brand voice**: weekly (or on-demand via `/social-media-team analyze`)
- **Competitor analysis**: weekly
- Track `last_analyzed` timestamp in config.json
