# Skill context audit (October 2026)

**Status:** proposal. Nothing has been deleted or merged. Each item below needs
an explicit OK before anyone acts on it.

## Why this matters

Every installed skill's `name` and `description` load into every chat, even when
the skill never runs. With the plugin installed in Claude Code, this repo loads
47 skills (40 under `skills/`, 7 under `.claude/skills/`). Their descriptions
total about 19,900 characters, roughly 5,000 tokens per chat, before any work
starts.

Usage counts are not available from the repo. Run `/skill-doctor` in the Claude
desktop app (Code tab) to see how often each skill actually fires, then use
that to confirm or reject the items below.

## Recommendations

### 1. Remove duplicate copies that load twice (low risk)

| Skill | Copies | Proposal |
|---|---|---|
| `impeccable` | `skills/`, `.claude/skills/`, `.agents/skills/`, `.github/skills/` (byte-identical) | Drop `skills/impeccable/`. `CLAUDE.md` names only the three per-harness copies; the `skills/` one makes Claude Code load it twice when the plugin is installed. Check `skills/watch/references/impeccable-slide-pipeline.md` first. |
| `investor-competitive-dossier` | `skills/` (canonical) and a `.claude/skills/` wrapper | Keep one. If the plugin is always installed, drop the wrapper; if the repo is used without the plugin, keep the wrapper and accept the duplicate. |

### 2. Merge overlapping skills (medium effort)

| Group | Skills | Overlap | Proposal |
|---|---|---|---|
| Channel to knowledge base | `channel-to-kb`, `channel-to-kb-ytdlp`, `channel-to-kb-supadata` | Same output, same trigger phrases; only the transcript fetcher differs. About 2,060 description chars. | One `channel-to-kb` skill with a fetcher choice (yt-dlp default, pytubefix, Supadata). Also removes the three-way byte-identical `assets/okf-template/` rule. |
| Competitor analysis | `aianalyst-competitor-analysis`, `competitor-analysis-pipeline`, `evidence-led-competitor-pipeline`, `investor-competitive-dossier` | The first two list nearly the same trigger phrases, so the model has to guess between them. | One public entry point (for example `competitor-analysis-pipeline`) that routes to the others; set the rest to `user-invocable: false` with short descriptions. |
| Graphics | `ai-graphics`, `explainer-graphic`, `image-generation-router` | `explainer-graphic` is a narrow case of `ai-graphics`. `image-generation-router` is an internal dependency, not something users ask for by name. | Fold `explainer-graphic` into `ai-graphics` as a mode. Mark `image-generation-router` internal and shorten its description. |

### 3. Shorten long descriptions (low risk)

A description only needs to say when to use the skill. These are over 600
characters; trimming each to about 300 saves roughly 2,500 characters.

| Skill | Chars |
|---|---|
| `impeccable` | 895 |
| `financial-model-review` | 728 |
| `channel-to-kb` | 717 |
| `channel-to-kb-supadata` | 681 |
| `channel-to-kb-ytdlp` | 662 |
| `build-client-acquisition-function` | 626 |
| `branded-pptx-deck` | 620 |

Run the three `skill-builder` audit scripts after any description change; they
check that the trigger phrases still match.

### 4. Keep as is

- `docx`, `pdf`, `improve`, `storm-research`: `CLAUDE.md` names these as
  portable recovery sources. They overlap with built-in host skills, but they
  exist so Codex and OpenHands have the same capability.
- `content-ideas`, `pipeline-runner`, `second-brain`, `plaid`,
  `karpathy-guidelines`: canonical shared sources mirrored under
  `plugins/content-ideas/skills/`.

## Also found

`.claude/settings.json` lists skill paths under `/home/sheke/...`, including
`/home/sheke/content-ideas.local/...`. Those only resolve on one machine. This
conflicts with the rule that host-specific paths must be configurable. It is
out of scope here, but worth fixing separately.

## Already done in the same change

- `CLAUDE.md` cut from about 25 KB to about 14 KB. Machine-specific setup
  moved to `docs/agent-reference/`; every rule the contract tests check stays
  in `CLAUDE.md`.
