"""/aggiorna: scarica l'ultima versione da GitHub e riavvia, senza toccare .env, data/ e memorie."""
import asyncio, io, os, shutil, sys, zipfile
from pathlib import Path
import httpx
from telegram.ext import CommandHandler
from pcbot.auth import restricted

REPO = os.getenv("UPDATE_REPO", "criscandidature-png/Main")
BRANCH = os.getenv("UPDATE_BRANCH", "claude/peaceful-tesla-n6m87j")
ROOT = Path(__file__).resolve().parents[1]
RESTART_CODE = 3
REPLACE = ("pcbot/", "videoedit/", "avvia.bat", "collega_claude.bat", "requirements.txt",
           "README.md", ".env.example")


def apply(data: bytes) -> list[str]:
    changed = []
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        top = z.namelist()[0].split("/")[0] + "/"
        for n in z.namelist():
            rel = n[len(top):]
            if not rel or n.endswith("/") or ".." in rel:
                continue
            dest = ROOT / rel
            if rel.startswith(REPLACE):
                pass
            elif rel.startswith("cervelli/") and (not dest.exists() or not rel.endswith("CLAUDE.md")):
                pass  # manuali e skill aggiornati; le memorie (CLAUDE.md) esistenti non si toccano
            else:
                continue
            content = z.read(n)
            if dest.exists() and dest.read_bytes() == content:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
            changed.append(rel)
    return changed


@restricted
async def aggiorna(update, context):
    msg = await update.message.reply_text("⬇️ Scarico gli aggiornamenti...")
    try:
        url = f"https://codeload.github.com/{REPO}/zip/refs/heads/{BRANCH}"
        async with httpx.AsyncClient(timeout=120, follow_redirects=True) as c:
            r = await c.get(url)
            r.raise_for_status()
        changed = apply(r.content)
        if not changed:
            return await msg.edit_text("✅ Sei già aggiornata.")
        if "requirements.txt" in changed:
            await msg.edit_text("📦 Installo le nuove librerie...")
            p = await asyncio.create_subprocess_exec(sys.executable, "-m", "pip", "install", "-q", "-r",
                                                     str(ROOT / "requirements.txt"))
            await p.wait()
        await msg.edit_text(f"✅ Aggiornati {len(changed)} file. Riavvio il team, torniamo online tra pochi secondi…")
        context.application.bot_data["restart"] = True
        asyncio.get_running_loop().call_later(2, lambda: os._exit(RESTART_CODE))
    except Exception as e:
        await msg.edit_text(f"❌ Aggiornamento non riuscito: {e}")


HANDLERS = [CommandHandler("aggiorna", aggiorna)]
HELP = "\n\n<b>🔄 Aggiornamenti</b>\n/aggiorna – scarica le novità da GitHub e riavvia il team"
