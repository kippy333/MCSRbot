from discord.ext import commands

from bot.storage.links_store import is_user_linked, set_link, delete_link, get_link
from bot.services.minecraft import UsernameToUuid

class Link(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="link")
    async def link(self, ctx: commands.Context, mc_user: str) -> None:
        if is_user_linked(ctx.author.id):
            await ctx.send("You are already linked to an account. Use `!unlink` first")
            return

        try:
            mc_uuid, mc_name = await UsernameToUuid(mc_user)
        except ValueError as e:
            await ctx.send(f"X {e}")
            return

        set_link(
            discord_id=ctx.author.id,
            mc_uuid=mc_uuid,
            mc_name=mc_name,
            discord_user=ctx.author.name,
        )

        await ctx.send(f"Done! Linked you to **{mc_name}** (`{mc_uuid}`)")

    @commands.command(name="unlink")
    async def unlink(self, ctx: commands.Context) -> None:
        deleted = delete_link(ctx.author.id)
        if deleted is None:
            await ctx.send(f"Error Unlinking to Account {deleted['mc_name']}")
        else:
            await ctx.send(f"Unlinked to minecraft account: {deleted['mc_name']}")

    @commands.command(name="whoami")
    async def whoami(self, ctx: commands.Context) -> None:
        acc = get_link(ctx.author.id)
        if acc is None:
           await ctx.send(f"You are not linked! Refer to !link <username>")
        else:
            await ctx.send(f"You are **{acc['mc_name']}** (`{acc['mc_uuid']}`)")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Link(bot))
