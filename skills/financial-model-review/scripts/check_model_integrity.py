#!/usr/bin/env python3
"""Deterministic arithmetic gate for a financial model before anyone interprets it.

Reads a JSON spec of period-indexed series plus the identities they are supposed
to satisfy, then reports every period where an identity fails by more than the
stated tolerance. Rounding noise and real breaks are separated explicitly so a
reviewer never has to argue about which is which.

Exit code is 1 if any identity BREAKS, so this can be used as a pipeline gate.

Spec format (JSON):
{
  "label": "DeepGrid v3",
  "periods": ["FY2027", "FY2028"],
  "tolerance": 0.02,
  "series": {"Revenue": [6.0, 41.17], "COGS": [2.79, 10.8],
             "Gross Profit": [3.2, 30.36]},
  "identities": [
    {"name": "Revenue - COGS = Gross Profit",
     "terms": {"Revenue": 1, "COGS": -1, "Gross Profit": -1}}
  ],
  "sums": [
    {"name": "Segments sum to Revenue",
     "of": ["ADAS", "Robotics"], "equals": "Revenue"}
  ],
  "ratios": [
    {"name": "Gross margin", "numerator": "Gross Profit",
     "denominator": "Revenue", "percent": true}
  ],
  "cagr": [{"name": "Revenue", "series": "Revenue"}]
}

Usage:
    python3 check_model_integrity.py spec.json
    python3 check_model_integrity.py spec.json --json findings.json
"""

import argparse
import json
import sys

OK, ROUNDING, BREAK = "OK", "ROUNDING", "BREAK"


def _series(spec, name):
    if name not in spec["series"]:
        raise KeyError(f"series '{name}' not defined in spec")
    return spec["series"][name]


def check_identity(spec, ident, tolerance):
    """An identity holds when its signed terms sum to zero in every period."""
    periods = spec["periods"]
    tol = ident.get("tolerance", tolerance)
    results = []
    for i, period in enumerate(periods):
        total = 0.0
        largest = 0.0
        for name, coeff in ident["terms"].items():
            val = float(_series(spec, name)[i])
            total += coeff * val
            largest = max(largest, abs(val))
        diff = round(total, 10)
        if abs(diff) <= tol:
            status = OK if diff == 0 else ROUNDING
        else:
            status = BREAK
        results.append(
            {
                "period": period,
                "diff": diff,
                "status": status,
                "pct_of_largest": (abs(diff) / largest * 100) if largest else 0.0,
            }
        )
    return {"name": ident["name"], "tolerance": tol, "results": results}


def sum_to_identity(sum_spec):
    terms = {name: 1 for name in sum_spec["of"]}
    equals = sum_spec["equals"]
    terms[equals] = terms.get(equals, 0) - 1
    return {"name": sum_spec["name"], "terms": terms,
            **({"tolerance": sum_spec["tolerance"]} if "tolerance" in sum_spec else {})}


def compute_ratios(spec):
    out = []
    for r in spec.get("ratios", []):
        num = _series(spec, r["numerator"])
        den = _series(spec, r["denominator"])
        vals = []
        for n, d in zip(num, den):
            if not d:
                vals.append(None)
            else:
                v = float(n) / float(d)
                vals.append(v * 100 if r.get("percent") else v)
        out.append({"name": r["name"], "values": vals,
                    "percent": bool(r.get("percent"))})
    return out


def compute_cagr(spec):
    out = []
    for c in spec.get("cagr", []):
        vals = [float(v) for v in _series(spec, c["series"])]
        first, last = vals[0], vals[-1]
        n = len(vals) - 1
        if first <= 0 or last <= 0 or n < 1:
            out.append({"name": c["name"], "cagr_pct": None, "multiple": None,
                        "note": "undefined (non-positive endpoint)"})
        else:
            out.append({"name": c["name"],
                        "cagr_pct": ((last / first) ** (1 / n) - 1) * 100,
                        "multiple": last / first,
                        "periods": n})
    return out


def run(spec):
    tolerance = float(spec.get("tolerance", 0.01))
    identities = list(spec.get("identities", []))
    identities += [sum_to_identity(s) for s in spec.get("sums", [])]
    checks = [check_identity(spec, i, tolerance) for i in identities]
    return {
        "label": spec.get("label", "model"),
        "periods": spec["periods"],
        "tolerance": tolerance,
        "checks": checks,
        "ratios": compute_ratios(spec),
        "cagr": compute_cagr(spec),
    }


def report(res):
    lines = [f"MODEL INTEGRITY — {res['label']}",
             f"periods: {', '.join(res['periods'])}   tolerance: +/-{res['tolerance']}",
             ""]
    breaks = 0
    for chk in res["checks"]:
        flagged = [r for r in chk["results"] if r["status"] == BREAK]
        rounding = [r for r in chk["results"] if r["status"] == ROUNDING]
        breaks += len(flagged)
        mark = "FAIL" if flagged else "pass"
        lines.append(f"[{mark}] {chk['name']}")
        for r in flagged:
            lines.append(
                f"       BREAK {r['period']}: off by {r['diff']:+.4g} "
                f"({r['pct_of_largest']:.1f}% of largest term)"
            )
        if rounding and not flagged:
            periods = ", ".join(r["period"] for r in rounding)
            lines.append(f"       rounding-only drift in {periods} (within tolerance)")
        lines.append("")

    if res["ratios"]:
        lines.append("DERIVED RATIOS")
        for r in res["ratios"]:
            suffix = "%" if r["percent"] else ""
            cells = "  ".join(
                f"{p}={v:.1f}{suffix}" if v is not None else f"{p}=n/a"
                for p, v in zip(res["periods"], r["values"])
            )
            lines.append(f"  {r['name']}: {cells}")
        lines.append("")

    if res["cagr"]:
        lines.append("GROWTH")
        for c in res["cagr"]:
            if c.get("cagr_pct") is None:
                lines.append(f"  {c['name']}: {c.get('note')}")
            else:
                lines.append(
                    f"  {c['name']}: {c['cagr_pct']:.1f}% CAGR over "
                    f"{c['periods']} periods ({c['multiple']:.0f}x)"
                )
        lines.append("")

    lines.append(f"RESULT: {breaks} break(s) beyond tolerance.")
    if breaks:
        lines.append("Do not interpret or present this model until each break is "
                     "explained or corrected.")
    return "\n".join(lines), breaks


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("spec")
    ap.add_argument("--json", metavar="PATH", help="also write findings as JSON")
    args = ap.parse_args()

    with open(args.spec, encoding="utf-8") as fh:
        spec = json.load(fh)

    try:
        res = run(spec)
    except KeyError as exc:
        sys.exit(f"spec error: {exc}")

    text, breaks = report(res)
    print(text)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=2)
    sys.exit(1 if breaks else 0)


if __name__ == "__main__":
    main()
