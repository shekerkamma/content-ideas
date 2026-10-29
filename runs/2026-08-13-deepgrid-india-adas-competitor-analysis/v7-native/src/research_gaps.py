#!/usr/bin/env python3
"""research_gaps.py — hit the dossier's own named evidence gaps with live search.

Tool order per the project rule: You.com livecrawl → Exa → (Firecrawl separately
for full-page capture of whatever this surfaces). Every target below is a gap the
deck already states, so a hit either raises a rung or leaves the gap standing.

Writes research/raw/*.json and research/findings.json (dated points + image
candidates with their source URL). Nothing here is promoted into the deck
automatically — extraction and adjudication stay separate steps.

    python3 src/research_gaps.py
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path('research/raw')
OUT.mkdir(parents=True, exist_ok=True)
YOU = os.environ.get('YOU_API_KEY', '').strip()
EXA = os.environ.get('EXA_API_KEY', '').strip()

TARGETS = [
    ('aebs-dates', 'India AEBS commercial vehicle mandate notified date 2027 2028 gazette CMVR N2 N3',
     'The deck rebases an April-2026 claim to notified 2027–28 dates'),
    ('starkenn-scale', 'Starkenn Technologies ADAS vehicles deployed turnover government tender revenue',
     '2,500+ vehicles and 30% government tender revenue are attributed, not verified'),
    ('gahan', 'Gahan Technologies radar camera occupancy ADAS India TRL qualification OEM',
     'No corroborated fact proves Gahan leads; qualification chain unevidenced'),
    ('drivebuddyai', 'drivebuddyAI Roadzen contract heavy trucks fleet ADAS deployment India',
     'The ~$2.5m / 3,000-truck contract needs primary confirmation'),
    ('sterling-minieye', 'Sterling Tools MINIEYE partnership exchange filing India ADAS commercial vehicle',
     'Exchange-filed January 2026; no named Indian OEM nomination or SOP evidenced'),
    ('bitsensing', 'bitsensing Series B funding radar automotive partnership India',
     '$25m Series B is attributed; India procurement and homologation unproven'),
    ('stradvision', 'STRADVISION deployed vehicles SVNet India commercial vehicle programme',
     '4m+ deployed vehicles is a global figure; India CV specifics not established'),
    ('zf-aptiv-india', 'ZF Aptiv India commercial vehicle ADAS AEBS nomination OEM programme N2 N3',
     'Programme specifics still need corroboration; India CV verification pending'),
    ('netrasemi', 'Netrasemi edge AI SoC India automotive ADAS qualification',
     'Adjacent compute option; automotive artifacts would show direct relevance'),
]


def you_search(q):
    # host is ydc-index.io (no api. prefix) and livecrawl takes "all" — the
    # api./"always" pair 403s. Matches skills/you-com-search/scripts/search.py.
    body = json.dumps({'query': q, 'country': 'IN',
                       'livecrawl': 'all', 'livecrawl_formats': ['markdown']}).encode()
    req = urllib.request.Request('https://ydc-index.io/v1/search', data=body,
                                 headers={'X-API-Key': YOU, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def exa_search(q):
    body = json.dumps({'query': q, 'numResults': 8, 'type': 'auto',
                       'contents': {'text': {'maxCharacters': 1200},
                                    'extras': {'imageLinks': 3}}}).encode()
    req = urllib.request.Request('https://api.exa.ai/search', data=body,
                                 headers={'x-api-key': EXA, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


NUM = re.compile(r'(?:(?:US)?\$|₹|Rs\.?\s?)\s?[\d,.]+\s?(?:crore|cr|lakh|million|billion|m|bn)?'
                 r'|\b\d[\d,]{2,}\+?\s+(?:vehicles|trucks|units|buses)'
                 r'|\b(?:20)\d{2}\b', re.I)
DATE = re.compile(r'\b(20\d{2})-(\d{2})-(\d{2})')


def harvest(key, payload, engine):
    points, images = [], []
    rows = []
    if engine == 'you':
        rows = (payload.get('results') or {}).get('web') or []
        for w in rows:
            txt = ' '.join(w.get('snippets') or []) or w.get('description', '')
            points.append({'engine': 'you.com', 'url': w.get('url'), 'title': w.get('title'),
                           'published': w.get('page_age'), 'text': txt[:900],
                           'numbers': sorted(set(NUM.findall(txt)))[:12]})
            if w.get('thumbnail_url'):
                images.append({'src': w['thumbnail_url'], 'page': w.get('url'),
                               'title': w.get('title'), 'engine': 'you.com'})
    else:
        rows = payload.get('results') or []
        for w in rows:
            txt = w.get('text') or ''
            points.append({'engine': 'exa', 'url': w.get('url'), 'title': w.get('title'),
                           'published': w.get('publishedDate'), 'text': txt[:900],
                           'numbers': sorted(set(NUM.findall(txt)))[:12]})
            for im in ((w.get('extras') or {}).get('imageLinks') or []):
                images.append({'src': im, 'page': w.get('url'),
                               'title': w.get('title'), 'engine': 'exa'})
    return points, images


def main():
    if not YOU or not EXA:
        print('YOU_API_KEY / EXA_API_KEY not in env', file=sys.stderr)
        return 1
    all_findings = []
    for key, query, gap in TARGETS:
        rec = {'target': key, 'query': query, 'gap': gap, 'points': [], 'images': []}
        for engine, fn in (('you', you_search), ('exa', exa_search)):
            try:
                payload = fn(query)
                (OUT / f'{key}.{engine}.json').write_text(json.dumps(payload, indent=1))
                p, i = harvest(key, payload, engine)
                rec['points'] += p
                rec['images'] += i
            except Exception as exc:                       # a dead engine must not kill the run
                rec.setdefault('errors', []).append(f'{engine}: {exc}')
            time.sleep(0.6)
        dated = sum(1 for p in rec['points'] if p.get('published'))
        print(f"{key:<18} {len(rec['points']):>2} results ({dated} dated) · "
              f"{len(rec['images']):>2} images{' · ' + '; '.join(rec.get('errors', [])) if rec.get('errors') else ''}")
        all_findings.append(rec)
    Path('research/findings.json').write_text(
        json.dumps({'generated': time.strftime('%Y-%m-%d'), 'targets': all_findings},
                   indent=1, ensure_ascii=False))
    tot = sum(len(r['points']) for r in all_findings)
    img = sum(len(r['images']) for r in all_findings)
    print(f'\n{tot} results · {img} image candidates -> research/findings.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
