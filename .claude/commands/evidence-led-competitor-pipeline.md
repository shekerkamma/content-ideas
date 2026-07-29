Use the repo-local `evidence-led-competitor-pipeline` skill to run or resume an
evidence-led competitor-analysis skillpipe for `$ARGUMENTS`.

Keep ownership boundaries explicit:

- Printing Press/Firecrawl and You.com are data taps.
- AI Analyst owns the evidence ledger, metric definitions, data quality, scoring,
  confidence, traceability, and allowed numbers.
- The competitor-analysis pipeline owns the decision story, editable branded PPTX,
  self-contained HTML, publishing when requested, and QA.
- The compound skillpipe owns stage state, handoff validation, resumability, sync,
  and the delivery manifest.

Read an existing run's `status.json` before creating a new run. Do not promote an
artifact to `reviewed` until the complete skillpipe validation passes.
