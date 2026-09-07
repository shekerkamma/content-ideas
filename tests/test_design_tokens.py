"""Contract tests for skills/design-tokens.

The dependency-free half runs everywhere. The render gates need Playwright, a
Chromium build, and axe-core, so their behavioural tests skip when those are
absent — but the *static* guarantee that no gate can silently skip is asserted
unconditionally, because that is the property the port exists to protect.
"""
from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "design-tokens"
SCRIPTS = SKILL / "scripts"
FIXTURES = SKILL / "assets" / "fixtures"

GATES = [
    "measure_render", "verify_states", "axe_audit", "verify_target_size",
    "verify_keyboard", "verify_focustrap", "verify_overflow",
    "verify_responsive", "verify_reduced_motion", "verify_rtl",
]


def run(*args, **kw):
    return subprocess.run(args, capture_output=True, text=True, cwd=SKILL, **kw)


# --- the token contract: stdlib only, always runs -------------------------

def test_validators_pass_on_bundled_assets():
    r = run("bash", str(SCRIPTS / "check.sh"))
    assert r.returncode == 0, r.stdout + r.stderr


@pytest.mark.parametrize("script", [
    "validate_tokens.py", "validate_contrast.py",
    "validate_theme_refs.py", "lint_hardcodes.py",
])
def test_validators_are_stdlib_only(script):
    """No pip install may stand between this repo and its token gate."""
    tree = ast.parse((SCRIPTS / script).read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    allowed = {
        "json", "re", "sys", "pathlib", "argparse", "collections",
        "itertools", "math", "os", "textwrap", "contrast", "__future__",
    }
    assert imported <= allowed, f"{script} imports {imported - allowed}"


def test_contrast_validator_fails_a_failing_pair(tmp_path):
    """A gate that cannot fail is not a gate."""
    import json
    colors = json.loads((SKILL / "assets" / "tokens" / "colors.json").read_text())
    colors["semantic"]["text"]["primary"]["$value"] = "#c9d1d9"  # 1.5:1 on white
    bad = tmp_path / "colors.json"
    bad.write_text(json.dumps(colors))
    r = run(sys.executable, str(SCRIPTS / "validate_contrast.py"), str(bad))
    assert r.returncode == 1, r.stdout


# --- the property the port exists to protect ------------------------------

@pytest.mark.parametrize("gate", GATES)
def test_gate_has_no_silent_skip(gate):
    """Upstream exited 0 when Playwright was missing. That must never come back.

    A render gate may only exit 0 after it has rendered something. Every
    unavailability path goes through lib/browser.mjs and exits 1.
    """
    source = (SCRIPTS / f"{gate}.mjs").read_text(encoding="utf-8")
    assert "SKIPPED" not in source, f"{gate} reintroduced a silent skip"
    assert "openBrowser" in source, f"{gate} bypasses the preflight"
    assert "chromium.launch" not in source, f"{gate} launches a browser directly"
    # Nothing may exit 0 before a page has been rendered: the only clean exit is
    # one the gate reaches after measuring something.
    launched = source.index("openBrowser()")
    for m in re.finditer(r"process\.exit\(0\)", source):
        assert m.start() > launched, (
            f"{gate} can exit 0 at offset {m.start()}, before the browser opens"
        )


@pytest.mark.parametrize("gate", GATES)
def test_gate_uses_findings_exit_code(gate):
    """Exit 1 means blocked and only blocked; findings are exit 2."""
    source = (SCRIPTS / f"{gate}.mjs").read_text(encoding="utf-8")
    assert "process.exit(1)" not in source, f"{gate} still conflates blocked with findings"
    assert "FINDINGS" in source


def test_axe_gate_never_reaches_the_network():
    source = (SCRIPTS / "axe_audit.mjs").read_text(encoding="utf-8")
    assert "cdnjs" not in source and "https://" not in source.split("*/", 1)[-1], (
        "axe-core must load from the local install only — a CDN rule set can drift"
    )


def test_run_gates_blocks_on_a_missing_target():
    r = run("bash", str(SCRIPTS / "run_gates.sh"), "does-not-exist.html")
    assert r.returncode == 1
    assert "BLOCKED" in r.stderr + r.stdout


def test_broken_fixture_is_still_broken_by_construction():
    """If the negative control is repaired, every clean result becomes unfalsifiable."""
    html = (FIXTURES / "broken" / "index.html").read_text(encoding="utf-8")
    assert "#b9c0c8" in html          # 1.4.3
    assert "900px" in html            # 1.4.10
    assert "animation: spin" in html  # 2.3.3
    assert 'role="button"' in html    # 2.1.1
    assert "@media (prefers-reduced-motion" not in html


# --- behavioural: needs a browser ----------------------------------------

def _browser_available() -> bool:
    if not shutil.which("node"):
        return False
    probe = subprocess.run(
        ["node", "-e", "import('playwright').then(()=>process.exit(0),()=>process.exit(1))"],
        capture_output=True, cwd=SKILL,
    )
    return probe.returncode == 0


needs_browser = pytest.mark.skipif(
    not _browser_available(), reason="playwright not importable"
)


@needs_browser
def test_clean_fixture_passes_every_gate():
    env = {**os.environ, "DESIGN_TOKENS_CHROMIUM": "auto"}
    r = subprocess.run(
        ["bash", str(SCRIPTS / "run_gates.sh"), "assets/fixtures/brandkit/index.html"],
        capture_output=True, text=True, cwd=SKILL, env=env,
    )
    if r.returncode == 1:
        pytest.skip(f"no Chromium build available: {r.stderr.strip()[:120]}")
    assert r.returncode == 0, r.stdout + r.stderr


@needs_browser
def test_broken_fixture_fails_the_gates():
    env = {**os.environ, "DESIGN_TOKENS_CHROMIUM": "auto"}
    r = subprocess.run(
        ["bash", str(SCRIPTS / "run_gates.sh"), "assets/fixtures/broken/index.html"],
        capture_output=True, text=True, cwd=SKILL, env=env,
    )
    if "BLOCKED" in r.stdout and r.returncode == 1:
        pytest.skip("no Chromium build available")
    assert r.returncode == 2, r.stdout + r.stderr
    for gate in ("contrast", "states", "target-size", "responsive", "reduced-motion"):
        assert gate in r.stdout


@needs_browser
def test_keyboard_gate_sees_a_control_outside_the_tab_order():
    """The upstream collection loop filtered this defect out of the population."""
    env = {**os.environ, "DESIGN_TOKENS_CHROMIUM": "auto"}
    r = subprocess.run(
        ["node", str(SCRIPTS / "verify_keyboard.mjs"), "assets/fixtures/broken/index.html"],
        capture_output=True, text=True, cwd=SKILL, env=env,
    )
    if r.returncode == 1:
        pytest.skip("no Chromium build available")
    assert r.returncode == 2
    assert "A0 not-in-tab-order" in r.stdout
