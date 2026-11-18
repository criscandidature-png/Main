"""Max insegnante di inglese: lezioni, quiz, correzioni, parola del giorno, English mode."""
import os
from datetime import time
from telegram.ext import CommandHandler
from pcbot import ai, storage
from pcbot.auth import restricted

BOT = "Max"
SYS = ("Sei Max, assistente personale e insegnante di inglese di Cristina. Segui la skill insegnante-inglese. "
       "Cristina è italiana, lavora in visual merchandising, video editing AI, social media e con l'hotellerie. "
       "Le lezioni sono compatte: situazione in 1 riga, 5 frasi con pronuncia, 1 regola in 2 righe, 1 errore tipico, 3 esercizi. ")


def prof():
    return storage.load("inglese", {"livello": "A2", "parole": [], "english_mode": False, "chat": None})


def save(p):
    storage.save("inglese", p)


async def ask(prompt, p):
    return await ai.generate(SYS + f"Livello attuale: {p['livello']}. Parole già studiate: "
                             + ", ".join(p["parole"][-60:]), [{"role": "user", "content": prompt}],
                             bot=BOT, max_tokens=2500)


def cmd(prompt_fn):
    @restricted
    async def h(update, context):
        p = prof()
        p["chat"] = update.effective_chat.id
        await update.message.chat.send_action("typing")
        try:
            txt = await ask(prompt_fn(" ".join(context.args)), p)
        except Exception as e:
            return await update.message.reply_text(f"❌ {e}")
        save(p)
        txt = track_words(txt)
        for i in range(0, len(txt), 4000):
            await update.message.reply_text(txt[i:i + 4000])
    return h


lezione = cmd(lambda a: f"Fammi una lezione (/inglese){' su: ' + a if a else ' su una situazione utile per me'}. "
                        "Alla fine scrivi una riga 'PAROLE: parola1, parola2, ...' con le parole nuove.")
quiz = cmd(lambda a: f"Fammi un quiz (/quiz){' su: ' + a if a else ' sulle parole già studiate'}. "
                     "Non dare le soluzioni: le correggi quando rispondo.")
correggi = cmd(lambda a: f"Correggi questo mio testo in inglese e spiegami gli errori: «{a}»" if a else
               "Dimmi di scrivere /correggi seguito da una frase in inglese.")


@restricted
async def livello(update, context):
    p = prof()
    if context.args and context.args[0].upper() in ("A1", "A2", "B1", "B2", "C1"):
        p["livello"] = context.args[0].upper(); save(p)
        return await update.message.reply_text(f"📈 Livello impostato: {p['livello']}")
    await update.message.reply_text(f"Livello attuale: {p['livello']}\nCambialo con /livello B1 "
                                    "(A1, A2, B1, B2, C1). Non sai il tuo livello? Chiedimi «fammi un test di livello».")


@restricted
async def english_mode(update, context):
    p = prof()
    p["english_mode"] = not p["english_mode"]; p["chat"] = update.effective_chat.id; save(p)
    await update.message.reply_text("🇬🇧 English mode ON: from now on I'll answer in English and correct you. "
                                    "Write /english again to stop." if p["english_mode"] else
                                    "🇮🇹 English mode disattivata, torno all'italiano.")


async def parola_del_giorno(context):
    p = prof()
    if not p.get("chat") or not p.get("giornaliera", True):
        return
    try:
        txt = await ask("Dammi la parola del giorno (formato della skill) e una mini domanda di ripasso "
                        "su una parola già studiata. Breve. Alla fine 'PAROLE: parola'.", p)
    except Exception:
        return
    p["parole"] += [w.strip() for line in txt.splitlines() if line.startswith("PAROLE:")
                    for w in line[7:].split(",") if w.strip()]
    save(p)
    await context.bot.send_message(p["chat"], "☀️ " + "\n".join(l for l in txt.splitlines()
                                                                 if not l.startswith("PAROLE:")))


@restricted
async def giornaliera(update, context):
    p = prof()
    p["giornaliera"] = not p.get("giornaliera", True); p["chat"] = update.effective_chat.id; save(p)
    await update.message.reply_text("☀️ Parola del giorno attiva (ogni mattina alle " + os.getenv("ENGLISH_TIME", "08:30") + ")"
                                    if p["giornaliera"] else "Parola del giorno disattivata.")


def track_words(text):
    p = prof()
    for line in text.splitlines():
        if line.startswith("PAROLE:"):
            p["parole"] += [w.strip() for w in line[7:].split(",") if w.strip()]
    save(p)
    return "\n".join(l for l in text.splitlines() if not l.startswith("PAROLE:"))


async def on_start(app):
    h, m = map(int, os.getenv("ENGLISH_TIME", "08:30").split(":"))
    app.job_queue.run_daily(parola_del_giorno, time(h, m), name="parola_del_giorno")


HANDLERS = [CommandHandler(["inglese", "lesson"], lezione), CommandHandler("quiz", quiz),
            CommandHandler("correggi", correggi), CommandHandler("livello", livello),
            CommandHandler("english", english_mode), CommandHandler("paroladelgiorno", giornaliera)]
HELP = ("\n\n<b>🇬🇧 Insegnante di inglese</b>\n/inglese [tema] – lezione di 5 minuti\n/quiz – ripasso\n"
        "/correggi frase – correggo il tuo inglese\n/english – conversazione in inglese (on/off)\n"
        "/livello B1 – il tuo livello\n/paroladelgiorno – on/off ogni mattina")
