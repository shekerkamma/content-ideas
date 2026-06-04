"""Tests for persistent path resolution helpers."""

from pathlib import Path
from unittest import mock
import unittest

import helpers  # noqa: F401

from lib import env


class ContentHomeTests(unittest.TestCase):
    def test_defaults_to_real_home_documents_content(self):
        with mock.patch.object(env, "real_home", return_value=Path("/home/tester")):
            with mock.patch.dict("os.environ", {}, clear=True):
                self.assertEqual(Path("/home/tester/Documents/Content"), env.content_home())

    def test_honors_content_home_override(self):
        with mock.patch.dict("os.environ", {"CONTENT_HOME": "/tmp/custom-content"}, clear=True):
            self.assertEqual(Path("/tmp/custom-content"), env.content_home())


if __name__ == "__main__":
    unittest.main()
