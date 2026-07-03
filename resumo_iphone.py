#!/usr/bin/env python3
"""Resumo super objetivo em imagem (formato iPhone) para encaminhar ao sr. José.

O Itiel quase sempre encaminha o material ao sr. José, que abre no **iPhone**.
Então, ao finalizar um documento, além do ``.pptx`` e do ``.pdf``, geramos uma
**imagem vertical** (retrato, alto contraste, tipografia grande) com o resumo
super objetivo — de bater o olho no celular e entender.

Duas etapas:

1. ``montar_html`` — monta um cartão HTML autocontido (retrato 4:5), a partir de
   título, unidade, data, alguns bullets e um destaque opcional. Função pura,
   fácil de testar.
2. ``renderizar_png`` — rasteriza o HTML em PNG. Tenta o **Playwright/Chromium**
   (disponível no Claude Code web) e, se não houver, cai para o **Chrome/Chromium
   headless** por linha de comando (o caminho comum no Mac do Itiel).

O nome do arquivo segue o padrão, com o sufixo ``(resumo iPhone)``:

    AAAA.MM.DD - UNIDADE - Título vFINAL (resumo iPhone).png
"""

from __future__ import annotations

import html as _html
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

# Retrato 4:5 — lê muito bem como imagem de mensagem no iPhone.
LARGURA = 1080
ALTURA = 1350

_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: {LARGURA}px; height: {ALTURA}px; }
body {
  font-family: -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  background: #ffffff;
  color: #14211b;
  padding: 84px 76px;
  display: flex;
  flex-direction: column;
}
.topo { display: flex; align-items: center; gap: 20px; margin-bottom: 44px; }
.chip {
  background: #1b5e3f; color: #fff; font-weight: 700; font-size: 30px;
  letter-spacing: 1px; padding: 12px 24px; border-radius: 999px;
}
.data { color: #5b6b63; font-size: 30px; font-weight: 600; }
.titulo {
  font-size: 68px; line-height: 1.08; font-weight: 800; letter-spacing: -1px;
  margin-bottom: 40px;
}
.destaque {
  background: #eef6f1; border-left: 12px solid #1b5e3f; border-radius: 14px;
  padding: 32px 36px; margin-bottom: 44px;
}
.destaque .num { font-size: 82px; font-weight: 800; color: #1b5e3f; line-height: 1; }
.destaque .rot { font-size: 32px; color: #3c4a43; margin-top: 10px; font-weight: 600; }
ul { list-style: none; display: flex; flex-direction: column; gap: 30px; }
li { display: flex; gap: 22px; font-size: 40px; line-height: 1.28; }
li::before {
  content: ''; flex: none; width: 20px; height: 20px; margin-top: 16px;
  background: #1b5e3f; border-radius: 6px;
}
.rodape {
  margin-top: auto; padding-top: 40px; border-top: 2px solid #e2eae5;
  color: #5b6b63; font-size: 28px; display: flex; justify-content: space-between;
}
.rodape b { color: #1b5e3f; }
""".replace("{LARGURA}", str(LARGURA)).replace("{ALTURA}", str(ALTURA))


def montar_html(
    *,
    titulo: str,
    unidade: str,
    data: str,
    bullets: list[str],
    destaque: str | None = None,
    destaque_rotulo: str | None = None,
    rodape: str = "Resumo executivo",
) -> str:
    """Monta o HTML autocontido do cartão-resumo (retrato iPhone).

    ``bullets`` deve ser curto e objetivo (recomendado 3 a 5 itens). ``destaque``
    é um número/linha de impacto opcional (ex.: "R$ 1,2 mi"); ``destaque_rotulo``
    é a legenda embaixo dele.
    """
    def esc(t: str) -> str:
        return _html.escape(t, quote=True)

    itens = "".join(f"<li>{esc(b)}</li>" for b in bullets if b.strip())

    bloco_destaque = ""
    if destaque:
        rot = f'<div class="rot">{esc(destaque_rotulo)}</div>' if destaque_rotulo else ""
        bloco_destaque = (
            f'<div class="destaque"><div class="num">{esc(destaque)}</div>{rot}</div>'
        )

    return (
        "<!doctype html><html lang='pt-br'><head><meta charset='utf-8'>"
        f"<style>{_CSS}</style></head><body>"
        f"<div class='topo'><span class='chip'>{esc(unidade)}</span>"
        f"<span class='data'>{esc(data)}</span></div>"
        f"<div class='titulo'>{esc(titulo)}</div>"
        f"{bloco_destaque}"
        f"<ul>{itens}</ul>"
        f"<div class='rodape'><span>{esc(rodape)}</span><span><b>INPASA</b></span></div>"
        "</body></html>"
    )


def _chrome_bin() -> str | None:
    if os.environ.get("CHROME_BIN"):
        return os.environ["CHROME_BIN"]
    candidatos = [
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/opt/pw-browsers/chromium",
    ]
    for c in candidatos:
        if shutil.which(c) or Path(c).exists():
            return c
    return None


def _render_playwright(html: str, out: Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return False
    try:
        with sync_playwright() as p:
            navegador = p.chromium.launch()
            pagina = navegador.new_page(viewport={"width": LARGURA, "height": ALTURA})
            pagina.set_content(html, wait_until="networkidle")
            pagina.screenshot(path=str(out))
            navegador.close()
        return out.exists()
    except Exception:
        return False


def _render_chrome_cli(html: str, out: Path) -> bool:
    binario = _chrome_bin()
    if not binario:
        return False
    with tempfile.TemporaryDirectory() as td:
        html_path = Path(td) / "card.html"
        html_path.write_text(html, encoding="utf-8")
        cmd = [
            binario,
            "--headless=new",
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={LARGURA},{ALTURA}",
            f"--screenshot={out}",
            html_path.as_uri(),
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, timeout=120)
        except (subprocess.CalledProcessError, subprocess.TimeoutError, OSError):
            # tenta o headless antigo, para Chromes mais velhos
            cmd[1] = "--headless"
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, timeout=120)
            except (subprocess.CalledProcessError, subprocess.TimeoutError, OSError):
                return False
        return out.exists()


def renderizar_png(html: str, out: Path) -> Path:
    """Rasteriza o HTML em PNG. Tenta Playwright e depois Chrome headless."""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if _render_playwright(html, out) or _render_chrome_cli(html, out):
        return out
    raise RuntimeError(
        "Não consegui rasterizar o resumo em PNG: nem Playwright nem Chrome/"
        "Chromium headless disponíveis. Instale o Google Chrome ou defina "
        "CHROME_BIN."
    )


def gerar_resumo_iphone(
    *,
    titulo: str,
    unidade: str,
    data: str,
    bullets: list[str],
    out: Path,
    destaque: str | None = None,
    destaque_rotulo: str | None = None,
) -> Path:
    """Atalho: monta o HTML e rasteriza o PNG do resumo para o sr. José."""
    html = montar_html(
        titulo=titulo,
        unidade=unidade,
        data=data,
        bullets=bullets,
        destaque=destaque,
        destaque_rotulo=destaque_rotulo,
    )
    return renderizar_png(html, out)
