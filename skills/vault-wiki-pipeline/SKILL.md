---
name: vault-wiki-pipeline
description: 'Use when maintaining Sheker''s Hyundai AI Vault as a connected Obsidian wiki: audit unresolved wikilinks, missing frontmatter, stale MOCs, empty boards, entity stubs, content-research routing, daily/dev-log propagation, and skill-piped vault cleanup.'
metadata:
  legacy-frontmatter: 'name: vault-wiki-pipeline

    description: Use when maintaining Sheker''s Hyundai AI Vault as a connected Obsidian wiki: audit unresolved wikilinks, missing frontmatter, stale MOCs, empty boards, entity stubs, content-research routing, daily/dev-log propagation, and skill-piped vault cleanup.'
---

# Vault Wiki Pipeline

Maintain this vault as an active wiki, not a folder dump.

## Pipe

1. Read `AGENTS.md` for vault rules.
2. Use `obsidian-markdown` rules for note shape: frontmatter, tags, concise content, `[[wikilinks]]`.
3. Run `scripts/audit_vault.py` to get current health.
4. Classify gaps using `references/routing.md`.
5. Create or update only the notes needed for the requested outcome.
6. Update MOCs, boards, daily note, and dev log when changes are made.
7. Re-run the audit and report before/after numbers.

## Default Actions

- Create missing entity notes when a high-frequency unresolved link blocks navigation.
- Add MOCs when a topic has enough notes to need a map.
- Update `Home.md` when a new hub should be first-level navigation.
- Update `Boards/Work.md` and `Tasks/` for durable follow-up work.
- Write audit outputs to `Reviews/` when doing a health pass.

## Guardrails

- Do not delete or archive notes without asking.
- Do not touch `Finances/` personal data without asking.
- Do not create huge generic encyclopedia pages. Prefer concise hub/stub pages.
- Do not duplicate a note if an alias or path already resolves the link.
- Keep content terse. Follow the banned-word list in `AGENTS.md`.

## Scripts

- `scripts/audit_vault.py`: scans markdown notes, aliases, wikilinks, frontmatter, folder counts, and board status. Use `--write-review` to create a review note. Use `--create-stubs --limit N --min-count M` only when the user wants active cleanup.

## References

- `references/routing.md`: where entities, MOCs, tasks, and research notes belong.
- `assets/entity-stub.md`: short default note pattern for script-created stubs.

