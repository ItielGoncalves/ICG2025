# -*- coding: utf-8 -*-
"""
Pacote estrategico (dados atualizados do dashboard v6 — 46 correias):
  - Apresentacao_Estrategica_Correias_INPASA.pptx
  - Apresentacao_Estrategica_Correias_INPASA.pdf
  - img_grupo_1_escopo.png / img_grupo_2_unidades.png / img_grupo_3_timeline.png
Uma unica base de dados alimenta tudo.
"""
import os
from datetime import date
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from PIL import Image, ImageDraw, ImageFont
import matplotlib

OUT = "/home/user/ICG2025/plano_seguranca"
FDIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
def F(bold=False, size=40):
    return ImageFont.truetype(os.path.join(FDIR, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

# ============ DADOS (dashboard v6) ============
raw = [
 ('NVM','TRL-519004-4','05/09/2026'),('NVM','TRL-519004-1','20/08/2026'),('NVM','TRL-519004-2','25/08/2026'),
 ('NVM','TRL-519004-3','30/08/2026'),('NVM','TRL-519004-5','10/09/2026'),('NVM','TRL-519424','05/08/2026'),
 ('NVM','TRL-519426','05/10/2026'),('NVM','TRL-519425','30/09/2026'),('NVM','TRL-719102','10/10/2026'),
 ('NVM','TRL-719104','20/09/2026'),('NVM','TRL-719103','05/10/2026'),('NVM','TRL-719101','15/10/2026'),
 ('NVM','TRL-509041','10/10/2026'),('NVM','TRL-519004-7','01/08/2026'),('NVM','TRL-519004-6','22/10/2026'),
 ('SNP','TRL-401002A','03/08/2026'),('SNP','TRL-401002B','10/08/2026'),('SNP','TRL-631501','30/11/2026'),
 ('SNP','TRL-631504','24/07/2026'),('SNP','TRL-631512','30/07/2026'),('SNP','TRL-409302','30/09/2026'),
 ('SNP','TRL-419419SA-1','30/09/2026'),('SNP','TRL-419419SA-2','07/10/2026'),('SNP','TRL-419419SB-2','07/10/2026'),
 ('SNP','TRL-419SB3','14/10/2026'),('SNP','TRL-419419SB-5','14/10/2026'),('SNP','TRL-419419SB-6','21/10/2026'),
 ('SNP','TRL-619038','21/10/2026'),('SNP','TRL-619023','29/10/2026'),('SNP','TRL-619041','29/10/2026'),
 ('SNP','TRL-1011235','11/10/2026'),
 ('SDL','TRL-1209011','24/07/2026'),('SDL','TRL-1219523','30/09/2026'),
 ('BLS','TRL-1519203A','SUBSTITUÍDA'),('BLS','TRL-1509208','10/07/2026'),('BLS','TRL-1509209','17/07/2026'),
 ('BLS','TRL-1509403','24/07/2026'),('BLS','ESTOQUE','30/09/2026'),
 ('SNP','TRL-1031004','30/10/2026'),('SNP','TRL-1031008','SUBSTITUÍDA'),('SNP','TRL-1031009','11/10/2026'),
 ('SNP','TRL-1031011','07/11/2026'),('SNP','TRL-1031012','15/11/2026'),('SNP','TRL-1219001','30/12/2026'),
 ('SNP','TRL-1219002','30/12/2026'),('NVM','TCD-501010','SUBSTITUÍDA'),
]
TODAY = date(2026, 7, 2)
def p(d):
    if d == 'SUBSTITUÍDA': return None
    dd, mm, yy = d.split('/'); return date(int(yy), int(mm), int(dd))
from collections import defaultdict
U = defaultdict(list)
for u, t, d in raw: U[u].append((t, p(d)))
ORDEM = ['NVM', 'SNP', 'SDL', 'BLS']
NOMES = {'NVM':'Nova Mutum','SNP':'Sinop','SDL':'Sidrolândia','BLS':'Balsas'}
HEX = {'NVM':'#3B82F6','SNP':'#F97316','SDL':'#22C55E','BLS':'#A855F7'}
def stat(u):
    rows = U[u]
    concl = sum(1 for _, dt in rows if dt is None)
    estoque = sum(1 for t, dt in rows if t == 'ESTOQUE')
    esteiras = [dt for t, dt in rows if dt and t != 'ESTOQUE']
    urg = sum(1 for _, dt in rows if dt and 0 <= (dt - TODAY).days <= 30)
    return dict(total=len(rows), concl=concl, estoque=estoque, urg=urg,
                last=max(esteiras), pend=len(rows) - concl)
ST = {u: stat(u) for u in ORDEM}
TOTAL = sum(s['total'] for s in ST.values())
CONCL = sum(s['concl'] for s in ST.values())
URG = sum(s['urg'] for s in ST.values())
GLAST = max(s['last'] for s in ST.values())
def fd(d): return d.strftime('%d/%m/%Y')

FRASE = {
 'NVM':"16 correias no plano; 1 já concluída. Última substituição em 22/10/2026.",
 'SNP':"23 correias no plano; 1 já concluída. Última em 30/12/2026 (esteiras de cavacos).",
 'SDL':"2 correias no plano. Ambas concluídas até 30/09/2026.",
 'BLS':"4 esteiras + 1 sobressalente; 1 concluída. Esteiras concluídas até 24/07/2026.",
}

# =====================================================================
# PPTX
# =====================================================================
def build_pptx():
    BG=RGBColor(0x0F,0x0F,0x1A); CARD=RGBColor(0x1E,0x1E,0x30); CARD2=RGBColor(0x25,0x25,0x38)
    LAR=RGBColor(0xF9,0x73,0x16); BR=RGBColor(0xFF,0xFF,0xFF); TXT=RGBColor(0xE0,0xE0,0xE0)
    MUT=RGBColor(0x9C,0xA3,0xAF); VERDE=RGBColor(0x22,0xC5,0x5E); VERM=RGBColor(0xEF,0x44,0x44)
    AMAR=RGBColor(0xEA,0xB3,0x08); GRID=RGBColor(0x2A,0x2A,0x40)
    COR={u:RGBColor(int(HEX[u][1:3],16),int(HEX[u][3:5],16),int(HEX[u][5:7],16)) for u in ORDEM}
    prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
    SW,SH=prs.slide_width,prs.slide_height; BLANK=prs.slide_layouts[6]
    def sl():
        s=prs.slides.add_slide(BLANK)
        b=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,SW,SH); b.fill.solid()
        b.fill.fore_color.rgb=BG; b.line.fill.background(); b.shadow.inherit=False; return s
    def rect(s,x,y,w,h,c,line=None,lw=1.0,rnd=False):
        sp=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rnd else MSO_SHAPE.RECTANGLE,x,y,w,h)
        sp.fill.solid(); sp.fill.fore_color.rgb=c
        if line is None: sp.line.fill.background()
        else: sp.line.color.rgb=line; sp.line.width=Pt(lw)
        sp.shadow.inherit=False; return sp
    def txt(s,x,y,w,h,t,size=18,bold=False,color=TXT,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,sp=None):
        tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
        tf.margin_left=Pt(2); tf.margin_right=Pt(2)
        for i,ln in enumerate(t.split('\n')):
            pa=tf.paragraphs[0] if i==0 else tf.add_paragraph(); pa.alignment=align
            if sp: pa.line_spacing=sp
            r=pa.add_run(); r.text=ln; r.font.size=Pt(size); r.font.bold=bold
            r.font.color.rgb=color; r.font.name='Inter'
        return tb
    def head(s,k,t):
        rect(s,0,0,SW,Inches(1.2),CARD); rect(s,0,Inches(1.2),SW,Inches(0.04),LAR)
        txt(s,Inches(0.55),Inches(0.16),Inches(12),Inches(0.3),k,size=12,bold=True,color=LAR)
        txt(s,Inches(0.55),Inches(0.46),Inches(12.2),Inches(0.6),t,size=25,bold=True,color=BR,anchor=MSO_ANCHOR.MIDDLE)
    def foot(s,n):
        txt(s,Inches(0.55),Inches(7.05),Inches(9),Inches(0.35),
            "INPASA  •  Plano de Substituição de Correias Transportadoras  •  ref. 02/07/2026",
            size=9,color=RGBColor(0x6B,0x72,0x80))
        txt(s,Inches(12.2),Inches(7.05),Inches(0.9),Inches(0.35),str(n),size=9,
            color=RGBColor(0x6B,0x72,0x80),align=PP_ALIGN.RIGHT)

    # 1 CAPA
    s=sl(); rect(s,0,Inches(4.55),SW,Inches(0.05),LAR)
    txt(s,Inches(0.9),Inches(1.5),Inches(11.5),Inches(0.5),"🏭  INPASA  •  APRESENTAÇÃO À DIRETORIA",size=15,bold=True,color=LAR)
    txt(s,Inches(0.9),Inches(2.25),Inches(11.6),Inches(1.8),"Plano de Substituição de\nCorreias Transportadoras",size=44,bold=True,color=BR,sp=1.05)
    txt(s,Inches(0.9),Inches(4.75),Inches(11.6),Inches(1.0),
        "Status do programa e cronograma de regularização por unidade\nNova Mutum • Sinop • Sidrolândia • Balsas",size=17,color=MUT,sp=1.2)
    txt(s,Inches(0.9),Inches(6.55),Inches(11.6),Inches(0.5),
        "Base: levantamento FLEXLAB (jun/2026) + plano de execução  |  Data de referência: 02/07/2026",size=12,color=RGBColor(0x6B,0x72,0x80))

    # 2 REGULARIZACAO POR UNIDADE
    s=sl(); head(s,"A PERGUNTA DA DIRETORIA","Quando cada unidade estará regularizada?")
    rect(s,Inches(0.55),Inches(1.45),Inches(12.25),Inches(0.85),CARD2,line=LAR,lw=1.25,rnd=True)
    txt(s,Inches(0.8),Inches(1.45),Inches(11.8),Inches(0.85),
        f"Programa concluído em  {fd(GLAST)}    |    {TOTAL} correias  •  {CONCL} já concluídas  •  {URG} urgentes (<=30 dias)  •  0 vencidas",
        size=15,bold=True,color=BR,anchor=MSO_ANCHOR.MIDDLE)
    cx=Inches(0.55); cw=Inches(2.95); gap=Inches(0.13); cy=Inches(2.55); ch=Inches(3.15)
    for i,u in enumerate(ORDEM):
        st=ST[u]; x=Emu(int(cx)+i*(int(cw)+int(gap)))
        rect(s,x,cy,cw,ch,CARD,rnd=True); rect(s,x,cy,cw,Inches(0.12),COR[u])
        txt(s,Emu(int(x)+Inches(0.2)),Emu(int(cy)+Inches(0.28)),Emu(int(cw)-Inches(0.4)),Inches(0.4),u,size=13,bold=True,color=COR[u])
        txt(s,Emu(int(x)+Inches(0.2)),Emu(int(cy)+Inches(0.62)),Emu(int(cw)-Inches(0.4)),Inches(0.5),NOMES[u],size=15,bold=True,color=BR)
        txt(s,Emu(int(x)+Inches(0.2)),Emu(int(cy)+Inches(1.15)),Emu(int(cw)-Inches(0.4)),Inches(0.35),"CONCLUÍDA EM",size=10,bold=True,color=MUT)
        txt(s,Emu(int(x)+Inches(0.2)),Emu(int(cy)+Inches(1.42)),Emu(int(cw)-Inches(0.4)),Inches(0.55),fd(st['last']),size=22,bold=True,color=COR[u])
        txt(s,Emu(int(x)+Inches(0.2)),Emu(int(cy)+Inches(2.05)),Emu(int(cw)-Inches(0.4)),Inches(1.0),FRASE[u],size=10.5,color=TXT,sp=1.05)
    foot(s,2)

    # 3 CRONOGRAMA (jul-dez)
    s=sl(); head(s,"LINHA DO TEMPO","Marcos de conclusão (jul → dez/2026)")
    tl_x=Inches(2.6); tl_w=Inches(9.9); start=date(2026,7,1); end=date(2026,12,31); span=(end-start).days; top=Inches(1.75)
    for name,m in [('Jul',7),('Ago',8),('Set',9),('Out',10),('Nov',11),('Dez',12)]:
        md=date(2026,m,1); px=int(tl_x)+int(((md-start).days/span)*int(tl_w))
        rect(s,Emu(px),Emu(int(top)),Pt(1),Inches(4.4),GRID)
        txt(s,Emu(px),Emu(int(top)-Inches(0.02)),Inches(1.4),Inches(0.3),name,size=12,bold=True,color=LAR)
    hx=int(tl_x)+int(((TODAY-start).days/span)*int(tl_w))
    rect(s,Emu(hx),Emu(int(top)+Inches(0.3)),Pt(2),Inches(4.05),VERM)
    txt(s,Emu(hx-Inches(0.3)),Emu(int(top)+Inches(0.02)),Inches(1.2),Inches(0.28),"HOJE",size=10,bold=True,color=VERM)
    rowh=Inches(0.95); ry=Emu(int(top)+Inches(0.55))
    for u in ORDEM:
        st=ST[u]
        txt(s,Inches(0.55),ry,Inches(1.95),rowh,f"{u} · {NOMES[u]}\n{st['total']} correias",size=11,bold=True,color=COR[u],anchor=MSO_ANCHOR.MIDDLE)
        x0=int(tl_x); x1=int(tl_x)+int(((st['last']-start).days/span)*int(tl_w))
        rect(s,Emu(x0),Emu(int(ry)+Inches(0.22)),Emu(max(x1-x0,int(Inches(0.2)))),Inches(0.42),COR[u],rnd=True)
        txt(s,Emu(x1+Inches(0.1)),Emu(int(ry)+Inches(0.2)),Inches(1.8),Inches(0.45),fd(st['last']),size=11,bold=True,color=BR,anchor=MSO_ANCHOR.MIDDLE)
        ry=Emu(int(ry)+int(rowh))
    txt(s,Inches(0.55),Inches(6.5),Inches(12),Inches(0.4),
        f"Conclusão de todo o programa: {fd(GLAST)} (última — Sinop, esteiras de cavacos da biomassa).",size=13,bold=True,color=LAR)
    foot(s,3)

    # 4 RECONCILIACAO
    s=sl(); head(s,"CONSISTÊNCIA DOS NÚMEROS","Reconciliação: levantamento × execução")
    # esquerda: levantamento
    rect(s,Inches(0.55),Inches(1.55),Inches(6.0),Inches(4.9),CARD,rnd=True)
    txt(s,Inches(0.8),Inches(1.75),Inches(5.5),Inches(0.4),"Levantamento FLEXLAB (jun/2026)",size=15,bold=True,color=LAR)
    for i,(t,c) in enumerate([
        ("148 correias auditadas no grupo",BR),
        ("102 mantidas em operação (conforme norma / 2ª linha)",MUT),
        ("46 a substituir  →  R$ 6,15 mi",BR),
        ("   • 41 reprovadas no ensaio ISO 340 (imediata)",MUT),
        ("   • 5 por degradação física (programada)",MUT)]):
        txt(s,Inches(0.85),Emu(int(Inches(2.35))+i*int(Inches(0.72))),Inches(5.5),Inches(0.7),("•  " if i in (0,2) else "")+t,size=13,color=c,bold=(i==2))
    # direita: execucao
    rect(s,Inches(6.8),Inches(1.55),Inches(6.0),Inches(4.9),CARD,rnd=True)
    txt(s,Inches(7.05),Inches(1.75),Inches(5.5),Inches(0.4),"Plano de execução (dashboard atual)",size=15,bold=True,color=VERDE)
    for i,(t,c) in enumerate([
        (f"{TOTAL} correias no plano  ✓ bate com as 46",BR),
        (f"   • {CONCL} já concluídas",MUT),
        (f"   • {TOTAL-CONCL} em execução",MUT),
        (f"Conclusão: {fd(GLAST)}",BR),
        ("0 correias vencidas",MUT)]):
        txt(s,Inches(7.1),Emu(int(Inches(2.35))+i*int(Inches(0.72))),Inches(5.5),Inches(0.7),("•  " if i in (0,3) else "")+t,size=13,color=c,bold=(i in(0,3)))
    txt(s,Inches(0.55),Inches(6.55),Inches(12.3),Inches(0.5),
        "Obs.: padronizar código NMT/NVM (mesma planta) · confirmar unidades DRD e LEM · 1 dos 46 é sobressalente em estoque (45 esteiras físicas).",
        size=10.5,color=AMAR)
    foot(s,4)

    # 5 ACAO / PCM
    s=sl(); head(s,"DECISÃO E AÇÃO","Cuidado especial até concluir a substituição")
    rect(s,Inches(0.55),Inches(1.55),Inches(6.0),Inches(4.9),CARD,rnd=True)
    txt(s,Inches(0.8),Inches(1.75),Inches(5.5),Inches(0.4),"⚠  Pontos de atenção",size=16,bold=True,color=VERM)
    for i,r in enumerate([
        f"{URG} correias urgentes (<=30 dias) — biomassa (SNP), DDGS (SDL/BLS), julho.",
        "Conclusão do programa depende da SNP (esteiras de cavacos, 30/12/2026).",
        "Biomassa e grãos: maior exposição a incêndio por atrito (rolete/correia).",
        "Janela de transição: risco elevado até a troca de todas as correias.",
    ]):
        txt(s,Inches(0.85),Emu(int(Inches(2.35))+i*int(Inches(1.0))),Inches(5.4),Inches(1.0),"•  "+r,size=13,color=TXT,sp=1.05)
    rect(s,Inches(6.8),Inches(1.55),Inches(6.0),Inches(4.9),CARD,rnd=True)
    txt(s,Inches(7.05),Inches(1.75),Inches(5.5),Inches(0.4),"✓  Encaminhamentos",size=16,bold=True,color=VERDE)
    for i,pz in enumerate([
        "PCM acionado para alinhar com TODAS as áreas cuidado reforçado até concluir a substituição das correias.",
        "Priorizar as correias urgentes de julho (biomassa/DDGS).",
        "Reporte quinzenal de avanço por unidade (concluídas x plano).",
        "Padronizar cadastro (NMT/NVM) e confirmar DRD/LEM.",
    ]):
        txt(s,Inches(7.1),Emu(int(Inches(2.35))+i*int(Inches(1.0))),Inches(5.4),Inches(1.0),"•  "+pz,size=13,color=TXT,sp=1.05)
    foot(s,5)

    path=os.path.join(OUT,"Apresentacao_Estrategica_Correias_INPASA.pptx"); prs.save(path)
    print("PPTX:",path,"slides:",len(prs.slides._sldIdLst))

# =====================================================================
# PDF
# =====================================================================
def build_pdf():
    BG='#0F0F1A';CARD='#1E1E30';CARD2='#252538';LAR='#F97316';BR='#FFFFFF';TXT='#E0E0E0'
    MUT='#9CA3AF';VERDE='#22C55E';VERM='#EF4444';AMAR='#EAB308';GRID='#2A2A40'
    W,H=960,540
    def PT(i): return i*72.0
    path=os.path.join(OUT,"Apresentacao_Estrategica_Correias_INPASA.pdf")
    c=canvas.Canvas(path,pagesize=(W,H))
    def box(x,yt,w,h,fill,rad=0,stroke=None,sw=1):
        c.setFillColor(HexColor(fill)); do=0
        if stroke: c.setStrokeColor(HexColor(stroke)); c.setLineWidth(sw); do=1
        yb=H-PT(yt)-PT(h)
        (c.roundRect if rad else c.rect)(PT(x),yb,PT(w),PT(h),*( (rad,) if rad else ()),fill=1,stroke=do)
    def line(x,yt,w,h,fill): box(x,yt,w,h,fill)
    def text(x,yt,s,size,fill,bold=False,align='l'):
        c.setFont('Helvetica-Bold' if bold else 'Helvetica',size); c.setFillColor(HexColor(fill)); yb=H-PT(yt)-size
        (c.drawCentredString if align=='c' else c.drawRightString if align=='r' else c.drawString)(PT(x),yb,s)
    def para(x,yt,wi,s,size,fill,bold=False,lead=None):
        f='Helvetica-Bold' if bold else 'Helvetica'; c.setFont(f,size); c.setFillColor(HexColor(fill))
        y=H-PT(yt)-size; lead=lead or size*1.25
        for ln in simpleSplit(s,f,size,PT(wi)): c.drawString(PT(x),y,ln); y-=lead
    def bg(): c.setFillColor(HexColor(BG)); c.rect(0,0,W,H,fill=1,stroke=0)
    def head(k,t):
        box(0,0,13.333,1.2,CARD); line(0,1.2,13.333,0.045,LAR)
        text(0.55,0.18,k,11,LAR,bold=True); text(0.55,0.52,t,22,BR,bold=True)
    def foot(n):
        text(0.55,7.08,"INPASA  •  Plano de Substituição de Correias Transportadoras  •  ref. 02/07/2026",8,'#6B7280')
        text(12.75,7.08,str(n),8,'#6B7280',align='r')
    COR=HEX
    # 1 CAPA
    bg(); line(0,4.55,13.333,0.05,LAR)
    text(0.9,1.5,"INPASA  •  APRESENTAÇÃO À DIRETORIA",14,LAR,bold=True)
    text(0.9,2.35,"Plano de Substituição de",37,BR,bold=True); text(0.9,3.15,"Correias Transportadoras",37,BR,bold=True)
    text(0.9,4.8,"Status do programa e cronograma de regularização por unidade",15,MUT)
    text(0.9,5.15,"Nova Mutum  •  Sinop  •  Sidrolândia  •  Balsas",15,MUT)
    text(0.9,6.6,"Base: levantamento FLEXLAB (jun/2026) + plano de execução   |   ref. 02/07/2026",11,'#6B7280'); c.showPage()
    # 2 UNIDADES
    bg(); head("A PERGUNTA DA DIRETORIA","Quando cada unidade estará regularizada?")
    box(0.55,1.45,12.25,0.85,CARD2,rad=8,stroke=LAR,sw=1.3)
    text(6.9,1.78,f"Programa concluído em {fd(GLAST)}    |    {TOTAL} correias  •  {CONCL} concluídas  •  {URG} urgentes  •  0 vencidas",13,BR,bold=True,align='c')
    cw=2.95;gap=0.13;cx=0.55;cy=2.55;ch=3.15
    for i,u in enumerate(ORDEM):
        st=ST[u]; x=cx+i*(cw+gap); box(x,cy,cw,ch,CARD,rad=8); line(x,cy,cw,0.12,COR[u])
        text(x+0.2,cy+0.3,u,13,COR[u],bold=True); text(x+0.2,cy+0.62,NOMES[u],14,BR,bold=True)
        text(x+0.2,cy+1.18,"CONCLUÍDA EM",9,MUT,bold=True); text(x+0.2,cy+1.45,fd(st['last']),21,COR[u],bold=True)
        para(x+0.2,cy+2.05,cw-0.4,FRASE[u],9.5,TXT,lead=12)
    foot(2); c.showPage()
    # 3 CRONOGRAMA
    bg(); head("LINHA DO TEMPO","Marcos de conclusão (jul -> dez/2026)")
    tl_x=2.6;tl_w=9.9;start=date(2026,7,1);end=date(2026,12,31);span=(end-start).days;top=1.75
    for name,m in [('Jul',7),('Ago',8),('Set',9),('Out',10),('Nov',11),('Dez',12)]:
        md=date(2026,m,1);fx=tl_x+((md-start).days/span)*tl_w; box(fx,top,0.014,4.4,GRID); text(fx,top-0.02,name,12,LAR,bold=True)
    hx=tl_x+((TODAY-start).days/span)*tl_w; box(hx,top+0.3,0.028,4.05,VERM); text(hx-0.28,top+0.02,"HOJE",9.5,VERM,bold=True)
    rowh=0.95;ry=top+0.55
    for u in ORDEM:
        st=ST[u]; text(0.55,ry+0.24,f"{u} · {NOMES[u]}",11,COR[u],bold=True); text(0.55,ry+0.5,f"{st['total']} correias",9,MUT)
        x1=tl_x+((st['last']-start).days/span)*tl_w; box(tl_x,ry+0.22,max(x1-tl_x,0.2),0.42,COR[u],rad=4)
        text(x1+0.1,ry+0.32,fd(st['last']),11,BR,bold=True); ry+=rowh
    text(0.55,6.55,f"Conclusão de todo o programa: {fd(GLAST)} (última — Sinop, esteiras de cavacos).",13,LAR,bold=True); foot(3); c.showPage()
    # 4 RECONCILIACAO
    bg(); head("CONSISTÊNCIA DOS NÚMEROS","Reconciliação: levantamento × execução")
    box(0.55,1.55,6.0,4.9,CARD,rad=8); text(0.8,1.78,"Levantamento FLEXLAB (jun/2026)",15,LAR,bold=True)
    L=[("•  148 correias auditadas no grupo",BR),("102 mantidas em operação",MUT),("•  46 a substituir  ->  R$ 6,15 mi",BR),
       ("   - 41 reprovadas ISO 340 (imediata)",MUT),("   - 5 degradação física (programada)",MUT)]
    for i,(t,cc) in enumerate(L): text(0.85,2.35+i*0.6,t,13,cc,bold=(i==2))
    box(6.8,1.55,6.0,4.9,CARD,rad=8); text(7.05,1.78,"Plano de execução (dashboard atual)",15,VERDE,bold=True)
    R=[(f"•  {TOTAL} correias no plano  (bate com as 46)",BR),(f"   - {CONCL} já concluídas",MUT),
       (f"   - {TOTAL-CONCL} em execução",MUT),(f"•  Conclusão: {fd(GLAST)}",BR),("   - 0 correias vencidas",MUT)]
    for i,(t,cc) in enumerate(R): text(7.1,2.35+i*0.6,t,13,cc,bold=(i in(0,3)))
    para(0.55,6.5,12.3,"Obs.: padronizar código NMT/NVM (mesma planta) · confirmar unidades DRD e LEM · 1 dos 46 é sobressalente em estoque (45 esteiras físicas).",10.5,AMAR); foot(4); c.showPage()
    # 5 ACAO
    bg(); head("DECISÃO E AÇÃO","Cuidado especial até concluir a substituição")
    box(0.55,1.55,6.0,4.9,CARD,rad=8); text(0.8,1.78,"! Pontos de atenção",15,VERM,bold=True)
    A=[f"{URG} correias urgentes (<=30 dias) — biomassa (SNP), DDGS (SDL/BLS), julho.",
       "Conclusão do programa depende da SNP (esteiras de cavacos, 30/12/2026).",
       "Biomassa e grãos: maior exposição a incêndio por atrito.",
       "Janela de transição: risco elevado até a troca de todas as correias."]
    ty=2.35
    for r in A: para(0.85,ty,5.4,"•  "+r,12,TXT,lead=15); ty+=0.9
    box(6.8,1.55,6.0,4.9,CARD,rad=8); text(7.05,1.78,"> Encaminhamentos",15,VERDE,bold=True)
    B=["PCM acionado para alinhar com TODAS as áreas cuidado reforçado até concluir a substituição.",
       "Priorizar as correias urgentes de julho (biomassa/DDGS).",
       "Reporte quinzenal de avanço por unidade.",
       "Padronizar cadastro (NMT/NVM) e confirmar DRD/LEM."]
    ty=2.35
    for r in B: para(7.1,ty,5.4,"•  "+r,12,TXT,lead=15); ty+=0.9
    foot(5); c.save(); print("PDF:",path)

# =====================================================================
# IMAGENS (PNG) PARA O GRUPO
# =====================================================================
def hx(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
BG=hx('#0F0F1A');CARD=hx('#1E1E30');CARD2=hx('#252538');LAR=hx('#F97316');BR=(255,255,255)
TXT=hx('#E0E0E0');MUT=hx('#9CA3AF');VERDE=hx('#22C55E');VERM=hx('#EF4444');AMAR=hx('#EAB308');GRID=hx('#2A2A40')
COR={u:hx(HEX[u]) for u in ORDEM}
Wp=1080

def new_img(h):
    im=Image.new('RGB',(Wp,h),BG); d=ImageDraw.Draw(im); return im,d
def brand(d,h):
    d.rectangle([0,0,Wp,96],fill=CARD); d.rectangle([0,96,Wp,100],fill=LAR)
    d.text((48,30),"INPASA — Substituição de Correias",font=F(True,34),fill=LAR)
    d.text((48,h-46),"Manutenção & Automação · ref. 02/07/2026",font=F(False,20),fill=MUT)

def img_escopo():
    h=1080; im,d=new_img(h); brand(d,h)
    d.text((48,150),"Programa de substituição — visão geral",font=F(True,44),fill=BR)
    kpis=[("46","correias no plano",BR),("3","já concluídas",VERDE),("43","em execução",LAR),
          ("0","vencidas",VERDE),("R$ 6,15 mi","investimento (46)",BR),("7","urgentes (≤30d)",AMAR)]
    x0,y0,cw,chh,gx,gy=48,260,320,190,24,28
    for i,(v,lb,cc) in enumerate(kpis):
        r,cidx=divmod(i,3); x=x0+cidx*(cw+gx); y=y0+r*(chh+gy)
        d.rounded_rectangle([x,y,x+cw,y+chh],radius=18,fill=CARD)
        d.rectangle([x,y,x+8,y+chh],fill=LAR)
        vsize=60 if len(v)<=3 else (44 if len(v)<=6 else 38)
        d.text((x+30,y+66),v,font=F(True,vsize),fill=cc,anchor='lm')
        d.text((x+30,y+140),lb,font=F(False,24),fill=MUT,anchor='lm')
    yb=y0+2*(chh+gy)+30
    d.rounded_rectangle([48,yb,Wp-48,yb+150],radius=18,fill=CARD2,outline=LAR,width=2)
    d.text((Wp//2,yb+42),"Conclusão de todo o programa",font=F(False,28),fill=MUT,anchor='mm')
    d.text((Wp//2,yb+100),fd(GLAST),font=F(True,58),fill=LAR,anchor='mm')
    path=os.path.join(OUT,"img_grupo_1_escopo.png"); im.save(path); print("IMG:",path)

def img_unidades():
    h=1080; im,d=new_img(h); brand(d,h)
    d.text((48,150),"Quando cada unidade fica pronta",font=F(True,44),fill=BR)
    ordem=sorted(ORDEM,key=lambda u:ST[u]['last'])
    y=260; rh=150
    for u in ordem:
        st=ST[u]; d.rounded_rectangle([48,y,Wp-48,y+rh-20],radius=18,fill=CARD)
        d.rectangle([48,y,58,y+rh-20],fill=COR[u])
        d.text((90,y+28),f"{u} · {NOMES[u]}",font=F(True,38),fill=COR[u])
        extra=f"{st['total']} correias · {st['concl']} concluída(s)"
        if st['estoque']: extra+=" · +1 sobressalente"
        d.text((90,y+82),extra,font=F(False,24),fill=MUT)
        d.text((Wp-80,y+40),fd(st['last']),font=F(True,46),fill=BR,anchor='rm')
        d.text((Wp-80,y+92),"concluída em",font=F(False,22),fill=MUT,anchor='rm')
        y+=rh
    d.rounded_rectangle([48,y,Wp-48,y+120],radius=18,fill=CARD2,outline=LAR,width=2)
    d.text((Wp//2,y+60),f"Todas as unidades concluídas até {fd(GLAST)}",font=F(True,36),fill=LAR,anchor='mm')
    path=os.path.join(OUT,"img_grupo_2_unidades.png"); im.save(path); print("IMG:",path)

def img_timeline():
    h=920; im,d=new_img(h); brand(d,h)
    d.text((48,140),"Linha do tempo — conclusão por unidade",font=F(True,40),fill=BR)
    lx,rx=300,Wp-60; top=250; start=date(2026,7,1); end=date(2026,12,31); span=(end-start).days
    for name,m in [('Jul',7),('Ago',8),('Set',9),('Out',10),('Nov',11),('Dez',12)]:
        md=date(2026,m,1); px=lx+int(((md-start).days/span)*(rx-lx))
        d.line([(px,top),(px,top+430)],fill=GRID,width=2); d.text((px,top-30),name,font=F(True,22),fill=LAR,anchor='mm')
    hxp=lx+int(((TODAY-start).days/span)*(rx-lx)); d.line([(hxp,top),(hxp,top+430)],fill=VERM,width=3)
    d.text((hxp-4,top-64),"HOJE",font=F(True,20),fill=VERM,anchor='mm')
    y=top+30; rh=95
    for u in sorted(ORDEM,key=lambda z:ST[z]['last']):
        st=ST[u]; d.text((60,y+30),f"{u}",font=F(True,30),fill=COR[u])
        d.text((60,y+64),f"{st['total']} corr.",font=F(False,20),fill=MUT)
        x1=lx+int(((st['last']-start).days/span)*(rx-lx))
        d.rounded_rectangle([lx,y+20,max(x1,lx+6),y+62],radius=8,fill=COR[u])
        d.text((min(x1+14,rx-140),y+22),fd(st['last']),font=F(True,24),fill=BR)
        y+=rh
    d.text((Wp//2,h-70),f"Programa concluído em {fd(GLAST)}",font=F(True,32),fill=LAR,anchor='mm')
    path=os.path.join(OUT,"img_grupo_3_timeline.png"); im.save(path); print("IMG:",path)

build_pptx(); build_pdf(); img_escopo(); img_unidades(); img_timeline()
print("OK — pacote gerado.")
