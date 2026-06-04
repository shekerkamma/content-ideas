"""Tests for the repo-local strategy pipeline runner."""

from pathlib import Path
import json
import tempfile
from unittest import mock
import unittest

import helpers  # noqa: F401

from lib import strategy_pipeline


def _fixture_use_case(idx, title):
    return {
        "id": f"uc-00{idx}",
        "title": title,
        "verticalName": title.lower(),
        "challenge": ["c1", "c2", "c3"],
        "solution": ["s1", "s2", "s3"],
        "how": ["h1", "h2", "h3"],
        "sourceUrls": ["https://example.com/a", "https://example.com/b"],
        "signals": [{"signalType": "trend", "postTitle": "Example signal"}],
        "confidence": "high",
    }


class LatestStrategyFeedTests(unittest.TestCase):
    def test_picks_latest_feed_with_use_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            research = Path(tmp) / "research"
            older = research / "2026-06-03"
            newer = research / "2026-06-04"
            older.mkdir(parents=True)
            newer.mkdir(parents=True)
            (older / "feed-data.json").write_text(json.dumps({"useCases": [_fixture_use_case(1, "Older")]}), encoding="utf-8")
            (newer / "feed-data.json").write_text(json.dumps({"useCases": [_fixture_use_case(2, "Newer")]}), encoding="utf-8")

            feed_path, data = strategy_pipeline.latest_strategy_feed(tmp)

        self.assertEqual("2026-06-04", feed_path.parent.name)
        self.assertEqual("Newer", data["useCases"][0]["title"])


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.use_cases = [
            _fixture_use_case(1, "On-Premise LLM for Healthcare"),
            _fixture_use_case(2, "Procurement Automation"),
        ]

    def test_selects_by_index(self):
        picked = strategy_pipeline.select_use_case(self.use_cases, "2")
        self.assertEqual("Procurement Automation", picked["title"])

    def test_selects_by_id(self):
        picked = strategy_pipeline.select_use_case(self.use_cases, "uc-001")
        self.assertEqual("On-Premise LLM for Healthcare", picked["title"])

    def test_selects_by_title_substring(self):
        picked = strategy_pipeline.select_use_case(self.use_cases, "procurement")
        self.assertEqual("Procurement Automation", picked["title"])


class Stage1RunTests(unittest.TestCase):
    def test_run_stage1_pipeline_writes_expected_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            content_root = Path(tmp) / "content"
            runs_dir = Path(tmp) / "runs"
            research = content_root / "research" / "2026-06-04"
            research.mkdir(parents=True)
            (research / "feed-data.json").write_text(
                json.dumps({"useCases": [_fixture_use_case(1, "Generative UI for Enterprise Agents")]}),
                encoding="utf-8",
            )

            with mock.patch.object(strategy_pipeline.gbrain, "gbrain_available", return_value=True), \
                 mock.patch.object(strategy_pipeline.gbrain, "recall", return_value="Recovered prior context."), \
                 mock.patch.object(strategy_pipeline, "today_utc", return_value="2026-06-04"):
                ctx = strategy_pipeline.run_stage1_pipeline("1", content_root=content_root, runs_dir=runs_dir)

            self.assertTrue(ctx.gbrain_used)
            self.assertTrue((ctx.run_dir / "content-research.md").exists())
            self.assertTrue((ctx.run_dir / "pipeline-status.md").exists())
            self.assertTrue((ctx.run_dir / "selected-use-case.json").exists())
            self.assertTrue((ctx.run_dir / "research-notes" / "01-gbrain-recall.md").exists())
            self.assertTrue((ctx.run_dir / "research-notes" / "INDEX.md").exists())
            status = (ctx.run_dir / "pipeline-status.md").read_text(encoding="utf-8")
            self.assertIn("✓ GBrain Recall", status)
            research_text = (ctx.run_dir / "content-research.md").read_text(encoding="utf-8")
            self.assertIn("Generative UI for Enterprise Agents", research_text)
            self.assertIn("Semantic retrieval executed", research_text)
            self.assertEqual("live", ctx.recall_mode)

    def test_run_stage1_pipeline_continues_when_gbrain_recall_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            content_root = Path(tmp) / "content"
            runs_dir = Path(tmp) / "runs"
            research = content_root / "research" / "2026-06-04"
            research.mkdir(parents=True)
            (research / "feed-data.json").write_text(
                json.dumps({"useCases": [_fixture_use_case(1, "Fallback Pipeline Topic")]}),
                encoding="utf-8",
            )

            with mock.patch.object(strategy_pipeline.gbrain, "gbrain_available", return_value=True), \
                 mock.patch.object(strategy_pipeline.gbrain, "recall", side_effect=RuntimeError("timeout")), \
                 mock.patch.object(strategy_pipeline, "today_utc", return_value="2026-06-04"):
                ctx = strategy_pipeline.run_stage1_pipeline("1", content_root=content_root, runs_dir=runs_dir)

            self.assertFalse(ctx.gbrain_used)
            self.assertFalse((ctx.run_dir / "research-notes" / "01-gbrain-recall.md").exists())
            status = (ctx.run_dir / "pipeline-status.md").read_text(encoding="utf-8")
            self.assertIn("◻ GBrain Recall", status)
            self.assertTrue((ctx.run_dir / "content-research.md").exists())
            self.assertEqual("timeout", ctx.recall_mode)

    def test_run_stage1_pipeline_reuses_prior_recall_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            content_root = Path(tmp) / "content"
            runs_dir = Path(tmp) / "runs"
            research = content_root / "research" / "2026-06-04"
            prior = runs_dir / "2026-06-03-real-estate" / "research-notes"
            research.mkdir(parents=True)
            prior.mkdir(parents=True)
            (research / "feed-data.json").write_text(
                json.dumps({"useCases": [_fixture_use_case(1, "Real Estate Brokerage AI")]}),
                encoding="utf-8",
            )
            (prior / "01-gbrain-recall.md").write_text(
                "---\n"
                "title: GBrain Recall - Real Estate Brokerage AI\n"
                "source_type: gbrain_page\n"
                "---\n\n"
                "# GBrain Recall - Real Estate Brokerage AI\n\n"
                "Recovered brokerage workflow context.\n",
                encoding="utf-8",
            )

            with mock.patch.object(strategy_pipeline, "DEFAULT_RUNS_DIR", runs_dir), \
                 mock.patch.object(strategy_pipeline.gbrain, "gbrain_available", return_value=True), \
                 mock.patch.object(strategy_pipeline.gbrain, "recall", side_effect=RuntimeError("timeout")), \
                 mock.patch.object(strategy_pipeline, "today_utc", return_value="2026-06-04"):
                ctx = strategy_pipeline.run_stage1_pipeline("1", content_root=content_root, runs_dir=runs_dir)

            self.assertTrue(ctx.gbrain_used)
            self.assertEqual("repo-reuse", ctx.recall_mode)
            reused = (ctx.run_dir / "research-notes" / "01-gbrain-recall.md").read_text(encoding="utf-8")
            self.assertIn("Recovered brokerage workflow context.", reused)
            self.assertIn("Reused prior repo-local GBrain recall artifact", reused)


if __name__ == "__main__":
    unittest.main()
