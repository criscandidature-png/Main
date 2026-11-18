"""Testo generato da AI. Ordine di scelta:
1. ANTHROPIC_API_KEY  → API di Claude (a pagamento)
2. Claude Code installato e collegato al tuo abbonamento Claude (USE_CLAUDE_CODE=1, default se trovato)
3. GEMINI_API_KEY     → Google Gemini (gratis)
"""
import asyncio, base64, os, shutil, tempfile
from pathlib import Path
import httpx


def claude_code():
    if os.getenv("USE_CLAUDE_CODE", "1") == "0":
        return None
    return shutil.which("claude") or next((str(p) for p in [
        Path.home() / ".local" / "bin" / "claude.exe", Path.home() / ".local" / "bin" / "claude"] if p.exists()), None)


STYLE = """

COME SCRIVI (regole più importanti di tutte le altre):
- Sei una professionista vera che scrive su Telegram a Cristina, una persona a cui tieni. Tono caldo, educato, sicuro, mai saccente.
- Breve: di norma 2-6 righe. Rispondi solo a ciò che ti è stato chiesto, niente premesse, riassunti o elenchi di cose che "potresti fare".
- Testi lunghi (caption, script, piani, lezioni) solo se richiesti, e comunque essenziali.
- Testo semplice: NIENTE asterischi, NIENTE grassetto, NIENTE titoli con #, NIENTE tabelle, NIENTE separatori ---. Per gli elenchi usa righe che iniziano con •
- Emoji: al massimo una, solo se naturale.
- Se manca un'informazione importante, fai UNA sola domanda breve invece di tirare a indovinare.
- Se c'è un problema o un limite, dillo con tatto e proponi subito la soluzione.
- Niente frasi da robot ("Ecco a te!", "Certamente!", "Spero ti sia utile").
- Non parlare mai di strumenti, permessi, file, skill o del fatto di essere un'AI: parla del lavoro, come farebbe una persona.
"""


def clean(text: str) -> str:
    """Toglie la formattazione markdown che su Telegram appare come simboli."""
    import re
    t = re.sub(r"```[a-zA-Z]*\n?", "", text)
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", t)
    t = re.sub(r"__(.+?)__", r"\1", t)
    t = re.sub(r"^#{1,6}\s*", "", t, flags=re.M)
    t = re.sub(r"^\s*[-*]\s+", "• ", t, flags=re.M)
    t = re.sub(r"^\s*-{3,}\s*$", "", t, flags=re.M)
    t = re.sub(r"^\|?\s*:?-{2,}.*$", "", t, flags=re.M)          # righe separatrici delle tabelle
    t = re.sub(r"^\|(.+)\|\s*$", lambda m: " · ".join(c.strip() for c in m[1].split("|")), t, flags=re.M)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def available():
    return bool(os.getenv("ANTHROPIC_API_KEY") or claude_code() or os.getenv("GEMINI_API_KEY"))


async def via_claude_code(exe, system, messages, image, bot=None):
    """Chiama `claude -p` (modalità non interattiva), usa il login del tuo abbonamento."""
    convo = "\n\n".join(("Utente: " if m["role"] == "user" else "Tu: ") + m["content"] for m in messages[:-1])
    prompt = (f"Conversazione precedente:\n{convo}\n\n" if convo else "") + messages[-1]["content"]
    tmp = tempfile.mkdtemp(prefix="bot_ai_")
    if bot:  # nella cartella del cervello Claude Code carica CLAUDE.md e le skill
        from pcbot import brain
        cwd = str(brain.folder(bot))
    else:
        cwd = tmp
    if image:
        foto = Path(tmp) / "foto.jpg"
        foto.write_bytes(image)
        prompt = f"Guarda l'immagine {foto} (usa lo strumento Read). " + prompt
    args = [exe, "-p", "--output-format", "text", "--append-system-prompt", system,
            "--allowedTools", "Read,Skill,Glob", "--add-dir", tmp, "--max-turns", "8"]
    proc = await asyncio.create_subprocess_exec(*args, cwd=cwd, stdin=asyncio.subprocess.PIPE,
                                                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await asyncio.wait_for(proc.communicate(prompt.encode("utf-8")), timeout=300)
    shutil.rmtree(tmp, ignore_errors=True)
    if proc.returncode:
        raise RuntimeError(f"Claude Code: {(err or out).decode(errors='replace')[-300:]}")
    return out.decode("utf-8", errors="replace").strip()


async def generate(system: str, messages: list[dict], image: bytes | None = None, max_tokens=1500,
                   bot: str | None = None) -> str:
    """messages: [{"role": "user"|"assistant", "content": "testo"}]. bot = nome del cervello da usare."""
    return clean(await _generate(system + STYLE, messages, image, max_tokens, bot))


async def _generate(system, messages, image, max_tokens, bot):
    if exe := (None if os.getenv("ANTHROPIC_API_KEY") else claude_code()):
        return await via_claude_code(exe, system, messages, image, bot)
    if bot:
        from pcbot import brain
        system += brain.context_text(bot)
    if os.getenv("ANTHROPIC_API_KEY"):
        from anthropic import AsyncAnthropic
        msgs = [dict(m) for m in messages]
        if image:
            msgs[-1]["content"] = [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                    "data": base64.b64encode(image).decode()}},
                                   {"type": "text", "text": msgs[-1]["content"]}]
        r = await AsyncAnthropic().messages.create(model=os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5"),
                                                   max_tokens=max_tokens, system=system, messages=msgs)
        return "".join(b.text for b in r.content if b.type == "text")

    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("Nessuna AI disponibile: installa Claude Code e fai il login, oppure metti GEMINI_API_KEY nel .env.")
    contents = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
                for m in messages]
    if image:
        contents[-1]["parts"].insert(0, {"inline_data": {"mime_type": "image/jpeg",
                                                         "data": base64.b64encode(image).decode()}})
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    async with httpx.AsyncClient(timeout=90) as c:
        r = await c.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                         params={"key": key}, json={
                             "system_instruction": {"parts": [{"text": system}]}, "contents": contents,
                             "generationConfig": {"maxOutputTokens": max_tokens * 3}})
    data = r.json()
    if r.status_code >= 400:
        raise RuntimeError(f"Gemini: {data.get('error', {}).get('message', r.text)[:300]}")
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    return "".join(p.get("text", "") for p in parts) or "(nessuna risposta)"
