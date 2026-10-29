import base64, json, os, re, sys, urllib.request, wave
KEY=os.environ["GOOGLE_GENERATIVE_AI_API_KEY"]
MODEL="gemini-3.1-flash-tts-preview"; VOICE="Charon"
raw=open('narration/clip-narration.md',encoding='utf8').read()
blocks={m.group(1):" ".join(m.group(3).split())
        for m in re.finditer(r"\*\*(\w+)\*\* · ([\d.]+) s[^\n]*\n(.+?)(?=\n\n---|\Z)",raw,re.S)}
for k in sys.argv[1:]:
    body=json.dumps({"contents":[{"parts":[{"text":blocks[k]}]}],
      "generationConfig":{"responseModalities":["AUDIO"],
        "speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":VOICE}}}}}).encode()
    req=urllib.request.Request(
      f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}",
      data=body,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=300) as r: d=json.load(r)
    pcm=base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
    p=f'narration/gemini/{k}.wav'
    with wave.open(p,'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    print(f'{k:8s} {len(pcm)/2/24000:5.1f}s -> {p}')
