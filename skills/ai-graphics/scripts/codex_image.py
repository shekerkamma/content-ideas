#!/usr/bin/env python3
"""Render an image with the Codex CLI's built-in image_gen tool.

Gateway-independent: talks to the local `codex` binary on ChatGPT-subscription
auth, so it works when OmniRoute / CLIProxyAPI are down. Peer of
omniroute_image.py, same --prompt/--prompt-file/--out contract.

  python3 codex_image.py --model gpt-5.6-sol \
    --prompt-file spec.txt --out out/card.png [--size 1024x1536]

Model ids are validated server-side: a wrong id fails with HTTP 400
"not supported when using Codex with a ChatGPT account". Note the shipping id
carries the -sol suffix; bare `gpt-5.6` is NOT accepted.
"""
import argparse, os, shutil, subprocess, sys, time
from pathlib import Path

GEN_DIR = Path.home() / ".codex" / "generated_images"
MAGIC = {b"\x89PNG": "png", b"\xff\xd8\xff": "jpeg"}


def _is_image(p: Path) -> str | None:
    try:
        head = p.open("rb").read(4)
    except OSError:
        return None
    for sig, kind in MAGIC.items():
        if head.startswith(sig):
            return kind
    return None


def _newest_generated(after: float) -> Path | None:
    if not GEN_DIR.is_dir():
        return None
    cands = [p for p in GEN_DIR.rglob("*")
             if p.is_file() and p.stat().st_mtime >= after and _is_image(p)]
    return max(cands, key=lambda p: p.stat().st_mtime, default=None)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gpt-5.6-sol")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt")
    g.add_argument("--prompt-file")
    ap.add_argument("--size", default=None, help="hint only, e.g. 1024x1536")
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=int, default=600)
    a = ap.parse_args()

    spec = Path(a.prompt_file).read_text() if a.prompt_file else a.prompt
    out = Path(a.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    size = f" Target size {a.size}." if a.size else ""
    task = (
        f"Use your built-in image generation tool to render this specification "
        f"verbatim.{size} Save the result to exactly this path: {out}\n"
        f"Do not summarise, critique, or alter the spec. Render it.\n\n"
        f"--- SPEC ---\n{spec}"
    )

    started = time.time() - 2
    proc = subprocess.run(
        ["codex", "exec", "-m", a.model, "--skip-git-repo-check", task],
        cwd=out.parent, capture_output=True, text=True, timeout=a.timeout,
        stdin=subprocess.DEVNULL,   # codex exec reads stdin when not a TTY and will hang
    )
    tail = (proc.stdout or "")[-800:] + (proc.stderr or "")[-800:]
    if "not supported when using Codex" in tail:
        print(f"FAIL: model '{a.model}' rejected by Codex.\n{tail}", file=sys.stderr)
        return 2

    # codex may write to --out directly, or park it under ~/.codex/generated_images
    if not (out.exists() and _is_image(out)):
        found = _newest_generated(started)
        if found:
            shutil.copy2(found, out)
        else:
            print(f"FAIL: no image produced.\n{tail}", file=sys.stderr)
            return 1

    kind = _is_image(out)
    if not kind:
        print(f"FAIL: {out} is not a valid image.", file=sys.stderr)
        return 1
    print(f"OK {out} ({kind}, {out.stat().st_size} bytes) via {a.model}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
