#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def F(sz,b=False): return ImageFont.truetype(FB if b else FR, sz)

# palette
BG=(15,23,42); PANEL=(30,41,59); PANEL2=(39,52,73); LINE=(51,65,85)
TXT=(226,232,240); MUTED=(148,163,184)
CT03=(59,130,246); CT04=(16,185,129); ELEV=(245,158,11); MARCO=(168,85,247)

PROJ=datetime(2026,6,16,13,0); TOTAL=90.0
def D(mo,dy,h,mi=0): return datetime(2026,mo,dy,h,mi)
def hrs(d): return (d-PROJ).total_seconds()/3600.0
def fmt(d): return d.strftime("%d/%m %H:%M")

T=[
 (2,"INÍCIO DAS DEMANDAS","marco",D(6,16,13),D(6,16,13),0,None,"milestone"),
 (4,"CT 03","ct03",D(6,16,13),D(6,20,7),90,None,"group"),
 (5,"Envio correia 42 pol p/ refilar","ct03",D(6,16,13),D(6,16,17),4,"SUMEK Sorriso",""),
 (6,"Refilamento de correia","ct03",D(6,16,17),D(6,17,5),12,"SUMEK Sorriso",""),
 (7,"Retorno de correia refilada 36 pol","ct03",D(6,17,5),D(6,17,9),4,None,""),
 (8,"Aquisição rolamentos/mancais/buchas","ct03",D(6,16,13),D(6,17,1),12,None,""),
 (9,"Chegada rolamentos/mancais/buchas","ct03",D(6,17,1),D(6,17,13),12,None,""),
 (10,"Tambor tração - usinar 65 mm","ct03",D(6,16,13),D(6,16,19),6,None,""),
 (11,"Montagem rolamentos no tambor tração","ct03",D(6,17,13),D(6,18,1),12,None,""),
 (12,"Rolo de contrapeso - coletar","ct03",D(6,16,13),D(6,16,19),6,"Vitale",""),
 (13,"Montagem rolos contrapeso pós-reforma","ct03",D(6,19,1),D(6,19,9),8,None,""),
 (14,"Roletes retorno s/ mancal (preservados)","ct03",D(6,16,13),D(6,17,1),12,None,""),
 (15,"Roletes retorno s/ mancal (substituídos)","ct03",D(6,18,19),D(6,19,1),6,None,""),
 (16,"Rolete retorno com mancal","ct03",D(6,18,19),D(6,19,1),6,None,""),
 (17,"Chegada de roletes de carga","ct03",D(6,16,13),D(6,18,5),40,None,""),
 (18,"Instalação rolete carga - 270 un","ct03",D(6,18,17),D(6,19,1),8,None,""),
 (19,"Revisão motorredutor A","ct03",D(6,16,13),D(6,18,13),48,"RAETEC",""),
 (20,"Revisão motorredutor B","ct03",D(6,16,13),D(6,18,13),48,"RAETES",""),
 (21,"Emenda dos cabos elétricos","ct03",D(6,16,13),D(6,18,1),36,None,""),
 (22,"Substituição sensores, PT100, desalinh.","ct03",D(6,16,13),D(6,18,5),40,None,""),
 (23,"Reforma estrutural (16 módulos)","ct03",D(6,16,13),D(6,19,1),60,None,""),
 (24,"Emenda a quente da correia","ct03",D(6,19,19),D(6,20,7),12,None,""),
 (25,"Passagem correia pós 270 roletes","ct03",D(6,19,1),D(6,19,19),18,None,""),
 (26,"Duto da CT 03 para CT 04","ct03",D(6,17,13),D(6,19,1),36,None,""),
 (27,"Coleta/entrega módulos completos","ct03",D(6,16,13),D(6,16,19),6,None,""),
 (28,"CT 04","ct04",D(6,16,13),D(6,17,19),30,None,"group"),
 (29,"Corte correia + novo trecho 15 m","ct04",D(6,16,13),D(6,17,7),18,None,""),
 (30,"Roletes retorno s/ mancal (preservados)","ct04",D(6,16,13),D(6,16,19),6,None,""),
 (31,"Roletes retorno s/ mancal (substituídos)","ct04",D(6,16,13),D(6,16,19),6,None,""),
 (32,"Rolete retorno com mancal","ct04",D(6,16,13),D(6,16,15),2,None,""),
 (33,"Emenda de 15 metros da correia","ct04",D(6,17,7),D(6,17,19),12,None,""),
 (34,"Aquisição rolamentos/mancais/buchas","ct04",D(6,16,13),D(6,17,1),12,None,""),
 (35,"Chegada rolamentos/mancais/buchas","ct04",D(6,17,1),D(6,17,13),12,None,""),
 (36,"Emborrachamento tambor de retorno","ct04",D(6,17,7),D(6,17,17),10,None,""),
 (37,"Elevador F (em inspeção)","elev",D(6,16,19),D(6,18,11),40,None,"group"),
 (38,"Substituir 30 canecas","elev",D(6,16,19),D(6,17,13),18,None,""),
 (39,"Revestimento dutos (Rhynoride)","elev",D(6,16,23),D(6,18,11),36,None,""),
 (3,"FINALIZAÇÃO DAS DEMANDAS","marco",D(6,20,7),D(6,20,7),0,None,"milestone"),
]
COL={"ct03":CT03,"ct04":CT04,"elev":ELEV,"marco":MARCO}

# ---- layout ----
W=2600
LM=40; LABEL=760            # left margin, label column width
GX0=LM+LABEL                # gantt start x
GW=W-GX0-40                 # gantt width
top=240                     # y where rows start
RH=29                       # row height
H=top+len(T)*RH+70

img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
def rr(box,r,fill,outline=None,wd=1): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=wd)
def text(xy,s,f,fill,anchor="la"): d.text(xy,s,font=f,fill=fill,anchor=anchor)

# header
text((LM,34),"🌾 RECUPERAÇÃO DO SISTEMA DE GRÃOS — SINOP 2026",F(40,True),TXT)
text((LM,86),"Cronograma R.0   •   Parada de 90 horas   •   Ter 16/06/26 13:00 → Sáb 20/06/26 07:00   •   3 frentes · 32 entregas",F(22),MUTED)

# KPIs
kpis=[("90 h","Duração total"),("3","Frentes"),("32","Entregas"),("~3,75 d","Dias corridos (24h)"),("60 h","Maior tarefa")]
kw=300; ky=130; kh=70
for i,(v,l) in enumerate(kpis):
    x=LM+i*(kw+16)
    rr((x,ky,x+kw,ky+kh),12,PANEL,LINE,1)
    text((x+18,ky+10),v,F(28,True),TXT)
    text((x+18,ky+46),l,F(15),MUTED)

# day grid header
days=["Ter 16/06","Qua 17/06","Qui 18/06","Sex 19/06","Sáb 20/06"]
def xfor(h): return GX0+ (h/TOTAL)*GW
# 5 day columns -> but project spans 90h starting 13:00; draw vertical lines every 24h from day starts
# Day boundaries at midnight: 16/06 00:00 is -13h. Lines at hours: -13(skip),11,35,59,83 -> midnights
for dline in [11,35,59,83]:
    x=xfor(dline); d.line([(x,top-6),(x,H-50)],fill=LINE,width=1)
# day labels centered between boundaries
bounds=[0,11,35,59,83,90]
for i,lab in enumerate(days):
    cx=(xfor(bounds[i])+xfor(bounds[i+1]))/2
    text((cx,200),lab,F(19,True),MUTED,anchor="ma")
# header separator
d.line([(LM,232),(W-40,232)],fill=LINE,width=2)
text((LM,200),"TAREFA",F(18,True),MUTED)

# rows
y=top
for (tid,name,g,s,e,dur,ext,kind) in T:
    col=COL[g]
    rowbg = PANEL2 if kind=="group" else (BG if (y//RH)%2==0 else (20,30,48))
    d.rectangle((LM,y,W-40,y+RH-2),fill=rowbg)
    # label
    idtxt=f"#{tid}"
    text((LM+10,y+5),idtxt,F(15,True),MUTED)
    nm = name if len(name)<=46 else name[:44]+"…"
    text((LM+60,y+5),nm,F(16,True if kind=="group" else False),TXT)
    if kind=="milestone":
        cx=xfor(hrs(s)); cy=y+RH//2; r=9
        d.polygon([(cx,cy-r),(cx+r,cy),(cx,cy+r),(cx-r,cy)],fill=MARCO)
    else:
        x1=xfor(hrs(s)); x2=xfor(hrs(e));
        if x2-x1<4: x2=x1+4
        by=y+5; bh=RH-12
        if kind=="group":
            rr((x1,y+3,x2,y+RH-5),7,col)
            text(((x1+x2)/2,y+RH//2-1),f"{name}  ({dur}h)",F(15,True),(255,255,255),anchor="mm")
        else:
            rr((x1,by,x2,by+bh),6,col)
            lbl=f"{dur}h"
            if ext: lbl=f"{dur}h · {ext}"
            if x2-x1>70:
                text((x1+8,y+RH//2-1),lbl,F(13),(255,255,255),anchor="lm")
            else:
                text((x2+6,y+RH//2-1),lbl,F(13),MUTED,anchor="lm")
    y+=RH

# legend
ly=H-38
items=[("CT 03 (frente principal)",CT03),("CT 04",CT04),("Elevador F",ELEV),("Marco início/fim",MARCO)]
lx=LM
for lab,c in items:
    d.rectangle((lx,ly,lx+22,ly+22),fill=c); text((lx+30,ly+2),lab,F(17),TXT)
    lx+=d.textlength(lab,font=F(17))+90
text((W-40,ly+2),"Obs.: cronograma sem coluna de responsável — terceiros citados: SUMEK · Vitale · RAETEC/RAETES",F(15),MUTED,anchor="ra")

out="/home/user/ICG2025/dashboard_sinop_2026.jpg"
img.convert("RGB").save(out,"JPEG",quality=92)
print("saved",out,img.size)
