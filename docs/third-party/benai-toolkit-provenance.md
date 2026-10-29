# BenAI toolkit — what was taken, what was not

Source pages, retrieved 2026-09-09:
- Fable 5.1 Toolkit — `benai.notion.site/Fable-5-1-Toolkit-3d01124570fe8136b457cf6f28c85139`
- Prompting Opus 5 — `benai.notion.site/Prompting-Opus-5-3d01124570fe80f9a6f9db36a15f7293`

Both are lead magnets for a paid programme. That does not make the material bad
— `eli5` also ships on Anthropic's official community marketplace — but it does
mean the framing optimises for perceived completeness. Two of the four skills
are under 5 KB.

**Model targeting:** the source attributes its interview pattern to a Claude
Fable field guide. This repo targets **Opus** (`meta-loop` runs Opus as sole
aggregator; `claudex-loop`'s deep tier hardcodes `model: 'opus'`). The ported
behaviours are model-agnostic interview craft, so they carry no Fable framing.

## Decisions

| Asset | Decision | Reason |
|---|---|---|
| `eli5` (401 B) | **Installed** — `~/.claude/skills/eli5/` | No equivalent here. `explainer-graphic` is infographic-and-analogy, not a plain-language HTML page. No trigger collision (`coding-tutor` and `last30days` use "ELI5" as prose only). |
| `rule-rewriter` (4.6 KB) | **Installed, and wired to a broken route** | `/claude-md-auditor` was documented in the global CLAUDE.md and existed **nowhere** — an empty directory. That route now points at `rule-rewriter`, converting an install into a repair. |
| `interview-me` (1.5 KB) | **Adapted, not installed** | `skills/interview-me` is 269 lines against ~40 and deeper where they overlap. Three behaviours were genuinely absent and were ported (below). |
| `instant-ui` (62 KB) | **Split; not installed** | Component inventory and four craft rules harvested into `refero-design/references/page-component-inventory.md`. Brand, paths and font policy rejected — see that file's provenance section. |
| 16 reference galleries | **Adopted** | 11 were missing from `refero-design`; added as `references/reference-galleries.md`, organised by need rather than as a flat list. |
| Retired-instructions checklist | **Ran as an audit; nothing to fix** | 8 of 10 mechanically-checkable patterns returned zero hits across both CLAUDE.md files and 344 SKILL.md files. The six matches are the opposite failure mode — gating a *completion claim* on evidence, which is correct. |
| Full Job Brief / Done Means / Why Sentence templates | **Not adopted** | Restating guidance this repo's CLAUDE.md and `interview-me` already carry. |
| Plain English voice block | **Not adopted** | `~/.claude/skills/voice.md` is already mandated globally for all written output. |
| `prompt-master` (15.8 KB) | **Not taken** | Bundles the other seven giveaways. Overlaps `skill-builder`, `writing-for-agents`, `skills-analyst` and now `rule-rewriter`. |

## Ported into `skills/interview-me`

Three behaviours, confirmed absent from the existing skill by grep before porting:

1. **Step 0 — read before you ask.** Never ask what reading would answer. With a
   five-to-seven question budget, a question spent on a discoverable fact is one
   not spent on a real unknown.
2. **Step 3b — name the blind spot.** Before the restate, say what the interview
   has *not* covered that could still change the outcome.
3. **When the user rambles.** Reconstruct it into answers and ask only about what
   it did not reach; re-asking something volunteered signals you were not
   listening.

**Deliberately not ported:** BenAI's step 6 executes the brief. This repo's
`interview-me` stops at confirmed intent and routes to `spec-driven-development`
or `idea-refine`. That is an architectural choice already made here, not an
oversight.

## Also found while doing this

Three routes documented in a CLAUDE.md resolve to nothing anywhere:
`/claude-md-auditor` (**fixed** — now `/rule-rewriter`), `/skill-distiller`, and
`/vertical-scorer`. Separately, 61 of 332 directories under `~/.claude/skills/`
contain no files; most are harmless shells whose real copy lives in the repo or
gstack tree, but the permission bits (`drwxrwxrwx` against `drwxr-xr-x` on
working skills) suggest a Windows-side copy that lost its contents.
