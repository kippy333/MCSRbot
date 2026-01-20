from discord.ext import commands

from bot.storage.links_store import Store_Link
from bot.services.minecraft import UsernameToUuid

class Link(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="link")
    async def link(self, ctx: commands.Context, MCUser: str) -> None:
        try:
            mc_uuid, mc_name = await UsernameToUuid(MCUser)
            Store_Link(mc_uuid, mc_name, ctx.author.id, ctx.author.name)
            await ctx.send(f"✅ Linked you to **{mc_name}**")
        except ValueError as e:
            await ctx.send(f"❌ {e}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Link(bot))
