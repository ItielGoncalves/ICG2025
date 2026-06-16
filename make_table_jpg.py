#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def F(sz,b=False): return ImageFont.truetype(FB if b else FR, sz)

BG=(15,23,42); PANEL=(30,41,59); LINE=(51,65,85)
TXT=(226,232,240); MUTED=(148,163,184); WHITE=(255,255,255)
CT03=(59,130,246); CT04=(16,185,129); ELEV=(245,158,11)

def D(mo,dy,h,mi=0): return datetime(2026,mo,dy,h,mi)
def fmt(d): return d.strftime("%a %d/%m  %H:%M").replace("Mon","Seg").replace("Tue","Ter").replace("Wed","Qua").replace("Thu","Qui").replace("Fri","Sex").replace("Sat","Sáb").replace("Sun","Dom")

# (id, serviço, início, término, duração, terceiro)
CT3=[
 (5,"Envio de correia 42 pol p/ refilar",D(6,16,13),D(6,16,17),4,"SUMEK Sorriso"),
 (6,"Refilamento de correia",D(6,16,17),D(6,17,5),12,"SUMEK Sorriso"),
 (7,"Retorno de correia refilada em 36 pol",D(6,17,5),D(6,17,9),4,""),
 (8,"Aquisição de rolamentos, mancais, buchas e vedações",D(6,16,13),D(6,17,1),12,""),
 (9,"Chegada dos rolamentos, mancais, buchas e vedações",D(6,17,1),D(6,17,13),12,""),
 (10,"Tambor tração - usinar tambor 65 mm",D(6,16,13),D(6,16,19),6,""),
 (11,"Montagem dos rolamentos e peças no tambor de tração",D(6,17,13),D(6,18,1),12,""),
 (12,"Rolo de contrapeso - coletar",D(6,16,13),D(6,16,19),6,"Vitale"),
 (13,"Montagem dos rolos de contrapeso após reforma estrutural",D(6,19,1),D(6,19,9),8,""),
 (14,"Instalar roletes retorno s/ mancal (módulos preservados)",D(6,16,13),D(6,17,1),12,""),
 (15,"Instalar roletes retorno s/ mancal (módulos substituídos)",D(6,18,19),D(6,19,1),6,""),
 (16,"Instalar rolete retorno com mancal",D(6,18,19),D(6,19,1),6,""),
 (17,"Chegada de roletes de carga",D(6,16,13),D(6,18,5),40,""),
 (18,"Instalação de rolete carga - 270 unidades",D(6,18,17),D(6,19,1),8,""),
 (19,"Revisão de motorredutor A",D(6,16,13),D(6,18,13),48,"RAETEC"),
 (20,"Revisão de motorredutor B",D(6,16,13),D(6,18,13),48,"RAETES"),
 (21,"Emenda dos cabos elétricos",D(6,16,13),D(6,18,1),36,""),
 (22,"Substituição de sensores, PT100, desalinhamento",D(6,16,13),D(6,18,5),40,""),
 (23,"Reforma estrutural (substituição de 16 módulos)",D(6,16,13),D(6,19,1),60,""),
 (24,"Emenda a quente da correia",D(6,19,19),D(6,20,7),12,""),
 (25,"Passagem da correia após montagem dos 270 roletes",D(6,19,1),D(6,19,19),18,""),
 (26,"Duto da CT 03 para CT 04",D(6,17,13),D(6,19,1),36,""),
 (27,"Coleta e entrega de módulos completos (estrutura + cavaletes)",D(6,16,13),D(6,16,19),6,""),
]
CT4=[
 (29,"Corte de correia e passagem de novo trecho 15 metros",D(6,16,13),D(6,17,7),18,""),
 (30,"Instalar roletes retorno s/ mancal (módulos preservados)",D(6,16,13),D(6,16,19),6,""),
 (31,"Instalar roletes retorno s/ mancal (módulos substituídos)",D(6,16,13),D(6,16,19),6,""),
 (32,"Instalar rolete retorno com mancal",D(6,16,13),D(6,16,15),2,""),
 (33,"Emenda de 15 metros da correia",D(6,17,7),D(6,17,19),12,""),
 (34,"Aquisição de rolamentos, mancais, buchas e vedações",D(6,16,13),D(6,17,1),12,""),
 (35,"Chegada dos rolamentos, mancais, buchas e vedações",D(6,17,1),D(6,17,13),12,""),
 (36,"Emborrachamento de tambor de retorno",D(6,17,7),D(6,17,17),10,""),
]
EL=[
 (38,"Substituir 30 canecas",D(6,16,19),D(6,17,13),18,""),
 (39,"Revestimento dos dutos dos elevadores (Rhynoride)",D(6,16,23),D(6,18,11),36,""),
]
SECTIONS=[("CT 03",CT03,CT3,D(6,16,13),D(6,20,7),90),
          ("CT 04",CT04,CT4,D(6,16,13),D(6,17,19),30),
          ("ELEVADOR F  (em inspeção)",ELEV,EL,D(6,16,19),D(6,18,11),40)]

# ---- column layout (landscape) ----
W=2200; LM=40; RM=40
# columns: ID | Serviço | Início | Término | Duração | Terceiro
cID=70; cSrv=820; cIni=300; cTer=300; cDur=130
x0=LM
xID=x0; xSrv=xID+cID; xIni=xSrv+cSrv; xTer=xIni+cIni; xDur=xTer+cTer; xExt=xDur+cDur
xEnd=W-RM

RH=46; HEADH=48; SECH=58
top=170
# compute height
rows=sum(len(s[2]) for s in SECTIONS)
H=top + len(SECTIONS)*(SECH+HEADH) + rows*RH + 90

img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
def text(xy,s,f,fill,anchor="lm"): d.text(xy,s,font=f,fill=fill,anchor=anchor)
def ell(s,f,maxw):
    if d.textlength(s,font=f)<=maxw: return s
    while s and d.textlength(s+"…",font=f)>maxw: s=s[:-1]
    return s+"…"

# title
text((LM,48),"🌾 RECUPERAÇÃO DO SISTEMA DE GRÃOS — SINOP 2026",F(36,True),TXT,anchor="lm")
text((LM,98),"Cronograma R.0  •  Serviços com hora de início e término  •  Parada de 90 h  (Ter 16/06 13:00 → Sáb 20/06 07:00)",F(20),MUTED,anchor="lm")

y=top
for sec_name,col,items,s0,e0,tot in SECTIONS:
    # section band
    d.rounded_rectangle((LM,y,xEnd,y+SECH-8),radius=10,fill=col)
    text((LM+18,y+(SECH-8)//2),sec_name,F(24,True),WHITE,anchor="lm")
    text((xEnd-18,y+(SECH-8)//2),f"{fmt(s0)}  →  {fmt(e0)}   |   {tot} h",F(19,True),WHITE,anchor="rm")
    y+=SECH
    # column header
    d.rectangle((LM,y,xEnd,y+HEADH),fill=PANEL)
    hf=F(17,True)
    text((xID+8,y+HEADH//2),"ID",hf,MUTED)
    text((xSrv+8,y+HEADH//2),"SERVIÇO",hf,MUTED)
    text((xIni+8,y+HEADH//2),"INÍCIO",hf,MUTED)
    text((xTer+8,y+HEADH//2),"TÉRMINO",hf,MUTED)
    text((xDur+8,y+HEADH//2),"DURAÇÃO",hf,MUTED)
    text((xExt+8,y+HEADH//2),"TERCEIRO",hf,MUTED)
    y+=HEADH
    for i,(tid,srv,s,e,dur,ext) in enumerate(items):
        rbg = BG if i%2==0 else (24,34,52)
        d.rectangle((LM,y,xEnd,y+RH),fill=rbg)
        cy=y+RH//2
        text((xID+8,cy),f"#{tid}",F(16),MUTED)
        text((xSrv+8,cy),ell(srv,F(18),cSrv-20),F(18),TXT)
        text((xIni+8,cy),fmt(s),F(17,True),(125,211,252))
        text((xTer+8,cy),fmt(e),F(17,True),(252,165,165))
        text((xDur+8,cy),f"{dur} h",F(17,True),TXT)
        if ext: text((xExt+8,cy),ext,F(16),(252,211,77))
        # column separators
        for xx in (xSrv,xIni,xTer,xDur,xExt):
            d.line([(xx,y),(xx,y+RH)],fill=(40,52,72),width=1)
        y+=RH
    y+=14

text((LM,H-46),"Obs.: o cronograma não possui coluna de responsável. Terceiros/locais citados nos serviços: SUMEK Sorriso · Vitale · RAETEC / RAETES.",F=F(16) if False else None) if False else text((LM,H-46),"Obs.: cronograma sem coluna de responsável. Terceiros citados nos serviços: SUMEK Sorriso · Vitale · RAETEC / RAETES.",F(16),MUTED,anchor="lm")

out="/home/user/ICG2025/servicos_inicio_fim_sinop_2026.jpg"
img.convert("RGB").save(out,"JPEG",quality=92)
print("saved",out,img.size)
