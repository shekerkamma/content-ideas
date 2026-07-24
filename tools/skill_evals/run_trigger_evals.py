#!/usr/bin/env python3
"""
[adapted] Ported from Shubhamsaboo/awesome-llm-apps
(agent_skills/evals/tools/run_trigger_evals.py, July 2026). Tier 2 — trigger &
routing. Deterministic, CI-safe, no model.

A skill's description is its entire trigger surface, so this checks it
lexically: positive prompts must score against their skill's description
clearly above near-miss negatives, and — across the whole catalog — no two
*distinct* skills should have near-colliding descriptions (an over-broad
description outranking the right skill).

Adapted for this repo's layout: the original tool assumes one flat directory
of skills. This repo vendors the SAME skill under the SAME name into multiple
roots on purpose (skills/, .claude/skills/, .agents/skills/,
skill-framework/.agents/skills/) so each host can load it — those are mirrored
copies, not rival skills, and must not collide with themselves. This version
discovers skills across all configured roots, dedupes by name (first
occurrence wins for scoring), and separately reports any name whose
description text has DRIFTED between its copies — that's a sync bug worth
fixing on its own, distinct from a real vocabulary collision between two
different skills.

Cases live in <root>/../evals/<skill>/trigger-cases.json relative to each
skill (same convention as upstream) — optional. A skill with no
trigger-cases.json is reported as WARN (not FAIL): authoring cases is a
follow-up per-skill task, not a blocker for adopting this tool.

    python3 run_trigger_evals.py                  # all configured roots
    python3 run_trigger_evals.py --root skills     # just one root
"""

import argparse
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

DEFAULT_ROOTS = [
    "skills",
    ".claude/skills",
    ".agents/skills",
    "skill-framework/.agents/skills",
]

STOP = set("""a an the and or of to in on for with is are was were be been it its this
that those these you your i me my we our they their he she his her do does did done
can could should would will just very really some any all not no yes if then than as
at by from into out up down over under again more most other own same so too s t don
""".split())

MARGIN = 1.15  # min positive score must beat max negative score by this factor


def tokens(text):
    out = set()
    for w in re.findall(r"[a-z0-9']+", text.lower()):
        if w in STOP or len(w) < 3:
            continue
        # crude stemmer: enough to match "projects/project", "finished/finish"
        for suf in ("ing", "ed", "es", "s"):
            if w.endswith(suf) and len(w) - len(suf) >= 3:
                w = w[: -len(suf)]
                break
        out.add(w)
    return out


def description_of(skill_md_path):
    text = open(skill_md_path, encoding="utf-8").read()
    m = re.search(r"^description:\s*(.+?)^(?=[a-zA-Z-]+:|---)", text, re.S | re.M)
    return m.group(1) if m else ""


def score(prompt_toks, desc_toks):
    if not prompt_toks:
        return 0.0
    return len(prompt_toks & desc_toks) / math.sqrt(len(prompt_toks))


def discover(roots):
    """Return {name: [(abs_skill_dir, raw_description), ...]} across all roots."""
    catalog = {}
    for root in roots:
        root_abs = os.path.join(REPO, root)
        if not os.path.isdir(root_abs):
            continue
        for entry in sorted(os.listdir(root_abs)):
            skill_dir = os.path.join(root_abs, entry)
            skill_md = os.path.join(skill_dir, "SKILL.md")
            if os.path.isfile(skill_md):
                desc = description_of(skill_md)
                catalog.setdefault(entry, []).append((skill_dir, desc))
    return catalog


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", action="append", dest="roots",
                     help="repo-relative root to scan (repeatable); default scans all of: %s"
                          % ", ".join(DEFAULT_ROOTS))
    args = ap.parse_args(argv)
    roots = args.roots or DEFAULT_ROOTS

    catalog = discover(roots)
    if not catalog:
        print("no skills found under %s" % ", ".join(roots))
        return 1

    failures = 0

    # --- drift check: same name, different description across roots --------
    # This repo has a deliberate "discovery wrapper" convention (see
    # docs/skills-audit-2026-07-12.md): a thin cross-host copy whose
    # description explicitly says it defers to the canonical skill elsewhere.
    # Those are SUPPOSED to have a different description — that's not drift,
    # it's the pattern working. Only flag divergence when neither copy reads
    # as a wrapper.
    WRAPPER_MARKERS = ("discovery wrapper", "compatibility wrapper", "canonical")
    skills = {}  # name -> token set (first-seen copy is canonical for scoring)
    for name, copies in sorted(catalog.items()):
        canonical_desc = copies[0][1]
        skills[name] = tokens(canonical_desc)
        diverged = [d for _, d in copies[1:] if d.strip() != canonical_desc.strip()]
        is_wrapper_pattern = any(
            any(marker in d.lower() for marker in WRAPPER_MARKERS)
            for _, d in copies
        )
        if diverged and not is_wrapper_pattern:
            print("DRIFT %s: description differs across %d cop%s — %s"
                  % (name, len(copies), "y" if len(copies) == 1 else "ies",
                     ", ".join(os.path.relpath(p, REPO) for p, _ in copies)))
            failures += 1

    # --- routing sanity across the catalog: no two DIFFERENT skills collide -
    names = sorted(skills)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = skills[names[i]], skills[names[j]]
            if not a or not b:
                continue
            overlap = len(a & b) / max(1, min(len(a), len(b)))
            if overlap > 0.5:
                print("FAIL  descriptions near-collide: %s vs %s (%.0f%% shared vocabulary)"
                      % (names[i], names[j], overlap * 100))
                failures += 1

    # --- per-skill trigger cases (optional, authored incrementally) --------
    no_cases = 0
    for name in names:
        skill_dir = catalog[name][0][0]
        case_file = os.path.join(os.path.dirname(skill_dir), "evals", name, "trigger-cases.json")
        if not os.path.exists(case_file):
            no_cases += 1
            continue
        cases = json.load(open(case_file, encoding="utf-8"))["cases"]
        pos, neg = [], []
        for c in cases:
            if c.get("lexical") is False:
                continue
            s = score(tokens(c["prompt"]), skills[name])
            (pos if c["should_trigger"] else neg).append((s, c["id"]))
            if c["should_trigger"] and len(skills) > 1:
                best = max(skills, key=lambda k: score(tokens(c["prompt"]), skills[k]))
                if best != name:
                    print("FAIL  %s: %r routes to %s instead" % (name, c["id"], best))
                    failures += 1
        if pos and neg:
            worst_pos, wp_id = min(pos)
            best_neg, bn_id = max(neg)
            if worst_pos <= best_neg * MARGIN:
                print("FAIL  %s: weakest positive %r (%.2f) does not clear strongest "
                      "near-miss %r (%.2f) — the description is missing vocabulary "
                      "users say, or a negative shares too much of it"
                      % (name, wp_id, worst_pos, bn_id, best_neg))
                failures += 1
            else:
                print("PASS  %s: %d positives clear %d near-misses "
                      "(weakest %.2f vs strongest %.2f)"
                      % (name, len(pos), len(neg), worst_pos, best_neg))

    print("\n%d skill(s) across %d root(s), %d with no trigger-cases.json authored yet"
          % (len(names), len(roots), no_cases))

    if failures:
        print("%d failure(s)" % failures)
        return 1
    print("trigger & routing: all clear")
    return 0


if __name__ == "__main__":
    sys.exit(main())
