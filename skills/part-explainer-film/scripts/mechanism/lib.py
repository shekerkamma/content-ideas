"""Mechanism primitives for DeepGrid part explainers (HyperFrames frames: HTML + seekable GSAP).

The fault-path film shows what a part DOES by animating the mechanism on the narration's words
(a wrong PWM edge, a blind gap between self-tests, a fault lighting a path). These primitives make
that vocabulary reusable, so each part is a scene spec, not a hand-built frame file.

Every primitive returns (body_html, css, timeline_js) for one frame prefix `p`, given `at`, a
function from a cue to seconds on the frame's own clock. Cues are words of the narration
("surge", "3.3", "word#2") or forced fractions of the scene ("@0.4"); make.resolve() blocks the build
on a cue word the narration never says, so a re-voice that drops a word fails loudly instead of drifting.

Design system: DeepGrid Semi tokens (ink ground, copper the one accent, teal only for a safe
state, hardware copper for power), Newsreader / Inter / JetBrains Mono. Content stays above
y = 880: the caption band is 900-1080.
"""
import html

C = dict(ink="#101212", surface="#191d1b", paper="#eeeae2", ink2="#a7b09f", muted="#a0a59b", copper="#d4a36e",
         hw="#bf7f3b", safe="#2f9e8c", line="#3d453b", frame="#566157", err="#e8a08a")
FONTS = """
@font-face{font-family:"DG Serif";src:url("assets/fonts/newsreader.woff2") format("woff2");font-weight:200 800}
@font-face{font-family:"DG Sans";src:url("assets/fonts/inter.woff2") format("woff2");font-weight:100 900}
@font-face{font-family:"DG Mono";src:url("assets/fonts/jetbrains-mono.woff2") format("woff2");font-weight:100 800}
"""
def E(s):
    """Escape text; keep µ lower-case, because text-transform:uppercase turns it into a capital mu that reads as M
    ("8 µs" rendered "8 MS" on the first SKU-6 build)."""
    return html.escape(str(s)).replace("µ", '<span style="text-transform:none">µ</span>')
X0, X1, Y0, Y1 = 120, 1800, 320, 860          # the stage; the header sits above it, captions below


def base_css(p):
    return f"""
#root{{position:absolute;inset:0;color:{C['paper']};font-family:"DG Sans",sans-serif;overflow:hidden}}
#{p}-bg{{position:absolute;inset:0;background:{C['ink']}}}
#{p}-grid{{position:absolute;inset:0;opacity:.32;background-image:linear-gradient({C['line']}22 1px,transparent 1px),linear-gradient(90deg,{C['line']}22 1px,transparent 1px);background-size:80px 80px}}
.{p}-k{{position:absolute;left:120px;top:96px;font-family:"DG Mono",monospace;font-size:24px;letter-spacing:4px;color:{C['copper']};text-transform:uppercase}}
.{p}-t{{position:absolute;left:120px;top:136px;font-family:"DG Serif",serif;font-size:76px;line-height:1.05;letter-spacing:-1.5px;color:{C['paper']};margin:0;max-width:1680px}}
.{p}-lbl{{font-family:"DG Mono",monospace;font-size:22px;letter-spacing:3px;color:{C['ink2']};text-transform:uppercase}}
.{p}-box{{position:absolute;border:2px solid {C['line']};border-radius:10px;background:{C['surface']};display:flex;flex-direction:column;justify-content:center;align-items:center;gap:8px;text-align:center;padding:10px}}
.{p}-box b{{font-family:"DG Sans",sans-serif;font-weight:700;font-size:30px;letter-spacing:.5px;color:{C['paper']}}}
.{p}-box span{{font-family:"DG Mono",monospace;font-size:20px;letter-spacing:2px;color:{C['ink2']};text-transform:uppercase}}
.{p}-stat{{position:absolute;font-family:"DG Serif",serif;color:{C['copper']};letter-spacing:-3px;line-height:.9}}
.{p}-sl{{position:absolute;font-family:"DG Mono",monospace;font-size:24px;letter-spacing:3px;color:{C['ink2']};text-transform:uppercase}}
"""


def frame(fid, p, kicker, title, body, css, tl):
    return f"""<template>
<style>
{FONTS}
{base_css(p)}
{css}
</style>
<div id="root" data-composition-id="{fid}" data-width="1920" data-height="1080">
  <div id="{p}-bg" class="clip" data-start="0" data-duration="__DUR__" data-track-index="0"></div>
  <div id="{p}-grid" class="clip" data-start="0" data-duration="__DUR__" data-track-index="1"></div>
  <div id="{p}-stage" class="clip" data-start="0" data-duration="__DUR__" data-track-index="2">
    <div class="{p}-k" id="{p}-k">{E(kicker)}</div>
    <h1 class="{p}-t" id="{p}-t">{E(title)}</h1>
{body}
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
(function(){{
  const tl = gsap.timeline({{ paused: true }});
  const E = "power3.out";
  tl.fromTo("#{p}-k",{{opacity:0,y:12}},{{opacity:1,y:0,duration:.5,ease:E}},0.1);
  tl.fromTo("#{p}-t",{{opacity:0,y:18}},{{opacity:1,y:0,duration:.7,ease:E}},0.25);
{tl}
  window.__timelines["{fid}"] = tl;
}})();
</script>
</template>
"""


# ------------------------------------------------------------------ primitives

def chain(p, at, nodes, light=(), packet=True, y=470, h=180, gap=56, ns=""):
    """Blocks in a row with arrows. `ns` keeps ids unique when two chains share a frame (classes stay the frame's). `light`: [(node_index, cue, colour?)] lights a block (copper by default)
    and, with packet=True, sends a copper dot from the previous lit block. A colour of 'safe' or 'hw' marks
    a safe state or a power element."""
    q = p + ns; n = len(nodes); w = (X1 - X0 - gap * (n - 1)) / n
    body, tl = [], []
    for i, nd in enumerate(nodes):
        x = X0 + i * (w + gap)
        body.append(f'<div class="{p}-box" id="{q}-n{i}" style="left:{x:.0f}px;top:{y}px;width:{w:.0f}px;height:{h}px;opacity:.25">'
                    f'<b>{E(nd[0])}</b>{f"<span>{E(nd[1])}</span>" if len(nd) > 1 and nd[1] else ""}</div>')
        if i:
            ax = x - gap
            body.append(f'<svg style="position:absolute;left:{ax:.0f}px;top:{y + h / 2 - 12:.0f}px" width="{gap}" height="24"><path id="{q}-a{i}" d="M4 12 H{gap - 10} M{gap - 18} 4 L{gap - 8} 12 L{gap - 18} 20" fill="none" stroke="{C["line"]}" stroke-width="3"/></svg>')
    for i in range(n):
        tl.append(f'tl.to("#{q}-n{i}",{{opacity:1,duration:.4}},{0.6 + 0.12 * i:.2f});')
    if packet:
        body.append(f'<div id="{q}-dot" style="position:absolute;left:0;top:{y + h + 26}px;width:22px;height:22px;border-radius:11px;background:{C["copper"]};opacity:0"></div>')
    prev = None
    for k, (i, cue, *col) in enumerate(light):
        t = at(cue); c = C.get(col[0], col[0]) if col else C["copper"]
        x = X0 + i * (w + gap)
        tint = f"{c}33" if c in (C["err"], C["safe"]) else C["surface"]   # a fault or a safe state reads at a glance
        tl.append(f'tl.to("#{q}-n{i}",{{borderColor:"{c}",backgroundColor:"{tint}",borderWidth:4,duration:.35}},{t:.2f});')
        tl.append(f'tl.fromTo("#{q}-n{i}",{{scale:1}},{{scale:1.04,duration:.18,yoyo:true,repeat:1}},{t:.2f});')
        if 0 < i <= n - 1:
            tl.append(f'tl.to("#{q}-a{i}",{{stroke:"{c}",duration:.3}},{max(0, t - .2):.2f});')
        if packet:
            cx = x + w / 2 - 11
            if prev is None:
                tl.append(f'tl.set("#{q}-dot",{{x:{cx:.0f},opacity:1}},{t:.2f});')
            else:
                tl.append(f'tl.to("#{q}-dot",{{x:{cx:.0f},duration:.6,ease:"power2.inOut"}},{max(0, t - .6):.2f});')
            prev = i
    return "\n".join(body), "", "\n".join(tl)


def stat(p, at, value, label, cue, x=X0, y=Y0 + 10, size=200, colour="copper"):
    t = at(cue)
    body = (f'<div class="{p}-stat" id="{p}-sv" style="left:{x}px;top:{y}px;font-size:{size}px;color:{C[colour]};opacity:0">{E(value)}</div>'
            f'<div class="{p}-sl" id="{p}-slb" style="left:{x}px;top:{y + size * .95:.0f}px;opacity:0">{E(label)}</div>')
    tl = (f'tl.fromTo("#{p}-sv",{{opacity:0,y:24}},{{opacity:1,y:0,duration:.6,ease:E}},{t:.2f});'
          f'tl.to("#{p}-slb",{{opacity:1,duration:.5}},{t + .3:.2f});')
    return body, "", tl


def counter(p, at, to, unit, label, cue, x=X0, y=Y0 + 10, size=220, dur=1.6):
    t = at(cue)
    body = (f'<div class="{p}-stat" style="left:{x}px;top:{y}px;font-size:{size}px"><span id="{p}-cn">0</span>'
            f'<span style="font-size:{size * .45:.0f}px;letter-spacing:0"> {E(unit)}</span></div>'
            f'<div class="{p}-sl" id="{p}-cl" style="left:{x}px;top:{y + size * .98:.0f}px;opacity:0">{E(label)}</div>')
    tl = (f'(function(){{const o={{v:0}};tl.to(o,{{v:{to},duration:{dur},ease:"power1.out",onUpdate:function(){{'
          f'document.getElementById("{p}-cn").textContent=Math.round(o.v).toLocaleString("en-US");}}}},{t:.2f});}})();'
          f'tl.to("#{p}-cl",{{opacity:1,duration:.5}},{t + .4:.2f});')
    return body, "", tl


def wave(p, at, kind, events=(), label="", x=X0, y=Y0 + 40, w=X1 - X0, h=420):
    """An animated trace. kinds: square, sine3, ripple, surge, chirp, diff, ramp.
    events: kind-specific cue -> effect (see each branch)."""
    body, tl = [], []
    svg = [f'<svg id="{p}-w" style="position:absolute;left:{x}px;top:{y}px" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           f'<line x1="0" y1="{h - 2}" x2="{w}" y2="{h - 2}" stroke="{C["line"]}" stroke-width="2"/>']
    mid = h / 2
    def path(d, pid, col, width=4, dash=False):
        svg.append(f'<path id="{p}-{pid}" d="{d}" fill="none" stroke="{col}" stroke-width="{width}"{" stroke-dasharray=\"10 8\"" if dash else ""}/>')
    def draw(pid, t, dur=2.2):
        tl.append(f'(function(){{const e=document.getElementById("{p}-{pid}");const L=e.getTotalLength();'
                  f'tl.fromTo(e,{{strokeDasharray:L,strokeDashoffset:L}},{{strokeDashoffset:0,duration:{dur},ease:"none"}},{t:.2f});}})();')
    import math
    if kind == "sine3":                      # three phases appear; events: [("build", cue)]
        for k, col in enumerate([C["copper"], C["ink2"], C["hw"]]):
            pts = " ".join(f"{i * w / 240:.1f},{mid - (h * .38) * math.sin(2 * math.pi * (i / 80) - k * 2.094):.1f}" for i in range(241))
            path("M" + pts.replace(" ", " L"), f"s{k}", col, 4)
        t = at(dict(events).get("build", "0.15"))
        for k in range(3): draw(f"s{k}", t + .25 * k, 2.4)
    elif kind == "square":                   # PWM; events: [("draw", cue)]
        seg = w / 12; d = f"M0 {h - 40}"
        for i in range(12):
            d += f" H{i * seg + seg * .3:.0f} V{60} H{i * seg + seg * .8:.0f} V{h - 40}"
        path(d + f" H{w}", "sq", C["copper"]); draw("sq", at(dict(events).get("draw", "0.15")))
    elif kind == "slew":                     # slope-shaped edges (trapezoid), a hard square ghost; events: [("draw", cue)]
        seg = w / 8; ghost = f"M0 {h - 40}"; d = f"M0 {h - 40}"; r = seg * .18
        for i in range(8):
            ghost += f" H{i * seg + seg * .2:.0f} V60 H{i * seg + seg * .7:.0f} V{h - 40}"
            d += f" H{i * seg + seg * .2 - r / 2:.0f} L{i * seg + seg * .2 + r / 2:.0f} 60 H{i * seg + seg * .7 - r / 2:.0f} L{i * seg + seg * .7 + r / 2:.0f} {h - 40}"
        path(ghost + f" H{w}", "gh", C["line"], 2, dash=True); path(d + f" H{w}", "sl", C["copper"])
        t = at(dict(events).get("draw", "0.15")); draw("gh", t, 1.6); draw("sl", t + .6, 2.4)
    elif kind == "ripple":                   # supply rail with ripple; events: ("dip", cue) a brownout, ("window", cue)
        ev = dict(events); base = h * .32
        pts = " ".join(f"{i * w / 300:.1f},{base + 10 * math.sin(i * .9):.1f}" for i in range(301))
        path("M" + pts.replace(" ", " L"), "rp", C["copper"], 3); draw("rp", at(ev.get("draw", "0.1")), 2.0)
        if "dip" in ev:
            dx = w * .62
            path(f"M{dx - 60} {base} L{dx} {h * .78} L{dx + 220} {h * .78} L{dx + 280} {base}", "dip", C["err"], 5)
            draw("dip", at(ev["dip"]), .8)
        if "glitch" in ev:
            gx = w * .25
            path(f"M{gx} {base} L{gx + 12} {h * .7} L{gx + 24} {base}", "gl", C["ink2"], 4)
            draw("gl", at(ev["glitch"]), .4)
    elif kind == "surge":                    # flat bus, a surge spike, a clamp ceiling; events: ("spike", cue), ("clamp", cue)
        ev = dict(events); base = h * .62; cl = h * .32
        path(f"M0 {base} H{w * .45} L{w * .5} {h * .04} L{w * .56} {base} H{w}", "raw", C["err"], 4, dash=True)
        path(f"M0 {base} H{w * .45} L{w * .47} {cl} H{w * .54} L{w * .56} {base} H{w}", "cl", C["copper"], 5)
        svg.append(f'<line id="{p}-ceil" x1="0" y1="{cl}" x2="{w}" y2="{cl}" stroke="{C["safe"]}" stroke-width="2" stroke-dasharray="6 8" opacity="0"/>')
        draw("raw", at(ev.get("spike", "0.2")), 1.2)
        tl.append(f'tl.to("#{p}-ceil",{{opacity:1,duration:.4}},{at(ev.get("clamp", "0.5")):.2f});')
        draw("cl", at(ev.get("clamp", "0.5")) + .2, 1.2)
        tl.append(f'tl.to("#{p}-raw",{{opacity:.25,duration:.4}},{at(ev.get("clamp", "0.5")) + .3:.2f});')
    elif kind == "chirp":                    # sawtooth frequency ramps; events: ("draw", cue), ("echo", cue)
        ev = dict(events); d = f"M0 {h - 30}"
        for i in range(5):
            d += f" L{(i + 1) * w / 5 - 6:.0f} 40 L{(i + 1) * w / 5:.0f} {h - 30}"
        path(d, "ch", C["copper"]); draw("ch", at(ev.get("draw", "0.15")), 2.6)
        if "echo" in ev:
            d2 = f"M{w * .06:.0f} {h - 30}"
            for i in range(5):
                d2 += f" L{(i + 1) * w / 5 - 6 + w * .06:.0f} 40 L{(i + 1) * w / 5 + w * .06:.0f} {h - 30}"
            path(d2, "ec", C["ink2"], 3, dash=True); draw("ec", at(ev["echo"]), 2.2)
    elif kind == "diff":                     # differential pair; events: ("draw", cue), ("shift", cue)
        ev = dict(events); seg = w / 10; a = f"M0 {mid - 60}"; b = f"M0 {mid + 60}"
        for i in range(10):
            hi, lo = (mid - 60, mid + 60) if i % 2 == 0 else (mid + 60, mid - 60)
            a += f" L{i * seg + seg * .15:.0f} {hi} H{(i + 1) * seg:.0f}"; b += f" L{i * seg + seg * .15:.0f} {lo} H{(i + 1) * seg:.0f}"
        path(a, "da", C["copper"]); path(b, "db", C["ink2"]); draw("da", at(ev.get("draw", "0.15"))); draw("db", at(ev.get("draw", "0.15")) + .2)
        if "shift" in ev:
            tl.append(f'tl.to("#{p}-w",{{y:-60,duration:.8,ease:"sine.inOut",yoyo:true,repeat:1}},{at(ev["shift"]):.2f});')
    svg.append("</svg>")
    body.append("".join(svg))
    if label:
        body.append(f'<div class="{p}-lbl" style="position:absolute;left:{x}px;top:{y + h + 14}px">{E(label)}</div>')
    return "\n".join(body), "", "\n".join(tl)


def timeline(p, at, span_label, marks=(), windows=(), sweep=None, y=560):
    """A time axis. marks: [(frac, text, cue, colour?)] ticks; windows: [(f0, f1, text, cue, colour?)] shaded
    spans; sweep: cue at which a cursor runs the axis."""
    body, tl = [], []
    w = X1 - X0
    body.append(f'<div id="{p}-ax" style="position:absolute;left:{X0}px;top:{y}px;width:{w}px;height:3px;background:{C["line"]};transform-origin:left"></div>')
    body.append(f'<div class="{p}-lbl" style="position:absolute;left:{X0}px;top:{y + 160}px">{E(span_label)}</div>')
    tl.append(f'tl.fromTo("#{p}-ax",{{scaleX:0}},{{scaleX:1,duration:1.0,ease:E}},0.5);')   # GSAP owns the transform (lint: css/gsap conflict)
    for k, (f0, f1, text, cue, *col) in enumerate(windows):
        c = C.get(col[0], col[0]) if col else C["copper"]
        body.append(f'<div id="{p}-wd{k}" style="position:absolute;left:{X0 + f0 * w:.0f}px;top:{y - 120}px;width:{(f1 - f0) * w:.0f}px;height:120px;background:{c}22;border:2px solid {c};border-bottom:0;opacity:0"></div>'
                    f'<div class="{p}-lbl" id="{p}-wt{k}" style="position:absolute;left:{X0 + f0 * w:.0f}px;top:{y - 160}px;color:{c};opacity:0">{E(text)}</div>')
        tl.append(f'tl.to(["#{p}-wd{k}","#{p}-wt{k}"],{{opacity:1,duration:.45}},{at(cue):.2f});')
    for k, (f, text, cue, *col) in enumerate(marks):
        c = C.get(col[0], col[0]) if col else C["paper"]
        body.append(f'<div id="{p}-m{k}" style="position:absolute;left:{X0 + f * w - 2:.0f}px;top:{y - 70}px;width:4px;height:140px;background:{c};opacity:0"></div>'
                    f'<div class="{p}-lbl" id="{p}-mt{k}" style="position:absolute;left:{X0 + f * w - 2:.0f}px;top:{y + 84}px;color:{c};opacity:0">{E(text)}</div>')
        tl.append(f'tl.to(["#{p}-m{k}","#{p}-mt{k}"],{{opacity:1,duration:.35}},{at(cue):.2f});')
    if sweep:
        body.append(f'<div id="{p}-cur" style="position:absolute;left:{X0}px;top:{y - 90}px;width:3px;height:180px;background:{C["copper"]};opacity:0"></div>')
        tl.append(f'tl.set("#{p}-cur",{{opacity:1}},{at(sweep):.2f});tl.to("#{p}-cur",{{x:{w},duration:3.5,ease:"none"}},{at(sweep):.2f});')
    return "\n".join(body), "", "\n".join(tl)


def rails(p, at, items, x=X0 + 40, y=Y0 + 20, h=480):
    """Rails ramping in order: items [(name, rel_height 0-1, cue)]; each ends with a power-good tick."""
    n = len(items); colw = (X1 - X0 - 80) / n
    body, tl = [], []
    for i, (name, lvl, cue) in enumerate(items):
        cx = x + i * colw; bh = h * lvl
        body.append(f'<div id="{p}-r{i}" style="position:absolute;left:{cx + colw * .2:.0f}px;top:{y + h - bh:.0f}px;width:{colw * .6:.0f}px;height:{bh:.0f}px;'
                    f'background:linear-gradient({C["copper"]},{C["hw"]});transform-origin:bottom;border-radius:4px"></div>'
                    f'<div class="{p}-lbl" style="position:absolute;left:{cx + colw * .2:.0f}px;top:{y + h + 16:.0f}px;width:{colw * .6:.0f}px;text-align:center;color:{C["paper"]};font-size:26px">{E(name)}</div>'
                    f'<div id="{p}-pg{i}" class="{p}-lbl" style="position:absolute;left:{cx + colw * .2:.0f}px;top:{y + h - bh - 44:.0f}px;width:{colw * .6:.0f}px;text-align:center;color:{C["safe"]};opacity:0">PG ✓</div>')
        t = at(cue)
        tl.append(f'tl.fromTo("#{p}-r{i}",{{scaleY:0}},{{scaleY:1,duration:1.1,ease:"power2.out"}},{t:.2f});tl.to("#{p}-pg{i}",{{opacity:1,duration:.3}},{t + 1.1:.2f});')
    return "\n".join(body), "", "\n".join(tl)


def stream(p, at, lanes, chips, slot=None, y=Y0 + 40):
    """Messages crossing lanes left to right. lanes: [name]; chips: [(lane, text, cue, colour?)];
    slot: (lane, cue, text) highlights a reserved time slot in a lane."""
    body, tl = [], []
    lh = min(110, (Y1 - y - 40) / max(1, len(lanes)))
    for i, name in enumerate(lanes):
        ly = y + i * lh
        body.append(f'<div class="{p}-lbl" style="position:absolute;left:{X0}px;top:{ly + lh / 2 - 12:.0f}px;width:260px">{E(name)}</div>'
                    f'<div style="position:absolute;left:{X0 + 280}px;top:{ly + lh / 2:.0f}px;width:{X1 - X0 - 280}px;height:2px;background:{C["line"]}"></div>')
    if slot:
        ln, cue, text = slot; ly = y + ln * lh
        body.append(f'<div id="{p}-slot" style="position:absolute;left:{X0 + 760}px;top:{ly + 8:.0f}px;width:280px;height:{lh - 16:.0f}px;border:2px dashed {C["safe"]};border-radius:8px;opacity:0"></div>'
                    f'<div class="{p}-lbl" id="{p}-slt" style="position:absolute;left:{X0 + 760}px;top:{ly - 26:.0f}px;color:{C["safe"]};opacity:0">{E(text)}</div>')
        tl.append(f'tl.to(["#{p}-slot","#{p}-slt"],{{opacity:1,duration:.4}},{at(cue):.2f});')
    for k, (ln, text, cue, *col) in enumerate(chips):
        c = C.get(col[0], col[0]) if col else C["copper"]; ly = y + ln * lh
        body.append(f'<div id="{p}-c{k}" style="position:absolute;left:{X0 + 280}px;top:{ly + lh / 2 - 26:.0f}px;padding:10px 18px;border-radius:6px;border:2px solid {c};background:{C["surface"]};'
                    f'font-family:DG Mono,monospace;font-size:22px;letter-spacing:2px;color:{c};text-transform:uppercase;opacity:0;white-space:nowrap">{E(text)}</div>')
        t = at(cue)
        tl.append(f'tl.set("#{p}-c{k}",{{opacity:1}},{t:.2f});tl.to("#{p}-c{k}",{{x:{X1 - X0 - 520},duration:4.2,ease:"none"}},{t:.2f});'
                  f'tl.to("#{p}-c{k}",{{opacity:0,duration:.3}},{t + 4.0:.2f});')
    return "\n".join(body), "", "\n".join(tl)


def gridmap(p, at, rows, cols, hits, fill_cue, label="", x=X0 + 520, y=Y0 + 10, w=900, h=500):
    """A map that fills cell by cell, then target hits light: hits [(r, c, cue)]."""
    body, tl = [], []
    cw, ch = w / cols, h / rows
    for r in range(rows):
        for c in range(cols):
            body.append(f'<div class="{p}-cell" style="position:absolute;left:{x + c * cw:.0f}px;top:{y + r * ch:.0f}px;width:{cw - 3:.0f}px;height:{ch - 3:.0f}px;background:{C["surface"]};opacity:0"></div>')
    tl.append(f'tl.to(".{p}-cell",{{opacity:1,duration:.05,stagger:{{each:0.012,from:"start"}}}},{at(fill_cue):.2f});')
    for k, (r, c, cue) in enumerate(hits):
        body.append(f'<div id="{p}-h{k}" style="position:absolute;left:{x + c * cw:.0f}px;top:{y + r * ch:.0f}px;width:{cw - 3:.0f}px;height:{ch - 3:.0f}px;background:{C["copper"]};opacity:0"></div>')
        tl.append(f'tl.to("#{p}-h{k}",{{opacity:1,duration:.3}},{at(cue):.2f});')
    if label:
        body.append(f'<div class="{p}-lbl" style="position:absolute;left:{x}px;top:{y + h + 14}px">{E(label)}</div>')
    return "\n".join(body), "", "\n".join(tl)


def items(p, at, rows, y=Y0 + 10):
    """Numbered rows that appear on cues: [(text, cue)]. For the closing scene."""
    body, tl = [], []
    for k, (text, cue) in enumerate(rows):
        yy = y + k * 150
        body.append(f'<div id="{p}-i{k}" style="position:absolute;left:{X0}px;top:{yy}px;width:{X1 - X0}px;display:flex;gap:36px;align-items:baseline;border-top:1px solid {C["line"]};padding-top:26px;opacity:0">'
                    f'<span style="font-family:DG Serif,serif;font-size:64px;color:{C["copper"]}">{k + 1:02d}</span>'
                    f'<span style="font-family:DG Sans,sans-serif;font-size:42px;color:{C["paper"]}">{E(text)}</span></div>')
        tl.append(f'tl.fromTo("#{p}-i{k}",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.5,ease:E}},{at(cue):.2f});')
    return "\n".join(body), "", "\n".join(tl)


def compose(*parts):
    """Join several primitives' (body, css, tl) into one."""
    return "\n".join(x[0] for x in parts), "\n".join(x[1] for x in parts), "\n".join(x[2] for x in parts)
