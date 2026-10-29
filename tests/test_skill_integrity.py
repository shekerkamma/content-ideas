"""Repo-wide skill integrity gate.

Runs every rule in scripts/check_skills.py. The rules were derived in
runs/2026-08-11-graph-engineering-contract-loop/, where four audit rounds found
that each one initially measured something adjacent to what mattered — a name
field instead of the routing surface, the working directory instead of what
ships, a top-level scan instead of the whole tree. Each rule carries a revision
note saying what it got wrong first.

These are enforced here rather than left as a script somebody remembers to run,
because the drift they catch stayed invisible for three months.
"""

import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHECKER = REPO / "scripts" / "check_skills.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_skills", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class SkillIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not CHECKER.is_file():
            raise unittest.SkipTest(f"missing {CHECKER}")
        cls.mod = _load()

    def _run(self, rule):
        return self.mod.RULES[rule]()

    def test_every_skill_has_closed_frontmatter(self):
        self.assertEqual([], self._run("frontmatter"))

    def test_no_duplicate_invocation_names(self):
        self.assertEqual([], self._run("dupes"))

    def test_name_matches_directory(self):
        self.assertEqual([], self._run("name"))

    def test_routing_is_reachable(self):
        self.assertEqual([], self._run("desc"))

    def test_no_two_skills_route_identically(self):
        # description, triggers, and '## When to invoke' across all six trees.
        self.assertEqual([], self._run("routing"))

    def test_no_unregistered_cross_tree_drift(self):
        # Registered exceptions must carry a non-empty reason AND evidence, and
        # only waive the trees they name.
        self.assertEqual([], self._run("crosstree"))

    def test_no_committed_bytecode(self):
        self.assertEqual([], self._run("bytecode"))

    def test_packaged_mirrors_match_and_are_tracked(self):
        self.assertEqual([], self._run("mirror"))


class RegistryTests(unittest.TestCase):
    """The exception registry is itself a claim and gets the same evidence bar."""

    def setUp(self):
        if not CHECKER.is_file():
            self.skipTest(f"missing {CHECKER}")
        self.mod = _load()

    def test_every_registered_variant_carries_reason_and_evidence(self):
        import json
        path = self.mod.VARIANTS_FILE
        self.assertTrue(path.is_file(), f"missing {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        for name, entry in data.items():
            if name.startswith("_"):
                continue
            with self.subTest(variant=name):
                self.assertTrue(str(entry.get("reason", "")).strip(),
                                f"{name}: empty reason")
                self.assertTrue(str(entry.get("evidence", "")).strip(),
                                f"{name}: empty evidence")
                self.assertTrue(entry.get("trees"),
                                f"{name}: must name the trees it waives")


if __name__ == "__main__":
    unittest.main()
