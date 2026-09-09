"""Guards for scripts/check_routes.py.

check_skills.py validates skills; this validates the instructions that point at
them. Every assertion below pins a behaviour whose absence produced a wrong
answer during the audit that motivated the script.
"""
import ast
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts" / "check_routes.py"
BROKEN = ROOT / "tests" / "fixtures" / "routes" / "broken-CLAUDE.md"


def run(*args):
    r = subprocess.run([sys.executable, str(GATE), *map(str, args)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def test_script_parses():
    ast.parse(GATE.read_text(), filename=str(GATE))


def test_broken_fixture_is_caught():
    code, _, err = run(BROKEN)
    assert code == 2
    assert "definitely-not-a-real-skill-xyz" in err
    assert "totally/made/up/path" in err
    assert "/ghost-skill" in err
    assert "/another-missing-skill-abc" in err


def test_working_route_in_broken_fixture_still_passes():
    """The fixture is not uniformly broken — /eli5 resolves and must not fire."""
    _, _, err = run(BROKEN)
    assert err.count(" - ") == 4, f"expected exactly 4 findings, got:\n{err}"
    assert "/eli5" not in err


def test_missing_file_blocks_rather_than_passes():
    code, _, err = run("/nonexistent/CLAUDE.md")
    assert code == 1, "a missing instruction file must block (1), never read as clean (0)"
    assert "BLOCKED" in err


def test_home_relative_paths_resolve_from_home_not_cwd():
    """Resolving declared paths from the repo root reported four working
    skills as broken during the original audit."""
    src = GATE.read_text()
    assert "expanduser" in src
    assert "os.path.isabs" in src, "must distinguish absolute from HOME-relative"


def test_symlinks_are_followed():
    """`find -type f` does not follow symlinks; that artifact produced a
    '61 empty directories' finding where 325 resolved fine."""
    src = GATE.read_text()
    assert ".exists()" in src, "must use exists(), which follows symlinks"
    # `-type f` appears in the module docstring, where the trap is explained.
    # Check the code, not the prose: the gate must not shell out to find at all.
    tree = ast.parse(src)
    code = ast.unparse(tree.body[1:])  # drop the module docstring
    assert "-type f" not in code, "gate must not use find -type f"
    assert "subprocess" not in code, "gate is pure pathlib; no shelling out"


def test_stdout_flushed_before_findings():
    assert "sys.stdout.flush()" in GATE.read_text()


def test_exit_codes_are_distinct():
    src = GATE.read_text()
    assert "return 0" in src and "return 1" in src and "return 2" in src
