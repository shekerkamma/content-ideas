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
