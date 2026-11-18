# PC Bot – controlla il tuo PC da iPhone con Telegram

## Setup (sul PC da controllare)
1. Su Telegram apri **@BotFather** → `/newbot` → copia il token.
2. Apri **@userinfobot** per sapere il tuo user ID.
3. Installa Python 3.10+, poi:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows  (macOS/Linux: source venv/bin/activate)
   pip install -r requirements.txt
   copy .env.example .env       # e compila token + ID
   python -m pcbot.main
   ```
4. Dall'iPhone scrivi `/start` al tuo bot.

## Comandi
| Modulo | Comandi |
|---|---|
| Sistema | `/status`, `/processi`, `/kill`, `/power` (spegni/riavvia/blocca/sospendi) |
| Schermo & Input | `/screen`, `/apri <url>`, `/app <nome>`, `/scrivi <testo>`, `/tasto <tasti>` |
| File | `/ls`, `/get <file>`, invio file → salvato sul PC |

## Aggiungere un nuovo "bot"
Crea `pcbot/modules/nome.py` con `HANDLERS` e `HELP`, poi aggiungilo a `MODULES` in `main.py`.

## Avvio automatico (Windows)
Crea un collegamento a `pythonw -m pcbot.main` (con cartella di avvio = progetto) in `shell:startup`.

## Sicurezza
- Solo gli ID in `ALLOWED_USERS` possono dare comandi.
- Non condividere mai il file `.env`.
- I file sono accessibili solo dentro `FILES_ROOT`.
