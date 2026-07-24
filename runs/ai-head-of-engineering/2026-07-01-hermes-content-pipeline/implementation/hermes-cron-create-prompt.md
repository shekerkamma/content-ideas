# Hermes Cron Creation Prompt

Use this inside Hermes after the You.com plugin and model provider are configured.

```text
Create a cron job named hermes-content-pipeline-daily.

Schedule: daily at 06:30 local time.
Workdir: /home/shekerk/content-ideas.
Delivery: local.

Task:
Run the Hermes content pipeline v1 in draft-only mode.

Execution command:
python3 /home/shekerk/content-ideas/runs/ai-head-of-engineering/2026-07-01-hermes-content-pipeline/implementation/runner.py --live --output-root /home/shekerk/content-ideas/runs/hermes-content-pipeline

Use these files:
- /home/shekerk/content-ideas/runs/ai-head-of-engineering/2026-07-01-hermes-content-pipeline/implementation/sources.yaml
- /home/shekerk/content-ideas/runs/ai-head-of-engineering/2026-07-01-hermes-content-pipeline/implementation/pipeline-config.yaml
- /home/shekerk/content-ideas/runs/ai-head-of-engineering/2026-07-01-hermes-content-pipeline/implementation/hermes-cron-workflow.md
- /home/shekerk/content-ideas/runs/ai-head-of-engineering/2026-07-01-hermes-content-pipeline/implementation/schemas/

Workflow:
1. Confirm mode is draft_only and publish_allowed is false.
2. Acquire a lock for the content pipeline run.
3. Scan configured source clusters using You.com as preferred search.
4. Normalize source items into the source queue.
5. Cluster and rank topic opportunities.
6. Generate up to 3 sourced research briefs.
7. Generate at most 1 draft package with LinkedIn, X, and newsletter variants.
8. Write memory write-back candidates with provenance.
9. Write run log, cost summary, warnings, and errors.
10. Release the lock.

Hard rules:
- Do not publish content.
- Do not send outbound messages.
- Do not use publishing credentials.
- Do not write API keys or secrets into artifacts.
- Stop if any config allows publishing.
- Stop if the daily cost cap is exceeded.
```
