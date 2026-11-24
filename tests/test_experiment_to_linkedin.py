"""experiment-to-linkedin: template filling and post checking (stdlib, no browser)."""
import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills" / "experiment-to-linkedin"
FILL = SKILL / "scripts" / "fill_template.py"
CHECK = SKILL / "scripts" / "check_post.py"
TEMPLATE = SKILL / "assets" / "template.html"
VALUES = SKILL / "examples" / "code-mode.values.json"


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)


def test_skeleton_lists_every_placeholder(tmp_path):
    out = tmp_path / "skel.json"
    assert run(FILL, "skeleton", TEMPLATE, out).returncode == 0
    entries = json.loads(out.read_text())
    assert len(entries) == TEMPLATE.read_text().count("[[")
    assert [e["n"] for e in entries] == list(range(1, len(entries) + 1))
    assert all(e["value"] == "" for e in entries)


def test_example_values_fill_the_current_template(tmp_path):
    out = tmp_path / "carousel.html"
    r = run(FILL, "fill", TEMPLATE, VALUES, out)
    assert r.returncode == 0, r.stderr
    html = out.read_text()
    assert "[[" not in html and "]]" not in html
    assert "Code Mode cut conversation tokens by" in html
    assert 'style="--v:34.4"' in html and 'style="--max:40"' in html
    assert '<span class="k">CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=1</span>' in html  # html entry kept raw


def test_text_values_are_escaped(tmp_path):
    entries = json.loads(VALUES.read_text())
    entries[0] = {**entries[0], "value": "A & B <test>"}
    vals = tmp_path / "v.json"
    vals.write_text(json.dumps(entries))
    out = tmp_path / "c.html"
    assert run(FILL, "fill", TEMPLATE, vals, out).returncode == 0
    assert "A &amp; B &lt;test&gt;" in out.read_text()


def test_fill_refuses_wrong_count_hint_or_empty(tmp_path):
    entries = json.loads(VALUES.read_text())
    cases = {
        "short": entries[:-1],
        "hint": [{**entries[0], "hint": "something else"}] + entries[1:],
        "empty": [{**entries[0], "value": "  "}] + entries[1:],
    }
    for name, data in cases.items():
        vals = tmp_path / f"{name}.json"
        vals.write_text(json.dumps(data))
        out = tmp_path / f"{name}.html"
        r = run(FILL, "fill", TEMPLATE, vals, out)
        assert r.returncode == 1, name
        assert "FAIL" in r.stderr, name
        assert not out.exists(), name


def test_check_post_passes_example_and_fails_rejected(tmp_path):
    assert run(CHECK, SKILL / "examples" / "code-mode.md").returncode == 0
    rejected = tmp_path / "rejected.md"
    rejected.write_text(
        "I tested Code Mode. It used half the tokens.\n\n"
        "2. Setup: 24 notes.\n3. Tokens: 34.4k → 18k.\n4. Time: 38 s → 67 s.\n\n"
        'claude-cm() { CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=1 claude "$@"; }\n\n'
        "Tried Code Mode yet?\n"
    )
    r = run(CHECK, rejected)
    assert r.returncode == 1
    assert "FAIL  closer is not a question" in r.stdout
    assert "FAIL  no code in the post body" in r.stdout
