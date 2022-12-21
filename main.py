#!/usr/bin/env python3

import discord
import os
import youtube_dl
from discord.ext import commands
from dotenv import load_dotenv
from time import sleep
import asyncio

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

voice_clients = {}

yt_dl_opts = {"format": "bestaudio/best"}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_opts = {"options": "-vn"}

@bot.event
async def on_ready():
    print(f"[+] {bot.user} is working!")

@bot.command(pass_context=True)
async def play(ctx):
    try:
        voice_channel = ctx.author.voice
        channel = None
        if voice_channel != None:
            await ctx.send(f"Você está em um canal de voz! {voice_channel.channel.name}")
            # channel = voice_channel.name
            vc = await voice_channel.channel.connect()
#            print(voice_channel)
#            vc.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source="override.mp3"))

            vc.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source="./endoftheworld.mp3"))

            while vc.is_playing():
                await asyncio.sleep(1)

            vc.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source="./littledarkage.mp3"))

            while vc.is_playing():
                await asyncio.sleep(1)

            await vc.disconnect()

        else:
            await ctx.send(f"{ctx.author.name}, você não está em um canal de voz!")


    except Exception as err:
        print(err)

load_dotenv()
bot.run(os.getenv("TOKEN"))
