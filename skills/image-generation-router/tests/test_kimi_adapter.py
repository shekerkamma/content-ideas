import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "kimi_adapter.py"
SPEC = importlib.util.spec_from_file_location("kimi_adapter", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class KimiAdapterTests(unittest.TestCase):
    def test_api_key_prefers_environment(self):
        with mock.patch.dict("os.environ", {"KIMI_API_KEY": "sk-env"}, clear=True):
            self.assertEqual(MODULE.api_key(Path("/nonexistent")), "sk-env")

    def test_api_key_reads_env_file(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / ".env"
            config.write_text('KIMI_API_KEY="sk-file-value"\n', encoding="utf-8")
            with mock.patch.dict("os.environ", {}, clear=True):
                self.assertEqual(MODULE.api_key(config), "sk-file-value")

    def test_api_key_missing_is_clear_error(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(MODULE.HelperError, "KIMI_API_KEY"):
                MODULE.api_key(Path("/nonexistent/kimi.env"))

    def test_select_model_prefers_known_free_default(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            self.assertEqual(
                MODULE.select_model(["anthropic/claude-fable-5", "moonshotai/kimi-k3-free"], None),
                "moonshotai/kimi-k3-free",
            )

    def test_base_url_resolution_order(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / ".env"
            config.write_text("KIMI_BASE_URL=https://from-config.example/v1\n", encoding="utf-8")
            with mock.patch.dict("os.environ", {}, clear=True):
                self.assertEqual(MODULE.base_url(config, "https://flag.example/v1"), "https://flag.example/v1")
                self.assertEqual(MODULE.base_url(config, None), "https://from-config.example/v1")
            with mock.patch.dict("os.environ", {"KIMI_BASE_URL": "https://from-env.example/v1"}, clear=True):
                self.assertEqual(MODULE.base_url(config, None), "https://from-env.example/v1")
            with mock.patch.dict("os.environ", {}, clear=True):
                self.assertEqual(MODULE.base_url(Path("/nonexistent"), None), MODULE.DEFAULT_BASE_URL)

    def test_select_model_rejects_unavailable_explicit_model(self):
        with self.assertRaisesRegex(MODULE.HelperError, "unavailable"):
            MODULE.select_model(["kimi-k3-free"], "k9-imaginary")

    def test_refine_payload_keeps_text_free_constraint(self):
        payload = MODULE.build_payload("prompt-refinement", "kimi-k3-free", "navy cover scene", None)
        self.assertEqual(payload["model"], "kimi-k3-free")
        self.assertIn("no text", payload["messages"][0]["content"])
        self.assertEqual(payload["messages"][1]["content"], "navy cover scene")

    def test_vision_payload_embeds_image_url(self):
        payload = MODULE.build_payload("vision-review", "k3", "describe layout", "data:image/png;base64,QUJD")
        content = payload["messages"][0]["content"]
        self.assertEqual(content[0], {"type": "text", "text": "describe layout"})
        self.assertEqual(content[1]["image_url"]["url"], "data:image/png;base64,QUJD")

    def test_sidecar_declares_non_image_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "refined.txt"
            output.write_text("refined\n", encoding="utf-8")
            sidecar = MODULE.write_sidecar(output, role="prompt-refinement", resolved_model="kimi-k3-free", prompt="p")
            record = json.loads(sidecar.read_text(encoding="utf-8"))
            self.assertIs(record["is_image_generation"], False)
            self.assertEqual(record["role"], "prompt-refinement")
            self.assertNotIn("execution_path", record)

    def test_probe_without_key_fails_gracefully(self):
        stderr = io.StringIO()
        with mock.patch.dict("os.environ", {}, clear=True):
            with mock.patch("sys.argv", ["kimi_adapter.py", "--probe", "--config", "/nonexistent/kimi.env"]):
                with contextlib.redirect_stderr(stderr):
                    exit_code = MODULE.main()
        self.assertEqual(exit_code, 1)
        self.assertIn("KIMI_API_KEY", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_helper_roles_never_include_a_pptx_execution_path(self):
        schema_path = Path(__file__).parents[2] / "pptx-visual-spec" / "references" / "visual-spec-schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        execution_paths = schema["$defs"]["visual"]["properties"]["execution"]["properties"]["path"]["enum"]
        for path in execution_paths:
            self.assertNotIn("kimi", path.lower())


if __name__ == "__main__":
    unittest.main()
