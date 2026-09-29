"""Pure transforms behind scripts/hosts/host_setup.py: idempotent and loss-free."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "host_setup", Path(__file__).resolve().parents[1] / "scripts" / "hosts" / "host_setup.py")
hs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hs)


def test_blank_gemini_keys_removes_values_and_keeps_other_lines():
    src = "A=1\nGOOGLE_API_KEY=secret1\nexport GEMINI_API_KEY=secret2\nB=2\n"
    out = hs.blank_gemini_keys(src)
    assert "secret1" not in out and "secret2" not in out
    assert "A=1" in out and "B=2" in out
    assert hs.gemini_key_values(out) == ["", ""]


def test_blank_gemini_keys_is_idempotent():
    once = hs.blank_gemini_keys("X=1\nGOOGLE_API_KEY=k\n")
    assert hs.blank_gemini_keys(once) == once
    assert once.count("GOOGLE_API_KEY=") == 1


def test_blank_gemini_keys_on_empty_file():
    assert hs.gemini_key_values(hs.blank_gemini_keys("")) == ["", ""]


YAML = """custom_providers:
  - name: cliproxyapi
    models:
      - claude-sonnet-4-6
      - gemini-3-flash-agent
      - gemini-pro-agent
      - gemini-3.5-flash-low
      - gemini-3.5-flash-extra-low
"""


def test_replace_dead_ids_collapses_to_one_live_id():
    out = hs.replace_dead_ids(YAML)
    for dead in hs.DEAD_PROXY_IDS:
        assert f"- {dead}\n" not in out + "\n"
    assert out.count("- gemini-3.5-flash") == 1
    assert "- gemini-pro-agent" in out and "- claude-sonnet-4-6" in out


def test_replace_dead_ids_is_idempotent_and_no_op_when_clean():
    once = hs.replace_dead_ids(YAML)
    assert hs.replace_dead_ids(once) == once
    clean = "models:\n  - gemini-3.5-flash\n"
    assert hs.replace_dead_ids(clean) == clean
