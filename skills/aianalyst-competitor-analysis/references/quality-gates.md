# AI Analyst Competitor Analysis Quality Gates

Use these gates before building, reviewing, or publishing client-facing PPTX/HTML artifacts. If a gate fails, keep status `draft` or `blocked`; do not call the artifact `reviewed`.

## Gate 1: Required Analytical Outputs

Block PPTX/HTML build until these exist:

- `outputs/evidence-ledger.csv`
- `outputs/evidence-ledger.md` or equivalent evidence summary
- `outputs/metric-definitions.md`
- `outputs/data-quality-report.md`
- `outputs/scoring-model.md`
- `outputs/competitor-brief.md`
- `outputs/story-architect-pack.md`

`outputs/storyboard-qa.md` and `outputs/artifact-traceability.md` may be created during the readiness gate, but must exist before final QA.

## Gate 2: Artifact Traceability

Create `outputs/artifact-traceability.md` before rendering final artifacts.

For every PPTX slide and HTML section, list:

| Artifact location | Assertion | Evidence basis | Confidence | Notes |
|---|---|---|---|---|
| Slide 7 / HTML `#heatmap` | Example assertion | `EV-0012`, `EV-0045`, Metric: Threat Score | medium | Vendor-published proof only |

Allowed evidence basis:

- one or more `claim_id`s from `evidence-ledger.csv`
- a metric defined in `metric-definitions.md`
- a score defined in `scoring-model.md`
- `synthesis` with supporting claim IDs
- `interpretation` with confidence and caveat

Fail conditions:

- slide/section has no evidence basis
- chart has no defined metric
- score has no scoring-model definition
- recommendation uses unsupported superlatives such as `best`, `strongest`, or `clear leader`
- evidence basis exists only in speaker notes when it drives a visible client-facing claim

## Gate 3: Datapoint Coverage Threshold

Add a datapoint coverage table to `data-quality-report.md` or `artifact-traceability.md`:

| Coverage item | Required |
|---|---:|
| Total evidence rows | yes |
| Numeric evidence rows | yes |
| Rows by competitor | yes |
| Rows by arena | yes |
| Rows by metric family | yes |
| Rows by confidence | yes |
| Rows by source type | yes |
| High-confidence rows | yes |
| Vendor-published rows | yes |
| Story-promoted datapoints | yes |
| Missing datapoints | yes |

Recommended minimums are context-dependent, but any competitor with fewer than three useful evidence rows or no high/medium-confidence rows must be marked low-confidence in heatmaps and battlecards.

## Gate 4: Search-Again Triggers

Run another targeted search pass before artifact build when any trigger is true:

- target proof is weak or only self-published
- no pricing or packaging datapoints for key competitors
- no implementation-time or time-to-value datapoints when implementation speed is part of the story
- no trust/compliance datapoints for enterprise positioning
- no support/productivity datapoints when productivity is a key claim
- no consulting/SI evidence when Accenture, BCG, Deloitte, IBM, McKinsey, or SIs shape buyer expectations
- competitor score relies mostly on low-confidence rows
- one competitor has much deeper evidence coverage than the others and the heatmap does not label confidence
- grill-me or story-architect identifies a strategic claim without evidence

If a search-again trigger cannot be resolved, document the missing datapoint, source attempts, and confidence impact. Do not silently fill the gap with prose.

## Gate 5: Story-Architect Lock

Before rendering:

- `story-architect-pack.md` must include BLUF, audience decision, tension, argument arc, slide spine, evidence map, datapoint promotion map, content cuts, rebuild instructions, and storyboard QA.
- slide titles must be assertions, not topic labels
- every planned slide must map to evidence, metric, score, synthesis, or labeled interpretation
- the datapoint promotion map must match the deck/page outline

If `grill-me` changes the BLUF, argument arc, slide order, evidence map, or datapoint promotion, update `story-architect-pack.md` before editing the deck or HTML.

## Gate 6: Client-Ready Claim Standard

Client-facing recommendations must be:

- supported by visible evidence or confidence label
- phrased to match evidence strength
- explicit about vendor-published vs independently verified proof
- clear about where the target wins, where incumbents can compress, and what proof would change confidence

Replace unsupported language:

| Avoid | Use |
|---|---|
| `clear leader` | `scores highest on available evidence, with medium confidence` |
| `proven ROI` | `vendor-published ROI proof` or `independently sourced ROI proof` |
| `enterprise-ready` | `shows enterprise-readiness signals: SOC 2, SSO, audit logs` |
| `faster than competitors` | `reported X% faster in vendor case study; competitor benchmarks unavailable` |

## Gate 7: Artifact QA

PPTX:

- branded template/workflow used
- slide count meets user requirement
- `client-package/*-draft.pptx` exists before QA
- `client-package/*-reviewed.pptx` exists only after QA passes
- render/contact-sheet review completed
- no visible text overflow or collisions
- OfficeCLI QA is mandatory for `reviewed` PPTX status unless the tool is unavailable and the user explicitly accepts `draft`/unreviewed delivery
- OfficeCLI output is saved under `client-package/qa/officecli/`
- status is `reviewed` only after render QA and OfficeCLI QA pass

Required OfficeCLI command pattern:

```bash
python3 scripts/officecli_qa.py \
  runs/<run>/client-package/<name>-draft.pptx \
  --out runs/<run>/client-package/qa/officecli \
  --required
```

Copy or write `*-reviewed.pptx` only after this command passes. If OfficeCLI fails due to content issues, fix the deck and rerun. If OfficeCLI fails due to missing local dependencies, mark the PPTX `blocked` or `draft` and report the exact failure; do not silently call it reviewed.

HTML:

- self-contained unless user requested a framework
- `client-package/site/index.html` exists
- tabs and sections match one-to-one
- datapoints/evidence tab or section exists when evidence is central
- Playwright or browser validation activates every tab
- if the user asked for a shareable/team URL, publish to GitHub Pages or the configured host
- `client-package/pages/<slug>/index.html` or equivalent publish source exists when GitHub Pages is used
- published URL verified with cache-busting query string when GitHub Pages is used

## Gate 8: Delivery Manifest

Write `client-package/delivery-manifest.json` before final response.

Required fields:

```json
{
  "artifact_status": "reviewed",
  "run_folder": "runs/<run>",
  "pptx": {
    "draft_path": "client-package/<name>-draft.pptx",
    "reviewed_path": "client-package/<name>-reviewed.pptx",
    "slide_count": 25,
    "qa_status": "passed",
    "officecli": {
      "status": "passed",
      "result_path": "client-package/qa/officecli",
      "required": true
    }
  },
  "html": {
    "local_path": "client-package/site/index.html",
    "publish_source_path": "client-package/pages/<slug>/index.html",
    "public_url": "https://<owner>.github.io/<repo>/<slug>/?v=<sha>",
    "qa_status": "passed"
  },
  "evidence": {
    "ledger_path": "outputs/evidence-ledger.csv",
    "row_count": 0,
    "story_promoted_count": 0
  },
  "published_commit": "<sha-or-null>",
  "updated_at": "<ISO-8601>"
}
```

Fail conditions:

- `reviewed_path` is missing when the user asked for PPTX
- OfficeCLI status is missing or not `passed` while PPTX artifact status is `reviewed`
- public URL is missing when the user asked for a shareable/team HTML URL
- public URL was not verified after publish
- manifest says `reviewed` while PPTX or HTML QA is missing

## Gate 9: Final Response Checklist

Final response must state:

- artifact status: `draft`, `reviewed`, or `blocked`
- run folder
- evidence ledger row count
- datapoint coverage summary
- PPTX path and slide count
- HTML local path and public URL when requested
- delivery manifest path
- QA checks run, including OfficeCLI command/result path/status
- review gates used
- unresolved evidence gaps or waived gates
