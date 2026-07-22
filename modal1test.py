import discord
import logging
import json

logger = logging.getLogger(__name__)

try:
    with open("courses.json","r") as courses_json_f:
        courses = json.load(courses_json_f)
except (FileNotFoundError, json.JSONDecodeError):
    logger.error("courses.json is missing or invalid")
    courses = {None: {"name":"courses.json is missing or damaged, contact an administrator"}}

options = []
for course in courses:
    options.append(discord.SelectOption(label=f"{courses[course].get('name', course)}", value=f"{course}"))


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

        self.add_item(discord.ui.Label(text="yo this is label", component=discord.ui.Select(options=options)))

        # self.add_item(discord.ui.Label(text="this is the label text", component=discord.TextInput()))

        self.add_item(discord.ui.TextInput(label="short",style=discord.TextStyle.short, placeholder="short placeholder"))

        self.add_item(discord.ui.TextInput(label="long",style=discord.TextStyle.long, placeholder="long placeholder"))

        self.add_item(discord.ui.TextInput(label="paragraph",style=discord.TextStyle.paragraph, placeholder="paragraph placeholder"))
