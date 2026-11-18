# 01 — La pipeline master di Kaye (dall'idea al video finito)

Questa è la sequenza che Kaye ripete in OGNI progetto (corto emotivo, spot, videoclip, trend). Le varianti sono in `07-ricette-progetti.md`.

## Fase 0 — Idea (vedi anche `10-crescita-e-creativita.md`)
- Parti da: un trend del momento (film in uscita, lancio di un prodotto, meme), un format già virale (regola outlier ≥500K views), un'emozione presa da un film ("I Am Legend", "Wall-E", "The Wild Robot", "Interstellar") rielaborata a modo tuo, un'esperienza reale (es. account falsi che copiano la sua faccia → videoclip "Replica"), un oggetto personale (il peluche coccodrillo dell'infanzia), una canzone (la musica fa da regista).
- **Idea collision**: scontra due cose che non c'entrano (format di un mondo + stile visivo di un altro).
- Per un brand: studia il sito e i vecchi spot (Kaye guardò 20+ spot Apple dagli anni 2000 a oggi), il DNA del brand (Red Bull = adrenalina/caos creativo; Apple = creatività vivace e slogan "Relax, it's iPhone"), le funzioni del prodotto da mostrare (gli occhiali Meta con assistente vocale), i colori.
- Moodboard: **Pinterest** (cartelle dedicate) o **Higgsfield Canvas** (moodboard infinito dove mappare tutta la storia con riferimenti).

## Fase 1 — Director's brief (un solo messaggio a Claude)
"Lazy prompting method": NON generare personaggi, stanze e oggetti separatamente in 30 messaggi (confonde il contesto e brucia crediti). Manda **un unico brief massiccio** con:
- la storia raccontata in linguaggio semplice "come a un'amica", senza tecnicismi;
- tutti i personaggi (+ riferimenti Pinterest/selfie allegati);
- le location;
- i prop/prodotti;
- la struttura di camera / le scene che immagini;
- eventuale voice-over o dialoghi;
- tono, emozione, piattaforma, durata.

Output richiesto: **un unico file** con scene (atti + finale), location, descrizioni dei character sheet, tutti i prompt. Così la trama "non cade a pezzi" e c'è continuità.

Struttura narrativa che Kaye usa per far *sentire* qualcosa:
- **Hook nei primi secondi** (l'apertura deve fermare lo scroll; se il primo draft "sembra un vlog qualsiasi", aggiungi qualcosa di totalmente inatteso: il cubo di vetro Apple che si gonfia di vernice ed esplode).
- Una storia che copre un arco (una vita intera, un'evoluzione).
- **Punto di svolta emotivo** (dramma/rottura) che tiene agganciati.
- **Alternanza emotiva**: pianto bilanciato da gioia pura; momenti quotidiani per il ritmo e l'intimità.
- **Ritmo**: dopo 5 shot ad alta energia il cervello si anestetizza → slow motion estremo.
- **Lascia una domanda** nello spettatore.
- **Finale**: evita il melodramma prevedibile; meglio un dettaglio sottile (la mano rugosa sulla mano polverosa del robot). Chiudere su una nota calda e umana (falò con amici, selfie di gruppo).
- Chiediti da regista: **"Quale emozione inattesa posso dare qui?"** (twist: i 4 personaggi diventano minifigure LEGO; il telefono che cade).

## Fase 2 — Asset (dettagli e template in `02-asset-sheets.md`)
1. Character sheet per OGNI personaggio che appare (anche comparse, folla, animali).
2. Varianti di stato (pulito/ferito, bambina/adolescente/adulta/anziana, sano/infetto, umano/minifigure).
3. Location sheet per ogni ambiente (anche la stessa location da due direzioni).
4. Model/prop/product sheet per ogni oggetto chiave (auto, telefono, spada, elmo, limousine).
5. Nomina ogni file sul computer e caricali su Higgsfield (Elements / progetto Cinema Studio).

Costo tipico asset: 20–50 crediti per un progetto intero. È la parte più economica e quella che fa la differenza.

## Fase 3 — Keyframe (opzionale ma potente)
Prima di animare, genera **immagini statiche delle scene** (character sheet + location come riferimenti) con inquadrature variate (wide, macro, livello pavimento, 85mm, 24mm sull'azione) e con l'istruzione di **re-illuminare** il personaggio. Poi animali. È il metodo che dà più controllo sull'inquadratura (vedi `04`).

## Fase 4 — Prompt delle scene
- Per ogni scena l'utente scrive 2–3 frasi: cosa fa la camera, cosa fa il personaggio, cosa fanno gli altri, cosa deve far provare la scena.
- Claude trasforma in prompt tecnici dettagliati (frame per frame, timing, camera, blocco fisica, cue sonori, negativi), taggando gli asset con i nomi file.
- Per inquadrature difficili: **schizzo brutto** (stick figure su carta/iPad) o screenshot di riferimento → Claude.
- Shooting schedule efficiente: riusa poche strutture di scena per più personaggi (3 strutture × 4 personaggi invece di 12 prompt unici).

## Fase 5 — Generazione (vedi `05` e `06`)
Higgsfield → Video (o Cinema Studio → video) → Seedance 2.5 → carica e tagga asset → incolla prompt → sound toggle ON → **draft 480p, batch 1** → revisione "da regista" → iterazione → upscale/qualità piena → batch per scegliere la "golden take".

## Fase 6 — Montaggio e audio
- Premiere Pro (più controllo) o CapCut (veloce e gratis).
- Taglia sul ritmo della musica o del voice-over; aggiungi SFX.
- "Frankenstein": unisci la parte migliore della take A con quella della take B. Non serve un prompt magico che faccia tutto in un unico piano: serve un buon taglio tra due take buone.
- Voice-over dentro Higgsfield (ElevenLabs v3, modalità Creative), musica con Suno (vedi `07`).
- Un brano emotivo forte per i corti ("one heart-wrenching track").

## Fase 7 — Pubblicazione e analisi (vedi `10`)
Hook, trial reels con varianti se il post decolla nelle prime 24h, guarda share e save, capisci perché ha funzionato e raddoppia.

## Checklist finale prima di consegnare un piano all'utente
- [ ] Brief unico con storia, emozione, svolta, finale
- [ ] Lista asset completa (ogni persona/animale/oggetto in scena ha uno sheet)
- [ ] Nomi file e tag coerenti
- [ ] Ogni prompt video: solo movimento + camera + emozione + fisica + negativi + re-light
- [ ] Piano draft 480p → upscale
- [ ] Piano di montaggio (musica/VO, ordine, tagli, SFX)
- [ ] Stima crediti
