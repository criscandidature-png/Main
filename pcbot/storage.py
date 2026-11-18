"""Piccolo archivio JSON per note, todo e promemoria."""
import json, os, threading
from pathlib import Path

DATA = Path(os.getenv("DATA_DIR", "data"))
DATA.mkdir(exist_ok=True)
_lock = threading.Lock()


def load(name, default):
    f = DATA / f"{name}.json"
    return json.loads(f.read_text("utf-8")) if f.exists() else default


def save(name, obj):
    with _lock:
        (DATA / f"{name}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=2), "utf-8")
