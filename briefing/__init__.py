"""Rotina do briefing diário em áudio.

Módulos:
- ``config``: caminhos e segredos (inclui a pasta de prints).
- ``ocr``: leitura (OCR/visão) dos prints e classificação.
- ``build``: montagem do texto do briefing.
- ``audio``: síntese de voz + frase de encerramento + 5s de silêncio final.
- ``telegram``: envio do áudio (silêncio incluído).
- ``automia``: conector autenticado (OAuth2) para o API Hub da Automia.
"""

from .config import Config
from .audio import CLOSING_PHRASE, TRAILING_SILENCE_MS
from .automia import AutomiaClient

__all__ = ["Config", "CLOSING_PHRASE", "TRAILING_SILENCE_MS", "AutomiaClient"]
