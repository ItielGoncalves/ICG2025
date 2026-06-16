#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math

FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def F(s,b=True): return ImageFont.truetype(FB if b else FR, s)

PAGE=(237,242,248); CARD=(255,255,255); BORDER=(203,213,225)
INK=(30,41,59); MUTED=(90,103,124); WHITE=(255,255,255)
GREEN=(22,163,74); RED=(220,38,38); BLUE=(37,99,235); AMBER=(217,119,6); TEAL=(13,148,136); GRAY=(107,114,128)
INPASA=(0,140,69)

W,H=2400,1660
img=Image.new("RGB",(W,H),PAGE); d=ImageDraw.Draw(img)
def t(xy,s,f,fill,anchor="lm",dd=d): dd.text(xy,s,font=f,fill=fill,anchor=anchor)
def rr(b,r,fill,outline=None,wd=2,dd=d): dd.rounded_rectangle(b,radius=r,fill=fill,outline=outline,width=wd)
def tint(c,p=0.85): return tuple(int(c[i]+(255-c[i])*p) for i in range(3))
def arrow(p1,p2,color,wd=12,head=24,dd=d):
    dd.line([p1,p2],fill=color,width=wd)
    ang=math.atan2(p2[1]-p1[1],p2[0]-p1[0])
    for a in (ang+math.radians(148),ang-math.radians(148)):
        dd.line([p2,(p2[0]+head*math.cos(a),p2[1]+head*math.sin(a))],fill=color,width=wd)

# ============ ILUSTRAÇÃO (recriação da foto) ============
def draw_scene(pw,ph):
    s=Image.new("RGB",(pw,ph),(210,228,245)); sd=ImageDraw.Draw(s)
    hy=int(ph*0.60)
    # céu gradiente
    for y in range(hy):
        f=y/hy; col=(int(196+ (236-196)*f),int(220+(244-220)*f),int(243+(250-243)*f))
        sd.line([(0,y),(pw,y)],fill=col)
    # chão
    sd.rectangle((0,hy,pw,ph),fill=(206,200,190))
    sd.rectangle((0,int(ph*0.86),pw,ph),fill=(150,118,86))
    # telhado grande do barracão (fundo)
    sd.polygon([(30,235),(pw*0.46,120),(pw-30,225),(pw-30,hy),(30,hy)],fill=(150,156,166))
    for i in range(6):
        xx=30+i*(pw-60)/6
        sd.line([(xx,hy),(xx*0.6+pw*0.46*0.4,150)],fill=(138,144,154),width=2)
    # barracão direito menor
    sd.polygon([(pw*0.62,300),(pw*0.80,250),(pw-30,300),(pw-30,hy),(pw*0.62,hy)],fill=(168,172,180))
    # torre EL-F (esquerda)
    sd.rectangle((255,150,322,hy),fill=(124,130,140))
    sd.rectangle((238,126,339,168),fill=(96,102,112))
    # torre EL-E (direita, mais alta) + casa de cabeça
    sd.rectangle((885,98,968,hy),fill=(124,130,140))
    sd.rectangle((866,70,987,124),fill=(96,102,112))
    # galeria CT-03 (entre torres + estende à esquerda)
    sd.polygon([(70,150),(300,162),(912,206),(912,238),(300,196),(70,182)],fill=(176,180,188))
    sd.line([(70,150),(912,206)],fill=(150,155,164),width=3)
    # duto EL-E -> CT-04
    sd.line([(950,250),(1185,332)],fill=(108,114,124),width=20)
    # galeria CT-04 (inferior direita)
    sd.polygon([(1185,318),(1410,300),(1410,330),(1185,348)],fill=(176,180,188))
    return s

def lbl(xy,s,txtcol,border,fnt,anchor="lm",dd=d):
    w=dd.textlength(s,font=fnt); h=fnt.size
    x,y=xy
    if anchor=="mm": x-=w/2
    pad=10
    rr((x-pad,y-h/2-pad,x+w+pad,y+h/2+pad),8,WHITE,border,3,dd=dd)
    dd.text((x,y),s,font=fnt,fill=txtcol,anchor="lm",dd=dd) if False else dd.text((x,y-h/2),s,font=fnt,fill=txtcol)

# logo Inpasa
lx2=W-50; lw=300; lh=92; lx1=lx2-lw; ly1=40; ly2=ly1+lh
rr((lx1,ly1,lx2,ly2),16,INPASA)
cx=lx1+44; cyl=(ly1+ly2)//2
d.polygon([(cx-14,cyl+16),(cx+18,cyl-18),(cx+20,cyl+8),(cx-2,cyl+18)],fill=(190,242,200))
t((lx1+78,cyl-10),"INPASA",F(34),WHITE,anchor="lm"); t((lx1+78,cyl+22),"Agroindustrial",F(15,False),(200,240,210),anchor="lm")

# header
t((50,52),"QUADRO POR EQUIPAMENTO — LIBERAÇÃO DOS CIRCUITOS",F(44),INK)
t((50,104),"Recuperação Sistema de Grãos — Sinop 2026 (R.0)   •   atividades pequenas suprimidas",F(23,False),MUTED)

# ---- painel ilustração ----
PX,PY,PW,PH=40,150,1480,620
scene=draw_scene(PW-8,PH-58)
img.paste(scene,(PX+4,PY+54))
rr((PX,PY,PX+PW,PY+PH),18,None,BORDER,3)
d.rectangle((PX+3,PY+3,PX+PW-3,PY+50),fill=CARD)
t((PX+24,PY+27),"REFERÊNCIA — recriação da foto enviada (esquema do sistema)",F(22),INK)
# rótulos sobre a cena (coords absolutas)
sx,sy=PX+4,PY+54
fL=F(26); fS=F(20)
def slbl(x,y,s,col,fnt=fL):
    w=d.textlength(s,font=fnt); pad=10
    rr((sx+x-pad,sy+y-fnt.size//2-pad,sx+x+w+pad,sy+y+fnt.size//2+pad),8,WHITE,col,3)
    t((sx+x,sy+y),s,fnt,col,anchor="lm")
slbl(95,250,"EL-F",GREEN)
slbl(60,470,"Fluxo alimentação",GREEN,fS)
slbl(470,300,"CT-03",GREEN)
slbl(1000,300,"EL-E",RED)
slbl(1085,360,"Duto",AMBER,fS)
slbl(1240,250,"CT-04",GREEN)
slbl(840,520,"Fluxo descarga",RED,fS)
# setas de fluxo
arrow((sx+288,sy+PH-130),(sx+288,sy+180),GREEN)
arrow((sx+288,sy+172),(sx+78,sy+158),GREEN)
arrow((sx+925,sy+PH-130),(sx+925,sy+120),RED)

# ---- painel direito: liberação resumida ----
RX=PX+PW+20; RW=W-40-RX
rr((RX,PY,RX+RW,PY+PH),18,CARD,BORDER,3)
t((RX+28,PY+44),"LIBERAÇÃO POR EQUIPAMENTO",F(26),INK)
rows=[("EL-E","✖ Danificado — fora da safra",GRAY),
      ("CT-04","Qua 17/06  19:00",TEAL),
      ("EL-F","Qui 18/06  11:00",GREEN),
      ("Duto","Sex 19/06  01:00",AMBER),
      ("CT-03","Sáb 20/06  07:00",BLUE)]
yy=PY+100
for nome,dt,col in rows:
    d.ellipse((RX+30,yy-14,RX+58,yy+14),fill=col)
    t((RX+74,yy),nome,F(28),INK,anchor="lm")
    t((RX+RW-28,yy),dt,F(26,False),col,anchor="rm")
    yy+=64
# hero milho
hy1=yy+18
rr((RX+24,hy1,RX+RW-24,PY+PH-26),14,tint(BLUE,0.9),BLUE,4)
t(((2*RX+RW)//2,hy1+44),"RECEBIMENTO DE MILHO",F(24),INK,anchor="mm")
t(((2*RX+RW)//2,hy1+86),"LIBERADO EM",F(18,False),MUTED,anchor="mm")
t(((2*RX+RW)//2,hy1+140),"Sáb 20/06 · 07:00",F(40),BLUE,anchor="mm")

# ============ Cards ============
cards=[
 ("CT-03","Correia principal (alim. + descarga)",BLUE,"Sáb 20/06  07:00","23 serviços · 90 h",False,
   ["Reforma estrutural – 16 módulos (60 h)","Revisão motorredutores A e B (48 h)",
    "Roletes de carga – 270 un (40 h)","Sensores / PT100 / desalinh. (40 h)",
    "Emenda de cabos elétricos (36 h)","★ Passagem + emenda a quente da correia"]),
 ("CT-04","Correia de descarga (via Duto)",TEAL,"Qua 17/06  19:00","8 serviços · 30 h",False,
   ["Corte + novo trecho de correia 15 m (18 h)","Emborrachamento tambor de retorno (10 h)",
    "Chegada de rolamentos / mancais (12 h)","★ Emenda de 15 m da correia (12 h)"]),
 ("EL-F","Elevador de alimentação",GREEN,"Qui 18/06  11:00","2 serviços · 40 h",False,
   ["Substituir 30 canecas (18 h)","★ Revestimento dutos – Rhynoride (36 h)"]),
 ("Duto","Transferência CT-03 → CT-04",AMBER,"Sex 19/06  01:00","1 serviço · 36 h",False,
   ["★ Duto da CT-03 para a CT-04 (36 h)"]),
 ("EL-E","Elevador de descarga",GRAY,"FORA DE ESCOPO","danificado",True,
   ["Danificado na ocorrência","NÃO é requerido para a safra (recebimento de milho)",
    "✖ Fora do escopo desta parada — recuperar depois"]),
]
cy0=PY+PH+30
cardW=(W-80-4*20)//5
cardH=H-cy0-180
for i,(nome,func,cor,libera,meta,flag,acts) in enumerate(cards):
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
        star=a.strip().startswith("★"); bad=a.strip().startswith("✖")
        col = cor if star else (GRAY if bad else INK); fnt=F(21, star or bad)
        words=a.split(); line=""; lines=[]
        for w in words:
            test=(line+" "+w).strip()
            if d.textlength(test,font=fnt)>cardW-44: lines.append(line); line=w
            else: line=test
        lines.append(line)
        for ln in lines: t((x+22,yy),ln,fnt,col,anchor="lm"); yy+=30
        yy+=8
    by=cy0+cardH-92
    rr((x+18,by,x+cardW-18,cy0+cardH-18),12,tint(cor,0.9),cor,3)
    t((x+cardW//2,by+24),"LIBERAÇÃO",F(16),MUTED,anchor="mm")
    t((x+cardW//2,by+56),libera,F(24),cor,anchor="mm")

# faixa resumo
fy=H-130
rr((40,fy,W-40,H-26),16,CARD,BORDER,2)
t((70,fy+38),"CIRCUITO DE ALIMENTAÇÃO  (EL-F → CT-03)",F(24),GREEN,anchor="lm")
t((70,fy+78),"Liberado:  Sáb 20/06  07:00",F(26,False),INK,anchor="lm")
t((900,fy+38),"CIRCUITO DE DESCARGA  (Duto → CT-04)",F(24),RED,anchor="lm")
t((900,fy+78),"Liberado:  Sex 19/06  01:00   (EL-E danificado, fora da safra)",F(26,False),INK,anchor="lm")

out="/home/user/ICG2025/quadro_equipamentos_liberacao.jpg"
img.convert("RGB").save(out,"JPEG",quality=94)
print("saved",out,img.size)
