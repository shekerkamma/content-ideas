#!/usr/bin/env python3
"""capture_primary.py — Firecrawl the primary artifacts the gap search surfaced.

Why screenshots of the source pages rather than competitor marketing images: the
visual-sourcing rule routes exact-state evidence to EXTRACT. A capture of ZF's
own press note IS the evidence; a competitor's product render is decoration that
would sit in a dossier implying proof it does not carry.

Writes research/primary/<key>.md, .png and research/primary-manifest.json.

    python3 src/capture_primary.py
"""
import base64
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

OUT = Path('research/primary')
OUT.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get('FIRECRAWL_API_KEY', '').strip()

# Each entry names the dossier claim it tests, so a capture is never "interesting
# but unattached". URLs are resolved from research/findings.json by matching the
# host — hand-typing them risks inventing a source that was never returned.
WANT = [
    ('zf-india-nomination', 'zf-aptiv-india', ('zf.com',),
     'ZF: "programme specifics still need corroboration"'),
    ('aptiv-gen6-india', 'zf-aptiv-india', ('aptiv.com', 'ir.aptiv.com'),
     'Aptiv: India CV specifics require verification'),
    ('stradvision-india-cv', 'stradvision', ('prnewswire.com',),
     'STRADVISION: "India CV specifics not established"'),
    ('drivebuddyai-expansion', 'drivebuddyai', ('globenewswire.com',),
     'drivebuddyAI: dossier stops at the initial $2.5m / 3,000 trucks'),
    ('drivebuddyai-ir', 'drivebuddyai', ('investors.roadzen.io', 'roadzen'),
     'drivebuddyAI: contract needs primary confirmation'),
    ('sterling-minieye-filing', 'sterling-minieye', ('thehindubusinessline.com', 'businessupturn.com'),
     'Sterling\u00d7MINIEYE: exchange-filed partnership, no named OEM nomination'),
    ('india-adas-dates', 'aebs-dates', ('economictimes', 'morth'),
     'Regulatory: April-2026 mandate claim rebased to notified 2027\u201328'),
]


def resolve():
    F = json.load(open('research/findings.json'))
    by_target = {t['target']: t for t in F['targets']}
    out = []
    for key, target, hosts, tests in WANT:
        urls = [p['url'] for p in by_target.get(target, {}).get('points', [])
                if p.get('url') and any(h in p['url'] for h in hosts)]
        seen, uniq = set(), []
        for u in urls:
            if u not in seen:
                seen.add(u)
                uniq.append(u)
        if uniq:
            out.append((key, uniq[0], tests))
        else:
            print(f'{key:<24} SKIPPED   no result matched {hosts}')
    return out


def scrape(url, formats):
    body = json.dumps({'url': url, 'formats': formats, 'onlyMainContent': True,
                       'timeout': 45000}).encode()
    req = urllib.request.Request(
        'https://api.firecrawl.dev/v2/scrape', data=body,
        headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def main():
    if not KEY:
        print('FIRECRAWL_API_KEY not in env', file=sys.stderr)
        return 1
    manifest = []
    for key, url, tests in resolve():
        rec = {'key': key, 'url': url, 'tests_claim': tests}
        try:
            res = scrape(url, ['markdown', {'type': 'screenshot', 'fullPage': False}])
            data = res.get('data') or {}
            md = data.get('markdown') or ''
            (OUT / f'{key}.md').write_text(md)
            rec['markdown_chars'] = len(md)
            rec['title'] = (data.get('metadata') or {}).get('title')
            rec['published'] = ((data.get('metadata') or {}).get('publishedTime')
                                or (data.get('metadata') or {}).get('article:published_time'))
            shot = data.get('screenshot')
            if shot:
                if shot.startswith('http'):
                    with urllib.request.urlopen(shot, timeout=60) as r:
                        png = r.read()
                else:
                    png = base64.b64decode(shot.split(',', 1)[-1])
                (OUT / f'{key}.png').write_bytes(png)
                rec['screenshot_bytes'] = len(png)
            rec['status'] = 'captured'
        except Exception as exc:
            rec['status'] = 'failed'
            rec['error'] = str(exc)[:160]
        print(f"{key:<24} {rec['status']:<9} "
              f"{rec.get('markdown_chars', 0):>6} chars  "
              f"{rec.get('screenshot_bytes', 0):>7} png  {rec.get('error', '')}")
        manifest.append(rec)
        time.sleep(1.0)
    Path('research/primary-manifest.json').write_text(
        json.dumps({'generated': time.strftime('%Y-%m-%d'), 'sources': manifest},
                   indent=1, ensure_ascii=False))
    ok = sum(1 for m in manifest if m['status'] == 'captured')
    print(f'\n{ok}/{len(manifest)} captured -> research/primary/')
    return 0


if __name__ == '__main__':
    sys.exit(main())
