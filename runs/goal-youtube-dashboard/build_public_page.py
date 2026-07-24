#!/usr/bin/env python3
"""Executive briefing build: @albertolgaard channel mapped to business problems.
Categories assigned by title rules (ordered, first match); demand = summed views.
Self-contained index.html for GitHub Pages."""
import json, pathlib

d = pathlib.Path(__file__).parent
DATA = json.load(open(d / "data.json"))
UPLOADS = DATA[1]["videos"]
PLAYLIST = DATA[0]["videos"]

# ordered rules: (category, [title substrings])
RULES = [
    ("Cut software spend", ["Never Pay", "cancelled", "killed every AI notetaker",
        "Usage Limits", "Cheapest Way To Host", "Gemma 4", "VEO 3", "CHEAPEST and EASIEST"]),
    ("Automate daily operations", ["Personal Assistant", "1000 Apps", "Workflows Without",
        "running my business", "replaced my editor", "thumbnail designer", "video is edited by AI"]),
    ("Win clients & grow pipeline", ["find me clients", "first AI Automation client",
        "Desperately Need", "B2B Ads", "Close an $8,400", "Getting Me Clients",
        "Boomer Businesses", "charge 10x", "Sell OpenClaw"]),
    ("Launch new revenue streams", ["$10K website", "made me $367,000", "$1M AI App",
        "Sell this AI app", "$32,655", "got paid $1200", "First $5000", "Hormozi",
        "$10K video", "First $10K"]),
    ("Grow the brand with AI content", ["viral on Instagram", "Instagram from 0", "Higgsfield",
        "cloned myself", "Fake AI ads", "fake AI ads"]),
    ("Build the capability (free courses)", ["COURSE", "Course", "Guide to Claude Code",
        "1000+ Hours", "Learn Claude Code", "Claude Skills", "BuildMyAgent",
        "Better Than 99%", "Beginner Guide", "Beginners Guide", "Beginner's"]),
    ("Strategy: where the money is", ["STOP selling", "Niches", "end of AI Agencies",
        "Ranked Business Models", "0-$40k", "stuck at $0", "First $1M", "Start Over",
        "Started an AI agency", "Opus 4.8", "killed OpenClaw", "almost lost",
        "on Your Phone", "Crazy Upgrade"]),
    ("Operator mindset", ["pov:", "lock in", "Expectations", "UNLEARN", "fear of being",
        "burning out", "$1M at 23", "financial freedom", "Parents Think",
        "unfair not to win", "58 sec"]),
]

CAT_META = {
    "Cut software spend": {
        "problem": "SaaS sprawl and AI subscriptions compound every month.",
        "get": "A build-don't-subscribe playbook: replace dictation, scheduling, screen "
               "recording, and notetaking tools with owned equivalents, and run AI models "
               "without per-seat fees.",
    },
    "Automate daily operations": {
        "problem": "Email, calendars, editing, and admin eat hours that never show up on a P&L.",
        "get": "Working assistant setups — Claude wired to your inbox, calendar, and 1,000+ "
               "apps — plus real automations for editing and design chores.",
    },
    "Win clients & grow pipeline": {
        "problem": "Customer acquisition is the #1 constraint for every services business.",
        "get": "Outbound systems run by AI (a 5% reply-rate campaign, clients on autopilot), "
               "B2B ad walkthroughs, and a recorded $8,400 close — the full acquisition motion.",
    },
    "Launch new revenue streams": {
        "problem": "New offers used to need engineers, budget, and a quarter of runway.",
        "get": "Documented builds with revenue attached: a $10K website in 30 minutes, an "
               "agent earning $32K/month, no-code apps sold at $10K — templates included.",
    },
    "Grow the brand with AI content": {
        "problem": "Content is the cheapest distribution — and the easiest thing to neglect.",
        "get": "AI-run social growth: 0→100K Instagram in 3 months, agent-generated video, "
               "and honest tests of what AI-made ads can and can't pass off.",
    },
    "Build the capability (free courses)": {
        "problem": "Teams stall on AI because nobody owns the learning curve.",
        "get": "15+ hours of free structured training — from first prompt to shipped agent — "
               "that would otherwise be a paid enablement program.",
    },
    "Strategy: where the money is": {
        "problem": "Which AI opportunities are real, and which are already saturated?",
        "get": "Niche selection, business-model rankings, pricing, and candid post-mortems "
               "(what stalls agencies at $0, what scales to $40K/month).",
    },
    "Operator mindset": {
        "problem": "Execution discipline is the silent killer of small AI ventures.",
        "get": "The founder's operating cadence — useful context, not the core library.",
    },
}


def categorize(title):
    for cat, keys in RULES:
        if any(k in title for k in keys):
            return cat
    return "Strategy: where the money is"


cats = {c: [] for c, _ in RULES}
for v in UPLOADS:
    cats[categorize(v["title"])].append(v)
for c in cats:
    cats[c].sort(key=lambda v: -v["views"])

fmt = lambda n: f"{n/1e6:.1f}M" if n >= 1e6 else (f"{n/1e3:.0f}K" if n >= 1e3 else str(n))

# ---- build category sections
sections = []
order = [c for c, _ in RULES if c != "Operator mindset"]
for c in order:
    vids = cats[c]
    total = sum(v["views"] for v in vids)
    meta = CAT_META[c]
    tops = "".join(
        f'<a class="vid" href="https://www.youtube.com/watch?v={v["id"]}" target="_blank">'
        f'<span class="vv mono">{fmt(v["views"])}</span><span class="vt">{v["title"].replace("<","&lt;")}</span></a>'
        for v in vids[:5]
    )
    more = f'<div class="more mono">+ {len(vids)-5} more in the library below</div>' if len(vids) > 5 else ""
    sections.append(f"""
  <div class="cat">
   <div class="cat-head">
    <h3>{c}</h3>
    <div class="sig mono">{fmt(total)} views &middot; {len(vids)} videos</div>
   </div>
   <p class="prob"><b>The problem:</b> {meta["problem"]}</p>
   <p class="getp"><b>What you get:</b> {meta["get"]}</p>
   {tops}{more}
  </div>""")

demand = sorted(((c, sum(v["views"] for v in cats[c]), len(cats[c])) for c in order),
                key=lambda x: -x[1])

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The 1-person AI business playbook — 98 free videos mapped to the problems they solve</title>
<meta name="description" content="Executive briefing: @albertolgaard's channel categorized by business problem — cut software spend, automate operations, win clients, launch revenue — with a synopsis of the full starter playlist.">
<style>
:root{{--bg:#080b11;--bg-elev:#0f141d;--glass:rgba(255,255,255,.04);--line:rgba(255,255,255,.09);
--ink:#eef2f7;--soft:#aeb8c7;--muted:#69748a;--teal:#2dd4bf;--mark:#0d9488}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:ui-sans-serif,system-ui,"Segoe UI",sans-serif;line-height:1.6}}
.mono{{font-family:ui-monospace,"SF Mono",Menlo,monospace}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 clamp(16px,4vw,48px)}}
.hero{{padding:64px 0 44px;border-bottom:1px solid var(--line);position:relative;overflow:hidden}}
.hero::before{{content:"";position:absolute;top:0;left:0;right:0;height:4px;
background:linear-gradient(135deg,#2dd4bf,#38bdf8,#e879f9)}}
.eyebrow{{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--teal)}}
h1{{font-size:clamp(1.9rem,4.4vw,3rem);font-weight:800;letter-spacing:-.02em;line-height:1.1;margin:.8rem 0 1rem;
background:linear-gradient(135deg,#2dd4bf,#38bdf8,#e879f9);-webkit-background-clip:text;background-clip:text;color:transparent;max-width:26ch}}
.lede{{font-size:1.08rem;color:var(--soft);max-width:66ch}} .lede b{{color:var(--ink)}}
.demand{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin:36px 0 4px}}
.dcard{{background:var(--glass);border:1px solid var(--line);border-radius:12px;padding:18px 20px}}
.dcard .n{{font-size:1.9rem;font-weight:800;letter-spacing:-.03em;color:var(--teal);line-height:1}}
.dcard .t{{font-size:.86rem;font-weight:600;margin-top:8px}}
.dcard .s{{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-top:4px}}
section{{padding:46px 0;border-bottom:1px solid var(--line)}}
h2{{font-size:1.5rem;font-weight:800;letter-spacing:-.02em;margin-bottom:4px}}
.kicker{{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--teal);margin-bottom:8px}}
.cats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:18px;margin-top:22px}}
.cat{{background:var(--glass);border:1px solid var(--line);border-radius:12px;padding:22px}}
.cat-head{{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:10px}}
.cat h3{{font-size:1.02rem;font-weight:700}}
.sig{{font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);white-space:nowrap}}
.prob,.getp{{font-size:.86rem;color:var(--soft);margin-bottom:8px}} .prob b,.getp b{{color:var(--ink)}}
.vid{{display:flex;gap:12px;align-items:baseline;padding:6px 8px;border-radius:8px;text-decoration:none;color:var(--ink)}}
.vid:hover{{background:rgba(255,255,255,.05)}}
.vv{{color:var(--teal);font-size:.76rem;min-width:44px;text-align:right}}
.vt{{font-size:.84rem;color:var(--soft)}} .vid:hover .vt{{color:var(--ink)}}
.more{{font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding:8px 8px 0}}
.arc{{margin-top:20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}}
.stage{{background:var(--glass);border:1px solid var(--line);border-radius:12px;padding:20px}}
.stage .k{{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--teal)}}
.stage .t{{font-weight:700;margin:4px 0 6px}}
.stage p{{font-size:.85rem;color:var(--soft)}}
.syn{{margin-top:22px;font-size:1rem;color:var(--soft);border-left:3px solid var(--teal);padding-left:16px;max-width:70ch}}
.syn b{{color:var(--ink)}}
/* explorer */
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:20px 0}}
.tile{{background:var(--glass);border:1px solid var(--line);border-radius:12px;padding:14px 16px}}
.tile .n{{font-size:1.6rem;font-weight:800;letter-spacing:-.03em;color:var(--teal)}}
.tile .l{{font-size:.64rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-top:4px}}
.filters{{display:flex;gap:10px;flex-wrap:wrap;margin:4px 0 16px}}
select,input{{background:var(--bg-elev);border:1px solid var(--line);color:var(--ink);border-radius:8px;padding:8px 12px;font-size:.9rem}}
input{{min-width:200px}} select:focus,input:focus{{outline:none;border-color:var(--teal)}}
.panel{{background:var(--glass);border:1px solid var(--line);border-radius:12px;padding:18px 20px}}
.row{{display:grid;grid-template-columns:minmax(150px,52%) 1fr 80px;gap:10px;align-items:center;padding:6px;border-radius:8px;cursor:pointer}}
.row:hover{{background:rgba(255,255,255,.05)}}
.row .t{{font-size:.84rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.bar{{height:13px;border-radius:0 4px 4px 0;background:var(--mark);min-width:2px}}
.row .v{{font-size:.78rem;color:var(--soft);text-align:right}}
#tip{{position:fixed;pointer-events:none;background:var(--bg-elev);border:1px solid var(--line);border-radius:8px;
padding:8px 12px;font-size:.78rem;display:none;z-index:9;max-width:320px}} #tip .m{{color:var(--muted)}}
footer{{padding:34px 0 46px;font-size:.78rem;color:var(--muted)}} footer a{{color:var(--teal);text-decoration:none}}
</style></head><body>

<div class="hero"><div class="wrap">
 <div class="eyebrow mono">executive briefing &middot; ai adoption library &middot; 98 videos &middot; 1.4M views analyzed</div>
 <h1>98 free videos that teach a business to run on AI &mdash; mapped to the problems they solve</h1>
 <p class="lede">Albert Ohlgaard built two seven-figure businesses with AI tools and publishes exactly how &mdash;
 for free. This briefing organizes his entire channel by <b>business problem</b>, so you can go straight to
 what you need: cutting software spend, automating operations, winning clients, or launching new revenue.
 View counts show where <b>1.4&nbsp;million viewers'</b> attention concentrates &mdash; a live demand signal
 for what businesses actually want from AI.</p>
 <div class="demand">
{"".join(f'  <div class="dcard"><div class="n">{fmt(t)}</div><div class="t">{c}</div><div class="s mono">{n} videos</div></div>' for c, t, n in demand[:4])}
 </div>
</div></div>

<section><div class="wrap">
 <div class="kicker mono">the library, by business problem</div>
 <h2>Seven problems this channel solves &mdash; pick yours</h2>
 <div class="cats">{"".join(sections)}</div>
</div></section>

<section><div class="wrap">
 <div class="kicker mono">start here &mdash; the 18-video playlist, summarized</div>
 <h2>&ldquo;Beginners Guide to a 1-Person AI Business&rdquo; as a curriculum</h2>
 <p class="syn">Watched in order, the playlist is a <b>complete operating course for an AI-run business</b>:
 it opens with a 4-hour foundation (why the window is now &mdash; 84% of people have never used AI &mdash; and
 how to stand up your first AI business), then moves through daily operations, client acquisition, and
 delivery, and closes with commercial strategy. A team that works through it ends up with a functioning
 assistant, an outbound system, a shipped build, and a pricing model &mdash; not just theory.</p>
 <div class="arc">
  <div class="stage"><div class="k mono">stage 1 &middot; foundation</div><div class="t">Why now, and the toolchain</div>
   <p>The 4-hour flagship course (767K views) plus tool mastery: using Claude Code well, fixing its cost/usage limits, and never paying for redundant AI tools.</p></div>
  <div class="stage"><div class="k mono">stage 2 &middot; operations</div><div class="t">Your AI back office</div>
   <p>Turn Claude into a personal assistant across email, calendar, and 1,000+ connected apps &mdash; the &ldquo;$3,000 assistant&rdquo; replaced for free.</p></div>
  <div class="stage"><div class="k mono">stage 3 &middot; acquisition</div><div class="t">Clients, found by AI</div>
   <p>An AI-run outbound campaign hitting a 5% reply rate, and a recorded $8,400 client close &mdash; the full sales motion, shown not described.</p></div>
  <div class="stage"><div class="k mono">stage 4 &middot; delivery &amp; strategy</div><div class="t">Ship, price, choose your market</div>
   <p>Build a $10K website in 30 minutes, then the commercial layer: which niches are worth it, why &ldquo;selling AI agents&rdquo; is the wrong offer, and the realistic path to the first $1M.</p></div>
 </div>
</div></section>

<section><div class="wrap">
 <div class="kicker mono">browse the full library</div>
 <h2>All 98 videos &mdash; filter, sort, click to watch</h2>
 <div class="tiles">
  <div class="tile"><div class="n" id="st-count">&ndash;</div><div class="l mono">videos in view</div></div>
  <div class="tile"><div class="n" id="st-total">&ndash;</div><div class="l mono">total views</div></div>
  <div class="tile"><div class="n" id="st-median">&ndash;</div><div class="l mono">median views</div></div>
  <div class="tile"><div class="n" id="st-top">&ndash;</div><div class="l mono">top video</div></div>
 </div>
 <div class="filters">
  <select id="f-group"></select>
  <select id="f-sort"><option value="views-desc">views &darr;</option><option value="views-asc">views &uarr;</option>
   <option value="date-desc">newest</option><option value="date-asc">oldest</option></select>
  <input id="f-q" placeholder="search titles&hellip;">
 </div>
 <div class="panel"><div id="list"></div></div>
</div></section>

<footer><div class="wrap mono">
 All videos by <a href="https://www.youtube.com/@albertolgaard">@albertolgaard</a> &mdash; free on YouTube,
 all credit to the creator &middot; public metadata compiled 2026-07-12 &middot; categorization and synopsis
 by an AI research agent
</div></footer>

<div id="tip"></div>
<script>
const DATA={json.dumps(DATA)};
const fmt=n=>n>=1e6?(n/1e6).toFixed(1)+"M":n>=1e3?(n/1e3).toFixed(n>=1e4?0:1)+"K":""+n;
const groupSel=document.getElementById("f-group");
DATA.forEach((g,i)=>groupSel.add(new Option(g.playlist+" ("+g.videos.length+")",i)));
groupSel.value=DATA.length>1?1:0;
const median=a=>{{const s=[...a].sort((x,y)=>x-y);return s.length?s[Math.floor(s.length/2)]:0}};
function current(){{
  const g=DATA[+groupSel.value];const q=document.getElementById("f-q").value.toLowerCase();
  let v=g.videos.filter(x=>x.title.toLowerCase().includes(q));
  const s=document.getElementById("f-sort").value;
  v.sort((a,b)=>s==="views-desc"?b.views-a.views:s==="views-asc"?a.views-b.views:
    s==="date-desc"?(b.date||"").localeCompare(a.date||""):(a.date||"").localeCompare(b.date||""));
  return v;}}
const tip=document.getElementById("tip");
function render(){{
  const v=current();
  document.getElementById("st-count").textContent=v.length;
  document.getElementById("st-total").textContent=fmt(v.reduce((a,x)=>a+x.views,0));
  document.getElementById("st-median").textContent=fmt(median(v.map(x=>x.views)));
  document.getElementById("st-top").textContent=v.length?fmt(Math.max(...v.map(x=>x.views))):"0";
  const max=Math.max(...v.map(x=>x.views),1);
  document.getElementById("list").innerHTML=v.map(x=>
    `<div class="row" data-id="${{x.id}}" data-d="${{x.date||""}}" data-dur="${{x.duration||""}}" data-v="${{x.views}}">
     <div class="t">${{x.title.replace(/</g,"&lt;")}}</div>
     <div><div class="bar" style="width:${{(100*x.views/max).toFixed(1)}}%"></div></div>
     <div class="v mono">${{fmt(x.views)}}</div></div>`).join("");}}
document.addEventListener("mousemove",e=>{{
  const r=e.target.closest(".row");
  if(!r){{tip.style.display="none";return}}
  const dur=r.dataset.dur?Math.round(r.dataset.dur/60)+" min":"?";
  tip.innerHTML=`<b>${{(+r.dataset.v).toLocaleString()}}</b> views<br><span class="m">${{r.dataset.d||"date n/a"}} &middot; ${{dur}}</span>`;
  tip.style.display="block";tip.style.left=Math.min(e.clientX+14,innerWidth-330)+"px";tip.style.top=(e.clientY+14)+"px";}});
document.addEventListener("click",e=>{{const r=e.target.closest(".row");
  if(r)window.open("https://www.youtube.com/watch?v="+r.dataset.id,"_blank");}});
["f-group","f-sort","f-q"].forEach(id=>document.getElementById(id).addEventListener("input",render));
render();
</script></body></html>"""

open(d / "index.html", "w").write(page)
print("index.html written,", len(page), "bytes")
print("\nCategory demand signals:")
for c, t, n in demand:
    print(f"  {fmt(t):>6}  {n:>2} videos  {c}")
mind = cats["Operator mindset"]
print(f"  (mindset bucket: {len(mind)} videos, {fmt(sum(v['views'] for v in mind))} — folded into library only)")
