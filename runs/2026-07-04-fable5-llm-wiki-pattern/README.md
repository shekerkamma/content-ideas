# Fable 5 / Karpathy LLM Wiki Pattern Capture

Source video:

- `Fable 5 + Karpathy's LLM Wiki is Basically Cheating`
- https://www.youtube.com/watch?v=hQvwMj7IJe4
- Uploader: Nate Herk | AI Automation
- Duration: 14:35

## Watch Captures

- Balanced transcript + frames: `/tmp/watch-fable5-patterns`
- Token-burner frames: `/tmp/watch-fable5-tokenburner`
- Focused setup frames: `/tmp/watch-fable5-setup-focus`
- Persisted contact sheet: [token-burner-contact-sheet.jpg](token-burner-contact-sheet.jpg)

Token-burner result: 38 selected frames from 39 scene-change candidates. The
video had relatively few scene changes, so token-burner did not produce hundreds
of frames. Important prompt and structure frames were inspected directly.

## Key Captured Instructions

- Use an LLM wiki as persistent accumulated knowledge, not one-off RAG.
- Human curates sources and judges structure; agent handles maintenance.
- `raw/` is read-only source input.
- `wiki/` is generated markdown knowledge output.
- `wiki/index.md` is the routing surface / table of contents.
- `wiki/log.md` is append-only operation history.
- `AGENTS.md` / `CLAUDE.md` hold host-specific rules and schema.
- Use flat structure for homogeneous corpora such as meeting transcripts.
- Use foldered structure for mixed corpora such as videos, tools, techniques,
  sources, entities, topics, and comparisons.
- Every ingest should update generated pages, backlinks, index, and log.
- Batch ingests should be reviewed by the human; if structure is confusing,
  update the rules and refactor.
- The system remains portable because the wiki is just markdown files with
  routing.

## Implementation

Implemented as repo-local skill:

- [skills/llm-wiki-agent/SKILL.md](../../skills/llm-wiki-agent/SKILL.md)
- [skills/llm-wiki-agent/references/fable5-llm-wiki-pattern.md](../../skills/llm-wiki-agent/references/fable5-llm-wiki-pattern.md)
- [skills/llm-wiki-agent/scripts/init_llm_wiki.py](../../skills/llm-wiki-agent/scripts/init_llm_wiki.py)

Registered in:

- [AGENTS.md](../../AGENTS.md)
- [CLAUDE.md](../../CLAUDE.md)
- [.claude/settings.json](../../.claude/settings.json)

## Shareable Demo

The interactive browser demo is here:

- [interactive-demo/index.html](interactive-demo/index.html)
- [interactive-demo/README.md](interactive-demo/README.md)

It is intentionally static. It shows the end-to-end LLM wiki agent workflow
without requiring API keys, local filesystem access, or a model backend:

1. initialize the wiki structure
2. ingest a source into source/concept/entity pages
3. answer a query by routing through `index.md`
4. log a maintenance pass

Use the repo-local skill for real local operation:

```bash
python3 skills/llm-wiki-agent/scripts/init_llm_wiki.py --root /tmp/my-llm-wiki --profile foldered
```

Publishing notes are in [PUBLISH.md](PUBLISH.md).

## Real Workflow Smoke Test

The repeatable smoke test for the video pattern is:

```bash
python3 skills/llm-wiki-agent/scripts/smoke_fable_ingest.py --reset
```

It tests the concrete workflow shown in the video:

1. initialize a vault
2. drop a URL-style source and PDF-extract source into `raw/`
3. ingest them into source/concept/entity/topic/answer pages
4. update `wiki/index.md`
5. append `wiki/log.md`
6. validate that a query can route through the wiki without scanning everything

Adapted test prompts are in [ADAPTED-PROMPTS.md](ADAPTED-PROMPTS.md).

For a live Chromium download test:

```bash
npm run llm-wiki:live
npm run llm-wiki:live:headed
```

The headed variant visibly downloads a URL and PDF through Chromium before
writing them into `/tmp/llm-wiki-fable-live/raw/` and ingesting them into the
wiki.
