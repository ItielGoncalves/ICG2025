#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math

FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def F(s,b=True): return ImageFont.truetype(FB if b else FR, s)

# ---- tema claro ----
PAGE=(237,242,248); CARD=(255,255,255); BORDER=(203,213,225)
INK=(30,41,59); MUTED=(90,103,124); WHITE=(255,255,255)
GREEN=(22,163,74); RED=(220,38,38); BLUE=(37,99,235); AMBER=(217,119,6); TEAL=(13,148,136)
INPASA=(0,140,69)

W,H=2400,1620
img=Image.new("RGB",(W,H),PAGE); d=ImageDraw.Draw(img)
def t(xy,s,f,fill,anchor="lm"): d.text(xy,s,font=f,fill=fill,anchor=anchor)
def rr(b,r,fill,outline=None,wd=2): d.rounded_rectangle(b,radius=r,fill=fill,outline=outline,width=wd)
def tint(c,p=0.85):
    return tuple(int(c[i]+(255-c[i])*p) for i in range(3))

def arrow(p1,p2,color,wd=12,head=26):
    d.line([p1,p2],fill=color,width=wd)
    ang=math.atan2(p2[1]-p1[1],p2[0]-p1[0])
    for a in (ang+math.radians(148),ang-math.radians(148)):
        d.line([p2,(p2[0]+head*math.cos(a),p2[1]+head*math.sin(a))],fill=color,width=wd)

# ===== Logo Inpasa (wordmark) =====
lx2=W-50; lw=300; lh=92; lx1=lx2-lw; ly1=40; ly2=ly1+lh
rr((lx1,ly1,lx2,ly2),16,INPASA)
# folha
cx=lx1+44; cy=(ly1+ly2)//2
d.polygon([(cx-14,cy+16),(cx+18,cy-18),(cx+20,cy+8),(cx-2,cy+18)],fill=(190,242,200))
t((lx1+78,cy-10),"INPASA",F(34),WHITE,anchor="lm")
t((lx1+78,cy+22),"Agroindustrial",F(15,False),(200,240,210),anchor="lm")

# ===== Header =====
t((50,52),"QUADRO POR EQUIPAMENTO — LIBERAÇÃO DOS CIRCUITOS",F(46),INK)
t((50,104),"Recuperação Sistema de Grãos — Sinop 2026 (R.0)   •   atividades pequenas suprimidas",F(24,False),MUTED)

# ===== Diagrama de fluxo (sem sobreposição) =====
DX,DY,DW,DH=40,150,W-80,470
rr((DX,DY,DX+DW,DY+DH),18,CARD,BORDER,2)
t((DX+30,DY+34),"FLUXO E LIBERAÇÃO DOS CIRCUITOS",F(26),INK)

def node(cx,cy,nome,tipo,libera,cor,liberado=False):
    bw,bh=360,150
    x1,y1,x2,y2=cx-bw//2,cy-bh//2,cx+bw//2,cy+bh//2
    rr((x1,y1,x2,y2),14,tint(cor,0.88),cor,3)
    d.rounded_rectangle((x1,y1,x2,y1+46),radius=14,fill=cor)
    d.rectangle((x1,y1+24,x2,y1+46),fill=cor)
    t((cx,y1+23),nome,F(30),WHITE,anchor="mm")
    t((cx,y1+72),tipo,F(17,False),INK,anchor="mm")
    lab="✔ "+libera if liberado else libera
    t((cx,y1+108),lab,F(23),cor,anchor="mm")
    t((cx,y1+134),"liberação",F(14,False),MUTED,anchor="mm")
    return (x1,y1,x2,y2)

laneA=DY+150; laneB=DY+330
# lane labels
t((DX+90,laneA),"ALIMENTAÇÃO",F(22),GREEN,anchor="mm")
t((DX+90,laneB),"DESCARGA",F(22),RED,anchor="mm")
d.line([(DX+200,DY+70),(DX+200,DY+DH-30)],fill=BORDER,width=2)

ax=DX+420; gap=470
# Alimentação: EL-F -> CT-03
nA1=node(ax,laneA,"EL-F","Elevador de alimentação","Qui 18/06 11:00",GREEN)
nA2=node(ax+gap,laneA,"CT-03","Correia principal","Sáb 20/06 07:00",BLUE)
arrow((nA1[2]+12,laneA),(nA2[0]-14,laneA),GREEN)
# Descarga: EL-E -> Duto -> CT-04
nB1=node(ax,laneB,"EL-E","Elevador de descarga","Já liberado",GREEN,liberado=True)
nB2=node(ax+gap,laneB,"Duto","CT-03 → CT-04","Sex 19/06 01:00",AMBER)
nB3=node(ax+2*gap,laneB,"CT-04","Correia de descarga","Qua 17/06 19:00",TEAL)
arrow((nB1[2]+12,laneB),(nB2[0]-14,laneB),RED)
arrow((nB2[2]+12,laneB),(nB3[0]-14,laneB),RED)

# Hero sistema completo (à direita)
hx1=DX+DW-470; hy1=DY+110; hx2=DX+DW-40; hy2=DY+DH-40
rr((hx1,hy1,hx2,hy2),16,tint(BLUE,0.9),BLUE,4)
t(((hx1+hx2)//2,hy1+50),"SISTEMA COMPLETO",F(26),INK,anchor="mm")
t(((hx1+hx2)//2,hy1+115),"LIBERADO EM",F(20,False),MUTED,anchor="mm")
t(((hx1+hx2)//2,hy1+170),"Sáb 20/06",F(46),BLUE,anchor="mm")
t(((hx1+hx2)//2,hy1+225),"07:00",F(40),BLUE,anchor="mm")

# ===== Cards detalhados =====
cards=[
 ("CT-03","Correia principal (alim. + descarga)",BLUE,"Sáb 20/06  07:00","23 serviços · 90 h",False,
   ["Reforma estrutural – 16 módulos (60 h)",
    "Revisão motorredutores A e B (48 h)",
    "Roletes de carga – 270 un (40 h)",
    "Sensores / PT100 / desalinh. (40 h)",
    "Emenda de cabos elétricos (36 h)",
    "★ Passagem + emenda a quente da correia"]),
 ("CT-04","Correia de descarga (via Duto)",TEAL,"Qua 17/06  19:00","8 serviços · 30 h",False,
   ["Corte + novo trecho de correia 15 m (18 h)",
    "Emborrachamento tambor de retorno (10 h)",
    "Chegada de rolamentos / mancais (12 h)",
    "★ Emenda de 15 m da correia (12 h)"]),
 ("EL-F","Elevador de alimentação",GREEN,"Qui 18/06  11:00","2 serviços · 40 h",False,
   ["Substituir 30 canecas (18 h)",
    "★ Revestimento dutos – Rhynoride (36 h)"]),
 ("Duto","Transferência CT-03 → CT-04",AMBER,"Sex 19/06  01:00","1 serviço · 36 h",False,
   ["★ Duto da CT-03 para a CT-04 (36 h)"]),
 ("EL-E","Elevador de descarga",GREEN,"JÁ LIBERADO","sem intervenção",True,
   ["Não foi danificado",
    "Sem atividades na parada",
    "✔ Operacional / disponível"]),
]
cy0=DY+DH+30
cardW=(W-80-4*20)//5
cardH=H-cy0-200
for i,(nome,func,cor,libera,meta,liberado,acts) in enumerate(cards):
    x=40+i*(cardW+20)
    rr((x,cy0,x+cardW,cy0+cardH),16,CARD,BORDER,2)
    d.rounded_rectangle((x,cy0,x+cardW,cy0+70),radius=16,fill=cor)
    d.rectangle((x,cy0+36,x+cardW,cy0+70),fill=cor)
    t((x+22,cy0+35),nome,F(38),WHITE,anchor="lm")
    t((x+22,cy0+100),func,F(20,False),INK,anchor="lm")
    t((x+22,cy0+132),meta,F(18,False),MUTED,anchor="lm")
    d.line([(x+18,cy0+158),(x+cardW-18,cy0+158)],fill=BORDER,width=1)
    yy=cy0+186
    t((x+22,yy),"PRINCIPAIS SERVIÇOS",F(16),MUTED,anchor="lm"); yy+=34
    for a in acts:
        star=a.strip().startswith("★"); chk=a.strip().startswith("✔")
        col = cor if star else (GREEN if chk else INK)
        fnt=F(21, star or chk)
        words=a.split(); line=""; lines=[]
        for w in words:
            test=(line+" "+w).strip()
            if d.textlength(test,font=fnt)>cardW-44: lines.append(line); line=w
            else: line=test
        lines.append(line)
        for ln in lines:
            t((x+22,yy),ln,fnt,col,anchor="lm"); yy+=30
        yy+=8
    # selo liberação
    by=cy0+cardH-92
    sealbg = tint(GREEN,0.85) if liberado else tint(cor,0.9)
    rr((x+18,by,x+cardW-18,cy0+cardH-18),12,sealbg,cor,3)
    t((x+cardW//2,by+24),"LIBERAÇÃO",F(16),MUTED,anchor="mm")
    t((x+cardW//2,by+56),libera,F(26 if not liberado else 24),cor,anchor="mm")

# ===== Faixa resumo circuitos =====
fy=H-140
rr((40,fy,W-40,H-30),16,CARD,BORDER,2)
t((70,fy+38),"CIRCUITO DE ALIMENTAÇÃO  (EL-F → CT-03)",F(24),GREEN,anchor="lm")
t((70,fy+78),"Liberado:  Sáb 20/06  07:00",F(26,False),INK,anchor="lm")
t((900,fy+38),"CIRCUITO DE DESCARGA  (EL-E → Duto → CT-04)",F(24),RED,anchor="lm")
t((900,fy+78),"Liberado:  Sex 19/06  01:00   (EL-E já operacional)",F(26,False),INK,anchor="lm")

out="/home/user/ICG2025/quadro_equipamentos_liberacao.jpg"
img.convert("RGB").save(out,"JPEG",quality=94)
print("saved",out,img.size)
