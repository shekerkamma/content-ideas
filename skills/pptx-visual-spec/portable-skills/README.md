# Portable PPTX skill mirrors

These directories are versioned mirrors of custom skills that previously existed only under
a single machine's `~/.claude/skills` tree. They are stored below the embedded visual-spec
skill so repo skill discovery does not treat them as duplicate top-level skills.

The canonical inventory and destination names live in
`../references/skill-registry.json`. Install or refresh them with:

```bash
python3 skills/pptx-visual-spec/scripts/install_cross_host.py --host all
```

Edit these repo mirrors first. Do not edit an installed symlink as if it were a separate copy.
For copy-only hosts, rerun the installer after edits and audit the result with
`scripts/audit_portability.py --host <host>`.

Non-identical existing directories are never overwritten implicitly. Review the diff, then
use `--replace-unmanaged` to preserve the old directory in the installer's timestamped backup
tree before installing the canonical source.

The complete MIT-licensed `ai-analyst` skill is mirrored here, including its embedded
`export-results` workflow. Its upstream source and license are recorded in the registry and
the mirror's `LICENSE` file.
