#!/usr/bin/env python3
"""Derive a draft template profile from a reference deck.

Never writes the canonical template-profile.json; always writes a distinctly
named draft that must be reviewed, copied over, and validated with
validate_template_profile.py. See references/template-derivation.md for the
heuristics used.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


EMU_PER_INCH = 914400

SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"
REFERENCES_DIR = SKILL_DIR / "references"

STRUCTURAL_DEFAULT_ARCHETYPES = {"cover", "executive-summary", "section-divider"}
DEFAULTED_GEOMETRY_FIELDS = ("grid_columns", "gutter_inches")
DEFAULTED_COMPOSITION_FIELDS = (
    "density",
    "corner_radius",
    "shadow_policy",
    "accent_policy",
    "whitespace_policy",
)


def _inches(value: int) -> float:
    return round(value / EMU_PER_INCH, 3)


def _load_default_template() -> dict[str, Any]:
    return json.loads(
        (ASSETS_DIR / "template-profile.template.json").read_text(encoding="utf-8")
    )


def _load_archetype_catalog() -> list[dict[str, Any]]:
    catalog = json.loads(
        (REFERENCES_DIR / "slide-archetypes.json").read_text(encoding="utf-8")
    )
    return catalog["archetypes"]


def _luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.299 * r + 0.587 * g + 0.114 * b


def _saturation(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    hi, lo = max(r, g, b), min(r, g, b)
    return (hi - lo) / 255.0


def derive_colors(image_paths: list[Path], notes: list[str]) -> dict[str, str] | None:
    """Sample dominant page/ink/accent colors from rendered slide images."""
    try:
        from PIL import Image
    except ImportError:
        notes.append("defaulted: brand.colors (Pillow not installed)")
        return None

    counts: dict[tuple[int, int, int], int] = {}
    sampled = 0
    for image_path in image_paths:
        try:
            with Image.open(image_path) as img:
                small = img.convert("RGB").resize((48, 27))
                quantized = small.quantize(colors=8).convert("RGB")
                for count, rgb in quantized.getcolors(48 * 27) or []:
                    counts[rgb] = counts.get(rgb, 0) + count
            sampled += 1
        except (OSError, ValueError):
            continue

    if not counts:
        notes.append("defaulted: brand.colors (no readable slide images)")
        return None

    palette = [rgb for rgb, _ in sorted(counts.items(), key=lambda item: item[1], reverse=True)]
    page = max(palette, key=_luminance)
    ink = min(palette, key=_luminance)
    neutral_candidates = [c for c in palette if c not in (page, ink)]
    accent = max(neutral_candidates, key=_saturation) if neutral_candidates else ink

    def hexcode(rgb: tuple[int, int, int]) -> str:
        return "#{:02X}{:02X}{:02X}".format(*rgb)

    notes.append(f"derived: brand.colors (sampled {sampled} slide image(s))")
    return {"page": hexcode(page), "ink": hexcode(ink), "accent": hexcode(accent)}


def derive_from_pptx(pptx_path: Path, notes: list[str]) -> dict[str, Any]:
    """Measure aspect ratio, fonts, and placeholder geometry from a reference .pptx."""
    from pptx import Presentation
    from pptx.enum.shapes import PP_PLACEHOLDER

    prs = Presentation(str(pptx_path))
    result: dict[str, Any] = {}

    slide_w, slide_h = prs.slide_width, prs.slide_height
    ratio = (slide_w / slide_h) if slide_h else 0
    if abs(ratio - (16 / 9)) < 0.02:
        aspect = "16:9"
    elif abs(ratio - (4 / 3)) < 0.02:
        aspect = "4:3"
    else:
        aspect = "custom"
    result["aspect_ratio"] = aspect
    notes.append(f"derived: template.aspect_ratio ({aspect})")

    title_bottoms_emu: list[int] = []
    footer_heights_emu: list[int] = []
    margin_candidates_in: list[float] = []
    title_sizes_pt: list[float] = []
    body_sizes_pt: list[float] = []
    font_names: set[str] = set()

    for slide in prs.slides:
        for shape in slide.shapes:
            if not getattr(shape, "is_placeholder", False):
                continue
            if shape.left is None or shape.top is None or shape.width is None or shape.height is None:
                continue
            ph_type = shape.placeholder_format.type
            is_title = ph_type in {PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE}

            if slide_w and slide_h:
                margin_candidates_in.extend(
                    _inches(v)
                    for v in (
                        shape.left,
                        shape.top,
                        slide_w - (shape.left + shape.width),
                        slide_h - (shape.top + shape.height),
                    )
                    if v >= 0
                )

            if is_title:
                title_bottoms_emu.append(shape.top + shape.height)
            elif slide_h and (slide_h - (shape.top + shape.height)) < 0.6 * EMU_PER_INCH:
                footer_heights_emu.append(shape.height)

            if not getattr(shape, "has_text_frame", False):
                continue
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    if run.font.name:
                        font_names.add(run.font.name)
                    if run.font.size is not None:
                        (title_sizes_pt if is_title else body_sizes_pt).append(run.font.size.pt)

    if title_sizes_pt:
        title_pt = round(max(title_sizes_pt))
        if title_pt >= 18:
            result["title_pt"] = title_pt
            notes.append(f"derived: typography.title_pt ({title_pt})")
    if body_sizes_pt:
        body_pt = round(min(body_sizes_pt))
        if body_pt >= 8:
            result["body_pt"] = body_pt
            notes.append(f"derived: typography.body_pt ({body_pt})")
    if font_names:
        sorted_fonts = sorted(font_names)
        result["max_font_families"] = len(sorted_fonts)
        result["heading_font"] = sorted_fonts[0]
        result["body_font"] = sorted_fonts[-1] if len(sorted_fonts) > 1 else sorted_fonts[0]
        notes.append(
            f"derived: typography.max_font_families and brand.heading_font/body_font "
            f"({len(sorted_fonts)} font(s) found)"
        )

    if title_bottoms_emu:
        title_zone = _inches(max(title_bottoms_emu))
        if title_zone > 0:
            result["title_zone_inches"] = round(title_zone, 2)
            notes.append(f"derived: geometry.title_zone_inches ({result['title_zone_inches']})")
    if margin_candidates_in:
        safe_margin = round(min(margin_candidates_in), 2)
        if safe_margin >= 0:
            result["safe_margin_inches"] = safe_margin
            notes.append(f"derived: geometry.safe_margin_inches ({safe_margin})")
    if footer_heights_emu:
        footer_zone = round(_inches(max(footer_heights_emu)), 2)
        result["footer_zone_inches"] = footer_zone
        notes.append(f"derived: geometry.footer_zone_inches ({footer_zone})")

    return result


def build_profile(args: argparse.Namespace) -> tuple[dict[str, Any], list[str]]:
    profile = _load_default_template()
    notes: list[str] = []

    source_label = args.pptx or args.evidence
    profile["template"]["source"] = source_label
    notes.append(f"derived: template.source ({source_label})")

    evidence: dict[str, Any] | None = None
    evidence_dir: Path | None = None
    if args.evidence:
        evidence_path = Path(args.evidence)
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        evidence_dir = evidence_path.parent

    if args.pptx:
        pptx_fields = derive_from_pptx(Path(args.pptx), notes)
        if "aspect_ratio" in pptx_fields:
            profile["template"]["aspect_ratio"] = pptx_fields["aspect_ratio"]
        for key in ("title_pt", "body_pt", "max_font_families"):
            if key in pptx_fields:
                profile["typography"][key] = pptx_fields[key]
        for key in ("heading_font", "body_font"):
            if key in pptx_fields:
                profile["brand"][key] = pptx_fields[key]
        for key in ("title_zone_inches", "safe_margin_inches", "footer_zone_inches"):
            if key in pptx_fields:
                profile["geometry"][key] = pptx_fields[key]

    for field in DEFAULTED_GEOMETRY_FIELDS:
        notes.append(f"defaulted: geometry.{field} (no reliable signal; kept template default)")
    for field in DEFAULTED_COMPOSITION_FIELDS:
        notes.append(f"defaulted: composition.{field} (no reliable signal; kept template default)")

    image_paths: list[Path] = []
    slide_word_counts: list[int] = []
    if evidence:
        for slide in evidence.get("slides", []):
            image = slide.get("image")
            if image:
                image_paths.append((evidence_dir / image) if evidence_dir else Path(image))
            text = slide.get("extracted_text") or ""
            if text:
                slide_word_counts.append(len(text.split()))

    colors = derive_colors(image_paths, notes) if image_paths else None
    if colors:
        profile["brand"]["colors"] = colors
    elif not image_paths:
        notes.append("defaulted: brand.colors (no slide images in evidence; kept template default)")

    catalog = _load_archetype_catalog()
    if slide_word_counts:
        candidate_ids = set(STRUCTURAL_DEFAULT_ARCHETYPES)
        for archetype in catalog:
            max_words = archetype["max_words"]
            if any(count <= max_words for count in slide_word_counts):
                candidate_ids.add(archetype["id"])
        profile["archetypes"] = sorted(candidate_ids)
        notes.append(f"derived: archetypes ({len(candidate_ids)} candidate(s) from slide word counts)")
    else:
        notes.append("defaulted: archetypes (no evidence slide text; kept template default)")

    return profile, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, help="Deck run directory")
    parser.add_argument("--evidence", help="Path to presentation-evidence.json")
    parser.add_argument("--pptx", help="Path to a reference .pptx file")
    parser.add_argument(
        "--out", help="Draft output path (default: <run>/draft-template-profile.json)"
    )
    args = parser.parse_args()

    if not args.evidence and not args.pptx:
        print(
            "usage: derive_template_profile.py --run <run-dir> "
            "[--evidence <presentation-evidence.json>] [--pptx <reference.pptx>]",
            file=sys.stderr,
        )
        print("error: at least one of --evidence or --pptx is required", file=sys.stderr)
        return 2

    run_dir = Path(args.run)
    run_dir.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.out) if args.out else run_dir / "draft-template-profile.json"

    try:
        profile, notes = build_profile(args)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    out_path.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for note in notes:
        print(note)
    print(f"draft written: {out_path}")
    print("Review, then: cp", out_path, "<run-dir>/template-profile.json")
    print("Validate with: python3 scripts/validate_template_profile.py <run-dir>/template-profile.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
