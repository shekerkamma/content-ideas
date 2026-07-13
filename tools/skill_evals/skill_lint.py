#!/usr/bin/env python3
"""
[vendored] Ported from Shubhamsaboo/awesome-llm-apps
(agent_skills/evals/tools/skill_lint.py, July 2026). Tier 1 — structural lint.
skill_lint.py — validate an agent skill directory against the agentskills.io spec.

Usage:
    python3 skill_lint.py <skill-dir> [--strict] [--json]

Checks (spec: https://agentskills.io/specification, verified July 2026):
  * SKILL.md exists and has parseable YAML frontmatter
  * name: 1-64 chars, lowercase a-z/0-9/hyphens, no leading/trailing/consecutive
    hyphens, must equal the directory name
  * description: present, 1-1024 chars, plus triggering heuristics
  * compatibility: <= 500 chars if present
  * body: warn at 400 lines, 500+ lines is a warning (error with --strict);
    ~5k-token budget warning
  * relative file references in the body must exist on disk
  * forward-slash paths only (backslash paths are an error)
  * TODO/FIXME-style markers are warnings
  * text-only skills (no scripts/ AND no references/) are warned

Exit codes: 0 = no errors (warnings allowed), 1 = errors found, 2 = usage error.
Python 3 stdlib only — no third-party dependencies (frontmatter parsing is
hand-rolled for the flat fields the spec defines; pyyaml is NOT required).
"""

import argparse
import json
import os
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESC = 1024
MAX_COMPAT = 500
BODY_WARN_LINES = 400
BODY_MAX_LINES = 500
BODY_TOKEN_BUDGET = 5000

KNOWN_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

WHEN_SIGNALS = re.compile(
    r"\b(use (this skill )?when|use (it |this )?for|when the user|when working"
    r"|use to|triggers? (on|when)|applies (when|to)|for tasks)\b",
    re.IGNORECASE,
)
FIRST_PERSON = re.compile(r"\b(I|I'll|I'm|I've|me|my|we|our|you should|you can)\b")
QUOTED_SPAN = re.compile(r"\"[^\"\n]*\"|'[^'\n]*'|“[^”\n]*”")
# Leading whitespace allowed before the fence markers — fenced blocks nested
# inside a numbered/bulleted list item are indented, and an anchor of `^```
# with no whitespace allowance silently fails to strip them (leaving any
# placeholder text inside to misfire the unfilled-placeholder check below).
FENCED_BLOCK = re.compile(r"^[ \t]*```.*?^[ \t]*```", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]+`")
# Unfilled template placeholders are multi-word angle-bracket spans in prose
# (e.g. "<what this skill does>"). Single-word forms like <path> are normal
# CLI-usage notation and HTML tags never contain multi-word lowercase text.
TEMPLATE_PLACEHOLDER = re.compile(r"<([a-z][a-z0-9'’,—-]*(?: [a-z0-9'’,—.…-]+)+[^>]*)>")
TODO_MARKER = re.compile(r"\b(TODO|FIXME|XXX|TBD)\b")
MD_LINK = re.compile(r"\]\(([^)\s#]+)\)")
# Capture the FULL leading token (~, absolute /, or ../ parent-dir prefix and
# any intermediate path segments), not just from the resource-dir keyword
# onward — a bare capture loses exactly the prefix that tells us how to
# resolve it (e.g. `~/.claude/skills/other-skill/scripts/x.py` or
# `../../scripts/x.py` cross-skill / repo-root references). The leading
# segment is optional so a plain bare `scripts/x.py` (no prefix at all)
# still matches, same as the original tool.
BARE_PATH = re.compile(r"(?:[~./][\w.\-]*/)?(?:[\w.\-]+/)*(?:scripts|references|assets|evals)/[\w.\-/]+")
BACKSLASH_PATH = re.compile(r"(?:scripts|references|assets|evals)\\")


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _indent_of(line):
    return len(line) - len(line.lstrip(" \t"))


def parse_block(fm_lines, i, min_indent):
    """Parse a nested YAML-ish block (map or sequence) starting at fm_lines[i],
    for lines indented >= min_indent. Returns (value, next_index, error).
    Supports arbitrary depth of maps-of-scalars, maps-of-lists, and
    lists-of-scalars — the house convention some skills here use for fields
    like `permissions: {file_read: [...], file_write: [...]}` that the
    agentskills.io spec itself doesn't define but is valid YAML."""
    n = len(fm_lines)
    while i < n and not fm_lines[i].strip():
        i += 1
    if i >= n or _indent_of(fm_lines[i]) < min_indent:
        return {}, i, None

    block_indent = _indent_of(fm_lines[i])
    first = fm_lines[i].strip()

    if first.startswith("- "):
        items = []
        while i < n:
            if not fm_lines[i].strip():
                i += 1
                continue
            if _indent_of(fm_lines[i]) < block_indent:
                break
            line = fm_lines[i]
            stripped = line.strip()
            if _indent_of(line) != block_indent or not stripped.startswith("- "):
                return None, i, "malformed list item at frontmatter line %d: %r" % (i + 2, stripped)
            rest = stripped[2:].strip()
            if ":" in rest and not rest.startswith(("'", '"')):
                k2, _, v2 = rest.partition(":")
                v2 = v2.strip()
                if v2 == "":
                    sub_value, i, err = parse_block(fm_lines, i + 1, block_indent + 1)
                    if err:
                        return None, i, err
                    items.append({k2.strip(): sub_value})
                    continue
                items.append({k2.strip(): unquote(v2)})
            else:
                items.append(unquote(rest))
            i += 1
        return items, i, None

    mapping = {}
    while i < n:
        if not fm_lines[i].strip():
            i += 1
            continue
        if _indent_of(fm_lines[i]) < block_indent:
            break
        line = fm_lines[i]
        stripped = line.strip()
        if _indent_of(line) != block_indent:
            return None, i, "unexpected indentation at frontmatter line %d: %r" % (i + 2, stripped)
        if stripped.startswith("#"):
            i += 1
            continue
        if ":" not in stripped:
            return None, i, "cannot parse entry at frontmatter line %d: %r (expected 'key: value')" % (i + 2, stripped)
        k2, _, v2 = stripped.partition(":")
        k2, v2 = k2.strip(), v2.strip()
        if v2 == "":
            sub_value, i, err = parse_block(fm_lines, i + 1, block_indent + 1)
            if err:
                return None, i, err
            mapping[k2] = sub_value
            continue
        mapping[k2] = unquote(v2)
        i += 1
    return mapping, i, None


def parse_frontmatter(text):
    """Minimal YAML parser for the flat frontmatter the spec defines.

    Supports: `key: value`, quoted values, block scalars (| and >), one-level
    nested maps (for `metadata:`), and inline flow maps (`{a: b, c: d}`).
    Returns (data, body, error). data is None on a parse error.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text, "SKILL.md must begin with a '---' YAML frontmatter block on line 1"
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            end = i
            break
    if end is None:
        return None, text, "frontmatter is never closed: add a '---' line after the YAML block"

    fm_lines = lines[1:end]
    body = "\n".join(lines[end + 1:])
    data = {}
    i = 0
    while i < len(fm_lines):
        raw = fm_lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if raw[:1] in (" ", "\t"):
            return None, body, (
                "unexpected indentation at frontmatter line %d (%r): top-level keys "
                "must start at column 0" % (i + 2, stripped)
            )
        if ":" not in raw:
            return None, body, "cannot parse frontmatter line %d: %r (expected 'key: value')" % (i + 2, stripped)
        key, _, val = raw.partition(":")
        key = key.strip()
        val = val.strip()

        if val in ("|", ">", "|-", ">-", "|+", ">+"):  # block scalar
            block = []
            i += 1
            while i < len(fm_lines) and (fm_lines[i][:1] in (" ", "\t") or not fm_lines[i].strip()):
                block.append(fm_lines[i].strip())
                i += 1
            joiner = " " if val.startswith(">") else "\n"
            data[key] = joiner.join(b for b in block if b)
            continue

        if val == "":  # nested block: map, list, or (house convention) map-of-lists
            nested, i, err = parse_block(fm_lines, i + 1, 1)
            if err:
                return None, body, "cannot parse nested block under %r: %s" % (key, err)
            data[key] = nested
            continue

        if val.startswith("{") and val.endswith("}"):  # inline flow map
            # A JSON object is also valid YAML flow syntax, and some skills here
            # embed a full nested JSON blob (arrays, quoted keys) in one field —
            # try json.loads first since the naive comma-split below can't
            # handle nested commas/braces. Fall back to the simple `{a: b}`
            # splitter for genuinely flat, unquoted YAML flow maps.
            try:
                data[key] = json.loads(val)
                i += 1
                continue
            except (ValueError, TypeError):
                pass
            nested = {}
            inner = val[1:-1].strip()
            if inner:
                for part in inner.split(","):
                    if ":" not in part:
                        return None, body, "cannot parse inline map for %r: %r" % (key, part.strip())
                    k2, _, v2 = part.partition(":")
                    nested[k2.strip()] = unquote(v2)
            data[key] = nested
            i += 1
            continue

        data[key] = unquote(val)
        i += 1
    return data, body, None


def suggest_name(name):
    s = str(name).strip().lower()
    s = re.sub(r"[_\s]+", "-", s)
    s = re.sub(r"[^a-z0-9-]", "", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s[:MAX_NAME] or "my-skill"


def check_name(name, dirname, errors):
    problems = []
    if not name:
        errors.append("frontmatter 'name' is missing or empty (required, 1-%d chars)" % MAX_NAME)
        return
    if len(name) > MAX_NAME:
        problems.append("longer than %d characters" % MAX_NAME)
    if re.search(r"[A-Z]", name):
        problems.append("uppercase not allowed")
    if re.search(r"[_\s]", name):
        problems.append("underscores/spaces not allowed")
    if re.search(r"[^a-zA-Z0-9\-_\s]", name):
        problems.append("only a-z, 0-9 and hyphens are allowed")
    if name.startswith("-") or name.endswith("-"):
        problems.append("must not start or end with a hyphen")
    if "--" in name:
        problems.append("consecutive hyphens not allowed")
    if problems or not NAME_RE.match(name):
        detail = "; ".join(problems) if problems else "does not match ^[a-z0-9]+(-[a-z0-9]+)*$"
        errors.append("name %r invalid: %s; try %r" % (name, detail, suggest_name(name)))
        return
    if name != dirname:
        errors.append(
            "name %r must equal the skill directory name %r: rename the directory "
            "or set 'name: %s'" % (name, dirname, dirname)
        )


def check_description(desc, errors, warnings):
    if not desc:
        errors.append(
            "frontmatter 'description' is missing or empty (required, 1-%d chars); "
            "state WHAT the skill does and WHEN to use it, with trigger keywords" % MAX_DESC
        )
        return
    if len(desc) > MAX_DESC:
        errors.append(
            "description is %d characters (max %d): trim it — a few keyword-rich "
            "sentences outperform a paragraph dump" % (len(desc), MAX_DESC)
        )
    ph = TEMPLATE_PLACEHOLDER.search(desc)
    if ph:
        errors.append(
            "description contains an unfilled template placeholder %r: replace "
            "every angle-bracket placeholder with specifics before shipping — "
            "a scaffolded description must never pass as done" % ph.group(0)
        )
    if len(desc) < 50:
        warnings.append(
            "description is only %d characters — too thin to trigger reliably; add "
            "what the skill does plus 'Use when …' contexts with the keywords users "
            "actually type" % len(desc)
        )
    # Quoted trigger phrases ("evaluate my agent") legitimately contain
    # first-person words — strip quoted spans before the voice check.
    desc_unquoted = QUOTED_SPAN.sub(" ", desc)
    if FIRST_PERSON.search(desc_unquoted):
        warnings.append(
            "description uses first/second-person voice (%r) outside quoted "
            "trigger phrases: rewrite in third person, e.g. 'Extracts …. Use "
            "when the user …'"
            % FIRST_PERSON.search(desc_unquoted).group(0)
        )
    if not WHEN_SIGNALS.search(desc):
        warnings.append(
            "description never states when to use the skill: add an explicit "
            "'Use when …' clause with trigger phrases — the description is the "
            "only text agents see before activation"
        )


def check_body(body, skill_dir, strict, errors, warnings, repo_root=None):
    body_lines = body.splitlines()
    n = len(body_lines)
    if n >= BODY_MAX_LINES:
        msg = (
            "SKILL.md body is %d lines (spec recommends < %d): move detail into "
            "references/ files with explicit load conditions" % (n, BODY_MAX_LINES)
        )
        (errors if strict else warnings).append(msg)
    elif n > BODY_WARN_LINES:
        warnings.append(
            "SKILL.md body is %d lines (warn threshold %d, spec limit %d): start "
            "moving reference material out now" % (n, BODY_WARN_LINES, BODY_MAX_LINES)
        )
    est_tokens = len(body) // 4
    if est_tokens > BODY_TOKEN_BUDGET:
        warnings.append(
            "SKILL.md body is roughly %d tokens (budget ~%d): every token competes "
            "with the user's task once the skill activates" % (est_tokens, BODY_TOKEN_BUDGET)
        )

    if BACKSLASH_PATH.search(body):
        errors.append(
            "backslash path found in SKILL.md (e.g. %r): the spec requires relative "
            "forward-slash paths" % BACKSLASH_PATH.search(body).group(0)
        )

    for marker in sorted(set(TODO_MARKER.findall(body))):
        warnings.append("unfinished-work marker %r found in SKILL.md body: resolve or remove it" % marker)

    # Fenced code blocks hold illustrative paths (example scanner reports,
    # template output) — only prose and links promise real files.
    prose = FENCED_BLOCK.sub("", body)

    # Unfilled scaffold placeholders in prose mean the skill is not done —
    # the whole point of "lint until clean" as a workflow gate. Inline code
    # spans are excluded (`<skill-dir>` CLI notation is legitimate).
    prose_no_code = INLINE_CODE.sub("", prose)
    for ph in sorted(set(m.group(0) for m in TEMPLATE_PLACEHOLDER.finditer(prose_no_code)))[:5]:
        errors.append(
            "unfilled template placeholder %s in SKILL.md body: replace it "
            "with real content before shipping" % ph
        )

    # A BARE_PATH match is only trustworthy as a standalone path when it's
    # actually delimited (whitespace, backtick, paren/bracket, start of
    # string) — not glued onto a preceding token. Without this, matches like
    # `<this-skill-dir>/scripts/x.py` (placeholder substitution — the ">" is
    # outside the char class, so the match starts at the bare "/") or
    # `"$SKILL_DIR/scripts/x.py"` (a shell variable, "$" outside the char
    # class) get misread as literal absolute/rooted paths.
    DELIMS = (" ", "\t", "\n", "(", "`", "[", '"', "'")
    bare_candidates = set()
    for m in BARE_PATH.finditer(prose):
        before = prose[m.start() - 1] if m.start() > 0 else " "
        if before in DELIMS:
            bare_candidates.add(m.group(0))

    candidates = set(MD_LINK.findall(prose)) | bare_candidates
    for cand in sorted(candidates):
        cand = cand.rstrip(".,:;)`'\"")
        # Strip a trailing file:line (or file:line:col) citation suffix —
        # common in review/debugging prose — before checking existence.
        cand = re.sub(r":\d+(?::\d+)?$", "", cand)
        if not cand or cand.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "\\" in cand:
            continue  # already reported as a backslash-path error
        # An ALL-CAPS leading segment (SKILL_DIR, REPO_ROOT, ...) is a
        # documented placeholder convention ("set SKILL_DIR to the path of
        # this skill"), not a literal directory name — real skill/repo dirs
        # in this convention are lowercase-hyphenated.
        if re.match(r"^[A-Z_][A-Z0-9_]*/", cand):
            continue

        if cand.startswith("~"):
            # Cross-skill/home-relative reference (e.g. the master+symlink
            # convention: `~/.claude/skills/other-skill/scripts/x.py`).
            # Verifiable for the current user; genuinely cross-machine only
            # if that user's home layout differs.
            if not os.path.exists(os.path.expanduser(cand)):
                errors.append(
                    "SKILL.md references %r (home-relative) but no such file exists: "
                    "fix the path or add the file" % cand
                )
            continue

        if cand.startswith("/"):
            # A machine-specific absolute path. Still worth checking it
            # resolves (a broken absolute reference is a real bug), but flag
            # the hardcoding itself as a separate portability issue either way
            # — CLAUDE.md's own rule is env vars over absolute paths.
            if not os.path.exists(cand):
                errors.append(
                    "SKILL.md references absolute path %r but it does not exist "
                    "on this machine: fix the path or add the file" % cand
                )
            warnings.append(
                "SKILL.md hardcodes a machine-specific absolute path (%r): use a "
                "relative path, '~/...', or an env var instead — this breaks for "
                "any other user or machine" % cand
            )
            continue

        # Plain relative reference. Check skill-relative first (the normal
        # case); some skills in this repo are documented to run "from the
        # repo root" instead (e.g. shared cross-cutting tools) — fall back to
        # repo-root-relative before calling it broken.
        if os.path.exists(os.path.join(skill_dir, cand)):
            continue
        if repo_root and os.path.exists(os.path.join(repo_root, cand)):
            warnings.append(
                "SKILL.md references %r which only resolves from the repo root, "
                "not from within the skill directory: say so explicitly (e.g. "
                "'from the repo root:') or use an unambiguous path" % cand
            )
            continue
        errors.append(
            "SKILL.md references %r but no such file exists in the skill "
            "directory%s: fix the path or add the file" % (
                cand, "" if repo_root else " (repo root not checked)"
            )
        )


def lint(skill_dir, strict=False, repo_root=None):
    errors, warnings = [], []
    skill_dir = os.path.abspath(skill_dir)
    dirname = os.path.basename(skill_dir)
    if repo_root:
        repo_root = os.path.abspath(repo_root)

    if not os.path.isdir(skill_dir):
        return ["%s is not a directory" % skill_dir], []

    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        errors.append("SKILL.md not found in %s (required at the skill root)" % skill_dir)
        return errors, warnings

    with open(skill_md, encoding="utf-8") as fh:
        text = fh.read()

    fm, body, perr = parse_frontmatter(text)
    if perr:
        errors.append("frontmatter parse error: %s" % perr)
        return errors, warnings

    check_name(fm.get("name"), dirname, errors)
    check_description(fm.get("description"), errors, warnings)

    compat = fm.get("compatibility")
    if compat is not None:
        if isinstance(compat, dict):
            compat = ""  # bare `compatibility:` with no value parses as an empty map
        if not str(compat).strip():
            warnings.append("compatibility is present but empty: remove it (most skills need none)")
        elif len(str(compat)) > MAX_COMPAT:
            errors.append("compatibility is %d characters (max %d)" % (len(str(compat)), MAX_COMPAT))

    metadata = fm.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        warnings.append("metadata should be a map of string keys to string values, got a scalar")

    for key in fm:
        if key not in KNOWN_KEYS:
            warnings.append(
                "unknown frontmatter key %r: only %s are defined by the spec; "
                "custom properties belong under 'metadata'" % (key, ", ".join(sorted(KNOWN_KEYS)))
            )

    check_body(body, skill_dir, strict, errors, warnings, repo_root=repo_root)

    # Any bundled resource directory counts — skills legitimately organize
    # on-demand material under names other than references/ (e.g. rules/).
    RESOURCE_DIRS = ("scripts", "references", "assets", "rules", "data",
                     "agents", "templates", "examples")
    bundled = [d for d in RESOURCE_DIRS
               if os.path.isdir(os.path.join(skill_dir, d))]
    if not bundled:
        (errors if strict else warnings).append(
            "text-only skill: no bundled resources (looked for %s) — "
            "production-grade skills ship executable tools or on-demand "
            "references; if all value lives in prose, reconsider whether "
            "this should be a skill at all"
            % "/, ".join(RESOURCE_DIRS)
        )

    return errors, warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate an agent skill directory (agentskills.io spec).")
    parser.add_argument("skill_dir", help="path to the skill directory (the folder containing SKILL.md)")
    parser.add_argument("--strict", action="store_true", help="promote spec-limit violations (500+ line body) to errors")
    parser.add_argument("--json", action="store_true", dest="as_json", help="emit machine-readable JSON")
    parser.add_argument("--repo-root", help="also accept relative paths resolved from this root "
                                             "(some skills document themselves as run 'from the repo root')")
    args = parser.parse_args(argv)

    errors, warnings = lint(args.skill_dir, strict=args.strict, repo_root=args.repo_root)

    if args.as_json:
        print(json.dumps({
            "skill": os.path.abspath(args.skill_dir),
            "strict": args.strict,
            "errors": errors,
            "warnings": warnings,
            "passed": not errors,
        }, indent=2))
    else:
        print("Linting %s (strict=%s)" % (os.path.abspath(args.skill_dir), "on" if args.strict else "off"))
        for msg in errors:
            print("  ERROR: %s" % msg)
        for msg in warnings:
            print("  WARN:  %s" % msg)
        verdict = "PASS" if not errors else "FAIL"
        print("  %s — %d error(s), %d warning(s)" % (verdict, len(errors), len(warnings)))

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
