# Reel "Manuale del Natale in negozio" (46,6 s)

## Consegna
- `06_EXPORT/reel_manuale_natale_finale.mp4`: 1080x1920, 30 fps, H.264 + AAC, voce ElevenLabs + musica + effetti
- `06_EXPORT/copertina_reel_1080x1920.jpg`: copertina del Reel
- `06_EXPORT/storyboard/`: 10 fotogrammi con l'area sicura Instagram evidenziata
- `04_GRAFICHE/copertina_manuale_segnaposto.png`: copertina del manuale disegnata (segnaposto)
- `05_AUDIO`: voce originale, `musica.wav`, `sfx.wav`, `mix.wav`

## Area sicura Instagram
Testi solo dentro x 80-890, y 250-1500 (controllo automatico: `python3 scripts/render.py check`).

## Sostituire la copertina con quella reale
Salva la copertina come `04_GRAFICHE/copertina_manuale_REALE.png` e rigenera:
`python3 scripts/render.py frames <cartella>` + ffmpeg con `05_AUDIO/mix.wav` (vedi comando nel repository).

## Da verificare
- Copertina e pagine del manuale sono illustrazioni segnaposto, non il PDF reale.
- Indirizzo del sito: "cristinaonline.it" (preso dallo storyboard, da confermare).
