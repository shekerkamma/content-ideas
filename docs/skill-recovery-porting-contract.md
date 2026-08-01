# Skill Recovery and Porting Contract

This contract governs investigation, recovery, and cross-host installation of
Claude Code and Codex skills. Its purpose is to prevent two recurring errors:
mistaking a project-only search for a host-wide integrity audit, and replacing
a customized skill with a related but incompatible upstream project.

## Canonical sources

The repository is the portable source of truth for these recovered skills:

| Skill | Canonical path | Confirmed recovery source |
| --- | --- | --- |
| `docx` | `skills/docx/` | Windows Hermes productivity skill |
| `pdf` | `skills/pdf/` | Windows Hermes productivity skill |
| `improve` | `skills/improve/` | Restored repo agent skill |
| `storm-research` | `skills/storm-research/` | Matching local archive of the customized workflow |

Global paths such as `~/.claude/skills/` and `~/.codex/skills/` are installation
targets. They are not canonical sources and must not be the only surviving copy.

## Search scope

Before asserting that a skill is missing or corrupted, enumerate and search all
relevant roots, including hidden and ignored files:

1. the full repository;
2. repo-local `skills/`, `.agents/`, `.claude/`, and plugin trees;
3. `~/.claude/skills/`, `~/.codex/skills/`, archives, and symlink targets;
4. adjacent repositories named by instructions or manifests;
5. mounted host application data, including Windows Hermes Desktop when it is
   the known source.

Report exact resolved roots, exclusions, and permission gaps. A count is valid
only for its stated scope.

## Detection and sourcing are different stages

Local corruption detection is performed locally. Inspect expected text/source
files for NUL bytes, parsing failures, truncated content, invalid frontmatter,
and syntax errors. Use Git integrity and status checks when the source is a Git
checkout. Exclude expected binary assets, Git objects, caches, and bytecode.

Web research cannot inspect the local filesystem. Exa, You.com, and Livecrawl
are recovery-sourcing tools: use them to find official repositories, release
artifacts, documentation, or historical copies after local detection identifies
what needs replacement.

Livecrawl Level 2 is a two-stage contract:

1. discovery returns candidate URLs through the configured search backend;
2. extraction fetches fresh contents for selected URLs through the configured
   extraction backend.

Record the backend and status for both stages. Search-only output, cached
snippets, or an unverified extraction is not a successful Level 2 run.

## Credentials and host configuration

Research credentials belong to the host application configuration. Do not add
API keys to this repository or create project-level secret copies. WSL wrappers
may read the Windows Hermes Desktop environment through its `/mnt/c` mount at
runtime. They must not print secret values. Host-global wrappers belong under
the user's global tool/skill configuration, not under this project.

## Recovery procedure

1. Identify exact corrupted files and validate the claim.
2. Locate the strongest matching source: byte-identical archive, canonical repo
   copy, authoritative upstream, then evidence-backed reconstruction.
3. Compare the candidate skill's name, triggers, inputs, outputs, references,
   and workflow to the installed customization.
4. Stage the entire candidate directory outside the installation target.
5. Remove generated `__pycache__/` and `*.pyc` files from the portable copy.
6. Run `bash scripts/verify-recovery-skills.sh` against the repo copy.
7. Back up the installed skill as `<name>.corrupt-backup-<UTC timestamp>`.
8. Replace only the named skill directory and keep the backup recoverable.
9. Compare the installed directory with the staged copy and rerun syntax and
   content validation.
10. Synchronize Codex discovery using `bash scripts/sync-codex-skills.sh` when
    global Claude Code installations change.

Never silently substitute a different workflow. In particular, the customized
`storm-research` HTML-report workflow is not equivalent to the upstream
`storm` Markdown workflow; recovery must preserve the customized interface.

## Porting rules

- Port complete directories, not only files previously reported as corrupt.
- Preserve licenses and source attribution.
- Keep filenames, relative imports, reference links, and templates intact.
- Never port `.env` files, tokens, caches, bytecode, backups, or machine-local
  absolute paths containing credentials.
- Commit the canonical repo copies and this contract together so another host
  can reconstruct the installation without relying on the repaired machine.

## Verification gate

Run:

```bash
bash scripts/verify-recovery-skills.sh
git diff --check
```

The verifier requires all four skill manifests, rejects NUL bytes and generated
Python artifacts, compiles Python sources using a temporary bytecode cache, and
checks the known-good hash of the customized STORM report template.
