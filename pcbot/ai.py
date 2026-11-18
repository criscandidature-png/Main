"""Testo generato da AI: usa Claude se c'è ANTHROPIC_API_KEY, altrimenti Google Gemini (gratis)."""
import base64, os
import httpx


def available():
    return bool(os.getenv("ANTHROPIC_API_KEY") or os.getenv("GEMINI_API_KEY"))


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

    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("Serve una chiave AI nel file .env: GEMINI_API_KEY (gratis su aistudio.google.com).")
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
