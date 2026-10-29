import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('gemini_video', Path(__file__).resolve().parents[1]/'skills/gemini-video/scripts/analyze.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)

class VideoTests(unittest.TestCase):
    def test_credential_config_wins_over_other_environment(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'config.yaml';p.write_text('gemini-api-key:\n  - api-key: test-host-secret\n')
            with patch.dict(v.os.environ, {'GEMINI_API_KEY':'other-secret'}):
                key,source=v.credential(p)
            self.assertEqual(key,'test-host-secret');self.assertEqual(source,str(p))

    def test_multiple_credentials_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'config.yaml';p.write_text('gemini-api-key:\n  - api-key: a\n  - api-key: b\n')
            with self.assertRaises(ValueError):v.credential(p)

    def test_non_youtube_urls_rejected(self):
        with self.assertRaises(ValueError):v.video_part('https://example.com/private.mp4')

    def test_bad_offsets_make_no_request(self):
        with patch.object(v,'request') as call:
            with self.assertRaises(ValueError):v.analyze('unused','unused',start=5,end=2)
            call.assert_not_called()

    def test_upload_deleted_when_generation_fails(self):
        file={'name':'files/test','uri':'https://generativelanguage.googleapis.com/test','mimeType':'video/mp4','state':'ACTIVE'}
        with patch.object(v,'credential',return_value=('test-secret','host')),patch.object(v,'video_part',return_value=(None,(Path('x.mp4'),'video/mp4'))),patch.object(v,'upload',return_value=file),patch.object(v,'request',side_effect=[RuntimeError('HTTP 429'),({}, {})]) as call:
            with self.assertRaises(RuntimeError):v.analyze('x.mp4','unused')
            self.assertEqual(call.call_args.kwargs.get('method'),'DELETE')

    def test_output_has_native_mode_model_and_no_credential(self):
        reply={'modelVersion':'gemini-3.8-flash','candidates':[{'content':{'parts':[{'text':'red then blue'}]}}]}
        with tempfile.TemporaryDirectory() as d,patch.object(v,'credential',return_value=('test-secret','host')),patch.object(v,'video_part',return_value=({'inlineData':{'mimeType':'video/mp4','data':'dmlkZW8='}},None)),patch.object(v,'request',return_value=(reply,{})):
            report=v.analyze('clip.mp4',d)
            text=(Path(d)/'analysis.json').read_text()
            self.assertNotIn('test-secret',text);self.assertNotIn('dmlkZW8=',text)
            self.assertEqual(report['returnedModel'],'gemini-3.8-flash');self.assertEqual(report['inputMode'],'inline-video')

if __name__ == '__main__':unittest.main()
