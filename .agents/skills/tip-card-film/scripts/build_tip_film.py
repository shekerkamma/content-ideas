#!/usr/bin/env python3
"""Build a HyperFrames project that cuts a talking-head video into "tip cards".

usage: python3 build_tip_film.py <spec.json> <out-dir>
then:  cd <out-dir> && npx hyperframes check && npx hyperframes render --output film.mp4

The choreography (the camera blurs and shrinks into a rounded picture-in-picture on the right while a
titled card builds on the left, then everything reverses) comes from the pattern; the look comes from the
spec's design tokens, so each film wears its own brand. Spec (all times in seconds of the camera video):

{
  "camera": "talk.mp4",                    # the recorded video; its own audio is the soundtrack
  "width": 1920, "height": 1080,
  "tokens": {"bg": "#f4f1ea", "ink": "#1d1f21", "ink2": "#5e646a", "accent": "#b4622a",
             "surface": "#1b1d1f", "surface_ink": "#f2efe8",
             "font_display": "Newsreader, serif", "font_text": "sans-serif"},
  "fonts": [{"family": "Newsreader", "file": "fonts/Newsreader.woff2", "weight": "400 700"}],
  "cards": [
    {"start": 12.4, "end": 17.8, "title": "Grab a font", "subtitle": "one that fits the brand",
     "image": "shots/fonts.png"},
    {"start": 21.0, "end": 26.0, "title": "Ask for SVG", "subtitle": "editable, animatable",
     "prompt": "Make the icons and the diagram as SVG, not raster."}
  ]
}

Each card shows an image, a prompt box, or neither. Paths are relative to the spec file and are copied
into <out-dir>/assets. Stdlib only; ffprobe reads the camera's duration.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys

DEFAULT_TOKENS = {'bg': '#f4f1ea', 'ink': '#1d1f21', 'ink2': '#5e646a', 'accent': '#b4622a',
                  'surface': '#1b1d1f', 'surface_ink': '#f2efe8',
                  'font_display': 'serif', 'font_text': 'sans-serif'}
GENERIC = {'serif', 'sans-serif', 'monospace', 'system-ui', 'cursive', 'fantasy', 'ui-serif', 'ui-sans-serif',
           'ui-monospace', 'ui-rounded', '-apple-system', 'blinkmacsystemfont'}
TRANSITION = 0.45   # camera move in or out
PIP = 0.34          # picture-in-picture width as a fraction of the frame


def die(msg: str) -> None:
    sys.exit('BLOCKED: ' + msg)


def duration(path: str) -> float:
    if not shutil.which('ffprobe'):
        die('ffprobe not found (install ffmpeg)')
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        die(f'cannot read the duration of {path}')


def named_families(stack: str) -> list[str]:
    return [f.strip().strip('"\'') for f in stack.split(',') if f.strip().strip('"\'').lower() not in GENERIC]


def validate(spec: dict, base: str, dur: float) -> None:
    problems, prev_end = [], 0.0
    for i, c in enumerate(spec.get('cards', [])):
        s, e = c.get('start'), c.get('end')
        if not isinstance(s, (int, float)) or not isinstance(e, (int, float)) or e <= s:
            problems.append(f'cards[{i}]: start/end must be numbers with end > start')
            continue
        if e - s < 2 * TRANSITION + 0.6:
            problems.append(f'cards[{i}]: {e - s:.2f}s is too short (min {2 * TRANSITION + 0.6:.2f}s for in, hold, out)')
        if s < prev_end + 0.2:
            problems.append(f'cards[{i}]: starts {s}s, overlapping or touching the previous card (ends {prev_end}s)')
        if e > dur:
            problems.append(f'cards[{i}]: ends {e}s, after the camera video ({dur:.2f}s)')
        if not c.get('title'):
            problems.append(f'cards[{i}]: title is required')
        if c.get('image') and not os.path.isfile(os.path.join(base, c['image'])):
            problems.append(f"cards[{i}]: image {c['image']} not found")
        if c.get('image') and c.get('prompt'):
            problems.append(f'cards[{i}]: give an image or a prompt, not both')
        prev_end = e
    t = {**DEFAULT_TOKENS, **spec.get('tokens', {})}
    declared = {f['family'] for f in spec.get('fonts', [])}
    for key in ('font_display', 'font_text'):
        for fam in named_families(t[key]):
            if fam not in declared:
                problems.append(f'tokens.{key}: "{fam}" needs a local file in "fonts" (HyperFrames renders offline), '
                                f'or use a generic family')
    for f in spec.get('fonts', []):
        if not os.path.isfile(os.path.join(base, f.get('file', ''))):
            problems.append(f"fonts: {f.get('file')} not found")
    if problems:
        die('spec problems:\n  ' + '\n  '.join(problems))


def build(spec_path: str, out: str) -> str:
    spec = json.load(open(spec_path, encoding='utf-8'))
    base = os.path.dirname(os.path.abspath(spec_path))
    cam = os.path.join(base, spec.get('camera', ''))
    if not os.path.isfile(cam):
        die(f"camera video {spec.get('camera')!r} not found")
    dur = round(duration(cam), 3)
    validate(spec, base, dur)
    W, H = int(spec.get('width', 1920)), int(spec.get('height', 1080))
    t = {**DEFAULT_TOKENS, **spec.get('tokens', {})}
    os.makedirs(os.path.join(out, 'assets'), exist_ok=True)

    def asset(rel: str) -> str:
        name = re.sub(r'[^\w.-]', '_', os.path.basename(rel))
        shutil.copy2(os.path.join(base, rel), os.path.join(out, 'assets', name))
        return 'assets/' + name

    cam_src = asset(spec['camera'])
    faces = ''.join(
        f"@font-face{{font-family:\"{f['family']}\";src:url(\"{asset(f['file'])}\");font-weight:{f.get('weight', '400')};"
        f"font-style:{f.get('style', 'normal')};font-display:block}}\n" for f in spec.get('fonts', []))

    # geometry, in canvas pixels: the camera wrapper scales from its top-left corner into the PiP slot
    s = PIP
    pip_w, pip_h = W * s, H * s
    margin = W * 0.045
    pip_x, pip_y = W - pip_w - margin, (H - pip_h) / 2
    radius = round(min(pip_w, pip_h) * 0.14 / s)   # radius before scaling, so it reads ~14% of the PiP

    cards_html, tweens = [], []
    for i, c in enumerate(spec.get('cards', [])):
        cid = f'card{i}'
        st, en = float(c['start']), float(c['end'])
        media = ''
        if c.get('image'):
            media = f'<div class="media" id="{cid}-media"><img src="{asset(c["image"])}" alt=""></div>'
        elif c.get('prompt'):
            media = (f'<div class="media prompt" id="{cid}-media"><div class="prompt-text" id="{cid}-text">'
                     f'{html.escape(c["prompt"])}</div><div class="prompt-bar"><span></span><b aria-hidden="true"><svg viewBox="0 0 24 24" width="60%" height="60%">'
                     f'<path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" '
                     f'stroke-linejoin="round"/></svg></b></div></div>')
        sub = f'<p class="sub" id="{cid}-sub">{html.escape(c.get("subtitle", ""))}</p>' if c.get('subtitle') else ''
        cards_html.append(
            f'<section class="clip card" id="{cid}" data-start="{st}" data-duration="{round(en - st, 3)}" data-track-index="2">'
            f'<div class="card-inner"><h2 class="title" id="{cid}-title">{html.escape(c["title"])}</h2>{sub}{media}</div></section>')
        # camera out to the PiP slot, with a short blur on the move
        tweens.append(f'tl.to("#camwrap", {{x: {pip_x:.1f}, y: {pip_y:.1f}, scale: {s}, borderRadius: {radius}, '
                      f'duration: {TRANSITION}, ease: "power3.inOut"}}, {st});')
        tweens.append(f'tl.to("#camfx", {{filter: "blur(14px)", duration: {TRANSITION / 2}, ease: "power1.in"}}, {st});')
        tweens.append(f'tl.to("#camfx", {{filter: "blur(0px)", duration: {TRANSITION / 2}, ease: "power1.out"}}, '
                      f'{st + TRANSITION / 2:.3f});')
        # card build
        tweens.append(f'tl.fromTo("#{cid}-title", {{y: 28, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.5, '
                      f'ease: "power3.out"}}, {st + 0.25:.3f});')
        if c.get('subtitle'):
            tweens.append(f'tl.fromTo("#{cid}-sub", {{y: 18, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.45, '
                          f'ease: "power3.out"}}, {st + 0.35:.3f});')
        if media:
            tweens.append(f'tl.fromTo("#{cid}-media", {{opacity: 0, scale: 0.96, filter: "blur(16px)"}}, '
                          f'{{opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "power2.out"}}, {st + 0.45:.3f});')
        if c.get('prompt'):
            tweens.append(f'tl.fromTo("#{cid}-text", {{clipPath: "inset(0 100% 0 0)"}}, {{clipPath: "inset(0 0% 0 0)", '
                          f'duration: {min(1.6, max(0.6, (en - st) * 0.35)):.2f}, ease: "none"}}, {st + 0.8:.3f});')
        tweens.append(f'tl.to("#{cid} .card-inner", {{opacity: 0, y: -12, duration: 0.3, ease: "power1.in"}}, '
                      f'{en - TRANSITION - 0.1:.3f});')
        # camera back to full frame
        tweens.append(f'tl.to("#camwrap", {{x: 0, y: 0, scale: 1, borderRadius: 0, duration: {TRANSITION}, '
                      f'ease: "power3.inOut"}}, {en - TRANSITION:.3f});')
        tweens.append(f'tl.to("#camfx", {{filter: "blur(14px)", duration: {TRANSITION / 2}, ease: "power1.in"}}, '
                      f'{en - TRANSITION:.3f});')
        tweens.append(f'tl.to("#camfx", {{filter: "blur(0px)", duration: {TRANSITION / 2}, ease: "power1.out"}}, '
                      f'{en - TRANSITION / 2:.3f});')

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<title>{html.escape(spec.get('title', 'Tip card film'))}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
{faces}:root {{ --bg: {t['bg']}; --ink: {t['ink']}; --ink2: {t['ink2']}; --accent: {t['accent']};
  --surface: {t['surface']}; --surface-ink: {t['surface_ink']};
  --font-display: {t['font_display']}; --font-text: {t['font_text']}; }}
body {{ margin: 0; background: var(--bg); }}
#root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--bg); font-family: var(--font-text); color: var(--ink); }}
#paper {{ position: absolute; inset: 0; background-color: var(--bg);
  background-image: radial-gradient(color-mix(in srgb, var(--ink) 16%, transparent) 1.2px, transparent 1.4px);
  background-size: {round(W / 64)}px {round(W / 64)}px; }}
#camwrap {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; overflow: hidden; transform-origin: 0 0;
  box-shadow: 0 {round(H / 40)}px {round(H / 12)}px color-mix(in srgb, var(--ink) 22%, transparent); }}
#camfx {{ position: absolute; inset: 0; }}
#cam {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.card {{ position: absolute; inset: 0; }}
.card-inner {{ position: absolute; left: {W * 0.07:.0f}px; top: 0; bottom: 0; width: {W * (1 - PIP) - W * 0.07 - margin * 2:.0f}px;
  display: flex; flex-direction: column; justify-content: center; }}
.title {{ margin: 0; font-family: var(--font-display); font-weight: 600; font-size: {H * 0.068:.0f}px; line-height: 1.05;
  letter-spacing: -0.015em; color: var(--ink); text-wrap: balance; }}
.sub {{ margin: {H * 0.014:.0f}px 0 0; font-size: {H * 0.03:.0f}px; line-height: 1.3; color: var(--ink2); }}
.media {{ margin-top: {H * 0.045:.0f}px; border-radius: {H * 0.018:.0f}px; overflow: hidden; max-height: {H * 0.5:.0f}px;
  box-shadow: 0 {H * 0.012:.0f}px {H * 0.05:.0f}px color-mix(in srgb, var(--ink) 20%, transparent); align-self: flex-start; max-width: 100%; }}
.media img {{ display: block; max-width: 100%; max-height: {H * 0.5:.0f}px; }}
.prompt {{ background: var(--surface); color: var(--surface-ink); padding: {H * 0.026:.0f}px {H * 0.03:.0f}px {H * 0.018:.0f}px;
  width: 100%; box-sizing: border-box; }}
.prompt-text {{ font-size: {H * 0.024:.0f}px; line-height: 1.45; min-height: {H * 0.07:.0f}px; }}
.prompt-bar {{ display: flex; justify-content: space-between; align-items: center; margin-top: {H * 0.018:.0f}px; }}
.prompt-bar span {{ height: {H * 0.006:.0f}px; width: 30%; border-radius: 99px; background: color-mix(in srgb, var(--surface-ink) 18%, transparent); }}
.prompt-bar b {{ display: grid; place-items: center; width: {H * 0.034:.0f}px; height: {H * 0.034:.0f}px; border-radius: {H * 0.008:.0f}px;
  background: var(--accent); color: var(--surface); font-size: {H * 0.02:.0f}px; }}
</style>
</head>
<body>
<div id="root" data-composition-id="tipfilm" data-start="0" data-width="{W}" data-height="{H}" data-duration="{dur}">
  <div id="paper"></div>
  {''.join(cards_html)}
  <div id="camwrap"><div id="camfx">
    <video id="cam" src="{cam_src}" data-start="0" data-duration="{dur}" data-track-index="1" muted playsinline></video>
  </div></div>
  <audio id="cam-audio" src="{cam_src}" data-start="0" data-duration="{dur}" data-track-index="0" data-volume="1"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.set("#camwrap", {{ x: 0, y: 0, scale: 1, borderRadius: 0 }}, 0);
tl.set("#camfx", {{ filter: "blur(0px)" }}, 0);
{chr(10).join(tweens)}
window.__timelines["tipfilm"] = tl;
</script>
</body>
</html>
"""
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(doc)
    return os.path.join(out, 'index.html')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    p = build(sys.argv[1], sys.argv[2])
    print(f'wrote {p}; next: cd {sys.argv[2]} && npx hyperframes check && npx hyperframes render --output film.mp4')
