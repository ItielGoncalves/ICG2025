"""Testes do acervo: registro (upsert) e busca por assunto/título.

Hermeticos: usam um catálogo em memória / tmp_path, não tocam Drive nem disco
real do acervo, nem dependem do LibreOffice.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from acervo import (  # noqa: E402
    buscar,
    carregar_catalogo,
    catalogo_vazio,
    chave_documento,
    registrar,
    salvar_catalogo,
)


def _cat_exemplo() -> dict:
    cat = catalogo_vazio()
    registrar(
        cat,
        data="2026.06.10",
        unidade="MULTI",
        titulo="Gestão Tática de Obras",
        assunto="Cadência tática de obras: marcos, riscos e recuperação de atrasos.",
        palavras_chave=["obras", "cronograma", "atrasos"],
        origem="local",
    )
    registrar(
        cat,
        data="2026.06.15",
        unidade="RVD",
        titulo="Segurança e Câmeras",
        assunto="Plano de câmeras e segurança patrimonial em Rio Verde.",
        palavras_chave=["segurança", "câmeras", "patrimônio"],
        origem="web",
    )
    return cat


def test_registrar_insere():
    cat = catalogo_vazio()
    registrar(cat, data="2026.06.10", unidade="MULTI", titulo="Obras")
    assert len(cat["documentos"]) == 1
    assert cat["documentos"][0]["versao"] == "FINAL"
    assert cat["documentos"][0]["unidade"] == "MULTI"


def test_registrar_faz_upsert_por_documento():
    # Mesma unidade+título com nova data => atualiza, não duplica.
    cat = catalogo_vazio()
    registrar(cat, data="2026.06.10", unidade="MULTI", titulo="Gestão Tática de Obras")
    registrar(cat, data="2026.06.20", unidade="MULTI", titulo="gestão tática de obras")
    assert len(cat["documentos"]) == 1
    assert cat["documentos"][0]["data"] == "2026.06.20"


def test_registrar_preserva_assunto_quando_novo_vem_vazio():
    cat = catalogo_vazio()
    registrar(
        cat,
        data="2026.06.10",
        unidade="MULTI",
        titulo="Obras",
        assunto="resumo importante",
        palavras_chave=["obras"],
    )
    # refinaliza sem reinformar o assunto: deve preservar o anterior.
    registrar(cat, data="2026.06.20", unidade="MULTI", titulo="Obras")
    doc = cat["documentos"][0]
    assert doc["assunto"] == "resumo importante"
    assert doc["palavras_chave"] == ["obras"]


def test_chave_documento_tolera_acento_e_caixa():
    assert chave_documento("MULTI", "Gestão Tática") == chave_documento(
        "multi", "gestao tatica"
    )


def test_buscar_por_assunto_tolerante_a_acento():
    cat = _cat_exemplo()
    # 'cameras' (sem acento) casa 'câmeras'
    achados = buscar(cat, "cameras")
    assert len(achados) == 1
    assert achados[0]["unidade"] == "RVD"


def test_buscar_por_titulo_ranqueia_acima():
    cat = _cat_exemplo()
    achados = buscar(cat, "obras")
    assert achados[0]["titulo"] == "Gestão Tática de Obras"
    assert achados[0]["_score"] > 0


def test_buscar_sem_resultado():
    cat = _cat_exemplo()
    assert buscar(cat, "xpto inexistente") == []


def test_buscar_consulta_vazia():
    cat = _cat_exemplo()
    assert buscar(cat, "   ") == []


def test_salvar_e_carregar_roundtrip(tmp_path):
    cat = _cat_exemplo()
    caminho = tmp_path / "catalogo.json"
    salvar_catalogo(cat, caminho)
    recarregado = carregar_catalogo(caminho)
    assert recarregado["documentos"] == cat["documentos"]
    assert recarregado["schema_versao"] == 1
