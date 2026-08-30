#!/usr/bin/env python3
"""Narrate the demo clips embedded in a deck: synthesize, then mux.

Playwright's `recordVideo` captures VIDEO ONLY, so a captured simulator clip has
no audio stream at all. Muxing a silent `anullsrc` track afterwards makes that
look deliberate. Author narration instead and mux it in; a page's own audio is a
bonus, never the plan.

Voice routes, best first:
  * Gemini TTS on an AI Studio key -- `gemini-3.1-flash-tts-preview` (or
    `gemini-2.5-flash-preview-tts`), voice `Charon` for an informative, low-pitch
    register. Returns 24 kHz mono PCM in `inlineData`; wrapped here as WAV.
    Send the TEXT ALONE: a style instruction in the prompt risks being spoken.
  * Windows SAPI (`--engine sapi`) as an offline fallback -- free and
    deterministic, but a dated concatenative voice.
  * NOT OpenAI: `/v1/audio/speech` bills against API credits, and a ChatGPT
    subscription cannot be pointed at it. Codex CLI, the one subscription-auth
    route, exposes no audio surface at all.

Input is a markdown file of blocks:

    **<clip-name>** · <clip seconds> s · <any note>
    <narration text>

Usage:
  narrate_clips.py <narration.md> <clip-dir> <out-dir> [--engine gemini|sapi]
"""
from __future__ import annotations
import argparse, base64, json, os, re, subprocess, sys, urllib.request, wave

LEAD, TAIL = 1.2, 1.2          # seconds of silence before/after the narration
DUCK = 0.5                     # gain applied to a clip's own audio under narration


def blocks(path: str) -> dict[str, str]:
    raw = open(path, encoding="utf8").read()
    return {m.group(1): " ".join(m.group(3).split())
            for m in re.finditer(r"\*\*(\S+)\*\* · ([\d.]+) s[^\n]*\n(.+?)(?=\n\n---|\Z)", raw, re.S)}


def dur(path: str) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", path], capture_output=True, text=True).stdout)


def gemini(text: str, out: str, model: str, voice: str) -> None:
    key = os.environ["GOOGLE_GENERATIVE_AI_API_KEY"]
    body = json.dumps({
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {"responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}},
    }).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
        data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("narration"); ap.add_argument("clip_dir"); ap.add_argument("out_dir")
    ap.add_argument("--engine", default="gemini", choices=["gemini", "sapi"])
    ap.add_argument("--model", default="gemini-3.1-flash-tts-preview")
    ap.add_argument("--voice", default="Charon")
    ap.add_argument("--own-audio", default="", help="comma-separated clips whose own audio to keep, ducked")
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    keep = {k for k in a.own_audio.split(",") if k}

    for name, text in blocks(a.narration).items():
        clip = os.path.join(a.clip_dir, f"{name}.mp4")
        wav = os.path.join(a.out_dir, f"{name}.wav")
        if a.engine == "gemini":
            gemini(text, wav, a.model, a.voice)
        else:
            raise SystemExit("sapi path is host-specific; see references for the PowerShell form")
        cd, sd = dur(clip), dur(wav)
        total = max(cd, LEAD + sd + TAIL)
        pad = max(0.0, total - cd)
        delay = int(LEAD * 1000)
        if name in keep:
            af = (f"[1:a]adelay={delay}|{delay},apad=whole_dur={total}[nar];"
                  f"[0:a]volume={DUCK},apad=whole_dur={total}[sim];"
                  f"[sim][nar]amix=inputs=2:duration=longest:dropout_transition=0,"
                  f"loudnorm=I=-17:TP=-1.5:LRA=11[a]")
        else:
            af = (f"[1:a]adelay={delay}|{delay},apad=whole_dur={total},"
                  f"loudnorm=I=-17:TP=-1.5:LRA=11[a]")
        # Hold the last frame rather than cutting the writing to fit the clip.
        vf = f"tpad=stop_mode=clone:stop_duration={pad:.2f}" if pad > 0.05 else "null"
        out = os.path.join(a.out_dir, f"{name}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", clip, "-i", wav,
                        "-filter_complex", f"[0:v]{vf}[v];{af}", "-map", "[v]", "-map", "[a]",
                        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
                        "-crf", "23", "-preset", "medium", "-r", "30",
                        "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
                        "-t", f"{total:.2f}", "-movflags", "+faststart", out], check=True)
        print(f"{name:10s} clip {cd:5.1f}s + narration {sd:5.1f}s -> {total:5.1f}s  {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
