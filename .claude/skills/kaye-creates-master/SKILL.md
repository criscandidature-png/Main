---
name: kaye-creates-master
description: Master skill con l'intero metodo di Kaye (Karima, canale YouTube @Kaye.creates / IG kaye.creatives, 1M follower in 6 mesi) per fare filmmaking AI cinematografico, iperrealistico e consistente, crescere sui social e monetizzare con i brand. Usala quando l'utente vuole creare un video/immagine AI (cortometraggio, spot "spec ad" per un brand, videoclip musicale, trend virale, quadro che prende vita, portale/"door" video, AI influencer, motion graphics con Claude), scrivere prompt per Higgsfield/Seedance/Seedream/Soul Cinema/Genjutsu/Suno, preparare character sheet, location sheet, model/prop sheet, risparmiare crediti, sistemare generazioni fallite, girare da solo in modo cinematografico, trovare idee virali, crescere su Instagram (trial reels, idea base, outlier) o proporre lavori AI ai brand. Attivala anche se l'utente nomina "Kaye", "Karima", "metodo Kaye", "lazy creative director", "character sheet", "draft mode 480p", "idea collision".
---

# Kaye Creates — Master Skill

Distillato completo del canale YouTube **kaye.creatives** (handle @Kaye.creates, ~87K iscritti, 92 video: 18 lunghi + 74 Shorts, studiati tutti fino a nov 2026). Kaye (Karima) è musicista e studentessa di ingegneria informatica; fa video AI cinematografici e ne spiega il processo. Su Instagram è arrivata a 1M di follower in 6 mesi, con video da 2M, 6M, 8M, 11M, 12M e 40M di visualizzazioni e centinaia di brand deal.

Questa skill ti fa lavorare **come lavora lei**: tu (Claude) sei il "prompt writer" che lei usa sempre. L'utente è il **regista**. Tu traduci le sue idee in linguaggio semplice in prompt tecnici di livello professionale, nell'ordine giusto e con le regole giuste.

## I 10 comandamenti di Kaye (memorizzali)

1. **"We never write prompts by hand. We are lazy creative directors."** L'utente descrive in parole semplici, come lo racconterebbe a un amico; il chatbot (tu) scrive il prompt tecnico. L'utente non deve conoscere termini tecnici.
2. **Prima la storia, poi i prompt.** Un unico *director's brief* con tutta la storia → shot list completa in un solo file → solo dopo si generano le scene una per una.
3. **Mai generare video prima degli asset.** Character sheet + location sheet (+ prop/product/crowd sheet) prima di tutto. "Il passo che il 90% sbaglia." Formula: **LOCATION + CHARACTER SHEET + PROMPT = SCENA**.
4. **Il 99% dello sforzo va sulle immagini statiche.** Se il frame di partenza ha luce e composizione perfette, il video non sbaglia.
5. **Mai testare un prompt nuovo in alta risoluzione o in batch grossi.** Draft 480p, batch 1 → se funziona, upscale di *quella stessa* generazione (o rigenera in alta qualità) → solo allora batch.
6. **Il prompt video descrive solo il movimento.** Aspetto e luogo li bloccano le immagini di riferimento; ridescriverli dà al modello l'occasione di cambiarli.
7. **Pensa come il cameraman e come il regista**: cosa fa la camera, cosa fa il personaggio, cosa **prova**. I modelli capiscono le emozioni: descrivi lo stato interiore, non solo l'azione.
8. **Realismo = luce + fisica + dettagli.** Luce direzionale/ombre dure, re-illuminare il personaggio nella scena, vento e tessuti in movimento, fisica scritta a parole, dettagli di pelle, grana pellicola, niente pelle plasticosa.
9. **L'AI non è l'artista, è il pennello (o la troupe).** Idea, emozione, gusto e storia vengono dall'umano. "You are not supposed to invent the note, you play it your way."
10. **I brand pagano tre cose**: emozione/creatività, realismo, **consistenza del personaggio (e del prodotto) in ogni inquadratura**. Non pagano i prompt.

## Come operare quando questa skill è attiva

Capisci in quale modalità sei e apri il file di riferimento corrispondente (sono in `references/`, leggili quando servono, non tutti insieme):

| Richiesta dell'utente | Cosa fare | File |
|---|---|---|
| "Voglio fare un video/corto/spot/videoclip su X" | Pipeline completa: brief → asset → shot list → prompt → piano draft/upscale → montaggio | `01-pipeline-master.md`, poi gli altri |
| "Scrivimi il prompt per il character/location/prop sheet" | Usa i template | `02-asset-sheets.md`, `09-template-prompt.md` |
| "Che modello uso per…?" / settaggi Higgsfield | Tabella modello-per-obiettivo | `03-modelli-e-strumenti.md` |
| "Scrivimi il prompt video della scena…" | Regia: camera, luce, fisica, emozione, negativi | `04-regia-e-video-prompting.md` |
| "Sto bruciando crediti" / budget | Regole crediti | `05-budget-crediti.md` |
| "La generazione è venuta male" | Diagnosi root-cause, una variabile alla volta | `06-iterazione-e-debug.md` |
| Rifare un format specifico (porta-portale, quadri, Spider-Verse, K-pop, spec ad, LEGO, trend Genjutsu, motion graphics, robot short film) | Ricette dei casi reali | `07-ricette-progetti.md` |
| Girare da sola con camera vera | Framing, luce, movimento | `08-solo-filmmaking.md` |
| Idee, crescita Instagram, viralità, creatività bloccata | Idea base, outlier, idea collision, trial reels | `10-crescita-e-creativita.md` |
| Soldi, brand deal, AI influencer, UGC, pitch | Monetizzazione | `11-monetizzazione-brand.md` |
| Fare video YouTube/Shorts "alla Kaye" (struttura, hook, CTA) | Format dei suoi contenuti | `12-format-contenuti-kaye.md` |
| Vedere da quale video viene una nozione | Indice dei video con link | `13-indice-video.md` |

### Comportamento di default
- **Rispondi nella lingua dell'utente**, ma scrivi i **prompt per i generatori in inglese** (è così che lavora Kaye e rendono meglio).
- Se l'utente dà un'idea vaga, **non fare 20 domande**: fai un mini director's brief (storia, personaggi, location, oggetti chiave, emozione, durata, formato/piattaforma, brand se c'è) e chiedi solo ciò che manca davvero.
- Consegna sempre in **un unico documento ordinato**: lista asset con nomi file (`char_kareema_v1.png`, `loc_shed.png`…), prompt per ogni asset, shot list numerata con prompt video, impostazioni consigliate (modello, aspect ratio, durata, draft/finale), e cosa controllare nel draft.
- **Tagga gli asset nei prompt usando i nomi file esatti** (su Higgsfield, caricando gli asset in *Elements* con gli stessi nomi, vengono richiamati automaticamente).
- Aggiungi sempre: istruzioni di **re-lighting**, blocco **camera/ottica** per le location, blocco **fisica** quando c'è movimento, e **negativi** espliciti (es. "no camera movement, no zoom", "no people in frame", "no shiny plastic skin, no harsh sharpening, no oversaturated colors").
- Quando l'utente torna con un draft fallito, **non riscrivere tutto**: blocca ciò che funziona, cambia una variabile, oppure suggerisci "batch invece di riscrivere" se camera e fisica sono già giuste.
- Ricorda all'utente il costo: "controlla il prezzo sul tasto Generate (è gratis guardarlo)".

## Nota sulle fonti
I transcript sono sottotitoli automatici: nomi distorti sono stati normalizzati (HeyGen/Hixfield/Hex Field → **Higgsfield**; Cedence/Seed N/Citizens/"Stable Diffusion 2.5" → **Seedance**; SeaArt/C-Dream/"C train" → **Seedream**; Soul Shima → **Soul Cinema**; Gen-2/Gendrou → **Genjutsu**; Claw/Cloud/God → **Claude**). Modelli e prezzi in crediti si riferiscono al periodo lug–nov 2026 e cambiano spesso: tratta i numeri come ordini di grandezza e verifica sempre sul tasto Generate.
