# Workspace map

Use supplied exact paths first. This is a task router, not an inventory.
Detailed references preserve the former entrypoint text verbatim. Read only the
named sections when their task applies. Paths/commands inside those copies resolve
from this repository root; do not follow their historical startup import lines.

## Entry points

| Path | Purpose / read when |
|---|---|
| `AGENTS.md` → `CLAUDE.md` | Short active instructions for Codex and Claude. |
| `docs/task-brief-template.md` | Saved decisions, current scope, dependencies, checks and state for sustained/resumed work. |
| `docs/seven-hacks-operating-policy.md` | Tested, conditional guidance for effort, instructions, saved plans, desktop tools and isolation. |
| `skills/<name>/SKILL.md` | Canonical workflow; bundled scripts, references and assets resolve here. |
| `skills/prompt-master/`, `skills/benai-interview-me/` | Ben AI Codex adaptations: prompt rewrite/audit or bounded requirement interview; preserve separate `interview-me`. |
| `skills/content-ideas/` | Content-feed application; scripts/lib holds fetchers, scoring and rendering. |
| `docs/reference/agent-workflows.md` | Complete previous AGENTS.md policy; scoped sections below. |
| `docs/reference/claude-workflows.md` | Complete previous CLAUDE.md guidance; scoped sections below. |

## Read before the applicable work

| Task | Required reference sections / routes |
|---|---|
| Plugin/application or skill edits | Claude reference: **Structure**, **Cross-host packaging**, **Commands**, **Skill integrity gate**, **Rules**; `tests/test_plugin_contract.py`, `scripts/check_skills.py`, `scripts/check_routes.py`. |
| Missing/corrupted files; recovery/porting | Agent reference: **Filesystem search and integrity rule**, **Skill recovery, research, and porting contract**; `docs/skill-recovery-porting-contract.md`. Include external roots and symlink targets. |
| Research, strategy, pipeline | Agent reference: **GBrain knowledge rule**, **Research-plugin rule**, **Configured research and browser routing**; Claude reference: **Evidence-ranking rules for research-bearing skills**, **Rules**, **GBrain**. |
| Presentations | Agent reference: **Client-facing PPTX rule**, **Presentation consolidation rule**; Claude reference: **Presentation system**, **Rules**, **Portable path defaults**; `skills/present/`, `docs/presentation-pipeline-cross-host-contract.md`. |
| Product roadmap/build; goal work | Agent reference: **Cross-host product-build skills**; Claude reference: **Shared Product-Build Skills**, **Claude Code Director Skill**; `skills/plaid/` and existing PLAID artifacts. |
| UI, animations and accessibility | Claude reference: **Design tokens and WCAG render gates**; the applicable design skill. |
| Videos, Google Vids/Slides, audio/PPTX media | Claude reference: **Google Vids: a real automation lane, reachable over CDP**, plus **Presentation system** for slide media; `skills/watch-video/`, `skills/gemini-video/` for analysis. |
| Part explainer films, motion over narrated deck films, LinkedIn carousels | `skills/part-explainer-film/` (storyboard + draw.io diagram → narrated film; `scripts/run_parts.py` batches parts, Kokoro or ElevenLabs), `skills/film-motion-overlay/` (measure stillness first; audio and captions proven identical), `skills/storyboard-to-carousel/` (1080×1350 PNG + PDF, redrawn blocks, never a pasted diagram). Social graphics go through `ai-graphics`' design-first track. |
| YouTube channel knowledge base | Agent reference: **Channel-to-KB skills**; Claude reference: **Channel-to-KB skills**; `skills/channel-to-kb-ytdlp/` or the named alternative. |
| Graphify extraction | Claude reference: **graphify runs on Claude Sonnet 5.5**; `skills/graphify/`, `scripts/graphify-pro`. |
| Desktop capability/discovery/browser | Agent reference: **Codex Desktop priority skills**, **Configured research and browser routing**, **In-app browser delivery preference**, **Playwright rule**; `docs/codex-wsl-skill-compatibility.md`, `docs/codex-capability-routing.md`. |
| Provider, proxy or cross-host config | Agent reference: **Local AI-gateway proxy diagnostics**, **Antigravity CLI & IDE cross-host sync contract**; Claude reference: **Model routing across hosts**, **Rules**, **DeepSeek Harness (dsh) model providers**; `docs/antigravity-sync-backlog.md`. |
| PDF services | Claude reference: **Local PDF service (Stirling PDF)**; `skills/pdf/`. |
| ADK/CopilotKit frontend tools | Claude reference: **ADK + AG-UI (Generative UI) rules**, **Reference repos (cloned locally)**. |
| Creating/auditing a skill | Claude reference: **Skill Builder**, **Cross-host packaging**, **Skill integrity gate**; `skills/skill-builder/`. |

Headings may include suffixes; use a targeted heading search before reading.
Update this map when listed entrypoints move. Omit generated runs, dependencies,
caches and secret locations.
