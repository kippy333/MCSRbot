import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

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
