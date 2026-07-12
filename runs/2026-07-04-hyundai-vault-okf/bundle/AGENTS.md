# Hyundai AI Plant Operations OKF Bundle - Codex/Generic Agent Instructions

This is a staged Open Knowledge Format bundle derived from Sheker's Obsidian
vault at `C:\Users\sheke\Documents\hyundai-ai-vault`.

The source vault was not modified. Treat this bundle as the read-only search and
answer surface unless the user explicitly asks to regenerate or edit it.

## Operating Contract

Use progressive disclosure:

```bash
python3 okf-cli.py index
python3 okf-cli.py find "<topic>"
python3 okf-cli.py read use-cases/<slug>
python3 okf-cli.py read architecture/<slug>
python3 okf-cli.py read technologies/<slug>
```

If the host exposes Python as `python`, that command can be substituted.

## Page Types

- `type: use_case` - Hyundai plant-operations AI use cases.
- `type: architecture` - architecture and integration notes.
- `type: technology` - technology/repository reference notes.

## Answering Questions

1. Start with `index.md` or `python3 okf-cli.py index`.
2. Search the user's topic with `python3 okf-cli.py find "<topic>"`.
3. Read the smallest relevant page set.
4. Follow relative markdown links when needed.
5. Ground answers in the pages and cite `source_path` from frontmatter.

Do not search the live vault or web unless the staged bundle is insufficient for
the question.

## Validation

Run from this directory:

```bash
python3 validate_okf_bundle.py
python3 okf-cli.py find "visual inspection"
python3 okf-cli.py read use-cases/uc-01-visual-inspection
```

