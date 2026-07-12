#!/usr/bin/env python3
"""Package content-pipeline markdown outputs into business-facing artifacts."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
from pathlib import Path
from typing import Iterable


DELIVERABLE_NAMES = [
    "business-outcome-memo.md",
    "source-register.md",
    "editorial-brief.md",
    "article-draft.md",
    "linkedin-post.md",
    "x-thread.md",
    "newsletter-blurb.md",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").strip()


def first_heading(markdown: str, fallback: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def strip_heading(markdown: str) -> str:
    lines = markdown.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).strip()
    return markdown


def md_inline(value: str) -> str:
    escaped = html.escape(value)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    url_pattern = r"(https?://[^\s<]+)"
    escaped = re.sub(url_pattern, r'<a href="\1">\1</a>', escaped)
    return escaped


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    in_list = False
    in_ol = False
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append(f"<p>{md_inline(' '.join(paragraph))}</p>")
            paragraph = []

    def close_lists() -> None:
        nonlocal in_list, in_ol
        if in_list:
            out.append("</ul>")
            in_list = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    for line in lines:
        raw = line.rstrip()
        if not raw:
            flush_paragraph()
            close_lists()
            continue
        if raw.startswith("### "):
            flush_paragraph()
            close_lists()
            out.append(f"<h3>{md_inline(raw[4:])}</h3>")
        elif raw.startswith("## "):
            flush_paragraph()
            close_lists()
            out.append(f"<h2>{md_inline(raw[3:])}</h2>")
        elif raw.startswith("# "):
            flush_paragraph()
            close_lists()
            out.append(f"<h1>{md_inline(raw[2:])}</h1>")
        elif raw.startswith("- "):
            flush_paragraph()
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{md_inline(raw[2:].strip())}</li>")
        elif re.match(r"^\d+\.\s+", raw):
            flush_paragraph()
            if in_list:
                out.append("</ul>")
                in_list = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{md_inline(re.sub(r'^\\d+\\.\\s+', '', raw))}</li>")
        else:
            paragraph.append(raw)

    flush_paragraph()
    close_lists()
    return "\n".join(out)


def load_deliverables(deliverables_dir: Path) -> dict[str, str]:
    payload = {}
    for name in DELIVERABLE_NAMES:
        path = deliverables_dir / name
        if path.exists():
            payload[name] = read_text(path)
    return payload


def write_business_package(deliverables_dir: Path, output_dir: Path, date: str) -> Path:
    docs = load_deliverables(deliverables_dir)
    metadata_path = deliverables_dir / "deliverables-metadata.json"
    metadata = json.loads(read_text(metadata_path)) if metadata_path.exists() else {}
    angle = metadata.get("business_angle", {})
    title = angle.get("title") or first_heading(docs.get("article-draft.md", ""), "Business Content Package")
    claim = angle.get("claim") or "Generated business content package"

    sections = []
    for name in DELIVERABLE_NAMES:
        if name not in docs:
            continue
        label = name.replace(".md", "").replace("-", " ").title()
        sections.append(
            f"<section><div class=\"section-label\">{html.escape(label)}</div>"
            f"{markdown_to_html(docs[name])}</section>"
        )

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --ink: #161616;
      --muted: #5a5f66;
      --line: #d9dee4;
      --panel: #f7f8fa;
      --accent: #0f766e;
      --accent-2: #a16207;
    }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: var(--ink);
      background: white;
      line-height: 1.55;
    }}
    .wrap {{
      max-width: 1040px;
      margin: 0 auto;
      padding: 40px 28px 64px;
    }}
    header {{
      border-bottom: 2px solid var(--line);
      padding-bottom: 24px;
      margin-bottom: 28px;
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .04em;
    }}
    h1 {{
      font-size: 34px;
      line-height: 1.15;
      margin: 10px 0 12px;
      letter-spacing: 0;
    }}
    h2 {{
      font-size: 22px;
      margin: 26px 0 10px;
      border-top: 1px solid var(--line);
      padding-top: 18px;
    }}
    h3 {{
      font-size: 17px;
      margin: 18px 0 8px;
    }}
    p, li {{
      font-size: 15px;
    }}
    a {{
      color: var(--accent);
      overflow-wrap: anywhere;
    }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin: 22px 0 10px;
    }}
    .metric {{
      background: var(--panel);
      border: 1px solid var(--line);
      padding: 12px;
      min-height: 76px;
    }}
    .metric strong {{
      display: block;
      font-size: 20px;
      margin-bottom: 4px;
    }}
    .metric span {{
      color: var(--muted);
      font-size: 13px;
    }}
    section {{
      margin: 30px 0;
    }}
    .section-label {{
      color: var(--accent-2);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    code {{
      background: #eef2f4;
      padding: 1px 4px;
      border-radius: 3px;
    }}
    @media (max-width: 760px) {{
      .summary {{
        grid-template-columns: 1fr 1fr;
      }}
      h1 {{
        font-size: 27px;
      }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <header>
      <div class="eyebrow">Hermes Content Pipeline · Business Package · {html.escape(date)}</div>
      <h1>{html.escape(title)}</h1>
      <p>{html.escape(claim)}</p>
      <div class="summary">
        <div class="metric"><strong>{html.escape(str(metadata.get("source_count", "n/a")))}</strong><span>source signals used</span></div>
        <div class="metric"><strong>{html.escape(str(len(metadata.get("deliverables", []))))}</strong><span>deliverables generated</span></div>
        <div class="metric"><strong>{html.escape(metadata.get("mode", "unknown"))}</strong><span>run mode</span></div>
        <div class="metric"><strong>No</strong><span>publish action taken</span></div>
      </div>
    </header>
    {''.join(sections)}
  </main>
</body>
</html>
"""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "business-package.html"
    path.write_text(html_doc, encoding="utf-8")
    return path


def write_csv(path: Path, rows: Iterable[dict[str, str]], fieldnames: list[str]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


def write_content_calendar(deliverables_dir: Path, output_dir: Path, date: str) -> Path:
    metadata = json.loads(read_text(deliverables_dir / "deliverables-metadata.json"))
    angle = metadata.get("business_angle", {})
    base_title = angle.get("title", "Generated Content Package")
    rows = [
        {
            "date": date,
            "channel": "Blog / Long-form",
            "asset": "article-draft.md",
            "business_goal": "Explain the agent operating-layer thesis",
            "status": "draft_review",
            "owner": "human_editor",
            "source": str(deliverables_dir / "article-draft.md"),
            "headline": base_title,
        },
        {
            "date": date,
            "channel": "LinkedIn",
            "asset": "linkedin-post.md",
            "business_goal": "Start business conversation with operators",
            "status": "draft_review",
            "owner": "human_editor",
            "source": str(deliverables_dir / "linkedin-post.md"),
            "headline": angle.get("claim", base_title),
        },
        {
            "date": date,
            "channel": "X",
            "asset": "x-thread.md",
            "business_goal": "Test concise thesis framing",
            "status": "draft_review",
            "owner": "human_editor",
            "source": str(deliverables_dir / "x-thread.md"),
            "headline": angle.get("claim", base_title),
        },
        {
            "date": date,
            "channel": "Newsletter",
            "asset": "newsletter-blurb.md",
            "business_goal": "Nurture existing audience with implementation pattern",
            "status": "draft_review",
            "owner": "human_editor",
            "source": str(deliverables_dir / "newsletter-blurb.md"),
            "headline": angle.get("claim", base_title),
        },
    ]
    return write_csv(
        output_dir / "content-calendar.csv",
        rows,
        ["date", "channel", "asset", "business_goal", "status", "owner", "source", "headline"],
    )


def write_decision_scorecard(deliverables_dir: Path, output_dir: Path, date: str) -> Path:
    metadata = json.loads(read_text(deliverables_dir / "deliverables-metadata.json"))
    angle = metadata.get("business_angle", {})
    rows = [
        {
            "date": date,
            "decision": "publish_after_human_edit",
            "rationale": angle.get("decision", ""),
            "business_outcome": "qualified conversations about agent operating models",
            "risk": "overclaiming source evidence",
            "control": "human editorial review plus source register",
            "status": "ready_for_review",
        },
        {
            "date": date,
            "decision": "do_not_auto_publish",
            "rationale": "public output remains a high-risk action",
            "business_outcome": "trust-preserving content workflow",
            "risk": "off-brand or unsupported claims",
            "control": "publish_allowed=false",
            "status": "enforced",
        },
        {
            "date": date,
            "decision": "reuse_memory_candidates",
            "rationale": "approved source/topic context should compound future runs",
            "business_outcome": "faster future briefing and drafting",
            "risk": "polluting memory with weak claims",
            "control": "provenance and confidence metadata",
            "status": "review_required",
        },
    ]
    return write_csv(
        output_dir / "decision-scorecard.csv",
        rows,
        ["date", "decision", "rationale", "business_outcome", "risk", "control", "status"],
    )


def write_publish_checklist(output_dir: Path, date: str) -> Path:
    rows = [
        {"date": date, "check": "All claims map to source register", "required": "yes", "status": "open"},
        {"date": date, "check": "Human editor approves voice and positioning", "required": "yes", "status": "open"},
        {"date": date, "check": "No confidential/internal details included", "required": "yes", "status": "open"},
        {"date": date, "check": "LinkedIn variant adapted for target buyer", "required": "yes", "status": "open"},
        {"date": date, "check": "Newsletter blurb has one clear CTA", "required": "yes", "status": "open"},
    ]
    return write_csv(output_dir / "publish-checklist.csv", rows, ["date", "check", "required", "status"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deliverables_dir", help="Path to deliverables/YYYY-MM-DD")
    parser.add_argument("--date", required=True)
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    deliverables_dir = Path(args.deliverables_dir)
    output_dir = Path(args.output_dir) if args.output_dir else deliverables_dir.parent.parent / "business-artifacts" / args.date
    outputs = [
        write_business_package(deliverables_dir, output_dir, args.date),
        write_content_calendar(deliverables_dir, output_dir, args.date),
        write_decision_scorecard(deliverables_dir, output_dir, args.date),
        write_publish_checklist(output_dir, args.date),
    ]
    package_index = {
        "date": args.date,
        "source_deliverables": str(deliverables_dir),
        "outputs": [str(path) for path in outputs],
    }
    index_path = output_dir / "package-index.json"
    index_path.write_text(json.dumps(package_index, indent=2) + "\n", encoding="utf-8")
    print(f"business_artifacts={output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

