# Source video

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=nI0Mhzcl2Fk |
| Title | I Built an AI Competitor Research System Without Scrapers |
| Uploader | Eric Tech |
| Uploaded | 2026-08-24 |
| Duration | 10:08 |
| Derived on | 2026-08-25 |
| Metadata source | `video.info.json` from the `watch` run |
| Capture | 1080p (format 137), 124 frames at scene threshold 0.08, max gap 14.9s |

## Why this file exists

This skill was derived from a demonstration, so its claims are only as current
as the video. When a step stops working, check the upload date first: UI from
2026-08-24 may simply have changed.

**The video is a sponsored vendor demo.** It carries a promo code and closes on
the vendor's own benchmark table. That does not make the workflow wrong, but it
does mean every efficiency claim in it is a marketing claim until measured, and
the derivation treats it that way.

## Demonstration span

01:33 – 07:28. Before that is the problem framing; after it is a vendor
benchmark and an outro. Two coherent jobs sit inside that span, so two skills
were derived rather than one:

| Span | Job | Skill |
|---|---|---|
| 01:33 – 02:56 | Ask a server what it exposes, before using it | `mcp-capability-probe` |
| 02:56 – 07:28 | Declarative collection into a local store | `dataset-collect` (this one) |

## Cited moments

| Timestamp | What it establishes | Evidence |
|---|---|---|
| 03:34 | Bulk records should be filtered away from the context window | narration |
| 05:56–06:06 | Narration describes a 3-step pipeline: search → enrich → database | narration **only** |
| 06:03 | `competitors.txt`: apify, bright-data, firecrawl, clay-hq, scrapegraphai | frame |
| 06:17 | The actual spec: **one** source, `from_file`, `input_key`, `parallel: 3`, `on_error: skip`, parquet storage partitioned by `source_id` + `collected_date` | frame |
| 06:10 | Dry run happens "before spending any credits" | narration |
| 06:31 | Run output: `Found 5 inputs from competitors.txt` / `Collected 5 records` / `Done. Collected 5 records across 1 sources.` | frame |
| 06:31 | Follow-on commands: `dataset status`, `dataset query --source`, `dataset query --sql`, `dataset load-db -c <connection>` | frame |
| 06:51 | Verification query is DuckDB over parquet: `FROM read_parquet('2026-06-18.parquet')` with `locations->>'$[0].country_code'` | frame |
| 06:52–07:08 | Scheduling is described | narration **only** — no frame shows a schedule |

## Where the screen and the narration disagree

The skill's Source/Tool Order ranks execution first, then on-screen text, then
narration. Three disagreements were resolved that way:

1. **Pipeline shape.** Narration: three steps ending in a database. Screen: one
   source writing parquet, with `load-db` offered afterwards as an optional
   separate command. The screen wins; the derived spec has explicit sources and
   no implicit enrichment step.
2. **"A database."** Narration says the data is stored "locally in a database".
   The screen shows parquet files queried with DuckDB — a file format plus an
   embedded query engine, not a database server. The derived skill uses JSONL
   for the same reason it does not use parquet: no dependency.
3. **Scheduling.** Asserted, never shown. Recorded as a gap rather than
   reconstructed from guesswork.

## Claims that were not verifiable from the video

- **Server-side filtering.** "AnySite stores the results on its side and
  performs the filtering there first" (03:34). The frames show a filtered
  result, which is equally consistent with filtering after the fact. Recorded
  as a vendor claim. The derived skill's benefit does not rest on it.
- **Self-healing extraction and the benchmark table** (07:28–08:54). The
  vendor's own published comparison against Apify and Bright Data, presented by
  a sponsored channel. Not evidence, and nothing in this skill depends on it.
