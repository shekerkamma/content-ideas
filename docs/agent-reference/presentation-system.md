# Presentation system

<!-- Moved out of CLAUDE.md so it only loads when needed. Read on demand. -->

- `skills/present/SKILL.md` is the single public router for presentation work.
- Keep output engines distinct: native PPTX uses `branded-pptx-deck`, controlled
  existing-PPTX edits use `pptx-toolkit`, HTML uses `presentation`, hosted Genspark uses
  `genspark-slides` plus `genspark-branded-deck`, and Markdown slides use `marp`.
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

