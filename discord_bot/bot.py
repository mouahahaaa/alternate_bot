import nextcord
from nextcord.ext import commands
from logging import Logger

class Bot(commands.Bot):
    def __init__(self, cogs: list[commands.Cog], logger: Logger):
        intents = nextcord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self._logger = logger
        for cog in cogs:
            self._add_cog(cog)

    def _add_cog(self, cog: commands.Cog):
        cog.setup(self)
        self.add_cog(cog)

    async def on_ready(self):
        self._logger.info(f"Connected as {self.user} (ID: {self.user.id})")

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Commande inconnue. Tape !help pour afficher la liste des commandes!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("La commande est incomplète!")
        else:
            self._logger.error(f"Error in command {ctx.command}: {error}")
            await ctx.send("Une erreur est survenue...")

    async def close(self):
        self._logger.info("Bot closed successfully.")
        await super().close()