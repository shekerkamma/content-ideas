# Cole Medin AI-Coding OKF Bundle - Claude Code Instructions

This directory is a read-only Open Knowledge Format bundle for Cole Medin's
AI-coding content. It uses the same portable workflow as Codex: markdown,
YAML frontmatter, `index.md`, `log.md`, and the stdlib-only `okf-cli.py`.

## Use The Bundle Directly

Do not build a RAG index or require external services for normal use. Navigate
progressively:

```bash
python3 okf-cli.py index
python3 okf-cli.py find "<topic>"
python3 okf-cli.py read concepts/<slug>
python3 okf-cli.py read videos/<slug>
```

## Response Workflow

1. Start from the root index or CLI index.
2. Use `find` for the user's topic.
3. Read the smallest relevant set of concept/video pages.
4. Follow relative markdown links only when the answer needs more context.
5. Cite source videos using `title` and `resource` from video frontmatter.

## Host Compatibility

Keep behavior aligned with `AGENTS.md`. If these files diverge, preserve the
shared contract: same CLI commands, same progressive disclosure, same read-only
default, and same source-citation rule.

## Validation

Run from this directory:

```bash
python3 validate_okf_bundle.py
python3 okf-cli.py index
python3 okf-cli.py find "PIV loop"
python3 okf-cli.py read concepts/the-piv-loop
```

