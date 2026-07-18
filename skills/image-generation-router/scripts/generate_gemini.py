#!/usr/bin/env python3
"""Generate an image through a local CLIProxyAPI Gemini route."""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
from datetime import datetime, timezone
from typing import Any, Iterable
import urllib.error
import urllib.request


SKILL_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = SKILL_ROOT / "contracts" / "image-generation-routing-contract.json"


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot load image-generation routing contract: {path}: {exc}") from exc
    return value


ROUTING_CONTRACT = load_contract()
GEMINI_CONTRACT = ROUTING_CONTRACT["providers"]["cliproxyapi-gemini"]
DEFAULT_BASE_URL = GEMINI_CONTRACT["base_url_default"]
DEFAULT_MODEL_ORDER = tuple(GEMINI_CONTRACT["preferred_models"])
DISCOVERY_ENDPOINT = GEMINI_CONTRACT["discovery_endpoint"]
GENERATION_ENDPOINT = GEMINI_CONTRACT["generation_endpoint"]
IMAGE_MODEL_MATCH = GEMINI_CONTRACT["image_model_match"].lower()


class RouterError(RuntimeError):
    pass


def client_key(config_path: Path) -> str:
    override = os.environ.get("CLIPROXYAPI_KEY")
    if override:
        return override
    try:
        text = config_path.expanduser().read_text(encoding="utf-8")
    except OSError as exc:
        raise RouterError(f"Cannot read CLIProxyAPI config: {config_path.expanduser()}: {exc}") from exc
    match = re.search(r'^\s+-\s+["\']?([^"\'\s#]+)["\']?\s*$', text, re.MULTILINE)
    if not match:
        raise RouterError(f"No client API key found in {config_path.expanduser()}")
    return match.group(1)


def request_json(
    url: str,
    key: str,
    *,
    payload: dict[str, Any] | None = None,
    timeout: int = 180,
) -> dict[str, Any]:
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
            error = json.loads(raw)
        except json.JSONDecodeError:
            error = raw.decode("utf-8", errors="replace")
        if isinstance(error, dict):
            detail = error.get("error", error)
            if isinstance(detail, dict):
                detail = detail.get("message", detail)
        else:
            detail = error
        raise RouterError(f"CLIProxyAPI HTTP {exc.code}: {detail}") from exc
    except OSError as exc:
        raise RouterError(f"Cannot reach CLIProxyAPI at {url}: {exc}") from exc
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RouterError("CLIProxyAPI returned non-JSON data") from exc
    if not isinstance(value, dict):
        raise RouterError("CLIProxyAPI returned an unsupported JSON shape")
    return value


def image_models(catalog: dict[str, Any]) -> list[str]:
    models = []
    for item in catalog.get("data", []):
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            model = item["id"]
            if IMAGE_MODEL_MATCH in model.lower():
                models.append(model)
    return sorted(set(models))


def select_model(available: list[str], requested: str | None) -> str:
    if requested:
        if requested not in available:
            choices = ", ".join(available) if available else "none"
            raise RouterError(f"Requested image model '{requested}' is unavailable; live image models: {choices}")
        return requested
    env_model = os.environ.get("CLIPROXYAPI_IMAGE_MODEL")
    if env_model:
        return select_model(available, env_model)
    for preferred in DEFAULT_MODEL_ORDER:
        if preferred in available:
            return preferred
    if available:
        return available[0]
    raise RouterError("CLIProxyAPI reports no image-capable models")


def all_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from all_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from all_strings(item)


def extract_data_image(response: dict[str, Any]) -> tuple[str, bytes]:
    pattern = re.compile(r"data:(image/(?:png|jpeg|webp));base64,([A-Za-z0-9+/=]+)")
    for value in all_strings(response):
        match = pattern.search(value)
        if match:
            try:
                return match.group(1), base64.b64decode(match.group(2), validate=True)
            except ValueError as exc:
                raise RouterError("CLIProxyAPI returned invalid base64 image data") from exc
    raise RouterError("CLIProxyAPI succeeded but returned no supported data image")


def save_image(data: bytes, media_type: str, output: Path) -> Path:
    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    suffix = output.suffix.lower()
    native = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}[media_type]
    if suffix in {native, ".jpeg" if native == ".jpg" else native}:
        output.write_bytes(data)
        return output
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        try:
            from PIL import Image
        except ImportError as exc:
            raise RouterError(
                f"Response is {media_type}, but output requests {suffix}; install Pillow or use {native}"
            ) from exc
        with Image.open(io.BytesIO(data)) as image:
            target_format = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG", ".webp": "WEBP"}[suffix]
            if target_format == "JPEG" and image.mode not in {"RGB", "L"}:
                image = image.convert("RGB")
            image.save(output, format=target_format)
        return output
    actual = output.with_suffix(native)
    actual.write_bytes(data)
    return actual


def write_provenance(
    output: Path,
    *,
    prompt: str,
    requested_model: str | None,
    resolved_model: str,
    source_media_type: str,
) -> Path:
    output_media_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(output.suffix.lower(), source_media_type)
    record = {
        "execution_path": "cliproxyapi-gemini",
        "provider": "gemini",
        "requested_model": requested_model,
        "resolved_model": resolved_model,
        "auth_mode": "local-client-key-plus-provider-oauth",
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "output_path": str(output),
        "source_media_type": source_media_type,
        "output_media_type": output_media_type,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    sidecar = Path(f"{output}.provenance.json")
    sidecar.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return sidecar


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--prompt-file", type=Path)
    result.add_argument("--out", type=Path)
    result.add_argument("--model")
    result.add_argument("--base-url", default=os.environ.get("CLIPROXYAPI_BASE_URL", DEFAULT_BASE_URL))
    result.add_argument(
        "--config",
        type=Path,
        default=Path(os.environ.get("CLIPROXYAPI_CONFIG", "~/cliproxyapi/config.yaml")),
    )
    result.add_argument("--timeout", type=int, default=180)
    result.add_argument("--list-models", action="store_true")
    result.add_argument("--probe", action="store_true")
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        key = client_key(args.config)
        base_url = args.base_url.rstrip("/")
        available = image_models(request_json(f"{base_url}{DISCOVERY_ENDPOINT}", key, timeout=args.timeout))
        if args.list_models:
            print("\n".join(available))
            return 0 if available else 1
        if args.probe:
            selected = select_model(available, args.model)
            print(f"CLIProxyAPI ready; selected image model: {selected}")
            return 0
        if not args.prompt_file or not args.out:
            raise RouterError("--prompt-file and --out are required for generation")
        prompt = args.prompt_file.expanduser().read_text(encoding="utf-8").strip()
        if not prompt:
            raise RouterError("Prompt file is empty")
        selected = select_model(available, args.model)
        response = request_json(
            f"{base_url}{GENERATION_ENDPOINT}",
            key,
            payload={
                "model": selected,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=args.timeout,
        )
        media_type, data = extract_data_image(response)
        output = save_image(data, media_type, args.out)
        sidecar = write_provenance(
            output,
            prompt=prompt,
            requested_model=args.model,
            resolved_model=selected,
            source_media_type=media_type,
        )
        print(f"Generated {output} with {selected}")
        print(f"Provenance {sidecar}")
        return 0
    except (OSError, RouterError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
