"""Contract tests for the graph-engineering skill.

Two layers:

1. The four scripts behave as SKILL.md claims — scaffold, gate, validate,
   collate. Exercised through their CLIs, because the CLI is the interface the
   skill actually documents.
2. The load-bearing invariants survive edits. The critic having no write tools
   and never receiving the builder's context are the two constraints that make
   the pattern work; a well-meaning edit that relaxes either one degrades the
   loop to a single agent with extra steps, silently. These are tests, not
   comments, for that reason.
"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "graph-engineering"
SCRIPTS = SKILL / "scripts"


def run(script, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True, text=True, check=False,
    )


def scaffold(tmp, project="Test loop"):
    return run("init_loop.py", "--project", project, "--dir", str(tmp),
               "--no-git", "--quiet")


CONTRACT_HEAD = """\
# Contract: t
Status: {status}
## Scope
Everything named below, nothing else.
## Criteria
| # | Criterion | Check |
|---|---|---|
"""

GOOD_ROWS = "".join(
    f"| {i} | Every row in out.csv has a score of exactly 1, 2, 3, 4 or 5 (rule {i}) "
    f"| `python3 check.py --rule r{i}` |\n"
    for i in range(1, 6)
)

CONTRACT_TAIL = """\
## Disputes resolved during negotiation
- Builder proposed 1-10. Auditor rejected. Settled on 1-5.
## Grading
Any criterion failing fails the item. There is no partial pass.
"""


def write_contract(path, status="AGREED", rows=GOOD_ROWS, tail=CONTRACT_TAIL):
    path.write_text(CONTRACT_HEAD.format(status=status) + rows + tail,
                    encoding="utf-8")


class InitLoopTests(unittest.TestCase):
    def test_scaffolds_every_artifact(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            res = scaffold(tmp)
            self.assertEqual(0, res.returncode, res.stderr)
            for rel in ("feature_list.json", "claude-progress.txt", "init.sh",
                        "contract.md", ".claude/agents/auditor.md"):
                self.assertTrue((tmp / rel).is_file(), f"missing {rel}")
            self.assertTrue((tmp / "traces").is_dir())

    def test_init_sh_is_executable(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            scaffold(tmp)
            self.assertTrue((tmp / "init.sh").stat().st_mode & 0o111)

    def test_scaffolded_contract_starts_as_draft(self):
        # A frozen contract is the gate; scaffolding one pre-AGREED would let
        # work start against criteria nobody argued over.
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            scaffold(tmp)
            text = (tmp / "contract.md").read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^Status:\s*DRAFT\s*$")

    def test_is_idempotent_without_force(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            scaffold(tmp)
            (tmp / "contract.md").write_text("EDITED BY HAND", encoding="utf-8")
            scaffold(tmp)
            self.assertEqual("EDITED BY HAND",
                             (tmp / "contract.md").read_text(encoding="utf-8"))

    def test_force_overwrites(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            scaffold(tmp)
            (tmp / "contract.md").write_text("EDITED BY HAND", encoding="utf-8")
            run("init_loop.py", "--project", "t", "--dir", str(tmp),
                "--no-git", "--quiet", "--force")
            self.assertIn("Status: DRAFT",
                          (tmp / "contract.md").read_text(encoding="utf-8"))


class CheckContractTests(unittest.TestCase):
    def _check(self, text, *extra):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "contract.md"
            path.write_text(text, encoding="utf-8")
            return run("check_contract.py", "--file", str(path), *extra)

    def test_accepts_a_frozen_specific_contract(self):
        res = self._check(CONTRACT_HEAD.format(status="AGREED")
                          + GOOD_ROWS + CONTRACT_TAIL)
        self.assertEqual(0, res.returncode, res.stdout)
        self.assertIn("PASS", res.stdout)

    def test_rejects_draft_status(self):
        res = self._check(CONTRACT_HEAD.format(status="DRAFT")
                          + GOOD_ROWS + CONTRACT_TAIL)
        self.assertEqual(1, res.returncode)
        self.assertIn("not AGREED", res.stdout)

    def test_rejects_criterion_with_no_check(self):
        rows = "| 1 | Every row in out.csv has a score of 1 to 5 | |\n"
        res = self._check(CONTRACT_HEAD.format(status="AGREED") + rows + CONTRACT_TAIL)
        self.assertEqual(1, res.returncode)
        self.assertIn("no Check", res.stdout)

    def test_rejects_unfalsifiable_wording(self):
        rows = "| 1 | The scoring should be accurate | `python3 check.py` |\n"
        res = self._check(CONTRACT_HEAD.format(status="AGREED") + rows + CONTRACT_TAIL)
        self.assertEqual(1, res.returncode)
        self.assertIn("unfalsifiable", res.stdout)

    def test_flags_an_offered_escape_hatch(self):
        tail = CONTRACT_TAIL.replace(
            "There is no partial pass.", "A partial pass is acceptable.")
        res = self._check(CONTRACT_HEAD.format(status="AGREED") + GOOD_ROWS + tail)
        self.assertIn("escape hatch offered", res.stdout)

    def test_does_not_flag_a_banned_escape_hatch(self):
        # Regression: "There is no partial pass" is the contract forbidding the
        # hatch. Flagging it trains people to ignore the warning.
        res = self._check(CONTRACT_HEAD.format(status="AGREED")
                          + GOOD_ROWS + CONTRACT_TAIL)
        self.assertNotIn("escape hatch", res.stdout)

    def test_strict_promotes_warnings_to_failures(self):
        thin = "| 1 | Every row in out.csv scores 1 to 5 | `python3 c.py` |\n"
        ok = self._check(CONTRACT_HEAD.format(status="AGREED") + thin + CONTRACT_TAIL)
        strict = self._check(CONTRACT_HEAD.format(status="AGREED") + thin
                             + CONTRACT_TAIL, "--strict")
        self.assertEqual(0, ok.returncode)
        self.assertEqual(1, strict.returncode)


class VerifyStateTests(unittest.TestCase):
    def _state(self, tmp, items):
        (tmp / "feature_list.json").write_text(
            json.dumps({"project": "t", "created": "2026-08-11", "items": items},
                       indent=2), encoding="utf-8")

    def _good_item(self, **over):
        item = {"id": 1, "name": "Every lead has a score between 1 and 5",
                "status": "failing", "verified_by": "python3 check.py", "notes": ""}
        item.update(over)
        return item

    def test_accepts_a_sound_state_layer(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            scaffold(tmp)
            self._state(tmp, [self._good_item()])
            res = run("verify_state.py", "--dir", str(tmp))
            self.assertEqual(0, res.returncode, res.stdout)

    def test_rejects_the_untouched_scaffold(self):
        # The placeholder item must not pass, or a loop can start against
        # "REPLACE ME" and look healthy.
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            scaffold(tmp)
            res = run("verify_state.py", "--dir", str(tmp))
            self.assertEqual(1, res.returncode)
            self.assertIn("placeholder", res.stdout)

    def test_rejects_non_binary_status(self):
        for bad in ("in progress", "mostly done", "blocked", ""):
            with tempfile.TemporaryDirectory() as d:
                tmp = Path(d)
                scaffold(tmp)
                self._state(tmp, [self._good_item(status=bad)])
                res = run("verify_state.py", "--dir", str(tmp))
                self.assertEqual(1, res.returncode, f"{bad!r} was accepted")
                self.assertIn("passing", res.stdout)

    def test_rejects_missing_verified_by(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            scaffold(tmp)
            self._state(tmp, [self._good_item(verified_by="")])
            res = run("verify_state.py", "--dir", str(tmp))
            self.assertEqual(1, res.returncode)
            self.assertIn("verified_by", res.stdout)

    def test_rejects_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            scaffold(tmp)
            self._state(tmp, [self._good_item(), self._good_item()])
            res = run("verify_state.py", "--dir", str(tmp))
            self.assertEqual(1, res.returncode)
            self.assertIn("duplicate", res.stdout)

    def test_reports_the_next_failing_item(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            scaffold(tmp)
            self._state(tmp, [
                self._good_item(id=1, status="passing"),
                self._good_item(id=2, name="No lead scored 4 without a contact",
                                status="failing"),
            ])
            res = run("verify_state.py", "--dir", str(tmp))
            self.assertEqual(0, res.returncode, res.stdout)
            self.assertIn("No lead scored 4 without a contact", res.stdout)


class CollateTracesTests(unittest.TestCase):
    def test_writes_review_packet_and_flags_deferral(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            scaffold(tmp)
            (tmp / "traces" / "run-a.txt").write_text(
                "auditor: looks fine, we can fix it later\n", encoding="utf-8")
            (tmp / "traces" / "run-b.txt").write_text(
                "auditor: criterion 1 failed at out.csv:12\n", encoding="utf-8")
            res = run("collate_traces.py", "--dir", str(tmp))
            self.assertEqual(0, res.returncode, res.stderr)
            review = (tmp / "traces" / "REVIEW.md").read_text(encoding="utf-8")
            self.assertIn("run-a.txt", review)
            self.assertIn("deferral", review)
            self.assertIn("run-b.txt", review)

    def test_fails_when_no_traces_captured(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            scaffold(tmp)
            res = run("collate_traces.py", "--dir", str(tmp))
            self.assertEqual(1, res.returncode)


class InvariantTests(unittest.TestCase):
    """The two constraints that make a builder/critic loop different from one
    agent talking to itself. Both are easy to relax by accident."""

    def setUp(self):
        self.auditor = (SKILL / "assets" / "auditor.md").read_text(encoding="utf-8")
        self.skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    def test_auditor_has_no_write_tools(self):
        m = re.search(r"(?m)^tools:\s*(.+)$", self.auditor)
        self.assertIsNotNone(m, "auditor.md declares no tools")
        tools = {t.strip() for t in m.group(1).split(",")}
        self.assertEqual({"Read", "Grep", "Glob", "Bash"}, tools)
        for forbidden in ("Write", "Edit", "NotebookEdit", "MultiEdit"):
            self.assertNotIn(forbidden, tools,
                             f"{forbidden} lets the critic fix what it should report")

    def test_auditor_bans_deferral_and_partial_pass(self):
        lowered = self.auditor.lower()
        self.assertIn("fix later", lowered)
        self.assertIn("no partial pass", lowered)

    def test_auditor_defaults_to_failure_when_unverifiable(self):
        self.assertIn("0.0", self.auditor)
        self.assertRegex(self.auditor.lower(), r"cannot be checked|evidence is missing")

    def test_skill_documents_critic_context_isolation(self):
        # Anthropic tried feeding the evaluator the generator's context and
        # backed it out. Losing this from the skill body loses the reason.
        # Asserted on booleans, not assertRegex, so a failure prints the rule
        # that went missing instead of the whole SKILL.md.
        lowered = self.skill.lower()
        self.assertIn("muddies", lowered,
                      "SKILL.md no longer explains why the critic stays blind")
        self.assertTrue(
            "do not feed the builder's transcript" in lowered,
            "SKILL.md no longer forbids feeding the builder's transcript to "
            "the critic — the constraint Anthropic tried and backed out of",
        )

    def test_skill_carries_editable_judgment_rules(self):
        self.assertIn("## Judgment rules", self.skill)
        self.assertIn("do not hardcode", self.skill.lower())

    def test_packaged_mirror_matches_canonical(self):
        packaged = REPO / "plugins" / "content-ideas" / "skills" / "graph-engineering"
        for path in SKILL.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            rel = path.relative_to(SKILL)
            twin = packaged / rel
            self.assertTrue(twin.is_file(), f"{rel} missing from packaged mirror")
            self.assertEqual(path.read_bytes(), twin.read_bytes(),
                             f"content drift in {rel}")


if __name__ == "__main__":
    unittest.main()
