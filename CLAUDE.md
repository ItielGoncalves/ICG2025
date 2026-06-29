# Estilo de comunicação do Itiel (REGRA PERMANENTE)

> Vale para **toda** comunicação escrita feita para o Itiel ou em nome dele:
> mensagens de WhatsApp, e-mails, textos de apoio e **o corpo das
> apresentações/documentos**.

- **NUNCA usar traço/hífen** (`—`, `–`, `-`) como pontuação no meio das frases.
  Em vez de traço, usar **vírgula, dois-pontos, ponto ou parênteses**, ou
  reescrever a frase. Isso é regra fixa, não pedir confirmação a cada vez.
  (Exceção óbvia: hífen interno de palavras compostas, ex.: "dois-pontos",
  e o separador ` - ` obrigatório do padrão de nome de arquivo abaixo.)

---

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
   correspondente, com o **mesmo nome** e marcado como `vFINAL`.
2. Manter **no máximo 3 versões distribuídas** por arquivo, **além da
   `vFINAL`**. Quando houver muitas versões, escolher 3 espalhadas
   **uniformemente** pelo histórico (sempre incluindo a mais recente) e
   **descartar as intermediárias** entre elas.
3. **Sempre preservar** a **`vFINAL`** (à parte, não conta nas 3) e a versão
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
> disco local — nesse caso, apenas nomeie o arquivo no padrão acima e o Itiel
> move para a pasta.
