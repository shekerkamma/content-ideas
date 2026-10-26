# Channel-to-KB skills

<!-- Moved out of CLAUDE.md so it only loads when needed. Read on demand. -->

Three peer skills that turn any YouTube channel into an OKF (Open Knowledge
Format) knowledge base / Karpathy-style LLM wiki, differing only in how they
fetch transcripts:
- `skills/channel-to-kb/SKILL.md` — pytubefix + youtube_transcript_api, free,
  no API key, can be IP-blocked on cloud hosts.
- `skills/channel-to-kb-ytdlp/SKILL.md` — yt-dlp, free, no API key, most
  reliable against YouTube changes. Recommended default.
- `skills/channel-to-kb-supadata/SKILL.md` — Supadata managed API, paid
  (`SUPADATA_API_KEY`), no IP-blocking risk.

Each skill bundles its own copy of the shared OKF toolkit under
`assets/okf-template/` (`SCHEMA.md`, `lint.py`, `scripts/build_indexes.py`)
and `references/pipeline-guide.md` — these four files must stay
byte-identical across all three skill directories (mirrors the
`plugins/content-ideas/skills/` byte-identical convention above). Output
bundles scaffold under `$CONTENT_HOME/knowledge-bases/<channel-slug>/`, never
the cwd. If upstream (`coleam00/cole-medin-knowledge-base`) changes its
`SCHEMA.md`, `lint.py`, `scripts/build_indexes.py`, or
`.claude/references/pipeline-guide.md`, re-port them into all three skills'
`assets/okf-template/` and `references/` and re-verify the scaffold lints
clean on an empty bundle before shipping.

