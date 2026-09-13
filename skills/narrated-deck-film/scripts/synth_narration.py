#!/usr/bin/env python3
"""Synthesise one audio file per slide from an AUTHORED narration corpus.

Reads narration from a JSON file on disk. It never derives narration from
extracted slide text -- see the skill's judgment rules for why.

Stdlib only. Resumable. Refuses to start a run it cannot finish.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

API = "https://api.elevenlabs.io/v1"
CREDIT_RATE = {
    "eleven_turbo_v2_5": 0.275, "eleven_flash_v2_5": 0.275,
    "eleven_turbo_v2": 0.275, "eleven_flash_v2": 0.275,
}
RETRYABLE = {429, 500, 502, 503, 504}


def _key():
    k = os.environ.get("ELEVENLABS_API_KEY")
    if not k:
        sys.exit(
            "BLOCKED: ELEVENLABS_API_KEY is not set.\n"
            "  export it in ~/.bashrc and mirror it into "
            ".claude/settings.local.json's env block.\n"
            "  Never hardcode it in a script."
        )
    return k


def _post(path, payload, key, timeout=180):
    req = urllib.request.Request(
        f"{API}{path}",
        data=json.dumps(payload).encode(),
        headers={"xi-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("request-id")


def _get(path, key):
    req = urllib.request.Request(f"{API}{path}", headers={"xi-api-key": key})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def budget(key):
    """Remaining characters on the account this billing cycle."""
    s = _get("/user/subscription", key)
    return s["character_limit"] - s["character_count"], s


def preflight(cfg, order, texts, key):
    """Fail before spending anything if the run cannot complete.

    The original pipeline discovered quota exhaustion at slide N with N-1
    slides already paid for and no usable film. Cost is checked up front.
    """
    chars = sum(len(texts[s]) for s in order if not _done(cfg, s))
    rate = CREDIT_RATE.get(cfg.get("model_id", "eleven_multilingual_v2"), 1.0)
    need = int(round(chars * rate))
    left, sub = budget(key)
    print(f"  tier={sub['tier']} used={sub['character_count']:,}/"
          f"{sub['character_limit']:,}  remaining={left:,}")
    print(f"  this run needs {chars:,} characters = {need:,} credits "
          f"at {rate}/char ({len([s for s in order if not _done(cfg,s)])} slides)")
    if need > left:
        sys.exit(
            f"BLOCKED: run needs {need:,} credits, account has {left:,}.\n"
            f"  Short by {need - left:,}. Nothing was spent.\n"
            f"  Options: wait for the cycle to reset, raise the plan, or split "
            f"the deck and render the parts across cycles."
        )
    return need


def _audio_path(cfg, slide):
    return os.path.join(cfg["audio_dir"], f"slide-{slide}.mp3")


def _done(cfg, slide):
    p = _audio_path(cfg, slide)
    return os.path.exists(p) and os.path.getsize(p) > 2000


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def synth(cfg, slide, text, key, prev_ids, prev_text, next_text):
    payload = {
        "text": text,
        "model_id": cfg.get("model_id", "eleven_multilingual_v2"),
        "voice_settings": cfg["voice_settings"],
    }
    # Request stitching: the model hears what came before and what follows, so
    # 13 separate calls land as one continuous read instead of 13 cold starts.
    if prev_ids:
        payload["previous_request_ids"] = prev_ids[-3:]
    if prev_text:
        payload["previous_text"] = prev_text[-400:]
    if next_text:
        payload["next_text"] = next_text[:400]

    url = (f"/text-to-speech/{cfg['voice_id']}"
           f"?output_format={cfg.get('output_format', 'mp3_44100_192')}")
    try:
        audio, rid = _post(url, payload, key)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:400]
        if e.code in RETRYABLE:
            raise RuntimeError(f"retryable {e.code}: {body}")
        # A 401/403/422 is a fault in the request or the credential. Retrying
        # it 8 times, as the original did, only hides it.
        sys.exit(f"BLOCKED: slide {slide} failed HTTP {e.code} (not retryable)\n  {body}")
    if len(audio) < 2000:
        sys.exit(f"BLOCKED: slide {slide} returned {len(audio)} bytes, not audio.")
    with open(_audio_path(cfg, slide), "wb") as f:
        f.write(audio)
    return rid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--dry-run", action="store_true",
                    help="preflight the budget and exit without spending")
    a = ap.parse_args()

    cfg = json.load(open(a.config))
    root = os.path.dirname(os.path.abspath(a.config))
    for k in ("audio_dir", "narration", "slides_dir", "work_dir"):
        if k in cfg and not os.path.isabs(cfg[k]):
            cfg[k] = os.path.join(root, cfg[k])
    os.makedirs(cfg["audio_dir"], exist_ok=True)

    texts = json.load(open(cfg["narration"]))
    order = [str(s) for s in cfg["slide_order"]]

    missing = [s for s in order if not texts.get(s, "").strip()]
    if missing:
        sys.exit(f"BLOCKED: no authored narration for slide(s) {missing} in "
                 f"{cfg['narration']}. Author it; do not fall back to slide text.")

    key = _key()
    print("== budget preflight ==")
    preflight(cfg, order, texts, key)
    if a.dry_run:
        print("dry run: nothing spent.")
        return

    print("\n== synthesising ==")
    prev_ids, spent = [], 0
    for i, s in enumerate(order):
        if _done(cfg, s):
            print(f"  slide {s:>3}  cached")
            continue
        prev_t = texts[order[i - 1]] if i else None
        next_t = texts[order[i + 1]] if i + 1 < len(order) else None
        rid = None
        for attempt in range(4):
            try:
                rid = synth(cfg, s, texts[s], key, prev_ids, prev_t, next_t)
                break
            except RuntimeError as e:
                if attempt == 3:
                    sys.exit(f"BLOCKED: slide {s} after 4 attempts: {e}")
                import time
                time.sleep(3 * (attempt + 1))
        if rid:
            prev_ids.append(rid)
        spent += len(texts[s])
        print(f"  slide {s:>3}  {duration(_audio_path(cfg, s)):6.2f}s  "
              f"{len(texts[s]):5d} chars")

    # The manifest is the single place durations are decided. Everything
    # downstream reads it; nothing downstream re-measures or hand-types a time.
    man = {"voice_id": cfg["voice_id"], "model_id": cfg.get("model_id"),
           "slides": []}
    for s in order:
        man["slides"].append({
            "slide": s,
            "audio": os.path.relpath(_audio_path(cfg, s), root),
            "duration": round(duration(_audio_path(cfg, s)), 3),
            "chars": len(texts[s]),
        })
    man["narration_seconds"] = round(sum(x["duration"] for x in man["slides"]), 2)
    mp = os.path.join(cfg["work_dir"], "narration-manifest.json")
    os.makedirs(cfg["work_dir"], exist_ok=True)
    json.dump(man, open(mp, "w"), indent=2)
    print(f"\nspent {spent:,} characters this run")
    print(f"narration total {man['narration_seconds']}s -> {mp}")


if __name__ == "__main__":
    main()
