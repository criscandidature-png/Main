"""Cervello di ogni bot: cervelli/<bot>/CLAUDE.md (memoria) + cervelli/<bot>/.claude/skills (skill).

Claude Code, eseguito dentro quella cartella, carica da solo memoria e skill.
Da Telegram: /impara, /memoria, /dimentica, /skill, e invio di un file SKILL.md o .zip.
"""
import io, re, zipfile
from pathlib import Path
from telegram.ext import CommandHandler, MessageHandler, filters
from pcbot.auth import restricted

ROOT = Path(__file__).resolve().parents[1] / "cervelli"
MARK = "## Cose imparate"


def folder(bot: str) -> Path:
    d = ROOT / bot.lower()
    (d / ".claude" / "skills").mkdir(parents=True, exist_ok=True)
    if not (d / "CLAUDE.md").exists():
        (d / "CLAUDE.md").write_text(f"# Memoria di {bot}\n\n{MARK}\n", "utf-8")
    return d


def memory_file(bot):
    return folder(bot) / "CLAUDE.md"


def lessons(bot) -> list[str]:
    text = memory_file(bot).read_text("utf-8")
    part = text.split(MARK, 1)[1] if MARK in text else ""
    return [l[2:].strip() for l in part.splitlines() if l.startswith("- ")]


def skills(bot) -> list[str]:
    return sorted(p.parent.name for p in (folder(bot) / ".claude" / "skills").glob("*/SKILL.md"))


def context_text(bot) -> str:
    """Per le AI che non leggono CLAUDE.md da sole (API, Gemini): manuali importati + cose imparate."""
    d = folder(bot)
    docs = "".join("\n\n" + (d / m).read_text("utf-8")
                   for m in re.findall(r"^@(\S+\.md)$", memory_file(bot).read_text("utf-8"), re.M) if (d / m).exists())
    l = lessons(bot)
    return docs + (("\n\nCose che Cristina ti ha insegnato, da seguire sempre:\n" + "\n".join(f"- {x}" for x in l)) if l else "")


def handlers(bot: str):
    @restricted
    async def impara(update, context):
        t = " ".join(context.args).strip()
        if not t:
            return await update.message.reply_text(
                "Uso: /impara <regola o informazione>\nEs: /impara i reel di lavoro finiscono sempre con 'Prenota una call'")
        f = memory_file(bot)
        s = f.read_text("utf-8")
        if MARK not in s:
            s += f"\n{MARK}\n"
        f.write_text(s.rstrip() + f"\n- {t}\n", "utf-8")
        await update.message.reply_text(f"🧠 Imparato! Ora so {len(lessons(bot))} cose.")

    @restricted
    async def memoria(update, context):
        l = lessons(bot)
        txt = "\n".join(f"{i + 1}. {x}" for i, x in enumerate(l)) or "Non mi hai ancora insegnato niente. Usa /impara"
        sk = skills(bot)
        await update.message.reply_text(f"🧠 Cose imparate:\n{txt}\n\n🧩 Skill: {', '.join(sk) or 'nessuna'}")

    @restricted
    async def dimentica(update, context):
        try:
            n = int(context.args[0]) - 1
            l = lessons(bot); removed = l.pop(n)
        except (IndexError, ValueError):
            return await update.message.reply_text("Uso: /dimentica N (il numero lo vedi con /memoria)")
        f = memory_file(bot)
        head = f.read_text("utf-8").split(MARK, 1)[0]
        f.write_text(head + MARK + "\n" + "".join(f"- {x}\n" for x in l), "utf-8")
        await update.message.reply_text(f"🗑 Dimenticato: {removed}")

    @restricted
    async def skill_cmd(update, context):
        if context.args and context.args[0] == "rimuovi" and len(context.args) > 1:
            import shutil
            d = folder(bot) / ".claude" / "skills" / context.args[1]
            if d.exists():
                shutil.rmtree(d)
                return await update.message.reply_text(f"🗑 Skill {context.args[1]} rimossa.")
            return await update.message.reply_text("Skill non trovata.")
        await update.message.reply_text(
            f"🧩 Skill installate: {', '.join(skills(bot)) or 'nessuna'}\n\n"
            "Per aggiungerne una mandami il file SKILL.md oppure lo .zip della skill, "
            "con didascalia: skill\nPer toglierla: /skill rimuovi <nome>")

    async def receive_skill(update, context):
        msg = update.message
        doc = msg.document
        data = bytes(await (await doc.get_file()).download_as_bytearray())
        base = folder(bot) / ".claude" / "skills"
        if doc.file_name.lower().endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                md = [n for n in z.namelist() if n.endswith("SKILL.md")]
                if not md:
                    return await msg.reply_text("❌ Nello zip non c'è un SKILL.md")
                prefix = md[0][: -len("SKILL.md")]
                name = Path(prefix).name or Path(doc.file_name).stem
                for n in z.namelist():
                    if n.startswith(prefix) and not n.endswith("/") and ".." not in n:
                        out = base / name / n[len(prefix):]
                        out.parent.mkdir(parents=True, exist_ok=True)
                        out.write_bytes(z.read(n))
        else:
            text = data.decode("utf-8", errors="replace")
            m = re.search(r"^name:\s*(.+)$", text, re.M)
            name = re.sub(r"[^\w-]", "-", (m[1] if m else Path(doc.file_name).stem).strip()).lower()
            (base / name).mkdir(parents=True, exist_ok=True)
            (base / name / "SKILL.md").write_text(text, "utf-8")
        await msg.reply_text(f"🧩 Skill «{name}» installata! Skill attuali: {', '.join(skills(bot))}")

    is_skill = filters.Document.ALL & filters.CaptionRegex(r"(?i)^\s*skill")
    return [CommandHandler("impara", impara), CommandHandler("memoria", memoria),
            CommandHandler("dimentica", dimentica), CommandHandler("skill", skill_cmd),
            MessageHandler(is_skill, restricted(receive_skill))]


HELP = ("\n\n<b>🧠 Insegnami</b>\n/impara regola – la ricordo per sempre\n/memoria – cosa so\n"
        "/dimentica N\n/skill – skill installate (mandami un SKILL.md o .zip con didascalia «skill»)")
