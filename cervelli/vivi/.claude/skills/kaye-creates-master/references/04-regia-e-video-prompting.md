# 04 — Regia e video prompting

> "L'AI è la troupe sul set: gira quello che chiedi. Tu sei il regista che chiama ogni inquadratura."

## Il principio base
Chi scrive "woman walks in painting" ottiene video piatti e robotici. Metti il cappello da regista e immagina **cosa succede tra i frame**:
1. **Qual è la storia** di questo momento?
2. **Cosa fa la camera?** (pensa come il cameraman che ha fisicamente la camera in mano)
3. **Cosa fa il personaggio** (azioni concrete, mai una posa statica)?
4. **Cosa prova?** — "I modelli AI capiscono in modo incredibile le emozioni umane. Non descrivere solo l'azione: descrivi lo stato emotivo." Es.: "She just returned from a very difficult battle. She's exhausted, she feels completely alone, and she walks like she just wants to lay down and rest." / "Her face shows raw adrenaline and excitement — she needs to feel that sudden rush."
5. **Cosa deve far provare la scena allo spettatore**?

L'utente scrive tutto questo in parole semplici (2–3 frasi per scena); Claude produce il prompt tecnico frame per frame con timing, camera, blocco fisica, cue SFX e negativi.

## Il prompt video descrive SOLO il movimento
"Più lungo non è meglio." Se carichi character sheet e location, aspetto e luogo sono già fissati: ridescriverli dà al modello la possibilità di cambiare qualcosa che era già deciso. Il prompt lavora su: azione, camera, emozione, fisica, timing, suono.

## Camera: vocabolario e trucchi usati da Kaye
- **Descrivi il movimento della camera, non la camera come oggetto**: scrivere "FPV drone" mette un drone vero nell'inquadratura. Scrivi invece come si muove la vista ("the view rushes low over the water, banking hard…").
- **Camere statiche**: scrivilo esplicitamente — "camera does not move, straight from above", "no camera movement and no zoom". "Se non dici al modello cosa NON fare, aggiunge un lento push-in che non hai chiesto." "Ai modelli PIACE aggiungere zoom casuali."
- **"Continuous single take"** all'inizio del prompt per un piano sequenza.
- **POV dentro un oggetto chiuso**: i modelli non capiscono i cambi di prospettiva dentro una scatola → esplicita "static extreme low angle perspective looking straight up from inside the box".
- **Over-the-shoulder**: camera dietro il personaggio, guarda oltre la spalla verso l'altro; il volto fuori campo di proposito ("la distanza tra loro È l'inquadratura").
- **Dolly zoom / zolly / vertigo shot**: la camera avanza zoomando indietro → soggetto fisso, sfondo che si allarga (usato nel lip-sync).
- **Low angle a livello del pavimento**: dà potenza al soggetto; l'obiettivo grandangolare lo esagera.
- **Scala delle inquadrature** (keyframe del teatro):
  - wide shot: stabilisce uno spazio fisico reale invece di uno sfondo "incollato";
  - extreme close-up con macro e sfondo sfocato: i **dettagli** fanno sembrare girato (i film veri sono pieni di piccoli momenti; l'AI quasi mai);
  - 85 mm con profondità di campo ridottissima: compressione, sembra pellicola e non un crop;
  - 24 mm basso, bloccato sul momento esatto dell'azione: congelare quel frame dà all'AI un bersaglio preciso.
- **Teleobiettivo 100 mm** su un close-up con sabbia/vento → "sembra girato con una camera da un milione".
- **Grandangolo** in volo → senso di velocità folle.
- **Drone wide + handheld documentaristico ravvicinato** per la stessa azione (scalata).
- **Citare un direttore della fotografia reale** per ottenerne lo stile: "Emmanuel Lubezki (The Revenant): raw, close-up, handheld".
- **Top-down / bird's-eye** per mappe, mani che disegnano, lavoro alla scrivania.
- **Extreme wide finale** "per far respirare il film" dopo tanta emozione (personaggi minuscoli nel frame).
- Camera che sale nel cielo come chiusura epica; frame che si allarga con un'azione del prodotto (24 mm → wide quando si preme il tasto).

## Luce (il dettaglio che separa l'AI noiosa dal cinema)
- Chiedi a Claude di **far combaciare la luce del personaggio con quella dell'ambiente**, così il personaggio "appartiene alla stanza".
- **Re-light**: gli sheet sono fotografati con luce bianca piatta da studio; senza istruzione il volto si porta dietro la luce da studio dentro la location e sembra finto. In ogni prompt di scena: "re-light her face according to the scene's light sources".
- **Ombre dure / luce direzionale** invece di luce morbida e nebbiosa.
- Cambiare l'ora del giorno è una leva (sera → giorno; golden hour per i finali).
- Contrasto di temperatura come transizione (bufera gelida → surf al sole).

## Fisica (il cheat code del realismo)
- **Vento e tessuti**: "Aggiungere vento e fisica dei tessuti è il cheat code definitivo: rende i video AI 10 volte più realistici." Un mantello completamente immobile all'aperto = finto. "Light breeze moving her hair and cloak/clothes."
- **Scrivi la fisica a parole** invece di sperare: la pallina che "rotola" era tecnicamente corretta ma emotivamente piatta → "A worn green and yellow tennis ball bouncing down the aisle, each bounce lower and shorter than the last, kicking up dust as it goes."
- **Physics block/box** nel prompt: peso degli oggetti ("the sword feels long and heavy"), trasferimento del peso del corpo ("she doesn't drop like a rigid block, she transfers her weight like in real life"), spruzzi d'oceano, passi pesanti, massa corporea.
- Per azioni atletiche/supereroistiche: vincoli fisici espliciti — massa corporea, luce, interazione con l'ambiente (corre sui tetti, scivola lungo i muri), durata — altrimenti "galleggia come un palloncino invece di oscillare con la gravità".
- **Imperfezione umana**: "she slips or stumbles slightly on the window frame before catching herself" → momento umano reale.
- **Gaze tracking**: gli occhi del personaggio devono **seguire l'oggetto che passa PRIMA** che il corpo reagisca, altrimenti la reazione è finta.

## Velocità e ritmo
- **Senso di velocità**: in aria vuota l'occhio perde il riferimento → metti **persone sullo sfondo** (scalatori sulle corde) e lo shot sembra un jet che passa.
- **Ritmo**: dopo 5 shot ad alta adrenalina il cervello si anestetizza → **slow motion estremo** (wide al rallentatore + extreme close-up del volto con vento e sabbia).
- Nelle sequenze multi-cut: "keep the action moving fast from start to finish" altrimenti l'AI si rompe verso la fine.
- Due scene consecutive come un unico momento: esterno wide → POV in prima persona (dagli occhiali che stanno registrando).

## Transizioni e montaggio pensato in fase di prompt
- **Match cut**: taglio tra due shot con stessa forma o stessa azione, così il salto sembra un movimento continuo. Esempi: taglio sulla pallina → 6 anni prima senza che il cervello se ne accorga; robot immobile nel capanno mentre fuori passano stagioni e decenni (ragnatele, polvere sulle spalle, luce da dorata a grigio invernale); stage jump del rapper in 6 ambientazioni (palco, sole, pioggia, notte, neve…); auto F1 → toro (Genjutsu).
- **Nascondere un taglio**: inizia lo shot successivo con un **extreme close-up ad alta velocità** (lo spara-ragnatele che esplode dal guanto) → nasconde il cambio d'ambiente.
- **Transizione naturale**: la tuta alare che sorvola la ciclista collega due scene e porta la seconda interazione col prodotto senza rompere la storia.
- **Split screen** stile anime/fumetto: tre close-up che scattano nello schermo uno dopo l'altro.
- **Macro slow-motion** del momento chiave con camera shake intenzionale + SFX a bassa frequenza all'impatto (il telefono che cade).

## Riferimenti visivi > paragrafi
- **Schizzo brutto**: per posizionamenti spaziali complessi (verticale capovolta sul bordo della scogliera, inquadrature nello specchio, angoli del corridoio, traiettoria con frecce) non scrivere un'ora di paragrafi: disegna stick figure su carta o iPad e mandalo a Claude con gli sheet. "All'AI non importa se sei Da Vinci: un riferimento dà 10× più comprensione di un prompt lungo."
- **Screenshot di un frame che ti piaceva** (anche da una generazione fallita) + schizzo: "Keep this exact camera framing from the screenshot, but use the scene from my stick figure drawing."
- **Keyframe da film** come storyboard spaziale (5 screenshot dello Spider-Verse: stanza, davanzale, inizio rotolamento, caduta dalla finestra, fuori campo).
- Frame di un film o foto Pinterest come riferimento di inquadratura.
- **Video di riferimento** per l'energia/il movimento (anche per animare un quadro).

## Animare i keyframe: 3 metodi (stesso costo, risultati diversi)
1. **Ogni keyframe separato**: preciso e consistente, ma senza transizioni.
2. **Un'unica generazione da 15 s con 4 tagli netti**: Claude unisce i 5 prompt in una sequenza continua; input = sheet + location + tutti i keyframe → tagli consistenti nello stesso ambiente.
3. **Solo sheet + location, scene descritte nel prompt**: volto e luogo consistenti ma l'inquadratura "deriva", meno cinematografico.
→ Ecco perché costruire prima i keyframe statici.

## Start & end frame (Cinema Studio)
Genera il frame iniziale e quello finale (2K, 21:9) → Cinema Studio 3.0 video, 15 s → Claude divide il prompt in ~6 tagli rapidi con SFX reali.

## Realismo "per sottrazione"
Il segreto non è chiedere attrezzatura cinematografica di lusso ma **elencare le cose brutte da spegnere**: "no shiny plastic skin, no harsh sharpening, no oversaturated colors". Toglierle una per una funziona meglio che chiedere qualcosa di specifico. Usa sempre anche un **negative prompt** (cosa il video NON deve essere/generare).

## Text-to-video senza riferimenti: 2 errori
1. Nominare la camera come oggetto (→ appare nell'inquadratura).
2. Pose statiche (→ manichino digitale rigido). Di' cosa sta FACENDO il personaggio.

## Video-to-video su footage reale
Base filmata col telefono (luce sufficiente, volto e corpo ben visibili). Nel prompt: "Don't change anything about the original video" + cosa cambia e quando ("right when the door opens, show the location from the photo like the door is a portal") + atmosfera (brezza, raggi di sole).

## Lip-sync senza "bocca da burattino"
- Non dare al modello l'intera canzone: isola lo snippet esatto per lo shot (5–11 s).
- **Togli il beat**: usa lo stem vocale isolato, così il modello non scambia i colpi di rullante per sillabe.
- Carica audio + asset + prompt (es. con dolly zoom).

## Combattimenti e azione complessa
Da solo testo = groviglio di arti. Usa **motion transfer** (Genjutsu) con clip di riferimento di veri artisti marziali (YouTube) + sheet + prompt breve su cosa sostituire e come. Kaye ha anche una skill Claude "Fight Engine" per fisica del combattimento, timing degli impatti e prompt di movimento avanzati.

## Tono e coerenza di brand
Un operaio che urla e agita le braccia era "troppo aggressivo per uno spot Apple" → ammorbidisci. La reazione deve stare nel tono del brand (stupore, meraviglia, comicità).

## Continuità
- Passa tutti i personaggi già comparsi nelle scene successive ("strict crowd continuity").
- Elementi della scena precedente devono persistere (la vernice sulla strada).
- "Use the exact same references as in the previous scene, just change the location."
