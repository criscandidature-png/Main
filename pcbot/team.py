"""Bacheca del team: Max, Vivi e Jess si passano il lavoro e sanno cosa fanno le colleghe."""
import re
from datetime import datetime
from telegram.ext import CommandHandler
from pcbot import storage
from pcbot.auth import ALLOWED, restricted

APPS = {}
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
            "Usalo solo quando serve davvero."
            + (f"\nUltimi passaggi nel team che ti riguardano:\n{recent}" if recent else ""))


async def dispatch(frm: str, to: str, text: str):
    to = to.lower()
    b = board()
    b.append({"time": datetime.now().strftime("%d/%m %H:%M"), "from": frm, "to": to, "text": text})
    storage.save("team_board", b[-50:])
    app = APPS.get(to)
    if app and ALLOWED:
        await app.bot.send_message(next(iter(ALLOWED)),
                                   f"📨 {frm} mi ha passato un lavoro:\n\n{text}\n\nRispondimi qui e ci penso io.")


async def handle_tags(answer: str, frm: str) -> str:
    tags = re.findall(r"\[\[PASSA:(max|vivi|jess):(.+?)\]\]", answer, flags=re.S | re.I)
    answer = re.sub(r"\s*\[\[PASSA:.+?\]\]", "", answer, flags=re.S).strip()
    for to, text in tags:
        if to.lower() == frm.lower():
            continue
        try:
            await dispatch(frm, to, text.strip())
            answer += f"\n\n📨 Ho passato il lavoro a {NOMI[to.lower()]}."
        except Exception:
            answer += f"\n\n(Non sono riuscita a contattare {NOMI[to.lower()]}.)"
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
