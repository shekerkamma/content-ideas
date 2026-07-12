#!/usr/bin/env python3
"""Install the repo-local You.com Hermes web plugin into ~/.hermes."""

from __future__ import annotations

import pathlib
import shutil
import sys

from hermes_cli.config import load_config, save_config, save_env_value


def main() -> int:
    api_key = sys.stdin.read().strip()
    if not api_key:
        print("missing YOU_API_KEY on stdin", file=sys.stderr)
        return 2

    src = pathlib.Path("/home/shekerk/content-ideas/hermes-plugins/web/you")
    dst = pathlib.Path.home() / ".hermes" / "plugins" / "web" / "you"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)

    save_env_value("YOU_API_KEY", api_key)

    cfg = load_config()
    web = cfg.setdefault("web", {})
    web["search_backend"] = "you"
    if not web.get("extract_backend"):
        web["extract_backend"] = "exa"

    plugins = cfg.setdefault("plugins", {})
    enabled = plugins.setdefault("enabled", [])
    for key in ("web/you", "web-you"):
        if key not in enabled:
            enabled.append(key)

    save_config(cfg)
    print(
        "installed web/you; "
        f"search_backend={web.get('search_backend')}; "
        f"extract_backend={web.get('extract_backend')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
