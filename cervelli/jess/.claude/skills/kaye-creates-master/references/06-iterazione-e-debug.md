# 06 — Iterazione e debug delle generazioni

> "L'AI è un processo di trial and error. La prima versione è una bozza. Il 90% dei principianti molla qui perché si aspetta un capolavoro al primo colpo. Non succede mai."

## Il loop
1. Brief semplice a Claude → prompt.
2. Draft 480p, batch 1.
3. **Rivedi "da regista"** (vedi checklist sotto).
4. Torna da Claude **nella stessa chat**: di' esattamente cosa è andato storto e cosa vuoi. Blocca ciò che funziona ("I'm locking everything that already works, but I want to change…").
5. Nuovo draft. Ripeti finché il movimento è giusto.
6. Upscale / alta qualità + batch → scegli la golden take.

## Checklist di revisione del draft
- **Hook**: ferma lo scroll o "sembra un vlog qualsiasi"? Manca il dramma?
- **Inquadratura**: troppo larga (il prodotto, eroe dello spot, non si vede)? Reazioni troppo lontane/piccole? Oggetto chiave coperto nel momento importante?
- **Aria morta**: secondi vuoti all'inizio (2 s a fissare un muro prima che entri qualcuno)?
- **Camera**: zoom/push-in non richiesti? Camera che fluttua invece del POV chiesto? Movimento piatto?
- **Volto e corpo**: morphing? Faccia inespressiva da "burattino 3D"? Arti che si deformano nella transizione?
- **Fisica**: capelli/vestiti immobili? Oggetti senza peso? Personaggio che galleggia invece di subire la gravità?
- **Continuità**: elementi della scena prima spariti? Personaggi della folla mancanti o cambiati?
- **Tono**: coerente col brand/storia? (Il gatto che parla con voce da uomo; l'operaio troppo aggressivo.)
- **Taglio**: due momenti che sembrano due clip separate invece di un movimento continuo?
- **Elementi indesiderati**: il sentiero di terra in mezzo al campo di papaveri, lo zoom inventato.

## Strategie di correzione (in ordine)
1. **Correggi a parole, specificamente**: "No, what I need is when she opens the door, there should be a breeze so that her hair sways, and the camera must be static, no zooms… sun rays… really realistic." / "Remove the dirt path. I want a huge clean field of poppy flowers. Make her face look more lively and add a light wind blowing her hair and her cloak."
2. **Lista aggressiva di aggiustamenti di framing** (più stretto sul prodotto, togli l'aria morta, prodotto visibile durante l'urto, gruppo più compatto nell'ultimo shot).
3. **Aggiungi lo stato interiore** e un'imperfezione umana se il personaggio è rigido.
4. **Scrivi la fisica** (rimbalzi, peso, vento, massa corporea).
5. **Se il prompt sbatte contro un muro, CAMBIA STRATEGIA** invece di ripetere lo stesso errore. Diagnosi: troppi compiti complessi in un unico piano continuo (stanza piena di oggetti + mettersi le cuffie + rotolare dalla finestra + transizione su uno skyline) → **dividi in due shot**, riusa una generazione precedente buona per il primo, nascondi il taglio con un extreme close-up.
6. **Riferimento visivo**: schizzo, screenshot di un frame riuscito, Blender, video di riferimento.
7. **Batch senza toccare il prompt** quando la logica è solida e i tag sono giusti ma c'è casualità (fino a 10 varianti per una scena di folla complessa).
8. **Frankenstein**: monta la parte migliore di ogni take.

## Mindset di debug (Spider-Verse)
"Cerca la causa: il corpo si deforma perché lo shot è troppo lungo? La camera zooma troppo? Manca il peso fisico? **Cambia UNA variabile alla volta**, testa a 480p, sii paziente; quando scatta, fai batch a piena risoluzione per catturare la golden take."

## Log reale delle 6 iterazioni Spider-Verse (esempio da replicare)
1. Camera piatta, personaggio rigido senza emozione.
2. + emozioni interiori ("raw adrenaline and excitement") + inciampo realistico → corpo deformato nella transizione.
3. Ancora deformato.
4. Diviso in 2 shot + taglio nascosto da close-up dello spara-ragnatele + cue vocali/emotivi → meglio, ma galleggia.
5. Schizzo stick figure + screenshot di un angolo riuscito → quasi.
6. Vincoli fisici: massa corporea, luce, interazione con la città (corre sui tetti, scivola sui muri), durata → giusto. Poi 4K batch 4.

## Iterare con Claude Motion (motion graphics)
Non rifare da zero: "Lock everything that already works; change the grain, make all visuals one style, slightly improve the text animation" + più riferimenti. Oppure: "I want the pacing to feel snappier and the text to pop a bit more."

## Sapere quando fermarsi (gusto da regista)
Kaye ha cancellato un finale su cui aveva lavorato un'ora (scena sul letto di morte) perché troppo cliché e prevedibile. Rinunciare a un'idea fa parte della regia.
