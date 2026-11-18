"""🎬 Vivi – editor video. Mandale un video, poi dai un comando."""
import asyncio, os, re, shutil, sys, tempfile, uuid
from datetime import datetime
from pathlib import Path
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, filters
from pcbot.auth import restricted
from pcbot import menu as _menu, team
from pcbot import ai, brain

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


def area(context):
    return context.chat_data.get("area")


def archivio(context) -> Path:
    """FILES_ROOT/Vivi/Lavoro o FILES_ROOT/Vivi/Personale"""
    d = FILES_ROOT / "Vivi" / (area(context) or "personale").capitalize()
    d.mkdir(parents=True, exist_ok=True)
    return d


async def send(update, path, chain=True, context=None):
    if context:  # copia sempre il risultato nella cartella dell'area
        shutil.copy2(path, archivio(context) / path.name)
    if path.stat().st_size > 50 * 2**20:
        dest = (archivio(context) if context else FILES_ROOT / "Vivi") / path.name
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
    await ask_area(m)


@restricted
async def from_pc(update, context):
    p = (FILES_ROOT / " ".join(context.args)).resolve()
    if FILES_ROOT not in p.parents or not p.is_file():
        return await update.message.reply_text("❌ File non trovato dentro FILES_ROOT.")
    context.chat_data["video"] = str(p)
    await ask_area(update.message)


# ---------- Lavoro / Personale + montaggio automatico (videoedit/editor.py) ----------
EDITOR = Path(__file__).resolve().parents[2] / "videoedit" / "editor.py"
STILI_LAVORO = ["giudice", "testimonial", "evento", "fiera", "youtube"]
LABEL = {"lavoro": "💼 Lavoro (Stefania)", "personale": "🏠 Personale"}


def kb(rows):
    return InlineKeyboardMarkup([[InlineKeyboardButton(t, callback_data=d) for t, d in r] for r in rows])


async def ask_area(message):
    await message.reply_text("✅ Video ricevuto! È per lavoro o personale?", reply_markup=kb(
        [[(LABEL["lavoro"], "vv:area:lavoro"), (LABEL["personale"], "vv:area:personale")]]))


async def ask_style(message, context):
    if area(context) == "lavoro":
        rows = [[(s.capitalize(), f"vv:stile:lavoro/{s}") for s in STILI_LAVORO[i:i + 3]] for i in (0, 3)]
        rows.append([("Base lavoro", "vv:stile:lavoro")])
    else:
        rows = [[("Personale", "vv:stile:personale"), ("📣 ADV (vendita)", "vv:stile:personale/adv")]]
    rows.append([("✂️ Modifica a mano (/aiuto)", "vv:manuale")])
    await message.reply_text("Che stile uso per il montaggio automatico?", reply_markup=kb(rows))


@restricted
async def area_cmd(update, context):
    """/lavoro o /personale – cambia area."""
    context.chat_data["area"] = (context.chat_data.pop("_cmd", None) or update.message.text.split()[0].lstrip("/").split("@")[0])
    await update.message.reply_text(f"Area: {LABEL[area(context)]}\nI file vanno in {archivio(context)}")
    if context.chat_data.get("video"):
        await ask_style(update.message, context)


@restricted
async def monta_cmd(update, context):
    """/monta – montaggio automatico del video attuale."""
    if not area(context):
        return await ask_area(update.message)
    await ask_style(update.message, context)


@restricted
async def buttons(update, context):
    q = update.callback_query
    await q.answer()
    _, kind, *val = q.data.split(":", 2) + [""]
    val = val[0]
    if kind == "area":
        context.chat_data["area"] = val
        await q.edit_message_text(f"{LABEL[val]} ✔︎")
        await ask_style(q.message, context)
    elif kind == "manuale":
        await q.edit_message_text(HELP, parse_mode="HTML")
    elif kind == "stile":
        context.chat_data["stile"] = val
        fmts = [("📱 9:16", "vv:fmt:9:16"), ("🖥 16:9", "vv:fmt:16:9"), ("Come l'originale", "vv:fmt:auto")]
        if val == "personale/adv":  # il 4:5 solo nelle ADV, e niente 16:9
            fmts = [("📱 9:16", "vv:fmt:9:16"), ("🖼 4:5 feed", "vv:fmt:4:5")]
        await q.edit_message_text(f"Stile: {val} ✔︎\nFormato?", reply_markup=kb([
            fmts,
            [("⚡ Anteprima veloce 480p", "vv:fmt:prev")]]))
    elif kind == "fmt":
        prev = val == "prev"
        fmt = context.chat_data.get("fmt", "auto") if prev else val
        context.chat_data["fmt"] = fmt
        await q.edit_message_text(f"🎬 Monto «{context.chat_data['stile']}» {fmt}"
                                  f"{' (anteprima)' if prev else ''}... può volerci qualche minuto.")
        await auto_edit(q.message, context, fmt, prev)


async def auto_edit(message, context, fmt, preview):
    try:
        video = current(context)
        args = [sys.executable, str(EDITOR), "tutto", str(video), "--profilo", context.chat_data["stile"],
                "--formato", fmt] + (["--anteprima"] if preview else []) + \
               ([] if os.getenv("ANTHROPIC_API_KEY") or ai.claude_code() else ["--senza-ai"])
        env = dict(os.environ, BOT_CERVELLO=str(brain.folder(NAME)), BOT_MEMORIA=brain.context_text(NAME))
        proc = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE, env=env,
                                                    stderr=asyncio.subprocess.STDOUT, cwd=EDITOR.parent)
        log = (await proc.communicate())[0].decode(errors="replace")
        m = re.search(r"\[fatto\] (.+\.mp4)", log)
        if proc.returncode or not m:
            return await message.reply_text("❌ Montaggio non riuscito:\n" + log[-1500:])
        result = Path(m[1].strip())
        dest = archivio(context) / result.name
        shutil.copy2(result, dest)
        if dest.stat().st_size <= 50 * 2**20:
            await message.reply_video(dest.open("rb"), supports_streaming=True)
        await message.reply_text(f"✅ Fatto! Salvato in {dest}")
        scene = result.parent / "scene_da_generare.txt"
        if scene.exists():
            await message.reply_document(scene.open("rb"), caption=(
                f"🎨 Scene AI da generare. Salvale in {result.parent / 'broll'} come 1.jpg, 2.mp4… "
                "poi rimanda /monta"))
    except Exception as e:
        await message.reply_text(f"❌ {e}")


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
    await send(update, o, chain=False, context=context)


@action
async def gif(update, context):
    o = out(".gif")
    await ffmpeg("-i", current(context), "-t", "8", "-vf",
                 "fps=12,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", o)
    await send(update, o, chain=False, context=context)


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
Ti chiedo se è <b>lavoro</b> o <b>personale</b>: i file finiscono in cartelle separate
(Vivi/Lavoro e Vivi/Personale) e uso gli stili giusti.

<b>Montaggio automatico</b> (tagli, sottotitoli, ritmo)
/monta – scegli stile e formato
/lavoro · /personale – cambia area
Stili lavoro: giudice, testimonial, evento, fiera, youtube

<b>Modifiche a mano</b> (si concatenano)

/taglia 0:05 0:20 – taglia
/verticale – 9:16 per Reel/TikTok
/quadrato – 1:1
/comprimi – riduce peso
/velocita 1.5 – accelera/rallenta
/testo Ciao! – scritta in sovraimpressione
/muto – togli audio
/audio – estrai mp3
/gif – prime 8s in GIF
/copertina 0:03 – fotogramma

🎨 /crea brief – creo un video da zero con il codice (motion graphics, titoli animati, spiegoni)

💬 Scrivimi liberamente: storyboard, prompt per Higgsfield/Kling/Seedance/Veo, musica Suno, effetti sonori…""" + brain.HELP + "\n\n<b>🤝 Team</b>\n/team – passaggi di lavoro tra noi\n/passa vivi testo – passa un lavoro"


@restricted
async def crea(update, context):
    """/crea <brief> – Vivi scrive codice (Remotion, HyperFrames, ffmpeg…) e genera un video sul PC."""
    brief = " ".join(context.args)
    exe = ai.claude_code()
    if not brief:
        return await update.message.reply_text(
            "Uso: /crea brief del video\nEs: /crea motion graphic 9:16 di 10 secondi con il titolo "
            "«L'accoglienza è un protocollo», colori rosso, bordeaux e oro")
    if not exe:
        return await update.message.reply_text("Serve Claude Code collegato (collega_claude.bat).")
    if context.chat_data.get("busy"):
        return await update.message.reply_text("Sto già creando un video, aspetta che finisca 🙂")
    proj = archivio(context) / "Progetti" / datetime.now().strftime("%Y%m%d_%H%M%S")
    proj.mkdir(parents=True, exist_ok=True)
    context.chat_data["busy"] = True
    msg = await update.message.reply_text(f"🎨 Creo il video… può volerci da 5 a 30 minuti.\nCartella: {proj}")
    prompt = (f"Brief di Cristina: {brief}\n\nCrea il video in questa cartella ({proj}). Usa le skill installate "
              "nel tuo cervello se servono (consulta catalogo-skill-video, usa solo strumenti già presenti o "
              "installabili con npm/npx dentro questa cartella). Node.js e ffmpeg sono disponibili. "
              "Non toccare file fuori da questa cartella. Alla fine salva il video finale come final.mp4 "
              "in questa cartella e rispondi con 2 righe: cosa hai fatto e cosa si può migliorare.")
    try:
        proc = await asyncio.create_subprocess_exec(
            exe, "-p", "--output-format", "text", "--add-dir", str(brain.folder(NAME)),
            "--append-system-prompt", "Sei Vivi, video editor e motion designer di Cristina. "
            + brain.context_text(NAME)[-4000:],
            "--allowedTools", "Bash,Write,Edit,Read,Glob,Grep,Skill", "--max-turns", "80",
            cwd=proj, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        out, err = await asyncio.wait_for(proc.communicate(prompt.encode("utf-8")), timeout=45 * 60)
        report = out.decode("utf-8", errors="replace").strip()
        videos = sorted(proj.rglob("*.mp4"), key=lambda p: (p.name != "final.mp4", -p.stat().st_mtime))
        if videos:
            v = videos[0]
            if v.stat().st_size <= 50 * 2**20:
                await update.message.reply_video(v.open("rb"), supports_streaming=True)
            await update.message.reply_text(f"✅ {v}\n\n{report[-1500:]}")
        else:
            await update.message.reply_text("❌ Nessun video creato.\n" + (report or err.decode(errors="replace"))[-1500:])
    except asyncio.TimeoutError:
        proc.kill()
        await update.message.reply_text(f"⏱ Ci ho messo troppo (45 min). Guarda la cartella {proj}")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")
    finally:
        context.chat_data["busy"] = False
        await msg.delete()


@restricted
async def chat(update, context):
    """Domande libere: storyboard, prompt video/Suno/SFX, consigli di montaggio, usando le sue skill."""
    if not _menu.addressed(update, context):
        return
    if not ai.available():
        return await update.message.reply_text("Per parlare con me serve Claude Code collegato (collega_claude.bat).")
    hist = context.chat_data.setdefault("hist", [])
    hist.append({"role": "user", "content": update.message.text})
    await update.message.chat.send_action("typing")
    try:
        answer = await ai.generate(
            "Sei Vivi, la video editor e regista AI di Cristina. Rispondi in italiano, pratica e precisa. "
            f"Area attuale: {area(context) or 'non scelta'}. Usa le tue skill quando servono "
            "(storyboard Gabry, motion control, Suno, effetti sonori, video Google gratis, inquadrature, "
            "protocollo V.A.P.). I prompt di produzione li scrivi in inglese, in blocchi pronti da copiare.",
            hist[-12:], bot=NAME, max_tokens=4000)
    except Exception as e:
        hist.pop()
        return await update.message.reply_text(f"❌ {e}")
    hist.append({"role": "assistant", "content": answer})
    del hist[:-12]
    for i in range(0, len(answer), 4000):
        await update.message.reply_text(answer[i:i + 4000])


@restricted
async def aiuto(update, context):
    await update.message.reply_text(HELP, parse_mode="HTML")
    if update.message.text.startswith("/start"):
        await show_menu(update, context)


HANDLERS = [CommandHandler(["start", "aiuto", "help"], aiuto), CommandHandler("pc", from_pc),
            CommandHandler(["lavoro", "personale"], area_cmd), CommandHandler("monta", monta_cmd),
            CommandHandler("crea", crea),
            CallbackQueryHandler(buttons, pattern=r"^vv:"), *brain.handlers(NAME), *team.handlers(NAME),
            MessageHandler(filters.VIDEO | filters.VIDEO_NOTE | filters.Document.VIDEO, receive),
            MessageHandler(filters.TEXT & ~filters.COMMAND, chat)] + [
    CommandHandler(f.__name__, f) for f in
    (taglia, verticale, quadrato, comprimi, velocita, muto, audio, gif, copertina, testo)]


MENU = [[("🎬 Monta video", "monta", None), ("🎨 Crea video", "crea", "Descrivi il video da creare")],
        [("💼 Lavoro", "lavoro", None), ("🏠 Personale", "personale", None)],
        [("✂️ Taglia", "taglia", "Da quando a quando? (es. 0:05 0:20)"), ("📱 Verticale", "verticale", None), ("🗜 Comprimi", "comprimi", None)],
        [("🖼 Copertina", "copertina", "A che secondo? (es. 0:03)"), ("🎵 Audio mp3", "audio", None), ("🧠 Memoria", "memoria", None)]]
MENU_HANDLERS, show_menu = _menu.build(MENU, HANDLERS)
