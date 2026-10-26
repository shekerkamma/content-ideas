"""Offline checks for skills/gemini-media-lane (no API calls)."""
import base64, importlib.util, io, json, re, subprocess, sys, wave
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills" / "gemini-media-lane"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, SKILL / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _wav(frames: bytes) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(frames)
    return buf.getvalue()


def test_skill_md_has_no_dollar_digit():
    # Claude Code replaces a dollar sign followed by a number with invocation arguments;
    # a price written that way rendered as "~banner.15" on 2026-10-26.
    assert re.findall(r"\$\d", (SKILL / "SKILL.md").read_text()) == []


def test_wav_check_passes_single_and_fails_double_header(tmp_path):
    cm = _load("check_media")
    good = tmp_path / "good.wav"; good.write_bytes(_wav(b"\0\0" * 240))
    double = tmp_path / "double.wav"; double.write_bytes(_wav(_wav(b"\0\0" * 240)))
    assert cm.check_wav(str(good)) == 0
    assert cm.check_wav(str(double)) == 1


def test_dr_extract_joins_every_text_part_in_order(tmp_path):
    png = base64.b64encode(b"\x89PNG\r\n\x1a\nfake").decode()
    result = {"status": "completed", "usage": {"total_input_tokens": 10, "grounding_tool_count": [{"count": 3}]},
              "steps": [{"type": "user_input"},
                        {"type": "model_output", "content": [{"type": "text", "text": "# Title\n\nShort opening."}]},
                        {"type": "model_output", "content": [
                            {"type": "image", "mime_type": "image/png", "data": png},
                            {"type": "text", "text": "## Body\n\n" + "much longer body text " * 20}]}]}
    src = tmp_path / "dr.json"; src.write_text(json.dumps(result))
    out = tmp_path / "report.md"
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "dr_extract.py"), str(src), str(out),
                        "--media", str(tmp_path / "media")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    text = out.read_text()
    assert text.startswith("# Title")            # the longest part alone would start at "## Body"
    assert text.index("Short opening") < text.index("## Body")
    assert (tmp_path / "media" / "research-chart-1.png").exists()
    assert "searches 3" in r.stdout


def test_dr_extract_refuses_unfinished_run(tmp_path):
    src = tmp_path / "dr.json"; src.write_text(json.dumps({"status": "in_progress", "steps": []}))
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "dr_extract.py"), str(src), str(tmp_path / "x.md")],
                       capture_output=True, text=True)
    assert r.returncode == 1
