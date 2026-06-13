"""Rotina do briefing diário em áudio.

Módulos:
- ``config``: caminhos e segredos (inclui a pasta de prints).
- ``ocr``: leitura (OCR/visão) dos prints e classificação.
- ``build``: montagem do texto do briefing.
- ``audio``: síntese de voz + frase de encerramento + 5s de silêncio final.
- ``telegram``: envio do áudio (silêncio incluído).
"""

from .config import Config
from .audio import CLOSING_PHRASE, TRAILING_SILENCE_MS

__all__ = ["Config", "CLOSING_PHRASE", "TRAILING_SILENCE_MS"]
