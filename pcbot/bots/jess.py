"""📱 Jess – social media manager: caption, hashtag, hook, idee, piano editoriale, post programmati."""
import re
from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, filters
from pcbot.auth import restricted
from pcbot import menu as _menu
from pcbot import ai, brain, notion, storage

NAME = "Jess"

BRAND = {
    "lavoro": ("Account di lavoro di Stefania Salvatore, \"La Madrina dell'Accoglienza\", prima esperta di "
               "accoglienza in Italia. Pubblico: imprenditori dell'ospitalità (hotel, ristoranti, B&B), "
               "a cui si dà del tu. Tono autorevole e provocatorio: \"l'accoglienza non è gentilezza, è un "
               "protocollo che fa tornare i clienti\". Parole chiave: metodo, regia, scientifico. "
               "Immaginario dantesco (giudice, inferno, paradiso). Frasi brevi, niente emoji eccessive."),
    "personale": ("Progetti di Cristina: Cristina Visual Merchandiser (campagna SOS NATALE in negozio, "
                  "manuale digitale su cristinaonline.it, pubblico: chi gestisce un negozio), caroselli per "
                  "@ire.project, contenuti AI video. Segui le indicazioni del manuale operativo per ogni progetto."),
}
SYSTEM = ("Sei Jess, la social media manager di Cristina. Scrivi in italiano, pronta da copiare e incollare, "
          "senza preamboli. Conosci Instagram, TikTok, YouTube e LinkedIn: hook nei primi 3 secondi, "
          "caption con prima riga forte, call to action, 5-15 hashtag mirati (mix di nicchia e medi), "
          "orari migliori. Profilo attuale: ")


def area(context):
    return context.chat_data.get("area", "lavoro")


async def ask_claude(context, prompt, image: bytes | None = None, max_tokens=1500):
    return await ai.generate(SYSTEM + BRAND[area(context)] + f" Oggi è {datetime.now():%A %d/%m/%Y}.",
                             [{"role": "user", "content": prompt}], image, max_tokens, bot=NAME)


async def reply_long(message, text):
    for i in range(0, len(text), 4000):
        await message.reply_text(text[i:i + 4000])


def task(prompt_fn, usage=None):
    @restricted
    async def handler(update, context):
        arg = " ".join(context.args)
        if usage and not arg:
            return await update.message.reply_text(usage)
        await update.message.chat.send_action("typing")
        try:
            await reply_long(update.message, await ask_claude(context, prompt_fn(arg)))
        except Exception as e:
            await update.message.reply_text(f"❌ {e}")
    return handler


caption = task(lambda a: f"Scrivi 3 varianti di caption Instagram per questo contenuto: {a}. "
                         "Per ognuna: prima riga hook, corpo breve, CTA. In fondo un unico blocco di hashtag.",
               "Uso: /caption di cosa parla il post (o mandami direttamente una foto)")
hashtag = task(lambda a: f"Dammi 20 hashtag per: {a}. Dividili in: grandi, medi, di nicchia. Solo hashtag.",
               "Uso: /hashtag argomento")
hook = task(lambda a: f"Scrivi 10 hook per i primi 3 secondi di un reel su: {a}. Brevi, diversi tra loro "
                      "(domanda, provocazione, numero, errore comune, storia).", "Uso: /hook argomento")
idee = task(lambda a: f"Proponi 10 idee di contenuto{' su ' + a if a else ''} per questa settimana: "
                      "formato (reel/carosello/storia), titolo, hook e perché funziona.")
script = task(lambda a: f"Scrivi lo script di un reel da 30-45 secondi su: {a}. Struttura: hook, problema, "
                        "contenuto, CTA. Indica tra parentesi quadre cosa si vede.", "Uso: /script argomento")
risposta = task(lambda a: f"Scrivi 3 possibili risposte a questo commento/DM ricevuto: «{a}»",
                "Uso: /risposta testo del commento")


@restricted
async def piano(update, context):
    """/piano [giorni] – piano editoriale, salvato su Notion se collegato."""
    days = int(context.args[0]) if context.args and context.args[0].isdigit() else 7
    await update.message.chat.send_action("typing")
    try:
        text = await ask_claude(context, (
            f"Crea un piano editoriale per i prossimi {days} giorni a partire da domani. "
            "Una riga per post, formato esatto: GG/MM HH:MM | formato | titolo | hook. "
            "Poi una riga vuota e 3 consigli brevi."), max_tokens=2500)
        await reply_long(update.message, text)
        if notion.enabled():
            n = 0
            for d, mth, h, mi, rest in re.findall(r"(\d{1,2})/(\d{1,2})\s+(\d{1,2}):(\d{2})\s*\|\s*(.+)", text):
                when = datetime.now().replace(month=int(mth), day=int(d), hour=int(h), minute=int(mi),
                                              second=0, microsecond=0)
                await notion.add("post", f"[{area(context)}] {rest.strip()}", when)
                n += 1
            await update.message.reply_text(f"🗓 {n} post salvati su Notion (Tipo: Post social).")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")


async def remind_post(context):
    d = context.job.data
    await context.bot.send_message(d["chat"], f"📣 È ora di pubblicare!\n\n{d['text']}")
    storage.save("posts", [p for p in storage.load("posts", []) if p["id"] != d["id"]])


def schedule(app, p):
    delay = max(datetime.fromisoformat(p["at"]) - datetime.now(), timedelta(seconds=1))
    app.job_queue.run_once(remind_post, delay, data=p, name=f"post{p['id']}")


@restricted
async def programma(update, context):
    """/programma 25/11 18:00 testo del post"""
    try:
        d, mth = map(int, context.args[0].split("/"))
        h, mi = map(int, context.args[1].split(":"))
        text = " ".join(context.args[2:]); assert text
        when = datetime.now().replace(month=mth, day=d, hour=h, minute=mi, second=0, microsecond=0)
    except Exception:
        return await update.message.reply_text("Uso: /programma 25/11 18:00 testo o titolo del post")
    p = {"id": int(datetime.now().timestamp() * 1000), "chat": update.effective_chat.id,
         "at": when.isoformat(), "text": text}
    storage.save("posts", storage.load("posts", []) + [p])
    schedule(context.application, p)
    if notion.enabled():
        try:
            await notion.add("post", f"[{area(context)}] {text}", when)
        except Exception:
            pass
    await update.message.reply_text(f"🗓 Ti avviso il {when:%d/%m alle %H:%M} di pubblicarlo.")


@restricted
async def photo(update, context):
    """Foto ricevuta → caption + hashtag guardando l'immagine."""
    await update.message.chat.send_action("typing")
    try:
        f = await update.message.photo[-1].get_file()
        img = bytes(await f.download_as_bytearray())
        extra = update.message.caption or ""
        await reply_long(update.message, await ask_claude(context, (
            f"Guarda questa immagine e scrivi 3 caption Instagram con hashtag. Note: {extra}"), image=img))
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")


@restricted
async def chat(update, context):
    if not _menu.addressed(update, context):
        return
    await update.message.chat.send_action("typing")
    try:
        await reply_long(update.message, await ask_claude(context, update.message.text))
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")


@restricted
async def area_cmd(update, context):
    if update.message.text.startswith(("/lavoro", "/personale")):
        context.chat_data["area"] = (context.chat_data.pop("_cmd", None) or update.message.text.split()[0].lstrip("/").split("@")[0])
        return await update.message.reply_text(f"Profilo: {area(context)} ✔︎")
    await update.message.reply_text("Per quale profilo lavoro?", reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("💼 Lavoro (Stefania)", callback_data="js:lavoro"),
        InlineKeyboardButton("🏠 Personale", callback_data="js:personale")]]))


@restricted
async def area_cb(update, context):
    q = update.callback_query
    await q.answer()
    context.chat_data["area"] = q.data.split(":")[1]
    await q.edit_message_text(f"Profilo: {area(context)} ✔︎  Cosa prepariamo? /aiuto")


HELP = """📱 <b>Ciao, sono Jess, la tua social media manager!</b>
Lavoro su due profili: /lavoro (Stefania, Madrina dell'Accoglienza) o /personale. /profilo per vedere i pulsanti.

/caption argomento – 3 caption + hashtag
📷 Mandami una foto → caption guardando l'immagine
/hashtag argomento
/hook argomento – 10 hook per reel
/script argomento – script reel 30-45s
/idee [tema] – 10 idee per la settimana
/piano [giorni] – piano editoriale (salvato su Notion)
/programma 25/11 18:00 testo – ti avviso quando pubblicare
/risposta testo – risposte a commenti e DM

Oppure scrivimi liberamente 💬""" + brain.HELP


@restricted
async def aiuto(update, context):
    await update.message.reply_text(HELP, parse_mode="HTML")
    if update.message.text.startswith("/start"):
        await show_menu(update, context)


async def on_start(app):
    for p in storage.load("posts", []):
        schedule(app, p)


HANDLERS = [CommandHandler(["start", "aiuto", "help"], aiuto),
            CommandHandler(["lavoro", "personale", "profilo"], area_cmd),
            CallbackQueryHandler(area_cb, pattern=r"^js:"),
            CommandHandler("caption", caption), CommandHandler("hashtag", hashtag),
            CommandHandler("hook", hook), CommandHandler("idee", idee), CommandHandler("script", script),
            CommandHandler("risposta", risposta), CommandHandler("piano", piano),
            CommandHandler("programma", programma),
            *brain.handlers(NAME),
            MessageHandler(filters.PHOTO, photo),
            MessageHandler(filters.TEXT & ~filters.COMMAND, chat)]


MENU = [[("💡 Idee", "idee", None), ("🗓 Piano settimana", "piano", None)],
        [("✍️ Caption", "caption", "Di cosa parla il post?"), ("🪝 Hook", "hook", "Argomento del reel?")],
        [("🎬 Script reel", "script", "Argomento del reel?"), ("#️⃣ Hashtag", "hashtag", "Argomento?")],
        [("💬 Rispondi a commento", "risposta", "Incolla il commento o il DM"), ("🔀 Profilo", "profilo", None)]]
MENU_HANDLERS, show_menu = _menu.build(MENU, HANDLERS)
