#!/usr/bin/env python3
"""Build a banner/social card: real HTML text over text-free Gemini art, rendered and OCR-checked.

  make_card.py --layout square|landscape --art ART.jpg --title "X" --tagline "Y" --out DIR [--no-render]

Steps: art-slot text check (check_media.py textfree) -> fill templates/card-<layout>.html
-> render with ai-graphics html_to_png.mjs -> OCR the text region (check_media.py ocr --region).
Writes DIR/card-<layout>.html (the editable source), DIR/art.jpg and DIR/card-<layout>.png.
Exit 0 = rendered and OCR passed; 1 = a check failed; 2 = usage or a missing tool.
"""
from __future__ import annotations
import argparse, html, os, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
LAYOUTS = {  # canvas and the text area the OCR check reads (fractions x0,y0,x1,y1)
    "square": {"canvas": "1080x1080", "region": "0,0,1,0.42"},
    "landscape": {"canvas": "1200x627", "region": "0,0.25,0.52,0.75"},
}
HTML_TO_PNG = os.environ.get("AI_GRAPHICS_HTML_TO_PNG",
                             str(Path.home() / ".claude/skills/ai-graphics/scripts/html_to_png.mjs"))
# On Windows the renderer lives in WSL (relative to its $HOME), like the WSL Tesseract fallback.
WSL_HTML_TO_PNG = os.environ.get("WSL_HTML_TO_PNG", "$HOME/.claude/skills/ai-graphics/scripts/html_to_png.mjs")


def fill(template: str, title: str, tagline: str) -> str:
    """Escaped substitution; refuses to leave a placeholder behind."""
    out = template.replace("{{TITLE}}", html.escape(title)).replace("{{TAGLINE}}", html.escape(tagline))
    if "{{" in out:
        raise ValueError("template still has an unfilled {{placeholder}}")
    return out


# Inside WSL, `wsl.exe -e sh` (and bash -lc) find the system /usr/bin/node v18, which wrote a
# 512 KiB non-PNG for html_to_png.mjs on 2026-10-26; nvm's node v24 wrote a valid PNG. Prefer
# WSL_NODE, else the newest nvm node, else whatever `node` is on PATH.
WSL_NODE_PICK = ('N="${WSL_NODE:-$(ls -d "$HOME"/.nvm/versions/node/*/bin/node 2>/dev/null '
                 '| sort -V | tail -1)}"; ')
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def render_argv(html_path: Path, png: Path, canvas: str) -> list[str] | None:
    node = os.environ.get("NODE_BIN") or shutil.which("node")
    if Path(HTML_TO_PNG).is_file() and node:
        return [node, HTML_TO_PNG, str(html_path), str(png), canvas]
    wsl = shutil.which("wsl.exe") or shutil.which("wsl")
    if os.name == "nt" and wsl:
        return [wsl, "-e", "sh", "-c",
                WSL_NODE_PICK + f'exec "${{N:-node}}" "{WSL_HTML_TO_PNG}" "$(wslpath -a "$1")" '
                '"$(wslpath -a "$2")" "$3"', "_", str(html_path), str(png), canvas]
    return None


def is_png(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(8) == PNG_MAGIC
    except OSError:
        return False


def run_check(*args: str) -> int:
    r = subprocess.run([sys.executable, str(HERE / "check_media.py"), *args], capture_output=True, text=True)
    print((r.stdout + r.stderr).strip())
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--layout", choices=LAYOUTS, required=True)
    ap.add_argument("--art", required=True); ap.add_argument("--title", required=True)
    ap.add_argument("--tagline", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--no-render", action="store_true", help="write the HTML only (no node/Tesseract needed)")
    a = ap.parse_args()
    lay, out = LAYOUTS[a.layout], Path(a.out)
    if not Path(a.art).is_file():
        print(f"no such art file: {a.art}")
        return 2
    out.mkdir(parents=True, exist_ok=True)
    if not a.no_render:
        rc = run_check("textfree", a.art)
        if rc:
            return rc
    shutil.copyfile(a.art, out / "art.jpg")
    page = out / f"card-{a.layout}.html"
    page.write_text(fill((SKILL / "templates" / f"card-{a.layout}.html").read_text(), a.title, a.tagline))
    print(f"wrote {page}")
    if a.no_render:
        return 0
    png = out / f"card-{a.layout}.png"
    argv = render_argv(page, png, lay["canvas"])
    if not argv:
        print(f"renderer not found: {HTML_TO_PNG} (set AI_GRAPHICS_HTML_TO_PNG)")
        return 2
    r = subprocess.run(argv, capture_output=True, text=True)
    if r.returncode or not png.is_file():
        print(f"render failed: {(r.stdout + r.stderr).strip()[:400]}")
        return 1
    if not is_png(png):
        print(f"render wrote a non-PNG file ({png.stat().st_size} bytes) at {png}: the renderer exited 0 "
              "but the output is corrupt. An old node (system v18) does this; set NODE_BIN / WSL_NODE to node 20+.")
        return 1
    print(f"rendered {png} ({lay['canvas']})")
    return run_check("ocr", str(png), a.title, a.tagline, "--region", lay["region"])


if __name__ == "__main__":
    sys.exit(main())
