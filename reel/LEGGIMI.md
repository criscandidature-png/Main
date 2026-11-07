# Reel "Uno scaffale pieno non è sempre uno scaffale efficace."

## Consegna
- `06_EXPORT/reel_visual_merchandising_finale.mp4`: 1080x1920, 30 fps, H.264 + AAC, 30 s, senza watermark
- `06_EXPORT/copertina_1080x1920.jpg`: copertina verticale
- `06_EXPORT/storyboard/`: fotogrammi chiave delle 6 scene
- `01_SCAFFALI`: scaffale vuoto / prima / dopo (PNG trasparenti)
- `02_PRODOTTI`: 12 confezioni generiche (4 categorie x 3 tonalità), PNG trasparenti
- `03_TESTI`: tutte le scritte del Reel in PNG trasparente (Inter Bold)
- `04_GRAFICHE`: pennellata, cerchio, freccia
- `05_AUDIO`: `musica.wav`, `sfx.wav` (effetti separati), `mix.wav` (usato nel video)

## Uso in CapCut (opzione 1)
1. Nuovo progetto 9:16 > importa il MP4.
2. Per cambiare la musica: separa l'audio dalla clip, elimina la traccia e importa `05_AUDIO/sfx.wav`
   allineato a 00:00, poi aggiungi un brano dalla libreria CapCut al 15-25% del volume.
3. Esporta 1080p, 30 fps.

## Rigenerare
`python3 scripts/render.py assets` · `python3 scripts/render.py frames <cartella>` · `python3 scripts/audio.py`,
poi ffmpeg (fotogrammi + `05_AUDIO/mix.wav`).

## Note aperte
- Il progetto CapCut (.draft) non è generabile in modo affidabile: il video è un MP4 completo.
- Nella scena 3 alcune confezioni si sovrappongono per un attimo durante lo spostamento.
- Musica ed effetti sono sintetizzati in locale (nessun diritto di terzi); è una base semplice.
