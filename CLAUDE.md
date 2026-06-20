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
| `DRD` | Dourados |

> Outras unidades a confirmar com o Itiel e acrescentar aqui conforme o padrão
> interno já usado.

## Exemplos

```
2026.06.06 - MULTI - Report Estratégico Semanal.pdf
2026.06.10 - MULTI - Gestão Tática de Obras v11.pptx
2026.06.08 - MULTI - Estudo de Equipamentos Móveis v07.pptx
2026.06.19 - DRD - Plano de Ações Supervisório v01.pptx
```

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
