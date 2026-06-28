# -*- coding: utf-8 -*-
"""
Gerador da apresentacao executiva:
"DataOps na Prática: IA a Serviço da Alta Gestão"
Comparativo Optix + DataMosaix vs. PlantPAx + TracOS (Inpasa)
Publico: Sr. José e Éder.

Tudo nativo (formas, tabelas e graficos do PowerPoint) -> 100% editavel.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.chart.data import CategoryChartData
from pptx.oxml.ns import qn

# ----------------------------------------------------------------------------
# Paleta
# ----------------------------------------------------------------------------
NAVY      = RGBColor(0x10, 0x2A, 0x43)   # fundo escuro / titulos
SLATE     = RGBColor(0x33, 0x4E, 0x68)   # texto secundario
GRAY      = RGBColor(0x62, 0x7D, 0x98)   # texto auxiliar
LIGHT     = RGBColor(0xF4, 0xF7, 0xFA)   # fundo claro
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
GREEN     = RGBColor(0x16, 0x9C, 0x52)   # Inpasa / acerto
GREEN_DK  = RGBColor(0x0E, 0x6B, 0x37)
OPTIX     = RGBColor(0x25, 0x63, 0xEB)   # azul Optix
OPTIX_DK  = RGBColor(0x1A, 0x44, 0xA8)
AMBER     = RGBColor(0xF5, 0x9E, 0x0B)   # laranja DataMosaix
AMBER_DK  = RGBColor(0xB4, 0x71, 0x05)
RED       = RGBColor(0xD9, 0x3A, 0x3A)   # alerta / hoje
CARD      = RGBColor(0xFF, 0xFF, 0xFF)
LINE      = RGBColor(0xD9, 0xE2, 0xEC)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
PG=[0]
def slide():
    PG[0]+=1
    return prs.slides.add_slide(BLANK)

def picture(s, path, x, y, w, h):
    return s.shapes.add_picture(path, x, y, width=w, height=h)

def image_slide(kicker, title, accent, intro, img, caption):
    s = slide(); bg(s, LIGHT)
    header(s, kicker, title, accent)
    txt(s, Inches(0.85), Inches(1.42), Inches(11.6), Inches(0.45),
        [[R(intro, 14, SLATE, False)]])
    rect(s, Inches(2.66), Inches(1.87), Inches(8.02), Inches(4.56), fill=WHITE, line=LINE, line_w=1, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
    picture(s, img, Inches(2.76), Inches(1.95), Inches(7.82), Inches(4.4))
    txt(s, Inches(0.85), Inches(6.55), Inches(11.6), Inches(0.5),
        [[R(caption, 12.5, GRAY, False)]], align=PP_ALIGN.CENTER)
    page_num(s)

def bg(s, color):
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = color

def rect(s, x, y, w, h, fill=None, line=None, line_w=0.75, shape=MSO_SHAPE.RECTANGLE,
         shadow=False):
    sp = s.shapes.add_shape(shape, x, y, w, h)
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    if shadow:
        el = sp._element.spPr
        ef = el.makeelement(qn('a:effectLst'), {})
        sh = ef.makeelement(qn('a:outerShdw'),
                            {'blurRad':'90000','dist':'40000','dir':'5400000','rotWithShape':'0'})
        clr = sh.makeelement(qn('a:srgbClr'), {'val':'1B2A3A'})
        alpha = clr.makeelement(qn('a:alpha'), {'val':'24000'})
        clr.append(alpha); sh.append(clr); ef.append(sh); el.append(ef)
    return sp

def txt(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        wrap=True, space_after=4):
    """runs: list of paragraphs; each paragraph is list of (text, size, color, bold, italic)"""
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after); p.space_before = Pt(0)
        for (t, sz, col, b, it) in para:
            r = p.add_run(); r.text = t
            r.font.size = Pt(sz); r.font.color.rgb = col
            r.font.bold = b; r.font.italic = it
            r.font.name = "Calibri"
    return tb

def R(t, sz, col, b=False, it=False):
    return (t, sz, col, b, it)

def bullets(s, x, y, w, h, items, size=15, color=SLATE, gap=8, marker_col=GREEN,
            anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap); p.space_before = Pt(0); p.line_spacing = 1.05
        # marker
        rm = p.add_run(); rm.text = "▪  "
        rm.font.size = Pt(size); rm.font.color.rgb = marker_col; rm.font.bold = True
        rm.font.name = "Calibri"
        if isinstance(it, tuple):
            head, rest = it
            r1 = p.add_run(); r1.text = head
            r1.font.size = Pt(size); r1.font.color.rgb = NAVY; r1.font.bold = True; r1.font.name="Calibri"
            r2 = p.add_run(); r2.text = rest
            r2.font.size = Pt(size); r2.font.color.rgb = color; r2.font.name="Calibri"
        else:
            r = p.add_run(); r.text = it
            r.font.size = Pt(size); r.font.color.rgb = color; r.font.name="Calibri"
    return tb

def header(s, kicker, title, accent=GREEN):
    """Cabecalho padrao de slide de conteudo (fundo claro)."""
    rect(s, 0, 0, SW, Inches(1.25), fill=WHITE)
    rect(s, 0, Inches(1.25), SW, Pt(2.2), fill=accent)
    rect(s, Inches(0.55), Inches(0.34), Inches(0.14), Inches(0.62), fill=accent)
    txt(s, Inches(0.85), Inches(0.30), Inches(11.6), Inches(0.3),
        [[R(kicker.upper(), 11.5, accent, True)]])
    txt(s, Inches(0.85), Inches(0.55), Inches(11.9), Inches(0.6),
        [[R(title, 25, NAVY, True)]])

def page_num(s):
    txt(s, Inches(12.4), Inches(7.05), Inches(0.8), Inches(0.3),
        [[R(str(PG[0]), 10, GRAY, False)]], align=PP_ALIGN.RIGHT)
    txt(s, Inches(0.85), Inches(7.05), Inches(6), Inches(0.3),
        [[R("Inpasa  ·  Gestão Estratégica de Automação", 9, GRAY, False)]])

def chip(s, x, y, label, fill, tcol=WHITE, w=Inches(1.9), h=Inches(0.34), size=11):
    sp = rect(s, x, y, w, h, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    sp.adjustments[0] = 0.5
    tf = sp.text_frame; tf.word_wrap = True
    tf.margin_top=Pt(1); tf.margin_bottom=Pt(1)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label; r.font.size = Pt(size); r.font.bold = True
    r.font.color.rgb = tcol; r.font.name = "Calibri"
    return sp

# ----------------------------------------------------------------------------
# 1. CAPA
# ----------------------------------------------------------------------------
s = slide(); bg(s, NAVY)
# faixa decorativa
rect(s, 0, 0, Inches(0.22), SH, fill=GREEN)
rect(s, Inches(0.22), 0, Inches(0.08), SH, fill=OPTIX)
# selo superior
chip(s, Inches(0.9), Inches(0.85), "GESTÃO ESTRATÉGICA  ·  AUTOMAÇÃO & DADOS",
     fill=RGBColor(0x1B,0x3A,0x57), w=Inches(4.6), h=Inches(0.42), size=12)
txt(s, Inches(0.9), Inches(2.0), Inches(11.4), Inches(2.2),
    [[R("DataOps na Prática:", 46, WHITE, True)],
     [R("IA a Serviço da Alta Gestão", 46, GREEN, True)]])
txt(s, Inches(0.92), Inches(3.95), Inches(11.0), Inches(1.0),
    [[R("Evolução da plataforma de automação da Inpasa  —  ", 19, RGBColor(0xCD,0xDA,0xE8), False),
      R("FactoryTalk Optix + DataMosaix", 19, OPTIX, True),
      R("  vs.  ", 19, RGBColor(0xCD,0xDA,0xE8), False),
      R("PlantPAx + TracOS", 19, AMBER, True)]])
# linha divisoria
rect(s, Inches(0.95), Inches(5.15), Inches(6.4), Pt(1.5), fill=RGBColor(0x35,0x52,0x70))
txt(s, Inches(0.95), Inches(5.2), Inches(11.6), Inches(1.5),
    [[R("Apresentado a:  ", 14, GRAY, False), R("Sr. José  e  Éder", 14, WHITE, True),
      R("      por  ", 14, GRAY, False), R("Itiel Gonçalves · VP Automação & Elétrica", 14, WHITE, True)],
     [R("Centro de Operações Integradas (COI)  ·  Benchmarking entre plantas  ·  Manutenção prescritiva", 13, GRAY, False)],
     [R("Base: sessão estratégica Inpasa × Rockwell  ·  Mayfield Heights, OH  ·  26/06/2026", 12.5, RGBColor(0x8F,0xA9,0xC2), False)]])
txt(s, Inches(9.8), Inches(6.75), Inches(2.7), Inches(0.4),
    [[R("2026.06.28  ·  MULTI  ·  vFINAL", 12, GRAY, True)]], align=PP_ALIGN.RIGHT)

# ----------------------------------------------------------------------------
# 2. CONTEXTO / POR QUE AGORA
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Contexto", "Por que olhar para isso agora", GREEN)
txt(s, Inches(0.85), Inches(1.55), Inches(11.6), Inches(0.9),
    [[R("A Inpasa cresceu de planta única para uma ", 16, SLATE, False),
      R("operação multi-unidades", 16, NAVY, True),
      R(" (Sinop, Nova Mutum, Dourados, Balsas, Sidrolândia e novas plantas). ", 16, SLATE, False),
      R("Os dados existem — mas vivem isolados dentro de cada planta.", 16, NAVY, True)]])
cards = [
    ("Reunião estratégica", "Encontro Inpasa x Rockwell (26/06) sobre parceria de tecnologia e inovação. Contato: Dan DeYoung (VP & GM, Design & Control).", OPTIX),
    ("Dados em silos", "Cada unidade tem seu PlantPAx adaptado às necessidades e padrões da Inpasa. Não há visão única, nem comparação direta entre as plantas.", AMBER),
    ("Decisão reativa", "Manutenção parcialmente reativa (TracOS cobre rotativos) e alarmes acima da norma — falta prescritivo e não rotativos.", RED),
    ("Janela de oportunidade", "Optix e DataMosaix amadureceram em 2026 (SCADA multi-site + Industrial DataOps).", GREEN),
]
cw = Inches(2.85); gap = Inches(0.2); x0 = Inches(0.85); y0 = Inches(2.75); ch = Inches(3.0)
for i,(t,d,c) in enumerate(cards):
    x = x0 + i*(cw+gap)
    rect(s, x, y0, cw, ch, fill=CARD, line=LINE, line_w=1, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
    rect(s, x, y0, cw, Inches(0.12), fill=c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, x+Inches(0.25), y0+Inches(0.35), cw-Inches(0.5), Inches(0.7),
        [[R(t, 16, c, True)]])
    txt(s, x+Inches(0.25), y0+Inches(1.05), cw-Inches(0.5), Inches(1.8),
        [[R(d, 13, SLATE, False)]])
txt(s, Inches(0.85), Inches(6.1), Inches(11.6), Inches(0.7),
    [[R("Pergunta central:  ", 15, NAVY, True),
      R("como transformar o dado que já geramos em decisão executiva, comparável entre plantas e antecipada por IA?", 15, SLATE, False, True)]])
page_num(s)

# ----------------------------------------------------------------------------
# 2b. REUNIAO ESTRATEGICA INPASA x ROCKWELL
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Parceria estratégica", "Inpasa × Rockwell — leitura da sessão de 26/06/2026", OPTIX)
txt(s, Inches(0.85), Inches(1.5), Inches(11.6), Inches(0.55),
    [[R("Encontro executivo no campus da Rockwell (Mayfield Heights, OH). A Inpasa apresentou seus objetivos de automação; a Rockwell trouxe a visão de COI, DataOps e IA industrial.", 14, SLATE, False)]])
_x=Inches(0.85); _y=Inches(2.2); _cw=Inches(5.75); _ch=Inches(4.3); _g=Inches(0.35)
rect(s, _x, _y, _cw, _ch, fill=CARD, line=LINE, line_w=1, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
rect(s, _x, _y, _cw, Inches(0.62), fill=OPTIX, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, _x+Inches(0.3), _y+Inches(0.13), _cw-Inches(0.6), Inches(0.4), [[R("Agenda da sessão", 16, WHITE, True)]])
bullets(s, _x+Inches(0.35), _y+Inches(0.85), _cw-Inches(0.7), Inches(3.3), [('Inpasa Goals & Objectives ', '— Itiel Gonçalves'), ('Trusted Partnership & Ecosystem ', "— Andrew D'Souza"), ('Process Characterization & Lab Tour ', '— Ed Walsh'), ('Software Leadership: COI & DataOps ', '— JP Wright'), ('Hardware Leadership: Process Initiative ', '— Brian Widman'), ('Strategic Plan & Executive Wrap-up ', "— Andrew D'Souza")], size=13, marker_col=OPTIX, gap=10)
_x1=_x+_cw+_g
rect(s, _x1, _y, _cw, _ch, fill=CARD, line=LINE, line_w=1, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
rect(s, _x1, _y, _cw, Inches(0.62), fill=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, _x1+Inches(0.3), _y+Inches(0.13), _cw-Inches(0.6), Inches(0.4), [[R("Quem participou", 16, WHITE, True)]])
bullets(s, _x1+Inches(0.35), _y+Inches(0.85), _cw-Inches(0.7), Inches(3.3), [('Itiel Gonçalves ', '— VP Automação & Elétrica (Inpasa)'), ('Dan DeYoung ', '— VP & GM, Design & Control'), ("Andrew D'Souza ", '— Diretor Software & Control, LATAM'), ('JP Wright ', '— Diretor Visualization & Production Data'), ('Brian Widman ', '— PM Controllers · Chris Stearns — PlantPAx PM'), ('Lúcio Granato ', '— Solution Architect (time Brasil)')], size=13, marker_col=NAVY, gap=10)
page_num(s)

# ----------------------------------------------------------------------------
# 3b. COMO O MUNDO ESTA MUDANDO (imagem)
# ----------------------------------------------------------------------------
image_slide("Por que agora · contexto de mercado", "Como o mundo da automação está mudando", OPTIX, "Da convergência IT/OT à automação definida por software e à IA — a régua subiu.", "assets/ai_progression.png", "Evolução da IA industrial: de regras e sistemas especialistas a machine learning, IA generativa, agentes de IA e frameworks agênticos — com aceleração acentuada.")

# ----------------------------------------------------------------------------
# 3. ONDE ESTAMOS HOJE (PlantPAx + TracOS)
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Cenário atual", "O que a Inpasa já tem hoje", AMBER)
# dois cards grandes
x0=Inches(0.85); y0=Inches(1.7); cw=Inches(5.75); ch=Inches(3.7); gap=Inches(0.35)
# PlantPAx
rect(s, x0, y0, cw, ch, fill=CARD, line=LINE, line_w=1, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
rect(s, x0, y0, cw, Inches(0.7), fill=AMBER, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, x0+Inches(0.3), y0+Inches(0.13), cw-Inches(0.6), Inches(0.5),
    [[R("PlantPAx", 19, WHITE, True), R("   supervisório por planta", 13, WHITE, False)]])
bullets(s, x0+Inches(0.35), y0+Inches(0.95), cw-Inches(0.7), Inches(2.6), [
    ("DCS/SCADA Rockwell ", "rodando em cada unidade"),
    ("PlantPAx parcial ", "diversos blocos (P_PID, P_VALVE, P_INTLK), parte customizados à Inpasa"),
    ("Dados nativos ", "modo Auto/Manual, Operador/Programa, interlocks"),
    ("Alarmes & Events ", "alarmes não reconhecidos já rastreados"),
], size=13.5, marker_col=AMBER, gap=9)
# TracOS
x1 = x0+cw+gap
rect(s, x1, y0, cw, ch, fill=CARD, line=LINE, line_w=1, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
rect(s, x1, y0, cw, Inches(0.7), fill=SLATE, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, x1+Inches(0.3), y0+Inches(0.13), cw-Inches(0.6), Inches(0.5),
    [[R("TracOS", 19, WHITE, True), R("   manutenção preditiva", 13, WHITE, False)]])
bullets(s, x1+Inches(0.35), y0+Inches(0.95), cw-Inches(0.7), Inches(2.6), [
    ("TracOS (Tractian) ", "monitoramento preditivo de rotativos"),
    ("Evita falhas ", "em média 5–6 por planta, com antecedência"),
    ("Ordens de serviço ", "e gestão de ativos por unidade"),
    ("Lacuna ", "não cobre não rotativos nem prescritivo"),
], size=13.5, marker_col=SLATE, gap=9)
txt(s, Inches(0.85), Inches(5.7), Inches(11.6), Inches(1.0),
    [[R("Resumo:  ", 15, NAVY, True),
      R("temos dados ricos e uma base Rockwell robusta. O que falta não é coletar — e ", 14.5, SLATE, False),
      R("contextualizar, comparar entre plantas e antecipar com IA.", 14.5, NAVY, True)]])
page_num(s)

# ----------------------------------------------------------------------------
# 4. A LACUNA
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Diagnóstico", "As 4 lacunas que travam a decisão executiva", RED)
gaps = [
    ("Silos por planta", "O dado fica preso em cada PlantPAx. Não existe uma visão única nem ranking entre unidades."),
    ("Sem benchmarking", "Sem comparar entre Sinop, Nova Mutum, Dourados, Balsas e Sidrolândia o índice de alarmes, de malhas em automático, de blocos em programa, de interlocks desativados e de variáveis simuladas."),
    ("Parcialmente reativa", "TracOS já evita 5–6 falhas/planta em rotativos. Falta cobrir equipamentos não rotativos e dar insight prescritivo para eles."),
    ("Excesso de alarmes", "Média do setor: 30+ alarmes/operador/hora (5x acima da ISA-18.2); ~70% são nuisance alarms."),
]
x0=Inches(0.85); y0=Inches(1.7); cw=Inches(5.75); ch=Inches(2.35); gx=Inches(0.35); gy=Inches(0.35)
for i,(t,d) in enumerate(gaps):
    r,c = divmod(i,2)
    x = x0 + c*(cw+gx); y = y0 + r*(ch+gy)
    rect(s, x, y, cw, ch, fill=CARD, line=LINE, line_w=1, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
    badge = rect(s, x+Inches(0.3), y+Inches(0.3), Inches(0.55), Inches(0.55),
                 fill=RED, shape=MSO_SHAPE.OVAL)
    tfb = badge.text_frame; tfb.paragraphs[0].alignment=PP_ALIGN.CENTER
    rb = tfb.paragraphs[0].add_run(); rb.text=str(i+1); rb.font.bold=True; rb.font.size=Pt(18); rb.font.color.rgb=WHITE; rb.font.name="Calibri"
    txt(s, x+Inches(1.05), y+Inches(0.33), cw-Inches(1.4), Inches(0.5),
        [[R(t, 18, NAVY, True)]])
    txt(s, x+Inches(0.32), y+Inches(1.05), cw-Inches(0.64), Inches(1.2),
        [[R(d, 13.5, SLATE, False)]])
page_num(s)

# ----------------------------------------------------------------------------
# 5. ARQUITETURA PROPOSTA (camadas)
# ----------------------------------------------------------------------------
s = slide(); bg(s, NAVY)
rect(s, 0, 0, SW, Inches(1.15), fill=NAVY)
rect(s, Inches(0.55), Inches(0.32), Inches(0.14), Inches(0.55), fill=GREEN)
txt(s, Inches(0.85), Inches(0.26), Inches(11.6), Inches(0.3),
    [[R("VISÃO DE ARQUITETURA", 11.5, GREEN, True)]])
txt(s, Inches(0.85), Inches(0.5), Inches(11.9), Inches(0.6),
    [[R("Do sensor à diretoria: as 4 camadas do dado", 25, WHITE, True)]])
layers = [
    ("4", "DECISÃO  ·  COI", "Dashboards únicos, benchmarking entre plantas, alertas e ranking em tempo real", GREEN),
    ("3", "EXECUÇÃO INTELIGENTE  ·  FactoryTalk Optix + ResilientEdge", "HMI/SCADA multi-site, edge resiliente, loop fechado com IA, acesso remoto", OPTIX),
    ("2", "DataOps + IA  ·  FactoryTalk DataMosaix + Atlas AI", "Contextualiza OT/IT/ET, RCA automatizada, agentes no-code, prescritivo", AMBER),
    ("1", "EDGE / OT  ·  PlantPAx + sensores + Tractian (o que já temos)", "Controladores, blocos, alarmes e monitoramento de rotativos (Tractian) por planta", SLATE),
]
y0=Inches(1.5); lh=Inches(1.18); gap=Inches(0.16); x0=Inches(1.1); lw=Inches(10.2)
for i,(n,t,d,c) in enumerate(layers):
    y = y0 + i*(lh+gap)
    rect(s, x0, y, lw, lh, fill=RGBColor(0x17,0x33,0x4E), line=c, line_w=1.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s, x0, y, Inches(1.0), lh, fill=c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, x0, y, Inches(1.0), lh, [[R(n,30,WHITE,True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x0+Inches(1.25), y+Inches(0.18), lw-Inches(1.5), Inches(0.45),
        [[R(t, 16.5, WHITE, True)]])
    txt(s, x0+Inches(1.25), y+Inches(0.62), lw-Inches(1.5), Inches(0.5),
        [[R(d, 12.5, RGBColor(0xB9,0xCA,0xDB), False)]])
# seta ascendente
arrow = rect(s, x0+lw+Inches(0.25), y0, Inches(0.7), lh*4+gap*3, fill=GREEN, shape=MSO_SHAPE.UP_ARROW)
txt(s, x0+lw+Inches(0.05), y0+lh*4+gap*3+Inches(0.05), Inches(1.1), Inches(0.4),
    [[R("valor", 11, GREEN, True)]], align=PP_ALIGN.CENTER)
page_num(s)

# ----------------------------------------------------------------------------
# 6. FACTORYTALK OPTIX + RESILIENTEDGE
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Camada de execução", "FactoryTalk Optix + ResilientEdge", OPTIX)
txt(s, Inches(0.85), Inches(1.5), Inches(11.6), Inches(0.7),
    [[R("De HMI para a ", 16, SLATE, False),
      R("base de execução inteligente", 16, OPTIX, True),
      R(" da Rockwell: HMI/SCADA cloud-enabled, projetada e implantada pelo navegador.", 16, SLATE, False)]])
feats = [
    ("SCADA multi-site (2026)", "Centraliza o supervisório de todas as plantas em uma plataforma, com redundância de servidor e workstation clients."),
    ("ResilientEdge", "Execução edge resiliente + analytics em nuvem, treino de IA e orquestração corporativa. Disponível global desde 18/06/2026."),
    ("Acesso remoto", "FactoryTalk Remote Access via VPN: investigar e resolver antes de viajar à planta remota."),
    ("Aberto / OPC UA", "Comunica nativamente com controladores Rockwell e de terceiros; roda em qualquer hardware."),
]
x0=Inches(0.85); y0=Inches(2.35); cw=Inches(5.75); ch=Inches(1.75); gx=Inches(0.35); gy=Inches(0.3)
for i,(t,d) in enumerate(feats):
    r,c=divmod(i,2); x=x0+c*(cw+gx); y=y0+r*(ch+gy)
    rect(s,x,y,cw,ch,fill=CARD,line=LINE,line_w=1,shape=MSO_SHAPE.ROUNDED_RECTANGLE,shadow=True)
    rect(s,x,y,Inches(0.1),ch,fill=OPTIX)
    txt(s,x+Inches(0.32),y+Inches(0.2),cw-Inches(0.6),Inches(0.5),[[R(t,16,OPTIX_DK,True)]])
    txt(s,x+Inches(0.32),y+Inches(0.72),cw-Inches(0.6),Inches(0.95),[[R(d,13,SLATE,False)]])
chip(s, Inches(0.85), Inches(6.35), "Para a Inpasa: o caminho natural do COI centralizado multi-planta",
     fill=OPTIX, w=Inches(7.6), h=Inches(0.5), size=13)
page_num(s)

# ----------------------------------------------------------------------------
# 6b. OPTIX AI DESIGN ASSISTANCE (imagem)
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Camada de execução · FactoryTalk Optix", "Optix AI Design Assistance — HMI assistido por IA", OPTIX)
txt(s, Inches(0.85), Inches(1.45), Inches(11.6), Inches(0.45),
    [[R("Projetar e implantar telas com apoio de IA: do rascunho à aplicação funcional.", 14, SLATE, False)]])
rect(s, Inches(2.66), Inches(1.87), Inches(8.02), Inches(4.56), fill=WHITE, line=LINE, line_w=1, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
picture(s, "assets/optix_ai_design.png", Inches(2.76), Inches(1.95), Inches(7.82), Inches(4.4))
txt(s, Inches(0.85), Inches(6.55), Inches(11.6), Inches(0.5),
    [[R("Gera telas a partir de Figma, foto ou rascunho à mão; conteúdo por texto conversacional; auto-geração de modelos e conectividade — releases v1.8 a v1.9 (2026).", 12.5, GRAY, False)]], align=PP_ALIGN.CENTER)
page_num(s)

# ----------------------------------------------------------------------------
# 6c. INDUSTRIAL DATAOPS (imagem)
# ----------------------------------------------------------------------------
image_slide("Camada de DataOps + IA", "Industrial DataOps — um hub para OT, IT e ET", AMBER, "Em vez de integrações ponto a ponto, um hub central contextualiza e reaproveita o dado.", "assets/industrial_dataops_hub.png", "O hub industrial consolida dados de OT, IT e ET com contextualização, modelos, qualidade e catálogo — reutilizáveis por várias aplicações e pela IA.")

# ----------------------------------------------------------------------------
# 7. FACTORYTALK DATAMOSAIX + ATLAS AI
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Camada de DataOps + IA", "FactoryTalk DataMosaix + Atlas AI", AMBER)
txt(s, Inches(0.85), Inches(1.5), Inches(11.6), Inches(0.35),
    [[R("Industrial DataOps do edge à nuvem: ", 14.5, AMBER_DK, True),
      R("contextualiza dados de operação, engenharia e TI para casos de uso de IA.", 14.5, SLATE, False)]])
feats = [
    ("RCA automatizada", "Análise de causa raiz sem precisar de um analista de dados dedicado.",
     "ao parar uma planta, o agente cruza alarmes, malhas e histórico e aponta a causa provável em segundos."),
    ("Manutenção prescritiva", "Detecta desgaste precoce e recomenda a ação antes da parada custosa.",
     "a posição real de uma válvula de controle passa a divergir do percentual comandado além do histórico — tendência de desgaste sinalizada antes da falha."),
    ("Agentes de IA contextuais", "Monitoram variáveis de processo e geram alertas contextualizados.",
     "exatamente o que o Hub de Automação está construindo — alerta quando uma malha foge do padrão da planta."),
    ("No-code", "A equipe de automação cria fluxos e agentes seguros sem programar.",
     "monta e ajusta os fluxos do DataMosaix sem depender de TI nem de código."),
]
x0=Inches(0.85); w=Inches(11.6); y0=Inches(1.98); rh=Inches(1.12); gap=Inches(0.12)
for i,(t,d,ex) in enumerate(feats):
    y=y0+i*(rh+gap)
    rect(s,x0,y,w,rh,fill=CARD,line=LINE,line_w=1,shape=MSO_SHAPE.ROUNDED_RECTANGLE,shadow=True)
    rect(s,x0,y,Inches(0.1),rh,fill=AMBER)
    txt(s,x0+Inches(0.32),y+Inches(0.12),w-Inches(0.7),Inches(0.32),[[R(t,16,AMBER_DK,True)]])
    txt(s,x0+Inches(0.32),y+Inches(0.45),w-Inches(0.7),Inches(0.26),[[R(d,12.5,SLATE,False)]])
    txt(s,x0+Inches(0.32),y+Inches(0.72),w-Inches(0.7),Inches(0.38),
        [[R("Ex. Inpasa:  ", 12, AMBER_DK, True, True), R(ex, 12, SLATE, False, True)]])
page_num(s)

# ----------------------------------------------------------------------------
# 7b. DATAMOSAIX ATLAS AI (imagem)
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Camada de DataOps + IA · FactoryTalk DataMosaix", "DataMosaix Atlas AI — agentes autônomos na operação", AMBER)
txt(s, Inches(0.85), Inches(1.45), Inches(11.6), Inches(0.45),
    [[R("Inteligência humana e agentes autônomos atuando em conjunto na operação industrial.", 14, SLATE, False)]])
rect(s, Inches(2.66), Inches(1.87), Inches(8.02), Inches(4.56), fill=WHITE, line=LINE, line_w=1, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
picture(s, "assets/datamosaix_atlas_ai.png", Inches(2.76), Inches(1.95), Inches(7.82), Inches(4.4))
txt(s, Inches(0.85), Inches(6.55), Inches(11.6), Inches(0.5),
    [[R("Agentes que decidem e agem com base em metas de negócio para aumentar produção e eliminar paradas, desperdício e risco; gêmeo digital que se aprimora continuamente.", 12.5, GRAY, False)]], align=PP_ALIGN.CENTER)
page_num(s)

# ----------------------------------------------------------------------------
# 8. COMPARATIVO HOJE vs PROPOSTO (tabela)
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Comparativo", "Hoje (PlantPAx + TracOS)  vs.  Proposto (Optix + DataMosaix)", GREEN)
rows = [
    ("Capacidade", "Hoje", "Com Optix + DataMosaix"),
    ("Supervisório", "Por planta, isolado", "Multi-site centralizado (SCADA Optix)"),
    ("Visão entre plantas", "Inexistente / manual", "Dashboards únicos e comparáveis"),
    ("Padrão de HMI", "PlantPAx parcial / customizado", "PlantPAx 2026 + ISA-101"),
    ("Manutenção", "Preditiva em rotativos (TracOS)", "Prescritiva, incl. não rotativos"),
    ("Causa raiz", "Investigação manual", "RCA automatizada por agente de IA"),
    ("Alarmes", "Acima da ISA-18.2", "Benchmarking e redução de nuisance"),
    ("Acesso remoto", "Via VPN (já temos)", "Mantém VPN + Remote Access (Optix)"),
    ("IT / OT / ET", "Silos", "Convergência em plataforma única"),
]
tx=Inches(0.85); ty=Inches(1.7); tw=Inches(11.6); rh=Inches(0.56)
colw=[Inches(3.0), Inches(4.0), Inches(4.6)]
y=ty
for ri,row in enumerate(rows):
    x=tx
    head = (ri==0)
    for ci,cell in enumerate(row):
        if head:
            fill = NAVY if ci==0 else (RED if ci==1 else GREEN)
        else:
            fill = WHITE if ri%2 else RGBColor(0xEC,0xF2,0xF7)
        cellsp = rect(s, x, y, colw[ci], rh, fill=fill, line=LINE, line_w=0.5)
        tf=cellsp.text_frame; tf.word_wrap=True
        tf.margin_left=Pt(8); tf.margin_right=Pt(6); tf.vertical_anchor=MSO_ANCHOR.MIDDLE
        p=tf.paragraphs[0]; p.alignment=PP_ALIGN.LEFT
        rr=p.add_run(); rr.text=cell
        rr.font.size=Pt(13 if not head else 13.5)
        rr.font.bold = head or ci==0
        if head: rr.font.color.rgb=WHITE
        elif ci==0: rr.font.color.rgb=NAVY
        elif ci==1: rr.font.color.rgb=SLATE
        else: rr.font.color.rgb=GREEN_DK
        rr.font.name="Calibri"
        x += colw[ci]
    y += rh
page_num(s)

# ----------------------------------------------------------------------------
# 9. ALARMES ISA-18.2 (grafico)
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Benchmarking de alarmes", "A norma ISA-18.2 e a oportunidade imediata", RED)
# grafico de barras
chart_data = CategoryChartData()
chart_data.categories = ["Limite ISA-18.2\n(máximo)", "Média do setor\n(hoje)", "Meta Inpasa\nno COI"]
chart_data.add_series("Alarmes por operador / hora", (6, 30, 6))
gx, gy, gw, gh = Inches(0.85), Inches(1.7), Inches(6.4), Inches(4.3)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, gx, gy, gw, gh, chart_data)
chart = gf.chart
chart.has_legend = False
chart.has_title = True
chart.chart_title.text_frame.text = "Alarmes por operador / hora"
chart.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(13)
chart.chart_title.text_frame.paragraphs[0].runs[0].font.color.rgb = NAVY
plot = chart.plots[0]
plot.has_data_labels = True
plot.data_labels.number_format = '0'
plot.data_labels.number_format_is_linked = False
plot.data_labels.font.size = Pt(14); plot.data_labels.font.bold=True
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
plot.gap_width = 60
ser = plot.series[0]
for idx, pt in enumerate(ser.points):
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = GREEN if idx in (0,2) else RED
cat_ax = chart.category_axis; cat_ax.tick_labels.font.size=Pt(11)
val_ax = chart.value_axis; val_ax.has_major_gridlines=True
val_ax.tick_labels.font.size=Pt(10)
# texto lateral
txt(s, Inches(7.55), Inches(1.85), Inches(5.0), Inches(0.6),
    [[R("5x acima do recomendado", 20, RED, True)]])
bullets(s, Inches(7.55), Inches(2.65), Inches(5.0), Inches(3.2), [
    "Planta bem gerenciada: < 6 alarmes/operador/hora em operação normal.",
    "Média das plantas: 30+ por operador/hora — cinco vezes o máximo.",
    "~70% dos alarmes em DCS/SCADA típicos são nuisance (não exigem ação).",
    ("Grafana (já implantado) ", "trata nuisance alarms, bad actors e alarm floods sobre o PlantPAx adaptado — base que já operamos hoje."),
], size=13.5, marker_col=RED, gap=11)
page_num(s)

# ----------------------------------------------------------------------------
# 9b. ANALISE DE ALARMES COM IA (imagem)
# ----------------------------------------------------------------------------
image_slide("Benchmarking de alarmes · IA", "Análise de alarmes assistida por IA", RED, "A análise histórica de alarmes que propomos já existe nas ferramentas FactoryTalk.", "assets/ftview_ai_alarms.png", "O FactoryTalk View AI responde perguntas como 'os 10 alarmes mais frequentes nos últimos 60 dias' — o tipo de insight que sustenta o ranking ISA-18.2 no COI.")

# ----------------------------------------------------------------------------
# 10. KPIs DE BENCHMARKING (tabela)
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Indicadores", "KPIs de benchmarking que o ecossistema já mede", GREEN)
rows = [
    ("KPI", "Ferramenta", "Disponível hoje?"),
    ("Alarmes por operador/hora", "Grafana (hoje) + DataMosaix", "Sim — sobre PlantPAx adaptado"),
    ("Alarmes não reconhecidos", "FT Alarms & Events", "Nativo"),
    ("Controles em Auto / Manual", "PlantPAx P_PID, P_VALVE", "Dado já no controlador"),
    ("Blocos Operador / Programa", "PlantPAx Command Source", "Campo nativo"),
    ("Interlocks desabilitados", "PlantPAx P_Gate + P_INTLK", "Rastreável"),
    ("Variáveis simuladas", "Tag audit via Studio 5000", "Possível"),
    ("Bad actors / nuisance", "Grafana (hoje)", "Sim — PlantPAx adaptado"),
    ("Benchmarking entre plantas", "DataMosaix (multi-site)", "Novidade que entra agora"),
]
tx=Inches(0.85); ty=Inches(1.62); rh=Inches(0.5)
colw=[Inches(4.3), Inches(4.3), Inches(3.0)]
y=ty
for ri,row in enumerate(rows):
    x=tx; head=(ri==0); last=(ri==len(rows)-1)
    for ci,cell in enumerate(row):
        if head: fill=NAVY
        elif last: fill=GREEN
        else: fill = WHITE if ri%2 else RGBColor(0xEC,0xF2,0xF7)
        cellsp=rect(s,x,y,colw[ci],rh,fill=fill,line=LINE,line_w=0.5)
        tf=cellsp.text_frame; tf.word_wrap=True
        tf.margin_left=Pt(8); tf.margin_right=Pt(6); tf.vertical_anchor=MSO_ANCHOR.MIDDLE
        p=tf.paragraphs[0]
        rr=p.add_run(); rr.text=cell; rr.font.size=Pt(12.5)
        rr.font.bold = head or ci==0 or last
        if head or last: rr.font.color.rgb=WHITE
        elif ci==0: rr.font.color.rgb=NAVY
        else: rr.font.color.rgb=SLATE
        rr.font.name="Calibri"
        x+=colw[ci]
    y+=rh
txt(s, Inches(0.85), Inches(6.75), Inches(11.6), Inches(0.4),
    [[R("Quase tudo já existe no dado atual — falta a camada que agrega e compara: o DataMosaix.", 13, GRAY, False, True)]])
page_num(s)

# ----------------------------------------------------------------------------
# 11. O QUE O DATAMOSAIX ADICIONA
# ----------------------------------------------------------------------------
s = slide(); bg(s, NAVY)
rect(s, Inches(0.55), Inches(0.32), Inches(0.14), Inches(0.55), fill=AMBER)
txt(s, Inches(0.85), Inches(0.26), Inches(11.6), Inches(0.3),
    [[R("O DELTA", 11.5, AMBER, True)]])
txt(s, Inches(0.85), Inches(0.5), Inches(11.9), Inches(0.6),
    [[R("O que o DataMosaix adiciona ao que já temos", 25, WHITE, True)]])
txt(s, Inches(0.85), Inches(1.45), Inches(11.6), Inches(0.7),
    [[R("Hoje o dado vive dentro de cada PlantPAx. O DataMosaix é a camada que ", 15.5, RGBColor(0xC8,0xD6,0xE4), False),
      R("agrega, contextualiza e compara", 15.5, AMBER, True),
      R(" — uma visão única de toda a operação.", 15.5, RGBColor(0xC8,0xD6,0xE4), False)]])
adds = [
    ("Indicadores comparáveis", "Alarmes/operador·hora, % de malhas em automático, blocos em programa, interlocks e variáveis simuladas — além do OEE — por planta, num só painel."),
    ("Planejamento enterprise", "Decisão de produção, manutenção e ações estratégicas em nível corporativo — visão consolidada da companhia, não por site isolado."),
    ("Visão multi-site", "Sinop, Nova Mutum, Dourados, Balsas, Sidrolândia e novas plantas, lado a lado, na mesma régua."),
    ("Contexto OT + IT + ET", "Une OT (processo / chão de fábrica), IT (sistemas corporativos / ERP) e ET (engenharia / ativos) num só contexto pronto para a IA."),
]
x0=Inches(0.85); y0=Inches(2.45); cw=Inches(2.85); ch=Inches(2.9); gap=Inches(0.2)
for i,(t,d) in enumerate(adds):
    x=x0+i*(cw+gap)
    rect(s,x,y0,cw,ch,fill=RGBColor(0x17,0x33,0x4E),line=AMBER,line_w=1.2,shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s,x,y0,cw,Inches(0.1),fill=AMBER,shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s,x+Inches(0.25),y0+Inches(0.38),cw-Inches(0.5),Inches(0.85),[[R(t,16.5,WHITE,True)]])
    txt(s,x+Inches(0.25),y0+Inches(1.2),cw-Inches(0.5),Inches(1.6),[[R(d,12.5,RGBColor(0xB9,0xCA,0xDB),False)]])
page_num(s)

# ----------------------------------------------------------------------------
# 12. CASOS DE USO NO COI (Inpasa)
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Aplicação direta", "Como isso aparece no COI da Inpasa", GREEN)
cases = [
    ("Tela única em tempo real", "Indicadores ao vivo por planta, lado a lado: % de malhas em automático, índice de alarmes/operador·hora, blocos em programa, interlocks e variáveis simuladas.", GREEN),
    ("Ranking de plantas", "Ordena as unidades pelos mesmos indicadores — quem está dentro e fora da ISA-18.2 — destacando boa prática e quem precisa de atenção.", OPTIX),
    ("Alertas automáticos", "Disparo ao cruzar o limite (ex.: 6 alarmes/operador·hora) — notificação por WhatsApp, e-mail ou o canal que o gestor preferir.", RED),
    ("Comparativo histórico", "Revela divergências por turno e antes/depois de parada, além de outros padrões — insights para operação e manutenção.", AMBER),
]
x0=Inches(0.85); y0=Inches(1.75); cw=Inches(5.75); ch=Inches(2.3); gx=Inches(0.35); gy=Inches(0.35)
for i,(t,d,c) in enumerate(cases):
    r,col=divmod(i,2); x=x0+col*(cw+gx); y=y0+r*(ch+gy)
    rect(s,x,y,cw,ch,fill=CARD,line=LINE,line_w=1,shape=MSO_SHAPE.ROUNDED_RECTANGLE,shadow=True)
    badge=rect(s,x+Inches(0.3),y+Inches(0.3),Inches(0.6),Inches(0.6),fill=c,shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    badge.adjustments[0]=0.3
    tfb=badge.text_frame; tfb.paragraphs[0].alignment=PP_ALIGN.CENTER
    rb=tfb.paragraphs[0].add_run(); rb.text=str(i+1); rb.font.bold=True; rb.font.size=Pt(20); rb.font.color.rgb=WHITE; rb.font.name="Calibri"
    txt(s,x+Inches(1.1),y+Inches(0.35),cw-Inches(1.45),Inches(0.9),[[R(t,17,NAVY,True)]])
    txt(s,x+Inches(0.32),y+Inches(1.08),cw-Inches(0.64),Inches(1.15),[[R(d,12.5,SLATE,False)]])
page_num(s)

# ----------------------------------------------------------------------------
# 12b. EVOLUCAO DO PLANTPAX (imagem)
# ----------------------------------------------------------------------------
image_slide("Modernização · plataforma", "Evolução do PlantPAx — do adaptado ao PlantPAx 2026", GREEN, "Não trocar a base: evoluir o PlantPAx adaptado de hoje para a direção 2026 da Rockwell.", "assets/plantpax_direction.png", "Direção 2026: integração com FactoryTalk Optix, arquitetura multi-node, +20 conectores, design em nuvem e Software Defined Automation — com Provisioning que reduz o deploy a 1–2 semanas.")

# ----------------------------------------------------------------------------
# 13. ROADMAP / DISPONIBILIDADE
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Roadmap", "Como evolui — do que já temos ao COI prescritivo", OPTIX)
phases = [
    ("Fase 1", "Já implementado", """Benchmarking de alarmes e KPIs já rodam hoje no Grafana — que já temos e está implantado — sobre o PlantPAx adaptado. Base pronta; o equivalente Rockwell (VantagePoint) não é necessário para começar.""", GREEN),
    ("Fase 2", "Preditivo", """O DataMosaix estende o monitoramento preditivo aos equipamentos não rotativos — os rotativos já são cobertos pela Tractian — e agrega as plantas em dashboards comparativos.""", AMBER),
    ("Fase 3", "Prescritivo + COI", """Em simulações de paradas em vários sites, com o COI centralizado a retomada das plantas ficou mais estável, rápida e otimizada — operação e manutenção. Com o time central treinando os sites, é possível até evitar desarmes.""", OPTIX),
]
x0=Inches(0.85); y0=Inches(1.9); cw=Inches(3.75); ch=Inches(3.5); gap=Inches(0.18)
for i,(l1,l2,d,c) in enumerate(phases):
    x=x0+i*(cw+gap)
    rect(s,x,y0,cw,ch,fill=CARD,line=c,line_w=1.5,shape=MSO_SHAPE.ROUNDED_RECTANGLE,shadow=True)
    rect(s,x,y0,cw,Inches(0.95),fill=c,shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s,x+Inches(0.3),y0+Inches(0.12),cw-Inches(0.6),Inches(0.8),[[R(l1,14,WHITE,False)],[R(l2,20,WHITE,True)]])
    txt(s,x+Inches(0.32),y0+Inches(1.15),cw-Inches(0.62),Inches(2.25),[[R(d,12.5,SLATE,False)]])
    if i<2:
        rect(s,x+cw-Inches(0.05),y0+ch/2-Inches(0.2),Inches(0.4),Inches(0.4),fill=c,shape=MSO_SHAPE.CHEVRON)
chip(s, Inches(0.85), Inches(5.7), "ResilientEdge: disponível global desde 18/06/2026  ·  SCADA multi-site em rollout 2026",
     fill=NAVY, w=Inches(9.0), h=Inches(0.5), size=13)
page_num(s)

# ----------------------------------------------------------------------------
# 13b. AMBICAO DA INPASA
# ----------------------------------------------------------------------------
s = slide(); bg(s, NAVY)
rect(s, 0, 0, Inches(0.22), SH, fill=GREEN)
rect(s, Inches(0.22), 0, Inches(0.08), SH, fill=OPTIX)
txt(s, Inches(0.9), Inches(0.7), Inches(11.6), Inches(0.4), [[R("A AMBIÇÃO DA INPASA", 12, GREEN, True)]])
txt(s, Inches(0.9), Inches(1.15), Inches(11.5), Inches(1.7),
    [[R("Ser referência em ", 34, WHITE, True), R("automação inteligente", 34, GREEN, True)],
     [R("na América Latina.", 34, WHITE, True)]])
txt(s, Inches(0.92), Inches(3.05), Inches(11.3), Inches(0.8),
    [[R("Não por status — mas pela vontade de gerar resultado para a companhia com tecnologia de ponta: mais produção, menos perdas e decisão baseada em dado.", 15, RGBColor(0xCD,0xDA,0xE8), False)]])
_p=[('Otimizar produção', 'visibilidade e decisão em tempo real'), ('Empoderar pessoas', 'operação e manutenção com apoio de IA'), ('Construir resiliência', 'menos paradas, retomadas mais estáveis'), ('Acelerar a transformação', 'do dado à ação, planta a planta')]
_x=Inches(0.9); _y=Inches(4.05); _cw=Inches(2.85); _ch=Inches(2.45); _g=Inches(0.18)
for _i,(_t,_d) in enumerate(_p):
    _xx=_x+_i*(_cw+_g)
    rect(s,_xx,_y,_cw,_ch,fill=RGBColor(0x17,0x33,0x4E),line=GREEN,line_w=1.2,shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s,_xx,_y,_cw,Inches(0.1),fill=GREEN,shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s,_xx+Inches(0.25),_y+Inches(0.35),_cw-Inches(0.5),Inches(0.9),[[R(_t,16,WHITE,True)]])
    txt(s,_xx+Inches(0.25),_y+Inches(1.25),_cw-Inches(0.5),Inches(1.0),[[R(_d,12.5,RGBColor(0xB9,0xCA,0xDB),False)]])

# ----------------------------------------------------------------------------
# 14. PROXIMOS PASSOS
# ----------------------------------------------------------------------------
s = slide(); bg(s, LIGHT)
header(s, "Decisão", "O que pedimos para avançar", GREEN)
steps = [
    ("Aprovar o piloto", """Começar por 1–2 indicadores em todas as plantas (ex.: controles em automático e índice de alarmes/operador·hora), ampliando depois para os demais. Estimativa: ~4–6 semanas para os 2 primeiros, conforme o volume de tags por unidade."""),
    ("Sequência de indicadores", """Controles em automático e índice de alarmes primeiro; depois blocos em programa, interlocks desabilitados e variáveis simuladas."""),
    ("Interlocutores Rockwell", """Time EUA: Andrew D'Souza (Software & Control LATAM), JP Wright (Visualization & Production Data), Brian Widman (Controllers), Chris Stearns (PlantPAx). Time Brasil: Lúcio Granato e Marcel. Anfitrião: Dan DeYoung (VP & GM, Design & Control)."""),
    ("Designar squad interno", """Gestores e equipe do Hub de Automação conduzindo os fluxos no-code do DataMosaix."""),
]
y0=Inches(1.7); rh=Inches(1.24); x0=Inches(0.85); w=Inches(11.6)
for i,(t,d) in enumerate(steps):
    y=y0+i*(rh+Inches(0.08))
    rect(s,x0,y,w,rh,fill=CARD,line=LINE,line_w=1,shape=MSO_SHAPE.ROUNDED_RECTANGLE,shadow=True)
    badge=rect(s,x0+Inches(0.3),y+Inches(0.34),Inches(0.55),Inches(0.55),fill=GREEN,shape=MSO_SHAPE.OVAL)
    tfb=badge.text_frame; tfb.paragraphs[0].alignment=PP_ALIGN.CENTER
    rb=tfb.paragraphs[0].add_run(); rb.text=str(i+1); rb.font.bold=True; rb.font.size=Pt(18); rb.font.color.rgb=WHITE; rb.font.name="Calibri"
    txt(s,x0+Inches(1.1),y+Inches(0.16),w-Inches(1.4),Inches(0.45),[[R(t,16,NAVY,True)]])
    txt(s,x0+Inches(1.1),y+Inches(0.6),w-Inches(1.4),Inches(0.6),[[R(d,12,SLATE,False)]])
page_num(s)

# ----------------------------------------------------------------------------
# 15. ENCERRAMENTO
# ----------------------------------------------------------------------------
s = slide(); bg(s, NAVY)
rect(s, 0, 0, Inches(0.22), SH, fill=GREEN)
rect(s, Inches(0.22), 0, Inches(0.08), SH, fill=OPTIX)
txt(s, Inches(1.0), Inches(2.3), Inches(11.2), Inches(2.2),
    [[R("O dado já existe.", 40, WHITE, True)],
     [R("Falta transformá-lo em decisão.", 40, GREEN, True)]])
txt(s, Inches(1.02), Inches(4.4), Inches(11.0), Inches(1.0),
    [[R("Optix + DataMosaix conectam o que a Inpasa já tem (PlantPAx + TracOS) a um COI único,", 17, RGBColor(0xCD,0xDA,0xE8), False)],
     [R("com benchmarking entre plantas e IA prescritiva — começando pelo ganho rápido.", 17, RGBColor(0xCD,0xDA,0xE8), False)]])
rect(s, Inches(1.05), Inches(5.7), Inches(5.5), Pt(1.5), fill=RGBColor(0x35,0x52,0x70))
txt(s, Inches(1.05), Inches(5.9), Inches(11), Inches(0.8),
    [[R("Gestão Estratégica de Automação  ·  Inpasa  ·  2026.06.28", 13, GRAY, True)]])

# ----------------------------------------------------------------------------
import os
out = "2026.06.28 - MULTI - DataOps na Prática IA a Serviço da Alta Gestão vFINAL.pptx"
prs.save(out)
print("OK ->", out, "| slides:", len(prs.slides._sldIdLst))
