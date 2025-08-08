from nextcord.ext import commands

class BaseCog(commands.Cog):
    def setup(self, bot: commands.Bot):
        self._bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong !")