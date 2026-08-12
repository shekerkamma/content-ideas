"""Gate rules and capture math for skills/video-to-skill.

Every rule here was written after a bug, not before one. The derivation of
`ai-blueprint-build-loop` from a 61-minute screencast exercised the gate twice
and broke it twice, and the capture stage produced a confident 86-frame sample
with a seven-minute blind spot. The tests below pin the fixes:

- `placeholders` failed on prose that merely mentioned TODO, because the derived
  skill documented a tool whose job is scanning for TODO/FIXME.
- `judgment` reported "no timestamp cited" against rules that cite timestamps,
  because it only read each bullet's first line.
- `name` failed on every relative-path invocation, because Path(".").name is "".
- `executed` did not exist, so the gate passed a skill nobody had ever run --
  which is the one thing a video-derived skill most needs proven.
- `coverage` reported a meaningless mean gap when duration was read from the
  wrong metadata key.
"""

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "video-to-skill"
GATE = SKILL / "scripts" / "check_derived_skill.py"
INIT = SKILL / "scripts" / "init_skill.py"
HYPER = SKILL / "scripts" / "hyperframes.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MINIMAL = """---
name: {name}
description: Use when exercising the video-to-skill gate in tests, a description long enough to route.
---

# Test Skill

## Procedure

1. Do the thing — route: `Bash`

## Judgment rules

- A rule traceable to the moment it was stated (video 10:39).

## Environment bindings

| Binding | In the video | On this machine |
|---|---|---|
| A tool | used on screen | confirm |

## Verification

Executed 2026-08-12 against a scratch repo; the endpoint returned 200.

```bash
echo ok
```
"""

PROVENANCE = """# Source video

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=TEST |
| Uploaded | 2026-08-10 |
"""

BINDINGS = """# Environment bindings

| # | Binding | Resolution |
|---|---|---|
| 1 | A tool | confirm |
"""


def build_skill(root: Path, name: str = "gate-fixture", **edits) -> Path:
    d = root / name
    (d / "references").mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(edits.get("skill", MINIMAL.format(name=name)), encoding="utf-8")
    (d / "references" / "source-video.md").write_text(
        edits.get("provenance", PROVENANCE), encoding="utf-8"
    )
    (d / "references" / "environment-bindings.md").write_text(
        edits.get("bindings", BINDINGS), encoding="utf-8"
    )
    return d


def run_gate(path: Path, *args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(GATE), str(path), "--no-collision-check", *args],
        capture_output=True,
        text=True,
    )


class GateBaselineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_wellformed_skill_passes(self):
        r = run_gate(build_skill(self.tmp))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_relative_path_does_not_break_the_name_rule(self):
        """Path('.').name is '' -- the rule must resolve before reading .name."""
        d = build_skill(self.tmp)
        r = subprocess.run(
            [sys.executable, str(GATE), ".", "--no-collision-check"],
            capture_output=True,
            text=True,
            cwd=d,
        )
        self.assertNotIn("does not match directory name", r.stdout)
        self.assertEqual(r.returncode, 0, r.stdout)


class PlaceholderRuleTests(unittest.TestCase):
    """Fires on scaffold markers, not on prose that discusses TODOs."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_scaffold_markers_fail(self):
        body = MINIMAL.format(name="gate-fixture").replace("Do the thing", "TODO-STEP")
        r = run_gate(build_skill(self.tmp, skill=body))
        self.assertIn("placeholders", r.stdout)
        self.assertNotEqual(r.returncode, 0)

    def test_bare_todo_table_cell_fails(self):
        r = run_gate(build_skill(self.tmp, bindings=BINDINGS + "\n| 2 | TODO | UNRESOLVED |\n"))
        self.assertIn("placeholders", r.stdout)

    def test_prose_mentioning_todo_passes(self):
        """A derived skill may document a tool that scans for TODO/FIXME."""
        body = MINIMAL.format(name="gate-fixture").replace(
            "Do the thing",
            "Run the audit, which scans for dead TODO/FIXME markers and stray console calls",
        )
        r = run_gate(build_skill(self.tmp, skill=body))
        self.assertEqual(r.returncode, 0, r.stdout)


class JudgmentRuleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_missing_section_fails(self):
        body = MINIMAL.format(name="gate-fixture").replace("## Judgment rules", "## Other")
        r = run_gate(build_skill(self.tmp, skill=body))
        self.assertIn("judgment", r.stdout)
        self.assertNotEqual(r.returncode, 0)

    def test_timestamp_on_a_wrapped_continuation_line_counts(self):
        """A wrapped bullet carries its citation on the next line, not the first."""
        body = MINIMAL.format(name="gate-fixture").replace(
            "- A rule traceable to the moment it was stated (video 10:39).",
            "- A rule whose statement runs long enough to wrap onto\n  a second line (video 10:39).",
        )
        r = run_gate(build_skill(self.tmp, skill=body))
        self.assertNotIn("no judgment rule cites", r.stdout)
        self.assertEqual(r.returncode, 0, r.stdout)


class BindingsRuleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_unresolved_table_row_fails(self):
        r = run_gate(
            build_skill(self.tmp, bindings=BINDINGS.replace("| 1 | A tool | confirm |",
                                                            "| 1 | A tool | UNRESOLVED |"))
        )
        self.assertIn("bindings", r.stdout)
        self.assertNotEqual(r.returncode, 0)

    def test_prose_legend_naming_unresolved_does_not_fire(self):
        """The explanatory legend says every binding starts UNRESOLVED; only rows count."""
        prose = "Each binding starts UNRESOLVED until resolved.\n\n" + BINDINGS
        r = run_gate(build_skill(self.tmp, bindings=prose))
        self.assertEqual(r.returncode, 0, r.stdout)


class ExecutionRuleTests(unittest.TestCase):
    """A derived skill nobody ran is a hypothesis; the gate must say so."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def _without_execution_record(self):
        return MINIMAL.format(name="gate-fixture").replace(
            "Executed 2026-08-12 against a scratch repo; the endpoint returned 200.",
            "Run this to check it.",
        )

    def test_missing_execution_record_fails(self):
        r = run_gate(build_skill(self.tmp, skill=self._without_execution_record()))
        self.assertIn("executed", r.stdout)
        self.assertNotEqual(r.returncode, 0)

    def test_declared_not_executed_fails_by_default(self):
        body = self._without_execution_record().replace(
            "Run this to check it.", "NOT EXECUTED. Would run this."
        )
        r = run_gate(build_skill(self.tmp, skill=body))
        self.assertIn("run it on the narrowest real case", r.stdout)
        self.assertNotEqual(r.returncode, 0)

    def test_allow_unexecuted_downgrades_to_a_warning_that_stays_visible(self):
        body = self._without_execution_record().replace(
            "Run this to check it.", "NOT EXECUTED. Would run this."
        )
        r = run_gate(build_skill(self.tmp, skill=body), "--allow-unexecuted")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("WARN", r.stdout)
        self.assertIn("not a validated skill", r.stdout)

    def test_missing_verification_section_still_fails(self):
        body = MINIMAL.format(name="gate-fixture").replace("## Verification", "## Notes")
        r = run_gate(build_skill(self.tmp, skill=body))
        self.assertIn("verify", r.stdout)
        self.assertNotEqual(r.returncode, 0)


class SecretsRuleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_credential_shaped_string_fails(self):
        body = MINIMAL.format(name="gate-fixture") + "\nexport K=gsk_" + "a" * 24 + "\n"
        r = run_gate(build_skill(self.tmp, skill=body))
        self.assertIn("secrets", r.stdout)
        self.assertNotEqual(r.returncode, 0)


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_scaffold_fails_its_own_gate(self):
        """A fresh scaffold must never be installable."""
        r = subprocess.run(
            [sys.executable, str(INIT), "--name", "scaffold-check",
             "--url", "https://example.test/v", "--out-dir", str(self.tmp)],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        gate = run_gate(self.tmp / "scaffold-check")
        self.assertNotEqual(gate.returncode, 0)
        self.assertIn("placeholders", gate.stdout)

    def test_refuses_to_scaffold_into_a_live_skills_tree(self):
        live = self.tmp / ".claude" / "skills"
        r = subprocess.run(
            [sys.executable, str(INIT), "--name", "nope",
             "--url", "https://example.test/v", "--out-dir", str(live)],
            capture_output=True, text=True,
        )
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("live skills tree", r.stderr)

    def test_rejects_non_kebab_names(self):
        r = subprocess.run(
            [sys.executable, str(INIT), "--name", "Not Kebab",
             "--url", "https://example.test/v", "--out-dir", str(self.tmp)],
            capture_output=True, text=True,
        )
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("kebab-case", r.stderr)


class CoverageMathTests(unittest.TestCase):
    """The gap report is the only signal that a sparse capture is untrustworthy."""

    @classmethod
    def setUpClass(cls):
        cls.hyper = _load(HYPER, "hyperframes")

    def _frames(self, times):
        return [{"timestamp_seconds": t} for t in times]

    def test_reports_the_largest_hole(self):
        cov = self.hyper.coverage(self._frames([0, 10, 200, 210]), 220.0)
        self.assertEqual(cov["count"], 4)
        self.assertEqual(cov["max_gap_seconds"], 190.0)

    def test_mean_gap_spans_the_whole_duration(self):
        """Reading duration from the wrong key made the tail edge negative,
        which cancelled the sum and reported a mean of 0.0 on real captures."""
        cov = self.hyper.coverage(self._frames([10, 20, 30]), 40.0)
        self.assertAlmostEqual(cov["mean_gap_seconds"], 10.0, places=1)
        self.assertGreater(cov["mean_gap_seconds"], 0.0)

    def test_empty_capture_reports_no_frames(self):
        self.assertEqual(self.hyper.coverage([], 100.0), {"count": 0})

    def test_screencast_threshold_is_below_watch_default(self):
        """The whole reason this script exists: 0.20 goes blind on screencasts."""
        installed = Path.home() / ".claude/skills/watch/scripts/frames.py"
        if not installed.is_file():
            self.skipTest("watch skill not installed on this host")
        watch_frames = _load(installed, "watch_frames")
        self.assertLess(self.hyper.SCREENCAST_THRESHOLD, watch_frames.SCENE_THRESHOLD)


if __name__ == "__main__":
    unittest.main()
