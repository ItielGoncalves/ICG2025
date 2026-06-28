# -*- coding: utf-8 -*-
"""
Renderiza o MESMO deck "DataOps na Prática" em PDF (reportlab), espelhando o
layout do gerador .pptx. Usado para exportar o PDF vFINAL quando o LibreOffice
não está disponível no ambiente.

Uso:
    python scripts/gerar_pdf_dataops.py "saida.pdf"
"""
import sys
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import HexColor

IN = 72.0
PW, PH = 13.333, 7.5            # polegadas
PWp, PHp = PW * IN, PH * IN

# ---- paleta (hex, iguais ao .pptx) ----
NAVY="#102A43"; SLATE="#334E68"; GRAY="#627D98"; LIGHT="#F4F7FA"; WHITE="#FFFFFF"
GREEN="#169C52"; GREEN_DK="#0E6B37"; OPTIX="#2563EB"; OPTIX_DK="#1A44A8"
AMBER="#F59E0B"; AMBER_DK="#B47105"; RED="#D93A3A"; CARD="#FFFFFF"; LINE="#D9E2EC"
NAVY_CARD="#17334E"; LAYER_DESC="#B9CADB"; COVER_SUB="#CDDAE8"; DIVIDER="#355270"
SEAL="#1B3A57"; SHADOW="#E3E8EE"; GRID="#DCE5EE"

out = sys.argv[1] if len(sys.argv) > 1 else "deck.pdf"
c = canvas.Canvas(out, pagesize=(PWp, PHp))

# ----------------------------------------------------------------------------
def esc(t):
    return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def run_markup(run):
    t, sz, col, b, it = run
    inner = esc(t)
    if it: inner = f"<i>{inner}</i>"
    if b:  inner = f"<b>{inner}</b>"
    return f'<font size="{sz}" color="{col}">{inner}</font>'

def R(t, sz, col, b=False, it=False):
    return (t, sz, col, b, it)

def rect(x, y, w, h, fill=None, line=None, line_w=0.75, rounded=False, radius=6):
    """x,y = canto superior-esquerdo em polegadas (origem no topo)."""
    rx = x*IN; ry = (PH - y - h)*IN; rw = w*IN; rh = h*IN
    if fill: c.setFillColor(HexColor(fill))
    if line:
        c.setStrokeColor(HexColor(line)); c.setLineWidth(line_w)
    do_fill = 1 if fill else 0
    do_stroke = 1 if line else 0
    if rounded:
        c.roundRect(rx, ry, rw, rh, radius, stroke=do_stroke, fill=do_fill)
    else:
        c.rect(rx, ry, rw, rh, stroke=do_stroke, fill=do_fill)

def card(x, y, w, h, fill=CARD, line=LINE, line_w=1, radius=8, shadow=True):
    if shadow:
        sx=x+0.035; sy=y+0.045
        c.setFillColor(HexColor(SHADOW))
        c.roundRect(sx*IN, (PH-sy-h)*IN, w*IN, h*IN, radius, stroke=0, fill=1)
    rect(x, y, w, h, fill=fill, line=line, line_w=line_w, rounded=True, radius=radius)

def make_para(runs, align=TA_LEFT, space_after=3, ls=1.18, indent=0, hang=0):
    maxsize = max(r[1] for r in runs)
    style = ParagraphStyle('p', fontName='Helvetica', fontSize=maxsize,
                           leading=maxsize*ls, alignment=align,
                           spaceAfter=space_after, leftIndent=indent,
                           firstLineIndent=hang)
    return Paragraph("".join(run_markup(r) for r in runs), style)

def paras(x, y, w, h, lines, align=TA_LEFT, anchor='top', space_after=3, ls=1.18):
    """lines: lista de paragrafos; cada paragrafo = lista de runs."""
    ps = [make_para(rs, align, space_after, ls) for rs in lines]
    avail = w*IN
    if anchor == 'middle':
        tot = 0
        for p in ps:
            tot += p.wrap(avail, 100000)[1]
        tot += space_after*(len(ps)-1)
        fh = tot + 2
        top_eff = y + (h - fh/IN)/2
        bottom = (PH - top_eff - fh/IN)*IN
        height = fh
    else:
        bottom = (PH - y - h)*IN
        height = h*IN
    fr = Frame(x*IN, bottom, avail, height, leftPadding=0, rightPadding=0,
               topPadding=0, bottomPadding=0, showBoundary=0)
    fr.addFromList(ps, c)

def bullets(x, y, w, h, items, size=14, color=SLATE, gap=8, marker=GREEN):
    ps = []
    for it in items:
        runs = [("•  ", size, marker, True, False)]
        if isinstance(it, tuple):
            head, rest = it
            runs.append((head, size, NAVY, True, False))
            runs.append((rest, size, color, False, False))
        else:
            runs.append((it, size, color, False, False))
        style = ParagraphStyle('b', fontName='Helvetica', fontSize=size,
                               leading=size*1.2, alignment=TA_LEFT,
                               spaceAfter=gap, leftIndent=14, firstLineIndent=-14)
        ps.append(Paragraph("".join(run_markup(r) for r in runs), style))
    fr = Frame(x*IN, (PH-y-h)*IN, w*IN, h*IN, leftPadding=0, rightPadding=0,
               topPadding=0, bottomPadding=0, showBoundary=0)
    fr.addFromList(ps, c)

def circle(cx, cy, r, fill):
    c.setFillColor(HexColor(fill))
    c.circle(cx*IN, (PH-cy)*IN, r*IN, stroke=0, fill=1)

def header(kicker, title, accent=GREEN):
    rect(0, 0, PW, 1.25, fill=WHITE)
    rect(0, 1.25, PW, 2.2/IN, fill=accent)
    rect(0.55, 0.34, 0.14, 0.62, fill=accent)
    paras(0.85, 0.30, 11.6, 0.3, [[R(kicker.upper(), 11.5, accent, True)]])
    paras(0.85, 0.55, 11.9, 0.6, [[R(title, 25, NAVY, True)]])

def page_num(n):
    paras(11.6, 7.05, 0.93, 0.3, [[R(str(n), 10, GRAY)]], align=TA_RIGHT)
    paras(0.85, 7.05, 7, 0.3, [[R("Inpasa  ·  Gestão Estratégica de Automação", 9, GRAY)]])

def chip(x, y, label, fill, tcol=WHITE, w=1.9, h=0.34, size=11):
    rect(x, y, w, h, fill=fill, rounded=True, radius=h*IN/2)
    paras(x, y, w, h, [[R(label, size, tcol, True)]], align=TA_CENTER, anchor='middle')

def page_bg(color):
    rect(0, 0, PW, PH, fill=color)

# ----------------------------------------------------------------------------
# 1. CAPA
# ----------------------------------------------------------------------------
page_bg(NAVY)
rect(0, 0, 0.22, PH, fill=GREEN)
rect(0.22, 0, 0.08, PH, fill=OPTIX)
chip(0.9, 0.85, "GESTÃO ESTRATÉGICA  ·  AUTOMAÇÃO & DADOS", fill=SEAL, w=4.6, h=0.42, size=12)
paras(0.9, 2.0, 11.4, 2.2,
      [[R("DataOps na Prática:", 46, WHITE, True)],
       [R("IA a Serviço da Alta Gestão", 46, GREEN, True)]], ls=1.1, space_after=6)
paras(0.92, 3.95, 11.0, 1.0,
      [[R("Evolução da plataforma de automação da Inpasa  —  ", 19, COVER_SUB),
        R("FactoryTalk Optix + DataMosaix", 19, OPTIX, True),
        R("  vs.  ", 19, COVER_SUB),
        R("PlantPAx + TracOS", 19, AMBER, True)]])
rect(0.95, 5.15, 6.4, 1.5/IN, fill=DIVIDER)
paras(0.95, 5.35, 11, 1.2,
      [[R("Apresentado a:  ", 14, GRAY), R("Sr. José  e  Éder", 14, WHITE, True)],
       [R("Centro de Operações Integradas (COI)  ·  Benchmarking entre plantas  ·  Manutenção prescritiva", 13, GRAY)]],
      space_after=5)
paras(9.6, 6.75, 2.9, 0.4, [[R("2026.06.28  ·  MULTI  ·  v02", 12, GRAY, True)]], align=TA_RIGHT)
c.showPage()

# ----------------------------------------------------------------------------
# 2. CONTEXTO
# ----------------------------------------------------------------------------
page_bg(LIGHT)
header("Contexto", "Por que olhar para isso agora", GREEN)
paras(0.85, 1.55, 11.6, 0.9,
      [[R("A Inpasa cresceu de planta única para uma ", 16, SLATE),
        R("operação multi-unidades", 16, NAVY, True),
        R(" (Sinop, Nova Mutum, Dourados, Balsas, Sidrolândia e novas plantas). ", 16, SLATE),
        R("Os dados existem — mas vivem isolados dentro de cada planta.", 16, NAVY, True)]])
cards2 = [
    ("Reunião estratégica", "Encontro Inpasa x Rockwell (26/06) sobre parceria de tecnologia e inovação. Contato: Dan DeYoung (VP executivo).", OPTIX),
    ("Dados em silos", "Cada unidade tem seu PlantPAx. Não há visão única nem comparação direta entre plantas.", AMBER),
    ("Decisão reativa", "Manutenção parcialmente reativa (TracOS cobre rotativos) e alarmes acima da norma — falta prescritivo e não rotativos.", RED),
    ("Janela de oportunidade", "Optix e DataMosaix amadureceram em 2026 (SCADA multi-site + Industrial DataOps).", GREEN),
]
cw=2.85; gap=0.2; x0=0.85; y0=2.75; ch=3.0
for i,(t,d,col) in enumerate(cards2):
    x=x0+i*(cw+gap)
    card(x, y0, cw, ch)
    rect(x, y0, cw, 0.12, fill=col, rounded=True, radius=4)
    paras(x+0.25, y0+0.35, cw-0.5, 0.7, [[R(t, 16, col, True)]])
    paras(x+0.25, y0+1.05, cw-0.5, 1.8, [[R(d, 13, SLATE)]])
paras(0.85, 6.1, 11.6, 0.7,
      [[R("Pergunta central:  ", 15, NAVY, True),
        R("como transformar o dado que já geramos em decisão executiva, comparável entre plantas e antecipada por IA?", 15, SLATE, False, True)]])
page_num(2); c.showPage()

# ----------------------------------------------------------------------------
# 3. HOJE
# ----------------------------------------------------------------------------
page_bg(LIGHT)
header("Cenário atual", "O que a Inpasa já tem hoje", AMBER)
x0=0.85; y0=1.7; cw=5.75; ch=3.7; gap=0.35
card(x0, y0, cw, ch)
rect(x0, y0, cw, 0.7, fill=AMBER, rounded=True, radius=8)
rect(x0, y0+0.35, cw, 0.35, fill=AMBER)
paras(x0+0.3, y0+0.13, cw-0.6, 0.5, [[R("PlantPAx", 19, WHITE, True), R("   supervisório por planta", 13, WHITE)]])
bullets(x0+0.35, y0+0.95, cw-0.7, 2.6, [
    ("DCS/SCADA Rockwell ", "rodando em cada unidade"),
    ("PlantPAx parcial ", "diversos blocos (P_PID, P_VALVE, P_INTLK), parte customizados à Inpasa"),
    ("Dados nativos ", "modo Auto/Manual, Operador/Programa, interlocks"),
    ("Alarmes & Events ", "alarmes não reconhecidos já rastreados"),
], size=13.5, marker=AMBER, gap=9)
x1=x0+cw+gap
card(x1, y0, cw, ch)
rect(x1, y0, cw, 0.7, fill=SLATE, rounded=True, radius=8)
rect(x1, y0+0.35, cw, 0.35, fill=SLATE)
paras(x1+0.3, y0+0.13, cw-0.6, 0.5, [[R("TracOS", 19, WHITE, True), R("   manutenção preditiva", 13, WHITE)]])
bullets(x1+0.35, y0+0.95, cw-0.7, 2.6, [
    ("TracOS (Tractian) ", "monitoramento preditivo de rotativos"),
    ("Evita falhas ", "em média 5–6 por planta, com antecedência"),
    ("Ordens de serviço ", "e gestão de ativos por unidade"),
    ("Lacuna ", "não cobre não rotativos nem prescritivo"),
], size=13.5, marker=SLATE, gap=9)
paras(0.85, 5.7, 11.6, 1.0,
      [[R("Resumo:  ", 15, NAVY, True),
        R("temos dados ricos e uma base Rockwell robusta. O que falta não é coletar — e ", 14.5, SLATE),
        R("contextualizar, comparar entre plantas e antecipar com IA.", 14.5, NAVY, True)]])
page_num(3); c.showPage()

# ----------------------------------------------------------------------------
# 4. LACUNAS
# ----------------------------------------------------------------------------
page_bg(LIGHT)
header("Diagnóstico", "As 4 lacunas que travam a decisão executiva", RED)
gaps = [
    ("Silos por planta", "O dado fica preso em cada PlantPAx. Não existe uma visão única nem ranking entre unidades."),
    ("Sem benchmarking", "Sem comparar entre Sinop, Nova Mutum, Dourados, Balsas e Sidrolândia o índice de alarmes, de malhas em automático, de blocos em programa, de interlocks desativados e de variáveis simuladas."),
    ("Parcialmente reativa", "TracOS já evita 5–6 falhas/planta em rotativos. Falta cobrir equipamentos não rotativos e dar insight prescritivo para eles."),
    ("Excesso de alarmes", "Média do setor: 30+ alarmes/operador/hora (5x acima da ISA-18.2); ~70% são nuisance alarms."),
]
x0=0.85; y0=1.7; cw=5.75; ch=2.35; gx=0.35; gy=0.35
for i,(t,d) in enumerate(gaps):
    r,cc=divmod(i,2); x=x0+cc*(cw+gx); y=y0+r*(ch+gy)
    card(x, y, cw, ch)
    circle(x+0.3+0.275, y+0.3+0.275, 0.275, RED)
    paras(x+0.3, y+0.3, 0.55, 0.55, [[R(str(i+1), 18, WHITE, True)]], align=TA_CENTER, anchor='middle')
    paras(x+1.05, y+0.33, cw-1.4, 0.5, [[R(t, 18, NAVY, True)]])
    paras(x+0.32, y+1.05, cw-0.64, 1.2, [[R(d, 13.5, SLATE)]])
page_num(4); c.showPage()

# ----------------------------------------------------------------------------
# 5. ARQUITETURA
# ----------------------------------------------------------------------------
page_bg(NAVY)
rect(0.55, 0.32, 0.14, 0.55, fill=GREEN)
paras(0.85, 0.26, 11.6, 0.3, [[R("VISÃO DE ARQUITETURA", 11.5, GREEN, True)]])
paras(0.85, 0.5, 11.9, 0.6, [[R("Do sensor à diretoria: as 4 camadas do dado", 25, WHITE, True)]])
layers = [
    ("4", "DECISÃO  ·  COI", "Dashboards únicos, benchmarking entre plantas, alertas e ranking em tempo real", GREEN),
    ("3", "EXECUÇÃO INTELIGENTE  ·  FactoryTalk Optix + ResilientEdge", "HMI/SCADA multi-site, edge resiliente, loop fechado com IA, acesso remoto", OPTIX),
    ("2", "DataOps + IA  ·  FactoryTalk DataMosaix + Atlas AI", "Contextualiza OT/IT/ET, RCA automatizada, agentes no-code, prescritivo", AMBER),
    ("1", "EDGE / OT  ·  PlantPAx + sensores + Tractian (o que já temos)", "Controladores, blocos, alarmes e monitoramento de rotativos (Tractian) por planta", SLATE),
]
y0=1.5; lh=1.18; gap=0.16; x0=1.1; lw=10.2
for i,(n,t,d,col) in enumerate(layers):
    y=y0+i*(lh+gap)
    rect(x0, y, lw, lh, fill=NAVY_CARD, line=col, line_w=1.5, rounded=True, radius=8)
    rect(x0, y, 1.0, lh, fill=col, rounded=True, radius=8)
    rect(x0+0.5, y, 0.5, lh, fill=col)
    paras(x0, y, 1.0, lh, [[R(n, 30, WHITE, True)]], align=TA_CENTER, anchor='middle')
    paras(x0+1.25, y+0.18, lw-1.5, 0.45, [[R(t, 16.5, WHITE, True)]])
    paras(x0+1.25, y+0.62, lw-1.5, 0.5, [[R(d, 12.5, LAYER_DESC)]])
# seta ascendente
ax=x0+lw+0.25; aw=0.7; ay=y0; ah=lh*4+gap*3
cxp=(ax+aw/2)*IN; head_b=ay+1.0; sw=0.34
pts=[(ax+aw/2, ay),(ax, head_b),(ax+aw/2-sw/2, head_b),(ax+aw/2-sw/2, ay+ah),
     (ax+aw/2+sw/2, ay+ah),(ax+aw/2+sw/2, head_b),(ax+aw, head_b)]
p=c.beginPath();
p.moveTo(pts[0][0]*IN,(PH-pts[0][1])*IN)
for (xx,yy) in pts[1:]:
    p.lineTo(xx*IN,(PH-yy)*IN)
p.close()
c.setFillColor(HexColor(GREEN)); c.drawPath(p, stroke=0, fill=1)
paras(x0+lw+0.05, y0+ah+0.05, 1.1, 0.4, [[R("valor", 11, GREEN, True)]], align=TA_CENTER)
page_num(5); c.showPage()

# ----------------------------------------------------------------------------
# 6. OPTIX
# ----------------------------------------------------------------------------
page_bg(LIGHT)
header("Camada de execução", "FactoryTalk Optix + ResilientEdge", OPTIX)
paras(0.85, 1.5, 11.6, 0.7,
      [[R("De HMI para a ", 16, SLATE), R("base de execução inteligente", 16, OPTIX, True),
        R(" da Rockwell: HMI/SCADA cloud-enabled, projetada e implantada pelo navegador.", 16, SLATE)]])
feats6 = [
    ("SCADA multi-site (2026)", "Centraliza o supervisório de todas as plantas em uma plataforma, com redundância de servidor e workstation clients."),
    ("ResilientEdge", "Execução edge resiliente + analytics em nuvem, treino de IA e orquestração corporativa. Disponível global desde 18/06/2026."),
    ("Acesso remoto", "FactoryTalk Remote Access via VPN: investigar e resolver antes de viajar à planta remota."),
    ("Aberto / OPC UA", "Comunica nativamente com controladores Rockwell e de terceiros; roda em qualquer hardware."),
]
x0=0.85; y0=2.35; cw=5.75; ch=1.75; gx=0.35; gy=0.3
for i,(t,d) in enumerate(feats6):
    r,cc=divmod(i,2); x=x0+cc*(cw+gx); y=y0+r*(ch+gy)
    card(x, y, cw, ch)
    rect(x, y, 0.1, ch, fill=OPTIX, rounded=True, radius=3)
    paras(x+0.32, y+0.2, cw-0.6, 0.5, [[R(t, 16, OPTIX_DK, True)]])
    paras(x+0.32, y+0.72, cw-0.6, 0.95, [[R(d, 13, SLATE)]])
chip(0.85, 6.35, "Para a Inpasa: o caminho natural do COI centralizado multi-planta", fill=OPTIX, w=7.6, h=0.5, size=13)
page_num(6); c.showPage()

# ----------------------------------------------------------------------------
# 7. DATAMOSAIX
# ----------------------------------------------------------------------------
page_bg(LIGHT)
header("Camada de DataOps + IA", "FactoryTalk DataMosaix + Atlas AI", AMBER)
paras(0.85, 1.5, 11.6, 0.35,
      [[R("Industrial DataOps do edge à nuvem: ", 14.5, AMBER_DK, True),
        R("contextualiza dados de operação, engenharia e TI para casos de uso de IA.", 14.5, SLATE)]])
feats7 = [
    ("RCA automatizada", "Análise de causa raiz sem precisar de um analista de dados dedicado.",
     "ao parar uma planta, o agente cruza alarmes, malhas e histórico e aponta a causa provável em segundos."),
    ("Manutenção prescritiva", "Detecta desgaste precoce e recomenda a ação antes da parada custosa.",
     "a posição real de uma válvula de controle passa a divergir do percentual comandado além do histórico — tendência de desgaste sinalizada antes da falha."),
    ("Agentes de IA contextuais", "Monitoram variáveis de processo e geram alertas contextualizados.",
     "exatamente o que o Hub de Automação está construindo — alerta quando uma malha foge do padrão da planta."),
    ("No-code", "A equipe de automação cria fluxos e agentes seguros sem programar.",
     "monta e ajusta os fluxos do DataMosaix sem depender de TI nem de código."),
]
x0d=0.85; wd=11.6; y0d=1.98; rhd=1.12; gapd=0.12
for i,(t,d,ex) in enumerate(feats7):
    y=y0d+i*(rhd+gapd)
    card(x0d, y, wd, rhd)
    rect(x0d, y, 0.1, rhd, fill=AMBER, rounded=True, radius=3)
    paras(x0d+0.32, y+0.12, wd-0.7, 0.32, [[R(t, 16, AMBER_DK, True)]])
    paras(x0d+0.32, y+0.45, wd-0.7, 0.26, [[R(d, 12.5, SLATE)]])
    paras(x0d+0.32, y+0.72, wd-0.7, 0.40, [[R("Ex. Inpasa:  ", 12, AMBER_DK, True, True), R(ex, 12, SLATE, False, True)]])
page_num(7); c.showPage()

# ----------------------------------------------------------------------------
# 8. COMPARATIVO (tabela)
# ----------------------------------------------------------------------------
page_bg(LIGHT)
header("Comparativo", "Hoje (PlantPAx + TracOS)  vs.  Proposto (Optix + DataMosaix)", GREEN)
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
tx=0.85; ty=1.7; rh=0.56; colw=[3.0,4.0,4.6]
y=ty
for ri,row in enumerate(rows):
    x=tx; head=(ri==0)
    for ci,cell in enumerate(row):
        if head: fill = NAVY if ci==0 else (RED if ci==1 else GREEN)
        else: fill = WHITE if ri%2 else "#ECF2F7"
        rect(x, y, colw[ci], rh, fill=fill, line=LINE, line_w=0.5)
        if head: tcol=WHITE
        elif ci==0: tcol=NAVY
        elif ci==1: tcol=SLATE
        else: tcol=GREEN_DK
        bold = head or ci==0
        paras(x+8/IN, y, colw[ci]-14/IN, rh,
              [[R(cell, 13.5 if head else 13, tcol, bold)]], anchor='middle')
        x+=colw[ci]
    y+=rh
page_num(8); c.showPage()

# ----------------------------------------------------------------------------
# 9. ALARMES ISA-18.2 (grafico desenhado)
# ----------------------------------------------------------------------------
page_bg(LIGHT)
header("Benchmarking de alarmes", "A norma ISA-18.2 e a oportunidade imediata", RED)
gx, gy, gw, gh = 0.85, 1.7, 6.4, 4.3
card(gx, gy, gw, gh, shadow=True)
paras(gx, gy+0.12, gw, 0.3, [[R("Alarmes por operador / hora", 13, NAVY, True)]], align=TA_CENTER)
plot_left=gx+0.7; plot_right=gx+gw-0.25; plot_top=gy+0.6; axis_bottom=gy+gh-0.75
plot_w=plot_right-plot_left; plot_h=axis_bottom-plot_top
vmax=32
for val in [0,8,16,24,32]:
    yy=axis_bottom - val/vmax*plot_h
    rect(plot_left, yy, plot_w, 0.6/IN, fill=GRID)
    paras(gx+0.05, yy-0.09, 0.6, 0.2, [[R(str(val), 9, GRAY)]], align=TA_RIGHT)
cats=[("Limite ISA-18.2","(máximo)",6,GREEN),
      ("Média do setor","(hoje)",30,RED),
      ("Meta Inpasa","no COI",6,GREEN)]
slot=plot_w/3
for i,(l1,l2,val,col) in enumerate(cats):
    cxx=plot_left+slot*(i+0.5)
    bw=slot*0.5; barh=val/vmax*plot_h; bar_top=axis_bottom-barh
    rect(cxx-bw/2, bar_top, bw, barh, fill=col)
    paras(cxx-0.7, bar_top-0.32, 1.4, 0.3, [[R(str(val), 15, NAVY, True)]], align=TA_CENTER)
    paras(cxx-slot/2, axis_bottom+0.1, slot, 0.6,
          [[R(l1, 11, SLATE, True)],[R(l2, 10, GRAY)]], align=TA_CENTER, space_after=1)
rect(plot_left, axis_bottom, plot_w, 1.0/IN, fill=GRAY)
paras(7.55, 1.85, 5.0, 0.6, [[R("5x acima do recomendado", 20, RED, True)]])
bullets(7.55, 2.65, 5.0, 3.2, [
    "Planta bem gerenciada: < 6 alarmes/operador/hora em operação normal.",
    "Média das plantas: 30+ por operador/hora — cinco vezes o máximo.",
    "~70% dos alarmes em DCS/SCADA típicos são nuisance (não exigem ação).",
    ("Grafana (já implantado) ", "trata nuisance alarms, bad actors e alarm floods sobre o PlantPAx adaptado — base que já operamos hoje."),
], size=13.5, marker=RED, gap=11)
page_num(9); c.showPage()

# ----------------------------------------------------------------------------
# 10. KPIs (tabela)
# ----------------------------------------------------------------------------
page_bg(LIGHT)
header("Indicadores", "KPIs de benchmarking que o ecossistema já mede", GREEN)
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
tx=0.85; ty=1.62; rh=0.5; colw=[4.3,4.3,3.0]
y=ty
for ri,row in enumerate(rows):
    x=tx; head=(ri==0); last=(ri==len(rows)-1)
    for ci,cell in enumerate(row):
        if head: fill=NAVY
        elif last: fill=GREEN
        else: fill = WHITE if ri%2 else "#ECF2F7"
        rect(x, y, colw[ci], rh, fill=fill, line=LINE, line_w=0.5)
        if head or last: tcol=WHITE
        elif ci==0: tcol=NAVY
        else: tcol=SLATE
        bold = head or ci==0 or last
        paras(x+8/IN, y, colw[ci]-14/IN, rh, [[R(cell, 12.5, tcol, bold)]], anchor='middle')
        x+=colw[ci]
    y+=rh
paras(0.85, 6.75, 11.6, 0.4,
      [[R("Quase tudo já existe no dado atual — falta a camada que agrega e compara: o DataMosaix.", 13, GRAY, False, True)]])
page_num(10); c.showPage()

# ----------------------------------------------------------------------------
# 11. O DELTA
# ----------------------------------------------------------------------------
page_bg(NAVY)
rect(0.55, 0.32, 0.14, 0.55, fill=AMBER)
paras(0.85, 0.26, 11.6, 0.3, [[R("O DELTA", 11.5, AMBER, True)]])
paras(0.85, 0.5, 11.9, 0.6, [[R("O que o DataMosaix adiciona ao que já temos", 25, WHITE, True)]])
paras(0.85, 1.45, 11.6, 0.7,
      [[R("Hoje o dado vive dentro de cada PlantPAx. O DataMosaix é a camada que ", 15.5, COVER_SUB),
        R("agrega, contextualiza e compara", 15.5, AMBER, True),
        R(" — uma visão única de toda a operação.", 15.5, COVER_SUB)]])
adds = [
    ("Indicadores comparáveis", "Alarmes/operador·hora, % de malhas em automático, blocos em programa, interlocks e variáveis simuladas — além do OEE — por planta, num só painel."),
    ("Planejamento enterprise", "Decisão de produção, manutenção e ações estratégicas em nível corporativo — visão consolidada da companhia, não por site isolado."),
    ("Visão multi-site", "Sinop, Nova Mutum, Dourados, Balsas, Sidrolândia e novas plantas, lado a lado, na mesma régua."),
    ("Contexto OT + IT + ET", "Une OT (processo / chão de fábrica), IT (sistemas corporativos / ERP) e ET (engenharia / ativos) num só contexto pronto para a IA."),
]
x0=0.85; y0=2.45; cw=2.85; ch=2.9; gap=0.2
for i,(t,d) in enumerate(adds):
    x=x0+i*(cw+gap)
    rect(x, y0, cw, ch, fill=NAVY_CARD, line=AMBER, line_w=1.2, rounded=True, radius=8)
    rect(x, y0, cw, 0.1, fill=AMBER, rounded=True, radius=3)
    paras(x+0.25, y0+0.38, cw-0.5, 0.85, [[R(t, 16.5, WHITE, True)]])
    paras(x+0.25, y0+1.2, cw-0.5, 1.6, [[R(d, 12.5, LAYER_DESC)]])
page_num(11); c.showPage()

# ----------------------------------------------------------------------------
# 12. CASOS DE USO COI
# ----------------------------------------------------------------------------
page_bg(LIGHT)
header("Aplicação direta", "Como isso aparece no COI da Inpasa", GREEN)
cases = [
    ("Tela única em tempo real", "Indicadores ao vivo por planta, lado a lado: % de malhas em automático, índice de alarmes/operador·hora, blocos em programa, interlocks e variáveis simuladas.", GREEN),
    ("Ranking de plantas", "Ordena as unidades pelos mesmos indicadores — quem está dentro e fora da ISA-18.2 — destacando boa prática e quem precisa de atenção.", OPTIX),
    ("Alertas automáticos", "Disparo ao cruzar o limite (ex.: 6 alarmes/operador·hora) — notificação por WhatsApp, e-mail ou o canal que o gestor preferir.", RED),
    ("Comparativo histórico", "Revela divergências por turno e antes/depois de parada, além de outros padrões — insights para operação e manutenção.", AMBER),
]
x0=0.85; y0=1.75; cw=5.75; ch=2.3; gx=0.35; gy=0.35
for i,(t,d,col) in enumerate(cases):
    r,cc=divmod(i,2); x=x0+cc*(cw+gx); y=y0+r*(ch+gy)
    card(x, y, cw, ch)
    rect(x+0.3, y+0.3, 0.6, 0.6, fill=col, rounded=True, radius=10)
    paras(x+0.3, y+0.3, 0.6, 0.6, [[R(str(i+1), 20, WHITE, True)]], align=TA_CENTER, anchor='middle')
    paras(x+1.1, y+0.35, cw-1.45, 0.9, [[R(t, 17, NAVY, True)]])
    paras(x+0.32, y+1.08, cw-0.64, 1.15, [[R(d, 12.5, SLATE)]])
page_num(12); c.showPage()

# ----------------------------------------------------------------------------
# 13. ROADMAP
# ----------------------------------------------------------------------------
page_bg(LIGHT)
header("Roadmap", "Como evolui — do que já temos ao COI prescritivo", OPTIX)
phases = [
    ("Fase 1", "Já implementado", """Benchmarking de alarmes e KPIs já rodam hoje no Grafana — que já temos e está implantado — sobre o PlantPAx adaptado. Base pronta; o equivalente Rockwell (VantagePoint) não é necessário para começar.""", GREEN),
    ("Fase 2", "Preditivo", """O DataMosaix estende o monitoramento preditivo aos equipamentos não rotativos — os rotativos já são cobertos pela Tractian — e agrega as plantas em dashboards comparativos.""", AMBER),
    ("Fase 3", "Prescritivo + COI", """Em simulações de paradas em vários sites, com o COI centralizado a retomada das plantas ficou mais estável, rápida e otimizada — operação e manutenção. Com o time central treinando os sites, é possível até evitar desarmes.""", OPTIX),
]
x0=0.85; y0=1.9; cw=3.75; ch=3.5; gap=0.18
for i,(l1,l2,d,col) in enumerate(phases):
    x=x0+i*(cw+gap)
    card(x, y0, cw, ch, line=col, line_w=1.5)
    rect(x, y0, cw, 0.95, fill=col, rounded=True, radius=8)
    rect(x, y0+0.5, cw, 0.45, fill=col)
    paras(x+0.3, y0+0.12, cw-0.6, 0.8, [[R(l1, 14, WHITE)],[R(l2, 20, WHITE, True)]], space_after=1)
    paras(x+0.32, y0+1.15, cw-0.62, 2.25, [[R(d, 12.5, SLATE)]])
    if i<2:
        mx=x+cw-0.02; my=y0+ch/2
        pth=c.beginPath()
        pth.moveTo(mx*IN,(PH-(my-0.2))*IN); pth.lineTo(mx*IN,(PH-(my+0.2))*IN)
        pth.lineTo((mx+0.28)*IN,(PH-my)*IN); pth.close()
        c.setFillColor(HexColor(col)); c.drawPath(pth, stroke=0, fill=1)
chip(0.85, 5.7, "ResilientEdge: disponível global desde 18/06/2026  ·  SCADA multi-site em rollout 2026", fill=NAVY, w=9.0, h=0.5, size=13)
page_num(13); c.showPage()

# ----------------------------------------------------------------------------
# 14. PROXIMOS PASSOS
# ----------------------------------------------------------------------------
page_bg(LIGHT)
header("Decisão", "O que pedimos para avançar", GREEN)
steps = [
    ("Aprovar o piloto", """Começar por 1–2 indicadores em todas as plantas (ex.: controles em automático e índice de alarmes/operador·hora), ampliando depois para os demais. Estimativa: ~4–6 semanas para os 2 primeiros, conforme o volume de tags por unidade."""),
    ("Sequência de indicadores", """Controles em automático e índice de alarmes primeiro; depois blocos em programa, interlocks desabilitados e variáveis simuladas."""),
    ("Interlocutores Rockwell", """Dan DeYoung — VP executivo; Lúcio — gerente de sistemas avançados (Brasil); Devair — gerente de atendimento Inpasa; Marcel — eng. sênior de sistemas avançados."""),
    ("Designar squad interno", """Gestores e equipe do Hub de Automação conduzindo os fluxos no-code do DataMosaix."""),
]
y0=1.7; rh=1.24; x0=0.85; w=11.6
for i,(t,d) in enumerate(steps):
    y=y0+i*(rh+0.08)
    card(x0, y, w, rh)
    circle(x0+0.3+0.275, y+0.34+0.275, 0.275, GREEN)
    paras(x0+0.3, y+0.34, 0.55, 0.55, [[R(str(i+1), 18, WHITE, True)]], align=TA_CENTER, anchor='middle')
    paras(x0+1.1, y+0.16, w-1.4, 0.45, [[R(t, 16, NAVY, True)]])
    paras(x0+1.1, y+0.6, w-1.4, 0.6, [[R(d, 12, SLATE)]])
page_num(14); c.showPage()

# ----------------------------------------------------------------------------
# 15. ENCERRAMENTO
# ----------------------------------------------------------------------------
page_bg(NAVY)
rect(0, 0, 0.22, PH, fill=GREEN)
rect(0.22, 0, 0.08, PH, fill=OPTIX)
paras(1.0, 2.3, 11.2, 2.2,
      [[R("O dado já existe.", 40, WHITE, True)],
       [R("Falta transformá-lo em decisão.", 40, GREEN, True)]], ls=1.1, space_after=6)
paras(1.02, 4.4, 11.0, 1.0,
      [[R("Optix + DataMosaix conectam o que a Inpasa já tem (PlantPAx + TracOS) a um COI único,", 17, COVER_SUB)],
       [R("com benchmarking entre plantas e IA prescritiva — começando pelo ganho rápido.", 17, COVER_SUB)]], space_after=4)
rect(1.05, 5.7, 5.5, 1.5/IN, fill=DIVIDER)
paras(1.05, 5.9, 11, 0.8, [[R("Gestão Estratégica de Automação  ·  Inpasa  ·  2026.06.28", 13, GRAY, True)]])
c.showPage()

c.save()
print("OK ->", out)
