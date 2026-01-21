import json
from pathlib import Path

# Where we store linked accounts
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "links.json"


def load_db() -> dict:
    """Read links.json and return it as a dict. If missing/broken, return {}."""
    if not DATA_PATH.exists():
        return {}

    try:
        with DATA_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_db(db: dict) -> None:
    """Save the dict back into links.json."""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def is_user_linked(guild_id: int, discord_id: int) -> bool:
    """Check if a user is linked in this server."""
    db = load_db()
    guild_bucket = db.get(str(guild_id), {})
    return isinstance(guild_bucket, dict) and str(discord_id) in guild_bucket


def get_link(guild_id: int, discord_id: int) -> dict | None:
    """Get the saved link for a user in this server (or None)."""
    db = load_db()
    return db.get(str(guild_id), {}).get(str(discord_id))


def set_link(guild_id: int, discord_id: int, mc_uuid: str, mc_name: str, discord_user: str) -> None:
    """Add/update a user's link in this server."""
    db = load_db()
    gkey = str(guild_id)
    ukey = str(discord_id)

    db.setdefault(gkey, {})
    db[gkey][ukey] = {
        "mc_uuid": mc_uuid,
        "mc_name": mc_name,
        "discord_user": discord_user,
    }
    save_db(db)


def delete_link(guild_id: int, discord_id: int) -> dict | None:
    """Remove a user's link in this server and return what was removed."""
    db = load_db()
    gkey = str(guild_id)
    ukey = str(discord_id)

    guild_bucket = db.get(gkey)
    if not isinstance(guild_bucket, dict):
        return None

    record = guild_bucket.pop(ukey, None)

    if record is not None:
        # if the server has no links left, remove the server key
        if not guild_bucket:
            db.pop(gkey, None)
        save_db(db)

    return record