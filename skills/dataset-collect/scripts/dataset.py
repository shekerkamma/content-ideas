#!/usr/bin/env python3
"""Declarative dataset collection with a local store. Stdlib only.

Turns a spec file into records on disk, then answers questions about them
*without* loading the records into a model's context window. That inversion is
the entire point: an agent asks this tool for the answer, not for the data.

Command surface mirrors the demonstration in the source video:

    dataset.py collect <spec>  [--dry-run] [--limit N]
    dataset.py status  <spec>
    dataset.py query   <spec> --source <id> [--count | --avg F | --top F]
                              [--where EXPR] [--select a,b] [--limit N]

Store layout (one file per source per collection date, so a re-run is
additive history rather than a destructive overwrite):

    <storage.path>/raw/<source_id>/<YYYY-MM-DD>.jsonl
    <storage.path>/metadata.json

`query` streams the store line by line and holds only what the requested
projection needs. `--count` and `--avg` over a million records return one
number and allocate almost nothing.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as _dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from adapters import AdapterError, expand_env, get_adapter  # noqa: E402
from specfile import SpecError, load_spec  # noqa: E402

MAX_PARALLEL = 16


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _today() -> str:
    return _dt.date.today().isoformat()


def _store_root(spec: dict, spec_path: Path) -> Path:
    raw = spec["storage"]["path"]
    p = Path(os.path.expanduser(raw))
    return p if p.is_absolute() else (spec_path.parent / p).resolve()


def _inputs_for(source: dict, spec_dir: Path) -> list:
    """Resolve a source's input list. No input list means one unkeyed call."""
    if "inputs" in source:
        vals = source["inputs"]
        if not isinstance(vals, list):
            raise SpecError(f"{source['id']}: 'inputs' must be a list")
        return list(vals)
    from_file = source.get("from_file")
    if from_file:
        fp = Path(from_file)
        if not fp.is_absolute():
            fp = spec_dir / fp
        if not fp.is_file():
            raise SpecError(f"{source['id']}: from_file not found: {fp}")
        return [ln.strip() for ln in fp.read_text(encoding="utf-8").splitlines()
                if ln.strip() and not ln.strip().startswith("#")]
    return [None]


def _coerce(text: str):
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    low = text.lower()
    if low in ("true", "false"):
        return low == "true"
    return text


def _get_field(rec: dict, path: str):
    """Dotted lookup: `a.b.0.c` walks dicts and list indices."""
    cur = rec
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        elif isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return cur


_OPS = ("!=", ">=", "<=", "~=", "=", ">", "<")


def _make_predicate(exprs: list[str]):
    """AND of simple `field OP value` tests. `~=` is substring, case-folded."""
    parsed = []
    for expr in exprs or []:
        for op in _OPS:
            if op in expr:
                field, _, raw = expr.partition(op)
                parsed.append((field.strip(), op, _coerce(raw.strip())))
                break
        else:
            raise SystemExit(f"bad --where {expr!r}; expected field OP value "
                             f"with OP in {', '.join(_OPS)}")

    def pred(rec: dict) -> bool:
        for field, op, want in parsed:
            got = _get_field(rec, field)
            try:
                if op == "=" and got != want:
                    return False
                if op == "!=" and got == want:
                    return False
                if op == "~=" and str(want).lower() not in str(got or "").lower():
                    return False
                if op in (">", "<", ">=", "<="):
                    if got is None:
                        return False
                    g, w = float(got), float(want)
                    if op == ">" and not g > w:
                        return False
                    if op == "<" and not g < w:
                        return False
                    if op == ">=" and not g >= w:
                        return False
                    if op == "<=" and not g <= w:
                        return False
            except (TypeError, ValueError):
                return False
        return True

    return pred


def _iter_records(root: Path, source_id: str, date: str | None = None):
    """Stream records from the store. Never materialises the whole source."""
    src_dir = root / "raw" / source_id
    if not src_dir.is_dir():
        return
    files = sorted(src_dir.glob(f"{date}.jsonl" if date else "*.jsonl"))
    for fp in files:
        with fp.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    yield json.loads(line)


# --------------------------------------------------------------------------
# collect
# --------------------------------------------------------------------------

def cmd_collect(args) -> int:
    spec_path = Path(args.spec).resolve()
    spec = load_spec(spec_path)
    spec_dir = spec_path.parent
    root = _store_root(spec, spec_path)

    plan = []
    for source in spec["sources"]:
        inputs = _inputs_for(source, spec_dir)
        if args.limit:
            inputs = inputs[: args.limit]
        plan.append((source, inputs))

    total = sum(len(i) for _, i in plan)
    print(f"dataset: {spec['name']}")
    print(f"store:   {root}")
    for source, inputs in plan:
        shown = ", ".join(str(i) for i in inputs[:5] if i is not None)
        more = f" (+{len(inputs) - 5} more)" if len(inputs) > 5 else ""
        print(f"  source {source['id']}: adapter={source['adapter']} "
              f"calls={len(inputs)} on_error={source.get('on_error', 'halt')}")
        if shown:
            print(f"    inputs: {shown}{more}")

    if args.dry_run:
        print(f"\nDRY RUN — {total} call(s) planned, 0 made, nothing written.")
        print("Re-run without --dry-run to collect.")
        return 0

    collected_date = _today()
    (root / "raw").mkdir(parents=True, exist_ok=True)
    summary, failures, wipeouts = {}, [], []

    for source, inputs in plan:
        sid = source["id"]
        fn = get_adapter(source["adapter"])
        parallel = max(1, min(int(source.get("parallel", 1)), MAX_PARALLEL))
        on_error = source.get("on_error", "halt")
        out_dir = root / "raw" / sid
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{collected_date}.jsonl"

        def one(value):
            return value, fn(source, value, spec_dir)

        rows = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as pool:
            futures = {pool.submit(one, v): v for v in inputs}
            for fut in concurrent.futures.as_completed(futures):
                value = futures[fut]
                try:
                    value, recs = fut.result()
                except (AdapterError, Exception) as exc:  # noqa: BLE001
                    msg = f"{sid}[{value}]: {exc}"
                    failures.append(msg)
                    if on_error == "halt":
                        for f in futures:
                            f.cancel()
                        print(f"\n✗ {msg}", file=sys.stderr)
                        print("on_error: halt — stopping. Nothing further collected.",
                              file=sys.stderr)
                        return 1
                    print(f"  ! skipped {msg}", file=sys.stderr)
                    continue
                for rec in recs:
                    rows.append({
                        "_source_id": sid,
                        "_collected_date": collected_date,
                        "_input": value,
                        **rec,
                    })

        src_failed = [f for f in failures if f.startswith(f"{sid}[")]
        if rows:
            # "w", not "a": a date partition is a snapshot of that day, so a
            # re-run replaces it. Appending was the first version's behaviour
            # and it silently doubled the store on the second run of the same
            # day -- count went 5 -> 10 with no warning, which quietly skews
            # every aggregate a scheduled retry touches.
            with out_file.open("w", encoding="utf-8") as fh:
                for rec in rows:
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"  ✓ collected {len(rows)} records for {sid} -> "
                  f"{out_file.relative_to(root)}")
        else:
            mark = "✗" if src_failed else "·"
            print(f"  {mark} collected 0 records for {sid}")
        summary[sid] = len(rows)
        wipeouts.extend([sid] if (not rows and src_failed) else [])

    meta_path = root / "metadata.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    meta.setdefault("name", spec["name"])
    meta.setdefault("runs", []).append({
        "collected_date": collected_date,
        "spec": str(spec_path),
        "records": summary,
        "failures": failures,
    })
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    grand = sum(summary.values())
    print(f"\nDone. Collected {grand} records across {len(summary)} source(s).")
    if failures:
        print(f"{len(failures)} input(s) skipped — see metadata.json.")

    # `on_error: skip` means "tolerate some failures", never "tolerate total
    # failure". A source where every input errored collected nothing, and
    # exiting 0 there would let a scheduled run report success forever after a
    # credential expired. Found by running the skill with EXA_API_KEY unset:
    # 2/2 inputs failed, exit code was 0, and the summary line read "Done."
    if wipeouts:
        print(f"\nFAILED: every input errored for: {', '.join(wipeouts)}. "
              f"Collected nothing. This is a failure regardless of on_error.",
              file=sys.stderr)
        return 1
    print("\nNext steps:")
    print(f"  Status:  dataset.py status {args.spec}")
    for sid in summary:
        print(f"  Query:   dataset.py query {args.spec} --source {sid} --limit 5")
        print(f"  Count:   dataset.py query {args.spec} --source {sid} --count")
        break
    return 0


# --------------------------------------------------------------------------
# status / query
# --------------------------------------------------------------------------

def cmd_status(args) -> int:
    spec_path = Path(args.spec).resolve()
    spec = load_spec(spec_path)
    root = _store_root(spec, spec_path)
    print(f"dataset: {spec['name']}")
    print(f"store:   {root}")
    if not (root / "raw").is_dir():
        print("  (nothing collected yet)")
        return 0
    for source in spec["sources"]:
        sid = source["id"]
        src_dir = root / "raw" / sid
        if not src_dir.is_dir():
            print(f"  {sid}: no data")
            continue
        files = sorted(src_dir.glob("*.jsonl"))
        n = sum(1 for _ in _iter_records(root, sid))
        size = sum(f.stat().st_size for f in files)
        dates = ", ".join(f.stem for f in files[-3:])
        print(f"  {sid}: {n} records in {len(files)} partition(s), "
              f"{size / 1024:.1f} KiB — latest: {dates}")
    return 0


def _print_table(rows: list[dict], fields: list[str]) -> None:
    if not rows:
        print("(no rows)")
        return
    widths = {f: max(len(f), *(len(str(r.get(f, ""))[:60]) for r in rows)) for f in fields}
    line = "  ".join(f.ljust(widths[f]) for f in fields)
    print(line)
    print("  ".join("-" * widths[f] for f in fields))
    for r in rows:
        print("  ".join(str(r.get(f, ""))[:60].ljust(widths[f]) for f in fields))


def cmd_query(args) -> int:
    spec_path = Path(args.spec).resolve()
    spec = load_spec(spec_path)
    root = _store_root(spec, spec_path)
    sid = args.source or spec["sources"][0]["id"]
    pred = _make_predicate(args.where)
    stream = (r for r in _iter_records(root, sid, args.date) if pred(r))

    if args.count:
        print(sum(1 for _ in stream))
        return 0

    if args.avg or args.sum_ or args.max_ or args.min_:
        field = args.avg or args.sum_ or args.max_ or args.min_
        vals = []
        for rec in stream:
            v = _get_field(rec, field)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                vals.append(float(v))
        if not vals:
            print(f"(no numeric values for {field!r})")
            return 1
        if args.avg:
            print(round(sum(vals) / len(vals), 4))
        elif args.sum_:
            print(round(sum(vals), 4))
        elif args.max_:
            print(max(vals))
        else:
            print(min(vals))
        return 0

    if args.top:
        rows = sorted(
            (r for r in stream if isinstance(_get_field(r, args.top), (int, float))),
            key=lambda r: float(_get_field(r, args.top)), reverse=True,
        )[: args.limit or 10]
    else:
        rows = []
        for rec in stream:
            rows.append(rec)
            if args.limit and len(rows) >= args.limit:
                break

    if args.select:
        fields = [f.strip() for f in args.select.split(",") if f.strip()]
        rows = [{f: _get_field(r, f) for f in fields} for r in rows]
    else:
        fields = list(rows[0].keys()) if rows else []

    if args.format == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        _print_table(rows, fields)
    return 0


# --------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Declarative dataset collection with a local, queryable store.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("collect", help="run the spec and write records to the store")
    c.add_argument("spec")
    c.add_argument("--dry-run", action="store_true",
                   help="print the plan and exit without making a single call")
    c.add_argument("--limit", type=int, help="cap inputs per source (cheap first run)")
    c.set_defaults(func=cmd_collect)

    s = sub.add_parser("status", help="what is in the store")
    s.add_argument("spec")
    s.set_defaults(func=cmd_status)

    q = sub.add_parser("query", help="answer a question without loading the records")
    q.add_argument("spec")
    q.add_argument("--source")
    q.add_argument("--date", help="restrict to one collection date (YYYY-MM-DD)")
    q.add_argument("--where", action="append", default=[],
                   help="field OP value; repeatable, ANDed")
    q.add_argument("--select", help="comma-separated fields (dotted paths allowed)")
    q.add_argument("--limit", type=int)
    q.add_argument("--count", action="store_true")
    q.add_argument("--avg", metavar="FIELD")
    q.add_argument("--sum", dest="sum_", metavar="FIELD")
    q.add_argument("--max", dest="max_", metavar="FIELD")
    q.add_argument("--min", dest="min_", metavar="FIELD")
    q.add_argument("--top", metavar="FIELD", help="sort desc by FIELD")
    q.add_argument("--format", choices=("table", "json"), default="table")
    q.set_defaults(func=cmd_query)

    args = ap.parse_args(argv)
    try:
        return args.func(args)
    except (SpecError, AdapterError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
