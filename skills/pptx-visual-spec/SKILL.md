---
name: pptx-visual-spec
description: EMBEDDED behavioral overlay for every skill that creates, rebuilds, exports, or materially edits a PowerPoint deck. Establishes one per-visual routing contract for exact reference extraction, native editable content, authored HTML/SVG/React assets, approved assets, and text-free image generation. Direct deck skills must read this before rendering and must emit a validated visual-spec.json.
category: Business Automation
---

# PPTX Visual Specification

This is the shared visual contract for all PowerPoint-producing workflows. It is based on
the stronger `vault-presales-pptx-pipeline` sourcing gate and incorporates the verified
Codex subscription-backed image-generation path.

## Required Use

Before rendering any slide deck:

1. Read [references/visual-sourcing-rules.md](references/visual-sourcing-rules.md).
   For hosted presentation products, also read
   [references/external-capabilities.md](references/external-capabilities.md).
2. Classify every meaningful visual region, not merely every slide.
3. Write `<run>/visual-spec.json` using
   [references/visual-spec-schema.json](references/visual-spec-schema.json).
4. Validate it before build and again before promoting the deck to `reviewed`:

```bash
python3 skills/pptx-visual-spec/scripts/validate_visual_spec.py \
  <run>/visual-spec.json
```

5. Keep the final deck shell native unless the selected deck skill explicitly declares an
   image-per-slide output. Even then, never send text or claims to an image model.

## Precedence

The shared contract overrides duplicated visual-routing prose or dated provider status in a
downstream deck skill. Deck-specific rules may tighten editability, branding, layout, or QA,
but may not weaken evidence fidelity, provenance, text safety, or generated-image limits.

## Required Handoff

Every direct PPTX builder consumes:

- `visual-spec.json` — routing and provenance per visual region;
- source assets and editable authored sources referenced by the spec;
- prompt files for generated assets;
- QA evidence proving crop, legibility, background match, and evidence separation.

## Skill Relationships

### Category
Business Automation

### Dependencies
- `ai-graphics` — executes HTML/SVG screenshots and generated raster routes.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `vault-presales-pptx-pipeline` | Behavioral source | always | vault-grade extract/author rules incorporated here |
| `branded-pptx-deck` | Behavioral overlay | direct native PPTX build | `<run>/visual-spec.json` |
| `video-to-deck` | Behavioral overlay | video-derived PPTX | `<run>/visual-spec.json` |
| `genspark-branded-deck` | Behavioral overlay | image/hybrid PPTX | `<run>/visual-spec.json` |
| `ai-graphics` | Sequential downstream | authored/generated raster required | `.html/.svg/.jsx` + `.png`, or prompt + generated `.png` |

## Host Compatibility

- Canonical source: `skills/pptx-visual-spec/` in the `content-ideas` repository.
- Install the contract and every governed repo/mirrored skill with the repo-tracked installer:

```bash
python3 skills/pptx-visual-spec/scripts/install_cross_host.py --host all
```

- Use `--mode copy` for Windows-native hosts or bundles that cannot follow symlinks.
- Use `--dry-run` before changing an existing host. Unmanaged destinations are refused;
  `--adopt-identical` is allowed only when the existing directory hashes to the canonical
  repo source.
- Resolve deliberate drift with `--replace-unmanaged`; the displaced directory is backed up
  under `~/.local/state/content-ideas/pptx-skill-backups/` before replacement.
- Override host locations with `CLAUDE_SKILLS_HOME`, `CODEX_SKILLS_HOME`, and
  `AGENTS_SKILLS_HOME`. Set `PPTX_VAULT_ROOT` only when auditing the optional vault skill.
- Audit repo sources with `audit_portability.py`; add `--host claude`, `--host codex`, or
  `--host agents` to verify installed state.
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
