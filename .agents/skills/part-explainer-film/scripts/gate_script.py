#!/usr/bin/env python3
"""Gate an authored explainer script before any voice is spent. Exit 0 clean, 2 findings, 1 blocked.

Checks, per scene and for the film: authored label (2-6 words) and narration; only the allowed
emotion tags and none of the pause tags; no dashes; no banned claim words; every numeral traced to
the storyboard or the product page text; narration does not recite its own source; estimated pace.

Usage: gate_script.py scenes.json [--page-text page.txt] [--wpm 145]
"""
import argparse, json, re, sys
from spoken import TAG, strip_tags, spoken_words, numerals

ALLOWED_TAGS = {"thoughtful", "curious", "serious", "confident"}   # judgment rule: arc points only
MAX_TAGS = 4
BANNED = re.compile(r"\b(certified|certification|compliant|compliance|guarantee[ds]?|world[- ]class|revolutionary|"
                    r"cutting[- ]edge|game[- ]chang\w*|seamless\w*|unparalleled)\b", re.I)
SPELLED = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|"
                     r"sixty|seventy|eighty|ninety|hundred|thousand)(-\w+)?\b", re.I)
ECHO_MAX = 0.35

def trigrams(t):
    w = re.findall(r"[a-z0-9]+", strip_tags(t).lower()); return {tuple(w[i:i+3]) for i in range(len(w) - 2)}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("scenes"); ap.add_argument("--page-text"); ap.add_argument("--wpm", type=float, default=145)
    a = ap.parse_args()
    d = json.load(open(a.scenes)); sc = d["scenes"]
    if not sc: sys.exit("BLOCKED: no scenes")
    corpus = " ".join([d.get("headline", "")] + [s.get("source", "") + " " + s.get("title", "") for s in sc])
    if a.page_text: corpus += " " + open(a.page_text, encoding="utf-8").read()
    known = numerals(corpus)
    F, tags_total, words_total = [], 0, 0
    for s in sc:
        sid, lab, nar = s["id"], s.get("label", "").strip(), s.get("narration", "").strip()
        if not nar: F.append(f"{sid}: narration not authored"); continue
        n = len(lab.split())
        if not 2 <= n <= 6: F.append(f"{sid}: label has {n} words, want 2-6: {lab!r}")
        tags = [t.strip("[]").strip().lower() for t in TAG.findall(nar)]
        tags_total += len(tags)
        for t in tags:
            if "pause" in t: F.append(f"{sid}: [{t}] pause tag; pauses come from punctuation (they ran 1.7-1.8 s)")
            elif t not in ALLOWED_TAGS: F.append(f"{sid}: tag [{t}] not in {sorted(ALLOWED_TAGS)}")
        if len(tags) > (2 if s.get("kind") == "close" else 1): F.append(f"{sid}: {len(tags)} tags in one scene; one at most, two in the close")
        for txt, where in ((nar, "narration"), (lab, "label")):
            if re.search("[—–]", txt): F.append(f"{sid}: dash in {where}")
            for m in BANNED.finditer(txt): F.append(f"{sid}: banned claim word {m.group(0)!r} in {where}")
            for m in SPELLED.finditer(strip_tags(txt)):
                if re.search(r"\b" + re.escape(m.group(0).lower()) + r"\b", corpus.lower()): continue  # a count the source states
                F.append(f"{sid}: spelled-out number {m.group(0)!r} in {where}; not in the source; write a numeral the claim gate can trace")
            for num in numerals(txt) - known:
                if where == "narration" and num in {"1", "2"}: continue
                F.append(f"{sid}: number {num} in {where} is not in the storyboard or product page text")
        src = trigrams(s.get("source", "")); mine = trigrams(nar)
        echo = len(mine & src) / len(mine) if mine else 0
        if echo > ECHO_MAX: F.append(f"{sid}: narration echoes its source {echo:.0%} (max {ECHO_MAX:.0%}); say what it means")
        words_total += spoken_words(nar)
    if tags_total > MAX_TAGS: F.append(f"film: {tags_total} emotion tags, max {MAX_TAGS}")
    est = words_total / a.wpm * 60
    print(f"{len(sc)} scenes, {words_total} spoken words, ~{est:.0f} s at {a.wpm:.0f} wpm, "
          f"{sum(len(s.get('narration', '')) for s in sc)} characters billed")
    if not 40 <= est <= 95: F.append(f"film: estimated {est:.0f} s, target 45-90 s")
    for f in F: print("FINDING", f)
    print("CLEAN" if not F else f"{len(F)} findings")
    sys.exit(2 if F else 0)

if __name__ == "__main__":
    main()
