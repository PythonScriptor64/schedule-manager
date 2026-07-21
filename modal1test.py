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

