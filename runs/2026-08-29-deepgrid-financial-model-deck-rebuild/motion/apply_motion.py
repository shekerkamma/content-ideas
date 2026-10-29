#!/usr/bin/env python3
"""Turn motion-plan.json into officecli batch commands and apply them.

Two facts from this repo's notes govern the mechanics:
  * officecli only persists writes to Windows-side paths, so the deck must be
    staged under C:\\ before any of this runs.
  * officecli's own `get` reads the resident's memory, not the file, so it can
    never be the proof that a write landed. The proof is the md5 changing on
    disk plus an independent read by lint_motion.py.
"""
from __future__ import annotations
import json, sys

def build(plan_path: str, out_path: str) -> int:
    plan = json.load(open(plan_path))['plan']
    cmds = []
    for p in plan:
        n = p['slide']
        cmds.append({"command": "set", "path": f"/slide[{n}]",
                     "props": {"transition": f"{p['transition']}-{p['transition_ms']}"}})
        for step in p['steps']:
            for i, item in enumerate(step['items']):
                props = {
                    "effect": step['effect'],
                    "class": step['cls'],
                    "direction": step['direction'],
                    "duration": str(step['duration']),
                    # Only the band's first shape carries the step trigger; the
                    # rest ride withPrevious and are separated by delay, so the
                    # band reads as ONE step that fills left-to-right.
                    "trigger": step['trigger'] if i == 0 else "withPrevious",
                }
                if item['delay']:
                    props["delay"] = str(item['delay'])
                cmds.append({"command": "add", "parent": item['path'],
                             "type": "animation", "props": props})
    json.dump(cmds, open(out_path, 'w'))
    return len(cmds)

if __name__ == '__main__':
    print(build(sys.argv[1], sys.argv[2]), 'commands')
