#!/usr/bin/env python3
"""Gate a scroll-scrub storyboard before any asset is generated.

Exit 0 clean, 1 blocked (cannot read the plan), 2 findings.

Every check here exists because the defect it catches is invisible until after
the footage is paid for.
"""
import argparse, json, pathlib, re, sys

# --- editable policy, mirrored from SKILL.md "Judgment rules" ---
MIN_COPY_VH = 1.0        # a beat carrying copy needs room to be read
MIN_BEAT_VH = 0.4        # below this nothing registers as a beat at all
MAX_BEAT_VH = 8.0        # above this the reader thinks the page has stalled
DURATION_COUPLING = 0.05 # vh within 5% of (seconds * k) for EVERY beat = inherited, not budgeted

CREDIBILITY = re.compile(
    r"\b(\d+\s*(\+|plus)?\s*(years?|clients?|customers?|projects?|installs?)"
    r"|award[- ]winning|award\b|testimonial|five[- ]star|\d+\s*star"
    r"|trusted by|as seen in|certified by|rated\b)", re.I)


def load(path):
    try:
        data = json.loads(pathlib.Path(path).read_text())
    except FileNotFoundError:
        print(f"BLOCKED: no storyboard at {path}", file=sys.stderr); sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"BLOCKED: storyboard is not valid JSON ({e})", file=sys.stderr); sys.exit(1)
    if not isinstance(data, list) or not data:
        print("BLOCKED: storyboard must be a non-empty list of beats", file=sys.stderr); sys.exit(1)
    return data


def check(beats):
    f = []
    seen, clips = set(), {}

    for i, b in enumerate(beats):
        bid = b.get("id") or f"<beat {i}>"
        if not b.get("id"):
            f.append(f"{bid}: no id — a beat that cannot be named cannot be reviewed")
        if bid in seen:
            f.append(f"{bid}: duplicate id")
        seen.add(bid)

        kind = b.get("kind")
        if kind not in ("scene", "transition"):
            f.append(f"{bid}: kind must be 'scene' or 'transition', got {kind!r}")
        if not b.get("visual"):
            f.append(f"{bid}: no visual described — nothing to generate from")

        vh = b.get("vh")
        if not isinstance(vh, (int, float)):
            f.append(f"{bid}: no vh budget — scroll distance must be a decision, not a default")
            vh = None
        elif vh < MIN_BEAT_VH:
            f.append(f"{bid}: {vh}vh is below {MIN_BEAT_VH}vh — too short to register as a beat")
        elif vh > MAX_BEAT_VH:
            f.append(f"{bid}: {vh}vh exceeds {MAX_BEAT_VH}vh — reads as a stalled page")

        copy = b.get("copy")
        if copy:
            if vh is not None and vh < MIN_COPY_VH:
                f.append(f"{bid}: carries copy but only {vh}vh "
                         f"— under {MIN_COPY_VH}vh the text is never read")
            if CREDIBILITY.search(str(copy)) and not b.get("sourced"):
                f.append(f"{bid}: copy makes a credibility claim without sourced:true "
                         f"— a render will never catch an invented one")
        elif not b.get("copy_waived"):
            f.append(f"{bid}: no copy and no copy_waived — silence is "
                     f"indistinguishable from an oversight")

        clip = b.get("clip")
        if clip:
            clips.setdefault(clip, {"beats": [], "seconds": b.get("clip_seconds")})
            clips[clip]["beats"].append(bid)
            if b.get("clip_seconds") and clips[clip]["seconds"] != b.get("clip_seconds"):
                f.append(f"{bid}: clip {clip!r} declared with two different durations")

        cf = b.get("continues_from")
        if cf:
            if not isinstance(cf, dict) or "clip" not in cf or "frame" not in cf:
                f.append(f"{bid}: continues_from must name a clip and a frame")
            elif cf["clip"] == clip:
                f.append(f"{bid}: continues_from points at its own clip {clip!r}")

    # a transition between two settings must exist as its own beat
    for i in range(len(beats) - 1):
        a, b2 = beats[i], beats[i + 1]
        if a.get("kind") == "scene" and b2.get("kind") == "scene" \
           and a.get("clip") and b2.get("clip") and a["clip"] != b2["clip"] \
           and not b2.get("continues_from"):
            f.append(f"{b2.get('id')}: new clip follows {a.get('id')} with no transition beat "
                     f"and no continues_from — that seam is a cut")

    # scroll budgeted, or merely inherited from footage length?
    pairs = [(b.get("vh"), b.get("clip_seconds")) for b in beats
             if isinstance(b.get("vh"), (int, float)) and b.get("clip_seconds")]
    if len(pairs) >= 3:
        ratios = [v / s for v, s in pairs]
        spread = (max(ratios) - min(ratios)) / max(ratios) if max(ratios) else 0
        if spread < DURATION_COUPLING:
            f.append("every beat's vh is the same multiple of its clip_seconds — scroll "
                     "distance has been inherited from footage length, not budgeted")
    return f, clips


def plan(beats):
    """Generation order: a clip is produced only after the clip it inherits from."""
    order, done = [], set()
    pending = {}
    for b in beats:
        c = b.get("clip")
        if not c or c in pending:
            continue
        pending[c] = b.get("continues_from", {}).get("clip")
    guard = 0
    while pending and guard < 100:
        guard += 1
        for c, parent in list(pending.items()):
            if parent is None or parent in done:
                order.append((c, parent)); done.add(c); pending.pop(c)
    if pending:
        order += [(c, pending[c]) for c in pending]
    return order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--plan", action="store_true", help="print the generation order")
    a = ap.parse_args()

    beats = load(a.storyboard)
    findings, clips = check(beats)
    total = sum(b.get("vh", 0) or 0 for b in beats)

    print(f"{len(beats)} beats  {len(clips)} clip(s)  {total:.1f}vh total scroll")
    for b in beats:
        mark = "T" if b.get("kind") == "transition" else " "
        copy = "copy" if b.get("copy") else ("waived" if b.get("copy_waived") else "MISSING")
        print(f"  {mark} {str(b.get('id')):<14} {str(b.get('vh','?')):>5}vh  "
              f"clip={b.get('clip','-'):<4} {copy}")

    if a.plan:
        print("\ngeneration order:")
        for c, parent in plan(beats):
            src = f"continues {parent}" if parent else "independent"
            print(f"  {c:<6} {src}")

    if findings:
        sys.stdout.flush()   # stderr is unbuffered; without this the findings
                             # print before the summary they refer to
        print(f"\n{len(findings)} finding(s):", file=sys.stderr)
        for x in findings:
            print(f"  - {x}", file=sys.stderr)
        return 2
    print("\nplan is clean. Pacing remains UNVERIFIED until the built page is scrolled.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
