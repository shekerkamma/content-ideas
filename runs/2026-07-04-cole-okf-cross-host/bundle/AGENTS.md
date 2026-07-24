# Cole Medin AI-Coding OKF Bundle - Codex/Generic Agent Instructions

This directory is a read-only Open Knowledge Format bundle for Cole Medin's
AI-coding content. It is intentionally portable across Codex, Claude Code,
Cursor, Gemini CLI, and other agents that can read markdown and run Python.

## Operating Contract

Use the bundle directly. Do not require a database, embeddings, MCP, or web
search for normal questions.

Start with progressive disclosure:

```bash
python3 okf-cli.py index
python3 okf-cli.py find "<topic>"
python3 okf-cli.py read concepts/<slug>
python3 okf-cli.py read videos/<slug>
```

If the host uses `python` instead of `python3`, substitute that command.

## Answering Questions

1. Read `index.md` or run `python3 okf-cli.py index`.
2. Search for the user's topic with `python3 okf-cli.py find "<topic>"`.
3. Read only the relevant `concepts/` and `videos/` pages.
4. Follow `related_concepts`, `related_videos`, and markdown links when useful.
5. Ground answers in the bundle. Cite source videos using the page `title` and
   `resource` frontmatter.

## Page Types

- `type: video` pages are source-grounded video summaries.
- `type: concept` pages are synthesis pages across multiple videos.
- `index.md`, `log.md`, `README.md`, `AGENTS.md`, and `CLAUDE.md` are reserved
  navigation/instruction files, not concepts.

## Modification Rule

Treat this bundle as read-only reference knowledge unless the user explicitly
asks to edit or extend it. If creating a derived bundle, copy this directory and
modify the copy.

## Validation

Run this from the bundle root:

```bash
python3 validate_okf_bundle.py
python3 okf-cli.py index
python3 okf-cli.py find "PIV loop"
python3 okf-cli.py read concepts/the-piv-loop
```

