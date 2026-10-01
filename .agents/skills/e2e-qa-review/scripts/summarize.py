#!/usr/bin/env python3
"""Turn sweep.mjs results into a findings table grouped by rule, for triage.

usage: python3 summarize.py qa/sweep-results.json > qa/SWEEP.md
Stdlib only. Flags findings that are usually measurement artefacts (references/false-greens.md) so they are
proved before anyone changes the site for them.
"""
import json
import sys
from collections import defaultdict

SUSPECT = {
    'target-size': 'if the sample says "partially obscured", test WCAG 2.4.11 directly (sticky header at scroll position)',
}


def main() -> None:
    src = sys.argv[1] if len(sys.argv) > 1 else 'qa/sweep-results.json'
    try:
        d = json.load(open(src))
    except FileNotFoundError:
        sys.exit(f'BLOCKED: {src} not found; the sweep did not run to completion, so there is nothing to summarise')
    rows = d['rows']
    out = [f"# Sweep: {d['loads']} page loads at {d['base']}", '']
    groups: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        at = f"{r['width']} {r['route']}"
        if not r['statusOk']:
            groups['HTTP status'].append(f"{at}: {r['status']}")
        for e in r['errs']:
            groups['Page errors'].append(f'{at}: {e}')
        for f in r['failed']:
            groups['Failed requests'].append(f'{at}: {f}')
        if r['h1'] != 1:
            groups['h1 count'].append(f"{at}: {r['h1']}")
        for s in r['skips']:
            groups['Heading skips'].append(f'{at}: {s}')
        if r['overflowX'] > 0:
            groups['Sideways scroll'].append(f"{at}: {r['overflowX']}px")
        for s in r['broken']:
            groups['Broken images'].append(f'{at}: {s}')
        if r['noBoxN']:
            groups['Images with no reserved box (CLS)'].append(f"{at}: {r['noBoxN']} e.g. {r['noBox'][:2]}")
        if r['small']:
            groups['Targets under the size floor'].append(f"{at}: {r['small']} e.g. {r['smallSample'][:3]}")
        if r['unrevealed']:
            groups['Reveals that never finished'].append(f"{at}: {r['unrevealed']}")
        if r.get('offFont'):
            groups['Text outside the declared fonts'].append(f"{at}: {', '.join(r['offFont'][:4])}")
        for h in r.get('emptyDisclosures', []):
            groups['Disclosures that open onto nothing'].append(f'{at}: "{h}"')
        for h in r.get('deadLinks', []):
            groups['Dead links in page content'].append(f'{at}: {h}')
        for v in r['axe']:
            note = f"  ({SUSPECT[v['id']]})" if v['id'] in SUSPECT else ''
            groups[f"axe {v['id']} ({v['impact']})"].append(f"{at}: {v['n']} node(s) {v['sample'][:1]}{note}")
        dz = r['design']
        if dz['emDash']:
            groups['Design: em dashes'].append(f"{at}: {dz['emDash']} e.g. {dz['emDashAt'][:2]}")
        if dz.get('straightQuotes'):
            groups['Design: straight quotes'].append(f"{at}: {dz['straightQuotes']} e.g. {dz['straightQuotesAt'][:2]}")
        if dz['counters']:
            groups['Design: numbered counters'].append(f"{at}: {dz['counters']}")
        if dz['italicHeads']:
            groups['Design: italic heading accents'].append(f"{at}: {dz['italicHeads'][:2]}")
        if dz.get('rasterIcons'):
            groups['Design: raster images used as icons (use SVG)'].append(f"{at}: {dz['rasterIcons'][:3]}")
        if r.get('lordiconNoCredit'):
            groups['Licence: Lordicon icon with no credit link'].append(at)
        if dz['pills']:
            groups['Design: pill buttons'].append(f"{at}: {dz['pills']}")
        if dz['eyebrowsPerH2'] > 0.34:
            groups['Design: eyebrow density > 1 per 3 sections'].append(f"{at}: {dz['eyebrowsPerH2']} per h2")
    if d.get('dupTitles'):
        groups['Duplicate titles'].extend(d['dupTitles'])
    if not groups:
        out.append('No findings.')
    for rule, items in groups.items():
        out.append(f'## {rule} ({len(items)})')
        out.extend(f'- {i}' for i in items[:12])
        if len(items) > 12:
            out.append(f'- ... {len(items) - 12} more')
        out.append('')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
