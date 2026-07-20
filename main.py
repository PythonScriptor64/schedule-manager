import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import sys
import time
import asyncio
import logging
from datetime import datetime
import course_select
import db_manager
import schedule_view
import config
import modal1test

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
start_time = datetime.now()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s; %(filename)s; %(funcName)s(); %(levelname)s: %(message)s"    
)
logger = logging.getLogger(__name__)

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        logger.debug("Bot initializing")
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        logger.debug("Running setup hook")
        if config.SYNC_COMMANDS_ON_STARTUP:
            logger.debug("Creating task to sync slash commands")
            asyncio.create_task(self.sync_commands())
        else:
            logger.debug("Sync commands on startup is disabled; will not sync slash commands.")

    async def on_ready(self):
        logger.info(f"Logged in as '{self.user}'")

    async def sync_commands(self):
        try:
            commands = await self.tree.sync()
            logger.info(f"Finished syncing slash commands; Synced {len(commands)} command(s)")
            return commands
        except Exception:
            logger.exception(f"Slash commands failed to sync;")
            return None

intents = discord.Intents.default()
intents.message_content = True
client = Bot(intents=intents, command_prefix=[]) # NEVER USE @bot.command, THE COMMAND PREFIX SHOULD REMAIN UNUSED UNLESS FOR TESTING

async def guild_only_check(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("Commands may only be used in a guild.", ephemeral=True)
        return False
    else:
        return True
client.tree.interaction_check = guild_only_check

@client.tree.command(description="Register your schedule with the database")
async def setschedule(interaction: discord.Interaction):
    logger.debug(f"/setschedule ran by '{interaction.user}'")
    await interaction.response.send_message(view=course_select.CourseSelectView(interaction), ephemeral=True)

@client.tree.command(description="Fetch a user's schedule")
async def fetchschedule(interaction: discord.Interaction, user: discord.User | None = None): # = None and the two types allow for the field to be left blank
    logger.debug(f"/fetchschedule ran by '{interaction.user}' targeting '{user}'")
    target_user_id = user.id if user else interaction.user.id
    await interaction.response.send_message(
        ephemeral=False,
        allowed_mentions=discord.AllowedMentions.none(),
        view=schedule_view.ScheduleView(
            db_manager.fetch_user_schedule(user_id=target_user_id),
            message=f"# <@{target_user_id}>'s Schedule"
        )
    )

@client.tree.command(description="Create and submit an event proposal")
async def registerevent(interaction: discord.Interaction):
    await interaction.response.send_modal(modal1test.ModalTest())

@client.tree.command(description="Syncs commands from bot; development use only")
async def sync(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.defer(thinking=True)
        sync_result = await client.sync_commands()
        if sync_result == None:
            await interaction.followup.send("Syncing commands failed!")
        else:
            await interaction.followup.send(f"Finished syncing slash commands; Synced {len(sync_result)} command(s)")
    else:
        await interaction.response.send_message("This command may only be run by administrators.")

@client.tree.command(description="Causes bot to exit; parent should restart the bot process")
async def restart(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        logger.info(f"Bot restart requested by '{interaction.user}' via /restart")
        await interaction.response.send_message("Safely closing database connection...")
        logger.info("Attempting to cleanup database connection")
        await asyncio.to_thread(db_manager.cleanup)
        await interaction.followup.send("Exiting!")
        logger.info("Closing client")
        await client.close()
    else:
        logger.info(f"User '{interaction.user}' lacks permission to restart bot")
        await interaction.response.send_message("This command may only be run by administrators.")

@client.tree.command(description="Check bot status")
async def status(interaction: discord.Interaction):
    logger.debug(f"/status ran by '{interaction.user}'")
    await interaction.response.send_message(f"uptime: {datetime.now() - start_time}") # improve this shit later

@client.tree.command(description="test if schedule select looks better as a modal")
async def schedulemodal(interaction: discord.Interaction): # DELETE THIS SHIT LATER
    await interaction.response.send_modal(__import__("schedulemodaltest1").CourseSelectModal())

client.run(BOT_TOKEN)