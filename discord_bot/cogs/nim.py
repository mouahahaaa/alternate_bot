import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ui, slash_command

class NimView(ui.View):
    def __init__(self, current_sticks: int):
        super().__init__(timeout=None)
        self.current_sticks = current_sticks

    @ui.button(label="Prendre 1", style=nextcord.ButtonStyle.primary)
    async def take_1(self, button: ui.Button, interaction: Interaction):
        await self.handle_turn(interaction, 1)

    @ui.button(label="Prendre 2", style=nextcord.ButtonStyle.primary)
    async def take_2(self, button: ui.Button, interaction: Interaction):
        await self.handle_turn(interaction, 2)

    @ui.button(label="Prendre 3", style=nextcord.ButtonStyle.primary)
    async def take_3(self, button: ui.Button, interaction: Interaction):
        await self.handle_turn(interaction, 3)

    async def handle_turn(self, interaction: Interaction, taken: int):
        if taken > self.current_sticks:
            await interaction.response.send_message(
                f"Tu ne peux pas prendre {taken}, il n'en reste que {self.current_sticks}.", ephemeral=True)
            return

        self.current_sticks -= taken
        if self.current_sticks == 0:
            await interaction.response.edit_message(
                content="Bravo, tu as gagné ! 🎉",
                embed=None,
                view=None)
            return

        # Tour IA (simple random)
        import random
        ai_take = min(random.randint(1, 3), self.current_sticks)
        self.current_sticks -= ai_take

        if self.current_sticks == 0:
            await interaction.response.edit_message(
                content=f"Tu as pris {taken}. L'IA prend {ai_take} et gagne... 😢",
                embed=None,
                view=None)
            return

        # Sinon on met à jour l'embed et laisse le jeu continuer
        embed = nextcord.Embed(
            title="Jeu Nim",
            description=f"Tu as pris {taken} bâtonnets.\n"
                        f"L'IA a pris {ai_take} bâtonnets.\n"
                        f"Il reste maintenant {self.current_sticks} bâtonnets.",
            color=0x00FF00
        )
        await interaction.response.edit_message(embed=embed, view=self)

class NimCog(commands.Cog):
    def setup(self, bot: commands.Bot):
        self._bot = bot

    @slash_command()
    async def nim(self, ctx):
        starting_sticks = 15
        embed = nextcord.Embed(
            title="Jeu Nim",
            description=f"Il y a {starting_sticks} bâtonnets.\nPrends entre 1 et 3 bâtonnets en cliquant sur un bouton.",
            color=0x00FF00
        )
        view = NimView(starting_sticks)
        await ctx.send(embed=embed, view=view)

