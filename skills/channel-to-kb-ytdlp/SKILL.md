---
name: channel-to-kb-ytdlp
description: >
  Use when the user wants to turn an entire YouTube channel into an OKF (Open
  Knowledge Format) knowledge base / Karpathy-style LLM wiki — phrases like
  "build a knowledge base from this channel", "turn this channel into a
  wiki", "/channel-to-kb-ytdlp @handle". Uses yt-dlp for both channel
  enumeration and subtitle download: free, no API key, most reliable against
  YouTube changes, captures publish dates automatically. Recommended default
  over the peer skills channel-to-kb (pytubefix, no key, can be IP-blocked on
  cloud hosts) and channel-to-kb-supadata (paid managed API, no IP-blocking
  risk). Ported from coleam00/cole-medin-knowledge-base.
license: MIT
argument-hint: "<@ChannelHandle or channel-URL>"
metadata:
  category: Content Research
  version: "1.0"
  source: https://github.com/coleam00/cole-medin-knowledge-base
---

# Build an OKF Knowledge Base from a YouTube Channel (yt-dlp)

Turn any YouTube channel into a synthesized, cross-linked knowledge base in
[Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/knowledge-catalog):
plain markdown + YAML frontmatter, navigated by index and relative links, no
database or embeddings required. Any AI can read the output with zero setup.

Uses yt-dlp for both channel enumeration and subtitle download. Free, no API
key required. Most reliable of the three `channel-to-kb*` variants — yt-dlp
is actively maintained and handles YouTube changes fast.

Resolve this skill's own directory from the loaded `SKILL.md` path before
running any script below (`<skill-dir>`).

## Output location

Default output directory is `$CONTENT_HOME/knowledge-bases/<channel-slug>/`
(`$CONTENT_HOME` defaults to `~/Documents/Content`, per this repo's
persistent-state convention — never write build state into the cwd). If the
user names a different location, use that instead. Call this directory
`<output-dir>` below.

## Step 0: Scaffold the OKF bundle

If `<output-dir>/SCHEMA.md` does not already exist, this is a fresh bundle —
copy the bundled OKF toolkit in before doing anything else:

```bash
mkdir -p "<output-dir>/scripts"
cp "<skill-dir>/assets/okf-template/SCHEMA.md" "<output-dir>/SCHEMA.md"
cp "<skill-dir>/assets/okf-template/lint.py" "<output-dir>/lint.py"
cp "<skill-dir>/assets/okf-template/scripts/build_indexes.py" "<output-dir>/scripts/build_indexes.py"
```

Both `lint.py` and `scripts/build_indexes.py` resolve their root relative to
their own file location, so once copied into `<output-dir>` they operate on
that bundle with no path edits needed.

Read the OKF contract this bundle obeys:
1. Read `<output-dir>/SCHEMA.md` (the maintainer contract: page types,
   frontmatter schemas, linking rules)
2. Skim the [OKF SPEC](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
   for the hard rules (every page needs `type` in frontmatter, `index.md` is
   reserved, cross-links are relative markdown paths)

If `<output-dir>/SCHEMA.md` already exists, skip this step — you're adding to
or rebuilding an existing bundle.

## Step 1: Fetch transcripts

```bash
uv run "<skill-dir>/scripts/fetch_transcripts.py" $ARGUMENTS --output-dir "<output-dir>/raw"
```

This enumerates all videos, downloads English subtitles as json3, and
converts them to timestamped OKF raw-transcript pages. Output:
`<output-dir>/raw/<slug>.md` files (each with `type: raw-transcript`
frontmatter, OKF-conformant) plus `<output-dir>/raw/manifest.json`.

Flags:
- `--limit N` to cap the number of videos (start here for testing)
- `--delay 3.0` to increase the pause between requests if you hit 429 rate limits

Wait for the script to complete before proceeding.

## Step 2: Build the OKF knowledge base

Read `<skill-dir>/references/pipeline-guide.md` for the full process. It
produces an OKF-conformant bundle with the structure defined in
`<output-dir>/SCHEMA.md`. The stages:

1. **Extract** — read each raw transcript, extract concepts/entities/quotes
   as JSON to `<output-dir>/scripts/extractions/`
2. **Canonicalize** — merge all extractions into a frozen taxonomy
   (`<output-dir>/scripts/manifest.json` + `<output-dir>/scripts/taxonomy.json`)
3. **Write** — write OKF concept/entity/source pages from the manifest (each
   with proper `type`, `title`, `description` frontmatter per SCHEMA.md)
4. **Index** — build `index.md` files for each directory (OKF's navigation
   layer)
5. **Validate** — run `lint.py` to enforce OKF conformance, link integrity,
   and index coverage

Process in batches per the guide. For channels under ~30 videos, this fits in
one session. For larger channels, save your extraction JSONs and resume
across sessions.

## Step 3: Build indexes

```bash
python "<output-dir>/scripts/build_indexes.py"
```

## Step 4: Validate OKF conformance

```bash
python "<output-dir>/lint.py"
```

This enforces the OKF contract: every `.md` has `type` frontmatter (E1),
every relative link resolves (E2), every page appears in its directory's
`index.md` (E3), sources/raw parity (E4). Fix all errors. The knowledge base
is ready when lint passes clean.

## Use the finished bundle with an agent

Once lint passes, point any coding agent at `<output-dir>` with a prompt like:

```
Use the knowledge base at <output-dir> as a reference. Read index.md, then
SCHEMA.md. This is an Open Knowledge Format (OKF) bundle — a linked wiki of
concepts and entities mined from the channel's videos. Navigate it the OKF
way: read the index, follow the relative links into concepts/, entities/,
and sources/, and open only the pages a question needs. When answering,
cite the concept/entity pages you used and the source video(s) they came
from (each page ends with a `## Sources` section listing videos and
timestamps). If something isn't covered, say so instead of guessing.
```
