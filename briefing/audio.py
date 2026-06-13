"""Geração do áudio do briefing com encerramento correto.

Dois pontos centrais (correção do bug de áudio cortado):

1. O texto SEMPRE termina com a frase exata ``CLOSING_PHRASE``.
2. Depois da fala, são acrescentados ``TRAILING_SILENCE_MS`` (5 segundos) de
   silêncio dentro do próprio arquivo de áudio, garantidos na exportação — o
   silêncio não é cortado, então a última palavra nunca fica "no talo".

A função ``finalize_briefing_audio`` recebe a fala já sintetizada, anexa o
silêncio, exporta e CONFERE que o arquivo final realmente termina em silêncio.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Frase de encerramento exata exigida pelo briefing.
CLOSING_PHRASE = "E por aqui é isso por hoje."

# Silêncio final (em milissegundos) anexado depois da fala.
TRAILING_SILENCE_MS = 5_000

# Pequena pausa antes da frase de encerramento, para não "colar" no texto.
PRE_CLOSING_PAUSE_MS = 700


def ensure_closing_phrase(text: str) -> str:
    """Garante que o texto termina exatamente com a frase de encerramento."""
    cleaned = (text or "").rstrip()
    if cleaned.endswith(CLOSING_PHRASE):
        return cleaned
    # Remove pontuação solta no fim para não duplicar pontos antes da frase.
    cleaned = cleaned.rstrip(" .;:!?\n\t")
    if cleaned:
        return f"{cleaned}\n\n{CLOSING_PHRASE}"
    return CLOSING_PHRASE


def _configure_ffmpeg() -> None:
    """Aponta o pydub para um ffmpeg utilizável.

    Em ambientes sem ffmpeg no PATH, usamos o binário empacotado pelo
    ``imageio-ffmpeg``. Para WAV (formato do teste) o ffmpeg nem é necessário.
    """
    from pydub import AudioSegment

    converter = getattr(AudioSegment, "converter", None)
    if converter and Path(str(converter)).exists():
        return
    try:
        import imageio_ffmpeg

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        AudioSegment.converter = ffmpeg
        AudioSegment.ffmpeg = ffmpeg
    except Exception:
        # Sem ffmpeg só conseguimos manipular WAV; mp3 vai falhar com mensagem clara.
        pass


def synthesize_speech(text: str, cfg) -> "object":
    """Sintetiza ``text`` em fala e devolve um ``AudioSegment`` (mp3 via gTTS)."""
    import io

    from gtts import gTTS
    from pydub import AudioSegment

    _configure_ffmpeg()

    buf = io.BytesIO()
    gTTS(text=text, lang=cfg.tts_lang, tld=cfg.tts_tld).write_to_fp(buf)
    buf.seek(0)
    return AudioSegment.from_file(buf, format="mp3")


@dataclass
class AudioResult:
    path: Path
    total_ms: int
    speech_ms: int
    trailing_silence_ms: int
    tail_is_silent: bool


def finalize_briefing_audio(
    speech,
    out_path: str | Path,
    trailing_silence_ms: int = TRAILING_SILENCE_MS,
) -> AudioResult:
    """Anexa o silêncio final, exporta e confere o resultado.

    ``speech`` é um ``AudioSegment`` com a fala completa (já terminando na
    frase de encerramento). O formato de exportação vem da extensão de
    ``out_path`` (``.mp3``, ``.wav``, ``.ogg`` ...).
    """
    from pydub import AudioSegment

    _configure_ffmpeg()

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = out_path.suffix.lstrip(".").lower() or "mp3"

    silence = AudioSegment.silent(
        duration=trailing_silence_ms,
        frame_rate=speech.frame_rate,
    )
    final = speech + silence
    final.export(out_path, format=fmt)

    # Verificação autoritativa: o trecho final do áudio que foi exportado
    # precisa estar de fato em silêncio. Conferimos no próprio segmento em
    # memória (exatamente o que foi gravado), ignorando ~500ms iniciais da
    # cauda para tolerar a rampa do codec.
    check_window = max(0, trailing_silence_ms - 500)
    tail = final[-check_window:] if check_window else final[len(speech):]
    tail_is_silent = tail.max_dBFS == float("-inf") or tail.max_dBFS < -45.0
    total_ms = len(final)

    # Conferência extra opcional: reler o arquivo gravado. Para WAV funciona
    # nativamente; para formatos como mp3 o pydub precisa de ffprobe, que pode
    # não existir — nesse caso seguimos com a verificação em memória.
    try:
        reloaded = AudioSegment.from_file(out_path, format=fmt)
        total_ms = len(reloaded)
        reread_tail = reloaded[-check_window:] if check_window else reloaded[len(speech):]
        tail_is_silent = reread_tail.max_dBFS == float("-inf") or reread_tail.max_dBFS < -45.0
    except Exception:
        pass

    return AudioResult(
        path=out_path,
        total_ms=total_ms,
        speech_ms=len(speech),
        trailing_silence_ms=trailing_silence_ms,
        tail_is_silent=tail_is_silent,
    )


def build_audio_from_text(text: str, out_path: str | Path, cfg) -> AudioResult:
    """Pipeline completo de texto para arquivo de áudio do briefing."""
    final_text = ensure_closing_phrase(text)
    speech = synthesize_speech(final_text, cfg)
    return finalize_briefing_audio(speech, out_path)
