#!/usr/bin/env python3
"""Blocking check: every BLOCKED marker must show the source search that justifies it.

A blocker is a claim about the corpus — "this fact is not in any source" — and it is the
one claim agents routinely assert without checking. In one run three separate blockers
(a product's description, the voice samples, a full product specification) were all sitting
in documents that had already been read. Each cost a rebuild cycle.

This makes the failure loud and, where it can, disproves the blocker directly: it greps the
run's own sources/ for terms drawn from the blocked file and reports candidate hits.

A blocker is acceptable when the file records the search, using a line like:

    Searched: sources/*.txt for "AD4", "AGV", "seaport" — no match. <date>

Exit 1 if any BLOCKED marker lacks a Searched: line.

Usage: check_blockers.py <run-dir>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BLOCKED = re.compile(r"\bBLOCKED\b|\bblocked on the founder\b", re.I)
SEARCHED = re.compile(r"^\s*(?:>\s*)?\*{0,2}Searched:", re.I | re.M)
# Words worth probing the sources for, drawn from the blocked file's own headings.
TERM = re.compile(r"\b([A-Z][A-Za-z0-9]{2,}|[A-Z]{2,}\d*)\b")

NOISE = {
    "BLOCKED", "Status", "The", "This", "That", "There", "Action", "Rules", "Evidence",
    "Examples", "Exclusions", "Never", "Always", "Voice", "Offer", "Proof", "Process",
    "Founder", "Until", "What", "When", "Which", "Because", "Source", "Note", "Searched",
    "Not", "Are", "Use", "Every", "Ask", "Move", "Where", "Then", "But", "And", "For",
    "You", "Our", "Its", "Their", "They", "With", "From", "Into", "Only", "Same", "Say",
    "Give", "Take", "Make", "Does", "Both", "Each", "Also", "Real", "One", "Two", "Three",
    "Plan", "Today", "Level", "File", "Files", "Write", "Read", "Fix", "Run", "Test",
}

# A term that appears everywhere is generic and tells you nothing. Distinctive terms are
# rare ones. Ignore anything above this share of the corpus.
MAX_HITS = 40


def probe(sources: Path, terms: list[str]) -> dict[str, int]:
    """Count occurrences of each term across the run's sources."""
    hits: dict[str, int] = {}
    if not sources.is_dir():
        return hits
    corpus = ""
    for f in sources.rglob("*"):
        if f.is_file() and f.suffix.lower() in {".txt", ".md"}:
            corpus += f.read_text(encoding="utf-8", errors="replace")
    low = corpus.lower()
    for t in terms:
        n = low.count(t.lower())
        if 0 < n <= MAX_HITS:
            hits[t] = n
    return hits


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    run = Path(sys.argv[1]).resolve()
    context = run / "context"
    if not context.is_dir():
        print(f"FAIL: no context/ under {run}")
        return 1

    failures = 0
    for path in sorted(context.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        if not BLOCKED.search(text):
            continue
        rel = path.relative_to(run)
        if SEARCHED.search(text):
            print(f"  OK    {rel} — blocker records its source search")
            continue

        failures += 1
        print(f"\n  FAIL  {rel} — BLOCKED with no 'Searched:' line")
        terms = [t for t in dict.fromkeys(TERM.findall(text)) if t not in NOISE][:12]
        hits = probe(run / "sources", terms)
        if hits:
            # rarest first — those are the distinctive ones worth checking
            top = sorted(hits.items(), key=lambda kv: kv[1])[:6]
            print("        terms from this file that DO appear in sources/:")
            for term, n in top:
                print(f"          {term!r}: {n} occurrence(s)")
            print("        Check these before claiming the fact is absent.")
        else:
            print("        (no candidate terms found in sources/ — blocker may be real,")
            print("         but it still must record the search that establishes it)")

    if failures:
        print(
            f"\nFAIL: {failures} blocker(s) assert a fact is missing without showing the search.\n"
            "Grep every supplied source, then either remove the blocker or record:\n"
            '  Searched: sources/*.txt for "<term>", "<synonym>" — no match. <date>'
        )
        return 1

    print("\nOK: every blocker records the source search behind it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
