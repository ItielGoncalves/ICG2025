# -*- coding: utf-8 -*-
"""Gera o folder (folheto promocional) do TechDay Dourados em JPEG.

Padrão visual Inpasa: verde (agro/etanol de milho) + acento dourado,
tipografia limpa sobre fundo branco.
"""
from PIL import Image, ImageDraw, ImageFont
import random

W, H = 1240, 1754  # A4 a ~150 dpi (retrato)

# ---- Paleta Inpasa ----
VERDE_ESC = (5, 59, 33)      # verde profundo
VERDE = (10, 122, 60)        # verde Inpasa
VERDE_CLARO = (146, 201, 122)
DOURADO = (240, 180, 30)     # milho / etanol
DOURADO_CLR = (252, 220, 130)
BRANCO = (255, 255, 255)
CINZA_CLARO = (240, 245, 240)
TEXTO = (40, 52, 46)
TITULO = (6, 66, 38)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(bold, size):
    return ImageFont.truetype(FB if bold else F, size)


img = Image.new("RGB", (W, H), BRANCO)
d = ImageDraw.Draw(img)


def vgrad(box, c1, c2):
    x0, y0, x1, y1 = box
    h = y1 - y0
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


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


# ---------- Cabeçalho ----------
HEAD = 440
vgrad((0, 0, W, HEAD), VERDE_ESC, VERDE)

# folhas/grãos decorativos
random.seed(11)
for _ in range(60):
    x = random.randint(40, W - 40)
    y = random.randint(28, HEAD - 120)
    r = random.choice([2, 2, 3, 4])
    d.ellipse((x, y, x + r, y + r), fill=(30, 110, 64))

# faixa diagonal dourada na base do cabeçalho
d.polygon([(0, HEAD), (W, HEAD - 42), (W, HEAD), (0, HEAD)], fill=DOURADO)
d.polygon([(0, HEAD - 6), (W, HEAD - 48), (W, HEAD - 38), (0, HEAD + 4)], fill=VERDE_ESC)

# marca "inpasa" (wordmark substituto)
d.text((70, 56), "inpasa", font=font(True, 58), fill=BRANCO)
d.ellipse((262, 66, 290, 94), fill=DOURADO)  # ponto/grão sobre a marca
d.text((70, 122), "TECH DAY", font=font(True, 100), fill=BRANCO)
d.text((74, 234), "DOURADOS", font=font(True, 60), fill=VERDE_CLARO)

# faixa de data
d.rounded_rectangle((70, 306, 520, 378), radius=14, fill=DOURADO)
d.text((92, 322), "18 e 19 de JUNHO", font=font(True, 38), fill=VERDE_ESC)

d.text((74, 392), "Inovação, automação e IA aplicada à indústria",
       font=font(False, 24), fill=DOURADO_CLR)

# ---------- Cartões de conteúdo (textos revisados) ----------
cards = [
    ("01", "Centro de Operações Integrado (COI)",
     "Visão e próximos passos. Apoio da Rockwell para um COI robusto e "
     "escalável, tendo como referência o modelo da Vale. Foco em automação, "
     "autonomia operacional e otimização da mão de obra."),
    ("02", "Controle Avançado & IA",
     "Malhas de PID, forces, bypass, simulações e cruzamento de informações, "
     "com aplicação de IA no controle avançado dos processos."),
    ("03", "Operacionalização e Arquitetura de Dados (DataOps)",
     "Coleta, historização (PI System / InfluxDB) e análise de dados "
     "operacionais. PyPoint Builder para varredura automática de "
     "controladores e benchmarking entre plantas."),
    ("04", "Logix AI — IA no controle industrial",
     "Otimização de código, predição de resultados, configuração autônoma e "
     "insights para operadores, na evolução rumo a controles autônomos."),
]

x0, x1 = 60, W - 60
y = HEAD + 50
for num, titulo, corpo in cards:
    tlines = wrap(titulo, font(True, 31), x1 - x0 - 150)
    blines = wrap(corpo, font(False, 25), x1 - x0 - 150)
    ch = 40 + len(tlines) * 38 + len(blines) * 34 + 40
    d.rounded_rectangle((x0, y, x1, y + ch), radius=20, fill=CINZA_CLARO)
    d.rounded_rectangle((x0, y, x0 + 12, y + ch), radius=6, fill=VERDE)
    # número
    d.ellipse((x0 + 36, y + 28, x0 + 116, y + 108), fill=VERDE)
    d.ellipse((x0 + 36, y + 28, x0 + 116, y + 108), outline=DOURADO, width=3)
    nb = font(True, 36)
    nw = d.textlength(num, font=nb)
    d.text((x0 + 76 - nw / 2, y + 48), num, font=nb, fill=BRANCO)
    # textos
    tx, ty = x0 + 150, y + 26
    for ln in tlines:
        d.text((tx, ty), ln, font=font(True, 31), fill=TITULO)
        ty += 38
    ty += 8
    for ln in blines:
        d.text((tx, ty), ln, font=font(False, 25), fill=TEXTO)
        ty += 34
    y += ch + 24

# ---------- Rodapé ----------
FY = H - 92
vgrad((0, FY, W, H), VERDE, VERDE_ESC)
d.rectangle((0, FY, W, FY + 6), fill=DOURADO)
d.text((70, FY + 26), "Dourados • 18 e 19/06", font=font(True, 30), fill=BRANCO)
rt = "Rockwell • COI • DataOps • Logix AI"
rw = d.textlength(rt, font=font(False, 24))
d.text((W - 70 - rw, FY + 32), rt, font=font(False, 24), fill=DOURADO_CLR)

img.save("folder_techday_dourados.jpg", "JPEG", quality=92)
print("OK -> folder_techday_dourados.jpg", img.size)
