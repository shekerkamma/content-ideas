#!/usr/bin/env python3
"""
Host compatibility audit for project skills.

Default behavior is warning-first so the repo can adopt the contract incrementally.
Use --strict to return nonzero when warnings are found.
"""
import argparse
import re
import sys
from pathlib import Path

REPO = Path.home() / "content-ideas"

PROJECT_SKILL_DIRS = [
    REPO / ".claude" / "skills",
    REPO / ".agents" / "skills",
    REPO / "skills",
]

GLOBAL_SKILL_DIRS = [
    Path.home() / ".claude" / "skills",
]

HOST_ROOTS = {
    ".claude/skills": "Claude Code",
    ".agents/skills": "Codex/OpenHands",
    "skills": "Repo-routed shared",
}

CLAUDE_FRONTMATTER_FIELDS = {
    "argument-hint",
    "allowed-tools",
    "context",
    "agent",
    "hooks",
    "disable-model-invocation",
    "user-invocable",
    "model",
}

CLAUDE_TOOL_TERMS = {
    "Read",
    "Write",
    "Edit",
    "MultiEdit",
    "Bash",
    "Grep",
    "Glob",
    "AskUserQuestion",
    "Task",
    "WebSearch",
    "WebFetch",
}


def find_skill_files(target=None, include_global=False):
    seen = set()
    skills = []
    skill_dirs = PROJECT_SKILL_DIRS + (GLOBAL_SKILL_DIRS if include_global else [])

    candidate = Path(target).expanduser() if target else None
    if candidate and candidate.exists():
        if candidate.is_dir():
            candidate = candidate / "SKILL.md"
        if candidate.name == "SKILL.md" and candidate.exists():
            return [(candidate.parent.name, candidate)]

    for base in skill_dirs:
        if not base.exists():
            continue
        for skill_md in base.rglob("SKILL.md"):
            if not skill_md.exists():
                continue
            name = skill_md.parent.name
            if target and target != name:
                continue
            real = skill_md.resolve()
            if real in seen:
                continue
            seen.add(real)
            skills.append((name, skill_md))
    return sorted(skills, key=lambda row: (row[0], str(row[1])))


def frontmatter(content):
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return ""
    return match.group(1)


def detect_root(skill_path):
    try:
        rel = skill_path.relative_to(REPO)
    except ValueError:
        if ".claude/skills" in skill_path.as_posix():
            return "~/.claude/skills", "Claude Code"
        return "unknown", "unknown"

    rel_text = rel.as_posix()
    for root, host in HOST_ROOTS.items():
        if rel_text.startswith(root + "/"):
            return root, host
    return "unknown", "unknown"


def has_section(content, heading):
    return bool(re.search(rf"^##\s+{re.escape(heading)}\s*$", content, re.MULTILINE))


def section_text(content, heading):
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s+|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def mirrored_paths(skill_name):
    paths = []
    for base in PROJECT_SKILL_DIRS:
        candidate = base / skill_name / "SKILL.md"
        if candidate.exists():
            paths.append(candidate)
    return paths


def is_non_claude_project_root(path):
    try:
        rel = path.relative_to(REPO).as_posix()
    except ValueError:
        return False
    return rel.startswith(".agents/skills/") or rel.startswith("skills/")


def audit_skill(skill_name, skill_path):
    try:
        content = skill_path.read_text(encoding="utf-8")
    except OSError as exc:
        return {
            "skill": skill_name,
            "path": skill_path,
            "root": "unknown",
            "host": "unknown",
            "warnings": [],
            "failures": [f"could not read skill file: {exc}"],
        }
    fm = frontmatter(content)
    host_section = section_text(content, "Host Compatibility")
    root, current_host = detect_root(skill_path)

    warnings = []
    failures = []

    if not has_section(content, "Host Compatibility"):
        warnings.append("missing ## Host Compatibility section")

    fm_fields = set(re.findall(r"^([a-zA-Z0-9_-]+):", fm, re.MULTILINE))
    claude_fields = sorted(fm_fields & CLAUDE_FRONTMATTER_FIELDS)
    if claude_fields and "Host Compatibility" not in content:
        warnings.append(
            "Claude-specific frontmatter without host compatibility notes: "
            + ", ".join(claude_fields)
        )

    tool_terms = sorted(term for term in CLAUDE_TOOL_TERMS if re.search(rf"`?{term}`?", content))
    if tool_terms and "Tool Mapping" not in host_section and "Host Compatibility" in content:
        warnings.append("Claude tool terms found but no Tool Mapping subsection")

    lower = content.lower()
    is_strategy_research = any(
        token in lower
        for token in ("strategy", "research", "deck", "pipeline", "gbrain", "web search")
    )
    if is_strategy_research and "Source / Tool Order" not in host_section:
        warnings.append("strategy/research-style skill missing Source / Tool Order")

    declares_codex = re.search(r"codex[^.\n]*:\s*yes", host_section, re.IGNORECASE)
    declares_openhands = re.search(r"openhands[^.\n]*:\s*yes", host_section, re.IGNORECASE)
    if (declares_codex or declares_openhands) and root == ".claude/skills":
        mirrors = mirrored_paths(skill_name)
        has_non_claude = any(is_non_claude_project_root(p) for p in mirrors)
        if not has_non_claude and "AGENTS" not in host_section:
            warnings.append("declares Codex/OpenHands support but no mirror or AGENTS routing is documented")

    if "skill-creator" in content and "Alternative / Peer" not in content:
        warnings.append("mentions skill-creator but does not document it as a peer/alternative")

    return {
        "skill": skill_name,
        "path": skill_path,
        "root": root,
        "host": current_host,
        "warnings": warnings,
        "failures": failures,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", help="skill name, skill dir, or SKILL.md path")
    parser.add_argument("--include-global", action="store_true", help="also scan ~/.claude/skills")
    parser.add_argument("--strict", action="store_true", help="return nonzero on warnings")
    args = parser.parse_args()

    skills = find_skill_files(args.target, include_global=args.include_global)
    if not skills:
        print("No matching skills found.")
        return 1

    print(f"Found {len(skills)} skill(s) to audit.\n")
    print("=" * 70)
    print("HOST COMPATIBILITY AUDIT")
    print("=" * 70)

    total_warnings = 0
    total_failures = 0

    for skill_name, skill_path in skills:
        result = audit_skill(skill_name, skill_path)
        warnings = result["warnings"]
        failures = result["failures"]
        total_warnings += len(warnings)
        total_failures += len(failures)

        status = "FAIL" if failures else ("WARN" if warnings else "PASS")
        print(f"  {status:4}  {skill_name} [{result['host']}: {result['root']}]")
        print(f"        {skill_path}")
        for issue in failures:
            print(f"        x {issue}")
        for issue in warnings:
            print(f"        ! {issue}")

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Skills audited : {len(skills)}")
    print(f"  Failures       : {total_failures}")
    print(f"  Warnings       : {total_warnings}")

    if total_failures:
        return 1
    if args.strict and total_warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
