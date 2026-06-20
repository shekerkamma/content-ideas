#!/usr/bin/env python3
"""
Batch 2 — Description Quality Tests
Checks that skill descriptions are trigger-focused (written for the model, not humans).
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
}

# Trigger-focused openers — model-facing language
TRIGGER_OPENERS = [
    r"^use when",
    r"^triggers? on",
    r"^invoke when",
    r"^run when",
    r"^use this when",
    r"^use for",
]

# Summary/human-facing language — red flags in the description lead
SUMMARY_PATTERNS = [
    r"^this skill",
    r"^this tool",
    r"^generates? ",
    r"^produces? ",
    r"^creates? ",
    r"^builds? ",
    r"^a skill (that|which|for)",
    r"^an? (automated|ai-powered|intelligent)",
    r"^helps? (you|users?|founders?)",
    r"^guides? ",
    r"^provides? ",
]

# Peer skills known from relationship audit — check if description disambiguates
KNOWN_PEERS = {
    "marp": ["branded-pptx-deck", "ikigai-gamma-slidedeck"],
    "branded-pptx-deck": ["marp", "gamma"],
    "ikigai": ["ikigai-gamma-slidedeck"],
    "ikigai-gamma-slidedeck": ["ikigai"],
    "ai-strategy-brief": ["ai-strategy-researcher"],
    "ai-strategy-researcher": ["ai-strategy-brief"],
    "drawio": ["workflow-visualizer", "excalidraw"],
    "workflow-visualizer": ["drawio"],
    "competitive-intel-sprint": ["ai-strategy-researcher"],
    "watch": ["content-research"],
    "content-research": ["watch"],
    "grill-me": ["learn-anything"],
    "ikigai-gamma-slidedeck": ["ikigai", "gcc-roadmap"],
    "video-to-deck": ["marp", "branded-pptx-deck"],
    "research-to-deck": ["ikigai-gamma-slidedeck"],
    "second-brain": ["graphify"],
    "guard": ["careful"],
    "careful": ["guard"],
    "analytics-to-comms": ["ai-strategy-brief"],
}


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
            if name in AUDITED_SKILLS:
                skills.append((name, skill_md))
    return sorted(skills, key=lambda x: x[0])


def extract_description(content):
    """Extract description from YAML frontmatter. Handles |, >-, >, and single-line."""
    # Literal block scalar: description: |
    m = re.search(r'^description:\s*\|[-]?\n((?:[ \t]+.+\n?)+)', content, re.MULTILINE)
    if m:
        lines = m.group(1).splitlines()
        return " ".join(l.strip() for l in lines if l.strip())
    # Folded block scalar: description: >- or description: >
    m = re.search(r'^description:\s*>[-]?\n((?:[ \t]+.+\n?)+)', content, re.MULTILINE)
    if m:
        lines = m.group(1).splitlines()
        return " ".join(l.strip() for l in lines if l.strip())
    # Single-line (quoted or unquoted)
    m = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    if m:
        val = m.group(1).strip()
        if val not in ("|", ">", ">-", "|-"):
            return val
    return None


def check_trigger_opener(desc):
    """Trigger phrase anywhere in first 300 chars — not necessarily the very first word."""
    lead = desc[:300].lower()
    return any(re.search(p, lead) for p in TRIGGER_OPENERS)




def check_no_summary_lead(desc):
    """Does description avoid leading with human-summary language?"""
    lead = desc.lower().strip()
    return not any(re.match(p, lead) for p in SUMMARY_PATTERNS)


def count_trigger_phrases(desc):
    """Count quoted phrases or 'triggers on X' patterns — natural language examples."""
    quoted = re.findall(r'"[^"]{3,}"', desc)
    triggers = re.findall(r'triggers? on[^.]+', desc, re.IGNORECASE)
    also = re.findall(r'also triggers? on[^.]+', desc, re.IGNORECASE)
    return len(quoted) + len(triggers) + len(also)


def check_peer_disambiguation(skill_name, desc):
    """If skill has known peers, does description mention at least one?"""
    peers = KNOWN_PEERS.get(skill_name, [])
    if not peers:
        return True, []  # No peers — pass by default
    desc_lower = desc.lower()
    mentioned = [p for p in peers if p.lower() in desc_lower or p.replace("-", " ").lower() in desc_lower]
    return len(mentioned) > 0, peers


def run_checks(skill_name, skill_path):
    content = skill_path.read_text(encoding="utf-8")
    desc = extract_description(content)
    if not desc:
        return {"desc_found": False}

    has_trigger_opener = check_trigger_opener(desc)
    no_summary_lead = check_no_summary_lead(desc)
    phrase_count = count_trigger_phrases(desc)
    peer_ok, peers = check_peer_disambiguation(skill_name, desc)

    return {
        "desc_found": True,
        "description_preview": desc[:120] + ("..." if len(desc) > 120 else ""),
        "has_trigger_opener": has_trigger_opener,
        "no_summary_lead": no_summary_lead,
        "phrase_count": phrase_count,
        "has_phrases": phrase_count >= 2,
        "peer_disambiguation_ok": peer_ok,
        "expected_peers": peers,
    }


def main():
    skills = find_skill_files()
    print(f"Found {len(skills)} audited skills to test.\n")

    failures = []
    warnings = []
    all_results = []

    for skill_name, skill_path in skills:
        r = run_checks(skill_name, skill_path)
        r["skill"] = skill_name
        all_results.append(r)

        skill_failures = []
        skill_warnings = []

        if not r.get("desc_found"):
            skill_failures.append("NO description field found in frontmatter")
            failures.append((skill_name, skill_failures))
            continue

        if not r["has_trigger_opener"]:
            skill_failures.append(f"Description does not start with trigger phrase")
        if not r["no_summary_lead"]:
            skill_failures.append(f"Description leads with human-summary language")
        if not r["peer_disambiguation_ok"]:
            skill_warnings.append(f"No peer skill mentioned (expected one of: {', '.join(r['expected_peers'])})")
        if not r["has_phrases"]:
            skill_warnings.append(f"Only {r['phrase_count']} trigger phrases found (recommend ≥2)")

        if skill_failures:
            failures.append((skill_name, skill_failures))
        if skill_warnings:
            warnings.append((skill_name, skill_warnings))

    # Print per-skill
    print("=" * 70)
    print("BATCH 2 — DESCRIPTION QUALITY TEST RESULTS")
    print("=" * 70)

    for r in all_results:
        name = r["skill"]
        if not r.get("desc_found"):
            print(f"  FAIL  {name}")
            print(f"         ✗ No description found")
            continue

        checks = [
            ("Trigger opener", r["has_trigger_opener"]),
            ("No summary lead", r["no_summary_lead"]),
            ("Phrases ≥2", r["has_phrases"]),
            ("Peer disambig", r["peer_disambiguation_ok"]),
        ]
        hard_pass = r["has_trigger_opener"] and r["no_summary_lead"]
        status = "PASS" if hard_pass else "FAIL"
        warn_note = " ⚠" if (not r["has_phrases"] or not r["peer_disambiguation_ok"]) and hard_pass else ""
        print(f"  {status:4}  {name}{warn_note}")
        print(f"         → {r['description_preview']}")
        for label, val in checks:
            if not val:
                icon = "✗" if label in ("Trigger opener", "No summary lead") else "⚠"
                print(f"         {icon} {label}")

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    total = len(all_results)
    fail_count = len(failures)
    warn_count = len(warnings)
    pass_count = total - fail_count
    print(f"  Total skills tested : {total}")
    print(f"  PASS                : {pass_count}")
    print(f"  FAIL (hard)         : {fail_count}")
    print(f"  WARN (soft)         : {warn_count}")

    if failures:
        print()
        print("FAILURES TO FIX:")
        for skill, issues in failures:
            print(f"  {skill}:")
            for issue in issues:
                print(f"    - {issue}")

    if warnings:
        print()
        print("WARNINGS (soft — review manually):")
        for skill, issues in warnings:
            print(f"  {skill}:")
            for issue in issues:
                print(f"    - {issue}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
