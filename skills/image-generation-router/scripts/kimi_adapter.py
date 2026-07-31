#!/usr/bin/env python3
"""Kimi K3 helper for the image-generation router.

Kimi is a vision-language model with NO raster image generation. This adapter is
therefore NOT a provider route and never appears in any execution-path enum. It
supports exactly two helper roles around the real image routes:

- prompt refinement: tighten a text-free image spec before the built-in OpenAI
  or Gemini/CLIProxyAPI route renders it;
- vision review: a second-opinion read of an existing image (reference deck
  screenshot, generated asset QA). The host model remains the source of truth.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://api.kimi.com/coding/v1"
DEFAULT_CONFIG = "~/.config/kimi/.env"
PREFERRED_MODELS = ("moonshotai/kimi-k3-free", "kimi-k3-free", "k3")
HELPER_ROLES = ("prompt-refinement", "vision-review")

REFINE_SYSTEM_PROMPT = (
    "You refine specifications for text-free image generation. Rewrite the given "
    "image spec to be more precise about composition, lighting, palette, and style. "
    "Hard constraints you must keep and restate: absolutely no text, letters, "
    "numbers, logos, watermarks, or glyphs of any kind in the image; the image is "
    "illustrative only and never evidence. Output ONLY the refined prompt text."
)


class HelperError(RuntimeError):
    pass


def config_value(config_path: Path, name: str) -> str | None:
    try:
        text = config_path.expanduser().read_text(encoding="utf-8")
    except OSError:
        return None
    match = re.search(rf'^\s*{name}\s*=\s*["\']?([^"\'\s#]+)["\']?\s*$', text, re.MULTILINE)
    return match.group(1) if match else None


def api_key(config_path: Path) -> str:
    override = os.environ.get("KIMI_API_KEY")
    if override:
        return override
    value = config_value(config_path, "KIMI_API_KEY")
    if not value:
        raise HelperError(
            f"KIMI_API_KEY is not set and no KIMI_API_KEY entry was found in {config_path.expanduser()}. "
            "Set KIMI_API_KEY or add a KIMI_API_KEY=... line to the config file."
        )
    return value


def base_url(config_path: Path, flag_value: str | None) -> str:
    if flag_value:
        return flag_value
    return (
        os.environ.get("KIMI_BASE_URL")
        or config_value(config_path, "KIMI_BASE_URL")
        or DEFAULT_BASE_URL
    )


def request_json(url: str, key: str, *, payload: dict[str, Any] | None = None, timeout: int = 120) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {key}",
            **({"Content-Type": "application/json"} if payload is not None else {}),
        },
        method="POST" if payload is not None else "GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        try:
            detail: Any = json.loads(raw)
        except json.JSONDecodeError:
            detail = raw.decode("utf-8", errors="replace")
        if isinstance(detail, dict):
            detail = detail.get("error", detail)
            if isinstance(detail, dict):
                detail = detail.get("message", detail)
        raise HelperError(f"Kimi HTTP {exc.code}: {detail}") from exc
    except OSError as exc:
        raise HelperError(f"Cannot reach Kimi endpoint at {url}: {exc}") from exc
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HelperError("Kimi endpoint returned non-JSON data") from exc
    if not isinstance(value, dict):
        raise HelperError("Kimi endpoint returned an unsupported JSON shape")
    return value


def catalog_models(catalog: dict[str, Any]) -> list[str]:
    models = []
    for item in catalog.get("data", []):
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            models.append(item["id"])
    return sorted(set(models))


def select_model(available: list[str], requested: str | None) -> str:
    if requested:
        if available and requested not in available:
            choices = ", ".join(available)
            raise HelperError(f"Requested Kimi model '{requested}' is unavailable; live models: {choices}")
        return requested
    env_model = os.environ.get("KIMI_MODEL")
    if env_model:
        return select_model(available, env_model)
    for preferred in PREFERRED_MODELS:
        if preferred in available:
            return preferred
    if available:
        return available[0]
    raise HelperError("Kimi catalog lists no models")


def message_text(response: dict[str, Any]) -> str:
    choices = response.get("choices")
    if isinstance(choices, list) and choices:
        message = choices[0].get("message") if isinstance(choices[0], dict) else None
        if isinstance(message, dict):
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content.strip()
    raise HelperError("Kimi response contained no message content")


def image_data_uri(path: Path) -> str:
    resolved = path.expanduser()
    media_type = mimetypes.guess_type(resolved.name)[0]
    if media_type not in {"image/png", "image/jpeg", "image/webp", "image/gif"}:
        raise HelperError(f"Unsupported image type for vision review: {resolved}")
    try:
        data = resolved.read_bytes()
    except OSError as exc:
        raise HelperError(f"Cannot read image: {resolved}: {exc}") from exc
    return f"data:{media_type};base64,{base64.b64encode(data).decode('ascii')}"


def build_payload(role: str, model: str, prompt: str, image_uri: str | None) -> dict[str, Any]:
    if role == "prompt-refinement":
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": REFINE_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
    else:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_uri}},
                ],
            }
        ]
    return {"model": model, "messages": messages, "stream": False}


def write_sidecar(output: Path, *, role: str, resolved_model: str, prompt: str) -> Path:
    record = {
        "helper": "kimi",
        "role": role,
        "is_image_generation": False,
        "resolved_model": resolved_model,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "output_path": str(output),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    sidecar = Path(f"{output}.kimi.json")
    sidecar.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return sidecar


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = result.add_mutually_exclusive_group(required=True)
    mode.add_argument("--refine-prompt", action="store_true", help="refine a text-free image spec")
    mode.add_argument("--describe-image", action="store_true", help="vision second-opinion on an image")
    mode.add_argument("--list-models", action="store_true")
    mode.add_argument("--probe", action="store_true")
    result.add_argument("--prompt-file", type=Path)
    result.add_argument("--image", type=Path)
    result.add_argument("--out", type=Path)
    result.add_argument("--model")
    result.add_argument("--base-url", default=None, help="overrides KIMI_BASE_URL env / config entry")
    result.add_argument("--config", type=Path, default=Path(os.environ.get("KIMI_CONFIG", DEFAULT_CONFIG)))
    result.add_argument("--timeout", type=int, default=120)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        key = api_key(args.config)
        endpoint_base = base_url(args.config, args.base_url).rstrip("/")
        available = catalog_models(request_json(f"{endpoint_base}/models", key, timeout=args.timeout))
        if args.list_models:
            print("\n".join(available))
            return 0 if available else 1
        if args.probe:
            selected = select_model(available, args.model)
            print(f"Kimi helper ready; selected model: {selected}")
            return 0
        if not args.prompt_file or not args.out:
            raise HelperError("--prompt-file and --out are required")
        prompt = args.prompt_file.expanduser().read_text(encoding="utf-8").strip()
        if not prompt:
            raise HelperError("Prompt file is empty")
        role = "prompt-refinement" if args.refine_prompt else "vision-review"
        image_uri = None
        if role == "vision-review":
            if not args.image:
                raise HelperError("--image is required with --describe-image")
            image_uri = image_data_uri(args.image)
        selected = select_model(available, args.model)
        response = request_json(
            f"{endpoint_base}/chat/completions",
            key,
            payload=build_payload(role, selected, prompt, image_uri),
            timeout=args.timeout,
        )
        text = message_text(response)
        output = args.out.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
        sidecar = write_sidecar(output, role=role, resolved_model=selected, prompt=prompt)
        print(f"Wrote {output} ({role}, model {selected})")
        print(f"Sidecar {sidecar}")
        return 0
    except (OSError, HelperError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
