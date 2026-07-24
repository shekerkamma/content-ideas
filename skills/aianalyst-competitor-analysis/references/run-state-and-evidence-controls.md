# Run State And Evidence Controls

Use this reference at the start of every AI Analyst competitor-analysis run and again before final delivery.

## Required Control Artifacts

Every run folder must maintain these files:

```text
status.json
outputs/allowed-numbers.yaml
outputs/sync-check.md
outputs/run-learnings.md
client-package/delivery-manifest.json
```

These files prevent restart confusion, unsupported visible numbers, artifact drift, and memory-only final responses.

## status.json Contract

Create or update `status.json` after every major stage. On `continue`, read it before doing any work.

Required shape:

```json
{
  "run_id": "<YYYY-MM-DD-target-aianalyst-competitor-analysis>",
  "target": "<target>",
  "artifact_status": "draft|reviewed|blocked",
  "current_stage": "frame|research|ledger|metrics|quality|scoring|brief|story|artifacts|qa|publish|complete",
  "completed_gates": [
    "prompt_fit",
    "operating_prompt",
    "gbrain_recall",
    "evidence_ledger",
    "metric_definitions",
    "data_quality",
    "scoring_model",
    "story_architect",
    "allowed_numbers",
    "artifact_traceability",
    "editable_pptx_qa",
    "html_qa",
    "publish"
  ],
  "blocked_gates": [
    {
      "gate": "<gate>",
      "reason": "<why blocked>",
      "next_action": "<specific next command or decision>"
    }
  ],
  "artifact_paths": {
    "operating_prompt": "inputs/operating-prompt.yaml",
    "evidence_ledger": "outputs/evidence-ledger.csv",
    "allowed_numbers": "outputs/allowed-numbers.yaml",
    "story_pack": "outputs/story-architect-pack.md",
    "deck_source": "client-package/genspark-deck/deck.html",
    "reviewed_pptx": "client-package/genspark-deck/build/<name>-reviewed.pptx",
    "html_local": "client-package/site/index.html",
    "html_publish_source": "client-package/pages/<slug>/index.html",
    "manifest": "client-package/delivery-manifest.json"
  },
  "next_command": "<one concrete next command or task>",
  "updated_at": "<ISO-8601>"
}
```

Rules:

- Do not restart a run when `status.json` exists unless the user explicitly asks for a new run.
- Do not mark `complete` until the delivery manifest exists and required artifacts are reviewed or explicitly waived.
- Keep `next_command` concrete enough that another session can resume without guessing.

## allowed-numbers.yaml Contract

Create `outputs/allowed-numbers.yaml` before any deck, HTML, chart, or generated-slide build that will show quantitative claims.

Required shape:

```yaml
allowed_numbers:
  - id: NUM-001
    visible_value: "60%+"
    normalized_value: "60 percent plus"
    meaning: "Implementation effort and timeline reduction claim"
    target_or_competitor: "<company>"
    source_artifact: "outputs/evidence-ledger.csv"
    claim_ids:
      - "EV-0001"
    source_url: "<url>"
    source_type: "official|vendor_published|third_party|analyst|internal"
    confidence: "high|medium|low"
    required_label: "vendor-published"
    allowed_locations:
      - "deck: slide 16"
      - "html: #datapoints"
    status: "allowed"

blocked_patterns:
  - pattern: "\\$[0-9]"
    reason: "No unsupported currency values in visible artifacts"
  - pattern: "\\bARR\\b|\\bTAM\\b|\\bSAM\\b|\\bSOM\\b|\\bCAGR\\b"
    reason: "No unsupported market/financial precision"

structural_numbers:
  - "slide numbers"
  - "dates"
  - "30/60/90 roadmap labels"
```

Rules:

- Supported numbers must be plugged in with their required labels.
- Unsupported numbers must be removed or converted to qualitative evidence-family language.
- Do not rely on prompt instructions alone. Scan actual visible output.
- If a generated tool invents a number, add it to `blocked_patterns` or cleanup notes before final QA.

## sync-check.md Contract

Create `outputs/sync-check.md` before final response.

Minimum checks:

| Check | Pass criteria |
|---|---|
| Deck vs allowed numbers | Every visible deck number appears in `allowed-numbers.yaml` or is structural |
| HTML vs allowed numbers | Every visible HTML number appears in `allowed-numbers.yaml` or is structural |
| Deck vs HTML story | Same BLUF, competitor arenas, proof gaps, and roadmap |
| Manifest vs files | Manifest paths exist and statuses match actual QA |
| Published URL | Public URL returns HTTP 200 when publishing was requested |
| Editable deck | Final PPTX has native editable text boxes or native shapes; image-only is not final |

Record:

- files checked
- scan commands or method
- pass/fail result
- unresolved drift
- waiver, if any

## Editable PPTX Verification

The final deck must have a machine-verifiable editability check.

For hybrid/native PPTX, count editable text shapes:

```bash
python3 - <<'PY'
from pptx import Presentation
p = "client-package/genspark-deck/build/<name>-reviewed.pptx"
prs = Presentation(p)
texts = sum(
    1
    for s in prs.slides
    for sh in s.shapes
    if getattr(sh, "has_text_frame", False) and sh.text_frame.text.strip()
)
print({"slides": len(prs.slides), "editable_text_shapes": texts})
PY
```

Write the result to `client-package/delivery-manifest.json`.

Fail conditions:

- `editable_text_shapes` is zero.
- final PPTX is image-only and editability was not explicitly waived.
- shape count is not recorded in the manifest.

## Manifest-First Final Response

Do not write the final response from memory.

Before final response:

1. Read `client-package/delivery-manifest.json`.
2. Read `status.json`.
3. Read `outputs/sync-check.md`.
4. Answer from those files.

If the manifest is missing or stale, update it before responding.

## User Corrections And Run Learnings

Create `outputs/run-learnings.md` whenever the user corrects the process, facts, or delivery expectation.

Record:

```markdown
# Run Learnings

## Corrections

- Date:
  User correction:
  What changed in this run:
  Reusable rule:
  Skill update needed: yes/no
  Skill files updated:
```

Rules:

- Treat repeated user corrections as QA failures, not as chat-only feedback.
- If the correction is reusable across runs, update the skill before final delivery or add a blocked note explaining why not.
- When a reusable global workflow is created, install it globally and add a slash command wrapper where supported.

## Publishing Rule

When publishing static HTML:

- Use `/publish-static-page` or the `github-pages-publisher` skill.
- Do not manually reason through `gh-pages` vs Actions Pages unless the publisher fails.
- Record published URL, commit, HTTP status, and publisher command in the manifest.

## Global Skill Install Rule

When a new reusable workflow is created during a run:

- keep the repo copy under `skills/<skill-name>/`
- install the global Codex copy under `~/.codex/skills/<skill-name>/`
- install the global Claude copy under `~/.claude/skills/<skill-name>/` when Claude is used
- add a slash command under `~/.claude/commands/<command>.md` when supported
- verify the installed skill/script help path
- commit the repo copy

Do not leave a reusable workflow as a one-off script only.
