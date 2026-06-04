import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import helpers  # noqa: F401

import generate_feed

FIXTURE_FEED = {
    "meta": {"date": "March 20, 2026", "subtitle": "s", "footer": "f"},
    "posts": [
        {
            "title": "A post",
            "text": "summary",
            "url": "https://x.com/acme/1",
            "handle": "@acme",
            "displayName": "Acme Co",
            "platform": "x",
            "timestamp": "2026-03-20T09:00:00Z",
            "sortValue": 3200,
            "engagement": {"likes": 300, "views": 3200},
            "zScore": 3.1,
            "comments": [],
        }
    ],
    "ideas": {"items": [{"title": "Idea", "concept": "c", "funnel": "mofu"}]},
}

FIXTURE_STRATEGY_FEED = {
    "meta": {"date": "June 3, 2026", "subtitle": "strategy", "footer": "f"},
    "posts": [
        {
            "title": "Hospitals want AI without cloud risk",
            "text": "summary",
            "url": "https://youtube.com/watch?v=abc",
            "handle": "@builder",
            "displayName": "Builder",
            "platform": "youtube",
            "timestamp": "2026-06-03T09:00:00Z",
            "sortValue": 44000,
            "engagement": {"likes": 2200, "views": 44000},
            "zScore": 2.6,
            "comments": [],
        }
    ],
    "ideas": {"items": [{"title": "Thought leadership angle", "concept": "c", "funnel": "bofu"}]},
    "useCases": [
        {
            "id": "uc-001",
            "kicker": "USE CASE 01  ·  VERTICAL",
            "title": "On-Premise LLM for Healthcare",
            "challenge": [
                "Patient data must stay on-site",
                "Clinical AI needs low latency",
                "Hospitals lack internal ML ops",
            ],
            "solution": [
                "On-prem inference keeps PHI in-network",
                "Optimized serving delivers bedside response",
                "Managed deployment removes internal ML burden",
            ],
            "how": [
                "Clinical event triggers internal API call",
                "LLM processes patient context on-site",
                "Result returns to the EHR with audit trail",
            ],
            "stats": [
                ["100%", "data on-prem"],
                ["<200ms", "inference latency"],
                ["HIPAA", "compliant by design"],
            ],
            "stack": [
                ["EXPERIENCE", "EHR integration / clinical UI"],
                ["ORCHESTRATION", "Inference routing + failover"],
                ["CONTEXT", "Patient records + guidelines"],
                ["ACTUATION", "EHR write-back + audit log"],
            ],
            "systems": ["EHR", "PACS", "Internal API", "Audit/Compliance"],
            "users": "CMIO · clinical informatics · IT security",
            "orgs": [
                ["Mayo Clinic", "Academic medical center with internal AI research lab"],
                ["Kaiser Permanente", "Integrated health system, 12M+ members"],
            ],
            "signals": [
                {
                    "postUrl": "https://youtube.com/watch?v=abc",
                    "postTitle": "Why hospitals are banning ChatGPT",
                    "handle": "@builder",
                    "platform": "youtube",
                    "engagement": {"views": 44000, "likes": 2200},
                    "signalType": "demand",
                    "extract": "Hospitals want AI, but PHI cannot leave the network.",
                }
            ],
            "patterns": ["Multiple high-signal posts mention healthcare + data sovereignty"],
            "verticalName": "On-premise LLM for healthcare",
            "sourceUrls": ["https://youtube.com/watch?v=abc", "https://example.com/hipaa"],
            "confidence": "high",
            "timestamp": "2026-06-03T00:00:00Z",
        }
    ],
}


def assert_valid_use_case_schema(testcase, use_case):
    testcase.assertRegex(use_case["id"], r"^uc-\d+$")
    testcase.assertIn(use_case["confidence"], {"high", "medium", "exploratory"})
    testcase.assertEqual(3, len(use_case["challenge"]))
    testcase.assertEqual(3, len(use_case["solution"]))
    testcase.assertEqual(3, len(use_case["how"]))
    testcase.assertEqual(3, len(use_case["stats"]))
    testcase.assertEqual(4, len(use_case["stack"]))
    testcase.assertGreaterEqual(len(use_case["systems"]), 3)
    testcase.assertLessEqual(len(use_case["systems"]), 5)
    testcase.assertGreaterEqual(len(use_case["orgs"]), 2)
    testcase.assertLessEqual(len(use_case["orgs"]), 4)
    testcase.assertGreaterEqual(len(use_case["sourceUrls"]), 1)
    testcase.assertTrue(use_case["verticalName"])
    testcase.assertTrue(all(len(item) == 2 for item in use_case["stats"]))
    testcase.assertEqual(
        ["EXPERIENCE", "ORCHESTRATION", "CONTEXT", "ACTUATION"],
        [item[0] for item in use_case["stack"]],
    )


class LoadTests(unittest.TestCase):
    def test_load_feed_and_feedback(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            run = Path(d)
            (run / "feed-data.json").write_text(json.dumps(FIXTURE_FEED))
            (run / "feedback.json").write_text(json.dumps({
                "reviews": [{"item_id": "ideas::Idea", "rating": "up", "note": "yes"}],
            }))
            feed = generate_feed.load_feed(run / "feed-data.json")
            self.assertEqual("March 20, 2026", feed["meta"]["date"])
            state = generate_feed.load_feedback_state(run / "feedback.json")
            self.assertEqual("up", state["ideas::Idea"]["rating"])

    def test_load_feed_missing(self):
        self.assertIsNone(generate_feed.load_feed(Path("/nope/feed-data.json")))

    def test_load_feed_strategy_use_cases_preserved(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            run = Path(d)
            (run / "feed-data.json").write_text(json.dumps(FIXTURE_STRATEGY_FEED))
            feed = generate_feed.load_feed(run / "feed-data.json")
            self.assertIn("useCases", feed)
            self.assertEqual("On-Premise LLM for Healthcare", feed["useCases"][0]["title"])
            assert_valid_use_case_schema(self, feed["useCases"][0])


class GenerateHtmlTests(unittest.TestCase):
    def test_placeholder_replaced_and_data_embedded(self):
        html = generate_feed.generate_html(FIXTURE_FEED, {}, "server")
        self.assertNotIn(generate_feed.PLACEHOLDER, html)
        self.assertIn("const FEED_DATA =", html)
        self.assertIn('const FEEDBACK_MODE = "server"', html)
        self.assertIn("March 20, 2026", html)

    def test_template_actually_has_placeholder(self):
        template = generate_feed.DEFAULT_TEMPLATE.read_text()
        self.assertIn(generate_feed.PLACEHOLDER, template)

    def test_static_mode_flag_distinguished(self):
        html = generate_feed.generate_html(FIXTURE_FEED, {}, "static")
        self.assertIn('const FEEDBACK_MODE = "static"', html)

    def test_strategy_use_cases_embedded_in_html(self):
        html = generate_feed.generate_html(FIXTURE_STRATEGY_FEED, {}, "server")
        self.assertIn('"useCases"', html)
        self.assertIn("On-Premise LLM for Healthcare", html)
        self.assertIn("On-premise LLM for healthcare", html)

    def test_strategy_fixture_matches_documented_shape(self):
        self.assertIn("useCases", FIXTURE_STRATEGY_FEED)
        self.assertEqual(1, len(FIXTURE_STRATEGY_FEED["useCases"]))
        assert_valid_use_case_schema(self, FIXTURE_STRATEGY_FEED["useCases"][0])


class MainTests(unittest.TestCase):
    def test_main_static_writes_strategy_html_to_default_path(self):
        with tempfile.TemporaryDirectory() as d:
            run = Path(d)
            feed_path = run / "feed-data.json"
            feed_path.write_text(json.dumps(FIXTURE_STRATEGY_FEED))

            with mock.patch("sys.stdout"):
                rc = generate_feed.main([str(run), "--static"])

            out = run / "for-you.html"
            self.assertEqual(0, rc)
            self.assertTrue(out.exists())
            html = out.read_text()
            self.assertIn("On-Premise LLM for Healthcare", html)
            self.assertIn('"useCases"', html)
            self.assertIn('const FEEDBACK_MODE = "static"', html)

    def test_main_static_writes_strategy_html_to_explicit_path(self):
        with tempfile.TemporaryDirectory() as d:
            run = Path(d)
            feed_path = run / "feed-data.json"
            feed_path.write_text(json.dumps(FIXTURE_STRATEGY_FEED))
            out = run / "exports" / "strategy-feed.html"

            with mock.patch("sys.stdout"):
                rc = generate_feed.main([str(run), "--static", str(out)])

            self.assertEqual(0, rc)
            self.assertTrue(out.exists())
            self.assertIn("On-premise LLM for healthcare", out.read_text())


if __name__ == "__main__":
    unittest.main()
