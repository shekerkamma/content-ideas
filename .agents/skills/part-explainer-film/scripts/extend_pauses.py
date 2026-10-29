#!/usr/bin/env python3
"""Open the pauses a voice rushed, to the Holt lengths, without touching the speech.

The Holt reference itself was made this way ("modest slowing and selected pauses extended"). Only
silence is inserted, at the gap the voice already left at a script comma, full stop or ellipsis;
speech is never time-stretched, because stretching cannot create emotion and smears consonants.

Gaps are located from the audio (silencedetect at -45 dB) and matched to script punctuation through
Whisper word times, using the midpoint between a word's end and the next word's start; Whisper word
times absorb silence, so they locate a boundary but never measure a pause. A boundary with no gap
within 0.35 s is left alone and reported; inside the window the LONGEST gap is taken (the nearest one
was a 0.07 s breath inside the word before a 0.24 s pause, measured 2026-10-03).

Usage: extend_pauses.py scenes.json --scene close   (updates voice.json to the paced file)
"""
import argparse, difflib, hashlib, json, os, pathlib, re, subprocess, sys

HOLT = {",": 0.32, ".": 0.65, "?": 0.65, "!": 0.65, "...": 1.1}

def gaps(p):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-af", "silencedetect=noise=-45dB:d=0.05", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return [(float(s), float(d)) for s, d in zip(re.findall(r"silence_start: ([\d.]+)", e), re.findall(r"silence_duration: ([\d.]+)", e))]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("scenes"); ap.add_argument("--scene", required=True); a = ap.parse_args()
    run = pathlib.Path(a.scenes).resolve().parent
    S = {s["id"]: s for s in json.load(open(a.scenes))["scenes"]}[a.scene]
    vj = json.load(open(run / "voice.json")); V = next(v for v in vj["scenes"] if v["scene"] == a.scene)
    src = run / V["audio"]
    if ".paced" in src.name: sys.exit("BLOCKED: already paced; work from the original voiced file")
    key = os.environ.get("GROQ_API_KEY") or subprocess.run(["bash", "-ic", 'printf %s "$GROQ_API_KEY"'], capture_output=True, text=True).stdout
    wj = run / "work" / "asr" / f"{a.scene}-{hashlib.md5(src.read_bytes()).hexdigest()[:10]}.words.json"   # content-keyed: a re-voice must be re-heard
    if not wj.exists():
        wj.parent.mkdir(parents=True, exist_ok=True)
        wj.write_text(subprocess.run(["curl", "-s", "https://api.groq.com/openai/v1/audio/transcriptions", "-H", f"Authorization: Bearer {key}",
            "-F", f"file=@{src}", "-F", "model=whisper-large-v3", "-F", "language=en", "-F", "response_format=verbose_json",
            "-F", "timestamp_granularities[]=word"], capture_output=True, text=True).stdout)
    words = json.load(open(wj))["words"]
    # script tokens with the punctuation that follows each
    text = re.sub(r"\[[^\]]+\]", " ", S["narration"])
    toks = [(m.group(1), m.group(2)) for m in re.finditer(r"([\w'’.-]+?)(\.\.\.|[.,?!])?(?=\s|$)", text)]
    n = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
    sm = difflib.SequenceMatcher(None, [n(t) for t, _ in toks], [n(w["word"]) for w in words])
    cuts, report = [], []
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            i, j = blk.a + k, blk.b + k
            p = toks[i][1]
            if not p or j + 1 >= len(words): continue
            mid = (words[j]["end"] + words[j + 1]["start"]) / 2
            near = [g for g in gaps(src) if abs(g[0] + g[1] / 2 - mid) <= 0.35]
            if not near: report.append(f"no gap near '{toks[i][0]}{p}' at {mid:.2f}s; left alone"); continue
            g = max(near, key=lambda g: g[1]); add = HOLT[p] - g[1]   # the real pause is the longest gap near the boundary
            if add > 0.02: cuts.append((g[0] + g[1] / 2, add)); report.append(f"'{toks[i][0]}{p}' gap {g[1]:.2f}s -> {HOLT[p]:.2f}s")
    if not cuts: print("\n".join(report)); print("nothing to extend"); return
    cuts.sort(); parts, filt, prev = [], [], 0.0
    for k, (t, add) in enumerate(cuts):
        filt.append(f"[0:a]atrim={prev}:{t},asetpts=PTS-STARTPTS[s{k}]"); filt.append(f"anullsrc=r=44100:cl=mono,atrim=0:{add:.3f}[z{k}]")
        parts += [f"[s{k}]", f"[z{k}]"]; prev = t
    filt.append(f"[0:a]atrim={prev},asetpts=PTS-STARTPTS[s{len(cuts)}]"); parts.append(f"[s{len(cuts)}]")
    filt.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1[out]")
    out = src.with_name(src.stem + ".paced.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-filter_complex", ";".join(filt), "-map", "[out]", "-ac", "1", "-ar", "44100", str(out)], check=True)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout)
    V.update({"audio": str(out.relative_to(run)), "duration": round(d, 3), "paced_from": str(src.relative_to(run)), "pauses_added_s": round(sum(c[1] for c in cuts), 2)})
    json.dump(vj, open(run / "voice.json", "w"), indent=1)
    print("\n".join(report)); print(f"{a.scene}: +{sum(c[1] for c in cuts):.2f}s of pause -> {out.name} ({d:.2f}s)")

if __name__ == "__main__":
    main()
