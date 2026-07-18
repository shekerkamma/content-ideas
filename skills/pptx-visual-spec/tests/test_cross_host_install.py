from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "install_cross_host.py"
SPEC = importlib.util.spec_from_file_location("install_cross_host", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def make_skill(path: Path, body: str = "# Test\n") -> None:
    path.mkdir(parents=True)
    (path / "SKILL.md").write_text(body, encoding="utf-8")


def test_symlink_is_relative_and_idempotent(tmp_path: Path) -> None:
    source = tmp_path / "repo" / "skills" / "sample"
    destination = tmp_path / "home" / ".claude" / "skills" / "sample"
    make_skill(source)

    assert MODULE.install_one(source, destination, "symlink", False, False).startswith("installed")
    assert destination.is_symlink()
    assert not destination.readlink().is_absolute()
    assert destination.resolve() == source.resolve()
    assert MODULE.install_one(source, destination, "symlink", False, False).startswith("ok")


def test_copy_refreshes_only_managed_destination(tmp_path: Path) -> None:
    source = tmp_path / "repo" / "sample"
    destination = tmp_path / "home" / "sample"
    make_skill(source, "one\n")

    MODULE.install_one(source, destination, "copy", False, False)
    (source / "SKILL.md").write_text("two\n", encoding="utf-8")
    result = MODULE.install_one(source, destination, "copy", False, False)
    assert result.startswith("installed")
    assert (destination / "SKILL.md").read_text(encoding="utf-8") == "two\n"


def test_unmanaged_destination_is_refused_unless_identical(tmp_path: Path) -> None:
    source = tmp_path / "repo" / "sample"
    destination = tmp_path / "home" / "sample"
    make_skill(source)
    make_skill(destination)

    assert MODULE.install_one(source, destination, "symlink", False, False).startswith("CONFLICT")
    result = MODULE.install_one(source, destination, "symlink", False, True)
    assert result.startswith("installed")
    assert destination.is_symlink()


def test_dry_run_makes_no_changes(tmp_path: Path) -> None:
    source = tmp_path / "repo" / "sample"
    destination = tmp_path / "home" / "sample"
    make_skill(source)

    assert MODULE.install_one(source, destination, "copy", True, False).startswith("would install")
    assert not destination.exists()


def test_replace_unmanaged_creates_backup(tmp_path: Path) -> None:
    source = tmp_path / "repo" / "sample"
    destination = tmp_path / "home" / "sample"
    backup_root = tmp_path / "backups"
    make_skill(source, "new\n")
    make_skill(destination, "old\n")

    result = MODULE.install_one(
        source,
        destination,
        "symlink",
        False,
        False,
        replace_unmanaged=True,
        backup_root=backup_root,
    )
    assert result.startswith("installed")
    assert destination.is_symlink()
    backup = backup_root / destination.as_posix().lstrip("/")
    assert (backup / "SKILL.md").read_text(encoding="utf-8") == "old\n"
