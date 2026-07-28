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

Initialize them without overwriting existing files:

```bash
python3 "$PPTX_DESIGN_QUALITY_DIR/scripts/init_deck_context.py" \
  --run <run-dir> --title "<deck title>"
```

Tailor both files, then validate:

```bash
python3 "$PPTX_DESIGN_QUALITY_DIR/scripts/validate_deck_context.py" \
  <run-dir>/deck-brief.md <run-dir>/deck-design.json
```

The JSON contract is defined in
[`references/deck-design-schema.json`](references/deck-design-schema.json).
Stable native rule IDs and their meanings are listed in
[`references/rules.md`](references/rules.md).

## Build loop

Apply these stages in order and loop back whenever a gate finds a defect:

1. **Craft** — use the brief to define the narrative spine, visual hierarchy, slide
   archetypes, and evidence plan before rendering.
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

## Reviewed gate

`*-reviewed.pptx` requires all of the following:

- deck context validation passed;
- `visual-spec.json` validation passed;
- the native deck builder's structural validation passed;
- `lint_pptx.py` has no error-severity findings, with warnings resolved or explicitly
  waived in `deck-design.json`;
- the real Office render was inspected;
- slide-by-slide Critique and Polish were completed;
- delivery status and editability are stated honestly.

HTML-derived decks must also run the repo's pinned Impeccable wrapper against their authored
HTML before PPTX export. Impeccable does not understand native `.pptx`; use `lint_pptx.py`
for the PowerPoint artifact.

## Relationships

| Skill | Pattern | Handoff |
|---|---|---|
| `pptx-visual-spec` | Mandatory peer overlay | `<run>/visual-spec.json` |
| `branded-pptx-deck` | Direct native builder | draft/reviewed `.pptx` |
| `genspark-branded-deck` | HTML/hybrid/native builder | source HTML and `.pptx` |
| `marp` | HTML/image-slide builder | source HTML and flattened `.pptx` |
| `officecli` | Downstream render QA | `<run>/qa/officecli/` |

## Dependencies

- `python-pptx` — required by `lint_pptx.py`.
- `jsonschema` — required by `validate_deck_context.py`.
- Version floors are declared in [`requirements.txt`](requirements.txt) for fresh hosts.
- The selected builder and Office render tooling remain responsible for their own
  dependencies; this overlay does not install packages at runtime.

## Gotchas

- Do not install or invoke the frontend Impeccable skill as a substitute for PPTX linting.
- Do not auto-fix narrative or brand decisions. Report them in Critique for explicit review.
- Do not waive a finding silently. Add the stable rule ID to `qa.ignore_rules` and record a
  reason in `qa.waivers`.
- Do not promote a deck based only on XML validity or a clean python-pptx round trip.
