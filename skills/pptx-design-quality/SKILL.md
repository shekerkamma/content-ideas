---
name: pptx-design-quality
description: Behavioral quality overlay for creating, rebuilding, or materially redesigning PowerPoint decks. Use when any native, hybrid, HTML-derived, or image-per-slide PPTX workflow must capture audience and design intent, apply a shared deck-refinement vocabulary, run deterministic PPTX design linting, and gate critique, audit, polish, and reviewed status.
---

# PPTX Design Quality

Use this overlay alongside `pptx-visual-spec`, the selected deck builder, and Office render
QA. It governs design intent and quality; it does not replace evidence routing, branded
templates, content validation, or PowerPoint structural validation.

## Required artifacts

Resolve the installed skill directory once per shell. This works from a repo checkout or a
cross-host installation:

```bash
# Prefer the host-provided plugin root, then the newest installed plugin cache.
for candidate in \
  "${CLAUDE_PLUGIN_ROOT:-}/skills/pptx-design-quality" \
  "${GEMINI_EXTENSION_DIR:-}/skills/pptx-design-quality" \
  "${CONTENT_IDEAS_DIR:-$HOME/content-ideas}/skills/pptx-design-quality" \
  "${CLAUDE_SKILLS_HOME:-$HOME/.claude/skills}/pptx-design-quality" \
  "${CODEX_SKILLS_HOME:-$HOME/.codex/skills}/pptx-design-quality" \
  "${AGENTS_SKILLS_HOME:-$HOME/.agents/skills}/pptx-design-quality" \
  "${ANTIGRAVITY_SKILLS_HOME:-$HOME/.gemini/antigravity/skills}/pptx-design-quality" \
  "${GEMINI_SKILLS_HOME:-$HOME/.gemini/config/skills}/pptx-design-quality" \
  ".agents/skills/pptx-design-quality"; do
  [ -f "$candidate/SKILL.md" ] && PPTX_DESIGN_QUALITY_DIR="$candidate" && break
done

if [ -z "${PPTX_DESIGN_QUALITY_DIR:-}" ]; then
  PPTX_DESIGN_QUALITY_DIR="$(ls -d \
    "$HOME/.codex/plugins/cache/"*/content-ideas/*/skills/pptx-design-quality/ \
    "$HOME/.codex/skills/"*/skills/pptx-design-quality/ \
    "$HOME/.claude/plugins/cache/content-ideas/content-ideas/"*/skills/pptx-design-quality/ \
    2>/dev/null | sort -V | tail -1)"
  PPTX_DESIGN_QUALITY_DIR="${PPTX_DESIGN_QUALITY_DIR%/}"
fi

[ -n "${PPTX_DESIGN_QUALITY_DIR:-}" ] || { echo "BLOCKED: pptx-design-quality not found" >&2; exit 1; }
export PPTX_DESIGN_QUALITY_DIR
```

Before building, create these files in the run directory:

- `deck-brief.md` — audience, decision, narrative promise, voice, anti-references,
  evidence/editability requirements, and success criteria.
- `deck-design.json` — deterministic typography, color, layout, and lint thresholds.
- `template-profile.json` — the selected template's brand, geometry, typography,
  composition rules, and approved slide archetypes.

Initialize them without overwriting existing files:

```bash
python3 "$PPTX_DESIGN_QUALITY_DIR/scripts/init_deck_context.py" \
  --run <run-dir> --title "<deck title>"
```

### Deriving a draft from a reference deck or a design canvas (optional)

When rebuilding from a reference presentation — or from a `/design` canvas drawn for
this deck — draft `template-profile.json` from it instead of hand-authoring from a
blank template:

```bash
python3 "$PPTX_DESIGN_QUALITY_DIR/scripts/derive_template_profile.py" \
  --run <run-dir> \
  --evidence <run-dir>/presentation-evidence.json \
  --pptx <reference.pptx> \
  --canvas <canvas-dir>
```

Any one of `--evidence` (from `presentation-source-bundle`), `--pptx`, or `--canvas`
works alone; supply more for a more complete draft. The script writes
`<run-dir>/draft-template-profile.json` only — it never overwrites
`template-profile.json`. Review the derivation notes it prints, tailor the draft, then
`cp` it over `template-profile.json` before validating. See
[`references/template-derivation.md`](references/template-derivation.md) for exactly what
each field's heuristic does and does not cover.

**`--canvas` takes the `/design` working tree** — the directory holding `canvas.json`
and the `*.dc.html` artboards. It is the only input that derives `geometry.grid_columns`,
`geometry.gutter_inches`, and `composition.corner_radius`, because a canvas declares its
grid and radii where a rendered deck only implies them. It is stdlib-only (no
`python-pptx`, no Pillow), and when combined with `--pptx` it wins every field it
derives — a canvas is the design you intend, a reference deck is the design you have.

Two things to hold onto:

- **The px scale is derived, not assumed.** The reference artboard's frame width in
  `canvas.json` fixes `pt = px * (slide_width_inches / frame_width_px) * 72`. At a
  1280x720 artboard that is 0.75pt/px; at 1920x1080 it is 0.5. Reading a canvas at a
  fixed 0.75 would inflate every size by a third on any other frame.
- **A canvas sets geometry, type, and brand — never evidence.** Claims and numbers stay
  with `presentation-evidence.json` and `check_claim_evidence.py`.

Tailor both files, then validate:

```bash
python3 "$PPTX_DESIGN_QUALITY_DIR/scripts/validate_deck_context.py" \
  <run-dir>/deck-brief.md <run-dir>/deck-design.json
python3 "$PPTX_DESIGN_QUALITY_DIR/scripts/validate_template_profile.py" \
  <run-dir>/template-profile.json
```

The JSON contract is defined in
[`references/deck-design-schema.json`](references/deck-design-schema.json).
Stable native rule IDs and their meanings are listed in
[`references/rules.md`](references/rules.md).
The reusable client-ready archetype catalog is
[`references/slide-archetypes.json`](references/slide-archetypes.json). Use its IDs in
`slide-plan.json`; extend the catalog instead of creating another presentation skill.

## Build loop

Apply these stages in order and loop back whenever a gate finds a defect:

1. **Craft** — use the brief to define the narrative spine, visual hierarchy, slide
   archetypes, and evidence plan before rendering. Record per-slide semantic intent in
   `slide-plan.json`; keep deck-wide typography and layout thresholds in
   `deck-design.json`.
2. **Build** — use the governed deck builder and `visual-spec.json`; keep claims, data,
   titles, and feasible diagrams editable.
3. **Critique** — inspect the rendered slides for hierarchy, clarity, emotional register,
   decision readiness, and whether the design expresses the specific deck rather than a
   generic template.
4. **Audit** — run structural validation, the deterministic linter, visual-spec validation,
   and Office render QA.
5. **Polish** — fix every verified defect, rebuild, and return to Critique. Do not promote
   the deck while any required gate is failing.

Run the native linter after each material build:

```bash
python3 "$PPTX_DESIGN_QUALITY_DIR/scripts/lint_pptx.py" \
  <run-dir>/<deck>-draft.pptx \
  --config <run-dir>/deck-design.json \
  --json --out <run-dir>/qa/pptx-design-lint.json
```

Exit `0` means no unresolved findings, `2` means design findings were detected, and
`1` means the lint run itself failed. `--fast` skips higher-cost image-resolution and
contrast checks for inner-loop builds.

When `deck-design.json` declares a `motion` block, also run the motion linter. Static
contact sheets and Office render QA both inspect resting frames, so neither can see a
transition or a build at all:

```bash
python3 "$PPTX_DESIGN_QUALITY_DIR/scripts/lint_motion.py" \
  <run-dir>/<deck>-draft.pptx \
  --config <run-dir>/deck-design.json \
  --json --out <run-dir>/qa/pptx-motion-lint.json
```

Same exit codes as `lint_pptx.py`. It reads transition and timing XML straight out of
the package rather than calling `officecli`, so the check stays independent of the tool
that authored the motion. Decks with no `motion` block exit `0` and report nothing.

Author motion with `officecli` (`transition` and `animation` elements — see the
`officecli` skill). **`officecli` only persists writes to Windows-side paths.** Given a
WSL path it prints `Updated ...` and leaves the file byte-identical, so run it against
`C:\...` and verify with `lint_motion.py` before trusting any motion edit.

A motion contract is a claim about what the deck does when it plays, and no
resting-frame check can confirm it. On Windows with PowerPoint available, render the
motion and review it:

```bash
python3 "$PPTX_DESIGN_QUALITY_DIR/scripts/motion_contact_sheet.py" \
  <run-dir>/<deck>-draft.pptx --out-dir <run-dir>/qa/motion --json
```

It drives PowerPoint's own `CreateVideo`, samples the result, and tiles it into
`motion-contact-sheet.png`. Exit `0` means a sheet was produced, `3` means blocked,
`1` means bad input. Run `--preflight-only` first to check the environment, and
`--from-video <mp4>` to rebuild the sheet without re-exporting.

Two failure modes it reports rather than dying obscurely:

- **PowerPoint is a single-instance COM server.** Automation attaches to whatever
  instance is already running, so one degraded window — long-running, or titled
  "(Unlicensed Product)" — makes every call fail with `0x80048240` while a freshly
  launched instance works. Preflight names the running instances; close PowerPoint
  and retry before concluding automation is unavailable.
- **PowerPoint cannot open a WSL path.** Decks under WSL are staged to a
  Windows-side temp directory, and paths are resolved to absolute first — a
  relative path is resolved against PowerPoint's own cwd and fails as `E_FAIL`.

Where PowerPoint is unavailable, say the deck's motion is unreviewed and label it
`blocked`; a passing `lint_motion.py` verifies the contract, not the playback.

For an evidence-derived deck (`slide-plan.json`'s `deck.evidence_contract` is non-null),
also run the mechanical claim-vs-evidence check before Office render QA:

```bash
python3 "$PPTX_DESIGN_QUALITY_DIR/scripts/check_claim_evidence.py" \
  <run-dir>/presentation-evidence.json \
  <run-dir>/slide-plan.json \
  --config <run-dir>/deck-design.json
```

This is a fast, deterministic pre-pass — regex number matching against cited evidence
text, not semantic claim verification. It generalizes `video-to-deck`'s Grill-Me
transcript check and the Genspark factual-integrity checklist so any evidence-derived
deck gets a mechanical scan, not only video- or Genspark-sourced ones; it does not
replace either richer procedure. No-ops (exit `0`) for a greenfield deck with no
evidence contract. Waive a finding the same way as a lint finding: add the rule ID to
`qa.ignore_rules` and a reason to `qa.waivers` in `deck-design.json`.

## Shared refinement vocabulary

Use these verbs as scoped operations. Do not interpret them as permission to change facts,
brand identity, or the approved narrative.

| Command | PowerPoint operation |
|---|---|
| `craft` | Brief → spine → visual plan → build → render → iterate |
| `critique` | Review storyline, hierarchy, clarity, resonance, and decision readiness |
| `audit` | Run technical, provenance, accessibility, and deterministic quality checks |
| `polish` | Fix verified defects and repeat all required gates |
| `bolder` | Increase scale, contrast, conviction, and whitespace around the main idea |
| `quieter` | Reduce accents, chrome, pills, shadows, and competing emphasis |
| `distill` | Cut redundant words, repeated evidence, nested containers, and extra messages |
| `typeset` | Repair hierarchy, wrapping, font consistency, and minimum sizes |
| `layout` | Repair grid alignment, rhythm, density, margins, and archetype choice |
| `harden` | Test long text, missing fonts, image crops, citations, export, and aspect ratio |

True narrative judgment stays in `critique`. Do not treat a deterministic heuristic as proof
that an action title has a meaningful “so what.”

For repeated comparison systems—company profiles, partner-lens heatmaps, scorecards, or
scenario tables—layout repetition may be an intentional analytical affordance. Keep the
geometry consistent, vary the evidence rather than the chrome, and document any
`LAYOUT_REPETITION` waiver only after the full contact sheet and real Office render confirm
that the sequence remains legible. Likewise, evaluate `TEXT_TOO_SMALL` against substantive
content separately from configured citations, asset captions, and pagination.

## Reviewed gate

`*-reviewed.pptx` requires all of the following:

- deck context validation passed;
- `visual-spec.json` validation passed;
- the native deck builder's structural validation passed;
- `lint_pptx.py` has no error-severity findings, with warnings resolved or explicitly
  waived in `deck-design.json`;
- when `slide-plan.json`'s `deck.evidence_contract` is non-null, `check_claim_evidence.py`
  has no unresolved `UNSOURCED_NUMBER` findings, with any waivers recorded in
  `deck-design.json`;
- the real Office render was inspected;
- slide-by-slide Critique and Polish were completed;
- delivery status and editability are stated honestly.

HTML-derived decks must also run the repo's pinned Impeccable wrapper against their authored
HTML before PPTX export. Impeccable does not understand native `.pptx`; use `lint_pptx.py`
for the PowerPoint artifact.

## Relationships

| Skill | Pattern | Handoff |
|---|---|---|
| `presentation-source-bundle` | Upstream evidence normalization | `<run>/presentation-evidence.json` |
| `pptx-visual-spec` | Mandatory peer overlay | `<run>/visual-spec.json` |
| `branded-pptx-deck` | Direct native builder | draft/reviewed `.pptx` |
| `genspark-branded-deck` | HTML/hybrid/native builder | source HTML and `.pptx` |
| `marp` | HTML/image-slide builder | source HTML and flattened `.pptx` |
| `officecli` | Downstream render QA | `<run>/qa/officecli/` |

## Dependencies

- `python-pptx` — required by `lint_pptx.py`.
- `jsonschema` — required by `validate_deck_context.py`.
- `Pillow` — required by `derive_template_profile.py` for brand color sampling from
  `--evidence` slide images. Not needed for `--pptx` or `--canvas`.
- Version floors are declared in [`requirements.txt`](requirements.txt) for fresh hosts.
- The selected builder and Office render tooling remain responsible for their own
  dependencies; this overlay does not install packages at runtime.

## Gotchas

- Do not install or invoke the frontend Impeccable skill as a substitute for PPTX linting.
- Do not auto-fix narrative or brand decisions. Report them in Critique for explicit review.
- Do not waive a finding silently. Add the stable rule ID to `qa.ignore_rules` and record a
  reason in `qa.waivers`.
- Do not promote a deck based only on XML validity or a clean python-pptx round trip.
