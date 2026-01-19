import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# Also attempt to load token.env at the repository root (workspace convenience)
root_token = Path(__file__).resolve().parents[2] / "token.env"
if root_token.exists():
    load_dotenv(dotenv_path=str(root_token))

def _must(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing required env var: {name}")
    return val

@dataclass(frozen=True)
class Config:
    discord_token: str = _must("DISCORD_TOKEN")
    command_prefix: str = os.getenv("COMMAND_PREFIX", "!")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

config = Config()
