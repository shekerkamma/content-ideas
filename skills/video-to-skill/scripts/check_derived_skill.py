#!/usr/bin/env python3
"""Gate a video-derived skill before it is installed anywhere.

A skill derived from a demonstration fails in ways a hand-written one does not:
placeholders left unfilled, environment assumptions silently inherited from the
demonstrator's machine, and confident steps with nothing that proves they ran.
Each rule below exists for one of those.

Exit 0 = safe to install. Non-zero = do not install; the failures are listed.

Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Match the marker forms init_skill.py actually writes -- NOT every occurrence of
# the word TODO. A derived skill may legitimately document a tool that scans for
# TODO/FIXME (the /audit gate in ai-blueprint-build-loop does exactly that), and
# a rule that fires on quoted subject matter trains people to bypass it.
PLACEHOLDER_RE = re.compile(
    r"""
      TODO-[A-Z][A-Z-]*        # scaffold markers: TODO-DESCRIBE, TODO-STEP, ...
    | PLACEHOLDER
    | <fill[-\s]in>
    | ^\s*TODO\s*$             # a line that is only TODO
    | \|\s*TODO\s*(?=\|)       # a table cell that is only TODO
    """,
    re.VERBOSE | re.MULTILINE,
)
DEFAULT_SKILL_ROOTS = [
    "~/.claude/skills",
    "~/.codex/skills",
    "~/.agents/skills",
]


class Report:
    def __init__(self) -> None:
        self.failures: list[tuple[str, str]] = []
        self.warnings: list[tuple[str, str]] = []

    def fail(self, rule: str, msg: str) -> None:
        self.failures.append((rule, msg))

    def warn(self, rule: str, msg: str) -> None:
        self.warnings.append((rule, msg))


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter-ish dict of top-level scalars, body). Empty dict if unclosed."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end]
    body = text[end + 4 :]
    fm: dict[str, str] = {}
    for line in raw.splitlines():
        if not line or line.startswith((" ", "\t", "#")):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip().strip("'\"")
    return fm, body


def sections(body: str) -> dict[str, str]:
    out: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current = line[3:].strip().lower()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    return out


def check_frontmatter(text: str, skill_dir: Path, rep: Report) -> dict:
    if not text.startswith("---"):
        rep.fail("frontmatter", "SKILL.md does not open with a '---' frontmatter block")
        return {}
    fm, _ = split_frontmatter(text)
    if not fm:
        rep.fail("frontmatter", "frontmatter block is never closed with '---'")
        return {}
    name = fm.get("name", "")
    if not name:
        rep.fail("name", "frontmatter has no 'name:' key")
    elif name != skill_dir.name:
        rep.fail("name", f"name: {name!r} does not match directory name {skill_dir.name!r}")
    desc = fm.get("description", "")
    if not desc:
        rep.fail("desc", "frontmatter has no 'description:' key")
    return fm


def check_routing(fm: dict, secs: dict, rep: Report) -> None:
    desc = fm.get("description", "")
    if len(desc) < 40 and "when to invoke" not in secs:
        rep.fail(
            "routing",
            "description is under 40 chars and there is no '## When to invoke' section — "
            "nothing can route to this skill",
        )


def check_placeholders(text: str, label: str, rep: Report) -> None:
    hits = sorted({m.group(0) for m in PLACEHOLDER_RE.finditer(text)})
    if hits:
        rep.fail(
            "placeholders",
            f"{label} still contains unfilled markers: {', '.join(hits[:6])}"
            + (" ..." if len(hits) > 6 else ""),
        )


def check_judgment_rules(secs: dict, rep: Report) -> None:
    body = secs.get("judgment rules")
    if body is None:
        rep.fail(
            "judgment",
            "no '## Judgment rules' section — thresholds and preferences from the video must "
            "be stated as editable policy, not buried in step text",
        )
        return
    bullets = [ln for ln in body.splitlines() if ln.strip().startswith(("-", "*", "1."))]
    if not bullets:
        rep.fail("judgment", "'## Judgment rules' section is empty")
        return
    # Search the whole section, not just the bullet's first line: a wrapped
    # bullet carries its "(video 37:22)" citation on a continuation line.
    if not re.search(r"\d{1,2}:\d{2}", body):
        rep.warn(
            "judgment",
            "no judgment rule cites a video timestamp — rules should be traceable to the "
            "moment the demonstrator stated them",
        )


def check_bindings(secs: dict, skill_dir: Path, rep: Report) -> None:
    bindings_file = skill_dir / "references" / "environment-bindings.md"
    texts = []
    if "environment bindings" in secs:
        texts.append(("SKILL.md '## Environment bindings'", secs["environment bindings"]))
    if bindings_file.is_file():
        texts.append((str(bindings_file), bindings_file.read_text(encoding="utf-8")))
    if not texts:
        rep.fail(
            "bindings",
            "no '## Environment bindings' section and no references/environment-bindings.md — "
            "a video-derived skill must state what it inherited from the demonstrator's machine",
        )
        return
    for label, text in texts:
        # Only the table rows matter; the explanatory prose legitimately uses the word.
        rows = [ln for ln in text.splitlines() if ln.strip().startswith("|")]
        unresolved = [ln for ln in rows if "UNRESOLVED" in ln]
        if unresolved:
            rep.fail(
                "bindings",
                f"{label} has {len(unresolved)} UNRESOLVED binding row(s) — resolve each as "
                "confirm / substitute / drop / BLOCKED-ON-USER before installing",
            )


def check_verification(secs: dict, rep: Report, allow_unexecuted: bool) -> None:
    body = secs.get("verification")
    if body is None:
        rep.fail(
            "verify",
            "no '## Verification' section — a derived skill must ship the command that proves "
            "it worked, not a claim that it did",
        )
        return
    if "```" not in body:
        rep.fail("verify", "'## Verification' section has no command block")

    # A skill derived from a video and never run is a hypothesis, not a skill.
    # Shipping the command that would prove it is not the same as having run it,
    # and a gate that cannot tell the difference certifies untested work.
    executed = re.search(
        r"\b(executed|verified|ran|run)\b[^.\n]{0,60}?\d{4}-\d{2}-\d{2}", body, re.IGNORECASE
    ) or re.search(r"\d{4}-\d{2}-\d{2}[^.\n]{0,60}?\b(executed|verified)\b", body, re.IGNORECASE)
    declared_unexecuted = re.search(r"NOT[ -]EXECUTED", body)

    if executed:
        return
    if declared_unexecuted:
        if allow_unexecuted:
            rep.warn(
                "executed",
                "skill declares NOT EXECUTED and --allow-unexecuted was passed: this is a "
                "derived hypothesis, not a validated skill. Do not present it as working",
            )
        else:
            rep.fail(
                "executed",
                "skill declares NOT EXECUTED — run it on the narrowest real case first. "
                "Pass --allow-unexecuted only when execution is genuinely blocked, and say so "
                "when reporting",
            )
        return
    rep.fail(
        "executed",
        "'## Verification' does not record an execution: state 'Executed <YYYY-MM-DD>' with "
        "what actually happened, or write NOT EXECUTED explicitly. A gate that cannot tell "
        "the two apart certifies untested work",
    )


def check_provenance(skill_dir: Path, rep: Report) -> None:
    path = skill_dir / "references" / "source-video.md"
    if not path.is_file():
        rep.fail("provenance", "missing references/source-video.md")
        return
    text = path.read_text(encoding="utf-8")
    if not re.search(r"https?://\S+", text):
        rep.fail("provenance", "references/source-video.md records no source URL")
    if not re.search(r"\d{4}-\d{2}-\d{2}", text):
        rep.fail(
            "provenance",
            "references/source-video.md records no date — UI shown in a video expires, and the "
            "upload date is how a future reader knows when to stop trusting it",
        )


def check_secrets(skill_dir: Path, rep: Report) -> None:
    patterns = [
        (re.compile(r"sk-[A-Za-z0-9]{16,}"), "OpenAI-style key"),
        (re.compile(r"gsk_[A-Za-z0-9]{16,}"), "Groq-style key"),
        (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub token"),
        (re.compile(r"AKIA[0-9A-Z]{12,}"), "AWS access key id"),
        (re.compile(r"(?i)\b(password|passwd|secret)\s*[=:]\s*\S{6,}"), "inline credential"),
    ]
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".json", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for rx, label in patterns:
            if rx.search(text):
                rep.fail("secrets", f"{path} appears to contain a {label} — remove it")


def check_collisions(skill_dir: Path, roots: list[str], rep: Report) -> None:
    name = skill_dir.name
    resolved_self = skill_dir.resolve()
    for root in roots:
        base = Path(root).expanduser()
        if not base.is_dir():
            continue
        for candidate in base.rglob("SKILL.md"):
            other = candidate.parent
            if other.resolve() == resolved_self:
                continue
            if other.name == name:
                rep.fail(
                    "collision",
                    f"a skill named {name!r} already exists at {other} — pick another name or "
                    "update that skill instead of installing a second one",
                )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("skill_dir", help="staged skill directory to gate")
    ap.add_argument(
        "--skills-root",
        action="append",
        default=None,
        help="skills tree to check for name collisions (repeatable). "
        f"Default: {', '.join(DEFAULT_SKILL_ROOTS)}",
    )
    ap.add_argument("--no-collision-check", action="store_true")
    ap.add_argument(
        "--allow-unexecuted",
        action="store_true",
        help="downgrade the execution requirement to a warning. Only for skills whose "
        "execution is genuinely blocked (paid service, hardware, destructive action).",
    )
    args = ap.parse_args()

    # resolve() before anything reads .name -- Path(".").name is "", which would
    # make the name rule fail on every relative-path invocation.
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        sys.stderr.write(f"ERROR: no SKILL.md at {skill_md}\n")
        return 2

    text = skill_md.read_text(encoding="utf-8")
    rep = Report()

    fm = check_frontmatter(text, skill_dir, rep)
    _, body = split_frontmatter(text)
    secs = sections(body)

    check_routing(fm, secs, rep)
    check_placeholders(text, "SKILL.md", rep)
    for ref in sorted((skill_dir / "references").glob("*.md")) if (skill_dir / "references").is_dir() else []:
        check_placeholders(ref.read_text(encoding="utf-8"), str(ref), rep)
    check_judgment_rules(secs, rep)
    check_bindings(secs, skill_dir, rep)
    check_verification(secs, rep, args.allow_unexecuted)
    check_provenance(skill_dir, rep)
    check_secrets(skill_dir, rep)
    if not args.no_collision_check:
        check_collisions(skill_dir, args.skills_root or DEFAULT_SKILL_ROOTS, rep)

    for rule, msg in rep.warnings:
        print(f"WARN  [{rule}] {msg}")
    for rule, msg in rep.failures:
        print(f"FAIL  [{rule}] {msg}")

    if rep.failures:
        print(f"\n{len(rep.failures)} failure(s) — do not install.")
        return 1
    print(f"PASS — {skill_dir} is safe to install ({len(rep.warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
