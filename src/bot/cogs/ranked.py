from discord.ext import commands

class Ranked(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send("pong")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ranked(bot))
