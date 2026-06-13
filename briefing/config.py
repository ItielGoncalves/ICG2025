"""Configuração central da rotina de briefing diário.

Todos os caminhos e segredos vêm de variáveis de ambiente, com defaults
sensatos. O caminho da pasta de prints é o ponto mais importante: por padrão
fica em ``<repo>/prints`` e pode ser sobrescrito com ``BRIEFING_PRINTS_DIR``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

# Raiz do repositório (este arquivo fica em <repo>/briefing/config.py)
REPO_ROOT = Path(__file__).resolve().parent.parent

# Pasta padrão onde ficam salvos os prints de e-mail, agenda e WhatsApp.
DEFAULT_PRINTS_DIR = REPO_ROOT / "prints"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"


def _env_path(var: str, default: Path) -> Path:
    value = os.getenv(var)
    return Path(value).expanduser() if value else default


@dataclass
class Config:
    """Parâmetros de execução da rotina."""

    # --- Pasta de prints/capturas -------------------------------------------
    prints_dir: Path = field(default_factory=lambda: _env_path("BRIEFING_PRINTS_DIR", DEFAULT_PRINTS_DIR))

    # --- OCR / visão (Anthropic) --------------------------------------------
    anthropic_api_key: str | None = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    anthropic_model: str = field(default_factory=lambda: os.getenv("BRIEFING_MODEL", "claude-opus-4-8"))

    # --- Síntese de voz (TTS) -----------------------------------------------
    tts_lang: str = field(default_factory=lambda: os.getenv("BRIEFING_TTS_LANG", "pt"))
    tts_tld: str = field(default_factory=lambda: os.getenv("BRIEFING_TTS_TLD", "com.br"))

    # --- Telegram ------------------------------------------------------------
    telegram_bot_token: str | None = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN"))
    telegram_chat_id: str | None = field(default_factory=lambda: os.getenv("TELEGRAM_CHAT_ID"))

    # --- Saída ---------------------------------------------------------------
    output_dir: Path = field(default_factory=lambda: _env_path("BRIEFING_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))

    def ensure_dirs(self) -> None:
        self.prints_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def telegram_configured(self) -> bool:
        return bool(self.telegram_bot_token and self.telegram_chat_id)
