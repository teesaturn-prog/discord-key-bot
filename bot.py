
import os
import discord
import logging

from discord import app_commands
from database import generate_key, setup

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CandyHub")

TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN environment variable")


class KeyBot(discord.Client):

    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Initialize database
        setup()

        # Register slash commands
        await self.tree.sync()

        logger.info("Slash commands synced.")


bot = KeyBot()


@bot.event
async def on_ready():
    logger.info("Bot online: %s", bot.user)


@bot.tree.command(
    name="getkey",
    description="Generate a 24-hour Candy Hub key"
)
async def getkey(interaction: discord.Interaction):

    await interaction.response.defer(ephemeral=True)

    try:
        key = generate_key(interaction.user.id)

        await interaction.followup.send(
            f"**Your Candy Hub key:**\n"
            f"```{key}```\n"
            f"Expires in **24 hours**.\n\n"
            f"Keep this key private.",
            ephemeral=True
        )

    except Exception:
        logger.exception("Key generation failed")

        await interaction.followup.send(
            "Something went wrong generating your key. "
            "Please try again later.",
            ephemeral=True
        )


@bot.event
async def on_error(event, *args, **kwargs):
    logger.exception("Discord event error: %s", event)


bot.run(TOKEN)
