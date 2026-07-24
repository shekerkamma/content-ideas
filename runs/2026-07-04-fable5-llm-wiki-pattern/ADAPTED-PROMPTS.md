# Adapted Prompts For Testing The Fable/Karpathy LLM Wiki Workflow

These prompts are adapted from the watched video and rewritten for this repo so
they work in both Codex and Claude Code.

## Setup Prompt

```text
You are my LLM wiki agent. Build a complete markdown second brain from this
source idea. Create host instructions for both AGENTS.md and CLAUDE.md, define
the raw/wiki/index/log schema, initialize the vault, and show one first ingest
example. From now on, every ingest and query must follow this schema.
```

Expected result:

- `raw/`
- `wiki/`
- `wiki/index.md`
- `wiki/log.md`
- `AGENTS.md`
- `CLAUDE.md`

## PDF + URL Ingest Prompt

```text
Read this URL capture and ingest it into the wiki. I also placed a PDF extract
in raw/ named claude-fable-5-llm-wiki-pdf-extract.md; ingest that too.

Create or update source, concept, entity, topic, and answer pages as needed.
Update wiki/index.md with route hints. Append wiki/log.md. Add markdown
backlinks between related pages. Treat raw/ as read-only.
```

Expected result:

- `wiki/sources/*`
- `wiki/concepts/*`
- `wiki/entities/*`
- `wiki/topics/*`
- `wiki/answers/*`
- updated `wiki/index.md`
- appended `wiki/log.md`

## Query Prompt

```text
Using only this wiki, answer: how do I build the same Fable/Karpathy LLM wiki
workflow?

Start from wiki/index.md, follow only relevant links, cite the pages you used,
and do not scan the whole bundle.
```

Expected route:

```text
wiki/index.md
-> wiki/answers/how-to-build-fable-style-llm-wiki.md
-> wiki/sources/karpathy-llm-wiki-url.md
-> wiki/sources/fable-5-llm-wiki-pdf.md
```

## Flat vs Structured Prompt

```text
Based on this wiki, should I keep the vault flat or structured? Answer from the
index and the relevant concept page only. Cite the pages used.
```

Expected route:

```text
wiki/index.md
-> wiki/concepts/flat-vs-foldered-wiki.md
```

## Repeatable Smoke Test

Run:

```bash
python3 skills/llm-wiki-agent/scripts/smoke_fable_ingest.py --reset
```

The script creates:

```text
/tmp/llm-wiki-fable-smoke
```

and validates:

- the vault initializes
- PDF and URL-style sources are dropped into `raw/`
- generated wiki pages are created
- `index.md` routes questions
- `log.md` records ingest and query
- answer pages cite source pages

## Live Chromium Download Test

Headless:

```bash
npm run llm-wiki:live
```

Headed / visible:

```bash
npm run llm-wiki:live:headed
```

Override sources:

```bash
npm run llm-wiki:live:headed -- --url <url> --pdf-url <pdf-url>
```

Expected result:

- Chromium opens/downloads the live URL and PDF
- captures are written into `/tmp/llm-wiki-fable-live/raw/`
- the raw PDF is preserved under `/tmp/llm-wiki-fable-live/raw/downloads/`
- source/concept/entity/answer pages are generated under `wiki/`
- `wiki/index.md` routes to the live answer page
- `wiki/log.md` records the live download ingest

Rules for agents:

- Use this live path only when live download or visible browser validation is
  requested.
- Do not mutate `raw/` source files after capture.
- Preserve original PDFs and source metadata.
- Generated source pages must cite raw paths and source URLs.
- Query answers must start from `wiki/index.md` and cite the pages used.
