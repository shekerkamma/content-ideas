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
import re
import shutil
import subprocess
import tempfile
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


class MirrorRuleTests(unittest.TestCase):
    """The mirror rule's tracked-in-git half, pinned against its own history.

    It once checked only the canonical side: `skills/<name>/` tracked meant
    pass, whatever state the mirror was in. A mirror sitting in one developer's
    working directory with zero tracked files therefore satisfied every check —
    byte-identity is compared on disk — while the plugin shipped nothing. These
    run the real rule against synthetic repos so the asymmetry cannot return
    unnoticed the way it did for three months.
    """

    @classmethod
    def setUpClass(cls):
        if not CHECKER.is_file():
            raise unittest.SkipTest(f"missing {CHECKER}")
        if shutil.which("git") is None:
            raise unittest.SkipTest("git not available")
        cls.mod = _load()

    def _repo(self, track_canonical: bool, track_mirror: bool) -> Path:
        """A miniature repo with one mirrored skill, tracking the sides asked for."""
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        canonical = root / "skills" / "demo"
        mirror = root / "plugins" / "content-ideas" / "skills" / "demo"
        for d in (canonical, mirror):
            d.mkdir(parents=True)
            (d / "SKILL.md").write_text("---\nname: demo\n---\n\nbody\n", encoding="utf-8")
        run = lambda *a: subprocess.run(
            ["git", *a], cwd=root, capture_output=True, text=True, check=True
        )
        run("init", "-q")
        run("config", "user.email", "t@test")
        run("config", "user.name", "t")
        if track_canonical:
            run("add", "skills/demo")
        if track_mirror:
            run("add", "plugins/content-ideas/skills/demo")
        if track_canonical or track_mirror:
            run("commit", "-qm", "fixture")
        return root

    def _run_against(self, root: Path) -> list:
        mod, orig = self.mod, (self.mod.REPO, self.mod.SKILLS, self.mod.MIRROR, self.mod.MIRRORED)
        mod.REPO = root
        mod.SKILLS = root / "skills"
        mod.MIRROR = root / "plugins" / "content-ideas" / "skills"
        mod.MIRRORED = ("demo",)
        try:
            return mod.rule_mirror()
        finally:
            mod.REPO, mod.SKILLS, mod.MIRROR, mod.MIRRORED = orig

    def test_both_sides_tracked_passes(self):
        self.assertEqual([], self._run_against(self._repo(True, True)))

    def test_untracked_mirror_fails(self):
        """The regression: this is the exact state meta-loop was in."""
        fails = self._run_against(self._repo(True, False))
        self.assertEqual(1, len(fails), fails)
        self.assertIn("packaged mirror", fails[0])
        self.assertIn("untracked", fails[0])

    def test_untracked_canonical_still_fails(self):
        fails = self._run_against(self._repo(False, True))
        self.assertEqual(1, len(fails), fails)
        self.assertIn("canonical", fails[0])

    def test_mirrored_list_matches_the_documented_contract(self):
        """CLAUDE.md named seven canonical shared sources; the rule enforced six.

        meta-loop was documented as mirrored and policed by nothing, which is
        how its mirror stayed untracked while the gate reported green.
        """
        claude_md = (REPO / "CLAUDE.md").read_text(encoding="utf-8")
        # Only the mirrored list. The paragraph immediately after it names the
        # *recovery* sources (docx, pdf, improve, storm-research), which carry a
        # different guarantee -- portable, bytecode-free, checked by
        # scripts/verify-recovery-skills.sh -- and are deliberately not mirrored.
        bullet = re.search(
            r"Treat ((?:`skills/[a-z0-9-]+/`[,\s]*(?:and\s+)?)+)as canonical shared sources",
            claude_md,
        )
        self.assertIsNotNone(
            bullet, "CLAUDE.md no longer states the canonical shared sources list"
        )
        documented = set(re.findall(r"`skills/([a-z0-9-]+)/`", bullet.group(1)))
        self.assertTrue(documented, "parsed an empty canonical list")
        missing = documented - set(self.mod.MIRRORED)
        self.assertEqual(
            set(), missing,
            f"documented as canonical/mirrored in CLAUDE.md but absent from MIRRORED: "
            f"{sorted(missing)}",
        )


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
