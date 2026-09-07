---
name: social-media-team
description: Use when the user asks to run a social media content pipeline, automate YouTube/X content creation, scout trending videos, write scripts in a brand voice, design thumbnails, edit video, or run the daily content workflow. Triggers on "social media team", "daily content pipeline", "scout trends", "write a script for my channel", "thumbnail designer", "content automation".
allowed-tools: Bash, Read, Write, Edit, Skill, Agent, AskUserQuestion, WebFetch, WebSearch
metadata:
  legacy-frontmatter:
    argument-hint: '[daily | agent-name | setup | status]'
    user-invocable: true
---

# /social-media-team — AI Content Creation Team

Orchestrator that coordinates 7 specialized AI agents to automate social media
content creation. Each agent can run independently or as part of the daily pipeline.

## Agents

| # | Agent | What it does | Skill |
|---|-------|-------------|-------|
| 1 | **Channel Analyst** | Study your channel + competitors, build brand voice profile | `channel-analyst` |
| 2 | **Trend Scout** | Find outlier videos on YouTube and X daily | `trend-scout` |
| 3 | **Script Writer** | Write hook, intro (30s scripted), bullet-point body in your voice | `script-writer` |
| 4 | **Thumbnail Designer** | Reference trending thumbnails, generate your version | `thumbnail-designer` |
| 5 | **Video Editor** | Auto-edit footage: filler removal, captions, B-roll, intro layers | `video-editor` |
| 6 | **Daily Reporter** | Compile everything to Google Sheets + send email digest | `daily-reporter` |
| 7 | **Shorts Creator** | Repurpose long-form into shorts (Phase 2) | `shorts-creator` |

## First-Run Setup

If `~/.claude/skills/social-media-team/config.json` does not exist, run onboarding:

1. **YouTube Channel URL** — your channel to analyze
2. **Brand Voice** — adjectives describing your style (e.g., "conversational, energetic, practical")
3. **Brand Colors** — hex codes for thumbnails/graphics (e.g., "#3D5A3A, #F5F0E8, #8B6F47")
4. **Brand Font** — primary font name
5. **Competitor Channels** — YouTube URLs of 5-10 creators in your niche to monitor
6. **Target Platforms** — which platforms to scout (default: YouTube, X)
7. **Content Niche** — your topic area (e.g., "AI tools, AI business, AI automation")
8. **Ideal Customer Avatar** — who you're talking to
9. **Profile Photos** — paths to 2-3 photos of you for thumbnail generation
10. **API Keys** — prompt for each:
    - YouTube Data API v3 key
    - Google Sheets API credentials (service account JSON path)
    - Gmail API credentials (OAuth JSON path)
    - NanoBanana Pro API key (for thumbnail generation)
    - Descript API key (for video editing)
    - OpenRouter API key (optional, for model routing)

Save to `config.json`:
```json
{
  "channel_url": "https://youtube.com/@channel",
  "brand_voice": "conversational, energetic, practical",
  "brand_colors": ["#3D5A3A", "#F5F0E8", "#8B6F47"],
  "brand_font": "Inter",
  "competitors": ["url1", "url2"],
  "platforms": ["youtube", "x"],
  "niche": "AI tools, AI business",
  "ica": "solopreneurs and small business owners learning AI",
  "profile_photos": ["./photos/headshot1.png"],
  "outlier_window_days": 5,
  "outlier_threshold": 200,
  "viral_threshold": 500,
  "google_sheet_id": "sheet-id",
  "email_recipient": "you@email.com",
  "apis": {
    "youtube_data_api": "stored-securely",
    "google_sheets_credentials": "/path/to/service-account.json",
    "gmail_credentials": "/path/to/oauth.json",
    "nanobanana_api": "stored-securely",
    "descript_api": "stored-securely",
    "openrouter_api": "stored-securely"
  }
}
```

Store sensitive API keys in `~/.claude/skills/social-media-team/.env` (gitignored):
```
YOUTUBE_DATA_API_KEY=xxx
NANOBANANA_API_KEY=xxx
DESCRIPT_API_KEY=xxx
OPENROUTER_API_KEY=xxx
```

## Commands

### `/social-media-team daily`
Run the full daily pipeline:

**Stage 1: Scout (parallel)**
- Invoke **Trend Scout** to find today's outlier videos from YouTube + X
- Invoke **Channel Analyst** (if brand voice refresh is due — weekly)

**Pass forward:** outlier videos list, brand voice profile

**Stage 2: Create (sequential)**
- Invoke **Script Writer** with the top outlier topic + brand voice
  - Produces: title, hook, 30s scripted intro, bullet-point body, CTA
- Invoke **Thumbnail Designer** with the outlier reference thumbnails + brand assets
  - Produces: 3 thumbnail variants (1 reference-style, 2 custom-style)

**Pass forward:** script package + thumbnail options

**Stage 3: Report**
- Invoke **Daily Reporter** to push everything to Google Sheets + send email digest

### `/social-media-team scout`
Run only Trend Scout — find today's outlier videos.

### `/social-media-team script <topic>`
Run only Script Writer on a specific topic.

### `/social-media-team thumbnail <reference-url>`
Run only Thumbnail Designer from a reference.

### `/social-media-team edit <video-path>`
Run only Video Editor on uploaded footage.

### `/social-media-team shorts <video-path>`
Run only Shorts Creator on a long-form video.

### `/social-media-team analyze`
Run only Channel Analyst — refresh brand voice + competitor analysis.

### `/social-media-team status`
Show current config, last run date, and agent health.

### `/social-media-team setup`
Re-run onboarding to update config.

## Daily Schedule

This skill is designed to run daily via `/schedule`:
```
/schedule social-media-team daily --cron "0 7 * * *" --name "daily-content-scout"
```

This triggers the full pipeline every morning at 7 AM, delivering:
- Updated Google Sheet with outlier videos
- Draft script for the best topic
- 3 thumbnail options
- Email digest summary

## Output Directory

All daily outputs are saved to:
```
~/social-media-content/
├── YYYY-MM-DD/
│   ├── outliers.json           # Raw outlier data
│   ├── script.md               # Today's script
│   ├── thumbnails/             # Generated thumbnail images
│   │   ├── variant-1.png
│   │   ├── variant-2.png
│   │   └── variant-3.png
│   └── report.md               # Daily summary
├── brand-voice.md              # Latest brand voice profile
├── competitor-analysis.md      # Latest competitor breakdown
└── content-calendar.json       # Running calendar
```

## Error Handling

- If YouTube API quota is exceeded → fall back to WebFetch scraping
- If NanoBanana API fails → generate thumbnail brief as text description for manual creation
- If Gmail send fails → save digest to `report.md` and notify in terminal
- If any agent fails → continue pipeline with remaining agents, report partial results

---

## Skill Relationships

### Category
Business Automation

### Dependencies
Skills that must be installed for this skill to work:
- `mkt-brand-voice` — provides the voice-profile.md behavioral overlay consumed by Script Writer and Channel Analyst
- `mkt-visual-identity` — provides `tokens.json` (brand colors, font, logo) consumed by Thumbnail Designer

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `mkt-brand-voice` | Behavioral overlay | always — modifies HOW script-writer and channel-analyst run | `~/.claude/skills/social-media-team/voice-profile.md` |
| `mkt-visual-identity` | Sequential upstream | must run first on new channel setup | `~/.claude/skills/social-media-team/tokens.json` (colors, font, logo) |
| `landing-page-gen` | Domain cluster | same content-marketing vertical | — |
| `content-research` | Sequential upstream (optional) | when ingesting competitor content for Channel Analyst | `~/social-media-content/competitor-analysis.md` |
| `watch` | Sequential upstream (optional) | when a competitor video URL is given to Channel Analyst or Trend Scout | transcript + frames from `/watch` output |

### Runtime Preamble

At invocation, surface setup state:

- "First run? Run `/mkt-brand-voice` and `/mkt-visual-identity` before the daily pipeline — they write the voice profile and brand tokens the Script Writer and Thumbnail Designer consume."
- "If you have a competitor video URL, I can run `/watch` on it first and feed the transcript into the analysis."
- "Daily schedule: `0 7 * * *` via `/schedule social-media-team daily`."

---

## Gotchas

- **Voice profile must exist before Script Writer runs:** If `voice-profile.md` is missing, the script will not reflect the channel's brand voice — it falls back to generic output. Run `/mkt-brand-voice` → Channel Analyst as the prerequisite.
- **`tokens.json` must exist before Thumbnail Designer runs:** Without brand colors and font from `/mkt-visual-identity`, thumbnails will use arbitrary styling. Wire it on first setup.
- **YouTube Data API quota resets daily at midnight PST:** If quota is exceeded during the daily run, the fallback is WebFetch scraping — but WebFetch misses view-count data needed for outlier scoring. Schedule the run before the creator peak window (7 AM local is usually safe).
- **NanoBanana API does not batch:** Each thumbnail variant is a separate API call. If the key is invalid, the pipeline stops at Stage 2 — generate a text brief and continue rather than halting the whole pipeline.
- **Never hardcode profile photo paths in config:** Use relative paths from the repo root or environment variables. Machine-specific absolute paths break on any other host.
