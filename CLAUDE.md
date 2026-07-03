# Padrão de nomenclatura de arquivos (apresentações e documentos)

> Esta é a regra oficial para nomear **qualquer** arquivo gerado para o Itiel
> (apresentações, relatórios, planilhas, PDFs). Vale a partir de agora e
> substitui o padrão antigo `APR_MULTI_GERAL_..._v01`.

## Estrutura

```
AAAA.MM.DD - UNIDADE - Título com espaços naturais [vN].ext
```

A data vem **sempre primeiro**, no formato `ano.mês.dia`, para que a listagem
por nome fique em ordem cronológica automaticamente.

## Componentes

| Bloco | Regra | Observação |
|---|---|---|
| **Data** | `AAAA.MM.DD` (ano → mês → dia, com pontos) | obrigatório; garante ordenação cronológica |
| ` - ` | espaço-traço-espaço | separador entre blocos |
| **Unidade** | código da unidade (ver tabela abaixo) | obrigatório |
| ` - ` | espaço-traço-espaço | separador entre blocos |
| **Título** | texto livre, palavras separadas por **espaço**, acentuação normal | **sem** underscores; legível |
| **Versão** | ` v01`, ` v2`, ` vFINAL` ao final do título | opcional; usar quando houver controle de versão |
| **Extensão** | `.pptx` (editável) · `.pdf` (exportado) · `.xlsx` · `.docx` | o mesmo conteúdo pode sair em `.pptx` e `.pdf` com a mesma versão |

## Códigos de unidade

| Código | Unidade |
|---|---|
| `MULTI` | Todas as unidades / assunto geral |
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

> Se aparecer uma unidade nova, confirmar o código com o Itiel e acrescentar
> aqui no mesmo padrão.

## Exemplos

```
2026.06.06 - MULTI - Report Estratégico Semanal.pdf
2026.06.10 - MULTI - Gestão Tática de Obras v11.pptx
2026.06.08 - MULTI - Estudo de Equipamentos Móveis v07.pptx
2026.06.19 - DRD - Plano de Ações Supervisório v01.pptx
```

## Fluxo ao criar uma apresentação ou documento

Sempre que o Itiel pedir para **criar uma apresentação ou documento**, antes de
gerar, **perguntar o destino**:

> "Isso é para a pasta de **Gestão Estratégica** (diretoria / gerências / equipe
> de gestão) ou só para **Downloads**?"

- **Gestão Estratégica** → nomear no padrão `AAAA.MM.DD - UNIDADE - Título [vN]`,
  confirmar a **unidade** quando não estiver clara, e **salvar direto** na pasta
  estratégica (ver "Onde salvar"). Na finalização, aplicar a regra de
  versionamento abaixo.
- **Downloads** → gerar normalmente, sem a obrigação do padrão/pasta (mas o
  padrão de nome continua recomendado).

> Em superfícies locais (Cowork / Desktop) dá para salvar direto na pasta certa.
> No Claude Code web, apenas nomear no padrão e o Itiel move o arquivo.

## Versionamento e finalização

Quando o Itiel disser que **a versão ficou boa / é a final**:

1. Gerar o arquivo final em **`.pptx`** (editável) **e** exportar o **`.pdf`**
   correspondente, com o **mesmo nome** e marcado como `vFINAL`. **Sempre
   manter as duas finais** (`.pptx` e `.pdf`) no diretório — tanto na pasta
   física quanto no repositório/acervo.
2. Gerar também a **imagem-resumo (iPhone)**: um resumo **super objetivo** em
   imagem vertical, porque o Itiel quase sempre encaminha ao **sr. José**, que
   abre no **iPhone**. Nome:
   `AAAA.MM.DD - UNIDADE - Título vFINAL (resumo iPhone).png`. Conteúdo: 3 a 5
   bullets diretos + um destaque opcional (número de impacto).
3. **Arquivar no acervo** e **registrar no catálogo** (ver "Acervo" abaixo),
   para que esse material vire consultável por assunto.
4. Manter **no máximo 3 versões distribuídas** por arquivo, **além da
   `vFINAL`**. Quando houver muitas versões, escolher 3 espalhadas
   **uniformemente** pelo histórico (sempre incluindo a mais recente) e
   **descartar as intermediárias** entre elas.
5. **Sempre preservar** a **`vFINAL`** (à parte, não conta nas 3) e a versão
   **mais recente**.

Exemplo de poda (distribuída):

```
v01 … v30  →  manter v10, v20 e v30 (distribuídas) + vFINAL; apagar o resto
```

> **Limitação por superfície:** a **poda/remoção** de arquivos antigos só
> funciona em superfícies **locais** (Cowork / Claude Desktop com acesso ao
> disco). No Claude Code na web (container isolado) não há como apagar arquivos
> do Mac — nesse caso, apenas nomear/gerar no padrão correto.

## Onde salvar (assuntos estratégicos)

Apresentações e documentos estratégicos (diretoria, gerências, equipe de gestão)
devem ser salvos diretamente em:

```
/Users/itielgoncalves/Documentos Local/c. ARQUIVOS PRINCIPAIS/Coorporativo/000 - Reunião Diretoria, gerencias e eq. de gestão
```

> **Limitação por superfície:** o salvamento direto nessa pasta só funciona em
> superfícies **locais** (Cowork / Claude Desktop com acesso a arquivos na
> máquina do Itiel). No Claude Code na web (container isolado) não há acesso ao
> disco local — nesse caso, o acervo no Google Drive resolve o salvamento e a
> consulta (ver abaixo).

## Acervo (pesquisa e salvamento nas duas superfícies)

O acervo é o **local único** de salvamento e de **consulta** das apresentações e
relatórios estratégicos. Ele existe para funcionar **tanto no web quanto no
local**, e a ponte entre as duas superfícies é o **Google Drive**.

- **Pasta no Drive:** `Acervo Estratégico`
  (`id 1HF2J6sMMGGY1nvDUEaJH4ypeq0J1ftIs`).
- **Pasta local (Mac):** a pasta estratégica em "Onde salvar" acima. Se o Itiel
  quiser convergência automática, ele pode sincronizar essa pasta com a pasta do
  Drive (Google Drive para Desktop).
- **Catálogo (o que unifica):** `acervo/catalogo.json` no repositório, espelhado
  no Drive. Cada `vFINAL` vira uma entrada com data, unidade, título,
  **assunto/resumo**, palavras-chave e os arquivos (`.pptx`, `.pdf`,
  `imagem_resumo`). Como só guardamos a `vFINAL`, cada documento aparece **uma
  vez** (refinalizar **atualiza** a entrada).

**Ao finalizar:**

- **Web (Claude Code):** gerar os artefatos no container, **subir os três** para
  a pasta `Acervo Estratégico` no Drive (`mcp__Google_Drive__create_file`,
  `parentId` = id acima, `base64Content` + `contentMimeType` +
  `disableConversionToGoogleType: true`), **registrar no catálogo**
  (`python acervo.py registrar …`) e subir o `catalogo.json` atualizado.
- **Local (Cowork / Desktop):** `python acervo.py arquivar "…vNN.pptx"
  --assunto "…" --palavras a,b --resumo "…" --resumo "…" --destaque "+12%"` —
  finaliza (`.pptx`+`.pdf`), gera o resumo iPhone, copia para a pasta
  estratégica e registra no catálogo, tudo de uma vez.

**Ao ser perguntado sobre um assunto:** consultar o catálogo antes de responder
e dizer qual documento trata, de quando é e como foi feito —
`python acervo.py buscar "termo"` (ou `listar`). No web, se o catálogo do repo
estiver defasado, ler o `catalogo.json` do Drive primeiro.
