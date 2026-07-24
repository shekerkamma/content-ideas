# Skill Activation Audit

Date: 2026-07-02

## Goal

Audit archived Claude skills against active Codex-visible skill roots and decide which skills should be intentionally re-exposed without recreating Codex skill-context budget pressure.

## Current State

- Active discoverable skills after this run: 81
- Valid Claude-global skills found: 173
- Valid Claude skills missing from active Codex roots: 110
- Broken Claude skill link: 1
- Newly exposed in this run:
  - `skills/watch -> /home/shekerk/.claude/skills/watch`
  - `skills/excalidraw -> /home/shekerk/.claude/skills/excalidraw`

The gap is intentional in part: many Claude skills were archived under Codex `skills-archive` folders dated 2026-07-01, apparently to reduce skill context load. Codex should not re-expose all archived skills by default.

## Recommendation

Use a two-layer model:

1. **Always-on repo skills**: only workflow-critical skills that should route automatically in normal Codex use.
2. **On-demand skill shelf**: archived Claude skills that remain available by path and can be symlinked into `skills/` when a workflow needs them.

Do not bulk symlink all 110 missing skills into `content-ideas/skills`. That likely recreates the discovery-budget issue and makes routing less reliable.

## Tier 0: Already Fixed

These should stay active because they directly support the video-to-diagram workflow.

| Skill | Reason | Status |
|---|---|---|
| `watch` | Video URL/local video ingestion, frame extraction, captions/Whisper. Needed for YouTube screenshot capture. | Exposed |
| `excalidraw` | Diagram recreation target. Needed for screenshot-to-editable-diagram workflows. | Exposed |

## Tier 1: Strong Candidates For Always-On

These are high-leverage workflow skills that are frequently downstream of strategy, research, deck, diagram, and consulting workflows. Re-expose intentionally if the goal is to make Codex behave like the full consulting/content OS.

| Skill | Why it matters | Chaining role | Activation |
|---|---|---|---|
| `content-research` | Multi-source ingestion from URLs, YouTube, LinkedIn, GitHub, and web pages. | Upstream evidence ingestion for research, strategy, and knowledge-base runs. | Recommended |
| `drawio` | Architecture and workflow diagrams in a broadly portable format. | Alternative/peer to `excalidraw` for formal system diagrams. | Recommended |
| `video-to-deck` | Turns watched video material into deck-ready output. | `watch -> video-to-deck -> branded-pptx-deck` or presentation workflow. | Recommended |
| `research-to-deck` | Converts research artifacts into deck structure. | `content-research -> research-to-deck -> branded-pptx-deck`. | Recommended |
| `research-to-strategy` | Converts research artifacts into strategy. | `content-research -> research-to-strategy -> brief/deck`. | Recommended |
| `ai-strategy-brief` | Core strategy narrative output. | Downstream of research, upstream of deck. | Recommended |
| `presales-deal-prep` | Client/prospect prep is central to this repo's consulting OS. | Account context -> deal brief -> objections/deck. | Recommended |
| `vertical-scorer` | Useful for evaluating niches/use cases and prioritizing markets. | Upstream decision gate before roadmap/deck. | Recommended |
| `workflow-visualizer` | Produces visual workflow maps. | Research/strategy -> visual system map. | Recommended |
| `graphify` | Project/code/content knowledge graphing. | Transform stage for source material and repo context. | Recommended if used often |

Suggested symlink commands if approved later:

```bash
ln -s /home/shekerk/.claude/skills/content-research skills/content-research
ln -s /home/shekerk/.claude/skills/drawio skills/drawio
ln -s /home/shekerk/.claude/skills/video-to-deck skills/video-to-deck
ln -s /home/shekerk/.claude/skills/research-to-deck skills/research-to-deck
ln -s /home/shekerk/.claude/skills/research-to-strategy skills/research-to-strategy
ln -s /home/shekerk/.claude/skills/ai-strategy-brief skills/ai-strategy-brief
ln -s /home/shekerk/.claude/skills/presales-deal-prep skills/presales-deal-prep
ln -s /home/shekerk/.claude/skills/vertical-scorer skills/vertical-scorer
ln -s /home/shekerk/.claude/skills/workflow-visualizer skills/workflow-visualizer
ln -s /home/shekerk/.claude/skills/graphify skills/graphify
```

## Tier 2: Project-Critical But Budget-Sensitive

These are important, but their trigger surface may be broad or they overlap with active repo skills. Keep archived until the workflow calls for them, or expose only after shortening descriptions.

| Skill | Reason to keep available | Budget concern |
|---|---|---|
| `ai-strategy-researcher` | Useful for deep AI strategy reports. | Overlaps with repo strategy skills and may trigger broadly. |
| `competitive-intel-sprint` | Strong for competitor/demo analysis. | Potentially heavy chain and overlaps with pipeline skills. |
| `ai-use-cases-consultant` | Useful for hyperscaler/use-case consulting. | Broad trigger; overlaps with AI Head of Engineering skills. |
| `ai-transformation` | Useful for maturity/operating-model work. | Broad consulting trigger surface. |
| `architecture-presentation` | Useful for turning architecture into teachable decks. | Overlaps with `drawio`, presentation, and branded deck workflows. |
| `architecture-to-everything` | Potentially useful compound skill. | Broad and likely large. |
| `engagement-management` | Useful for consulting governance. | Workflow-specific, not needed every session. |
| `solution-delivery` | Useful for implementation governance. | Workflow-specific. |
| `continuous-improvement` | Useful post-launch. | Later lifecycle, not default. |
| `contract-reviewer` | High value when needed. | Legal/commercial trigger only. |
| `difficult-conversation-prep` | Useful for comms coaching. | Not core to everyday Codex coding/research. |
| `mkt-brand-voice` | Useful for content/brand output. | Broad writing trigger; expose only if content work dominates. |
| `mkt-visual-identity` | Useful for brand systems. | Design-specific and can overlap with design skills. |
| `explainer-graphic` | Useful for visual explanation. | Overlaps with Excalidraw/Draw.io/visualizer. |

## Tier 3: Presentation Pack

Expose as a pack only when the workflow is presentation-native. These overlap heavily with existing branded PPTX/deck workflows and can add substantial routing noise.

| Skill | Recommendation |
|---|---|
| `presentation` | Keep archived unless HTML/presentation editing is frequent. |
| `presentation-content-writer` | On-demand; overlaps with strategy/deck writing. |
| `presentation-theme` | On-demand for theme swaps. |
| `presentation-exporter` | On-demand for export operations. |
| `presentation-speaker-notes` | On-demand for presenter prep. |
| `presentation-accessibility` | On-demand QA step for accessibility. |
| `marp` | On-demand if Marp remains a common deck format. |
| `openkb-deck-editorial` | Keep archived unless OpenKB deck workflow is active. |
| `openkb-deck-neon` | Keep archived unless OpenKB deck workflow is active. |
| `openkb-html-critic` | Keep archived unless OpenKB deck workflow is active. |

## Tier 4: Browser, Web, And Capture Helpers

These are useful, but many overlap with `playwright-cli`, `web`, Firecrawl, and existing repo search tools.

| Skill | Recommendation |
|---|---|
| `agent-browser` | Consider activating if browser automation beyond Playwright snapshots is frequent. |
| `browse` | Keep archived; Codex already has web/search tools. |
| `archive-is` | On-demand for archive.today/paywall/cache retrieval. |
| `connect-chrome` | On-demand when attaching to a real browser profile. |
| `setup-browser-cookies` | On-demand; sensitive because it touches logged-in browser state. |
| `open-gstack-browser` | Keep archived unless GStack browser workflow is active. |
| `postman-explore` | On-demand API discovery helper. |
| `wikipedia` | Keep archived; use generic web unless Wikipedia workflow is recurring. |

## Tier 5: Review, Guardrails, And Meta-Workflow

Useful for human process and QA, but broad triggers can crowd the skill list. Keep only one or two always-on if needed.

| Skill | Recommendation |
|---|---|
| `grill-me` | Strong candidate if you want systematic pressure-testing before execution. |
| `llm-council` | On-demand for high-stakes decision review. |
| `review` | Keep archived; active `code-reviewer` and review instructions already exist. |
| `code-review-specialist` | Keep archived unless preferred over active `code-reviewer`. |
| `qa` | On-demand; repo has QA patterns already. |
| `qa-only` | On-demand. |
| `guard` | On-demand. |
| `careful` | On-demand. |
| `checkpoint` | On-demand. |
| `freeze` / `unfreeze` | On-demand workflow controls. |
| `health` | On-demand. |
| `retro` | On-demand. |
| `session-handoff` | Consider activating if long sessions are common. |
| `autoplan` | Keep archived unless you prefer it over `goal-loop-orchestrator`. |

## Tier 6: Third-Party Connector Skills

Keep archived unless the corresponding service is actively used and authenticated. These can add many broad triggers and may not be useful without credentials.

| Skill | Recommendation |
|---|---|
| `slack` | On-demand; activate only if Slack CLI/auth is configured. |
| `notion` | On-demand; Codex already has Google/Teams/Drive connectors in this host. |
| `linear` | On-demand for Linear projects. |
| `cal-com` | On-demand scheduling workflow. |
| `google-ads` | On-demand marketing analytics. |
| `dub` | On-demand link management. |
| `substack` | On-demand publishing. |
| `fireflies` | On-demand meeting intelligence. |
| `podscan` | On-demand podcast research. |
| `hackernews` | On-demand HN source monitoring. |
| `trigger-dev` | On-demand Trigger.dev ops. |
| `scrape-creators` | Consider activating if content/reddit/youtube scraping is frequent and credentials are configured. |

## Tier 7: Keep Archived / Low Priority

These appear niche, redundant, demo-like, or ambiguous without more context.

```text
00-account-briefing
affiliate-workflow
analytics-to-comms
benchmark
cal-com
canary
cheat
codex
cso
design-consultation
design-html
design-review
design-shotgun
devex-review
document-release
gstack
gstack-upgrade
investigate
land-and-deploy
landing-page-gen
learn
learn-anything
notebooklm
office-hours
openkb
pair-agent
plan-ceo-review
plan-design-review
plan-devex-review
plan-eng-review
printing-press
setup-deploy
ship
social-media-team
ss
time-skill
time-tokyo
tool-humanizer
weather-fetcher
weather-fetcher-tokyo
```

Some of these may be valuable in Claude Code, but they should not be globally active in Codex unless they support a recurring workflow in this repo.

## Broken Skill Link

`/home/shekerk/.claude/skills/standup/SKILL.md` is a broken symlink:

```text
/home/shekerk/.claude/skills/standup/SKILL.md -> /home/shekerk/.claude/skills/gstack/standup/SKILL.md
```

Recommendation: either repair the target if `standup` is still useful, or remove/archive the broken symlink. Do not expose `standup` to Codex until this is fixed.

## Duplicate/Overlap Findings

The repo currently has duplicate active skill families:

- `skills/ai-head-of-engineering-*`
- `.agents/skills/ai-head-of-engineering-*`
- `skills/storm-research`
- `.agents/skills/storm-research`

Recommendation: keep canonical repo-local `skills/` copies active and move duplicate `.agents/skills` copies out of active discovery if Codex budget pressure returns. Do not delete without checking whether another host depends on `.agents/skills`.

## Suggested Activation Set

If you want one more activation pass after restart, expose only this set:

```text
content-research
drawio
video-to-deck
research-to-deck
research-to-strategy
ai-strategy-brief
presales-deal-prep
vertical-scorer
workflow-visualizer
graphify
```

If budget pressure appears after restart, remove in this order:

1. `graphify`
2. `workflow-visualizer`
3. `vertical-scorer`
4. `research-to-deck`
5. `video-to-deck`

Keep `watch` and `excalidraw` because they are narrow and directly solve the current workflow.

## Video-To-Excalidraw Chain

Recommended chain for the YouTube screenshot recreation workflow:

```text
watch -> frame review -> excalidraw -> screenshot QA -> export
```

Optional richer chain:

```text
watch -> content-research -> research-to-deck/video-to-deck -> excalidraw/drawio -> branded-pptx-deck
```

Use focused `watch` windows for exact screen capture:

```bash
python3 skills/watch/scripts/watch.py "<video-url>" --start 1:20 --end 1:45 --resolution 1024 --max-frames 50
```

## Decision

Do not bulk re-enable all archived skills. Keep the active Codex skill surface small and intentional. The best near-term move is:

1. Restart Codex so `watch` and `excalidraw` load.
2. Test discovery with a prompt containing `/watch <youtube-url>`.
3. If discovery is stable, optionally expose the Tier 1 activation set.
4. If discovery budget warnings return, trim duplicates from `.agents/skills` before adding more archived Claude skills.
