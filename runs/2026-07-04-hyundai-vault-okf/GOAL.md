# Goal: Hyundai Vault OKF Bundle

## Objective

Create a staged OKF bundle from `C:\Users\sheke\Documents\hyundai-ai-vault`
using the same pattern as the Cole Medin AI-Coding Knowledge Bundle, while
leaving the Obsidian vault untouched.

## Scope

First bundle: Hyundai AI Plant Operations.

- 8 use-case notes from the vault root.
- 5 architecture notes from `architecture/`.
- 16 technology/repository notes from `repos/` referenced by the use cases and
  `Home.md`.

## Acceptance Criteria

- Generated bundle lives under this run folder.
- Source vault is read-only.
- Bundle has root and folder indexes.
- Bundle has `AGENTS.md` for Codex/generic agents.
- Bundle has `CLAUDE.md` for Claude Code.
- Bundle has `okf-cli.py` for index/search/read.
- Bundle has `validate_okf_bundle.py`.
- Obsidian wiki links are converted to relative markdown links when the target
  exists in the bundle.
- CLI and validation smoke tests pass.

## Verification Commands

Run from `bundle/`:

```bash
python3 validate_okf_bundle.py
python3 okf-cli.py index
python3 okf-cli.py find "visual inspection"
python3 okf-cli.py read use-cases/uc-01-visual-inspection
python3 okf-cli.py find "digital traceability"
python3 okf-cli.py find "edge deployment"
python3 okf-cli.py read architecture/edge-deployment
```

