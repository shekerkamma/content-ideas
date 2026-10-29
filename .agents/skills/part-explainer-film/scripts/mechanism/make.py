#!/usr/bin/env python3
"""Build a mechanism explainer for one part: existing gated narration -> HyperFrames project -> MP4.

Reuses the part's voiced scenes (content-ideas runs/2026-10-03-part-explainers/<part>: scenes.json for the
script, voice.json for the gated audio), so only the picture changes and no TTS credit is spent. Word
timings come from Groq Whisper and are aligned to the script so captions use the script's spelling.
Frames come from specs/<part>.py over lib.py's primitives; everything after the frames is the
faceless-explainer workflow's own scripts (captions, assemble, transitions) and the HyperFrames CLI.

Usage: make.py <part> [--render]   -> ~/hyperframes-videos/videos/<part>-mechanism/
"""
import argparse, difflib, importlib.util, json, os, pathlib, re, shutil, subprocess, sys

HOME = pathlib.Path.home(); HERE = pathlib.Path(__file__).resolve().parent
RUNS = HOME / "content-ideas/runs/2026-10-03-part-explainers"
TEMPLATE = HOME / "hyperframes-videos/videos/dg32-fault-path-explained"
FE = HOME / ".claude/skills/faceless-explainer/scripts"
DS = HOME / "deepgrid-dr-silicon-v6/design-system/fonts"
NODE_BIN = (sorted(HOME.glob(".nvm/versions/node/v2*/bin")) or [pathlib.Path("/usr/bin")])[-1]   # HyperFrames needs Node 20+; the PATH node here is 18
ENV = dict(os.environ, PATH=f"{NODE_BIN}:{os.environ['PATH']}")
sys.path.insert(0, str(HERE)); import lib


def sh(*cmd, cwd=None, check=True):
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, env=ENV, capture_output=True, text=True)
    if check and r.returncode: sys.exit(f"BLOCKED: {' '.join(map(str, cmd[:4]))}\n{r.stdout[-1500:]}{r.stderr[-1500:]}")
    return r


def groq_words(wav, cache):
    if cache.exists(): return json.load(open(cache))["words"]
    key = os.environ.get("GROQ_API_KEY") or subprocess.run(["bash", "-ic", 'printf %s "$GROQ_API_KEY"'], capture_output=True, text=True).stdout
    r = subprocess.run(["curl", "-s", "https://api.groq.com/openai/v1/audio/transcriptions", "-H", f"Authorization: Bearer {key}", "-F", f"file=@{wav}",
                        "-F", "model=whisper-large-v3-turbo", "-F", "language=en", "-F", "response_format=verbose_json", "-F", "timestamp_granularities[]=word"],
                       capture_output=True, text=True).stdout
    j = json.loads(r)
    if "words" not in j: sys.exit(f"BLOCKED: transcription failed for {wav}: {str(j)[:200]}")
    cache.write_text(json.dumps(j)); return j["words"]


def align(script, heard):
    """Script words carrying the transcriber's times, so captions spell what the script says."""
    sw = re.sub(r"\[[^\]]+\]", " ", script).replace("...", " ").split()
    n = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
    sm = difflib.SequenceMatcher(None, [n(w) for w in sw], [n(w["word"]) for w in heard], autojunk=False)
    t = [None] * len(sw)
    for b in sm.get_matching_blocks():
        for k in range(b.size): t[b.a + k] = (heard[b.b + k]["start"], heard[b.b + k]["end"])
    # interpolate words the transcriber split or merged
    known = [i for i, x in enumerate(t) if x]
    for i in range(len(sw)):
        if t[i] is None:
            lo = max([k for k in known if k < i], default=None); hi = min([k for k in known if k > i], default=None)
            s = t[lo][1] if lo is not None else 0.0; e = t[hi][0] if hi is not None else (heard[-1]["end"] if heard else s + .3)
            t[i] = (s, max(s + .05, e))
    # the transcriber can overlap neighbours ("or" 9.20-9.36, "0.9" from 8.88); captions sort by start, so force order
    out, prev = [], 0.0
    for w, (a, b) in zip(sw, t):
        a = max(a, prev); b = max(b, a + .05); prev = b
        out.append({"text": w, "start": round(a, 3), "end": round(b, 3)})
    return out


def resolve(cue, ws, dur, where="scene"):
    """A cue to seconds on the scene's clock. Spoken words first: "3.3", "1.8" and "0.9" are rail values the
    narration says, not fractions (the first resolver read "3.3" as 3.3 x the scene and put a rail 47 s into a
    14 s scene). "@0.4" or a float forces a fraction; "word#2" is the second occurrence; a decimal of 1 or less
    is a fraction only when no word matches it. A cue that resolves to nothing blocks the build."""
    c = str(cue)
    if isinstance(cue, float) or c.startswith("@"): return float(c.lstrip("@")) * dur
    key, _, nth = c.partition("#"); nth = int(nth or 1); hits = 0
    for w in ws:
        if re.sub(r"[^a-z0-9.µ]", "", w["text"].lower()).rstrip(".").startswith(key.lower()):
            hits += 1
            if hits == nth: return w["start"]
    if re.fullmatch(r"[0-9]*\.[0-9]+", key) and float(key) <= 1: return float(key) * dur
    raise SystemExit(f"BLOCKED: {where}: cue word {cue!r} not in its narration")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("part"); ap.add_argument("--render", action="store_true"); a = ap.parse_args()
    run = RUNS / a.part; proj = HOME / "hyperframes-videos/videos" / f"{a.part}-mechanism"
    spec_mod = importlib.util.spec_from_file_location("spec", HERE / "specs" / f"{a.part}.py")
    spec = importlib.util.module_from_spec(spec_mod); spec_mod.loader.exec_module(spec)
    scenes = json.load(open(run / "scenes.json")); voice = {v["scene"]: v for v in json.load(open(run / "voice.json"))["scenes"]}
    # 1. project skeleton from the template (its caption skin, frame.md, CLI pin); never its frames or audio
    (proj / "assets/voice").mkdir(parents=True, exist_ok=True); (proj / "assets/fonts").mkdir(parents=True, exist_ok=True)
    (proj / "compositions/frames").mkdir(parents=True, exist_ok=True); (proj / ".hyperframes").mkdir(exist_ok=True); (proj / "work").mkdir(exist_ok=True)
    for f in ("hyperframes.json", "frame.md", ".hyperframes/caption-skin.html"): shutil.copy(TEMPLATE / f, proj / f)
    pkg = json.load(open(TEMPLATE / "package.json")); pkg["name"] = f"{a.part}-mechanism"; json.dump(pkg, open(proj / "package.json", "w"), indent=2)
    for f in (TEMPLATE / "assets/fonts").iterdir():   # the caption skin's Georgia; the template's copies are read-only
        if not (proj / "assets/fonts" / f.name).exists(): shutil.copyfile(f, proj / "assets/fonts" / f.name)
    for src, dst in (("newsreader-latin-wght-normal.woff2", "newsreader.woff2"), ("inter-latin-wght-normal.woff2", "inter.woff2"),
                     ("jetbrains-mono-latin-wght-normal.woff2", "jetbrains-mono.woff2")): shutil.copy(DS / src, proj / "assets/fonts" / dst)
    (proj / "BRIEF.md").write_text(f"""---\nworkflow: faceless-explainer\nflow: automation\nstoryboard: no\nmessage: {json.dumps(scenes['headline'])}\ndestination: embed\naspect: 1920x1080\nlanguage: en\naudience: "engineers and technical buyers evaluating {scenes['kicker']}"\nangle: concept\nvoice: existing gated narration (content-ideas runs/2026-10-03-part-explainers/{a.part})\n---\n\nMechanism explainer for {scenes['kicker']}: the picture animates what the part does on the narration's words,\nmatching the DG32 fault-path film. Narration, captions and claims come from the gated part explainer;\nevery figure is from the product page and every animation is illustrative. Pre-silicon.\n""")
    # 2. audio + aligned word timings
    voices, frames_md, script_md = [], [], [f"# SCRIPT — {a.part}-mechanism\n"]
    S = scenes["scenes"]
    for i, s in enumerate(S, 1):
        v = voice[s["id"]]; wav = proj / "assets/voice" / f"{i:02d}.wav"
        sh("ffmpeg", "-v", "error", "-y", "-i", run / v["audio"], "-ac", "1", "-ar", "48000", wav)
        dur = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav).stdout)
        words = align(s["narration"], groq_words(wav, proj / "work" / f"{i:02d}.words.json"))
        voices.append({"frame": i, "path": f"assets/voice/{i:02d}.wav", "duration_s": round(dur, 3),
                       "words": [dict(id=f"w{i}-{k}", **w) for k, w in enumerate(words)]})
        text = re.sub(r"\s+", " ", re.sub(r"\[[^\]]+\]", " ", s["narration"])).strip()
        fid = f"{i:02d}-{s['id']}"
        frames_md.append(f"## Frame {i} — {s['label']}\n\n- scene: {spec.SCENES[s['id']]['scene']}\n- duration: {dur:.3f}s\n"
                         f"- transition_in: {'cut' if i == 1 else 'crossfade'}\n- status: animated\n- voiceover: {json.dumps(text)}\n"
                         f"- src: compositions/frames/{fid}.html\n- on_screen: {json.dumps(s['label'])}\n")
        script_md.append(f"## Line {i} — {s['label']} (Frame {i})\n\n    {text}\n")
    json.dump({"bgm": None, "bgm_pending": False, "voices": voices, "sfx": []}, open(proj / "audio_meta.json", "w"), indent=1)
    total = sum(v["duration_s"] for v in voices)
    (proj / "STORYBOARD.md").write_text(f"""---\nformat: 1920x1080\nduration: {total:.0f}s\nmessage: {json.dumps(scenes['headline'])}\narc: Problem → Mechanism → Proof → What is unproven\naudience: engineers evaluating {scenes['kicker']}\nmode: autonomous\nmusic: none\n---\n\n""" + "\n".join(frames_md))
    (proj / "SCRIPT.md").write_text("\n".join(script_md))
    # 3. frames: the spec over the primitives, cues resolved against each scene's own words
    for i, s in enumerate(S, 1):
        v = voices[i - 1]; dur = v["duration_s"]; ws = v["words"]
        at = lambda cue, ws=ws, dur=dur, sid=s["id"]: resolve(cue, ws, dur, f"{a.part} scene {sid}")
        sc = spec.SCENES[s["id"]]; p = f"f{i:02d}"
        body, css, tl = sc["build"](p, at)
        fdur = dur + (0.5 if i < len(S) else 0)
        html = lib.frame(f"{i:02d}-{s['id']}", p, sc.get("kicker", scenes["kicker"]), s["label"], body, css, tl).replace("__DUR__", f"{fdur:.3f}")
        (proj / "compositions/frames" / f"{i:02d}-{s['id']}.html").write_text(html)
    # 4. the workflow's own scripts, then the CLI gates
    sh("node", FE / "captions.mjs", "build", "--storyboard", "./STORYBOARD.md", "--audio-meta", "./audio_meta.json", "--hyperframes", ".", "--out", "./caption_groups.json", cwd=proj)
    # captions.mjs takes a light palette's ink and accents; on the dark ground they measured 1.27:1. The
    # fault-path film fixed the same three tokens by hand; here the build sets them and proves it did.
    cp = proj / "compositions/captions.html"; c = cp.read_text()
    for k, v in (("--cap-ink", "#eeeae2"), ("--cap-accent", "#d4a36e"), ("--cap-accent-2", "#3d453b")):
        c, n = re.subn(rf"{k}:\s*#[0-9a-fA-F]{{6}};", f"{k}: {v};", c)
        if n != 1: sys.exit(f"BLOCKED: caption token {k} found {n} times in captions.html")
    cp.write_text(c)
    sh("node", FE / "assemble-index.mjs", "--storyboard", "./STORYBOARD.md", "--hyperframes", ".", cwd=proj)
    sh("node", FE / "transitions.mjs", "inject", "--storyboard", "./STORYBOARD.md", "--hyperframes", ".", cwd=proj)
    sh("node", FE / "transitions.mjs", "verify", "--storyboard", "./STORYBOARD.md", "--index", "./index.html", cwd=proj)
    lint = sh("npx", "--yes", "hyperframes@0.8.31", "lint", cwd=proj, check=False)
    print(lint.stdout[-600:]); print(f"{a.part}: {len(S)} frames, {total:.1f} s -> {proj}")
    if a.render:
        sh("npx", "--yes", "hyperframes@0.8.31", "render", "--skill=faceless-explainer", "--quality", "high", "--output", "renders/video.mp4", cwd=proj)
        print("rendered", proj / "renders/video.mp4")


if __name__ == "__main__":
    main()
