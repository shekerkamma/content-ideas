#!/usr/bin/env python3
"""Turn a Deep Research `agent status` JSON into a Markdown report plus saved charts.

  dr_extract.py dr-result.json research.md [--media DIR]

The report arrives split across several `model_output` text parts. Joining all of them in
order matters: keeping only the longest part drops the report's opening sections. Image parts
(the charts the agent draws) are saved as DIR/research-chart-N.<ext> and linked inline.
Prints the usage line for the cost estimate. Exit 0 = report written, 1 = not completed or empty.
"""
from __future__ import annotations
import argparse, base64, json, os, sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("result"); ap.add_argument("out")
    ap.add_argument("--media", default=None, help="folder for chart images (default: next to OUT)")
    a = ap.parse_args()
    d = json.load(open(a.result))
    if d.get("status") != "completed":
        print(f"status is {d.get('status')!r}, not completed")
        return 1
    media = a.media or os.path.dirname(os.path.abspath(a.out))
    os.makedirs(media, exist_ok=True)
    rel = os.path.relpath(media, os.path.dirname(os.path.abspath(a.out)))
    parts, n = [], 0
    for step in d.get("steps", []):
        if step.get("type") != "model_output":
            continue
        for c in step.get("content") or []:
            if c.get("type") == "text":
                parts.append(c["text"])
            elif c.get("type") == "image" and c.get("data"):
                n += 1
                ext = (c.get("mime_type") or "image/png").split("/")[-1]
                name = f"research-chart-{n}.{ext}"
                with open(os.path.join(media, name), "wb") as f:
                    f.write(base64.b64decode(c["data"]))
                parts.append(f"\n![chart {n}]({rel}/{name})\n")
    report = "\n".join(parts).strip()
    if not report:
        print("no text parts in the result")
        return 1
    with open(a.out, "w") as f:
        f.write(report + "\n")
    u = d.get("usage") or {}
    searches = sum(g.get("count", 0) for g in u.get("grounding_tool_count") or [])
    print(f"wrote {a.out}: {len(report.split())} words, {n} chart(s); first line: {report.splitlines()[0][:80]!r}")
    print(f"usage: input {u.get('total_input_tokens')} (cached {u.get('total_cached_tokens')}), "
          f"output {u.get('total_output_tokens')}, thinking {u.get('total_thought_tokens')}, searches {searches}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
