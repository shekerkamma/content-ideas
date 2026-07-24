#!/usr/bin/env python3
"""Build the self-contained dashboard.html from data.json (Aurora Glass tokens,
dataviz-skill rules: single validated hue #0d9488 for marks, hover layer,
filter row, text in ink tokens)."""
import json, pathlib

d = pathlib.Path(__file__).parent
DATA = json.load(open(d / "data.json"))

HOOKS = [
    {"views": 766708, "title": "Start a 1-Person Business with Claude (4 HOUR COURSE)",
     "hook": "Cold-open: third-party authority clips (“one person, $1B company”) before the creator speaks. Anti-get-rich-quick disclaimer (“click off if…”) at 1:03 filters the audience. Data-visual hook at 1:52: 8.1B dots, “84% have never used AI — you’re early.”"},
    {"views": 53026, "title": "How I Turned Claude Into My Personal Assistant",
     "hook": "Cold-open fear-authority quote in first 3s (“lose your job to somebody who uses AI”). Gap framing: “most people use AI the completely wrong way.” Numeric promise stack: one setup, 10x productivity, 10 minutes, “saves you a $3,000 assistant.”"},
    {"views": 50344, "title": "I fixed Claude Code Usage Limits",
     "hook": "Pain-point cold open (“$200/mo plan, still rate-limited”). Mechanism teaser: harness vs brain (“you’re only paying for the brain”). Promise: “use Claude Code completely free forever.”"},
]
SHARED = ("Every winner runs the same credibility block at ~1:00 — “no university, "
          "built two million-dollar companies, credit to Claude/ChatGPT” — then a concrete "
          "numeric promise. Hooks are pain or borrowed authority, never topic announcements.")

html = """<!doctype html>
<html><head><meta charset="utf-8"><title>@albertolgaard — playlist explorer</title>
<style>
:root{--bg:#080b11;--bg-elev:#0f141d;--glass:rgba(255,255,255,.04);--line:rgba(255,255,255,.09);
--ink:#eef2f7;--soft:#aeb8c7;--muted:#69748a;--teal:#2dd4bf;--mark:#0d9488}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:ui-sans-serif,system-ui,"Segoe UI",sans-serif;padding:40px clamp(16px,4vw,64px)}
.mono{font-family:ui-monospace,"SF Mono",Menlo,monospace}
.eyebrow{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--teal)}
h1{font-size:2.2rem;font-weight:800;letter-spacing:-.02em;margin:.4rem 0 .3rem;
background:linear-gradient(135deg,#2dd4bf,#38bdf8,#e879f9);-webkit-background-clip:text;background-clip:text;color:transparent;display:inline-block}
.sub{color:var(--soft);max-width:70ch;line-height:1.5}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:26px 0}
.tile{background:var(--glass);border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.tile .n{font-size:1.9rem;font-weight:800;letter-spacing:-.03em;color:var(--teal)}
.tile .l{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-top:6px}
.filters{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 18px}
select,input{background:var(--bg-elev);border:1px solid var(--line);color:var(--ink);border-radius:8px;padding:8px 12px;font-size:.9rem}
input{min-width:220px}
select:focus,input:focus{outline:none;border-color:var(--teal)}
.grid{display:grid;grid-template-columns:2fr 1fr;gap:22px;align-items:start}
@media(max-width:980px){.grid{grid-template-columns:1fr}}
.panel{background:var(--glass);border:1px solid var(--line);border-radius:12px;padding:20px 22px}
.panel h2{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--teal);font-weight:400;margin-bottom:14px}
.row{display:grid;grid-template-columns:minmax(160px,44%) 1fr 84px;gap:10px;align-items:center;padding:7px 6px;border-radius:8px;cursor:pointer}
.row:hover{background:rgba(255,255,255,.05)}
.row .t{font-size:.86rem;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bar{height:14px;border-radius:0 4px 4px 0;background:var(--mark);min-width:2px}
.row .v{font-size:.8rem;color:var(--soft);text-align:right}
.pat td,.pat th{padding:6px 8px;font-size:.82rem;text-align:left;border-bottom:1px solid var(--line)}
.pat th{font-size:.66rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);font-weight:400}
.pat td.num{text-align:right;color:var(--soft)}
.pat td.up{color:var(--teal);text-align:right}
.hook{border-top:1px solid var(--line);padding:12px 0}
.hook:first-of-type{border-top:none;padding-top:0}
.hook .hv{color:var(--teal);font-weight:700;font-size:.8rem}
.hook .ht{font-weight:600;font-size:.9rem;margin:2px 0 4px}
.hook p{font-size:.82rem;color:var(--soft);line-height:1.5}
.shared{margin-top:14px;font-size:.82rem;color:var(--soft);border-left:3px solid var(--teal);padding-left:12px;line-height:1.5}
#tip{position:fixed;pointer-events:none;background:var(--bg-elev);border:1px solid var(--line);border-radius:8px;
padding:8px 12px;font-size:.78rem;color:var(--ink);display:none;z-index:9;max-width:320px}
#tip .m{color:var(--muted)}
footer{margin-top:26px;font-size:.68rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
</style></head><body>
<div class="eyebrow mono">youtube playlist explorer &middot; real data via yt-dlp &middot; 2026-07-12</div>
<h1>@albertolgaard &mdash; what actually gets views</h1>
<div class="sub">98 videos scraped (18 in &ldquo;Beginners Guide to a 1-Person AI Business&rdquo; + 80 uploads).
Bars = views. Patterns ranked by median-view uplift. Winner hooks from watch-skill transcripts of the top 3.</div>
<div class="tiles">
 <div class="tile"><div class="n" id="st-count">&ndash;</div><div class="l mono">videos in view</div></div>
 <div class="tile"><div class="n" id="st-total">&ndash;</div><div class="l mono">total views</div></div>
 <div class="tile"><div class="n" id="st-median">&ndash;</div><div class="l mono">median views</div></div>
 <div class="tile"><div class="n" id="st-top">&ndash;</div><div class="l mono">top video views</div></div>
</div>
<div class="filters">
 <select id="f-group"></select>
 <select id="f-sort">
  <option value="views-desc">views &darr;</option><option value="views-asc">views &uarr;</option>
  <option value="date-desc">newest</option><option value="date-asc">oldest</option>
 </select>
 <input id="f-q" placeholder="search titles&hellip;">
</div>
<div class="grid">
 <div class="panel"><h2 class="mono">videos</h2><div id="list"></div></div>
 <div>
  <div class="panel"><h2 class="mono">title patterns vs median views</h2>
   <table class="pat"><thead><tr><th>pattern</th><th>n</th><th>median</th><th>uplift</th></tr></thead>
   <tbody id="pat"></tbody></table></div>
  <div class="panel" style="margin-top:22px"><h2 class="mono">what the winners do (watch-skill transcripts)</h2>
   <div id="hooks"></div><div class="shared">__SHARED__</div></div>
 </div>
</div>
<div id="tip"></div>
<footer class="mono">source: data.json &middot; marks #0d9488 (dataviz-validated) &middot; goal: runs/goal-youtube-dashboard</footer>
<script>
const DATA=__DATA__;const HOOKS=__HOOKS__;
const fmt=n=>n>=1e6?(n/1e6).toFixed(1)+"M":n>=1e3?(n/1e3).toFixed(n>=1e4?0:1)+"K":""+n;
const groupSel=document.getElementById("f-group");
DATA.forEach((g,i)=>groupSel.add(new Option(g.playlist+" ("+g.videos.length+")",i)));
groupSel.value=DATA.length>1?1:0;
const median=a=>{const s=[...a].sort((x,y)=>x-y);return s.length?s[Math.floor(s.length/2)]:0};
function current(){
  const g=DATA[+groupSel.value];const q=document.getElementById("f-q").value.toLowerCase();
  let v=g.videos.filter(x=>x.title.toLowerCase().includes(q));
  const s=document.getElementById("f-sort").value;
  v.sort((a,b)=>s==="views-desc"?b.views-a.views:s==="views-asc"?a.views-b.views:
    s==="date-desc"?(b.date||"").localeCompare(a.date||""):(a.date||"").localeCompare(b.date||""));
  return v;}
const tip=document.getElementById("tip");
function render(){
  const v=current();
  document.getElementById("st-count").textContent=v.length;
  document.getElementById("st-total").textContent=fmt(v.reduce((a,x)=>a+x.views,0));
  document.getElementById("st-median").textContent=fmt(median(v.map(x=>x.views)));
  document.getElementById("st-top").textContent=v.length?fmt(Math.max(...v.map(x=>x.views))):"0";
  const max=Math.max(...v.map(x=>x.views),1);
  document.getElementById("list").innerHTML=v.map(x=>
    `<div class="row" data-id="${x.id}" data-d="${x.date||""}" data-dur="${x.duration||""}" data-v="${x.views}">
     <div class="t">${x.title.replace(/</g,"&lt;")}</div>
     <div><div class="bar" style="width:${(100*x.views/max).toFixed(1)}%"></div></div>
     <div class="v mono">${fmt(x.views)}</div></div>`).join("");
  patterns(v);}
function patterns(v){
  const med=median(v.map(x=>x.views));const map={};
  const stop=new Set(["the","a","an","to","of","in","for","and","with","your","you","how","i","my","is","it","this","on"]);
  v.forEach(x=>{const w=x.title.toLowerCase().replace(/[^a-z0-9$ ]/g," ").split(/\\s+/).filter(t=>t&&!stop.has(t));
    new Set(w.concat(w.slice(0,-1).map((t,i)=>t+" "+w[i+1]))).forEach(t=>{(map[t]=map[t]||[]).push(x.views)});});
  const rows=Object.entries(map).filter(([t,a])=>a.length>=3&&t.length>2)
    .map(([t,a])=>({t,n:a.length,m:median(a),up:med?median(a)/med:0}))
    .sort((a,b)=>b.up-a.up).slice(0,12);
  document.getElementById("pat").innerHTML=rows.map(r=>
    `<tr><td>${r.t}</td><td class="num mono">${r.n}</td><td class="num mono">${fmt(r.m)}</td><td class="up mono">${r.up.toFixed(1)}x</td></tr>`).join("");}
document.getElementById("hooks").innerHTML=HOOKS.map(h=>
  `<div class="hook"><span class="hv mono">${fmt(h.views)} views</span><div class="ht">${h.title}</div><p>${h.hook}</p></div>`).join("");
document.addEventListener("mousemove",e=>{
  const r=e.target.closest(".row");
  if(!r){tip.style.display="none";return}
  const dur=r.dataset.dur?Math.round(r.dataset.dur/60)+" min":"?";
  tip.innerHTML=`<b>${(+r.dataset.v).toLocaleString()}</b> views<br><span class="m">${r.dataset.d||"date n/a"} &middot; ${dur}</span>`;
  tip.style.display="block";tip.style.left=Math.min(e.clientX+14,innerWidth-330)+"px";tip.style.top=(e.clientY+14)+"px";});
document.addEventListener("click",e=>{const r=e.target.closest(".row");
  if(r)window.open("https://www.youtube.com/watch?v="+r.dataset.id,"_blank");});
["f-group","f-sort","f-q"].forEach(id=>document.getElementById(id).addEventListener("input",render));
render();
</script></body></html>"""

html = html.replace("__DATA__", json.dumps(DATA)).replace("__HOOKS__", json.dumps(HOOKS)).replace("__SHARED__", SHARED)
open(d / "dashboard.html", "w").write(html)
print("dashboard.html written,", len(html), "bytes")
