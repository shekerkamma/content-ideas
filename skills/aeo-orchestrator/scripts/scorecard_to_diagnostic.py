#!/usr/bin/env python3
"""Generate a buyer-facing Agentic SaaS Exposure Diagnostic from scorecard HTML."""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[dict] = []
        self.current: dict | None = None
        self.cells: list[str] = []
        self.in_cell = False
        self.cell_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "tr" and "main" in set(attr.get("class", "").split()):
            self.current = {
                "type": attr.get("data-type", ""),
                "verdict": attr.get("data-verdict", ""),
                "search": html.unescape(attr.get("data-search", "")),
            }
            self.cells = []
        elif self.current is not None and tag == "td":
            self.in_cell = True
            self.cell_text = []

    def handle_endtag(self, tag: str) -> None:
        if self.current is not None and tag == "td" and self.in_cell:
            self.cells.append(clean(" ".join(self.cell_text)))
            self.in_cell = False
        elif self.current is not None and tag == "tr":
            if len(self.cells) >= 10:
                self.current.update(
                    {
                        "rank": self.cells[0],
                        "use_case": self.cells[2].lstrip("▸").strip(),
                        "proof_summary": self.cells[3],
                        "saas_affected": self.cells[4],
                        "volume": self.cells[5],
                        "determinism": self.cells[6],
                        "data_moat": self.cells[7],
                        "build_vs_buy": self.cells[9],
                    }
                )
                self.rows.append(self.current)
            self.current = None

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.cell_text.append(data)


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def extract_detail(search: str, marker: str) -> str:
    text = clean(search)
    idx = text.lower().find(marker)
    if idx == -1:
        return text[:450]
    return text[idx + len(marker) : idx + len(marker) + 520].strip()


def rows_from_html(path: Path) -> list[dict]:
    parser = TableParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.rows


def verdict_counts(rows: list[dict]) -> Counter[str]:
    return Counter(row["verdict"] for row in rows)


def group_by_type(rows: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row["type"]].append(row)
    return dict(groups)


def top_rows(rows: list[dict], verdict: str, limit: int = 6) -> list[dict]:
    filtered = [row for row in rows if row["verdict"] == verdict]
    score = {"H": 3, "M": 2, "L": 1}
    return sorted(
        filtered,
        key=lambda row: (
            -score.get(row.get("volume", ""), 0),
            -score.get(row.get("determinism", ""), 0),
            score.get(row.get("data_moat", ""), 0),
            int(row.get("rank") or 999),
        ),
    )[:limit]


def row_bullet(row: dict) -> str:
    return (
        f"- **{row['use_case']}** ({row['type']}, {row['verdict'].title()}): "
        f"{row['saas_affected']} | proof: {row['proof_summary']} | "
        f"why it matters: {row['build_vs_buy']}."
    )


def render(rows: list[dict], source_url: str) -> str:
    counts = verdict_counts(rows)
    groups = group_by_type(rows)
    replace = top_rows(rows, "REPLACE", 10)
    renegotiate = top_rows(rows, "RENEGOTIATE", 6)
    keep = top_rows(rows, "KEEP", 6)
    lines: list[str] = [
        "# Agentic SaaS Exposure Diagnostic",
        "",
        "## Executive Thesis",
        "",
        "AI agents do not replace all SaaS. They replace the workflow layer where task volume is high, output is deterministic, and the underlying data moat is weak. They renegotiate seat economics where the system of record remains valuable but workflow seats shrink. They enrich platforms where proprietary data, auditability, or operational history is the moat.",
        "",
        "This diagnostic converts the Agent Replacement Scorecard into a pre-sales conversation asset: which software categories are exposed, what has already been deployed, and where a buyer should run a fast agent pilot.",
        "",
        "## Scorecard Snapshot",
        "",
        f"- Source: {source_url}",
        f"- Use cases analyzed: {len(rows)}",
        f"- Replace: {counts.get('REPLACE', 0)}",
        f"- Renegotiate: {counts.get('RENEGOTIATE', 0)}",
        f"- Keep: {counts.get('KEEP', 0)}",
        f"- Agent types: {', '.join(sorted(groups))}",
        "",
        "## Buyer Interpretation",
        "",
        "- **Replace** means the buyer should run build-vs-buy math immediately. The exposed spend is usually per-seat workflow tooling, BPO, or low-moat add-ons.",
        "- **Renegotiate** means the buyer should keep the core platform but challenge per-seat modules, assistant add-ons, or workflow licenses.",
        "- **Keep** means the platform owns data, audit trail, or system-of-record gravity. The agent should ride on top via API/MCP rather than replace the platform.",
        "",
        "## Highest-Exposure Replace Zones",
        "",
    ]
    lines.extend(row_bullet(row) for row in replace)
    lines.extend(
        [
            "",
            "## Renegotiate Zones",
            "",
        ]
    )
    lines.extend(row_bullet(row) for row in renegotiate)
    lines.extend(
        [
            "",
            "## Keep / Enrich Zones",
            "",
        ]
    )
    lines.extend(row_bullet(row) for row in keep)
    lines.extend(
        [
            "",
            "## What This Means For A Buyer",
            "",
            "1. Inventory your software stack by workflow, not vendor.",
            "2. Mark each workflow by volume, determinism, and data moat.",
            "3. For high-volume, deterministic, low-moat workflows, run a two-week parallel agent pilot.",
            "4. For high-moat systems, keep the platform and move spend from seats to agent access, API usage, or outcome pricing.",
            "5. Use the scorecard as renewal leverage: seat compression is now a credible alternative, not a theoretical threat.",
            "",
            "## Two-Week Pilot Path",
            "",
            "Week 1:",
            "- Pick one Replace workflow with clear input/output boundaries.",
            "- Export 50-100 historical examples.",
            "- Build an agent loop that drafts or resolves the task while preserving human review.",
            "- Measure resolution rate, cycle time, exception rate, and human escalation quality.",
            "",
            "Week 2:",
            "- Run the agent in parallel with the current SaaS workflow.",
            "- Compare cost per completed task against seat/tool spend.",
            "- Identify which records must remain in the system of record.",
            "- Decide: replace workflow layer, renegotiate module/seat pricing, or keep and enrich.",
            "",
            "## Where AEO Fits",
            "",
            "This diagnostic also creates the AEO job: when buyers ask AI systems which SaaS categories agents can replace, this scorecard should be cited. The AEO workflow should track whether AI answers surface this asset, which sources they cite instead, and which content or citation gaps prevent the scorecard from winning the recommendation.",
            "",
            "## Recommended Next Action",
            "",
            "Use this diagnostic as the first pre-sales artifact. For a named prospect, map their stack against the 25 archetypes, then produce a custom Keep / Renegotiate / Replace view and a two-week pilot recommendation.",
            "",
            "## Method Note",
            "",
            "The scorecard verdicts are directional strategy judgments from named deployment examples. They are not measured replacement counts. A prospect-specific diagnostic should verify source claims, software spend, workflow volume, integration constraints, compliance boundaries, and human-review requirements before recommending replacement.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    rows = rows_from_html(args.html)
    if not rows:
        raise SystemExit("No scorecard rows found")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(rows, args.source_url), encoding="utf-8")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
