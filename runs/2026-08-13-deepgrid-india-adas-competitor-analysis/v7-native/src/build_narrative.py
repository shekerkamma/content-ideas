#!/usr/bin/env python3
"""build_narrative.py — the storyboard the deck was missing.

Applies /narrative-builder (Pyramid Principle + SCQA) to the 73 bound slides.

The defect it fixes: the source order splits every competitor across four
separate blocks — evidence at slide 20, threat at 22, move at 21, falsifier at
59 — so no competitor is ever argued in one place, and the reader cannot hold
the case against anyone. Grouping is the whole point of a storyboard.

Writes narrative.json (acts, order, act questions, pyramid, hostile questions),
consumed by build_bound_deck.mjs.

    python3 src/build_narrative.py
"""
import json
import re

ENTITIES = [
    ('Starkenn', r'starkenn'), ('Gahan', r'gahan'), ('drivebuddyAI', r'drivebuddy'),
    ('ZF', r'\bzf\b'), ('Aptiv', r'aptiv'), ('STRADVISION', r'stradvision'),
    ('Sterling×MINIEYE', r'sterling|minieye'), ('bitsensing', r'bitsensing'),
    ('Netrasemi', r'netrasemi'), ('Incumbent bundle', r'incumbent|bosch|continental|valeo'),
]
# the market map that names three rivals is a field page, not a Starkenn page
FIELD_OVERRIDE = {8}
FALSIFIER = re.compile(
    r'falsifier|watchlist|raise on|remains adjacent|unproven until|keep as conditional'
    r'|until .*verified|global scale|only if its .*verified'
    r'|confirm control', re.I)
# "evidence assessment", "credible ... pending", "appears ahead" read as falsifier
# language but are the entity's opening evidence page; they lead the group.
EVIDENCE_LEAD = re.compile(
    r'evidence assessment|competitive profile|evidence profile|structural threat'
    r'|appears ahead|signals material|credible .*(comparator|signal|player|option)'
    r'|not established|not direct|positioning map', re.I)

ACTS = [
    {'id': 'A1', 'no': 'Act I', 'name': 'The verdict',
     'question': 'What should DeepGrid do, before any of the evidence?',
     'settles': 'The answer, the four gates that fund it, and the five claims that stop.',
     'slides': [1, 2, 3, 4]},
    {'id': 'A2', 'no': 'Act II', 'name': 'The field',
     'question': 'Who occupies India CV ADAS, and what does each arena actually reward?',
     'settles': 'Four arenas, four control points, and the three rivals that earn war-room time.',
     'slides': [5, 6, 7, 8, 11, 12, 13]},
    {'id': 'A3', 'no': 'Act III', 'name': 'The contest',
     'question': 'Against each rival: what is proven, where are they strong, and what would change the rating?',
     'settles': 'Ten competitors, each argued in one place — evidence, threat by arena, our move, the falsifier.',
     'slides': []},                      # filled by entity grouping
    {'id': 'A4', 'no': 'Act IV', 'name': 'The wedge',
     'question': 'What exactly does DeepGrid sell, and why would an integrator embed it?',
     'settles': 'A bounded perception subsystem, a productised integration boundary, and a costed path.',
     'slides': [14, 10, 15, 16, 40, 41, 42, 43, 44, 56, 71, 73]},
    {'id': 'A5', 'no': 'Act V', 'name': 'The plan',
     'question': 'What must be true in 90 days, and who owns each gate?',
     'settles': 'A dated sprint, quarterly evidence gates, a war room, and the rule for moving a threat score.',
     'slides': [37, 38, 39, 55, 57, 72]},
]

PYRAMID = {
    'governing_thought':
        'DeepGrid cannot win India CV ADAS as a full-system supplier — ZF and Aptiv own braking, '
        'ECU, calibration, approval and warranty. It can win as the bounded perception layer an '
        'accountable integrator embeds, and the only thing between here and there is reproducible '
        'evidence that four funded gates buy in 90 days.',
    'supports': [
        {'claim': 'The field is occupied by control point, not by product.',
         'because': 'A competitor is dangerous when it owns something DeepGrid must pass through. '
                    'ZF and Aptiv hold the gates that decide a programme; no feature answers that.',
         'proof': 'Act II · four arenas, four control points'},
        {'claim': 'No competitor placement in this dossier is independently verified.',
         'because': 'Every rating rests on company statements, not on procurement or homologation '
                    'artifacts, so the war room must move scores on evidence events rather than announcements.',
         'proof': 'Act III · ten evidence ladders and falsifiers'},
        {'claim': 'DeepGrid’s current claims outrun its evidence, and that is the binding constraint.',
         'because': 'The April-2026 mandate date is wrong, five claims are unsupported, and a projected '
                    'die price is being compared to a system price. Proof deficit — not feature deficit — is what blocks entry.',
         'proof': 'Act IV · the wedge · Act V · the 90-day sprint'},
    ],
}

HOSTILE = [
    ('“India-native” is our differentiator — why retire it?',
     'It is not a control point. Government buyers reward demonstrable performance and procurement '
     'credibility; nationality alone has never cleared a homologation gate. Lead with measured '
     'constrained-compute VRU performance instead.'),
    ('If ZF and Aptiv own the vehicle, is there any position left at all?',
     'Yes — the perception layer they choose to embed. That is a Tier-2 position inside their safety '
     'case, which is exactly why the market-entry event is a named braking Tier-1 accepting our '
     'interfaces, not an OEM win.'),
    ('Starkenn shows 2,500+ vehicles. Are we not already behind?',
     'That figure is an attributed claim, not a verified fact, and it sits in mining retrofit — the '
     'arena with the lowest integration bar. Their government and OEM evidence is unverified. '
     'Field access is real; qualification is not demonstrated.'),
    ('The ASIC gives us a 3–7× cost advantage. Why gate the capital?',
     'Because a projected die price is not comparable to a system price. The bridge must carry NRE, '
     'yield, package, qualification, warranty and lifecycle. Commission the break-even model first; '
     'the direction is not the magnitude.'),
    ('Why only four gates? Can we not run more in parallel?',
     'Four parallel gates already exceed the engineering and management capacity of a company this '
     'size. Running six dilutes all of them rather than clearing any one. The stop rule is explicit: '
     're-plan if two of four miss their first milestone.'),
    ('What would make you change this recommendation?',
     'A named Indian CV OEM qualifying DeepGrid directly, with no braking Tier-1 in the loop, before '
     '1 October 2027. That single observable overturns the attach-and-prove thesis, and it is on the page.'),
]


def entity_of(title, sid):
    if sid in FIELD_OVERRIDE:
        return None
    for name, rx in ENTITIES:
        if re.search(rx, title, re.I):
            return name
    return None


def role_rank(o):
    """evidence → threat by arena → our move → the falsifier."""
    t = o['spine']['action_title']
    if re.search(r'falsifier', t, re.I):     # explicit wins over the lead phrases
        return 3
    if EVIDENCE_LEAD.search(t):
        return 0
    if FALSIFIER.search(t):
        return 3
    return {'P1': 0, 'P2': 1, 'P7': 1}.get(o['pattern_id'], 2)


def main():
    bound = json.load(open('bound-envelopes.json'))['slides']
    by_id = {o['slide_id']: o for o in bound}

    groups, order3 = [], []
    for name, _ in ENTITIES:
        ids = [o['slide_id'] for o in bound
               if entity_of(o['spine']['action_title'], o['slide_id']) == name]
        ids.sort(key=lambda i: (role_rank(by_id[i]), i))
        groups.append({'entity': name, 'slides': ids})
        order3 += ids
    ACTS[2]['slides'] = order3
    ACTS[2]['groups'] = groups

    order, seen = [], set()
    for act in ACTS:
        for sid in act['slides']:
            if sid in seen:
                raise SystemExit(f'slide {sid} assigned to two acts')
            seen.add(sid)
            order.append({'slide_id': sid, 'act': act['id']})
    missing = sorted(set(by_id) - seen)
    if missing:
        raise SystemExit(f'unassigned slides: {missing}')

    out = {'contract_version': 'narrative-1.0',
           'core_message': PYRAMID['governing_thought'],
           'scqa': {
               'situation': 'India CV ADAS is already occupied — by control point, not by product. '
                            'ZF and Aptiv hold braking, ECU, calibration, approval and warranty.',
               'complication': 'DeepGrid’s claims outrun its evidence: the mandate date is wrong, five '
                               'claims are unsupported, and no competitor placement here is independently verified.',
               'question': 'Where can DeepGrid still win, against whom, and what must be true first?',
               'answer': 'Attach and prove. Sell a bounded perception subsystem inside an accountable '
                         'integrator, fund four evidence gates, and decide in 90 days.'},
           'acts': [{k: v for k, v in a.items() if k != 'slides'} | {'slides': a['slides']} for a in ACTS],
           'pyramid': PYRAMID, 'hostile_questions': HOSTILE, 'order': order}
    json.dump(out, open('narrative.json', 'w'), indent=1, ensure_ascii=False)

    print(f'narrative.json · {len(order)} slides across {len(ACTS)} acts')
    for a in ACTS:
        print(f"  {a['no']:<7} {a['name']:<14} {len(a['slides']):>2} pages")
    print('\nAct III grouping (evidence → threat → move → falsifier):')
    for g in groups:
        print(f"  {g['entity']:<18} {g['slides']}")


if __name__ == '__main__':
    main()
