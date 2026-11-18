# Progetto Team Bot di Cristina – passaggio di consegne
Questa cartella contiene il team di bot Telegram di Cristina. Leggi tutto prima di agire.
Parla con Cristina in italiano, in modo semplice e breve: non è una programmatrice.

## Cosa c'è
- `pcbot/` – programma Python che avvia 3 bot Telegram nello stesso processo (`python -m pcbot.main`):
  - **Max** (`pcbot/bots/max.py`): assistente personale – promemoria, to-do, note, diario, Notion (tutto il Notion tramite il connettore dell'account Claude), controllo PC (`pcbot/modules/`), insegnante di inglese (`pcbot/english.py`), `/aggiorna` (`pcbot/updater.py`).
  - **Vivi** (`pcbot/bots/vivi.py`): video editor – riceve video, area Lavoro/Personale, montaggio automatico con `videoedit/editor.py`, `/crea` (video da codice con Claude Code), chat libera.
  - **Jess** (`pcbot/bots/jess.py`): social media manager – caption, hook, script, piano editoriale (anche su Notion), promemoria di pubblicazione.
- `pcbot/ai.py` – testo AI: API Claude se c'è ANTHROPIC_API_KEY, altrimenti Claude Code (`claude -p`, abbonamento di Cristina), altrimenti Gemini. Regole di stile (risposte brevi, niente asterischi) + pulizia markdown.
- `pcbot/brain.py` – "cervello" di ogni bot in `cervelli/<bot>/` (CLAUDE.md = memoria, `.claude/skills/` = skill). Da Telegram: /impara, /memoria, /dimentica, /skill.
- `pcbot/team.py` – bacheca del team: le bot si passano il lavoro con [[PASSA:nome:testo]] e si rispondono (max 3 giri). /team, /passa.
- `pcbot/menu.py` – menu fisso a pulsanti per ogni bot; nei gruppi rispondono solo se chiamate.
- `videoedit/` – editor video (Whisper + Claude + FFmpeg). Profili in `videoedit/profili/`: lavoro (Stefania Salvatore, La Madrina dell'Accoglienza: giudice, testimonial, evento, fiera, youtube) e personale; `personale/adv` = reel di vendita con parole chiave ARANCIONI #FF7A1A e formato 4:5 (solo ADV). Testi sempre nella safe zone e mai sul viso (rilevamento volti OpenCV <5).
- `avvia.bat` – avvia il team e lo riavvia da solo se si ferma; `avvio_automatico.bat` – avvio a ogni accensione; `collega_claude.bat` – login Claude Code.
- `.env` – token Telegram (MAX_TOKEN, VIVI_TOKEN, JESS_TOKEN), ALLOWED_USERS, FILES_ROOT, eventuali chiavi. NON mostrarlo e NON caricarlo su GitHub.
- `data/` – promemoria, to-do, progressi di inglese, bacheca del team (locale, non su GitHub).

## Dove si trova sul PC
`C:\Users\Cristina\Desktop\TEAMBOT\Main-claude-peaceful-tesla-n6m87j`, ambiente Python in `..\venv`.
Codice su GitHub: repo `criscandidature-png/Main`, branch `claude/peaceful-tesla-n6m87j` (repo PUBBLICO: niente materiali privati di Stefania o libri protetti).

## Comandi utili
- Avviare: doppio clic su `avvia.bat` (oppure `..\venv\Scripts\activate` e `python -m pcbot.main`).
- Installare librerie: `..\venv\Scripts\activate` poi `pip install -r requirements.txt`.
- Aprire/chiudere un programma: `start "" capcut` / `taskkill /IM CapCut.exe /F`.

## Stato al 18/11/2026 e cose in sospeso
- Le bot si sono fermate mentre Cristina era fuori casa: verificare che `avvia.bat` sia aperto, che le librerie siano installate e copiare gli ultimi file (pcbot, cervelli, videoedit, avvia.bat, avvio_automatico.bat, requirements.txt) se non già aggiornati; poi lanciare una volta `avvio_automatico.bat`.
- Notion per Max: `cervelli/max/.mcp.json` (server ufficiale https://mcp.notion.com/mcp). Login una volta con `collega_notion.bat` (/mcp → notion → Authenticate). In alternativa il connettore claude.ai (`mcp__claude_ai_Notion`).
- Da decidere con Cristina: i due PDF di Stefania (Brand Positioning Statement, Metodo Merenda) – progetto privato o invio da Telegram; riferimenti per i reel personali NON di vendita; eventuale versione su server per avere le bot attive anche a PC spento.
- Regole di Cristina: niente testi fuori dalla safe zone o sulla faccia; testi/immagini anche dietro la persona con maschera; arancione solo nelle ADV; 4:5 solo nelle ADV; prima di cancellare/spostare su Notion chiedere conferma.
