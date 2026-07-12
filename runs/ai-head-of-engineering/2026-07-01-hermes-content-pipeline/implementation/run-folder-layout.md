# Run Folder Layout

Canonical runtime root:

```text
runs/hermes-content-pipeline/
  config/
    sources.yaml
    pipeline-config.yaml
  queue/
    source-items/
      YYYY-MM-DD/
        source-item-<source-id>-<hash>.json
    topic-clusters/
      YYYY-MM-DD/
        topic-cluster-<slug>.json
    research-briefs/
      YYYY-MM-DD/
        brief-<slug>.md
        brief-<slug>.json
    draft-packages/
      YYYY-MM-DD/
        draft-<slug>.md
        draft-<slug>.json
    review-decisions/
      YYYY-MM-DD/
        review-<draft-id>.json
  memory-writeback/
    YYYY-MM-DD/
      memory-candidates.json
      accepted-memory.md
  deliverables/
    YYYY-MM-DD/
      README.md
      business-outcome-memo.md
      source-register.md
      editorial-brief.md
      article-draft.md
      linkedin-post.md
      x-thread.md
      newsletter-blurb.md
      deliverables-metadata.json
  logs/
    YYYY-MM-DD/
      run-log.json
      errors.md
      cost-summary.md
  .locks/
    content-pipeline.lock
```

## Artifact Rules

- JSON files are machine-readable contracts.
- Markdown files are human review surfaces.
- Every source claim in a draft must map back to a research brief citation.
- Every research brief citation must include a source URL and fetched date.
- Review decisions are separate files so drafts are not mutated silently.
- Published status is not allowed in v1.

## Promotion Flow

```text
source item -> topic cluster -> research brief -> draft package -> review decision -> memory write-back
```

No artifact promotes itself. Each stage reads the prior stage and writes a new artifact.
