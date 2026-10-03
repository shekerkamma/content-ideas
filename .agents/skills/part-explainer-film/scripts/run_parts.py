#!/usr/bin/env python3
"""Voice, gate, render, build and verify explainers for many parts, each part isolated.

The worked batch from the ten-part run (2026-10-03), with what it taught built in:
- each part runs on its own and logs to <run>/<part>/log.txt; one failure never stops the others (the first
  batch's `exit` inside a brace group ended the whole loop at the first failing part);
- Kokoro gets up to two speed-tuning passes (its speed is non-linear; one pass overshot on two scenes);
- ElevenLabs is paid: one budget preflight across ALL parts before any character is spent, and a part whose
  voice gate fails is reported, never re-voiced automatically.

Each part folder must already hold a gated scenes.json and page-text.txt (SKILL.md steps 1-4).
Usage:
  run_parts.py --runs <dir> --provider kokoro|elevenlabs --svg-dir <dir> --ds <design-system> \\
      [--wordmark <png>] [--alias sku-4=dg32-lite] [--node <node>] part [part ...]
Re-voicing the nine placeholders in the Founder Voice after the ElevenLabs reset:
  ELEVENLABS_API_KEY=... run_parts.py --runs runs/2026-10-03-part-explainers --provider elevenlabs \\
      --svg-dir ~/deepgrid-dr-silicon-v6/public/diagrams --ds ~/deepgrid-dr-silicon-v6/design-system \\
      --alias sku-4=dg32-lite sku-1 sku-2 sku-4 sku-5 sku-6 sku-7 sku-8 sku-9 d100
then `python3 scripts/explainers/sync.py --skip-films` in the site repo.
"""
import argparse, json, os, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
SYNTH = HERE.parents[1] / "narrated-deck-film" / "scripts"


def sh(log, *cmd, cwd):
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, capture_output=True, text=True)
    log.write(f"$ {' '.join(map(str, cmd[:3]))} ...\n{r.stdout}{r.stderr}\n"); log.flush()
    return r.returncode


def clean(run):
    g = run / "voice-gate.json"
    return g.exists() and not json.load(open(g))["findings"]


def pace(log, run):
    for s in json.load(open(run / "scenes.json"))["scenes"]:
        sh(log, sys.executable, HERE / "extend_pauses.py", "scenes.json", "--scene", s["id"], cwd=run)


def budget_ok(runs, parts):
    sys.path.insert(0, str(SYNTH)); import synth_narration as sn
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key: sys.exit("BLOCKED: ELEVENLABS_API_KEY is not set; nothing was spent")
    need = sum(len(s["narration"]) for p in parts for s in json.load(open(runs / p / "scenes.json"))["scenes"])
    left, sub = sn.budget(key)
    print(f"ElevenLabs {sub['tier']}: {left:,} characters left; these {len(parts)} parts need {need:,}")
    if need > left: sys.exit(f"BLOCKED: short by {need - left:,} characters; nothing was spent. Split the parts across cycles.")


def part(a, name):
    run = a.runs / name; d = a.alias.get(name, name)
    log = open(run / "log.txt", "w")
    for f in ("scenes.json", "page-text.txt"):
        if not (run / f).exists(): return "BLOCKED", f"no {f}"
    if sh(log, sys.executable, HERE / "voice.py", "scenes.json", "--provider", a.provider, "--page-text", "page-text.txt", cwd=run):
        return "BLOCKED", "voicing failed (see log)"
    pace(log, run); sh(log, sys.executable, HERE / "measure_voice.py", "scenes.json", cwd=run)
    if a.provider == "kokoro":
        for _ in range(2):
            if clean(run): break
            sh(log, sys.executable, HERE / "tune_kokoro.py", "scenes.json", cwd=run)
            sh(log, sys.executable, HERE / "voice.py", "scenes.json", "--provider", "kokoro", "--page-text", "page-text.txt", cwd=run)
            pace(log, run); sh(log, sys.executable, HERE / "measure_voice.py", "scenes.json", cwd=run)
    if not clean(run):
        f = json.load(open(run / "voice-gate.json"))["findings"]
        return "VOICE NOT CLEAN", "; ".join(f)[:200] + ("  (paid: not re-voiced; fix the line, waive with a reason, or re-voice that scene)" if a.provider == "elevenlabs" else "")
    svg = a.svg_dir / f"{d}-architecture.svg"
    rf = [a.node, HERE / "render_frames.mjs", ".", "--svg", svg, "--ds", a.ds] + (["--wordmark", a.wordmark] if a.wordmark else [])
    if sh(log, *rf, cwd=run): return "BLOCKED", "render failed (see log)"
    if sh(log, sys.executable, HERE / "build_film.py", ".", "--out", f"{name}-explainer", cwd=run): return "BLOCKED", "build failed"
    if sh(log, sys.executable, HERE / "verify_film.py", ".", "--out", f"{name}-explainer", cwd=run): return "FINDINGS", "delivery gate (see log)"
    wpm = json.load(open(run / "voice-gate.json"))["film_wpm"]; dur = json.load(open(run / "out" / "film.json"))["duration"]
    return "DONE", f"{dur:.0f} s, {wpm} wpm"


def node20():
    """The PATH node on this machine is v18, which Playwright rejects; fall back to the newest nvm install."""
    def major(n):
        try: return int(subprocess.run([n, "--version"], capture_output=True, text=True).stdout.strip().lstrip("v").split(".")[0])
        except Exception: return 0
    cands = [shutil.which("node")] + sorted(map(str, pathlib.Path.home().glob(".nvm/versions/node/v*/bin/node")), key=lambda p: [int(x) for x in p.split("/v")[-1].split("/")[0].split(".")], reverse=True)
    for n in filter(None, cands):
        if major(n) >= 20: return n
    sys.exit("BLOCKED: no Node 20+ found for Playwright; pass --node")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("parts", nargs="+")
    ap.add_argument("--runs", type=pathlib.Path, required=True); ap.add_argument("--provider", choices=["kokoro", "elevenlabs"], required=True)
    ap.add_argument("--svg-dir", type=pathlib.Path, required=True); ap.add_argument("--ds", type=pathlib.Path, required=True)
    ap.add_argument("--wordmark", type=pathlib.Path); ap.add_argument("--alias", action="append", default=[])
    ap.add_argument("--node", default=None, help="Node 20+ (Playwright refuses older); default: PATH node if new enough, else the newest nvm node")
    a = ap.parse_args(); a.runs = a.runs.resolve(); a.alias = dict(x.split("=", 1) for x in a.alias)
    a.node = a.node or node20()
    if a.provider == "elevenlabs": budget_ok(a.runs, a.parts)
    rows = []
    for name in a.parts:
        try: rows.append((name, *part(a, name)))
        except Exception as e: rows.append((name, "BLOCKED", f"{type(e).__name__}: {e}"))
        print(f"{rows[-1][0]:>8}  {rows[-1][1]:<16} {rows[-1][2]}", flush=True)
    sys.exit(0 if all(r[1] == "DONE" for r in rows) else 2)


if __name__ == "__main__":
    main()
