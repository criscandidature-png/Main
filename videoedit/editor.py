#!/usr/bin/env python3
"""Editor video a basso consumo di crediti.

Flusso:  analizza (locale, gratis) -> pianifica (Claude legge SOLO testo) -> renderizza (FFmpeg)

Esempi:
  python editor.py tutto  clip.mp4 --profilo lavoro
  python editor.py tutto  clip.mp4 --profilo personale --formato 9:16 --anteprima
  python editor.py tutto  clip.mp4 --profilo lavoro --senza-ai      # zero crediti
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

QUI = Path(__file__).resolve().parent
CARTELLA_PROFILI = QUI / "profili"
CARTELLA_LAVORO = QUI / "lavori"


# ----------------------------------------------------------------- utilità
def esegui(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"Errore comando:\n{' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r.stdout + r.stderr


def carica_profilo(nome: str) -> dict:
    f = CARTELLA_PROFILI / f"{nome}.yaml"
    if not f.exists():
        disponibili = ", ".join(p.stem for p in CARTELLA_PROFILI.glob("*.yaml"))
        sys.exit(f"Profilo '{nome}' non trovato. Disponibili: {disponibili}")
    return yaml.safe_load(f.read_text(encoding="utf-8"))


def info_video(video: Path) -> dict:
    out = esegui(["ffprobe", "-v", "error", "-print_format", "json",
                  "-show_streams", "-show_format", str(video)])
    d = json.loads(out[out.index("{"):])
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    w, h = int(v["width"]), int(v["height"])
    rot = int(v.get("tags", {}).get("rotate", 0) or 0)
    for sd in v.get("side_data_list", []):
        rot = int(sd.get("rotation", rot) or rot)
    if abs(rot) in (90, 270):
        w, h = h, w
    return {"larghezza": w, "altezza": h, "durata": float(d["format"]["duration"])}


def rileva_formato(info: dict) -> str:
    return "9:16" if info["altezza"] > info["larghezza"] else "16:9"


def cartella_di(video: Path) -> Path:
    c = CARTELLA_LAVORO / video.stem
    c.mkdir(parents=True, exist_ok=True)
    return c


def pulisci(parola: str) -> str:
    return re.sub(r"[^\wàèéìòù']", "", parola.lower())


# ---------------------------------------------------------- 1. ANALISI
def analizza(video: Path, profilo: dict, forza: bool = False) -> dict:
    out = cartella_di(video) / "analisi.json"
    if out.exists() and not forza:
        print(f"[analisi] uso cache {out}")
        return json.loads(out.read_text())

    info = info_video(video)
    print(f"[analisi] {info['larghezza']}x{info['altezza']}, {info['durata']:.1f}s — trascrivo in locale…")
    from faster_whisper import WhisperModel  # import lento: solo se serve

    modello = WhisperModel(os.environ.get("WHISPER_MODEL", "small"), compute_type="int8")
    segs, _ = modello.transcribe(str(video), language=profilo.get("lingua", "it"),
                                 word_timestamps=True, vad_filter=True)
    segmenti = []
    for s in segs:
        parole = [{"w": p.word.strip(), "s": round(p.start, 3), "e": round(p.end, 3)}
                  for p in (s.words or []) if p.word.strip()]
        if parole:
            segmenti.append({"id": len(segmenti), "s": parole[0]["s"], "e": parole[-1]["e"],
                             "testo": s.text.strip(), "parole": parole})
    dati = {"video": str(video), "info": info, "segmenti": segmenti}
    out.write_text(json.dumps(dati, ensure_ascii=False, indent=1))
    print(f"[analisi] {len(segmenti)} frasi trovate -> {out}")
    return dati


# ---------------------------------------------------- 2. PIANIFICAZIONE
def segmenti_ripetuti(segmenti: list[dict], soglia: float) -> set[int]:
    """Frasi rifatte: se una frase somiglia alla successiva, scarta la prima (tieni l'ultima presa)."""
    scarta = set()
    for a, b in zip(segmenti, segmenti[1:]):
        ta, tb = pulisci(a["testo"]), pulisci(b["testo"])
        if not ta:
            continue
        # confronto anche con l'inizio della frase dopo (falsa partenza)
        r = max(difflib.SequenceMatcher(None, ta, tb).ratio(),
                difflib.SequenceMatcher(None, ta, tb[: len(ta)]).ratio())
        if r >= soglia:
            scarta.add(a["id"])
    return scarta


def chiedi_a_claude(segmenti: list[dict], profilo: dict, formato: str, durata_max) -> dict:
    """UNA sola chiamata, solo testo. Restituisce id da tenere + hook."""
    import anthropic

    righe = "\n".join(f"{s['id']}|{s['s']:.1f}-{s['e']:.1f}|{s['testo']}" for s in segmenti)
    sistema = (
        "Sei un montatore video. Ricevi la trascrizione di un video divisa in frasi numerate "
        "(id|inizio-fine secondi|testo). Scegli quali frasi tenere per un montaggio efficace. "
        "Non riscrivere il testo. Rispondi solo usando lo strumento 'piano_montaggio'.\n\n"
        f"STILE ({profilo['nome']}, formato {formato}):\n{profilo['ai']['istruzioni']}\n"
        + (f"Durata finale massima: {durata_max} secondi.\n" if durata_max else "")
    )
    strumento = {
        "name": "piano_montaggio",
        "description": "Piano di montaggio",
        "input_schema": {
            "type": "object",
            "properties": {
                "tieni": {"type": "array", "items": {"type": "integer"},
                          "description": "id delle frasi da tenere"},
                "hook": {"type": ["integer", "null"],
                         "description": "id della frase da mettere in apertura, o null"},
                "note": {"type": "string", "description": "max 1 riga"},
            },
            "required": ["tieni", "hook"],
        },
    }
    client = anthropic.Anthropic()
    r = client.messages.create(
        model=profilo["ai"].get("modello", "claude-haiku-5-5"),
        max_tokens=1024,
        system=[{"type": "text", "text": sistema, "cache_control": {"type": "ephemeral"}}],
        tools=[strumento],
        tool_choice={"type": "tool", "name": "piano_montaggio"},
        messages=[{"role": "user", "content": righe}],
    )
    print(f"[piano] token: input {r.usage.input_tokens}, output {r.usage.output_tokens}")
    return next(b.input for b in r.content if b.type == "tool_use")


def taglia_dentro(seg: dict, cfg: dict) -> list[list[float]]:
    """Dentro una frase: togli riempitivi e pause lunghe, tagliando solo TRA le parole."""
    rif = {pulisci(x) for x in cfg.get("riempitivi", [])} if cfg.get("togli_riempitivi") else set()
    m, pmax = cfg["margine"], cfg["pausa_max"]
    pezzi: list[list[float]] = []
    for p in seg["parole"]:
        if pulisci(p["w"]) in rif:
            continue
        s, e = p["s"] - m, p["e"] + m
        if pezzi and s - pezzi[-1][1] <= pmax:
            pezzi[-1][1] = e
        else:
            pezzi.append([s, e])
    return pezzi


def pianifica(analisi: dict, profilo: dict, formato: str, senza_ai: bool) -> dict:
    cfg = profilo["taglio"]
    fmt = profilo["formati"][formato]
    segmenti = analisi["segmenti"]
    durata_tot = analisi["info"]["durata"]

    scarta = segmenti_ripetuti(segmenti, cfg["soglia_ripetizione"]) if cfg.get("togli_ripetizioni") else set()
    candidati = [s for s in segmenti if s["id"] not in scarta]

    ordine = [s["id"] for s in candidati]
    note = "solo regole (senza AI)"
    if not senza_ai and candidati:
        risposta = chiedi_a_claude(candidati, profilo, formato, fmt.get("durata_max"))
        validi = {s["id"] for s in candidati}
        tieni = sorted(i for i in risposta.get("tieni", []) if i in validi)
        if not tieni:
            print("[piano] ATTENZIONE: Claude non ha tenuto nulla, uso solo le regole.")
        else:
            ordine = tieni
            hook = risposta.get("hook")
            if hook in validi:
                ordine = [hook] + [i for i in tieni if i != hook]
            note = risposta.get("note", "")

    per_id = {s["id"]: s for s in segmenti}
    clip = []
    for i in ordine:
        for s, e in taglia_dentro(per_id[i], cfg):
            clip.append({"seg": i, "s": round(max(0, s), 3), "e": round(min(durata_tot, e), 3)})

    # limite di durata: taglia dalla coda
    if fmt.get("durata_max"):
        tot, tenute = 0.0, []
        for c in clip:
            if tot + (c["e"] - c["s"]) > fmt["durata_max"]:
                break
            tenute.append(c)
            tot += c["e"] - c["s"]
        clip = tenute

    piano = {"profilo": profilo["nome"], "formato": formato, "note": note,
             "scartate_ripetizioni": sorted(scarta), "clip": clip}
    valida_piano(piano, durata_tot)
    durata = sum(c["e"] - c["s"] for c in clip)
    print(f"[piano] {len(clip)} clip, {durata:.1f}s su {durata_tot:.1f}s originali. {note}")
    return piano


def valida_piano(piano: dict, durata_tot: float) -> None:
    if not piano["clip"]:
        sys.exit("Piano vuoto: niente da montare.")
    for c in piano["clip"]:
        if not (0 <= c["s"] < c["e"] <= durata_tot + 0.01):
            sys.exit(f"Clip non valida: {c}")
        if c["e"] - c["s"] < 0.15:
            sys.exit(f"Clip troppo corta (rischio taglio a metà parola): {c}")


# ------------------------------------------------------- 3. RENDERING
def colore_ass(hex_: str) -> str:
    h = hex_.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def tempo_ass(t: float) -> str:
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def crea_sottotitoli(piano: dict, analisi: dict, fmt: dict, dest: Path) -> Path | None:
    st = fmt.get("sottotitoli", {})
    if not st.get("attivi"):
        return None
    allin = {"basso": 2, "centro": 5, "alto": 8}[st.get("posizione", "basso")]
    testa = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {fmt['larghezza']}
PlayResY: {fmt['altezza']}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginL, MarginR, MarginV
Style: S,{st['font']},{st['dimensione']},{colore_ass(st['colore'])},{colore_ass(st['bordo'])},&H00000000,1,{st['spessore_bordo']},0,{allin},60,60,{st['margine_verticale'] if allin != 5 else 0}

[Events]
Format: Layer, Start, End, Style, Text
"""
    per_id = {s["id"]: s for s in analisi["segmenti"]}
    righe, t0 = [], 0.0  # t0 = posizione della clip nel video finale
    n = st.get("parole_per_riga", 5)
    for c in piano["clip"]:
        parole = [p for p in per_id[c["seg"]]["parole"]
                  if p["s"] >= c["s"] - 0.01 and p["e"] <= c["e"] + 0.01]
        for k in range(0, len(parole), n):
            g = parole[k:k + n]
            testo = " ".join(p["w"] for p in g)
            if st.get("maiuscolo"):
                testo = testo.upper()
            a = t0 + g[0]["s"] - c["s"]
            b = t0 + (parole[k + n]["s"] if k + n < len(parole) else g[-1]["e"]) - c["s"]
            righe.append(f"Dialogue: 0,{tempo_ass(a)},{tempo_ass(b)},S,{testo}")
        t0 += c["e"] - c["s"]
    dest.write_text(testa + "\n".join(righe) + "\n", encoding="utf-8")
    return dest


def renderizza(video: Path, analisi: dict, piano: dict, profilo: dict, anteprima: bool) -> Path:
    fmt = dict(profilo["formati"][piano["formato"]])
    W, H = fmt["larghezza"], fmt["altezza"]
    cart = cartella_di(video)
    ass = crea_sottotitoli(piano, analisi, fmt, cart / "sottotitoli.ass")

    zoom = fmt.get("zoom", {})
    filtri, uscite = [], []
    for i, c in enumerate(piano["clip"]):
        z = zoom.get("fattore", 1.0) if zoom.get("attivo") and (c["seg"] % zoom.get("ogni", 2) == 1) else 1.0
        # riempi il formato (scala + ritaglio centrale), con eventuale punch-in
        filtri.append(
            f"[0:v]trim={c['s']}:{c['e']},setpts=PTS-STARTPTS,"
            f"scale={int(W * z)}:{int(H * z)}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},setsar=1,fps=30[v{i}];"
            f"[0:a]atrim={c['s']}:{c['e']},asetpts=PTS-STARTPTS,"
            f"afade=t=in:d=0.02,afade=t=out:st={max(0, c['e'] - c['s'] - 0.02):.3f}:d=0.02[a{i}]"
        )
        uscite.append(f"[v{i}][a{i}]")
    catena_v = "[cv]"
    if ass:
        percorso = str(ass).replace("\\", "/").replace(":", "\\:")
        catena_v = f"[cv]subtitles='{percorso}'"
    if anteprima:
        catena_v += ",scale=-2:480"
    filtri.append(f"{''.join(uscite)}concat=n={len(uscite)}:v=1:a=1[cv][ca]")
    filtri.append(f"{catena_v}[vout]")
    filtri.append(f"[ca]loudnorm=I={profilo['audio']['loudness']}:TP=-1.5:LRA=11[aout]")

    tag = piano["formato"].replace(":", "x")
    out = cart / f"{video.stem}_{profilo['nome']}_{tag}{'_ANTEPRIMA' if anteprima else ''}.mp4"
    script = cart / "filtri.txt"
    script.write_text(";\n".join(filtri))
    print(f"[render] {'anteprima 480p' if anteprima else 'finale'} -> {out}")
    esegui(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video),
            "-filter_complex_script", str(script), "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "ultrafast" if anteprima else "medium",
            "-crf", "28" if anteprima else "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    return out


# ---------------------------------------------------------------- CLI
def main() -> None:
    ap = argparse.ArgumentParser(description="Editor video lavoro/personale, 16:9 e 9:16")
    ap.add_argument("comando", choices=["analizza", "pianifica", "renderizza", "tutto"])
    ap.add_argument("video", type=Path)
    ap.add_argument("--profilo", required=True, help="lavoro | personale | (altri in profili/)")
    ap.add_argument("--formato", choices=["16:9", "9:16", "auto"], default="auto",
                    help="formato di uscita (auto = come il video originale)")
    ap.add_argument("--senza-ai", action="store_true", help="solo regole, zero crediti")
    ap.add_argument("--anteprima", action="store_true", help="render veloce a 480p")
    ap.add_argument("--rifai-analisi", action="store_true", help="ignora la cache")
    a = ap.parse_args()

    if not a.video.exists():
        sys.exit(f"File non trovato: {a.video}")
    profilo = carica_profilo(a.profilo)
    cart = cartella_di(a.video)

    analisi = analizza(a.video, profilo, a.rifai_analisi)
    formato = rileva_formato(analisi["info"]) if a.formato == "auto" else a.formato
    print(f"[info] profilo={profilo['nome']} formato={formato}")
    f_piano = cart / f"piano_{profilo['nome']}_{formato.replace(':', 'x')}.json"

    if a.comando in ("pianifica", "tutto"):
        piano = pianifica(analisi, profilo, formato, a.senza_ai)
        f_piano.write_text(json.dumps(piano, ensure_ascii=False, indent=1))
        print(f"[piano] salvato in {f_piano} (puoi modificarlo a mano prima del render)")
    if a.comando in ("renderizza", "tutto"):
        if not f_piano.exists():
            sys.exit("Nessun piano: esegui prima 'pianifica'.")
        piano = json.loads(f_piano.read_text())
        valida_piano(piano, analisi["info"]["durata"])
        print(f"[fatto] {renderizza(a.video, analisi, piano, profilo, a.anteprima)}")


if __name__ == "__main__":
    main()
