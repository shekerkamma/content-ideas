#!/usr/bin/env python3
"""Voice gate. Per scene: spoken-word pace, longest internal pause, and a transcript-vs-script word match.
Exit 0 clean, 2 findings, 1 blocked.

Pauses come from ffmpeg silencedetect on the audio, never from transcript word gaps: Whisper's word
timestamps absorb trailing silence (measured 2026-10-03: 0.0 s "gaps" where 0.86 s of silence sat).
The transcript check needs GROQ_API_KEY; without it the check is BLOCKED, not skipped.

A transcript difference is waived only by a scene's "voice_waivers": [{"diff", "reason"}], and every
waiver is printed on each run. Usage: measure_voice.py scenes.json [--wpm 140-155] [--max-pause 1.6]
"""
import argparse, difflib, hashlib, json, os, pathlib, re, subprocess, sys
from spoken import spoken_words, strip_tags

def silences(p, lead_trim=0.3):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-af", "silencedetect=noise=-38dB:d=0.15", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", e)]; du = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", e)]
    return [(s, d) for s, d in zip(st, du)]

def transcribe(p, key, cache):
    if cache.exists(): return json.load(open(cache))["text"]
    r = subprocess.run(["curl", "-s", "https://api.groq.com/openai/v1/audio/transcriptions", "-H", f"Authorization: Bearer {key}",
                        "-F", f"file=@{p}", "-F", "model=whisper-large-v3", "-F", "response_format=json", "-F", "language=en"],
                       capture_output=True, text=True).stdout
    j = json.loads(r)
    if "text" not in j: sys.exit(f"BLOCKED: transcription failed: {str(j)[:200]}")
    json.dump(j, open(cache, "w")); return j["text"]

UNITS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
                                     "fifteen sixteen seventeen eighteen nineteen".split())}
UNITS.update({w: 10 * i for i, w in enumerate("_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()) if w != "_"})
SAME = {"pole": "poll", "break": "brake", "dyes": "dies", "kilometers": "kilometres", "khz": "kilohertz", "ghz": "gigahertz",
        "mhz": "megahertz", "mw": "milliwatts", "colour": "color", "metre": "meter", "metres": "meters", "light": "lite"}
def norm(t):
    """Words as compared: a spoken number in either text becomes digits ("fifteen" = "15", "thirty-two" = "32"),
    because the transcriber writes numerals for some numbers and words for others."""
    t = strip_tags(t).lower().replace("...", " ")
    t = re.sub(r"(\d)\s*-\s*volt", r"\1 volt", t)
    t = re.sub(r"\b(sku|dg)-?(\d)", r"\1 \2", t)
    out, cur = [], None
    for x in re.findall(r"[a-z]+|\d+(?:\.\d+)?", t):
        if x in UNITS: cur = UNITS[x] if cur is None else cur + UNITS[x]; continue   # "thirty two" = 32
        if x == "hundred" and cur is not None: cur *= 100; continue
        if cur is not None: out.append(str(cur)); cur = None
        out.append(x)
    if cur is not None: out.append(str(cur))
    return [SAME.get(x, x) for x in out]   # homophones and the transcriber's spellings sound the same

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("scenes"); ap.add_argument("--wpm", default="140-155"); ap.add_argument("--max-pause", type=float, default=1.6)
    a = ap.parse_args(); lo, hi = map(float, a.wpm.split("-"))
    run = pathlib.Path(a.scenes).resolve().parent
    doc = json.load(open(a.scenes)); sc = {s["id"]: s for s in doc["scenes"]}; lex = doc.get("pronounce", {})
    def said(t):   # compare against what the TTS was told to say
        for k, v in lex.items(): t = t.replace(k, v)
        return t
    vo = json.load(open(run / "voice.json"))["scenes"]
    key = os.environ.get("GROQ_API_KEY") or subprocess.run(["bash", "-ic", 'printf %s "$GROQ_API_KEY"'], capture_output=True, text=True).stdout
    if not key: sys.exit("BLOCKED: GROQ_API_KEY not set; the transcript check cannot run (it is not optional)")
    (run / "work" / "asr").mkdir(parents=True, exist_ok=True)
    F, rows, W, T = [], [], 0, 0.0
    for v in vo:
        p = run / v["audio"]; s = sc[v["scene"]]; d = v["duration"]; sw = spoken_words(s["narration"])
        sil = silences(p); inner = [x for x in sil if x[0] > 0.3 and x[0] + x[1] < d - 0.2]
        talk = d - sum(x[1] for x in sil if x[0] <= 0.3 or x[0] + x[1] >= d - 0.2)  # trim head/tail silence
        wpm = sw / talk * 60; W += sw; T += talk
        longest = max([x[1] for x in inner], default=0)
        heard = transcribe(p, key, run / "work" / "asr" / f"{p.stem}-{hashlib.md5(p.read_bytes()).hexdigest()[:10]}.json")   # keyed by content: a re-voiced take with the same name is re-heard
        want, got = norm(said(s["narration"])), norm(heard)
        ratio = difflib.SequenceMatcher(None, want, got).ratio()
        diff = [f"{tag}:{' '.join(want[i1:i2])}->{' '.join(got[j1:j2])}" for tag, i1, i2, j1, j2 in
                difflib.SequenceMatcher(None, want, got).get_opcodes() if tag != "equal"]
        # audio carries no word spaces: "bus load" heard as "busload" is the transcriber's spacing, not the voice
        spacing = [x for x in diff if x.startswith("replace:") and x[8:].split("->")[0].replace(" ", "") == x[8:].split("->")[1].replace(" ", "")]
        for x in spacing: print(f"  SPACING {v['scene']} {x}: same letters, transcriber's word split")
        diff = [x for x in diff if x not in spacing]
        if not diff: ratio = 1.0
        waived = [w for w in s.get("voice_waivers", []) if w["diff"] in diff]
        for w in waived: print(f"  WAIVED {v['scene']} {w['diff']}: {w['reason']}")
        if waived and len(waived) == len(diff): ratio = 1.0
        rows.append({"scene": v["scene"], "seconds": d, "spoken_words": sw, "wpm": round(wpm), "longest_pause": round(longest, 2),
                     "pauses": [round(x[1], 2) for x in inner], "match": round(ratio, 3), "diff": diff, "heard": heard.strip()})
        if longest > a.max_pause: F.append(f"{v['scene']}: pause {longest:.2f} s over {a.max_pause}")
        if ratio < 0.97: F.append(f"{v['scene']}: transcript differs from script ({ratio:.0%}): {diff}")
        if not (lo - 15 <= wpm <= hi + 15):
            pw = s.get("pace_waiver")   # a single scene may run slow or fast with a written reason; the film band never waives
            if pw: print(f"  PACE WAIVED {v['scene']} {wpm:.0f} wpm: {pw}")
            else: F.append(f"{v['scene']}: {wpm:.0f} wpm far outside {a.wpm}")
    film = W / T * 60
    if not (lo <= film <= hi): F.append(f"film: {film:.0f} wpm outside {a.wpm}")
    json.dump({"film_wpm": round(film, 1), "scenes": rows, "findings": F}, open(run / "voice-gate.json", "w"), indent=1, ensure_ascii=False)
    for r in rows: print(f"{r['scene']:>6} {r['seconds']:6.2f}s {r['wpm']:4d} wpm  longest pause {r['longest_pause']:.2f}s  match {r['match']:.0%}  {r['diff'] or ''}")
    print(f"film {film:.0f} wpm (spoken words over talking time)")
    for f in F: print("FINDING", f)
    print("CLEAN" if not F else f"{len(F)} findings"); sys.exit(2 if F else 0)

if __name__ == "__main__":
    main()
