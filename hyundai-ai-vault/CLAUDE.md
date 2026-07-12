You are working in a Hyundai-focused personal second brain — a knowledge management system, not a code project. Your job is to keep the wiki current, useful, and well-organized based on the raw notes the user captures.

Read `README.md` first. This is the source of truth for the system.

## Scope

Focus on Hyundai-related AI topics:
- dealer operations
- customer support and CRM workflows
- manufacturing and supply chain AI
- enterprise agent systems
- implementation notes, vendor comparisons, and account intelligence

## Common Tasks

- Translate raw: run the prompt in `translate.md` against `/raw`.
- Project digest: summarize a `/projects/<name>/` folder into its README.
- Answer questions: read `/wiki` first, then `/projects`, then `/archive`.

## Hard Rules

1. Never delete anything from `/raw` or `/archive`. Move only, never delete.
2. Never overwrite a `/wiki` entry blindly. Always read it first, then merge.
3. Never modify `/archive` after a file lands there.
4. When uncertain, log the uncertainty in the entry instead of guessing.

## Wiki Voice and Structure

- Default tone: clear, factual, terse.
- Preserve the user's phrasing when it carries signal.
- Keep one topic per file with kebab-case filenames.
- Prefer updating an existing topic note over creating near-duplicates.
- Record source provenance when it matters.
