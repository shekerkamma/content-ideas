#!/usr/bin/env python3
"""Check that an instruction file's routes resolve to something real.

check_skills.py validates the skills. This validates the *instructions that
point at them* — a CLAUDE.md accumulates routes to skills that were renamed,
moved, or never written, and nothing else catches that. First run over
~/.claude/CLAUDE.md found nine.

Two checks:
  paths    — every `path/to/SKILL.md` in backticks resolves
  triggers — every "When the user types `/x`" resolves to a skill somewhere

Exit 0 clean, 1 blocked (no file to read), 2 findings.

Two traps this encodes, both of which produced wrong answers first time:

  * Declared paths are relative to HOME, not to the repo. Resolving them from
    the repo root reported four working skills as broken.
  * `find -type f` does not follow symlinks, so a symlinked skill counts as
    zero files. That produced a "61 empty directories" finding that was
    entirely an artifact — 325 of them resolved fine. Use os.path.exists,
    which follows.
"""
import argparse, os, pathlib, re, sys

PATH_RE = re.compile(r"`(~?[A-Za-z0-9._/-]*SKILL\.md)`")
TRIGGER_RE = re.compile(r"When the user types `/([a-z0-9-]+)`")

DEFAULT_ROOTS = [
    "~/.claude/skills", "~/.codex/skills",
    "~/content-ideas/skills", "~/content-ideas/.claude/skills",
    "~/content-ideas.local/skill-framework/.agents/skills",
]


def resolve(decl: str) -> pathlib.Path:
    """A declared path is absolute, ~-anchored, or relative to HOME."""
    p = os.path.expanduser(decl)
    return pathlib.Path(p if os.path.isabs(p) else os.path.join(os.path.expanduser("~"), p))


def trigger_resolves(name: str, roots) -> bool:
    for r in roots:
        base = pathlib.Path(os.path.expanduser(r))
        # exists() follows symlinks; a symlinked SKILL.md is a real skill.
        if (base / name / "SKILL.md").exists():
            return True
        if (base / f"{name}.md").exists():
            return True
    cmd = pathlib.Path(os.path.expanduser("~/.claude/commands")) / f"{name}.md"
    return cmd.exists()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", default=["~/.claude/CLAUDE.md"],
                    help="instruction files to check (default: ~/.claude/CLAUDE.md)")
    ap.add_argument("--root", action="append", default=None,
                    help="extra skill root to search for triggers (repeatable)")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    roots = list(DEFAULT_ROOTS) + (a.root or [])
    targets = [pathlib.Path(os.path.expanduser(f)) for f in a.files]
    missing_files = [t for t in targets if not t.is_file()]
    if missing_files:
        for t in missing_files:
            print(f"BLOCKED: no such instruction file: {t}", file=sys.stderr)
        return 1

    findings, n_paths, n_trigs = [], 0, 0
    for t in targets:
        text = t.read_text(encoding="utf-8", errors="replace")
        for decl in sorted(set(PATH_RE.findall(text))):
            n_paths += 1
            if not resolve(decl).exists():
                findings.append(f"{t.name}: declared path does not resolve — {decl}")
        for name in sorted(set(TRIGGER_RE.findall(text))):
            n_trigs += 1
            if not trigger_resolves(name, roots):
                findings.append(f"{t.name}: /{name} resolves to no skill in any root")

    if not a.quiet:
        print(f"{len(targets)} file(s): {n_paths} declared path(s), {n_trigs} trigger(s)")
    if findings:
        sys.stdout.flush()   # stderr is unbuffered; without this the findings
                             # print before the summary they refer to
        print(f"\n{len(findings)} finding(s):", file=sys.stderr)
        for f in findings:
            print(f"  - {f}", file=sys.stderr)
        return 2
    if not a.quiet:
        print("all routes resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
