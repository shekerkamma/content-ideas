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


# --- banner: HTML text over text-free art ---------------------------------------------------

import shutil
import pytest


def _row(text, conf):
    return {"text": text, "conf": str(conf)}


def test_textfree_ignores_trace_noise_but_flags_words():
    cm = _load("check_media")
    noise = [_row("Ly", 60), _row("G", 92), _row("“4", 80), _row("al ;", 40), _row("", 95)]
    assert cm.words_in(noise, 85) == []                       # clean chip art from the 2026-10-26 set
    words = noise + [_row("attention", 95), _row("DEEPGRID", 91)]
    assert cm.words_in(words, 85) == [("attention", 95), ("DEEPGRID", 91)]


def test_fill_escapes_and_refuses_leftover_placeholders():
    mc = _load("make_card")
    out = mc.fill("<h1>{{TITLE}}</h1><p>{{TAGLINE}}</p>", "R&D <2DOM>", "on its own clock")
    assert out == "<h1>R&amp;D &lt;2DOM&gt;</h1><p>on its own clock</p>"
    with pytest.raises(ValueError):
        mc.fill("{{TITLE}} {{OTHER}}", "a", "b")


@pytest.mark.parametrize("layout", ["square", "landscape"])
def test_make_card_writes_exact_strings_without_rendering(tmp_path, layout):
    art = tmp_path / "in.jpg"; art.write_bytes(b"\xff\xd8\xff\xd9")
    r = subprocess.run([sys.executable, str(SKILL / "scripts" / "make_card.py"), "--layout", layout,
                        "--art", str(art), "--title", "DG32-2DOM",
                        "--tagline", "An attention engine on its own clock", "--out", str(tmp_path / "o"),
                        "--no-render"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    page = (tmp_path / "o" / f"card-{layout}.html").read_text()
    assert "<h1>DG32-2DOM</h1>" in page and "<p>An attention engine on its own clock</p>" in page
    assert "url(art.jpg)" in page and "{{" not in page and "white-space:nowrap" in page
    assert (tmp_path / "o" / "art.jpg").read_bytes() == art.read_bytes()


def test_skill_md_routes_banner_through_html_text():
    md = (SKILL / "SKILL.md").read_text()
    assert "make_card.py" in md and "No text, no letters, no numbers, no logos anywhere" in md
    assert "Banner text is HTML, never model-drawn" in md


REPO = SKILL.parents[1]
TESS = REPO / ".tools/tesseract/bin/tesseract"
PILOT = REPO / "runs/2026-10-26-gemini-media-dg32-2dom-linkedin"


@pytest.mark.skipif(not (TESS.exists() and (PILOT / "art-slot.jpg").exists() and (PILOT / "card.jpg").exists()),
                    reason="needs repo-local Tesseract and the 2026-10-26 pilot images (local only)")
def test_textfree_end_to_end_on_pilot_images():
    cm = SKILL / "scripts" / "check_media.py"
    run = lambda f: subprocess.run([sys.executable, str(cm), "textfree", str(f)], capture_output=True).returncode
    assert run(PILOT / "art-slot.jpg") == 0          # clean Gemini art
    assert run(PILOT / "card.jpg") == 1              # model-drawn title + tagline


def test_render_output_must_be_a_real_png(tmp_path):
    mc = _load("make_card")
    good = tmp_path / "g.png"; good.write_bytes(mc.PNG_MAGIC + b"rest")
    bad = tmp_path / "b.png"; bad.write_bytes(bytes.fromhex("1c0517fb48836c25") + b"\0" * 64)  # 2026-10-26 v18 output
    assert mc.is_png(good) and not mc.is_png(bad) and not mc.is_png(tmp_path / "missing.png")


def test_windows_bridge_prefers_nvm_node_over_system_node():
    mc = _load("make_card")
    assert ".nvm/versions/node" in mc.WSL_NODE_PICK and "WSL_NODE" in mc.WSL_NODE_PICK
