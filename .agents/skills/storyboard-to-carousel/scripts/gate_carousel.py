#!/usr/bin/env python3
"""Gate authored carousel copy before rendering. Exit 0 clean, 2 findings, 1 blocked.

Per slide: body authored and at most 25 words; each beat's hero figure and every close/CTA item (3 each,
at most 14 words) are checked like the body; (cover/close/cta included); title at most 70 characters;
no dashes; no banned claim words; every numeral traced to the storyboard or the product page text;
the body does not recite its own source (trigram echo over 40 %); straight quotes become curly ones
on render, so they are not findings here.
Usage: gate_carousel.py carousel.json [--page-text page.txt]
"""
import argparse, json, re, sys

BANNED = re.compile(r"\b(certified|certification|compliant|compliance|guarantee[ds]?|world[- ]class|revolutionary|cutting[- ]edge|"
                    r"game[- ]chang\w*|seamless\w*|unparalleled|unlock\w*|leverag\w*)\b", re.I)
def nums(t): return set(re.findall(r"\d+(?:\.\d+)?", t.replace(",", "")))
def tri(t):
    w = re.findall(r"[a-z0-9]+", t.lower()); return {tuple(w[i:i + 3]) for i in range(len(w) - 2)}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("carousel"); ap.add_argument("--page-text"); a = ap.parse_args()
    d = json.load(open(a.carousel)); S = d["slides"]
    if not S: sys.exit("BLOCKED: no slides")
    corpus = " ".join(s.get("source", "") + " " + s.get("title", "") for s in S) + " " + d.get("url", "")
    if a.page_text: corpus += " " + open(a.page_text, encoding="utf-8").read()
    known = nums(corpus); F = []
    for s in S:
        sid, title, body = s["id"], s.get("title", "").strip(), s.get("body", "").strip()
        if not body: F.append(f"{sid}: body not authored"); continue
        if s["kind"] == "cta" and not title: F.append(f"{sid}: cta title not authored")
        n = len(body.split())
        if n > 25: F.append(f"{sid}: body has {n} words, max 25")
        if len(title) > 70: F.append(f"{sid}: title is {len(title)} characters, max 70")
        extra = []
        if s.get("stat"): extra += [(s["stat"].get("value", ""), "stat"), (s["stat"].get("label", ""), "stat label")]
        for k, it in enumerate(s.get("items", [])):
            extra.append((it, f"item {k + 1}"))
            if len(it.split()) > 14: F.append(f"{sid}: item {k + 1} has {len(it.split())} words, max 14")
        if s["kind"] in ("close", "cta") and len(s.get("items", [])) != 3: F.append(f"{sid}: needs exactly 3 items, has {len(s.get('items', []))}")
        for txt, where in ((title, "title"), (body, "body"), *extra):
            if re.search("[—–]", txt): F.append(f"{sid}: dash in {where}")
            for m in BANNED.finditer(txt): F.append(f"{sid}: banned word {m.group(0)!r} in {where}")
            for x in nums(txt) - known: F.append(f"{sid}: number {x} in {where} is not in the storyboard or product page")
        src, mine = tri(s.get("source", "")), tri(body)
        if mine and len(mine & src) / len(mine) > 0.4: F.append(f"{sid}: body echoes its source {len(mine & src) / len(mine):.0%}; say what it means")
    for f in F: print("FINDING", f)
    print("CLEAN" if not F else f"{len(F)} findings"); sys.exit(2 if F else 0)

if __name__ == "__main__":
    main()
