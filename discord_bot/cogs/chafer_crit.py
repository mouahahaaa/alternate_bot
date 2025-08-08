import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ui, slash_command
import random
import asyncio

ARAKNE_NORMAL_IMAGE = "https://static.ankama.com/dofus-touch/www/game/monsters/200/52.w200h.png"
ARAKNE_CRIT_IMG = "https://static.ankama.com/dofus-touch/www/game/monsters/200/259.w200h.png"
WIN_IMG = "https://static.ankama.com/upload/backoffice/direct/2024-11-18/44f496a3a4279d0f4fd9bc5641e56690.jpg"

class AraKritView(ui.View):
    def __init__(self, player1: nextcord.Member, player2: nextcord.Member):
        super().__init__(timeout=None)
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.player1_crit = False
        self.game_over = False
        self.lap = 1
        self.crit = None

    @ui.button(label=f"Invoquer", style=nextcord.ButtonStyle.green)
    async def invoke(self, button: ui.Button, interaction: Interaction):
        if interaction.user != self.current_player:
            await interaction.response.send_message("Ce n'est pas ton tour !", ephemeral=True)
            return

        button.disabled = True
        await interaction.response.edit_message(view=self)
        embed = nextcord.Embed(title=f"{self.player1.display_name} vs {self.player2.display_name} - Tour {self.lap}", color=0xFF0000)

        if self.crit is not None:
            if self.crit:
                embed.set_thumbnail(url=ARAKNE_CRIT_IMG)
            else:
                embed.set_thumbnail(url=ARAKNE_NORMAL_IMAGE)

        await interaction.edit_original_message(embed=embed, view=self)

        await asyncio.sleep(1)

        self.crit = random.random() < 0.25
        if self.crit:
            image = ARAKNE_CRIT_IMG
        else:
            image = ARAKNE_NORMAL_IMAGE

        embed.set_image(url=image)
        await interaction.edit_original_message(embed=embed, view=self)

        if self.current_player == self.player1:
            if self.crit:
                self.player1_crit = True
                # Check if player 2 crits
                self.current_player = self.player2
                embed.description = (
                    f"C'est à {self.player2.mention} d'invoquer..."
                )
                button.disabled = False
            else:
                self.current_player = self.player2
                embed.description = (
                    f"C'est à {self.player2.mention} d'invoquer..."
                )
                button.disabled = False

        else:
            if self.crit and not self.player1_crit:
                # Player 2 wins
                embed.title = f"🏆 {self.player2.display_name} gagne !"
                embed.color = 0xFFFF00
                button.disabled = True
                self.game_over = True
            else:
                if self.player1_crit:
                    # If player 1 crit previously, then player 1 wins
                    embed.title = f"🏆 {self.player1.display_name} gagne !"
                    embed.color = 0xFFFF00
                    button.disabled = True
                    self.game_over = True
                else:
                    # Go back to player 1
                    self.current_player = self.player1
                embed.description = (
                    f"C'est à {self.player1.mention} d'invoquer..."
                )
                button.disabled = False
                self.lap += 1

        if self.game_over:
            await asyncio.sleep(2)
            embed.set_image(url=WIN_IMG)
            embed.set_thumbnail(url=None)
            embed.description = ""
            self.remove_item(button)

        await interaction.edit_original_message(embed=embed, view=self)

class AraKritCog(commands.Cog):
    def setup(self, bot: commands.Bot):
        self._bot = bot

    @slash_command()
    async def arakrit(self, interaction: nextcord.Interaction, player2: nextcord.Member):
        if player2 == interaction.user:
            await interaction.response.send_message("Tu ne peux pas jouer contre toi-même.")
            return

        await interaction.response.send_message(f"{player2.mention}, tu as été défié par {interaction.user.mention} !")

        embed = nextcord.Embed(
            title="AraKrit",
            description=f"{interaction.user.mention} vs {player2.mention}\nC'est à {interaction.user.mention} d'invoquer...",
            color=0x00FF00
        )
        view = AraKritView(interaction.user, player2)
        await interaction.followup.send(embed=embed, view=view)

