# Skillpipe Handoff Contract

## Invariants

1. Treat Printing Press, You.com, Exa, and Firecrawl as data taps.
2. Treat the evidence ledger as the source of truth for claims.
3. Define every ranked or charted metric before scoring.
4. Preserve source type, freshness, evidence strength, and confidence separately.
5. Generate the story from validated analytical artifacts, not raw crawl output.
6. Generate the PPTX and HTML from the same locked story spine.
7. Require a validated visual specification before rendering PowerPoint.
8. Promote a deck to `reviewed` only after editable-text, real-render, and OfficeCLI QA.
9. Generate the final response from the delivery manifest, status, and sync check.

## Stage Handoffs

| From | To | Required handoff |
|---|---|---|
| Data taps | AI Analyst | Raw captures, source URLs, retrieval dates, source ownership, and search log |
| AI Analyst | Story | Evidence ledger, metric definitions, data-quality report, scoring model, brief, and allowed numbers |
| Story | Visual/build | BLUF, assertion-title spine, evidence map, promoted datapoints, content cuts, and traceability |
| Visual/build | QA | Draft PPTX, builder source, visual spec, standalone HTML, visible text, and asset attribution |
| QA | Delivery | Reviewed editable PPTX, browser-tested HTML, manifest, sync check, and explicit artifact status |

## Gate Waivers

Record a waiver in `status.json`, `outputs/sync-check.md`, and the delivery manifest. A
waived mandatory gate keeps the artifact `draft` unless the governing skill explicitly
permits reviewed status. Never waive source traceability, editable-text verification, or
unsupported-number cleanup for a client-facing reviewed deck.

## Existing-Run Upgrade

When upgrading an existing run:

1. Preserve source captures, approved assets, builders, decks, and QA evidence.
2. Create `status.json` before further work.
3. Backfill the evidence ledger from existing claim/source contracts where possible.
4. Mark inferred classifications and synthesis as such.
5. Reuse valid QA evidence only when it applies to the exact final artifact checksum.
6. Rebuild missing HTML, manifest, sync, and evidence-control artifacts in place.
7. Do not call a previously reviewed filename reviewed under the new contract until the
   full skillpipe validates.
