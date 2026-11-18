# Il mio team di bot Telegram

| Bot | Ruolo |
|---|---|
| 🧑‍💼 **Max** | Assistente personale: promemoria, to-do, note, controllo del PC, chat libera (AI) |
| 🎬 **Vivi** | Video editor: taglia, verticale 9:16, comprimi, velocità, testo, GIF, audio |
| 📱 **Jess** | Social media manager – *in arrivo* |

Tutti girano sul PC con un solo comando e rispondono solo al tuo ID Telegram.

## Setup
1. Su **@BotFather** crea due bot (`/newbot`): uno per Max e uno per Vivi. Copia i token.
   Con `/setuserpic` e `/setdescription` puoi dare a ognuno foto e descrizione.
2. Scopri il tuo ID con **@userinfobot**.
3. Installa **Python 3.10+** e **FFmpeg** (Windows: `winget install ffmpeg`, Mac: `brew install ffmpeg`).
4. Nella cartella del progetto:
   ```bash
   python -m venv venv
   venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
   pip install -r requirements.txt
   copy .env.example .env         # poi compila token e ID
   python -m pcbot.main
   ```
5. Su iPhone scrivi `/start` a Max e a Vivi.

## Max
- `/ricorda 10m chiama mamma` · `/ricorda 18:30 palestra` · `/ricorda 25/12 09:00 auguri` · `/promemoria`
- `/todo compra latte` · `/todo` · `/fatto 1` — `/nota idea` · `/nota` · `/cancella 1`
- PC: `/status` `/processi` `/kill` `/power` `/screen` `/apri` `/app` `/scrivi` `/tasto` `/ls` `/get`
- Messaggi liberi → risponde con Claude (serve `ANTHROPIC_API_KEY`, opzionale)

## Vivi
Mandale un video (max 20 MB, limite Telegram) o usa `/pc Video/clip.mp4` per un file sul PC.
Le modifiche si concatenano: es. `/taglia 0:05 0:30` → `/verticale` → `/testo Nuovo video!`
Comandi: `/taglia` `/verticale` `/quadrato` `/comprimi` `/velocita 1.5` `/testo` `/muto` `/audio` `/gif` `/copertina`

## Aggiungere un bot (es. Jess)
Crea `pcbot/bots/jess.py` con `NAME`, `HANDLERS` e aggiungi `("JESS_TOKEN", jess)` a `TEAM` in `pcbot/main.py`.

## Avvio automatico (Windows)
Collegamento a `venv\Scripts\pythonw.exe -m pcbot.main` (avvia in: cartella progetto) dentro `shell:startup`.
