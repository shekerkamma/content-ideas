#!/usr/bin/env python3
"""
skill-evals — free tiers (1 structural, 1b security, 2 trigger/routing) across
every configured skill root in this repo. Stdlib only, no network calls, no
tokens spent. Adapted from Shubhamsaboo/awesome-llm-apps
(agent_skills/evals/, July 2026) for this repo's multi-root skill layout.

Usage:
    python3 tools/skill_evals/run_all.py            # human-readable
    python3 tools/skill_evals/run_all.py --json      # machine-readable summary

Exit codes: 0 = clean (lint errors allowed as warnings unless --strict;
CRITICAL security findings and trigger FAILs always fail), 1 = failures found,
2 = usage error.

This does NOT run tier 3 (behavioral evals via evals.json / expectations[]) —
that tier costs tokens and is on-demand only; see the skill-evals section of
docs/ or ask for it explicitly per skill.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import skill_lint  # noqa: E402
import skill_scanner  # noqa: E402
import run_trigger_evals  # noqa: E402

DEFAULT_ROOTS = run_trigger_evals.DEFAULT_ROOTS
SKIP_DIRS = skill_scanner.SKIP_DIRS


def discover_skill_dirs(roots):
    """One entry per physical skill directory (no dedup — divergence between
    physical copies across roots is exactly what tier 1/1b should catch)."""
    found = []
    for root in roots:
        root_abs = os.path.join(REPO, root)
        if not os.path.isdir(root_abs):
            continue
        for entry in sorted(os.listdir(root_abs)):
            skill_dir = os.path.join(root_abs, entry)
            if os.path.isdir(skill_dir) and os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
                found.append(skill_dir)
    return found


def run_lint(skill_dirs, strict):
    results = []
    for sd in skill_dirs:
        errors, warnings = skill_lint.lint(sd, strict=strict, repo_root=REPO)
        results.append({
            "path": os.path.relpath(sd, REPO),
            "errors": errors,
            "warnings": warnings,
        })
    return results


def run_scanner(skill_dirs):
    results = []
    for sd in skill_dirs:
        findings = skill_scanner.scan_skill(sd)
        results.append({
            "path": os.path.relpath(sd, REPO),
            "findings": [f.as_dict() for f in findings],
        })
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", action="append", dest="roots",
                     help="repo-relative root to scan (repeatable); default: %s"
                          % ", ".join(DEFAULT_ROOTS))
    ap.add_argument("--strict", action="store_true",
                     help="promote tier-1 spec-limit violations to errors")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args(argv)
    roots = args.roots or DEFAULT_ROOTS

    skill_dirs = discover_skill_dirs(roots)
    if not skill_dirs:
        print("no skills found under %s" % ", ".join(roots), file=sys.stderr)
        return 2

    lint_results = run_lint(skill_dirs, args.strict)
    scan_results = run_scanner(skill_dirs)

    lint_error_total = sum(len(r["errors"]) for r in lint_results)
    lint_warn_total = sum(len(r["warnings"]) for r in lint_results)
    critical_total = sum(
        1 for r in scan_results for f in r["findings"] if f["severity"] == "CRITICAL"
    )
    warn_total = sum(
        1 for r in scan_results for f in r["findings"] if f["severity"] == "WARN"
    )

    trigger_argv = []
    for root in roots:
        trigger_argv += ["--root", root]
    print("=== Tier 2: trigger & routing ===" if not args.as_json else "", end="" if args.as_json else "\n")
    if not args.as_json:
        trigger_exit = run_trigger_evals.main(trigger_argv)
    else:
        # capture trigger tier's stdout so JSON stays parseable
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            trigger_exit = run_trigger_evals.main(trigger_argv)
        trigger_output = buf.getvalue()

    if not args.as_json:
        print("\n=== Tier 1: structural lint (%d skill dirs) ===" % len(skill_dirs))
        for r in lint_results:
            if r["errors"] or r["warnings"]:
                print("-- %s: %d error(s), %d warning(s)" % (r["path"], len(r["errors"]), len(r["warnings"])))
                for e in r["errors"]:
                    print("   ERROR: %s" % e)
                for w in r["warnings"]:
                    print("   WARN:  %s" % w)

        print("\n=== Tier 1b: security scan ===")
        for r in scan_results:
            crit = [f for f in r["findings"] if f["severity"] == "CRITICAL"]
            for f in crit:
                print("-- %s: [CRITICAL] %s %s:%s — %s" % (
                    r["path"], f["check"], f["file"], f["line"], f["message"]))

        print("\n=== Summary ===")
        print("skill dirs scanned: %d (roots: %s)" % (len(skill_dirs), ", ".join(roots)))
        print("tier 1 lint:   %d error(s), %d warning(s)" % (lint_error_total, lint_warn_total))
        print("tier 1b scan:  %d CRITICAL, %d WARN" % (critical_total, warn_total))
        print("tier 2 trigger: %s" % ("PASS" if trigger_exit == 0 else "FAIL"))
    else:
        out = {
            "skill_dirs_scanned": len(skill_dirs),
            "roots": roots,
            "lint": lint_results,
            "scan": scan_results,
            "trigger_exit": trigger_exit,
            "trigger_output": trigger_output,
            "summary": {
                "lint_errors": lint_error_total,
                "lint_warnings": lint_warn_total,
                "scan_critical": critical_total,
                "scan_warn": warn_total,
            },
        }
        print(json.dumps(out, indent=2))

    failed = bool(lint_error_total) or bool(critical_total) or (trigger_exit != 0)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
