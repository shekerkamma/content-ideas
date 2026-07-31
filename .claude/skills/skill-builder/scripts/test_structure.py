#!/usr/bin/env python3
"""
Batch 1 — Level 1 Structure Tests
Scans all SKILL.md files across skill directories and validates structural completeness.
"""
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
SKILL_DIRS = [
    REPO_ROOT / ".claude" / "skills",
    REPO_ROOT / ".agents" / "skills",
    REPO_ROOT / "skills",
    REPO_ROOT / "plugins" / "content-ideas" / "skills",
]

VALID_CATEGORIES = {
    "Library / API Reference",
    "Product Verification",
    "Data & Analysis",
    "Business Automation",
    "Scaffolding & Templates",
    "Code Quality & Review",
    "CI/CD & Deployment",
    "Runbook",
    "Infrastructure Ops",
}

AUDITED_SKILLS = {
    "content-research", "ai-strategy-researcher", "ai-strategy-brief",
    "grill-me", "plaid", "karpathy-guidelines", "branded-pptx-deck",
    "mkt-visual-identity", "mkt-brand-voice", "presales-deal-prep",
    "vertical-scorer", "office-hours", "plan-ceo-review",
    "graphify", "social-media-team", "research-to-deck", "learn-anything",
    "competitive-intel-sprint", "difficult-conversation-prep", "watch",
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
    "skill-builder",
}

def find_skill_files():
    """Find all SKILL.md files, resolving symlinks to avoid duplicate checks."""
    seen_real_paths = set()
    skills = []
    for base in SKILL_DIRS:
        if not base.exists():
            continue
        for skill_md in base.rglob("SKILL.md"):
            if not skill_md.is_file():
                continue
            real = skill_md.resolve()
            if real in seen_real_paths:
                continue
            seen_real_paths.add(real)
            # derive skill name from parent directory
            skill_name = skill_md.parent.name
            if skill_name in AUDITED_SKILLS:
                skills.append((skill_name, skill_md))
    return sorted(skills, key=lambda x: x[0])

def extract_frontmatter_name(content):
    m = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    return m.group(1).strip() if m else None

def strip_fenced_code(content):
    """Remove fenced code blocks so templates don't count as live sections."""
    return re.sub(r"```.*?```", "", content, flags=re.DOTALL)

def check_section(content, heading):
    return bool(re.search(r'^#{1,3}\s+' + re.escape(heading), content, re.MULTILINE))

def count_gotchas(content):
    """Count bullet entries under ## Gotchas."""
    m = re.search(r'## Gotchas\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not m:
        return 0
    block = m.group(1)
    return len(re.findall(r'^\s*[-*]', block, re.MULTILINE))

def extract_category(content):
    """Extract category value from ### Category block."""
    m = re.search(r'### Category\s*\n([^\n#]+)', content)
    return m.group(1).strip() if m else None

def run_checks(skill_name, skill_path):
    content = skill_path.read_text(encoding="utf-8")
    visible_content = strip_fenced_code(content)
    lines = content.splitlines()
    line_count = len(lines)
    results = {}

    # C1: Has ## Skill Relationships
    results["has_skill_relationships"] = check_section(visible_content, "Skill Relationships")

    # C2: Has ## Gotchas
    results["has_gotchas"] = check_section(visible_content, "Gotchas")

    # C3: name matches directory
    fm_name = extract_frontmatter_name(content)
    results["name_matches_dir"] = (fm_name == skill_name) if fm_name else None

    # C4: Under 500 lines
    results["under_500_lines"] = line_count <= 500
    results["line_count"] = line_count

    # C5: Valid category
    category = extract_category(visible_content)
    results["category"] = category
    results["valid_category"] = (category in VALID_CATEGORIES) if category else False

    # C6: Runtime preamble exists
    results["has_runtime_preamble"] = check_section(visible_content, "Runtime Preamble")

    # C7: Gotchas has >= 3 entries
    gotcha_count = count_gotchas(visible_content)
    results["gotcha_count"] = gotcha_count
    results["gotchas_substantial"] = gotcha_count >= 3

    return results

def main():
    skills = find_skill_files()
    print(f"Found {len(skills)} audited skills to test.\n")

    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"

    all_results = []
    failures = []
    warnings = []

    for skill_name, skill_path in skills:
        r = run_checks(skill_name, skill_path)
        row = {"skill": skill_name, "path": str(skill_path), **r}
        all_results.append(row)

        skill_failures = []
        skill_warnings = []

        if not r["has_skill_relationships"]:
            skill_failures.append("MISSING ## Skill Relationships")
        if not r["has_gotchas"]:
            skill_failures.append("MISSING ## Gotchas")
        if r["name_matches_dir"] is False:
            skill_failures.append(f"name mismatch: frontmatter='{r.get('category')}' dir='{skill_name}'")
        if not r["valid_category"]:
            skill_failures.append(f"INVALID category: '{r['category']}'")
        if not r["has_runtime_preamble"]:
            skill_failures.append("MISSING ### Runtime Preamble")
        if not r["gotchas_substantial"]:
            skill_failures.append(f"THIN Gotchas: only {r['gotcha_count']} entries (need ≥3)")
        if not r["under_500_lines"]:
            skill_warnings.append(f"OVER 500 lines: {r['line_count']} lines")

        if skill_failures:
            failures.append((skill_name, skill_failures))
        if skill_warnings:
            warnings.append((skill_name, skill_warnings))

    # Print per-skill summary
    print("=" * 70)
    print("BATCH 1 — STRUCTURE TEST RESULTS")
    print("=" * 70)

    for row in all_results:
        name = row["skill"]
        checks = [
            ("Skill Relationships", row["has_skill_relationships"]),
            ("Gotchas", row["has_gotchas"]),
            ("Name match", row["name_matches_dir"] if row["name_matches_dir"] is not None else False),
            ("Valid category", row["valid_category"]),
            ("Runtime preamble", row["has_runtime_preamble"]),
            ("Gotchas ≥3", row["gotchas_substantial"]),
        ]
        passed = all(v for _, v in checks)
        over = not row["under_500_lines"]
        status = PASS if passed else FAIL
        line_note = f" [{row['line_count']} lines{'⚠' if over else ''}]"
        print(f"  {status:4}  {name}{line_note}")
        for label, val in checks:
            if not val:
                print(f"         ✗ {label}")

    print()
    print("=" * 70)
    print(f"SUMMARY")
    print("=" * 70)
    total = len(all_results)
    fail_count = len(failures)
    warn_count = len(warnings)
    pass_count = total - fail_count
    print(f"  Total skills tested : {total}")
    print(f"  PASS                : {pass_count}")
    print(f"  FAIL                : {fail_count}")
    print(f"  WARNINGS (>500 ln)  : {warn_count}")

    if failures:
        print()
        print("FAILURES TO FIX:")
        for skill, issues in failures:
            print(f"  {skill}:")
            for issue in issues:
                print(f"    - {issue}")

    if warnings:
        print()
        print("WARNINGS:")
        for skill, issues in warnings:
            print(f"  {skill}:")
            for issue in issues:
                print(f"    - {issue}")

    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
