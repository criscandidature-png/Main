"""🎬 Vivi – editor video. Mandale un video, poi dai un comando."""
import asyncio, os, shutil, tempfile, uuid
from pathlib import Path
from telegram.ext import CommandHandler, MessageHandler, filters
from pcbot.auth import restricted

NAME = "Vivi"
WORK = Path(tempfile.gettempdir()) / "vivi"
WORK.mkdir(exist_ok=True)
FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
FILES_ROOT = Path(os.getenv("FILES_ROOT", Path.home())).resolve()


def current(context):
    p = context.chat_data.get("video")
    if not p or not Path(p).exists():
        raise ValueError("Prima mandami un video (o usa /pc <percorso>).")
    return Path(p)


async def ffmpeg(*args):
    proc = await asyncio.create_subprocess_exec(FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
                                                *map(str, args), stderr=asyncio.subprocess.PIPE)
    _, err = await proc.communicate()
    if proc.returncode:
        raise RuntimeError(err.decode()[-500:])


def out(ext=".mp4"):
    return WORK / f"{uuid.uuid4().hex}{ext}"


async def send(update, path, chain=True, context=None):
    if path.stat().st_size > 50 * 2**20:
        dest = FILES_ROOT / "Vivi" / path.name
        dest.parent.mkdir(exist_ok=True)
        shutil.move(path, dest)
        await update.message.reply_text(f"📁 File oltre 50 MB, salvato sul PC: {dest}")
        path = dest
    elif path.suffix == ".mp4":
        await update.message.reply_video(path.open("rb"), supports_streaming=True)
    else:
        await update.message.reply_document(path.open("rb"), filename=path.name)
    if chain and context and path.suffix == ".mp4":
        context.chat_data["video"] = str(path)  # i comandi successivi lavorano sul risultato


def action(fn):
    @restricted
    async def wrapper(update, context):
        msg = await update.message.reply_text("🎬 Ci lavoro...")
        try:
            await fn(update, context)
            await msg.delete()
        except Exception as e:
            await msg.edit_text(f"❌ {e}")
    return wrapper


@restricted
async def receive(update, context):
    m = update.message
    media = m.video or m.document or m.video_note
    if media.file_size and media.file_size > 20 * 2**20:
        return await m.reply_text("Telegram permette ai bot di scaricare max 20 MB.\n"
                                  "Per file grandi mettilo sul PC e usa /pc <percorso>.")
    dest = out()
    await (await media.get_file()).download_to_drive(dest)
    context.chat_data["video"] = str(dest)
    await m.reply_text("✅ Video ricevuto! Cosa faccio? /aiuto")


@restricted
async def from_pc(update, context):
    p = (FILES_ROOT / " ".join(context.args)).resolve()
    if FILES_ROOT not in p.parents or not p.is_file():
        return await update.message.reply_text("❌ File non trovato dentro FILES_ROOT.")
    context.chat_data["video"] = str(p)
    await update.message.reply_text(f"✅ Uso {p.name}")


@action
async def taglia(update, context):
    """/taglia 0:05 0:20"""
    a, b = context.args[:2]
    o = out(); await ffmpeg("-ss", a, "-to", b, "-i", current(context), "-c:v", "libx264", "-c:a", "aac", o)
    await send(update, o, context=context)


@action
async def verticale(update, context):
    """Ritaglio centrale 9:16 1080x1920 per Reel/TikTok."""
    o = out()
    await ffmpeg("-i", current(context), "-vf",
                 "crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=1080:1920,setsar=1",
                 "-c:v", "libx264", "-crf", "20", "-c:a", "aac", o)
    await send(update, o, context=context)


@action
async def quadrato(update, context):
    o = out()
    await ffmpeg("-i", current(context), "-vf", "crop='min(iw,ih)':'min(iw,ih)',scale=1080:1080",
                 "-c:v", "libx264", "-crf", "20", "-c:a", "aac", o)
    await send(update, o, context=context)


@action
async def comprimi(update, context):
    o = out()
    await ffmpeg("-i", current(context), "-vf", "scale='min(1280,iw)':-2", "-c:v", "libx264",
                 "-crf", "28", "-preset", "fast", "-c:a", "aac", "-b:a", "96k", o)
    await send(update, o, context=context)


@action
async def velocita(update, context):
    """/velocita 1.5"""
    s = float(context.args[0]); o = out()
    atempo = ",".join(["atempo=2.0"] * int(s // 2) + [f"atempo={s / 2 ** int(s // 2)}"]) if s >= 0.5 else "atempo=0.5"
    await ffmpeg("-i", current(context), "-filter_complex",
                 f"[0:v]setpts=PTS/{s}[v];[0:a]{atempo}[a]", "-map", "[v]", "-map", "[a]", o)
    await send(update, o, context=context)


@action
async def muto(update, context):
    o = out(); await ffmpeg("-i", current(context), "-c:v", "copy", "-an", o)
    await send(update, o, context=context)


@action
async def audio(update, context):
    o = out(".mp3"); await ffmpeg("-i", current(context), "-vn", "-b:a", "192k", o)
    await send(update, o, chain=False)


@action
async def gif(update, context):
    o = out(".gif")
    await ffmpeg("-i", current(context), "-t", "8", "-vf",
                 "fps=12,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", o)
    await send(update, o, chain=False)


@action
async def copertina(update, context):
    """/copertina 0:03 – estrae un fotogramma."""
    t = context.args[0] if context.args else "0"
    o = out(".jpg"); await ffmpeg("-ss", t, "-i", current(context), "-frames:v", "1", "-q:v", "2", o)
    await update.message.reply_photo(o.open("rb"))


@action
async def testo(update, context):
    """/testo Ciao a tutti – scritta in basso."""
    t = " ".join(context.args).replace("'", "’").replace(":", "\\:")
    o = out()
    await ffmpeg("-i", current(context), "-vf",
                 f"drawtext=text='{t}':fontcolor=white:fontsize=h/18:box=1:boxcolor=black@0.5:"
                 "boxborderw=20:x=(w-text_w)/2:y=h-text_h-h/10", "-c:a", "copy", o)
    await send(update, o, context=context)


HELP = """🎬 <b>Ciao, sono Vivi, la tua video editor!</b>
Mandami un video (max 20 MB) oppure /pc &lt;percorso&gt; per un file sul PC.
Ogni modifica si applica al risultato precedente, così puoi concatenarle.

/taglia 0:05 0:20 – taglia
/verticale – 9:16 per Reel/TikTok
/quadrato – 1:1
/comprimi – riduce peso
/velocita 1.5 – accelera/rallenta
/testo Ciao! – scritta in sovraimpressione
/muto – togli audio
/audio – estrai mp3
/gif – prime 8s in GIF
/copertina 0:03 – fotogramma"""


@restricted
async def aiuto(update, context):
    await update.message.reply_text(HELP, parse_mode="HTML")


HANDLERS = [CommandHandler(["start", "aiuto", "help"], aiuto), CommandHandler("pc", from_pc),
            MessageHandler(filters.VIDEO | filters.VIDEO_NOTE | filters.Document.VIDEO, receive)] + [
    CommandHandler(f.__name__, f) for f in
    (taglia, verticale, quadrato, comprimi, velocita, muto, audio, gif, copertina, testo)]
