#!/usr/bin/env python3
"""Emit derived facts from the DeepGrid Semi financial model as cited, retrievable documents.

Why this exists
---------------
The Ask Dossier surface answers by deterministic retrieval with no model call. That
works only for facts that exist as text. Measured against the shipped index, the
load-bearing findings of a SKU analysis do not:

    "11,626" (cumulative dies)   0 hits in corpus, 0 in site index
    "Rs364"  (die cost in INR)   0 hits in corpus, 0 in site index
    "2.5 : 1.5" (mix ratio)      0 hits in corpus, 0 in site index

They are arithmetic over retrieved cells, so no retrieval improvement reaches them.
This script moves that arithmetic from query time to BUILD time: it computes the
facts and emits them as first-class documents carrying formula, inputs and source
cells. Retrieval stays deterministic and citable; the facts simply now exist.

Every emitted record is reproducible from the CSVs in data/ — nothing is hardcoded
except sheet/column labels used to locate values.

Usage:  python3 derive_facts.py [--data DIR] [--out FILE] [--sku NAME]
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

FY = ["FY2027", "FY2028", "FY2029", "FY2030", "FY2031", "FY2032"]
PREFIX = "deepgrid_semi_financial_model_corrected_v3_sept__"


def _num(s):
    try:
        return float(str(s).replace(",", "").strip())
    except (ValueError, AttributeError):
        return None


def load_revenue(path: Path):
    """Return {sku: {segment, domain, asp, units[6], revenue[6]}}.

    The sheet interleaves a units row and a revenue row per SKU. They are told
    apart by column 2: an integer price marks the units row, a domain label marks
    the revenue row.
    """
    skus: dict[str, dict] = {}
    for row in csv.reader(path.open(encoding="utf-8")):
        if len(row) < 9:
            continue
        name, seg, col2 = row[0].strip(), row[1].strip(), row[2].strip()
        if not name or name.startswith(("Surface", "Total", "FY", "Revenue (")):
            continue
        vals = [_num(x) or 0.0 for x in row[3:9]]
        if len(vals) != 6:
            continue
        rec = skus.setdefault(name, {"segment": seg})
        if col2.isdigit():
            rec["asp"] = int(col2)
            rec["units"] = vals
        elif col2:
            rec["domain"] = col2
            rec["revenue"] = vals
    return {k: v for k, v in skus.items() if "units" in v and "revenue" in v}


def load_assumptions(path: Path):
    """Segment gross margins by year, plus the USD/INR rate if the CSV carries it."""
    margins, fx = {}, None
    for row in csv.reader(path.open(encoding="utf-8")):
        if not row:
            continue
        label = row[0].strip()
        if label in ("Systems", "Sensors", "Semiconductors", "Robotics"):
            vals = [_num(x) for x in row[1:7]]
            if all(v is not None for v in vals):
                margins[label] = vals
        if label.replace(" ", "").upper() in ("USD/INR", "USDINR"):
            for c in row[1:]:
                if (v := _num(c)) and v > 1:
                    fx = v
                    break
    return margins, fx


def load_fx_from_dump(path: Path):
    """Recover USD/INR from the cell dump.

    The per-sheet CSV export starts at the Assumptions table header and drops the
    macro block above it, so the FX rate is absent from assumptions.csv. It is
    present in the dump as a label cell followed by its value cell:

        B6: USD / INR
        C6: 94

    Every tapeout INR figure is computed as `$ * Assumptions!C6 / 1e7`, so this is
    the rate the model itself uses. Returns None if the dump is absent or changed
    shape - the caller then skips currency-derived facts rather than guessing.
    """
    if not path.exists():
        return None
    label_row = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or ":" not in s:
            continue
        cell, _, val = s.partition(":")
        cell, val = cell.strip(), val.strip()
        if len(cell) < 2 or not cell[0].isalpha() or not cell[1:].isdigit():
            continue
        if val.replace(" ", "").upper() in ("USD/INR", "USDINR"):
            label_row = cell[1:]
        elif label_row and cell[1:] == label_row:
            if (v := _num(val)) and v > 1:
                return v
            label_row = None
    return None


def load_tapeout(path: Path):
    """Per-die cost, NRE, breakeven volume, incumbent comparison."""
    out = {}
    keys = {
        "Per-die cost at volume ($)": "die_cost_usd",
        "Breakeven volume (chips to recover NRE)": "breakeven_chips",
        "Total program NRE (one-time)": "nre_usd",
        "Gross margin per chip ($)": "gm_per_chip_usd",
        "Incumbent ADAS SoC cost ($)": "incumbent_usd",
        "Cost advantage vs incumbent (x)": "cost_advantage_x",
        "Good die per wafer": "good_die_per_wafer",
        "SoC2 die area (mm2)": "die_area_mm2",
    }
    for row in csv.reader(path.open(encoding="utf-8")):
        if len(row) < 2:
            continue
        if (k := keys.get(row[0].strip())) is not None and (v := _num(row[1])) is not None:
            out[k] = v
    return out


def fact(fid, text, formula, inputs, cites, tags):
    return {
        "id": fid,
        "text": " ".join(text.split()),
        "formula": formula,
        "inputs": inputs,
        "cites": cites,
        "tags": tags,
        "derived": True,
        "generator": "derive_facts.py",
    }


def derive(skus, margins, fx, tp):
    facts = []
    total_fy32 = sum(v["revenue"][5] for v in skus.values())
    die_usd = tp.get("die_cost_usd")
    die_inr = die_usd * fx if (die_usd and fx) else None
    breakeven = tp.get("breakeven_chips")

    facts.append(fact(
        "derived/portfolio-fy2032-total",
        f"Total FY2032 revenue across all {len(skus)} SKUs is Rs{total_fy32:,.2f} Cr. "
        f"Every SKU share percentage in this dossier is computed against this figure.",
        "sum(revenue[FY2032] for all SKUs)",
        [f"Revenue Build!{s}" for s in list(skus)[:3]] + ["..."],
        ["Revenue Build!Total (check)"], ["portfolio", "total", "fy2032"]))

    if die_usd and fx:
        facts.append(fact(
            "derived/soc2-die-cost-inr",
            f"One SoC2 die costs ${die_usd:.4f} at volume, which is Rs{die_inr:,.0f} "
            f"at the model's USD/INR rate of {fx:g}. The die cost is identical in every "
            f"product that carries one, regardless of that product's price.",
            "die_cost_usd * usd_inr",
            ["Tapeout Unit Economics!Per-die cost at volume ($)", "Assumptions!USD / INR"],
            ["Tapeout Unit Economics!Per-die cost at volume ($)"],
            ["soc2", "die", "cost", "unit-economics"]))

    for name, s in sorted(skus.items()):
        slug = (name.lower().replace(" ", "-").replace("+", "plus")
                .replace("(", "").replace(")", "").replace(".", "").replace("/", "-"))
        asp, units, rev = s["asp"], s["units"], s["revenue"]
        seg, dom = s.get("segment", ""), s.get("domain", "")
        fy32 = rev[5]
        share = fy32 / total_fy32 * 100 if total_fy32 else 0

        # 1. arithmetic integrity, re-derived rather than copied
        checks = [(u * asp / 1e7, r) for u, r in zip(units, rev)]
        ok = sum(1 for c, r in checks if abs(c - r) < 0.002)
        facts.append(fact(
            f"derived/{slug}/revenue-integrity",
            f"'{name}' revenue reproduces from units x ASP in {ok} of {len(checks)} fiscal "
            f"years (ASP Rs{asp:,}). {'The revenue build is internally consistent for this SKU.' if ok == len(checks) else 'MISMATCH: at least one year does not reconcile.'}",
            "units[y] * asp / 1e7 == revenue[y]  (tolerance 0.002 Cr)",
            [f"Revenue Build!{name} units", f"Revenue Build!{name} revenue"],
            [f"Revenue Build!{name}"], ["verification", "arithmetic", slug]))

        # 2. share of portfolio
        margin = margins.get(seg, [None] * 6)[5]
        mtxt = f" Its segment ({seg}) carries a {margin*100:.0f}% gross margin in FY2032." if margin else ""
        facts.append(fact(
            f"derived/{slug}/fy2032-share",
            f"'{name}' contributes Rs{fy32:,.2f} Cr in FY2032, {share:.2f}% of the "
            f"Rs{total_fy32:,.2f} Cr total.{mtxt}",
            "revenue[FY2032] / portfolio_total_FY2032 * 100",
            [f"Revenue Build!{name}", "Revenue Build!Total (check)",
             f"Assumptions!{seg} gross margin"],
            [f"Revenue Build!{name}"], ["share", "fy2032", slug]))

        # 3. growth shape - is it a constant multiple?
        mult = [round(units[i + 1] / units[i], 3) for i in range(1, 5) if units[i]]
        if mult:
            rounded = {round(m, 2) for m in mult}
            const = len(rounded) == 1
            nominal = next(iter(rounded)) if const else None
            exact = const and len(set(mult)) == 1
            facts.append(fact(
                f"derived/{slug}/growth-shape",
                f"'{name}' unit growth runs {' / '.join(f'{m:g}x' for m in mult)} across "
                f"FY2029-FY2032. " + ((f"That is a constant {nominal:g}x every year"
                + ("" if exact else " (the first step differs only by integer rounding of unit counts)")
                + ", which is a modelling assumption rather than a derived forecast.") if const else
                "The multiple varies year to year."),
                "units[y+1] / units[y] for each consecutive pair",
                [f"Revenue Build!{name} units"], [f"Revenue Build!{name}"],
                ["growth", "assumption", slug]))

        # 4. silicon intensity + breakeven contribution (compute SKUs carry one SoC2)
        if die_inr and dom == "Compute":
            cum = sum(units)
            pct = die_inr / asp * 100
            facts.append(fact(
                f"derived/{slug}/silicon-intensity",
                f"Silicon is {pct:.2f}% of the price of '{name}' (Rs{die_inr:,.0f} die in a "
                f"Rs{asp:,} product). {100-pct:.2f}% of the price is SDK, packaging, board and channel.",
                "(die_cost_usd * usd_inr) / asp * 100",
                ["Tapeout Unit Economics!Per-die cost at volume ($)", "Assumptions!USD / INR",
                 f"Revenue Build!{name} ASP"],
                ["Tapeout Unit Economics!Per-die cost at volume ($)"],
                ["silicon", "unit-economics", slug]))
            if breakeven:
                facts.append(fact(
                    f"derived/{slug}/breakeven-contribution",
                    f"'{name}' consumes {cum:,.0f} SoC2 dies across FY2028-FY2032 "
                    f"(one die per unit), {cum/breakeven*100:.1f}% of the {breakeven:,.0f}-chip "
                    f"NRE breakeven. It would need {breakeven/cum:.1f}x its planned volume to "
                    f"repay the tapeout on its own.",
                    "sum(units) / breakeven_chips * 100",
                    [f"Revenue Build!{name} units",
                     "Tapeout Unit Economics!Breakeven volume (chips to recover NRE)"],
                    ["Tapeout Unit Economics!Breakeven volume (chips to recover NRE)"],
                    ["breakeven", "nre", "dies", slug]))

    # line-level: the A100 compute boxes considered together
    line = {k: v for k, v in skus.items() if k.startswith("A100 compute box")}
    if line and die_inr and breakeven:
        cum = sum(sum(v["units"]) for v in line.values())
        rev32 = sum(v["revenue"][5] for v in line.values())
        u4 = next((v["units"] for k, v in line.items() if "4ch" in k), None)
        facts.append(fact(
            "derived/a100-compute-line/breakeven",
            f"The {len(line)} A100 compute box SKUs together consume {cum:,.0f} SoC2 dies "
            f"across FY2028-FY2032 and produce Rs{rev32:,.2f} Cr in FY2032. That die volume is "
            f"{cum/breakeven*100:.1f}% of the {breakeven:,.0f}-chip NRE breakeven, so the compute "
            f"line cannot fund the tapeout: the kits carry that volume. The line's role is adoption, "
            f"not silicon margin.",
            "sum(units across A100 compute SKUs) / breakeven_chips * 100",
            ["Revenue Build!A100 compute box 1ch/2ch/4ch",
             "Tapeout Unit Economics!Breakeven volume (chips to recover NRE)"],
            ["Tapeout Unit Economics!Breakeven volume (chips to recover NRE)"],
            ["a100", "compute-line", "breakeven", "platform-thesis"]))
        if u4:
            # Compare at 1 dp: unit counts are integers, so a small early-year cohort
            # rounds a genuinely constant ratio to 2.51:1.51 while later years give
            # 2.50:1.50. Testing exact string equality would drop a real finding.
            pairs = [(sum(v["units"][i] for k, v in line.items() if "1ch" in k) / u4[i],
                      sum(v["units"][i] for k, v in line.items() if "2ch" in k) / u4[i])
                     for i in range(1, 6) if u4[i]]
            ratios = [f"{a:.1f}:{b:.1f}:1.0" for a, b in pairs]
            if pairs and len(set(ratios)) == 1:
                facts.append(fact(
                    "derived/a100-compute-line/mix-ratio",
                    f"The 1ch:2ch:4ch unit mix is fixed at {ratios[0]} in every revenue year "
                    f"FY2028-FY2032. A constant mix across five years is an input to the model, "
                    f"not a result of it, and real channel mix typically drifts as a line matures.",
                    "units_1ch[y] : units_2ch[y] : units_4ch[y], each year",
                    ["Revenue Build!A100 compute box 1ch/2ch/4ch units"],
                    ["Revenue Build!A100 compute box 4ch +SDK (PCIe)"],
                    ["a100", "mix", "assumption"]))
    return facts


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=str(Path(__file__).parent / "data"))
    ap.add_argument("--out", default="derived-facts.json")
    ap.add_argument("--dump", help="cell dump used to recover USD/INR when the CSV omits it")
    ap.add_argument("--sku", help="only emit facts whose id mentions this substring")
    a = ap.parse_args()

    d = Path(a.data)
    need = {"revenue_build": "revenue", "assumptions": "assumptions",
            "tapeout_unit_economics": "tapeout"}
    paths = {}
    for stem, key in need.items():
        p = d / f"{PREFIX}{stem}.csv"
        if not p.exists():
            print(f"ERROR: missing {p}", file=sys.stderr)
            return 1
        paths[key] = p

    skus = load_revenue(paths["revenue"])
    margins, fx = load_assumptions(paths["assumptions"])
    fx_source = "Assumptions CSV"
    if fx is None:
        dump = Path(a.dump) if a.dump else d.parent / "evidence" / "corrected-model-dump.txt"
        fx = load_fx_from_dump(dump)
        fx_source = f"cell dump ({dump.name})" if fx else "NOT FOUND"
    tp = load_tapeout(paths["tapeout"])
    if not skus:
        print("ERROR: no SKUs parsed from the revenue build", file=sys.stderr)
        return 1
    if fx is None:
        print("WARNING: USD/INR not found; currency-derived facts are skipped",
              file=sys.stderr)

    facts = derive(skus, margins, fx, tp)
    if a.sku:
        facts = [f for f in facts if a.sku.lower() in f["id"].lower()
                 or a.sku.lower() in f["text"].lower()]

    Path(a.out).write_text(json.dumps(facts, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"SKUs parsed        : {len(skus)}")
    print(f"USD/INR            : {fx if fx else 'NOT FOUND'}  (source: {fx_source})")
    print(f"die cost / breakeven: ${tp.get('die_cost_usd', '?')} / {tp.get('breakeven_chips', '?')}")
    print(f"derived facts      : {len(facts)} -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
