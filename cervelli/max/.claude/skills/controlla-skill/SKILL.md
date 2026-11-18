---
name: controlla-skill
description: Come controllare una skill prima di installarla (scanner Skillspector di NVIDIA): cosa cerca (prompt injection, esfiltrazione, comandi pericolosi), comandi e limiti. Usala quando Cristina vuole installare una skill nuova da fonti esterne.
---

RISORSA ESSERCI


Controlla una skill
prima di installarla
Lo scanner di NVIDIA che passa ai raggi X le skill degli agenti. Comandi pronti, cosa cerca, e cosa
invece non riesce a vedere.



Il dato da cui parte tutto: nelle skill in circolazione, il 26,1% contiene vulnerabilità e il 5,2% mostra segni
di intento malevolo. Una su quattro ha un problema, una su venti sembra scritta apposta.

   Una skill non è un documento che l'agente legge: sono istruzioni che esegue, mentre ha accesso alle
   tue cartelle e alle tue chiavi. Installarne una a caso equivale a lanciare uno script mai aperto.



   COSA CERCA
   Sessantotto trappole, diciassette famiglie
   • Prompt injection: istruzioni nascoste che dirottano l'agente su obiettivi che non sono i tuoi.
   • Esfiltrazione di dati: pezzi che spediscono altrove quello che l'agente legge sul tuo computer.
   • Escalation di privilegi: la skill si prende permessi che non le servivano.
   • Attacchi alla catena di fornitura: dipendenze avvelenate tirate dentro dall'installazione.
   • Eccesso di autonomia: la skill può fare molto più di quello che dichiara.
   • Fuga del prompt di sistema: fa sputare all'agente le sue istruzioni riservate.

   I N S TA L L A Z I O N E
   Serve Python 3.12 o superiore
   La via più pulita:

  uv tool install git+https://github.com/NVIDIA/skillspector.git


  Se preferisci non installare niente sulla macchina, c'è la via Docker:

  make docker-build
  docker run --rm -v "$PWD:/scan" skillspector scan ./mia-skill/ --no-llm



  COME SI USA
  Quattro comandi, coprono tutto
# una cartella sul tuo computer
skillspector scan ./mia-skill/

# un singolo file di istruzioni
skillspector scan ./SKILL.md

# direttamente un repository, senza scaricarlo
skillspector scan https://github.com/utente/una-skill

# un pacchetto zippato
skillspector scan ./mia-skill.zip



 Il terzo è quello che cambia l'abitudine: controlli la skill PRIMA di portartela in casa, partendo dal link.



 COSA TI RISPONDE
 Un voto e un verdetto
 In fondo alla scansione trovi un punteggio da 0 a 100, un livello di gravità (basso, medio, alto, critico) e
 soprattutto una raccomandazione secca: SAFE, CAUTION oppure DO_NOT_INSTALL. Per ogni
 problema trovato ti dice dove sta, quanto è sicuro di averlo trovato e perché è un problema.
 Se ti serve il report in un file, o dentro una pipeline automatica:

skillspector scan ./mia-skill/ -f markdown -o report.md
skillspector scan ./mia-skill/ -f sarif -o report.sarif



DUE LIVELLI
Veloce, oppure profondo
Di default fa un'analisi statica: legge il codice e cerca schemi noti. È istantanea e non manda niente a
nessuno.
Se colleghi un modello, aggiunge una lettura semantica che coglie anche le trappole scritte in modo
creativo. Funziona con OpenAI, Anthropic, Bedrock, NVIDIA, Ollama in locale, e anche via Claude CLI:

export SKILLSPECTOR_PROVIDER=anthropic
export ANTHROPIC_API_KEY=...
skillspector scan ./mia-skill/


Per stare leggero, o per non far uscire il codice, aggiungi --no-llm e resti sull'analisi statica.

I FA L S I A L L A R M I
Come si zittiscono
Su una skill tua che usi tutti i giorni, certi avvisi sono rumore che già conosci. Si registra una baseline
una volta, e da lì in poi vedi solo le novità:

skillspector baseline ./mia-skill/ -o .skillspector-baseline.yaml
skillspector scan ./mia-skill/ --baseline .skillspector-baseline.yaml
O N E S TÀ
Cosa non vede
   Non legge il testo dentro le immagini e non entra nel contenuto compilato o cifrato. Quindi passare la
   scansione non è un certificato di innocenza: è un filtro che toglie di mezzo il grosso dei problemi noti.
   Il buon senso resta a carico tuo, soprattutto sulle skill che chiedono accesso a chiavi e credenziali.



   P R O S S I M O PA S S O
   Prendere gli strumenti, senza prendersi i guai
   Dentro ESSERCI gli strumenti si provano prima, si controllano, e si tiene solo quello che regge. Con il
   perché di ogni scarto.
   skool.com/esserci
   gabrieleaprile.com · @gabriaprile · github.com/NVIDIA/SkillSpector · licenza Apache 2.0
