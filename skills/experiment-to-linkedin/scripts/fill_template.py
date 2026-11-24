#!/usr/bin/env python3
"""Fill the carousel template's [[placeholders]] from a JSON values file.

Two commands:

  skeleton <template.html> [values.json]
      Write a JSON list with one entry per placeholder, in page order:
      {"n": 1, "hint": "Series title, e.g. ...", "value": ""}
      Fill in each "value". Default output is stdout.

  fill <template.html> <values.json> <out.html>
      Replace each placeholder with its value. Refuses (exit 1) when the number of
      entries or any hint differs from the template, so a values file written for an
      older template can't silently land in the wrong slots, and when a value is empty.

Values are text and are HTML-escaped. For markup (a highlighted code line, a <br>),
give {"html": "..."} instead of {"value": "..."}; it is inserted as-is.
Stdlib only.
"""
import html
import json
import re
import sys

PLACEHOLDER = re.compile(r"\[\[([^\]]*)\]\]")


def placeholders(template_text):
    return PLACEHOLDER.findall(template_text)


def skeleton(template_path, out_path=None):
    hints = placeholders(open(template_path, encoding="utf-8").read())
    entries = [{"n": i, "hint": h, "value": ""} for i, h in enumerate(hints, 1)]
    text = json.dumps(entries, ensure_ascii=False, indent=2) + "\n"
    if out_path:
        open(out_path, "w", encoding="utf-8").write(text)
        print(f"skeleton: {len(entries)} placeholders -> {out_path}", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


def fill(template_path, values_path, out_path):
    src = open(template_path, encoding="utf-8").read()
    hints = placeholders(src)
    entries = json.load(open(values_path, encoding="utf-8"))
    problems = []
    if len(entries) != len(hints):
        problems.append(f"template has {len(hints)} placeholders, values file has {len(entries)} entries")
    replacements = []
    for i, (hint, entry) in enumerate(zip(hints, entries), 1):
        if entry.get("hint") != hint:
            problems.append(f"#{i}: hint {entry.get('hint')!r} does not match template {hint!r}")
        if "html" in entry:
            value = str(entry["html"])
        else:
            value = html.escape(str(entry.get("value", "")), quote=False)
        if not value.strip():
            problems.append(f"#{i} ({hint}): empty value")
        replacements.append(value)
    if problems:
        for p in problems[:20]:
            print(f"FAIL  {p}", file=sys.stderr)
        if len(problems) > 20:
            print(f"FAIL  ... and {len(problems) - 20} more", file=sys.stderr)
        return 1
    it = iter(replacements)
    out = PLACEHOLDER.sub(lambda m: next(it), src)
    open(out_path, "w", encoding="utf-8").write(out)
    print(f"filled {len(replacements)} placeholders -> {out_path}")
    return 0


def main(argv):
    if len(argv) >= 2 and argv[0] == "skeleton" and len(argv) <= 3:
        return skeleton(*argv[1:])
    if len(argv) == 4 and argv[0] == "fill":
        return fill(*argv[1:])
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
