"""Testes da lógica de nomenclatura e poda de versões.

Hermeticos: não tocam disco nem dependem do LibreOffice. Exercitam o parsing
do padrão "AAAA.MM.DD - UNIDADE - Título [vN].ext" e a seleção distribuída de
versões a manter.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gestao_arquivos import (  # noqa: E402
    FINAL,
    parse_nome,
    planejar_poda,
    selecionar_para_manter,
)


def test_parse_nome_com_versao():
    n = parse_nome("2026.06.10 - MULTI - Gestão Tática de Obras v11.pptx")
    assert n is not None
    assert n.data == "2026.06.10"
    assert n.unidade == "MULTI"
    assert n.titulo == "Gestão Tática de Obras"
    assert n.versao == 11
    assert n.ext == ".pptx"


def test_parse_nome_vfinal():
    n = parse_nome("2026.06.06 - DRD - Report Estratégico Semanal vFINAL.pdf")
    assert n is not None
    assert n.versao == FINAL
    assert n.unidade == "DRD"


def test_parse_nome_sem_versao():
    n = parse_nome("2026.03.16 - SNP - Estudo Headcount Manutenção.pptx")
    assert n is not None
    assert n.versao is None
    assert n.titulo == "Estudo Headcount Manutenção"


def test_parse_nome_fora_do_padrao():
    assert parse_nome("qualquer coisa.pptx") is None
    assert parse_nome("APR_MULTI_GERAL_X_2026-06-06_v01.pdf") is None


def test_formatar_roundtrip():
    original = "2026.06.19 - DRD - Plano de Ações Supervisório v01.pptx"
    assert parse_nome(original).formatar() == original


def test_selecionar_mantem_tudo_quando_poucas():
    assert selecionar_para_manter([1, 2, 3]) == {1, 2, 3}
    assert selecionar_para_manter([4]) == {4}


def test_selecionar_distribuido_1_a_30():
    # Exemplo do Itiel: 30 versões -> manter v10, v20, v30.
    assert selecionar_para_manter(list(range(1, 31))) == {10, 20, 30}


def test_selecionar_sempre_inclui_a_mais_recente():
    escolhidos = selecionar_para_manter([1, 2, 3, 4, 5, 6, 7])
    assert 7 in escolhidos
    assert len(escolhidos) == 3


def test_planejar_poda_agrupa_por_documento(tmp_path):
    nomes = [
        "2026.06.01 - MULTI - Correias Antichama v01.pptx",
        "2026.06.02 - MULTI - Correias Antichama v02.pptx",
        "2026.06.03 - MULTI - Correias Antichama v03.pptx",
        "2026.06.04 - MULTI - Correias Antichama v04.pptx",
        "2026.06.10 - MULTI - Correias Antichama vFINAL.pptx",  # nunca poda
        "2026.06.01 - DRD - Outro Documento v01.pptx",  # grupo separado
    ]
    arquivos = []
    for nome in nomes:
        p = tmp_path / nome
        p.write_text("x")
        arquivos.append(p)

    remover = planejar_poda(arquivos)
    nomes_removidos = {p.name for p in remover}

    # 4 versões numeradas -> mantém 3, remove 1; vFINAL e o grupo DRD ficam.
    assert len(nomes_removidos) == 1
    assert "2026.06.10 - MULTI - Correias Antichama vFINAL.pptx" not in nomes_removidos
    assert "2026.06.01 - DRD - Outro Documento v01.pptx" not in nomes_removidos
