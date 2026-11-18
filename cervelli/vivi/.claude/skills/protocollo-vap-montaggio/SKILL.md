---
name: protocollo-vap-montaggio
description: Guida di lavoro per montare i video della serie Protocollo V.A.P. (area LAVORO, Stefania): cartelle, progetto CapCut, script, regole di stile e procedura usate sul video 2, da adattare ai video successivi. Usala per ogni video V.A.P.
---

Protocollo V.A.P. — Guida per montare il video
4
Preparata il 26 ottobre 2026 dal lavoro sul video 2 ("Protocollo vap 2"). Serve a un altro profilo Claude
(o a Cristina) per rifare lo stesso lavoro, con le stesse regole e lo stesso stile, sul quarto video della
serie.

1. Come usare questa guida
   Cristina: apri il nuovo profilo Claude, collega il computer (vedi sezione 10), incolla il testo di
   00_PROMPT_PER_CLAUDE.txt e carica i file del video 4.
   Claude: leggi tutta la guida prima di toccare qualsiasi cosa. Gli script in scripts_video2/ sono la
   base del video 2: non sono uno strumento a un clic. Hanno nomi di file e percorsi scritti dentro e
   vanno adattati al video 4 (sezione 5).
   Nel video 2 le sigle pt1 , pt2 , pt3 sono le tre parti di registrazione di quel video, non il numero del
   video.

2. Il lavoro in una pagina
1. Preparare cartella di lavoro e progetto CapCut vuoto.
2. Abbinare ogni video della camera al suo audio del microfono e misurare lo sfasamento.
3. Tenere solo la voce principale (lei) e togliere la voce bassa dell'uomo che suggerisce.
4. Trascrivere, confrontare con lo script e tenere per ogni frase l'ultima ripresa corretta.
5. Costruire la timeline: video con camera muta + audio del microfono agganciato, con zoom irregolari.
6. Rivedere ogni taglio come lo sentirebbe chi guarda e correggere gli errori.
7. Aggiungere barra loghi, sottotitoli, grafiche, suoni degli errori e frecce.
8. Scrivere nel progetto CapCut (solo a CapCut chiuso, dopo il backup) e dire a Cristina quale progetto
   aprire.
9. Cristina controlla, segnala gli errori con i tempi della nuova timeline, si correggono e si riscrive.

3. Regole ferme (non si discutono)
   Lingua e tono: italiano, risposte brevi e oneste. Cristina lavora sotto pressione e spesso vicino al
   limite d'uso: niente giri di parole, messaggi di stato brevi durante i lavori lunghi.
   La voce dell'uomo non si deve MAI sentire, nemmeno una sillaba. Se hai dubbi su un pezzo,
   taglialo.
   Per ogni frase si tiene l'ULTIMA ripresa CORRETTA, non per forza l'ultima in assoluto. Se l'ultima ha
   inciampi, ripetizioni, false partenze o lei parla con qualcuno presente, si usa la precedente detta
   bene. Va controllato tutto il video, non solo i punti che Cristina segnala: "ce ne saranno altri".
   Si scrive nel progetto CapCut solo con CapCut chiuso (file .locked assente, draft_content.json
   con data di modifica stabile) e dopo che Cristina ha scritto "chiuso". Prima si fa sempre un backup.
   Se CapCut resta aperto, alla chiusura sovrascrive le modifiche.
   Download solo con il permesso esplicito di Cristina. Niente azioni finanziarie. Non usare sotto-
   agenti se lei non li chiede.
   Dille sempre quale progetto aprire e se la versione è già scritta. Nel video 2 ha chiesto "dove la
   trovo l'ultima versione?" perché non avevo ancora scritto e lei vedeva ancora i loghi sparsi.


                                        Protocollo V.A.P. · guida video 4 · pagina 1/5
   Non dire "fatto" per cose che non hai potuto verificare (per esempio come CapCut apre i nuovi
   elementi, o l'audio dei punti di taglio ascoltato davvero). Dillo chiaramente.
   Quando togli o aggiungi pezzi, tutti i tempi dopo si spostano. Dille la nuova durata e chiedile di
   segnalare gli errori con i tempi della nuova timeline.

4. Cosa serve per il video 4
Chiedere a Cristina (una volta sola, tutto insieme) quello che non si può indovinare:
   I video della camera (MP4) e i file audio del microfono (m4a) di ogni parte di registrazione, e quale
   audio va con quale video.
   Lo script con le note sulle grafiche (dove vanno, cosa mostrare). Esempio del formato:
    esempio_script_video2.txt .

   Quali loghi vanno nella barra (nel video 2: VAP, elo, EmerBuddy, Black Chamber) e come si scrivono i
   nomi (es. "Eloo").
   Il testo e il link vero per la chiamata all'azione e la schermata finale. Posti disponibili o scadenze solo
   se sono reali.
   Un progetto CapCut vuoto per il video 4, aperto almeno una volta in CapCut, così esiste già nella
   cartella dei progetti ( com.lveditor.draft ).
   Se esiste già un video 3 montato, usarlo come riferimento più recente dello stile.
Cartelle sul PC di Cristina (collegarle al nuovo profilo):
   Lavoro: Desktop\Contenuti\Progetti Marketing\ (qui c'è VAP_video2 , la libreria grafiche
    VAP_grafiche , i suoni VAP_sfx , e questo kit).
   Progetti CapCut: C:\Users\Cristina\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\ .
   Modello da cui si copiano segmenti, tracce e suoni: il progetto "PROTOCOLLO VAP SCRIPT 1" (video
   1) in quella cartella.

5. Passi, con gli script del video 2
Gli script stanno in scripts_video2/work/ (montaggio) e scripts_video2/grafiche/ (grafiche). Prima di
tutto: copia la cartella VAP_video2 come VAP_video4 (senza build , backup , audio e frames , che
pesano oltre 2 GB) e cambia in vap2_lib.py le costanti LIVE (nome del progetto) e WORK (cartella di
lavoro).
 Passo          Script (video 2)                            Cosa fa / cosa cambiare
 Sincronia       sync_probe.py , probe.py                   Trova l'offset tra microfono e camera. Nel video 2: camera =
                                                            mic + 15,1687 s (pt1), + 3,5196 s (pt2), + 2,2204 s (pt3), con
                                                            deriva −7,08 µs/s. Va rimisurato per le registrazioni nuove
                                                            (dizionario OFF in vap2_lib.py ).
 Voce bassa      segs_voices.py ,                           Distingue lei dalla voce bassa: livello microfono meno livello
                 probe_voices.py ,                          camera, a fotogrammi di 20 ms. Lei ≈ −2 dB, voce bassa ≈
                 cuts_step1.py                              −15 dB, soglia −8,5 dB. La registrazione ha questa struttura:
                                                            l'uomo dice la frase, poi lei la ripete.
 Voce bassa,     gccscan.py , gccfine.py ,                  Correlazione GCC-PHAT tra mic e camera: lei ≈ −0,6 ms, lui
 affinamento     vap2_cutman.py                             ≈ −16 ms. Serve a trovare i frammenti dell'uomo rimasti.
                                                            Elenco dei tagli in cut_list.json .




                                        Protocollo V.A.P. · guida video 4 · pagina 2/5
 Passo          Script (video 2)                            Cosa fa / cosa cambiare
 Trascrizione   transcribe.py ,                             faster-whisper (modello in models/whisper-turbo ). Il
                transcribe_chunk.py                         computer virtuale ha 2 CPU: ogni chiamata dura al massimo
                                                            circa 3 minuti e i lavori in background muoiono alla fine della
                                                            chiamata. Lavora a blocchi e fai ripartire da dove eri arrivato.
 Scelta dei     nlp.py , align.py ,                         Allinea la trascrizione allo script e sceglie l'ultimo take
 take           make_keep.py , units.py ,                   corretto. Esce cuts_final.json .
                chunks.py , qa_final.py

 Timeline       vap2_final.py , vap2_patch1.py              Crea video (camera muta) + audio del mic e gli zoom.
                                                             vap2_patch1.py dà un id locale diverso a ogni file e sposta
                                                            l'inquadratura verso il basso.
 Correzioni     vap2_edit.py                                Modifica i segmenti per indice con un controllo di sicurezza
                                                            (parte + file sorgente atteso): toglie, accorcia, sostituisce.
                                                            Scrive in build/edit_<ora>/ .
 Diagnosi       segasr.py , livewin.py ,                    Vedi sezione 7.
                showwin.py , joinasr.py ,
                winasr.py , gaps.py

 Mappa tempi    make_warp.py                                Calcola grafiche/warp.json , che collega il tempo
                                                            "originale" al tempo reale della timeline dopo i tagli.
 Grafiche       grafiche/scenes_v2.py ,                     Le scene sono nella lista SCENES (nome, inizio, durata,
                gfx_lib.py , gfx_extra.py ,                 funzione). run_gfx.py le rende a pezzi, riprendibile, circa
                run_gfx.py , fit.json                       140 s per chiamata.
 Rifinitura     vap2_deco.py                                Ricostruisce tutte le tracce che iniziano per VAP2 : barra,
                                                            loghi, grafiche, suoni, frecce, sottotitoli. Si può rilanciare
                                                            quante volte vuoi. SRC=<cartella> sceglie la base;
                                                             WRITE=1 scrive nel progetto vivo.

Ordine consigliato per ogni giro di correzioni: vap2_edit.py → make_warp.py (con SRC = cartella edit)
→ run_gfx.py (con FORCE=1 se i tempi sono cambiati) → vap2_deco.py (con SRC = cartella edit, WRITE=1
solo a CapCut chiuso).

6. Stile da rispettare
   Tela: 1920×1080, 30 fotogrammi al secondo. Camera muta (volume 0), audio dal microfono su
   traccia separata.
   Tagli: solo parlato, nessuna pausa lunga. Le false partenze si tolgono.
   Zoom irregolari tra 1,05 e 1,35, soprattutto 1,15 e 1,20, mai due clip di fila quasi uguali (nel video 2:
   valori [1.05 … 1.35] , pesi [1,2,4,4,2,1,1] , differenza minima 0,05). L'inquadratura scende con
    transform.y = −0,9 × (zoom − 1) perché la testa non esca mai dall'inquadratura.

   Barra loghi IN BASSO (nel video 1 era in alto), con 4 loghi equidistanti: margini uguali di 240 px e
   spazi uguali di 321,7 px. Posizioni x del video 2: VAP −0,702, elo −0,2696, EmerBuddy 0,1430, Black
   Chamber 0,628, y circa −0,93. La barra sparisce quando c'è una grafica a tutto schermo.
   Sottotitoli: font Poppins, bianchi, con ombra, y = −0,8, animazione "Lettera per lettera", larghezza
   massima 0,82. Vanno corretti i nomi: il partner è "Eloo" (la trascrizione automatica scrive "Hello");
   "V.A.P." con i punti; "AI Act". L'elenco delle correzioni automatiche è la lista FIX in vap2_deco.py .
   Grafiche: solo dove lo script le indica. Sfondo bianco a quadretti, Poppins Black / ExtraBold, entrata
   "glitch", icone nere. Scala massima 0,88. Centrate sull'asse x = 960: i riquadri di fit.json devono




                                        Protocollo V.A.P. · guida video 4 · pagina 3/5
   essere simmetrici ( a = min(x0, 1920 − x1) ). Tra una grafica e la successiva niente fotogrammi vuoti
   (si chiudono i buchi fino a 12 fotogrammi).
   Suoni degli errori: sfx_negativo_v1.wav su ogni X rossa, sfx_negativo_forte_v1.wav sulla prima
   scritta barrata di ogni scena, 0,05 s prima dell'evento. Gli eventi sono in grafiche/sfx_events.json
   (si generano con sfx_events.py ). I file audio sono in VAP_sfx e nel progetto modello.
   Frecce verdi: all'espressione "il link qui sotto" compaiono due frecce verdi che puntano verso il
   basso, una a destra e una a sinistra, per circa un minuto, con rimbalzo (immagine
    assets/freccia_verde.png , scala 0,21, x ±0,58, y tra −0,02 e −0,20 ogni 0,45 s). Vanno sopra di lei.
   "Madrina" non c'è più nella serie.

7. Come trovare gli errori (la parte che sbagliamo di più)
Nel video 2 il primo montaggio conteneva errori che io non avevo visto e che Cristina ha sentito: una "e"
in più, una frase fuori onda, "per gestire contatto" dopo "per gestire i contatti caldi", false partenze, lei
che parlava con una persona presente ("Volevo dire così…"), "sempre, sempre", frasi di preparazione
ripetute, "prima di qualsiasi" detto due volte e "gli gli".
    Non fidarti delle parole con i tempi di Whisper: sbagliano di circa 0,5 s e cancellano le false
    partenze. Una trascrizione "pulita" non dimostra che l'audio lo sia.
    Metodo che funziona, in ordine: 1. segasr.py parte inizio fine — trascrive il microfono per tratti di
    parlato (separati da silenzi). Mostra tutti i take di una frase. 2. livewin.py / showwin.py — trascrive
    ogni pezzo della timeline montata, con silenzio fra un pezzo e l'altro. 3. joinasr.py / winasr.py —
    trascrive il montato contiguo, come lo sente chi guarda: qui si vedono parole doppie e frasi spezzate
    nei punti di giunzione. 4. gaps.py — controlla pause e frammenti molto corti.
    Controlla in particolare: la fine di ogni pezzo (parole finali di un take sbagliato), l'inizio (false
    partenze), le giunzioni (parole raddoppiate), i pezzi sotto 0,5 s, le frasi dette a chi è presente in
    studio.
    Dopo ogni correzione, ritrascrivi la zona contigua per verificare che si legga bene.
    Ai bordi di una zona corretta i sottotitoli automatici lasciano parole sparse ("Lui", "E", "La"). Si risolve
    riscrivendo a mano i sottotitoli dell'intera zona e allargandola ai pezzi vicini ( PATCH in vap2_edit.py ,
    che produce patch_windows.json per vap2_deco.py ).
    Ricorda che l'ASR non vede tutto: nel messaggio finale a Cristina elenca i punti da riascoltare a
    orecchio.

8. Errori già fatti (non ripeterli)
   Scrivere con CapCut aperto: alla chiusura il programma sovrascrive tutto. Controlla .locked e
   aspetta "chiuso".
   Stesso local_material_id per video diversi: le anteprime sono sbagliate. Ogni file ha un id locale
   univoco ( vap2_patch1.py ).
   Ricostruire dal backup quando lei ha già modificato la bozza: cancelli il suo lavoro. In quel caso
   modifica sul posto.
   Quattro copie del draft: draft_content.json , template-2.tmp , Timelines/<id>/draft_content.json ,
   Timelines/<id>/template-2.tmp devono essere identiche (lo script lo verifica).

   Grafiche non centrate (es. la panoramica "TRIAGE" spostata a destra): riquadri simmetrici in
   fit.json .

   Barra loghi con spazi diversi e tracce sovrapposte: le posizioni x esatte stanno in POS di
   vap2_deco.py .

   Parole sparse nei sottotitoli dopo un taglio: vedi sezione 7.


                                         Protocollo V.A.P. · guida video 4 · pagina 4/5
   Dire che è "l'ultima versione" senza dire dove: nomina sempre il progetto da aprire.
   Promettere che CapCut accetti elementi nuovi (frecce con rimbalzo, traccia dei suoni) prima che lei
   l'abbia aperto: nel video 2 non era ancora stato verificato. Chiedile se si vedono.

9. Controllo finale prima di dire "pronto"
   ☐ Nessuna voce dell'uomo (riascolta tutti i punti dove lui e lei si sovrappongono).
   ☐ Ogni frase ha l'ultima ripresa corretta; nessuna parola doppia; nessun frammento fuori onda.
   ☐ Tutti i sottotitoli leggono bene; "Eloo"; niente parole sparse.
   ☐ Barra loghi in basso, loghi equidistanti, sparisce durante le grafiche.
   ☐ Grafiche solo dove lo script le chiede, centrate, senza buchi tra l'una e l'altra.
   ☐ Suoni degli errori sulle X rosse e sui testi barrati.
   ☐ Frecce verdi da "il link qui sotto" fino alla fine.
   ☐ Chiamata all'azione e schermata finale con link e dati veri (non inventare mai posti o scadenze).
   ☐ Quattro copie del draft identiche, check() senza errori, durata finale riportata a Cristina.
   ☐ Hai detto a Cristina quale progetto aprire, la nuova durata, cosa non hai potuto verificare e cosa
   riascoltare.

10. Avviare il nuovo profilo
1. Sul computer di Cristina apri l'app Claude desktop con il nuovo profilo e avvia un nuovo task.
2. Scegli "Collega a questo computer" e dai accesso a Desktop (almeno Contenuti\Progetti
   Marketing ) e alla cartella dei progetti CapCut ( com.lveditor.draft ).
3. Incolla il testo di 00_PROMPT_PER_CLAUDE.txt e indica la cartella KIT_VAP_PARTE_4 .
4. Metti i file del video 4 (MP4, m4a, script) in una cartella nuova, per esempio VAP_video4\originali , e
   dillo a Claude.
5. Il nuovo profilo non vede i documenti dell'altro profilo (progetto "AGENTE CAPCUT", chat
   precedenti): tutto quello che serve sta in questo kit.

11. Limiti da conoscere
   Gli script sono costruiti sul video 2: nomi di file, numero di parti, scene grafiche e risincronizzazione
   sono suoi. Vanno adattati, e questo richiede ore di lavoro, non minuti.
   Il computer virtuale è lento (2 CPU): trascrivere 25 minuti di registrazione richiede molte chiamate a
   blocchi.
   Gli errori di ripresa che la trascrizione non mostra (intonazione, pause, respiri) si trovano solo
   riascoltando. Cristina li segnala meglio di qualsiasi script: usa i suoi tempi.
   Per il video 4 serve ancora la chiamata all'azione: link e dati reali vanno chiesti a Cristina.
Fonte: lavoro svolto dal 21 al 26 ottobre 2026 sul progetto CapCut "Protocollo vap 2".




                                         Protocollo V.A.P. · guida video 4 · pagina 5/5
