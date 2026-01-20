import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "links.json"

def Store_Link(mc_uuid: str, mc_name: str, discord_id: int, discord_user: str) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Load existing DB (or start empty)
    if DATA_PATH.exists():
        with DATA_PATH.open("r", encoding="utf-8") as f:
            db = json.load(f)
    else:
        db = {}

    # Upsert this user
    db[str(discord_id)] = {
        "mc_uuid": mc_uuid,
        "mc_name": mc_name,
        "discord_user": discord_user
    }

    # Save back
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)
