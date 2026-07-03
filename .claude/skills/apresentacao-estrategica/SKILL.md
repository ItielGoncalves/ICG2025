---
name: apresentacao-estrategica
description: >-
  Use SEMPRE que o Itiel pedir para criar/gerar uma apresentação, slide, deck,
  documento, relatório, planilha ou PDF. Garante o destino correto (Gestão
  Estratégica vs Downloads), a nomenclatura padrão
  "AAAA.MM.DD - UNIDADE - Título [vN].ext" e a regra de versionamento/poda.
---

# Apresentação / documento no padrão do Itiel

Quando o Itiel pedir para **criar uma apresentação ou documento**, siga este
fluxo antes de gerar qualquer coisa.

## 1. Perguntar o destino (sempre)

Pergunte de forma direta:

> "Isso é para a pasta de **Gestão Estratégica** (diretoria / gerências / equipe
> de gestão) ou só para **Downloads**?"

- **Downloads** → gere normalmente. O padrão de nome é recomendado, mas não
  obrigatório, e não precisa salvar na pasta estratégica.
- **Gestão Estratégica** → siga os passos 2 a 4.

## 2. Nomear no padrão

```
AAAA.MM.DD - UNIDADE - Título com espaços naturais [vN].ext
```

- **Data** primeiro, `ano.mês.dia` com **pontos** (ordena cronologicamente).
- **Unidade**: confirme com o Itiel se não estiver clara.

| Código | Unidade |
|---|---|
| `MULTI` | Todas as unidades / geral |
| `SNP` | Sinop |
| `MTU` | Nova Mutum |
| `BLS` | Balsas |
| `LEM` | Luís Eduardo Magalhães |
| `RVD` | Rio Verde |
| `RND` | Rondonópolis |
| `SDR` | Sidrolândia |
| `SPD` | São Pedro |
| `LRL` | Laurel |
| `DRD` | Dourados |

- **Título**: texto livre, palavras com **espaço** e acento normal, sem
  underscores.
- **Versão** (` v01`, ` vFINAL`): opcional, ao final do título.

## 3. Salvar na pasta certa (Gestão Estratégica)

```
/Users/itielgoncalves/Documentos Local/c. ARQUIVOS PRINCIPAIS/Coorporativo/000 - Reunião Diretoria, gerencias e eq. de gestão
```

> Salvar direto só funciona em superfície **local** (Cowork / Claude Desktop com
> acesso ao disco). No Claude Code web, apenas nomeie no padrão.

## 4. Finalização, acervo e resumo para o sr. José

Quando o Itiel disser que **a versão ficou boa / é a final**, entregue os
**três artefatos** e registre no acervo:

1. Gerar o **`.pptx`** (editável) **e** exportar o **`.pdf`**, mesmo nome,
   marcados como `vFINAL`. **Sempre manter as duas finais** (`.pptx` e `.pdf`)
   no diretório — físico e repositório.
2. Gerar a **imagem-resumo (iPhone)** — um resumo **super objetivo** em imagem
   vertical, porque o Itiel quase sempre encaminha ao **sr. José**, que abre no
   **iPhone**. Nome:
   `AAAA.MM.DD - UNIDADE - Título vFINAL (resumo iPhone).png`.
   Conteúdo: 3 a 5 bullets diretos + um destaque opcional (número de impacto).
3. **Arquivar no acervo** (ver seção 5) e **registrar no catálogo** para busca.
4. Poda de versões: manter no máximo **3 versões distribuídas** por arquivo,
   **além da `vFINAL`** (ex.: `v01…v30` → `v10`, `v20`, `v30` + `vFINAL`).
   **Sempre preservar** a `vFINAL` e a mais recente.

> A **poda/remoção** só funciona em superfície local. No Claude Code web não há
> como apagar arquivos do Mac.

## 5. O acervo (pesquisa + salvamento nas duas superfícies)

O acervo é **único** e vive no **Google Drive**, pasta **`Acervo Estratégico`**
(`id 1HF2J6sMMGGY1nvDUEaJH4ypeq0J1ftIs`). O que unifica tudo é o **catálogo**
(`acervo/catalogo.json` no repo, espelhado no Drive): data, unidade, título,
**assunto/resumo** e os arquivos de cada `vFINAL`.

**Ao finalizar — modo web (Claude Code):**

1. Gere os artefatos no container (`.pptx`, `.pdf`, `... (resumo iPhone).png`).
2. **Suba os três** para a pasta `Acervo Estratégico` no Drive via
   `mcp__Google_Drive__create_file` (`parentId` = id acima, `base64Content` +
   `contentMimeType`, `disableConversionToGoogleType: true` para manter os
   binários).
3. **Registre no catálogo**: `python acervo.py registrar "<nome vFINAL>" --assunto "..." --palavras a,b,c --origem web`, e suba o `catalogo.json` atualizado para o Drive também.
4. Entregue os arquivos ao Itiel na conversa (o `.png` é o que ele manda ao sr. José).

**Ao finalizar — modo local (Cowork / Desktop):** um comando faz tudo (finaliza,
copia para a pasta estratégica do Mac, gera o resumo e registra no catálogo):

```bash
python acervo.py arquivar "AAAA.MM.DD - UNIDADE - Título vNN.pptx" \
  --assunto "o que o documento trata" --palavras obras,cronograma \
  --resumo "Bullet 1" --resumo "Bullet 2" --resumo "Bullet 3" \
  --destaque "+12%" --destaque-rotulo "avanço vs. plano"
```

## 6. Consulta ("qual apresentação fala sobre X?")

Quando o Itiel perguntar sobre um assunto, **busque no catálogo** antes de
responder — e diga qual documento trata, de quando é e como foi feito:

```bash
python acervo.py buscar "segurança patrimonial"
python acervo.py listar
```

No web, se o `catalogo.json` do repo estiver defasado, leia a versão do Drive
(`Acervo Estratégico/catalogo.json`) antes de responder.

## Helpers locais

```bash
python gestao_arquivos.py finalize "AAAA.MM.DD - UNIDADE - Título vNN.pptx"  # só vFINAL .pptx + .pdf
python gestao_arquivos.py prune "/caminho/da/pasta" --apply                  # poda mantendo 3 + vFINAL
python acervo.py arquivar "…vNN.pptx" --assunto "…" --resumo "…"             # finaliza + acervo + resumo + catálogo
python acervo.py buscar "termo"                                              # pesquisa por assunto/título
```

> O resumo iPhone usa o navegador para rasterizar: no web, Chromium/Playwright
> (já disponível); no Mac, o **Google Chrome headless** (ou defina `CHROME_BIN`).
