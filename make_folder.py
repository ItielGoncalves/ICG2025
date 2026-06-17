# -*- coding: utf-8 -*-
"""Folder do TechDay Dourados em JPEG — visual tech (Inpasa verde + azul).

Elementos: cabeçalho com circuito/nós e glow, ícones desenhados por tema,
tiles em degradê, paleta Inpasa verde+azul com acento dourado.
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
VERDE_NEON = (90, 230, 150)
AZUL_NEON = (90, 200, 255)
DOURADO = (244, 187, 32)
DOURADO_CLR = (253, 224, 140)
BRANCO = (255, 255, 255)
CINZA_CLARO = (242, 246, 245)
TEXTO = (44, 56, 54)
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


# ================= CABEÇALHO =================
HEAD = 500
grad_h((0, 0, W, HEAD), VERDE_ESC, AZUL_ESC)

# --- camada de glow + circuito (RGBA, depois blur) ---
glow = Image.new("RGBA", (W, HEAD), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
random.seed(21)
nodes = [(random.randint(40, W - 40), random.randint(30, HEAD - 90)) for _ in range(26)]
# traços de circuito ligando nós próximos
for i, (x1, y1) in enumerate(nodes):
    for x2, y2 in nodes[i + 1:]:
        if abs(x1 - x2) + abs(y1 - y2) < 230:
            gd.line([(x1, y1), (x2, y2)], fill=(90, 180, 230, 60), width=2)
# nós brilhantes
for (x, y) in nodes:
    col = random.choice([VERDE_NEON, AZUL_NEON, DOURADO])
    gd.ellipse((x - 5, y - 5, x + 5, y + 5), fill=col + (180,))
glow = glow.filter(ImageFilter.GaussianBlur(3))
img.paste(Image.alpha_composite(
    img.crop((0, 0, W, HEAD)).convert("RGBA"), glow).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)

# nós nítidos por cima
for (x, y) in nodes:
    d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(220, 240, 255))

# linha neon de dados na base do cabeçalho
ny = HEAD - 46
d.line([(0, ny), (W, ny)], fill=AZUL_NEON, width=2)
for gx in range(0, W, 6):
    a = 120 + int(100 * math.sin(gx / 40.0))
    d.point((gx, ny), fill=(min(255, a + 120),) * 3)
# faixa diagonal dourada fina
d.polygon([(0, HEAD), (W, HEAD - 26), (W, HEAD), (0, HEAD)], fill=DOURADO)
d.polygon([(0, HEAD - 4), (W, HEAD - 30), (W, HEAD - 24), (0, HEAD + 2)], fill=AZUL_ESC)

# marca + título com glow
tglow = Image.new("RGBA", (W, HEAD), (0, 0, 0, 0))
tg = ImageDraw.Draw(tglow)
tg.text((70, 130), "TECH DAY", font=font(True, 108), fill=AZUL_NEON + (255,))
tglow = tglow.filter(ImageFilter.GaussianBlur(10))
img.paste(Image.alpha_composite(
    img.crop((0, 0, W, HEAD)).convert("RGBA"), tglow).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)

d.text((70, 56), "inpasa", font=font(True, 60), fill=BRANCO)
d.ellipse((268, 66, 298, 96), fill=DOURADO)
d.text((70, 130), "TECH DAY", font=font(True, 108), fill=BRANCO)
d.text((74, 252), "DOURADOS", font=font(True, 56), fill=VERDE_NEON)

d.rounded_rectangle((70, 326, 522, 398), radius=16, fill=DOURADO)
d.text((92, 342), "18 e 19 de JUNHO", font=font(True, 38), fill=AZUL_ESC)
d.text((74, 412), "Inovação, automação e IA aplicada à indústria",
       font=font(False, 24), fill=DOURADO_CLR)

# ================= ÍCONES =================
def ic_screen(cx, cy, col):  # COI — central de operações
    d.rounded_rectangle((cx - 30, cy - 24, cx + 30, cy + 14), radius=5,
                        outline=col, width=4)
    pts = [(cx - 24, cy - 2), (cx - 14, cy - 2), (cx - 8, cy - 14),
           (cx, cy + 6), (cx + 8, cy - 8), (cx + 14, cy - 2), (cx + 24, cy - 2)]
    d.line(pts, fill=col, width=3, joint="curve")
    d.rectangle((cx - 10, cy + 14, cx + 10, cy + 18), fill=col)
    d.rectangle((cx - 18, cy + 20, cx + 18, cy + 24), fill=col)


def ic_chip(cx, cy, col):  # controle avançado & IA
    d.rounded_rectangle((cx - 22, cy - 22, cx + 22, cy + 22), radius=6,
                        outline=col, width=4)
    d.rounded_rectangle((cx - 9, cy - 9, cx + 9, cy + 9), radius=3,
                        outline=col, width=3)
    for o in (-12, 0, 12):
        d.line([(cx + o, cy - 22), (cx + o, cy - 30)], fill=col, width=3)
        d.line([(cx + o, cy + 22), (cx + o, cy + 30)], fill=col, width=3)
        d.line([(cx - 22, cy + o), (cx - 30, cy + o)], fill=col, width=3)
        d.line([(cx + 22, cy + o), (cx + 30, cy + o)], fill=col, width=3)


def ic_db(cx, cy, col):  # dataops
    w, h = 24, 9
    for off in (-22, -4, 14):
        d.ellipse((cx - w, cy + off - h, cx + w, cy + off + h),
                  outline=col, width=3)
    d.line([(cx - w, cy - 22), (cx - w, cy + 14)], fill=col, width=3)
    d.line([(cx + w, cy - 22), (cx + w, cy + 14)], fill=col, width=3)
    d.arc((cx - w, cy + 14 - h, cx + w, cy + 14 + h), 0, 180, fill=col, width=3)


def ic_neural(cx, cy, col):  # logix ai
    L = [(cx - 24, cy - 16), (cx - 24, cy + 16)]
    Mi = [(cx, cy - 22), (cx, cy), (cx, cy + 22)]
    R = [(cx + 24, cy - 10), (cx + 24, cy + 10)]
    for a in L:
        for b in Mi:
            d.line([a, b], fill=col, width=2)
    for b in Mi:
        for c in R:
            d.line([b, c], fill=col, width=2)
    for (x, y) in L + Mi + R:
        d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=col)


ICONS = {"screen": ic_screen, "chip": ic_chip, "db": ic_db, "neural": ic_neural}


def tile(size, c):
    t = Image.new("RGB", (size, size))
    td = ImageDraw.Draw(t)
    c2 = darker(c, 0.6)
    for i in range(size):
        k = i / (size - 1)
        col = tuple(int(c[j] + (c2[j] - c[j]) * k) for j in range(3))
        td.line([(0, i), (size, i)], fill=col)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1),
                                           radius=22, fill=255)
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
    ("03", VERDE, "db", "Operacionalização e Arquitetura de Dados (DataOps)",
     "Coleta, historização (PI System / InfluxDB) e análise de dados "
     "operacionais. PyPoint Builder para varredura automática de "
     "controladores e benchmarking entre plantas."),
    ("04", AZUL, "neural", "Logix AI — IA no controle industrial",
     "Otimização de código, predição de resultados, configuração autônoma e "
     "insights para operadores, na evolução rumo a controles autônomos."),
]

x0, x1 = 60, W - 60
TS = 104  # tile size
y = HEAD + 46
for num, cor, ikind, titulo, corpo in cards:
    tlines = wrap(titulo, font(True, 31), x1 - x0 - 190)
    blines = wrap(corpo, font(False, 24), x1 - x0 - 190)
    body_h = 36 + len(tlines) * 38 + 6 + len(blines) * 33
    ch = max(TS + 36, body_h + 30)
    # cartão com borda sutil
    d.rounded_rectangle((x0, y, x1, y + ch), radius=22, fill=CINZA_CLARO)
    d.rounded_rectangle((x0, y, x1, y + ch), radius=22, outline=darker(cor, 0.9),
                        width=2)
    # tile com ícone
    tx_, ty_ = x0 + 28, y + (ch - TS) // 2
    t_img, t_mask = tile(TS, cor)
    img.paste(t_img, (tx_, ty_), t_mask)
    ICONS[ikind](tx_ + TS // 2, ty_ + TS // 2, BRANCO)
    # número (badge dourado)
    d.ellipse((tx_ - 6, ty_ - 6, tx_ + 32, ty_ + 32), fill=DOURADO)
    nb = font(True, 24)
    nw = d.textlength(num, font=nb)
    d.text((tx_ + 13 - nw / 2, ty_ + 1), num, font=nb, fill=AZUL_ESC)
    # textos
    tx = x0 + 28 + TS + 26
    ty = y + (ch - body_h) // 2 + 6
    for ln in tlines:
        d.text((tx, ty), ln, font=font(True, 31), fill=TITULO)
        ty += 38
    ty += 6
    for ln in blines:
        d.text((tx, ty), ln, font=font(False, 24), fill=TEXTO)
        ty += 33
    y += ch + 22

# ================= RODAPÉ =================
FY = H - 96
grad_h((0, FY, W, H), VERDE, AZUL)
d.rectangle((0, FY, W, FY + 5), fill=DOURADO)
# nós no rodapé
random.seed(5)
for _ in range(18):
    fx = random.randint(40, W - 40)
    fy = random.randint(FY + 12, H - 12)
    d.ellipse((fx, fy, fx + 3, fy + 3), fill=(180, 220, 255))
d.text((70, FY + 28), "Dourados • 18 e 19/06", font=font(True, 30), fill=BRANCO)
rt = "Rockwell • COI • DataOps • Logix AI"
rw = d.textlength(rt, font=font(False, 24))
d.text((W - 70 - rw, FY + 34), rt, font=font(False, 24), fill=DOURADO_CLR)

img.save("folder_techday_dourados.jpg", "JPEG", quality=93)
print("OK -> folder_techday_dourados.jpg", img.size)
