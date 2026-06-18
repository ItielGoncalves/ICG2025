#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera dois PDFs sobre a evolucao da automacao na Inpasa:
  1) Visao_Inpasa_Automacao.pdf      -> deck (16:9, 10 paginas)
  2) Inpasa_Evolucao_Automacao.pdf   -> documento-texto institucional
Tudo via reportlab (LibreOffice indisponivel no ambiente).
"""
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, ListFlowable, ListItem)
from reportlab.pdfgen import canvas as canvasmod
import math

NAVY  = HexColor("#122A4A"); BLUE  = HexColor("#1F5CA8"); BLUE2 = HexColor("#3E7CC4")
AMBER = HexColor("#F2A033"); GREEN = HexColor("#2F9E44"); RED   = HexColor("#C8473B")
YELLOW= HexColor("#E2B033"); LIGHT = HexColor("#F4F6F9"); INK   = HexColor("#1B2A41")
GRAY  = HexColor("#5B6B7F"); LINE  = HexColor("#D7DEE7"); SOFT  = HexColor("#E9F0F8")

IN = inch
# ============================================================
# PARTE 1 — DECK PDF (16:9)
# ============================================================
PW, PH = 13.333*IN, 7.5*IN
def ty(y, h=0.0): return PH - (y+h)*IN   # top-based inches -> pdf points

def rrect(c, x, y, w, h, fill=None, stroke=None, lw=1.0, r=0.0):
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(lw)
    c.roundRect(x*IN, ty(y, h), w*IN, h*IN, r*IN,
                stroke=1 if stroke is not None else 0,
                fill=1 if fill is not None else 0)

def oval(c, x, y, w, h, fill):
    c.setFillColor(fill); c.ellipse(x*IN, ty(y, h), (x+w)*IN, ty(y), fill=1, stroke=0)

def wrap(c, text, font, size, maxw):
    words = text.split(); lines=[]; cur=""
    for w in words:
        t = (cur+" "+w).strip()
        if c.stringWidth(t, font, size) <= maxw*IN: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def line(c, x, y, w, text, size, color, bold=False, align="l"):
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, size); c.setFillColor(color)
    if align=="c": c.drawCentredString((x+w/2)*IN, ty(y)-size*0.9, text)
    elif align=="r": c.drawRightString((x+w)*IN, ty(y)-size*0.9, text)
    else: c.drawString(x*IN, ty(y)-size*0.9, text)

def block(c, x, y, w, text, size, color, bold=False, lead=None, align="l"):
    font = "Helvetica-Bold" if bold else "Helvetica"
    lead = lead or size*1.25
    for i, ln in enumerate(wrap(c, text, font, size, w)):
        line(c, x, y+(i*lead)/IN, w, ln, size, color, bold, align)
    return y + (len(wrap(c, text, font, size, w))*lead)/IN

def kicker(c, label):
    rrect(c, 0.55, 0.62, 0.16, 0.46, fill=AMBER)
    line(c, 0.82, 0.6, 11, label, 12.5, BLUE, bold=True)

def foot(c, p, dark=False):
    col = white if dark else GRAY
    line(c, 0.55, 7.05, 8, "INPASA  ·  Avanço da Automação — Visão e Jornada", 8.5, col)
    line(c, 11.4, 7.05, 1.4, f"{p:02d}", 9, AMBER, bold=True, align="r")

def donut(c, cx, cy, r, parts, caption):
    """parts: list of (frac, color, label%). Draw doughnut centered at cx,cy (inches)."""
    start = 90.0
    for frac, col, _ in parts:
        ext = -360.0*frac
        c.setFillColor(col); c.setStrokeColor(white); c.setLineWidth(1.5)
        c.wedge((cx-r)*IN, ty(cy+r), (cx+r)*IN, ty(cy-r), start, ext, fill=1, stroke=1)
        start += ext
    c.setFillColor(LIGHT)
    ir = r*0.60
    c.ellipse((cx-ir)*IN, ty(cy+ir), (cx+ir)*IN, ty(cy-ir), fill=1, stroke=0)
    # percentage labels
    ang = 90.0
    for frac, col, lab in parts:
        mid = math.radians(ang - 360*frac/2)
        lr = r*0.80
        lx = cx + lr*math.cos(mid); lyc = cy - lr*math.sin(mid)
        c.setFont("Helvetica-Bold", 9); c.setFillColor(white)
        c.drawCentredString(lx*IN, ty(lyc)-4, lab)
        ang -= 360*frac
    line(c, cx-1.5, cy+r+0.12, 3.0, caption, 9.5, NAVY, bold=True, align="c")

def build_deck(path):
    c = canvasmod.Canvas(path, pagesize=(PW, PH))

    # S1 capa
    c.setFillColor(NAVY); c.rect(0,0,PW,PH, fill=1, stroke=0)
    rrect(c,0,0,13.333,0.28,fill=AMBER); rrect(c,0,7.22,13.333,0.28,fill=BLUE)
    oval(c,0.9,1.5,0.9,0.9,AMBER); line(c,0.9,1.62,0.9,"IA",24,NAVY,bold=True,align="c")
    line(c,0.9,3.0,11.6,"Avanço da Automação",46,white,bold=True)
    line(c,0.9,3.85,11.6,"na Inpasa",46,AMBER,bold=True)
    rrect(c,0.95,4.95,3.2,0.05,fill=BLUE2)
    line(c,0.9,5.2,11.5,"De controlar a planta a governar a planta",19,LIGHT)
    line(c,0.9,6.4,11.5,"Apresentação institucional  ·  Liderança e Parceiros de Automação Industrial",12.5,HexColor("#AEB9C8"))
    c.showPage()

    # S2 virada de chave
    c.setFillColor(LIGHT); c.rect(0,0,PW,PH,fill=1,stroke=0)
    kicker(c,"A VIRADA DE CHAVE")
    block(c,0.82,1.05,12.0,"Automação deixou de ser controlar a planta.",27,NAVY,bold=True)
    line(c,0.82,1.75,12,"Passou a enxergar e governar o estado dela em tempo real.",24,AMBER,bold=True)
    block(c,0.82,2.95,11.6,"O operador deixa de atuar o tempo todo e passa a ser o vigia. O sistema opera — e audita a si mesmo.",15,GRAY)
    pil=[("01","Controle","Malhas estáveis, automáticas e auditadas",GREEN),
         ("02","Gestão de Alarmes","Foco no que exige ação do operador",BLUE),
         ("03","Manutenção Preditiva","Agir antes da falha, preservando ativos",AMBER)]
    for i,(n,t,d,col) in enumerate(pil):
        x=0.82+i*4.12
        rrect(c,x,4.1,3.78,2.05,fill=white,stroke=LINE,lw=1,r=0.06)
        rrect(c,x,4.1,3.78,0.16,fill=col)
        line(c,x+0.32,4.5,3.2,n,16,col,bold=True)
        line(c,x+0.32,4.98,3.2,t,18,NAVY,bold=True)
        block(c,x+0.32,5.5,3.1,d,12.5,GRAY)
    foot(c,2); c.showPage()

    # S3 dashboard
    c.setFillColor(LIGHT); c.rect(0,0,PW,PH,fill=1,stroke=0)
    kicker(c,"ONDE ESTAMOS HOJE  ·  EVIDÊNCIA MEDIDA")
    block(c,0.82,1.02,12.2,"Estado das malhas de controle — últimos 15 dias",23,NAVY,bold=True)
    def kpirow(yy,header,tiles):
        line(c,0.55,yy,12.3,header,11.5,NAVY,bold=True)
        n=len(tiles); g=0.12; tw=(12.33-(n-1)*g)/n
        for i,(lab,val,col) in enumerate(tiles):
            x=0.55+i*(tw+g)
            rrect(c,x,yy+0.30,tw,0.92,fill=col,r=0.04)
            line(c,x,yy+0.52,tw,str(val),24,white,bold=True,align="c")
            line(c,x,yy+1.0,tw,lab,9,white,bold=True,align="c")
    util=[("AUTO",87,GREEN),("MANUAL",6,RED),("PROGRAMA",82,GREEN),("OPERADOR",54,YELLOW),("BYPASS",1,RED),("MANUT.",8,YELLOW)]
    proc=[("AUTO",147,GREEN),("MANUAL",22,RED),("PROGRAMA",125,GREEN),("OPERADOR",27,YELLOW),("BYPASS",0,GREEN),("MANUT.",1,YELLOW)]
    kpirow(1.55,"MALHAS DE UTILIDADES",util)
    kpirow(2.92,"MALHAS DE PROCESSO",proc)
    donut(c,1.9,5.55,0.95,[(0.94,GREEN,"94%"),(0.06,RED,"6%")],"Utilid. — Auto × Manual")
    donut(c,5.0,5.55,0.95,[(0.60,GREEN,"60%"),(0.40,YELLOW,"40%")],"Utilid. — Prog. × Operador")
    donut(c,8.2,5.55,0.95,[(0.87,GREEN,"87%"),(0.13,RED,"13%")],"Proc. — Auto × Manual")
    donut(c,11.3,5.55,0.95,[(0.82,GREEN,"82%"),(0.18,YELLOW,"18%")],"Proc. — Prog. × Operador")
    foot(c,3); c.showPage()

    # S4 ativos Dourados
    c.setFillColor(LIGHT); c.rect(0,0,PW,PH,fill=1,stroke=0)
    kicker(c,"GESTÃO DE ATIVOS  ·  PILOTO EM DOURADOS")
    block(c,0.82,1.05,12.2,"Da malha ao ativo: visibilidade e disciplina operacional",24,NAVY,bold=True)
    for i,(num,lab) in enumerate([("5","objetos simulados (unidade piloto)"),("48","objetos simulados (visão consolidada)")]):
        x=0.82+i*3.0
        rrect(c,x,2.0,2.7,1.9,fill=NAVY,r=0.06)
        line(c,x,2.55,2.7,num,52,AMBER,bold=True,align="c")
        block(c,x+0.2,3.3,2.3,lab,11.5,white,align="c")
    caps=[("Equipamentos em simulação","monitorados em tempo real"),
          ("Ativos inoperantes e fora de operação","identificados automaticamente"),
          ("Auditoria de usuário","quem fez o quê, em qual estação"),
          ("Tempo em simulação","métrica inédita de disciplina operacional")]
    for i,(t,d) in enumerate(caps):
        y=2.0+i*0.55
        oval(c,7.0,y+0.04,0.16,0.16,AMBER)
        line(c,7.3,y,5.6,t,13.5,NAVY,bold=True)
        line(c,7.3,y+0.26,5.6,d,11.5,GRAY)
    rrect(c,0.82,4.4,11.7,0.95,fill=SOFT,stroke=BLUE2,lw=1,r=0.04)
    block(c,1.1,4.55,11.2,"Plano: validar em Dourados e padronizar para todo o Grupo Inpasa — gestão unificada e visibilidade operacional dos ativos.",13.5,INK)
    foot(c,4); c.showPage()

    # S5 operacao observatoria
    c.setFillColor(NAVY); c.rect(0,0,PW,PH,fill=1,stroke=0)
    rrect(c,0.55,0.62,0.16,0.46,fill=AMBER)
    line(c,0.82,0.6,11,"CONCEITO  ·  OPERAÇÃO OBSERVATÓRIA",12.5,AMBER,bold=True)
    block(c,0.82,1.15,12,"O operador supervisiona. O sistema opera.",29,white,bold=True)
    cc=[("Operador → Vigia","Supervisiona, decide sobre exceções e direciona. Sai do controle manual repetitivo."),
        ("Sistema → Opera e audita","Mantém as malhas em automático e registra cada desvio do estado normal.")]
    for i,(t,d) in enumerate(cc):
        x=0.82+i*6.05
        rrect(c,x,2.5,5.7,1.5,fill=HexColor("#1B3A5E"),stroke=BLUE2,lw=1,r=0.05)
        line(c,x+0.35,2.7,5.0,t,17,AMBER,bold=True)
        block(c,x+0.35,3.25,5.0,d,13,LIGHT)
    rrect(c,0.82,4.45,11.7,1.6,fill=HexColor("#143152"),stroke=AMBER,lw=1.25,r=0.05)
    line(c,1.15,4.7,11.0,"As malhas de controle viram sensores de saúde.",18,white,bold=True)
    block(c,1.15,5.3,11.0,"Desvios no comportamento de uma malha antecipam a falha antes que ela vire um evento — detecção preditiva nascendo de dentro do próprio controle.",13.5,LIGHT)
    foot(c,5,dark=True); c.showPage()

    # S6 dados
    c.setFillColor(LIGHT); c.rect(0,0,PW,PH,fill=1,stroke=0)
    kicker(c,"A BASE  ·  ARQUITETURA DE DADOS")
    block(c,0.82,1.05,12.2,"Dados confiáveis e organizados são a fundação de tudo",24,NAVY,bold=True)
    cam=[("Coleta","De controladores e instrumentos",BLUE),
         ("Historiação","Série temporal confiável",BLUE2),
         ("Contextualização","Dado com significado operacional",AMBER),
         ("Análise","Insight, comparação e decisão",GREEN)]
    for i,(t,d,col) in enumerate(cam):
        x=0.82+i*3.15
        rrect(c,x,2.2,2.7,1.5,fill=white,stroke=LINE,lw=1,r=0.05)
        rrect(c,x,2.2,0.14,1.5,fill=col)
        line(c,x+0.32,2.45,2.3,t,16,NAVY,bold=True)
        block(c,x+0.32,2.95,2.3,d,11.5,GRAY)
        if i<3: line(c,x+2.7,2.7,0.45,"▶",18,AMBER,bold=True,align="c")
    de=[("Varredura automática dos controladores","Padroniza a informação em escala, sem trabalho manual."),
        ("Benchmarking entre plantas","Saber qual unidade opera melhor — e por quê — e levar a melhor prática às demais.")]
    for i,(t,d) in enumerate(de):
        x=0.82+i*6.05
        rrect(c,x,4.35,5.7,1.55,fill=SOFT,stroke=BLUE2,lw=1,r=0.05)
        line(c,x+0.35,4.55,5.0,t,15,BLUE,bold=True)
        block(c,x+0.35,5.1,5.0,d,12.5,INK)
    foot(c,6); c.showPage()

    # S7 IA
    c.setFillColor(LIGHT); c.rect(0,0,PW,PH,fill=1,stroke=0)
    kicker(c,"INTELIGÊNCIA  ·  IA NO CONTROLE E MANUTENÇÃO")
    block(c,0.82,1.05,12.2,"IA onde ela gera valor: controlar melhor e falhar menos",24,NAVY,bold=True)
    fr=[("Controle avançado e adaptativo","Ajusta-se ao processo e reduz variabilidade.",GREEN),
        ("IA que aprende e recomenda","Predição de resultados e apoio à decisão do operador.",BLUE),
        ("Manutenção preditiva de verdade","Do reativo (corretiva/preventiva) ao agir antes da falha.",AMBER)]
    for i,(t,d,col) in enumerate(fr):
        x=0.82+i*4.12
        rrect(c,x,2.2,3.78,2.0,fill=white,stroke=LINE,lw=1,r=0.06)
        rrect(c,x,2.2,3.78,0.16,fill=col)
        block(c,x+0.32,2.55,3.15,t,16,NAVY,bold=True)
        block(c,x+0.32,3.45,3.15,d,12.5,GRAY)
    rrect(c,0.82,4.7,11.7,1.2,fill=NAVY,r=0.05)
    line(c,0.82,5.18,11.7,"Menos paradas  ·  Mais confiabilidade  ·  Ativos preservados  ·  Operação mais autônoma",16,white,bold=True,align="c")
    foot(c,7); c.showPage()

    # S8 COI
    c.setFillColor(NAVY); c.rect(0,0,PW,PH,fill=1,stroke=0)
    rrect(c,0.55,0.62,0.16,0.46,fill=AMBER)
    line(c,0.82,0.6,11,"VISÃO  ·  CENTRO DE OPERAÇÕES INTEGRADO (COI)",12.5,AMBER,bold=True)
    block(c,0.82,1.15,12,"Uma só sala de inteligência para todo o Grupo",28,white,bold=True)
    it=[("Robusto e escalável","Cresce com o Grupo, unidade a unidade."),
        ("Centraliza decisão, não só telas","Visão única e autonomia operacional."),
        ("Otimização de mão de obra","Especialistas focados onde agregam mais.")]
    for i,(t,d) in enumerate(it):
        x=0.82+i*3.95
        rrect(c,x,2.5,3.7,1.7,fill=HexColor("#1B3A5E"),stroke=BLUE2,lw=1,r=0.05)
        block(c,x+0.3,2.7,3.2,t,15.5,AMBER,bold=True)
        block(c,x+0.3,3.5,3.2,d,12,LIGHT)
    block(c,0.82,4.65,11.7,"Inspirado em modelos já consolidados em indústrias de grande porte — trazido para a realidade do agronegócio da Inpasa.",13.5,LIGHT)
    foot(c,8,dark=True); c.showPage()

    # S9 roadmap
    c.setFillColor(LIGHT); c.rect(0,0,PW,PH,fill=1,stroke=0)
    kicker(c,"ROADMAP  ·  UM CAMINHO JÁ EM MOVIMENTO")
    block(c,0.82,1.05,12.2,"Incremental, medido e em execução",24,NAVY,bold=True)
    et=[("HOJE","Malhas medidas e auditadas + piloto de ativos em Dourados",GREEN,"Em andamento"),
        ("CURTO","Padronização de dados + gestão de ativos em todo o Grupo",BLUE,"Próximo"),
        ("MÉDIO","IA aplicada ao controle e à manutenção preditiva",AMBER,"A seguir"),
        ("VISÃO","Centro de Operações Integrado e operação autônoma",NAVY,"Destino")]
    rrect(c,1.0,3.55,11.3,0.06,fill=LINE)
    for i,(fase,desc,col,tag) in enumerate(et):
        x=0.82+i*3.15; cx=x+1.35
        oval(c,cx-0.16,3.42,0.32,0.32,col)
        rrect(c,x,2.0,2.7,1.15,fill=white,stroke=LINE,lw=1,r=0.05)
        rrect(c,x,2.0,2.7,0.5,fill=col)
        line(c,x,2.16,2.7,fase,14,white,bold=True,align="c")
        block(c,x+0.2,2.58,2.3,desc,11,INK,align="c")
        line(c,x,3.9,2.7,tag,11,col,bold=True,align="c")
    rrect(c,0.82,5.0,11.7,1.0,fill=SOFT,stroke=BLUE2,lw=1,r=0.05)
    line(c,0.82,5.4,11.7,"Cada etapa entrega valor por si — e prepara a seguinte.",16,BLUE,bold=True,align="c")
    foot(c,9); c.showPage()

    # S10 fechamento
    c.setFillColor(NAVY); c.rect(0,0,PW,PH,fill=1,stroke=0)
    rrect(c,0,0,13.333,0.28,fill=AMBER); rrect(c,0,7.22,13.333,0.28,fill=BLUE)
    line(c,0.9,2.4,11.5,"A Inpasa sabe",44,white,bold=True)
    line(c,0.9,3.25,11.5,"aonde quer chegar.",44,AMBER,bold=True)
    rrect(c,0.95,4.35,3.2,0.05,fill=BLUE2)
    block(c,0.9,4.6,11.3,"Damos os passos com método e medição. Buscamos parceiros que acelerem essa visão — com tecnologia robusta, escalável e que respeite a jornada que já construímos.",15,LIGHT)
    line(c,0.9,6.0,11.3,"Obrigado.",22,AMBER,bold=True)
    c.showPage()
    c.save()
    print("OK deck ->", path)

# ============================================================
# PARTE 2 — DOCUMENTO-TEXTO PDF
# ============================================================
def build_doc(path):
    styles = getSampleStyleSheet()
    H1 = ParagraphStyle("H1", parent=styles["Heading1"], textColor=NAVY,
                        fontName="Helvetica-Bold", fontSize=17, spaceBefore=16, spaceAfter=6, leading=20)
    H2 = ParagraphStyle("H2", parent=styles["Heading2"], textColor=BLUE,
                        fontName="Helvetica-Bold", fontSize=12.5, spaceBefore=10, spaceAfter=3, leading=15)
    BODY = ParagraphStyle("BODY", parent=styles["BodyText"], textColor=INK,
                          fontName="Helvetica", fontSize=10.5, leading=15.5, alignment=TA_JUSTIFY, spaceAfter=6)
    LEAD = ParagraphStyle("LEAD", parent=BODY, textColor=GRAY, fontSize=11.5, leading=16,
                          fontName="Helvetica-Oblique")
    BULL = ParagraphStyle("BULL", parent=BODY, leftIndent=14, spaceAfter=3)
    TITLE = ParagraphStyle("TITLE", parent=styles["Title"], textColor=NAVY,
                           fontName="Helvetica-Bold", fontSize=24, leading=28, spaceAfter=2, alignment=TA_LEFT)
    SUB = ParagraphStyle("SUB", parent=styles["Normal"], textColor=AMBER,
                         fontName="Helvetica-Bold", fontSize=13, spaceAfter=2)
    META = ParagraphStyle("META", parent=styles["Normal"], textColor=GRAY, fontSize=9, spaceAfter=2)

    def bullets(items):
        return ListFlowable(
            [ListItem(Paragraph(t, BULL), leftIndent=10, value="•") for t in items],
            bulletType="bullet", start="•", leftIndent=10)

    doc = SimpleDocTemplate(path, pagesize=A4, topMargin=2.0*IN*0.5, bottomMargin=0.7*IN,
                            leftMargin=0.85*IN, rightMargin=0.85*IN,
                            title="A Evolução da Automação na Inpasa")
    E=[]
    E.append(Paragraph("A Evolução da Automação na Inpasa", TITLE))
    E.append(Paragraph("De controlar a planta a governar a planta", SUB))
    E.append(Paragraph("Documento institucional · Visão, estado atual e jornada · Junho/2026", META))
    E.append(Spacer(1,4))
    E.append(HRFlowable(width="100%", thickness=2, color=AMBER, spaceAfter=10))

    E.append(Paragraph("Em resumo", H2))
    E.append(Paragraph(
        "A automação na Inpasa deixou de ser apenas o ato de controlar a planta — manter variáveis "
        "no setpoint — para se tornar a capacidade de <b>enxergar e governar o estado da planta em "
        "tempo real</b>. O operador passa a atuar como vigia; o sistema opera e audita a si mesmo. "
        "Esta evolução já é mensurável, está em execução por meio de pilotos concretos, e aponta "
        "para um destino claro: a operação autônoma e um Centro de Operações Integrado para todo o "
        "Grupo.", LEAD))

    E.append(Paragraph("1. Contexto e propósito", H1))
    E.append(Paragraph(
        "Este documento consolida a visão e a jornada de evolução da automação na Inpasa, servindo "
        "de base para o alinhamento institucional com a liderança e com os parceiros tecnológicos. "
        "A mensagem central é de protagonismo: a Inpasa sabe aonde quer chegar e tem dado os passos "
        "com método e medição. Aos parceiros cabe acelerar essa visão com tecnologia robusta, "
        "escalável e respeitosa à jornada já construída.", BODY))

    E.append(Paragraph("2. A virada de chave", H1))
    E.append(Paragraph(
        "Por muito tempo, automação significou controlar a planta. O salto que perseguimos é outro: "
        "<b>enxergar e governar</b> o estado da planta continuamente. Isso se apoia em três pilares:", BODY))
    E.append(bullets([
        "<b>Controle</b> — malhas estáveis, automáticas e auditadas.",
        "<b>Gestão de alarmes</b> — foco no que realmente exige ação do operador.",
        "<b>Manutenção preditiva</b> — agir antes da falha, preservando ativos e produção.",
    ]))

    E.append(Paragraph("3. Onde estamos hoje: evidência medida", H1))
    E.append(Paragraph(
        "A maturidade da nossa automação não é aspiração — é dado. O estado das malhas de controle "
        "nos últimos 15 dias mostra alta adesão ao modo automático e, sobretudo, <b>visibilidade "
        "de cada exceção</b>:", BODY))
    data=[["Categoria","Auto","Manual","Programa","Operador","Bypass","Manut."],
          ["Utilidades","87","6","82","54","1","8"],
          ["Processo","147","22","125","27","0","1"]]
    t=Table(data, colWidths=[1.5*IN]+[0.78*IN]*6)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),9.5),
        ("FONTNAME",(0,1),(0,-1),"Helvetica-Bold"),("TEXTCOLOR",(0,1),(0,-1),NAVY),
        ("ALIGN",(1,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[white,LIGHT]),
        ("GRID",(0,0),(-1,-1),0.5,LINE),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    E.append(t); E.append(Spacer(1,6))
    E.append(Paragraph(
        "Em proporção, <b>94% das malhas de utilidades</b> e <b>87% das de processo</b> operam em "
        "automático. O mais relevante, porém, é que hoje cada malha em manual, cada interlock em "
        "bypass e cada variável em modo operador são <b>medidos e auditados</b> — o que antes era "
        "invisível tornou-se governança. (Nota de método: o estado considerado é o visto pela HMI; "
        "mudanças por lógica de PLC ainda não são auditadas — um limite que reconhecemos e que "
        "compõe o próximo passo de rigor.)", BODY))

    E.append(Paragraph("4. Gestão de ativos: o piloto de Dourados", H1))
    E.append(Paragraph(
        "Demos um passo além do controle: a gestão de ativos. Em Dourados, iniciamos um piloto de "
        "indicadores que já entrega visibilidade inédita sobre o parque de equipamentos:", BODY))
    E.append(bullets([
        "Monitoramento de equipamentos em <b>simulação</b> (objetos simulados em tempo real).",
        "Identificação de <b>ativos inoperantes</b> e de equipamentos fora de operação.",
        "<b>Auditoria de usuário</b>: quem simulou, em qual estação e há quanto tempo.",
        "<b>Tempo em simulação</b> — métrica inédita de disciplina operacional.",
    ]))
    E.append(Paragraph(
        "Após a validação dos resultados, a proposta é <b>expandir a solução para todas as unidades "
        "do Grupo Inpasa</b>, padronizando a gestão e aumentando a visibilidade operacional dos ativos.", BODY))

    E.append(Paragraph("5. Operação observatória", H1))
    E.append(Paragraph(
        "Esse caminho nos leva ao conceito de <b>operação observatória</b>: o operador supervisiona "
        "e o sistema opera. Mais do que isso, as próprias malhas de controle passam a funcionar como "
        "<b>sensores de saúde</b> — desvios em seu comportamento antecipam falhas antes que se tornem "
        "eventos. É a manutenção preditiva nascendo de dentro do próprio controle.", BODY))

    E.append(Paragraph("6. Arquitetura de dados (DataOps)", H1))
    E.append(Paragraph(
        "Nada disso se sustenta sem dados confiáveis e organizados. Estamos estruturando a arquitetura "
        "de dados operacionais da Inpasa em camadas — <b>coleta, historiação, contextualização e "
        "análise</b> — com varredura automática dos controladores para padronizar a informação em "
        "escala. Isso habilita o <b>benchmarking entre plantas</b>: saber qual unidade opera melhor, "
        "por quê, e levar a melhor prática às demais.", BODY))

    E.append(Paragraph("7. IA aplicada ao controle e à manutenção", H1))
    E.append(Paragraph(
        "Com a base de dados pronta, a inteligência artificial entra onde gera valor real:", BODY))
    E.append(bullets([
        "<b>Controle avançado e adaptativo</b>, que se ajusta ao processo e reduz variabilidade.",
        "<b>IA que aprende</b> com o processo e com a operação, predizendo resultados e recomendando ações.",
        "<b>Manutenção preditiva de verdade</b>, saindo do ciclo caro de corretiva e preventiva.",
    ]))
    E.append(Paragraph(
        "O resultado esperado é direto: menos paradas, mais confiabilidade, ativos preservados e uma "
        "operação progressivamente mais autônoma.", BODY))

    E.append(Paragraph("8. Centro de Operações Integrado (COI)", H1))
    E.append(Paragraph(
        "Tudo converge para o <b>Centro de Operações Integrado</b>: uma sala única de inteligência que "
        "integra as unidades do Grupo. A visão é de um COI robusto e escalável, inspirado em modelos "
        "já consolidados em indústrias de grande porte. Mais do que centralizar telas, trata-se de "
        "<b>centralizar a decisão</b> — autonomia operacional, otimização de mão de obra especializada "
        "e uma visão única do Grupo Inpasa.", BODY))

    E.append(Paragraph("9. Ecossistema de parceiros e frentes em curso", H1))
    E.append(Paragraph(
        "A jornada avança com apoio do ecossistema de automação. As frentes de trabalho técnicas já "
        "endereçam temas como racionalização de alarmes, monitoração de forces, bypass e simulações, "
        "tratamento de dados em massa, auto-tuning de malhas PID e estudos de caso de aplicação "
        "(a exemplo da caldeira de Dourados). Esse trabalho se organiza em fóruns técnicos e eventos "
        "de alinhamento que aproximam a operação da Inpasa das melhores práticas e tecnologias "
        "disponíveis no mercado, sempre preservando a neutralidade e o protagonismo da Inpasa na "
        "definição do destino.", BODY))

    E.append(Paragraph("10. Roadmap", H1))
    E.append(bullets([
        "<b>Hoje:</b> malhas medidas e auditadas + piloto de gestão de ativos em Dourados.",
        "<b>Curto prazo:</b> padronização de dados + gestão de ativos em todo o Grupo.",
        "<b>Médio prazo:</b> IA aplicada ao controle e à manutenção preditiva.",
        "<b>Visão:</b> Centro de Operações Integrado e operação autônoma.",
    ]))
    E.append(Paragraph(
        "Cada etapa entrega valor por si e prepara a seguinte — o caminho é incremental, medido e "
        "já está em movimento.", BODY))

    E.append(Spacer(1,6))
    E.append(HRFlowable(width="100%", thickness=1.5, color=BLUE2, spaceAfter=8))
    E.append(Paragraph("Mensagem-chave", H2))
    E.append(Paragraph(
        "<b>A Inpasa sabe aonde quer chegar.</b> Automação deixou de ser controlar a planta — passou "
        "a ser enxergar e governar o estado dela em tempo real. O operador vira vigia; o sistema audita "
        "cada malha e cada ativo. Buscamos parceiros que acelerem essa visão.", LEAD))

    doc.build(E)
    print("OK doc ->", path)

if __name__ == "__main__":
    base = "/home/user/ICG2025/apresentacao/"
    build_deck(base+"Visao_Inpasa_Automacao.pdf")
    build_doc(base+"Inpasa_Evolucao_Automacao.pdf")
