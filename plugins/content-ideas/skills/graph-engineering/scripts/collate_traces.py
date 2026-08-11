#!/usr/bin/env python3
"""Collate captured agent traces into a review packet for the tuning loop.

Reading traces is the primary debugging loop for a contract harness — not
running more experiments. This script indexes what was captured and writes the
divergence-hunting prompt so a fresh session can work through it.

It deliberately does not summarize the traces. Summaries are where the signal
dies; the point is to read what the agent actually did.

Stdlib only.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

TRACE_GLOBS = ("*.txt", "*.log", "*.jsonl", "*.md")

# Cheap signals worth flagging so you know which trace to open first. These are
# pointers for a human reader, not a verdict.
SIGNALS = {
    "deferral": [
        r"\bfix (?:it )?later\b", r"\bfor now\b", r"\bwe can revisit\b",
        r"\btake[s]? (?:about )?\d+ weeks?\b", r"\bgood enough\b",
        r"\bpunt\b", r"\bfollow[- ]up\b",
    ],
    "unverified pass": [
        r"\blooks? (?:fine|good|correct)\b", r"\bseems to work\b",
        r"\bshould (?:be )?work\b", r"\bpresumably\b", r"\bassuming\b",
        r"\bprobably (?:fine|correct|works)\b",
    ],
    "hedge": [
        r"\bappropriate(?:ly)?\b", r"\breasonabl[ey]\b", r"\bmostly\b",
        r"\bpartial(?:ly)? pass\b",
    ],
}

REVIEW_PROMPT = """\
Read every trace file listed below, in full. Do not summarize them to me.

For each point where the auditor passed something it should have failed:
1. Quote the exact moment from the trace, with the file name.
2. Say what a careful human reviewer would have caught there.
3. Propose a specific edit to `.claude/agents/auditor.md` that would have
   caught it.

Do not rewrite the whole prompt. Give me targeted changes, each tied to the
trace line that justifies it.

If you find no such moment, say so plainly rather than inventing one.
"""


def scan(path: Path) -> dict[str, int]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    hits: dict[str, int] = {}
    lowered = text.lower()
    for label, patterns in SIGNALS.items():
        count = sum(len(re.findall(p, lowered)) for p in patterns)
        if count:
            hits[label] = count
    return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Collate agent traces into a review packet.",
    )
    ap.add_argument("--dir", default=".", help="Project directory")
    ap.add_argument(
        "--traces", default="traces",
        help="Trace subdirectory relative to --dir (default: traces)",
    )
    ap.add_argument(
        "--out", default=None,
        help="Output path (default: <traces>/REVIEW.md)",
    )
    args = ap.parse_args(argv)

    root = Path(args.dir).expanduser().resolve()
    trace_dir = (root / args.traces).resolve()
    if not trace_dir.is_dir():
        print(f"FAIL: no trace directory at {trace_dir}", file=sys.stderr)
        print("      capture runs first, e.g.:", file=sys.stderr)
        print('      claude -p "$(cat prompt.txt)" > traces/run-$(date +%F-%H%M).txt 2>&1',
              file=sys.stderr)
        return 1

    files: list[Path] = []
    for pattern in TRACE_GLOBS:
        files.extend(trace_dir.glob(pattern))
    files = sorted({f for f in files if f.name != "REVIEW.md"})

    if not files:
        print(f"FAIL: no trace files in {trace_dir}", file=sys.stderr)
        return 1

    out_path = Path(args.out).resolve() if args.out else trace_dir / "REVIEW.md"

    lines = [
        "# Trace review packet",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Traces: `{trace_dir}`",
        "",
        "## The prompt to run in a fresh session",
        "",
        "```text",
        REVIEW_PROMPT.rstrip(),
        "```",
        "",
        "## Trace files",
        "",
        "| File | Size | Lines | Signals to check first |",
        "|---|---|---|---|",
    ]

    total_bytes = 0
    flagged = 0
    for f in files:
        size = f.stat().st_size
        total_bytes += size
        try:
            n_lines = sum(1 for _ in f.open("r", encoding="utf-8", errors="replace"))
        except OSError:
            n_lines = 0
        hits = scan(f)
        if hits:
            flagged += 1
        signal = ", ".join(f"{k} ×{v}" for k, v in sorted(hits.items())) or "—"
        lines.append(
            f"| `{f.name}` | {size / 1024:.1f} KB | {n_lines} | {signal} |"
        )

    lines += [
        "",
        f"**{len(files)} trace(s), {total_bytes / 1024:.1f} KB total. "
        f"{flagged} carry at least one signal.**",
        "",
        "The signal column is a hint about which file to open first. It is a "
        "regex over the text, not a verdict — a trace with no signals can still "
        "be where the loop went wrong, and a flagged line can be entirely fine "
        "in context.",
        "",
        "Read the whole thing. Grepping traces with a second agent is a useful "
        "first pass for finding where a run veered off; it does not replace "
        "reading them line by line. Understanding why the model thought what it "
        "thought is the skill being built here.",
        "",
    ]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {out_path}")
    print(f"  {len(files)} trace(s), {total_bytes / 1024:.1f} KB, {flagged} flagged")
    print("\nOpen a fresh session and run the prompt at the top of that file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
