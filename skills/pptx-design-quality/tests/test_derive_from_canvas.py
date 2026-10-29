"""Canvas-input derivation.

Deliberately free of `pptx`/`PIL` importorskip guards: the --canvas path is
stdlib-only, and these tests must run on a host where neither optional
dependency is installed.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


SKILL_DIR = Path(__file__).resolve().parents[1]
DERIVER = SKILL_DIR / "scripts/derive_template_profile.py"
VALIDATOR = SKILL_DIR / "scripts/validate_template_profile.py"

ARTBOARD = """<!doctype html>
<html><head><style>
  .root {{ width: {frame_w}px; height: {frame_h}px; padding: {pad}px; background: #0B1B2B; }}
  .title {{ font-family: "Aptos Display", sans-serif; font-size: {title}px; color: #FFFFFF; }}
  .grid {{ display: grid; grid-template-columns: repeat(12, 1fr); gap: {gap}px; }}
  .card {{ border-radius: {radius}px; background: #12283F; }}
  .body {{ font-family: "Aptos", sans-serif; font-size: {body}px; color: #D6E2EE; }}
  .accent {{ font-family: "Aptos", sans-serif; font-size: {body}px; color: #22D3EE; }}
  .caption {{ font-family: "Aptos", sans-serif; font-size: {caption}px; color: #7C8DA0; }}
</style></head><body><div class="root">
  <div class="title">T</div>
  <div class="grid"><div class="card">
    <p class="body">B</p><p class="accent">A</p><p class="caption">C</p>
  </div></div>
</div></body></html>
"""


def run_deriver(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(DERIVER), *args], check=False, capture_output=True, text=True
    )


def write_canvas(
    tmp_path: Path,
    *,
    frame_w: int = 1280,
    frame_h: int = 720,
    title: int = 40,
    body: int = 18,
    caption: int = 10,
    pad: int = 48,
    gap: int = 16,
    radius: int = 8,
    extra: dict[str, str] | None = None,
    manifest: bool = True,
) -> Path:
    canvas_dir = tmp_path / "canvas"
    canvas_dir.mkdir(parents=True)
    (canvas_dir / "Main.dc.html").write_text(
        ARTBOARD.format(
            frame_w=frame_w,
            frame_h=frame_h,
            title=title,
            body=body,
            caption=caption,
            pad=pad,
            gap=gap,
            radius=radius,
        ),
        encoding="utf-8",
    )
    files = ["Main.dc.html"]
    for name, text in (extra or {}).items():
        (canvas_dir / name).write_text(text, encoding="utf-8")
        files.append(name)

    if manifest:
        (canvas_dir / "canvas.json").write_text(
            json.dumps(
                {
                    "artboards": [
                        {
                            "file": name,
                            "x": index * (frame_w + 80),
                            "y": 0,
                            "w": frame_w,
                            "h": frame_h,
                        }
                        for index, name in enumerate(files)
                    ],
                    "launch": {"view": "canvas"},
                }
            ),
            encoding="utf-8",
        )
    return canvas_dir


def derive(tmp_path: Path, canvas_dir: Path) -> tuple[dict, str]:
    run_dir = tmp_path / "run"
    result = run_deriver(["--run", str(run_dir), "--canvas", str(canvas_dir)])
    assert result.returncode == 0, result.stderr
    profile = json.loads((run_dir / "draft-template-profile.json").read_text(encoding="utf-8"))
    return profile, result.stdout


def test_canvas_alone_produces_a_schema_valid_draft(tmp_path: Path) -> None:
    pytest.importorskip("jsonschema")
    canvas_dir = write_canvas(tmp_path)
    profile, _ = derive(tmp_path, canvas_dir)

    canonical = tmp_path / "run/template-profile.json"
    canonical.write_text(json.dumps(profile), encoding="utf-8")
    validated = subprocess.run(
        [sys.executable, str(VALIDATOR), str(canonical)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert validated.returncode == 0, validated.stderr


def test_point_scale_comes_from_the_frame_not_a_constant(tmp_path: Path) -> None:
    """A 1280px 16:9 frame is 0.75pt/px; a 1920px one is 0.5pt/px.

    Hardcoding 0.75 (the 96dpi CSS constant) would report 30pt for both and is
    the exact mistake this input exists to prevent.
    """
    profile_1280, _ = derive(tmp_path / "a", write_canvas(tmp_path / "a", title=40))
    profile_1920, _ = derive(
        tmp_path / "b", write_canvas(tmp_path / "b", frame_w=1920, frame_h=1080, title=40)
    )

    assert profile_1280["typography"]["title_pt"] == 30.0
    assert profile_1920["typography"]["title_pt"] == 20.0


def test_derives_the_three_fields_the_pptx_path_cannot(tmp_path: Path) -> None:
    canvas_dir = write_canvas(tmp_path, gap=16, radius=8)
    profile, stdout = derive(tmp_path, canvas_dir)

    assert profile["geometry"]["grid_columns"] == 12
    assert profile["geometry"]["gutter_inches"] == 0.167
    assert profile["composition"]["corner_radius"] == 0.083
    for field in ("grid_columns", "gutter_inches"):
        assert f"defaulted: geometry.{field}" not in stdout
    assert "defaulted: composition.corner_radius" not in stdout


def test_safe_margin_comes_from_a_frame_width_root(tmp_path: Path) -> None:
    profile, _ = derive(tmp_path, write_canvas(tmp_path, pad=48))
    assert profile["geometry"]["safe_margin_inches"] == 0.5


def test_fonts_split_by_size_not_alphabetically(tmp_path: Path) -> None:
    """The .pptx path picks fonts alphabetically and says so; this one does not.

    "Aptos Display" sorts before "Aptos", so alphabetical order would agree by
    accident here -- the size ramp is what must decide.
    """
    profile, _ = derive(tmp_path, write_canvas(tmp_path))
    assert profile["brand"]["heading_font"] == "Aptos Display"
    assert profile["brand"]["body_font"] == "Aptos"
    assert profile["typography"]["max_font_families"] == 2


def test_cover_hero_does_not_set_the_deck_title_size(tmp_path: Path) -> None:
    """Typography is scoped to the reference artboard, not the whole canvas."""
    cover = ARTBOARD.format(
        frame_w=1280, frame_h=720, title=64, body=18, caption=10, pad=48, gap=16, radius=8
    )
    canvas_dir = write_canvas(tmp_path, title=40, extra={"Cover.dc.html": cover})
    profile, stdout = derive(tmp_path, canvas_dir)

    assert profile["typography"]["title_pt"] == 30.0  # 40px on Main, not 64px on Cover
    assert "largest text on Main.dc.html" in stdout


def test_artboard_names_seed_archetypes(tmp_path: Path) -> None:
    comparison = ARTBOARD.format(
        frame_w=1280, frame_h=720, title=40, body=18, caption=10, pad=48, gap=16, radius=8
    )
    canvas_dir = write_canvas(tmp_path, extra={"Comparison.dc.html": comparison})
    profile, _ = derive(tmp_path, canvas_dir)

    assert "comparison" in profile["archetypes"]
    assert {"cover", "executive-summary", "section-divider"} <= set(profile["archetypes"])


def test_canvas_json_path_is_accepted_as_well_as_the_directory(tmp_path: Path) -> None:
    canvas_dir = write_canvas(tmp_path)
    run_dir = tmp_path / "run2"
    result = run_deriver(["--run", str(run_dir), "--canvas", str(canvas_dir / "canvas.json")])

    assert result.returncode == 0, result.stderr
    assert (run_dir / "draft-template-profile.json").is_file()


def test_missing_canvas_json_still_derives_what_markup_carries(tmp_path: Path) -> None:
    """No manifest means no frame, so no px scale -- fonts and grid still land."""
    canvas_dir = write_canvas(tmp_path, manifest=False)
    profile, stdout = derive(tmp_path, canvas_dir)

    assert "defaulted: px scale" in stdout
    assert profile["brand"]["heading_font"] == "Aptos Display"
    assert profile["geometry"]["grid_columns"] == 12
    assert profile["typography"]["title_pt"] == 30  # untouched template default


def test_directory_without_artboards_errors_cleanly(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    result = run_deriver(["--run", str(tmp_path / "run"), "--canvas", str(empty)])

    assert result.returncode == 1
    assert "no *.dc.html artboards" in result.stderr


def test_input_guard_names_canvas(tmp_path: Path) -> None:
    result = run_deriver(["--run", str(tmp_path)])

    assert result.returncode == 2
    assert "at least one of --evidence, --pptx or --canvas is required" in result.stderr


def test_unused_rules_in_a_shared_stylesheet_do_not_join_the_type_ramp(tmp_path: Path) -> None:
    """Found by running the L01-L16 canvas, not by reading the code.

    One stylesheet shared across every artboard carries a `.cover {64px}` rule
    that only the cover element uses. Counting declared-but-unapplied rules put
    48pt into `title_pt` on a body slide whose title is 40px, silently defeating
    the reference-artboard scoping.
    """
    canvas_dir = tmp_path / "canvas"
    canvas_dir.mkdir(parents=True)
    shared = """<!doctype html><html><head><style>
      .root {{ width: 1280px; height: 720px; padding: 48px; }}
      .cover {{ font-family: "Georgia", serif; font-size: 64px; }}
      .title {{ font-family: "Georgia", serif; font-size: 40px; }}
      .body {{ font-family: "Aptos", sans-serif; font-size: 18px; }}
    </style></head><body><div class="root">{markup}</div></body></html>"""

    (canvas_dir / "Main.dc.html").write_text(
        shared.format(markup='<div class="title">T</div><div class="body">B</div>'),
        encoding="utf-8",
    )
    (canvas_dir / "Cover.dc.html").write_text(
        shared.format(markup='<div class="cover">C</div>'), encoding="utf-8"
    )
    (canvas_dir / "canvas.json").write_text(
        json.dumps(
            {
                "artboards": [
                    {"file": "Main.dc.html", "x": 0, "y": 0, "w": 1280, "h": 720},
                    {"file": "Cover.dc.html", "x": 1360, "y": 0, "w": 1280, "h": 720},
                ]
            }
        ),
        encoding="utf-8",
    )

    profile, _ = derive(tmp_path, canvas_dir)
    assert profile["typography"]["title_pt"] == 30.0  # 40px used, not 64px declared
