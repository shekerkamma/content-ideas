#!/usr/bin/env python3
"""merge_authoring.py — fold authored batches into the slide envelopes.

Authoring happens in bounded batches (<=4 slides) per
`references/batch-authoring.md`. Each batch file is a plain map of
slide_id -> {field: value}. Merging is additive and explicit:

  * a batch may only fill fields that are null, or fields it names under
    "_override" — so an authored sentence can never silently replace recovered
    source material without the batch saying so;
  * every write is logged, so `authoring-log.json` shows which fields on which
    slides are authored rather than recovered. That distinction is the whole
    point: recovered text is the source's own words, authored text is mine.

  python3 merge_authoring.py --envelopes slide-envelopes.json --batch authoring/batch-01.json
"""
import argparse, json, pathlib, datetime

FIELDS = {'analytical_question', 'executive_answer', 'counterargument', 'falsifier',
          'implication', 'decision', 'owner', 'trigger', 'stop_or_escalate_rule',
          'archetype', 'dominant_exhibit'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--envelopes', required=True)
    ap.add_argument('--batch', required=True, nargs='+')
    ap.add_argument('--log', default='authoring-log.json')
    a = ap.parse_args()

    doc = json.load(open(a.envelopes))
    by_id = {e['slide_id']: e for e in doc['slides']}
    log = json.load(open(a.log)) if pathlib.Path(a.log).exists() else {'entries': []}

    wrote = skipped = 0
    for bf in a.batch:
        batch = json.load(open(bf))
        override = set(batch.pop('_override', []))
        for sid, fields in batch.items():
            e = by_id[int(sid)]
            for k, v in fields.items():
                if k == 'logic':
                    e['logic'] = {**e.get('logic', {}), **{kk: vv for kk, vv in v.items() if vv}}
                    log['entries'].append({'slide': int(sid), 'field': 'logic', 'batch': bf})
                    wrote += 1
                    continue
                if k not in FIELDS:
                    raise SystemExit(f'{bf}: slide {sid}: unknown field {k!r}')
                key = f'{sid}.{k}'
                if e.get(k) and key not in override:
                    skipped += 1
                    continue
                e[k] = v
                log['entries'].append({'slide': int(sid), 'field': k, 'batch': bf})
                wrote += 1

    json.dump(doc, open(a.envelopes, 'w'), indent=1)
    log['updated_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    json.dump(log, open(a.log, 'w'), indent=1)

    done = [e for e in doc['slides']
            if all(e.get(f) for f in ('analytical_question', 'executive_answer', 'counterargument',
                                      'falsifier', 'implication', 'decision', 'owner', 'trigger',
                                      'stop_or_escalate_rule'))]
    print(f'wrote {wrote} fields, skipped {skipped} already-present')
    print(f'slides with a COMPLETE envelope: {len(done)} of {len(doc["slides"])}')


if __name__ == '__main__':
    main()
