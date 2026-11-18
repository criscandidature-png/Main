import logging
from dotenv import load_dotenv

load_dotenv()

import os
from telegram import BotCommand
from telegram.ext import Application, CommandHandler
from pcbot.auth import restricted, ALLOWED
from pcbot.modules import system, screen, files

MODULES = {"Sistema": system, "Schermo & Input": screen, "File": files}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@restricted
async def start(update, context):
    txt = "🤖 Controllo PC\n\n" + "\n\n".join(f"<b>{n}</b>\n{m.HELP}" for n, m in MODULES.items())
    await update.message.reply_text(txt, parse_mode="HTML")


async def post_init(app):
    cmds = [BotCommand(h.commands and next(iter(h.commands)), "comando")
            for m in MODULES.values() for h in m.HANDLERS if isinstance(h, CommandHandler)]
    await app.bot.set_my_commands([BotCommand("start", "aiuto")] + cmds)


def main():
    token = os.environ["TELEGRAM_TOKEN"]
    if not ALLOWED:
        raise SystemExit("Imposta ALLOWED_USERS nel file .env")
    app = Application.builder().token(token).post_init(post_init).build()
    app.add_handler(CommandHandler(["start", "help"], start))
    for m in MODULES.values():
        app.add_handlers(m.HANDLERS)
    app.run_polling()


if __name__ == "__main__":
    main()
