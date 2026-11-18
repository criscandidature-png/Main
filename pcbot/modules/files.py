"""Bot File: naviga, scarica e carica file (limitato a FILES_ROOT)."""
import os
from pathlib import Path
from telegram.ext import CommandHandler, MessageHandler, filters
from pcbot.auth import restricted

ROOT = Path(os.getenv("FILES_ROOT", Path.home())).resolve()


def safe(rel: str) -> Path:
    p = (ROOT / rel).resolve()
    if p != ROOT and ROOT not in p.parents:
        raise ValueError("Percorso fuori dalla cartella consentita")
    return p


@restricted
async def ls(update, context):
    try:
        p = safe(" ".join(context.args))
        items = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))[:60]
        lines = [("📄 " if i.is_file() else "📁 ") + i.name for i in items]
        await update.message.reply_text(f"{p}\n" + ("\n".join(lines) or "(vuota)"))
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")


@restricted
async def get(update, context):
    try:
        p = safe(" ".join(context.args))
        if p.stat().st_size > 50 * 2**20:
            return await update.message.reply_text("File oltre 50 MB (limite Telegram).")
        await update.message.reply_document(p.open("rb"), filename=p.name)
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")


@restricted
async def upload(update, context):
    doc = update.message.document
    dest = safe("Telegram") / doc.file_name
    dest.parent.mkdir(exist_ok=True)
    f = await doc.get_file()
    await f.download_to_drive(dest)
    await update.message.reply_text(f"💾 Salvato in {dest}")


HANDLERS = [CommandHandler("ls", ls), CommandHandler("get", get),
            MessageHandler(filters.Document.ALL, upload)]
HELP = "/ls [cartella]\n/get <file>\nInvia un file → salvato in FILES_ROOT/Telegram"
