# Goal: Cross-Host Cole Medin OKF Bundle

## Objective

Create a repo-local, verified OKF bundle workspace for the Cole Medin
AI-Coding Knowledge Bundle that works in both Codex and Claude Code hosts.

## Acceptance Criteria

- Bundle content is copied into this run folder without the source `.git`
  directory.
- `AGENTS.md` documents the Codex/generic-agent workflow.
- `CLAUDE.md` documents the Claude Code workflow.
- The same `okf-cli.py` commands work in both hosts:
  - `python3 okf-cli.py index`
  - `python3 okf-cli.py find "<topic>"`
  - `python3 okf-cli.py read <path>`
- Hosts that expose Python as `python` instead of `python3` can substitute that
  command; this Linux validation environment only has `python3`.
- `validate_okf_bundle.py` verifies OKF conformance and the Cole-specific
  `video`/`concept` profile.
- Smoke tests prove index, search, read, and validation all pass.

## Verification Commands

Run from `bundle/`:

```bash
python3 validate_okf_bundle.py
python3 okf-cli.py index
python3 okf-cli.py find "PIV loop"
python3 okf-cli.py read concepts/the-piv-loop
python3 okf-cli.py read videos/principled-agentic-engineer
```
