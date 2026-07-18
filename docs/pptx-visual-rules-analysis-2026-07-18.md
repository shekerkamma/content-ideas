# PPTX visual-rules analysis — 2026-07-18

## Decision

Use the vault sourcing gate as the policy foundation, but make the shared
`pptx-visual-spec` overlay the canonical cross-skill contract. The vault remains the strongest
deck implementation; the overlay prevents its rules from being re-copied differently into
video, branded, Genspark, research, and specialist deck workflows.

## Conflicts found

| Area | Existing conflict | Resolution |
|---|---|---|
| Exact evidence vs data | Vault says data routes native first; video fidelity needs exact UI/terminal pixels | Test whether exact appearance/state is evidence first; ordinary underlying data remains native |
| Authored graphic vs generated image | Several skills call both “generated” | Reserve `author-*` for deterministic HTML/SVG/React and `image-model` for model-created raster imagery |
| Codex subscription vs OmniRoute | Older skills treat `codex/gpt-5.5` OmniRoute limits as Codex image availability | Built-in `image_gen` is a separate primary route; provider status applies only to an explicit provider adapter |
| Model identity | Orchestration model and image engine are conflated | Record both separately; image engine remains `null` when the tool does not report it |
| HTML/SVG status | Some skills describe code rendering as a fallback | Deterministic HTML/SVG is the default for any new text-bearing raster asset |
| Flattening | Native deck rules are incorrectly interpreted as “zero images” | Images may occupy regions inside native slides; only full-slide flattening is banned unless the output mode explicitly permits it |
| Per-slide classification | A slide is assigned one route despite hybrid composition | Classify every meaningful visual region; a slide may combine routes |
| QA | Provider preflight is treated as image success | Require actual asset inspection and real Office render of the placed crop |

## Canonical route vocabulary

`extract`, `place-asset`, `native`, `author-html`, `author-svg`, `author-react`,
`image-model`, and `none`.

## Propagation tiers

1. Direct PPTX builders must read the contract and emit/validate `visual-spec.json`.
2. Deck orchestrators must pass the visual spec to their selected direct builder.
3. Source/preview generators such as Genspark may retain their native behavior, but their
   recovered assets must be classified through this contract before a final PPTX rebuild.
4. QA-only skills validate the resulting deck; they do not decide visual routes.

## Implemented

- Added canonical embedded skill: `skills/pptx-visual-spec/`.
- Added shared JSON Schema and validator with tests for native, exact extraction, and
  image-model constraints.
- Synchronized the canonical sourcing rules byte-for-byte into `ai-graphics` and both vault
  host copies.
- Updated the vault runtime registry to separate ready built-in Codex `image_gen` from the
  optional/limited OmniRoute adapter.
- Pinned 30 governed direct builders, modifiers, and orchestrators through
  `references/skill-registry.json`.
- Installed `pptx-visual-spec` symlinks for repo agent discovery, Claude Code, Codex, and the
  global agent host.
- Added `audit_skill_pins.py`; current result: 30 governed skills, all pinned, no stale route
  status.

## Cross-machine portability

- Replaced machine-specific paths in the governed registry with repo-relative sources,
  host-root environment variables, and optional `PPTX_VAULT_ROOT` resolution.
- Added repo mirrors for 15 PPTX-relevant custom skills that previously lived only under
  `~/.claude/skills`, including the complete MIT-licensed `ai-analyst` distribution. Its embedded
  `export-results` workflow no longer depends on an untracked global installation.
- Added `install_cross_host.py` for Claude, Codex, global agent, and project-agent roots.
  POSIX installs use relative symlinks by default; copy-only hosts use managed copies.
- The installer refuses unmanaged destinations. `--adopt-identical` is limited to content-
  identical directories, with caches and platform metadata excluded from comparison.
- Added `audit_portability.py` and installation tests. The source audit currently reports 30
  portable sources with no hardcoded user or WSL paths.
- Added an external-capability contract for Canva, Google Slides, Gamma, and Genspark. Host
  authorization remains local, while every absent connector now has a declared portable
  fallback and a diagnostic command.

## Deliberate exclusions

- `officecli-qa`, PDF utilities, presentation accessibility, and other QA/export helpers do
  not decide visual routes; they validate or transform an already specified artifact.
- Canva, Google Slides, Gamma, and the Genspark connector are external creation/reference
  surfaces. Their internal generation policy cannot be edited locally; the shared contract is
  enforced when their output is recovered, packaged, or rebuilt into the final PPTX.
