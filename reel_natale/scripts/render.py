"""Reel 'Manuale del Natale in negozio' - grafica 2D sincronizzata con la voce ElevenLabs.
1080x1920, 30 fps. Tutti i testi stanno nell'area sicura Instagram SAFE (verificata in automatico).

  python render.py still T OUT.png
  python render.py frames DIR [T0 T1]
  python render.py check            -> verifica area sicura su tutti i fotogrammi
  python render.py assets           -> esporta grafiche separate e copertina
"""
import math, os, random, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "reel", "scripts"))
from render import (ease, ease_out, fade, text_sprite, paste, overlay, brush, hex2rgb,  # noqa: E402
                    ORANGE, CREAM, ANTH, WHITE)

ROOT = os.path.dirname(HERE)
W, H, FPS = 1080, 1920, 30
DUR = 46.6
RED, GOLD, GREEN, SKIN = "#C62828", "#E2B33C", "#2E7D4F", "#F2C9A5"
SAFE = (80, 250, 890, 1500)          # x0, y0, x1, y1: fuori da qui niente testo
CX = (SAFE[0] + SAFE[2]) // 2         # centro dell'area sicura (485)
MAXW = SAFE[2] - SAFE[0] - 30

# tempi della voce (rilevati dalle pause dell'audio)
T = dict(s1=0.0, s2=3.3, s2b=3.9, s3=5.45, s4=7.2, l1=7.35, l2=9.5, l3=11.35, l4=12.15, l5=12.75,
         s5=15.95, s6=21.0, s7=22.3, s8=25.8, s8b=27.7, f1=28.95, f2=30.35, f3=32.35,
         s9=34.05, s10=37.3, s11=39.8, s12=43.4)

BOXES = []   # rettangoli di testo disegnati (per il controllo area sicura)

def fit(s, size, color=ANTH, bold=True, maxw=MAXW):
    sp = text_sprite(s, size, color, bold)
    while sp.width > maxw:
        size -= 2
        sp = text_sprite(s, size, color, bold)
    return sp

def txt(fr, s, size, y, a, color=ANTH, bold=True, x=CX, t0=None, t=None, rise=26):
    if a <= 0.01:
        return
    sp = fit(s, size, color, bold)
    if t0 is not None:
        y += rise * (1 - ease((t - t0) / .45))
    paste(fr, sp, x, y, a)
    if a > .5:
        BOXES.append((x - sp.width / 2, y - sp.height / 2, x + sp.width / 2, y + sp.height / 2, s))

def hl(fr, s, size, y, a, t, t0, col=ORANGE, fg=WHITE):
    """Testo bianco su pennellata che si allunga."""
    if a <= 0.01:
        return
    sp = fit(s, size, fg, maxw=MAXW - 40)
    overlay(fr, lambda d: brush(d, CX - sp.width / 2 - 18, y - sp.height / 2 - 14, CX + sp.width / 2 + 18,
                                y + sp.height / 2 + 14, ease((t - t0) / .4), col), a)
    paste(fr, sp, CX, y, a * ease((t - t0 - .15) / .25))
    if a > .5:
        BOXES.append((CX - sp.width / 2 - 18, y - sp.height / 2, CX + sp.width / 2 + 18, y + sp.height / 2, s))

# ---------------- sfondo e decorazioni ----------------
SNOW = [(random.Random(i).uniform(0, W), random.Random(i + 99).uniform(0, H), random.Random(i + 7).uniform(3, 8))
        for i in range(70)]

def background(t, col=CREAM, snow=True, tint=None):
    im = Image.new("RGBA", (W, H), col)
    d = ImageDraw.Draw(im)
    if tint:
        im.alpha_composite(Image.new("RGBA", (W, H), tint))
    o = math.sin(t * .8) * 10
    d.ellipse((-230, -210 + o, 250, 270 + o), fill=hex2rgb(ORANGE, 60))
    d.ellipse((880, 1660 - o, 1320, 2100 - o), fill=hex2rgb(RED, 45))
    if snow:
        for x, y, r in SNOW:
            yy = (y + t * 60 * r / 5) % H
            xx = x + math.sin(t + y) * 12
            d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=(255, 255, 255, 210))
    return im

def person(d, x, y, s, col, bag=None, hair=ANTH):
    d.ellipse((x - 26 * s, y - 150 * s, x + 26 * s, y - 98 * s), fill=SKIN)
    d.pieslice((x - 27 * s, y - 152 * s, x + 27 * s, y - 112 * s), 180, 360, fill=hair)
    d.rounded_rectangle((x - 38 * s, y - 96 * s, x + 38 * s, y - 10 * s), int(26 * s), fill=col)
    d.rectangle((x - 26 * s, y - 14 * s, x - 6 * s, y), fill=ANTH)
    d.rectangle((x + 6 * s, y - 14 * s, x + 26 * s, y), fill=ANTH)
    if bag:
        d.rounded_rectangle((x + 34 * s, y - 62 * s, x + 80 * s, y - 14 * s), 4, fill=bag)
        d.arc((x + 44 * s, y - 80 * s, x + 70 * s, y - 50 * s), 180, 360, fill=ANTH, width=max(2, int(4 * s)))
        d.rectangle((x + 54 * s, y - 62 * s, x + 60 * s, y - 14 * s), fill=GOLD)

def storefront(d, t, crowd=0.0):
    x0, x1, y0, y1 = 130, 840, 820, 1430
    d.rectangle((x0, y0, x1, y1), fill="#FFFFFF")
    for i in range(10):  # tenda a righe
        c = RED if i % 2 == 0 else WHITE
        xa = x0 - 20 + i * (x1 - x0 + 40) / 10
        d.polygon([(xa, y0 - 10), (xa + (x1 - x0 + 40) / 10, y0 - 10),
                   (xa + (x1 - x0 + 40) / 10, y0 + 70), (xa, y0 + 70)], fill=c)
    d.rounded_rectangle((x0 - 20, y0 - 90, x1 + 20, y0 - 10), 14, fill=ANTH)
    d.rectangle((x0 + 40, y0 + 120, 560, y1 - 90), fill="#FDE9D6", outline=ANTH, width=8)  # vetrina
    d.rectangle((620, y0 + 120, 790, y1), fill="#7A4A2A", outline=ANTH, width=8)            # porta
    d.ellipse((760, y0 + 380, 776, y0 + 396), fill=GOLD)
    for k in range(9):  # ghirlanda
        cx = x0 + 60 + k * 50
        d.ellipse((cx - 22, y0 + 100, cx + 22, y0 + 140), fill=GREEN)
        if k % 2:
            d.ellipse((cx - 7, y0 + 112, cx + 7, y0 + 126), fill=RED if k % 4 == 1 else GOLD)
    for k, (gx, gw, gh, gc) in enumerate([(220, 90, 80, RED), (330, 70, 110, GREEN), (420, 100, 70, GOLD)]):
        yb = y1 - 92
        d.rectangle((gx, yb - gh, gx + gw, yb), fill=gc)
        d.rectangle((gx + gw / 2 - 6, yb - gh, gx + gw / 2 + 6, yb), fill=WHITE)
    d.rectangle((x0 - 30, y1, x1 + 30, y1 + 24), fill=ANTH)

# ---------------- scene ----------------
def sc_hook(t):
    fr = background(t)
    d = ImageDraw.Draw(fr)
    storefront(d, t)
    # clienti con regali che arrivano
    for i, (sx, ex, col, bag, dl) in enumerate([(-120, 260, ORANGE, RED, 0), (1200, 470, GREEN, GOLD, .3),
                                                (-160, 120, "#2D7DD2", GOLD, .6), (1240, 700, RED, GREEN, .9)]):
        k = ease_out((t - dl) / 1.6)
        x = sx + (ex - sx) * k
        person(d, x, 1450 + (i % 2) * 20, 1.15, col, bag)
    txt(fr, "I TUOI CLIENTI", 84, 340, fade(t, .2, 3.1), t0=.2, t=t)
    txt(fr, "PENSANO GIÀ", 84, 440, fade(t, .45, 3.1), t0=.45, t=t)
    hl(fr, "AI REGALI DI NATALE", 76, 560, fade(t, .8, 3.1), t, .8, RED)
    # 3.3-7.2: domanda + avviso
    txt(fr, "E TU,", 92, 360, fade(t, T["s2"], 7.0), t0=T["s2"], t=t)
    txt(fr, "SEI PRONTO", 84, 470, fade(t, T["s2b"], 7.0), t0=T["s2b"], t=t)
    txt(fr, "AD ACCOGLIERLI?", 84, 570, fade(t, T["s2b"] + .2, 7.0), color=ORANGE, t0=T["s2b"] + .2, t=t)
    a = fade(t, T["s3"], 7.0)
    if a > 0:
        overlay(fr, lambda d: d.rounded_rectangle((CX - 400, 615, CX + 400, 712), 22, fill=ANTH), a)
        txt(fr, "NON FARTI COGLIERE IMPREPARATO!", 46, 663, a, color=WHITE)
    return fr

LIST = [("l1", "Decorazioni"), ("l2", "Vetrine da organizzare"), ("l3", "Prodotti da esporre"),
        ("l4", "Promozioni da pianificare"), ("l5", "Scorte da controllare")]

def todo(fr, t, y0, n_shown, checks=0.0, a=1.0, t_check0=0):
    """Foglio 'DA FARE' che si allunga; checks>0 spunta le voci in sequenza."""
    if a <= .01:
        return
    rows = sum(ease((n - i)) for i, n in enumerate([n_shown] * 5))
    h = 150 + rows * 112
    def f(d):
        d.rounded_rectangle((CX - 360 + 8, y0 + 8, CX + 360 + 8, y0 + h + 8), 26, fill=(0, 0, 0, 35))
        d.rounded_rectangle((CX - 360, y0, CX + 360, y0 + h), 26, fill=WHITE)
        d.rounded_rectangle((CX - 360, y0, CX + 360, y0 + 26), 13, fill=RED)
    overlay(fr, f, a)
    txt(fr, "DA FARE", 52, y0 + 92, a, color=RED)
    for i, (_, s) in enumerate(LIST):
        k = ease(n_shown - i)
        if k <= 0:
            continue
        y = y0 + 190 + i * 112
        ck = ease((t - t_check0 - i * .35) / .3) if checks else 0
        def box(d, y=y, ck=ck):
            d.rounded_rectangle((CX - 300, y - 30, CX - 240, y + 30), 10, outline=ANTH, width=6,
                                fill=GREEN if ck > .5 else None)
            if ck > 0:
                pts = [(CX - 288, y), (CX - 274, y + 16), (CX - 250, y - 18)]
                d.line(pts[:2] if ck < .5 else pts, fill=WHITE, width=8)
        overlay(fr, box, a * k)
        sp = fit(s, 44, ANTH, bold=True, maxw=500)
        paste(fr, sp, CX - 215 + sp.width / 2, y + 18 * (1 - k), a * k)
        BOXES.append((CX - 215, y - 25, CX - 215 + sp.width, y + 25, s)) if a * k > .5 else None

def sc_problem(t):
    fr = background(t, tint=hex2rgb(RED, 18))
    n = sum(1 for k, _ in LIST if t >= T[k]) + 0.0
    # comparsa morbida dell'ultima voce
    for k, _ in LIST:
        if T[k] <= t < T[k] + .35:
            n = n - 1 + (t - T[k]) / .35
    txt(fr, "MENTRE PENSI", 70, 330, fade(t, T["s4"]), t0=T["s4"], t=t)
    txt(fr, "ALLE DECORAZIONI...", 70, 420, fade(t, T["s4"] + .2), color=RED, t0=T["s4"] + .2, t=t)
    shake = math.sin(t * 30) * 3 * fade(t, T["l5"] + .3)
    todo(fr, t, int(520 + shake), n, a=fade(t, T["s4"] + .1))
    return fr

def sc_urgency(t):
    fr = background(t, tint=hex2rgb(RED, 30))
    d = ImageDraw.Draw(fr)
    t0 = T["s5"]
    days = ["15 NOV", "22 NOV", "29 NOV", "6 DIC", "13 DIC", "20 DIC"]
    i = min(len(days) - 1, int(max(0, t - t0 - .3) / .75))
    flip = ((t - t0 - .3) % .75) / .75
    # calendario
    cx, cy = CX, 760
    d.rounded_rectangle((cx - 230, cy - 210, cx + 230, cy + 210), 30, fill=WHITE)
    d.rounded_rectangle((cx - 230, cy - 210, cx + 230, cy - 110), 30, fill=RED)
    d.rectangle((cx - 230, cy - 140, cx + 230, cy - 110), fill=RED)
    for rx in (-120, 120):
        d.rounded_rectangle((cx + rx - 14, cy - 240, cx + rx + 14, cy - 180), 10, fill=ANTH)
    day, mon = days[i].split()
    txt(fr, mon, 54, cy - 160, 1, color=WHITE)
    sp = text_sprite(day, 190, ANTH if mon == "NOV" else RED)
    sq = 1 - .25 * math.sin(min(1, flip * 3) * math.pi) if i < len(days) - 1 else 1
    sp2 = sp.resize((sp.width, max(1, int(sp.height * sq))))
    paste(fr, sp2, cx, cy + 50, 1)
    BOXES.append((cx - sp.width / 2, cy - 60, cx + sp.width / 2, cy + 150, day))
    # barra del tempo che si accorcia
    p = 1 - ease((t - t0) / 4.6) * .88
    txt(fr, "TEMPO PER ORGANIZZARTI", 40, 1060, 1, bold=True)
    def bar(d):
        d.rounded_rectangle((CX - 340, 1100, CX + 340, 1150), 25, fill=hex2rgb(ANTH, 40))
        col = GREEN if p > .6 else (GOLD if p > .3 else RED)
        d.rounded_rectangle((CX - 340, 1100, CX - 340 + 680 * p, 1150), 25, fill=col)
    overlay(fr, bar, 1)
    # il negozio si riempie
    for k in range(9):
        a = ease((t - t0 - .4 - k * .45) / .3)
        if a > 0:
            px = 150 + (k % 5) * 160 + (k // 5) * 80
            person(d, px, 1430 + (k // 5) * 40, .85, [ORANGE, GREEN, "#2D7DD2", RED, GOLD][k % 5],
                   [RED, GOLD, GREEN][k % 3])
    txt(fr, "IL NEGOZIO SI RIEMPIE", 62, 340, fade(t, t0), t0=t0, t=t)
    hl(fr, "IL TEMPO DIMINUISCE", 62, 450, fade(t, t0 + 1.6), t, t0 + 1.6, RED)
    return fr

def manual_cover(scale=1.0):
    """Copertina illustrata segnaposto: sostituibile con quella reale (04_GRAFICHE/copertina_manuale.png)."""
    real = os.path.join(ROOT, "04_GRAFICHE", "copertina_manuale_REALE.png")
    w, h = 520, 700
    if os.path.exists(real):
        im = Image.open(real).convert("RGBA").resize((w, h), Image.LANCZOS)
    else:
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=RED)
        d.rounded_rectangle((0, 0, 34, h - 1), 16, fill="#9E1F1F")
        d.rectangle((w / 2 - 14, 0, w / 2 + 14, h), fill=GOLD)
        d.rectangle((0, 300, w, 328), fill=GOLD)
        d.ellipse((w / 2 - 60, 254, w / 2 - 4, 330), outline=GOLD, width=14)
        d.ellipse((w / 2 + 4, 254, w / 2 + 60, 330), outline=GOLD, width=14)
        d.rounded_rectangle((60, 380, w - 60, 640), 20, fill=CREAM)
        for i, (s, sz, c) in enumerate([("MANUALE", 56, RED), ("DEL NATALE", 50, ANTH), ("IN NEGOZIO", 50, ANTH)]):
            sp = text_sprite(s, sz, c)
            im.alpha_composite(sp, (int(w / 2 - sp.width / 2), 400 + i * 72))
        sp = text_sprite("Guida pratica", 30, ORANGE, bold=False)
        im.alpha_composite(sp, (int(w / 2 - sp.width / 2), 600 - 10))
        sp = text_sprite("CRISTINA", 30, WHITE)
        im.alpha_composite(sp, (int(w / 2 - sp.width / 2), 120))
    if scale != 1:
        im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    return im

_COVER = {}
def cover(scale):
    k = round(scale, 2)
    if k not in _COVER:
        _COVER[k] = manual_cover(k)
    return _COVER[k]

def sc_panic(t):
    t0 = T["s6"]
    k = ease_out((t - t0) / .25)
    fr = background(t, col=ORANGE, snow=True)
    s = text_sprite("MA NIENTE", 110, WHITE)
    s2 = text_sprite("PANICO!", 150, ANTH)
    z = .6 + .4 * k
    for sp, y in ((s, 760), (s2, 900)):
        sp = sp.resize((int(sp.width * z), int(sp.height * z)))
        paste(fr, sp, CX, y, k)
        BOXES.append((CX - sp.width / 2, y - sp.height / 2, CX + sp.width / 2, y + sp.height / 2, "panico"))
    return fr

def sc_manual(t):
    fr = background(t)
    t0 = T["s7"]
    txt(fr, "PER QUESTO HO CREATO", 56, 330, fade(t, t0, T["s8"] - .1), t0=t0, t=t)
    k = ease_out((t - t0 - .2) / .7)
    cv = cover(.92)
    y = 900 + (1 - k) * 500
    rot = (1 - k) * -8 + math.sin(t * 1.5) * 1.2
    paste(fr, cv.rotate(rot, resample=Image.BICUBIC, expand=True), CX, y, k)
    hl(fr, "IL MANUALE DEL NATALE IN NEGOZIO", 46, 1430, fade(t, t0 + 1.2, T["s8"] - .1), t, t0 + 1.2, RED)
    return fr

FEAT = [("f1", "CALENDARIO OPERATIVO", "cal"), ("f2", "ORGANIZZAZIONE DEL PUNTO VENDITA", "shop"),
        ("f3", "CHECKLIST DA STAMPARE", "check")]

def icon(d, kind, x, y):
    if kind == "cal":
        d.rounded_rectangle((x - 40, y - 36, x + 40, y + 40), 10, fill=WHITE)
        d.rectangle((x - 40, y - 36, x + 40, y - 14), fill=RED)
        for i in range(3):
            for j in range(2):
                d.rectangle((x - 28 + i * 22, y - 4 + j * 20, x - 14 + i * 22, y + 8 + j * 20), fill=ANTH)
    elif kind == "shop":
        d.rectangle((x - 40, y - 40, x + 40, y + 40), fill=WHITE)
        for yy in (-10, 22):
            d.rectangle((x - 40, y + yy, x + 40, y + yy + 6), fill=ANTH)
        for i, c in enumerate((RED, GREEN, GOLD)):
            d.rectangle((x - 32 + i * 24, y - 32, x - 14 + i * 24, y - 10), fill=c)
            d.rectangle((x - 32 + i * 24, y + 2, x - 14 + i * 24, y + 22), fill=c)
    else:
        d.rounded_rectangle((x - 34, y - 42, x + 34, y + 42), 8, fill=WHITE)
        for j in range(3):
            d.rectangle((x - 24, y - 26 + j * 24, x - 12, y - 14 + j * 24), fill=GREEN)
            d.rectangle((x - 4, y - 23 + j * 24, x + 24, y - 17 + j * 24), fill=ANTH)

def sc_guide(t):
    fr = background(t)
    t0 = T["s8"]
    txt(fr, "UNA GUIDA PRATICA", 72, 330, fade(t, t0), t0=t0, t=t)
    hl(fr, "PASSO DOPO PASSO", 60, 440, fade(t, T["s8b"]), t, T["s8b"], ORANGE)
    # copertina piccola che si sposta in alto a sinistra? resta al centro, dietro alle schede
    for i, (k, s, ic) in enumerate(FEAT):
        a = fade(t, T[k], d=.3)
        if a <= 0:
            continue
        y = 640 + i * 260 + 30 * (1 - ease((t - T[k]) / .4))
        def card(d, y=y, ic=ic):
            d.rounded_rectangle((CX - 395, y - 105, CX + 395, y + 105), 30, fill=WHITE)
            d.rounded_rectangle((CX - 395, y - 105, CX - 380, y + 105), 8, fill=[RED, GREEN, GOLD][i])
            d.ellipse((CX - 360, y - 70, CX - 220, y + 70), fill=[RED, GREEN, GOLD][i])
            icon(d, ic, CX - 290, y)
        overlay(fr, card, a)
        words = s.split()
        if len(s) > 22:  # due righe
            mid = len(words) // 2
            l1, l2 = " ".join(words[:mid]), " ".join(words[mid:])
            for j, ln in enumerate((l1, l2)):
                sp = fit(ln, 44, maxw=560)
                paste(fr, sp, CX - 190 + sp.width / 2, y - 28 + j * 58, a)
                BOXES.append((CX - 190, y - 55, CX - 190 + sp.width, y + 60, ln)) if a > .5 else None
        else:
            sp = fit(s, 44, maxw=560)
            paste(fr, sp, CX - 190 + sp.width / 2, y, a)
            BOXES.append((CX - 190, y - 25, CX - 190 + sp.width, y + 25, s)) if a > .5 else None
    # pagine illustrate prima delle schede
    a = fade(t, t0 + .2, T["f1"] - .2)
    if a > 0:
        def pages(d):
            for i in range(3):
                x = CX - 260 + i * 260
                yy = 980 + math.sin(t * 2 + i) * 8
                d.rounded_rectangle((x - 110, yy - 160, x + 110, yy + 160), 14, fill=WHITE, outline=hex2rgb(ANTH, 60), width=3)
                d.rectangle((x - 80, yy - 130, x + 80, yy - 110), fill=[RED, GREEN, GOLD][i])
                for j in range(6):
                    d.rectangle((x - 80, yy - 80 + j * 30, x + (80 if j % 3 else 20), yy - 70 + j * 30), fill=hex2rgb(ANTH, 90))
        overlay(fr, pages, a)
    return fr

def sc_novembre(t):
    fr = background(t)
    t0 = T["s9"]
    txt(fr, "ANCHE SE SEI", 72, 360, fade(t, t0), t0=t0, t=t)
    txt(fr, "GIÀ A NOVEMBRE", 80, 460, fade(t, t0 + .2), color=RED, t0=t0 + .2, t=t)
    d = ImageDraw.Draw(fr)
    cx, cy = CX, 900
    a = fade(t, t0 + .1)
    def cal(d):
        d.rounded_rectangle((cx - 300, cy - 230, cx + 300, cy + 250), 30, fill=WHITE)
        d.rounded_rectangle((cx - 300, cy - 230, cx + 300, cy - 140), 30, fill=RED)
        d.rectangle((cx - 300, cy - 160, cx + 300, cy - 140), fill=RED)
        for r in range(5):
            for c in range(7):
                n = r * 7 + c + 1
                if n > 30:
                    continue
                x, y = cx - 255 + c * 85, cy - 100 + r * 70
                past = n < 7
                d.rounded_rectangle((x - 30, y - 24, x + 30, y + 24), 8, fill=hex2rgb(ANTH, 50) if past else hex2rgb(GREEN, 70))
    overlay(fr, cal, a)
    txt(fr, "NOVEMBRE", 46, cy - 185, a, color=WHITE)
    hl(fr, "PUOI ANCORA ORGANIZZARTI!", 52, 1300, fade(t, t0 + 1.4), t, t0 + 1.4, GREEN)
    return fr

def sc_today(t):
    fr = background(t)
    t0 = T["s10"]
    txt(fr, "NON ASPETTARE", 72, 330, fade(t, t0, T["s11"] - .1), t0=t0, t=t)
    txt(fr, "L'ULTIMO MOMENTO", 72, 425, fade(t, t0 + .2, T["s11"] - .1), color=RED, t0=t0 + .2, t=t)
    hl(fr, "PREPARATI OGGI", 76, 340, fade(t, T["s11"]), t, T["s11"], ORANGE)
    txt(fr, "PER ACCOGLIERE AL MEGLIO", 46, 450, fade(t, T["s11"] + .5), t0=T["s11"] + .5, t=t, bold=False)
    txt(fr, "I TUOI CLIENTI DOMANI", 50, 510, fade(t, T["s11"] + .7), t0=T["s11"] + .7, t=t)
    todo(fr, t, 600, 5, checks=1, a=fade(t, t0 + .1), t_check0=t0 + .5)
    return fr

def sc_cta(t):
    fr = background(t)
    t0 = T["s12"]
    cv = cover(.6)
    k = ease_out((t - t0) / .5)
    paste(fr, cv, CX, 640 + (1 - k) * 80, k)
    txt(fr, "TROVI IL MANUALE", 64, 990, fade(t, t0 + .2), t0=t0 + .2, t=t)
    txt(fr, "SUL MIO SITO", 64, 1075, fade(t, t0 + .35), t0=t0 + .35, t=t)
    hl(fr, "cristinaonline.it", 60, 1195, fade(t, t0 + .6), t, t0 + .6, ORANGE)
    a = fade(t, t0 + 1.2)
    overlay(fr, lambda d: d.rounded_rectangle((CX - 240, 1290, CX + 240, 1380), 45, fill=ANTH), a)
    txt(fr, "LINK IN BIO", 46, 1335, a, color=WHITE)
    txt(fr, "@cristina.visual.merchandiser", 36, 1450, fade(t, t0 + 1.4), color=ORANGE)
    return fr

SCENES = [(0, sc_hook), (T["s4"], sc_problem), (T["s5"], sc_urgency), (T["s6"], sc_panic), (T["s7"], sc_manual),
          (T["s8"], sc_guide), (T["s9"], sc_novembre), (T["s10"], sc_today), (T["s12"], sc_cta)]

def frame_at(t):
    BOXES.clear()
    idx = max(i for i, (s, _) in enumerate(SCENES) if t >= s)
    fr = SCENES[idx][1](t)
    st = SCENES[idx][0]
    if idx and t - st < .25 and SCENES[idx][1] is not sc_panic:  # dissolvenza d'ingresso
        prev = SCENES[idx - 1][1](t)
        fr = Image.blend(prev, fr, ease((t - st) / .25))
    if t > DUR - .7:
        fr.alpha_composite(Image.new("RGBA", (W, H), hex2rgb(CREAM, int(255 * ease((t - DUR + .7) / .7)))))
    return fr.convert("RGB")

def check_safe():
    bad = 0
    for i in range(int(DUR * FPS)):
        frame_at(i / FPS)
        for x0, y0, x1, y1, s in BOXES:
            if x0 < SAFE[0] or y0 < SAFE[1] or x1 > SAFE[2] or y1 > SAFE[3]:
                bad += 1
                print(f"t={i / FPS:.2f} fuori area: '{s}' ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
                break
    print("OK area sicura" if not bad else f"{bad} fotogrammi con testo fuori area")

def guides(img):
    """Sovrappone l'area sicura (solo per lo storyboard)."""
    im = img.convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle((0, 0, W, SAFE[1]), fill=(0, 0, 0, 70)); d.rectangle((0, SAFE[3], W, H), fill=(0, 0, 0, 70))
    d.rectangle((0, SAFE[1], SAFE[0], SAFE[3]), fill=(0, 0, 0, 70)); d.rectangle((SAFE[2], SAFE[1], W, SAFE[3]), fill=(0, 0, 0, 70))
    d.rectangle(SAFE, outline=(0, 200, 255, 255), width=4)
    im.alpha_composite(ov)
    return im.convert("RGB")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "still":
        im = frame_at(float(sys.argv[2]))
        (guides(im) if len(sys.argv) > 4 else im).save(sys.argv[3])
    elif cmd == "frames":
        out = sys.argv[2]; os.makedirs(out, exist_ok=True)
        t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0
        t1 = float(sys.argv[4]) if len(sys.argv) > 4 else DUR
        for i in range(int(t0 * FPS), int(t1 * FPS)):
            frame_at(i / FPS).save(os.path.join(out, f"f{i:04d}.png"), compress_level=1)
    elif cmd == "check":
        check_safe()
    elif cmd == "assets":
        g = os.path.join(ROOT, "04_GRAFICHE"); os.makedirs(g, exist_ok=True)
        manual_cover().save(os.path.join(g, "copertina_manuale_segnaposto.png"))
        os.makedirs(os.path.join(ROOT, "06_EXPORT"), exist_ok=True)
        fr = background(0); paste(fr, cover(1.0), CX, 1000)
        hl(fr, "IL MANUALE DEL NATALE IN NEGOZIO", 46, 330, 1, 9, 0, RED)
        txt(fr, "cristinaonline.it", 50, 1440, 1, color=ORANGE)
        fr.convert("RGB").save(os.path.join(ROOT, "06_EXPORT", "copertina_reel_1080x1920.jpg"), quality=95)
