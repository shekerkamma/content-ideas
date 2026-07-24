# Hyundai AI Plant Operations OKF Bundle - Claude Code Instructions

This is a staged OKF bundle generated from Sheker's Hyundai Obsidian vault. It
uses the same host-neutral workflow as Codex: markdown, YAML frontmatter,
folder-level `index.md`, `log.md`, and the stdlib-only `okf-cli.py`.

## Use The Bundle Directly

Navigate progressively:

```bash
python3 okf-cli.py index
python3 okf-cli.py find "<topic>"
python3 okf-cli.py read <path>
```

Read only relevant pages. Cite `source_path` from frontmatter when answering.

## Scope

- `use-cases/` - Hyundai plant-operations use cases.
- `architecture/` - supporting architecture/integration pages.
- `technologies/` - technology and repository reference notes.

## Compatibility

Keep behavior aligned with `AGENTS.md`: same CLI commands, same progressive
disclosure rule, same read-only default, and same `source_path` citation rule.

