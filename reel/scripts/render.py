"""Reel 'Uno scaffale pieno non è sempre uno scaffale efficace.'
Renderer 2D offline: genera asset PNG separati e i fotogrammi del video (1080x1920, 30 fps).

Uso:
  python render.py assets            -> esporta asset separati
  python render.py still T OUT.png   -> fotogramma al tempo T (secondi)
  python render.py frames DIR [T0 T1] -> sequenza PNG per ffmpeg
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 30.0
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ORANGE, CREAM, ANTH, WHITE = "#F47721", "#FFF3E6", "#222222", "#FFFFFF"
FB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
FR = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"

CATS = {  # categoria: (nome, colori)
    "succhi": ("SUCCHI", ["#3FA34D", "#57B85F", "#2E8B3E"]),
    "conserve": ("CONSERVE", ["#C8443A", "#D9604F", "#A8322B"]),
    "confez": ("CONFEZIONATI", ["#2D7DD2", "#4A93E0", "#1F63AD"]),
    "cereali": ("CEREALI", ["#E9B530", "#F2C657", "#C9961C"]),
}

# ---------------- utilità ----------------
def ease(x):
    x = max(0.0, min(1.0, x))
    return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2

def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3

def fade(t, t_in, t_out=None, d=0.35):
    a = ease((t - t_in) / d)
    if t_out is not None:
        a *= 1 - ease((t - t_out) / d)
    return a

def hex2rgb(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)

_font = {}
def font(path, size):
    k = (path, size)
    if k not in _font:
        _font[k] = ImageFont.truetype(path, size)
    return _font[k]

_txt = {}
def text_sprite(s, size, color=ANTH, bold=True):
    k = (s, size, color, bold)
    if k not in _txt:
        f = font(FB if bold else FR, size)
        l, t, r, b = f.getbbox(s)
        im = Image.new("RGBA", (r - l + 8, b - t + 8), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((4 - l, 4 - t), s, font=f, fill=color)
        _txt[k] = im
    return _txt[k]

def paste(frame, sprite, x, y, alpha=1.0, anchor="c"):
    if alpha <= 0.01:
        return
    if alpha < 1:
        sprite = sprite.copy()
        sprite.putalpha(sprite.getchannel("A").point(lambda v: int(v * alpha)))
    w, h = sprite.size
    if anchor == "c":
        x, y = x - w // 2, y - h // 2
    elif anchor == "l":
        y = y - h // 2
    frame.alpha_composite(sprite, (int(x), int(y)))

def put_text(frame, s, size, x, y, alpha, color=ANTH, bold=True, rise=24, prog=1.0):
    paste(frame, text_sprite(s, size, color, bold), x, y + rise * (1 - prog), alpha)

def overlay(frame, draw_fn, alpha):
    if alpha <= 0.01:
        return
    ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(ov))
    if alpha < 1:
        ov.putalpha(ov.getchannel("A").point(lambda v: int(v * alpha)))
    frame.alpha_composite(ov)

# ---------------- scaffale ----------------
SX0, SX1 = 110, 970
BOARDS = [850, 1050, 1250, 1450]  # y del piano di ogni ripiano
SHELF_TOP = 650

def make_shelf():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((SX0 - 30, SHELF_TOP - 40, SX1 + 30, BOARDS[-1] + 70), 18, fill="#3A3A3A")
    d.rectangle((SX0, SHELF_TOP, SX1, BOARDS[-1]), fill="#F6EBDD")
    d.rectangle((SX0, SHELF_TOP, SX1, SHELF_TOP + 14), fill="#E6D6C3")
    d.rounded_rectangle((SX0 - 30, SHELF_TOP - 70, SX1 + 30, SHELF_TOP - 30), 10, fill=ORANGE)
    for by in BOARDS:
        d.rectangle((SX0, by - 200 + 6, SX1, by - 200 + 18), fill=(0, 0, 0, 0)) if False else None
        d.rectangle((SX0 - 6, by, SX1 + 6, by + 22), fill="#DADADA")
        d.rectangle((SX0 - 6, by + 22, SX1 + 6, by + 34), fill="#BDBDBD")
        d.rectangle((SX0, by - 10, SX1, by), fill=(0, 0, 0, 25))
    d.rectangle((SX0 - 30, BOARDS[-1] + 34, SX1 + 30, BOARDS[-1] + 70), fill="#2B2B2B")
    return im

# ---------------- prodotti ----------------
def make_product(cat, shade):
    col = CATS[cat][1][shade]
    if cat == "succhi":  # brick con tappo
        w, h = 82, 150
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rectangle((26, 0, 56, 14), fill=WHITE, outline="#CFCFCF")
        d.polygon([(4, 34), (20, 12), (62, 12), (78, 34)], fill=col)
        d.rounded_rectangle((4, 32, 78, h - 1), 6, fill=col)
        d.ellipse((18, 62, 64, 108), fill=WHITE)
        d.ellipse((28, 72, 54, 98), fill=hex2rgb("#F47721") if shade == 0 else "#F2C14E")
        d.rectangle((4, h - 26, 78, h - 18), fill=(255, 255, 255, 90))
    elif cat == "conserve":  # barattolo
        w, h = 92, 104
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((10, 0, 82, 20), 5, fill="#444444")
        d.rounded_rectangle((4, 18, 88, h - 1), 16, fill=col)
        d.rounded_rectangle((12, 44, 80, 84), 6, fill=CREAM)
        d.rectangle((22, 58, 70, 66), fill=col)
        d.ellipse((14, 26, 26, 38), fill=(255, 255, 255, 110))
    elif cat == "confez":  # scatola bassa
        w, h = 112, 112
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((2, 2, w - 2, h - 2), 6, fill=col)
        d.rectangle((2, 30, w - 2, 46), fill=WHITE)
        d.rounded_rectangle((18, 58, w - 18, 96), 18, fill=(255, 255, 255, 70))
        d.rectangle((2, 2, w - 2, 10), fill=(0, 0, 0, 40))
    else:  # cereali: scatola alta
        w, h = 104, 170
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((2, 2, w - 2, h - 2), 6, fill=col)
        d.rectangle((2, 16, w - 2, 44), fill=ANTH)
        d.rectangle((16, 26, w - 16, 34), fill=CREAM)
        d.pieslice((16, 74, w - 16, 144), 0, 180, fill=WHITE)
        for cx, cy in ((34, 100), (52, 94), (70, 102), (44, 108), (62, 108)):
            d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill="#C9961C")
    return im

# 4 categorie x 6 = 24 prodotti (stessi prodotti in PRIMA e DOPO)
PRODUCTS = []
for cat in ["cereali", "succhi", "conserve", "confez"]:
    for i in range(6):
        PRODUCTS.append({"cat": cat, "shade": [0, 0, 1, 1, 2, 2][i], "id": len(PRODUCTS)})

SLOT_W = (SX1 - SX0 - 40) / 6
def slot_x(i):
    return SX0 + 20 + SLOT_W * (i + 0.5)

# DOPO: un ripiano per categoria, allineati, sfumature ordinate
SHELF_OF = {"cereali": 0, "succhi": 1, "conserve": 2, "confez": 3}
for p in PRODUCTS:
    k = p["id"] % 6
    p["after"] = (slot_x(k), BOARDS[SHELF_OF[p["cat"]]], 0.0)

# PRIMA: stesse confezioni mescolate, disallineate, alcune inclinate
rng = random.Random(7)
order = list(range(24)); rng.shuffle(order)
for slot, pid in enumerate(order):
    sh, k = divmod(slot, 6)
    jitter = rng.uniform(-16, 16)
    rot = rng.choice([0, 0, 0, rng.uniform(-9, 9)])
    PRODUCTS[pid]["before"] = (slot_x(k) + jitter, BOARDS[sh], rot)

SPRITES = {}
def sprite(p):
    k = (p["cat"], p["shade"])
    if k not in SPRITES:
        SPRITES[k] = make_product(*k)
    return SPRITES[k]

def draw_products(layer, prog):
    """prog 0 = PRIMA, 1 = DOPO. Ogni prodotto ha il suo ritardo per un movimento progressivo."""
    for p in PRODUCTS:
        bx, by, br = p["before"]; ax, ay, ar = p["after"]
        delay = SHELF_OF[p["cat"]] * 0.12 + (p["id"] % 6) * 0.025
        q = 1.0 if prog >= 1 else ease((prog - delay) / 0.5)
        x = bx + (ax - bx) * q
        y = by + (ay - by) * q - math.sin(q * math.pi) * 40  # leggero arco
        r = br + (ar - br) * q
        sp = sprite(p)
        if abs(r) > 0.2:
            sp = sp.rotate(r, resample=Image.BICUBIC, expand=True)
        w, h = sp.size
        layer.alpha_composite(sp, (int(x - w / 2), int(y - h)))

SHELF = None
def shelf_layer(prog, tags=0.0):
    global SHELF
    if SHELF is None:
        SHELF = make_shelf()
    im = SHELF.copy()
    draw_products(im, prog)
    if tags > 0.01:  # cartellini categoria sul bordo dei ripiani
        for cat, sh in SHELF_OF.items():
            s = text_sprite(CATS[cat][0], 26, WHITE)
            tag = Image.new("RGBA", (s.width + 24, s.height + 8), hex2rgb(CATS[cat][1][2]))
            tag.alpha_composite(s, (12, 4))
            paste(im, tag, SX0 + 10, BOARDS[sh] + 12, tags, anchor="tl") if False else \
                paste(im, tag, SX0 + 8 + tag.width / 2, BOARDS[sh] + 17, tags)
    return im

# ---------------- grafiche ----------------
def background(t, deco=1.0):
    im = Image.new("RGBA", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    o = math.sin(t * 0.8) * 12
    d.ellipse((-220, -200 + o, 260, 280 + o), fill=hex2rgb(ORANGE, int(60 * deco)))
    d.ellipse((860, 1640 - o, 1300, 2080 - o), fill=hex2rgb(ORANGE, int(60 * deco)))
    for i in range(5):
        d.ellipse((930 + i * 26, 210, 942 + i * 26, 222), fill=hex2rgb(ORANGE, int(200 * deco)))
    return im

def brush(d, x0, y0, x1, y1, prog, col=ORANGE):
    """Pennellata con bordi irregolari che si allunga da sinistra."""
    if prog <= 0:
        return
    xe = x0 + (x1 - x0) * prog
    rng2 = random.Random(3)
    top = [(x0 + (xe - x0) * i / 12, y0 + rng2.uniform(-6, 6)) for i in range(13)]
    bot = [(x0 + (xe - x0) * i / 12, y1 + rng2.uniform(-6, 6)) for i in range(12, -1, -1)]
    d.polygon(top + [(xe + 12, (y0 + y1) / 2)] + bot + [(x0 - 12, (y0 + y1) / 2)], fill=col)

def ring(d, cx, cy, rx, ry, prog, width=8, col=ORANGE):
    if prog <= 0:
        return
    d.arc((cx - rx, cy - ry, cx + rx, cy + ry), -90, -90 + 360 * prog, fill=col, width=width)

def badge(frame, n, x, y, a):
    def f(d):
        d.ellipse((x - 28, y - 28, x + 28, y + 28), fill=ORANGE)
    overlay(frame, f, a)
    paste(frame, text_sprite(str(n), 32, WHITE), x, y, a)

def arrow(d, x0, y0, x1, y1, prog, width=10, col=ORANGE):
    if prog <= 0:
        return
    xe, ye = x0 + (x1 - x0) * prog, y0 + (y1 - y0) * prog
    d.line((x0, y0, xe, ye), fill=col, width=width)
    ang = math.atan2(ye - y0, xe - x0)
    L = 34
    d.polygon([(xe + math.cos(ang) * 10, ye + math.sin(ang) * 10),
               (xe - L * math.cos(ang - .5), ye - L * math.sin(ang - .5)),
               (xe - L * math.cos(ang + .5), ye - L * math.sin(ang + .5))], fill=col)

def label_box(frame, s, x, y, a, size=34, prog=1.0):
    sp = text_sprite(s, size, WHITE)
    box = Image.new("RGBA", (sp.width + 40, sp.height + 22), (0, 0, 0, 0))
    ImageDraw.Draw(box).rounded_rectangle((0, 0, box.width - 1, box.height - 1), 14, fill=ANTH)
    box.alpha_composite(sp, (20, 11))
    paste(frame, box, x, y + 20 * (1 - prog), a)

# ---------------- scene ----------------
def scene_shelf(t):
    """Scene 1-4: lo scaffale resta fermo, cambiano testi e indicatori."""
    fr = background(t)
    prog = (t - 10.4) / 4.8 if t > 10.4 else 0.0
    prog = min(prog, 1.0)
    tags = fade(t, 15.0, d=0.6)
    sh = shelf_layer(prog, tags)
    # Scena 1: ingresso dal basso
    ent = ease_out(t / 0.9)
    dy = (1 - ent) * 260
    fr.alpha_composite(sh, (0, int(dy))) if dy < 1 else fr.alpha_composite(sh.crop((0, 0, W, H - int(dy))), (0, int(dy)))

    # ---- Scena 1 (0-4)
    a = fade(t, 0.3, 3.7)
    put_text(fr, "UNO SCAFFALE PIENO", 84, W / 2, 330, a, prog=ease((t - .3) / .5))
    a2 = fade(t, 1.4, 3.7)
    bp = ease((t - 1.9) / 0.6)
    s1 = text_sprite("È DAVVERO ", 84); s2 = text_sprite("EFFICACE?", 84)
    tw = s1.width + s2.width; x0 = W / 2 - tw / 2
    yy = 460 + 24 * (1 - ease((t - 1.4) / .5))
    overlay(fr, lambda d: brush(d, x0 + s1.width - 6, yy - 52, x0 + tw + 4, yy + 52, bp), a2)
    paste(fr, s1, x0 + s1.width / 2, yy, a2)
    paste(fr, text_sprite("EFFICACE?", 84, ANTH if bp < .5 else WHITE), x0 + s1.width + s2.width / 2, yy, a2)

    # ---- Scena 2 (4-9)
    a = fade(t, 4.0, 8.75)
    put_text(fr, "COSA NON FUNZIONA?", 72, W / 2, 310, a, prog=ease((t - 4) / .5))
    items = [  # (testo, centro anello, raggi, posizione etichetta)
        ("CATEGORIE POCO CHIARE", (W / 2, BOARDS[0] - 90), (430, 120), 420),
        ("GERARCHIA VISIVA DEBOLE", (W / 2, BOARDS[1] - 90), (430, 115), 482),
        ("PRODOTTI DIFFICILI DA TROVARE", (720, BOARDS[3] - 70), (150, 100), 544),
    ]
    for i, (s, (cx, cy), (rx, ry), ly) in enumerate(items):
        ti = 4.5 + i * 1.4
        ai = fade(t, ti, 8.75)
        overlay(fr, lambda d, cx=cx, cy=cy, rx=rx, ry=ry, ti=ti: ring(d, cx, cy, rx, ry, ease((t - ti) / .6)), ai if t < ti + 1.35 or i == 2 else ai * 0.35)
        badge(fr, i + 1, cx - rx + 10, cy - ry + 10, ai)
        sp = text_sprite(s, 38)
        paste(fr, sp, 200 + sp.width / 2, ly + 16 * (1 - ease((t - ti) / .4)), ai)
        badge(fr, i + 1, 150, ly, ai)
    # Scena 2: piccolo zoom sull'ultimo punto evitato: si usa la lente
    if 7.3 <= t < 8.9:
        a3 = fade(t, 7.5, 8.75)
        overlay(fr, lambda d: [d.line((720 + 110, BOARDS[3] - 70 + 70, 900, BOARDS[3] + 60), fill=ORANGE, width=12)], a3)

    # ---- Scena 3 (9-16)
    a = fade(t, 9.0, 15.6)
    put_text(fr, "LA SOLUZIONE?", 84, W / 2, 330, a, color=ORANGE, prog=ease((t - 9) / .5))
    a = fade(t, 9.8, 15.6)
    put_text(fr, "UN'ESPOSIZIONE", 64, W / 2, 445, a, prog=ease((t - 9.8) / .5))
    put_text(fr, "PIÙ ORGANIZZATA.", 64, W / 2, 525, a, prog=ease((t - 9.9) / .5))

    # ---- Scena 4 (16-22)
    msgs = ["RAGGRUPPA PER CATEGORIA", "ALLINEA LE CONFEZIONI", "CREA UNA GERARCHIA VISIVA"]
    for i, s in enumerate(msgs):
        ti = 16.2 + i * 1.8
        ai = fade(t, ti, 21.7)
        cur = 1.0 if (t < ti + 1.8 or i == 2) else 0.45
        sp = text_sprite(s, 46)
        y = 300 + i * 90 + 20 * (1 - ease((t - ti) / .45))
        paste(fr, sp, 200 + sp.width / 2, y, ai * cur)
        badge(fr, i + 1, 150, y, ai * cur)
        act = fade(t, ti + 0.2, ti + 1.75 if i < 2 else 21.7)
        if i == 0:  # parentesi attorno ai gruppi
            def f(d):
                for b in BOARDS:
                    d.rounded_rectangle((SX0 + 4, b - 186, SX1 - 4, b - 2), 16, outline=ORANGE, width=6)
            overlay(fr, f, act)
        elif i == 1:  # linee di allineamento
            def f(d):
                p = ease((t - ti - .2) / .7)
                for b in BOARDS:
                    for xx in range(SX0, int(SX0 + (SX1 - SX0) * p), 34):
                        d.line((xx, b - 4, xx + 18, b - 4), fill=ORANGE, width=6)
                for k in range(6):
                    x = slot_x(k)
                    d.line((x, SHELF_TOP + 20, x, SHELF_TOP + 20 + (BOARDS[-1] - SHELF_TOP - 20) * p), fill=hex2rgb(ORANGE, 120), width=3)
            overlay(fr, f, act)
        else:  # ripiano all'altezza degli occhi
            def f(d):
                d.rounded_rectangle((SX0 - 14, BOARDS[1] - 196, SX1 + 14, BOARDS[1] + 8), 16, outline=ORANGE, width=10)
            overlay(fr, f, act)
            label_box(fr, "ALTEZZA OCCHI = PRIORITÀ", W / 2, BOARDS[1] + 60, act, 32, ease((t - ti - .2) / .4))
    return fr

def mini(prog, tags):
    sh = shelf_layer(prog, tags).crop((SX0 - 40, SHELF_TOP - 80, SX1 + 40, BOARDS[-1] + 80))
    s = 470 / sh.width
    return sh.resize((470, int(sh.height * s)), Image.LANCZOS)

_MINI = {}
def scene_compare(t):
    fr = background(t)
    if not _MINI:
        _MINI["a"], _MINI["b"] = mini(0, 0), mini(1, 1)
    a = fade(t, 22.0, d=.4)
    put_text(fr, "STESSO SCAFFALE", 60, W / 2, 380, a)
    def bgsplit(d):
        d.rectangle((0, 560, W // 2 - 6, 1560), fill=hex2rgb("#F3E2CF"))
        d.rectangle((W // 2 + 6, 560, W, 1560), fill=hex2rgb("#FFE3CC"))
    overlay(fr, bgsplit, a)
    ma, mb = _MINI["a"], _MINI["b"]
    y = 1080
    paste(fr, ma, W / 4, y + 40 * (1 - ease((t - 22) / .5)), a)
    paste(fr, mb, 3 * W / 4, y + 40 * (1 - ease((t - 22.3) / .5)), fade(t, 22.3, d=.4))
    put_text(fr, "PRIMA", 64, W / 4, 680, a)
    put_text(fr, "DOPO", 64, 3 * W / 4, 680, fade(t, 22.3, d=.4), color=ORANGE)
    overlay(fr, lambda d: arrow(d, W / 2 - 60, 1080, W / 2 + 60, 1080, ease((t - 22.8) / .6), 14), 1)
    put_text(fr, "STESSI PRODOTTI,", 50, W / 2, 1660, fade(t, 23.4), bold=False)
    put_text(fr, "ESPOSIZIONE PIÙ CHIARA", 50, W / 2, 1730, fade(t, 23.6))
    return fr

def scene_end(t):
    fr = background(t)
    lines = ["IL VISUAL", "MERCHANDISING", "NON È SOLO", "DECORAZIONE."]
    for i, s in enumerate(lines):
        ti = 26.1 + i * 0.12
        put_text(fr, s, 78, W / 2, 470 + i * 96, fade(t, ti), prog=ease((t - ti) / .5))
    ti = 27.2
    s = text_sprite("È STRATEGIA ESPOSITIVA.", 70, WHITE)
    a = fade(t, ti)
    overlay(fr, lambda d: brush(d, W / 2 - s.width / 2 - 20, 920, W / 2 + s.width / 2 + 20, 1020, ease((t - ti) / .5)), a)
    paste(fr, s, W / 2, 970, fade(t, ti + .3))
    put_text(fr, "@cristina.visual.merchandiser", 46, W / 2, 1290, fade(t, 27.9), color=ORANGE)
    put_text(fr, "SEGUIMI PER ALTRI", 44, W / 2, 1390, fade(t, 28.2), bold=False)
    put_text(fr, "CONSIGLI SULLA GDO.", 44, W / 2, 1450, fade(t, 28.3))
    return fr

def frame_at(t):
    if t < 21.9:
        fr = scene_shelf(t)
    elif t < 25.9:
        fr = scene_compare(t)
    else:
        fr = scene_end(t)
    # zoom lento nella scena 1
    if t < 4.0:
        z = 1 + 0.035 * ease(t / 4.0)
        big = fr.resize((int(W * z), int(H * z)), Image.BICUBIC)
        ox, oy = (big.width - W) // 2, (big.height - H) // 2
        fr = big.crop((ox, oy, ox + W, oy + H))
    # dissolvenze morbide tra blocchi e chiusura
    for tc in (21.9, 25.9):
        if tc - 0.3 <= t < tc + 0.3:
            k = 1 - abs(t - tc) / 0.3
            veil = Image.new("RGBA", (W, H), hex2rgb(CREAM, int(255 * k)))
            fr.alpha_composite(veil)
    if t > 29.3:
        veil = Image.new("RGBA", (W, H), hex2rgb(CREAM, int(255 * ease((t - 29.3) / .7))))
        fr.alpha_composite(veil)
    return fr.convert("RGB")

# ---------------- CLI ----------------
def export_assets():
    d = lambda n: os.makedirs(os.path.join(ROOT, n), exist_ok=True) or os.path.join(ROOT, n)
    make_shelf().save(os.path.join(d("01_SCAFFALI"), "scaffale_vuoto.png"))
    shelf_layer(0).save(os.path.join(d("01_SCAFFALI"), "scaffale_prima.png"))
    shelf_layer(1, 1).save(os.path.join(d("01_SCAFFALI"), "scaffale_dopo.png"))
    for c in CATS:
        for s in range(3):
            make_product(c, s).save(os.path.join(d("02_PRODOTTI"), f"{c}_{s + 1}.png"))
    for n in ("03_TESTI", "04_GRAFICHE", "05_AUDIO", "06_EXPORT"):
        d(n)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "assets":
        export_assets()
    elif cmd == "still":
        frame_at(float(sys.argv[2])).save(sys.argv[3])
    elif cmd == "frames":
        out = sys.argv[2]; os.makedirs(out, exist_ok=True)
        t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0
        t1 = float(sys.argv[4]) if len(sys.argv) > 4 else DUR
        for i in range(int(t0 * FPS), int(t1 * FPS)):
            frame_at(i / FPS).save(os.path.join(out, f"f{i:04d}.png"), compress_level=1)
