#!/usr/bin/env python3
"""assemble_envelopes.py — build slide content envelopes per the Accenture guide.

Schema is `references/accenture-guide-content-envelope.md` (OUTPUT INCLUDES):
action_title · analytical_question · executive_answer · evidence_blocks[] with
status and evidence IDs · logic.type/mechanism · counterargument · falsifier ·
implication · decision · owner · trigger · stop_or_escalate_rule ·
dominant_exhibit · archetype · source/speaker notes.

Most fields are RECOVERABLE rather than invented: the source pages already carry a
question (their subtitle), a bounded verdict, a falsifier, a decision and a
trigger. This assembles those and reports exactly which fields are missing, so
authoring effort goes only where the material is genuinely absent — and so no
field is silently filled with a template sentence.

  python3 assemble_envelopes.py --model slide-model.json \
      --ledger outputs/evidence-ledger.csv --out slide-envelopes.json
"""
import argparse, csv, json, re, collections

STATUS_MAP = {
    'supported':            'verified fact',
    'company_claim':        'attributed claim',
    'needs_qualification':  'qualified interpretation',
    'needs_primary_source': 'insufficient evidence',
}

# headings the source uses for each envelope role
ROLE = {
    'verdict':   re.compile(r'^(bounded verdict|verdict|key insight|analytical conclusion|strategic reading|comparative verdict)$', re.I),
    'falsifier': re.compile(r'^(falsifier|falsifier test|falsification criteria|falsifier criteria|what could break the view)$', re.I),
    'counter':   re.compile(r'^(counterargument|counter-?argument|competitive reading|evidence gap|caveat required|what remains unknown|scope gap|evidence boundary)$', re.I),
    'implication': re.compile(r'^(strategic implication|implication|so what.*)$', re.I),
    'decision':  re.compile(r'^(decision|decision gate|management action|governance response|recommended response)$', re.I),
    'trigger':   re.compile(r'^(trigger|stop condition|escalate|stop/escalate|next meeting output)$', re.I),
    'next':      re.compile(r'^(next steps?|next actions?|action items?|implementation steps?)$', re.I),
    'mechanism': re.compile(r'^(mechanism|causal mechanism|why this matters|how it works|value-chain mechanism|market mechanism|conversion mechanism)$', re.I),
}


def text_of(b):
    parts = [x for x in b.get('body', []) if x]
    tags = [t for t in b.get('tags', []) if t and t != b.get('heading')]
    return ' '.join(parts).strip() or ' · '.join(tags)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True)
    ap.add_argument('--ledger', required=True)
    ap.add_argument('--out', default='slide-envelopes.json')
    a = ap.parse_args()

    model = json.load(open(a.model))['slides']
    ledger = collections.defaultdict(list)
    for r in csv.DictReader(open(a.ledger)):
        if r['statement'].startswith('Slide headline:'):
            continue
        ledger[str(r['slide_id'])].append(r)

    out, missing = [], collections.Counter()
    for s in model:
        n = s['n']
        claims = ledger.get(str(n), [])
        roles = {k: None for k in ROLE}
        rest = []
        for b in s['blocks']:
            h = (b.get('heading') or '').strip()
            hit = next((k for k, rx in ROLE.items() if h and rx.match(h)), None)
            if hit and not roles[hit]:
                roles[hit] = {'heading': h, 'text': text_of(b)}
            else:
                rest.append(b)

        ev = [{
            'evidence_id': c['claim_id'],
            'claim': c['statement'],
            'status': STATUS_MAP.get(c['status'], c['status']),
            'competitor': c['competitor'],
            'arena': c['arena'],
            'gap': c['evidence_gap'],
            'confidence': c['confidence'],
        } for c in claims]

        env = {
            'slide_id': n,
            'archetype': None,                      # assigned by the builder
            'action_title': s['title'],
            'analytical_question': s['subtitle'] or None,
            'executive_answer': (roles['verdict'] or {}).get('text'),
            'evidence_blocks': ev,
            'logic': {'type': None, 'mechanism': (roles['mechanism'] or {}).get('text')},
            'counterargument': (roles['counter'] or {}).get('text'),
            'falsifier': (roles['falsifier'] or {}).get('text'),
            'implication': (roles['implication'] or {}).get('text'),
            'decision': (roles['decision'] or {}).get('text'),
            'owner': None,
            'trigger': (roles['trigger'] or {}).get('text'),
            'stop_or_escalate_rule': None,
            'supporting_blocks': [{'label': b.get('heading') or '', 'text': text_of(b),
                                   'tags': b.get('tags', [])} for b in rest],
            'source_note': f'Evidence ledger claims {claims[0]["claim_id"]}–{claims[-1]["claim_id"]}'
                           if claims else 'No ledger claims mapped',
        }
        for f in ('analytical_question', 'executive_answer', 'counterargument', 'falsifier',
                  'implication', 'decision', 'trigger'):
            if not env[f]:
                missing[f] += 1
        out.append(env)

    json.dump({'contract_version': '1.0', 'slide_count': len(out), 'slides': out},
              open(a.out, 'w'), indent=1)

    print(f'{len(out)} envelopes -> {a.out}')
    ec = [len(e['evidence_blocks']) for e in out]
    print(f'evidence blocks: total {sum(ec)} · min {min(ec)} · max {max(ec)}')
    print('\nfields still needing authoring (absent in the source material):')
    for f, c in missing.most_common():
        print(f'  {f:24s} {c:3d} of {len(out)}')
    print('\nfields always authored (never present in source): owner, stop_or_escalate_rule, logic.type')


if __name__ == '__main__':
    main()
