"""🧑‍💼 Max – assistente personale: promemoria, note, to-do, controllo PC, chat con AI."""
import os, re
from datetime import datetime, timedelta
from telegram.ext import CommandHandler, MessageHandler, filters
from pcbot.auth import restricted
from pcbot import ai, storage, notion
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
    if job.data.get("notion"):
        try:
            await notion.done(job.data["notion"])
        except Exception:
            pass
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
    if notion.enabled():
        try:
            r["notion"] = await notion.add("reminders", text, when)
        except Exception as e:
            await update.message.reply_text(f"⚠️ Notion: {e}")
    storage.save("reminders", storage.load("reminders", []) + [r])
    schedule(context.application, r)
    await update.message.reply_text(f"👍 Te lo ricordo il {when:%d/%m alle %H:%M}")


@restricted
async def promemoria(update, context):
    rems = sorted(storage.load("reminders", []), key=lambda r: r["at"])
    txt = "\n".join(f"• {datetime.fromisoformat(r['at']):%d/%m %H:%M} – {r['text']}" for r in rems)
    await update.message.reply_text(txt or "Nessun promemoria.")


# ---------- To-do e note (su Notion se configurato, altrimenti in locale) ----------
def _list_cmd(kind, emoji):
    @restricted
    async def handler(update, context):
        try:
            if context.args:
                text = " ".join(context.args)
                if notion.enabled():
                    await notion.add(kind, text)
                else:
                    storage.save(kind, storage.load(kind, []) + [text])
                return await update.message.reply_text(
                    f"{emoji} Aggiunto{' su Notion' if notion.enabled() else ''}.")
            if notion.enabled():
                rows = await notion.items(kind)
                context.chat_data[kind] = [pid for pid, _ in rows]
                texts = [t for _, t in rows]
            else:
                texts = storage.load(kind, [])
            await update.message.reply_text(
                "\n".join(f"{i + 1}. {t}" for i, t in enumerate(texts)) or "Lista vuota.")
        except Exception as e:
            await update.message.reply_text(f"❌ {e}")
    return handler


def _del_cmd(kind):
    @restricted
    async def handler(update, context):
        try:
            n = int(context.args[0]) - 1
            if notion.enabled():
                ids = context.chat_data.get(kind) or [pid for pid, _ in await notion.items(kind)]
                await (notion.done(ids[n]) if kind == "todo" else notion.remove(ids[n]))
                ids.pop(n)
                return await update.message.reply_text("✅ Aggiornato su Notion.")
            items = storage.load(kind, [])
            removed = items.pop(n); storage.save(kind, items)
            await update.message.reply_text(f"✅ Rimosso: {removed}")
        except (IndexError, ValueError):
            await update.message.reply_text("Indica il numero (guardalo con /todo o /nota), es. /fatto 2")
        except Exception as e:
            await update.message.reply_text(f"❌ {e}")
    return handler


@restricted
async def diario(update, context):
    """/diario oggi ho finito il montaggio – annotazione datata su Notion."""
    if not notion.enabled():
        return await update.message.reply_text("Collega Notion nel .env (NOTION_TOKEN, NOTION_PAGE_ID).")
    await notion.add("log", " ".join(context.args) or "Nota")
    await update.message.reply_text("📓 Salvato nel diario su Notion.")


@restricted
async def notion_cmd(update, context):
    if not notion.enabled():
        return await update.message.reply_text("Notion non collegato: aggiungi NOTION_TOKEN e NOTION_PAGE_ID nel .env.")
    try:
        await notion.db_id()
        await update.message.reply_text("✅ Notion collegato: trovi tutto nel database «🧑‍💼 Max».")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")


# ---------- Chat libera con Claude (opzionale) ----------
SYSTEM_BASE = ("Sei Max, l’assistente personale dell’utente (al femminile). Rispondi in italiano, in modo breve, "
          "pratico e cordiale. Se l'utente chiede un promemoria a orario, suggerisci il comando /ricorda. "
          "Per salvare cose da fare suggerisci /todo, per le idee /nota.")
SYSTEM = (SYSTEM_BASE + " "
          "Quando l'utente ti dice cose da fare, idee o fatti da ricordare, salvali su Notion con lo "
          "strumento aggiungi_notion senza chiedere conferma.")

SYSTEM_TAGS = (SYSTEM_BASE + " Quando l'utente ti dice cose da fare, idee o eventi da ricordare, "
               "aggiungi in fondo alla risposta una riga per ognuno nel formato esatto "
               "[[SALVA:todo:testo]] oppure [[SALVA:notes:testo]] oppure [[SALVA:log:testo]]. "
               "Non usare strumenti.")


async def save_tags(answer):
    tags = re.findall(r"\[\[SALVA:(todo|notes|log):(.+?)\]\]", answer)
    answer = re.sub(r"\s*\[\[SALVA:.+?\]\]", "", answer).strip()
    saved = []
    for kind, text in tags:
        try:
            if notion.enabled():
                await notion.add(kind, text.strip())
            elif kind in ("todo", "notes"):
                storage.save(kind, storage.load(kind, []) + [text.strip()])
            saved.append(text.strip())
        except Exception:
            pass
    if saved:
        answer += "\n\n💾 Salvato: " + "; ".join(saved)
    return answer


NOTION_TOOL = {
    "name": "aggiungi_notion",
    "description": "Salva un elemento nel database Notion dell'utente.",
    "input_schema": {"type": "object", "properties": {
        "tipo": {"type": "string", "enum": ["todo", "notes", "log"],
                 "description": "todo = cosa da fare, notes = idea/info, log = evento del diario"},
        "testo": {"type": "string"}}, "required": ["tipo", "testo"]}}


@restricted
async def chat(update, context):
    if not ai.available():
        return await update.message.reply_text("Per parlare liberamente con me aggiungi GEMINI_API_KEY "
                                               "(gratis) nel .env. Intanto usa /aiuto.")
    hist = context.chat_data.setdefault("hist", [])
    hist.append({"role": "user", "content": update.message.text})
    await update.message.chat.send_action("typing")
    try:
        if os.getenv("ANTHROPIC_API_KEY"):
            answer = await claude_with_notion(hist)
        else:
            answer = await ai.generate(SYSTEM_TAGS + f" Oggi è {datetime.now():%A %d/%m/%Y %H:%M}.", hist[-20:])
            answer = await save_tags(answer)
    except Exception as e:
        hist.pop()
        return await update.message.reply_text(f"❌ {e}")
    hist.append({"role": "assistant", "content": answer})
    del hist[:-20]
    await update.message.reply_text(answer[:4000])


async def claude_with_notion(hist):
    """Con Claude Max può salvare da sola su Notion."""
    from anthropic import AsyncAnthropic
    client = AsyncAnthropic()
    kw = dict(model=os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5"), max_tokens=1024,
              system=SYSTEM + f" Oggi è {datetime.now():%A %d/%m/%Y %H:%M}.")
    if notion.enabled():
        kw["tools"] = [NOTION_TOOL]
    msgs = hist[-20:]
    while True:
        resp = await client.messages.create(messages=msgs, **kw)
        if resp.stop_reason != "tool_use":
            return "".join(b.text for b in resp.content if b.type == "text")
        msgs = msgs + [{"role": "assistant", "content": resp.content}]
        results = []
        for b in resp.content:
            if b.type == "tool_use":
                try:
                    await notion.add(b.input["tipo"], b.input["testo"])
                    out = "Salvato su Notion."
                except Exception as e:
                    out = f"Errore: {e}"
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": out})
        msgs.append({"role": "user", "content": results})


HELP = f"""🧑‍💼 <b>Ciao, sono Max, la tua assistente!</b>

<b>Promemoria</b>
/ricorda 10m · 2h · 18:30 · 25/12 09:00 &lt;testo&gt;
/promemoria – elenco

<b>To-do e note</b>
/todo [testo] – aggiungi o mostra · /fatto N
/nota [testo] – aggiungi o mostra · /cancella N
/diario [testo] – annotazione datata su Notion
/notion – verifica collegamento

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
            CommandHandler("diario", diario), CommandHandler("notion", notion_cmd),
            *system.HANDLERS, *screen.HANDLERS, *files.HANDLERS,
            MessageHandler(filters.TEXT & ~filters.COMMAND, chat)]
