import logging
from discord.ext import commands, tasks

log = logging.getLogger(__name__)

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.poller.start()

    def cog_unload(self) -> None:
        self.poller.cancel()

    @tasks.loop(seconds=15)
    async def poller(self) -> None:
        # later: poll MCSR Ranked API for tracked users
        pass

    @poller.before_loop
    async def before_poller(self) -> None:
        await self.bot.wait_until_ready()
        log.info("Poller started")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
