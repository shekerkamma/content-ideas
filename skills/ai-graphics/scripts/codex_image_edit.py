#!/usr/bin/env python3
"""Reference-conditioned image generation with Images 2.0 on the ChatGPT subscription.

Peer of codex_image.py (text-only) — same --prompt/--prompt-file/--out contract,
plus one or more --ref images the model conditions on. Talks to the local `codex`
binary, so auth is the signed-in ChatGPT/Codex subscription and no API key is held
or billed.

  python3 codex_image_edit.py --ref brand-hero.png \
    --prompt-file spec.txt --out out/hero-variant.png [--mode style] [--size 1024x1536]

Two mechanics are load-bearing and non-obvious:

  * `-i/--image` is VARIADIC, so a trailing positional prompt is swallowed as a
    filename. The prompt therefore goes over stdin with the `-` sentinel, which is
    also the codex-bridge pattern that closes stdin as a side effect (an argv
    prompt on an inherited stdin hangs for the full timeout with no output).
  * The built-in tool parks its artifact in $CODEX_HOME/generated_images/ rather
    than honoring a save path, so retrieval takes the freshest file postdating
    this run instead of trusting the model to write --out.

Verification (2026-09-08): PARTIAL — argument plumbing and provenance decoding are
executed and passing; reference conditioning is NOT YET EXECUTED. The subscription
quota was exhausted before any render completed ("You've hit your usage limit ...
try again at 9:20 AM"), so the claim that Images 2.0 honors an attached reference
is a hypothesis here, not a result. Re-run the paired test in
scripts/../tests/ (edit-with-ref vs no-ref control) after a quota reset and replace
this note with the outcome. Treat --mode style/variation as unproven until then.

Provenance is read back from the C2PA manifest and printed, so the run reports the
model that actually rendered rather than the one we assumed.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

GEN_DIR = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "generated_images"
MAGIC = {b"\x89PNG": "png", b"\xff\xd8\xff": "jpeg", b"RIFF": "webp"}
MTIME_SKEW = 2.0  # tolerate mtime granularity / clock skew

MODES = {
    "edit": (
        "Edit the attached reference image according to the specification below. "
        "Preserve everything the specification does not ask you to change: subject "
        "identity, composition, lighting, and palette must carry over."
    ),
    "style": (
        "Use the attached reference image(s) as STYLE and ART-DIRECTION reference. "
        "Render the new subject described below so it reads as belonging to the same "
        "brand and visual world: same palette, lighting, texture, and finish. Do not "
        "copy the reference's subject or composition."
    ),
    "variation": (
        "Produce a new variation consistent with the attached reference image(s). "
        "Keep the subject and brand identity recognizably the same; vary only what "
        "the specification below asks to vary."
    ),
}


def _is_image(p: Path) -> str | None:
    try:
        head = p.open("rb").read(4)
    except OSError:
        return None
    return next((k for sig, k in MAGIC.items() if head.startswith(sig)), None)


def _newest_generated(after: float) -> Path | None:
    if not GEN_DIR.is_dir():
        return None
    floor = after - MTIME_SKEW
    cands = [
        p for p in GEN_DIR.rglob("*")
        if p.is_file() and p.stat().st_mtime >= floor and _is_image(p)
    ]
    return max(cands, key=lambda p: p.stat().st_mtime, default=None)


def _cbor_text(blob: bytes, pos: int) -> tuple[str, int]:
    """Decode a CBOR definite-length text string at `pos` -> (value, next_pos).

    Major type 3: 0x60|n encodes the byte length inline for n < 24, then 0x78
    takes a following 1-byte length. Anything else here is not a short string.
    """
    if pos >= len(blob):
        return "", pos
    b = blob[pos]
    if 0x60 <= b < 0x78:
        n, start = b - 0x60, pos + 1
    elif b == 0x78:
        n, start = blob[pos + 1], pos + 2
    else:
        return "", pos
    return blob[start:start + n].decode("utf-8", "replace"), start + n


def _provenance(p: Path) -> str:
    """Model name/version from the C2PA manifest, or '' when absent.

    The manifest is CBOR inside a JUMBF box. Rather than pull a C2PA parser (the
    repo is stdlib-only at runtime), locate the softwareAgent keys and decode the
    two text strings that follow them.
    """
    try:
        blob = p.read_bytes()
    except OSError:
        return ""
    i = blob.find(b"softwareAgent")
    if i < 0:
        return ""
    j = blob.find(b"dname", i)
    if j < 0:
        return ""
    name, nxt = _cbor_text(blob, j + 5)
    if not name:
        return ""
    k = blob.find(b"gversion", nxt)
    ver = _cbor_text(blob, k + 8)[0] if 0 <= k <= nxt + 4 else ""
    return f"{name} {ver}".strip()


def _image_flag() -> str:
    """Feature name for the built-in tool: renamed at Codex CLI ~0.145."""
    try:
        feats = subprocess.run(
            ["codex", "features", "list"], capture_output=True, text=True, timeout=15
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return "image_generation"
    return "image_generation" if "image_generation" in feats else "imagegenext"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ref", action="append", required=True, metavar="FILE",
                    help="reference image; repeat for multi-image consistency")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt")
    g.add_argument("--prompt-file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", choices=sorted(MODES), default="edit")
    ap.add_argument("--model", default="gpt-5.6-sol",
                    help="mainline model hosting the image tool (not the image model)")
    ap.add_argument("--size", default=None, help="e.g. 1024x1536; passed as a directive")
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()

    refs = [Path(r).expanduser().resolve() for r in a.ref]
    for r in refs:
        if not r.is_file():
            print(f"FAIL: reference not found: {r}", file=sys.stderr)
            return 2
        if not _is_image(r):
            print(f"FAIL: reference is not a PNG/JPEG/WebP: {r}", file=sys.stderr)
            return 2

    spec = Path(a.prompt_file).read_text(encoding="utf-8") if a.prompt_file else a.prompt
    out = Path(a.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    size = f" Target size {a.size}." if a.size else ""
    task = (
        f"{MODES[a.mode]}{size}\n"
        f"Use your built-in image generation tool. Render the specification verbatim; "
        f"do not summarise, critique, or negotiate it. Save the result to exactly this "
        f"path: {out}\n\n--- SPECIFICATION ---\n{spec}"
    )

    cmd = ["codex", "exec", "-m", a.model, "--skip-git-repo-check",
           "--enable", _image_flag()]
    for r in refs:
        cmd += ["-i", str(r)]
    cmd.append("-")  # prompt arrives on stdin; keeps it clear of variadic -i

    started = time.time()
    try:
        proc = subprocess.run(cmd, input=task, cwd=out.parent, capture_output=True,
                              text=True, timeout=a.timeout)
    except subprocess.TimeoutExpired:
        print(f"FAIL: codex exec exceeded {a.timeout}s.", file=sys.stderr)
        return 1

    tail = (proc.stdout or "")[-1000:] + (proc.stderr or "")[-1000:]
    if "not supported when using Codex" in tail:
        print(f"FAIL: model '{a.model}' rejected by Codex.\n{tail}", file=sys.stderr)
        return 2

    if not (out.exists() and _is_image(out)):
        found = _newest_generated(started)
        if not found:
            print(f"FAIL: no image produced.\n{tail}", file=sys.stderr)
            return 1
        shutil.copy2(found, out)

    kind = _is_image(out)
    if not kind:
        print(f"FAIL: {out} is not a valid image.", file=sys.stderr)
        return 1

    prov = _provenance(out) or "unknown (no C2PA manifest)"
    print(f"OK {out} ({kind}, {out.stat().st_size} bytes)")
    print(f"   rendered by: {prov}   |   refs: {len(refs)}   mode: {a.mode}   host: {a.model}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
