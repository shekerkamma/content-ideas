#!/usr/bin/env python3
"""Narrate the demo clips embedded in a deck: synthesize, then mux.

Playwright's `recordVideo` captures VIDEO ONLY, so a captured simulator clip has
no audio stream at all. Muxing a silent `anullsrc` track afterwards makes that
look deliberate. Author narration instead and mux it in; a page's own audio is a
bonus, never the plan.

Voice routes, best first:
  * Gemini TTS on an AI Studio key -- `gemini-3.1-flash-tts-preview` (or
    `gemini-2.5-flash-preview-tts`), voice `Charon` for an informative, low-pitch
    register. Those return 24 kHz mono PCM in `inlineData`, wrapped here as WAV.
    `gemini-3.8-flash-tts` / `gemini-3.8-flash-lite-tts` return a finished
    `audio/wav` instead; wrapping that again nests one RIFF inside another (a
    header click at the start, and the wrong duration), so only raw PCM is wrapped.
    Send the TEXT ALONE: a style instruction in the prompt risks being spoken.
    On 3.8 put direction in `speech_metadata.style` instead -- see `--style`.
  * Designed voices (3.8): pass `--voice voice_<id>` from `POST /v1beta/voices`.
    They expire a year after creation.
  * Windows SAPI (`--engine sapi`) as an offline fallback -- free and
    deterministic, but a dated concatenative voice.
  * NOT OpenAI: `/v1/audio/speech` bills against API credits, and a ChatGPT
    subscription cannot be pointed at it. Codex CLI, the one subscription-auth
    route, exposes no audio surface at all.

Input is a markdown file of blocks:

    **<clip-name>** · <clip seconds> s · <any note>
    <narration text>

Dialogue mode (`--speakers Host=Puck,Guest=Charon`, 3.8 models only): one turn
per line, optional per-turn style in brackets, inline tags like [sigh] allowed:

    **<clip-name>** · <clip seconds> s
    Host (curious): So what does the DG32 actually do?
    Guest (dry, confident): [sigh] Thirty-two cores at the edge.

Every turn is sent as its own part carrying `speech_metadata.speaker`; a single
"Host: ... Guest: ..." text part is rejected by 3.8 with HTTP 400.

Usage:
  narrate_clips.py <narration.md> <clip-dir> <out-dir> [--engine gemini|sapi]
                   [--model M] [--voice V] [--style S] [--speakers A=v1,B=v2]
"""
from __future__ import annotations
import argparse, base64, io, json, os, re, subprocess, sys, urllib.error, urllib.request, wave

LEAD, TAIL = 1.2, 1.2          # seconds of silence before/after the narration
DUCK = 0.5                     # gain applied to a clip's own audio under narration
SR = 24000
TURN = re.compile(r"^\s*([A-Za-z][\w-]*)\s*(?:\(([^)]*)\))?\s*:\s*(.+)$")


def blocks(path: str) -> dict[str, str]:
    """Raw block text, line breaks kept (dialogue needs them)."""
    raw = open(path, encoding="utf8").read()
    return {m.group(1): m.group(3).strip()
            for m in re.finditer(r"\*\*(\S+)\*\* · ([\d.]+) s[^\n]*\n(.+?)(?=\n\n---|\Z)", raw, re.S)}


def turns(text: str, speakers: dict[str, str]) -> list[dict]:
    """Parse `Speaker (style): line` turns. Unmatched lines continue the previous turn."""
    out: list[dict] = []
    for line in text.splitlines():
        m = TURN.match(line)
        if m and m.group(1) in speakers:
            meta = {"speaker": m.group(1)}
            if m.group(2):
                meta["style"] = m.group(2).strip()
            out.append({"text": m.group(3).strip(), "speech_metadata": meta})
        elif line.strip() and out:
            out[-1]["text"] += " " + line.strip()
        elif line.strip():
            raise SystemExit(f"dialogue line has no known speaker {sorted(speakers)}: {line!r}")
    if not out:
        raise SystemExit("dialogue block contains no turns")
    return out


def to_wav(audio: bytes) -> bytes:
    """3.8 models return a finished WAV; older ones raw 24 kHz PCM. Wrap only PCM."""
    if audio.startswith(b"RIFF"):
        return audio
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(audio)
    return buf.getvalue()


def voice_config(voice: str) -> dict:
    # A designed/cloned voice id goes in `voice`; a stock name in prebuiltVoiceConfig.
    return {"voice": voice} if voice.startswith("voice_") else {"prebuiltVoiceConfig": {"voiceName": voice}}


def dur(path: str) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", path], capture_output=True, text=True).stdout)


def request_body(text: str, voice: str, style: str = "", speakers: dict[str, str] | None = None) -> dict:
    if speakers:
        parts = turns(text, speakers)
        speech = {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
            {"speaker": s, "voiceConfig": voice_config(v)} for s, v in speakers.items()]}}
    else:
        part: dict = {"text": " ".join(text.split())}
        if style:
            part["speech_metadata"] = {"style": style}
        parts = [part]
        speech = {"voiceConfig": voice_config(voice)}
    return {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": speech}}


def gemini(body: dict, out: str, model: str) -> None:
    key = os.environ["GOOGLE_GENERATIVE_AI_API_KEY"]
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{model}: HTTP {e.code}: {e.read()[:500].decode(errors='replace')}")
    parts = d["candidates"][0]["content"]["parts"]
    data = next(p["inlineData"]["data"] for p in parts if "inlineData" in p)
    with open(out, "wb") as f:
        f.write(to_wav(base64.b64decode(data)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("narration"); ap.add_argument("clip_dir"); ap.add_argument("out_dir")
    ap.add_argument("--engine", default="gemini", choices=["gemini", "sapi"])
    ap.add_argument("--model", default="gemini-3.1-flash-tts-preview")
    ap.add_argument("--voice", default="Charon", help="stock voice name, or a designed voice_<id>")
    ap.add_argument("--style", default="", help="delivery direction (3.8 speech_metadata.style)")
    ap.add_argument("--speakers", default="", help="dialogue mode: Host=Puck,Guest=Charon (3.8 only)")
    ap.add_argument("--own-audio", default="", help="comma-separated clips whose own audio to keep, ducked")
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    keep = {k for k in a.own_audio.split(",") if k}
    speakers = dict(kv.split("=", 1) for kv in a.speakers.split(",") if kv)
    # Measured 2026-09-29: 3.1 answers speech_metadata with 400 "not supported for this model".
    if (speakers or a.style) and "3.8" not in a.model:
        raise SystemExit(f"--speakers/--style need a gemini-3.8 TTS model (speech_metadata); got {a.model}")

    for name, text in blocks(a.narration).items():
        clip = os.path.join(a.clip_dir, f"{name}.mp4")
        wav = os.path.join(a.out_dir, f"{name}.wav")
        if a.engine == "gemini":
            gemini(request_body(text, a.voice, a.style, speakers), wav, a.model)
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
