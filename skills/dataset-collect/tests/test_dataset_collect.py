"""Tests for dataset-collect. Stdlib + pytest, no network.

The two regression tests at the bottom pin defects that execution found and
reading could not: a total-failure run that reported success, and a same-day
re-run that doubled the store.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
DATASET = SCRIPTS / "dataset.py"

sys.path.insert(0, str(SCRIPTS))

from specfile import SpecError, load_spec, parse_yaml_subset  # noqa: E402


def run(*args, cwd=None):
    return subprocess.run([sys.executable, str(DATASET), *args],
                          capture_output=True, text=True, cwd=cwd)


FIXTURE = [
    {"company": "alpha", "name": "Alpha", "employees": 10, "country": "US"},
    {"company": "beta", "name": "Beta", "employees": 30, "country": "DE"},
    {"company": "gamma", "name": "Gamma", "employees": 50, "country": "US"},
]


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    (tmp_path / "fixture.json").write_text(json.dumps(FIXTURE), encoding="utf-8")
    (tmp_path / "inputs.txt").write_text("alpha\nbeta\ngamma\n", encoding="utf-8")
    (tmp_path / "spec.yaml").write_text(
        "name: t\n"
        "sources:\n"
        "  - id: s1\n"
        "    adapter: file\n"
        "    fixture: fixture.json\n"
        "    from_file: inputs.txt\n"
        "    input_key: company\n"
        "    parallel: 2\n"
        "    on_error: skip\n"
        "storage:\n"
        "  format: jsonl\n"
        "  path: ./data/t/\n",
        encoding="utf-8")
    return tmp_path


# ---------------------------------------------------------------- spec parsing

def test_parses_the_on_screen_spec_shape():
    """The exact YAML shape read off the source video at 06:17."""
    parsed = parse_yaml_subset(
        "name: competitor-monitor\n"
        "description: 'Dataset: competitor-monitor'\n"
        "sources:\n"
        "  - id: competitor_profiles\n"
        "    endpoint: /api/linkedin/company\n"
        "    from_file: competitors.txt\n"
        "    input_key: company\n"
        "    parallel: 3\n"
        "    on_error: skip\n"
        "storage:\n"
        "  format: parquet\n"
        "  path: ./data/competitor-monitor/\n"
        "  partition_by:\n"
        "    - source_id\n"
        "    - collected_date\n")
    assert parsed["name"] == "competitor-monitor"
    assert parsed["sources"][0]["parallel"] == 3
    assert parsed["sources"][0]["on_error"] == "skip"
    assert parsed["storage"]["partition_by"] == ["source_id", "collected_date"]


def test_unsupported_yaml_raises_rather_than_guessing():
    with pytest.raises(SpecError):
        parse_yaml_subset("a: &anchor x\n")
    with pytest.raises(SpecError):
        parse_yaml_subset("just_a_bare_line\n")


def test_missing_adapter_is_rejected(tmp_path: Path):
    p = tmp_path / "s.yaml"
    p.write_text("name: t\nsources:\n  - id: a\nstorage:\n  path: ./d/\n",
                 encoding="utf-8")
    with pytest.raises(SpecError, match="adapter"):
        load_spec(p)


def test_unsupported_storage_format_is_rejected(tmp_path: Path):
    p = tmp_path / "s.yaml"
    p.write_text("name: t\nsources:\n  - id: a\n    adapter: file\n"
                 "storage:\n  format: parquet\n  path: ./d/\n", encoding="utf-8")
    with pytest.raises(SpecError, match="parquet"):
        load_spec(p)


# ---------------------------------------------------------------- collect/query

def test_dry_run_writes_nothing(project: Path):
    r = run("collect", "spec.yaml", "--dry-run", cwd=project)
    assert r.returncode == 0, r.stderr
    assert "DRY RUN" in r.stdout and "0 made" in r.stdout
    assert not (project / "data").exists()


def test_collect_then_aggregate(project: Path):
    assert run("collect", "spec.yaml", cwd=project).returncode == 0
    assert (project / "data/t/raw/s1").is_dir()

    count = run("query", "spec.yaml", "--source", "s1", "--count", cwd=project)
    assert count.stdout.strip() == "3"

    avg = run("query", "spec.yaml", "--source", "s1", "--avg", "employees", cwd=project)
    assert avg.stdout.strip() == "30.0"          # (10+30+50)/3

    top = run("query", "spec.yaml", "--source", "s1", "--top", "employees",
              "--select", "name", "--limit", "1", "--format", "json", cwd=project)
    assert json.loads(top.stdout) == [{"name": "Gamma"}]


def test_where_filters_and_ands(project: Path):
    run("collect", "spec.yaml", cwd=project)
    r = run("query", "spec.yaml", "--source", "s1", "--where", "employees>15",
            "--where", "country=US", "--count", cwd=project)
    assert r.stdout.strip() == "1"               # Gamma only


def test_limit_caps_inputs(project: Path):
    run("collect", "spec.yaml", "--limit", "2", cwd=project)
    r = run("query", "spec.yaml", "--source", "s1", "--count", cwd=project)
    assert r.stdout.strip() == "2"


def test_provenance_columns_are_added(project: Path):
    run("collect", "spec.yaml", cwd=project)
    line = next((project / "data/t/raw/s1").glob("*.jsonl")).read_text().splitlines()[0]
    rec = json.loads(line)
    assert rec["_source_id"] == "s1"
    assert rec["_input"] in {"alpha", "beta", "gamma"}
    assert rec["_collected_date"]


def test_spec_paths_resolve_against_the_spec_not_the_cwd(project: Path, tmp_path: Path):
    """Running from elsewhere must collect the same data."""
    other = tmp_path / "elsewhere"
    other.mkdir()
    r = run("collect", str(project / "spec.yaml"), cwd=other)
    assert r.returncode == 0, r.stderr
    assert (project / "data/t/raw/s1").is_dir()
    assert not (other / "data").exists()


# ---------------------------------------------------------------- regressions

def test_total_failure_exits_nonzero_even_with_on_error_skip(project: Path):
    """Regression: every input failing once printed `Done.` and exited 0.

    `on_error: skip` means tolerate *some* failures. A scheduled run whose
    credential expired would otherwise report success forever.
    """
    (project / "spec.yaml").write_text(
        (project / "spec.yaml").read_text().replace(
            "fixture: fixture.json", "fixture: does-not-exist.json"),
        encoding="utf-8")
    r = run("collect", "spec.yaml", cwd=project)
    assert r.returncode == 1, f"expected failure exit, got {r.returncode}"
    assert "FAILED" in r.stderr


def test_partial_failure_still_succeeds(project: Path):
    """Negative control for the rule above: skip must still tolerate partials."""
    (project / "inputs.txt").write_text("alpha\nnope\n", encoding="utf-8")
    r = run("collect", "spec.yaml", cwd=project)
    assert r.returncode == 0, r.stderr
    assert run("query", "spec.yaml", "--source", "s1", "--count",
               cwd=project).stdout.strip() == "1"


def test_same_day_rerun_is_idempotent(project: Path):
    """Regression: appending doubled the store from 5 records to 10."""
    for _ in range(3):
        assert run("collect", "spec.yaml", cwd=project).returncode == 0
    r = run("query", "spec.yaml", "--source", "s1", "--count", cwd=project)
    assert r.stdout.strip() == "3", "a date partition is a snapshot, not a log"


def test_env_interpolation_errors_on_missing_variable():
    from adapters import AdapterError, expand_env
    with pytest.raises(AdapterError, match="DEFINITELY_NOT_SET"):
        expand_env("${ENV:DEFINITELY_NOT_SET}")


def test_no_credentials_in_shipped_assets():
    """A spec is committable: it may name env vars, never hold their values."""
    for path in (SKILL / "assets").rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            assert "sk-" not in text
            assert "Bearer ey" not in text
