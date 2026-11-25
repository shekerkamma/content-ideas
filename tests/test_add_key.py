"""scripts/add_key.py writes a key to both layers and never prints it."""
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "add_key.py"
VALUE = "test-VALUE-not-a-real-key-0001"


def run(tmp, name, value=VALUE, extra=(), stdin_value=True):
    proj = tmp / "proj"
    (proj / ".claude").mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(SCRIPT), name, "--project-dir", str(proj),
           "--bashrc", str(tmp / "bashrc"), *extra]
    if stdin_value:
        cmd.append("--stdin")
    p = subprocess.run(cmd, input=(value + "\n") if stdin_value else None,
                       stdin=None if stdin_value else subprocess.DEVNULL,
                       capture_output=True, text=True, start_new_session=True)
    return p, proj / ".claude" / "settings.local.json", tmp / "bashrc"


def test_adds_to_both_layers_and_never_prints_value(tmp_path):
    p, settings, bashrc = run(tmp_path, "NEW_SERVICE_API_KEY")
    assert p.returncode == 0, p.stderr
    assert VALUE not in p.stdout and VALUE not in p.stderr
    assert json.loads(settings.read_text())["env"]["NEW_SERVICE_API_KEY"] == VALUE
    assert bashrc.read_text() == f"export NEW_SERVICE_API_KEY={VALUE}\n"
    assert stat.S_IMODE(settings.stat().st_mode) == 0o600


def test_keeps_other_settings_and_replaces_existing_entries(tmp_path):
    proj = tmp_path / "proj" / ".claude"
    proj.mkdir(parents=True)
    (proj / "settings.local.json").write_text(json.dumps(
        {"env": {"OTHER": "keep", "K": "old"}, "permissions": {"allow": ["x"]}}))
    (tmp_path / "bashrc").write_text(
        "alias ll='ls -l'\nexport K=old\nexport OTHER=keep\nexport K=older\n")
    p, settings, bashrc = run(tmp_path, "K")
    assert p.returncode == 0, p.stderr
    assert "replaced" in p.stdout
    data = json.loads(settings.read_text())
    assert data["env"] == {"OTHER": "keep", "K": VALUE}
    assert data["permissions"] == {"allow": ["x"]}
    assert bashrc.read_text() == f"alias ll='ls -l'\nexport K={VALUE}\nexport OTHER=keep\n"


def test_value_with_quotes_and_spaces_survives_the_shell(tmp_path):
    tricky = "a b'c\"$HOME`x`"
    p, _, bashrc = run(tmp_path, "TRICKY", value=tricky)
    assert p.returncode == 0, p.stderr
    out = subprocess.run(["bash", "-c", f'source "{bashrc}"; printf %s "$TRICKY"'],
                         capture_output=True, text=True).stdout
    assert out == tricky


def test_refuses_bad_name_empty_value_and_broken_json(tmp_path):
    p, settings, bashrc = run(tmp_path, "lower-case")
    assert p.returncode == 2 and not settings.exists() and not bashrc.exists()
    p, settings, bashrc = run(tmp_path, "EMPTY", value="  ")
    assert p.returncode == 1 and not settings.exists() and not bashrc.exists()
    settings.write_text("{ not json")
    p, settings, bashrc = run(tmp_path, "K")
    assert p.returncode == 1 and "not valid JSON" in p.stderr
    assert settings.read_text() == "{ not json" and not bashrc.exists()


def test_without_a_terminal_it_refuses_instead_of_reading_visibly(tmp_path):
    p, settings, bashrc = run(tmp_path, "K", stdin_value=False)
    assert p.returncode == 3 and "own terminal" in p.stderr
    assert not settings.exists() and not bashrc.exists()
