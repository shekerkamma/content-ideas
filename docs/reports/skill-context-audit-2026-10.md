# Skill context audit (October 2026)

**Status:** closed. Long descriptions are shortened and overlapping groups are
disambiguated. After review, nothing is deleted or merged; each decision and
its reason is below.

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

### 1. Duplicate copies (reviewed: keep `impeccable`)

| Skill | Copies | Decision |
|---|---|---|
| `impeccable` | `skills/`, `.claude/skills/`, `.agents/skills/`, `.github/skills/` | **Keep all.** The copies are not identical: `skills/impeccable/` has extra `reference/degraded/` files and other differences. It is also the canonical source that `scripts/sync-presentation-pipeline-hosts.sh` installs to other hosts, as part of the governed presentation bundle in `config/presentation-pipeline-hosts.json`. Removing it would break that sync. |
| `investor-competitive-dossier` | `skills/` (canonical) and a `.claude/skills/` wrapper | **Keep the wrapper.** It is 160 characters and makes the skill available before anyone installs the plugin. |

### 2. Overlapping skills (reviewed: no merges)

| Group | Decision | Why |
|---|---|---|
| `channel-to-kb`, `-ytdlp`, `-supadata` | **Keep three skills.** | After item 3 their descriptions total about 1,000 characters, so a merge saves little. They are a deliberate peer set ported from upstream with a byte-identical-asset rule, and a merge would mean re-porting all three. |
| `competitor-analysis-pipeline`, `aianalyst-competitor-analysis`, `evidence-led-competitor-pipeline` | **Keep; descriptions rewritten.** | They are layers, not copies: base delivery pipeline, evidence-dataset layer, and an orchestrator that chains both. The old descriptions repeated the same trigger list. Each now says which layer it is and points to the others (about 1,450 → 995 characters). `investor-competitive-dossier` stays separate (investor diligence, not competitor analysis). |
| `ai-graphics`, `explainer-graphic`, `image-generation-router` | **Keep.** | `explainer-graphic` and `ai-graphics` are both in the governed presentation bundle (`config/presentation-pipeline-hosts.json`), and `explainer-graphic` is in the `skill-builder` audit list. Folding it would break the host sync and the audits. `image-generation-router` is a dependency that other skills call by name. |

### 3. Shorten long descriptions (done)

A description only needs to say when to use the skill. These were over 600
characters. All but `impeccable` are now about 300 to 345 characters, saving
about 2,000 characters. Each kept its "Use when" opener, its trigger
phrases, and its peer-skill pointers. `impeccable` is left alone because it is
upstream content that `npx impeccable skills install` would overwrite.

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

## Also found (fixed)

`.claude/settings.json` had a `skills` list of `/home/sheke/...` paths. Claude
Code has no such setting, so the list never loaded anything on any machine. It
is replaced by the documented `extraKnownMarketplaces` + `enabledPlugins` pair,
which enables this repo's own `content-ideas` plugin (every skill under
`skills/`). `tests/test_plugin_contract.py` now checks the file stays free of
machine paths.

## Already done in the same change

- `CLAUDE.md` cut from about 25 KB to about 14 KB. Machine-specific setup
  moved to `docs/agent-reference/`; every rule the contract tests check stays
  in `CLAUDE.md`.
