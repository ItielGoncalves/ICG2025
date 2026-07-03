# -*- coding: utf-8 -*-
"""
Versao PDF da apresentacao estrategica (mesmo conteudo do PPTX).
Gerada direto com reportlab (LibreOffice indisponivel no ambiente).
Saida: plano_seguranca/Apresentacao_Estrategica_Correias_INPASA.pdf
"""
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit

# ---------- DADOS (identicos ao PPTX) ----------
raw = [
 ('NVM','MILHO','TRL-519004-4','09/05/2026'),('NVM','MILHO','TRL-519004-1','20/08/2026'),
 ('NVM','MILHO','TRL-519004-2','25/08/2026'),('NVM','MILHO','TRL-519004-3','30/08/2026'),
 ('NVM','MILHO','TRL-519004-5','10/09/2026'),('NVM','MILHO','TRL-519424','05/08/2026'),
 ('NVM','MILHO','TRL-519426','30/09/2026'),('NVM','MILHO','TRL-519425','30/09/2026'),
 ('NVM','MILHO','TRL-719102','30/09/2026'),('NVM','MILHO','TRL-719104','20/09/2026'),
 ('NVM','MILHO','TRL-719103','05/10/2026'),('NVM','MILHO','TRL-719101','30/09/2026'),
 ('NVM','DDGS','TRL-509041','10/10/2026'),('NVM','MILHO','TRL-519004-7','01/08/2026'),
 ('NVM','MILHO','TRL-519004-6','30/09/2026'),
 ('SNP','BIOMASSA','TRL-401002A','01/08/2026'),('SNP','BIOMASSA','TRL-401002B','01/08/2026'),
 ('SNP','BIOMASSA','TRL-631501','17/07/2026'),('SNP','BIOMASSA','TRL-631504','17/07/2026'),
 ('SNP','BIOMASSA','TRL-631512','17/07/2026'),('SNP','DDGS','TRL-409302','30/09/2026'),
 ('SNP','GRAOS','TRL-419419SA-1','30/09/2026'),('SNP','GRAOS','TRL-419419SA-2','30/09/2026'),
 ('SNP','GRAOS','TRL-419419SB-2','30/09/2026'),('SNP','GRAOS','TRL-419SB3','30/09/2026'),
 ('SNP','GRAOS','TRL-419419SB-5','30/09/2026'),('SNP','GRAOS','TRL-419419SB-6','30/09/2026'),
 ('SNP','GRAOS','TRL-619038','30/09/2026'),('SNP','GRAOS','TRL-619023','30/09/2026'),
 ('SNP','GRAOS','TRL-619041','30/09/2026'),('SNP','GRAOS','TRL-1011235','30/09/2026'),
 ('SDL','DDGS','TRL-1209011','17/07/2026'),('SDL','GRAOS','TRL-1219523','30/09/2026'),
 ('BLS','GRAOS','TRL-1519203A','SUBSTITUÍDA'),('BLS','DDGS','TRL-1509208','17/07/2026'),
 ('BLS','DDGS','TRL-1509209','17/07/2026'),('BLS','DDGS','TRL-1509403','17/07/2026'),
 ('BLS','ALMOX','ESTOQUE','30/09/2026'),
 ('SNP','BIOMASSA','TRL-1031004','30/09/2026'),('SNP','BIOMASSA','TRL-1031008','SUBSTITUÍDA'),
 ('SNP','BIOMASSA','TRL-1031009','30/09/2026'),('SNP','BIOMASSA','TRL-1031011','30/09/2026'),
 ('SNP','BIOMASSA','TRL-1031012','30/09/2026'),
]
TODAY = date(2026, 7, 2)
def parse(d):
    if d == 'SUBSTITUÍDA': return None
    dd, mm, yy = d.split('/'); return date(int(yy), int(mm), int(dd))
U = {}
for u, a, t, d in raw:
    U.setdefault(u, []).append((t, a, parse(d), d))
def stats(u):
    rows = U[u]
    subst = sum(1 for _, _, dt, _ in rows if dt is None)
    venc = sum(1 for _, _, dt, _ in rows if dt and dt < TODAY)
    urg = sum(1 for _, _, dt, _ in rows if dt and 0 <= (dt - TODAY).days <= 30)
    pend = [dt for _, _, dt, _ in rows if dt]
    return dict(total=len(rows), subst=subst, venc=venc, urg=urg,
                pend=len(rows) - subst, first=min(pend), last=max(pend))
NOMES = {'NVM':'Nova Mutum (NVM)','SNP':'Sinop (SNP)','SDL':'Sidrolândia (SDL)','BLS':'Balsas (BLS)'}
COR = {'NVM':'#3B82F6','SNP':'#F97316','SDL':'#22C55E','BLS':'#A855F7'}
ORDEM = ['NVM','SNP','SDL','BLS']
ST = {u: stats(u) for u in ORDEM}
GLAST = max(s['last'] for s in ST.values())
TOTAL = sum(s['total'] for s in ST.values()); SUBST = sum(s['subst'] for s in ST.values())
URG = sum(s['urg'] for s in ST.values()); VENC = sum(s['venc'] for s in ST.values())
def fd(d): return d.strftime('%d/%m/%Y')

# ---------- ESTILO ----------
BG='#0F0F1A'; CARD='#1E1E30'; CARD2='#252538'; LAR='#F97316'; BR='#FFFFFF'
TXT='#E0E0E0'; MUT='#9CA3AF'; VERDE='#22C55E'; VERM='#EF4444'; AMAR='#EAB308'
GRID='#2A2A40'
W, H = 960, 540
def P(inch): return inch * 72.0

out = "/home/user/ICG2025/plano_seguranca/Apresentacao_Estrategica_Correias_INPASA.pdf"
c = canvas.Canvas(out, pagesize=(W, H))

def box(x, y_top, w, h, fill, radius=0, stroke=None, sw=1):
    c.setFillColor(HexColor(fill))
    if stroke:
        c.setStrokeColor(HexColor(stroke)); c.setLineWidth(sw); do_s = 1
    else:
        do_s = 0
    yb = H - P(y_top) - P(h)
    if radius:
        c.roundRect(P(x), yb, P(w), P(h), radius, fill=1, stroke=do_s)
    else:
        c.rect(P(x), yb, P(w), P(h), fill=1, stroke=do_s)

def line(x, y_top, w, h, fill):
    box(x, y_top, w, h, fill)

def text(x, y_top, s, size, fill, bold=False, align='l', font='Helvetica'):
    f = font + ('-Bold' if bold else '')
    c.setFont(f, size); c.setFillColor(HexColor(fill))
    yb = H - P(y_top) - size
    if align == 'c':
        c.drawCentredString(P(x), yb, s)
    elif align == 'r':
        c.drawRightString(P(x), yb, s)
    else:
        c.drawString(P(x), yb, s)

def para(x, y_top, w_in, s, size, fill, bold=False, leading=None, font='Helvetica'):
    f = font + ('-Bold' if bold else '')
    c.setFont(f, size); c.setFillColor(HexColor(fill))
    lines = simpleSplit(s, f, size, P(w_in))
    lead = leading or size * 1.25
    y = H - P(y_top) - size
    for ln in lines:
        c.drawString(P(x), y, ln); y -= lead
    return len(lines)

def bg():
    c.setFillColor(HexColor(BG)); c.rect(0, 0, W, H, fill=1, stroke=0)

def header(kicker, title):
    box(0, 0, 13.333, 1.2, CARD)
    line(0, 1.2, 13.333, 0.045, LAR)
    text(0.55, 0.18, kicker, 11, LAR, bold=True)
    text(0.55, 0.52, title, 22, BR, bold=True)

def footer(n):
    text(0.55, 7.08, "INPASA  •  Plano de Substituição de Correias Transportadoras  •  2026", 8, '#6B7280')
    text(12.75, 7.08, str(n), 8, '#6B7280', align='r')

# ===== 1 CAPA =====
bg()
line(0, 4.55, 13.333, 0.05, LAR)
text(0.9, 1.5, "INPASA  •  APRESENTAÇÃO À DIRETORIA", 14, LAR, bold=True)
text(0.9, 2.35, "Plano de Substituição de", 37, BR, bold=True)
text(0.9, 3.15, "Correias Transportadoras", 37, BR, bold=True)
text(0.9, 4.8, "Status do programa e cronograma de regularização por unidade", 15, MUT)
text(0.9, 5.15, "Nova Mutum  •  Sinop  •  Sidrolândia  •  Balsas", 15, MUT)
text(0.9, 6.6, "Gestão de Manutenção Industrial   |   Data de referência: 02/07/2026", 11, '#6B7280')
c.showPage()

# ===== 2 REGULARIZACAO POR UNIDADE =====
bg()
header("A PERGUNTA DA DIRETORIA", "Quando cada unidade estará regularizada?")
box(0.55, 1.45, 12.25, 0.85, CARD2, radius=8, stroke=LAR, sw=1.3)
hl = (f"Programa 100% regularizado até {fd(GLAST)}    |    {TOTAL} correias  •  "
      f"{SUBST} já substituídas  •  {URG} urgentes (<=30 dias)" + (f"  •  {VENC} vencida" if VENC else ""))
text(6.9, 1.78, hl, 13, BR, bold=True, align='c')
cw = 2.95; gap = 0.13; cx = 0.55; cy = 2.55; ch = 3.15
frases = {
 'NVM':"São {t} esteiras no plano. A última será concluída em {last} — data de regularização da unidade.",
 'SNP':"São {t} esteiras no plano; {sub} já substituída. A última será concluída em {last}.",
 'SDL':"São {t} esteiras no plano. Ambas concluídas até {last}.",
 'BLS':"4 esteiras + 1 sobressalente em estoque; {sub} já substituída. Última em {last}.",
}
for i, u in enumerate(ORDEM):
    st = ST[u]; x = cx + i * (cw + gap)
    box(x, cy, cw, ch, CARD, radius=8)
    line(x, cy, cw, 0.12, COR[u])
    text(x + 0.2, cy + 0.3, u, 13, COR[u], bold=True)
    text(x + 0.2, cy + 0.62, NOMES[u].split('(')[0].strip(), 14, BR, bold=True)
    text(x + 0.2, cy + 1.18, "REGULARIZADA EM", 9, MUT, bold=True)
    text(x + 0.2, cy + 1.45, fd(st['last']), 21, COR[u], bold=True)
    para(x + 0.2, cy + 2.05, cw - 0.4, frases[u].format(t=st['total'], sub=st['subst'], last=fd(st['last'])),
         9.5, TXT, leading=12)
    if st['venc']:
        text(x + 0.2, cy + 2.82, f"! {st['venc']} vencida (atrasada)", 9.5, VERM, bold=True)
footer(2)
c.showPage()

# ===== 3 CRONOGRAMA =====
bg()
header("LINHA DO TEMPO", "Marcos de regularização (jul -> out/2026)")
tl_x = 2.6; tl_w = 9.9
start = date(2026,7,1); end = date(2026,10,31); span = (end - start).days
top = 1.75
for name, m in [('Julho',7),('Agosto',8),('Setembro',9),('Outubro',10)]:
    md = date(2026, m, 1); fx = tl_x + ((md - start).days / span) * tl_w
    box(fx, top, 0.014, 4.4, GRID)
    text(fx, top - 0.02, name, 12, LAR, bold=True)
hx = tl_x + ((TODAY - start).days / span) * tl_w
box(hx, top + 0.3, 0.028, 4.05, VERM)
text(hx - 0.32, top + 0.02, "HOJE", 9.5, VERM, bold=True)
rowh = 0.95; ry = top + 0.55
for u in ORDEM:
    st = ST[u]
    text(0.55, ry + 0.28, u, 12, COR[u], bold=True)
    text(0.55, ry + 0.55, f"{st['total']} correias", 10, MUT)
    x1 = tl_x + ((st['last'] - start).days / span) * tl_w
    box(tl_x, ry + 0.22, max(x1 - tl_x, 0.2), 0.42, COR[u], radius=4)
    text(x1 + 0.1, ry + 0.32, fd(st['last']), 11, BR, bold=True)
    ry += rowh
text(0.55, 6.55, f"Conclusão do programa: {fd(GLAST)} (última correia — Nova Mutum / DDGS).", 13, LAR, bold=True)
footer(3)
c.showPage()

# ===== 4 RESUMO POR UNIDADE (tabela) =====
bg()
header("VISÃO CONSOLIDADA", "Resumo executivo por unidade")
cols = ["Unidade","Correias","Substituídas","Em execução","Próxima","Regularização","Alerta"]
colw = [0.20,0.12,0.13,0.12,0.14,0.14,0.15]
tx = 0.55; tw = 12.25; hy = 1.6; rh = 0.55
xx = tx
for j, cl in enumerate(cols):
    w = tw * colw[j]
    box(xx, hy, w, 0.6, CARD2)
    text(xx + w/2, hy + 0.22, cl, 10, LAR, bold=True, align='c')
    xx += w
ry = hy + 0.6
for idx, u in enumerate(ORDEM):
    st = ST[u]
    alerta = (f"{st['venc']} vencida" if st['venc'] else (f"{st['urg']} urgentes" if st['urg'] else "-"))
    acor = VERM if st['venc'] else (AMAR if st['urg'] else MUT)
    vals = [NOMES[u], str(st['total']), str(st['subst']), str(st['pend']), fd(st['first']), fd(st['last']), alerta]
    xx = tx
    for j, v in enumerate(vals):
        w = tw * colw[j]
        box(xx, ry, w, rh, CARD if idx % 2 == 0 else BG)
        col = COR[u] if j == 0 else (acor if j == 6 else TXT)
        b = j in (0,5,6)
        if j == 0:
            text(xx + 0.12, ry + 0.2, v, 10, col, bold=b)
        else:
            text(xx + w/2, ry + 0.2, v, 10, col, bold=b, align='c')
        xx += w
    ry += rh
xx = tx
tot = [f"TOTAL ({len(ORDEM)} un.)", str(TOTAL), str(SUBST), str(TOTAL-SUBST), "-", fd(GLAST), f"{VENC} venc / {URG} urg"]
for j, v in enumerate(tot):
    w = tw * colw[j]
    box(xx, ry, w, rh, LAR)
    if j == 0:
        text(xx + 0.12, ry + 0.2, v, 10, BG, bold=True)
    else:
        text(xx + w/2, ry + 0.2, v, 10, BG, bold=True, align='c')
    xx += w
footer(4)
c.showPage()

# ===== 5 ATENCAO E PROXIMOS PASSOS =====
bg()
header("DECISÃO", "Pontos de atenção e próximos passos")
box(0.55, 1.55, 6.0, 4.9, CARD, radius=8)
text(0.8, 1.78, "! Riscos / prioridades", 15, VERM, bold=True)
riscos = [
 "NVM: 1 correia VENCIDA (atrasada desde 09/05/2026) — regularizar imediatamente.",
 f"{URG} correias urgentes (<=30 dias), concentradas em 17/07 e 01/08 — biomassa (SNP), DDGS (SDL/BLS).",
 "Áreas de biomassa e grãos: maior exposição a incêndio por atrito (rolete/correia).",
 "Conclusão do programa depende de NVM (última em 10/10/2026).",
]
ty = 2.35
for r in riscos:
    n = para(0.85, ty, 5.4, "•  " + r, 12, TXT, leading=15)
    ty += 0.28 * n + 0.35
box(6.8, 1.55, 6.0, 4.9, CARD, radius=8)
text(7.05, 1.78, "> Próximos passos", 15, VERDE, bold=True)
passos = [
 "Priorizar a correia vencida de NVM e as urgentes de 17/07 nesta semana.",
 "Confirmar disponibilidade de correia antichama e mão de obra para o pico de set/2026.",
 "Reportar avanço quinzenal por unidade (esteiras concluídas x plano).",
 "Antecipar itens de NVM para fechar o programa antes de 10/10/2026, se possível.",
]
ty = 2.35
for p in passos:
    n = para(7.1, ty, 5.4, "•  " + p, 12, TXT, leading=15)
    ty += 0.28 * n + 0.35
footer(5)
c.showPage()

c.save()
print("OK:", out)
