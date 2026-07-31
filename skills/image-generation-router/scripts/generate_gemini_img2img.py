#!/usr/bin/env python3
"""Image-conditioned generation through the local CLIProxyAPI Gemini route.

Companion to generate_gemini.py: reuses its auth/model-selection/response-parsing,
adds a reference image as an OpenAI-compatible vision `image_url` content part.
Neither generate_gemini.py nor OmniRoute's omniroute_image.py accept a reference
image (both are text-prompt-only) — this is the only image-conditioned path in
this repo's image tooling. Verified working against gemini-3.1-flash-image, 2026-07-23.

Always instruct the model explicitly to omit every word/label/number visible in
the reference — text-heavy references (data-labeled diagrams) still come out
clean with a strongly worded "ignore all text" instruction in the prompt.
"""
import argparse
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_gemini as G


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True, type=Path, help="Reference image to condition on")
    parser.add_argument("--prompt-file", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--model")
    parser.add_argument("--base-url", default=None, help="Defaults to generate_gemini's DEFAULT_BASE_URL / CLIPROXYAPI_BASE_URL env")
    parser.add_argument("--config", type=Path, default=Path("~/cliproxyapi/config.yaml"))
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    try:
        key = G.client_key(args.config)
        base_url = (args.base_url or G.DEFAULT_BASE_URL).rstrip("/")
        available = G.image_models(G.request_json(f"{base_url}{G.DISCOVERY_ENDPOINT}", key, timeout=args.timeout))
        selected = G.select_model(available, args.model)
        print(f"model: {selected}")

        ref_b64 = base64.b64encode(args.ref.read_bytes()).decode("ascii")
        prompt = args.prompt_file.read_text(encoding="utf-8").strip()
        if not prompt:
            raise G.RouterError("Prompt file is empty")

        payload = {
            "model": selected,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{ref_b64}"}},
                ],
            }],
            "stream": False,
        }
        response = G.request_json(f"{base_url}{G.GENERATION_ENDPOINT}", key, payload=payload, timeout=args.timeout)
        media_type, data = G.extract_data_image(response)
        out = G.save_image(data, media_type, args.out)
        print(f"saved: {out}")
        return 0
    except G.RouterError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
