import discord
import logging

logger = logging.getLogger(__name__)

class CreateEventModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Create an event")

        self.add_item(discord.ui.TextDisplay(content="test"))

        self.add_item(discord.ui.TextInput(label="short",style=discord.TextStyle.short, placeholder="short placeholder"))
        self.add_item(discord.ui.TextInput(label="paragraph",style=discord.TextStyle.paragraph, placeholder="paragraph placeholder"))
