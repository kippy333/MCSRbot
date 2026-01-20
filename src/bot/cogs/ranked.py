from discord.ext import commands
from bot.services.mcsrranked import getStats
from bot.storage.links_store import is_user_linked, set_link, delete_link, get_link
from bot.services.mcsrranked import format_ms
import discord


class Ranked(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send("pong")

    @commands.command(name="auth")
    async def auth(self, ctx: commands.Context) -> None:
        await ctx.send(str(ctx.author.id) + " " + str(ctx.author.name))


    @commands.command(name="stats")
    async def stats(self, ctx: commands.Context, username: str | None = None) -> None:
        # Decide identifier
        if username is None:
            acc = get_link(ctx.author.id)
            if acc is None:
                await ctx.send("You are not linked. Use `!link <username>` first, or run `!stats <username>`.")
                return
            identifier = acc.get("mc_uuid") or acc.get("mc_name")
        else:
            identifier = username.strip()

        # Fetch stats
        try:
            nickname, elo_rank, weekly_races = await getStats(identifier)
        except ValueError as e:
            await ctx.send(f"❌ {e}")
            return

        # Build embed
        embed = discord.Embed(
            title="MCSR Ranked Stats",
            description=f"Stats for **{nickname}**",
        )
        embed.add_field(name="Elo Rank", value=str(elo_rank) if elo_rank is not None else "Unranked", inline=True)
        embed.add_field(name="Weekly Races", value=str(len(weekly_races)), inline=True)

        if weekly_races:
            best = min(weekly_races, key=lambda r: r.get("rank", 10**9))
            best_rank = best.get("rank")
            best_time = best.get("time")
            embed.add_field(
                name="Best Weekly Race",
                value=f"Rank: {best_rank if best_rank is not None else 'N/A'}\nTime: {format_ms(best_time)}",
                inline=False,
            )

        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ranked(bot))
            

        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ranked(bot))
