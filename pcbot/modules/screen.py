"""Bot Schermo: screenshot, tastiera, apertura link/app."""
import io, platform, subprocess, webbrowser
import mss, mss.tools
from telegram.ext import CommandHandler
from pcbot.auth import restricted


@restricted
async def screenshot(update, context):
    with mss.mss() as s:
        shot = s.grab(s.monitors[0])
        png = mss.tools.to_png(shot.rgb, shot.size)
    await update.message.reply_document(io.BytesIO(png), filename="screen.png")


@restricted
async def open_url(update, context):
    if not context.args:
        return await update.message.reply_text("Uso: /apri <url>")
    webbrowser.open(context.args[0])
    await update.message.reply_text("🌐 Aperto.")


@restricted
async def app(update, context):
    if not context.args:
        return await update.message.reply_text("Uso: /app <programma> (es. notepad, spotify)")
    name = " ".join(context.args)
    cmd = f'start "" "{name}"' if platform.system() == "Windows" else name
    subprocess.Popen(cmd, shell=True)
    await update.message.reply_text(f"🚀 Avviato {name}")


@restricted
async def type_text(update, context):
    import pyautogui
    pyautogui.write(" ".join(context.args), interval=0.02)
    await update.message.reply_text("⌨️ Scritto.")


@restricted
async def key(update, context):
    """/tasto ctrl c  oppure  /tasto volumeup"""
    import pyautogui
    if not context.args:
        return await update.message.reply_text("Uso: /tasto <tasti> (es. ctrl c, playpause, volumeup)")
    pyautogui.hotkey(*context.args)
    await update.message.reply_text("✅")


HANDLERS = [CommandHandler("screen", screenshot), CommandHandler("apri", open_url),
            CommandHandler("app", app), CommandHandler("scrivi", type_text),
            CommandHandler("tasto", key)]
HELP = ("/screen – screenshot\n/apri <url>\n/app <programma>\n/scrivi <testo>\n"
        "/tasto <tasti> – es. playpause, volumeup, ctrl c")
