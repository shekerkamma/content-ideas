#!/usr/bin/env python3
"""Derive a build-order animation plan from a deck's own shape geometry.

Input is `officecli query <deck> shape --json`, which returns every shape in
the package with a STABLE @id path and resolved geometry -- one call for a
whole deck. That makes the plan independent of the builder: nothing has to be
tagged at build time, and the plan survives a rebuild.

Bands are read top-to-bottom; inside a band, columns wipe left-to-right, so a
row of peer cards fills the way a signal runs through a chain.

THE RULE THAT MAKES THIS WORK: one perceived step per BAND, not per column.
Inside a band every shape is `withPrevious` and the left-to-right stagger comes
from `delay`, not from `trigger`. A four-card row is then one click and one
motion instead of four. Assigning a trigger per column blows the step budget on
every content slide, and collapsing bands to fix the count destroys exactly the
left-to-right motion that was the point.

Note that lint_motion.py's `max_build_steps_per_slide` counts one entry per
effect NODE (per animated shape), not per perceived step -- the two readings
differ by an order of magnitude on a dense deck. Set that cap as a node
ceiling with the reason recorded, and keep the click budget here in MAX_STEPS.
"""
from __future__ import annotations
import json, re, sys, collections

PX_PER_PT = 1280 / 960          # the 13.333in stage rendered on a 1280px canvas
BAND_GAP  = 26                  # px: a larger vertical jump starts a new band
COL_GAP   = 8                   # px: a larger horizontal jump starts a new column
HEADER_Y  = 162                 # kicker/title/subtitle/rule appear with the slide
FOOTER_Y  = 646                 # footer + page number appear with the slide
MAX_STEPS = 8                   # perceived build steps per slide
STAGGER   = 110                 # ms between columns inside one band


def to_px(v: str) -> float:
    v = str(v).strip()
    m = re.match(r'^(-?[\d.]+)\s*(cm|mm|pt|in|px|emu)?$', v)
    if not m:
        return 0.0
    n, u = float(m.group(1)), (m.group(2) or 'pt')
    pt = {'pt': n, 'in': n * 72, 'cm': n / 2.54 * 72, 'mm': n / 25.4 * 72,
          'px': n * 0.75, 'emu': n / 12700}[u]
    return pt * PX_PER_PT


def load(path: str):
    d = json.load(open(path))
    per = collections.defaultdict(list)
    for r in d['data']['results']:
        m = re.match(r'/slide\[(\d+)\]', r['path'])
        f = r.get('format') or {}
        per[int(m.group(1))].append(dict(
            path=r['path'],
            x=to_px(f.get('x', 0)), y=to_px(f.get('y', 0)),
            w=to_px(f.get('width', 0)), h=to_px(f.get('height', 0)),
            z=f.get('zorder', 0), text=(r.get('text') or '').strip(),
        ))
    return per


def seat_filter(shapes, seats):
    """Drop shapes that a video will cover.

    An embedded clip is present from the first frame -- officecli media carries
    no build -- so anything animating underneath it would wipe in behind
    something already on screen. Its frame must rest with the slide.
    """
    if not seats:
        return shapes
    out = []
    for s in shapes:
        area = max(1.0, s['w'] * s['h'])
        covered = False
        for st in seats:
            ix = max(0, min(s['x'] + s['w'], st['x'] + st['w']) - max(s['x'], st['x']))
            iy = max(0, min(s['y'] + s['h'], st['y'] + st['h']) - max(s['y'], st['y']))
            if ix * iy / area > 0.5:
                covered = True
                break
        if not covered:
            out.append(s)
    return out


def bands_of(shapes):
    """Group a slide's body shapes into bands (rows), each split into columns."""
    body = [s for s in shapes
            if s['w'] < 1270                      # not a full-bleed background
            and s['h'] < 600                      # not a grid hairline or panel
            and s['y'] + s['h'] > HEADER_Y        # not the header block
            and s['y'] < FOOTER_Y]                # not the footer strip
    if not body:
        return []
    body.sort(key=lambda s: (round(s['y'] / BAND_GAP), s['x'], s['z']))

    bands, cur, top = [], [], None
    for s in body:
        if top is None or s['y'] - top <= BAND_GAP:
            cur.append(s); top = s['y'] if top is None else min(top, s['y'])
        else:
            bands.append(cur); cur, top = [s], s['y']
    if cur:
        bands.append(cur)

    out = []
    for band in bands:
        band.sort(key=lambda s: (s['x'], s['z']))
        cols, col, right = [], [], None
        for s in band:
            if right is None or s['x'] <= right + COL_GAP:
                col.append(s); right = max(right or 0, s['x'] + s['w'])
            else:
                cols.append(col); col, right = [s], s['x'] + s['w']
        if col:
            cols.append(col)
        out.append(cols)
    return out


def plan_slide(shapes, dark: bool, seats=()):
    """One perceived build step per band.

    Inside a band the columns are staggered by delay rather than by trigger, so
    a four-card row fills left-to-right as ONE step -- the marching fill the
    product simulators use -- instead of costing four clicks.
    """
    groups = bands_of(seat_filter(shapes, seats))
    if not groups:
        return []

    budget = 4 if dark else MAX_STEPS
    while len(groups) > budget:
        # Merge the adjacent pair that is cheapest to combine.
        i = min(range(len(groups) - 1),
                key=lambda k: len(groups[k]) + len(groups[k + 1]))
        groups[i:i + 2] = [groups[i] + groups[i + 1]]

    steps = []
    for bi, cols in enumerate(groups):
        chain = len(cols) >= 3          # a row of peers reads as a signal chain
        items = []
        for ci, col in enumerate(cols):
            for s in sorted(col, key=lambda s: s['z']):
                items.append(dict(path=s['path'], delay=ci * STAGGER))
        wide = any(s['w'] > 700 for col in cols for s in col)
        steps.append(dict(
            effect='wipe',
            cls='entrance',
            direction='right' if chain else 'up',
            duration=320 if chain else (450 if wide else 380),
            trigger='withPrevious' if bi == 0 else 'afterPrevious',
            items=items,
        ))
    return steps


def main(shapes_json: str, out: str, dark_csv: str, seats_json: str = ''):
    dark = {int(x) for x in dark_csv.split(',') if x.strip()}
    seats = collections.defaultdict(list)
    if seats_json:
        for st in json.load(open(seats_json))['seats']:
            # A clip covers its frame too, so exclude against the frame rect.
            f = st.get('frame', st)
            seats[st['slide']].append(f)
    per = load(shapes_json)
    plan = []
    for n in sorted(per):
        steps = plan_slide(per[n], n in dark, seats.get(n, ()))
        plan.append(dict(
            slide=n,
            transition='fade',
            transition_ms=600 if n in dark else 400,
            steps=steps,
        ))
    json.dump(dict(deck_slides=len(plan), plan=plan), open(out, 'w'), indent=1)
    tot = sum(len(p['steps']) for p in plan)
    nodes = sum(len(s['items']) for p in plan for s in p['steps'])
    print(f'slides {len(plan)}  perceived steps {tot}  '
          f'max/slide {max(len(p["steps"]) for p in plan)}  animated shapes {nodes}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2],
         sys.argv[3] if len(sys.argv) > 3 else '',
         sys.argv[4] if len(sys.argv) > 4 else '')
