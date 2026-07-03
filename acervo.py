#!/usr/bin/env python3
"""Acervo estratégico — catálogo pesquisável de apresentações e documentos.

Este módulo é o coração do "acervo": um único **catálogo** (``catalogo.json``)
que registra cada documento **final** (``vFINAL``) do Itiel — data, unidade,
título, um resumo do **assunto** e os arquivos (.pptx/.pdf) com seus links.

Ele existe para funcionar nas **duas superfícies**:

- **Web (Claude Code)**: os binários são enviados para a pasta
  ``Acervo Estratégico`` no Google Drive (ver ``GDRIVE_ACERVO_ID``) e o
  catálogo é atualizado/registrado ali também. O upload em si é feito pelo
  conector do Google Drive; este módulo cuida do **catálogo** e do **padrão**.
- **Local (Cowork / Desktop)**: o comando ``arquivar`` finaliza o ``.pptx``
  (gera ``vFINAL`` .pptx + .pdf), **copia** para a pasta estratégica do Mac e
  registra no mesmo catálogo.

Como só guardamos a ``vFINAL`` (decisão do Itiel), cada documento aparece
**uma vez** no catálogo, identificado por (unidade + título). Refinalizar um
documento **atualiza** a entrada, não cria outra.

Uso rápido:

    python acervo.py buscar "obras"                 # pesquisa por assunto/título
    python acervo.py listar                         # lista o acervo
    python acervo.py registrar "2026.06.10 - MULTI - Gestão Tática de Obras vFINAL.pptx" \
        --assunto "Cadência tática de obras: marcos, riscos e recuperação." \
        --palavras obras,tática,cronograma
    python acervo.py arquivar "2026.06.10 - MULTI - Gestão Tática de Obras v11.pptx" \
        --pasta "/caminho/da/pasta estratégica" \
        --assunto "..." --palavras obras,tática
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import unicodedata
from pathlib import Path

from gestao_arquivos import FINAL, Nome, finalizar, parse_nome
from resumo_iphone import gerar_resumo_iphone

# ID da pasta "Acervo Estratégico" no Google Drive do Itiel (destino no modo web).
GDRIVE_ACERVO_ID = "1HF2J6sMMGGY1nvDUEaJH4ypeq0J1ftIs"

# Pasta estratégica no Mac (destino no modo local). Ver CLAUDE.md.
PASTA_ESTRATEGICA_LOCAL = (
    "/Users/itielgoncalves/Documentos Local/c. ARQUIVOS PRINCIPAIS/"
    "Coorporativo/000 - Reunião Diretoria, gerencias e eq. de gestão"
)

# Catálogo versionado junto ao repo; também espelhado no Drive.
CATALOGO_PADRAO = Path(__file__).resolve().parent / "acervo" / "catalogo.json"

SCHEMA_VERSAO = 1

# Pesos por campo na busca (quanto maior, mais relevante o casamento).
_PESOS = {"titulo": 5, "palavras_chave": 4, "unidade": 3, "assunto": 2, "data": 1}


def _dobrar_acento(texto: str) -> str:
    """Minúsculas sem acento, para busca tolerante ('tática' casa 'tatica')."""
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sem_acento.casefold()


def _slug(texto: str) -> str:
    """Identificador estável a partir de texto livre."""
    base = _dobrar_acento(texto)
    return "-".join("".join(c if c.isalnum() else " " for c in base).split())


def chave_documento(unidade: str, titulo: str) -> str:
    """Identidade de um documento no acervo (independe de data e versão)."""
    return _slug(f"{unidade}-{titulo}")


# --------------------------------------------------------------------------- #
# Catálogo: carregar / salvar / registrar / buscar
# --------------------------------------------------------------------------- #

def catalogo_vazio() -> dict:
    return {
        "schema_versao": SCHEMA_VERSAO,
        "acervo": {
            "google_drive_pasta": "Acervo Estratégico",
            "google_drive_id": GDRIVE_ACERVO_ID,
            "pasta_local": PASTA_ESTRATEGICA_LOCAL,
        },
        "documentos": [],
    }


def carregar_catalogo(caminho: Path = CATALOGO_PADRAO) -> dict:
    if not caminho.exists():
        return catalogo_vazio()
    with caminho.open(encoding="utf-8") as fh:
        return json.load(fh)


def salvar_catalogo(catalogo: dict, caminho: Path = CATALOGO_PADRAO) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8") as fh:
        json.dump(catalogo, fh, ensure_ascii=False, indent=2, sort_keys=False)
        fh.write("\n")


def registrar(
    catalogo: dict,
    *,
    data: str,
    unidade: str,
    titulo: str,
    assunto: str = "",
    palavras_chave: list[str] | None = None,
    arquivos: dict | None = None,
    origem: str = "",
) -> dict:
    """Insere ou **atualiza** (upsert) o documento no catálogo.

    A identidade é (unidade + título); refinalizar atualiza a mesma entrada,
    mantendo o acervo com **uma** vFINAL por documento.
    """
    chave = chave_documento(unidade, titulo)
    entrada = {
        "id": chave,
        "data": data,
        "unidade": unidade.upper(),
        "titulo": titulo,
        "versao": "FINAL",
        "assunto": assunto,
        "palavras_chave": palavras_chave or [],
        "arquivos": arquivos or {},
        "origem": origem,
    }

    documentos = catalogo.setdefault("documentos", [])
    for i, doc in enumerate(documentos):
        if doc.get("id") == chave:
            # preserva campos previamente preenchidos se o novo vier vazio
            entrada["assunto"] = assunto or doc.get("assunto", "")
            entrada["palavras_chave"] = palavras_chave or doc.get("palavras_chave", [])
            entrada["arquivos"] = arquivos or doc.get("arquivos", {})
            documentos[i] = entrada
            break
    else:
        documentos.append(entrada)

    documentos.sort(key=lambda d: (d.get("data", ""), d.get("id", "")))
    return entrada


def _pontuar(doc: dict, termos: list[str]) -> int:
    campos = {
        "titulo": doc.get("titulo", ""),
        "palavras_chave": " ".join(doc.get("palavras_chave", [])),
        "unidade": doc.get("unidade", ""),
        "assunto": doc.get("assunto", ""),
        "data": doc.get("data", ""),
    }
    normalizados = {k: _dobrar_acento(v) for k, v in campos.items()}
    score = 0
    for termo in termos:
        for campo, peso in _PESOS.items():
            if termo in normalizados[campo]:
                score += peso
    return score


def buscar(catalogo: dict, consulta: str) -> list[dict]:
    """Documentos que casam com a consulta, do mais relevante ao menos.

    Casa por **assunto**, título, palavras-chave, unidade e data — tolerante a
    acento e maiúsculas. Retorna cada doc com um campo extra ``_score``.
    """
    termos = [t for t in _dobrar_acento(consulta).split() if t]
    if not termos:
        return []
    resultados = []
    for doc in catalogo.get("documentos", []):
        score = _pontuar(doc, termos)
        if score > 0:
            resultados.append({**doc, "_score": score})
    # ordena por score desc; empate pela data mais recente primeiro
    resultados.sort(key=lambda d: (-d["_score"], _neg_data(d.get("data", ""))))
    return resultados


def _neg_data(data: str) -> str:
    """Chave para ordenar datas em ordem decrescente como string."""
    # inverte cada dígito para que a ordenação ascendente vire descendente
    return "".join(str(9 - int(c)) if c.isdigit() else c for c in data)


# --------------------------------------------------------------------------- #
# Modo local: arquivar (finalizar + copiar para a pasta + registrar)
# --------------------------------------------------------------------------- #

def nome_resumo_iphone(pptx_final: Path) -> str:
    """Nome do PNG-resumo a partir do .pptx final, no padrão do Itiel."""
    return f"{pptx_final.stem} (resumo iPhone).png"


def arquivar_local(
    pptx: Path,
    pasta_acervo: Path,
    *,
    assunto: str = "",
    palavras_chave: list[str] | None = None,
    resumo_bullets: list[str] | None = None,
    resumo_destaque: str | None = None,
    resumo_destaque_rotulo: str | None = None,
    catalogo_path: Path = CATALOGO_PADRAO,
    gerar_pdf_tambem: bool = True,
) -> dict:
    """Finaliza um .pptx, copia a vFINAL para a pasta do acervo e registra.

    Pensado para superfície **local** (acesso ao disco). Sempre mantém no
    acervo a final em **.pptx e .pdf**; se ``resumo_bullets`` for informado,
    também gera a **imagem-resumo (iPhone)** para o sr. José. Retorna a
    entrada registrada no catálogo.
    """
    if not pasta_acervo.is_dir():
        raise FileNotFoundError(f"Pasta do acervo não encontrada: {pasta_acervo}")

    gerados = finalizar(pptx, gerar_pdf_tambem=gerar_pdf_tambem)

    nome: Nome | None = parse_nome(gerados[0].name)
    if nome is None:
        raise ValueError(
            f"Arquivo final fora do padrão, não dá para catalogar: {gerados[0].name}"
        )

    arquivos: dict = {}
    pptx_final = gerados[0]
    for origem in gerados:
        destino = pasta_acervo / origem.name
        if destino.resolve() != origem.resolve():
            shutil.copy2(origem, destino)
        arquivos[origem.suffix.lstrip(".").lower()] = {
            "nome": destino.name,
            "caminho_local": str(destino),
        }

    if resumo_bullets:
        png_destino = pasta_acervo / nome_resumo_iphone(pptx_final)
        gerar_resumo_iphone(
            titulo=nome.titulo,
            unidade=nome.unidade,
            data=nome.data,
            bullets=resumo_bullets,
            out=png_destino,
            destaque=resumo_destaque,
            destaque_rotulo=resumo_destaque_rotulo,
        )
        arquivos["imagem_resumo"] = {
            "nome": png_destino.name,
            "caminho_local": str(png_destino),
        }

    catalogo = carregar_catalogo(catalogo_path)
    entrada = registrar(
        catalogo,
        data=nome.data,
        unidade=nome.unidade,
        titulo=nome.titulo,
        assunto=assunto,
        palavras_chave=palavras_chave,
        arquivos=arquivos,
        origem="local",
    )
    salvar_catalogo(catalogo, catalogo_path)
    return entrada


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _lista_palavras(valor: str | None) -> list[str]:
    if not valor:
        return []
    return [p.strip() for p in valor.split(",") if p.strip()]


def _fmt_doc(doc: dict) -> str:
    linha = f"{doc.get('data','?')} - {doc.get('unidade','?')} - {doc.get('titulo','?')} [vFINAL]"
    if doc.get("assunto"):
        linha += f"\n    assunto: {doc['assunto']}"
    arquivos = doc.get("arquivos", {})
    for ext, info in arquivos.items():
        alvo = info.get("drive_url") or info.get("caminho_local") or info.get("nome", "")
        linha += f"\n    {ext}: {alvo}"
    return linha


def _cmd_buscar(args: argparse.Namespace) -> int:
    catalogo = carregar_catalogo(Path(args.catalogo))
    achados = buscar(catalogo, args.consulta)
    if not achados:
        print(f"Nada encontrado para: {args.consulta!r}")
        return 0
    print(f"{len(achados)} resultado(s) para {args.consulta!r}:\n")
    for doc in achados:
        print(_fmt_doc(doc))
        print()
    return 0


def _cmd_listar(args: argparse.Namespace) -> int:
    catalogo = carregar_catalogo(Path(args.catalogo))
    docs = catalogo.get("documentos", [])
    if not docs:
        print("Acervo vazio.")
        return 0
    print(f"{len(docs)} documento(s) no acervo:\n")
    for doc in docs:
        print(_fmt_doc(doc))
        print()
    return 0


def _cmd_registrar(args: argparse.Namespace) -> int:
    nome = parse_nome(args.arquivo)
    if nome is None:
        print(f"Nome fora do padrão: {args.arquivo}", file=sys.stderr)
        return 2
    catalogo = carregar_catalogo(Path(args.catalogo))
    registrar(
        catalogo,
        data=nome.data,
        unidade=nome.unidade,
        titulo=nome.titulo,
        assunto=args.assunto or "",
        palavras_chave=_lista_palavras(args.palavras),
        origem=args.origem or "",
    )
    salvar_catalogo(catalogo, Path(args.catalogo))
    print(f"Registrado: {nome.data} - {nome.unidade} - {nome.titulo}")
    return 0


def _cmd_arquivar(args: argparse.Namespace) -> int:
    try:
        entrada = arquivar_local(
            Path(args.pptx),
            Path(args.pasta),
            assunto=args.assunto or "",
            palavras_chave=_lista_palavras(args.palavras),
            resumo_bullets=[b.strip() for b in (args.resumo or []) if b.strip()],
            resumo_destaque=args.destaque,
            resumo_destaque_rotulo=args.destaque_rotulo,
            catalogo_path=Path(args.catalogo),
            gerar_pdf_tambem=not args.no_pdf,
        )
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1
    print("Arquivado no acervo:")
    print(_fmt_doc(entrada))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--catalogo", default=str(CATALOGO_PADRAO), help="caminho do catalogo.json"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_busca = sub.add_parser("buscar", help="pesquisar por assunto/título/unidade")
    p_busca.add_argument("consulta", help="termo(s) de busca")
    p_busca.set_defaults(func=_cmd_buscar)

    p_listar = sub.add_parser("listar", help="listar o acervo")
    p_listar.set_defaults(func=_cmd_listar)

    p_reg = sub.add_parser("registrar", help="registrar um documento no catálogo")
    p_reg.add_argument("arquivo", help="nome no padrão AAAA.MM.DD - UNIDADE - Título vFINAL.ext")
    p_reg.add_argument("--assunto", help="resumo do que o documento trata")
    p_reg.add_argument("--palavras", help="palavras-chave separadas por vírgula")
    p_reg.add_argument("--origem", help="web ou local")
    p_reg.set_defaults(func=_cmd_registrar)

    p_arq = sub.add_parser(
        "arquivar", help="[local] finalizar .pptx, copiar p/ a pasta e registrar"
    )
    p_arq.add_argument("pptx", help="arquivo .pptx de origem")
    p_arq.add_argument(
        "--pasta", default=PASTA_ESTRATEGICA_LOCAL, help="pasta do acervo (Mac)"
    )
    p_arq.add_argument("--assunto", help="resumo do que o documento trata")
    p_arq.add_argument("--palavras", help="palavras-chave separadas por vírgula")
    p_arq.add_argument(
        "--resumo", action="append", metavar="BULLET",
        help="bullet do resumo iPhone p/ o sr. José (repita a flag por bullet)",
    )
    p_arq.add_argument("--destaque", help="número/linha de destaque no resumo (ex.: '+12%')")
    p_arq.add_argument("--destaque-rotulo", dest="destaque_rotulo",
                       help="legenda do destaque")
    p_arq.add_argument("--no-pdf", action="store_true", help="não gerar o PDF")
    p_arq.set_defaults(func=_cmd_arquivar)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
