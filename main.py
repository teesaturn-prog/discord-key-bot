
import discord
from discord import app_commands
from discord.ext import commands
import secrets
import string
import time
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

keys = {}

def make_key():
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(24))

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is online as {bot.user}")

@bot.tree.command(name="getkey", description="Get your 24-hour key")
async def getkey(interaction: discord.Interaction):
    user_id = interaction.user.id
    key = make_key()

    keys[user_id] = {
        "key": key,
        "expires": time.time() + 86400
    }

    await interaction.response.send_message(
        "Your key has been sent to your DMs!",
        ephemeral=True
    )

    try:
        await interaction.user.send(
            f"🔑 **Here is your key!**\n\n"
            f"`{key}`\n\n"
            f"This key lasts **24 hours**. "
            f"After that, use `/getkey` to generate a new one."
        )
    except discord.Forbidden:
        await interaction.followup.send(
            "I couldn't DM you. Please allow messages from this server.",
            ephemeral=True
        )

bot.run(TOKEN)
