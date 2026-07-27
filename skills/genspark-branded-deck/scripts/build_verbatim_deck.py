#!/usr/bin/env python3
"""build_verbatim_deck.py — wrap recovered source slides into a renderable deck.

VERBATIM route only. Each file in --src is the source deck's own slide markup and
is used UNCHANGED. This script adds only the export stage, the render hook, and a
generic auto-fit pass. It makes no content, layout, colour or type decisions.

  python3 build_verbatim_deck.py --src slides --css chrome.css --out deck.html

Recover the inputs first — see references/verbatim-recovery.md.
"""
import argparse, pathlib, re

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="{css}">
<style>
  *{{box-sizing:border-box}}
  html,body{{height:100%;margin:0;padding:0}}
  body{{background:var(--bg-0,#000);color:var(--ink-0,#fff);overflow:hidden;
    -webkit-font-smoothing:antialiased}}
  .viewport{{position:fixed;inset:0;display:grid;place-items:center;overflow:hidden;
    background:var(--bg-0,#000)}}
  .stage{{width:{w}px;height:{h}px;position:relative;flex:none;
    transform:scale(var(--fit,1));transform-origin:center center}}
  .slide{{position:absolute;inset:0;overflow:hidden;opacity:0;visibility:hidden}}
  .slide.is-active,.slide.render-static{{opacity:1;visibility:visible}}
  /* text-free background pass for the hybrid export */
  body.export-bg .stage,body.export-bg .stage *{{color:transparent!important;text-shadow:none!important}}
  .deck-nav{{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);display:flex;gap:14px;
    align-items:center;z-index:99;background:rgba(0,0,0,.72);border:1px solid rgba(255,255,255,.18);
    border-radius:40px;padding:8px 14px}}
  .nav-btn{{width:34px;height:34px;border-radius:50%;border:1px solid rgba(255,255,255,.22);
    background:transparent;color:#fff;cursor:pointer}}
  .counter{{font-family:ui-monospace,monospace;font-size:13px;color:#ddd;min-width:64px;text-align:center}}
  .export-mode .deck-nav{{display:none!important}}
</style>
</head>
<body>
<div class="viewport"><div class="stage" id="stage">
"""

TAIL = r"""
</div></div>
<nav class="deck-nav"><button class="nav-btn" id="prevBtn">&#8592;</button>
<div class="counter"><span id="curNum">01</span> / <span id="totNum">00</span></div>
<button class="nav-btn" id="nextBtn">&#8594;</button></nav>
<script>
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var total=slides.length, cur=0;
  var stage=document.getElementById('stage');
  var curNum=document.getElementById('curNum'), totNum=document.getElementById('totNum');
  var prevBtn=document.getElementById('prevBtn'), nextBtn=document.getElementById('nextBtn');
  totNum.textContent=String(total).padStart(2,'0');
  function fit(){stage.style.setProperty('--fit',
    Math.min(window.innerWidth/__W__, window.innerHeight/__H__));}
  window.addEventListener('resize',fit); fit();
  function draw(){slides.forEach(function(s,i){s.classList.toggle('is-active',i===cur)});
    curNum.textContent=String(cur+1).padStart(2,'0');
    prevBtn.disabled=cur===0;nextBtn.disabled=cur===total-1;}
  function go(i){cur=Math.max(0,Math.min(total-1,i));draw()}
  nextBtn.onclick=function(){go(cur+1)};prevBtn.onclick=function(){go(cur-1)};
  document.addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();go(cur+1)}
    else if(e.key==='ArrowLeft'){e.preventDefault();go(cur-1)}});
  draw();

  // Generic auto-fit. Two distinct source-deck defects, both of which print text
  // on top of other text once the boxes are absolutely positioned:
  //   (a) a box with an explicit height whose own copy overflows it;
  //   (b) a box with NO declared height that auto-grows into the fixed-position
  //       box beneath it (a two-line title landing on its subtitle).
  // (b) is invisible to a scrollHeight test — clientHeight grows with the text —
  // so it needs a real collision check. Shrink only the offending box; positions
  // and content are untouched.
  function boxesIn(slide){
    return [].slice.call(slide.querySelectorAll('[data-object-type="textbox"],[data-object="true"]'))
      .filter(function(el){
        return getComputedStyle(el).position === 'absolute' && el.textContent.trim();
      });
  }
  // Scale a box and every descendant that carries its own font-size, so the
  // shrink works no matter which element the stylesheet sizes.
  function scaleBox(el, factor){
    var nodes = [el].concat([].slice.call(el.querySelectorAll('*')));
    nodes.forEach(function(n){
      if (n.__baseFs === undefined) n.__baseFs = parseFloat(getComputedStyle(n).fontSize) || 0;
      if (n.__baseFs) n.style.fontSize = (n.__baseFs * factor) + 'px';
    });
  }
  function hasDeclaredHeight(el){
    return /(^|;)\s*height\s*:/.test(el.getAttribute('style') || '');
  }
  function autofit(){
    var n = 0;
    document.querySelectorAll('.slide').forEach(function(slide){
      var boxes = boxesIn(slide);
      boxes.forEach(function(el){
        var factor = 1, guard = 0;
        // (a) self-overflow, only meaningful when a height was declared
        if (hasDeclaredHeight(el)) {
          while (el.scrollHeight > el.clientHeight + 1 && factor > 0.68 && guard++ < 60) {
            factor -= 0.02; scaleBox(el, factor);
          }
        } else {
          // (b) collides with, OR comes within PAD of, a box positioned below it.
          // PAD matters: PowerPoint's line metrics run slightly taller than the
          // browser's, so a box that clears by 1px in HTML overlaps in the PPTX.
          // Demanding real clearance absorbs that drift.
          // Budget for ONE MORE wrapped line than the browser currently shows.
          // The browser and PowerPoint disagree at the wrap boundary: a title
          // that fits one line in Chrome routinely takes two in PowerPoint, and
          // the extra line lands on whatever sits below. Testing the *actual*
          // bottom therefore passes here and fails in the deliverable.
          var PAD = 8;
          var extraLine = function(){
            var mx = 0;
            [el].concat([].slice.call(el.querySelectorAll('*'))).forEach(function(n){
              var f = parseFloat(getComputedStyle(n).fontSize) || 0;
              if (n.textContent.trim() && f > mx) mx = f;
            });
            return mx * 1.3;
          };
          var hits = function(){
            var ra = el.getBoundingClientRect();
            var effBottom = ra.bottom + extraLine() + PAD;
            return boxes.some(function(b){
              if (b === el || el.contains(b) || b.contains(el)) return false;
              var rb = b.getBoundingClientRect();
              if (rb.top <= ra.top + 1) return false;      // only downward collisions
              return (Math.min(effBottom, rb.bottom) - Math.max(ra.top, rb.top)) > 4 &&
                     (Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left)) > 4;
            });
          };
          while (hits() && factor > 0.68 && guard++ < 60) { factor -= 0.02; scaleBox(el, factor); }
        }
        // Headroom. Satisfying the constraint in the browser is not enough: the
        // export rebuilds each box from its captured bbox, and PowerPoint's
        // metrics run marginally wider. A box that *just* fits one line here
        // re-wraps to two there and lands on whatever sits below. One extra
        // step buys ~3% horizontal slack, which is the difference between
        // "fits in Chrome" and "fits in PowerPoint".
        if (factor !== 1) { factor -= 0.03; scaleBox(el, factor); n++; }
      });
    });
    return n;
  }

  // Measure only after webfonts settle, then publish the hook so the renderer
  // can never screenshot a pre-fit frame.
  var ready=(document.fonts&&document.fonts.ready)?document.fonts.ready:Promise.resolve();
  ready.then(function(){
    window.__deckAutofit=autofit();
    window.__deck=DECK;
  });

  var DECK={total:total,
    fitOne:function(){stage.style.setProperty('--fit',1);},
    show:function(i){slides.forEach(function(s,k){s.classList.remove('is-active');
      s.classList.toggle('render-static',k===i);});}};
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="slides", help="dir of recovered slide .html files")
    ap.add_argument("--css", default="chrome.css", help="the source deck's stylesheet")
    ap.add_argument("--out", default="deck.html")
    ap.add_argument("--title", default="")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    a = ap.parse_args()

    files = sorted(pathlib.Path(a.src).glob("*.html"))
    if not files:
        raise SystemExit(f"no slide files in {a.src}/ — recover them first")

    parts = []
    for f in files:
        html = f.read_text(encoding="utf-8")
        m = re.search(r'data-screen-label="([^"]+)"', html)
        label = (m.group(1) if m else f.stem).replace('"', "&quot;")
        parts.append(f'<section class="slide" data-title="{label}">\n{html}\n</section>')

    head = HEAD.format(title=a.title or pathlib.Path(a.out).stem, css=a.css, w=a.width, h=a.height)
    tail = TAIL.replace("__W__", str(a.width)).replace("__H__", str(a.height))
    pathlib.Path(a.out).write_text(head + "\n".join(parts) + tail, encoding="utf-8")
    print(f"DONE: {len(files)} slides (verbatim) at {a.width}x{a.height} -> {a.out}")
