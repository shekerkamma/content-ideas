#!/usr/bin/env python3
"""Bridge Claude Code to Codex's subscription-backed built-in image generation."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image


def inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-file", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--workdir", required=True, type=Path)
    parser.add_argument("--model", default=os.environ.get("CODEX_IMAGE_ORCHESTRATION_MODEL", "gpt-5.6-sol"))
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    codex = shutil.which("codex")
    if not codex:
        raise SystemExit("codex CLI is not installed or not on PATH")

    workdir = args.workdir.resolve()
    prompt_file = args.prompt_file.resolve()
    out = args.out.resolve()
    if not prompt_file.is_file():
        raise SystemExit(f"prompt file not found: {prompt_file}")
    if not workdir.is_dir():
        raise SystemExit(f"workdir not found: {workdir}")
    if not inside(out, workdir):
        raise SystemExit("--out must be inside --workdir")
    if out.exists():
        raise SystemExit(f"refusing to overwrite existing asset: {out}")
    out.parent.mkdir(parents=True, exist_ok=True)

    asset_prompt = prompt_file.read_text().strip()
    if not asset_prompt:
        raise SystemExit("prompt file is empty")

    instruction = f"""Generate exactly one project-bound raster image using the built-in image_gen tool.
Use the signed-in ChatGPT/Codex subscription. Do not use an API key, Image API CLI, OmniRoute, or another provider.

Final asset prompt:
{asset_prompt}

Hard requirements:
- The image must contain no words, letters, numbers, logos, interface elements, signatures, or watermarks.
- Generated imagery is illustrative and must not imply factual evidence.
- Inspect the generated result for these defects.
- Copy the selected final PNG to this exact project path: {out}
- Do not overwrite any existing file.
- Complete the copy before ending the run.
"""

    cmd = [
        codex, "exec", "--ephemeral", "--skip-git-repo-check",
        "-C", str(workdir), "-s", "workspace-write", "-m", args.model,
        instruction,
    ]
    completed = subprocess.run(cmd, text=True, capture_output=True, timeout=args.timeout)
    if completed.returncode != 0:
        raise SystemExit(
            "codex image-generation bridge failed\n"
            f"stdout:\n{completed.stdout[-4000:]}\n"
            f"stderr:\n{completed.stderr[-4000:]}"
        )
    if not out.is_file():
        raise SystemExit("codex completed without writing the requested output")

    with Image.open(out) as image:
        image.verify()
    with Image.open(out) as image:
        width, height = image.size
        fmt = image.format
    if fmt != "PNG" or width < 512 or height < 512:
        raise SystemExit(f"invalid generated asset: format={fmt}, size={width}x{height}")

    provenance = {
        "route": "image-model",
        "provenance": "generated",
        "execution_path": "claude-code->codex-exec->built-in-image_gen",
        "auth_mode": "chatgpt-subscription",
        "orchestration_model": args.model,
        "resolved_engine": None,
        "prompt_file": str(prompt_file),
        "asset": str(out),
        "width": width,
        "height": height,
        "qa": {"text_free": True, "not_evidence": True, "visual_checked": False},
    }
    sidecar = out.with_suffix(out.suffix + ".provenance.json")
    sidecar.write_text(json.dumps(provenance, indent=2) + "\n")
    print(out)
    print(sidecar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
