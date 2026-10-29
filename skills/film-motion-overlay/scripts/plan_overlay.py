#!/usr/bin/env python3
"""Plan attention motion over a narrated deck film: for each caption cue, the region of the slide the
sentence is about, or nothing.

Inputs are the film's own build records, never OCR: <slug>-film.json (slide segments and times), the
.vtt (cue times), and the deck's artifact-tool inspect.ndjson (every text box with its bbox on the
1280x720 stage). A cue matches the text box sharing the most distinctive words and numbers with it
(numbers spoken as words are normalised: "thirty-nine" = 39). Title, kicker and footer boxes are never
targets: the headline is already where the eye starts. A cue with no match below the threshold keeps
the previous framing; nothing moves without a reason.

Usage: plan_overlay.py --film film.mp4 --film-json f.json --vtt f.vtt --inspect deck.inspect.ndjson --out plan.json [--min-score 2.0]
"""
import argparse, json, math, re, sys

STOP = set("the a an and or of to in on at for by with from is are was were be been it its this that these those as into "
           "than then there here what which who how one two each every per can will not no but so if more most only same "
           "your you we our they their them about also just between does do has have had".split())
UNITS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
         "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
         "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}

def numbers_in_words(t):
    """'one hundred thirty' -> 130, 'thirty-nine' -> 39, 'three thousand two hundred' -> 3200 (good enough for narration)."""
    out, cur, total, seen = [], 0, 0, False
    for w in re.findall(r"[a-z]+", t.lower().replace("-", " ")) + ["."]:
        if w in UNITS: cur += UNITS[w]; seen = True
        elif w == "hundred" and seen: cur = max(cur, 1) * 100
        elif w == "thousand" and seen: total += max(cur, 1) * 1000; cur = 0
        elif w == "and" and seen: continue
        else:
            if seen: out.append(str(total + cur))
            cur, total, seen = 0, 0, False
    return out

def tokens(t):
    t = t.replace("\u00a0", " ")
    nums = re.findall(r"\d+(?:[.,]\d+)?", t)
    nums = [n.replace(",", "") for n in nums] + numbers_in_words(t)
    words = [w for w in re.findall(r"[a-z][a-z0-9-]{2,}", t.lower()) if w not in STOP and w not in UNITS]
    return set(words) | {"#" + n for n in nums}

def ts(s):
    h, m, x = s.split(":"); return int(h) * 3600 + int(m) * 60 + float(x)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--film-json", required=True); ap.add_argument("--vtt", required=True); ap.add_argument("--inspect", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--min-score", type=float, default=2.0)
    ap.add_argument("--stage", default="1280x720")
    ap.add_argument("--film", help="the film itself; slide boundaries are then measured from it, not taken from film.json")
    a = ap.parse_args()
    SW, SH = map(int, a.stage.split("x"))
    film = json.load(open(a.film_json))
    if a.film:   # slide boundaries from cuts measured in the film itself: build records drift (+0.13 s by slide 13 on LITE architecture)
        import subprocess, pathlib
        cuts = json.loads(subprocess.run([sys.executable, str(pathlib.Path(__file__).with_name("find_cuts.py")), a.film], capture_output=True, text=True).stdout)
        if len(cuts) != len(film["segments"]) - 1: sys.exit(f"BLOCKED: measured {len(cuts)} cuts, film.json has {len(film['segments']) - 1}; check find_cuts on this film")
        vd = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=duration", "-of", "csv=p=0", a.film], capture_output=True, text=True).stdout)
        edges = [0.0] + cuts + [vd]
        for k, seg in enumerate(film["segments"]): seg["start"], seg["duration"] = edges[k], round(edges[k + 1] - edges[k], 4)
    cues = [(ts(m.group(1)), ts(m.group(2)), m.group(3).strip()) for m in
            re.finditer(r"(\d\d:\d\d:\d\d\.\d+) --> (\d\d:\d\d:\d\d\.\d+)\s*\n(.+?)(?:\n\n|\Z)", open(a.vtt, encoding="utf-8").read(), re.S)]
    if not cues: sys.exit("BLOCKED: no cues parsed from the VTT")
    boxes = {}
    for line in open(a.inspect, encoding="utf-8"):
        r = json.loads(line)
        if r.get("kind") in ("textbox", "shape") and "bbox" in r: boxes.setdefault(r["slide"], []).append(r)
    plan = {"stage": [SW, SH], "segments": []}; hit = 0
    for seg in film["segments"]:
        s0, s1 = seg["start"], seg["start"] + seg["duration"]; sl = seg["slide"]
        def label(b):
            """An uppercase phrase label outside a card (a table header row, a kicker, a small caption) shares words
            with the sentence but is never what it is about: 25 of 234 first-pass targets were these."""
            t = b["text"]; letters = re.sub(r"[^A-Za-z]", "", t); words = re.findall(r"[A-Za-z]{3,}", t)
            return len(letters) >= 3 and letters == letters.upper() and b["bbox"][3] < 60 and (len(words) >= 2 or not re.search(r"\d", t))
        tb = [b for b in boxes.get(sl, []) if b["kind"] == "textbox" and b.get("text") and not label(b)
              and b["bbox"][1] >= 0.2 * SH and b["bbox"][1] + b["bbox"][3] <= 0.9 * SH]      # not title, not footer, not a label
        shapes = [b for b in boxes.get(sl, []) if b["kind"] == "shape"]
        df = {}
        for b in tb:
            for k in tokens(b["text"]): df[k] = df.get(k, 0) + 1
        moves = []
        for c0, c1, text in [c for c in cues if s0 <= c[0] < s1]:
            ct = tokens(text); best, score = None, 0.0
            for b in tb:
                shared = ct & tokens(b["text"])
                sc = sum((2.0 if k.startswith("#") else 1.0) * math.log(1 + len(tb) / df[k]) for k in shared)
                if sc > score: best, score = b, sc
            target = None
            if best and score >= a.min_score:
                x, y, w, h = best["bbox"]
                # grow to the smallest card that contains the box, so the frame lands on the whole card
                cont = [s for s in shapes if s["bbox"][0] <= x + 1 and s["bbox"][1] <= y + 1 and s["bbox"][0] + s["bbox"][2] >= x + w - 1
                        and s["bbox"][1] + s["bbox"][3] >= y + h - 1 and s["bbox"][2] * s["bbox"][3] < 0.35 * SW * SH]
                if cont: x, y, w, h = min(cont, key=lambda s: s["bbox"][2] * s["bbox"][3])["bbox"]
                target = {"bbox": [x, y, w, h], "text": best["text"][:80], "score": round(score, 2)}; hit += 1
            moves.append({"t": round(c0, 3), "end": round(c1, 3), "cue": text[:90], "target": target})
        head = [b["bbox"] for b in boxes.get(sl, []) if b["kind"] == "textbox" and b.get("text") and b["bbox"][1] < 0.2 * SH]
        keep = None
        if head:   # the headline band (kicker, title, subtitle) must stay whole in every framing
            x0 = min(b[0] for b in head); y0 = min(b[1] for b in head)
            keep = [x0, y0, max(b[0] + b[2] for b in head) - x0, max(b[1] + b[3] for b in head) - y0]
        plan["segments"].append({"slide": sl, "start": s0, "duration": seg["duration"], "keep": keep, "moves": moves})
    json.dump(plan, open(a.out, "w"), indent=1, ensure_ascii=False)
    total = sum(len(s["moves"]) for s in plan["segments"])
    print(f"{len(plan['segments'])} slides, {total} cues, {hit} matched to a region ({hit/total:.0%}) -> {a.out}")

if __name__ == "__main__":
    main()
