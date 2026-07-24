# LLM Wiki Agent Demo

This is a static, shareable browser demo of the LLM Wiki Agent workflow adapted
from the Fable/Karpathy LLM wiki pattern.

The demo is not a live model backend. It simulates the agent state transitions so
people can see the product behavior before wiring it to Codex, Claude Code, or a
local CLI.

## Run Locally

From the repo root:

```bash
npm run browser:demo
```

Open:

```text
http://127.0.0.1:8766/
```

## Automated Browser Tests

Headless:

```bash
npm run browser:test
```

Headed / visible:

```bash
npm run browser:test:headed
```

Both commands use `playwright.demo.config.ts` and work from Codex or Claude Code
when Chromium and local port binding are available.

## Test Flow

1. Click `Initialize Wiki`.
2. Click `Ingest Source`.
3. Confirm new pages appear under `raw/` and `wiki/`.
4. Click `Ask Query`.
5. Confirm the answer cites routed wiki pages.
6. Click `Run Maintenance`.
7. Confirm `wiki/log.md` records the maintenance pass.
8. Click `Reset` to replay the flow.

## What It Demonstrates

- `raw/` stores human-provided source material.
- `wiki/` stores generated markdown knowledge.
- `wiki/index.md` is the first page an agent reads for routing.
- `wiki/log.md` records ingest/query/maintenance operations.
- Source, concept, and entity pages are linked through backlinks.
- Answers should be grounded in relevant pages, not in a full-bundle scan.

## Real Agent Path

For real local operation, use the repo skill:

```bash
python3 skills/llm-wiki-agent/scripts/init_llm_wiki.py --root /tmp/my-llm-wiki --profile foldered
```

Then ask Codex or Claude Code to ingest files from `raw/` using the instructions
in `AGENTS.md` and `CLAUDE.md`.
