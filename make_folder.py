# -*- coding: utf-8 -*-
"""Folder do TechDay Dourados em JPEG — visual tech preenchido (Inpasa verde+azul).

Fontes maiores, fundo com textura de circuito, ícones por tema e faixa de
tecnologias/parceiros. Paleta Inpasa verde + azul com acento dourado.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import math

W, H = 1240, 1754

# ---- Paleta Inpasa (verde + azul) ----
VERDE_ESC = (4, 54, 32)
VERDE = (16, 140, 70)
AZUL = (18, 78, 145)
AZUL_ESC = (7, 30, 66)
VERDE_NEON = (95, 235, 155)
AZUL_NEON = (95, 205, 255)
DOURADO = (244, 187, 32)
DOURADO_CLR = (253, 224, 140)
BRANCO = (255, 255, 255)
CINZA_CLARO = (243, 247, 246)
WM = (228, 238, 234)        # watermark suave
TEXTO = (40, 52, 50)
TITULO = (8, 58, 40)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(b, s):
    return ImageFont.truetype(FB if b else F, s)


def darker(c, f):
    return tuple(int(x * f) for x in c)


img = Image.new("RGB", (W, H), BRANCO)
d = ImageDraw.Draw(img)


def grad_h(box, c1, c2):
    x0, y0, x1, y1 = box
    n = x1 - x0
    for i in range(n):
        t = i / max(n - 1, 1)
        c = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        d.line([(x0 + i, y0), (x0 + i, y1)], fill=c)


def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ===== textura de circuito de fundo (corpo) =====
random.seed(99)
bn = [(random.randint(20, W - 20), random.randint(540, H - 120)) for _ in range(60)]
for i, (x1, y1) in enumerate(bn):
    for x2, y2 in bn[i + 1:]:
        if abs(x1 - x2) + abs(y1 - y2) < 170:
            d.line([(x1, y1), (x2, y2)], fill=WM, width=1)
for (x, y) in bn:
    d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=WM)
# hexágonos decorativos suaves
def hexagon(cx, cy, r, col, w=2):
    pts = [(cx + r * math.cos(math.radians(60 * k - 30)),
            cy + r * math.sin(math.radians(60 * k - 30))) for k in range(6)]
    d.line(pts + [pts[0]], fill=col, width=w)
for (hx, hy, hr) in [(1130, 720, 70), (90, 1180, 90), (1150, 1460, 60)]:
    hexagon(hx, hy, hr, WM, 2)
    hexagon(hx, hy, hr - 16, WM, 1)

# ================= CABEÇALHO =================
HEAD = 520
grad_h((0, 0, W, HEAD), VERDE_ESC, AZUL_ESC)

# camada glow + circuito
glow = Image.new("RGBA", (W, HEAD), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
random.seed(21)
nodes = [(random.randint(40, W - 40), random.randint(28, HEAD - 80)) for _ in range(30)]
for i, (x1, y1) in enumerate(nodes):
    for x2, y2 in nodes[i + 1:]:
        if abs(x1 - x2) + abs(y1 - y2) < 240:
            gd.line([(x1, y1), (x2, y2)], fill=(95, 185, 235, 65), width=2)
for (x, y) in nodes:
    col = random.choice([VERDE_NEON, AZUL_NEON, DOURADO])
    gd.ellipse((x - 5, y - 5, x + 5, y + 5), fill=col + (190,))
# grande hexágono tech à direita
for rr in (150, 120):
    pts = [(1080 + rr * math.cos(math.radians(60 * k - 30)),
            150 + rr * math.sin(math.radians(60 * k - 30))) for k in range(6)]
    gd.line(pts + [pts[0]], fill=(120, 200, 240, 70), width=3)
glow = glow.filter(ImageFilter.GaussianBlur(3))
img.paste(Image.alpha_composite(
    img.crop((0, 0, W, HEAD)).convert("RGBA"), glow).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)
for (x, y) in nodes:
    d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(225, 242, 255))

# linha de dados neon
ny = HEAD - 52
d.line([(0, ny), (W, ny)], fill=AZUL_NEON, width=2)
# faixa diagonal dourada
d.polygon([(0, HEAD), (W, HEAD - 30), (W, HEAD), (0, HEAD)], fill=DOURADO)
d.polygon([(0, HEAD - 5), (W, HEAD - 35), (W, HEAD - 28), (0, HEAD + 2)], fill=AZUL_ESC)

# título com glow (fontes maiores)
tglow = Image.new("RGBA", (W, HEAD), (0, 0, 0, 0))
tg = ImageDraw.Draw(tglow)
tg.text((68, 124), "TECH DAY", font=font(True, 132), fill=AZUL_NEON + (255,))
tglow = tglow.filter(ImageFilter.GaussianBlur(12))
img.paste(Image.alpha_composite(
    img.crop((0, 0, W, HEAD)).convert("RGBA"), tglow).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)

d.text((70, 46), "inpasa", font=font(True, 66), fill=BRANCO)
d.ellipse((296, 56, 330, 90), fill=DOURADO)
d.text((68, 124), "TECH DAY", font=font(True, 132), fill=BRANCO)
d.text((72, 270), "DOURADOS", font=font(True, 66), fill=VERDE_NEON)

d.rounded_rectangle((70, 350, 558, 426), radius=18, fill=DOURADO)
d.text((92, 364), "18 e 19 de JUNHO", font=font(True, 46), fill=AZUL_ESC)
d.text((74, 440), "Inovação, automação e IA aplicada à indústria",
       font=font(False, 27), fill=DOURADO_CLR)

# ================= ÍCONES =================
def ic_screen(cx, cy, col):
    d.rounded_rectangle((cx - 36, cy - 28, cx + 36, cy + 18), radius=6,
                        outline=col, width=5)
    pts = [(cx - 28, cy - 2), (cx - 16, cy - 2), (cx - 9, cy - 17),
           (cx, cy + 8), (cx + 9, cy - 10), (cx + 16, cy - 2), (cx + 28, cy - 2)]
    d.line(pts, fill=col, width=4, joint="curve")
    d.rectangle((cx - 12, cy + 18, cx + 12, cy + 23), fill=col)
    d.rectangle((cx - 22, cy + 25, cx + 22, cy + 30), fill=col)


def ic_chip(cx, cy, col):
    d.rounded_rectangle((cx - 28, cy - 28, cx + 28, cy + 28), radius=8,
                        outline=col, width=5)
    d.rounded_rectangle((cx - 12, cy - 12, cx + 12, cy + 12), radius=4,
                        outline=col, width=4)
    for o in (-15, 0, 15):
        d.line([(cx + o, cy - 28), (cx + o, cy - 38)], fill=col, width=4)
        d.line([(cx + o, cy + 28), (cx + o, cy + 38)], fill=col, width=4)
        d.line([(cx - 28, cy + o), (cx - 38, cy + o)], fill=col, width=4)
        d.line([(cx + 28, cy + o), (cx + 38, cy + o)], fill=col, width=4)


def ic_db(cx, cy, col):
    w, h = 30, 11
    for off in (-28, -6, 16):
        d.ellipse((cx - w, cy + off - h, cx + w, cy + off + h),
                  outline=col, width=4)
    d.line([(cx - w, cy - 28), (cx - w, cy + 16)], fill=col, width=4)
    d.line([(cx + w, cy - 28), (cx + w, cy + 16)], fill=col, width=4)
    d.arc((cx - w, cy + 16 - h, cx + w, cy + 16 + h), 0, 180, fill=col, width=4)


def ic_neural(cx, cy, col):
    L = [(cx - 30, cy - 20), (cx - 30, cy + 20)]
    Mi = [(cx, cy - 28), (cx, cy), (cx, cy + 28)]
    R = [(cx + 30, cy - 13), (cx + 30, cy + 13)]
    for a in L:
        for b in Mi:
            d.line([a, b], fill=col, width=3)
    for b in Mi:
        for c in R:
            d.line([b, c], fill=col, width=3)
    for (x, y) in L + Mi + R:
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=col)


ICONS = {"screen": ic_screen, "chip": ic_chip, "db": ic_db, "neural": ic_neural}


def tile(size, c):
    t = Image.new("RGB", (size, size))
    td = ImageDraw.Draw(t)
    c2 = darker(c, 0.58)
    for i in range(size):
        k = i / (size - 1)
        col = tuple(int(c[j] + (c2[j] - c[j]) * k) for j in range(3))
        td.line([(0, i), (size, i)], fill=col)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1),
                                           radius=26, fill=255)
    return t, mask


# ================= CARTÕES =================
cards = [
    ("01", VERDE, "screen", "Centro de Operações Integrado (COI)",
     "Visão e próximos passos. Apoio da Rockwell para um COI robusto e "
     "escalável, tendo como referência o modelo da Vale. Foco em automação, "
     "autonomia operacional e otimização da mão de obra."),
    ("02", AZUL, "chip", "Controle Avançado & IA",
     "Malhas de PID, forces, bypass, simulações e cruzamento de informações, "
     "com aplicação de IA no controle avançado dos processos."),
    ("03", VERDE, "db", "Operacionalização e Arquitetura de Dados",
     "DataOps: coleta, historização (PI System / InfluxDB) e análise de dados. "
     "PyPoint Builder para varredura automática de controladores e "
     "benchmarking entre plantas."),
    ("04", AZUL, "neural", "Logix AI — IA no controle industrial",
     "Otimização de código, predição de resultados, configuração autônoma e "
     "insights para operadores, na evolução rumo a controles autônomos."),
]

x0, x1 = 56, W - 56
TS = 120
TITLE_FS, BODY_FS = 34, 26

FY = H - 100                 # topo do rodapé
SY = FY - 178                # topo da faixa de tecnologias
region_top = HEAD + 26
region_bot = SY - 26
gap = 18
CH = int((region_bot - region_top - gap * (len(cards) + 1)) / len(cards))

y = region_top + gap
for num, cor, ik, titulo, corpo in cards:
    tl = wrap(titulo, font(True, TITLE_FS), x1 - x0 - 30 - TS - 30 - 20)
    bl = wrap(corpo, font(False, BODY_FS), x1 - x0 - 30 - TS - 30 - 20)
    d.rounded_rectangle((x0, y, x1, y + CH), radius=24, fill=CINZA_CLARO)
    d.rounded_rectangle((x0, y, x1, y + CH), radius=24, outline=darker(cor, 0.85),
                        width=3)
    tx_, ty_ = x0 + 30, int(y + (CH - TS) // 2)
    t_img, t_mask = tile(TS, cor)
    img.paste(t_img, (tx_, ty_), t_mask)
    ICONS[ik](tx_ + TS // 2, ty_ + TS // 2, BRANCO)
    d.ellipse((tx_ - 8, ty_ - 8, tx_ + 38, ty_ + 38), fill=DOURADO)
    nb = font(True, 28)
    nw = d.textlength(num, font=nb)
    d.text((tx_ + 15 - nw / 2, ty_ + 1), num, font=nb, fill=AZUL_ESC)
    bh = len(tl) * 44 + 10 + len(bl) * 36
    tx = x0 + 30 + TS + 30
    ty = int(y + (CH - bh) // 2)
    for ln in tl:
        d.text((tx, ty), ln, font=font(True, TITLE_FS), fill=TITULO)
        ty += 44
    ty += 10
    for ln in bl:
        d.text((tx, ty), ln, font=font(False, BODY_FS), fill=TEXTO)
        ty += 36
    y += CH + gap

# ================= FAIXA TECNOLOGIAS & PARCEIROS =================
d.text((x0, SY), "TECNOLOGIAS & PARCEIROS", font=font(True, 30), fill=TITULO)
d.line([(x0, SY + 44), (x1, SY + 44)], fill=VERDE, width=3)

tags = [("Rockwell", VERDE), ("PI System", AZUL), ("InfluxDB", VERDE),
        ("Logix AI", AZUL), ("PyPoint Builder", VERDE), ("IA / ML", AZUL)]
px, py = x0, SY + 60
for txt, cor in tags:
    tw = d.textlength(txt, font=font(True, 26))
    pw = tw + 80
    if px + pw > x1:
        px = x0
        py += 68
    d.rounded_rectangle((px, py, px + pw, py + 56), radius=28, fill=BRANCO,
                        outline=cor, width=3)
    d.ellipse((px + 16, py + 16, px + 40, py + 40), fill=cor)
    d.ellipse((px + 24, py + 24, px + 32, py + 32), fill=BRANCO)
    d.text((px + 56, py + 13), txt, font=font(True, 26), fill=darker(cor, 0.8))
    px += pw + 18

# ================= RODAPÉ =================
grad_h((0, FY, W, H), VERDE, AZUL)
d.rectangle((0, FY, W, FY + 6), fill=DOURADO)
random.seed(5)
for _ in range(22):
    fx = random.randint(40, W - 40)
    fy = random.randint(FY + 12, H - 14)
    d.ellipse((fx, fy, fx + 3, fy + 3), fill=(185, 222, 255))
d.text((70, FY + 30), "Dourados • 18 e 19/06", font=font(True, 34), fill=BRANCO)
rt = "COI • DataOps • Logix AI • IA"
rw = d.textlength(rt, font=font(True, 26))
d.text((W - 70 - rw, FY + 36), rt, font=font(True, 26), fill=DOURADO_CLR)

img.save("folder_techday_dourados.jpg", "JPEG", quality=93)
print("OK -> folder_techday_dourados.jpg", img.size)
