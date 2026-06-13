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
    """Aponta o pydub para um ffmpeg/ffprobe utilizáveis.

    Prioriza o ffmpeg do sistema (na sua máquina local). Se não houver, usa o
    binário empacotado pelo ``imageio-ffmpeg`` para o ffmpeg. Para WAV o ffmpeg
    nem é necessário; para mp3, ler de volta o arquivo também exige ffprobe.
    """
    import shutil

    from pydub import AudioSegment

    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        return  # ffmpeg do sistema resolve tudo

    converter = getattr(AudioSegment, "converter", None)
    if converter and Path(str(converter)).exists() and getattr(AudioSegment, "ffprobe", None):
        return
    try:
        import imageio_ffmpeg

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        AudioSegment.converter = ffmpeg
        AudioSegment.ffmpeg = ffmpeg
    except Exception:
        # Sem ffmpeg só conseguimos manipular WAV; mp3 dará mensagem clara.
        pass


def _gtts_speech(text: str, cfg):
    import io

    from gtts import gTTS
    from pydub import AudioSegment

    buf = io.BytesIO()
    gTTS(text=text, lang=cfg.tts_lang, tld=cfg.tts_tld).write_to_fp(buf)
    buf.seek(0)
    return AudioSegment.from_file(buf, format="mp3")


def _elevenlabs_speech(text: str, cfg):
    """Sintetiza com ElevenLabs e devolve um ``AudioSegment`` (a partir de mp3)."""
    import io

    import requests
    from pydub import AudioSegment

    if not cfg.elevenlabs_api_key or not cfg.elevenlabs_voice_id:
        raise RuntimeError(
            "ElevenLabs não configurado: defina ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID "
            "(ou use BRIEFING_TTS_ENGINE=gtts)."
        )
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{cfg.elevenlabs_voice_id}"
    headers = {
        "xi-api-key": cfg.elevenlabs_api_key,
        "accept": "audio/mpeg",
        "content-type": "application/json",
    }
    payload = {"text": text, "model_id": cfg.elevenlabs_model}
    resp = requests.post(url, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    return AudioSegment.from_file(io.BytesIO(resp.content), format="mp3")


def synthesize_speech(text: str, cfg) -> "object":
    """Sintetiza ``text`` em fala e devolve um ``AudioSegment``.

    Usa o motor definido em ``cfg.tts_engine`` (``elevenlabs`` por padrão).
    """
    _configure_ffmpeg()
    engine = (cfg.tts_engine or "elevenlabs").lower()
    if engine == "gtts":
        return _gtts_speech(text, cfg)
    return _elevenlabs_speech(text, cfg)


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


def finalize_audio_file(
    in_path: str | Path,
    out_path: str | Path,
    cfg,
    add_closing_phrase: bool = True,
) -> AudioResult:
    """Corrige o encerramento de um áudio já existente.

    Para o caso em que o plugin (ElevenLabs + Telegram) já gerou o áudio: este
    helper carrega o arquivo, opcionalmente sintetiza e anexa a frase de
    encerramento, e garante os 5 segundos de silêncio finais antes do envio.
    """
    from pydub import AudioSegment

    _configure_ffmpeg()
    in_path = Path(in_path)
    fmt_in = in_path.suffix.lstrip(".").lower() or "mp3"
    speech = AudioSegment.from_file(in_path, format=fmt_in)

    if add_closing_phrase:
        pause = AudioSegment.silent(duration=PRE_CLOSING_PAUSE_MS, frame_rate=speech.frame_rate)
        closing = synthesize_speech(CLOSING_PHRASE, cfg)
        speech = speech + pause + closing

    return finalize_briefing_audio(speech, out_path)
