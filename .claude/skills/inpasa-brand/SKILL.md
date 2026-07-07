---
name: inpasa-brand
description: >
  Aplica a identidade visual oficial da INPASA Agroindustrial S/A em qualquer material
  que precise ser criado ou formatado — apresentações (.pptx), documentos Word (.docx),
  PDFs, relatórios, planilhas (.xlsx), dashboards e e-mails. Use esta skill SEMPRE que
  o usuário pedir para criar, formatar ou padronizar qualquer material da INPASA:
  relatório de projeto, apresentação para diretoria, ata de reunião, planilha de
  acompanhamento, sumário executivo, comunicado interno, memorando, dashboard, ou
  qualquer outro documento corporativo. Também acionar quando o usuário mencionar
  "brandbook", "identidade visual", "padrão INPASA", "cores da empresa", "template",
  "logo", "unidades INPASA" (NMT, RVD, RDN, BLS, LEM, SNP, SPD, LRL, DRD, SDR), ou
  pedir materiais "no padrão da empresa". Acionar também quando o usuário mencionar
  qualquer abreviação de unidade INPASA num contexto de material a ser criado.
  Público-alvo principal: Diretoria e liderança interna. Idioma: Português (BR).
---

# INPASA Brand Skill

Garante que todos os materiais criados sigam rigorosamente o Manual de Identidade
Corporativa da INPASA. **Sempre leia este SKILL.md antes de criar qualquer material**,
e consulte os arquivos de referência em `references/` conforme a tabela ao final.

---

## 1. Identidade da Marca

- **Nome oficial:** INPASA Agroindustrial S/A
- **Tagline:** MAIS QUE ENERGIA
- **Posicionamento:** Maior biorrefinaria de grãos da América Latina e 2ª maior do mundo — milho, sorgo e biomassa.
- **Missão:** Produzir soluções limpas e sustentáveis para atender a demanda crescente de energia do planeta.
- **Visão:** Ser reconhecida mundialmente pela sustentabilidade, qualidade e tecnologias empregadas.
- **Valores:** Ética · Profissionalismo · Credibilidade · Simplicidade · Trabalho em equipe · Transparência · Dinamismo

---

## 2. Paleta de Cores Oficial

### Cores Primárias (uso prioritário)

| Nome | HEX | RGB | Uso |
|---|---|---|---|
| Azul INPASA | `#124E81` | 18 / 78 / 129 | Cor dominante (60–70% do peso visual) |
| Ouro | `#EAA239` | 234 / 162 / 57 | Acento institucional (slides de conteúdo, taglines) |
| Ouro Vibrante | `#FFA32A` | 255 / 163 / 42 | Acento de capa, barra superior decorativa |
| Cinza Claro | `#BDBFC1` | 189 / 191 / 193 | Neutro / linhas de grade / texto secundário |

> **Nota técnica:** as cores acima foram extraídas diretamente do `inpasa_template.pptx`
> oficial. O brandbook impresso pode listar `#304F7E` como Azul INPASA — esse é
> um valor histórico/teórico. **Use sempre `#124E81`** para casar visualmente
> com os assets do template (logos, formas, ícones).

### Cores Secundárias (destaques)

| Nome | HEX | Uso típico |
|---|---|---|
| Verde Escuro | `#007D77` | Sustentabilidade / ETE |
| Terracota | `#CC5121` | Alertas / críticos |
| Verde Claro | `#609346` | Indicadores positivos / OK |
| Azul Claro | `#007CC5` | Links / chamadas |

### Regras de Cor

- O **Azul INPASA (`#124E81`)** é a cor dominante — 60–70% do peso visual de qualquer material.
- O **Ouro (`#EAA239`)** é acento — usar com parcimônia (eyebrows de seção, destaques pontuais).
- O **Ouro Vibrante (`#FFA32A`)** aparece apenas na barra decorativa superior das capas e em CTAs.
- **Sem gradientes** em nenhum elemento da marca.
- Capa e encerramento: fundo Azul INPASA sólido (ou foto industrial escurecida sobreposta com azul).
- Slides de conteúdo: fundo branco (`#FFFFFF`) com acentos azul/ouro.
- **Status semáforo:** Verde `#609346` = OK · Ouro `#EAA239` = Atenção · Terracota `#CC5121` = Crítico.

---

## 3. Tipografia

| Uso | Fonte | Peso | Tamanho mínimo |
|---|---|---|---|
| Títulos | Montserrat | ExtraBold | 28pt |
| Subtítulos | Montserrat | SemiBold | 18pt |
| Texto corrido | Montserrat | Medium / Regular | 11pt |
| Tagline "MAIS QUE ENERGIA" | Montserrat | Bold Italic | — |

**Fallback:** Arial Bold para títulos, Arial para corpo. Montserrat é gratuita
no Google Fonts e já vem embarcada no template oficial — preferir sempre.

> **Nota técnica:** versões antigas do brandbook citam "Nexa Black Italic" para
> a tagline, mas o template oficial em uso emprega Montserrat Bold Italic.
> Para garantir consistência com os assets do template, **use Montserrat Bold
> Italic** em todas as taglines.

---

## 4. Logotipo

A skill possui **10 variantes oficiais** em `assets/logos/` — **todas com fundo
transparente (RGBA)**, prontas para uso sobre qualquer fundo. **Nunca recriar
logo via código, shapes ou tipografia** — sempre usar arquivo PNG.

**Para escolher a variante correta, consulte `references/logos.md`** (árvore de
decisão por tipo de fundo + posicionamento padrão por tipo de material).

### Verificação obrigatória ao usar logo
Antes de inserir um logo num material, confirmar que o arquivo está em modo
RGBA (com canal alpha). Se algum logo aparecer com retângulo opaco ao redor,
o asset está corrompido — **NÃO entregar o material**, regenerar o asset.

### Proibições absolutas
❌ Rotacionar · ❌ Alterar cores · ❌ Outline · ❌ Distorcer
❌ Aplicar sobre fundo sem contraste · ❌ Marca d'água com transparência
❌ Aplicar moldura · ❌ Desalinhar · ❌ Gradiente · ❌ Sombra/efeito 3D

---

## 5. Unidades INPASA

A INPASA opera **10 unidades** entre Brasil e Paraguai. **Use SEMPRE os códigos
oficiais** em nomes de arquivo, rodapés e identificadores formais.

### Resumo

| Código | Nome curto | UF/País | Status |
|---|---|---|---|
| LRL | Laurel | Paraguai | Operação |
| SPD | San Pedro | Paraguai | Operação |
| SNP | Sinop | MT | Operação |
| NMT | Nova Mutum | MT | Operação |
| DRD | Dourados | MS | Operação |
| SDR | Sidrolândia | MS | Operação |
| BLS | Balsas | MA | Operação |
| LEM | Luís Eduardo | BA | Construção |
| RVD | Rio Verde | GO | Construção |
| RDN | Rondonópolis | MT | Construção |

**Para regras detalhadas** (identificação em rodapé, materiais multi-unidade,
fases F1/F2/F3, marcos por unidade, idioma para Paraguai), **consulte
`references/unidades.md`.**

---

## 6. Nomenclatura de Arquivos

**Padrão obrigatório** para todo arquivo gerado:

<!--
  ATENÇÃO — CONTEÚDO PARCIAL.
  Este SKILL.md foi reconstruído a partir do texto colado pelo usuário na
  sessão do Claude Code (o comando /inpasa-brand original vive no claude.ai).
  O conteúdo original foi CORTADO no meio da Seção 6 (Nomenclatura de Arquivos).
  Ainda faltam, para a skill funcionar 100% neste projeto:
    - o restante da Seção 6 em diante;
    - os arquivos de referência citados: references/logos.md, references/unidades.md
      (e demais referenciados na tabela final);
    - os 10 logos oficiais em assets/logos/ (PNG RGBA).
  Cole o restante do conteúdo e anexe os PNGs para completar.
-->
