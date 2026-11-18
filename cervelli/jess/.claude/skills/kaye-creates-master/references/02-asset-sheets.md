# 02 — Asset: character sheet, location sheet, prop/product/crowd sheet

"Pensa agli asset come agli ingredienti di una torta: farina, uova e zucchero pronti prima di cucinare." Senza asset: facce che cambiano a ogni frame, outfit che mutano, auto che si trasformano a metà inquadratura, folle che si sciolgono, sfondi che cambiano stanza a ogni shot. "La consistenza degli asset separa l'AI slop amatoriale da un contratto da 10.000 $."

---
## 1. Character sheet
**Cos'è**: una "mappa a 360°" / "blueprint" del personaggio che blocca volto, altezza, proporzioni, outfit da ogni angolo. Da quel momento non descrivi più la faccia nei prompt: alleghi l'immagine.

### Ingredienti da dare a Claude
- **Selfie chiari** (meglio più selfie da angoli diversi, buona luce, tratti del viso ben visibili).
- **Riferimento outfit** (Pinterest: es. "avant-garde leather motor outfit", "woman in knight armor", streetwear).
- Eventuale riferimento di prodotto da indossare (occhiali Oakley gialli, ecc.).
- Richiesta in parole semplici.

### Richiesta-tipo (testuale di Kaye, spot iPhone)
> "Write me a three panel character sheet prompt of the girl in my selfie, full body, front portrait, and side profile. Keep my exact face, skin tone, and hair from the selfie, but put me in the outfit from the reference image. Clean white studio background and photo realistic."

Varianti usate:
- "Make a character sheet using photos 2 and 3, tag it as Kareema, and put her in the look from photo 1."
- "Here is my selfie. I want to create a character sheet from it for a medieval art scene. Three views, full body, front portrait, and side profile on a clean white studio background. Put me in a modest medieval dress… make it realistic."
- Per ricreare l'outfit esatto di un quadro: quadro + selfie chiaro.
- Personaggi senza riferimento: "Write me a character sheet prompt for a 75-year-old Asian grandmother with a high bun." / "a guy 25–30, street style, black sunglasses, punk red spike hairstyle."

### Anatomia di un buon prompt di character sheet
- NON descrive una scena: descrive un foglio di riferimento.
- **Layout**: Kaye usa più layout:
  - 3 pannelli: full body frontale, ritratto frontale, profilo laterale.
  - 2 pannelli: figura intera in piedi + close-up stretto dal petto in su (dà corpo e volto insieme).
  - **Trucco del layout (videoclip "Replica")**: full body frontale (sinistra), full body di schiena (centro), ritratto close-up (destra), con **entrambe le figure intere tagliate al collo**: così il volto compare solo nel close-up nitido. Motivo: quando il modello disegna una testa piccola in una figura intera, il volto esce sfocato/distorto e poi confonde il modello video.
- **Sfondo bianco/vuoto da studio** di proposito: niente elementi extra che confondano il modello video.
- **La parte più lunga = dettagli della pelle**: "fair skin with warm undertone, light freckles across the nose and cheeks, a few birthmarks". È ciò che rende il risultato reale invece che "generato".
- **Numeri specifici = consistenza**: età, peso, altezza ("German Shepherd, 5 years old, 35 kg, 65 cm at the withers, tennis ball in his mouth"). Parametri rigidi a cui ancorarsi → niente proporzioni strane.
- **Vincoli positivi** (cosa includere/seguire) e **vincoli negativi** (cosa evitare).
- Kaye usa **lo stesso prompt base** di character sheet in tutti i video: cambia solo l'outfit.

### Generazione
- Higgsfield → Images (o Cinema Studio → Image).
- Modello: **Seedream 5.0 Pro** (texture ultra-realistiche, pelle, zero "plastica", nitidezza grafica) — il suo preferito; **Soul 2.0** (pelle eccellente e molto economico, usato nello spot iPhone); **Nano Banana Pro** (alternativa).
- Input: selfie (+ outfit ref) come immagini di riferimento.
- Aspect ratio **16:9**, qualità **2K**, **batch 3–4** → confronta e scegli la "golden take" più somigliante. (Le immagini costano poco: qui il batch è OK.)
- Cuore ❤ su Higgsfield per salvare le migliori (la galleria si riempie in fretta).
- Itera in linguaggio naturale: "Actually she is a fighter now, not a villager. Swap the dress for… Keep everything else the same." / "Add the dark baggy Bermuda shorts with frayed edges, hands covered in suit gloves, pink web outlines."

### Varianti di stato (stesso personaggio, stati diversi)
- Pulito (flashback) vs con ferite e graffi (presente): stessa faccia, stesso cappello, stessi occhialoni.
- Invecchiamento: 4 sheet (6 anni, adolescente, 25 anni, anziana) → per tenere il volto identico tra le età, manda il selfie a Claude chiedendo di usare il riferimento del volto in ogni prompt + metti il volto come input in generazione.
- Animale sano vs infetto ("milky white clouded eyes with almost no pupil, burst blood vessels around the eyes, matted clumped fur with bald patches showing gray skin").
- Travestimento (Kaye nel completo della guardia del corpo con la maschera tolta).
- Trasformazione stilistica: "Take these four character sheets and transform them into matching LEGO minifigure character sheets. Keep their exact clothes, hair, glasses, and accessories, but adapt them to classic plastic minifigure proportions."

### Regola dei personaggi secondari
- **Se più persone ridono/si muovono nella stessa inquadratura, OGNI persona ha bisogno del suo sheet** (il fallimento del falò: solo lei aveva lo sheet → facce degli amici "slop"). Anche il cane.
- **Crowd sheet**: se la folla "si scioglie" e si muove come AI slop, crea uno sheet dedicato per la folla invece di combattere col prompt.
- Varietà di facce interessanti per i cast numerosi (17 sheet nello spot iPhone, 11 nello spot Oakley).
- Creature/mostri: sheet dedicato (Ciclope, robot con "eye sockets with glowing warm sensor lights" per un viso più espressivo).

### Soul ID (alternativa economica per il proprio volto)
Higgsfield → Soul ID → Create character → carica **molte** foto/selfie di alta qualità → dai un nome → training. Poi Soul 2.0 + il tuo avatar = il tuo volto **senza allegare riferimenti**. ~0,125 crediti contro ~2,5 di uno sheet su Seedream (≈20× meno). Si allena una volta per un'intera serie.

---
## 2. Location sheet ("il passo più importante e più trascurato")
Senza location sheet il personaggio "sta in una stanza diversa a ogni inquadratura".

### Due modi
1. **Da riferimento**: Pinterest o quadro → "Describe this background location with zero people in the frame." / "something similar to this".
2. **Dalla testa**: descrivi l'atmosfera. Esempi reali:
   - "Write me a prompt for an empty corner grocery store on a New York side street. Bright midday sun. Food stands outside. 35 mm cinematic style. No people in the frame."
   - "Early misty morning, no orange tint, poppy field with a foggy background, trees and hills fading into mist. The background should feel deep and layered."
   - "Top of a cliff right on the edge, strong wind, cloudy weather, a massive cliff 3,000 m high with jagged mountains all around."
   - "A vast, dramatic ocean cliff at dusk, stormy waves crashing against rocks below, misty fog hanging over the horizon."
   - Per un tunnel/gola stretta: schizzo → prompt location.

### Cosa deve contenere il prompt (Claude lo espande)
- Dettagli materiali/superfici (sono ciò che lo fa sembrare fotografato).
- **Luce** dettagliata: chiedi esplicitamente **cinematic lighting / hard shadows** — la luce morbida e nebbiosa è ciò che fa sembrare "sloppy" molti shot AI.
- **Attrezzatura camera/ottica** e look generale.
- **Negativi**: "no people, no pedestrians, no shopkeeper" → sfondo pulito dove inserire i personaggi; cosa evitare.
- **Blocco ottico/camera fisso** incollato alla fine di OGNI prompt location (la "ricetta segreta" di Kaye): impone distorsione anamorfica, color grading corretto, grana pellicola organica invece di levigatezza finta, profondità e caratteristiche dell'obiettivo realistiche. Template in `09-template-prompt.md`.

### Generazione
- Modello: **Soul Cinema** (ottimizzato per luce architettonica, ottiche reali, profondità naturale, grana pellicola, prospettive larghe; il modello immagine più economico della piattaforma, ~20× meno di alternative). Risultato "sembra uno still IMAX / un set vero".
- 16:9 (o 21:9 per look widescreen in Cinema Studio), 2K, batch 4 per scegliere lo sfondo migliore.
- Ancorare il mondo: tutte le location intorno a un luogo centrale (la casa di Kareema: soggiorno, cortile, camera, capanno… 9 location).
- Stessa location da più direzioni (corridoio backstage da due lati).

---
## 3. Model / prop / product sheet
"Come il character sheet tiene coerente un umano, il model sheet insegna all'AI le dimensioni esatte di un oggetto da ogni angolo."
- Prodotto: "Write me a prompt for a collage model sheet of this burgundy smartphone from front, back, and side angles on a white background." → **Seedream 5.0 Pro** (precisione grafica, dettagli nitidi, contrasto, strutture complesse), 16:9, batch 4.
- Auto: prima la versione neutra (F1 bianca), poi la versione brandizzata con il trucco del **wrap**: "Image 1 is an example of how I want my car wrapped, and image 2 is my car. I need a prompt where my car from image 2 gets wrapped and customized exactly like the one in image 1."
- Oggetti tenuti in mano dal personaggio: manda il character sheet a Claude → "a neat, refined sword and helmet suited to the girl and her costume."
- Plastica/LEGO (borchie, micro-riflessi): Seedream 5.0 Pro.
- Veicoli di scena (limousine nera oscurata), animali (toro, cavallo, gatto Bob, cane).
- Colore che "stacca": bici rosa acceso perché il meteo di montagna era cupo.

---
## 4. Quando NON servono gli sheet
Un singolo close-up stretto dove una foto di riferimento blocca già posa e angolo: basta riferimento + selfie + prodotto nel prompt box. "Sapere quando servono gli sheet e quando basta un riferimento è la differenza tra sprecare crediti e lavorare da pro." Nel dubbio, con più persone o movimento: fai lo sheet.

## 5. Gestione file
- Nomina ogni file sul computer (es. `char_kareema_clean.png`, `loc_shed.png`, `prop_iphone18_burgundy.png`).
- Chiedi a Claude di **taggare gli asset nei prompt con i nomi file esatti** / di dargli un titolo.
- Su Higgsfield carica tutto in **Elements** o nella cartella progetto di **Cinema Studio**: i nomi coincidenti fanno richiamare automaticamente gli elementi.
