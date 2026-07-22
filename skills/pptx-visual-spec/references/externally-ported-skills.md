# Externally-ported skills

`install_cross_host.py` only installs skills registered in `skill-registry.json`
with a repo-relative `source`, and it explicitly skips `ownership: "external"`
entries (`select_entries` filters `e["ownership"] != "external"`). Two skills in
the client-ready PPTX chain fall outside that automation entirely. Track them
here so a canonical-source change doesn't silently drift on the hosts below —
this file is the reminder the installer cannot give you.

## vault-presales-pptx-pipeline

- **Canonical source:** `C:\Users\sheke\Documents\hyundai-ai-vault\.claude\skills\vault-presales-pptx-pipeline`
  (a separate vault repo, not this one — hence `ownership: "external"`).
- **Registry entry:** `root_env: PPTX_VAULT_ROOT`, `source_relative`, `optional: true`.
  This lets a consumer skill *resolve* the vault path at runtime; it does not
  make the installer copy it anywhere.
- **Manually ported copies** (as of 2026-07-21, replacing a fabricated
  Kimi-K3-image-generation SKILL.md that was a live routing hazard):
  - `~/.claude/skills/vault-presales-pptx-pipeline` — symlink to the canonical vault path.
  - `~/.codex/skills/vault-presales-pptx-pipeline` — symlink to the canonical vault path.
  - `C:\Users\sheke\.gemini\config\skills\vault-presales-pptx-pipeline` — real copy + `.ported-from`.
  - `D:\New folder\Antigravity-test\antigravity-skills\.agents\skills\vault-presales-pptx-pipeline` — real copy + `.ported-from`.
  - `C:\Users\sheke\.gemini\antigravity\skills\vault-presales-pptx-pipeline` — real copy + `.ported-from`.
- **Refresh after any canonical change** (the two Windows copies without a symlink):
  ```bash
  SRC="/mnt/c/Users/sheke/Documents/hyundai-ai-vault/.claude/skills/vault-presales-pptx-pipeline"
  for DST in \
    "/mnt/c/Users/sheke/.gemini/config/skills/vault-presales-pptx-pipeline" \
    "/mnt/d/New folder/Antigravity-test/antigravity-skills/.agents/skills/vault-presales-pptx-pipeline" \
    "/mnt/c/Users/sheke/.gemini/antigravity/skills/vault-presales-pptx-pipeline"; do
    cp -r "$SRC/SKILL.md" "$SRC/references" "$SRC/scripts" "$SRC/assets" "$DST/"
  done
  ```
- **Verify no copy has regressed to inventing capabilities:**
  ```bash
  grep -ril "kimi" "/mnt/c/Users/sheke/.gemini/config/skills/vault-presales-pptx-pipeline" \
    "/mnt/d/New folder/Antigravity-test/antigravity-skills/.agents/skills/vault-presales-pptx-pipeline" \
    "/mnt/c/Users/sheke/.gemini/antigravity/skills/vault-presales-pptx-pipeline" 2>/dev/null || echo "clean"
  ```
  A hit means a copy claims Kimi does something it cannot (image generation) —
  see `skills/image-generation-router/SKILL.md` "Kimi K3 Helper (Not A Provider)".

## ai-graphics

- **Canonical source:** `~/.claude/skills/ai-graphics` (WSL-global; no copy lives in
  this repo, so it cannot be added to `skill-registry.json` — the registry's
  `source` field is repo-relative by construction).
- **Why it matters here:** it is the default HTML/SVG-to-screenshot raster route
  that `vault-presales-pptx-pipeline` and `image-generation-router` both depend on
  for anything with text (see `visual-tool-routing.md` "HTML/SVG → screenshot is
  the default raster route").
- **Manually ported copies** (2026-07-21, `examples/` omitted to keep the copy lean):
  - `C:\Users\sheke\.gemini\config\skills\ai-graphics`
  - `C:\Users\sheke\.gemini\antigravity\skills\ai-graphics`
- **Refresh after any canonical change:**
  ```bash
  for ROOT in "/mnt/c/Users/sheke/.gemini/config/skills" "/mnt/c/Users/sheke/.gemini/antigravity/skills"; do
    (cd ~/.claude/skills/ai-graphics && cp -r SKILL.md assets deck-image-routing.md reference.md \
      scripts templates troubleshoot.md visual-sourcing-rules.md "$ROOT/ai-graphics/")
  done
  ```

## officecli

Deliberately **not** ported to `antigravity` / `gemini-config` — its CLI runtime is
unverified on Windows-native (see the `note` field on its `skill-registry.json`
entry). Antigravity PPTX QA falls back to preview contact sheets until that CLI
is verified there; do not copy it across as a shortcut.
