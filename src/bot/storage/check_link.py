import json
from pathlib import Path
from typing import Any

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "links.json"

def is_user_linked(discord_id: int, path: Path) -> bool:
    """
    Return True if str(ctx.author.id) is a key in the JSON file (expected to be a dict).
    """
    p = Path(Path)
    if not p.exists():
        return False
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        print("Error")
        return False
    return isinstance(data, dict) and str(ctx.author.id) in data