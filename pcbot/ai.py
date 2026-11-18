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


def available():
    return bool(os.getenv("ANTHROPIC_API_KEY") or claude_code() or os.getenv("GEMINI_API_KEY"))


async def via_claude_code(exe, system, messages, image):
    """Chiama `claude -p` (modalità non interattiva), usa il login del tuo abbonamento."""
    convo = "\n\n".join(("Utente: " if m["role"] == "user" else "Tu: ") + m["content"] for m in messages[:-1])
    prompt = (f"Conversazione precedente:\n{convo}\n\n" if convo else "") + messages[-1]["content"]
    cwd = tempfile.mkdtemp(prefix="bot_ai_")
    if image:
        (Path(cwd) / "foto.jpg").write_bytes(image)
        prompt = "Guarda l'immagine foto.jpg in questa cartella (usa lo strumento Read). " + prompt
    args = [exe, "-p", "--output-format", "text", "--append-system-prompt", system,
            "--allowedTools", "Read" if image else "", "--max-turns", "3"]
    proc = await asyncio.create_subprocess_exec(*args, cwd=cwd, stdin=asyncio.subprocess.PIPE,
                                                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await asyncio.wait_for(proc.communicate(prompt.encode("utf-8")), timeout=300)
    shutil.rmtree(cwd, ignore_errors=True)
    if proc.returncode:
        raise RuntimeError(f"Claude Code: {(err or out).decode(errors='replace')[-300:]}")
    return out.decode("utf-8", errors="replace").strip()


async def generate(system: str, messages: list[dict], image: bytes | None = None, max_tokens=1500) -> str:
    """messages: [{"role": "user"|"assistant", "content": "testo"}]"""
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

    if exe := claude_code():
        return await via_claude_code(exe, system, messages, image)

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
