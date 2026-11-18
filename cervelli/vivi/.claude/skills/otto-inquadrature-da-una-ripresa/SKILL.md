---
name: otto-inquadrature-da-una-ripresa
description: Metodo per ricavare nuove inquadrature (orbita, dall'alto, allontanamento) da un unico video a camera fissa con Seedance su KIE, mantenendo parlato e labiale: prompt, parametri e costi reali. Usala per dare varietà di angoli ai video parlati.
---

RISORSA ESSERCI




Una ripresa sola,
otto inquadrature
Il procedimento esatto per rigirare un piano fisso da angoli che non hai mai
ripreso. Col prompt vero, il parametro che ti frega, e il conto che dice quale delle
due strade conviene a te. Misurato su un video fatto, non su una guida letta.




Questo metodo prende un video girato una volta sola, con la camera ferma, e ne tira fuori altre
inquadrature: la camera che orbita, che sale sopra la testa, che si allontana. La persona non rifà
niente: parlato, labiale, espressioni e gesti restano quelli del girato originale, cambia solo il
punto di vista. Serve un modello video che accetti un video di riferimento, e qui è stato usato
Seedance 2.5 su KIE.


    Tutti i numeri di questa guida sono misurati su una lavorazione vera, finita e pubblicata.
    Nessuno è stimato dal listino: dove c’è una cifra, quella cifra è stata pagata.




UNO

Le due strade, e il conto che le separa
Generazione unica — un colpo solo
Mandi il video intero con dentro la scaletta a tempi, e il modello ti restituisce tutto già montato.
I tagli non stonano fra loro perché li fa la stessa generazione. Ma gli stacchi li decide lui: sul
nostro video il primo cade preciso (+0,26 secondi dal punto chiesto), gli ultimi arrivano fino a
due secondi dopo.

Segmenti separati — una generazione per inquadratura
Il taglio lo decidi tu, al fotogramma. Ogni pezzo paga un minimo di cinque secondi anche se ne
dura due, quindi il primo giro costa un po’ di più. Ed è proprio quel minimo piccolo a rendere
quasi gratis una modifica.

Il consiglio che si legge ovunque, e che avevamo scritto anche noi, è: parti dalla generazione
unica perché costa meno. Ecco il conto vero.




                                                                                                       1/7
    UN GIRO COMPLETO, senza ripensamenti
      generazione unica        $11,21
      sette segmenti           $11,97


    POI, PER OGNI MODIFICA
      unica: si rifà tutto          $11,21
      segmenti: solo il pezzo        $1,71


      0 modifiche     unica 11,21    segmenti 11,97     -> unica, per 0,76
      1 modifica      unica 22,42    segmenti 13,68     -> SEGMENTI, per 8,74
      2 modifiche     unica 33,63    segmenti 15,39     -> SEGMENTI, per 18,24
      3 modifiche     unica 44,84    segmenti 17,10     -> SEGMENTI, per 27,74




    Il vantaggio della generazione unica è settantasei centesimi, e sparisce al primo
    ripensamento. Non conviene "fino a un certo punto": conviene solo se non cambi niente.



•   Il motivo è che nella strada unica il ritocco non esiste. Non rifai tre secondi: rifai trenta. Chi
    arriva dal montaggio normale non se lo aspetta, perché lì si cambia sempre un pezzo solo.
•   Quindi la domanda per scegliere non è quanto sei bravo, è: quanti passaggi di
    approvazione ha il tuo lavoro? Se lo guardi solo tu e sai già cosa vuoi, generazione unica. Se
    lo vede un cliente, un socio o chiunque possa dire "cambiamo questa cosa", segmenti.


DUE

Il prompt, in tre blocchi
Il prompt che funziona ha tre parti, in quest’ordine. Lo lascio in inglese perché è la lingua in cui è
stato dato al modello: tradurlo cambia i risultati.

Blocco 1 — la regola: cosa può cambiare e cosa no


    @video1 is the source performance, a single locked
    static shot. Re-shoot this exact performance from new
    camera viewpoints. Everything the person does comes
    from @video1 and matches it frame for frame: speech,
    lip movements, expressions, gestures, body motion,
    timing. Nothing is re-performed and nothing is added
    to the person: only the camera changes. Same person,
    same face, same clothing, same room, same lighting.



Blocco 2 — le parole esatte che si sentono
Si incolla il parlato per intero, nella lingua originale, in ordine. Non è una didascalia: serve al
modello per tenere il labiale agganciato.



                                                                                                         2/7
Blocco 3 — la scaletta, una riga per inquadratura


    SHOT LIST. Cut to a new camera exactly at these times:


    00.0-03.2   Handheld frontal medium-wide, pushing in with
                the natural sway of walking.
    03.2-07.1   Handheld low angle from slightly right,
                drifting laterally, breathing movement.
    07.1-09.3   Handheld birds-eye from directly overhead,
                floating and correcting slightly.
    09.3-11.9   [la riga della formica: vedi sezione dopo]
    11.9-17.2   Aerial drone: starts elevated and angled down,
                climbs and pulls away, live drone sway.
    17.2-20.6   Handheld tight close-up, slightly below eye
                level, orbiting about 30 degrees.
    20.6-24.4   Handheld three-quarter from the left, moving
                laterally with the operator steps.
    24.4-29.2   Handheld wide of the room, floating slowly
                backwards, gentle sway.


    Each cut is a hard cut between two cameras.
    No transitions, no fades, no text, no graphics.



•   L’ultima riga conta quanto le altre: senza, il modello mette dissolvenze e a volte scritte.
•   Sulla camera a mano diciamo come abbiamo fatto, perché non abbiamo provato altro:
    l’abbiamo chiesta in due posti insieme, un blocco in cima (EVERY SHOT IS HANDHELD,
    there is no locked-off camera anywhere) e la parola Handheld su sette righe di scaletta su
    otto, esclusa quella del drone che è aerea. Ha funzionato al primo colpo. Se basti uno dei
    due da solo non lo sappiamo: non l’abbiamo verificato.


DUE E MEZZO

La riga che decide un piano, e come si sbaglia
Il tratto in cui compare un elemento nuovo va scritto con più cura di tutti. La prima versione
diceva "macro sulla scrivania, poca profondità di campo": il modello ha eseguito alla lettera, e
la persona dietro è diventata una macchia scura irriconoscibile. Non aveva sbagliato lui.


    "Poca profondità di campo" non basta mai da sola. Va detto cosa resta a fuoco E cosa deve
    restare leggibile anche se sfocato. Quello che non nomini, sparisce.



Questa è la versione che ha funzionato, ed è quella che ha prodotto il video:




                                                                                                   3/7
    09.3-11.9    Handheld low shot close to the desk surface.
    A small electronic ant walks across the desk, weaving
    between the objects: matte dark metal body, faint warm
    indicator lights, thin articulated legs, moving like a
    real insect. THE CAMERA FOLLOWS THE ANT as it moves.
    Behind it, the man stays clearly visible in frame and
    KEEPS TALKING throughout: he is softly out of focus but
    still readable, his mouth moving and his hands gesturing
    exactly as in @video1. Moderate depth of field, not
    extreme: the ant is sharp, the man behind is soft but
    recognisable and evidently speaking. The ant is the only
    new element in the whole video.



•   Le tre cose che la fanno funzionare: dire che la camera SEGUE l’oggetto nuovo, dire che la
    persona resta in campo e continua a parlare, e scrivere "moderate depth of field, not
    extreme" al posto di "very shallow".


TRE

Il parametro che ti frega

    reference_video_urls : [ url del tuo girato ]
    resolution              : 720p
    aspect_ratio            : 16:9
    duration                : 30        <-- QUESTO




      `duration` ha come valore di partenza 5. Se non lo passi, ricevi un video di cinque secondi e lo
      paghi come tale. Non è scritto nella scheda del modello: si vede solo aprendo il playground.



•   A noi quella dimenticanza è costata 6,17 dollari in un colpo solo.
•   Altro inciampo: l’identificativo del modello va scritto per intero, `bytedance/
    seedance-2-5`. Da riga di comando gli alias funzionano, da dentro il codice no.
•   Il conto si fa su ingresso più uscita, non solo sui secondi generati: un pezzo da tre secondi si
    paga come sei. E i secondi si arrotondano per eccesso, con un minimo di cinque in uscita.


Q UAT T R O

Cosa NON serve: la scheda personaggio
Le guide in giro dicono di costruire prima una scheda del personaggio, cioè un’immagine con
più viste del viso, e di passarla al modello. Provata due volte: ha prodotto due persone diverse
dal soggetto vero, barba più chiara e viso più magro.



                                                                                                         4/7
    Una scheda sbagliata è peggio di nessuna scheda, perché il prompt dice al modello di
    prendere l’identità del viso da lì. Senza, la prende dal video di riferimento, che contiene la
    persona vera. Il volto ha tenuto.




CINQUE

Quanto costa davvero, in tre voci
Il video che hai visto è costato undici dollari e ventuno. Arrivarci ne è costati quarantaquattro e
cinquantacinque. La differenza però non è tutta apprendimento, ed è più utile spaccarla:


   errori evitabili leggendo una guida           $17,38
     la strada sbagliata provata prima
     il parametro duration dimenticato


   modifiche volute dopo aver visto              $22,42
     due giri interi, uno per ogni cambio


   la generazione buona finale                   $11,21
   ----------------------------------------------
   totale speso                                  $44,55




    Una guida ti fa risparmiare gli errori, non i ripensamenti.



I 17 dollari della prima voce questa guida te li toglie: sono cose che ora sai. I 22 della seconda
no, perché nascono dal guardare il risultato e volerlo diverso, che è una cosa sana e capita
quasi sempre. Ed è esattamente per questo che la scelta della strada, all’inizio, pesa più del
prompt.


    Prezzi di settembre 2026, listino marcato beta. Prima di fare conti seri, ricontrolla.




CINQUE E MEZZO

Controlla cosa c’è dopo l’ultima parola
Il modello non restituisce solo le immagini: restituisce anche l’audio, ri-sintetizzato. E in coda al
nostro video ci aveva messo una frase che la persona non ha mai detto, due decimi di secondo
dopo l’ultima parola vera. Un “grazie per la visione” che nessuno aveva scritto.




                                                                                                        5/7
      Se monti usando l’audio della generazione, quella frase finisce nel video pubblicato. Se usi
      l’audio del girato originale non si sente nemmeno, ed è il motivo per cui conviene tenere
      l’audio vero e usare il generato solo per le immagini.



•     Il controllo dura dieci secondi: trascrivi il video generato e guarda cosa c’è dopo l’ultima
      parola del tuo copione. Se c’è qualcosa, taglialo.
•     Attenzione a un segnale che inganna: in quella coda la trascrizione dava a tutte le parole lo
      stesso istante, che di solito è il marchio di una parola immaginata dal riconoscitore. Lì
      invece il suono c’era davvero, misurato. Quindi non fidarti del solo timestamp: ascolta.


SEI

La regola per chi scrive il testo
Questa è la parte che non trovi nelle guide, e che vale più del prompt.


      Con la generazione unica il copione NON deve nominare i movimenti di camera. Gli stacchi li
      decide il modello e slittano: la parola arriva sopra l’inquadratura precedente.



Sul nostro video, con una prima stesura che li nominava, sarebbe successo questo:


    «la camera mi gira intorno»        orbita a 7,29s       ok
    «sale e mi guarda da sopra»        alto   a 10,67s     1,39s di ritardo
    «si stacca e apre la stanza»       drone a 13,29s      1,44s di ritardo



•     Due righe su tre avrebbero avuto la parola sopra l’inquadratura sbagliata per quasi un
      secondo e mezzo. È l’errore che nessuno sa spiegare e tutti sentono.
•     Se il tuo testo deve chiamare i movimenti per nome, ti serve la strada a segmenti. È una
      scelta di scrittura che dipende dalla strada, e va fatta prima di scrivere.
Una nota su come ci siamo arrivati, perché è più utile della regola: nel nostro caso il copione è
stato alleggerito per una ragione di ritmo, non per questo problema, che non conoscevamo. La
scelta giusta è arrivata da una richiesta che parlava d’altro. Capita più spesso di quanto sembri,
e conviene accorgersene.


E ADESSO

Dove si impara a farlo sul serio
Questa è una ricetta sola, misurata su un lavoro solo. Quello che la rende ripetibile è il metodo
che ci sta sotto: sapere quale strada scegliere prima di partire, scrivere il prompt dicendo
anche quello che deve restare, e tenere il conto di quanto costa davvero invece di quanto
dovrebbe costare.



                                                                                                      6/7
È esattamente quello che facciamo dentro Magia Creativa 2.0: si smontano i lavori veri, coi
numeri davanti e senza saltare la parte in cui qualcosa non funziona.



    P R O S S I M O PA S S O

    Magia Creativa 2.0
    Qui hai visto come si fa una cosa. Dentro Magia Creativa si impara a farne altre: si smontano
    i lavori veri, coi numeri davanti e senza saltare la parte in cui qualcosa non funziona.



        Magia Creativa 2.0




gabrieleaprile.com · @gabriaprile · metodo verificato su una lavorazione reale, settembre 2026




                                                                                                    7/7
