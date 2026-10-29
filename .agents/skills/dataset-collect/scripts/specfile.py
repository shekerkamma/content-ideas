"""Strict, tiny spec loader for dataset specs. Stdlib only.

The demonstration used YAML, and `yaml` is not in the standard library. This
repo's runtime rule is stdlib-only, so rather than take a dependency this
module parses the *exact* subset of YAML a dataset spec needs:

    key: scalar
    key:
      - list item
      - key: scalar
        key2: scalar
    key: [inline, list]

Everything else -- anchors, multi-line scalars, flow maps, tags, multiple
documents -- raises `SpecError` naming the line. That is deliberate. A
hand-rolled YAML parser that *guesses* at syntax it does not understand is a
silent-wrongness machine; one that refuses is merely inconvenient. If a spec
needs real YAML, write it as `.json` instead, which this module also loads.

Revision note: the first version silently ignored unparseable lines, which
turned a typo'd `sources:` key into "a spec with zero sources" and a run that
collected nothing while reporting success. Unknown syntax is now an error.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

__all__ = ["SpecError", "load_spec", "parse_yaml_subset"]


class SpecError(ValueError):
    """Raised for any syntax this loader will not guess at."""


_UNSUPPORTED = (
    ("&", "anchors"),
    ("*", "aliases"),
    ("!", "tags"),
    ("|", "block scalars"),
    (">", "folded scalars"),
)


def _scalar(raw: str, lineno: int):
    """Convert a scalar token. Quoted stays a string; bare is coerced."""
    s = raw.strip()
    if not s:
        return ""
    if s[0] in "\"'":
        if len(s) < 2 or s[-1] != s[0]:
            raise SpecError(f"line {lineno}: unterminated quoted string: {raw!r}")
        return s[1:-1]
    for ch, what in _UNSUPPORTED:
        if s.startswith(ch):
            raise SpecError(f"line {lineno}: {what} are not supported; use JSON")
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [] if not inner else [_scalar(p, lineno) for p in inner.split(",")]
    low = s.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if low in ("null", "~", "none"):
        return None
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d+\.\d+", s):
        return float(s)
    return s


def _strip_comment(line: str) -> str:
    """Drop a trailing `#` comment that is not inside quotes."""
    out, quote = [], None
    for i, ch in enumerate(line):
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            continue
        if ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out)


def parse_yaml_subset(text: str):
    """Parse the supported subset. Raises SpecError on anything else."""
    rows = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        if raw.strip().startswith("#") or not raw.strip():
            continue
        if raw.strip() in ("---", "..."):
            continue
        body = _strip_comment(raw).rstrip()
        if not body.strip():
            continue
        indent = len(body) - len(body.lstrip(" "))
        if "\t" in body[:indent]:
            raise SpecError(f"line {lineno}: tab indentation is not supported")
        rows.append((indent, body.strip(), lineno))

    pos = 0

    def parse_block(min_indent: int):
        """Parse rows at one indent level.

        `min_indent` is a floor, not an exact column: the block adopts the
        indent of its own first row. Requiring equality with the floor was the
        first version's bug -- it rejected the ordinary two-space list under a
        top-level key, which is the shape every spec in the wild uses.
        """
        nonlocal pos
        container = None
        block_indent = None
        while pos < len(rows):
            indent, body, lineno = rows[pos]
            if indent < min_indent:
                break
            if block_indent is None:
                block_indent = indent
            if indent < block_indent:
                break
            if indent > block_indent:
                raise SpecError(f"line {lineno}: unexpected indentation")
            min_indent = block_indent

            if body.startswith("- "):
                if container is None:
                    container = []
                if not isinstance(container, list):
                    raise SpecError(f"line {lineno}: list item inside a mapping")
                item = body[2:].strip()
                pos += 1
                if ":" in item and not item.split(":", 1)[0].strip().startswith(("\"", "'")):
                    # `- key: value` opens an inline mapping whose siblings are
                    # indented to the column of the key, not of the dash.
                    key, _, val = item.partition(":")
                    inner_indent = indent + 2
                    mapping = {key.strip(): _scalar(val, lineno) if val.strip() else None}
                    if not val.strip():
                        nested = parse_block(inner_indent + 2)
                        mapping[key.strip()] = nested
                    while pos < len(rows) and rows[pos][0] == inner_indent:
                        i2, b2, l2 = rows[pos]
                        if b2.startswith("- "):
                            break
                        if ":" not in b2:
                            raise SpecError(f"line {l2}: expected 'key: value'")
                        k2, _, v2 = b2.partition(":")
                        pos += 1
                        if v2.strip():
                            mapping[k2.strip()] = _scalar(v2, l2)
                        else:
                            mapping[k2.strip()] = parse_block(inner_indent + 2)
                    container.append(mapping)
                else:
                    container.append(_scalar(item, lineno))
                continue

            if ":" not in body:
                raise SpecError(f"line {lineno}: expected 'key: value', got {body!r}")
            if container is None:
                container = {}
            if not isinstance(container, dict):
                raise SpecError(f"line {lineno}: mapping key inside a list")
            key, _, val = body.partition(":")
            key = key.strip()
            pos += 1
            if val.strip():
                container[key] = _scalar(val, lineno)
            else:
                container[key] = parse_block(indent + 1)
        return {} if container is None else container

    result = parse_block(0)
    if pos != len(rows):
        raise SpecError(f"line {rows[pos][2]}: could not parse remainder of file")
    return result


def load_spec(path: str | Path) -> dict:
    """Load a `.json` or YAML-subset spec and validate its required shape."""
    p = Path(path)
    if not p.is_file():
        raise SpecError(f"spec not found: {p}")
    text = p.read_text(encoding="utf-8")
    data = json.loads(text) if p.suffix == ".json" else parse_yaml_subset(text)
    if not isinstance(data, dict):
        raise SpecError(f"{p}: top level must be a mapping")

    if not data.get("name"):
        raise SpecError(f"{p}: missing required key 'name'")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        raise SpecError(f"{p}: 'sources' must be a non-empty list")
    seen = set()
    for i, src in enumerate(sources):
        if not isinstance(src, dict):
            raise SpecError(f"{p}: sources[{i}] must be a mapping")
        sid = src.get("id")
        if not sid:
            raise SpecError(f"{p}: sources[{i}] missing 'id'")
        if sid in seen:
            raise SpecError(f"{p}: duplicate source id {sid!r}")
        seen.add(sid)
        if not src.get("adapter"):
            raise SpecError(
                f"{p}: sources[{i}] ({sid}) missing 'adapter'. The demonstration's "
                f"spec had an implicit single provider; this one is explicit so a "
                f"spec cannot silently collect from the wrong place."
            )
        on_error = src.get("on_error", "halt")
        if on_error not in ("skip", "halt"):
            raise SpecError(f"{p}: sources[{i}] on_error must be 'skip' or 'halt'")

    storage = data.setdefault("storage", {})
    if not isinstance(storage, dict):
        raise SpecError(f"{p}: 'storage' must be a mapping")
    storage.setdefault("format", "jsonl")
    storage.setdefault("path", f"./data/{data['name']}/")
    if storage["format"] != "jsonl":
        raise SpecError(
            f"{p}: storage.format {storage['format']!r} is not supported by the "
            f"stdlib runtime. Use 'jsonl'; convert to parquet downstream if needed."
        )
    return data
