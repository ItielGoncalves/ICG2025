#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def F(s,b=True): return ImageFont.truetype(FB if b else FR, s)

BG=(15,23,42); PANEL=(30,41,59); PANEL2=(39,52,73); LINE=(51,65,85)
TXT=(226,232,240); MUTED=(148,163,184); WHITE=(255,255,255)
GREEN=(34,197,94); RED=(239,68,68); BLUE=(59,130,246); AMBER=(245,158,11); TEAL=(20,184,166)
STEEL=(120,134,156); STEELD=(74,85,104)

W,H=2200,1480
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
def t(xy,s,f,fill,anchor="lm"): d.text(xy,s,font=f,fill=fill,anchor=anchor)
def rr(b,r,fill,outline=None,wd=2): d.rounded_rectangle(b,radius=r,fill=fill,outline=outline,width=wd)

def arrow(p1,p2,color,wd=10,head=22):
    import math
    d.line([p1,p2],fill=color,width=wd)
    ang=math.atan2(p2[1]-p1[1],p2[0]-p1[0])
    for a in (ang+math.radians(150),ang-math.radians(150)):
        d.line([p2,(p2[0]+head*math.cos(a),p2[1]+head*math.sin(a))],fill=color,width=wd)

# ===== Header =====
t((40,46),"🌾 QUADRO POR EQUIPAMENTO — LIBERAÇÃO DOS CIRCUITOS",F(38),TXT)
t((40,94),"Recuperação Sistema de Grãos — Sinop 2026 (R.0)  •  esquema baseado na foto enviada  •  atividades pequenas suprimidas",F(20,False),MUTED)

# ===== Esquema (referência da foto) =====
DX,DY,DW,DH=40,140,2120,470
rr((DX,DY,DX+DW,DY+DH),16,(22,32,50),LINE,2)
t((DX+24,DY+28),"ESQUEMA DO SISTEMA (ref. foto)",F(18),MUTED)

# coordenadas no esquema
ground=DY+DH-40
# EL-F tower (esquerda)
elf_x=DX+260
d.line([(elf_x,ground),(elf_x,DY+150)],fill=STEEL,width=26)
d.rectangle((elf_x-22,DY+120,elf_x+22,DY+165),fill=STEELD)
# EL-E tower (direita, mais alta)
ele_x=DX+1120
d.line([(ele_x,ground),(ele_x,DY+95)],fill=STEEL,width=30)
d.rectangle((ele_x-26,DY+70,ele_x+26,DY+125),fill=STEELD)
# CT-03 viga (entre torres, estendendo à esquerda)
ct03_l=(DX+70,DY+150); ct03_r=(ele_x,DY+210)
d.line([ct03_l,ct03_r],fill=STEEL,width=22)
# Duto desce da CT-03/EL-E até CT-04
duto_top=(ele_x+10,DY+250); ct04_l=(DX+1330,DY+330)
d.line([duto_top,ct04_l],fill=STEELD,width=16)
# CT-04 (inferior direita)
ct04_r=(DX+1820,DY+310)
d.line([ct04_l,ct04_r],fill=STEEL,width=20)

# fluxos
arrow((elf_x,ground-10),(elf_x,DY+175),GREEN)                 # alimentação sobe EL-F
arrow((elf_x,DY+162),(DX+90,DY+158),GREEN)                    # ... e segue CT-03 p/ esquerda
arrow((ele_x,ground-10),(ele_x,DY+120),RED)                   # descarga sobe EL-E
# legenda fluxos
d.rectangle((DX+24,ground+4,DX+50,ground+24),fill=GREEN); t((DX+58,ground+14),"Fluxo alimentação",F(17),TXT)
d.rectangle((DX+360,ground+4,DX+386,ground+24),fill=RED);  t((DX+394,ground+14),"Fluxo descarga",F(17),TXT)

# badge de liberação no esquema
def badge(cx,cy,nome,data,cor):
    bw,bh=300,86
    rr((cx-bw//2,cy-bh//2,cx+bw//2,cy+bh//2),12,PANEL,cor,3)
    t((cx,cy-20),nome,F(22),cor,anchor="mm")
    t((cx,cy+16),"libera "+data,F(19,False),TXT,anchor="mm")

badge(elf_x,DY+95,"EL-F","Qui 18/06 11:00",GREEN)
badge(DX+560,DY+95,"CT-03","Sáb 20/06 07:00",BLUE)
badge(ele_x,DY+45 if False else DY+260,"EL-E","sem escopo*",RED) if False else badge(ele_x+150,DY+150,"EL-E","s/ escopo*",RED)
badge(DX+1480,DY+210,"Duto","Sex 19/06 01:00",AMBER)
badge(DX+1700,DY+400,"CT-04","Qua 17/06 19:00",TEAL)

# ===== Cards detalhados por equipamento =====
# (nome, função, cor, libera, nº serviços/horas, [atividades principais (suprimidas as pequenas)])
cards=[
 ("CT-03","Correia principal (alimentação + descarga)",BLUE,"Sáb 20/06  07:00","23 serviços · 90 h",
   ["Reforma estrutural – 16 módulos (60 h)",
    "Revisão motorredutores A e B (48 h)",
    "Roletes de carga – 270 un (40 h)",
    "Sensores / PT100 / desalinh. (40 h)",
    "Emenda cabos elétricos (36 h)",
    "★ Passagem + emenda a quente da correia"]),
 ("CT-04","Correia de descarga (recebe via Duto)",TEAL,"Qua 17/06  19:00","8 serviços · 30 h",
   ["Corte + novo trecho de correia 15 m (18 h)",
    "Emborrachamento tambor de retorno (10 h)",
    "Chegada de rolamentos/mancais (12 h)",
    "★ Emenda de 15 m da correia (12 h)"]),
 ("EL-F","Elevador de alimentação",GREEN,"Qui 18/06  11:00","2 serviços · 40 h",
   ["Substituir 30 canecas (18 h)",
    "★ Revestimento dutos – Rhynoride (36 h)"]),
 ("Duto","Transferência CT-03 → CT-04",AMBER,"Sex 19/06  01:00","1 serviço · 36 h",
   ["★ Duto da CT-03 para a CT-04 (36 h)"]),
 ("EL-E","Elevador de descarga",RED,"a definir *","sem atividades",
   ["* Não consta no cronograma R.0",
    "  — confirmar se entra no escopo",
    "  da parada ou já está liberado"]),
]
cy=DY+DH+30
cardW=(W-40-40-4*16)//5
cardH=H-cy-150
for i,(nome,func,cor,libera,meta,acts) in enumerate(cards):
    x=40+i*(cardW+16)
    rr((x,cy,x+cardW,cy+cardH),14,PANEL,LINE,2)
    d.rounded_rectangle((x,cy,x+cardW,cy+58),radius=14,fill=cor)
    d.rectangle((x,cy+30,x+cardW,cy+58),fill=cor)
    t((x+18,cy+29),nome,F(28),WHITE,anchor="lm")
    t((x+18,cy+82),func,F(15,False),TXT,anchor="lm")
    t((x+18,cy+108),meta,F(14,False),MUTED,anchor="lm")
    d.line([(x+14,cy+128),(x+cardW-14,cy+128)],fill=LINE,width=1)
    yy=cy+150
    t((x+18,yy),"PRINCIPAIS SERVIÇOS",F(13),MUTED,anchor="lm"); yy+=28
    for a in acts:
        col = cor if a.strip().startswith("★") else TXT
        # wrap simples
        words=a.split(); line=""; lines=[]
        for w in words:
            test=(line+" "+w).strip()
            if d.textlength(test,font=F(15,False))>cardW-36: lines.append(line); line=w
            else: line=test
        lines.append(line)
        for ln in lines:
            t((x+18,yy),ln,F(15,False),col,anchor="lm"); yy+=22
        yy+=6
    # selo de liberação
    by=cy+cardH-70
    rr((x+14,by,x+cardW-14,cy+cardH-14),10,(13,20,36),cor,2)
    t((x+cardW//2,by+18),"LIBERAÇÃO",F(13),MUTED,anchor="mm")
    t((x+cardW//2,by+42),libera,F(20),cor,anchor="mm")

# ===== Faixa resumo de circuitos =====
fy=H-115
rr((40,fy,W-40,H-30),14,PANEL2,LINE,2)
t((64,fy+30),"CIRCUITO DE ALIMENTAÇÃO  (EL-F → CT-03)",F(19),GREEN,anchor="lm")
t((64,fy+62),"Liberado:  Sáb 20/06  07:00",F(20,False),TXT,anchor="lm")
t((760,fy+30),"CIRCUITO DE DESCARGA  (EL-E → Duto → CT-04)",F(19),RED,anchor="lm")
t((760,fy+62),"Liberado:  Sex 19/06  01:00   (EL-E a confirmar*)",F(20,False),TXT,anchor="lm")
rr((1560,fy+14,W-54,H-44),10,(13,20,36),BLUE,3)
t((1790,fy+34),"SISTEMA COMPLETO",F(16),MUTED,anchor="mm")
t((1790,fy+64),"Sáb 20/06  07:00",F(24),BLUE,anchor="mm")

out="/home/user/ICG2025/quadro_equipamentos_liberacao.jpg"
img.convert("RGB").save(out,"JPEG",quality=93)
print("saved",out,img.size)
