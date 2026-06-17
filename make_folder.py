# -*- coding: utf-8 -*-
"""Gera o folder (folheto promocional) do TechDay Dourados em JPEG."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1240, 1754  # A4 a ~150 dpi (retrato)

# Paleta (tema industrial / tecnologia)
AZUL_ESCURO = (11, 31, 58)
AZUL = (16, 60, 110)
CIANO = (0, 184, 217)
CIANO_CLARO = (120, 224, 240)
BRANCO = (255, 255, 255)
CINZA = (90, 104, 122)
CINZA_CLARO = (238, 242, 247)
TEXTO = (38, 50, 66)

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
HEAD = 430
vgrad((0, 0, W, HEAD), AZUL_ESCURO, AZUL)

# detalhe diagonal ciano
d.polygon([(0, HEAD), (W, HEAD - 70), (W, HEAD), (0, HEAD)], fill=CIANO)
d.polygon([(0, HEAD - 6), (W, HEAD - 76), (W, HEAD - 64), (0, HEAD + 6)], fill=AZUL_ESCURO)

# pontos decorativos (circuito)
import random
random.seed(7)
for _ in range(70):
    x = random.randint(40, W - 40)
    y = random.randint(30, HEAD - 110)
    r = random.choice([1, 1, 2, 2, 3])
    d.ellipse((x, y, x + r, y + r), fill=(40, 90, 150))

d.text((70, 70), "TECHDAY", font=font(True, 92), fill=BRANCO)
d.text((74, 168), "DOURADOS", font=font(True, 70), fill=CIANO_CLARO)

# faixa de data
d.rounded_rectangle((70, 270, 540, 350), radius=14, fill=CIANO)
d.text((92, 288), "18 e 19 de JUNHO", font=font(True, 40), fill=AZUL_ESCURO)

d.text((74, 372), "Inovação, Automação e IA aplicada à indústria",
       font=font(False, 27), fill=CIANO_CLARO)

# ---------- Cartões de conteúdo ----------
cards = [
    ("01", "Centro de Operações Integrado (COI)",
     "Visão e próximos passos. Apoio da Rockwell para um COI robusto e "
     "escalável, com referência ao modelo da Vale. Automação, autonomia "
     "operacional e otimização de mão de obra."),
    ("02", "Controle Avançado & Aplicação de IA",
     "Malhas de PID, forces, bypass, simulações e cruzamento de informações. "
     "Aplicação de IA no controle avançado dos processos."),
    ("03", "DataOps & Arquitetura de Dados",
     "Coleta, historização (PI System / InfluxDB) e análise de dados "
     "operacionais. PyPoint Builder para varredura automática de controladores "
     "e benchmarking entre plantas."),
    ("04", "Logix AI — IA no Controle Industrial",
     "Otimização de código, predição de resultados, configuração autônoma e "
     "insights para operadores, rumo a controles autônomos."),
]

x0, x1 = 60, W - 60
y = HEAD + 55
for num, titulo, corpo in cards:
    tlines = wrap(titulo, font(True, 33), x1 - x0 - 150)
    blines = wrap(corpo, font(False, 25), x1 - x0 - 150)
    ch = 44 + len(tlines) * 40 + len(blines) * 34 + 40
    # cartão
    d.rounded_rectangle((x0, y, x1, y + ch), radius=20, fill=CINZA_CLARO)
    d.rounded_rectangle((x0, y, x0 + 12, y + ch), radius=6, fill=CIANO)
    # número
    d.ellipse((x0 + 36, y + 28, x0 + 116, y + 108), fill=AZUL)
    nb = font(True, 38)
    nw = d.textlength(num, font=nb)
    d.text((x0 + 76 - nw / 2, y + 46), num, font=nb, fill=BRANCO)
    # textos
    tx = x0 + 150
    ty = y + 28
    for ln in tlines:
        d.text((tx, ty), ln, font=font(True, 33), fill=AZUL_ESCURO)
        ty += 40
    ty += 8
    for ln in blines:
        d.text((tx, ty), ln, font=font(False, 25), fill=TEXTO)
        ty += 34
    y += ch + 26

# ---------- Rodapé ----------
FY = H - 90
vgrad((0, FY, W, H), AZUL, AZUL_ESCURO)
d.text((70, FY + 22), "Dourados • 18 e 19/06", font=font(True, 30), fill=BRANCO)
rt = "Rockwell • COI • DataOps • Logix AI"
rw = d.textlength(rt, font=font(False, 24))
d.text((W - 70 - rw, FY + 28), rt, font=font(False, 24), fill=CIANO_CLARO)

img.save("folder_techday_dourados.jpg", "JPEG", quality=92)
print("OK -> folder_techday_dourados.jpg", img.size)
