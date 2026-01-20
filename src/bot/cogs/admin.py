from discord.ext import commands
import logging

log = logging.getLogger(__name__)


class Admin(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

	@commands.command(name="echo")
	async def echo(self, ctx: commands.Context, *, message: str) -> None:
		"""Echo a message back to the channel (admin utility)."""
		await ctx.send(message)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Admin(bot))

