import discord
import logging
import json


logger = logging.Logger(__name__)

try:
    with open("courses.json","r") as courses_json_f:
        courses = json.load(courses_json_f)
except (FileNotFoundError, json.JSONDecodeError):
    logger.error("courses.json is missing or invalid")
    courses = {None: {"name":"courses.json is missing or damaged, contact an administrator"}}

options = []
for course in courses:
    options.append(discord.SelectOption(label=f"{courses[course].get('name', course)}", value=f"{course}"))


class CourseSelectModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="## Select your courses\n-# Leave a slot blank to keep existing selection")

        for period in range(1,7):
            period_dropdown_ar = discord.ui.ActionRow()
            period_dropdown_ar.add_item(PeriodDropdown(self, period))
            self.add_item(period_dropdown_ar)






class PeriodDropdown(discord.ui.Select):
    def __init__(self, parent_view: CourseSelectModal, period: int):
        super().__init__(options=options,placeholder=f"Period {period}")
        self.period = period
        self.parent_view = parent_view

    async def callback(self, interaction):
        self.parent_view.select_class(self.period, self.values[0])
        await interaction.response.defer()
