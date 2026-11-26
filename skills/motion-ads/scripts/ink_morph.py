#!/usr/bin/env python3
"""Work out how one flat image can physically turn into another, pixel by pixel.

This is the "transform, don't dissolve" rule made concrete for flat graphics: screens, logos,
icons, text. Every dark pixel of image A is paired with a nearby dark pixel of image B. Animate
each pair from its start to its end and A re-forms into B, with nothing fading.

How pixels are paired:
  - pixels that are dark in both images stay where they are;
  - the rest are matched in rounds: each target asks for its nearest free source, the closest
    asker wins, so journeys stay short and neighbours travel together;
  - if B has more ink, the extra pixels split off from ink that is already there;
  - if A has more ink, the extra pixels merge into B's nearest ink.

For each pair of images it writes <out>/morph-N.bin: rows of six int16 numbers
(start x, start y, end x, end y, start shade, end shade), shade 0 = paper to --levels-1 = full ink.
<out>/morphs.json lists the files with counts and typical travel distances.
Every morph is checked: the particles must redraw A exactly at the start and B exactly at the end.

In the page, load the file as an Int16Array and move each particle with an eased 0-to-1 value.
Give neighbours the same start delay (a wave that spreads from one point works well) so shapes
stretch and flow. Random delays turn the picture into dust.

All images must be the same size. Dark-on-light by default; use --invert for light-on-dark.

Needs: numpy, scipy, Pillow.
"""
import argparse
import json
import os
import sys
import time


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("images", nargs="+", help="two or more images, in the order they appear")
    p.add_argument("--out", default="morphs", help="folder to write to (default morphs/)")
    p.add_argument("--levels", type=int, default=4, help="shades to keep, including paper (default 4, as on a 2-bit e-ink screen)")
    p.add_argument("--invert", action="store_true", help="treat light pixels as the ink")
    p.add_argument("--spread", type=int, default=12, help="extra pixels pick one of this many nearest neighbours (default 12)")
    a = p.parse_args()
    if len(a.images) < 2:
        p.error("give at least two images")

    import numpy as np
    from PIL import Image
    from scipy.spatial import cKDTree

    top = a.levels - 1

    def shades(path):
        grey = np.asarray(Image.open(path).convert("L")).astype(float)
        ink = grey if a.invert else 255 - grey
        return np.round(ink / (255.0 / top)).astype(np.int16)

    def rows(src, dst, A, B):
        return np.column_stack([src[:, 1], src[:, 0], dst[:, 1], dst[:, 0], A[src[:, 0], src[:, 1]], B[dst[:, 0], dst[:, 1]]])

    def pair(A, B, seed):
        rng = np.random.default_rng(seed)
        shared = (A > 0) & (B > 0)
        stay = np.argwhere(shared)
        leaving = np.argwhere((A > 0) & ~shared)
        arriving = np.argwhere((B > 0) & ~shared)
        free, waiting = np.arange(len(leaving)), np.arange(len(arriving))
        from_idx, to_idx, rounds = [], [], 0
        while len(free) and len(waiting):
            dist, nearest = cKDTree(leaving[free]).query(arriving[waiting])
            order = np.argsort(dist, kind="stable")
            winners = order[np.unique(nearest[order], return_index=True)[1]]
            from_idx.append(free[nearest[winners]])
            to_idx.append(waiting[winners])
            keep_w = np.ones(len(waiting), bool)
            keep_w[winners] = False
            keep_f = np.ones(len(free), bool)
            keep_f[nearest[winners]] = False
            waiting, free, rounds = waiting[keep_w], free[keep_f], rounds + 1
        from_idx = np.concatenate(from_idx) if from_idx else np.zeros(0, int)
        to_idx = np.concatenate(to_idx) if to_idx else np.zeros(0, int)
        table = [rows(stay, stay, A, B), rows(leaving[from_idx], arriving[to_idx], A, B)]
        all_a, all_b = np.argwhere(A > 0), np.argwhere(B > 0)
        if len(waiting) and len(all_a):
            target = arriving[waiting]
            k = min(a.spread, len(all_a))
            _, near = cKDTree(all_a).query(target, k=k)
            near = near.reshape(len(target), -1)
            source = all_a[near[np.arange(len(target)), rng.integers(0, k, len(target))]]
            table.append(rows(source, target, A, B))
        if len(free) and len(all_b):
            source = leaving[free]
            k = min(a.spread, len(all_b))
            _, near = cKDTree(all_b).query(source, k=k)
            near = near.reshape(len(source), -1)
            target = all_b[near[np.arange(len(source)), rng.integers(0, k, len(source))]]
            table.append(rows(source, target, A, B))
        P = np.concatenate(table).astype(np.int16)
        travel = np.hypot(P[:, 2] - P[:, 0], P[:, 3] - P[:, 1])
        moved = travel[travel > 0]
        info = {"particles": len(P), "stay": len(stay), "moved": len(from_idx), "split": len(waiting), "merged": len(free), "rounds": rounds,
                "median_px": float(np.median(moved)) if len(moved) else 0.0, "p95_px": float(np.percentile(moved, 95)) if len(moved) else 0.0}
        return P, info

    images = [shades(path) for path in a.images]
    if len({im.shape for im in images}) != 1:
        sys.exit("All images must be the same size: " + ", ".join(f"{os.path.basename(n)} {im.shape[1]}x{im.shape[0]}" for n, im in zip(a.images, images)))
    os.makedirs(a.out, exist_ok=True)
    listing = []
    for i in range(len(images) - 1):
        started = time.time()
        P, info = pair(images[i], images[i + 1], i)
        for xi, yi, si, ref in ((0, 1, 4, images[i]), (2, 3, 5, images[i + 1])):
            redraw = np.zeros_like(ref)
            np.maximum.at(redraw, (P[:, yi], P[:, xi]), P[:, si])
            if not (redraw == ref).all():
                sys.exit(f"morph {i} does not redraw its image exactly: do not use it")
        P.tofile(os.path.join(a.out, f"morph-{i}.bin"))
        info.update(file=f"morph-{i}.bin", start=os.path.basename(a.images[i]), end=os.path.basename(a.images[i + 1]),
                    width=int(images[i].shape[1]), height=int(images[i].shape[0]), levels=a.levels)
        listing.append(info)
        print(f"morph-{i}: {info['particles']} particles, {info['moved']} travel (typically {info['median_px']:.0f} px), "
              f"{info['split']} split, {info['merged']} merge, {time.time() - started:.1f} s")
    json.dump(listing, open(os.path.join(a.out, "morphs.json"), "w"), indent=1)
    print(f"Every morph redraws both of its images exactly. Wrote {len(listing)} to {a.out}/")


if __name__ == "__main__":
    main()
