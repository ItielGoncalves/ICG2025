#!/usr/bin/env python3
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# cores
INK=RGBColor(0x1E,0x29,0x3B); MUTED=RGBColor(0x5A,0x67,0x7C); WHITE=RGBColor(0xFF,0xFF,0xFF)
PAGE=RGBColor(0xED,0xF2,0xF8); CARD=RGBColor(0xFF,0xFF,0xFF); BORDER=RGBColor(0xCB,0xD5,0xE1)
GREEN=RGBColor(0x16,0xA3,0x4A); RED=RGBColor(0xDC,0x26,0x26); BLUE=RGBColor(0x25,0x63,0xEB)
AMBER=RGBColor(0xD9,0x77,0x06); TEAL=RGBColor(0x0D,0x94,0x88); GRAY=RGBColor(0x6B,0x72,0x80)

def tint(c,p=0.88):
    return RGBColor(int(c[0]+(255-c[0])*p),int(c[1]+(255-c[1])*p),int(c[2]+(255-c[2])*p))

prs=Presentation()
prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
s=prs.slides.add_slide(prs.slide_layouts[6])

def IN(v): return Inches(v)

def bg(slide,color):
    r=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,prs.slide_width,prs.slide_height)
    r.fill.solid(); r.fill.fore_color.rgb=color; r.line.fill.background()
    r.shadow.inherit=False
    slide.shapes._spTree.remove(r._element); slide.shapes._spTree.insert(2,r._element)
    return r
bg(s,PAGE)

def box(x,y,w,h,fill=None,line=None,line_w=1.0,rounded=False,radius=0.08):
    shp=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,IN(x),IN(y),IN(w),IN(h))
    if rounded:
        try: shp.adjustments[0]=radius
        except: pass
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb=fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb=line; shp.line.width=Pt(line_w)
    shp.shadow.inherit=False
    return shp

def txt(x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,wrap=True):
    tb=s.shapes.add_textbox(IN(x),IN(y),IN(w),IN(h)); tf=tb.text_frame
    tf.word_wrap=wrap; tf.vertical_anchor=anchor
    tf.margin_left=Pt(2); tf.margin_right=Pt(2); tf.margin_top=Pt(1); tf.margin_bottom=Pt(1)
    if isinstance(runs[0],tuple): runs=[runs]
    for i,para in enumerate(runs):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align
        for (tval,size,color,bold) in para:
            r=p.add_run(); r.text=tval; r.font.size=Pt(size); r.font.color.rgb=color
            r.font.bold=bold; r.font.name="Calibri"
    return tb

# ===== Título =====
txt(0.35,0.20,12.6,0.6,[("QUADRO POR EQUIPAMENTO — LIBERAÇÃO DOS CIRCUITOS",26,INK,True)])
txt(0.37,0.72,12.6,0.35,[("Recuperação Sistema de Grãos — Sinop 2026 (R.0)   •   atividades pequenas suprimidas",13,MUTED,False)])

# ===== Placeholder da FOTO (esquerda) =====
ph=box(0.35,1.15,8.0,3.35,fill=tint(BLUE,0.94),line=BLUE,line_w=2.0,rounded=True,radius=0.04)
# tracejado visual via texto
txt(0.35,2.35,8.0,1.0,[
    [("📷  ÁREA PARA A FOTO",20,BLUE,True)],
    [("Insira aqui a foto do sistema (Inserir ▸ Imagem) e ajuste sobre esta área",12,MUTED,False)],
    [("Sugestão de rótulos sobre a foto:  EL-F · CT-03 · EL-E · Duto · CT-04  +  fluxo alimentação (verde) / descarga (vermelho)",11,MUTED,False)],
],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)

# ===== Painel direito: liberação por equipamento =====
rx=8.55; rw=4.45
box(rx,1.15,rw,3.35,fill=CARD,line=BORDER,line_w=1.5,rounded=True,radius=0.04)
txt(rx+0.25,1.30,rw-0.5,0.4,[("LIBERAÇÃO POR EQUIPAMENTO",15,INK,True)])
rows=[("EL-E","✖ Danificado — fora da safra",GRAY),
      ("CT-04","Qua 17/06  19:00",TEAL),
      ("EL-F","Qui 18/06  11:00",GREEN),
      ("Duto","Sex 19/06  01:00",AMBER),
      ("CT-03","Sáb 20/06  07:00",BLUE)]
yy=1.78
for nome,dt,col in rows:
    dot=box(rx+0.28,yy+0.04,0.18,0.18,fill=col,rounded=True,radius=0.5)
    txt(rx+0.55,yy-0.02,1.5,0.3,[(nome,15,INK,True)])
    txt(rx+1.7,yy-0.02,rw-1.95,0.3,[(dt,14,col,True)],align=PP_ALIGN.RIGHT)
    yy+=0.42
# hero milho
hy=yy+0.10
box(rx+0.2,hy,rw-0.4,1.0,fill=tint(BLUE,0.90),line=BLUE,line_w=2.0,rounded=True,radius=0.10)
txt(rx+0.2,hy+0.08,rw-0.4,0.9,[
    [("🌽 RECEBIMENTO DE MILHO — LIBERADO EM",13,INK,True)],
    [("Sáb 20/06 · 07:00",24,BLUE,True)],
],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)

# ===== Cards (5) =====
cards=[
 ("CT-03","Correia principal (alim. + descarga)",BLUE,"Sáb 20/06  07:00","23 serviços · 90 h",
   ["Reforma estrutural – 16 módulos (60 h)","Revisão motorredutores A e B (48 h)",
    "Roletes de carga – 270 un (40 h)","Sensores / PT100 / desalinh. (40 h)",
    "Emenda de cabos elétricos (36 h)","★ Passagem + emenda a quente da correia"]),
 ("CT-04","Correia de descarga (via Duto)",TEAL,"Qua 17/06  19:00","8 serviços · 30 h",
   ["Corte + novo trecho 15 m (18 h)","Emborrachamento tambor retorno (10 h)",
    "Chegada rolamentos / mancais (12 h)","★ Emenda de 15 m da correia (12 h)"]),
 ("EL-F","Elevador de alimentação",GREEN,"Qui 18/06  11:00","2 serviços · 40 h",
   ["Substituir 30 canecas (18 h)","★ Revestimento dutos – Rhynoride (36 h)"]),
 ("Duto","Transferência CT-03 → CT-04",AMBER,"Sex 19/06  01:00","1 serviço · 36 h",
   ["★ Duto da CT-03 para a CT-04 (36 h)"]),
 ("EL-E","Elevador de descarga",GRAY,"FORA DE ESCOPO","danificado",
   ["Danificado na ocorrência","NÃO requerido p/ a safra (milho)","✖ Fora do escopo — recuperar depois"]),
]
cx=0.35; cy=4.70; cw=2.52; ch=2.10; gap=0.105
for nome,func,cor,libera,meta,acts in cards:
    box(cx,cy,cw,ch,fill=CARD,line=BORDER,line_w=1.0,rounded=True,radius=0.06)
    box(cx,cy,cw,0.42,fill=cor,rounded=True,radius=0.10)
    box(cx,cy+0.21,cw,0.21,fill=cor)
    txt(cx+0.12,cy+0.02,cw-0.2,0.4,[(nome,18,WHITE,True)],anchor=MSO_ANCHOR.MIDDLE)
    txt(cx+0.12,cy+0.46,cw-0.2,0.45,[
        [(func,9.5,INK,True)],[(meta,8.5,MUTED,False)]])
    # bullets
    runs=[]
    for a in acts:
        star=a.startswith("★"); bad=a.startswith("✖")
        col=cor if star else (GRAY if bad else INK)
        runs.append([(a,8.7,col,star or bad)])
    txt(cx+0.12,cy+0.92,cw-0.22,0.95,runs)
    # selo
    box(cx+0.12,cy+ch-0.42,cw-0.24,0.32,fill=tint(cor,0.90),line=cor,line_w=1.2,rounded=True,radius=0.18)
    txt(cx+0.12,cy+ch-0.42,cw-0.24,0.32,[
        [("LIBERAÇÃO  ",8,MUTED,True),(libera,11,cor,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    cx+=cw+gap

# ===== Rodapé circuitos =====
box(0.35,6.95,12.63,0.42,fill=CARD,line=BORDER,line_w=1.0,rounded=True,radius=0.2)
txt(0.5,6.96,6.2,0.4,[[("ALIMENTAÇÃO (EL-F→CT-03):  ",11,GREEN,True),("Sáb 20/06 07:00",11,INK,True)]],anchor=MSO_ANCHOR.MIDDLE)
txt(6.7,6.96,6.2,0.4,[[("DESCARGA (Duto→CT-04):  ",11,RED,True),("Sex 19/06 01:00  (EL-E fora da safra)",11,INK,True)]],anchor=MSO_ANCHOR.MIDDLE)

out="/home/user/ICG2025/quadro_equipamentos_sinop_2026.pptx"
prs.save(out)
print("saved",out)
