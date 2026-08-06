#!/usr/bin/env python3
"""Fail fast when the portable AI Analyst agent registry is incomplete."""

from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[2]
REGISTRY = SKILL_ROOT / "run-analysis" / "references" / "agent-registry.yaml"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    try:
        raw = REGISTRY.read_bytes()
    except OSError as exc:
        fail(f"cannot read registry {REGISTRY}: {exc}")
    if b"\x00" in raw:
        fail(f"NUL byte found in {REGISTRY}")

    try:
        document = yaml.safe_load(raw.decode("utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        fail(f"invalid registry: {exc}")

    agents = document.get("agents") if isinstance(document, dict) else None
    if not isinstance(agents, list) or not agents:
        fail("registry must contain a non-empty agents list")

    by_name: dict[str, dict] = {}
    for entry in agents:
        if not isinstance(entry, dict) or not entry.get("name"):
            fail("every registry entry must be a mapping with a name")
        name = entry["name"]
        if name in by_name:
            fail(f"duplicate agent name: {name}")
        by_name[name] = entry

        relative_file = entry.get("file")
        if not isinstance(relative_file, str) or not relative_file:
            fail(f"agent {name} has no file")
        agent_file = (SKILL_ROOT / relative_file).resolve()
        try:
            agent_file.relative_to(SKILL_ROOT)
        except ValueError:
            fail(f"agent {name} escapes the portable skill root: {relative_file}")
        if not agent_file.is_file():
            fail(f"agent file not found: {relative_file}")
        try:
            content = agent_file.read_bytes()
            if b"\x00" in content:
                fail(f"NUL byte found in agent file: {relative_file}")
            if not content.decode("utf-8").strip():
                fail(f"agent file is empty: {relative_file}")
        except (OSError, UnicodeDecodeError) as exc:
            fail(f"invalid agent file {relative_file}: {exc}")

    edges: dict[str, set[str]] = {name: set() for name in by_name}
    indegree = {name: 0 for name in by_name}
    for name, entry in by_name.items():
        dependencies = list(entry.get("depends_on") or []) + list(
            entry.get("depends_on_any") or []
        )
        for dependency in dependencies:
            if dependency not in by_name:
                fail(f"unknown dependency: {name} depends on {dependency}")
            if name not in edges[dependency]:
                edges[dependency].add(name)
                indegree[name] += 1

    ready = deque(sorted(name for name, degree in indegree.items() if degree == 0))
    visited: list[str] = []
    while ready:
        current = ready.popleft()
        visited.append(current)
        for dependent in sorted(edges[current]):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)
    if len(visited) != len(by_name):
        cyclic = sorted(name for name, degree in indegree.items() if degree > 0)
        fail(f"dependency cycle detected among: {', '.join(cyclic)}")

    pipeline_agents = [
        name for name, entry in by_name.items() if entry.get("pipeline_step") is not None
    ]
    print(
        f"OK: {len(by_name)} registry entries, {len(pipeline_agents)} pipeline nodes, "
        f"{len(set(entry['file'] for entry in agents))} referenced files; DAG is acyclic."
    )


if __name__ == "__main__":
    main()
