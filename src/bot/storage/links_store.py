import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "links.json"

def load_db() -> dict:
    """Load the JSON DB into a dict. Returns {} if missing/empty."""
    if not DATA_PATH.exists():
        return {}

    try:
        with DATA_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        # File exists but is corrupted/empty
        return {}
    except OSError:
        return {}

def save_db(db: dict) -> None:
    """Write the dict DB back to the JSON file."""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def is_user_linked(discord_id: int) -> bool:
    db = load_db()
    return str(discord_id) in db


def get_link(discord_id: int):
    db = load_db()
    return db.get(str(discord_id))


def set_link(discord_id: int, mc_uuid: str, mc_name: str, discord_user: str) -> None:
    db = load_db()
    db[str(discord_id)] = {
        "mc_uuid": mc_uuid,
        "mc_name": mc_name,
        "discord_user": discord_user,
    }
    save_db(db)


def delete_link(discord_id: int) -> dict | None:
    db = load_db()
    key = str(discord_id)
    record = db.pop(key, None)
    if record is not None:
        save_db(db)
    return record
