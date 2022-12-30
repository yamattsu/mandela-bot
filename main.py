#!/usr/bin/env python3
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from rich.console import Console

from musicbot import MusicBot

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

# Descrição de coisas

bot = commands.Bot(
    command_prefix="$", 
    description="A bot for play musics on call with friends",
    intents=intents
)
console = Console()

@bot.event
async def on_ready():
    console.print(
        f"[bold light_cyan3]\n{'>'*4} [/bold light_cyan3][bold medium_spring_green][+] {bot.user} is "
        "working![/bold medium_spring_green]\n"
    )
    await bot.add_cog(MusicBot(bot))

load_dotenv()
bot.run(os.getenv("DISCORD_API_TOKEN"))
