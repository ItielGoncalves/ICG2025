"""Envio do áudio do briefing pelo Telegram.

Usa ``sendAudio``, que envia o arquivo exatamente como foi exportado — ou seja,
o silêncio final de 5 segundos vai junto, sem corte na entrega.
"""

from __future__ import annotations

from pathlib import Path

import requests

_API = "https://api.telegram.org/bot{token}/sendAudio"


def send_audio(cfg, audio_path: str | Path, caption: str | None = None) -> dict:
    """Envia o arquivo de áudio para o chat configurado e devolve a resposta da API."""
    if not cfg.telegram_configured:
        raise RuntimeError(
            "Telegram não configurado: defina TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID."
        )

    audio_path = Path(audio_path)
    url = _API.format(token=cfg.telegram_bot_token)

    last_exc: Exception | None = None
    for attempt in range(4):  # pequenas retentativas para falhas de rede
        try:
            with audio_path.open("rb") as fh:
                files = {"audio": (audio_path.name, fh, "audio/mpeg")}
                data = {"chat_id": cfg.telegram_chat_id}
                if caption:
                    data["caption"] = caption[:1024]
                resp = requests.post(url, data=data, files=files, timeout=120)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:  # rede instável
            last_exc = exc
            import time

            time.sleep(2 ** attempt)
    raise RuntimeError(f"Falha ao enviar áudio ao Telegram: {last_exc}")
