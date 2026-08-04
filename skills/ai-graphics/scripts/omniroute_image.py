#!/usr/bin/env python3
"""Generate an image through the local OmniRoute server (Windows side) from WSL.

Handles the whole transport dance: body JSON -> Windows temp file ->
powershell.exe Invoke-RestMethod POST -> BOM-tolerant response parse ->
b64_json OR data:URL decode -> optional Pillow canvas fit -> output file.

Usage:
  python3 omniroute_image.py --provider codex --model codex/gpt-5.5 \
      --prompt-file spec.txt --size 1024x1536 --out /path/out.png \
      [--canvas 1080x1350] [--quality low]

Exit codes: 0 ok, 1 API/transport error, 2 bad args.
"""
import argparse, base64, json, os, struct, subprocess, sys, time

WIN_TEMP_WSL = os.environ.get("OMNIROUTE_WIN_TEMP", "/mnt/c/Users/sheke/AppData/Local/Temp")
WIN_TEMP_WIN = os.environ.get("OMNIROUTE_WIN_TEMP_WIN", r"C:\Users\sheke\AppData\Local\Temp")
BASE_URL = os.environ.get("OMNIROUTE_BASE_URL", "http://localhost:20128")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", required=True, help="image provider: codex | nvidia | comfyui")
    ap.add_argument("--model", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt")
    g.add_argument("--prompt-file")
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--quality", default=None, help="gpt-image only: low|medium|high")
    ap.add_argument("--out", required=True)
    ap.add_argument("--canvas", default=None,
                    help="WxH: scale to fit and pad with sampled background color (needs Pillow)")
    a = ap.parse_args()

    prompt = a.prompt if a.prompt else open(a.prompt_file).read()
    body = {"model": a.model, "prompt": prompt, "n": 1, "size": a.size}
    if a.quality:
        body["quality"] = a.quality

    tag = f"orimg-{int(time.time())}-{os.getpid()}"
    body_wsl = f"{WIN_TEMP_WSL}/{tag}-body.json"
    resp_wsl = f"{WIN_TEMP_WSL}/{tag}-resp.json"
    body_win = f"{WIN_TEMP_WIN}\\{tag}-body.json"
    resp_win = f"{WIN_TEMP_WIN}\\{tag}-resp.json"
    with open(body_wsl, "w") as f:
        json.dump(body, f)

    ps = (
        f"try {{ $r = Invoke-RestMethod -Method Post -Uri "
        f"'{BASE_URL}/api/v1/providers/{a.provider}/images/generations' "
        f"-ContentType 'application/json' -InFile '{body_win}'; "
        f"$r | ConvertTo-Json -Depth 6 -Compress | Set-Content -Encoding utf8 '{resp_win}'; 'OK' }} "
        f"catch {{ $s = $_.Exception.Response.GetResponseStream(); "
        f"if ($s) {{ (New-Object IO.StreamReader($s)).ReadToEnd() }} else {{ $_.Exception.Message }} }}"
    )
    r = subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps],
                       capture_output=True, text=True, timeout=600)
    tail = (r.stdout or "").strip().splitlines()
    status = tail[-1] if tail else ""
    if status != "OK":
        print(f"ERROR: {status or r.stderr.strip()}", file=sys.stderr)
        return 1

    resp = json.load(open(resp_wsl, encoding="utf-8-sig"))
    d = resp["data"][0]
    b64 = d.get("b64_json") or d.get("url", "").split(",", 1)[-1]
    raw = base64.b64decode(b64)

    if a.canvas:
        from PIL import Image
        import io
        cw, ch = (int(x) for x in a.canvas.lower().split("x"))
        src = Image.open(io.BytesIO(raw)).convert("RGB")
        scale = min(cw / src.width, ch / src.height)
        nw, nh = round(src.width * scale), round(src.height * scale)
        scaled = src.resize((nw, nh), Image.LANCZOS)
        bg = src.getpixel((min(5, src.width - 1), src.height // 2))
        canvas = Image.new("RGB", (cw, ch), bg)
        canvas.paste(scaled, ((cw - nw) // 2, (ch - nh) // 2))
        canvas.save(a.out)
        print(f"saved: {a.out} {cw}x{ch} (source {src.width}x{src.height}, padded bg={bg})")
    else:
        with open(a.out, "wb") as f:
            f.write(raw)
        dims = ""
        if raw[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", raw[16:24])
            dims = f" {w}x{h}"
        print(f"saved: {a.out}{dims} ({len(raw)} bytes)")
    if d.get("revised_prompt"):
        print(f"revised_prompt: {d['revised_prompt'][:200]}")
    for p in (body_wsl, resp_wsl):
        try: os.remove(p)
        except OSError: pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
