"""Tests for the repo-local gbrain bridge."""

from pathlib import Path
from unittest import mock
import unittest

import helpers  # noqa: F401

from lib import gbrain


class GBrainEnvTests(unittest.TestCase):
    def test_gbrain_env_uses_real_home_and_prepends_bun(self):
        with mock.patch.object(gbrain, "real_home", return_value=Path("/home/tester")):
            env = gbrain.gbrain_env({"PATH": "/usr/bin", "HOME": "/tmp/snap-home"})
        self.assertEqual("/home/tester", env["HOME"])
        self.assertTrue(env["PATH"].startswith("/home/tester/.bun/bin:"))
        self.assertEqual("1", env["MCP_STDIO"])

    def test_resolve_gbrain_command_prefers_repo_cli(self):
        bun = Path("/home/tester/.bun/bin/bun")
        cli = Path("/home/tester/gbrain/src/cli.ts")

        def _exists(path):
            return path in {bun, cli}

        with mock.patch.object(gbrain, "real_home", return_value=Path("/home/tester")), \
             mock.patch("pathlib.Path.exists", autospec=True, side_effect=lambda self: _exists(self)):
            cmd = gbrain.resolve_gbrain_command()
        self.assertEqual(
            ["/home/tester/.bun/bin/bun", "run", "/home/tester/gbrain/src/cli.ts"],
            cmd,
        )


class RecallNoteTests(unittest.TestCase):
    def test_render_recall_note_has_expected_shape(self):
        text = gbrain.render_recall_note(
            title="GBrain Recall - Test Topic",
            query_text="test semantic query",
            response_text="Recovered prior findings.",
            slug="concepts/test-topic",
        )
        self.assertIn("source_type: gbrain_page", text)
        self.assertIn("source_slug: concepts/test-topic", text)
        self.assertIn("Query: `test semantic query`", text)
        self.assertIn("Recovered prior findings.", text)

    def test_write_recall_note_creates_parent_dir(self):
        with helpers.tmp_env_file(""):  # cheap context helper for cleanup symmetry
            tmp_root = Path(__file__).resolve().parent / ".tmp-gbrain-test"
            out = tmp_root / "research-notes" / "01-gbrain-recall.md"
            try:
                gbrain.write_recall_note(
                    out,
                    title="GBrain Recall - Demo",
                    query_text="demo query",
                    response_text="Demo result",
                )
                self.assertTrue(out.exists())
                self.assertIn("Demo result", out.read_text(encoding="utf-8"))
            finally:
                out.unlink(missing_ok=True)
                (tmp_root / "research-notes").rmdir()
                tmp_root.rmdir()


if __name__ == "__main__":
    unittest.main()
