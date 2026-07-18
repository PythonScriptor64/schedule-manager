import discord
import json

try:
    with open("courses.json","r") as courses_json_f:
        courses = json.load(courses_json_f)

except (FileNotFoundError, json.JSONDecodeError):
    courses = {}

def format_schedule(schedule: dict[int, str | None]):
    output = []
    for period in range(1,7):
        course_id = schedule.get(period, None)
        if not course_id:
            output.append(f"## Per. {period}) - __Course Not Set__")
            continue

        course = courses.get(course_id, {})
        course_name = course.get("name", None)

        if not course_name:
            output.append(f"## Per. {period}) - __Unresolvable Course ID__: `{course_id}`")
            continue

        output.append(f"## Per. {period}) - __{course_name}__")

    return "\n".join(output)

class ScheduleView(discord.ui.LayoutView):
    def __init__(self, schedule: dict[int, str | None], message: str):
        super().__init__()
        container = discord.ui.Container(accent_color=discord.Color.blurple())
        container.add_item(
            discord.ui.TextDisplay(
                content=message
            )
        )
        container.add_item(
            discord.ui.Separator(spacing=discord.SeparatorSpacing.small)
        )

        container.add_item(
            discord.ui.TextDisplay(
                content=format_schedule(schedule=schedule)
            )
        )

        self.add_item(container)
