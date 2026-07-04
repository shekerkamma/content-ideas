---
name: llm-wiki-agent
description: Build and operate a markdown LLM wiki/second-brain bundle from raw sources using the Karpathy LLM Wiki pattern, adapted for both Codex and Claude Code. Use when the user says LLM wiki, second brain, wiki ingest, raw-to-wiki, Karpathy wiki, Fable wiki pattern, or asks to ingest documents/videos/URLs into a markdown knowledge base.
category: Knowledge Management
license: MIT
---

# LLM Wiki Agent

Use this skill to create or maintain a model-readable markdown wiki that can be
used by Codex, Claude Code, Fable-style Claude Code sessions, Hermes, or any
agent that can read files.

The implementation is model-neutral. Fable 5 may be useful later for richer UI
or synthesis, but the base wiki must work with ordinary Codex and Claude Code.

## Source Pattern

This skill adapts the pattern from Nate Herk's "Fable 5 + Karpathy's LLM Wiki is
Basically Cheating" video and Karpathy's LLM Wiki gist:

- `raw/` is where humans put source material. Treat it as read-only input.
- `wiki/` is where the agent writes structured markdown knowledge.
- `wiki/index.md` is the table of contents and routing surface.
- `wiki/log.md` is append-only operation history.
- `AGENTS.md` and `CLAUDE.md` define the rules/schema for Codex and Claude Code.
- Every ingest should update both the wiki pages and routing surfaces.
- Flat folder structures are fine when the corpus is small or homogeneous.
- Foldered structures are useful when source types naturally diverge.

Read `references/fable5-llm-wiki-pattern.md` before designing a new wiki.

## Quick Start

To initialize a new wiki:

```bash
python3 skills/llm-wiki-agent/scripts/init_llm_wiki.py --root path/to/wiki --profile foldered
```

Profiles:

- `flat`: `raw/`, `wiki/index.md`, `wiki/log.md`, and wiki pages directly under
  `wiki/`.
- `foldered`: also creates `wiki/concepts/`, `wiki/entities/`, `wiki/sources/`,
  and `wiki/topics/`.
- `okf`: creates an OKF-compatible bundle layout with root `index.md`, `log.md`,
  `sources/`, `concepts/`, and `entities/`.

## Ingest Workflow

1. Identify the source:
   - local markdown/PDF/transcript/article pasted by the user
   - URL the user asks to ingest
   - generated video transcript or watch output
2. Place or reference source material under `raw/` when possible.
3. Read `wiki/index.md` and recent entries in `wiki/log.md`.
4. Decide whether existing pages should be updated or new pages created.
5. Create/update source, concept, entity, topic, and comparison pages as needed.
6. Add backlinks between related pages.
7. Update `wiki/index.md` with one-line summaries and route hints.
8. Append an entry to `wiki/log.md`.
9. Report what changed and what source paths support the changes.

## Query Workflow

When answering from a wiki:

1. Start with `wiki/index.md`.
2. Read recent `wiki/log.md` entries when recency matters.
3. Follow links only to relevant pages.
4. Prefer source-backed claims. Mark inference explicitly.
5. Cite source paths or page names.
6. Do not scan the whole wiki unless the question requires it.

## Maintenance Workflow

Run maintenance after every 5-10 ingests or when answers feel weak:

- check orphan pages
- check stale backlinks
- identify contradictions
- merge duplicate concepts
- split oversized pages
- update `index.md`
- append a `lint` or `maintenance` entry to `log.md`

## Guardrails

- The human curates sources and judges structure; the agent does the filing.
- Do not mutate `raw/` files unless the user explicitly asks.
- Do not invent sources.
- Keep claims traceable to source pages.
- Use markdown links, not host-specific plugin links.
- Avoid embedding/vector systems as the default. The wiki should work as plain
  markdown first.
- Make the structure make sense to both the model and the human.

