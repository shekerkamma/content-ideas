# GOAL — YouTube playlist dashboard (@albertolgaard)

Status: **done** · Turns used: 6 of 30 · Started/finished: 2026-07-12

## Verification evidence (final)

1. (executable) `data.json`: 2 groups, 98 videos, 98 with non-null views. PASS
2. (browser, headless Playwright) zero console errors; count 80=80; top
   767K=766,708; group switch 18=18; sort-asc first row 997=997; search
   "claude" 19=19 rows. PASS — full results in the run log, screenshot
   `dashboard-verify.png`.

## Contract

- **TASK:** Scrape every playlist of https://www.youtube.com/@albertolgaard/playlists
  with yt-dlp, collect the videos (title, views, playlist), and analyze which
  title/topic patterns correlate with stronger view performance.
- **WHY:** Show which concepts drive views for this creator — input for the
  user's own content-strategy pipeline (content-ideas feed).
- **OUTCOME:** A self-contained interactive dashboard at
  `runs/goal-youtube-dashboard/dashboard.html` (Aurora Glass tokens) backed by
  `data.json`: explorable by playlist, sortable by views, with a
  title-pattern/performance summary.
- **CONSTRAINTS:** Real data only, via installed yt-dlp (no new API keys, no
  paid calls). Single self-contained HTML file (inline data, no CDN). Follow
  DESIGN.md tokens and the dataviz skill. Stop after 30 turns.
- **VERIFICATION:**
  1. (executable) `data.json` parses, has ≥1 playlist and ≥10 videos with
     non-null view counts.
  2. (browser) Headless Playwright: dashboard loads with zero console errors,
     playlist filter and view-sort interactions change the rendered rows,
     and the rendered total video count + top-video views match `data.json`.

## Iteration log

- [turn 1] Channel has 1 playlist ("Beginners Guide to a 1-Person AI
  Business", 18 videos) — added the uploads tab (80 videos) as a second group
  for pattern signal. Flat extraction carried no view counts → per-video
  metadata fetch running in background (98 unique ids, xargs -P8).
- [turn 2] dataviz skill loaded; palette validated: brand teal #2dd4bf FAILS
  the dark-mode lightness band for marks → bars use #0d9488 (ALL CHECKS
  PASS); #2dd4bf stays on UI chrome/stat text only.
- [turn 2] Per user instruction: enrich with the watch skill — transcript-only
  pass on the top-3 videos by views, so the pattern panel reports what
  winners SAY, not just title tokens. Runs after view counts land.

- [reframe] v2 published: executive briefing (business problems, demand signals, playlist curriculum) replaced creator-analytics framing per user feedback; card + README updated; live confirmed HTTP 200.
