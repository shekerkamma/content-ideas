# Hyundai AI Plant Operations OKF Bundle

This bundle was generated from `C:\Users\sheke\Documents\hyundai-ai-vault` as a
safe staged copy. The Obsidian vault was not modified.

## What's Inside

- `index.md` - root table of contents.
- `use-cases/` - 8 Hyundai AI plant-operations use cases.
- `architecture/` - supporting architecture and integration notes.
- `technologies/` - technology/repository references linked from the use cases.
- `source-vault/` - local copies of the original source notes for plugin-free editor links.
- `okf-cli.py` - dependency-free navigation and keyword search.
- `validate_okf_bundle.py` - OKF/profile validator.
- `AGENTS.md` and `CLAUDE.md` - host instructions for Codex and Claude Code.

## How To Use

```bash
python3 okf-cli.py index
python3 okf-cli.py find "visual inspection"
python3 okf-cli.py read use-cases/uc-01-visual-inspection
```

When answering, cite the original vault note using the `source_path` field in
frontmatter.

Each generated page also includes:

- an `Original source (local copy)` relative link inside this bundle
- an `Original source (WSL)` link under `/mnt/c/Users/sheke/Documents/hyundai-ai-vault`
- an `Original source (Windows)` `file:///C:/...` link
- the equivalent Windows path for VS Code/Obsidian lookup

If VS Code shows the WSL or Windows source link as broken, use the local-copy
link. It is a normal relative markdown link and does not require Obsidian or VS
Code plugins.
