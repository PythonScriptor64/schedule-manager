import discord


class ModalTest(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="submit an event")

        # container = discord.ui.Container(accent_color=discord.Color.blurple())

        # container.add_item(
        #     discord.ui.TextDisplay(
        #         content="yo wasup"
        #     )
        # )

        # self.add_item(container)

        self.add_item(discord.ui.TextDisplay(content="test"))

