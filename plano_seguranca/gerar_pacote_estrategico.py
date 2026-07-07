# -*- coding: utf-8 -*-
"""
Pacote estrategico no PADRAO DE MARCA INPASA (tema claro, Azul #124E81 dominante,
Ouro #EAA239, Montserrat). Dados do dashboard v6 (46 correias). Codigos oficiais NMT/SDR.
Saidas: PPTX, PDF e 3 PNGs para o grupo.
NOTA: logotipo oficial ainda nao disponivel como arquivo -> area reservada.
"""
import os, copy
from datetime import date
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/user/ICG2025/plano_seguranca"
FONTS = os.path.join(OUT, "fonts")
SRCPPTX = os.path.join(OUT, "fontes", "mapeamento_correias_v04.pptx")  # deck de origem (mapa 148->46)
def F(w='Regular', s=40):
    return ImageFont.truetype(os.path.join(FONTS, f"Montserrat-{w}.ttf"), s)

# ---- reportlab: registrar Montserrat ----
pdfmetrics.registerFont(TTFont('Mont', os.path.join(FONTS, 'Montserrat-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Mont-Med', os.path.join(FONTS, 'Montserrat-Medium.ttf')))
pdfmetrics.registerFont(TTFont('Mont-Sb', os.path.join(FONTS, 'Montserrat-SemiBold.ttf')))
pdfmetrics.registerFont(TTFont('Mont-Bd', os.path.join(FONTS, 'Montserrat-Bold.ttf')))
pdfmetrics.registerFont(TTFont('Mont-Xb', os.path.join(FONTS, 'Montserrat-ExtraBold.ttf')))

# ============ CORES DA MARCA ============
AZUL='#124E81'; OURO='#EAA239'; OUROV='#FFA32A'; CINZA='#BDBFC1'
VERDE='#609346'; TERRA='#CC5121'; VERDEESC='#007D77'; AZULCL='#007CC5'
BRANCO='#FFFFFF'; TXTD='#20303F'; MUT='#6B7885'; CARDBG='#F2F5F8'
UNITHEX={'NMT':AZUL,'SNP':OURO,'SDR':VERDEESC,'BLS':AZULCL}

# ============ DADOS (dashboard v6) — remapeado p/ codigos oficiais ============
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
CODMAP={'NVM':'NMT','SDL':'SDR','SNP':'SNP','BLS':'BLS'}  # codigo dashboard -> oficial
TODAY=date(2026,7,2)
def p(d):
    if d=='SUBSTITUÍDA': return None
    dd,mm,yy=d.split('/'); return date(int(yy),int(mm),int(dd))
from collections import defaultdict
U=defaultdict(list)
for u,t,d in raw: U[CODMAP[u]].append((t,p(d)))
ORDEM=['NMT','SNP','SDR','BLS']
NOMES={'NMT':'Nova Mutum','SNP':'Sinop','SDR':'Sidrolândia','BLS':'Balsas'}
def stat(u):
    rows=U[u]; concl=sum(1 for _,dt in rows if dt is None)
    estoque=sum(1 for t,dt in rows if t=='ESTOQUE')
    esteiras=[dt for t,dt in rows if dt and t!='ESTOQUE']
    urg=sum(1 for _,dt in rows if dt and 0<=(dt-TODAY).days<=30)
    return dict(total=len(rows),concl=concl,estoque=estoque,urg=urg,last=max(esteiras),pend=len(rows)-concl)
ST={u:stat(u) for u in ORDEM}
TOTAL=sum(s['total'] for s in ST.values()); CONCL=sum(s['concl'] for s in ST.values())
URG=sum(s['urg'] for s in ST.values()); GLAST=max(s['last'] for s in ST.values())
def fd(d): return d.strftime('%d/%m/%Y')
FRASE={
 'NMT':"16 correias no plano; 1 concluída. Última substituição em 22/10/2026.",
 'SNP':"23 correias no plano; 1 concluída. Última em 30/12/2026 (esteiras de cavacos).",
 'SDR':"2 correias no plano. Ambas concluídas até 30/09/2026.",
 'BLS':"4 esteiras + 1 sobressalente; 1 concluída. Esteiras concluídas até 24/07/2026.",
}

def rgb(h): return RGBColor(int(h[1:3],16),int(h[3:5],16),int(h[5:7],16))

# =====================================================================
# PPTX  (tema claro / marca INPASA)
# =====================================================================
def build_pptx():
    cAZUL=rgb(AZUL);cOURO=rgb(OURO);cOUROV=rgb(OUROV);cCINZA=rgb(CINZA);cVERDE=rgb(VERDE)
    cTERRA=rgb(TERRA);cVERDEESC=rgb(VERDEESC);cAZULCL=rgb(AZULCL);cBR=rgb(BRANCO)
    cTXT=rgb(TXTD);cMUT=rgb(MUT);cCARD=rgb(CARDBG); COR={u:rgb(UNITHEX[u]) for u in ORDEM}
    prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
    SW,SH=prs.slide_width,prs.slide_height; BLANK=prs.slide_layouts[6]
    def sl(bg=cBR):
        s=prs.slides.add_slide(BLANK)
        b=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,SW,SH); b.fill.solid()
        b.fill.fore_color.rgb=bg; b.line.fill.background(); b.shadow.inherit=False; return s
    def rect(s,x,y,w,h,c,line=None,lw=1.0,rnd=False):
        sp=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rnd else MSO_SHAPE.RECTANGLE,x,y,w,h)
        sp.fill.solid(); sp.fill.fore_color.rgb=c
        if line is None: sp.line.fill.background()
        else: sp.line.color.rgb=line; sp.line.width=Pt(lw)
        sp.shadow.inherit=False; return sp
    def txt(s,x,y,w,h,t,size=18,bold=False,color=cTXT,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,sp=None,italic=False,font='Montserrat'):
        tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
        tf.margin_left=Pt(2); tf.margin_right=Pt(2)
        for i,ln in enumerate(t.split('\n')):
            pa=tf.paragraphs[0] if i==0 else tf.add_paragraph(); pa.alignment=align
            if sp: pa.line_spacing=sp
            r=pa.add_run(); r.text=ln; r.font.size=Pt(size); r.font.bold=bold; r.font.italic=italic
            r.font.color.rgb=color; r.font.name=font
        return tb
    def head(s,k,t):
        rect(s,0,0,SW,Inches(1.15),cAZUL); rect(s,0,Inches(1.15),SW,Inches(0.05),cOUROV)
        txt(s,Inches(0.55),Inches(0.16),Inches(12),Inches(0.3),k,size=12,bold=True,color=cOURO)
        txt(s,Inches(0.55),Inches(0.44),Inches(12.2),Inches(0.62),t,size=25,bold=True,color=cBR,anchor=MSO_ANCHOR.MIDDLE)
    def foot(s,n):
        txt(s,Inches(0.55),Inches(7.02),Inches(10),Inches(0.35),
            "INPASA Agroindustrial S/A  ·  Manutenção & Automação  ·  ref. 02/07/2026",size=9,color=cMUT)
        txt(s,Inches(12.2),Inches(7.02),Inches(0.9),Inches(0.35),str(n),size=9,color=cMUT,align=PP_ALIGN.RIGHT)

    # 1 CAPA (fundo azul solido)
    s=sl(cAZUL)
    rect(s,0,0,SW,Inches(0.35),cOUROV)  # barra decorativa superior
    # area reservada p/ logo (canto sup. esquerdo)
    txt(s,Inches(0.9),Inches(1.35),Inches(11.5),Inches(0.5),"APRESENTAÇÃO À DIRETORIA",size=15,bold=True,color=cOURO)
    txt(s,Inches(0.9),Inches(2.1),Inches(11.6),Inches(1.8),"Plano de Substituição de\nCorreias Transportadoras",size=44,bold=True,color=cBR,sp=1.05)
    txt(s,Inches(0.9),Inches(4.55),Inches(11.6),Inches(0.9),
        "Status do programa e cronograma de regularização por unidade\nNova Mutum · Sinop · Sidrolândia · Balsas",size=16,color=rgb('#C7D6E6'),sp=1.2)
    rect(s,Inches(0.9),Inches(5.75),Inches(3.0),Pt(2),cOUROV)
    txt(s,Inches(0.9),Inches(5.95),Inches(11),Inches(0.5),"MAIS QUE ENERGIA",size=18,bold=True,italic=True,color=cOURO)
    txt(s,Inches(0.9),Inches(6.7),Inches(11.6),Inches(0.4),
        "Base: levantamento FLEXLAB (jun/2026) + plano de execução  |  ref. 02/07/2026",size=11,color=rgb('#9FB4C9'))

    # 2 MAPEAMENTO (copia nativa da pagina 2 do deck de origem) + contorno vermelho nas 46
    src=Presentation(SRCPPTX); ss=src.slides[1]
    ms=prs.slides.add_slide(BLANK)
    for sh in ss.shapes:
        ms.shapes._spTree.append(copy.deepcopy(sh._element))
    o=ms.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(8.74),Inches(1.30),Inches(4.44),Inches(5.68))
    o.fill.background(); o.line.color.rgb=rgb('#E00000'); o.line.width=Pt(3.5); o.shadow.inherit=False
    # etiqueta "FOCO" como badge vermelho no canto superior do contorno
    bd=ms.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(11.43),Inches(1.05),Inches(1.75),Inches(0.28))
    bd.fill.solid(); bd.fill.fore_color.rgb=rgb('#E00000'); bd.line.fill.background(); bd.shadow.inherit=False
    bp=bd.text_frame.paragraphs[0]; bp.alignment=PP_ALIGN.CENTER
    br=bp.add_run(); br.text="◄ FOCO AGORA"; br.font.size=Pt(10)
    br.font.bold=True; br.font.color.rgb=rgb('#FFFFFF'); br.font.name='Montserrat'

    # 3 REGULARIZACAO POR UNIDADE
    s=sl(); head(s,"A PERGUNTA DA DIRETORIA","Quando cada unidade estará regularizada?")
    rect(s,Inches(0.55),Inches(1.45),Inches(12.25),Inches(0.8),cCARD,line=cAZUL,lw=1.25,rnd=True)
    txt(s,Inches(0.8),Inches(1.45),Inches(11.8),Inches(0.8),
        f"Programa concluído em {fd(GLAST)}    |    {TOTAL} correias · {CONCL} concluídas · {URG} urgentes (<=30 dias) · 0 vencidas",
        size=15,bold=True,color=cAZUL,anchor=MSO_ANCHOR.MIDDLE)
    cx=Inches(0.55);cw=Inches(2.95);gap=Inches(0.13);cy=Inches(2.5);ch=Inches(3.2)
    for i,u in enumerate(ORDEM):
        st=ST[u]; x=Emu(int(cx)+i*(int(cw)+int(gap)))
        rect(s,x,cy,cw,ch,cCARD,rnd=True); rect(s,x,cy,cw,Inches(0.13),COR[u])
        txt(s,Emu(int(x)+Inches(0.2)),Emu(int(cy)+Inches(0.3)),Emu(int(cw)-Inches(0.4)),Inches(0.4),u,size=13,bold=True,color=COR[u])
        txt(s,Emu(int(x)+Inches(0.2)),Emu(int(cy)+Inches(0.64)),Emu(int(cw)-Inches(0.4)),Inches(0.5),NOMES[u],size=15,bold=True,color=cTXT)
        txt(s,Emu(int(x)+Inches(0.2)),Emu(int(cy)+Inches(1.18)),Emu(int(cw)-Inches(0.4)),Inches(0.35),"CONCLUÍDA EM",size=10,bold=True,color=cMUT)
        txt(s,Emu(int(x)+Inches(0.2)),Emu(int(cy)+Inches(1.45)),Emu(int(cw)-Inches(0.4)),Inches(0.55),fd(st['last']),size=22,bold=True,color=COR[u])
        txt(s,Emu(int(x)+Inches(0.2)),Emu(int(cy)+Inches(2.1)),Emu(int(cw)-Inches(0.4)),Inches(1.0),FRASE[u],size=10.5,color=cTXT,sp=1.05)
    foot(s,3)

    # 3 CRONOGRAMA (jul-dez)
    s=sl(); head(s,"LINHA DO TEMPO","Marcos de conclusão (jul → dez/2026)")
    tl_x=Inches(2.6);tl_w=Inches(9.9);start=date(2026,7,1);end=date(2026,12,31);span=(end-start).days;top=Inches(1.75)
    for name,m in [('Jul',7),('Ago',8),('Set',9),('Out',10),('Nov',11),('Dez',12)]:
        md=date(2026,m,1);px=int(tl_x)+int(((md-start).days/span)*int(tl_w))
        rect(s,Emu(px),Emu(int(top)),Pt(1),Inches(4.4),cCINZA)
        txt(s,Emu(px),Emu(int(top)-Inches(0.02)),Inches(1.4),Inches(0.3),name,size=12,bold=True,color=cAZUL)
    hx=int(tl_x)+int(((TODAY-start).days/span)*int(tl_w))
    rect(s,Emu(hx),Emu(int(top)+Inches(0.3)),Pt(2),Inches(4.05),cTERRA)
    txt(s,Emu(hx-Inches(0.3)),Emu(int(top)+Inches(0.02)),Inches(1.2),Inches(0.28),"HOJE",size=10,bold=True,color=cTERRA)
    rowh=Inches(0.95);ry=Emu(int(top)+Inches(0.55))
    for u in ORDEM:
        st=ST[u]
        txt(s,Inches(0.55),ry,Inches(1.95),rowh,f"{u} · {NOMES[u]}\n{st['total']} correias",size=11,bold=True,color=COR[u],anchor=MSO_ANCHOR.MIDDLE)
        x0=int(tl_x);x1=int(tl_x)+int(((st['last']-start).days/span)*int(tl_w))
        rect(s,Emu(x0),Emu(int(ry)+Inches(0.22)),Emu(max(x1-x0,int(Inches(0.2)))),Inches(0.42),COR[u],rnd=True)
        txt(s,Emu(x1+Inches(0.1)),Emu(int(ry)+Inches(0.2)),Inches(1.8),Inches(0.45),fd(st['last']),size=11,bold=True,color=cTXT,anchor=MSO_ANCHOR.MIDDLE)
        ry=Emu(int(ry)+int(rowh))
    txt(s,Inches(0.55),Inches(6.5),Inches(12),Inches(0.4),
        f"Conclusão de todo o programa: {fd(GLAST)} (última — Sinop, esteiras de cavacos da biomassa).",size=13,bold=True,color=cAZUL)
    foot(s,4)

    # 4 RECONCILIACAO
    s=sl(); head(s,"CONSISTÊNCIA DOS NÚMEROS","Reconciliação: levantamento × execução")
    rect(s,Inches(0.55),Inches(1.55),Inches(6.0),Inches(4.75),cCARD,rnd=True)
    txt(s,Inches(0.8),Inches(1.75),Inches(5.5),Inches(0.4),"Levantamento FLEXLAB (jun/2026)",size=15,bold=True,color=cAZUL)
    for i,(t,c) in enumerate([("148 correias auditadas no grupo",cTXT),("102 mantidas em operação",cMUT),
        ("46 a substituir  →  R$ 6,15 mi (só correias)",cTXT),("   • 41 reprovadas no ensaio ISO 340",cMUT),("   • 5 por degradação física",cMUT)]):
        txt(s,Inches(0.85),Emu(int(Inches(2.35))+i*int(Inches(0.68))),Inches(5.5),Inches(0.66),("•  " if i in(0,2) else "")+t,size=13,color=c,bold=(i==2))
    rect(s,Inches(6.8),Inches(1.55),Inches(6.0),Inches(4.75),cCARD,rnd=True)
    txt(s,Inches(7.05),Inches(1.75),Inches(5.5),Inches(0.4),"Plano de execução (dashboard atual)",size=15,bold=True,color=cVERDE)
    for i,(t,c) in enumerate([(f"{TOTAL} correias no plano  ✓ bate com as 46",cTXT),(f"   • {CONCL} já concluídas",cMUT),
        (f"   • {TOTAL-CONCL} em execução",cMUT),(f"Conclusão: {fd(GLAST)}",cTXT),("0 correias vencidas",cMUT)]):
        txt(s,Inches(7.1),Emu(int(Inches(2.35))+i*int(Inches(0.68))),Inches(5.5),Inches(0.66),("•  " if i in(0,3) else "")+t,size=13,color=c,bold=(i in(0,3)))
    txt(s,Inches(0.55),Inches(6.35),Inches(12.3),Inches(0.6),
        "Obs.: R$ 6,15 mi = somente as correias (material) — montagem com mão de obra interna, apenas vulcanização externa · "
        "Dourados (DRD) e LEM sem itens críticos (reprovados ISO 340) nesta 1ª etapa · cadastro do dashboard usa NVM/SDL → padronizar p/ NMT/SDR · "
        "1 dos 46 é sobressalente em estoque (45 esteiras físicas).",
        size=10.5,color=cTERRA)
    foot(s,5)

    # 5 ACAO / PCM
    s=sl(); head(s,"DECISÃO E AÇÃO","Cuidado especial até concluir a substituição")
    rect(s,Inches(0.55),Inches(1.55),Inches(6.0),Inches(4.75),cCARD,rnd=True)
    txt(s,Inches(0.8),Inches(1.75),Inches(5.5),Inches(0.4),"Pontos de atenção",size=16,bold=True,color=cTERRA)
    for i,r in enumerate([f"{URG} correias urgentes (<=30 dias) — biomassa (SNP), DDGS (SDR/BLS), julho.",
        "Conclusão do programa depende da SNP (esteiras de cavacos, 30/12/2026).",
        "Biomassa e grãos: maior exposição a incêndio por atrito (rolete/correia).",
        "Janela de transição: risco elevado até a troca de todas as correias."]):
        txt(s,Inches(0.85),Emu(int(Inches(2.35))+i*int(Inches(0.95))),Inches(5.4),Inches(0.95),"•  "+r,size=13,color=cTXT,sp=1.05)
    rect(s,Inches(6.8),Inches(1.55),Inches(6.0),Inches(4.75),cCARD,rnd=True)
    txt(s,Inches(7.05),Inches(1.75),Inches(5.5),Inches(0.4),"Encaminhamentos",size=16,bold=True,color=cVERDE)
    for i,pz in enumerate(["Segurança e PCM acionados para alinhar com TODAS as áreas cuidado reforçado até concluir a substituição das correias.",
        "Priorizar as correias urgentes de julho (biomassa/DDGS).",
        "Reporte quinzenal de avanço por unidade (concluídas x plano).",
        "Padronizar cadastro na origem (NVM/SDL → NMT/SDR)."]):
        txt(s,Inches(7.1),Emu(int(Inches(2.35))+i*int(Inches(0.95))),Inches(5.4),Inches(0.95),"•  "+pz,size=13,color=cTXT,sp=1.05)
    foot(s,6)

    path=os.path.join(OUT,"Apresentacao_Estrategica_Correias_INPASA.pptx"); prs.save(path)
    print("PPTX:",path,"slides:",len(prs.slides._sldIdLst))

# =====================================================================
# PDF (tema claro / marca)
# =====================================================================
def build_pdf():
    W,H=960,540
    def PT(i): return i*72.0
    path=os.path.join(OUT,"Apresentacao_Estrategica_Correias_INPASA.pdf")
    c=canvas.Canvas(path,pagesize=(W,H))
    def box(x,yt,w,h,fill,rad=0,stroke=None,sw=1):
        c.setFillColor(HexColor(fill)); do=0
        if stroke: c.setStrokeColor(HexColor(stroke)); c.setLineWidth(sw); do=1
        yb=H-PT(yt)-PT(h)
        (c.roundRect if rad else c.rect)(PT(x),yb,PT(w),PT(h),*((rad,) if rad else ()),fill=1,stroke=do)
    def line(x,yt,w,h,fill): box(x,yt,w,h,fill)
    def text(x,yt,s,size,fill,bold=False,align='l',italic=False):
        fn='Mont-Bd' if bold else 'Mont'; c.setFont(fn,size); c.setFillColor(HexColor(fill)); yb=H-PT(yt)-size
        (c.drawCentredString if align=='c' else c.drawRightString if align=='r' else c.drawString)(PT(x),yb,s)
    def para(x,yt,wi,s,size,fill,bold=False,lead=None):
        fn='Mont-Bd' if bold else 'Mont'; c.setFont(fn,size); c.setFillColor(HexColor(fill))
        y=H-PT(yt)-size; lead=lead or size*1.3
        for ln in simpleSplit(s,fn,size,PT(wi)): c.drawString(PT(x),y,ln); y-=lead
    def bg(col=BRANCO): c.setFillColor(HexColor(col)); c.rect(0,0,W,H,fill=1,stroke=0)
    def head(k,t):
        box(0,0,13.333,1.15,AZUL); line(0,1.15,13.333,0.05,OUROV)
        text(0.55,0.18,k,11,OURO,bold=True); text(0.55,0.5,t,22,BRANCO,bold=True)
    def foot(n):
        text(0.55,7.05,"INPASA Agroindustrial S/A  ·  Manutenção & Automação  ·  ref. 02/07/2026",8,MUT)
        text(12.75,7.05,str(n),8,MUT,align='r')
    COR=UNITHEX
    # 1 CAPA
    bg(AZUL); box(0,0,13.333,0.35,OUROV)
    text(0.9,1.35,"APRESENTAÇÃO À DIRETORIA",14,OURO,bold=True)
    text(0.9,2.1,"Plano de Substituição de",37,BRANCO,bold=True); text(0.9,2.9,"Correias Transportadoras",37,BRANCO,bold=True)
    text(0.9,4.5,"Status do programa e cronograma de regularização por unidade",15,'#C7D6E6')
    text(0.9,4.85,"Nova Mutum · Sinop · Sidrolândia · Balsas",15,'#C7D6E6')
    line(0.9,5.7,3.0,0.03,OUROV); text(0.9,5.9,"MAIS QUE ENERGIA",17,OURO,bold=True)
    text(0.9,6.7,"Base: levantamento FLEXLAB (jun/2026) + plano de execução   |   ref. 02/07/2026",11,'#9FB4C9'); c.showPage()
    # 2 MAPEAMENTO (reproducao da pagina 2 do levantamento) + contorno vermelho nas 46
    bg()
    box(0,0,13.333,0.64,'#124E81'); box(0,0,0.06,0.64,'#EAA239')
    text(0.2,0.16,"Resultado do Levantamento — 148 Correias · NMT · SNP · SDR · DRD · BLS · LEM",14,BRANCO,bold=True)
    text(13.1,0.2,"Grupo INPASA · Jun/2026",10,'#C7D6E6',align='r')
    box(0.2,0.76,12.9,0.5,'#EAF5DC',stroke='#609346',sw=1)
    text(0.35,0.9,"FLEXLAB 0397/26 · 08/06/2026 · NMT CT-010 (correia do sinistro): ANTICHAMA CONFIRMADA — ISO 340 · inclusa nas 88 antichama 2ª linha",10.5,'#2E5E2A',bold=True)
    box(0.2,1.38,8.58,0.30,'#609346'); text(4.49,1.44,"MANTER EM OPERAÇÃO — 102 correias",12,BRANCO,bold=True,align='c')
    box(8.84,1.38,4.26,0.30,'#D97706'); text(10.97,1.44,"SUBSTITUIR — 46 · R$ 6,15M",12,BRANCO,bold=True,align='c')
    cards=[
      (0.20,"19","12,8%","1ª Linha","Identificação visual na correia",["ID visual impressa na correia","Conforme exigência normativa","Rastreabilidade completa"],"CONFORME NORMA","#2E7D32"),
      (2.36,"56","37,8%","2ª Linha","Ev. física + teste aprovado",["Evidência física em campo","Aprovadas — ISO 340 campo","Pendente laudo laboratorial"],"PENDENTE LAUDO","#4E8B3A"),
      (4.52,"10","6,8%","2ª Linha","Com laudo, sem ID visual",["Laudo ou doc. de conformidade","Sem marcação visual na correia","NMT CT-010 — Flexlab 0397/26"],"REGULARIZAR ID","#609346"),
      (6.68,"17","11,5%","2ª Linha","Só teste, sem laudo e sem ID",["Aprovadas no teste ISO 340","Sem laudo e sem ID visual","Maior exposição — priorizar doc."],"OBTER LAUDO","#74A83A"),
      (8.84,"41","27,7%","Reprovadas","Falha no ensaio ISO 340",["SNP: 21 itens · R$ 3,55 mi","NMT: 15 itens · R$ 1,70 mi","SDR/BLS/LEM: 5 itens · R$ 0,90 mi"],"SUBSTITUIÇÃO IMEDIATA","#CC5121"),
      (11.00,"5","3,4%","Degradação","Antichama 2ª linha",["Aprovadas no ensaio ISO 340","Degradação física prematura","Substituição sendo programada"],"PROG. SUBSTITUIÇÃO","#D97706"),
    ]
    for (x,num,pct,cat,sub,bul,btn,col) in cards:
        w=2.10; top=1.78; h=5.12
        box(x,top,w,h,'#FFFFFF',stroke='#E2E7EC',sw=1)
        box(x,top,w,0.56,col)
        text(x+0.12,top+0.1,num,26,BRANCO,bold=True); text(x+w-0.1,top+0.2,pct,11,BRANCO,align='r')
        text(x+0.12,top+0.72,cat,12,'#1F2937',bold=True); text(x+0.12,top+1.0,sub,9,'#6B7280')
        box(x+0.12,top+1.28,w-0.24,0.012,'#E2E7EC')
        yy=top+1.45
        for b in bul:
            c.setFillColor(HexColor(col)); c.circle(PT(x+0.18),H-PT(yy+0.08),2.0,fill=1,stroke=0)
            para(x+0.3,yy,w-0.4,b,8.3,'#374151',lead=10); yy+=0.52
        box(x+0.12,top+4.62,w-0.24,0.36,col); text(x+w/2,top+4.71,btn,8.0,BRANCO,bold=True,align='c')
    c.setStrokeColor(HexColor('#E00000')); c.setLineWidth(3.2)
    c.roundRect(PT(8.74),H-PT(1.30)-PT(5.68),PT(4.44),PT(5.68),10,fill=0,stroke=1)
    box(11.43,1.05,1.75,0.28,'#E00000'); text(12.305,1.12,"◄ FOCO AGORA",10,BRANCO,bold=True,align='c')
    foot(2); c.showPage()
    # 3 UNIDADES
    bg(); head("A PERGUNTA DA DIRETORIA","Quando cada unidade estará regularizada?")
    box(0.55,1.45,12.25,0.8,CARDBG,rad=8,stroke=AZUL,sw=1.3)
    text(6.9,1.72,f"Programa concluído em {fd(GLAST)}   |   {TOTAL} correias · {CONCL} concluídas · {URG} urgentes · 0 vencidas",12.5,AZUL,bold=True,align='c')
    cw=2.95;gap=0.13;cx=0.55;cy=2.5;ch=3.2
    for i,u in enumerate(ORDEM):
        st=ST[u]; x=cx+i*(cw+gap); box(x,cy,cw,ch,CARDBG,rad=8); line(x,cy,cw,0.13,COR[u])
        text(x+0.2,cy+0.32,u,13,COR[u],bold=True); text(x+0.2,cy+0.66,NOMES[u],14,TXTD,bold=True)
        text(x+0.2,cy+1.2,"CONCLUÍDA EM",9,MUT,bold=True); text(x+0.2,cy+1.48,fd(st['last']),21,COR[u],bold=True)
        para(x+0.2,cy+2.1,cw-0.4,FRASE[u],9.5,TXTD,lead=12)
    foot(3); c.showPage()
    # 3 CRONOGRAMA
    bg(); head("LINHA DO TEMPO","Marcos de conclusão (jul -> dez/2026)")
    tl_x=2.6;tl_w=9.9;start=date(2026,7,1);end=date(2026,12,31);span=(end-start).days;top=1.75
    for name,m in [('Jul',7),('Ago',8),('Set',9),('Out',10),('Nov',11),('Dez',12)]:
        md=date(2026,m,1);fx=tl_x+((md-start).days/span)*tl_w; box(fx,top,0.014,4.4,CINZA); text(fx,top-0.02,name,12,AZUL,bold=True)
    hx=tl_x+((TODAY-start).days/span)*tl_w; box(hx,top+0.3,0.028,4.05,TERRA); text(hx-0.28,top+0.02,"HOJE",9.5,TERRA,bold=True)
    rowh=0.95;ry=top+0.55
    for u in ORDEM:
        st=ST[u]; text(0.55,ry+0.24,f"{u} · {NOMES[u]}",11,COR[u],bold=True); text(0.55,ry+0.5,f"{st['total']} correias",9,MUT)
        x1=tl_x+((st['last']-start).days/span)*tl_w; box(tl_x,ry+0.22,max(x1-tl_x,0.2),0.42,COR[u],rad=4)
        text(x1+0.1,ry+0.32,fd(st['last']),11,TXTD,bold=True); ry+=rowh
    text(0.55,6.5,f"Conclusão de todo o programa: {fd(GLAST)} (última — Sinop, esteiras de cavacos).",13,AZUL,bold=True); foot(4); c.showPage()
    # 4 RECONCILIACAO
    bg(); head("CONSISTÊNCIA DOS NÚMEROS","Reconciliação: levantamento × execução")
    box(0.55,1.55,6.0,4.75,CARDBG,rad=8); text(0.8,1.78,"Levantamento FLEXLAB (jun/2026)",15,AZUL,bold=True)
    L=[("•  148 correias auditadas no grupo",TXTD),("102 mantidas em operação",MUT),("•  46 a substituir  ->  R$ 6,15 mi (só correias)",TXTD),
       ("   - 41 reprovadas ISO 340",MUT),("   - 5 degradação física",MUT)]
    for i,(t,cc) in enumerate(L): text(0.85,2.35+i*0.62,t,13,cc,bold=(i==2))
    box(6.8,1.55,6.0,4.75,CARDBG,rad=8); text(7.05,1.78,"Plano de execução (dashboard atual)",15,VERDE,bold=True)
    R=[(f"•  {TOTAL} correias no plano  (bate com as 46)",TXTD),(f"   - {CONCL} já concluídas",MUT),
       (f"   - {TOTAL-CONCL} em execução",MUT),(f"•  Conclusão: {fd(GLAST)}",TXTD),("   - 0 correias vencidas",MUT)]
    for i,(t,cc) in enumerate(R): text(7.1,2.35+i*0.62,t,13,cc,bold=(i in(0,3)))
    para(0.55,6.28,12.3,"Obs.: R$ 6,15 mi = somente as correias (material) — montagem com mão de obra interna, apenas vulcanização externa · Dourados (DRD) e LEM sem itens críticos (reprovados ISO 340) nesta 1ª etapa · cadastro do dashboard usa NVM/SDL -> padronizar p/ NMT/SDR · 1 dos 46 é sobressalente em estoque (45 esteiras).",10,TERRA); foot(5); c.showPage()
    # 5 ACAO
    bg(); head("DECISÃO E AÇÃO","Cuidado especial até concluir a substituição")
    box(0.55,1.55,6.0,4.75,CARDBG,rad=8); text(0.8,1.78,"Pontos de atenção",15,TERRA,bold=True)
    A=[f"{URG} correias urgentes (<=30 dias) — biomassa (SNP), DDGS (SDR/BLS), julho.",
       "Conclusão do programa depende da SNP (esteiras de cavacos, 30/12/2026).",
       "Biomassa e grãos: maior exposição a incêndio por atrito.",
       "Janela de transição: risco elevado até a troca de todas as correias."]
    ty=2.35
    for r in A: para(0.85,ty,5.4,"•  "+r,12,TXTD,lead=15); ty+=0.88
    box(6.8,1.55,6.0,4.75,CARDBG,rad=8); text(7.05,1.78,"Encaminhamentos",15,VERDE,bold=True)
    B=["Segurança e PCM acionados para alinhar com TODAS as áreas cuidado reforçado até concluir a substituição.",
       "Priorizar as correias urgentes de julho (biomassa/DDGS).",
       "Reporte quinzenal de avanço por unidade.",
       "Padronizar cadastro na origem (NVM/SDL -> NMT/SDR)."]
    ty=2.35
    for r in B: para(7.1,ty,5.4,"•  "+r,12,TXTD,lead=15); ty+=0.88
    foot(6); c.save(); print("PDF:",path)

# =====================================================================
# IMAGENS (tema claro / marca)
# =====================================================================
def hx(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
iAZUL=hx(AZUL);iOURO=hx(OURO);iOUROV=hx(OUROV);iCINZA=hx(CINZA);iVERDE=hx(VERDE)
iTERRA=hx(TERRA);iVERDEESC=hx(VERDEESC);iAZULCL=hx(AZULCL);iBR=hx(BRANCO)
iTXT=hx(TXTD);iMUT=hx(MUT);iCARD=hx(CARDBG); iUNIT={u:hx(UNITHEX[u]) for u in ORDEM}
Wp=1080
def new_img(h): im=Image.new('RGB',(Wp,h),iBR); return im,ImageDraw.Draw(im)
def brand(d,h):
    d.rectangle([0,0,Wp,96],fill=iAZUL); d.rectangle([0,96,Wp,102],fill=iOUROV)
    d.text((48,26),"INPASA",font=F('ExtraBold',40),fill=iBR)
    d.text((250,40),"·  Substituição de Correias",font=F('Medium',26),fill=hx('#C7D6E6'))
    d.text((48,h-46),"MAIS QUE ENERGIA · Manutenção & Automação · ref. 02/07/2026",font=F('Medium',20),fill=iMUT)

def img_escopo():
    h=1080; im,d=new_img(h); brand(d,h)
    d.text((48,150),"Programa de substituição — visão geral",font=F('ExtraBold',44),fill=iAZUL)
    kpis=[("46","correias no plano",iAZUL),("3","já concluídas",iVERDE),("43","em execução",iAZUL),
          ("0","vencidas",iVERDE),("R$ 6,15 mi","somente correias",iAZUL),("7","urgentes (≤30d)",iOURO)]
    x0,y0,cw,chh,gx,gy=48,260,320,190,24,28
    for i,(v,lb,cc) in enumerate(kpis):
        r,cidx=divmod(i,3); x=x0+cidx*(cw+gx); y=y0+r*(chh+gy)
        d.rounded_rectangle([x,y,x+cw,y+chh],radius=18,fill=iCARD)
        d.rectangle([x,y,x+8,y+chh],fill=iAZUL)
        vs=60 if len(v)<=3 else (44 if len(v)<=6 else 38)
        d.text((x+30,y+66),v,font=F('ExtraBold',vs),fill=cc,anchor='lm')
        d.text((x+30,y+140),lb,font=F('Medium',24),fill=iMUT,anchor='lm')
    yb=y0+2*(chh+gy)+20
    d.rounded_rectangle([48,yb,Wp-48,yb+140],radius=18,fill=iAZUL)
    d.text((Wp//2,yb+44),"CONCLUSÃO DE TODO O PROGRAMA",font=F('SemiBold',26),fill=hx('#C7D6E6'),anchor='mm')
    d.text((Wp//2,yb+100),fd(GLAST),font=F('ExtraBold',54),fill=iBR,anchor='mm')
    ny=yb+175
    d.text((Wp//2,ny),"R$ 6,15 mi = apenas as correias (material).",font=F('Medium',21),fill=iMUT,anchor='mm')
    d.text((Wp//2,ny+32),"Montagem: mão de obra interna · Vulcanização: externa.",font=F('Medium',21),fill=iMUT,anchor='mm')
    d.text((Wp//2,ny+70),"Escopo (1ª etapa): NMT · SNP · SDR · BLS  —  Dourados e LEM sem itens críticos (ISO 340).",font=F('SemiBold',19),fill=iAZUL,anchor='mm')
    path=os.path.join(OUT,"img_grupo_1_escopo.png"); im.save(path); print("IMG:",path)

def img_unidades():
    h=1080; im,d=new_img(h); brand(d,h)
    d.text((48,150),"Quando cada unidade fica pronta",font=F('ExtraBold',44),fill=iAZUL)
    y=260; rh=150
    for u in sorted(ORDEM,key=lambda z:ST[z]['last']):
        st=ST[u]; d.rounded_rectangle([48,y,Wp-48,y+rh-20],radius=18,fill=iCARD)
        d.rectangle([48,y,58,y+rh-20],fill=iUNIT[u])
        d.text((90,y+28),f"{u} · {NOMES[u]}",font=F('ExtraBold',38),fill=iUNIT[u])
        extra=f"{st['total']} correias · {st['concl']} concluída(s)"+(" · +1 sobressalente" if st['estoque'] else "")
        d.text((90,y+84),extra,font=F('Medium',24),fill=iMUT)
        d.text((Wp-80,y+38),fd(st['last']),font=F('ExtraBold',46),fill=iTXT,anchor='rm')
        d.text((Wp-80,y+90),"concluída em",font=F('Medium',22),fill=iMUT,anchor='rm')
        y+=rh
    d.rounded_rectangle([48,y,Wp-48,y+120],radius=18,fill=iAZUL)
    d.text((Wp//2,y+60),f"Todas as unidades concluídas até {fd(GLAST)}",font=F('ExtraBold',36),fill=iBR,anchor='mm')
    path=os.path.join(OUT,"img_grupo_2_unidades.png"); im.save(path); print("IMG:",path)

def img_timeline():
    h=920; im,d=new_img(h); brand(d,h)
    d.text((48,140),"Linha do tempo — conclusão por unidade",font=F('ExtraBold',40),fill=iAZUL)
    lx,rx=300,Wp-60; top=250; start=date(2026,7,1); end=date(2026,12,31); span=(end-start).days
    for name,m in [('Jul',7),('Ago',8),('Set',9),('Out',10),('Nov',11),('Dez',12)]:
        md=date(2026,m,1); px=lx+int(((md-start).days/span)*(rx-lx))
        d.line([(px,top),(px,top+430)],fill=iCINZA,width=2); d.text((px,top-30),name,font=F('Bold',22),fill=iAZUL,anchor='mm')
    hxp=lx+int(((TODAY-start).days/span)*(rx-lx)); d.line([(hxp,top),(hxp,top+430)],fill=iTERRA,width=3)
    d.text((hxp-4,top-64),"HOJE",font=F('Bold',20),fill=iTERRA,anchor='mm')
    y=top+30; rh=95
    for u in sorted(ORDEM,key=lambda z:ST[z]['last']):
        st=ST[u]; d.text((60,y+28),f"{u}",font=F('ExtraBold',30),fill=iUNIT[u])
        d.text((60,y+64),f"{st['total']} corr.",font=F('Medium',20),fill=iMUT)
        x1=lx+int(((st['last']-start).days/span)*(rx-lx))
        d.rounded_rectangle([lx,y+20,max(x1,lx+6),y+62],radius=8,fill=iUNIT[u])
        d.text((min(x1+14,rx-150),y+22),fd(st['last']),font=F('Bold',24),fill=iTXT)
        y+=rh
    d.text((Wp//2,h-64),f"Programa concluído em {fd(GLAST)}",font=F('ExtraBold',32),fill=iAZUL,anchor='mm')
    path=os.path.join(OUT,"img_grupo_3_timeline.png"); im.save(path); print("IMG:",path)

build_pptx(); build_pdf(); img_escopo(); img_unidades(); img_timeline()
print("OK — pacote INPASA gerado.")
