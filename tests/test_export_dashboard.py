import csv
import json
import tempfile
import unittest
from pathlib import Path

import helpers  # noqa: F401

import export_dashboard

FEED = {
    "meta": {"date": "March 20, 2026"},
    "posts": [
        {
            "title": "Outlier post",
            "url": "https://x.com/acme/1",
            "handle": "@acme",
            "displayName": "Acme Co",
            "platform": "x",
            "sortValue": 3200,
            "engagement": {"likes": 300, "views": 3200},
            "zScore": 3.1,
        },
        {
            "title": "Baseline beater",
            "url": "https://youtube.com/watch?v=1",
            "handle": "@me",
            "platform": "youtube",
            "performanceDirection": "up",
        },
        {"title": "Plain", "platform": "x", "engagement": None},
    ],
    "ideas": {
        "items": [
            {"title": "Idea A", "funnel": "mofu", "brief": {"suggestedHook": "Hook"}},
            {"title": "Idea B", "funnel": "tofu"},
        ],
        "patterns": ["**Short** wins"],
    },
}


class ExportDashboardTests(unittest.TestCase):
    def _run(self, feed):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "feed-data.json").write_text(json.dumps(feed), encoding="utf-8")
        self.assertEqual(0, export_dashboard.main([str(tmp)]))
        return tmp / "dashboard"

    def test_writes_posts_ideas_and_summary(self):
        out = self._run(FEED)
        with (out / "posts.csv").open(encoding="utf-8") as fh:
            posts = list(csv.DictReader(fh))
        self.assertEqual(3, len(posts))
        self.assertEqual("Acme Co", posts[0]["creator"])
        self.assertEqual("@me", posts[1]["creator"])
        self.assertEqual("300", posts[0]["likes"])
        self.assertEqual("", posts[2]["likes"])
        self.assertEqual(["True", "True", "False"], [p["isOutlier"] for p in posts])

        with (out / "ideas.csv").open(encoding="utf-8") as fh:
            ideas = list(csv.DictReader(fh))
        self.assertEqual("Hook", ideas[0]["suggestedHook"])

        summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(3, summary["posts"])
        self.assertEqual(2, summary["outliers"])
        self.assertEqual({"x": 2, "youtube": 1}, summary["postsByPlatform"])
        self.assertEqual({"mofu": 1, "tofu": 1}, summary["ideasByFunnel"])
        self.assertFalse((out / "use-cases.csv").exists())

    def test_use_cases_exported_in_strategy_mode_and_cleared_after(self):
        feed = dict(FEED, useCases=[{"id": "uc-001", "title": "T", "signals": [{}, {}]}])
        out = self._run(feed)
        with (out / "use-cases.csv").open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        self.assertEqual("2", rows[0]["signalCount"])

        export_dashboard.export(FEED, out)
        self.assertFalse((out / "use-cases.csv").exists())

    def test_missing_feed_returns_error(self):
        tmp = Path(tempfile.mkdtemp())
        self.assertEqual(1, export_dashboard.main([str(tmp)]))


if __name__ == "__main__":
    unittest.main()
