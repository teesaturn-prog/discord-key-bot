
import os
import discord
from discord import app_commands
from database import generate_key, setup

TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN")

class KeyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = KeyBot()

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

@bot.tree.command(
    name="getkey",
    description="Generate a 24-hour key"
)
async def getkey(interaction: discord.Interaction):
    key = generate_key(interaction.user.id)

    await interaction.response.send_message(
        f"Your key:\n`{key}`\n\nExpires in 24 hours.",
        ephemeral=True
    )

bot.run(TOKEN)
