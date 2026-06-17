# -*- coding: utf-8 -*-
"""Gera o folder (folheto promocional) do TechDay Dourados em JPEG.

Padrão visual Inpasa: verde + azul (cores da marca), acento dourado,
tipografia limpa sobre fundo branco.
"""
from PIL import Image, ImageDraw, ImageFont
import random

W, H = 1240, 1754  # A4 a ~150 dpi (retrato)

# ---- Paleta Inpasa (verde + azul) ----
VERDE_ESC = (5, 64, 36)
VERDE = (12, 124, 62)
AZUL = (16, 70, 130)
AZUL_ESC = (9, 38, 78)
VERDE_CLARO = (150, 205, 130)
AZUL_CLARO = (130, 190, 235)
DOURADO = (242, 183, 28)
DOURADO_CLR = (252, 222, 135)
BRANCO = (255, 255, 255)
CINZA_CLARO = (240, 245, 244)
TEXTO = (40, 52, 50)
TITULO = (8, 60, 40)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(bold, size):
    return ImageFont.truetype(FB if bold else F, size)


img = Image.new("RGB", (W, H), BRANCO)
d = ImageDraw.Draw(img)


def grad(box, c1, c2, horizontal=False):
    x0, y0, x1, y1 = box
    n = (x1 - x0) if horizontal else (y1 - y0)
    for i in range(n):
        t = i / max(n - 1, 1)
        c = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        if horizontal:
            d.line([(x0 + i, y0), (x0 + i, y1)], fill=c)
        else:
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


# ---------- Cabeçalho (degradê verde -> azul) ----------
HEAD = 470
grad((0, 0, W, HEAD), VERDE_ESC, AZUL, horizontal=True)
# leve escurecimento no topo para contraste do texto
ov = Image.new("RGB", (W, 150), (0, 0, 0))
img.paste(Image.blend(img.crop((0, 0, W, 150)), ov, 0.18), (0, 0))

# grãos/pontos decorativos discretos no lado azul
random.seed(13)
for _ in range(45):
    x = random.randint(720, W - 30)
    y = random.randint(28, HEAD - 150)
    r = random.choice([2, 3, 4])
    d.ellipse((x, y, x + r, y + r), fill=(60, 130, 180))

# faixa diagonal dourada fina na base do cabeçalho
d.polygon([(0, HEAD), (W, HEAD - 30), (W, HEAD), (0, HEAD)], fill=DOURADO)
d.polygon([(0, HEAD - 5), (W, HEAD - 35), (W, HEAD - 27), (0, HEAD + 3)], fill=AZUL_ESC)

# marca "inpasa" (wordmark recriado)
d.text((70, 52), "inpasa", font=font(True, 60), fill=BRANCO)
d.ellipse((268, 62, 298, 92), fill=DOURADO)  # grão sobre a marca

d.text((70, 124), "TECH DAY", font=font(True, 102), fill=BRANCO)
d.text((74, 240), "DOURADOS", font=font(True, 58), fill=VERDE_CLARO)

# faixa de data
d.rounded_rectangle((70, 312, 520, 384), radius=14, fill=DOURADO)
d.text((92, 328), "18 e 19 de JUNHO", font=font(True, 38), fill=AZUL_ESC)

# tagline com respiro acima da faixa dourada
d.text((74, 398), "Inovação, automação e IA aplicada à indústria",
       font=font(False, 24), fill=DOURADO_CLR)

# ---------- Cartões (acento alternando verde/azul) ----------
cards = [
    ("01", VERDE, "Centro de Operações Integrado (COI)",
     "Visão e próximos passos. Apoio da Rockwell para um COI robusto e "
     "escalável, tendo como referência o modelo da Vale. Foco em automação, "
     "autonomia operacional e otimização da mão de obra."),
    ("02", AZUL, "Controle Avançado & IA",
     "Malhas de PID, forces, bypass, simulações e cruzamento de informações, "
     "com aplicação de IA no controle avançado dos processos."),
    ("03", VERDE, "Operacionalização e Arquitetura de Dados (DataOps)",
     "Coleta, historização (PI System / InfluxDB) e análise de dados "
     "operacionais. PyPoint Builder para varredura automática de "
     "controladores e benchmarking entre plantas."),
    ("04", AZUL, "Logix AI — IA no controle industrial",
     "Otimização de código, predição de resultados, configuração autônoma e "
     "insights para operadores, na evolução rumo a controles autônomos."),
]

x0, x1 = 60, W - 60
y = HEAD + 50
for num, cor, titulo, corpo in cards:
    tlines = wrap(titulo, font(True, 31), x1 - x0 - 150)
    blines = wrap(corpo, font(False, 25), x1 - x0 - 150)
    ch = 40 + len(tlines) * 38 + len(blines) * 34 + 40
    d.rounded_rectangle((x0, y, x1, y + ch), radius=20, fill=CINZA_CLARO)
    d.rounded_rectangle((x0, y, x0 + 12, y + ch), radius=6, fill=cor)
    # número
    d.ellipse((x0 + 36, y + 28, x0 + 116, y + 108), fill=cor)
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

# ---------- Rodapé (degradê verde -> azul) ----------
FY = H - 92
grad((0, FY, W, H), VERDE, AZUL, horizontal=True)
d.rectangle((0, FY, W, FY + 6), fill=DOURADO)
d.text((70, FY + 26), "Dourados • 18 e 19/06", font=font(True, 30), fill=BRANCO)
rt = "Rockwell • COI • DataOps • Logix AI"
rw = d.textlength(rt, font=font(False, 24))
d.text((W - 70 - rw, FY + 32), rt, font=font(False, 24), fill=DOURADO_CLR)

img.save("folder_techday_dourados.jpg", "JPEG", quality=92)
print("OK -> folder_techday_dourados.jpg", img.size)
