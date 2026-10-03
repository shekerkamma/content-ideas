#!/usr/bin/env python3
"""Voice every scene of a gated script. Two providers, one output contract.

  elevenlabs  the Founder Voice on eleven_v3 (the measured decision, references/voice.md). Delegates to
              narrated-deck-film/scripts/synth_narration.py: budget preflight, resume, fail-fast on 4xx.
              Needs ELEVENLABS_API_KEY in the environment.
  kokoro      the free local placeholder (bm_george, Holt profile). Emotion tags are stripped, because
              Kokoro would read them aloud. Delegates to use-case-film/scripts/tts_beats.py.

Writes <run>/audio/<scene>.{mp3,wav} and <run>/voice.json: [{scene, audio, duration}], the one place
scene durations are decided. Usage: voice.py scenes.json --provider elevenlabs|kokoro --page-text page.txt [--dry-run]
"""
import argparse, json, os, pathlib, subprocess, sys
from spoken import strip_tags

HERE = pathlib.Path(__file__).resolve().parent
SKILLS = HERE.parent.parent
VOICE = {"voice_id": "xqmZGpVMlMzAiUYMY0NQ", "model_id": "eleven_v3",
         "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}}   # take D, 2026-10-03

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("scenes")
    ap.add_argument("--provider", choices=["elevenlabs", "kokoro"], required=True); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--page-text", help="product page text, passed to the script gate")
    a = ap.parse_args()
    run = pathlib.Path(a.scenes).resolve().parent; audio = run / "audio"; audio.mkdir(exist_ok=True)
    doc = json.load(open(a.scenes)); sc = doc["scenes"]
    # Pronunciation lexicon: what the TTS hears, never what the captions show ("DG32-LITE" -> "D G 32 Light").
    lex = doc.get("pronounce", {})
    def say(t):
        for k, v in lex.items(): t = t.replace(k, v)
        return t
    gcmd = [sys.executable, str(HERE / "gate_script.py"), a.scenes] + (["--page-text", a.page_text] if a.page_text else [])
    gate = subprocess.run(gcmd, capture_output=True, text=True)
    if gate.returncode:
        print(gate.stdout, gate.stderr); sys.exit("BLOCKED: the script gate is not clean; fix the writing before spending voice.")
    ids = [s["id"] for s in sc]
    if a.provider == "elevenlabs":
        work = run / "work"; work.mkdir(exist_ok=True)
        json.dump({s["id"]: say(s["narration"]) for s in sc}, open(work / "narration.json", "w"), indent=1, ensure_ascii=False)
        cfg = dict(VOICE, narration="narration.json", slide_order=ids, audio_dir=str(audio / "el"), work_dir=".",
                   output_format="mp3_44100_192")
        json.dump(cfg, open(work / "synth.json", "w"), indent=1)
        cmd = [sys.executable, str(SKILLS / "narrated-deck-film/scripts/synth_narration.py"), str(work / "synth.json")]
        if a.dry_run: cmd.append("--dry-run")
        if subprocess.run(cmd).returncode: sys.exit("BLOCKED: synth_narration failed (see above)")
        if a.dry_run: return
        files = {i: audio / "el" / f"slide-{i}.mp3" for i in ids}
    else:
        beats = [{"id": s["id"], "vo": strip_tags(say(s["narration"])), "speed": s.get("kokoro_speed", 1.0)} for s in sc]
        bj = run / "work" / "kokoro-beats.json"; bj.parent.mkdir(exist_ok=True); json.dump(beats, open(bj, "w"), indent=1)
        if a.dry_run: print(f"{len(beats)} scenes would be voiced locally; free"); return
        py = os.path.expanduser("~/.venvs/kokoro/bin/python")
        if subprocess.run([py, str(SKILLS / "use-case-film/scripts/tts_beats.py"), str(bj), str(audio / "kokoro")]).returncode:
            sys.exit("BLOCKED: Kokoro failed (see above)")
        files = {i: audio / "kokoro" / f"{i}.wav" for i in ids}
    man = [{"scene": i, "audio": str(files[i].relative_to(run)), "duration": round(dur(files[i]), 3)} for i in ids]
    json.dump({"provider": a.provider, **({"voice": VOICE} if a.provider == "elevenlabs" else {"voice": "kokoro bm_george"}),
               "scenes": man}, open(run / "voice.json", "w"), indent=1)
    print(f"{len(man)} scenes, {sum(m['duration'] for m in man):.1f} s of narration -> {run/'voice.json'}")

if __name__ == "__main__":
    main()
