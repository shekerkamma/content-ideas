# Fable 5 / Karpathy LLM Wiki Pattern Notes

Source video analyzed with the local `watch` skill:

- Title: `Fable 5 + Karpathy's LLM Wiki is Basically Cheating`
- URL: https://www.youtube.com/watch?v=hQvwMj7IJe4
- Uploader: Nate Herk | AI Automation
- Duration: 14:35
- Captures:
  - balanced transcript + frames: `/tmp/watch-fable5-patterns`
  - token-burner frames: `/tmp/watch-fable5-tokenburner`
  - focused setup frames: `/tmp/watch-fable5-setup-focus`

## What The Video Demonstrates

The video shows an LLM wiki as a persistent markdown knowledge graph between raw
sources and agent answers. The point is not that Fable 5 is required. The point
is that once source material is routed into markdown pages with links, index,
and logs, any file-reading agent can use it.

## Core Operating Model

The file tree shown in the video:

```text
my-wiki/
  raw/          # human puts source material here; read-only for the agent
  wiki/         # agent writes generated knowledge here
    index.md   # table of contents and routing surface
    log.md     # operation history
    *.md       # generated wiki pages
  CLAUDE.md    # rules/schema for the host
```

Codex adaptation:

```text
my-wiki/
  raw/
  wiki/
    index.md
    log.md
    *.md
  AGENTS.md
  CLAUDE.md
```

Use both `AGENTS.md` and `CLAUDE.md` so the same wiki can be opened in Codex,
Claude Code, or a Fable-enabled Claude Code session.

## Voice Prompt Patterns Captured

These are adapted prompt patterns from the video, rewritten for this repo so we
can use them without model/vendor lock-in.

### Initial Wiki Setup Prompt

Use when creating a new wiki from Karpathy's gist or a source idea file:

```text
You are my LLM wiki agent. Build this source idea into a complete second-brain
wiki. Guide the setup step by step. Create host instructions for both AGENTS.md
and CLAUDE.md, define the schema and folder conventions, initialize index.md
and log.md, and show the first ingest example. From now on, every ingest and
query should follow this schema.
```

### URL + Local File Ingest Prompt

Use when the user gives a URL and drops a file into `raw/`:

```text
Read this URL and ingest it into the wiki. I also placed a file in raw/ named
<file-name>; ingest that too. Update the index, append the log, create or update
source/concept/entity/topic pages as needed, and cross-link related ideas.
```

### Visual Resource Prompt

The video also shows a one-shot prompt asking the model to turn a graph of
transcripts and relationships into a beginner-friendly HTML resource. The
transferable pattern is:

```text
Turn this dense wiki/graph into a beginner-friendly visual resource. Make it
simple to click through, avoid overwhelming readers, show how tools,
techniques, videos, and ideas connect, and cite the pages each idea came from.
```

## Structural Lessons

- The wiki should grow incrementally.
- `raw/` stores sources; `wiki/` stores generated pages.
- `index.md` is content-oriented routing, not just a file listing.
- `log.md` is chronological and append-only.
- Backlinks are what make the wiki valuable compared with isolated summaries.
- Flat structures can be better for homogeneous data like meeting transcripts.
- Foldered structures can be better for mixed domains such as videos, tools,
  techniques, sources, topics, entities, and comparisons.
- An ingest may turn one source into one page or many pages.
- The agent should decide page granularity, then the human should review it.
- If a batch ingest creates confusing folders, update the rules and rerun or
  refactor.

## Recommended Page Types

Use these as a starting set, not a rigid ontology:

- `source`: a source document, video, PDF, article, transcript, meeting, or URL
- `concept`: reusable idea that appears across sources
- `entity`: person, company, product, model, tool, repo, organization
- `topic`: domain hub or collection
- `comparison`: page that contrasts two or more entities/concepts
- `note`: filed answer or synthesis that does not deserve its own concept yet

## Cross-Host Adaptation

For Codex:

- `AGENTS.md` is the default routing/schema surface.
- Use shell reads and `rg` first.
- Keep scripts stdlib and local.
- Avoid host-specific URI links.

For Claude Code / Fable:

- `CLAUDE.md` is the default routing/schema surface.
- The same markdown wiki structure should work.
- Fable can be used later for richer visual synthesis, but ingestion rules stay
  model-neutral.

## Acceptance Criteria For A Working Wiki

- `raw/` exists and is treated as read-only input.
- `wiki/index.md` exists and helps the agent route questions.
- `wiki/log.md` exists and records setup, ingest, query, and maintenance events.
- Generated wiki pages have source traceability.
- Related pages link to each other.
- The wiki can answer a question by reading `index.md`, then a small set of
  relevant pages.
- The wiki can be operated by both Codex and Claude Code.

