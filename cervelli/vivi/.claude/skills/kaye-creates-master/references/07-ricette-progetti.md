# 07 — Ricette dei progetti reali (replicabili)

Ogni ricetta: risultato → passi → trucchi specifici. Kaye ripete: "Non ti do uno script da copiare parola per parola: ti mostro i fondamentali per costruire la TUA versione."

---
## A. La porta-portale (11M views + 30K follower in 3 giorni)
1. **Filma davvero** col telefono: tu che apri una porta di casa ed esci. Luce sufficiente, volto e corpo visibili. (Serve per il video-to-video.)
2. **Mondo**: Pinterest "fantasy world", "dreamcore world" → scegli il più magico.
3. **Prompt** con Claude: carica la foto e scrivi in parole tue: "I've got a video of me opening a door in my house plus a separate photo of a location. That photo should show up on the other side of the door. Don't change anything about the original video. Right when the door opens, show the location from the photo on the other side, like the door is a portal. That's the moment I step through and start running around. Add a light breeze right as the door opens, just enough to move my hair and clothes a bit, plus some soft sunlight coming through." → Claude dà breakdown scena per scena + negative prompt.
   - Abitudine chiave: **scena per scena** (la porta si apre → appare la location → lei passa), più comportamento della camera.
4. **Generazione**: Higgsfield → Video → Upload media (footage + foto location) → incolla → SFX on → 9:16 o 16:9 → 1080p/4K → **Seedance 2.0** (accetta footage grezzo).
5. Una generazione → controlla → correggi ("brezza che muove i capelli, camera statica senza zoom, raggi di sole, molto realistico") → poi batch e scegli.
6. Varianti: altri mondi/stili. Serie "Welcome to my world" (nel mio mondo la macchina è un piccione, apri una porta e arrivi dove vuoi).

## B. Corto emotivo "Kareema e il robot" (100+ ore, ~1.641 crediti)
- Ispirazione: The Wild Robot, Wall-E (far amare un pezzo di metallo). Storia che copre una vita: regalo d'infanzia → crescono insieme → lei si sposa/ha figli → il robot si guasta, dimenticato nel capanno → finale caldo e speranzoso.
- Asset: robot umanoide (non stile Transformer) con occhi a sensori caldi luminosi; 4 sheet di lei per età; 9 location attorno alla casa (Soul Cinema).
- Scena 1: POV dal basso dall'interno della scatola mentre la bambina apre il coperchio (riscritto come "static extreme low angle looking straight up from inside the box").
- Bonding compresso: gioco in giardino, favole nel fortino di coperte, adolescente in camera, robot che si prende cura di lei. Luce coerente con l'ambiente, vento.
- Svolta: vita adulta piena (pianto bilanciato da gioia; momento quotidiano di scelta dell'outfit) → il legame si allontana.
- **Match cut del tempo**: robot immobile nel capanno buio mentre stagioni e decenni passano fuori dalla finestra polverosa (5 prompt).
- Finale scartato (letto di morte = cliché) → close-up della mano rugosa che si posa sulla mano polverosa del robot.

## C. Corto "ragazza + cane zombie" (ispirato a I Am Legend; 2M+ views, ha avviato un trend pagato dalle aziende AI; 790 crediti)
- Director's brief → file unico. Pinterest: ragazza post-apocalittica con cappello da pilota, corsia di supermercato abbandonata con luce, pastore tedesco con gilet, campo da basket scolastico invaso dalla vegetazione.
- Sheet doppi (lei pulita/ferita; cane sano/infetto con numeri precisi).
- 9 scene: piano sequenza delle mani che tremano e occhi lucidi; over-the-shoulder col fucile abbassato; cane da solo medio statico "no camera movement, no zoom"; lei si accovaccia, posa il fucile, si asciuga le lacrime e sorride ("want to play" = centro emotivo); pallina che rimbalza (fisica scritta) → **match cut sulla pallina** al passato; wide dall'alto senza tagli della corsa; close-up "clean and unhurt"; gioco puro insieme; extreme wide finale sul tetto di un'auto arrugginita mentre lo nutre dalle mani.
- Montaggio con un brano straziante.

## D. Videoclip musicale K-pop "Replica" (4.153 crediti; equivalente 200–300K $)
1. **Musica con Suno**: chiedi a Claude un prompt tecnico ("Write a Suno prompt for a high energy K-pop girl crush dance rap track, solo female artist, mixed English/Korean verses, and a catchy one-word English hook of your choice") → hook generico ("fire") → chiedi hook insoliti (glitch, mirage, voltage, replica, velvet, ricochet) → riscrivi il testo attorno alla parola scelta.
   - Suno → Create → **Advanced**: testo con i **tag di performance tra parentesi** (gang vocals, silence breaks: Suno li legge come arrangiamento), style box, **Exclude styles** (ballad, acoustic, piano, chill → niente cambi di genere a metà), voce femminile, durata custom 130 s, weirdness 50%, style influence 50%, titolo. Scegli tra le due take.
2. **Storia da un'esperienza reale** (account falsi con la sua faccia → superstar perseguitata da cloni). Estetica dal brano: cyberpunk coreano neon (viola, neon, accenti acidi).
3. **Asset**: 4 location (esterno club, camerino, corridoio backstage da due direzioni, vicolo); sheet: protagonista Y2K blu metallico + stivali argento, cloni (emo capelli blu, pugile in completo, cyber), guardie del corpo, travestimento; **crowd sheet**; **prop sheet** limousine. Layout con figure intere tagliate al collo.
4. **Shot list unica** da Claude (3 atti + finale). LOCATION + SHEET + PROMPT = SCENA; Seedance 2.5 draft → upscale.
5. **Lip-sync**: snippet 5–11 s, stem vocale senza beat, dolly zoom.
6. **Fight**: Genjutsu motion transfer da clip di arti marziali reali; skill "Fight Engine".
7. **Montaggio**: traccia Suno in timeline, lip-sync allineato alla voce, scene di storia a tempo di beat, SFX.

## E. "Spec ad" per grandi brand (serie "fake commercials until they notice me")
Strategia: spot finti di altissimo livello per brand miliardari → visibilità, commenti dei team (Apple ha commentato), inbound di clienti.
- **Ep. 1 iPhone 18** (800K–1M views): 20+ spot Apple studiati; storia: cammina con l'iPhone non ancora uscito, la gente impazzisce e la segue, selfie di gruppo finale. 17 character sheet (nonna asiatica col gatto, punk con cresta rossa, operai, ballerina, ragazza col cappello rosa…), model sheet del telefono nel colore "leaked" burgundy, 4 location di New York. Hook: il cubo Apple si gonfia di vernice ed esplode, l'onda si ferma a 1 mm dalla scarpa mentre lei passeggia indifferente. Pivot non pianificato dallo slogan "Relax, it's iPhone": il telefono cade (macro slow-mo, shake, SFX bassi) → reazioni a raffica → split screen fumetto → raccolta dall'alto → schermo intatto, battuta, sollievo → selfie con UI del telefono, frame che si allarga, camera che vola nel cielo.
- **Ep. 2 Red Bull F1** (3M+ views, fatto in una sera): pilota che perde, furiosa, versa una lattina nel serbatoio → l'auto si trasforma nella supercar Red Bull → sorpassa tutti → match cut auto/toro (Genjutsu) → slogan in scena. Trucchi: wrap dell'auto da riferimento; blocco ottico nelle location; batch invece di riscrivere; **Blender** per la traiettoria ultra-veloce.
- **Ep. 3 Oakley × Meta** (1.180 crediti vs 500K $): studio del sito e delle funzioni (assistente vocale "Hey Meta"); storia su Canvas: verticale su una mano sul bordo della scogliera (hook da Pinterest) → tuta alare nella gola → POV dagli occhiali → scalatori sullo sfondo per la velocità → ciclista con bici rosa (transizione) → cavallo nel deserto al rallentatore con sabbia sul volto (prova del prodotto) → scalata in bufera (stile Lubezki) → surf al sole → mappa dall'alto, Antartide coi pinguini, motoscafo (senza sheet: close-up con solo riferimento) → falò con amici (ogni amico con il suo sheet, anche il cane) → si toglie gli occhiali.
- Regole: mostrare il prodotto come eroe e **sempre consistente**; integrare le funzioni del prodotto nella storia (voce, POV, tasto azione); restare nel tono del brand; chiudere su nota umana + product shot.

## F. Blender + Opus per traiettorie impossibili (zero competenze 3D)
1. Scarica il plugin Higgsfield per Blender, trascina il file in Blender, fai login → c'è un prompt box Higgsfield dentro Blender.
2. Scegli Opus, descrivi in frasi semplici azioni e **movimenti di camera** → scrive il Python e costruisce l'animazione da solo.
3. Render e download → usalo come **video di riferimento** in Seedance 2.5 con il prompt originale + istruzione che camera e fisica devono **combaciare esattamente** con il riferimento Blender.

## G. LEGO × "Leonardo" — realismo al primo colpo (spot da "10.000 $")
- Un unico brief: 4 personaggi (fotografa asiatica nell'appartamento di NY, Kiko fan del rock giapponese con stanza vintage e Fuji alla finestra, Sergio messicano coi baffi nel café di tacos, Brian costruttore sul grattacielo di Manhattan), location, prop LEGO (fotocamera, chitarra rosa, taco, gru gialla), struttura di camera, script del voice-over → Claude sputa tutti i prompt in 40 s.
- Cinema Studio + cartella progetto; Seedream per persone e LEGO, Soul Cinema per le location.
- **3 strutture di scena riusate per 4 personaggi**: (1) extreme close-up ritratto con lento dolly zoom out; (2) figura intera statica wide con prop; (3) micro close-up sul prop; (4) tutti insieme.
- Twist: nel finale diventano minifigure LEGO. Voice-over ElevenLabs v3 "Arthur", modalità Creative. Montaggio sul VO.

## H. Quadri classici che prendono vita (8M+ views; serie medievale/Odissea)
- Trend del momento (Odissea) → moodboard Pinterest ("classical painting", "medieval art", "Odyssey art illustrations") → ~8 quadri.
- Sheet in due modi (outfit tuo vs outfit esatto del quadro); sheet delle creature (Ciclope); location dal quadro "with zero people" o dalla testa; blocco camera in ogni location.
- Video: Claude struttura frame per frame + physics block (spruzzi, passi pesanti); 480p, 4–5 s; poi giorno invece di sera + vento sui tessuti; finale in alta qualità con SFX. Abbina ogni quadro a una trama da film.
- Variante rapida (Short): "descrivi cosa deve far *sentire* il quadro" (il modello legge l'intenzione emotiva) oppure dai un video di riferimento per l'energia.
- Gestione critiche ("l'AI non deve toccare l'arte classica"): riconosci il punto, spiega che l'AI è un pennello e che ti ha fatto guardare i quadri più da vicino, chiedi nei commenti quale quadro animare.

## I. Gwen Stacy Spider-Verse (8M views, migliaia di ricreazioni)
- "Ogni universo ha la sua Gwen: com'è Gwen nel MIO universo?" → outfit proprio (bermuda cargo grigi, felpa blu, caschetto, piercing).
- 5 screenshot del film come storyboard spaziale; richiesta: "We are creating Spider-Man style animation. Base character is 100% locked to my attached character sheet. The environment must match image 1…" + azione frame per frame + battuta + camera.
- 6 iterazioni (vedi `06`). Seedance 2.0 allora; 2.5 oggi dà luce sulla tuta, peso fisico reale e drone che la segue.

## J. Il cavaliere nel campo di papaveri / la ragazza sul bordo della scogliera (6M views, trend)
- Sheet da Pinterest "woman in knight armor" + selfie; prop sheet spada ed elmo; location con nebbia stratificata.
- Prompt-storia con stato interiore; camera: parte bassa sui piedi (passo pesante, lascia cadere l'elmo) → sale lungo il corpo mentre arranca nel campo → gira di lato mentre si lascia cadere sull'erba. Physics box (spada pesante, trasferimento del peso), cue SFX.
- Fix: via il sentiero di terra, volto più vivo, vento su capelli e mantello.

## K. Trend con Genjutsu (milioni di views in media)
1. **Swap semplice**: sheet (anche del gatto) → Genjutsu → carica il video di riferimento (qualsiasi trend, 4–30 s) + sheet → prompt breve "cosa viene sostituito con cosa" + tag → genera uno, controlla fisica e volto, poi batch. (Rain Dance ~2M; hotel lobby; Birds of a Feather.)
2. **Avanzato** (stesso movimento, cambi ambiente/azione): prompt **obbligatorio**. Es. la camminata/salto sul palco: 6 sheet + 6 prompt (palco normale, sole, pioggia, notte, neve…) + footage originale → 6 clip → match cut nell'editor + esplosione finale (3M+ views).
3. **AI influencer** (vedi `11`).

## L. Motion graphics con Claude (622K views — il suo video più visto)
- **Su footage grezzo** (talking head): Claude → Artifacts → Motion; collega l'MCP di Higgsfield (B-roll e visual generati in chat); carica video grezzo + **script** (mappa ogni frase); carica **più clip di riferimento** dello stile; allega la tua **skill di motion design** (regole e strutture di codice); descrivi in frasi semplici cosa vuoi e dove, senza termini tecnici; Opus 5.5 → scarica il file → itera bloccando ciò che funziona. 34 min contro 5 ore del designer.
- **Da zero (launch video)**: riferimenti di launch video high-end + elementi Pinterest + skill + descrizione del vibe come a un motion designer → v1 → "pacing più scattante, testo che risalta di più" → v2 (stile ritagli di riviste). 20 minuti.
- Regola: un prompt pigro di una frase = risultato banale; **"il prompt è il 90% del lavoro"** → riferimenti + asset di brand + direzione vera.
- Verdetto onesto: Claude vince su velocità e prezzo; il designer umano porta gusto, conosce brand e pubblico, micro-dettagli (lens flare, ecc.). Ma ai brand non importa chi monta: importa che sia bello.

## M. Design con testo (ChatGPT Image 2.0)
- Mock-up prodotto in 2 minuti vs 13 ore del designer: descrivi prodotto, packaging, tagline, scritte piccole sul retro; specifica "no broken letters, only actual readable text".
- UI di app/siti, ad creative, campagne brand (sequenza di prompt per angoli prodotto e packaging), poster.

## N. Contenuti personali/nostalgici
- Il giocattolo preferito dell'infanzia (coccodrillo) generato in posti e scene diverse descrivendo **i sentimenti** che avevi allora e non sapevi illustrare.
- "Il tuo piccolo mondo" surreale (serie Welcome to my world, dreamcore, pixel art).
