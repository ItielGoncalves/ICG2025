# Acervo Estratégico

Local **único** de salvamento e de **consulta** das apresentações e relatórios
finais do Itiel. Funciona nas duas superfícies (Claude Code **web** e **local**),
usando o **Google Drive** como ponte e o **catálogo** como índice pesquisável.

## Peças

- **Pasta no Google Drive:** `Acervo Estratégico`
  (`id 1HF2J6sMMGGY1nvDUEaJH4ypeq0J1ftIs`) — destino dos binários no modo web e
  ponto de convergência com a pasta local (se sincronizada via Google Drive para
  Desktop).
- **Pasta local (Mac):**
  `/Users/itielgoncalves/Documentos Local/c. ARQUIVOS PRINCIPAIS/Coorporativo/000 - Reunião Diretoria, gerencias e eq. de gestão`
- **`catalogo.json`** (aqui, espelhado no Drive) — o índice. Uma entrada por
  documento **final**, com data, unidade, título, **assunto/resumo**,
  palavras-chave e arquivos (`pptx`, `pdf`, `imagem_resumo`).

## O que cada `vFINAL` gera

1. `AAAA.MM.DD - UNIDADE - Título vFINAL.pptx` (editável)
2. `AAAA.MM.DD - UNIDADE - Título vFINAL.pdf` (exportado)
3. `AAAA.MM.DD - UNIDADE - Título vFINAL (resumo iPhone).png` — resumo super
   objetivo em imagem vertical, para encaminhar ao **sr. José** (abre no iPhone).

Só a `vFINAL` fica no acervo (decisão do Itiel), então cada documento aparece
**uma vez**; refinalizar **atualiza** a entrada.

## Comandos (`acervo.py`, na raiz do repo)

```bash
# LOCAL — finaliza + resumo iPhone + copia p/ a pasta + cataloga, tudo junto:
python acervo.py arquivar "…vNN.pptx" --assunto "…" --palavras a,b \
  --resumo "Bullet 1" --resumo "Bullet 2" --destaque "+12%" --destaque-rotulo "…"

# Registrar no catálogo sem copiar arquivos (usado no fluxo web após o upload):
python acervo.py registrar "…vFINAL.pptx" --assunto "…" --palavras a,b --origem web

# Consultar:
python acervo.py buscar "termo"      # por assunto/título/unidade, tolerante a acento
python acervo.py listar
```

## Fluxo no modo web (Claude Code)

1. Gerar `.pptx`, `.pdf` e `… (resumo iPhone).png` no container.
2. Subir os três para a pasta `Acervo Estratégico` no Drive
   (`mcp__Google_Drive__create_file` com `parentId`, `base64Content`,
   `contentMimeType` e `disableConversionToGoogleType: true`).
3. `python acervo.py registrar …` e subir o `catalogo.json` atualizado ao Drive.
4. Entregar os arquivos ao Itiel na conversa.

## Requisitos

- **PDF:** LibreOffice headless (Mac: `brew install --cask libreoffice`) ou
  `LIBREOFFICE_BIN`.
- **Resumo iPhone (PNG):** navegador para rasterizar — Chromium/Playwright no
  web; **Google Chrome headless** no Mac (ou `CHROME_BIN`).
