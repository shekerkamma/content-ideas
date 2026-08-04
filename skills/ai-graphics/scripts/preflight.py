#!/usr/bin/env python3
"""ai-graphics preflight — verify the whole chain before doing any work.

Costs nothing: probes use intentionally-bogus models, so drivers answer with
errors (which proves them reachable) without generating an image.

Usage: python3 preflight.py [--skip-server]
Exit 0 = all critical checks pass.
"""
import json, os, subprocess, sys, time

BASE_URL = os.environ.get("OMNIROUTE_BASE_URL", "http://localhost:20128")
WIN_TEMP_WSL = os.environ.get("OMNIROUTE_WIN_TEMP", "/mnt/c/Users/sheke/AppData/Local/Temp")
WIN_TEMP_WIN = os.environ.get("OMNIROUTE_WIN_TEMP_WIN", r"C:\Users\sheke\AppData\Local\Temp")
PW_ROOT = os.environ.get("PLAYWRIGHT_ROOT", os.path.expanduser("~/content-ideas"))

results = []  # (name, ok, critical, note)


def check(name, ok, critical=True, note=""):
    results.append((name, ok, critical, note))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{' — ' + note if note else ''}")


def probe_provider(provider):
    """POST a bogus model; the error body tells us whether the driver exists."""
    tag = f"pf-{int(time.time())}-{provider}"
    body_wsl, body_win = f"{WIN_TEMP_WSL}/{tag}.json", f"{WIN_TEMP_WIN}\\{tag}.json"
    with open(body_wsl, "w") as f:
        json.dump({"model": f"{provider}/preflight-bogus-model", "prompt": "x", "n": 1}, f)
    ps = (
        f"try {{ Invoke-WebRequest -Method Post -Uri "
        f"'{BASE_URL}/api/v1/providers/{provider}/images/generations' "
        f"-ContentType 'application/json' -InFile '{body_win}' | Out-Null; 'HTTP200' }} "
        f"catch {{ $s = $_.Exception.Response.GetResponseStream(); "
        f"if ($s) {{ (New-Object IO.StreamReader($s)).ReadToEnd() }} else {{ 'NOCONN: ' + $_.Exception.Message }} }}"
    )
    try:
        r = subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps],
                           capture_output=True, text=True, timeout=90)
        out = (r.stdout or "").strip().splitlines()
        os.remove(body_wsl)
        return out[-1] if out else "EMPTY"
    except Exception as e:
        return f"NOCONN: {e}"


def main():
    skip_server = "--skip-server" in sys.argv
    print("ai-graphics preflight\n")

    # 1. Windows temp bridge
    try:
        p = f"{WIN_TEMP_WSL}/pf-write-test"
        open(p, "w").write("ok"); os.remove(p)
        check("Windows temp bridge writable", True, note=WIN_TEMP_WSL)
    except Exception as e:
        check("Windows temp bridge writable", False, note=str(e))

    # 2. Server + image route + per-provider drivers
    if not skip_server:
        resp = probe_provider("preflight-nonexistent")
        server_up = "Unknown image provider" in resp
        check("OmniRoute server + images route", server_up, note=BASE_URL if server_up else resp[:100])
        if server_up:
            for prov in ("codex", "nvidia", "comfyui"):
                r = probe_provider(prov)
                if "Unknown image provider" in r:
                    check(f"image driver: {prov}", False, critical=(prov != "comfyui"), note="no driver")
                elif r.startswith("NOCONN"):
                    check(f"image driver: {prov}", False, critical=(prov != "comfyui"), note=r[:80])
                else:
                    # any model-level/upstream error means the driver answered
                    note = "driver reachable"
                    if prov == "comfyui" and "fetch failed" in r:
                        note = "driver wired; local ComfyUI app not running"
                    check(f"image driver: {prov}", True, critical=(prov != "comfyui"), note=note)

    # 3. Playwright + chromium (Track A)
    pw_ok = os.path.exists(f"{PW_ROOT}/node_modules/playwright")
    check("playwright resolvable", pw_ok, note=PW_ROOT if pw_ok else f"not in {PW_ROOT} — set PLAYWRIGHT_ROOT")
    chrome = None
    cache = os.path.expanduser("~/.cache/ms-playwright")
    if os.path.isdir(cache):
        for d in sorted(os.listdir(cache), reverse=True):
            if d.startswith("chromium-"):
                for sub in ("chrome-linux64/chrome", "chrome-linux/chrome"):
                    p = f"{cache}/{d}/{sub}"
                    if os.path.exists(p):
                        chrome = p; break
            if chrome: break
    if not chrome:
        for p in ("/usr/bin/chromium-browser", "/usr/bin/chromium", "/snap/bin/chromium"):
            if os.path.exists(p):
                chrome = p; break
    check("chromium executable", bool(chrome), note=chrome or "none found — npx playwright install chromium")

    # 4. Pillow (canvas fitting)
    try:
        import PIL  # noqa: F401
        check("Pillow (canvas/pad)", True, critical=False, note=f"v{PIL.__version__}")
    except ImportError:
        check("Pillow (canvas/pad)", False, critical=False, note="pip install pillow — --canvas unavailable")

    crit_fails = [n for n, ok, crit, _ in results if not ok and crit]
    print(f"\n{'ALL CRITICAL CHECKS PASS' if not crit_fails else 'CRITICAL FAILURES: ' + ', '.join(crit_fails)}")
    print("(see troubleshoot.md for fixes)")
    return 1 if crit_fails else 0


if __name__ == "__main__":
    sys.exit(main())
