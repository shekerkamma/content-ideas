import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "watch" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import download  # noqa: E402

BOT_CHECK = (
    "ERROR: [youtube] abc: Sign in to confirm you’re not a bot. "
    "Use --cookies-from-browser or --cookies for the authentication.\n"
)


def _fake_run(stderr, returncode=1):
    return lambda cmd, **kw: types.SimpleNamespace(returncode=returncode, stderr=stderr)


class CookiesArgsTest(unittest.TestCase):
    def test_no_cookies_configured(self):
        with mock.patch.object(download, "get_config", return_value={"cookies_file": None}):
            self.assertEqual(download._cookies_args(), [])

    def test_existing_cookies_file_is_passed(self):
        with tempfile.NamedTemporaryFile(suffix=".txt") as f:
            with mock.patch.object(download, "get_config", return_value={"cookies_file": f.name}):
                self.assertEqual(download._cookies_args(), ["--cookies", f.name])

    def test_missing_cookies_file_is_ignored(self):
        with mock.patch.object(download, "get_config", return_value={"cookies_file": "/nonexistent/c.txt"}):
            self.assertEqual(download._cookies_args(), [])


class RunYtdlpTest(unittest.TestCase):
    def test_bot_check_fails_fast_with_options(self):
        with mock.patch.object(download.subprocess, "run", _fake_run(BOT_CHECK)):
            with self.assertRaises(SystemExit) as ctx:
                download._run_ytdlp(["yt-dlp", "url"])
        self.assertIn("WATCH_COOKIES_FILE", str(ctx.exception))

    def test_bot_check_with_cookies_says_reexport(self):
        with mock.patch.object(download.subprocess, "run", _fake_run(BOT_CHECK)):
            with self.assertRaises(SystemExit) as ctx:
                download._run_ytdlp(["yt-dlp", "--cookies", "c.txt", "url"])
        self.assertIn("re-export", str(ctx.exception))

    def test_other_errors_return_exit_code(self):
        with mock.patch.object(download.subprocess, "run", _fake_run("ERROR: subtitles 429\n")):
            self.assertEqual(download._run_ytdlp(["yt-dlp", "url"]), 1)
