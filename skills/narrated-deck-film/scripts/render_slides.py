#!/usr/bin/env python3
"""Render structural slides (executive summary, act dividers, conclusion) as
PNGs in the host deck's own design system.

Tokens are derived from the deck, not invented -- see the skill's judgment
rules. Chromium headless, no Playwright dependency.
"""
import argparse
import base64
import glob
import html
import json
import os
import subprocess
import sys
import tempfile

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "fonts")


def font_face_css(font_dir):
    """Embed every bundled TTF as a data URI.

    Chromium here does not resolve fontconfig families: a page asking for
    Poppins renders pixel-identical to the serif control. It fails silently,
    so the deck's typeface must travel inside the document.
    """
    faces, seen = [], []
    for path in sorted(glob.glob(os.path.join(font_dir, "*.ttf"))):
        name = os.path.basename(path)[:-4]
        fam, _, style = name.partition("-")
        weight = {"Regular": 400, "Medium": 500, "SemiBold": 600,
                  "Bold": 700}.get(style, 400)
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        faces.append(f"@font-face{{font-family:'{fam}';font-weight:{weight};"
                     f"font-style:normal;font-display:block;"
                     f"src:url(data:font/ttf;base64,{b64}) format('truetype')}}")
        seen.append(f"{fam} {weight}")
    if not faces:
        sys.exit(f"BLOCKED: no fonts in {font_dir}. The deck typeface would "
                 f"silently fall back to serif.")
    return "".join(faces), seen

CHROME_CANDIDATES = [
    os.environ.get("DECK_CHROMIUM", ""),
    os.path.expanduser("~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome"),
    "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome",
]

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1920px;height:1080px;background:var(--bg);font-family:'Poppins',sans-serif;
     color:var(--ink);overflow:hidden;position:relative}
.pad{position:absolute;inset:0;padding:62px 80px 76px;display:flex;flex-direction:column}
h1{font-family:'Poppins',sans-serif;font-weight:600;font-size:47px;line-height:1.12;
   letter-spacing:-.5px;max-width:1450px}
.sub{font-size:19px;color:var(--muted);margin-top:16px;max-width:1300px;line-height:1.5}
.kicker{position:absolute;top:62px;right:80px;background:var(--pill);color:#fff;
  font-size:14px;font-weight:600;letter-spacing:3.4px;padding:13px 26px;border-radius:24px}
.foot{position:absolute;left:80px;right:80px;bottom:34px;display:flex;
  justify-content:space-between;font-size:13px;color:var(--foot)}
.lede{position:absolute;left:80px;bottom:74px;font-size:17px;font-weight:600;color:var(--ink)}
/* stat grid */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:26px;margin-top:58px;flex:0 0 auto}
.stat{background:var(--neutral);border:1px solid var(--line);border-radius:18px;padding:40px 32px 32px;
      display:flex;flex-direction:column;min-height:452px}
.stat .n{font-size:62px;font-weight:600;letter-spacing:-2px;line-height:1}
.stat .l{font-size:19px;font-weight:600;margin-top:20px;line-height:1.35}
.stat .d{font-size:16.5px;color:var(--muted);margin-top:16px;line-height:1.55;flex:1}
.stat .s{font-size:13.5px;color:var(--foot);margin-top:16px;font-family:'IBM Plex Mono',monospace;
   letter-spacing:.2px;border-top:1px solid var(--line);padding-top:11px}
.band{margin-top:auto;flex-shrink:0;background:var(--green);border:1px solid var(--greenline);
  border-radius:16px;padding:24px 30px;font-size:19px;line-height:1.5}
.band b{font-weight:600}
/* divider */
.divwrap{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;
  padding:0 80px}
.divwrap .act{font-size:14px;font-weight:600;letter-spacing:4px;color:var(--muted)}
.divwrap h1{font-size:76px;max-width:1500px;margin-top:24px}
.rule{width:190px;height:5px;background:var(--ink);margin:44px 0 34px;border-radius:3px}
.divwrap p{font-size:23px;color:var(--muted);max-width:1180px;line-height:1.55}
/* native table */
.tbl{flex:1;margin-top:30px;overflow:hidden;display:flex;flex-direction:column;justify-content:center}
.tbl table{width:100%;border-collapse:collapse;font-size:25px}
.tbl th{text-align:left;font-size:15px;font-weight:600;letter-spacing:2.4px;
  color:var(--muted);padding:0 22px 18px 0;border-bottom:2px solid var(--line)}
.tbl td{padding:22px 22px 22px 0;border-bottom:1px solid var(--line);
  color:var(--ink);vertical-align:top;line-height:1.4}
.tbl td.mono{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:23px;
  color:var(--ink);white-space:nowrap}
.tbl td.dim{color:var(--muted)}
.tbl tr:last-child td{border-bottom:none}
.tblnote{margin-top:16px;font-size:16px;color:var(--muted);flex-shrink:0}
/* pull quote */
.quote{flex:1;display:flex;flex-direction:column;justify-content:center;max-width:1500px}
.quote .q{font-size:62px;font-weight:600;line-height:1.18;letter-spacing:-1px}
.quote .attr{margin-top:34px;font-size:19px;color:var(--muted)}
/* full-bleed screenshot */
.bleed{position:absolute;inset:0}
.bleed img{width:100%;height:100%;object-fit:cover}
.bleedcap{position:absolute;left:0;right:0;bottom:0;padding:52px 80px 40px;
  background:linear-gradient(transparent,rgba(6,18,30,.93) 42%)}
.bleedkick{font-size:14px;font-weight:600;letter-spacing:3.4px;color:#7fe3c0;margin-bottom:14px}
.bleedcap h1{color:#fff;font-size:44px;max-width:1400px}
.bleedcap .sub{color:rgba(255,255,255,.86);margin-top:12px;max-width:1250px}
/* screenshot slide */
.shotwrap{flex:1;margin-top:30px;display:flex;align-items:center;justify-content:center;
  background:var(--neutral);border:1px solid var(--line);border-radius:16px;overflow:hidden;
  padding:20px}
.shotwrap img{max-width:100%;max-height:100%;object-fit:contain;border-radius:8px;
  box-shadow:0 2px 14px rgba(13,43,69,.10)}
.shotnote{margin-top:18px;font-size:16px;color:var(--muted);flex-shrink:0}
/* timeline */
.tl{margin-top:96px;flex:1;display:flex;flex-direction:column;justify-content:center}
.tlline{position:absolute;top:26px;left:2%;right:2%;height:3px;background:var(--line);z-index:1}
.tlrow{display:grid;grid-template-columns:repeat(4,1fr);position:relative}
.tlc{padding:0 22px;text-align:center}
.dot{width:19px;height:19px;border-radius:50%;background:var(--ink);margin:18px auto 26px;
  position:relative;z-index:2}
.tlc .d{font-size:25px;font-weight:600}
.tlc .t{font-size:17px;color:var(--muted);margin-top:14px;line-height:1.55}
.ask{margin-top:auto;flex-shrink:0;background:var(--pill);color:#fff;border-radius:18px;padding:34px 40px;
  display:flex;align-items:center;gap:44px}
.ask .big{font-size:52px;font-weight:600;letter-spacing:-1.5px;white-space:nowrap}
.ask .txt{font-size:18.5px;line-height:1.5;opacity:.93}
"""

TOKENS = {"bg": "#ffffff", "ink": "#0d2b45", "muted": "#5b6b7c", "foot": "#9eabb8",
          "pill": "#12263a", "neutral": "#f6f8fa", "line": "#e2e8ee",
          "green": "#eef6f1", "greenline": "#cfe4d8"}


def page(body, tok, faces, extra=""):
    v = ";".join(f"--{k}:{x}" for k, x in tok.items())
    return (f"<!doctype html><meta charset=utf-8><style>{faces}"
            f":root{{{v}}}{CSS}{extra}</style><body>{body}</body>")


def foot(s):
    return (f'<div class="foot"><span>{html.escape(s["footer"])}</span>'
            f'<span>{html.escape(s.get("page",""))}</span></div>')


def build(s):
    k = f'<div class="kicker">{html.escape(s["kicker"])}</div>' if s.get("kicker") else ""
    if s["template"] == "divider":
        return (f'<div class="divwrap"><div class="act">{html.escape(s["act"])}</div>'
                f'<h1>{html.escape(s["title"])}</h1><div class="rule"></div>'
                f'<p>{html.escape(s["body"])}</p></div>{k}{foot(s)}')
    if s["template"] == "stats":
        cards = "".join(
            f'<div class="stat"><div class="n">{html.escape(c["n"])}</div>'
            f'<div class="l">{html.escape(c["l"])}</div>'
            f'<div class="d">{html.escape(c["d"])}</div>'
            f'<div class="s">{html.escape(c["s"])}</div></div>' for c in s["cards"])
        band = f'<div class="band">{s["band"]}</div>' if s.get("band") else ""
        return (f'<div class="pad"><h1>{html.escape(s["title"])}</h1>'
                f'<div class="sub">{html.escape(s["subtitle"])}</div>'
                f'<div class="stats">{cards}</div>{band}</div>{k}{foot(s)}')
    if s["template"] == "table":
        head = "".join(f"<th>{html.escape(h)}</th>" for h in s["columns"])
        rows = ""
        for r in s["rows"]:
            tds = ""
            for i, cell in enumerate(r):
                cls = (s.get("col_class") or {}).get(str(i), "")
                tds += f'<td class="{cls}">{html.escape(str(cell))}</td>'
            rows += f"<tr>{tds}</tr>"
        note = (f'<div class="tblnote">{html.escape(s["note"])}</div>'
                if s.get("note") else "")
        return (f'<div class="pad"><h1>{html.escape(s["title"])}</h1>'
                f'<div class="sub">{html.escape(s.get("subtitle",""))}</div>'
                f'<div class="tbl"><table><thead><tr>{head}</tr></thead>'
                f'<tbody>{rows}</tbody></table></div>{note}</div>{k}{foot(s)}')
    if s["template"] == "quote":
        return (f'<div class="pad"><div class="quote">'
                f'<div class="q">{html.escape(s["quote"])}</div>'
                f'<div class="attr">{html.escape(s.get("attribution",""))}</div>'
                f'</div></div>{k}{foot(s)}')
    if s["template"] == "bleed":
        import base64 as _b
        b64 = _b.b64encode(open(s["image"], "rb").read()).decode()
        kick = (f'<div class="bleedkick">{html.escape(s["kicker"])}</div>'
                if s.get("kicker") else "")
        return (f'<div class="bleed"><img src="data:image/png;base64,{b64}"></div>'
                f'<div class="bleedcap">{kick}<h1>{html.escape(s["title"])}</h1>'
                f'<div class="sub">{html.escape(s.get("subtitle",""))}</div></div>')
    if s["template"] == "shot":
        import base64 as _b64
        with open(s["image"], "rb") as fh:
            b64 = _b64.b64encode(fh.read()).decode()
        note = (f'<div class="shotnote">{html.escape(s["note"])}</div>'
                if s.get("note") else "")
        return (f'<div class="pad"><h1>{html.escape(s["title"])}</h1>'
                f'<div class="sub">{html.escape(s.get("subtitle",""))}</div>'
                f'<div class="shotwrap"><img src="data:image/png;base64,{b64}"></div>'
                f'{note}</div>{k}{foot(s)}')
    if s["template"] == "timeline":
        cols = "".join(
            f'<div class="tlc"><div class="dot"></div><div class="d">{html.escape(c["d"])}</div>'
            f'<div class="t">{html.escape(c["t"])}</div></div>' for c in s["milestones"])
        return (f'<div class="pad"><h1>{html.escape(s["title"])}</h1>'
                f'<div class="sub">{html.escape(s["subtitle"])}</div>'
                f'<div class="tl">'
                f'<div class="tlrow"><div class="tlline"></div>{cols}</div></div>'
                f'<div class="ask"><div class="big">{html.escape(s["ask"])}</div>'
                f'<div class="txt">{html.escape(s["ask_body"])}</div></div>'
                f'</div>{k}{foot(s)}')
    sys.exit(f"BLOCKED: unknown template {s['template']}")


def chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    sys.exit("BLOCKED: no Chromium found. Set DECK_CHROMIUM to a binary that exists.")


def prove_font(binpath, faces, family="Poppins"):
    """A font that fails to load renders as the fallback and looks fine.

    Measure the family against serif: identical widths mean the @font-face
    never applied. This is the negative control -- without it, a whole deck
    ships in the wrong typeface and nothing reports it.
    """
    probe = ("<!doctype html><meta charset=utf-8><style>" + faces +
             "span{font-size:100px}</style><body>"
             f"<span id=a style=\"font-family:'{family}';font-weight:600\">Hamburgefonstiv</span>"
             "<span id=b style=\"font-family:serif;font-weight:600\">Hamburgefonstiv</span>"
             "<script>document.fonts.ready.then(function(){document.title="
             "[a.getBoundingClientRect().width,"
             "b.getBoundingClientRect().width].join('|')})</script></body>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(probe)
        src = f.name
    p = subprocess.run([binpath, "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--virtual-time-budget=5000", "--dump-dom", f"file://{src}"], capture_output=True, text=True)
    os.unlink(src)
    import re as _re
    m = _re.search(r"<title>([\d.]+)\|([\d.]+)</title>", p.stdout)
    if not m:
        sys.exit("BLOCKED: font probe produced no measurement. Typeface UNVERIFIED.")
    a, b = float(m.group(1)), float(m.group(2))
    if abs(a - b) < 1.0:
        sys.exit(f"BLOCKED: '{family}' measures identical to serif "
                 f"({a:.1f}px vs {b:.1f}px) -- the embedded face did not load. "
                 f"Every slide would render in the wrong typeface and look fine.")
    print(f"  font proof: {family} {a:.0f}px vs serif {b:.0f}px -- distinct")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    tok = {**TOKENS, **spec.get("tokens", {})}
    os.makedirs(a.out, exist_ok=True)
    binpath = chrome()
    faces, seen = font_face_css(spec.get("font_dir", FONT_DIR))
    print(f"== rendering {len(spec['slides'])} slides with "
          f"{os.path.basename(binpath)} ==")
    print(f"  embedded: {', '.join(seen)}")
    prove_font(binpath, faces)
    for s in spec["slides"]:
        htm = page(build(s), tok, faces, spec.get("css", ""))
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(htm)
            src = f.name
        out = os.path.join(a.out, f"{s['id']}.png")
        p = subprocess.run([binpath, "--headless=new", "--disable-gpu",
                            "--hide-scrollbars", "--no-sandbox",
                            "--force-device-scale-factor=2",
                            "--window-size=1920,1080", "--virtual-time-budget=5000",
                            f"--screenshot={out}", f"file://{src}"],
                           capture_output=True, text=True)
        os.unlink(src)
        if not os.path.exists(out) or os.path.getsize(out) < 5000:
            sys.exit(f"BLOCKED: {s['id']} did not render\n{p.stderr[-800:]}")
        print(f"  {s['id']:<12} {s['template']:<9} {os.path.getsize(out)//1024:>5} KB")


if __name__ == "__main__":
    main()
