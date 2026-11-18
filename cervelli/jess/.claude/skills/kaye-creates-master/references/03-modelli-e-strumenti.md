# 03 — Modelli e strumenti (stack di Kaye, 2026)

> "Non esiste il miglior modello AI. Se qualcuno te lo dice, mente. I modelli sono pennelli: non dipingi i dettagli fini con un rullo da muro. Scegli lo strumento giusto per il lavoro."

Piattaforma principale: **Higgsfield** (tutti i modelli in un posto, cambio con un clic, progetti organizzati). Prompt writer: **Claude** (Opus 5.5 per i compiti complessi; vanno bene anche ChatGPT o Gemini). È un **"two-app workflow"**: scrivi/modifichi i prompt nel chatbot, generi su Higgsfield.

## Immagini — modello per obiettivo
| Obiettivo | Modello | Perché |
|---|---|---|
| Character sheet umani iperrealistici | **Seedream 5.0 Pro** (preferito) | texture della pelle, tratti del volto, zero plastica, nitidezza e contrasto grafico |
| Persone/ritratti/fashion "foto vera" | **Soul 2.0** | addestrato su dati fotografici reali: come la luce colpisce la pelle, sfocature delle lenti, pieghe dei tessuti; molto economico. 3:4 per ritratti verticali |
| Location / still cinematografici / ambienti | **Soul Cinema** | luce architettonica, grana pellicola, profondità atmosferica, prospettiva larga; il più economico (~20× meno) |
| Prodotti, auto, oggetti, plastica/LEGO | **Seedream 5.0 Pro** | precisione grafica, strutture complesse, alto contrasto |
| Design con testo: poster, packaging, mock-up, UI di app/siti, campagne brand | **ChatGPT Image 2.0** | ha un modello linguistico dentro: capisce lettere e ortografia → testo leggibile, non "sciolto" |
| Creazioni rapide quotidiane, copertine reel, thumbnail, più soggetti insieme | **Nano Banana Pro** (logica spaziale, soggetti distinti e proporzionati) + **Seedream** (thumbnail pulite) | carichi gli asset, li tagghi, spieghi in frasi semplici |
| Volto tuo senza riferimenti | **Soul ID** + Soul 2.0 | training una volta, ~20× più economico |

Confronto osservato: stesso prompt di ritratto → ChatGPT e Nano Banana danno pelle cerosa/levigata; Soul 2.0 sembra uno shooting vero. Stesso prompt di location → ChatGPT render piatto e artificiale; Soul 2.0 troppo pulito "da studio"; Soul Cinema indistinguibile da una scena vera.

## Video
| Uso | Modello / tool |
|---|---|
| Quasi tutto (scene narrative, azione, emozioni, multi-asset) | **Seedance 2.5** — "niente batte Seedance 2.5": capisce emozioni umane, movimenti di camera complessi senza rovinare il volto, fisica del corpo, tagging multi-asset, generazione audio. Ha la **draft mode 480p** + upscale della stessa generazione. Fino a ~30 s e fino a ~50 riferimenti in input (dall'ago 2026) |
| Video-to-video su footage reale (es. la porta-portale) | **Seedance 2.0** — accetta footage grezzo intero |
| Motion transfer: rifare un trend, coreografie, combattimenti | **Genjutsu** (Higgsfield) — estrae il movimento da un clip di 4–30 s e lo applica ai tuoi character sheet; accetta anche IP famose come riferimento (non genera il volto protetto) |
| Scambio oggetti mantenendo camera e luce (match cut metaforico auto→toro) | **Genjutsu** |
| Sequenze da regista con frame iniziale/finale | **Cinema Studio 3.0** (Higgsfield) — progetto unico, image + video mode, start/end keyframe, 21:9 |
| Traiettorie di camera ad altissima velocità precise | **Blender + plugin Higgsfield + Opus** (vedi `07`) come riferimento video per Seedance |

## Audio
- **Suno** (Advanced mode) per le canzoni; Pro ~10 $/mese = 2.500 crediti; 5 crediti a brano, ne genera sempre 2.
- **ElevenLabs v3** dentro Higgsfield (tab Audio) per voice-over: voce "Arthur" per narrazione calda e profonda; **delivery mode "Creative"** (performance emotiva dinamica, pause naturali, variazioni) invece di "Natural"; batch 4 e scegli.
- **Sound effects toggle** di Higgsfield: genera l'audio dentro il video (Claude aggiunge cue sonori nel prompt). Nota: alza il costo.

## Motion graphics
- **Claude → Artifacts → Motion** (chat normale, niente Claude Code né After Effects). Con Opus 5.5 renderizza animazioni 2D/3D in HTML. Collegare l'**MCP di Higgsfield** a Claude per generare immagini/B-roll dentro la chat. Dettagli in `07-ricette-progetti.md`.

## Montaggio
- **Premiere Pro** (più controllo) o **CapCut** (veloce, gratis).

## Impostazioni Higgsfield ricorrenti
- Images: modello, aspect ratio (16:9 sheet e location; 3:4 ritratti; 21:9 cinema), qualità 2K, batch 3–4, input di riferimento.
- Video: carica media (eligibility check di qualche secondo), tagga, incolla prompt, sound toggle, aspect ratio (9:16 verticale / 16:9 / 4:3 usato nello spot iPhone), durata, risoluzione (480p draft → 720/1080p/4K), batch.
- Il **costo appare sul tasto Generate** e cambia in tempo reale con le impostazioni.
- **Canvas**: moodboard infinito per la storia.
- **Cinema Studio**: "+" → nuovo progetto/cartella dedicata: tutti gli asset e le generazioni in un posto.
- **Elements**: libreria asset richiamabili per nome.
- **AI Influencer builder** (in Genjutsu → Add character → AI influencer): tipo, genere, fisico, capelli, tratti → "Turn to motion".
