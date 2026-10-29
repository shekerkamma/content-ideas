#!/usr/bin/env python3
"""Assemble the film's slide sequence as a PDF deck.

Existing slides are carried across as their ORIGINAL PDF pages -- never
re-rendered from image exports. The source deck is a vector PDF with real
text; rasterising it to PNG and back would throw that away for nothing.
Only the structural slides this pipeline authored are newly rendered, and
they are rendered as vector pages at the source deck's exact page size.

Reads the same film config the video is built from, so deck and film cannot
drift: one `slide_order`, one narration corpus.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_slides as RS  # noqa: E402


def render_new_page(slide, tok, faces, binpath, page_w_in, page_h_in, out):
    """One authored slide as a single vector PDF page at the deck's size."""
    # The templates are laid out on a 1920x1080 CSS stage; a print page is
    # measured in inches at 96 CSS px/in. Derive the scale, never hardcode it.
    scale = (page_w_in * 96.0) / 1920.0
    css = (f"@page{{size:{page_w_in}in {page_h_in}in;margin:0}}"
           f"html{{margin:0;padding:0}}"
           f"body{{margin:0;padding:0;width:1920px;height:1080px;"
           f"overflow:hidden;zoom:{scale:.6f}}}")
    html = RS.page(RS.build(slide), tok, faces).replace(
        "</style>", css + "</style>", 1)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
        src = f.name
    p = subprocess.run([binpath, "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--no-pdf-header-footer", "--virtual-time-budget=15000",
                        f"--print-to-pdf={out}", f"file://{src}"],
                       capture_output=True, text=True)
    os.unlink(src)
    if not os.path.exists(out) or os.path.getsize(out) < 2000:
        sys.exit(f"BLOCKED: {slide['id']} did not render to PDF\n{p.stderr[-600:]}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--new-slides", required=True,
                    help="the render_slides spec holding the authored slides")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    import pypdf
    cfg = json.load(open(a.config))
    root = os.path.dirname(os.path.abspath(a.config))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(root, p)

    src_pdf = cfg.get("source_pdf")
    if not src_pdf:
        sys.exit("BLOCKED: config has no `source_pdf`. Refusing to rebuild "
                 "slides from image exports when a vector source exists.")
    reader = pypdf.PdfReader(rel(src_pdf))
    pages = cfg["source_pages"]
    box = reader.pages[0].mediabox
    pw, ph = float(box.width) / 72.0, float(box.height) / 72.0

    spec = json.load(open(rel(a.new_slides)))
    by_id = {s["id"]: s for s in spec["slides"]}
    tok = {**RS.TOKENS, **spec.get("tokens", {})}
    faces, _ = RS.font_face_css(spec.get("font_dir", RS.FONT_DIR))
    binpath = RS.chrome()
    RS.prove_font(binpath, faces)

    order = [str(s) for s in cfg["slide_order"]]
    writer = pypdf.PdfWriter()
    tmp = tempfile.mkdtemp()
    carried = authored = 0
    print(f"== {len(order)} slides at {pw:.3f}x{ph:.3f}in ==")
    for s in order:
        if s in pages:
            writer.add_page(reader.pages[int(pages[s]) - 1])
            carried += 1
        elif s in by_id:
            p = render_new_page(by_id[s], tok, faces, binpath, pw, ph,
                                os.path.join(tmp, f"{s}.pdf"))
            writer.add_page(pypdf.PdfReader(p).pages[0])
            authored += 1
        else:
            sys.exit(f"BLOCKED: slide {s} is in neither the source deck nor "
                     f"the authored spec.")

    # Narration travels with the deck, one note per slide.
    narr = json.load(open(rel(cfg["narration"])))
    for i, s in enumerate(order):
        if narr.get(s):
            writer.add_outline_item(f"{i+1}. {narr[s][:70]}", i)

    out = rel(a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        writer.write(f)
    print(f"  {carried} original pages carried, {authored} authored")
    print(f"  {os.path.relpath(out, root)}  {os.path.getsize(out)/1048576:.1f} MB")


if __name__ == "__main__":
    main()
