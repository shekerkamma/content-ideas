#!/usr/bin/env python3
"""Gate a contract.md before the loop is allowed to start.

Mechanical pre-pass only. It catches contracts that cannot possibly produce
actionable critiques: missing AGREED status, criteria with no check, and hedge
words that no evidence can falsify.

It does not replace reading the contract. A criterion can pass every check here
and still be vague.

Stdlib only. Exits 0 when the contract is loop-ready, 1 otherwise.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Words that make a criterion unfalsifiable. Two reasonable people can always
# disagree about whether "appropriate" was achieved.
HEDGE_WORDS = [
    "appropriate", "appropriately", "accurate", "accurately", "reasonable",
    "reasonably", "well organized", "well-organized", "good", "clean",
    "properly", "correctly", "as needed", "if necessary", "etc",
    "high quality", "high-quality", "user friendly", "user-friendly",
    "robust", "sensible", "adequate", "nice", "polished", "intuitive",
]

# Escape hatches that let the critic defer instead of failing an item.
ESCAPE_HATCHES = ["fix later", "partial pass", "good enough", "revisit later", "tbd"]

# A hatch preceded by one of these on the same line is being banned, not offered.
NEGATION_RE = re.compile(
    r"\b(no|not|never|without|ban(?:s|ned)?|forbid(?:s|den)?|"
    r"disallow(?:s|ed)?|prohibit(?:s|ed)?|is not|are not)\b"
)

MIN_CRITERIA = 5


class Finding:
    def __init__(self, level: str, where: str, message: str, fix: str = "") -> None:
        self.level = level
        self.where = where
        self.message = message
        self.fix = fix

    def render(self) -> str:
        head = f"  [{self.level}] {self.where}: {self.message}"
        return head + (f"\n         fix: {self.fix}" if self.fix else "")


def parse_criteria_rows(text: str) -> list[tuple[int, list[str]]]:
    """Return (line_no, cells) for every Markdown table row under ## Criteria."""
    lines = text.splitlines()
    rows: list[tuple[int, list[str]]] = []
    in_section = False
    for i, raw in enumerate(lines, start=1):
        line = raw.strip()
        if re.match(r"^#{1,6}\s", line):
            in_section = bool(re.match(r"^#{1,6}\s+criteria\b", line, re.I))
            continue
        if not in_section or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells:
            continue
        joined = "".join(cells).replace("-", "").replace(":", "").strip()
        if not joined:  # separator row
            continue
        if cells[0].lower() in {"#", "id", "no"} or cells[0].lower().startswith("criterion"):
            continue  # header row
        rows.append((i, cells))
    return rows


def check(text: str) -> tuple[list[Finding], dict]:
    findings: list[Finding] = []
    lowered = text.lower()

    # --- Status
    m = re.search(r"^status:\s*(.+)$", text, re.I | re.M)
    status = m.group(1).strip() if m else None
    if status is None:
        findings.append(Finding(
            "FAIL", "header", "no `Status:` line found",
            "add `Status: DRAFT` and drive it to AGREED through negotiation",
        ))
    elif status.upper() != "AGREED":
        findings.append(Finding(
            "FAIL", "header", f"Status is {status!r}, not AGREED",
            "the auditor must review the criteria adversarially and agree before work starts",
        ))

    # --- Scope
    if not re.search(r"^#{1,6}\s+scope\b", text, re.I | re.M):
        findings.append(Finding(
            "WARN", "structure", "no `## Scope` section",
            "state what is in scope and, more importantly, what is not",
        ))

    # --- Criteria
    rows = parse_criteria_rows(text)
    if not rows:
        findings.append(Finding(
            "FAIL", "criteria", "no criteria rows found under a `## Criteria` heading",
            "use a table with columns: # | Criterion | Check",
        ))
    elif len(rows) < MIN_CRITERIA:
        findings.append(Finding(
            "WARN", "criteria",
            f"only {len(rows)} criteria — Anthropic's reference app settled on 27",
            "vague criteria produce vague critiques; split each one until every "
            "row is a single yes/no",
        ))

    checked = 0
    for line_no, cells in rows:
        label = f"criterion line {line_no}"
        criterion = cells[1] if len(cells) > 1 else cells[0]
        check_cell = cells[2] if len(cells) > 2 else ""

        if not criterion:
            findings.append(Finding("FAIL", label, "empty criterion text"))
            continue

        if not check_cell:
            findings.append(Finding(
                "FAIL", label, f"no Check for {criterion[:50]!r}",
                "name the command or the reviewer that decides; if you cannot, "
                "the criterion is written badly",
            ))
        else:
            checked += 1

        hits = [w for w in HEDGE_WORDS if re.search(rf"\b{re.escape(w)}\b", criterion.lower())]
        if hits:
            findings.append(Finding(
                "FAIL", label,
                f"unfalsifiable wording {hits!r} in {criterion[:50]!r}",
                "rewrite so two reasonable people cannot disagree about whether it passed",
            ))

    # --- Escape hatches anywhere in the contract.
    # A contract that *bans* an escape hatch ("there is no partial pass") is
    # doing the right thing, so only flag an unnegated mention.
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.lower().strip()
        if line.startswith("<!--") or not line:
            continue
        for hatch in ESCAPE_HATCHES:
            idx = line.find(hatch)
            if idx < 0:
                continue
            if NEGATION_RE.search(line[:idx]):
                continue  # the contract is forbidding it, not offering it
            findings.append(Finding(
                "WARN", f"line {line_no}", f"escape hatch offered: {hatch!r}",
                "every soft option you leave available will get used",
            ))

    # --- Grading rule
    if not re.search(r"^#{1,6}\s+grading\b", text, re.I | re.M):
        findings.append(Finding(
            "WARN", "structure", "no `## Grading` section",
            "state that any failing criterion fails the item — no partial pass",
        ))

    # --- Disputes
    if not re.search(r"^#{1,6}\s+disputes\b", text, re.I | re.M):
        findings.append(Finding(
            "WARN", "structure", "no `## Disputes` section",
            "record what the auditor pushed back on and how it resolved — this is "
            "the record of the negotiation actually happening",
        ))

    stats = {
        "criteria": len(rows),
        "with_check": checked,
        "status": status or "(none)",
    }
    return findings, stats


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gate a contract.md before the loop starts.")
    ap.add_argument("--dir", default=".", help="Directory holding contract.md")
    ap.add_argument("--file", help="Path to the contract file (overrides --dir)")
    ap.add_argument(
        "--strict", action="store_true",
        help="Treat WARN findings as failures",
    )
    args = ap.parse_args(argv)

    path = Path(args.file) if args.file else Path(args.dir) / "contract.md"
    path = path.expanduser().resolve()
    if not path.is_file():
        print(f"FAIL: no contract at {path}", file=sys.stderr)
        print("      run init_loop.py first, or pass --file", file=sys.stderr)
        return 1

    findings, stats = check(path.read_text(encoding="utf-8"))
    fails = [f for f in findings if f.level == "FAIL"]
    warns = [f for f in findings if f.level == "WARN"]

    print(f"contract: {path}")
    print(f"  status:   {stats['status']}")
    print(f"  criteria: {stats['criteria']} ({stats['with_check']} with a Check)\n")

    for f in fails + warns:
        print(f.render())

    blocking = fails or (warns if args.strict else [])
    if blocking:
        print(f"\nFAIL ({len(fails)} blocking, {len(warns)} advisory)")
        print("The loop must not start against this contract.")
        return 1

    if warns:
        print(f"\nPASS with {len(warns)} advisory finding(s).")
    else:
        print("PASS — contract is loop-ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
