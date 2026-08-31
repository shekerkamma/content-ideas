# content-ideas plugin

A cross-host skill that turns competitor activity into a daily "For You" feed of
content ideas. Runs the same on Claude Code and Codex (and any host that reads
`AGENTS.md`). Dependency-free Python (stdlib only) plus a single self-contained
HTML renderer.

## Structure
- `skills/content-ideas/SKILL.md` — canonical skill definition (the entry point)
- `skills/content-ideas/scripts/scrape.py` — competitor/own-channel scraper
- `skills/content-ideas/scripts/generate_feed.py` — builds the For You HTML feed
- `skills/content-ideas/scripts/lib/` — platform fetchers, scoring, relevance, rendering
- `skills/content-ideas/assets/for-you-template.html` — renderer template
- `skills/content-ideas/references/content-strategy.md` — idea-generation guidance

## Cross-host packaging
- `.claude-plugin/plugin.json` + `marketplace.json` — Claude Code install
- `.codex-plugin/plugin.json` (`"skills": "./skills/"`) — Codex install
- `AGENTS.md` → `@CLAUDE.md` — Codex / generic-agent entry point
- `commands/content-ideas.md` — Claude Code slash command
- `hooks/hooks.json` — SessionStart setup preflight (one-line hint, silent when ready)

### Skill source and porting contract

- Treat `skills/content-ideas/`, `skills/pipeline-runner/`,
  `skills/second-brain/`, `skills/plaid/`,
  `skills/karpathy-guidelines/`, `skills/meta-loop/`, and
  `skills/graph-engineering/` as canonical shared sources.
- Treat `skills/docx/`, `skills/pdf/`, `skills/improve/`, and
  `skills/storm-research/` as canonical shared recovery sources for those
  skills. They must remain portable across Claude Code and Codex and must not
  contain generated Python bytecode or host credentials.
- Keep matching copies under `plugins/content-ideas/skills/` byte-identical.
- `skills/meta-loop/` runs Claude Code Opus as the sole aggregator and isolated
  Codex CLI models as workers; keep its host installations synchronized with
  the canonical repo copy and never place credentials in worker briefs.
- Keep Claude-only UI fields as enhancements; repeat critical safety and
  fallback behavior in skill bodies for Codex and OpenHands.
- Before shipping skill changes, run the plugin contract, the three
  `skill-builder` audit scripts, and the full pytest suite.

### `.agents/skills/` is the one tree all three hosts already read

Reaching Claude Code, Codex, and DeepSeek Harness does not need a third
packaging format. DSH's `@deepseek-ai/dsh-skill-filesystem` resolves five roots
in rank order, and **rank 200 is `<projectRoot>/.agents/skills`** — a tree this
repo already maintains. Measured 2026-08-25 by driving the provider directly
against this checkout; it returned 61 skills with descriptions parsed.

So a cross-host skill is `skills/<name>/` plus a byte-identical copy in
`.agents/skills/<name>/`, which `check_skills.py --rule crosstree` already
enforces. Four constraints come from DSH and bind the canonical copy too:

- **Single-level bundles only.** `<name>/SKILL.md` or a flat `<name>.md`.
  Nested `**/SKILL.md` discovery is deliberately excluded, so a skill cannot
  hide sub-skills in subdirectories.
- **`name` must be kebab-case and `description` must be top-level.** Both are
  required; DSH parses frontmatter as open YAML with the `yaml` package.
- **`disable-model-invocation` / `user-invocable` fail closed.** A camel-case
  spelling or a non-boolean value **drops the entire skill** from discovery with
  a warning — it does not fall back to permissive. This is why commit
  `7f3d602`'s move of `user-invocable` under `metadata.legacy-frontmatter:` is
  safe: DSH treats `metadata` as an opaque object and defaults to permitting.
- **Project root is the nearest ancestor containing `.git`.** A skill tree
  outside the repo is invisible to the project-scoped roots.

`~/.dsh/skills` (rank 400) and `~/.agents/skills` (rank 500) are the user-scope
equivalents for skills that should follow the machine rather than the repo.

### Evidence-ranking rules for research-bearing skills

Any skill that recommends a tool, vendor, library, stack, or comparable
project carries an editable `## Judgment rules` section stating these three.
Keep the policy on the page and tunable — never hardcode it into step
instructions. Currently applied in `skills/plaid/SKILL.md`,
`skills/graph-engineering/SKILL.md`, `skills/design-tokens/SKILL.md`, and
`.claude/skills/saas-replacement-auditor/SKILL.md`; extend to
`ai-head-of-engineering-build-vs-buy-auditor`, `ai-head-of-engineering-stack-picker`,
and `investor-competitive-dossier` when they are next touched.

- **Popularity is not fit.** Never rank options by GitHub stars, download
  counts, or social popularity alone. Stars are a bookmark count that only
  increases: they record that people liked something once, not that it fits
  this problem. Rank on fit to stated constraints, then on maintenance
  signals carrying an exact date. This is the same failure the
  `last30days` skill deliberately inverts — that skill treats stars as a
  trend signal on purpose, and is the one documented exception.
- **Split every comparable in two: what transfers, and what exists only
  because that project got big.** A mature project's plugin system,
  multi-tenancy, or infrastructure reflects its team size, scale, and
  deployment history — not ours. Copying the second half imports complexity
  without the reasons for it, and sizing a build against it inflates cost
  estimates until sound candidates fail. State which half each
  recommendation rests on.
- **Cost every vendor at three points, not one:** during build with zero
  users, the first day real users arrive, and at 10x that. "Free to start"
  is not "cheap to operate." A per-seat or per-active-user price invisible
  in month one is a roadmap constraint by month six; a tool inside a free
  tier today becomes a replacement candidate the month it crosses the cap.
  Name the cap and the crossing point, not just today's invoice.

Adapted from `AaravKashyap12/advise-project-approach` (MIT) rather than
installed — this repo already owns that workflow four times over in `plaid`,
`saas-replacement-auditor`, `ai-head-of-engineering-build-vs-buy-auditor`,
and `deep-research`, and that skill does external research without honoring
the global Research Tool Order.

## Channel-to-KB skills (ported from coleam00/cole-medin-knowledge-base)

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

## Shared Product-Build Skills
- `skills/graph-engineering/SKILL.md` — builder/critic contract loop: state on
  disk, an adversarial auditor subagent with no write access, a frozen
  negotiated contract, and a real verification command. Scripts scaffold and
  gate the loop (`init_loop.py`, `check_contract.py`, `verify_state.py`,
  `collate_traces.py`). Distinct from `meta-loop` (multi-model council) and
  `goal-loop-orchestrator` (skill-chain planner). Two invariants are
  load-bearing and must survive any edit: the critic never receives the
  builder's transcript or reasoning, and the critic never gets write tools.
- `skills/plaid/SKILL.md` — Product Led AI Development: idea, validation,
  planning, `docs/design.md`, launch, and roadmap execution.
- `skills/karpathy-guidelines/SKILL.md` — coding guardrails: think before
  coding, keep solutions minimal, edit surgically, and verify success criteria.
- `skills/video-to-skill/SKILL.md` — derive a runnable skill from a public video
  URL that demonstrates a workflow. The Claude Code analogue of Cowork's
  record-a-skill, with the input swapped: a published video instead of your own
  screen recording. Scripts scaffold, capture, and gate
  (`init_skill.py`, `hyperframes.py`, `check_derived_skill.py`); enforced by
  `tests/test_video_to_skill.py`. Peer of `video-to-deck` (same input, deck
  output) and `skill-builder` (same output, written-spec input). Lives in
  `skills/` only — like `video-to-deck`, it is not one of the seven canonical
  skills mirrored into `plugins/content-ideas/skills/`, and `.codex-plugin`'s
  `"skills": "./skills/"` already exposes it to Codex.

### `claudex-loop` is installed, not vendored — and three repo rules bind it

`chaseai-yt/claudex-loop` (MIT) is installed as a user-scope plugin, not adapted
into a skill tree: `/claudex-loop:claudex-loop`, `:codex-review`, `:codex-build`.
Installing rather than forking is deliberate, and the reasoning inverts the
`design-tokens` and `advise-project-approach` precedents above. It ships 3 skills
and **zero** agents, hooks, or MCP servers, so it makes no claim on this repo's
instruction surface — the disqualifier that forced adaptation for
`ux-ui-agent-skills`. And its load-bearing half is codex CLI invocation mechanics,
whose failure mode is silent *and* a security failure (see the resume/sandbox
finding above) and whose flag surface moves between CLI releases. That is the
worst possible thing to vendor; upstream is the right owner and the marketplace
auto-updates.

What it adds that this repo does not already own is a **persistent adversarial
session**: Codex resumes one thread across rounds, so it attacks its own accepted
fixes. Route by critic identity, not by shape — `codex-worker-loop` also runs
Claude-plans/Codex-builds, but its critic is a second Opus instance (same vendor,
same family); `graph-engineering` scaffolds a harness for a repeated job and its
critic guarantee is strictly stronger (never sees the builder's transcript, never
gets write tools); `meta-loop` is a council, not a two-model argument.

The skill carries no `## Source / Tool Order` and no `## Judgment rules`, so three
repo-global rules govern it unchanged and must be honored by whoever runs it:

- **Research Tool Order applies to Phase 0 without exception.** Its research gate
  reaches for WebSearch and a deep-research workflow; GBrain recall comes first,
  then Exa, then Firecrawl, and WebSearch is never the first move.
- **Phase 0 greenfield recon recommends a stack**, which puts it squarely inside
  the evidence-ranking rules above: popularity is not fit, split every comparable
  into what transfers versus what exists only because that project got big, and
  cost every vendor at three points.
- **Its `deep` tier hardcodes `model: 'opus'`** on every research `agent()` call.
  Defensible as a downgrade from Fable for search-and-summarize work, but it is a
  model policy baked into steps rather than stated on the page and tunable — treat
  a change to it as a policy decision, not a drive-by edit.

`PLAN.md` and `PLAN-REVIEW-LOG.md` are written deliverables, so `voice.md` applies
to both.

### Deriving from video: three findings that are silent when wrong

These cost a full re-derivation each. They generalize past this skill to any
frame-based work, including `video-to-deck` and `watch` itself.

- **`watch`'s default download can be 360p and nothing errors.** Under
  YouTube's SABR restriction yt-dlp may only offer format 18 (640x360), at
  which terminal text and code diffs are unreadable — and raising
  `--resolution` merely upscales blur at 4x the token cost. Check
  `frames.get_metadata()["width"]` before reading frames; recover the format
  ladder with `--extractor-args "youtube:player_client=default,mweb,web_embedded"`.
- **`--detail token-burner` is not dense on screencasts.** It is uncapped but
  still gates on `SCENE_THRESHOLD = 0.20`, tuned for filmed video with cuts. A
  screencast changes one pane while chrome, editor, and webcam hold still.
  Measured on a 61-minute tutorial: 86 frames with a **7m10s** blind spot,
  versus 470 frames with a 39s worst gap at threshold 0.10 plus gap fill. The
  threshold is a module constant with no CLI flag, which is why
  `hyperframes.py` exists. Note `video-to-deck` references a
  `--detail scene-complete` mode that **does not exist** in the installed
  `watch`; `hyperframes.py` is the working equivalent.
- **Auto-captions are unreliable for anything typed.** They rendered
  `/overview` as "slashoverview" and omitted seven commands entirely. Read
  every command, path, flag, and filename off a frame.
- **`--detail transcript` is not an analysis of a screencast — it is a
  transcript of someone talking over one.** A deck built from captions alone
  reads as thin because it is: measured on a 12-minute `/design` walkthrough,
  the captions carried roughly a sixth of the substance. The narration is
  deixis without referents ("this right here", "you'll see this panel") while
  the screen holds the file names, line counts, version ids, hex values and
  debug readouts. Twelve targeted 1080p frames beat 212 caption segments.
  Use `transcript` to *find* the moments, then re-run for frames at them —
  never as the only pass when the deliverable is about what a tool does.

**A derived skill is a hypothesis until executed.** `check_derived_skill.py`
fails without an execution record in `## Verification`; `NOT EXECUTED` plus
`--allow-unexecuted` downgrades it to a warning that stays in the file. This
rule was added after execution falsified four claims in a skill that had already
passed every other gate — including the demonstrator's own narration about which
command cuts the git branch. Ranking when sources disagree: **execution, then
on-screen text, then narration.**

## Presentation system

- `skills/present/SKILL.md` is the single public router for presentation work.
- Keep output engines distinct: native PPTX uses `branded-pptx-deck`, controlled
  existing-PPTX edits use `pptx-toolkit`, HTML uses `presentation`, hosted Genspark uses
  `genspark-slides` plus `genspark-branded-deck`, and Markdown slides use `marp`.
- **A client-ready deck is built with `vault-presales-pptx-pipeline` and
  artifact-tool presentation JSX — not with `pptxkit`/python-pptx.** `pptxkit`
  is the correct builder for `branded-pptx-deck` and it validates cleanly, so a
  hand-rolled deck looks finished and passes every structural gate while
  missing the method entirely. Three decks were built the wrong way in one
  session before the routing was followed; the tell is hand-written layout
  helpers instead of `deck-kit.mjs`'s `card`/`kpi`/`table`/`chain`/`rail`, and
  fixed card heights instead of `'auto'`.
- Keep template profiles and slide archetypes inside `pptx-design-quality`; do not create
  another top-level presentation skill for each template, layout, critic, or adapter.
- Keep acquisition utilities inside `presentation-source-bundle`; web/PDF/OneDrive intake
  is evidence normalization, not a presentation renderer.
- When a reference deck exists, draft `template-profile.json` and `slide-plan.json` from it
  instead of hand-authoring from the blank template: `pptx-design-quality/scripts/
  derive_template_profile.py` (brand colors, fonts, geometry) and `pptx-visual-spec/
  scripts/draft_slide_plan.py` (per-slide archetype and evidence links). Both write a
  distinctly named draft only — never the canonical contract file — and still require
  tailoring plus the normal validators before build. Adapted from analyzing
  `pamelafox/presentation-skills`'s ingestion skills against this repo's contract-owning
  skills, not ported 1:1; see `skills/pptx-design-quality/references/template-derivation.md`.
- `/design` (Claude Code's built-in design-canvas skill) feeds that same seam and stops
  there: `derive_template_profile.py --canvas <canvas-dir>` reads a canvas working tree
  (`canvas.json` plus `*.dc.html`) into a draft profile. It is the only input that derives
  `geometry.grid_columns`, `geometry.gutter_inches`, and `composition.corner_radius`,
  which the `.pptx` and evidence inputs document as underivable. Three rules keep it in
  its lane:
  - **A canvas is a design-contract input, never an output engine.** It emits `.dc.html`
    plus a hosted artifact, and its PDF export rasterizes each artboard to one page, so
    it can no more deliver a client deck than `genspark-branded-deck` can. Client-facing
    PPTX still comes from `BRANDED_PPTX_TEMPLATE` / `branded-pptx-deck`. Do not add
    `/design` to the `present` router.
  - **Never let a canvas source evidence.** Geometry, type, and brand only; claims and
    numbers stay with `presentation-evidence.json` and `check_claim_evidence.py`. A
    profile derived from a canvas you drew is already a measurement of your own intent.
  - **The px scale is derived from the artboard frame, never hardcoded.** A canvas is
    authored in CSS px and a slide renders on a fixed-inch stage, so
    `pt = px * (slide_width_inches / frame_width_px) * 72`. That is 0.75pt/px at a
    1280x720 artboard — the vault pipeline's own stage (`deck-kit.mjs`:
    `setViewportSize(1280, 720)` = 13.333 x 7.5in) — and 0.5 at 1920x1080. Hardcoding
    0.75 is the same misread that the points-vs-pixels rule already exists to prevent;
    `tests/test_derive_from_canvas.py` pins both frame widths so it cannot creep back.
- For an evidence-derived deck, run `pptx-design-quality/scripts/check_claim_evidence.py`
  as a fast mechanical pre-pass (unsourced-number scan against cited evidence) before the
  richer `video-to-deck` Grill-Me or Genspark factual-integrity review; it does not replace
  either.
- Impeccable (`pbakaus/impeccable`, MIT... Apache 2.0) is installed for the HTML-based
  surfaces only: `.claude/skills/impeccable/`, `.agents/skills/impeccable/`, and
  `.github/skills/impeccable/` (one copy per detected harness, installed via
  `npx impeccable skills install`; hooks wired into `.claude/settings.local.json`
  (gitignored, machine-local), `.codex/hooks.json`, and `.github/hooks/impeccable.json`).
  It does not understand native `.pptx` — never install or invoke it as a substitute for
  `pptx-design-quality/scripts/lint_pptx.py`, which already covers the PPTX-native
  equivalent checks (overflow, overlap, contrast, font/color-count caps, DPI, layout
  repetition) with its own `qa.ignore_rules`/`qa.waivers` waiver mechanism.
  `scripts/design-qa-detect.sh` is the pinned wrapper (`impeccable@3.5.0`, requires
  Node >= 24) that `marp` and `genspark-branded-deck` run against authored HTML before
  PPTX export; bump the pin there and in this file together when upgrading.

### `deck-kit.mjs` reads the design system's points as pixels

The Client-Ready PPTX Design System is written in **points**; artifact-tool works in
**pixels** at 1px = 0.75pt. `assets/deck-kit.mjs` in `vault-presales-pptx-pipeline`
sets its type in pixels but uses the spec's point numbers as those pixel values:

| Role | Spec pt | Spec px | Kit px | Actually renders |
|---|---|---|---|---|
| Slide title | 24–30 | 32–40 | 30 | **22.5pt** |
| Body | 12–14 | 16–19 | 13 | **9.75pt** |
| Card heading | 12–16 | 16–21 | 15 | **11.25pt** |
| Kicker | 8–10 | 11–13 | 10 | **7.5pt** |
| Footer | 7–8 | 9–11 | 9 | **6.75pt** |

Every role lands under floor, so **every deck built from the kit renders about a
quarter too small** — which reads as bland and thin no matter how good the words are.
This is the exact trap the kit's own build reference documents.

`runs/2026-08-22-design-video-brief/kit-spec.mjs` is a working correction: it keeps the
kit's geometry and primitives and re-cuts `header`/`footer`/`card`/`kpi`/`table`/`chain`/
`rail` at `PX(pt) = pt / 0.75`. Effect on `lint_pptx.py` for the same deck:
`TEXT_TOO_SMALL` 33 → 0, `SLIDE_MISSING_TITLE` 8 → 1 (the linter needs ≥24pt to
recognise a title at all), total warnings 70 → 29.

**The fix belongs upstream** in the vault canonical
(`hyundai-ai-vault/.agents/skills/vault-presales-pptx-pipeline/assets/deck-kit.mjs`),
which is outside this repo and symlinked into four host roots — changing it moves every
future deck, so it needs a deliberate decision rather than a drive-by edit. Until then,
import `kit-spec.mjs` alongside the kit.

### `lint_pptx.py` cannot see a box too short for one line

`lint_pptx.py` and `preview_pptx.py` disagree on overflow, and the linter is the weaker
of the two:

```
lint:    available_lines = max(1, int(height / line_height))
preview: overflow = total_h > h + 0.03
```

That `max(1, …)` floors the available height at one line, so a box with room for **zero**
lines scores as having room for one. Four shapes needing 0.22in in a 0.11in box passed
lint clean and were plainly broken on the render.
`runs/2026-08-22-design-video-brief/overflow_scan.py` replicates the preview rule
headlessly so the gap is findable without reading images. Run both gates; a clean
`lint_pptx.py` is not evidence that text fits. Adopting the preview comparison inside
`lint_pptx.py` would newly flag existing decks, so it is a gate-semantics decision, not a
bug fix.

### Both text gates measure artifact-tool decks at 14pt, because the size is not on the run

`lint_pptx.py` and `preview_pptx.py` both resolve a paragraph's size with
`para.runs[0].font.size` and fall back to **14pt** when it is `None`. artifact-tool
writes the size to the paragraph's `a:defRPr` and emits `<a:r>` with no `<a:rPr>`, so
that fallback fires on **every** paragraph — measured 941/941 on a 30-slide deck. The
consequence runs both ways: 9.75pt labels are over-measured (phantom overflow) and a
44pt cover headline is under-measured (real overflow missed).

The visible symptom is a contact sheet covered in red overflow boxes on a deck that is
actually clean. On one build the raw count was **164 "overflowing" shapes; resolving
`defRPr` first brought it to 24**, and those 24 were real.

`skills/pptx-design-quality/scripts/overflow_scan.py` and `preview_pptx_fixed.py`
are the corrected copies — same wrap width, same 1.18 line
stacking, same 0.03in tolerance, only the size resolution changed. Use them for any
artifact-tool deck. Do **not** read red boxes off the stock `preview_pptx.py` for these
decks; it is rendering the whole deck at one font size.

Related: `lint_pptx.py`'s `TEXT_TOO_SMALL` enforces a flat 14pt floor, but the design
system specifies body 12–14pt, table/chart labels 9–11pt, kicker 8–10pt and footer
7–8pt. A deck that is correct against the contract fires hundreds of these. Waive the
rule with a documented reason; do not inflate the type to satisfy a linter that is
stricter than the spec it enforces.

### Text hidden behind a later opaque shape — the defect class no gate owned

Draw order matters: a card or table band drawn *after* a footer, page number, or chart
axis label covers it completely. The slide is not overlapping by any text-vs-text test
and it is inside the canvas, so `SHAPE_OUT_OF_BOUNDS` and `TEXT_BOX_OVERLAP` both pass.
**OfficeCLI catches it** (`Text "02" is hidden behind overlapping shape …`) and was the
only gate that did.

Building the check is where the lesson is. The first version gated its occluder scan on
finding `spPr/solidFill/srgbClr`, that XPath matched nothing, and it reported **0
occlusions on a deck where OfficeCLI reported 15** — a gate that goes green because it
measured nothing. Treat any no-text drawn shape as an occluder rather than trying to
prove it has a fill. Fixed, it reported exactly 15 and agreed with OfficeCLI.
`skills/pptx-design-quality/scripts/verify_deck.py` carries all three checks (bounds,
text collision, occlusion) plus background-aware WCAG contrast. Set
`DECK_DARK_SLIDES=1,6,12` so it resolves contrast against dark backgrounds correctly.

### Two header defects that the kit produces silently

- **A long title drops below the design system's 24pt floor.** `kit-spec.mjs`'s
  `header()` steps the size down when a title exceeds ~60 characters, landing at
  21.75pt — under the 24–30pt spec, and under the size `lint_pptx.py` needs to
  recognise a title at all (which is why 13 slides reported `SLIDE_MISSING_TITLE`).
  Titles must fit one line at full size: **~52 characters at 1160px**.
- **A subtitle over ~105 characters wraps into the rule beneath it.** The band between
  the subtitle at y=106 and the rule at y=146 holds one line at 12.75pt.

Both are assertable at build time. Add the checks to the builder rather than catching
them on a contact sheet: have `hdr()` push to a `VIOLATIONS` list, alongside a
measured-flow layout guard that fails the build when any block runs past the footer.

### Measured flow beats hand-typed y coordinates

The 66 layout errors in that build had one cause: lower-half blocks placed at a
hand-typed `y` while their cards were `'auto'` height. The fix is a `flow(startY, tag,
limit)` helper that stacks blocks by measured height and records a violation when the
running `y` passes the footer or a declared ceiling. Card copy then has to earn its
space, which is the correct pressure. Do not chase these one at a time on renders.

### Animated slides: motion is invisible to every resting-frame gate

`lint_pptx.py`, `preview_pptx.py` contact sheets, and OfficeCLI render QA all inspect
resting frames, so none of them can see a transition or a build. Two gates in
`pptx-design-quality` cover that blind spot, and both are opt-in: a `deck-design.json`
with no `motion` block is unaffected.

- `scripts/lint_motion.py` — contract gate. Reads transition and `<p:timing>` XML
  straight out of the package, deliberately **not** via `officecli`, so the check is
  independent of the tool that authored the motion. Stdlib only.
- `scripts/motion_contact_sheet.py` — render gate. Drives PowerPoint's own
  `CreateVideo`, samples the result, and tiles it. `--from-video` rebuilds the sheet
  without re-exporting; `--preflight-only` checks the environment.
- `MOTION_EXIT_BREAKS_REST_STATE` is an error, not a warning, and is therefore not
  waivable. Content that exits is absent from the resting frame, so it is missing from
  PDF export, contact sheets, and render QA. **Design animated slides so the final
  resting state is the complete slide** — that is what keeps motion compatible with the
  existing delivery gate instead of weakening it. Allow exits deliberately via
  `motion.allowed_effect_classes`, never by waiver.

### Planning motion: derive it from the deck's own geometry

`officecli query <deck> shape --json` returns every shape in the package with a
**stable `@id` path** plus resolved geometry, in one call (3,259 shapes on an
81-slide deck). That is enough to plan a whole build order without python-pptx,
without tagging anything at build time, and without the plan going stale when
the deck is rebuilt. `pptx-design-quality/scripts/plan_motion.py` and
`apply_motion.py` are the pair: geometry in, `officecli batch` commands out.

**One perceived step per BAND, not per column.** Cluster shapes into bands by
`y`, then into columns by horizontal overlap. Inside a band every shape is
`withPrevious` and the left-to-right stagger comes from `delay` (~110 ms per
column), never from `trigger`. A four-card row is then one click and one
motion; a seven-column signal chain runs across 770 ms as a single step. Both
wrong answers cost a cycle: a trigger per column blows the step budget on every
content slide, and collapsing bands to fix the count destroys exactly the
left-to-right motion that was the point.

**`max_build_steps_per_slide` counts nodes, not steps.** `lint_motion.py`'s
`_build_steps` appends one entry per `cTn` carrying a `presetClass` — one entry
per animated *shape*. On a dense deck the two readings differ by an order of
magnitude: 487 perceived steps against 2,602 nodes, with the densest slide at
5 steps and 120 nodes. So the cap is a node ceiling; set it as one, record the
reason **in the config file**, and keep the real click budget upstream in the
planner. Raising a cap because a gate went red, without saying which quantity
it now measures, is how a gate stops measuring anything.

### Narrating an embedded clip, and why the sim's own audio is rarely enough

`recordVideo` in Playwright captures **video only** — the `.webm` has no audio
stream at all. Muxing an `anullsrc` track afterwards then makes a silent capture
look deliberate, and a `volume: 0` default hides it completely. Author narration
and mux it in instead; the page's own audio is a bonus, not the plan.

- **Gemini TTS is the free good-quality route here.** `gemini-3.1-flash-tts-preview`
  (also `gemini-2.5-flash-preview-tts`) on the AI Studio key returns 24 kHz mono
  PCM in `inlineData`; wrap it as WAV. Voice `Charon` matches an informative,
  low-pitch register. Send the text alone — a style instruction in the prompt
  risks being vocalised.
- **A ChatGPT subscription cannot drive OpenAI TTS.** `/v1/audio/speech` bills
  against API credits only, and Codex CLI — the one route that does use
  subscription auth — exposes no audio surface at all (`image_gen` only).
- **Windows SAPI is the offline fallback**: `System.Speech.Synthesis` via
  PowerShell, voices "Microsoft David/Zira Desktop", free and deterministic,
  but a dated concatenative voice.
- Size the narration to the clip and hold the last frame
  (`tpad=stop_mode=clone`) when it runs a little long, rather than cutting the
  writing to fit.

### Capturing a page's own audio on WSLg

- **Record `RDPSink.monitor`, never `default`.** The default source is
  `RDPSource` — the *microphone*. It records room noise, which measures as
  healthy signal (peak 2,818 with nothing playing) and reads as success.
  `ffmpeg -sources pulse` lists both.
- **Chromium needs `--enable-speech-dispatcher` for `speechSynthesis`.** Without
  it, `speak()` is silently inert. Proven with a three-way control: flag+speak
  produced peak 32,768, flag without speak produced 0, speak without flag
  produced 0.
- **`speechSynthesis.getVoices()` returning 0 does not mean speech is
  unavailable.** With the flag set it still reported an empty list while
  speaking perfectly. Test by speaking and measuring, never by counting voices.
- **Web Audio needs a TRUSTED gesture.** `page.mouse.click()` goes through CDP
  Input and unlocks it; an in-page `el.click()` does not, so a capture driven
  entirely by scripted clicks records silence. This is the cost of the DOM-click
  workaround used to get past overlays — pay it once with a real click first.
- **`x11grab` is useless under WSLg** — it returns pure black, because the
  compositor never puts window content on the X root. Use Playwright video plus
  a separate monitor recording, and align them with an explicit marker: flash a
  white full-screen div and fire a 1 kHz beep in the same tick, then mux at the
  measured flash-to-beep offset. Measured 5.21 s here, and verified afterwards
  at 0.00 s drift.

### Embedding a live HTML demo in a deck: the seat is declared, not guessed

A browser-based simulator can ship inside a client `.pptx` as a playable clip.
`officecli add <deck> /slide[N] --type media` takes `src`, `poster`, geometry,
`autoPlay`, `loop` and `trim`, so the deck stays native and the demo travels
with it. `pptx-design-quality/scripts/capture_html_sim.mjs` records the page,
`attach_media.py` places the clip.

- **Have the builder write the seat.** It emits `<deck>-video-seats.json` naming
  the rect it left empty behind each frame; `attach_media.py` fills it and
  `plan_motion.py` *excludes* it. An embedded clip has no build, so anything
  animating underneath wipes in behind something already on screen. One file,
  two readers, and the clip lands inside its frame rather than near it.
- **Order is media, then motion.** The motion plan comes from a shape query, so
  it has to see the final slide.
- **Click through the DOM.** These consoles paint confidentiality watermarks and
  intro panels that intercept pointer events, so `page.click()` times out on a
  button that is perfectly clickable from script. Use
  `page.evaluate(s => document.querySelector(s).click())` — same failure as the
  Google survey iframe in the Vids lane.
- **Re-encode to H.264 + a silent AAC track.** Playwright records VP8 in WebM,
  which PowerPoint accepts and then renders as a black rectangle.
- **Video parts land at top-level `media/mediadata*.mp4`, not `ppt/media/`.** A
  check filtering on `'/media/' in name` reported **0 mp4s on a deck holding
  four**; the file having grown 0.55 MB → 20.8 MB is what said the check was
  wrong rather than the deck. Verify by listing the largest parts, not by
  matching a path you assumed.

### A text box sized to its own estimator still overflows

A card helper that computed its height as `TH(text, w-52)` while placing the
text box at width `w-72` under-measured every string near a wrap boundary: 23
shapes overflowed on a deck whose build-time layout guard reported clean,
because the guard and the box were asking different questions. Measure at the
**box's** width, then pad for the ~0.1in side insets PPTX adds and the
estimator does not model. Same class as the `defRPr` trap above: two gates
agreeing means nothing when both inherit the same wrong number.

### Authoring motion: four silent failures, each costing a full debug cycle

- **`officecli` only persists writes to Windows-side paths.** Given a WSL path it prints
  `Updated /slide[1]: transition=morph`, `close` reports `Resident closed`, and its own
  `query` reads the change back — while the file on disk stays **byte-identical md5**. A
  control property (`name=`) fails the same way, so it is every write, not transitions.
  Run it against `C:\...` and verify with `lint_motion.py`, never with `officecli get`:
  its reads see the resident's memory, not the artifact.
- **PowerPoint is a single-instance COM server.** `New-Object -ComObject
  PowerPoint.Application` attaches to whatever instance is already running. One degraded
  window — long-running, or titled "(Unlicensed Product)" — makes every call fail with
  `0x80048240`, and a WMI licence table will happily corroborate the wrong conclusion.
  Close PowerPoint and retry against a fresh instance before blaming activation.
- **PowerPoint cannot open a WSL path, and a relative path is worse than a wrong one.**
  `wslpath -w` maps a relative path to a relative Windows path, which PowerPoint resolves
  against its own cwd — under WSL a `\\wsl.localhost\...` UNC path — failing as an opaque
  `E_FAIL`. Resolve to absolute first; stage WSL-hosted decks into a Windows temp dir.
- **`SlideShowSettings.Run()` fails from a minimized window** with the same
  `0x80048240`, which reads as a permissions problem and is not. Maximize and foreground
  first, or skip COM entirely and launch `POWERPNT.EXE /S <deck>`.

**Morph matches objects across slides by shape name.** Give the shapes that should travel
stable names on every slide; rename one and morph silently degrades to a fade. Verify a
morph by measuring intermediate positions in the rendered MP4 — positions that exist on no
slide are the tween, and that measurement is the only proof that is not eyeballing.

### `codex exec` hangs on an inherited stdin

`codex exec` reads stdin when it is not a TTY. A bridge that passes its prompt as
**argv** never writes to or closes that stream, so the call blocks for the entire
timeout and returns **no output and no error** — indistinguishable from a slow model.
Measured 2026-08-23, same command and model, only stdin varying:

| stdin | Result |
|---|---|
| inherited (open pipe) | **hangs** — timed out at 86.5s |
| `subprocess.DEVNULL` | completes in 8.7s, rc=0 |

The tell is how the prompt is delivered. Bridges that pipe it in — `meta-loop`,
`codex-worker-loop`, `impeccable`, `scripts/codex_cli_bridge.py` — append `-` and
call `communicate(brief)`, which closes stdin as a side effect and is safe by
construction. The two that pass the prompt as argv are exactly the two that forgot
stdin existed: `skills/video-to-deck/scripts/generate_with_codex_cli.py` and
`ai-graphics`'s `codex_image.py`. Both now pass `stdin=subprocess.DEVNULL`. Audit any
new codex bridge on that axis before its first long-running use.

**Codex model ids: test the exact id, never the family name.** `gpt-5.6-sol` works on
ChatGPT-subscription auth including built-in `image_gen`; bare `gpt-5.6` returns
`400 not supported when using Codex with a ChatGPT account`. A bogus id returns the
same 400, which is what makes `-m` a validated flag and a passing run real evidence.
`ai-graphics` previously generalised the bare-`gpt-5.6` failure into "gpt-5.6 does not
exist upstream"; that note was believed and cost a full detour into paid image
providers before the live catalog was checked.

### `codex exec resume` inherits `danger-full-access` and has no `-s` to stop it

`~/.codex/config.toml` on this machine sets top-level `approval_policy = "never"`
and `sandbox_mode = "danger-full-access"`. `codex exec` accepts `-s read-only`;
**`codex exec resume` does not accept `-s` at all** (codex-cli 0.148.0 — its
options are `-c`, `-m`, `-i`, `--json`, `-o`, `--last`, `--all`,
`--enable/--disable`, `--ephemeral`, `--strict-config`, `--skip-git-repo-check`,
`--ignore-rules`, `--ignore-user-config`, `--dangerously-bypass-*`). So a resumed
"read-only review" session silently inherits write access unless the call carries
`-c sandbox_mode="read-only"`.

Measured 2026-08-25 in a throwaway git repo, one thread, only the flag varying:

| call | result |
|---|---|
| `codex exec -s read-only` | `VERDICT: BLOCKED`, nothing written |
| `codex exec resume <tid> -c sandbox_mode="read-only"` | `VERDICT: BLOCKED`, nothing written |
| `codex exec resume <tid>` (no flag) | **`VERDICT: WROTE`** — file created on disk |

Omitting the flag does not degrade to a stricter default; it hands a critic that
is supposed to be reading your repo the ability to edit it. Every resume in a
review loop must carry it, and the no-flag negative control above is the only
thing that proves the flag is live — a passing read-only round on its own is
equally consistent with the flag doing nothing. Audit any codex bridge on this
axis alongside the stdin axis above.

## Design tokens and WCAG render gates

`skills/design-tokens/` is the token contract and the only place in this repo that
measures a rendered page against named WCAG 2.2 criteria. Two commands, two
different claims, and they are not interchangeable:

- `scripts/check.sh` — stdlib Python, no browser. The token JSON parses, aliases
  resolve, the six required contrast pairs pass in light *and* dark, every
  `var(--x)` resolves to the theme, and no component hardcodes a hex or px. A
  clean run says nothing about how anything renders.
- `scripts/run_gates.sh <page.html>` — opens the page in Chromium and runs ten
  gates (1.4.3, 1.4.10, 1.4.11, 2.1.1, 2.1.2, 2.3.3, 2.4.3, 2.5.8, axe-core
  A/AA, RTL). Exit **0** clean, **1** blocked, **2** findings.

Adapted from `plugin87/ux-ui-agent-skills` v2.5.2 (MIT) rather than installed —
its 17 skills collide with `design-review` and `prototype` and land on a surface
already held by `impeccable`, `refero-design`, `frontend-ui-engineering`, and
`design-html`, and its `CLAUDE.md`/`.claude/rules/` layer wants to own the host
repo's instruction surface (`validate_instruction_surface.py` enforces a 320-line
budget). Full accounting in `skills/design-tokens/references/provenance.md`. The
138-system reference corpus went to `skills/refero-design/references/design-systems/`,
where reference corpora belong.

### A gate that skips is not a gate that passes

Every render gate upstream opened with
`catch { console.log('… — SKIPPED'); process.exit(0); }`. Upstream CI installs
Chromium in a dedicated job so it never bites there; **`npm test` upstream
contains no render gate at all**, so running the suite locally reports green over
a page nothing opened. Three changes make that impossible here, and
`tests/test_design_tokens.py` asserts all three statically so they cannot creep
back:

- A missing Playwright, browser, target, or axe-core is `BLOCKED` on stderr with
  exit 1, and `run_gates.sh` calls the page UNMEASURED. No `process.exit(0)` may
  appear before the browser opens.
- Exit 1 means blocked and only blocked; findings are exit 2 (matching
  `scripts/design-qa-detect.sh`).
- axe-core loads from the local install only. Upstream's CDN fallback lets one
  gate's rule set differ between two runs.

`assets/fixtures/broken/` is the negative control — six of nine gates fire on it
by construction, each defect commented against its criterion. A clean run on a
clean fixture is not evidence the gates work; that fixture is.

**`verify_keyboard.mjs` had to be fixed before it could be trusted.** Its
collection loop read `if (!vis(el) || !operable(el) || !tabbable(el)) continue;`
— so a `role="button"` div with no `tabindex`, the plainest WCAG 2.1.1 failure
and the one its own "Fix A" text describes, was filtered out of the population
rather than reported. It measured "of the controls already reachable, do they
answer Enter/Space". Now emits `[A0 not-in-tab-order]`.

**`DESIGN_TOKENS_CHROMIUM`** covers the Playwright-build mismatch this machine
has (installed Playwright expects build 1228; the cache holds 1208 and 1234):
`auto` picks the newest cached build and prints which one served the run,
`<path>` pins one and checks it exists first — `executablePath` is accepted
without verification, so a path that is set is not a path that resolves.

## Local PDF service (Stirling PDF)

A self-hosted PDF operations service on `http://localhost:8090` — merge, split,
OCR, redact, compress, convert — for any skill that must not ship a client
document to a third-party web tool. 259 REST endpoints behind 60 UI tools.
Runbook, licensing boundary, and host quirks: `docs/stirling-pdf-local-service.md`.

Lives at `~/apps/stirling-pdf/` (machine-local service, not a repo artifact);
`./stirling {up|down|logs|status|update|open}` and `smoke_test.py` sit beside it.
Three facts bind anyone wiring a skill to it:

- **Set the multipart part's `Content-Type` explicitly.** `/api/v1/convert/pdf/word`
  rejects `application/octet-stream` with a bare HTTP 400, a zero-byte body, and
  nothing in the server log; it wants `application/pdf`. `curl -F` guesses the
  right type from the extension, so the same request succeeds from a shell and
  fails from a hand-rolled client — which reads as a flaky endpoint and is not.
- **The OpenAPI spec is `/v1/api-docs`, not `/v3/api-docs`.** The SPA serves
  `index.html` for unknown paths, so a wrong path returns **200 HTML** rather
  than a 404. Check `content_type`, never the status code alone.
- **It is open-core, and the split is not where you would guess.** All 60 PDF
  tools are the MIT half; the proprietary half is auth, policy, audit, billing,
  clustering, and their MCP server, under a licence barring production and
  client-facing use. Local single-user operation never reaches it; reselling or
  hosting for an organization does.

### An OCR test that returned 200, a valid PDF, and real text — and proved nothing

The first OCR check here passed twice over for the wrong reasons: it sent an
`ocrType` outside the endpoint's enum (200, silently another mode), and it ran
against a PDF that **already had a text layer**, so extraction recovered text
that predated OCR. The rewritten test builds the negative control first —
render to PNG, rebuild as an image-only PDF, **assert zero extractable
characters**, then OCR and assert text returns. 0 chars before, 334 after,
28/40 known words matched.

The same round found the mirror failure: **four of the suite's first-run
failures were wrong assertions, not defects** — `pdfinfo` column padding broke a
substring match, `pdfinfo` on an encrypted file prints no `Encrypted:` line to
parse at all, and a watermark drawn with a subsetted font carrying no
`ToUnicode` map is invisible to text extraction while being plainly there on the
render. Both directions are the same rule this repo already runs on: a gate
whose own assertion was never tested reports a hypothesis, not a result.

## Claude Code Director Skill
- `.claude/skills/claude-code-director/SKILL.md` — Director Framework (Cole Medin):
  Plan First → Manage Context → Verify The Work → Build The System. Generates
  PLAN.md, context budget, verification harness, and system evolution notes.
- Trigger: `/claude-code-director` or "director mode", "plan this properly",
  "stop vibe coding", "apply the director framework"

Claude Code project settings are in `.claude/settings.json` and point at these
repo-local skill files. Codex discovers the packaged copies after installing
the repo marketplace plugin, whose `.codex-plugin/plugin.json` exposes
`"skills": "./skills/"`. `AGENTS.md` remains the repo-level fallback before
plugin installation.

For long-running app builds, use PLAID as the product source of truth and
Codex/Claude `/goal` as the execution loop:
1. Read `vision.json`, `docs/product-vision.md`, `docs/prd.md`, and
   `docs/product-roadmap.md`.
2. If `docs/design.md` is present, follow it for UI. If it is missing, use the
   brand guidance in `docs/product-vision.md` and keep the UI restrained.
3. Execute roadmap tasks in order, one phase at a time.
4. Mark roadmap checkboxes complete only after implementation and verification.
5. Run available build, lint, test, and manual verification before reporting a
   goal achieved.

The skill resolves its own directory from the Codex cache, the Claude plugin
cache, or a repo checkout — see the resolution block at the top of `SKILL.md`.
Keep that block in sync if directory names change.

## Commands
```bash
# run the test suite (stdlib + pytest, no network)
# pytest is the repo's ONE declared dev dependency ([dependency-groups] dev),
# so it lives in .venv, not on system python. /usr/bin/python3 is Debian
# PEP 668 externally-managed with no pip — do not try to install into it.
# `uv run` syncs the dev group against uv.lock and works without activation.
uv run --frozen pytest -q

# exercise the scraper / feed generator directly against a checkout
python3 skills/content-ideas/scripts/scrape.py --help
python3 skills/content-ideas/scripts/generate_feed.py --help

# mirror every ~/.claude/skills entry into ~/.codex/skills so Codex sees the
# same skill set as Claude Code (idempotent, safe to re-run after installing
# new skills on either host)
bash scripts/sync-codex-skills.sh

# synchronize the governed presentation pipeline to Claude Code and the
# Windows Hermes Desktop profile mounted into WSL; differing host copies are
# backed up before replacement
bash scripts/sync-presentation-pipeline-hosts.sh

# validate the portable recovery skills and their integrity manifest
bash scripts/verify-recovery-skills.sh

# repo-wide skill integrity gate (all six skill trees, 450 SKILL.md files)
python3 scripts/check_skills.py
python3 scripts/check_skills.py --rule crosstree   # one rule in isolation

# design-token contract (stdlib Python, no browser, works on Codex)
bash skills/design-tokens/scripts/check.sh

# WCAG 2.2 render gates over a page: 0 clean, 1 blocked, 2 findings.
# Needs `npm i -D playwright axe-core` + a Chromium build; DESIGN_TOKENS_CHROMIUM=auto
# uses a cached build when Playwright's expected one is missing.
DESIGN_TOKENS_CHROMIUM=auto bash skills/design-tokens/scripts/run_gates.sh <page.html>
```

`testpaths` in `pyproject.toml` is `["tests", "skills/*/tests"]`. The glob is
load-bearing: it collects skill-local suites that previously never ran, while
excluding `skills/skill-builder/scripts/test_*.py` — those match `test_*.py`, contain
zero test functions, and scan `~/.claude/skills` at import time. Do not widen it to
`.claude/skills`; four skill-builder basenames collide across the two trees. Tests
needing a skill's opt-in dependency guard with `pytest.importorskip`, including ones
that only shell out to a dependency-using script via `sys.executable`.

## Skill integrity gate

`scripts/check_skills.py` is the deterministic gate over every skill tree in
the repo — `skills/`, `.claude/skills/`, `.agents/skills/`, `.github/skills/`,
`plugins/content-ideas/skills/`, and `portable-skills/`. It is enforced by
`tests/test_skill_integrity.py`, so it runs with the normal pytest suite.

| Rule | What it protects |
|---|---|
| `frontmatter` | every SKILL.md has a closed YAML block |
| `name` | `name:` equals its directory name |
| `dupes` | no invocation name declared by two directories |
| `routing` | no two skills share a `description:`, `triggers:`, or `## When to invoke` — fuzzy-matched, because exact equality fell to a trailing period |
| `desc` | routing is *reachable*: a 40+ char description, or a `## When to invoke`, or `triggers:` |
| `crosstree` | no skill's body differs across trees unless registered in `scripts/cross-tree-variants.json` |
| `mirror` | packaged mirrors are byte-identical **and tracked in git** |
| `bytecode` | no committed `__pycache__`/`.pyc` |

**Do not relax `desc` back into a minimum-length rule.** gstack's catalog trim
deliberately shortens Claude-host descriptions and moves routing prose into the
body plus `proactive-suggestions.json`. A short description is that
optimization working; enforcing length re-inflates the always-loaded catalog
this repo is trying to shrink.

**`scripts/cross-tree-variants.json` is evidence-gated, not a waiver list.**
Every entry needs a non-empty `reason` and `evidence` and must name each tree it
covers; the rule validates all three, so an entry cannot silently waive more
than it claims. Two entries carry an `open_question` rather than pretending
resolution — leave those unresolved rather than closing them with a guess.

**When a rule goes from red to green, ask what moved.** Every rule in that file
carries a revision note recording what it measured wrongly first. Four audit
rounds found the same failure repeatedly: a check that goes green because the
thing it measures moved is worse than no check, because it now certifies the
defect. The full discipline is written up in
`skills/graph-engineering/SKILL.md` under "Verification discipline" — read it
before adding or editing a rule.

## Rules
- Runtime stays dependency-free: stdlib only (`urllib`, `json`, ...). No pip installs at runtime.
- `skills/content-ideas/scripts/lib/__init__.py` is a bare package marker — no eager imports.
- Persistent state lives under `$CONTENT_HOME` (default `~/Documents/Content`), never the cwd.
- Credentials live in `~/.config/content/.env` (`SCRAPECREATORS_API_KEY`, `SETUP_COMPLETE`).
- API keys used by this project's skills follow a two-layer pattern, because
  Claude Code and Codex have no shared secrets mechanism:
  - **`.claude/settings.local.json`'s `env` block** — Claude-Code-specific.
    Injected directly into every session for this project regardless of how
    the session was launched; works even in non-interactive Bash tool calls,
    which don't source `~/.bashrc`. Gitignored (`.gitignore` has the
    `.claude/settings.local.json` pattern) — never the committed
    `.claude/settings.json`.
  - **`~/.bashrc` `export`** — the cross-host baseline. Codex reads secrets
    from its own process environment directly (e.g. `bearer_token_env_var`
    in `~/.codex/config.toml` for the gbrain MCP server); it has no
    settings.local.json equivalent, so this layer is what Codex — and any
    interactively-launched Claude Code session — actually relies on.
  - Write to both layers together; neither replaces the other. Never put a
    real key in `~/.config/content/.env`'s tracked convention notes, a
    commit, or any file under version control.
  - Currently configured this way: `SUPADATA_API_KEY`, `GBRAIN_REMOTE_TOKEN`,
    `OPENAI_API_KEY`, `EXA_API_KEY`, `GOOGLE_GENERATIVE_AI_API_KEY`,
    `GROQ_API_KEY`. When hunting for an already-configured key before asking
    the user for a new one, check beyond this repo and beyond WSL paths —
    Windows-side app configs (e.g. `/mnt/c/Users/<user>/AppData/Local/hermes/.env`,
    `/mnt/c/Users/<user>/.config/watch/.env`, `/mnt/c/Users/<user>/.fcc/.env`,
    `/mnt/c/Users/<user>/.cli-proxy-api/config.yaml`) have held real values
    that their WSL-side namesakes didn't.
- Local AI-gateway/router proxies on the Windows side are common places to
  find already-configured provider keys and model routing before assuming a
  tool is broken or asking for new credentials:
  - **`free-claude-code` (fcc)** — `~/.fcc/.env` (provider keys plus
    `MODEL`/`MODEL_OPUS`/`MODEL_SONNET`/`MODEL_HAIKU` routing), binaries at
    `~/.local/bin/fcc-*.exe`. Actively developed upstream — before trusting a
    hard failure, check whether the installed build predates the commit that
    fixed it (`fcc-server --version`), and update via the installer one-liner
    in its README before debugging further.
  - **OmniRoute** — dashboard/API on `127.0.0.1:20128`; the gateway API key
    lives in its SQLite-backed dashboard, not `.env` (`~/OmniRoute/.env` only
    holds server-runtime secrets like `INITIAL_PASSWORD`/`JWT_SECRET`). Use
    the bundled `omniroute` CLI (`providers list`, `models <provider>`,
    `usage logs`, `setup-claude`, `setup-kilo`, `launch --profile <name>`)
    instead of the dashboard when a CLI path exists — no login needed.
    `providers list` / `models` catalog entries are not proof a model ID is
    actually routable, and `auto/*` combos can silently pick a different
    provider than expected — confirm with a real `/v1/chat/completions` call
    and cross-check `omniroute usage logs` for the provider/status that
    actually served it.
  - **cli-proxy-api** (`router-for-me/CLIProxyAPI`, often bundled inside
    another tool's `bin/`, e.g. Hermes) — config at
    `~/.cli-proxy-api/config.yaml`, OAuth credentials as
    `<provider>-<email>.json` in the same directory. Must be launched with an
    explicit `-config <path>` flag; it does not reliably resolve the config
    path from a WSL-launched process's working directory. Stored OAuth
    tokens refresh lazily on the next proxied request, not on a timer — a
    stale `expired` timestamp with the process not currently running is not
    itself a bug.
  - **Hermes Agent** (NousResearch, git install) — `~/AppData/Local/hermes/`.
    `hermes skills list-modified` lists real user-customized skills by name;
    a noisy `git status` in its `hermes-agent` checkout (e.g. from a botched
    update stash/restore) does not by itself threaten them — Hermes tracks
    skill customizations separately from raw git diff state.
- PowerShell or native `.exe` processes launched from a WSL Bash shell
  inherit the WSL cwd, which Windows renders as a `\\wsl.localhost\<distro>\...`
  UNC path — cmd.exe refuses it outright, and some native exes silently
  resolve relative config paths against it and fail instead of erroring
  clearly. Pass an explicit Windows working directory or absolute paths
  rather than relying on the invoked process's own relative-path resolution.
- If `gbrain` is available as an MCP server, use it by default for cross-session
  memory and retrieval before repeating strategy or pipeline research from
  scratch.
- Treat `gbrain` as an explicit chain stage:
  - `GBrain Recall` before `content-research`, strategy synthesis, or pipeline
    Stage 1 work
  - `GBrain Write-back` after the run when durable findings should become
    reusable memory
- Treat GBrain as the durable knowledge layer for recurring companies, people,
  prospects, verticals, themes, named accounts, and prior research findings.
- Treat GBrain retrieval as embedding-backed semantic retrieval by default, not
  just keyword lookup.
- Prefer semantic recall first; use synthesis only when the task needs merged
  interpretation rather than simple recall.
- Read from GBrain first when the task references an entity or topic that may
  have appeared in prior work, and write durable findings back after the run
  when they are likely to matter again.
- When a chained run or pipeline uses GBrain, reflect that explicitly in the
  run status instead of treating it as invisible setup.
- Do not use GBrain as the system of record for deliverables. Briefs, feed
  data, decks, and client-facing artifacts must still be written to local files
  in the repo or run folders.
- In Codex Desktop or any host that exposes stronger research plugins such as
  `exa`, prefer those plugins for discovery and current web research during
  Stage 1 research and strategy/pipeline work. Use them to find better official
  product pages, documentation, GitHub repos, competitive signals, and current
  operator proof points faster than generic search alone.
- In terminal-first hosts such as Codex CLI, prefer the closest equivalent:
  an MCP-connected research server or a local CLI/API wrapper for tools such as
  Exa when available. Treat that as the terminal analogue to desktop plugin
  access.
- Concrete terminal patterns to prefer when available:
  - Exa MCP over remote/HTTP MCP
  - a local Exa API wrapper that calls `https://api.exa.ai/search`
- Codex Desktop plugin access is a discovery advantage, not an exception path.
  The same workflow, delivery, QA, and source-verification rules still apply.
- Plugin-assisted research improves discovery; it does not replace local file generation,
  branded PPTX build and QA, repo-specific workflow rules, or the requirement to
  verify that final cited sources are primary and current.
- Host-specific paths must be configurable. Prefer environment variables over
  machine-specific absolute paths for branded templates, delivery destinations,
  second-brain exports, and vault locations.
- Client-facing PowerPoint output must use the branded PowerPoint template at
  `BRANDED_PPTX_TEMPLATE`, or fall back to
  `~/.claude/templates/branded-template.pptx`, or the downstream
  `branded-pptx-deck` / `pptxkit` workflow that wraps it. Do not generate
  client-facing `.pptx` decks from ad hoc `python-pptx` slide layouts or blank
  presentations. If the branded template/workflow is unavailable, stop and say
  the PPTX is blocked rather than shipping an unbranded substitute.
- Every client-facing slide must contain structured content, not just a title
  and a few loose bullets. Default to a clear slide contract per page:
  action title, supporting structure (cards/table/scorecard/use-case layout),
  and explicit evidence, implication, or next-step content. For use-case decks,
  always include at least one detailed use-case realization slide using the
  branded layout (challenge, solution, how-it-works, stats, stack, systems,
  users, organizations).
- PPTX QA is a delivery gate, not an optional polish step. Before delivering any
  client-facing deck:
  1. the branded builder must save successfully with validation enabled
  2. slide text must be checked for overlap, overflow, and collisions
  3. if `preview_pptx.py` is available, its contact sheets must be reviewed
  4. if preview tooling is unavailable, say the deck is unreviewed for visual QA
     and do not present it as final
  5. if overlap is observed, fix the deck before delivery
  6. use a delivery status explicitly: `draft`, `reviewed`, or `blocked`
  7. use filename suffixes that match that status: `*-draft.pptx`,
     `*-reviewed.pptx`, `*-blocked.txt` or equivalent
  8. keep the branded deck builder script in the run folder so QA fixes are
     reproducible
  9. the reviewed deck must be the one copied to the user-facing delivery path
     resolved from `CLIENT_DELIVERY_DIR`
  10. minimum visual QA checklist:
      - no red overflow boxes in `preview_pptx.py`
      - no title/subtitle collisions
      - no clipped text in stat bars, callout strips, or side panels
      - footer/page number present on each slide
- When building strategy/pipeline outputs from use cases, content-research notes,
  or external documents that reference OpenHands, treat the OpenHands GitHub
  repo and docs as the source of truth for implementation details:
  - Repo: `https://github.com/OpenHands/OpenHands`
  - Docs: `https://docs.openhands.dev/`
  Use these to ground coding snippets, agent patterns, skills/microagents, MCP
  integration, CLI/headless workflows, deployment models, and solution-stack
  technology choices. Prefer verified OpenHands primitives over invented
  orchestration details.
- Version is tracked in `pyproject.toml`, `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, and the
  `version:` field of `SKILL.md` — keep them identical. `tests/test_plugin_contract.py` enforces this.
- `SKILL.md` frontmatter only carries the keys Claude Code's skill spec
  permits at the top level. Commit `7f3d602` moved everything else —
  `version`, `argument-hint`, `user-invocable` — under
  `metadata.legacy-frontmatter:`. That is the current canonical layout; do not
  "restore" those keys to the top level. The contract test accepts either
  position, so a normalizer pass over `skills/` does not break it — but that
  commit changed 199 files under `skills/` and none under `plugins/`, which
  is exactly the drift the byte-identity check exists to catch. **Any
  frontmatter normalization must run over `plugins/content-ideas/skills/` in
  the same commit.**

## GBrain (MCP server — persistent memory layer)

GBrain is wired as an MCP server for this project, reachable over HTTP (not
stdio) at `http://127.0.0.1:3131/mcp` with a per-agent bearer token.
It provides persistent knowledge-graph memory across sessions.

### Location & config
- Repo: `~/gbrain` (cloned from `github.com/garrytan/gbrain`)
- Brain: `~/.gbrain/brain.pglite` (local embedded Postgres, zero DB cost)
- Engine: PGLite
- Search mode: `conservative` (cheapest tier)
- Embeddings: `google:gemini-embedding-001`, 768 dims (requires
  `GOOGLE_GENERATIVE_AI_API_KEY` — get one at
  `https://aistudio.google.com/apikey`; this is a different credential from
  the Gemini CLI's OAuth-personal login and cannot be substituted for it)
- Chat/synthesis: `google:gemini-2.0-flash-exp` (chat), `google:gemini-2.0-flash`
  (query expansion)
- Cost: **$0.00/month** on free tier

### Running it — systemd user service, not an ad hoc background process
- Server process: `~/.config/systemd/user/gbrain.service` runs
  `gbrain serve --http --port 3131` with `Restart=on-failure`.
- `systemctl --user enable gbrain.service` is set, and
  `loginctl enable-linger sheke` is enabled, so the service survives both a
  closed terminal and a full logout — it starts on WSL boot, not just on
  login.
- To check it: `systemctl --user status gbrain.service` /
  `curl http://127.0.0.1:3131/health`.
- `gbrain reinit-pglite` (or any full reinit) wipes the auth-tokens table —
  every connected host's bearer token goes invalid at once and needs
  `gbrain auth create <name>` + `gbrain connect ... --install --force` again
  per host.
- MCP registration is **project-scoped per working directory**, not global —
  `gbrain connect --install` only updates the entry for whatever directory
  you ran it from. Re-run it from `content-ideas` specifically after any
  token rotation, or other projects silently keep the stale token.

### When to use GBrain vs local files
- **GBrain pages**: prospects, people, companies, recurring research topics,
  verticals, use-case themes, meeting notes, deal context — anything that
  compounds across sessions and benefits from graph traversal and synthesis.
- **Local files** (`$CONTENT_HOME/research/`): pipeline run artifacts,
  feed-data.json, strategy briefs, PPTX decks — session-scoped deliverables
  that follow the pipeline-runner workflow.
- **Memory files** (`~/.claude/projects/.../memory/`): behavioral guidance,
  user preferences, project meta — things that shape how the agent works.

### Cost guardrails
- Search mode is `conservative`. Do NOT change to `balanced` or `tokenmax`
  without explicit user approval — cost scales 2.5× to 5× respectively.
- Dream cycle / enrichment crons are NOT enabled. Do not enable without
  explicit user approval — each cron job fires LLM calls.
- Prefer `search` (keyword, free) over `ask`/`query` (synthesis, costs
  tokens) for simple lookups.
- For strategy/pipeline recall, prefer embedding-backed semantic retrieval over
  plain keyword lookup when both are available. Escalate to synthesis only when
  the task needs aggregation, interpretation, or merged judgment.
- When writing pages, embeddings fire automatically. Batch writes where
  possible to reduce embedding calls.

### GBrain commands (via MCP or CLI)
```bash
gbrain search <query>        # keyword search (free)
gbrain query <question>      # hybrid search + synthesis (costs tokens)
gbrain get <slug>            # read a page (free)
gbrain put <slug>            # write/update a page (embedding cost)
gbrain list --type <T>       # list pages (free)
```

## DeepSeek Harness (dsh) model providers

`dsh` is installed globally (`npm i -g @deepseek-ai/dsh`) with profiles under
`~/.dsh/profiles/{headless,web}/`. Contract:
`docs/dsh-multi-model-provider-contract.md`. Secrets-free config example:
`docs/dsh-cordis-patch.example.yml`.

- **A catalog entry is not a routable model.** Confirm every model with a real
  `chat/completions` call *and* an end-to-end `dsh` run before configuring it.
  OmniRoute lists 29 DeepSeek models and 28 fail; its Cursor routes return
  HTTP 200 with zero output tokens in 4 ms, so status-code checks certify them
  as healthy.
- **Port from `~/.hermes/config.yaml` rather than rebuilding auth.** Its
  `custom_providers` of `type: openai_compatible` map 1:1 onto dsh's
  `api: openai-completions`. The same provider can work there and 403 in
  OmniRoute — a failure in one host's copy is not evidence the provider is down.
- **zenmux is prepaid per-token, not a subscription** (`claude-opus-5` is
  $25/M output) and exposes no balance endpoint. For Claude at zero cost use
  the `claude-code-cli` route.
- `scripts/claude_code_bridge.py` reproduces Hermes' `cli://claude-code`
  `external_process` provider for dsh: an OpenAI-compatible shim that spawns
  `claude -p`, storing no credential. It never emits `tool_calls`, so that
  route bypasses dsh's own tools, permissions, sandbox, and trajectory — a
  passing smoke test is indistinguishable from a real tool-calling model.
- Windows-side gateways (OmniRoute 20128, CLIProxyAPI 8317) are **not** on
  `127.0.0.1` from WSL — use the default-gateway IP, which changes on reboot.
- **`~/.dsh/settings.yaml` silently beats every `--patch` overlay.** When its
  `agent-default-model` block is present, `dsh --patch ~/.dsh/patches/<x>.yml`
  is ignored with no warning, which disables all the documented escape hatches
  at once. **`--dump-config` cannot detect this** — it composes the profile tree
  without the user settings layer that wins at runtime, so it shows the overlay
  correctly applied while the run goes elsewhere. Prove a model switch by
  pointing an overlay at a bogus model id and confirming the run *fails*; to
  actually switch, edit `settings.yaml`.
- **dsh resolves credentials from `~/.dsh/.credentials.yaml`, not only the
  environment.** A run succeeds with the key unset in the shell. So the
  two-layer pattern above (bashrc + `settings.local.json`) does not by itself
  reach dsh — add the key to `.credentials.yaml` (mode 600) as well, and never
  treat an env-only check as proof a route is unconfigured.
- **A dead default model looks like a broken dsh.** While
  `oc/deepseek-v4-flash-free` was pinned in `settings.yaml`, every run failed at
  boot regardless of the route requested. Check the default before debugging the
  provider. That model is now **gone from both routes it ever had**: opencode
  returns `401 Free promotion has ended … subscribe to OpenCode Go` (the
  credential is fine — `oc/big-pickle` works on the same key), and zenmux no
  longer lists the `-free` id at all, its successor `deepseek/deepseek-v4-flash`
  being $0.66/M. This is a **discontinued promotion, not exhausted credits**: a
  top-up does not fix it. Routing an agent onto another provider to work around
  a model is evidence it is unavailable, not evidence it works.
- **NVIDIA's NIM free tier is intermittently flaky, per-model and transient** —
  a model can go 3/3 and then 1/3 with `404`s minutes later, and dsh can return
  `PI_AI_ERROR: Service temporarily overloaded` on a route that works on retry.
  Re-run before concluding a model is dead. This does not soften the
  catalog-is-not-proof rule, which governs first configuration; it governs
  *re-testing something already verified*.
- The `nvidia` route (`integrate.api.nvidia.com/v1`, `NVIDIA_NIM_API_KEY`) is
  NVIDIA's free credit pool, direct rather than via OpenRouter. 20 of its 103
  catalog models are verified routable — see the contract doc for the list and
  for the exclusions. Four excluded models **hang past 180 s with no status
  code**, which a generous timeout reads as pending rather than broken; that is
  the failure mode to design checks against here.

## Google Vids: a real automation lane, reachable over CDP

Vids has no API and no MCP connector, but it is fully drivable in a browser and the
whole Slides-to-narrated-video path works. Verified end to end on 2026-08-29: a 30-slide
deck became an 8:55 1080p MP4 with per-scene AI voiceover and captions.

The route is **Slides → "Turn into video"**, not the Vids home page. Open the deck in
Google Slides (a `.pptx` in Office-compatibility mode is fine — no conversion needed),
open the **Transform** side panel, and click **Turn into video**. Vids creates one scene
per slide, writes narration from the slide content, and adds a licensed music bed. It
does **not** read speaker notes aloud, so source-cell provenance in notes is safe.

### Standing it up

```bash
CHROME=~/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome   # NOT chrome-linux
"$CHROME" --remote-debugging-port=9222 --user-data-dir=~/.cache/vids-automation-profile \
  --no-first-run --no-default-browser-check https://vids.google.com &
```

Then `chromium.connectOverCDP('http://127.0.0.1:9222')`. WSLg provides `DISPLAY=:0`, so
the window is visible and **the user completes 2FA themselves** — never handle the
credential. Tick "Don't ask again on this device" and the profile stays authenticated.

- **`agent-browser` on this machine is a broken symlink** into a deleted
  `hermes-agent/node_modules`. One dead path is not a dead lane; Playwright + CDP works.
- **A Google survey iframe steals every click.** Remove `#google-hats-survey` before each
  interaction or clicks time out against "iframe intercepts pointer events".
- Uploading to Drive: the Drive MCP needs base64 through context (211k tokens for a
  167KB deck — over the read limit), so use the browser. Drive builds its file input on
  demand, and clicking the menu item is intercepted; the **Alt+C then U** shortcut with
  `page.waitForEvent('filechooser')` works.

### Vids flattens an embedded PPTX clip; composite it back in afterwards

"Turn into video" imports the deck as still slides. A `.pptx` that carries
embedded media loses it: the F slides arrive as their poster frame, so the
demonstrator sits motionless for its whole scene while the narration describes
what it is doing. Vids also has no way to say "use the deck's narration, not
this clip's audio", because the clip is not there at all.

Fix it in post on the exported MP4 rather than fighting the import:

- **Take the scene windows from the exported caption stream**, not from the
  editor. Each narration block's first cue marks its scene start, and the next
  block's first cue marks the end. That is derived from the artifact, survives
  a re-export, and needs no browser session.
- **The seat maps by a flat scale factor.** A 1280x720 slide stage renders to
  1920x1080, so a seat at (48,168,800,450) becomes (72,252,1200,675). Verify by
  drawing the rect on a real frame before encoding — one crop check costs
  seconds and catches a letterbox or crop assumption.
- **`overlay=...:enable='between(t,start,end)'` with `-c:a copy`** puts the live
  clip in the seat and leaves the voiceover bit-for-bit untouched. Confirm with
  an audio-stream MD5 before and after; the clips must contribute video only.
- **Prove motion against the static original, not against a threshold.** Mean
  absolute difference between two frames of the seat region ran 0.00-0.34 on the
  untouched export and 3.9-35.8 on the composited one. Two of the four sims
  change slowly enough that their absolute delta alone reads as ambiguous; the
  control is what makes it a measurement.

### Vids: three silent failures that survive a green-looking run

Measured across an 88- and a 90-slide rebuild, Aug 30-31.

- **"Update all voiceovers" DOES re-time every scene — wait before measuring.**
  Changing the voice and confirming *Replace all existing voiceovers?* re-fits
  the scene durations to the new audio: one part went 09:56.7 -> 13:41.6, and
  the narration rate fell from **192 wpm to 152 wpm**. Read the total too soon
  and it still shows the old duration, which reads as "voice does not affect
  pace" — a wrong conclusion this repo reached once and acted on. Re-read the
  playhead after the outdated badges clear, not before.
- **An export can serve a stale render.** A part exported *after* a voice change
  downloaded in seconds at the pre-change duration (563.99 s while the editor
  read 11:55.5 = 715.4 s). It looks like a fast success. **Always compare the
  downloaded file's duration against the editor's readout before using it**; a
  fast download is the tell, because a real render is slow.
- **Speaking rate is the pacing metric, not span.** `words / caption-span`
  conflates rate with dead air. Compute `words / sum(cue durations)`: the good
  render was 151.9 wpm with 4.3% silence, the bad one 192.0 wpm with 1.3%.

Scene start times for compositing come from the editor's timeline labels
(`... starting in scene N at X seconds with duration Y`), read by walking the
Voiceover panel's scene arrows — the panel **persists its selected scene across
a reload**, so a walk that assumes it starts at scene 1 silently reads the wrong
slide. Captions are the fallback and can be partial (one 45-scene export
produced 31 cues covering 2:52-9:36 while the audio was complete throughout).

### A same-name Drive upload blocks on a dialog the uploader never sees

Uploading a file whose name already exists raises *"already exists in this
location. Do you want to replace the existing file with a new version?"* and
**waits**. A driver that hands the file to the input and then blind-waits before
closing the page reports success and uploads nothing. Choosing *Replace existing
file* keeps the same file id, so previously shared links stay valid. Poll for the
dialog and report its text rather than sleeping;
`runs/2026-08-29-.../video/vids/upload_deck2.mjs` is the corrected driver.

### Vids caps a Slides import at 45 slides, behind a dialog that looks like a hang

"Turn into video" on an 85-slide deck produced a Vids doc that sat at **one
scene and 00:00.0 for ten minutes**. It was not importing. A modal was waiting:
*Select slides — 45 out of 85 selected*, with a Next button. 45 is the ceiling;
the rest are silently dropped. Screenshot the page before concluding an import
is slow — scene count and duration both read exactly like a hang while a dialog
holds the flow.

For a longer deck, split it, run the lane twice, and concatenate: both exports
come out 1920x1080 h264 / aac 44.1k stereo, so `ffmpeg -f concat -c copy` joins
them without re-encoding. Split on a section divider so each part opens on
context.

Two more traps in the same flow:

- **"Update all voiceovers" exists only on the All scenes tab.** On Current
  scene the button is the singular "Update voiceover", which regenerates one and
  looks like it did everything. Switch tabs first, then click, then confirm the
  *Replace all existing voiceovers?* dialog. The voice survives the tab switch.
- **A stale Drive tab makes the upload shortcut silently dead.** Alt+C then U
  fires no `filechooser` event at all on a Drive tab left over from an earlier
  step. Open a fresh tab per upload, press Escape first (a native chooser from a
  failed run blocks every shortcut), and click the grid to give it focus.

### Two scripting traps that read as broken automation

- **Never round-trip a RegExp through `.source` into `page.evaluate`.** Built in
  a heredoc, `'Scene (\\d+) / '` reached the page as `Scene (\\d+)`, matching a
  literal backslash, so the probe returned null forever and every navigation
  failed instantly. That reads as a dead panel, and it is not. Build the regex
  *inside* evaluate and pass only plain values.
- **`x.innerText` is undefined on SVG-backed buttons**, so a bare `.trim()` in a
  `querySelectorAll` scan throws mid-sweep and takes the whole probe with it.
  Guard with `(x.innerText||'')`.

### Vids' "background music" may not be music, so never match on the provider

On one of two videos generated the same way, Vids seated **"John F. Kennedy
Inaugural Speech, January 20, 1961 (Provided by Youtube)"** in the background
lane instead of a Shutterstock bed — a full 12-minute speech playing under the
narration. The removal step searched for `Provided by Shutterstock|background
music`, matched nothing, and reported **"music before: false"**, so a
contaminated export shipped as verified-clean.

Identify the bed **structurally**, never by provider or by the word "music": a
timeline element whose `aria-label` contains `starting in scene` but is *not*
`- <VoiceName> starting in scene` (the per-scene voiceover). That test found the
track on the first pass and confirmed the other video genuinely had none.

**Read the exported caption track — it is the cheapest ground truth available.**
Vids muxes a `mov_text` stream generated from the actual audio, so
`ffmpeg -map 0:s:0 out.srt` shows what really plays. Contamination is obvious
there: 1,158 cues before, 318 after, with the stray speech interleaved line by
line against the narration.

Two ways this was misdiagnosed before it was fixed, both worth avoiding:

- **A narrow phrase grep understated the damage 26x.** Searching the captions
  for oath wording (`kennedy|solemnly|swear|...`) returned 10 cues spanning 28
  seconds, so it read as a blip confined to scene 1. The speech continues in
  words that share no vocabulary with the oath ("Vice President Johnson", "a
  long twilight struggle"), and it ran the entire 12:32. Sample the captions at
  intervals and *read* them; do not trust a keyword set drawn from the first
  thing you noticed.
- **Caption text cannot verify narration wording.** Captions are ASR output, so
  "₹270 Cr" comes back as "270 crore" and a verbatim match fails on correct
  audio — it scored a known-good Part A at 24/45. Use the editor read-back for
  script fidelity, and the captions only for detecting foreign audio.

### Proving a music bed is gone: count digital silence, not loudness

A narration-only export still has a high median RMS, so a loudness threshold
proves nothing and a "% below -50 dB" cutoff picks up ordinary speech gaps. The
discriminator is **true digital silence**: a *music* bed fills every gap, so with
music essentially no window sits at -inf, while the measured narration-only
export had 1,156 such windows and 19.6% below -50 dB against a with-music
baseline of 0.1%. Check for the existence of silent windows; do not pick an
arbitrary percentage threshold, which is what made a clean export first read as
"music likely present".

**But this test only rules out a continuous bed.** A speech clip has its own
pauses, so it leaves silent windows and passes — the contaminated export above
scored as clean on exactly this measure. Silence counting is a check on *music*,
never a check that the audio contains only what you intended. For that, read the
caption stream.

### Five Vids behaviours that cost a cycle each

- **The voice reverts to the default on page reload.** Select the voice and click
  "Update all voiceovers" in one uninterrupted session. A reload between the two silently
  applies the old voice, and the panel label lies about which is active.
- **"Update all voiceovers" opens a "Replace all existing voiceovers?" confirm dialog.**
  An unconfirmed click looks like a completed regeneration. Scenes carry a "Voiceover
  outdated" badge until it actually runs; that badge count is the honest progress signal.
- **The narration editor is an `about:blank` iframe holding one editable node**, Docs
  style. `[contenteditable=true]` does **not** match it — probe for *any*
  `[contenteditable]`, or enumerate `page.frames()`. Clicking the paragraph focuses the
  iframe; Ctrl+A then `keyboard.type` replaces the text. Click the paragraph **body**,
  not the "Scene n / 30" header — a click on the header turns Ctrl+A and typing into
  scene navigation, which reads exactly like data loss and is not.
- **Scene 1's timeline `aria-label` is "Scene 1 of 2"**, every other scene is "of 30".
  Match `^Scene 1 of ` or navigate by the panel header, which is authoritative.
- **Removing the music track barely changes the file size.** AAC compresses silence to
  almost nothing and the 1080p video dominates: 20,801,557 → 20,801,564 bytes, a 7-byte
  delta that looks exactly like a cached re-render. Prove it on the audio instead —
  measure the noise floor in 100ms windows. With music, 0.1% of windows sit below −50dB;
  without, 33.3% are at digital silence (−240dB).

Working scripts live in
`runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids/`:
`replace_all.mjs` (bulk narration replacement, 30/30 verified), `verify_all.mjs`
(read-back verification against the source script), `final2.mjs` (voice + regenerate
with the confirm dialog), `upload3.mjs` (Drive upload), `dogo.mjs` (MP4 export).

### The playwright MCP needs Node 20+, and its own metadata hides that

`@playwright/mcp` declares `engines: {node: ">=18"}`, which is stale — Playwright's
runtime rejects anything under 20 (`You are running Node.js 18.19.1. Playwright requires
Node.js 20 or higher.`). npm installs it happily, so the server starts and dies, and the
host reports only `CONNECTION_CLOSED`. This machine's default `node` is `/usr/bin/node`
v18, so the MCP fails at every session start while `npx @playwright/mcp` works fine from
an nvm shell. Fix is to pin the command in `~/.claude.json`:

```json
"playwright": {
  "command": "/home/sheke/.nvm/versions/node/v24.18.1/bin/npx",
  "args": ["-y", "@playwright/mcp@latest"],
  "env": { "PATH": "/home/sheke/.nvm/versions/node/v24.18.1/bin:/usr/local/bin:/usr/bin:/bin" }
}
```

A failed MCP connection is worth reproducing by hand before calling it transient — the
error that explains it never reaches the host.

### Two commands that report success without doing anything

- **`Browser.setDownloadBehavior` silently no-ops on an externally launched browser.**
  Downloads land in the browser's own default directory. Search for the file rather than
  trusting the configured path.
- **`rm -f` exits 0 when its argument matches nothing.** With an em-dash or other
  non-ASCII in the filename, a quoting slip means "removed" prints while the file stays.
  Verify with a listing, never the exit code. The same self-match hazard applies to
  `pkill -f <pattern>` run from a shell whose own command line contains the pattern — it
  kills the calling shell (exit 144). Match on `ps -eo pid,args | awk` instead.

## Reference repos (cloned locally)

- `~/awesome-llm-apps/generative_ui_agents/` — 7 Generative UI agent demos
  (Google ADK + CopilotKit AG-UI). All deps installed. Each project has its
  own Python venv at `agent/.venv/` and Node deps in `node_modules/`.
  Requires `.env` with API keys (Gemini, Tavily, etc.) to run.
- `~/real-estate-dashboard-agent/` — forked from ai-dashboard-canvas-agent,
  customized for Summit Realty Group (DFW brokerage). Run with `npm run dev`.
  Pushed to `github.com/shekerkamma/real-estate-dashboard-agent`.
- `~/gbrain/` — GBrain knowledge brain. Bun runtime. 50 skills. MCP server.

## ADK + AG-UI (Generative UI) rules

- When building or forking any ADK agent that uses CopilotKit frontend tools
  (`useCopilotAction` — e.g. `add_chart`, `update_chart`, `delete_chart`),
  the agent's server-side `tools` list MUST include `AGUIToolset()` from
  `ag_ui_adk`. Without it, the AG-UI middleware cannot inject frontend tool
  definitions at runtime and ADK throws "Tool not found." Import:
  `from ag_ui_adk import ADKAgent, AGUIToolset`
- Frontend-side tools (registered via `useCopilotAction` in React) must NOT
  be duplicated as server-side `FunctionTool` stubs. They arrive via the
  `RunAgentInput.tools` payload and are injected as `ClientProxyTool` wrappers
  through the `AGUIToolset` → `ClientProxyToolset` substitution.
- Pipeline use cases can produce working demos as a Stage 7 artifact:
  pipeline use case → fork a generative UI demo from
  `~/awesome-llm-apps/generative_ui_agents/` → customize with domain-specific
  tools and instructions → ship as proof-of-concept. The RE dashboard is the
  first instance of this pattern.
- Gemini free tier rate limits: `gemini-3.5-flash` has 20 RPM, hits limits
  fast during interactive demos. Prefer `gemini-2.5-flash` for ADK agents.

## Portable path defaults

Use these environment variables to make the same workflow portable across
Codex, Claude, and terminal hosts:

- `BRANDED_PPTX_TEMPLATE` — branded `.pptx` template path. Default fallback:
  `~/.claude/templates/branded-template.pptx`
- `CLIENT_DELIVERY_DIR` — optional copy-out location for reviewed decks
- `SECOND_BRAIN_DIR` — optional content-research export directory
- `OBSIDIAN_VAULT_DIR` — optional vault root for content-research notes

If an env var is unset, do not invent a machine-specific substitute beyond the
documented fallback. Report the step as blocked or skip the optional export.

## Skill Builder

- **skill-builder** (`.claude/skills/skill-builder/SKILL.md`) — guided skill creation and audit tool following Claude Code official best practices.
- Trigger: `/skill-builder` or "help me build a skill" or "audit this skill"
- Supports: new skill discovery interview · existing skill audit · frontmatter optimization
- Technical reference: `.claude/skills/skill-builder/reference.md`
