"""Bacheca del team: Max, Vivi e Jess si passano il lavoro e sanno cosa fanno le colleghe."""
import asyncio, logging, re
from datetime import datetime
from telegram.ext import CommandHandler
from pcbot import storage
from pcbot.auth import ALLOWED, restricted

APPS = {}
_TASKS = set()


async def _safe(coro):
    try:
        await coro
    except Exception:
        logging.getLogger("team").exception("Passaggio di lavoro non riuscito")
NOMI = {"max": "Max", "vivi": "Vivi", "jess": "Jess"}
RUOLI = ("Il team di Cristina: Max (assistente personale, agenda, promemoria, Notion, PC, insegnante di inglese), "
         "Vivi (video editor e regista: montaggi, video AI, storyboard, prompt, musica), "
         "Jess (social media manager: caption, hook, script, piano editoriale, community).")


def register(name, app):
    APPS[name.lower()] = app


def board():
    return storage.load("team_board", [])


def context_for(bot: str) -> str:
    """Testo da aggiungere al prompt: chi sono le colleghe, cosa è successo, come passare un lavoro."""
    b = [x for x in board() if bot.lower() in (x["to"], x["from"].lower())][-8:]
    recent = "\n".join(f"- {x['time']} {x['from']} → {NOMI.get(x['to'], x['to'])}: {x['text'][:300]}" for x in b)
    return ("\n\n" + RUOLI + f" Tu sei {bot}.\n"
            "Se una richiesta è più adatta a una collega, o serve il suo aiuto, fai la tua parte e passale il "
            "lavoro aggiungendo in fondo UNA riga nel formato esatto [[PASSA:vivi:messaggio chiaro per lei]] "
            "(oppure jess / max). Il messaggio deve contenere tutto quello che le serve (testi, brief, scadenze). "
            "Usalo quando serve davvero o quando Cristina ti chiede di confrontarti con una collega: le colleghe "
            "sono sempre raggiungibili così."
            + (f"\nUltimi passaggi nel team che ti riguardano:\n{recent}" if recent else ""))


MAX_GIRI = 3  # massimo botta e risposta automatici tra colleghe, per non andare avanti all'infinito


async def dispatch(frm: str, to: str, text: str, giro: int = 1):
    """La collega riceve il messaggio, ci lavora SUBITO e risponde nella sua chat; può rispondere a sua volta."""
    to = to.lower()
    b = board()
    b.append({"time": datetime.now().strftime("%d/%m %H:%M"), "from": frm, "to": to, "text": text})
    storage.save("team_board", b[-50:])
    app = APPS.get(to)
    if not (app and ALLOWED):
        return
    chat = next(iter(ALLOWED))
    await app.bot.send_message(chat, f"📨 Da {frm}:\n{text}")
    await app.bot.send_chat_action(chat, "typing")
    from pcbot import ai
    risposta = await ai.generate(
        f"Sei {NOMI[to]}. La collega {frm} ti scrive (Cristina legge la chat). Rispondi a {frm} da professionista: "
        "fai la tua parte del lavoro o dai il tuo parere concreto. Se devi rispondere o ripassare il lavoro a "
        f"{frm} o a un'altra collega usa la riga [[PASSA:...]]."
        + ("" if giro < MAX_GIRI else " Questo è l'ultimo scambio: chiudi tu e riassumi a Cristina cosa avete deciso, "
                                     "senza passare ad altre."),
        [{"role": "user", "content": f"Messaggio di {frm}: {text}"}], bot=NOMI[to], giro=giro + 1)
    for i in range(0, len(risposta), 4000):
        await app.bot.send_message(chat, risposta[i:i + 4000])


async def handle_tags(answer: str, frm: str, giro: int = 1) -> str:
    tags = re.findall(r"\[\[PASSA:(max|vivi|jess):(.+?)\]\]", answer, flags=re.S | re.I)
    answer = re.sub(r"\s*\[\[PASSA:.+?\]\]", "", answer, flags=re.S).strip()
    for to, text in tags:
        if to.lower() == frm.lower():
            continue
        if giro > MAX_GIRI:
            continue
        t = asyncio.get_running_loop().create_task(_safe(dispatch(frm, to, text.strip(), giro)))
        _TASKS.add(t)
        t.add_done_callback(_TASKS.discard)
        answer += f"\n\n📨 Ne parlo con {NOMI[to.lower()]}: trovi la sua risposta nella sua chat."
    return answer


def handlers(bot: str):
    @restricted
    async def team_cmd(update, context):
        b = board()[-10:]
        txt = "\n".join(f"• {x['time']} {x['from']} → {NOMI.get(x['to'], x['to'])}: {x['text'][:150]}" for x in b)
        await update.message.reply_text(txt or "Nessun passaggio di lavoro nel team per ora.")

    @restricted
    async def passa(update, context):
        """/passa vivi testo – passa tu un lavoro a una collega."""
        if len(context.args) < 2 or context.args[0].lower() not in NOMI:
            return await update.message.reply_text("Uso: /passa vivi messaggio (oppure jess, max)")
        await dispatch(bot, context.args[0], " ".join(context.args[1:]))
        await update.message.reply_text(f"📨 Passato a {NOMI[context.args[0].lower()]}.")

    return [CommandHandler("team", team_cmd), CommandHandler("passa", passa)]
