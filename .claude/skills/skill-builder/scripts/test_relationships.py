#!/usr/bin/env python3
"""
Batch 3 — Relationship Graph Consistency Tests

Checks:
1. Named skill existence — every skill referenced in a Relationships table exists
2. Bidirectional consistency — if A declares B as downstream, B should declare A as upstream
3. Handoff artifact plausibility — no hardcoded machine-specific paths
4. No "none" / placeholder skill names in tables
"""
import os
import re
import sys
from pathlib import Path

SKILL_DIRS = [
    Path.home() / ".claude" / "skills",
    Path.home() / "content-ideas" / ".claude" / "skills",
    Path.home() / "content-ideas" / "skills",
]

# Skills that were actually audited in the June 2026 audit pass — must have Relationships section
AUDITED_SKILLS = {
    "content-research", "ai-strategy-researcher", "ai-strategy-brief",
    "grill-me", "plaid", "karpathy-guidelines", "branded-pptx-deck",
    "mkt-visual-identity", "mkt-brand-voice", "presales-deal-prep",
    "vertical-scorer", "office-hours", "plan-ceo-review",
    "graphify", "social-media-team", "research-to-deck", "learn-anything",
    "competitive-intel-sprint", "watch",
    "architecture-to-everything", "drawio", "architecture-presentation",
    "workflow-visualizer", "notebooklm", "explainer-graphic",
    "ai-use-cases-consultant", "openhands-niche-agency", "saas-replacement-auditor",
    "ai-feature-integrator", "founders-build-stack", "ikigai", "ikigai-gamma-slidedeck",
    "qa", "investigate", "ship", "retro", "marp", "gcc-roadmap",
    "video-to-deck", "landing-page-gen", "presentation-accessibility", "second-brain",
    "strategy-consulting", "solution-delivery", "ai-transformation",
    "engagement-management", "continuous-improvement",
    "session-handoff", "tool-humanizer", "cheat", "guard", "careful",
    "health", "checkpoint", "00-account-briefing", "ai-strategy-council",
    "analytics-to-comms", "affiliate-workflow",
    "difficult-conversation-prep",
}


# Broader set of skills known to exist — used only for existence-check warnings
# (referenced in tables but not required to have Relationships sections themselves)
KNOWN_SKILLS = AUDITED_SKILLS | {
    "claude-code-director", "skill-builder", "code-reviewer", "deep-research",
    "pipeline-runner", "content-ideas",
    "plan-eng-review", "plan-design-review", "plan-devex-review",
    "gamma", "excalidraw", "gbrain",
    "ai-analyst", "openkb",
}

# Placeholder / invalid skill names that should not appear
BAD_SKILL_NAMES = {"none", "n/a", "tbd", "—", "-", "", "skill-name", "your-skill"}

# Hardcoded path patterns that should be env vars instead
HARDCODED_PATH_PATTERNS = [
    r"/mnt/c/Users/[^/\s]+",        # WSL Windows path
    r"/home/[a-z]+(?!/\.claude)",   # User home (not ~/.claude)
    r"C:\\Users\\[^\s]+",           # Windows path
    r"/Users/[a-z]+/",              # macOS home
]

# Valid portable path prefixes (OK to appear)
ALLOWED_PATH_PREFIXES = [
    r"\$[A-Z_]+",            # Env var like $SECOND_BRAIN_DIR
    r"~/",                   # Home-relative
    r"\{[a-z_-]+\}",        # Template vars like {topic-slug}
    r"\[",                   # Bracketed placeholders
    r"docs/",               # Relative project path
    r"brainstorms/",         # Relative project path
    r"vision\.json",         # Known project file
    r"vision-json",
]

# Directional keywords in pattern column
UPSTREAM_PATTERNS = [
    "upstream", "prerequisite", "gate", "input from",
]
DOWNSTREAM_PATTERNS = [
    "downstream", "parallel", "complement", "amplifier",
    "alternative", "fallback", "domain cluster",
    "orchestrat",
]

def find_skill_files():
    seen = set()
    skills = []
    for base in SKILL_DIRS:
        if not base.exists():
            continue
        for skill_md in base.rglob("SKILL.md"):
            real = skill_md.resolve()
            if real in seen:
                continue
            seen.add(real)
            name = skill_md.parent.name
            if name in AUDITED_SKILLS and name != "difficult-conversation-proof":
                skills.append((name, skill_md))
    return sorted(skills, key=lambda x: x[0])


def parse_relationships_table(content):
    """
    Extract rows from ## Relationships table.
    Returns list of dicts: {skill, pattern, condition, artifact}
    """
    # Find the Relationships section
    m = re.search(r'### Relationships\s*\n(.*?)(?=\n###|\n##|\Z)', content, re.DOTALL)
    if not m:
        return []

    table_text = m.group(1)
    rows = []
    for line in table_text.splitlines():
        line = line.strip()
        if not line.startswith('|') or line.startswith('|---') or 'Skill' in line:
            continue
        parts = [p.strip() for p in line.strip('|').split('|')]
        if len(parts) >= 2:
            skill_raw = parts[0].strip('`').strip()
            pattern = parts[1] if len(parts) > 1 else ""
            condition = parts[2] if len(parts) > 2 else ""
            artifact = parts[3] if len(parts) > 3 else ""
            if skill_raw:
                rows.append({
                    "skill": skill_raw,
                    "pattern": pattern.lower(),
                    "condition": condition,
                    "artifact": artifact,
                })
    return rows


def classify_direction(pattern):
    """Return 'upstream', 'downstream', or 'peer' based on pattern text."""
    p = pattern.lower()
    if any(u in p for u in UPSTREAM_PATTERNS):
        return "upstream"
    if any(d in p for d in DOWNSTREAM_PATTERNS):
        return "downstream"
    return "peer"


def check_hardcoded_paths(artifact, skill_name):
    """Return list of hardcoded path issues found in artifact string."""
    issues = []
    for pattern in HARDCODED_PATH_PATTERNS:
        matches = re.findall(pattern, artifact)
        for m in matches:
            # Check if it's an allowed portable prefix
            is_ok = any(re.match(ap, artifact) for ap in ALLOWED_PATH_PREFIXES)
            if not is_ok:
                issues.append(f"Hardcoded path '{m}' — use env var ($SECOND_BRAIN_DIR, $OBSIDIAN_VAULT_DIR, ~/) instead")
    return issues


def run_checks(skill_name, skill_path, all_skills_index):
    """
    Returns dict with check results.
    all_skills_index: {name: rows} map built from all skills first pass
    """
    content = skill_path.read_text(encoding="utf-8")
    rows = parse_relationships_table(content)

    has_relationships_section = "### Relationships" in content
    failures = []
    warnings = []

    if not has_relationships_section:
        failures.append("Missing '### Relationships' subsection in Skill Relationships")
        return {"rows": [], "failures": failures, "warnings": warnings, "has_section": False}

    if not rows:
        warnings.append("Relationships table is empty — no skill references declared")
        return {"rows": [], "failures": failures, "warnings": warnings, "has_section": True}

    for row in rows:
        ref_skill = row["skill"]

        # Check 1: No placeholder/bad skill names
        if ref_skill.lower() in BAD_SKILL_NAMES:
            failures.append(f"Placeholder skill name '{ref_skill}' in relationships table")
            continue

        # Check 2: Referenced skill exists in our known set
        if ref_skill not in KNOWN_SKILLS:
            # Soft warning — some skills reference external tools (gamma, excalidraw, etc.)
            warnings.append(f"Referenced skill '{ref_skill}' not in known skill set (may be external tool or sub-skill)")

        # Check 3: Hardcoded paths in artifact column
        path_issues = check_hardcoded_paths(row["artifact"], skill_name)
        for issue in path_issues:
            failures.append(issue)

    return {"rows": rows, "failures": failures, "warnings": warnings, "has_section": True}


def check_bidirectional(all_skills_rows):
    """
    Check bidirectionality: if A declares B as downstream,
    B should declare A as upstream (or at minimum mention A).

    Returns: list of (skill_a, skill_b, issue) tuples
    """
    issues = []

    for skill_a, rows_a in all_skills_rows.items():
        for row in rows_a:
            skill_b = row["skill"]
            direction = classify_direction(row["pattern"])

            if skill_b not in all_skills_rows or skill_b not in AUDITED_SKILLS:
                continue  # External tool or non-audited skill — skip bidirectionality check

            if direction == "downstream":
                # A → B: B should have A in its upstream relationships
                b_rows = all_skills_rows.get(skill_b, [])
                b_refs_a = any(r["skill"] == skill_a for r in b_rows)
                if not b_refs_a:
                    issues.append((
                        skill_a, skill_b,
                        f"'{skill_a}' declares '{skill_b}' as downstream, but '{skill_b}' doesn't reference '{skill_a}' back"
                    ))

            elif direction == "upstream":
                # A ← B: B should have A in its downstream relationships
                b_rows = all_skills_rows.get(skill_b, [])
                b_refs_a = any(r["skill"] == skill_a for r in b_rows)
                if not b_refs_a:
                    issues.append((
                        skill_a, skill_b,
                        f"'{skill_a}' declares '{skill_b}' as upstream, but '{skill_b}' doesn't reference '{skill_a}' back"
                    ))

    return issues


def main():
    skills = find_skill_files()
    print(f"Found {len(skills)} audited skills to test.\n")

    # First pass: collect all relationship rows
    all_skills_rows = {}  # skill_name → [row dicts]
    all_results = {}

    for skill_name, skill_path in skills:
        result = run_checks(skill_name, skill_path, {})
        all_results[skill_name] = result
        all_skills_rows[skill_name] = result["rows"]

    # Second pass: bidirectionality check
    bidir_issues = check_bidirectional(all_skills_rows)

    # Print per-skill results
    print("=" * 70)
    print("BATCH 3 — RELATIONSHIP GRAPH CONSISTENCY")
    print("=" * 70)

    total_hard_failures = 0
    total_warnings = 0
    hard_fail_skills = []
    warn_skills = []

    for skill_name, _ in skills:
        result = all_results[skill_name]
        f = result["failures"]
        w = result["warnings"]
        row_count = len(result["rows"])

        if f:
            total_hard_failures += len(f)
            hard_fail_skills.append(skill_name)
            print(f"  FAIL  {skill_name} ({row_count} rel rows)")
            for issue in f:
                print(f"         ✗ {issue}")
        elif w:
            warn_skills.append(skill_name)
            total_warnings += len(w)
            print(f"  PASS  {skill_name} ⚠ ({row_count} rel rows)")
            for issue in w:
                print(f"         ⚠ {issue}")
        else:
            print(f"  PASS  {skill_name} ({row_count} rel rows)")

    # Bidirectionality report
    print()
    print("=" * 70)
    print("BIDIRECTIONALITY AUDIT")
    print("=" * 70)

    if bidir_issues:
        # Group by severity: only flag when both skills are in audited set
        confirmed = [(a, b, msg) for a, b, msg in bidir_issues if b in AUDITED_SKILLS]
        external_only = [(a, b, msg) for a, b, msg in bidir_issues if b not in AUDITED_SKILLS]

        print(f"  {len(confirmed)} missing back-references (audited ↔ audited pairs):")
        for a, b, msg in confirmed[:30]:  # Cap at 30 to avoid noise
            print(f"    ⚠ {msg}")
        if len(confirmed) > 30:
            print(f"    ... and {len(confirmed) - 30} more")
    else:
        print("  All downstream/upstream pairs are bidirectional. ✓")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    total = len(skills)
    pass_count = total - len(hard_fail_skills)
    print(f"  Total skills tested      : {total}")
    print(f"  PASS (structure + paths) : {pass_count}")
    print(f"  FAIL (hard)              : {len(hard_fail_skills)}")
    print(f"  WARN (soft)              : {len(warn_skills)}")
    print(f"  Hard failures total      : {total_hard_failures}")
    print(f"  Bidir gaps (audited)     : {len([i for i in bidir_issues if i[1] in AUDITED_SKILLS])}")

    if hard_fail_skills:
        print()
        print("HARD FAILURES TO FIX:")
        for s in hard_fail_skills:
            print(f"  {s}:")
            for issue in all_results[s]["failures"]:
                print(f"    - {issue}")

    return 1 if hard_fail_skills else 0


if __name__ == "__main__":
    sys.exit(main())
