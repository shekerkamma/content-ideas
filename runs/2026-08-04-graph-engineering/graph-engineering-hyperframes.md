# Hyperframe classification — Why Graph Engineering will 10x your Claude/Codex

Source: local capture (`watch --detail token-burner --resolution 1280`, closest available
substitute for the missing `scene-complete` mode — see run report). 28 scene-change
candidates over the full 26:29 runtime, 0 dropped by the tool's own dedup (28 selected of
28 candidates). `max_gap_seconds` ≈ 435s (17:38 → 24:53), which falls in an
uninterrupted talking-explanation stretch (the presenter walking through the "on-ramp"
and "ready-made pipelines" slides verbally after the last new slide) — expected, not a
coverage gap.

| Frame | t | Classification | Disposition |
|---|---|---|---|
| 0001 | 00:00 | talking-head | excluded — presenter-only, no informative content |
| 0002 | 00:03 | duplicate/low-value | excluded — blank transition frame |
| 0003 | 00:06 | talking-head | excluded |
| 0004 | 00:19 | duplicate/low-value | excluded — gradient transition frame |
| 0005 | 00:41 | talking-head | excluded |
| 0006 | 00:59 | duplicate/low-value | excluded — gradient transition frame |
| 0007 | 01:05 | talking-head | excluded |
| 0008 | 01:19 | duplicate/low-value | excluded — decorative podcast-brand intro bumper, no informative content |
| 0009 | 01:20 | duplicate/low-value | excluded — same bumper, presenter framed inside it |
| 0010 | 01:29 | text-slide | **kept** — "Three Ways to Get Work Out of AI" |
| 0011 | 01:51 | text-slide | **kept** — "The Before / After" |
| 0012 | 02:33 | talking-head | excluded |
| 0013 | 02:50 | text-slide | **kept** — "One Chat vs One Graph" |
| 0014 | 03:42 | talking-head | excluded |
| 0015 | 03:53 | diagram | **kept** — "The Vocabulary: Jobs, Arrows, State" |
| 0016 | 06:39 | talking-head | excluded |
| 0017 | 06:50 | text-slide | **kept** — "Knowledge Graph vs Agent Graph" |
| 0018 | 08:43 | talking-head | excluded |
| 0019 | 08:57 | text-slide | **kept** — "The Qualifying Test" (6 conditions) |
| 0020 | 10:01 | talking-head | excluded |
| 0021 | 10:17 | diagram | **kept** — "The Worked Example: Shopify AI Bookkeeping" |
| 0022 | 13:23 | talking-head | excluded |
| 0023 | 13:37 | diagram | **kept** — "The Diamond Pattern" |
| 0024 | 15:10 | talking-head | excluded |
| 0025 | 15:16 | text-slide | **kept** — "The On-Ramp: Three Levels of Implementation" |
| 0026 | 17:14 | talking-head | excluded |
| 0027 | 17:38 | text-slide | **kept** — "Ready-Made Pipelines: Three Graphs You Can Steal" |
| 0028 | 24:53 | talking-head | excluded — closing remarks, no new slide |

**Kept: 10 distinct slides** (all screen-shared graphics from the presenter's own deck —
`exact-source-evidence`, routed to Route 0 extract, never redrawn as native shapes).
**Excluded: 18** (13 talking-head, 3 transition frames, 2 intro-bumper frames) — all
accounted for above with reason; none dropped silently.

No meaningful hyperframe was skipped.
