#!/usr/bin/env python3
"""Entrypoint da rotina do briefing diário.

Fluxo:
1. Lê os prints da pasta configurada (OCR/visão) e classifica em e-mail,
   agenda e WhatsApp, destacando o que exige ação.
2. Monta o texto do briefing (prints + conteúdo já vindo de ClickUp/atas/
   anotações, passado via ``--base``).
3. Gera o áudio terminando com "E por aqui é isso por hoje." + 5s de silêncio.
4. Envia o áudio pelo Telegram (silêncio incluído), se as credenciais existirem.

Exemplos:
    python run_briefing.py                 # roda o briefing do dia
    python run_briefing.py --base hoje.txt # injeta o conteúdo das outras fontes
    python run_briefing.py --no-telegram   # gera o áudio mas não envia
    python run_briefing.py --test          # teste rápido sem ler prints
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

from briefing.config import Config
from briefing import audio as audio_mod
from briefing import build as build_mod
from briefing import ocr as ocr_mod
from briefing import telegram as telegram_mod


def _today_stamp() -> str:
    return dt.date.today().isoformat()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gera e envia o briefing diário em áudio.")
    parser.add_argument("--base", type=Path, help="Arquivo com o conteúdo das demais fontes (ClickUp/atas/anotações).")
    parser.add_argument("--no-telegram", action="store_true", help="Não envia pelo Telegram.")
    parser.add_argument("--test", action="store_true", help="Teste rápido: não lê prints, usa um texto curto.")
    parser.add_argument("--out", type=Path, help="Caminho do arquivo de áudio de saída (.mp3).")
    args = parser.parse_args(argv)

    cfg = Config()
    cfg.ensure_dirs()

    print(f"Pasta de prints configurada: {cfg.prints_dir}")

    base_text = None
    if args.base:
        base_text = args.base.read_text(encoding="utf-8")

    if args.test:
        items = []
        base_text = base_text or "Este é um teste da rotina de briefing."
        print("Modo teste: pulando a leitura dos prints.")
    else:
        images = ocr_mod.list_print_images(cfg)
        print(f"Prints encontrados: {len(images)}")
        items = ocr_mod.extract_items(cfg)
        print(f"Itens extraídos dos prints: {len(items)}")

    text = build_mod.build_briefing_text(items, base_sections=base_text)
    print("\n----- TEXTO DO BRIEFING -----")
    print(text)
    print("----- FIM DO TEXTO -----\n")

    out_path = args.out or (cfg.output_dir / f"briefing-{_today_stamp()}.mp3")
    result = audio_mod.build_audio_from_text(text, out_path, cfg)
    print(
        f"Áudio gerado: {result.path}\n"
        f"  duração total: {result.total_ms/1000:.1f}s "
        f"(fala {result.speech_ms/1000:.1f}s + {result.trailing_silence_ms/1000:.0f}s de silêncio)\n"
        f"  silêncio final confirmado: {'sim' if result.tail_is_silent else 'NÃO'}"
    )
    if not result.tail_is_silent:
        print("AVISO: o silêncio final não foi confirmado na exportação.", file=sys.stderr)

    if args.no_telegram:
        print("Envio pelo Telegram pulado (--no-telegram).")
    elif cfg.telegram_configured:
        telegram_mod.send_audio(cfg, result.path, caption=f"Briefing diário — {_today_stamp()}")
        print("Áudio enviado pelo Telegram.")
    else:
        print("Telegram não configurado (TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID); envio pulado.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
