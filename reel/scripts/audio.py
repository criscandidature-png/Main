"""Genera musica strumentale discreta + effetti sonori sincronizzati (sintesi locale, nessun diritto d'autore)."""
import numpy as np, wave, os
SR, DUR = 48000, 30.0
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "05_AUDIO")
n = int(SR * DUR); t = np.arange(n) / SR
def env(L, a=.005, r=.3):
    x = np.arange(L) / SR; return np.minimum(1, x / a) * np.exp(-x / r)
def note(f, L, r=.4, h=(1, .5, .25)):
    x = np.arange(L) / SR; return sum(w * np.sin(2*np.pi*f*(k+1)*x) for k, w in enumerate(h)) * env(L, .01, r)
def add(buf, sig, at, g):
    i = int(at * SR)
    if i >= n: return
    j = min(n, i + len(sig)); buf[i:j] += sig[:j-i] * g
# --- musica: 100 bpm, Am-F-C-G, pad + arpeggio pizzicato
mus = np.zeros(n); beat = 60/100
chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [130.8, 196, 261.6], [196, 246.9, 293.7]]
for bar in range(int(DUR / (4*beat)) + 1):
    ch = chords[bar % 4]; t0 = bar * 4 * beat
    for f in ch: add(mus, note(f/2, int(SR*4*beat), 1.6, (1, .3)), t0, .10)
    for k in range(8):
        add(mus, note(ch[k % 3]*2, int(SR*.5), .18, (1, .2)), t0 + k*beat/2, .07)
    add(mus, note(55 if bar % 4 == 0 else ch[0]/4, int(SR*.6), .25, (1,)), t0, .18)
mus *= np.minimum(1, t/1.0) * np.minimum(1, (DUR - t)/1.5)
# --- effetti
sfx = np.zeros(n); rng = np.random.default_rng(1)
def pop(f=880): L = int(SR*.12); return note(f, L, .04, (1, .3))
def whoosh(d=.5):
    L = int(SR*d); x = rng.standard_normal(L); x = np.convolve(x, np.ones(30)/30, 'same')
    return x * np.sin(np.linspace(0, np.pi, L))**2 * 3
def chime(): return sum(note(f, int(SR*1.2), .5, (1, .2)) for f in (1046.5, 1318.5, 1568))/3
def click(): return note(1500, int(SR*.05), .015, (1,))
for at, s, g in [(0, whoosh(.7), .25), (.3, pop(660), .5), (1.4, pop(880), .5), (1.9, whoosh(.35), .3),
                 (4.0, pop(660), .4), (4.5, pop(990), .45), (5.9, pop(990), .45), (7.3, pop(990), .45),
                 (9.0, pop(660), .5), (9.8, pop(880), .4), (10.4, whoosh(1.2), .2), (15.0, chime(), .35),
                 (16.2, pop(990), .45), (18.0, pop(990), .45), (19.8, pop(990), .45), (21.8, whoosh(.5), .25),
                 (22.8, whoosh(.4), .3), (26.0, pop(660), .45), (27.2, whoosh(.35), .3), (27.9, chime(), .3)]:
    add(sfx, s, at, g)
for sh in range(4):  # "clic" quando ogni gruppo arriva in posizione
    add(sfx, click(), 10.4 + 4.8*(sh*.12 + .5) + .1, .4)
for name, buf in (("musica.wav", mus), ("sfx.wav", sfx), ("mix.wav", mus*.8 + sfx)):
    b = buf / max(1, np.abs(buf).max()) * .9 if name == "mix.wav" else np.clip(buf, -1, 1)
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((b*32767).astype(np.int16).tobytes())
