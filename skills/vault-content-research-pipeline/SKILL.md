---
name: vault-content-research-pipeline
description: Use when ingesting, enriching, or organizing web clippings, YouTube transcripts, LinkedIn posts, GitHub repos, articles, or research notes in Sheker's vault; routes content into content-research, updates the Content Research MOC, creates wiki entities, and feeds content ideas or POC assets.
---

# Vault Content Research Pipeline

Turn raw clippings into reusable wiki intelligence.

## Pipe

1. Read `prompts/enrich-clippings.md` for source-type enrichment rules.
2. Use `obsidian-markdown` for note shape and wikilinks.
3. Use `vault-wiki-pipeline` after enrichment to resolve high-value entities.
4. Update `content-research/_index/Content Research MOC.md`.
5. If a note has strong application potential, hand it to `vault-content-ideas-pipeline`.
6. If a note has POC or client value, hand it to `vault-poc-factory-pipeline`.

## Required Output Sections

Each enriched research note needs:
- `## TL;DR`
- `## Key Takeaways` or source-specific equivalent
- `## Integration Potential`
- `## Steal-Worthy Elements`
- `## Backlinks`

## Grounding Rules

- Every person mentioned should link to `People/`.
- Every tool/platform should link to `technologies/`.
- Every reusable method should link to `Knowledge/`.
- Every business application should link to `Projects/` or a MOC.
- Do not leave a strong idea trapped inside `content-research/`; graduate it to `Ideas/`, `Content/`, or `Projects/`.

## References

- `references/research-to-wiki.md`: handoff rules.

