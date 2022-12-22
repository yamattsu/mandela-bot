#!/usr/bin/env python3

import discord
import os
import youtube_dl
from discord.ext import commands
from dotenv import load_dotenv
from time import sleep
from music_utils import get_musics
import asyncio

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"[+] {bot.user} is working!")

@bot.command(pass_context=True)
async def play(ctx):
    try:
        voice_channel = ctx.author.voice
        channel = None
        if voice_channel != None:
            await ctx.send(f"[+] Entrando no canal de voz e começando a reprodução da playlist!")
            vc = await voice_channel.channel.connect()
            musics = get_musics("./musics")

            #print(musics)

            for music in musics:
                await ctx.send(f"Reproduzindo: {music}")
                vc.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source=music))
                vc.source = discord.PCMVolumeTransformer(vc.source, 0.7)

                while vc.is_playing():
                    await asyncio.sleep(1)
            
            await ctx.send("[+] Playlist finalizada!")
            await vc.disconnect()

        else:
            await ctx.send(f"[+] {ctx.author.name}, você não está em um canal de voz!")


    except Exception as err:
        print(err)

load_dotenv()
bot.run(os.getenv("TOKEN"))
