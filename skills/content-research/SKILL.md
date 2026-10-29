---
name: content-research
description: "Chain: ingest any content (YouTube, LinkedIn, GitHub, web) → analyze → Obsidian second brain → knowledge graph. Paste one or more URLs of any type."
argument-hint: "<url> [url-2] [url-3] — YouTube, LinkedIn, GitHub, or any web URL"
allowed-tools: Bash, Read, Write, Edit, Skill, Agent, AskUserQuestion, WebFetch, WebSearch
user-invocable: true
---

# /content-research — Ingest → Analyze → Obsidian Second Brain → Knowledge Graph

This skill chains five steps into one command for **any content source**: YouTube videos, LinkedIn posts/profiles/articles, GitHub repos/READMEs, or any web page. It detects the source type, ingests it with the right tool, analyzes it, saves a structured second-brain note, syncs to the Obsidian vault with wikilinks and backlinks, and feeds it into the knowledge graph via `/graphify`.

## Step 1 — Parse input & detect source types

Extract all URLs from the user's input. Classify each by pattern:

| Pattern | Source Type | Ingest Method |
|---------|------------|---------------|
| `youtube.com/watch`, `youtu.be/`, `vimeo.com`, `tiktok.com`, `x.com/*/video`, `instagram.com/reel` | **video** | `/watch` skill |
| `linkedin.com/posts/`, `linkedin.com/pulse/`, `linkedin.com/in/*/recent-activity` | **linkedin-post** | WebFetch (scrape) |
| `linkedin.com/in/` (profile only) | **linkedin-profile** | WebFetch (scrape) |
| `linkedin.com/company/` | **linkedin-company** | WebFetch (scrape) |
| `github.com/<owner>/<repo>` (no deeper path) | **github-repo** | Bash: `gh api`, clone + read README/docs |
| `github.com/<owner>/<repo>/blob/`, `/tree/` | **github-file** | WebFetch or `gh api` for raw content |
| `github.com/<owner>` (profile only) | **github-profile** | `gh api users/<owner>`, repos list |
| Everything else | **web-page** | WebFetch |

Process each URL sequentially through the full pipeline.

## Step 2 — For each URL, run the chain:

### 2a — Ingest the content

#### Video sources → `/watch`

Invoke the `/watch` skill:
```
/watch <url> analyze the content structure
```
Read ALL frame paths returned. Pay special attention to:
- First 5 frames (the hook / opening)
- Frames showing text, graphics, b-roll transitions, pattern interrupts
- Thumbnail/title card if visible

#### LinkedIn posts/articles → WebFetch

```
WebFetch <linkedin-url>
```

Extract:
- **Author**: name, headline, follower count if visible
- **Post text**: full content including hashtags
- **Engagement**: likes, comments, reposts if visible
- **Media**: images, carousels, embedded videos (if video, chain to `/watch`)
- **Date posted**
- **Post type**: text-only / image / carousel / video / article / poll / document

#### LinkedIn profiles → WebFetch

```
WebFetch <linkedin-profile-url>
```

Extract:
- **Name, headline, location**
- **About section**
- **Experience** (current + recent roles)
- **Featured content** (posts, articles, links)
- **Skills / endorsements** (top ones)
- **Activity pattern** (posting frequency if visible)

#### GitHub repos → `gh api` + clone

```bash
gh api repos/<owner>/<repo> --jq '{name, description, stars: .stargazers_count, forks: .forks_count, language, topics, license: .license.spdx_id, created: .created_at, updated: .pushed_at}'
```

Then read key files:
```bash
# README
gh api repos/<owner>/<repo>/readme --jq '.content' | base64 -d

# Directory structure (top-level)
gh api repos/<owner>/<repo>/contents --jq '.[].name'

# Recent commits
gh api repos/<owner>/<repo>/commits --jq '.[0:10] | .[] | {date: .commit.author.date, msg: .commit.message}'
```

Extract:
- **What it does**: from README + description
- **Tech stack**: language, dependencies, framework
- **Traction**: stars, forks, contributors, recent activity
- **Architecture**: directory structure, key patterns
- **Documentation quality**: README depth, examples, guides
- **Community**: issues, PRs, discussions activity

#### GitHub profiles → `gh api`

```bash
gh api users/<owner> --jq '{name, bio, company, location, followers, public_repos, blog}'
gh api users/<owner>/repos --jq 'sort_by(-.stargazers_count) | .[0:10] | .[] | {name, description, stars: .stargazers_count, language}'
```

#### Web pages → WebFetch

```
WebFetch <url>
```

Extract the main content, stripping navigation/ads/boilerplate.

### 2b — Content Analysis (adapted by source type)

#### For Videos — full hook/visual/script analysis:

**Hook Analysis (first 3-10 seconds)**
- Visual hook, verbal hook, pattern interrupt, promise, curiosity gap

**Content Structure**
- Format, pacing, sections with timestamps, retention hooks

**Visual Strategy**
- B-roll, face:screen ratio, text overlays, thumbnail style

**Script Techniques**
- Tone, script density, CTA placement, credibility moves

#### For LinkedIn Posts — engagement/authority analysis:

**Hook Analysis (first 2 lines — before "see more")**
- Opening pattern: question / stat / bold claim / story / contrarian take
- Does it stop the scroll? Why?

**Content Structure**
- Format: story / listicle / hot take / framework / case study / thread
- Line breaks / white space strategy
- Length (short punch vs. long narrative)

**Engagement Drivers**
- CTA type: ask a question / share your take / tag someone / DM me
- Hashtag strategy: count, relevance, branded vs. generic
- Comment bait: what triggers replies?

**Authority Signals**
- Credibility: personal experience, data, name drops, results
- Positioning: thought leader / practitioner / educator / provocateur

#### For GitHub Repos — technical/adoption analysis:

**Problem & Solution**
- What problem does it solve?
- How is it different from alternatives?

**Technical Assessment**
- Architecture quality (from structure + README)
- Documentation completeness
- Test coverage indicators
- CI/CD setup

**Adoption Signals**
- Star velocity (stars vs. age)
- Fork-to-star ratio
- Issue response time (if visible)
- Contributor diversity

**Integration Potential**
- How could this be used in our work?
- Dependencies / compatibility
- License implications

#### For Web Pages — general content analysis:

**Content Assessment**
- Topic, depth, perspective
- Key claims and evidence
- Unique insights vs. rehashed ideas

**Credibility**
- Author authority, sources cited, data quality

### 2c — Save Second-Brain Note

Write a structured markdown note to the appropriate subdirectory:

```
~/projects/hyundai-peopletech-deck/second-brain/youtube/<slug>.md    # videos
~/projects/hyundai-peopletech-deck/second-brain/linkedin/<slug>.md   # LinkedIn
~/projects/hyundai-peopletech-deck/second-brain/github/<slug>.md     # GitHub
~/projects/hyundai-peopletech-deck/second-brain/web/<slug>.md        # web pages
```

Use the appropriate template per source type:

#### Video note template:
```markdown
---
title: "<Video Title>"
source: <URL>
source_type: video
creator: <Channel Name>
duration: "<MM:SS>"
date_watched: <YYYY-MM-DD>
tags: [content-research, video, <topic-tags>]
---

# <Video Title>

## TL;DR
<2-3 sentences>

## Hook Breakdown (0:00 - 0:XX)
- **Visual**: <what's on screen>
- **Opening line**: "<exact quote>"
- **Pattern interrupt**: <timestamp + what happens>
- **Promise**: <what viewer will get>
- **Hook rating**: Strong / Medium / Weak — <why>

## Content Structure
| Section | Timestamp | What Happens |
|---------|-----------|-------------|

## Visual Strategy
- **Face:Screen ratio**: XX:YY
- **B-roll style**: ...
- **Cuts per minute**: ~X

## Key Takeaways
1. ...

## Steal-Worthy Elements
- ...

## Quotable
- "<quote>" (t=MM:SS)
```

#### LinkedIn note template:
```markdown
---
title: "<Post opening or article title>"
source: <URL>
source_type: linkedin-post
author: <Name>
author_headline: "<Headline>"
date_watched: <YYYY-MM-DD>
engagement: {likes: X, comments: X, reposts: X}
tags: [content-research, linkedin, <topic-tags>]
---

# <Post Title / Opening>

## TL;DR
<2-3 sentences>

## Full Post Text
> <quoted post content>

## Hook Analysis (first 2 lines)
- **Opening pattern**: question / stat / bold claim / story
- **Scroll-stop rating**: Strong / Medium / Weak — <why>

## Content Structure
- **Format**: story / listicle / framework / hot take
- **Length**: <word count estimate>
- **White space**: heavy / moderate / dense

## Engagement Analysis
- **CTA**: <what they asked>
- **Comment bait**: <what triggers replies>
- **Hashtags**: <list>

## Authority Signals
- **Credibility**: <how they establish it>
- **Positioning**: <thought leader / practitioner / etc.>

## Key Takeaways
1. ...

## Steal-Worthy Elements
- ...

## Quotable
- "<memorable line>"
```

#### GitHub note template:
```markdown
---
title: "<repo-name>"
source: <URL>
source_type: github-repo
owner: <owner>
stars: <count>
language: <primary>
license: <SPDX>
date_watched: <YYYY-MM-DD>
tags: [content-research, github, <language>, <topic-tags>]
---

# <owner>/<repo-name>

## TL;DR
<2-3 sentences: what it does, why it matters>

## What It Does
<from README>

## Tech Stack
- **Language**: ...
- **Framework**: ...
- **Dependencies**: key ones

## Traction
- **Stars**: X | **Forks**: X | **Age**: X months
- **Star velocity**: ~X stars/month
- **Recent activity**: last commit <date>

## Architecture
```
<directory structure>
```

## Key Design Decisions
- ...

## Integration Potential
- **Use case for us**: <how we could use this>
- **Effort to integrate**: Low / Medium / High
- **License**: <implications>

## Steal-Worthy Elements
- ...
```

#### Web page note template:
```markdown
---
title: "<Page Title>"
source: <URL>
source_type: web
author: <if known>
date_watched: <YYYY-MM-DD>
tags: [content-research, web, <topic-tags>]
---

# <Page Title>

## TL;DR
<2-3 sentences>

## Key Content
<structured summary>

## Key Takeaways
1. ...

## Steal-Worthy Elements
- ...

## Quotable
- "<memorable line>"
```

### 2d — Obsidian Second Brain (auto-feed)

After saving the note to the project's `second-brain/` directory, copy it into the Obsidian vault and enrich it with Obsidian-native features.

**Vault location:** `/mnt/c/Users/sheke/Documents/hyundai-ai-vault/content-research/`

**Directory mapping:**
```
/mnt/c/Users/sheke/Documents/hyundai-ai-vault/content-research/
├── youtube/        ← video notes
├── linkedin/       ← LinkedIn post/profile notes
├── github/         ← repo/profile assessments
├── web/            ← web page notes
├── _index/         ← MOC (Map of Content), daily logs
└── _templates/     ← note templates
```

**For each note, do three things:**

1. **Copy the note** from `second-brain/<type>/` to `/mnt/c/Users/sheke/Documents/hyundai-ai-vault/content-research/<type>/`

2. **Add Obsidian wikilinks** — convert plain-text references to `[[wikilinks]]`:
   - Creator/author names → `[[Creator - Brad]]`
   - Tools mentioned → `[[yt-dlp]]`, `[[ffmpeg]]`, `[[Claude Code]]`
   - Concepts/techniques → `[[Pattern Interrupt]]`, `[[Hook Analysis]]`
   - Related notes → `[[other-note-slug]]`
   - Add a `## Backlinks` section at the bottom listing what this note connects to

3. **Update the MOC** — append a row to the "Recent Ingestions" table in `/mnt/c/Users/sheke/Documents/hyundai-ai-vault/content-research/_index/Content Research MOC.md`:
   ```
   | <date> | <creator> | <title> | <type> | [[<slug>]] |
   ```
   Also increment the Stats counters at the bottom.

**Obsidian tags:** ensure the frontmatter `tags` array uses Obsidian-friendly format (no spaces, lowercase). Add `#source/<type>` tag (e.g., `#source/youtube`, `#source/linkedin`).

### 2e — Knowledge Graph (graphify)

After syncing to Obsidian, invoke `/graphify` to extract entities, relationships, and concepts into the knowledge graph:

```
/graphify <path-to-obsidian-note>
```

This maps the content into a queryable knowledge graph, connecting:
- **Creators / Authors** → their techniques, tools, topics, platforms
- **Techniques** → which content uses them (hooks, frameworks, architectures)
- **Tools / Repos** → mentioned or analyzed across sources
- **Concepts** → cross-source relationships
- **Companies** → people, products, strategies

Over time, the graph reveals patterns across all ingested content — which techniques cluster, which authors share approaches, how tools connect across ecosystems.

## Step 3 — Summary

After processing all URLs, print a summary table:

| Source | Type | Title | Key Finding | Notes Saved |
|--------|------|-------|-------------|-------------|
| URL | video/linkedin/github/web | Title | One-liner | path |

## Multi-source mode

When multiple URLs of mixed types are provided, process them sequentially. After all are done, print a **cross-source comparison** if applicable:
- Common themes across sources
- How different platforms present similar ideas
- Unique insights from each source type
- Connection opportunities (e.g., a GitHub repo mentioned in a LinkedIn post that was demoed in a YouTube video)

## Tips
- For long videos (>10 min), focus `/watch` on the first 60 seconds for hook analysis, then sparse full scan
- Use `--resolution 1024` for videos with slides/code on screen
- LinkedIn posts behind auth walls may return limited content — try archive.is as fallback
- GitHub private repos require `gh auth` — the skill will warn if access is denied
- Mix source types freely: `/content-research <youtube-url> <linkedin-url> <github-url>`
