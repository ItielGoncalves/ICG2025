"""Testes do encerramento do áudio (correção do corte da última palavra).

São hermeticos: não dependem de rede nem de ffmpeg. A "fala" é simulada por um
tom senoidal (pydub puro) exportado em WAV, e verificamos que:
- o texto sempre termina com a frase exata de encerramento;
- o arquivo final tem ~5s de silêncio no fim, e esse trecho está de fato em silêncio.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from briefing import audio as audio_mod  # noqa: E402
from briefing.audio import CLOSING_PHRASE, TRAILING_SILENCE_MS  # noqa: E402


def test_ensure_closing_phrase_appends_when_missing():
    out = audio_mod.ensure_closing_phrase("Resumo do dia.")
    assert out.endswith(CLOSING_PHRASE)


def test_ensure_closing_phrase_no_duplicate():
    text = f"Resumo do dia.\n\n{CLOSING_PHRASE}"
    out = audio_mod.ensure_closing_phrase(text)
    assert out.endswith(CLOSING_PHRASE)
    assert out.count(CLOSING_PHRASE) == 1


def test_ensure_closing_phrase_empty():
    assert audio_mod.ensure_closing_phrase("") == CLOSING_PHRASE
    assert audio_mod.ensure_closing_phrase("   \n ") == CLOSING_PHRASE


def _fake_speech(ms: int = 2000):
    from pydub.generators import Sine

    return Sine(440).to_audio_segment(duration=ms)


def test_finalize_appends_five_seconds_of_silence(tmp_path):
    speech = _fake_speech(2000)
    out = tmp_path / "briefing.wav"
    result = audio_mod.finalize_briefing_audio(speech, out)

    # Duração total = fala + 5s, com pequena tolerância de codec/container.
    expected = len(speech) + TRAILING_SILENCE_MS
    assert abs(result.total_ms - expected) <= 200
    assert result.trailing_silence_ms == TRAILING_SILENCE_MS
    assert out.exists()


def test_tail_is_actually_silent(tmp_path):
    speech = _fake_speech(2000)
    out = tmp_path / "briefing.wav"
    result = audio_mod.finalize_briefing_audio(speech, out)
    assert result.tail_is_silent, "Os últimos 5 segundos deveriam estar em silêncio."


def test_speech_region_is_not_silent(tmp_path):
    """Garante que o teste de silêncio não é trivial: a fala não é silenciosa."""
    from pydub import AudioSegment

    speech = _fake_speech(2000)
    out = tmp_path / "briefing.wav"
    audio_mod.finalize_briefing_audio(speech, out)

    reloaded = AudioSegment.from_file(out, format="wav")
    speech_region = reloaded[:1500]
    assert speech_region.max_dBFS > -20.0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
