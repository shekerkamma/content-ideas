#!/usr/bin/env python3
"""Images 2.0 (`gpt-image-2`) called directly, with no mainline model in the path.

Third peer of codex_image.py (subscription, text-only) and codex_image_edit.py
(subscription, reference-conditioned). Same --prompt/--prompt-file/--out contract.

Why this route exists rather than always going through Codex:

  * NO PROMPT REVISION. The Codex/Responses path runs a mainline model that
    rewrites the prompt before rendering, which quietly defeats this skill's
    whole method ("never send a raw prompt — write a structured design spec").
    Here the spec reaches gpt-image-2 as written.
  * NO PLAN CAP. Billed per image against OPENAI_API_KEY, so it does not compete
    with Codex usage and does not stop at a subscription reset window.
  * TRUE REFERENCE EDITING. /v1/images/edits accepts the reference file itself.
    The note elsewhere in this skill that there is "no /images/edits endpoint"
    is scoped to the OmniRoute gateway, not to OpenAI direct.

It costs real money, unlike its two peers. Print the estimate first with
--dry-run; nothing is spent until you drop that flag.

  python3 openai_image.py --prompt-file spec.txt --out out/hero.png
  python3 openai_image.py --ref brand.png --prompt-file spec.txt --out out/v2.png

Stdlib only, per the repo runtime rule. The key is read from the environment and
never printed.
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

API = "https://api.openai.com/v1/images"
MAGIC = {b"\x89PNG": "png", b"\xff\xd8\xff": "jpeg", b"RIFF": "webp"}

# Rough per-image cost at 1024x1024, for the pre-spend estimate only. Larger
# canvases scale up roughly with pixel count; treat as an order of magnitude,
# not a quote.
COST = {"low": 0.006, "medium": 0.053, "high": 0.211, "auto": 0.053}

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from codex_image_edit import _provenance  # C2PA readback, shared with the peer
except ImportError:
    def _provenance(_p):
        return ""


def _is_image(p: Path) -> str | None:
    try:
        head = p.open("rb").read(4)
    except OSError:
        return None
    return next((k for sig, k in MAGIC.items() if head.startswith(sig)), None)


def _multipart(fields: dict[str, str], files: list[tuple[str, Path]]) -> tuple[bytes, str]:
    """Build a multipart/form-data body. urllib has no encoder of its own."""
    boundary = f"----codex{uuid.uuid4().hex}"
    sep = f"--{boundary}".encode()
    out = bytearray()
    for k, v in fields.items():
        out += sep + b"\r\n"
        out += f'Content-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, path in files:
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        out += sep + b"\r\n"
        out += (f'Content-Disposition: form-data; name="{k}"; filename="{path.name}"\r\n'
                f"Content-Type: {ctype}\r\n\r\n").encode()
        out += path.read_bytes() + b"\r\n"
    out += f"--{boundary}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={boundary}"


def _post(url: str, body: bytes, ctype: str, key: str, timeout: int) -> dict:
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        raise SystemExit(f"FAIL: HTTP {e.code} from {url}\n{detail}")
    except urllib.error.URLError as e:
        raise SystemExit(f"FAIL: cannot reach {url}: {e.reason}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt")
    g.add_argument("--prompt-file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--ref", action="append", metavar="FILE",
                    help="reference image; switches to /images/edits. Repeatable.")
    ap.add_argument("--model", default="gpt-image-2",
                    help="'chatgpt-image-latest' tracks the ChatGPT production version")
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--quality", default="medium", choices=sorted(COST))
    ap.add_argument("--n", type=int, default=1, help="multi-image consistency set")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--dry-run", action="store_true",
                    help="print the request and cost estimate; spend nothing")
    a = ap.parse_args()

    spec = Path(a.prompt_file).read_text(encoding="utf-8") if a.prompt_file else a.prompt
    out = Path(a.out).expanduser().resolve()
    refs = [Path(r).expanduser().resolve() for r in (a.ref or [])]
    for r in refs:
        if not r.is_file() or not _is_image(r):
            print(f"FAIL: reference missing or not an image: {r}", file=sys.stderr)
            return 2

    endpoint = "edits" if refs else "generations"
    est = COST[a.quality] * a.n
    print(f"route: /v1/images/{endpoint}  model={a.model}  size={a.size} "
          f"quality={a.quality} n={a.n}  refs={len(refs)}")
    print(f"estimated cost: ~${est:.3f} (1024^2 baseline; larger canvases cost more)")
    if a.dry_run:
        print("dry run — nothing sent.")
        return 0

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("FAIL: OPENAI_API_KEY is not set in this environment.", file=sys.stderr)
        return 2

    fields = {"model": a.model, "prompt": spec, "size": a.size,
              "quality": a.quality, "n": str(a.n)}
    if refs:
        # multiple references go as repeated image[] parts
        name = "image[]" if len(refs) > 1 else "image"
        body, ctype = _multipart(fields, [(name, r) for r in refs])
    else:
        body, ctype = json.dumps({**fields, "n": a.n}).encode(), "application/json"

    data = _post(f"{API}/{endpoint}", body, ctype, key, a.timeout)
    items = data.get("data") or []
    if not items:
        print(f"FAIL: no image in response: {json.dumps(data)[:400]}", file=sys.stderr)
        return 1

    out.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for i, item in enumerate(items):
        b64 = item.get("b64_json")
        if not b64:
            print(f"FAIL: response item {i} carries no b64_json.", file=sys.stderr)
            return 1
        target = out if i == 0 else out.with_name(f"{out.stem}-{i + 1}{out.suffix}")
        target.write_bytes(base64.b64decode(b64))
        written.append(target)

    for t in written:
        kind = _is_image(t)
        if not kind:
            print(f"FAIL: {t} is not a valid image.", file=sys.stderr)
            return 1
        prov = _provenance(t) or "unknown (no C2PA manifest)"
        print(f"OK {t} ({kind}, {t.stat().st_size} bytes) — rendered by: {prov}")
    if usage := data.get("usage"):
        print(f"   usage: {json.dumps(usage)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
