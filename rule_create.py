import discord
import logging

logger = logging.getLogger(__name__)

class TestModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="test modal")
        self.add_item(
            discord.ui.TextInput(
                label="new modal stuff",
                default="2u358ghr9eiufsdjnk d",
                style=discord.TextStyle.short
            )
        )

    
class RuleCreateModal(discord.ui.Modal):
    def __init__(self, command_interaction: discord.Interaction):
        super().__init__(title="Create a rule")

        self.add_item(
            discord.ui.TextInput(
                label="Title",
                placeholder="Rule Title",
                style=discord.TextStyle.short,
            )
        )
        self.add_item(
            discord.ui.TextInput(
                label="Description",
                placeholder="Rule Description",
                style=discord.TextStyle.long,
            )
        )
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("on submit")

    