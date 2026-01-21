# src/bot/cogs/link.py
import logging
log = logging.getLogger(__name__)
from discord.ext import commands

from bot.services.minecraft import UsernameToUuid
from bot.storage.links_store import delete_link, get_link, is_user_linked, set_link


class Link(commands.Cog):
    """Commands for linking/unlinking Minecraft accounts (per server)."""

    def __init__(self, bot: commands.Bot) -> None:
        """Save the bot so we can use it later if needed."""
        self.bot = bot

    @commands.command(name="link")
    async def link(self, ctx: commands.Context, mc_user: str | None = None) -> None:
        """Link your Discord account to a Minecraft username."""
        if mc_user is None:
            await ctx.send("Usage: `!link <minecraft_username>`")
            return
        else:
            if ctx.guild is None:
                await ctx.send("Use this command in a server, not DMs.")
                return

            if is_user_linked(ctx.guild.id, ctx.author.id):
                await ctx.send("You're already linked here. Use `!unlink` first.")
                return

            try:
                mc_uuid, mc_name = await UsernameToUuid(mc_user)
            except ValueError as e:
                await ctx.send(f"❌ {e}")
                return

            set_link(
                guild_id=ctx.guild.id,
                discord_id=ctx.author.id,
                mc_uuid=mc_uuid,
                mc_name=mc_name,
                discord_user=ctx.author.name,
            )

            log.info(
                "link | guild=%s (%s) user=%s (%s) mc=%s (%s)",
                ctx.guild.name, ctx.guild.id,
                ctx.author.name, ctx.author.id,
                mc_name, mc_uuid
            )


            await ctx.send(f"✅ Linked you to **{mc_name}** (`{mc_uuid}`)")

    @commands.command(name="unlink")
    async def unlink(self, ctx: commands.Context) -> None:
        """Remove your link in this server."""
        if ctx.guild is None:
            await ctx.send("Use this command in a server, not DMs.")
            return

        deleted = delete_link(ctx.guild.id, ctx.author.id)
        if deleted is None:
            await ctx.send("You're not linked in this server.")
            return
        
        log.info(
            "unlink | guild=%s (%s) user=%s (%s) mc=%s (%s)",
            ctx.guild.name, ctx.guild.id,
            ctx.author.name, ctx.author.id,
            deleted["mc_name"], deleted["mc_uuid"]
        )

        await ctx.send(f"✅ Unlinked from **{deleted['mc_name']}**")

    @commands.command(name="whoami")
    async def whoami(self, ctx: commands.Context) -> None:
        """Show what Minecraft account you're linked to in this server."""
        if ctx.guild is None:
            await ctx.send("Use this command in a server, not DMs.")
            return

        acc = get_link(ctx.guild.id, ctx.author.id)
        if acc is None:
            await ctx.send("You're not linked. Use `!link <username>`")
            return

        await ctx.send(f"You are **{acc['mc_name']}** (`{acc['mc_uuid']}`)")


async def setup(bot: commands.Bot) -> None:
    """Called when the cog is loaded."""
    await bot.add_cog(Link(bot))
