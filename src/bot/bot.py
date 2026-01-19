import logging
import discord
from discord.ext import commands

log = logging.getLogger(__name__)

INITIAL_EXTENSIONS = (
    "bot.cogs.admin",
    "bot.cogs.ranked",
    "bot.cogs.events",
)

class MyBot(commands.Bot):
    def __init__(self, *, command_prefix: str) -> None:
        intents = discord.Intents.default()
        intents.message_content = True  # only if you need prefix commands reading message content
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self) -> None:
        for ext in INITIAL_EXTENSIONS:
            try:
                await self.load_extension(ext)
                log.info("Loaded extension: %s", ext)
            except Exception:
                log.exception("Failed to load extension: %s", ext)

    async def on_ready(self) -> None:
        log.info("Logged in as %s (id=%s)", self.user, self.user.id)
