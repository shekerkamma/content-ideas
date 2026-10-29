---
name: trend-scout
description: "Find outlier videos on YouTube and X daily — rank by outlier score, prioritize small creators popping off."
user-invocable: false
allowed-tools: Bash, Read, Write, Edit, Agent, WebFetch, WebSearch
---

# Trend Scout Agent

Scans YouTube and X daily to find videos and posts that are significantly
outperforming their creator's average — the outlier signal.

## Inputs

- `config.json` — competitor channels, niche keywords, platforms, outlier thresholds
- YouTube Data API key from `.env`

## Outlier Score Formula

```
Outlier Score = (Video Views in N days / Channel Average N-day Views) × 100
```

- `N` = `outlier_window_days` from config (default: 5 days)
- Score > **200** = strong outlier (2x normal)
- Score > **500** = viral outlier (5x normal)

Agent flags videos with score > `outlier_threshold` (default: 200).

**Priority weighting**: smaller creators (under 50K subs) with high outlier scores
are ranked ABOVE large creators with the same score. A 10K-sub channel getting
5x their normal views is a stronger signal than a 1M-sub channel getting 2x.

## Process

### Step 1: YouTube Outlier Scan

For each competitor channel in config:

```bash
# Get channel's recent videos (last 7 days)
curl -s "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=CHANNEL_ID&order=date&publishedAfter=DATE_ISO&maxResults=10&type=video&key=$YOUTUBE_DATA_API_KEY"

# Get view counts for those videos
curl -s "https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet,contentDetails&id=VIDEO_IDS&key=$YOUTUBE_DATA_API_KEY"

# Get channel's average views (from last 50 videos for baseline)
# Calculate: total views of last 50 / 50 = channel average
```

For each video, compute:
- **Views** in the outlier window
- **Channel average** views for similar-age videos
- **Outlier score**
- **Engagement rate**: (likes + comments) / views × 100
- **Title** and **thumbnail URL**

Also scan for **niche keywords** beyond just competitor channels:

```bash
# Search YouTube for niche-relevant videos from the last N days
curl -s "https://www.googleapis.com/youtube/v3/search?part=snippet&q=NICHE_KEYWORDS&order=viewCount&publishedAfter=DATE_ISO&maxResults=25&type=video&key=$YOUTUBE_DATA_API_KEY"
```

For discovered channels not in the competitor list, compute outlier score by
pulling their channel average on-the-fly.

### Step 2: X (Twitter) Trend Scan

Use WebSearch (Exa preferred) to find trending AI content on X:

```
Search: "site:x.com AI [niche keywords] filter:links" last 48 hours
```

Also search for viral threads:
```
Search: "site:x.com [niche keywords] thread" sort by engagement
```

For each trending post/thread, extract:
- **Author**: handle, follower count
- **Content**: full text or thread summary
- **Engagement**: likes, retweets, replies, bookmarks
- **Links**: any referenced tools, articles, demos
- **Topic**: what the post is about
- **Virality signal**: engagement relative to author's typical posts

### Step 3: Cross-Platform Topic Clustering

Group outlier content by **topic** across platforms:
- Cluster videos and posts talking about the same thing
- Identify topics trending on BOTH YouTube and X (strongest signal)
- Rank topics by combined outlier strength

### Step 4: Extract Hooks & Formulas

For the top 5 outlier videos, extract:

- **Title**: exact title text
- **Thumbnail**: screenshot URL / description
- **Hook** (first 30 seconds): use WebFetch on the video page, or if transcript
  is available, grab the first ~100 words
- **Hook formula**: classify the pattern
  - Problem → Promise
  - Shocking stat → Context
  - Contrarian take → Proof
  - Story open → Curiosity gap
  - Demo tease → "Here's how"
- **Why it worked**: 1-2 sentences on the outlier's success factor

### Step 5: Output

Produce `outliers.json`:
```json
{
  "date": "YYYY-MM-DD",
  "youtube_outliers": [
    {
      "rank": 1,
      "title": "Video Title",
      "channel": "Channel Name",
      "channel_subs": 12000,
      "views": 45000,
      "channel_avg_views": 3000,
      "outlier_score": 1500,
      "engagement_rate": 8.2,
      "url": "https://youtube.com/watch?v=xxx",
      "thumbnail_url": "https://...",
      "hook_text": "First 30 seconds transcript...",
      "hook_formula": "Problem → Promise",
      "topic": "AI automation for small business",
      "why_it_worked": "Tapped into solopreneur pain point with specific dollar savings"
    }
  ],
  "x_outliers": [
    {
      "rank": 1,
      "author": "@handle",
      "followers": 5000,
      "text": "Post content...",
      "likes": 2300,
      "retweets": 450,
      "topic": "AI automation",
      "url": "https://x.com/..."
    }
  ],
  "trending_topics": [
    {
      "topic": "AI automation for small business",
      "platforms": ["youtube", "x"],
      "combined_signal_strength": "very strong",
      "content_angle_suggestion": "How I built a $0/month AI employee that does X"
    }
  ],
  "top_recommendation": {
    "topic": "...",
    "why": "...",
    "reference_videos": ["url1", "url2"],
    "suggested_angle": "..."
  }
}
```

Also update the Google Sheet (via Daily Reporter) with outlier data:
- **Tab: Daily Outliers** — one row per outlier video/post
- **Tab: Trending Topics** — clustered topics with signal strength

## API Quota Management

YouTube Data API v3 has a daily quota of 10,000 units:
- `search.list` = 100 units per call
- `videos.list` = 1 unit per call
- `channels.list` = 1 unit per call

Budget per daily run:
- 10 competitor channels × search = 1,000 units
- 3 keyword searches = 300 units
- ~100 video stats lookups = 100 units
- ~10 channel stats = 10 units
- **Total: ~1,410 units/day** (well within quota)

If quota is exceeded, fall back to WebFetch scraping of channel pages.
