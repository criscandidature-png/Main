"""Musica (tesa fino a 'Ma niente panico!', poi luminosa con campanelli) + effetti, sotto la voce."""
import numpy as np, wave, os
SR, DUR, CUT = 48000, 46.6, 21.0
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "05_AUDIO")
n = int(SR * DUR); t = np.arange(n) / SR
def env(L, a=.005, r=.3):
    x = np.arange(L) / SR; return np.minimum(1, x / a) * np.exp(-x / r)
def note(f, L, r=.4, h=(1, .5, .25)):
    x = np.arange(L) / SR; return sum(w * np.sin(2*np.pi*f*(k+1)*x) for k, w in enumerate(h)) * env(L, .01, r)
def add(buf, sig, at, g):
    i = int(at * SR)
    if i >= n or i < 0: return
    j = min(n, i + len(sig)); buf[i:j] += sig[:j-i] * g
mus = np.zeros(n)
# parte 1: tensione (Am, pulsazione di ottavi in accelerazione, 112 bpm)
b = 60/112
for k in range(int(CUT / (b/2))):
    at = k * b / 2
    if at > CUT - .4: break
    root = [110, 110, 98, 104][int(at / (4*b)) % 4]
    add(mus, note(root, int(SR*.25), .09, (1, .4)), at, .22)
    if k % 2 == 0: add(mus, note(root*4, int(SR*.2), .06, (1,)), at, .05 + .05*at/CUT)
    if k % 8 == 0: add(mus, note(root*2, int(SR*2), 1.0, (1, .3)), at, .06)
# tic-tac dell'orologio nella scena urgenza
for k in range(int((CUT - 16) / .5)): add(mus, note(2400, int(SR*.03), .01, (1,)), 16 + k*.5, .08)
# parte 2: maggiore, luminosa, con campanelli (100 bpm)
b = 60/100
ch = [[261.6, 329.6, 392], [220, 261.6, 329.6], [174.6, 220, 261.6], [196, 246.9, 293.7]]
bar = 0; at = CUT + .15
while at < DUR:
    c = ch[bar % 4]
    for f in c: add(mus, note(f/2, int(SR*4*b), 1.6, (1, .3)), at, .09)
    add(mus, note(c[0]/4, int(SR*.6), .3, (1,)), at, .2)
    for k in range(8): add(mus, note(c[[0, 1, 2, 1][k % 4]]*4, int(SR*.6), .25, (1, .1, .3)), at + k*b/2, .045)
    bar += 1; at += 4*b
fadein = np.clip((t - CUT) / .1, 0, 1); fadeout = np.clip((CUT - .05 - t) / .3, 0, 1)
mus *= np.where(t < CUT, fadeout, fadein) * np.minimum(1, (DUR - t) / 1.2) * np.minimum(1, t / .3)
sfx = np.zeros(n); rng = np.random.default_rng(1)
def pop(f=880): return note(f, int(SR*.12), .04, (1, .3))
def whoosh(d=.5):
    L = int(SR*d); x = np.convolve(rng.standard_normal(L), np.ones(30)/30, 'same')
    return x * np.sin(np.linspace(0, np.pi, L))**2 * 3
def chime(): return sum(note(f, int(SR*1.4), .6, (1, .2)) for f in (1046.5, 1318.5, 1568, 2093))/4
for at in (7.35, 9.5, 11.35, 12.15, 12.75): add(sfx, pop(760), at, .35)
for k in range(6): add(sfx, whoosh(.18), 16.25 + k*.75, .15)
add(sfx, whoosh(.5), 20.6, .3); add(sfx, chime(), 21.0, .4)
add(sfx, whoosh(.6), 22.4, .25); add(sfx, chime(), 23.1, .25)
for at in (28.95, 30.35, 32.35): add(sfx, pop(990), at, .35)
for k in range(5): add(sfx, pop(1180), 37.8 + k*.35, .3)
add(sfx, chime(), 43.6, .25)
def save(name, buf):
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(buf, -1, 1)*32767).astype(np.int16).tobytes())
save("musica.wav", mus * .8); save("sfx.wav", sfx)
