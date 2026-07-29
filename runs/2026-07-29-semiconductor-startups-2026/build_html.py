#!/usr/bin/env python3
"""Build the self-contained HTML companion to the 44-slide decision deck."""

from __future__ import annotations

import csv
import html
import json
from collections import Counter
from pathlib import Path


RUN = Path(__file__).resolve().parent
OUT = RUN / "client-package" / "site" / "index.html"
CONTENT = json.loads((RUN / "outputs" / "decision-deck-content.json").read_text(encoding="utf-8"))
with (RUN / "outputs" / "evidence-ledger.csv").open(encoding="utf-8") as handle:
    LEDGER = list(csv.DictReader(handle))


def esc(value: object) -> str:
    return html.escape(str(value))


def render_cards(items: list[dict], label_key: str = "label", text_key: str = "text") -> str:
    return "".join(
        f'<article class="card"><strong>{esc(item.get(label_key, ""))}</strong>'
        f'<p>{esc(item.get(text_key, ""))}</p></article>'
        for item in items
    )


def render_slide(slide: dict) -> str:
    body = ""
    if "profile" in slide:
        body = render_cards([{"label": k, "text": v} for k, v in slide["profile"].items()])
    elif "columns" in slide:
        body = render_cards(slide["columns"])
    elif "plays" in slide:
        body = render_cards(slide["plays"])
    elif "models" in slide:
        body = render_cards(slide["models"])
    elif "icps" in slide:
        body = render_cards(slide["icps"], text_key="need")
    elif "motions" in slide:
        body = render_cards(slide["motions"])
    elif "arrows" in slide:
        body = render_cards(slide["arrows"])
    elif "rows" in slide:
        headers = slide.get("headers", [])
        head = "".join(f"<th>{esc(item)}</th>" for item in headers)
        rows = "".join(
            "<tr>" + "".join(f"<td>{esc(cell)}</td>" for cell in row) + "</tr>"
            for row in slide["rows"]
        )
        body = f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
    elif "gates" in slide:
        body = render_cards([{"label": f"{x[0]} · {x[1]}", "text": x[2]} for x in slide["gates"]])
    else:
        body = f'<p class="claim">{esc(slide.get("claim") or slide.get("takeaway") or slide.get("subtitle", ""))}</p>'
    source_links = []
    by_id = {source["id"]: source for source in CONTENT["sources"]}
    for source_id in slide.get("evidence", []):
        source = by_id[source_id]
        source_links.append(f'<a href="{esc(source["path"])}" rel="noreferrer">{esc(source["title"])}</a>')
    return f"""
    <section id="slide-{slide['id']}" class="report-section" data-group="{esc(slide.get('kicker', 'analysis'))}">
      <div class="eyebrow">{esc(slide.get('kicker', slide.get('company', 'ANALYSIS')))}</div>
      <h2>{esc(slide['title'])}</h2>
      <p class="subtitle">{esc(slide.get('subtitle', ''))}</p>
      <div class="grid">{body}</div>
      <details><summary>Evidence and confidence</summary>
        <p>{esc(slide.get('citation', ''))}</p>
        <p class="sources">{' · '.join(source_links)}</p>
      </details>
    </section>"""


def main() -> None:
    confidence = Counter(row["confidence"] for row in LEDGER)
    source_types = Counter(row["source_type"] for row in LEDGER)
    sections = "\n".join(render_slide(slide) for slide in CONTENT["slides"][1:])
    sources = "".join(
        f'<li><a href="{esc(source["path"])}">{esc(source["title"])}</a>'
        f'<span>{esc(source.get("date", ""))}</span></li>'
        for source in CONTENT["sources"]
    )
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The 10 Coolest Semiconductor Startups of 2026 — Evidence-Led Decision Screen</title>
<style>
:root{{--navy:#09192b;--ink:#193047;--muted:#607184;--teal:#00a98f;--gold:#f7b731;--paper:#f4f7f9;--line:#d9e2e8}}
*{{box-sizing:border-box}} body{{margin:0;font:16px/1.55 Inter,Segoe UI,Arial,sans-serif;color:var(--ink);background:var(--paper)}}
a{{color:#087c70}} .hero{{background:linear-gradient(135deg,#071627,#12364a);color:white;padding:72px max(24px,calc((100vw - 1160px)/2)) 64px}}
.hero h1{{font-size:clamp(38px,6vw,72px);line-height:1.02;max-width:980px;margin:12px 0 22px}} .hero p{{max-width:840px;font-size:20px;color:#d8e6ed}}
.eyebrow{{color:var(--teal);font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}} .hero .eyebrow{{color:#55e0ca}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:32px}} .kpi{{padding:17px;border:1px solid #456273;border-radius:12px;background:#ffffff0d}}
.kpi b{{display:block;font-size:28px;color:white}} nav{{position:sticky;top:0;z-index:3;display:flex;gap:12px;overflow:auto;padding:12px max(20px,calc((100vw - 1160px)/2));background:#fffffff2;border-bottom:1px solid var(--line);backdrop-filter:blur(12px)}}
nav a{{white-space:nowrap;text-decoration:none;font-weight:700;padding:7px 12px;border-radius:999px}} nav a:hover{{background:#dff5f0}}
main{{max-width:1160px;margin:auto;padding:24px}} .report-section{{background:white;border:1px solid var(--line);border-radius:18px;padding:34px;margin:22px 0;box-shadow:0 8px 30px #17324a0c}}
h2{{font-size:clamp(28px,4vw,44px);line-height:1.12;margin:8px 0}} .subtitle{{font-size:18px;color:var(--muted);max-width:900px}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:22px 0}} .card{{border:1px solid var(--line);border-left:5px solid var(--teal);border-radius:12px;padding:18px;background:#fbfdfe}}
.card strong{{font-size:13px;color:#087c70;letter-spacing:.06em}} .card p{{margin:.5em 0 0}} .claim{{font-size:22px;font-weight:700;max-width:900px}}
.table-wrap{{grid-column:1/-1;overflow:auto}} table{{width:100%;border-collapse:collapse;font-size:14px}} th,td{{padding:12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}} th{{background:var(--navy);color:white;position:sticky;top:0}}
details{{border-top:1px solid var(--line);padding-top:14px;color:var(--muted)}} summary{{cursor:pointer;font-weight:700;color:var(--ink)}} .sources a{{margin-right:8px}}
.references li{{display:flex;justify-content:space-between;gap:20px;padding:10px 0;border-bottom:1px solid var(--line)}} footer{{max-width:1160px;margin:auto;padding:20px 24px 70px;color:var(--muted)}}
@media(max-width:760px){{.kpis,.grid{{grid-template-columns:1fr}}.hero{{padding-top:46px}}.report-section{{padding:24px}}.references li{{display:block}}}}
</style>
</head>
<body>
<header class="hero" id="top">
  <div class="eyebrow">Evidence-led semiconductor landscape · July 2026</div>
  <h1>The 10 Coolest Semiconductor Startups of 2026</h1>
  <p>Use the cohort as a validation portfolio—not a winner ranking. Prioritize heterogeneous-infrastructure adoption paths, then require Phase 0 calibration before named-partner recommendations.</p>
  <div class="kpis">
    <div class="kpi"><b>10</b>closed-cohort companies</div>
    <div class="kpi"><b>4</b>infrastructure arenas</div>
    <div class="kpi"><b>{len(LEDGER)}</b>evidence rows</div>
    <div class="kpi"><b>{confidence.get('high',0)}/{confidence.get('medium',0)}</b>high / medium confidence</div>
  </div>
</header>
<nav aria-label="Report navigation">
  <a href="#slide-2">Executive answer</a><a href="#slide-5">Market map</a>
  <a href="#slide-7">ICP & GTM</a><a href="#slide-12">Companies</a>
  <a href="#slide-26">Partner lenses</a><a href="#slide-34">Actions</a>
  <a href="#evidence">Evidence</a>
</nav>
<main>
{sections}
<section id="evidence" class="report-section">
  <div class="eyebrow">Evidence coverage</div>
  <h2>The evidence is attributable, but independence remains the limiting factor</h2>
  <div class="grid">
    <article class="card"><strong>LEDGER</strong><p>{len(LEDGER)} sourced rows; {confidence.get('high',0)} high-confidence and {confidence.get('medium',0)} medium-confidence.</p></article>
    <article class="card"><strong>SOURCE MIX</strong><p>{source_types.get('official',0)} official, {source_types.get('press',0)} press, and {source_types.get('analyst',0)} analyst rows.</p></article>
    <article class="card"><strong>CAVEAT</strong><p>Specific company disclosures are attributable but predominantly vendor-published.</p></article>
    <article class="card"><strong>NEXT PROOF</strong><p>Independent benchmarks, production customers, supply assurance, support ownership, and partner economics.</p></article>
  </div>
</section>
<section id="references" class="report-section references">
  <div class="eyebrow">Primary sources</div><h2>Fifteen current sources anchor the screen</h2>
  <ul>{sources}</ul>
</section>
</main>
<footer>Closed-cohort public-evidence screen. Candidate readiness judgments require Phase 0 calibration before organization-specific use.</footer>
</body></html>"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
