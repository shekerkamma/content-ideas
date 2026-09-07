---
name: affiliate-workflow
description: 'End-to-end AI affiliate marketing pipeline: niche research, Higgsfield UGC/cinematic video generation, Canva Pinterest carousel creation, and bonus content (hooks, captions, calendar). Trigger when user wants to create affiliate marketing content.'
metadata:
  legacy-frontmatter:
    trigger: /affiliate-workflow
---

# /affiliate-workflow

End-to-end AI-powered affiliate marketing workflow. Takes a niche (or discovers one), then generates video ads, Pinterest carousels, and supporting content using Higgsfield and Canva MCPs.

## Pipeline Overview

The workflow has 5 stages. Each stage produces a deliverable. Run them in order, but any stage can be re-run independently.

| Stage | What | Tool | Output |
|-------|------|------|--------|
| 1 | Niche Research | Exa web search | Ranked niche report + top 10 products |
| 2 | UGC Video | Higgsfield `generate_video` | Short-form UGC product video |
| 3 | Cinematic Ad | Higgsfield `generate_video` | Polished cinematic product ad |
| 4 | Pinterest Carousel | Canva `generate-design` | 4-slide Pinterest pin carousel |
| 5 | Bonus Content | Claude (no MCP) | Hooks, captions, calendar, DM sequence |

## What You Must Do When Invoked

### 0. Parse arguments

- `/affiliate-workflow` with no args — start from Stage 1 (niche research)
- `/affiliate-workflow <niche>` — skip Stage 1, use the given niche
- `/affiliate-workflow resume` — check for existing `affiliate-workflow/` dir in cwd, read README.md status table, resume from first incomplete stage
- `/affiliate-workflow <stage-number>` — jump to that stage (e.g. `/affiliate-workflow 3` runs cinematic ad only)

### 1. Niche Research

Use `mcp__claude_ai_Exa__web_search_exa` to research trending affiliate niches. Score each on 4 dimensions (Earning Potential, Viral Ease, Beginner Friendliness, Scalability) out of 10. Pick the winner.

Then research top 10 products in that niche with commission rates, viral potential, and beginner ease scores.

**Output:** Write `affiliate-workflow/01-niche-research-report.md` with:
- Top 5 categories ranked table
- Winner deep-dive: why it wins, top 10 products, beginner strategy, platform allocation, content cadence, commission structure

### 2. UGC Video Generation

Generate a UGC-style product video using Higgsfield.

**Steps:**
1. Pick the best product from Stage 1 for UGC content (high viral + ease scores)
2. Check Higgsfield balance: `mcp__higgsfield__balance`
3. If credits available, get cost estimate first: `mcp__higgsfield__generate_video` with `get_cost: true`
4. Confirm with user, then generate: `mcp__higgsfield__generate_video` with model `seedance_2_0`, aspect_ratio `9:16`, duration 5
5. Poll with `mcp__higgsfield__job_status` (wait `poll_after_seconds` between calls)
6. If no credits, write the prompt to file for manual use later

**Prompt formula for UGC videos:**
```
Realistic UGC-style video of [person description] in [setting]. They are [action with product]. [Lighting description]. [Camera angle]. Authentic, not overly produced. [Product] is the visual hero.
```

**Output:** Write `affiliate-workflow/02-higgsfield-ugc-video-prompt.md` with:
- Primary prompt + 2 alternative angle prompts
- Each prompt includes: product, niche, platform, video concept, visual style, mood, colors

### 3. Cinematic Ad Generation

Same flow as Stage 2 but with polished cinematic style.

**Prompt formula for cinematic ads:**
```
Cinematic product advertisement for [product]. [Dramatic opening]. [Product hero shot with dramatic lighting]. [Lifestyle context shot]. Professional color grading, shallow depth of field, smooth camera movement.
```

**Output:** Write `affiliate-workflow/03-higgsfield-cinematic-ad-prompt.md` with:
- Primary prompt + 2 alternative angle prompts
- Cinematic direction: camera moves, lighting, color grade, sound design notes

### 4. Pinterest Carousel

Generate a 4-slide Pinterest carousel using Canva.

**Slide structure (always follow this):**
1. **Hook** — attention-grabbing title slide ("Your [thing] could look like this")
2. **Problem** — pain points the audience relates to
3. **Routine/System** — numbered steps or tips (the value)
4. **Result + CTA** — transformation + "shop my setup" with product prices + #affiliate disclosure

**Steps:**
1. Generate each slide: `mcp__claude_ai_Canva__generate-design` with `design_type: "pinterest_pin"`
2. For each, provide a detailed query with: slide number, content, design direction (sage green + warm white palette, modern sans-serif, clean minimal layout)
3. Ask user to pick preferred candidate from each batch
4. Finalize with `mcp__claude_ai_Canva__create-design-from-candidate`
5. If quota limited, write prompts to file for later

**Output:** Write `affiliate-workflow/05-pinterest-carousel-slides.md` with:
- Status table (which slides generated, which pending)
- Ready-to-paste prompts for any slides not yet generated

### 5. Bonus Content

Generate supporting content using Claude directly (no MCP needed). Create 5 bonus sections:

1. **30 Viral Hooks** — scroll-stopping openers for TikTok/Reels/Pinterest
2. **Pinterest SEO Captions** — keyword-rich descriptions for each carousel slide
3. **30-Day Content Calendar** — daily posting plan across TikTok, Reels, Pinterest
4. **Follow-Up DM Sequence** — 3-message nurture sequence for engaged followers
5. **Multi-Platform Repurposing Guide** — how to adapt one piece across all platforms

**Output:** Write `affiliate-workflow/04-bonus-hooks-captions-calendar.md`

### 6. Finalize

After all stages complete:
1. Update `affiliate-workflow/README.md` with current status of all files
2. Offer to commit and push changes
3. Summarize what was created and what's still pending (quota limits, etc.)

## Important Rules

- **Always check balances/quotas before generating.** Don't waste the user's time on tools that will fail.
- **Always get cost estimates first** (`get_cost: true`) and confirm with user before spending credits.
- **Write prompts to files even if generation fails.** The user can run them later when quota resets.
- **Vertical format only.** All video and Pinterest content is 9:16 (vertical) for TikTok/Reels/Pinterest.
- **Include #affiliate disclosure** on any content with product links or prices.
- **Niche-agnostic.** The workflow works for any niche, not just home organization. Don't hardcode products.
