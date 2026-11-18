"""Menu fisso con pulsanti per ogni bot.

- Chat privata: tastiera sempre visibile sotto la chat (ReplyKeyboard).
- Gruppo: pulsanti sotto il messaggio (/menu), così i tre bot non si rubano la tastiera.
- Pulsanti che richiedono un testo (es. "✍️ Caption"): il bot chiede, il messaggio successivo è la risposta.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationHandlerStop, CallbackQueryHandler, CommandHandler, MessageHandler, filters
from pcbot.auth import ALLOWED


def addressed(update, context) -> bool:
    """In privato sempre; nei gruppi solo se il bot è menzionato o gli si risponde."""
    chat = update.effective_chat
    if chat.type == "private":
        return True
    msg = update.effective_message
    me = context.bot.username or ""
    if msg and msg.text and f"@{me}".lower() in msg.text.lower():
        return True
    r = msg.reply_to_message if msg else None
    return bool(r and r.from_user and r.from_user.id == context.bot.id)


class _U:
    """Update "finto" per eseguire un comando da un pulsante inline."""
    def __init__(self, q):
        self.message = self.effective_message = q.message
        self.effective_user = q.from_user
        self.effective_chat = q.message.chat
        self.callback_query = None


def build(items, handlers):
    """items: righe di (etichetta, comando, domanda_o_None). handlers: lista HANDLERS del bot."""
    cmds = {}
    for h in handlers:
        if isinstance(h, CommandHandler):
            for c in h.commands:
                cmds.setdefault(c, h.callback)
    flat = [it for row in items for it in row]
    by_label = {lab: (cmd, ask) for lab, cmd, ask in flat}

    def reply_kb():
        return ReplyKeyboardMarkup([[KeyboardButton(l) for l, _, _ in row] for row in items],
                                   resize_keyboard=True, is_persistent=True)

    def inline_kb():
        return InlineKeyboardMarkup([[InlineKeyboardButton(l, callback_data=f"mn:{flat.index((l, c, a))}")
                                      for l, c, a in row] for row in items])

    async def run(update, context, cmd, text=""):
        context.args = text.split()
        context.chat_data["_cmd"] = cmd
        try:
            await cmds[cmd](update, context)
        finally:
            context.chat_data.pop("_cmd", None)

    async def show(update, context):
        if update.effective_user.id not in ALLOWED:
            return
        if update.effective_chat.type == "private":
            await update.effective_message.reply_text("📲 Menu pronto qui sotto 👇", reply_markup=reply_kb())
        else:
            await update.effective_message.reply_text("📲 Cosa faccio?", reply_markup=inline_kb())

    async def start_label(update, context, cmd, ask):
        if ask:
            context.chat_data["_pending"] = cmd
            await update.effective_message.reply_text(f"✏️ {ask}")
        else:
            await run(update, context, cmd)

    async def on_label(update, context):
        if update.effective_user.id not in ALLOWED:
            return
        cmd, ask = by_label[update.message.text.strip()]
        context.chat_data.pop("_pending", None)
        await start_label(update, context, cmd, ask)
        raise ApplicationHandlerStop

    async def on_pending(update, context):
        cmd = context.chat_data.get("_pending")
        if not cmd or update.effective_user.id not in ALLOWED:
            return
        if update.effective_chat.type != "private" and not addressed(update, context):
            return
        context.chat_data.pop("_pending")
        await run(update, context, cmd, update.message.text)
        raise ApplicationHandlerStop

    async def on_inline(update, context):
        q = update.callback_query
        await q.answer()
        if q.from_user.id not in ALLOWED:
            return
        lab, cmd, ask = flat[int(q.data.split(":")[1])]
        u = _U(q)
        if ask:
            context.chat_data["_pending"] = cmd
            await q.message.reply_text(f"✏️ {ask} (rispondi a questo messaggio)")
        else:
            await run(u, context, cmd)

    labels = filters.Text(list(by_label))
    return [
        (CommandHandler("menu", show), 0),
        (MessageHandler(labels, on_label), -1),
        (MessageHandler(filters.TEXT & ~filters.COMMAND, on_pending), -1),
        (CallbackQueryHandler(on_inline, pattern=r"^mn:"), 0),
    ], show
