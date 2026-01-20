from discord.ext import commands

class Ranked(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send("pong")

    @commands.command(name="auth")
    async def auth(self, ctx: commands.Context) -> None:
        await ctx.send(str(ctx.author.id) + " " + str(ctx.author.name))

    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ranked(bot))
