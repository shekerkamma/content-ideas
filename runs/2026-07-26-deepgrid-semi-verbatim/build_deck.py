#!/usr/bin/env python3
"""build_deck.py — assemble deck.html from the reference deck's own slide files.

Each file in slides/ is the source deck's slide markup, used VERBATIM. This script
only wraps them in the export stage and attaches the render hook. It does not
re-author content and does not change any layout.

  python3 build_deck.py --out deck.html
"""
import argparse, pathlib, re

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>DeepGrid Semi — Pre-Series A Investor &amp; GTM Strategy</title>
<link rel="stylesheet" href="chrome.css">
<style>
  *{box-sizing:border-box}
  html,body{height:100%;margin:0;padding:0}
  body{background:var(--bg-0);color:var(--ink-0);font-family:var(--font-body);overflow:hidden;
    -webkit-font-smoothing:antialiased}
  .viewport{position:fixed;inset:0;display:grid;place-items:center;overflow:hidden;background:var(--bg-0)}
  .stage{width:1920px;height:1080px;position:relative;flex:none;
    transform:scale(var(--fit,1));transform-origin:center center}
  .slide{position:absolute;inset:0;overflow:hidden;opacity:0;visibility:hidden}
  .slide.is-active,.slide.render-static{opacity:1;visibility:visible}
  /* text-free background pass for the hybrid export: hide glyphs, keep panels/rules/gradients */
  body.export-bg .stage,body.export-bg .stage *{color:transparent!important;text-shadow:none!important}
  .deck-nav{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);display:flex;gap:14px;
    align-items:center;z-index:99;background:rgba(10,18,32,.8);border:1px solid var(--line);
    border-radius:40px;padding:8px 14px}
  .nav-btn{width:34px;height:34px;border-radius:50%;border:1px solid var(--line);
    background:transparent;color:var(--ink-0);cursor:pointer}
  .counter{font-family:var(--font-mono);font-size:13px;color:var(--ink-1);min-width:64px;text-align:center}
  .export-mode .deck-nav{display:none!important}
</style>
</head>
<body>
<div class="viewport"><div class="stage" id="stage">
"""

TAIL = """
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
  function fit(){stage.style.setProperty('--fit',Math.min(window.innerWidth/1920,window.innerHeight/1080));}
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

  // QA autofit (source-deck defect): a few textboxes declare a height smaller
  // than their text needs, so the overflow spills onto the box beneath
  // (e.g. slide 25's synthesis heading over its own paragraph). Shrink ONLY
  // those boxes' type until the text fits. Positions and content are unchanged.
  function autofit(){
    var n=0;
    document.querySelectorAll('.slide [data-object-type="textbox"]').forEach(function(el){
      if(getComputedStyle(el).position!=='absolute') return;
      var base=parseFloat(getComputedStyle(el).fontSize), size=base, guard=0;
      while(el.scrollHeight>el.clientHeight+1 && size>base*0.68 && guard++<60){
        size-=0.5; el.style.fontSize=size+'px';
      }
      if(size!==base) n++;
    });
    return n;
  }

  // Measure only after webfonts are ready, then publish the export hook so the
  // renderer never screenshots a pre-fit frame.
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
    ap.add_argument("--src", default="slides")
    ap.add_argument("--out", default="deck.html")
    a = ap.parse_args()

    files = sorted(pathlib.Path(a.src).glob("*.html"))
    parts = []
    for f in files:
        html = f.read_text(encoding="utf-8")
        # QA fix (source-deck defect): title textboxes are declared width:1400px
        # height:70px. Long titles wrap to a second line and spill onto the
        # subtitle beneath. Widen to the full 1680px content width — 280px of
        # unused margin — so they fit on one line. Content is untouched.
        html = re.sub(
            r'(font-size:52px[^"]*?)"',
            lambda mm: mm.group(0),
            html)
        def _widen(mo):
            style = mo.group(1)
            if "font-size:52px" not in style:
                return mo.group(0)
            style = re.sub(r"width:\s*1400px", "width:1680px", style)
            return mo.group(0).replace(mo.group(1), style)
        html = re.sub(r'style="([^"]*?)"', _widen, html)

        m = re.search(r'data-screen-label="([^"]+)"', html)
        label = m.group(1) if m else f.stem
        parts.append(f'<section class="slide" data-title="{label}">\n{html}\n</section>')

    pathlib.Path(a.out).write_text(HEAD + "\n".join(parts) + TAIL, encoding="utf-8")
    print(f"DONE: {len(files)} slides (verbatim) -> {a.out}")
