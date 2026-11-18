"""Avvia tutti i bot del team (ognuno col suo token Telegram) in un unico processo."""
import asyncio, logging, os
from dotenv import load_dotenv

load_dotenv()

from telegram import BotCommand
from telegram.ext import Application, CommandHandler
from pcbot.auth import ALLOWED
from pcbot.bots import vivi, jess, max as max_bot

TEAM = [("MAX_TOKEN", max_bot), ("VIVI_TOKEN", vivi), ("JESS_TOKEN", jess)]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("team")


async def build(token, bot):
    app = Application.builder().token(token).concurrent_updates(True).build()
    app.add_handlers(bot.HANDLERS)
    for h, group in getattr(bot, "MENU_HANDLERS", []):
        app.add_handler(h, group)
    await app.initialize()
    cmds = sorted({c for h in bot.HANDLERS if isinstance(h, CommandHandler) for c in h.commands})
    await app.bot.set_my_commands([BotCommand("menu", "📲 mostra il menu")] +
                                  [BotCommand(c, c) for c in cmds if c not in ("start", "help", "menu")][:99])
    if hasattr(bot, "on_start"):
        await bot.on_start(app)
    await app.start()
    await app.updater.start_polling()
    log.info("✅ %s è online", bot.NAME)
    return app


async def run():
    if not ALLOWED:
        raise SystemExit("Imposta ALLOWED_USERS nel file .env")
    apps = [await build(os.environ[k], b) for k, b in TEAM if os.getenv(k)]
    if not apps:
        raise SystemExit("Nessun token trovato nel .env")
    try:
        await asyncio.Event().wait()
    finally:
        for a in apps:
            await a.updater.stop(); await a.stop(); await a.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass
