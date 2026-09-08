#!/usr/bin/env python3
"""Beats + measured manifest -> composition HTML and one assembled narration track.

Card types: title | rule | quote | list | stats | gate | risk | cta

Every data-start and data-duration comes from the manifest. Nothing here decides
a time; this script only lays out what measure_beats.py already determined.

Usage: build_film.py <beats.json> <manifest.json> <audio-dir> <out-dir> [--gap 0.55]
  beats.json entries: {"id","film","v","head","sub","items","stats","cta","kicker","meta"}
"""
import argparse, html, json, pathlib, subprocess, sys

H = lambda s: html.escape(str(s)) if s else ""

CSS = """*{box-sizing:border-box}html,body{margin:0;width:1920px;height:1080px;overflow:hidden;
background:#f6f5f9;color:#191822;font-family:'Helvetica Neue',Arial,sans-serif}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:#f6f5f9}
.clip{position:absolute;inset:0}.pg{position:absolute;inset:0;background:#f6f5f9}
.hdr{position:absolute;top:56px;left:96px;right:96px;display:flex;justify-content:space-between;align-items:baseline}
.bd{font-size:24px;letter-spacing:10px}.code{font-size:20px;letter-spacing:4px;color:#9c5716;font-weight:600}
.meta{position:absolute;top:104px;left:96px;right:96px;display:flex;justify-content:space-between;font-size:17px;color:#8b8a96;letter-spacing:1px}
.bar{position:absolute;left:96px;right:96px;bottom:56px;height:2px;background:#e2dde7}
.fill{height:2px;background:#9c5716;width:100%;transform-origin:left center}
.body{position:absolute;left:96px;right:96px;top:190px;bottom:120px;display:flex;flex-direction:column;justify-content:center}
.kick{font-size:19px;letter-spacing:5px;color:#9c5716;margin:0 0 26px}
.ttl{font-family:Georgia,serif;font-size:104px;line-height:1.05;letter-spacing:-3px;margin:0;max-width:1560px;font-weight:normal}
.hd{font-family:Georgia,serif;font-size:74px;line-height:1.12;letter-spacing:-2px;margin:0;max-width:1580px;font-weight:normal}
.sub{font-size:32px;line-height:1.55;color:#4a4956;margin:30px 0 0;max-width:1420px}
ul.it{margin:34px 0 0;padding:0;list-style:none;max-width:1620px}
ul.it li{font-size:31px;line-height:1.45;padding:22px 0 22px 44px;border-top:1px solid #e2dde7;position:relative;color:#2c2b38}
ul.it li:before{content:'';position:absolute;left:4px;top:36px;width:16px;height:2px;background:#9c5716}
.stats{display:flex;gap:56px;margin-top:10px}
.stat{flex:1;border-top:2px solid #9c5716;padding-top:26px}
.sv{font-family:Georgia,serif;font-size:88px;line-height:1;color:#9c5716;margin:0;letter-spacing:-3px}
.sl{font-size:27px;margin:16px 0 0;font-weight:600}
.sn{font-size:21px;line-height:1.45;color:#7a7986;margin:10px 0 0}
.band{border-left:4px solid #9c5716;padding:6px 0 6px 40px}
.riskband{border-left:4px solid #b03a2e;padding:6px 0 6px 40px}
.btn{display:inline-block;margin-top:44px;background:#9c5716;color:#fff;font-size:32px;padding:26px 52px}
.shot{position:absolute;right:96px;bottom:120px;width:520px;height:400px;overflow:hidden;opacity:.16}
.shot img{position:absolute;width:100%;top:50%;transform:translateY(-50%)}"""


def card(b):
    v = b.get("v", "quote")
    kick = f'<p class="kick" data-a>{H(b["kicker"])}</p>' if b.get("kicker") else ""
    if v in ("title", "cta"):
        cta = f'<div><span class="btn" data-a>{H(b["cta"])}</span></div>' if b.get("cta") else ""
        sub = f'<p class="sub" data-a>{H(b["sub"])}</p>' if b.get("sub") else ""
        return (f'<div class="body">{kick}'
                f'<h1 class="ttl" data-a>{H(b.get("head"))}</h1>{sub}{cta}</div>')
    if v in ("list", "rule"):
        li = "".join(f'<li data-a>{H(x)}</li>' for x in b.get("items", []))
        return f'<div class="body">{kick}<h2 class="hd" data-a>{H(b.get("head"))}</h2><ul class="it">{li}</ul></div>'
    if v == "stats":
        st = "".join(f'<div class="stat" data-a><p class="sv">{H(x[0])}</p>'
                     f'<p class="sl">{H(x[1])}</p><p class="sn">{H(x[2])}</p></div>'
                     for x in b.get("stats", []))
        return f'<div class="body">{kick}<div class="stats">{st}</div></div>'
    if v in ("gate", "risk"):
        cls = "riskband" if v == "risk" else "band"
        return (f'<div class="body"><div class="{cls}">{kick}'
                f'<h2 class="hd" data-a>{H(b.get("head"))}</h2>'
                f'<p class="sub" data-a>{H(b.get("sub"))}</p></div></div>')
    return (f'<div class="body">{kick}<h2 class="hd" data-a>{H(b.get("head"))}</h2>'
            f'<p class="sub" data-a>{H(b.get("sub"))}</p></div>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("beats"); ap.add_argument("manifest")
    ap.add_argument("audio_dir"); ap.add_argument("out_dir")
    ap.add_argument("--gap", type=float, default=0.55)
    a = ap.parse_args()

    beats = json.loads(pathlib.Path(a.beats).read_text())
    man = json.loads(pathlib.Path(a.manifest).read_text())
    audio = pathlib.Path(a.audio_dir); out_root = pathlib.Path(a.out_dir)

    by_film = {}
    for b in beats:
        by_film.setdefault(b.get("film") or b["id"].rsplit("-", 1)[0], []).append(b)

    for fid, fbeats in by_film.items():
        if fid not in man:
            sys.exit(f"BLOCKED: no manifest entry for {fid}")
        m = man[fid]; total = m["total"] + 0.8
        secs, tl = [], []
        for i, b in enumerate(fbeats):
            e = m["beats"][i]
            st, du = e["start"], (total - e["start"] if i == len(fbeats) - 1 else e["dur"])
            head = b.get("meta") or {}
            secs.append(
                f'<section class="clip" id="b{i}" data-start="{st:.3f}" data-duration="{du:.3f}" data-track-index="1">'
                f'<div class="pg"></div>'
                + ('<div class="shot"><img src="hero.png" alt=""></div>' if b.get("hero") else "")
                + f'<div class="hdr"><span class="bd">{H(head.get("brand","")) }</span>'
                  f'<span class="code">{H(head.get("code",""))}</span></div>'
                  f'<div class="meta"><span>{H(head.get("left",""))}</span>'
                  f'<span>{H(head.get("right",""))}</span></div>{card(b)}</section>')
            n = max(len(b.get("items", [])) or len(b.get("stats", [])), 4)
            stag = min(0.9, max(0.18, (du - 2.5) / n))
            tl.append(f"tl.fromTo('#b{i} [data-a]',{{y:24,opacity:0}},"
                      f"{{y:0,opacity:1,duration:.6,stagger:{stag:.2f},ease:'power3.out'}},{st:.3f});")

        d = out_root / fid; d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(
            '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=1920, height=1080">'
            f'<title>{H(fid)}</title><script src="gsap.min.js"></script><style>{CSS}</style></head><body>'
            f'<div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" '
            f'data-width="1920" data-height="1080">{"".join(secs)}'
            f'<section class="clip" data-start="0" data-duration="{total:.3f}" data-track-index="2">'
            f'<div class="bar"><div class="fill" id="pf"></div></div></section></div><script>'
            'window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});'
            f'{"".join(tl)}tl.fromTo("#pf",{{scaleX:0}},{{scaleX:1,duration:{total:.3f},ease:"none"}},0);'
            'window.__timelines.main=tl;</script></body></html>')

        inputs, filt = [], []
        for i, b in enumerate(fbeats):
            inputs += ["-i", str(audio / f"{b['id']}.wav")]
            filt.append(f"[{i}:a]apad=pad_dur={a.gap}[a{i}]")
        fc = ";".join(filt) + ";" + "".join(f"[a{i}]" for i in range(len(fbeats))) \
             + f"concat=n={len(fbeats)}:v=0:a=1[out]"
        subprocess.run(["ffmpeg", "-v", "error", *inputs, "-filter_complex", fc,
                        "-map", "[out]", "-ar", "24000", "-ac", "1", "-y",
                        str(d / "narration.wav")], check=True)
        print(f"{fid:<10} {total/60:5.2f} min  {len(fbeats)} beats -> {d}")


if __name__ == "__main__":
    main()
