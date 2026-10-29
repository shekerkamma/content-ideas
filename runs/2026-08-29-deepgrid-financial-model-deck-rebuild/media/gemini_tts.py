#!/usr/bin/env python3
"""Synthesize each clip's narration with Gemini TTS (AI Studio key).

Returns 24 kHz 16-bit mono PCM in inlineData; we wrap it as WAV. No style
prefix is sent: an instruction in the prompt risks being vocalised, and the
Charon voice is already the informative register we want.
"""
import base64, json, os, re, subprocess, sys, urllib.request, wave

KEY = os.environ["GOOGLE_GENERATIVE_AI_API_KEY"]
MODEL = os.environ.get("TTS_MODEL", "gemini-3.1-flash-tts-preview")
VOICE = os.environ.get("TTS_VOICE", "Charon")
OUT = sys.argv[2] if len(sys.argv) > 2 else "."

raw = open(sys.argv[1], encoding="utf8").read()
blocks = {m.group(1): " ".join(m.group(3).split())
          for m in re.finditer(r"\*\*(\w+)\*\* · ([\d.]+) s[^\n]*\n(.+?)(?=\n\n---|\Z)", raw, re.S)}

for k, text in blocks.items():
    body = json.dumps({
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}},
        },
    }).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}",
        data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    part = d["candidates"][0]["content"]["parts"][0]
    pcm = base64.b64decode(part["inlineData"]["data"])
    path = os.path.join(OUT, f"{k}.wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    print(f"{k:9s} {len(pcm)/2/24000:6.1f}s  {len(text.split()):4d} words -> {path}")
