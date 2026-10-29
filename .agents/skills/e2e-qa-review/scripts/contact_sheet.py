#!/usr/bin/env python3
"""Tile a folder of screenshots into labelled contact sheets for the one bounded visual round.

usage: python3 contact_sheet.py <shots-dir> <out-prefix>
  writes <out-prefix>-desktop.png and <out-prefix>-phone.png (files named desktop-*.png / phone-*.png, as
  sweep.mjs saves them). Needs Pillow; without it, says so and exits 1 rather than pretending.
"""
import glob
import os
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit('BLOCKED: Pillow is not installed (pip/uv add pillow); look at the screenshots directly instead')


def sheet(files: list[str], out: str, cols: int, tile_w: int) -> None:
    ims = [Image.open(f).convert('RGB') for f in files]
    th = int(tile_w * ims[0].height / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    canvas = Image.new('RGB', (cols * (tile_w + 6), rows * (th + 22)), (30, 30, 30))
    draw = ImageDraw.Draw(canvas)
    for i, (f, im) in enumerate(zip(files, ims)):
        x, y = (i % cols) * (tile_w + 6), (i // cols) * (th + 22)
        canvas.paste(im.resize((tile_w, th)), (x, y + 20))
        draw.text((x + 2, y + 4), os.path.basename(f).split('-', 1)[-1][:-4][:42], fill=(230, 200, 150))
    canvas.save(out)
    print(f'{out}: {len(files)} screenshots')


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, prefix = sys.argv[1], sys.argv[2]
    for tag, cols, w in (('desktop', 6, 360), ('phone', 10, 150)):
        files = sorted(glob.glob(os.path.join(src, f'{tag}-*.png')))
        if files:
            sheet(files, f'{prefix}-{tag}.png', cols, w)


if __name__ == '__main__':
    main()
