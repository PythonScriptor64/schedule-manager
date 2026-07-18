import discord
import logging
import db_manager
import schedule_view
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

class CourseSelectView(discord.ui.LayoutView):
    def __init__(self, command_interaction: discord.Interaction):
        self.command_interaction = command_interaction
        self.selected_classes = { i: None for i in range(1,7) }
        super().__init__(timeout=180)
        container = discord.ui.Container(accent_color=discord.Color.blurple())
        container.add_item(
            discord.ui.TextDisplay(content="## Select the courses you have\n-# Leave a slot blank to keep existing selection")
        )

        for period in range(1,7):
            period_dropdown_ar = discord.ui.ActionRow()
            period_dropdown_ar.add_item(PeriodDropdown(self, period))
            container.add_item(period_dropdown_ar)

        save_button_ar = discord.ui.ActionRow(SaveButton(self))
        container.add_item(save_button_ar)
        self.add_item(container)
    
    def select_class(self, period: int, class_value: str):
        self.selected_classes[period] = class_value

    def save_classes(self):
        db_manager.save_user_schedule(self.selected_classes, self.command_interaction.user.id)


class PeriodDropdown(discord.ui.Select):
    def __init__(self, parent_view: CourseSelectView, period: int):
        super().__init__(options=options,placeholder=f"Period {period}")
        self.period = period
        self.parent_view = parent_view

    async def callback(self, interaction):
        self.parent_view.select_class(self.period, self.values[0])
        await interaction.response.defer()

class SaveButton(discord.ui.Button):
    def __init__(self, parent_view: CourseSelectView):
        super().__init__(
            label="Save",
            style=discord.ButtonStyle.success,
            custom_id="save_button"
        )
        self.parent_view = parent_view
    
    async def callback(self, interaction):
        self.parent_view.save_classes()
        await interaction.response.send_message(
            ephemeral=True,
            view=schedule_view.ScheduleView(
                schedule=self.parent_view.selected_classes,
                message="# Saved schedule successfully!"
            )
        )

