"""Offline checks for narrate_clips.py: WAV handling and dialogue request shape."""
import importlib.util, io, pathlib, wave

import pytest

spec = importlib.util.spec_from_file_location(
    "narrate_clips", pathlib.Path(__file__).parents[1] / "scripts" / "narrate_clips.py")
nc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nc)

SPK = {"Host": "Puck", "Guest": "voice_abc123"}


def test_raw_pcm_is_wrapped_once():
    wav = nc.to_wav(b"\x00\x00" * 24000)
    assert wav.startswith(b"RIFF") and wav.find(b"RIFF", 4) == -1
    with wave.open(io.BytesIO(wav)) as w:
        assert w.getnframes() == 24000 and w.getframerate() == 24000


def test_finished_wav_is_not_rewrapped():
    # 3.8 returns audio/wav; the old code nested it inside a second RIFF.
    inner = nc.to_wav(b"\x00\x00" * 100)
    assert nc.to_wav(inner) == inner


def test_dialogue_turns_carry_speaker_and_style():
    body = nc.request_body("Host (curious): So what?\nGuest: [sigh] Cores.\n  and more.", "Charon", speakers=SPK)
    parts = body["contents"][0]["parts"]
    assert parts == [
        {"text": "So what?", "speech_metadata": {"speaker": "Host", "style": "curious"}},
        {"text": "[sigh] Cores. and more.", "speech_metadata": {"speaker": "Guest"}},
    ]
    cfgs = body["generationConfig"]["speechConfig"]["multiSpeakerVoiceConfig"]["speakerVoiceConfigs"]
    assert cfgs[0]["voiceConfig"] == {"prebuiltVoiceConfig": {"voiceName": "Puck"}}
    assert cfgs[1]["voiceConfig"] == {"voice": "voice_abc123"}


def test_unknown_speaker_fails_loudly():
    with pytest.raises(SystemExit):
        nc.request_body("Narrator: hello", "Charon", speakers=SPK)


def test_mono_body_unchanged_without_style():
    body = nc.request_body("Line one\nline two", "Charon")
    assert body["contents"][0]["parts"] == [{"text": "Line one line two"}]
    assert body["generationConfig"]["speechConfig"] == {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Charon"}}}


def test_cli_dialogue_argv_and_script():
    argv, script = nc.cli_args("Host: So what?\nGuest: [sigh] Cores.\n  and more.", "Charon", "",
                               SPK, "gemini-3.8-flash-tts", "/o/a.wav")
    assert script == "Host: So what?\nGuest: [sigh] Cores. and more."
    assert argv[1:] == ["tts", "--stdin", "-m", "gemini-3.8-flash-tts",
                        "--multi-speaker", "Host=Puck,Guest=voice_abc123", "--out", "/o/a.wav", "--no-interactive"]


def test_cli_mono_uses_voice():
    argv, script = nc.cli_args("Line one\nline two", "voice_abc123", "", {}, "gemini-3.1-flash-tts-preview", "/o/a.wav")
    assert script == "Line one line two" and argv[argv.index("--voice") + 1] == "voice_abc123"


@pytest.mark.parametrize("text,style,spk", [
    ("Host (curious): So what?\nGuest: Cores.", "", SPK),   # per-turn style
    ("Host: So what?", "dry", SPK),                          # global style, dialogue
    ("Plain line", "warm", {}),                              # global style, mono
])
def test_cli_refuses_to_drop_style(text, style, spk):
    with pytest.raises(SystemExit, match="--engine gemini"):
        nc.cli_args(text, "Charon", style, spk, "gemini-3.8-flash-tts", "/o/a.wav")


def _fake_cli(tmp_path, body: str):
    # Stand-in for the binary: records stdin + key, then writes whatever `body` does to --out.
    exe = tmp_path / "gemini-api"
    exe.write_text("#!/usr/bin/env python3\nimport sys,os\nout=sys.argv[sys.argv.index('--out')+1]\n"
                   f"open(os.path.join(os.path.dirname(out),'seen.txt'),'w').write(os.environ.get('GEMINI_API_KEY','')+'|'+sys.stdin.read())\n"
                   + body)
    exe.chmod(0o755)
    return str(exe)


def test_cli_runs_fills_key_and_checks_wav(tmp_path, monkeypatch):
    wav = nc.to_wav(b"\x00\x00" * 240)
    (tmp_path / "src.wav").write_bytes(wav)
    exe = _fake_cli(tmp_path, f"open(out,'wb').write(open({str(tmp_path / 'src.wav')!r},'rb').read())\n")
    monkeypatch.setenv("GEMINI_API_BIN", exe)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("GOOGLE_GENERATIVE_AI_API_KEY", "k-test")
    out = str(tmp_path / "a.wav")
    nc.gemini_cli(*nc.cli_args("Hello", "Charon", "", {}, "m", out), out)
    assert (tmp_path / "a.wav").read_bytes() == wav
    assert (tmp_path / "seen.txt").read_text() == "k-test|Hello"


def test_cli_non_wav_output_fails(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_BIN", _fake_cli(tmp_path, "open(out,'wb').write(b'not audio')\n"))
    out = str(tmp_path / "a.wav")
    with pytest.raises(SystemExit, match="no WAV"):
        nc.gemini_cli(*nc.cli_args("Hello", "Charon", "", {}, "m", out), out)


def test_cli_nonzero_exit_surfaces_stderr(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_BIN", _fake_cli(tmp_path, "sys.stderr.write('quota gone'); sys.exit(1)\n"))
    out = str(tmp_path / "a.wav")
    with pytest.raises(SystemExit, match="quota gone"):
        nc.gemini_cli(*nc.cli_args("Hello", "Charon", "", {}, "m", out), out)
