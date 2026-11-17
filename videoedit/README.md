# Editor video — Lavoro / Personale

Monta video con uno stile fisso, spendendo pochissimi crediti.

```
ANALIZZA (gratis, locale)  ->  PIANIFICA (Claude legge solo testo)  ->  RENDERIZZA (FFmpeg, gratis)
Whisper: parole + tempi        1 chiamata, sceglie frasi + hook        tagli, formato, sottotitoli, audio
```

## Installazione
```bash
# serve ffmpeg installato
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...        # non serve con --senza-ai
```

## Uso
```bash
# Profilo LAVORO, il formato si rileva da solo (16:9 o 9:16)
python editor.py tutto clip.mp4 --profilo lavoro

# Profilo PERSONALE, forza il verticale, anteprima veloce a 480p
python editor.py tutto clip.mp4 --profilo personale --formato 9:16 --anteprima

# Zero crediti: solo regole (via pause, "ehm", frasi ripetute)
python editor.py tutto clip.mp4 --profilo lavoro --senza-ai
```

### Flusso consigliato (per non sbagliare)
1. `pianifica` → controlla/modifica `lavori/<video>/piano_*.json`
2. `renderizza --anteprima` → guarda il risultato
3. `renderizza` → versione finale (non spende crediti: riusa il piano)

La trascrizione viene salvata in cache: rifare il piano o il render non la ripete.

## Profili
In `profili/lavoro.yaml` e `profili/personale.yaml`, ognuno con le sezioni `"16:9"` e `"9:16"`:
- **taglio**: pausa massima, margine, parole riempitive, gestione delle ripetizioni
- **ai**: modello e istruzioni di stile per Claude
- **formati**: risoluzione, durata massima, zoom (punch-in), stile sottotitoli
- **audio**: loudness

Per un nuovo stile basta copiare un file YAML (es. `profili/cliente_x.yaml`) e usare `--profilo cliente_x`.

## Come taglia
- Taglia solo **tra le parole** (tempi di Whisper + margine): mai a metà parola.
- Frasi rifatte: tiene **l'ultima presa**.
- Claude riceve solo righe `id|tempi|testo` e restituisce gli id da tenere: non tocca i tempi, quindi non può sbagliare i tagli.
- Il piano viene validato prima del render.

## Consigli in fase di ripresa
- Fai 1 secondo di pausa prima di ogni frase.
- Se sbagli, ripeti **tutta** la frase.
- Audio pulito (microfono vicino) = trascrizione migliore = tagli migliori.
