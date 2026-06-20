#!/usr/bin/env python3
"""Helper local para apresentações/documentos no padrão do Itiel.

Padrão de nome (ver CLAUDE.md):

    AAAA.MM.DD - UNIDADE - Título com espaços naturais [vN].ext

Faz duas coisas, pensadas para rodar **numa máquina local** (Cowork / Desktop)
com acesso ao disco:

1. ``finalize``  — dado um .pptx, gera o ``... vFINAL.pptx`` e exporta o
   ``... vFINAL.pdf`` (via LibreOffice headless).
2. ``prune``     — numa pasta, mantém no máximo 3 versões **distribuídas** por
   arquivo (mais a ``vFINAL``) e remove as do meio. É **dry-run por padrão**;
   só apaga de verdade com ``--apply``.

A conversão para PDF precisa do LibreOffice instalado (no Mac:
``brew install --cask libreoffice``). Defina ``LIBREOFFICE_BIN`` para apontar
um binário específico, se necessário.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# Bloco de versão no fim do título: " v01", " v11", " vFINAL" (case-insensitive).
_VERSAO_RE = re.compile(r"\s+v(?:(?P<num>\d+)|(?P<final>final))\s*$", re.IGNORECASE)

# Nome completo: "AAAA.MM.DD - UNIDADE - Título [vN]"
_NOME_RE = re.compile(
    r"^(?P<data>\d{4}\.\d{2}\.\d{2})\s+-\s+(?P<unidade>[^-]+?)\s+-\s+(?P<resto>.+)$"
)

FINAL = "FINAL"  # sentinela para a versão vFINAL


@dataclass
class Nome:
    """Um nome de arquivo decomposto no padrão do Itiel."""

    data: str
    unidade: str
    titulo: str
    versao: object  # int, "FINAL" ou None
    ext: str

    @property
    def chave_base(self) -> tuple[str, str]:
        """Identifica um mesmo documento (independe de data e versão)."""
        return (self.unidade.upper(), self.titulo.casefold())

    def formatar(self) -> str:
        sufixo_versao = ""
        if self.versao == FINAL:
            sufixo_versao = " vFINAL"
        elif isinstance(self.versao, int):
            sufixo_versao = f" v{self.versao:02d}"
        return f"{self.data} - {self.unidade} - {self.titulo}{sufixo_versao}{self.ext}"


def parse_nome(filename: str) -> Nome | None:
    """Decompõe um nome no padrão. Retorna ``None`` se não casar."""
    stem, ext = os.path.splitext(os.path.basename(filename))
    m = _NOME_RE.match(stem)
    if not m:
        return None

    resto = m.group("resto").strip()
    versao: object = None
    mv = _VERSAO_RE.search(resto)
    if mv:
        versao = FINAL if mv.group("final") else int(mv.group("num"))
        resto = resto[: mv.start()].strip()

    return Nome(
        data=m.group("data"),
        unidade=m.group("unidade").strip(),
        titulo=resto,
        versao=versao,
        ext=ext,
    )


def selecionar_para_manter(versoes: list[int], keep: int = 3) -> set[int]:
    """Escolhe quais versões numeradas manter, distribuídas uniformemente.

    Sempre inclui a mais recente. Para a numeração ``1..30`` com ``keep=3`` o
    resultado é ``{10, 20, 30}`` (terços do total), como o Itiel descreveu.
    """
    unicas = sorted(set(versoes))
    if len(unicas) <= keep:
        return set(unicas)

    vmax = unicas[-1]
    alvos = [round(vmax * (i + 1) / keep) for i in range(keep)]
    escolhidos: set[int] = set()
    for alvo in alvos:
        candidatos = [v for v in unicas if v not in escolhidos]
        # mais próximo do alvo; empate vai para a versão maior.
        escolhidos.add(min(candidatos, key=lambda v: (abs(v - alvo), -v)))
    return escolhidos


def planejar_poda(arquivos: list[Path], keep: int = 3) -> dict[Path, str]:
    """Mapeia arquivos -> motivo de remoção. ``vFINAL`` nunca entra.

    Agrupa por documento (unidade + título), e dentro de cada grupo decide
    quais versões numeradas remover. Arquivos fora do padrão são ignorados.
    """
    grupos: dict[tuple[str, str], list[tuple[int, Path]]] = {}
    for arq in arquivos:
        nome = parse_nome(arq.name)
        if nome is None or not isinstance(nome.versao, int):
            continue  # ignora não-padrão e a vFINAL (sempre preservada)
        grupos.setdefault(nome.chave_base, []).append((nome.versao, arq))

    remover: dict[Path, str] = {}
    for itens in grupos.values():
        versoes = [v for v, _ in itens]
        manter = selecionar_para_manter(versoes, keep=keep)
        for versao, arq in itens:
            if versao not in manter:
                remover[arq] = f"v{versao:02d} (poda: mantendo {sorted(manter)})"
    return remover


def _libreoffice_bin() -> str | None:
    if os.environ.get("LIBREOFFICE_BIN"):
        return os.environ["LIBREOFFICE_BIN"]
    candidatos = [
        "soffice",
        "libreoffice",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    ]
    for c in candidatos:
        if shutil.which(c) or Path(c).exists():
            return c
    return None


def gerar_pdf(pptx: Path, outdir: Path | None = None) -> Path:
    """Converte um .pptx em .pdf via LibreOffice headless."""
    binario = _libreoffice_bin()
    if not binario:
        raise RuntimeError(
            "LibreOffice não encontrado. Instale (Mac: 'brew install --cask "
            "libreoffice') ou defina LIBREOFFICE_BIN."
        )
    outdir = outdir or pptx.parent
    subprocess.run(
        [binario, "--headless", "--convert-to", "pdf", "--outdir", str(outdir), str(pptx)],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    pdf = outdir / (pptx.stem + ".pdf")
    if not pdf.exists():
        raise RuntimeError(f"Conversão falhou: {pdf} não foi gerado.")
    return pdf


def finalizar(pptx: Path, gerar_pdf_tambem: bool = True) -> list[Path]:
    """Gera o .pptx e o .pdf marcados como vFINAL, a partir de um .pptx."""
    if pptx.suffix.lower() != ".pptx":
        raise ValueError(f"Esperado um .pptx, recebi: {pptx.name}")

    nome = parse_nome(pptx.name)
    if nome is not None:
        nome.versao = FINAL
        destino_pptx = pptx.with_name(nome.formatar())
    else:
        # Fora do padrão: tira " vNN"/" vFINAL" do fim e acrescenta " vFINAL".
        base = _VERSAO_RE.sub("", pptx.stem).strip()
        destino_pptx = pptx.with_name(f"{base} vFINAL.pptx")

    if destino_pptx.resolve() != pptx.resolve():
        shutil.copy2(pptx, destino_pptx)

    gerados = [destino_pptx]
    if gerar_pdf_tambem:
        gerados.append(gerar_pdf(destino_pptx))
    return gerados


def _cmd_prune(args: argparse.Namespace) -> int:
    pasta = Path(args.pasta)
    if not pasta.is_dir():
        print(f"Pasta não encontrada: {pasta}", file=sys.stderr)
        return 2

    arquivos = sorted(p for p in pasta.iterdir() if p.is_file())
    remover = planejar_poda(arquivos, keep=args.keep)
    if not remover:
        print("Nada a podar — todos os documentos já têm no máximo "
              f"{args.keep} versões.")
        return 0

    acao = "REMOVENDO" if args.apply else "[dry-run] removeria"
    for arq, motivo in sorted(remover.items()):
        print(f"{acao}: {arq.name}  ->  {motivo}")
        if args.apply:
            arq.unlink()

    if not args.apply:
        print("\nNada foi apagado. Rode de novo com --apply para confirmar.")
    return 0


def _cmd_finalize(args: argparse.Namespace) -> int:
    pptx = Path(args.pptx)
    if not pptx.is_file():
        print(f"Arquivo não encontrado: {pptx}", file=sys.stderr)
        return 2
    try:
        gerados = finalizar(pptx, gerar_pdf_tambem=not args.no_pdf)
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1
    for g in gerados:
        print(f"Gerado: {g.name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_prune = sub.add_parser("prune", help="podar versões antigas numa pasta")
    p_prune.add_argument("pasta", help="pasta com os arquivos")
    p_prune.add_argument("--keep", type=int, default=3, help="versões a manter (default: 3)")
    p_prune.add_argument("--apply", action="store_true", help="apagar de verdade")
    p_prune.set_defaults(func=_cmd_prune)

    p_fin = sub.add_parser("finalize", help="gerar vFINAL (.pptx + .pdf)")
    p_fin.add_argument("pptx", help="arquivo .pptx de origem")
    p_fin.add_argument("--no-pdf", action="store_true", help="não gerar o PDF")
    p_fin.set_defaults(func=_cmd_finalize)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
