"""scripts/add_key.py writes a key to settings.local.json and keys.env, never prints it,
and --migrate moves secret exports out of .bashrc."""
import json
import stat
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "add_key.py"
VALUE = "test-VALUE-not-a-real-key-0001"


def run(tmp, *args, value=VALUE, stdin_value=True):
    proj = tmp / "proj"
    (proj / ".claude").mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(SCRIPT), *args, "--project-dir", str(proj),
           "--bashrc", str(tmp / "bashrc"), "--keys-file", str(tmp / "cfg" / "keys.env")]
    if stdin_value:
        cmd.append("--stdin")
    p = subprocess.run(cmd, input=(value + "\n") if stdin_value else None,
                       stdin=None if stdin_value else subprocess.DEVNULL,
                       capture_output=True, text=True, start_new_session=True)
    return p, proj / ".claude" / "settings.local.json", tmp / "bashrc", tmp / "cfg" / "keys.env"


def shell_value(bashrc, name, home):
    # keys.env is found through $HOME in the source line, so point HOME at the test dir
    return subprocess.run(["bash", "-c", f'source "{bashrc}"; printf %s "${name}"'],
                          capture_output=True, text=True, env={"HOME": str(home), "PATH": "/usr/bin:/bin"}).stdout


def test_writes_settings_and_keys_file_and_never_prints_value(tmp_path):
    p, settings, bashrc, keys = run(tmp_path, "NEW_SERVICE_API_KEY")
    assert p.returncode == 0, p.stderr
    assert VALUE not in p.stdout and VALUE not in p.stderr
    assert json.loads(settings.read_text())["env"]["NEW_SERVICE_API_KEY"] == VALUE
    assert f"export NEW_SERVICE_API_KEY={VALUE}\n" in keys.read_text()
    assert VALUE not in bashrc.read_text()            # .bashrc holds no key
    assert "keys.env" in bashrc.read_text()           # it only sources the file
    for f in (settings, keys):
        assert stat.S_IMODE(f.stat().st_mode) == 0o600


def test_bashrc_sources_keys_file_end_to_end(tmp_path):
    keys_dir = tmp_path / ".config"
    p = subprocess.run([sys.executable, str(SCRIPT), "K_TOKEN", "--stdin",
                        "--project-dir", str(tmp_path / "proj"), "--bashrc", str(tmp_path / ".bashrc"),
                        "--keys-file", str(keys_dir / "keys.env")],
                       input=VALUE + "\n", capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert shell_value(tmp_path / ".bashrc", "K_TOKEN", tmp_path) == VALUE


def test_replaces_entries_and_removes_stale_bashrc_export(tmp_path):
    (tmp_path / "proj" / ".claude").mkdir(parents=True)
    (tmp_path / "proj" / ".claude" / "settings.local.json").write_text(json.dumps(
        {"env": {"OTHER": "keep", "K": "old"}, "permissions": {"allow": ["x"]}}))
    (tmp_path / "cfg").mkdir()
    (tmp_path / "cfg" / "keys.env").write_text("export K=old\nexport OTHER=keep\nexport K=older\n")
    (tmp_path / "bashrc").write_text("alias ll='ls -l'\nexport K=stale\n")
    p, settings, bashrc, keys = run(tmp_path, "K")
    assert p.returncode == 0, p.stderr
    data = json.loads(settings.read_text())
    assert data["env"] == {"OTHER": "keep", "K": VALUE} and data["permissions"] == {"allow": ["x"]}
    assert keys.read_text() == f"export K={VALUE}\nexport OTHER=keep\n"
    assert "export K=stale" not in bashrc.read_text() and "alias ll" in bashrc.read_text()
    assert "removed 1 old export of K" in p.stdout


def test_value_with_quotes_and_spaces_survives_the_shell(tmp_path):
    tricky = "a b'c\"$HOME`x`"
    p, _, _, keys = run(tmp_path, "TRICKY", value=tricky)
    assert p.returncode == 0, p.stderr
    out = subprocess.run(["bash", "-c", f'source "{keys}"; printf %s "$TRICKY"'],
                         capture_output=True, text=True).stdout
    assert out == tricky


def test_refuses_bad_name_empty_value_and_broken_json(tmp_path):
    p, settings, bashrc, keys = run(tmp_path, "lower-case")
    assert p.returncode == 2 and not settings.exists() and not keys.exists()
    p, settings, bashrc, keys = run(tmp_path, "EMPTY", value="  ")
    assert p.returncode == 1 and not settings.exists() and not keys.exists()
    settings.write_text("{ not json")
    p, settings, bashrc, keys = run(tmp_path, "K")
    assert p.returncode == 1 and "not valid JSON" in p.stderr
    assert settings.read_text() == "{ not json" and not keys.exists() and not bashrc.exists()


def test_without_a_terminal_it_refuses_instead_of_reading_visibly(tmp_path):
    p, settings, bashrc, keys = run(tmp_path, "K", stdin_value=False)
    assert p.returncode == 3 and "own terminal" in p.stderr
    assert not settings.exists() and not keys.exists()


BASHRC = """# ~/.bashrc
export PATH="$HOME/bin:$PATH"
export NVM_DIR="$HOME/.nvm"
# gbrain
export GBRAIN_REMOTE_TOKEN="tok-SECRET-1"
export OPENAI_API_KEY='sk-SECRET-2'
export SCROLLCRAFT_HOME=/opt/sc
    export INDENTED_API_KEY=inside-a-block
export OPENAI_API_KEY='sk-SECRET-3'
alias ll='ls -l'
"""


def migrate(tmp, *extra):
    (tmp / "home" / ".config").mkdir(parents=True, exist_ok=True)
    rc = tmp / "home" / ".bashrc"
    if not rc.exists():
        rc.write_text(BASHRC)
    keys = tmp / "home" / ".config" / "keys.env"
    p = subprocess.run([sys.executable, str(SCRIPT), "--migrate", "--bashrc", str(rc),
                        "--keys-file", str(keys), *extra], capture_output=True, text=True)
    return p, rc, keys


def test_migrate_dry_run_lists_names_only_and_changes_nothing(tmp_path):
    p, rc, keys = migrate(tmp_path, "--dry-run")
    assert p.returncode == 0, p.stderr
    assert "GBRAIN_REMOTE_TOKEN" in p.stdout and "OPENAI_API_KEY" in p.stdout
    assert "SECRET" not in p.stdout and "SECRET" not in p.stderr
    assert rc.read_text() == BASHRC and not keys.exists()


def test_migrate_moves_secret_exports_and_keeps_everything_else(tmp_path):
    p, rc, keys = migrate(tmp_path)
    assert p.returncode == 0, p.stderr
    assert "SECRET" not in p.stdout and "SECRET" not in p.stderr
    new_rc = rc.read_text()
    assert "SECRET" not in new_rc                                   # no key left in .bashrc
    for kept in ('export PATH="$HOME/bin:$PATH"', "SCROLLCRAFT_HOME", "alias ll", "# gbrain",
                 "export INDENTED_API_KEY"):                        # indented lines are left alone
        assert kept in new_rc
    assert sum("keys.env" in l for l in new_rc.splitlines()) == 1
    assert new_rc.index("keys.env") < new_rc.index("SCROLLCRAFT_HOME")  # sourced where the keys were
    k = keys.read_text()
    assert 'export GBRAIN_REMOTE_TOKEN="tok-SECRET-1"' in k          # moved verbatim
    assert "export OPENAI_API_KEY='sk-SECRET-3'" in k and "SECRET-2" not in k  # last one wins, as before
    assert stat.S_IMODE(keys.stat().st_mode) == 0o600
    backups = list(keys.parent.glob("keys.env.bashrc-backup-*"))
    assert len(backups) == 1 and backups[0].read_text() == BASHRC
    assert stat.S_IMODE(backups[0].stat().st_mode) == 0o600
    home = tmp_path / "home"
    assert shell_value(rc, "OPENAI_API_KEY", home) == "sk-SECRET-3"
    assert shell_value(rc, "GBRAIN_REMOTE_TOKEN", home) == "tok-SECRET-1"


def test_migrate_twice_is_a_no_op(tmp_path):
    migrate(tmp_path)
    rc_after, = [(tmp_path / "home" / ".bashrc").read_text()]
    p, rc, keys = migrate(tmp_path)
    assert p.returncode == 0 and "nothing to move" in p.stdout
    assert rc.read_text() == rc_after
