#!/usr/bin/env python3
"""Scaffold a derived skill from a watched video, with provenance attached.

Reads video metadata from the `watch` work directory when it is available
(free, no network) and falls back to a yt-dlp metadata call. Writes a staging
directory -- never into a live skills tree. Installation is a separate,
explicit step that happens only after check_derived_skill.py passes.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def slug_ok(name: str) -> bool:
    return bool(NAME_RE.match(name)) and len(name) <= 64


def find_info_json(work_dir: Path | None) -> Path | None:
    if work_dir is None:
        return None
    for candidate in (work_dir / "download", work_dir):
        if not candidate.is_dir():
            continue
        hits = sorted(candidate.glob("*.info.json"))
        if hits:
            return hits[0]
    return None


def metadata_from_info_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "title": data.get("title", ""),
        "uploader": data.get("uploader") or data.get("channel", ""),
        "upload_date": data.get("upload_date", ""),
        "duration": data.get("duration"),
        "webpage_url": data.get("webpage_url", ""),
        "source": f"info.json ({path})",
    }


def metadata_from_ytdlp(url: str) -> dict:
    try:
        out = subprocess.run(
            ["yt-dlp", "--skip-download", "--dump-single-json", url],
            capture_output=True,
            text=True,
            timeout=120,
            check=True,
        )
    except FileNotFoundError:
        return {"source": "unavailable (yt-dlp not installed)", "webpage_url": url}
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        sys.stderr.write(f"warning: yt-dlp metadata lookup failed: {exc}\n")
        return {"source": "unavailable (yt-dlp lookup failed)", "webpage_url": url}
    data = json.loads(out.stdout)
    return {
        "title": data.get("title", ""),
        "uploader": data.get("uploader") or data.get("channel", ""),
        "upload_date": data.get("upload_date", ""),
        "duration": data.get("duration"),
        "webpage_url": data.get("webpage_url", url),
        "source": "yt-dlp live lookup",
    }


def fmt_upload_date(raw: str) -> str:
    if len(raw) == 8 and raw.isdigit():
        return f"{raw[0:4]}-{raw[4:6]}-{raw[6:8]}"
    return raw or "unknown"


def fmt_duration(seconds) -> str:
    if not isinstance(seconds, (int, float)):
        return "unknown"
    seconds = int(seconds)
    return f"{seconds // 60}:{seconds % 60:02d}"


SKILL_TEMPLATE = """---
name: {name}
description: TODO-DESCRIBE — one sentence starting "Use when ...", naming the trigger phrases a user would actually type. Must be specific enough that it cannot collide with an existing skill.
metadata:
  derived-from-video: {url}
  derived-on: '{today}'
  source-upload-date: '{upload_date}'
---

# {title_case}

TODO-SUMMARY — two sentences: what this does, and what it deliberately does not do.

**Source:** derived from a video demonstration, not from running the workflow.
See `references/source-video.md` for provenance and `references/environment-bindings.md`
for every assumption that came from the demonstrator's machine rather than yours.

## When to invoke

TODO-TRIGGERS — the situations and phrasings that should route here.

## Procedure

Each step names the tool route it runs on in this host, not the click the
demonstrator made. A step that can only be performed by a human hand is marked
`BLOCKED-ON-USER` and stops the run.

1. TODO-STEP — route: `Bash` | `Playwright MCP` | `Read/Write` | `API` | `BLOCKED-ON-USER`
2. TODO-STEP

## Judgment rules

Editable policy. These are the thresholds and preferences the demonstrator
stated out loud; they are the part of the skill most likely to need tuning, so
they live here rather than buried in the steps.

- TODO-RULE — with the timestamp it came from, e.g. `(video 10:39)`

## Environment bindings

Everything below was true on the demonstrator's machine. Each row must be
resolved before this skill runs. See `references/environment-bindings.md`.

| Binding | In the video | On this machine |
|---|---|---|
| TODO | TODO | UNRESOLVED |

## Verification

A command or observable check that proves the skill worked, not a claim that it
did:

```bash
TODO-VERIFY
```

## Limits

- Derived from pixels and narration, not an event stream: exact selectors,
  coordinates, and any step performed off-screen were never captured.
- Third-party UI shown in the source video dates from {upload_date_h}. Treat
  every UI specific as expiring evidence and re-check before trusting it.
- TODO-LIMITS
"""

PROVENANCE_TEMPLATE = """# Source video

| Field | Value |
|---|---|
| URL | {url} |
| Title | {title} |
| Uploader | {uploader} |
| Uploaded | {upload_date} |
| Duration | {duration} |
| Derived on | {today} |
| Metadata source | {source} |

## Why this file exists

This skill was derived from a demonstration, so its claims are only as current
as the video. When a step stops working, check this date first: UI shown in a
video from {upload_date} may simply have changed.

## Demonstration span

TODO — the timestamp range containing the actual demonstration, excluding
intro, sponsor reads, and outro.

## Cited moments

Every procedural step and judgment rule in SKILL.md carries the timestamp it was
read from. List anything load-bearing here.

| Timestamp | What it establishes |
|---|---|
| TODO | TODO |
"""

BINDINGS_TEMPLATE = """# Environment bindings

The gap between a screen recording of your own machine and a video of someone
else's is entirely in this file. Cowork's record-a-skill has no equivalent
problem: it recorded you, so the paths, logins, and installed extensions were
already yours.

Each binding starts `UNRESOLVED`. Resolve it by one of:

- **substitute** — the same job, done a different way on this machine
- **confirm** — verified to exist here as well
- **drop** — the step existed only because of the demonstrator's setup
- **BLOCKED-ON-USER** — needs a credential or a human decision

Never resolve a binding by assuming. A binding guessed wrong produces a skill
that fails silently on someone else's environment, which is worse than a skill
that refuses to start.

| # | Binding | In the video | Resolution | Notes |
|---|---|---|---|---|
| 1 | TODO | TODO | UNRESOLVED | |

## Credentials

Any step requiring a logged-in session is `BLOCKED-ON-USER` by default. Do not
write credentials into this file, into SKILL.md, or into any run artifact.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--name", required=True, help="kebab-case skill name (== directory name)")
    ap.add_argument("--url", required=True, help="source video URL")
    ap.add_argument("--out-dir", required=True, help="staging directory (NOT a live skills tree)")
    ap.add_argument("--work-dir", help="watch work directory, to reuse its metadata for free")
    ap.add_argument("--force", action="store_true", help="overwrite an existing staging dir")
    args = ap.parse_args()

    if not slug_ok(args.name):
        sys.stderr.write(
            f"ERROR: --name must be kebab-case ([a-z0-9] and hyphens), got {args.name!r}\n"
        )
        return 2

    out_root = Path(args.out_dir).expanduser()
    target = out_root / args.name
    if target.exists() and not args.force:
        sys.stderr.write(f"ERROR: {target} already exists (pass --force to overwrite)\n")
        return 2

    for marker in (".claude/skills", ".agents/skills", ".github/skills"):
        if marker in str(target):
            sys.stderr.write(
                f"ERROR: refusing to scaffold into a live skills tree: {target}\n"
                "Stage the skill elsewhere and install it only after the gate passes.\n"
            )
            return 2

    info = find_info_json(Path(args.work_dir).expanduser() if args.work_dir else None)
    meta = metadata_from_info_json(info) if info else metadata_from_ytdlp(args.url)

    upload_date = fmt_upload_date(meta.get("upload_date", ""))
    today = date.today().isoformat()
    title_case = args.name.replace("-", " ").title()

    (target / "references").mkdir(parents=True, exist_ok=True)

    (target / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(
            name=args.name,
            url=meta.get("webpage_url") or args.url,
            today=today,
            upload_date=upload_date,
            upload_date_h=upload_date,
            title_case=title_case,
        ),
        encoding="utf-8",
    )
    (target / "references" / "source-video.md").write_text(
        PROVENANCE_TEMPLATE.format(
            url=meta.get("webpage_url") or args.url,
            title=meta.get("title") or "unknown",
            uploader=meta.get("uploader") or "unknown",
            upload_date=upload_date,
            duration=fmt_duration(meta.get("duration")),
            today=today,
            source=meta.get("source", "unknown"),
        ),
        encoding="utf-8",
    )
    (target / "references" / "environment-bindings.md").write_text(
        BINDINGS_TEMPLATE, encoding="utf-8"
    )

    print(f"scaffolded: {target}")
    print(f"  SKILL.md                            (fill every TODO-* marker)")
    print(f"  references/source-video.md          (provenance: {upload_date})")
    print(f"  references/environment-bindings.md  (resolve every UNRESOLVED row)")
    print()
    print("Next: fill it in, then gate it:")
    print(f"  python3 scripts/check_derived_skill.py {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
