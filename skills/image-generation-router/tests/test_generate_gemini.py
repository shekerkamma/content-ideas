import base64
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from jsonschema import Draft202012Validator


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "generate_gemini.py"
SPEC = importlib.util.spec_from_file_location("generate_gemini", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class GenerateGeminiTests(unittest.TestCase):
    def test_image_models_filters_and_sorts(self):
        catalog = {"data": [{"id": "text-model"}, {"id": "z-image"}, {"id": "a-image"}]}
        self.assertEqual(MODULE.image_models(catalog), ["a-image", "z-image"])

    def test_select_model_prefers_known_live_default(self):
        available = ["other-image", "gemini-3.1-flash-image"]
        with mock.patch.dict("os.environ", {}, clear=True):
            self.assertEqual(MODULE.select_model(available, None), "gemini-3.1-flash-image")

    def test_select_model_rejects_unavailable_explicit_model(self):
        with self.assertRaisesRegex(MODULE.RouterError, "unavailable"):
            MODULE.select_model(["gemini-3.1-flash-image"], "gemini-3-pro-image-preview")

    def test_extract_data_image(self):
        encoded = base64.b64encode(b"image-bytes").decode("ascii")
        response = {"choices": [{"message": {"content": f"data:image/jpeg;base64,{encoded}"}}]}
        media_type, data = MODULE.extract_data_image(response)
        self.assertEqual(media_type, "image/jpeg")
        self.assertEqual(data, b"image-bytes")

    def test_client_key_does_not_require_yaml_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "config.yaml"
            config.write_text('api-keys:\n  - "sk-test-value"\n', encoding="utf-8")
            with mock.patch.dict("os.environ", {}, clear=True):
                self.assertEqual(MODULE.client_key(config), "sk-test-value")

    def test_pptx_schema_accepts_router_execution_path(self):
        schema_path = Path(__file__).parents[2] / "pptx-visual-spec" / "references" / "visual-spec-schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        execution_paths = schema["$defs"]["visual"]["properties"]["execution"]["properties"]["path"]["enum"]
        self.assertIn("cliproxyapi-gemini", execution_paths)

    def test_normative_contract_matches_schema(self):
        skill_root = Path(__file__).parents[1]
        contract = json.loads((skill_root / "contracts/image-generation-routing-contract.json").read_text())
        schema = json.loads((skill_root / "contracts/image-generation-routing-contract.schema.json").read_text())
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(contract)), [])

    def test_adapter_reads_endpoints_and_model_order_from_contract(self):
        gemini = MODULE.ROUTING_CONTRACT["providers"]["cliproxyapi-gemini"]
        self.assertEqual(MODULE.DISCOVERY_ENDPOINT, gemini["discovery_endpoint"])
        self.assertEqual(MODULE.GENERATION_ENDPOINT, gemini["generation_endpoint"])
        self.assertEqual(MODULE.DEFAULT_MODEL_ORDER, tuple(gemini["preferred_models"]))


if __name__ == "__main__":
    unittest.main()
