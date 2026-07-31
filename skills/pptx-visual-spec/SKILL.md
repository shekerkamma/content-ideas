---
name: pptx-visual-spec
description: EMBEDDED behavioral overlay for every skill that creates, rebuilds, exports, or materially edits a PowerPoint deck. Establishes one per-visual routing contract for exact reference extraction, native editable content, authored HTML/SVG/React assets, approved assets, and text-free image generation. Direct deck skills must read this before rendering and must emit a validated visual-spec.json.
---

# PPTX Visual Specification

This is the shared visual contract for all PowerPoint-producing workflows. It is based on
the stronger `vault-presales-pptx-pipeline` sourcing gate and incorporates the verified
Codex subscription-backed image-generation path.

## Required Use

Before rendering any slide deck:

1. Read the sibling `pptx-design-quality` skill, initialize and validate
   `<run>/deck-brief.md` plus `<run>/deck-design.json`, then read
   [references/visual-sourcing-rules.md](references/visual-sourcing-rules.md).
   For hosted presentation products, also read
   [references/external-capabilities.md](references/external-capabilities.md).
   For video-derived Genspark work, read the canonical
   [Genspark video-to-deck contract](references/genspark-video-deck-contract.md).
2. Classify every meaningful visual region, not merely every slide.
3. For a rebuild, source presentation, or video-derived deck, use
   `presentation-source-bundle` to write `<run>/presentation-evidence.json`, then tailor
   `<run>/slide-plan.json` from `assets/slide-plan.template.json`. Greenfield decks with no
   source artifact still require `slide-plan.json`, but set `deck.evidence_contract` to
   `null` and validate the slide plan directly against `references/slide-plan-schema.json`.
4. Write `<run>/visual-spec.json` using
   [references/visual-spec-schema.json](references/visual-spec-schema.json).
5. Validate it before build and again before promoting the deck to `reviewed`:

```bash
python3 skills/pptx-visual-spec/scripts/validate_visual_spec.py \
  <run>/visual-spec.json
```

   When a source evidence contract exists, also validate the semantic chain:

```bash
python3 skills/pptx-visual-spec/scripts/validate_presentation_contracts.py \
  <run>/presentation-evidence.json \
  <run>/slide-plan.json \
  <run>/visual-spec.json \
  --check-files
```

6. Keep the final deck shell native unless the selected deck skill explicitly declares an
   image-per-slide output. Even then, never send text or claims to an image model.

## Precedence

The shared contract overrides duplicated visual-routing prose or dated provider status in a
downstream deck skill. Deck-specific rules may tighten editability, branding, layout, or QA,
but may not weaken evidence fidelity, provenance, text safety, or generated-image limits.

## Required Handoff

Every direct PPTX builder consumes:

- `presentation-evidence.json` — source slides, deterministic text, transcript segments,
  frames, checksums, and rights status for source-derived decks;
- `slide-plan.json` — claims, evidence references, audience job, visual IDs, speaker notes,
  and accessibility intent per slide;
- `visual-spec.json` — routing and provenance per visual region;
- source assets and editable authored sources referenced by the spec;
- prompt files for generated assets;
- QA evidence proving crop, legibility, background match, and evidence separation.

## Skill Relationships

### Category
Business Automation

### Dependencies
- `pptx-design-quality` — supplies per-deck design context, refinement vocabulary, and
  deterministic native-PPTX linting.
- `ai-graphics` — executes HTML/SVG screenshots and generated raster routes.
- `image-generation-router` — selects built-in OpenAI first and routes explicit or
  fallback Gemini generation through CLIProxyAPI without silent model substitution.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `presentation-source-bundle` | Sequential upstream | rebuild, source presentation, or video-derived deck | `<run>/presentation-evidence.json` |
| `pptx-design-quality` | Behavioral peer overlay | every deck build | `<run>/deck-brief.md`, `<run>/deck-design.json`, and lint report |
| `vault-presales-pptx-pipeline` | Behavioral source | always | vault-grade extract/author rules incorporated here |
| `branded-pptx-deck` | Behavioral overlay | direct native PPTX build | `<run>/visual-spec.json` |
| `video-to-deck` | Behavioral overlay | video-derived PPTX | `<run>/visual-spec.json` |
| `genspark-branded-deck` | Behavioral overlay | image/hybrid PPTX | `<run>/visual-spec.json` |
| `genspark-slides` | Hosted upstream | Genspark generation/recovery | `<run>/genspark-handoff.json` |
| `ai-graphics` | Sequential downstream | authored/generated raster required | `.html/.svg/.jsx` + `.png`, or prompt + generated `.png` |
| `image-generation-router` | Behavioral overlay | `image-model` route selected | prompt + generated image + provenance JSON |

## Host Compatibility

- Canonical source: `skills/pptx-visual-spec/` in the `content-ideas` repository.
- Install the contract and every governed repo/mirrored skill with the repo-tracked installer:

```bash
python3 skills/pptx-visual-spec/scripts/install_cross_host.py --host all
```

- Use `--mode copy` for Windows-native hosts or bundles that cannot follow symlinks.
- Antigravity is a first-class copy-only target. Install both Windows roots with
  `--host antigravity --host gemini-config --windows-home /mnt/c/Users/<name>`; alternatively
  set `WINDOWS_USER_HOME`, `ANTIGRAVITY_SKILLS_HOME`, or `GEMINI_SKILLS_HOME`.
- Use repeatable `--skill <registered-name>` arguments for a scoped install or audit when
  only one governed skill should be refreshed.
- Use `--dry-run` before changing an existing host. Unmanaged destinations are refused;
  `--adopt-identical` is allowed only when the existing directory hashes to the canonical
  repo source.
- Resolve deliberate drift with `--replace-unmanaged`; the displaced directory is backed up
  under `~/.local/state/content-ideas/pptx-skill-backups/` before replacement.
- Override host locations with `CLAUDE_SKILLS_HOME`, `CODEX_SKILLS_HOME`, and
  `AGENTS_SKILLS_HOME`. Set `PPTX_VAULT_ROOT` only when auditing the optional vault skill.
- Audit repo sources with `audit_portability.py`; add `--host claude`, `--host codex`, or
  `--host agents` to verify installed state.
- The Genspark/video chain is explicitly installed to Claude, Codex, global agents,
  project agents, Antigravity, and Gemini Config. Port the contract and all three
  participating skills together:

```bash
python3 skills/pptx-visual-spec/scripts/install_cross_host.py \
  --host all \
  --skill pptx-visual-spec \
  --skill video-to-deck \
  --skill genspark-slides \
  --skill genspark-branded-deck
```
- The complete `ai-analyst` distribution is a repo-tracked mirror. Hosted connectors are
  capability-checked and have local fallbacks; authentication remains host-local by design.

## Gotchas

- **Exact-state evidence beats redraw:** a real UI, terminal, document figure, or supplied
  artwork whose appearance matters routes to `extract`, even when pixels contain text.
- **Ordinary data stays native:** a number appearing in a source document does not make the
  source screenshot mandatory when the task is to communicate the data editably.
- **Generated does not mean authored:** deterministic HTML/SVG/React assets use `author-*`;
  only model-created organic imagery uses `image-model`.
- **Do not invent an image engine name:** record it only when the executing tool reports it.
