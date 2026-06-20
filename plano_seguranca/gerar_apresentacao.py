# -*- coding: utf-8 -*-
"""
Gera a apresentacao executiva do Plano de Acao de Seguranca (INPASA).
Foco: instrumentacao, automacao e prevencao de incendio nas areas criticas.
Saida: plano_seguranca/Plano_Acao_Seguranca_INPASA.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# ---- Paleta ----
AZUL = RGBColor(0x0B, 0x3D, 0x5C)     # cabecalho
AZUL_CLARO = RGBColor(0x1F, 0x77, 0xB4)
LARANJA = RGBColor(0xE8, 0x6A, 0x17)  # alerta / destaque
CINZA = RGBColor(0x44, 0x44, 0x44)
CINZA_CLARO = RGBColor(0xF2, 0xF4, 0xF6)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
VERDE = RGBColor(0x2E, 0x7D, 0x32)
VERMELHO = RGBColor(0xC0, 0x39, 0x2B)
AMARELO = RGBColor(0xF1, 0xC4, 0x0F)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(BLANK)


def rect(slide, x, y, w, h, color, line=None):
    from pptx.enum.shapes import MSO_SHAPE
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sp.fill.solid()
    sp.fill.fore_color.rgb = color
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(0.75)
    sp.shadow.inherit = False
    return sp


def txt(slide, x, y, w, h, text, size=18, bold=False, color=CINZA,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri"):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Pt(4)
    tf.margin_right = Pt(4)
    tf.margin_top = Pt(2)
    tf.margin_bottom = Pt(2)
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        r.font.name = font
    return tb


def bullets(slide, x, y, w, h, items, size=16, color=CINZA, gap=6):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, it in enumerate(items):
        if isinstance(it, tuple):
            text, lvl = it
        else:
            text, lvl = it, 0
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = lvl
        p.space_after = Pt(gap)
        r = p.add_run()
        bullet = "•  " if lvl == 0 else "–  "
        r.text = bullet + text
        r.font.size = Pt(size if lvl == 0 else size - 2)
        r.font.color.rgb = color
        r.font.name = "Calibri"
    return tb


def header(slide, kicker, title):
    rect(slide, 0, 0, SW, Inches(1.15), AZUL)
    rect(slide, 0, Inches(1.15), SW, Inches(0.06), LARANJA)
    txt(slide, Inches(0.5), Inches(0.12), Inches(12), Inches(0.35),
        kicker, size=12, bold=True, color=AMARELO)
    txt(slide, Inches(0.5), Inches(0.42), Inches(12.3), Inches(0.7),
        title, size=26, bold=True, color=BRANCO, anchor=MSO_ANCHOR.MIDDLE)


def footer(slide, n):
    txt(slide, Inches(0.5), Inches(7.05), Inches(8), Inches(0.35),
        "Plano de Ação de Segurança — INPASA  |  Manutenção & Automação",
        size=9, color=RGBColor(0x99, 0x99, 0x99))
    txt(slide, Inches(12.2), Inches(7.05), Inches(0.9), Inches(0.35),
        str(n), size=9, color=RGBColor(0x99, 0x99, 0x99), align=PP_ALIGN.RIGHT)


def table(slide, x, y, w, rows, col_w, header_fill=AZUL, fsize=11,
          row_h=Inches(0.4)):
    """rows[0] = header. col_w = list de fracoes (somam 1)."""
    nrows = len(rows)
    ncols = len(rows[0])
    gtbl = slide.shapes.add_table(nrows, ncols, x, y, w, row_h * nrows).table
    # larguras
    for ci, frac in enumerate(col_w):
        gtbl.columns[ci].width = Emu(int(w * frac))
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = gtbl.cell(ri, ci)
            cell.margin_left = Pt(5)
            cell.margin_right = Pt(5)
            cell.margin_top = Pt(2)
            cell.margin_bottom = Pt(2)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run()
            r.text = str(val)
            r.font.name = "Calibri"
            if ri == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_fill
                r.font.bold = True
                r.font.color.rgb = BRANCO
                r.font.size = Pt(fsize + 0.5)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = BRANCO if ri % 2 else CINZA_CLARO
                r.font.color.rgb = CINZA
                r.font.size = Pt(fsize)
    return gtbl


# =====================================================================
# SLIDE 1 — CAPA
# =====================================================================
s = add_slide()
rect(s, 0, 0, SW, SH, AZUL)
rect(s, 0, Inches(4.7), SW, Inches(0.08), LARANJA)
txt(s, Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.5),
    "INPASA  •  PRODUÇÃO DE ETANOL", size=16, bold=True, color=AMARELO)
txt(s, Inches(0.8), Inches(2.1), Inches(11.7), Inches(2.0),
    "Plano de Ação de Segurança\nInstrumentação, Automação e Prevenção de Incêndio",
    size=40, bold=True, color=BRANCO)
txt(s, Inches(0.8), Inches(5.0), Inches(11.7), Inches(1.2),
    "Áreas críticas: Armazenagem de Grãos • Torres de Resfriamento • Caldeira (transportadores) • Destilaria\n"
    "Escopo: 4 a 6 unidades  |  Contexto: Manutenção & Automação",
    size=16, color=RGBColor(0xCF, 0xDD, 0xE8))
txt(s, Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.5),
    "Documento de trabalho — versão preliminar para priorização  •  Junho/2026",
    size=12, color=RGBColor(0x9F, 0xB4, 0xC4))

# =====================================================================
# SLIDE 2 — SUMARIO EXECUTIVO
# =====================================================================
s = add_slide()
header(s, "VISÃO GERAL", "Sumário Executivo")
bullets(s, Inches(0.5), Inches(1.5), Inches(12.3), Inches(5.2), [
    "Objetivo: garantir a funcionalidade da instrumentação e reduzir o risco de incêndio nas áreas de maior histórico de acidentes.",
    "Diagnóstico mostra que os incêndios em grãos NÃO foram apenas princípios de fogo — houve incêndios recorrentes.",
    ("Causa raiz nº1 (grãos): roletes travando → atrito → ignição, agravado por correias sem proteção antichama.", 1),
    ("Causa raiz nº2 (torres): respingo de solda no recheio durante trabalho a quente.", 1),
    ("Causa raiz nº3 (caldeira): fogo nos transportadores de alimentação (mesma natureza dos grãos).", 1),
    "A inspeção visual por operador já se mostrou insuficiente → migrar para detecção instrumentada + intertravamento.",
    "Estratégia recomendada: DEFESA EM CAMADAS — Prevenção → Detecção → Supressão → Gestão.",
    "Programa faseado (Fase 0 a 3), replicável nas 4–6 unidades, com priorização por risco e causa raiz.",
], size=16, gap=8)

# =====================================================================
# SLIDE 3 — DIAGNOSTICO POR AREA (causa raiz)
# =====================================================================
s = add_slide()
header(s, "DIAGNÓSTICO", "Áreas críticas e causa raiz")
rows = [
    ["Área", "Situação atual", "Causa raiz do incêndio/acidente"],
    ["Armazenagem de grãos",
     "Termometria de silo OK. Patinagem parcial. Sem detecção de fagulha.",
     "Roletes travando + correia não-antichama. Housekeeping de poeira deficiente."],
    ["Torres de resfriamento",
     "Incêndios durante manutenção.",
     "Respingo de solda cai no recheio (fill) — trabalho a quente sem barreira."],
    ["Caldeira (biomassa)",
     "Câmera termográfica anuncia no supervisório. Acidentes ≠ fogo.",
     "Fogo ocorre nos transportadores de alimentação (correia/rolete)."],
    ["Destilaria",
     "Área classificada, controle mais maduro.",
     "Incidentes pequenos — prioridade menor (manter conformidade Ex)."],
]
table(s, Inches(0.5), Inches(1.5), Inches(12.3), rows,
      [0.18, 0.37, 0.45], fsize=12, row_h=Inches(1.0))
footer(s, 3)

# =====================================================================
# SLIDE 4 — MATRIZ DE RISCO
# =====================================================================
s = add_slide()
header(s, "PRIORIZAÇÃO", "Matriz de risco (qualitativa)")
rows = [
    ["Área / Cenário", "Probabilidade", "Severidade", "Risco"],
    ["Grãos — incêndio por rolete/correia", "Alta", "Alta", "CRÍTICO"],
    ["Grãos — explosão de poeira", "Média", "Muito alta", "CRÍTICO"],
    ["Torres — ignição do recheio (solda)", "Média", "Alta", "ALTO"],
    ["Caldeira — fogo nos transportadores", "Média", "Alta", "ALTO"],
    ["Destilaria — vazamento/ignição", "Baixa", "Muito alta", "MÉDIO"],
]
t = table(s, Inches(0.6), Inches(1.6), Inches(12.1), rows,
          [0.42, 0.19, 0.19, 0.20], fsize=13, row_h=Inches(0.62))
# colorir coluna Risco
cores = {"CRÍTICO": VERMELHO, "ALTO": LARANJA, "MÉDIO": AMARELO}
for ri in range(1, len(rows)):
    cell = t.cell(ri, 3)
    val = rows[ri][3]
    cell.fill.solid()
    cell.fill.fore_color.rgb = cores.get(val, CINZA_CLARO)
    cell.text_frame.paragraphs[0].runs[0].font.color.rgb = BRANCO
    cell.text_frame.paragraphs[0].runs[0].font.bold = True
txt(s, Inches(0.6), Inches(6.4), Inches(12), Inches(0.5),
    "Prioridade de execução: itens CRÍTICOS primeiro (grãos), depois ALTOS (torres e caldeira).",
    size=13, bold=True, color=AZUL)
footer(s, 4)

# =====================================================================
# SLIDE 5 — ESTRATEGIA DEFESA EM CAMADAS
# =====================================================================
s = add_slide()
header(s, "ESTRATÉGIA", "Defesa em camadas")
camadas = [
    ("1. PREVENÇÃO", "Eliminar a causa antes do fogo: monitorar patinagem, temperatura de mancal, alinhamento; controle de poeira; PT de trabalho a quente.", VERDE),
    ("2. DETECÇÃO", "Detectar cedo: detecção de fagulha nos chutes, cabo de calor (LHD) na correia, termografia, CO em silos.", AZUL_CLARO),
    ("3. SUPRESSÃO", "Conter o evento: extinção de fagulha por água, dilúvio/água-névoa zoneada, parada segura automática.", LARANJA),
    ("4. GESTÃO", "Sustentar: integração ao SCADA/Rockwell, KPIs, plano de calibração, CMMS e auditoria das PTs.", CINZA),
]
y = Inches(1.55)
for titulo, desc, cor in camadas:
    rect(s, Inches(0.5), y, Inches(3.1), Inches(1.15), cor)
    txt(s, Inches(0.6), y, Inches(2.9), Inches(1.15), titulo, size=16,
        bold=True, color=BRANCO, anchor=MSO_ANCHOR.MIDDLE)
    rect(s, Inches(3.75), y, Inches(9.05), Inches(1.15), CINZA_CLARO)
    txt(s, Inches(3.95), y, Inches(8.7), Inches(1.15), desc, size=14,
        color=CINZA, anchor=MSO_ANCHOR.MIDDLE)
    y += Inches(1.32)
footer(s, 5)

# =====================================================================
# SLIDES 6-9 — FASES
# =====================================================================
def fase_slide(n, kicker, titulo, prazo, itens, capex):
    s = add_slide()
    header(s, kicker, titulo)
    txt(s, Inches(0.5), Inches(1.3), Inches(12), Inches(0.4),
        "Prazo sugerido: " + prazo, size=14, bold=True, color=LARANJA)
    bullets(s, Inches(0.5), Inches(1.9), Inches(12.3), Inches(4.0), itens,
            size=15, gap=7)
    rect(s, Inches(0.5), Inches(6.25), Inches(12.3), Inches(0.6), AZUL)
    txt(s, Inches(0.7), Inches(6.25), Inches(12), Inches(0.6),
        "CAPEX estimado: " + capex, size=14, bold=True, color=BRANCO,
        anchor=MSO_ANCHOR.MIDDLE)
    footer(s, n)
    return s

fase_slide(
    6, "FASE 0", "Diagnóstico e levantamento (base de tudo)",
    "0–60 dias  •  baixo custo",
    [
        "Inventário/TAG de TODOS os elevadores e correias por unidade (você indicou 30–50 por unidade).",
        "Levantar quais já têm detecção de PATINAGEM e quais NÃO têm.",
        "Levantar quais têm DETECÇÃO DE FAGULHA e o tipo de sensor existente.",
        "Mapear pontos de transferência/chutes (onde entra fagulha) e correias longas (onde entra LHD).",
        "Mapear correias que ainda NÃO são antichama (cruzar com o plano de troca Continental em andamento).",
        "Diagnóstico de housekeeping de poeira e cotação com fornecedores de despoeiramento.",
    ],
    "Engenharia/consultoria ~ R$ 50 mil a R$ 120 mil (ou execução interna pelo PCM).")

fase_slide(
    7, "FASE 1 — PRIORIDADE MÁXIMA", "Atacar a causa raiz dos grãos",
    "2–6 meses",
    [
        "Completar DETECÇÃO DE PATINAGEM (zero-speed) nos elevadores/correias faltantes, integrada ao PLC com parada segura.",
        "Instalar TEMPERATURA DE MANCAL online nos elevadores e polias críticas (hoje o monitoramento varia/não há) — alarme + intertravamento.",
        "Acelerar a troca por CORREIA ANTICHAMA Continental (programa já em andamento).",
        "Reforçar a PERMISSÃO DE TRABALHO A QUENTE: vigia de fogo, isolamento, proteção do recheio/correia — com auditoria (hoje há negligências).",
        "Programa de HOUSEKEEPING / despoeiramento nos pontos de acúmulo (reduz risco de explosão).",
    ],
    "~ R$ 650 mil em sensores (base 200 equip.) + housekeeping a cotar + correias (programa existente).")

fase_slide(
    8, "FASE 2", "Detecção e supressão",
    "6–18 meses",
    [
        "DETECÇÃO DE FAGULHA (GreCon ou Firefly) nos pontos de transferência críticos de grãos e nos transportadores da caldeira.",
        "CABO DE DETECÇÃO LINEAR DE CALOR (LHD) ao longo das correias longas (Protectowire/Securiton).",
        "TORRES: proteção do recheio durante serviço + estudo de dilúvio/água-névoa; tratar como item de trabalho a quente.",
        "Detecção de CO / autoaquecimento onde aplicável na armazenagem.",
        "Supressão por água (extinção de fagulha) acionando PARADA SEGURA automática.",
    ],
    "Ordem de R$ 2 a 3 milhões no programa (sistemas cotados por projeto).")

fase_slide(
    9, "FASE 3", "Automação, integração e gestão",
    "12–24 meses",
    [
        "Integrar todos os sensores e detecções ao SCADA / Rockwell (FactoryTalk) com tela única de status de segurança.",
        "Dashboards e KPIs de confiabilidade (MTBF, MTTR, disponibilidade, % calibração em dia).",
        "Termografia FIXA Ex nos pontos críticos (chutes, mancais, CCM) já anunciando no supervisório (como já existe na caldeira).",
        "Plano de calibração e CMMS para registrar inspeção/troca de roletes (substituir o controle manual).",
        "Avaliar conformidade NR-13 da caldeira (gerenciador de chama/BMS) — fora da prioridade de incêndio atual.",
    ],
    "Ordem de R$ 0,5 a 1 milhão no programa.")

# =====================================================================
# SLIDE 10 — PARADA DE EMERGENCIA / BOTOEIRA
# =====================================================================
s = add_slide()
header(s, "SEGURANÇA DE MÁQUINAS", "Parada de emergência em esteiras longas")
bullets(s, Inches(0.5), Inches(1.45), Inches(12.3), Inches(3.6), [
    "Em correia longa NÃO se usa botoeira espaçada por distância — usa-se CHAVE DE EMERGÊNCIA POR CABO (pull-cord / trip-wire).",
    "NR-12 (transportadores contínuos): o dispositivo deve ser acionável AO LONGO DE TODA A EXTENSÃO. Botoeira pontual não atende; o cabo atende.",
    "ABNT NBR ISO 13850: o acionador deve estar acessível de QUALQUER ponto de circulação.",
    "Prática: cabo dos dois lados onde há circulação; cada chave cobre ~80–100 m de cabo.",
    ("Esteira de 120–150 m → tipicamente 2 chaves (uma de cada extremidade) ou 1 central.", 1),
    "Resultado: a 'distância a percorrer' tende a ZERO — o operador puxa o cabo no ponto onde está.",
], size=15, gap=8)
rect(s, Inches(0.5), Inches(5.7), Inches(12.3), Inches(1.0), CINZA_CLARO)
txt(s, Inches(0.7), Inches(5.7), Inches(12), Inches(1.0),
    "Atenção: se a sua dúvida for distância de fuga até o SOLO em passarela elevada, o critério é outro "
    "(rota de fuga / escadas de acesso) — definir após confirmar o layout das passarelas.",
    size=13, bold=True, color=AZUL, anchor=MSO_ANCHOR.MIDDLE)
footer(s, 10)

# =====================================================================
# SLIDE 11 — FORNECEDORES RECOMENDADOS
# =====================================================================
s = add_slide()
header(s, "FORNECEDORES", "Tecnologia × fornecedor recomendado")
rows = [
    ["Tecnologia", "Fornecedor ideal", "Custo de referência"],
    ["Patinagem / velocidade / alinhamento / temp. mancal", "4B Braime (Go4B), Electro-Sensors", "~ R$ 2.500 / sensor (compra+instal.)"],
    ["Detecção de fagulha (spark detection)", "GreCon (Fagus-GreCon), Firefly", "Sistema por projeto (US$ 30–80k)"],
    ["Cabo linear de calor (LHD) / DTS fibra", "Protectowire, Securiton; AP Sensing/Bandweaver (DTS)", "Cabo + painel por correia"],
    ["Correia antichama", "Continental (ContiTech) — em andamento", "Programa existente"],
    ["Termografia (preditiva / fixa Ex)", "FLIR (Teledyne), Fluke", "Portátil R$ 15–40k; fixa por ponto"],
    ["Chave de emergência por cabo", "Steute, Bernstein, Rees, IFM", "~ R$ 3–8k / chave"],
]
table(s, Inches(0.5), Inches(1.5), Inches(12.3), rows,
      [0.40, 0.34, 0.26], fsize=11.5, row_h=Inches(0.66))
footer(s, 11)

# =====================================================================
# SLIDE 12 — CAPEX CONSOLIDADO
# =====================================================================
s = add_slide()
header(s, "INVESTIMENTO", "CAPEX estimado por fase (programa 4–6 unidades)")
rows = [
    ["Fase", "Escopo principal", "CAPEX estimado"],
    ["Fase 0", "Diagnóstico / levantamento de sensores", "R$ 50 – 120 mil"],
    ["Fase 1", "Causa raiz grãos (patinagem, temp. mancal, PT, poeira)", "~ R$ 650 mil + housekeeping a cotar"],
    ["Fase 2", "Detecção de fagulha + LHD + torres + supressão", "R$ 2 – 3 milhões"],
    ["Fase 3", "Automação, integração SCADA, KPIs, termografia fixa", "R$ 0,5 – 1 milhão"],
    ["TOTAL", "Programa completo, faseado, replicável nas unidades", "Ordem de R$ 5 – 9 milhões"],
]
t = table(s, Inches(0.5), Inches(1.6), Inches(12.3), rows,
          [0.12, 0.58, 0.30], fsize=13, row_h=Inches(0.7))
# destacar linha total
for ci in range(3):
    cell = t.cell(len(rows) - 1, ci)
    cell.fill.solid()
    cell.fill.fore_color.rgb = AZUL
    cell.text_frame.paragraphs[0].runs[0].font.color.rgb = BRANCO
    cell.text_frame.paragraphs[0].runs[0].font.bold = True
txt(s, Inches(0.5), Inches(6.5), Inches(12.3), Inches(0.7),
    "Estimativas preliminares (ordem de grandeza) com base em 200 equipamentos (≈40 × 5 unidades) e R$ 2.500/sensor. "
    "Valores de sistemas (fagulha, supressão) exigem cotação por projeto.",
    size=11, color=VERMELHO)
footer(s, 12)

# =====================================================================
# SLIDE 13 — NORMAS
# =====================================================================
s = add_slide()
header(s, "CONFORMIDADE", "Normas e referências aplicáveis")
bullets(s, Inches(0.5), Inches(1.5), Inches(6.1), Inches(5.0), [
    "NR-12 — Segurança em máquinas (transportadores, parada de emergência).",
    "NR-13 — Caldeiras e vasos de pressão.",
    "NR-23 — Proteção contra incêndios.",
    "NR-33 / NR-35 — Espaço confinado / trabalho em altura.",
], size=15, gap=12)
bullets(s, Inches(6.8), Inches(1.5), Inches(6.0), Inches(5.0), [
    "ABNT NBR ISO 13850 — Parada de emergência.",
    "ABNT NBR ISO 13849 / IEC 62061 — PL/SIL de segurança.",
    "ABNT NBR IEC 60079 — Atmosferas explosivas (Ex), destilaria.",
    "NFPA 61 / 654 — Poeira combustível (grãos).",
], size=15, gap=12)
footer(s, 13)

# =====================================================================
# SLIDE 14 — ROADMAP
# =====================================================================
s = add_slide()
header(s, "EXECUÇÃO", "Roadmap")
fases = [
    ("FASE 0\nDiagnóstico", "0–2 m", VERDE),
    ("FASE 1\nCausa raiz grãos", "2–6 m", VERMELHO),
    ("FASE 2\nDetecção/supressão", "6–18 m", LARANJA),
    ("FASE 3\nAutomação/gestão", "12–24 m", AZUL_CLARO),
]
x = Inches(0.6)
w = Inches(2.95)
for titulo, prazo, cor in fases:
    rect(s, x, Inches(2.4), w, Inches(1.7), cor)
    txt(s, x, Inches(2.5), w, Inches(1.1), titulo, size=16, bold=True,
        color=BRANCO, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x, Inches(3.55), w, Inches(0.5), prazo, size=13,
        color=BRANCO, align=PP_ALIGN.CENTER)
    x = Emu(int(x) + int(w) + Inches(0.13))
txt(s, Inches(0.6), Inches(4.6), Inches(12), Inches(1.5),
    "As fases podem rodar em paralelo entre unidades. Recomenda-se iniciar a Fase 1 numa unidade-piloto, "
    "validar resultados e replicar nas demais (4–6 unidades).",
    size=15, color=CINZA)
footer(s, 14)

# =====================================================================
# SLIDE 15 — PROXIMOS PASSOS
# =====================================================================
s = add_slide()
header(s, "DECISÕES", "Próximos passos")
bullets(s, Inches(0.5), Inches(1.5), Inches(12.3), Inches(5.0), [
    "Aprovar a Fase 0 (diagnóstico) e definir a unidade-piloto.",
    "Confirmar número exato de equipamentos por unidade para fechar o CAPEX.",
    "Confirmar marcas para padronização: controlador Rockwell, sensores Sense, posicionadores (SMAR?), válvulas Bray.",
    "Definir responsável (PCM/Automação/SESMT) e cronograma de levantamento de sensores.",
    "Selecionar fornecedores de fagulha (GreCon × Firefly) e disparar cotações.",
    "Auditar e reforçar o processo de Permissão de Trabalho a Quente (ação de custo baixo e alto impacto).",
], size=16, gap=10)
footer(s, 15)

out = "/home/user/ICG2025/plano_seguranca/Plano_Acao_Seguranca_INPASA.pptx"
prs.save(out)
print("OK:", out, "| slides:", len(prs.slides._sldIdLst))
