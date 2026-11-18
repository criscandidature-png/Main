"""Sincronizzazione con Notion: Max salva to-do, note, promemoria e diario in un database.

Al primo avvio crea da solo il database "🧑‍💼 Max" dentro la pagina NOTION_PAGE_ID.
"""
import os, re
from datetime import datetime
import httpx
from pcbot import storage

API = "https://api.notion.com/v1"
TYPES = {"todo": "To-do", "notes": "Nota", "reminders": "Promemoria", "log": "Diario", "post": "Post social"}


def enabled():
    return bool(os.getenv("NOTION_TOKEN") and os.getenv("NOTION_PAGE_ID"))


def _client():
    return httpx.AsyncClient(base_url=API, timeout=20, headers={
        "Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
        "Notion-Version": "2022-06-28"})


def _page_id():
    raw = os.environ["NOTION_PAGE_ID"]
    m = re.search(r"([0-9a-f]{32})$", raw.split("?")[0].split("#")[0].replace("-", ""))
    return m[1] if m else raw


async def _req(method, path, **kw):
    async with _client() as c:
        r = await c.request(method, path, **kw)
        if r.status_code >= 400:
            raise RuntimeError(f"Notion {r.status_code}: {r.json().get('message', r.text)}")
        return r.json()


async def db_id():
    cfg = storage.load("notion", {})
    if cfg.get("db"):
        return cfg["db"]
    db = await _req("POST", "/databases", json={
        "parent": {"type": "page_id", "page_id": _page_id()},
        "title": [{"text": {"content": "🧑‍💼 Max"}}],
        "properties": {
            "Nome": {"title": {}},
            "Tipo": {"select": {"options": [{"name": v} for v in TYPES.values()]}},
            "Fatto": {"checkbox": {}},
            "Data": {"date": {}},
        }})
    storage.save("notion", {"db": db["id"]})
    return db["id"]


async def add(kind, text, when: datetime | None = None, body: str | None = None):
    props = {"Nome": {"title": [{"text": {"content": text[:2000]}}]},
             "Tipo": {"select": {"name": TYPES[kind]}},
             "Data": {"date": {"start": (when or datetime.now()).astimezone().isoformat()}}}
    payload = {"parent": {"database_id": await db_id()}, "properties": props}
    if body:
        payload["children"] = [{"paragraph": {"rich_text": [{"text": {"content": body[i:i + 2000]}}]}}
                               for i in range(0, min(len(body), 20000), 2000)]
    return (await _req("POST", "/pages", json=payload))["id"]


async def items(kind):
    """Elementi aperti (non fatti) di un tipo: lista di (page_id, testo)."""
    res = await _req("POST", f"/databases/{await db_id()}/query", json={
        "filter": {"and": [{"property": "Tipo", "select": {"equals": TYPES[kind]}},
                           {"property": "Fatto", "checkbox": {"equals": False}}]},
        "sorts": [{"property": "Data", "direction": "ascending"}], "page_size": 100})
    return [(p["id"], "".join(t["plain_text"] for t in p["properties"]["Nome"]["title"]))
            for p in res["results"]]


async def done(page_id):
    await _req("PATCH", f"/pages/{page_id}", json={"properties": {"Fatto": {"checkbox": True}}})


async def remove(page_id):
    await _req("PATCH", f"/pages/{page_id}", json={"archived": True})
