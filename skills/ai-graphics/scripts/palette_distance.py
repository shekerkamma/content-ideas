#!/usr/bin/env python3
"""Share-weighted palette distance from candidate images to a style reference.

Style transfer has no absolute pass mark, so this is deliberately COMPARATIVE:
the `--mode style` arm must land closer to the reference palette than the
no-reference control does. A fixed threshold would be the wrong test — it calls
a correct render wrong whenever the subject legitimately shifts the histogram,
which is precisely what a style test asks the subject to do.

  python3 palette_distance.py <reference> <candidate>...

Reads as: for each dominant colour in the candidate, the distance to its nearest
neighbour in the reference palette, weighted by how much of the image it covers.
0 means the palettes coincide; the scale is RGB euclidean, so ~14 separates two
deliberately opposite design systems (measured: navy/teal infographic vs cream
editorial page).
"""
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("BLOCKED: Pillow is required (pip install pillow). Not measuring.")

SAMPLE = 240


def palette(path: str, n: int = 8) -> list[tuple[float, tuple[int, int, int]]]:
    im = Image.open(path).convert("RGB").resize((SAMPLE, SAMPLE))
    q = im.quantize(colors=n, method=Image.MEDIANCUT).convert("RGB")
    counts = sorted(q.getcolors(SAMPLE * SAMPLE), key=lambda c: -c[0])
    total = sum(c for c, _ in counts) or 1
    return [(c / total, rgb) for c, rgb in counts]


def distance(cand, ref) -> float:
    return sum(
        share * min(sum((a - b) ** 2 for a, b in zip(rgb, r)) ** 0.5 for _, r in ref)
        for share, rgb in cand
    )


def _hexes(pal, k=5):
    return [f"#%02x%02x%02x" % c for _, c in pal[:k]]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    ref = palette(argv[0])
    print(f"reference {argv[0].split('/')[-1]}: {_hexes(ref)}")
    for p in argv[1:]:
        cand = palette(p)
        print(f"{distance(cand, ref):8.2f}  {p.split('/')[-1]:26s} {_hexes(cand)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
