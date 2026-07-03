"""Testes do cartão-resumo (iPhone). Só a parte pura: montagem do HTML.

Não rasteriza PNG (isso depende de navegador) — apenas garante que o HTML
sai bem-formado, com escape, e contém os campos essenciais.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from resumo_iphone import montar_html  # noqa: E402


def test_html_contem_campos_essenciais():
    html = montar_html(
        titulo="Gestão Tática de Obras",
        unidade="MULTI",
        data="2026.06.10",
        bullets=["Marco A recuperado", "Risco B em aberto"],
    )
    assert "Gestão Tática de Obras" in html
    assert "MULTI" in html
    assert "2026.06.10" in html
    assert "Marco A recuperado" in html
    assert "Risco B em aberto" in html
    assert html.lstrip().startswith("<!doctype html>")


def test_html_escapa_conteudo():
    html = montar_html(
        titulo="Obras <A&B>",
        unidade="MULTI",
        data="2026.06.10",
        bullets=["item com <tag> & 'aspas'"],
    )
    assert "<A&B>" not in html
    assert "&lt;A&amp;B&gt;" in html
    assert "&lt;tag&gt;" in html


def test_html_destaque_opcional():
    sem = montar_html(titulo="T", unidade="U", data="D", bullets=["b"])
    assert "class='destaque'" not in sem and 'class="destaque"' not in sem

    com = montar_html(
        titulo="T", unidade="U", data="D", bullets=["b"],
        destaque="+12%", destaque_rotulo="avanço",
    )
    assert "+12%" in com
    assert "avanço" in com
    assert "destaque" in com


def test_html_ignora_bullets_vazios():
    html = montar_html(
        titulo="T", unidade="U", data="D",
        bullets=["real", "   ", ""],
    )
    assert html.count("<li>") == 1
