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
| `SNP` / `SNOP` | Sinop |
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

## 4. Finalização e versionamento

Quando o Itiel disser que **a versão ficou boa / é a final**:

1. Gerar o **`.pptx`** (editável) **e** exportar o **`.pdf`**, mesmo nome,
   marcados como `vFINAL`.
2. Manter no máximo **3 versões distribuídas** por arquivo, **além da
   `vFINAL`**. Havendo muitas versões, escolher 3 espalhadas **uniformemente**
   pelo histórico (sempre incluindo a mais recente) e apagar as do meio.
   - Ex.: `v01…v30` → manter `v10`, `v20`, `v30` + `vFINAL`; apagar o resto.
3. **Sempre preservar** a `vFINAL` (à parte) e a versão mais recente.

> A **poda/remoção** de arquivos só funciona em superfície local. No Claude Code
> web não há como apagar arquivos do Mac.
