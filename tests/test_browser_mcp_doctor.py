from pathlib import Path

from scripts.browser_mcp_doctor import (
    find_literal_secrets,
    parse_json_mcp_names,
    parse_toml_mcp_names,
    parse_yaml_mcp_names,
)


def test_parses_host_server_names(tmp_path: Path) -> None:
    json_path = tmp_path / "config.json"
    json_path.write_text('{"mcpServers":{"playwright":{},"gbrain":{}}}')
    toml_path = tmp_path / "config.toml"
    toml_path.write_text('[mcp_servers.chrome-devtools]\ncommand="npx"\n')
    yaml_path = tmp_path / "config.yaml"
    yaml_path.write_text("mcp_servers:\n  browser-use:\n    enabled: false\nplugins:\n  enabled: []\n")

    assert parse_json_mcp_names(json_path) == ["gbrain", "playwright"]
    assert parse_toml_mcp_names(toml_path) == ["chrome-devtools"]
    assert parse_yaml_mcp_names(yaml_path) == ["browser-use"]


def test_detects_literals_without_flagging_env_references(tmp_path: Path) -> None:
    literal = tmp_path / "literal.json"
    literal.write_text('{"headers":{"Authorization":"Bearer abcdefghijklmnop"}}')
    env_ref = tmp_path / "env.json"
    env_ref.write_text('{"env":{"API_KEY":"${API_KEY}"},"url":"https://example.test/mcp?key=${API_KEY}"}')

    assert find_literal_secrets(literal)
    assert not find_literal_secrets(env_ref)
