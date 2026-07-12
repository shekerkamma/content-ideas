# Hermes Content Pipeline Implementation Package

This package turns the approved use case into a first implementation contract.

The v1 pipeline is draft-only:

1. Scan configured sources.
2. Normalize source items into a queue.
3. Cluster and rank topic opportunities.
4. Generate source-grounded research briefs.
5. Generate draft article packages and promotional variants.
6. Queue outputs for human editorial review.
7. Write durable topic/source memory.
8. Log cost, model route, and run health.

No v1 step publishes content.

## Files

| File | Purpose |
|---|---|
| `sources.yaml` | Initial source cluster config and extraction policy |
| `pipeline-config.yaml` | Runtime settings, model routing, cost caps, and approval gates |
| `runner.py` | Local draft-only runner that writes queue artifacts and logs |
| `validate_artifacts.py` | Lightweight smoke validator for runtime artifacts |
| `package_business_outputs.py` | Converts generated markdown deliverables into HTML/CSV business artifacts |
| `run-folder-layout.md` | Canonical run/output directory structure |
| `hermes-cron-workflow.md` | First scheduled Hermes workflow |
| `hermes-cron-job.template.json` | Portable cron job shape aligned to observed Hermes job JSON |
| `hermes-cron-create-prompt.md` | Plain-English prompt to create the cron inside Hermes |
| `schemas/source-item.schema.json` | Normalized source queue item |
| `schemas/topic-cluster.schema.json` | Ranked topic cluster |
| `schemas/research-brief.schema.json` | Source-grounded research brief |
| `schemas/draft-package.schema.json` | Article draft plus promotional variants |
| `schemas/run-log.schema.json` | Cost and health logging |
| `schemas/review-decision.schema.json` | Editorial review status |

## Runtime Outputs

Each run writes:

- source queue artifacts
- topic cluster artifacts
- research brief artifacts
- draft package artifacts
- memory write-back candidates
- business deliverables under `deliverables/YYYY-MM-DD/`
- logs and cost summary

## Environment

Required outside repo files:

- `YOU_API_KEY`

Optional:

- `YOU_BASE_URL`
- `ANTHROPIC_API_KEY` or the configured Hermes model provider credentials
- GBrain connection details, if not already configured in the host

## Existing You.com Integration

This repo already includes:

- `hermes-plugins/web/you/provider.py`
- `hermes-plugins/web/you/plugin.yaml`
- `scripts/install_you_hermes_plugin.py`

Use the installer to configure Hermes search without storing the key in the repo.

## Local Smoke Run

Offline mode is the default:

```bash
python3 runs/ai-head-of-engineering/2026-07-01-hermes-content-pipeline/implementation/runner.py \
  --date 2026-07-01 \
  --output-root runs/hermes-content-pipeline-smoke

python3 runs/ai-head-of-engineering/2026-07-01-hermes-content-pipeline/implementation/validate_artifacts.py \
  runs/hermes-content-pipeline-smoke \
  --date 2026-07-01

python3 runs/ai-head-of-engineering/2026-07-01-hermes-content-pipeline/implementation/package_business_outputs.py \
  runs/hermes-content-pipeline-smoke/deliverables/2026-07-01 \
  --date 2026-07-01
```

Live You.com mode must be explicit:

```bash
python3 runs/ai-head-of-engineering/2026-07-01-hermes-content-pipeline/implementation/runner.py \
  --live \
  --output-root runs/hermes-content-pipeline
```

## Launch Boundary

The workflow may write draft artifacts, run logs, and memory entries.
It must not publish to a CMS, social channel, or email list in v1.
