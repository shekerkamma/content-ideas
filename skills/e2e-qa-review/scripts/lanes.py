#!/usr/bin/env python3
"""Run the specialist skills' deterministic checks as lanes of one QA run, and record every lane's outcome.

usage (from the site's directory): python3 lanes.py qa/lanes.json
exit 0 every applicable lane ran clean · 2 findings · 1 an applicable lane was BLOCKED.

Lanes (see references/lanes.md for who owns which defect):
  guidelines  web-design-guidelines/scripts/audit.mjs over the source tree (5 source regexes)
  impeccable  `npx impeccable@<pin> detect --json` over the source (Node >= 24); warnings gate, advisory drift is
              handed to the improve-ui reviewer
  scrollcraft scroll-craft/scripts/shoot.mjs at desktop, phone and reduced motion, ONLY when the build uses the
              scroll-craft engine (data-sc-act); otherwise recorded as not-applicable with the reason
A lane that cannot run is BLOCKED and says why. It is never dropped from the report, because a lane that skips
must not read as a lane that passed. Stdlib only.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

HOME = os.path.expanduser('~')
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def find_skill(name: str, cfg: dict) -> str | None:
    """Locate a peer skill: explicit config, env, sibling of this skill, host skill roots, plugin cache."""
    env = os.environ.get('E2E_QA_' + name.upper().replace('-', '_') + '_DIR')
    cands = [cfg.get('skillDirs', {}).get(name), env, os.path.join(os.path.dirname(SKILL_DIR), name),
             os.path.join(os.path.dirname(SKILL_DIR), 'ui-skills', 'skills', name)]
    cands += [os.path.join(r, name) for r in (f'{HOME}/.claude/skills', f'{HOME}/.agents/skills', '.agents/skills',
                                              '.claude/skills', f'{HOME}/.codex/skills')]
    cands += sorted(glob.glob(f'{HOME}/.claude/plugins/cache/*/*/*/skills/{name}'), reverse=True)
    return next((c for c in cands if c and os.path.isfile(os.path.join(c, 'SKILL.md'))), None)


def node_at_least(major: int) -> str | None:
    """A node binary new enough for the lane: PATH first, then the newest nvm install that qualifies."""
    bins = [shutil.which('node')] + sorted(glob.glob(f'{HOME}/.nvm/versions/node/v*/bin/node'),
                                           key=lambda p: [int(x) for x in re.findall(r'\d+', p.split('/v')[-1])[:3]],
                                           reverse=True)
    for b in filter(None, bins):
        try:
            v = subprocess.run([b, '-p', 'process.versions.node'], capture_output=True, text=True).stdout
            if int(v.split('.')[0]) >= major:
                return b
        except (OSError, ValueError):
            pass
    return None


def lane_guidelines(cfg: dict) -> dict:
    d = find_skill('web-design-guidelines', cfg)
    if not d:
        return {'status': 'blocked', 'reason': 'web-design-guidelines skill not found (set skillDirs or E2E_QA_WEB_DESIGN_GUIDELINES_DIR)'}
    node = node_at_least(18)
    src = cfg.get('src', '.')
    if not node or not os.path.isdir(src):
        return {'status': 'blocked', 'reason': f'node missing or source dir {src} not found'}
    r = subprocess.run([node, os.path.join(d, 'scripts', 'audit.mjs'), src], capture_output=True, text=True)
    if r.returncode or 'Audit complete' not in r.stdout:
        return {'status': 'blocked', 'reason': 'audit.mjs did not complete: ' + (r.stderr or r.stdout)[-300:]}
    found = []
    for line in r.stdout.splitlines():
        m = re.match(r'(.+?):(\d+): \[([^\]]+)\] (.*)', line)
        if m:
            found.append({'file': m[1], 'line': int(m[2]), 'rule': m[3], 'message': m[4]})
    n = re.search(r'across (\d+) file', r.stdout)
    if n and n[1] == '0':
        return {'status': 'blocked', 'reason': f'audit.mjs scanned 0 files under {src}: an empty population passes'}
    return {'status': 'ran', 'skill': d, 'scanned': int(n[1]) if n else None, 'findings': found}


IMPECCABLE_SKIP = re.compile(r'(^|/)(vendor|node_modules|dist|build|\.next|downloads)(/|$)|\.min\.(js|css)$')


def lane_impeccable(cfg: dict) -> dict:
    """Gate on warning and above over the SOURCE (what a fix edits). Advisory design-system drift is kept apart and
    handed to the improve-ui reviewer, whose contract/runtime/correction proofs are built for exactly that question."""
    pin = cfg.get('impeccableVersion', '4.1.0')
    node = node_at_least(24)
    if not node:
        return {'status': 'blocked', 'reason': 'impeccable needs Node >= 24 and none was found on PATH or under nvm'}
    targets = cfg.get('impeccableTargets') or [cfg.get('src', '.')]
    if not all(os.path.exists(t) for t in targets):
        return {'status': 'blocked', 'reason': f'impeccable target(s) {targets} not found'}
    npx = os.path.join(os.path.dirname(node), 'npx')
    env = {**os.environ, 'PATH': os.path.dirname(node) + os.pathsep + os.environ.get('PATH', '')}
    r = subprocess.run([npx, '--yes', f'impeccable@{pin}', 'detect', '--json', *targets],
                       capture_output=True, text=True, env=env, timeout=900)
    if r.returncode not in (0, 2):
        return {'status': 'blocked', 'reason': f'impeccable@{pin} exited {r.returncode}: ' + r.stderr[-300:]}
    try:
        items = json.loads(r.stdout or '[]')
    except json.JSONDecodeError:
        return {'status': 'blocked', 'reason': 'impeccable output was not JSON: ' + r.stdout[:200]}
    rows = [{'file': os.path.relpath(i.get('file', '')), 'line': i.get('line'), 'rule': i.get('antipattern'),
             'severity': i.get('severity'), 'category': i.get('category'), 'message': i.get('snippet') or i.get('name')}
            for i in items]
    rows = [x for x in rows if not IMPECCABLE_SKIP.search(x['file'])]  # a vendored library's colours are not the site's
    advisory = [x for x in rows if x['severity'] == 'advisory']
    by_rule: dict[str, int] = {}
    for x in advisory:
        by_rule[x['rule']] = by_rule.get(x['rule'], 0) + 1
    return {'status': 'ran', 'version': pin, 'targets': targets,
            'findings': [x for x in rows if x['severity'] != 'advisory'],
            'advisory': {'count': len(advisory), 'by_rule': by_rule, 'sample': advisory[:40],
                         'route': 'improve-ui reviewer (candidates only; each needs contract + runtime + correction)'}}


SHOOT_HEADS = ('DEAD SCROLL', 'FROZEN CLIP', 'LEGS THAT NEVER REACH', 'LEGS STUCK ON POSTER', 'CUES THAT NEVER PEAK',
               'CONTRAST FAIL', 'CONTRAST THIN', 'CONSOLE ERRORS', 'FAILED REQUESTS')


def parse_shoot(stdout: str, tag: str) -> list[dict]:
    """shoot.mjs prints each finding class as a heading followed by indented items (DEAD SCROLL is one line)."""
    found, head = [], None
    for line in stdout.splitlines():
        hit = next((h for h in SHOOT_HEADS if line.startswith(h)), None)
        if hit:
            head = hit
            rest = line[len(hit):].lstrip(' :(').strip()
            if hit == 'DEAD SCROLL' and rest:
                found.append({'file': tag, 'line': None, 'rule': hit, 'message': rest})
        elif head and line.startswith('  ') and line.strip():
            found.append({'file': tag, 'line': None, 'rule': head, 'message': line.strip()})
        elif not line.strip():
            head = None
    return found


def lane_scrollcraft(cfg: dict) -> dict:
    dist = cfg.get('dist', '')
    uses = False
    for f in glob.glob(os.path.join(dist, '**', '*.html'), recursive=True) + glob.glob(os.path.join(dist, '**', '*.js'), recursive=True):
        with open(f, errors='ignore') as fh:
            if 'data-sc-act' in fh.read():
                uses = True
                break
    if not uses:
        return {'status': 'not-applicable', 'reason': 'no data-sc-act in the build: the page does not use the scroll-craft '
                'engine, so its harness has nothing to read; generic scroll reveals are covered by the sweep'}
    d = find_skill('scroll-craft', cfg)
    if not d:
        return {'status': 'blocked', 'reason': 'the build uses scroll-craft but the skill was not found'}
    node = node_at_least(18)
    url = cfg.get('url') or cfg.get('base')
    out = cfg.get('scrollOut', 'qa/scroll')
    runs = {'desktop': [], 'phone': ['--width', '390', '--height', '844'], 'reduced': ['--reduced-motion']}
    found, logs, runs_state = [], {}, {}
    env = dict(os.environ)
    if cfg.get('scrollChrome'):  # must be a Chrome with h264: bundled Chromium paints posters and "passes"
        env['SCROLLCRAFT_CHROME'] = cfg['scrollChrome']
    for tag, extra in runs.items():
        cmd = [node, os.path.join(d, 'scripts', 'shoot.mjs'), '--url', url, '--out', f'{out}/{tag}', *extra]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=1200, env=env)
        retried = bool(r.returncode) and 'TimeoutError' in (r.stderr + r.stdout)
        if retried:  # headless screenshots under WSL time out intermittently, on a different pass each run
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=1200, env=env)
        if r.returncode:  # shoot.mjs exits 0 whatever it finds; non-zero means that pass could not run
            err = (r.stderr or r.stdout).strip().splitlines()
            runs_state[tag] = 'blocked: ' + next((x for x in err if 'Error' in x or 'error' in x), err[-1] if err else '?')[:200]
            continue
        runs_state[tag] = 'ran after one retry' if retried else 'ran'
        logs[tag] = f'{out}/{tag}/sheet.png'
        found += parse_shoot(r.stdout, tag)
    # one blocked pass must not discard the passes that ran; the lane is still BLOCKED until all three run
    blocked = {k: v for k, v in runs_state.items() if not v.startswith('ran')}
    res = {'status': 'blocked' if blocked else 'ran', 'skill': d, 'passes': runs_state, 'sheets': logs, 'findings': found}
    if blocked:
        res['reason'] = '; '.join(f'{k} {v}' for k, v in blocked.items())
    return res


LANES = {'guidelines': lane_guidelines, 'impeccable': lane_impeccable, 'scrollcraft': lane_scrollcraft}


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else 'qa/lanes.json'
    if not os.path.isfile(path):
        sys.exit(f'BLOCKED: config {path} not found (see references/config.md)')
    cfg = json.load(open(path))
    out = {}
    for name in cfg.get('lanes', list(LANES)):
        try:
            out[name] = LANES[name](cfg)
        except subprocess.TimeoutExpired as e:
            out[name] = {'status': 'blocked', 'reason': f'timed out after {e.timeout}s'}
        res = out[name]
        n = len(res.get('findings', []))
        print(f"{name:12} {res['status']:15} {n:>4} findings  {res.get('reason', '')[:160]}")
    dest = cfg.get('out', 'qa/lanes-results.json')
    os.makedirs(os.path.dirname(dest) or '.', exist_ok=True)
    json.dump(out, open(dest, 'w'), indent=1)
    blocked = [k for k, v in out.items() if v['status'] == 'blocked']
    findings = sum(len(v.get('findings', [])) for v in out.values())
    print(f'-> {dest}')
    sys.exit(1 if blocked else 2 if findings else 0)


if __name__ == '__main__':
    main()
