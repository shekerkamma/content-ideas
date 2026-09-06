# Cross-host skill port report

Date: 2026-08-09

## Scope

Searched and resolved skills from:

- `/home/sheke/.claude/skills`
- `/home/sheke/.codex/skills`
- `/home/sheke/content-ideas/skills`
- `/home/sheke/content-ideas/portable-skills`
- `/home/sheke/content-ideas/.claude/skills`
- `/home/sheke/content-ideas/.agents/skills`
- `/home/sheke/content-ideas/plugins`
- referenced sources under `/home/sheke/agent-skills`, `/home/sheke/compound-engineering-plugin`, `/home/sheke/.agents/skills`, `/mnt/c/Users/sheke/.claude/skills`, `/mnt/c/Users/sheke/claude-skills-bundle/skills`, and `/mnt/c/Users/sheke/Documents/hyundai-ai-vault/.agents/skills`

## Result

- Valid top-level Claude-root skills detected: 296
- Unique host skill names represented by the import manifest: 310
- Existing repository skill copies preserved: 37
- Host/recovered skills copied: 273
- Additional repository-only skills: 4
- Active repository skills after port: 314
- Codex validation: 314 pass, 0 fail
- Copied resource comparisons: 273 pass, 0 fail under declared exclusions
- NUL-bearing text/source files: 0
- Repository skill-tree size: approximately 106 MB

Codex-target physical copies took precedence over same-name Claude copies.
Existing repository copies took precedence over both host installations.
Thirteen broken host symlinks were recovered from `portable-skills/`; two other
broken-link names already had active repository copies.

## Exclusions

The port excludes generated or host-private state:

- nested `.git/`
- `node_modules/`
- `__pycache__/` and `*.pyc`
- secret `.env` files

One configured secret file was detected and excluded:
`social-media-team/.env`. Only its variable names were inspected; its values
were not copied or reported.

## Portability status

All skills are now syntactically discoverable by Codex. Claude-specific
frontmatter was moved under `metadata.legacy-frontmatter` while skill bodies
and bundled resources were preserved. The portability audit records 160 skills
that mention at least one host-specific path, Claude interaction name, or
platform-specific alternative. `AGENTS.md` defines the cross-host translation
rules for those references. Absolute `/home/sheke` dependencies in executable
paths were removed from the active portable copies.

## Evidence

- `manifest.tsv` — source precedence and destination for every host skill name
- `exclusions.tsv` — broken links and secret/runtime exclusions
- `validation.tsv` — Codex validator result for all 314 active skills
- `resource-integrity.tsv` — resource comparison for copied skills
- `frontmatter-normalization.tsv` — normalization actions
- `portability-findings.tsv` — remaining host-specific references

Codex Cloud verification task:
https://chatgpt.com/codex/tasks/task_e_6a7802272da08327be228e1fcbbb61fd

Cloud result: commit `7f3d6024a77ee5232707e81bb6ac54bf77311ac9`
was checked out; all 314 immediate skill bundles had valid YAML frontmatter and
the requested representative resources; forbidden runtime/secret artifacts
were absent. Verdict: `CLOUD_SKILL_PORT=PASS`.

## Integrity caveat

`git fsck --no-dangling` was clean for the current repository and the external
`gstack` source. `/home/sheke/agent-skills` has an unrelated invalid tag ref
(`refs/tags/0.6.0`) and a dirty working tree; its referenced skill directories
were copied read-only and validated individually rather than treating that
external repository as globally healthy.
