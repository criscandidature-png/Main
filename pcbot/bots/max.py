"""🧑‍💼 Max – assistente personale: promemoria, note, to-do, controllo PC, chat con AI."""
import os, re
from datetime import datetime, timedelta
from telegram.ext import CommandHandler, MessageHandler, filters
from pcbot.auth import restricted
from pcbot import storage
from pcbot.modules import system, screen, files

NAME = "Max"

# ---------- Promemoria ----------
def parse_when(s: str):
    """'10m', '2h', '1g', '18:30', '25/12 09:00'"""
    now = datetime.now()
    if m := re.fullmatch(r"(\d+)([mhg])", s):
        n, u = int(m[1]), m[2]
        return now + timedelta(**{{"m": "minutes", "h": "hours", "g": "days"}[u]: n})
    if m := re.fullmatch(r"(\d{1,2}):(\d{2})", s):
        t = now.replace(hour=int(m[1]), minute=int(m[2]), second=0, microsecond=0)
        return t if t > now else t + timedelta(days=1)
    raise ValueError


async def fire(context):
    job = context.job
    await context.bot.send_message(job.chat_id, f"⏰ Promemoria: {job.data['text']}")
    rems = [r for r in storage.load("reminders", []) if r["id"] != job.data["id"]]
    storage.save("reminders", rems)


def schedule(app, r):
    when = datetime.fromisoformat(r["at"])
    app.job_queue.run_once(fire, max(when - datetime.now(), timedelta(seconds=1)),
                           chat_id=r["chat"], data=r, name=str(r["id"]))


@restricted
async def ricorda(update, context):
    args = context.args
    try:
        if len(args) >= 3 and re.fullmatch(r"\d{1,2}/\d{1,2}", args[0]):
            d, mth = map(int, args[0].split("/"))
            h, mi = map(int, args[1].split(":"))
            when = datetime.now().replace(month=mth, day=d, hour=h, minute=mi, second=0, microsecond=0)
            text = " ".join(args[2:])
        else:
            when, text = parse_when(args[0]), " ".join(args[1:])
        assert text
    except Exception:
        return await update.message.reply_text(
            "Uso: /ricorda 10m chiama mamma · /ricorda 18:30 palestra · /ricorda 25/12 09:00 auguri")
    r = {"id": int(datetime.now().timestamp() * 1000), "chat": update.effective_chat.id,
         "at": when.isoformat(), "text": text}
    storage.save("reminders", storage.load("reminders", []) + [r])
    schedule(context.application, r)
    await update.message.reply_text(f"👍 Te lo ricordo il {when:%d/%m alle %H:%M}")


@restricted
async def promemoria(update, context):
    rems = sorted(storage.load("reminders", []), key=lambda r: r["at"])
    txt = "\n".join(f"• {datetime.fromisoformat(r['at']):%d/%m %H:%M} – {r['text']}" for r in rems)
    await update.message.reply_text(txt or "Nessun promemoria.")


# ---------- To-do e note ----------
def _list_cmd(kind, emoji):
    @restricted
    async def handler(update, context):
        items = storage.load(kind, [])
        if context.args:
            items.append(" ".join(context.args)); storage.save(kind, items)
            return await update.message.reply_text(f"{emoji} Aggiunto.")
        txt = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(items))
        await update.message.reply_text(txt or "Lista vuota.")
    return handler


def _del_cmd(kind):
    @restricted
    async def handler(update, context):
        items = storage.load(kind, [])
        try:
            done = items.pop(int(context.args[0]) - 1); storage.save(kind, items)
            await update.message.reply_text(f"✅ Rimosso: {done}")
        except Exception:
            await update.message.reply_text("Indica il numero, es. /fatto 2")
    return handler


# ---------- Chat libera con Claude (opzionale) ----------
SYSTEM = ("Sei Max, l'assistente personale dell'utente. Rispondi in italiano, in modo breve, "
          "pratico e cordiale. Se l'utente chiede un promemoria, suggerisci il comando /ricorda.")


@restricted
async def chat(update, context):
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return await update.message.reply_text("Per parlare liberamente con me aggiungi ANTHROPIC_API_KEY nel .env. "
                                               "Intanto usa /aiuto.")
    from anthropic import AsyncAnthropic
    hist = context.chat_data.setdefault("hist", [])
    hist.append({"role": "user", "content": update.message.text})
    await update.message.chat.send_action("typing")
    resp = await AsyncAnthropic(api_key=key).messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5"), max_tokens=1024,
        system=SYSTEM + f" Oggi è {datetime.now():%A %d/%m/%Y %H:%M}.", messages=hist[-20:])
    answer = "".join(b.text for b in resp.content if b.type == "text")
    hist.append({"role": "assistant", "content": answer})
    del hist[:-20]
    await update.message.reply_text(answer)


HELP = f"""🧑‍💼 <b>Ciao, sono Max, il tuo assistente!</b>

<b>Promemoria</b>
/ricorda 10m · 2h · 18:30 · 25/12 09:00 &lt;testo&gt;
/promemoria – elenco

<b>To-do e note</b>
/todo [testo] – aggiungi o mostra · /fatto N
/nota [testo] – aggiungi o mostra · /cancella N

<b>PC</b>
{system.HELP}
{screen.HELP}
{files.HELP}

Scrivimi anche in modo libero 💬"""


@restricted
async def aiuto(update, context):
    await update.message.reply_text(HELP, parse_mode="HTML")


async def on_start(app):
    for r in storage.load("reminders", []):
        schedule(app, r)


HANDLERS = [CommandHandler(["start", "aiuto", "help"], aiuto),
            CommandHandler("ricorda", ricorda), CommandHandler("promemoria", promemoria),
            CommandHandler("todo", _list_cmd("todo", "📝")), CommandHandler("fatto", _del_cmd("todo")),
            CommandHandler("nota", _list_cmd("notes", "🗒")), CommandHandler("cancella", _del_cmd("notes")),
            *system.HANDLERS, *screen.HANDLERS, *files.HANDLERS,
            MessageHandler(filters.TEXT & ~filters.COMMAND, chat)]
